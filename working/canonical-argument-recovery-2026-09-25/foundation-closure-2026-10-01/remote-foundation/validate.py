"""Validate the exact reviewed continuation; stage objects without moving main."""
from pathlib import Path, PurePosixPath
import base64
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import urllib.request

REPO = "EpiLogos/Antykathera-Essay-Work"
BASE = "fec057ae84cbebed9bd270271ae8798db6e5e879"
ROOT = Path.cwd()
BATCH = Path("working/canonical-argument-recovery-2026-09-25/foundation-closure-2026-10-01/remote-foundation")
OUT = Path(os.environ["RUNNER_TEMP"]) / "canonical-foundation-validation"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = json.loads((BATCH / "INPUTS.json").read_text())
RESULTS = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def safe(name):
    part = PurePosixPath(name)
    assert not part.is_absolute() and ".." not in part.parts, name
    path = ROOT / name
    assert not path.is_symlink() and path.resolve().is_relative_to(ROOT), name
    return path


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def run(args, name, required=True):
    with (OUT / name).open("w") as stream:
        result = subprocess.run(args, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    RESULTS[name] = {"command": args, "exit": result.returncode}
    print(name, result.returncode, flush=True)
    if required and result.returncode:
        raise RuntimeError(f"{name}: exit {result.returncode}; exact output retained")
    return result.returncode


def generated(name):
    ep = "submission-package/essay/symbolon/episteme/"
    return (name.startswith(ep + "maps/navigation/")
            or name in {ep + "sources/" + n for n in ("SOURCE-INDEX.md", "PASSAGE-LEDGER.md", "MAIN-SOURCES.md")}
            or name == "submission-package/essay/section-rooms/README.md"
            or bool(re.fullmatch(r"submission-package/essay/section-rooms/\d\d-[^/]+/ROOM\.md", name)))


def api(endpoint, value):
    request = urllib.request.Request(
        "https://api.github.com/repos/" + REPO + "/" + endpoint,
        data=json.dumps(value).encode(), method="POST",
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "Accept": "application/vnd.github+json", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)


assert os.environ["GITHUB_REPOSITORY"] == REPO
assert os.environ["GITHUB_REF"] == "refs/heads/canonical-foundation-2026-10-02"
head = git("rev-parse", "HEAD").decode().strip()
assert head == os.environ["GITHUB_SHA"]
assert not git("status", "--porcelain")
subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT, check=True)
records = MANIFEST["records"]
canon = {r["path"] for r in records}
assert len(records) == len(canon) == 68
assert not any("/movements/" in p or p.endswith("/THE-RETURN-OF-ZERO.md") or p.endswith(("/NOTES.md", "/HISTORY.md")) for p in canon)
for r in records:
    assert sha(git("show", BASE + ":" + r["path"])) == r["preimage_sha256"], r["path"]
    assert sha(safe(r["path"]).read_bytes()) == r["postimage_sha256"], r["path"]
proofs = MANIFEST["proofs"]
for r in proofs:
    assert sha(safe(r["path"]).read_bytes()) == r["sha256"], r["path"]
allowed_input = canon | {r["path"] for r in proofs} | set(MANIFEST["transport_paths"])
assert set(git("diff", "--name-only", BASE, "HEAD").decode().splitlines()) == allowed_input

protected = MANIFEST["protected"]
for r in protected:
    actual = os.readlink(ROOT / r["path"]).encode() if r["mode"] == "120000" else (ROOT / r["path"]).read_bytes()
    assert blob(actual) == r["base_blob"], r["path"]

spec = importlib.util.spec_from_file_location("recovery_audit", ROOT / "tools/audit-canonical-argument-recovery.py")
audit_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = audit_module
spec.loader.exec_module(audit_module)
public = sorted(p for p in canon if audit_module.is_public_argument_surface(Path(p)))
strict_args = ["python3", "tools/audit-canonical-argument-recovery.py", "--strict", "--json"]
for p in public:
    strict_args += ["--path", p]
run(strict_args, "strict.json")
run(["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_canonical_argument_recovery_audit.py", "-v"], "detector-tests.txt")
for builder in ("build-source-projections.py", "build-section-rooms.py", "build-navigation.py"):
    run(["python3", "tools/" + builder], builder + ".build.txt")
    run(["python3", "tools/" + builder, "--check"], builder + ".check.txt")

run(["python3", "tools/audit-reader-navigation.py", "--output", str(OUT / "reader-navigation.json")], "reader-navigation.stdout")
reader_report = json.loads((OUT / "reader-navigation.json").read_text())
old_reader = json.loads(git("show", BASE + ":submission-package/essay/symbolon/episteme/maps/navigation/reader-audit.json"))
old_problems = {(r["source"], r["href"], r["status"]) for r in old_reader["problems"]}
new_changed_problems = [r for r in reader_report["problems"] if r["source"] in canon and (r["source"], r["href"], r["status"]) not in old_problems]
(OUT / "changed-reader-problems.json").write_text(json.dumps(new_changed_problems, indent=2) + "\n")
assert not new_changed_problems, new_changed_problems
rooms = ("00-integral-threshold", "01-differentiating-mind", "02-return-of-zero", "03-two-logics", "04-mathematical-substrate", "05-psychoid-flowering", "06-objective-internality", "07-instrument-returns")
room_args = ["python3", "tools/audit-room-depth.py", "--project-root", ".", "--require-deepened"]
for room in rooms:
    room_args += ["--room", room]
run(room_args, "room-depth.txt")
run(["python3", "tools/audit-pre-manuscript.py", "--project-root", ".", "--output", str(OUT / "pre-manuscript.json")], "pre-manuscript.txt")
run(["python3", "tools/okf-workspace.py", "effects", "C41", "--depth", "4", "--json"], "effects-C41-after.json")
run(["python3", "tools/okf-workspace.py", "doctor", "--json"], "doctor.json")
doctor = json.loads((OUT / "doctor.json").read_text())
forbidden_source_kinds = {"duplicate-source-house", "duplicate-passage-id", "dangling-room-link", "dangling-room-fragment", "missing-passage-locator", "missing-passage-status", "missing-passage-provenance"}
source_failures = [r for r in doctor["debts"] if r["kind"] in forbidden_source_kinds]
assert not source_failures, source_failures
governing_dangles = [r for r in doctor["debts"] if r["kind"] == "unresolved-link" and r["authority"] == "governing"]
assert not governing_dangles, governing_dangles
missing_quality = {r["path"]: r["missing"] for r in doctor["quality_assessments"] if r["missing"]}
assert missing_quality == MANIFEST["deferred_quality_missing"], missing_quality

tracked = [p for p in git("ls-files", "-z").decode().split("\0") if p]
def snapshot():
    return {p: blob(os.readlink(ROOT / p).encode() if (ROOT / p).is_symlink() else (ROOT / p).read_bytes()) for p in tracked}
before_suite = snapshot()
suite_exit = run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], "full-suite.txt", False)
assert before_suite == snapshot(), "Frozen tracked files changed during full suite"
suite = (OUT / "full-suite.txt").read_text()
skip_lines = [line for line in suite.splitlines() if " ... skipped " in line]
expected_skip = "setUpClass (test_aikit_wiki_parity.AikitWikiParityTests) ... skipped 'aikit is not available; set AIKIT_BIN or put it on PATH'"
assert skip_lines == [expected_skip], skip_lines
if suite_exit:
    failures = re.findall(r"^FAIL: ([^\n]+)", suite, re.M)
    assert failures == ["test_canonical_graph_has_no_missing_quality_surfaces_or_governing_dangles (test_okf_workspace.OkfWorkspaceTests.test_canonical_graph_has_no_missing_quality_surfaces_or_governing_dangles)"], suite[-15000:]
    assert "FAILED (failures=1, skipped=1)" in suite and "Ran 132 tests" in suite
    failed_block = suite[suite.index("\nFAIL: "):]
    movement_paths = set(re.findall(r"submission-package/essay/section-rooms/[^\s'\"]+/movements/[^\s'\"]+\.md", failed_block))
    assert movement_paths == set(MANIFEST["deferred_failure_paths"]), movement_paths
    assert not re.search(r"^ERROR: ", suite, re.M)
run(["git", "diff", "--check"], "diff-check.txt")
generated_paths = sorted(p for p in git("diff", "--name-only").decode().splitlines() if p)
assert all(generated(p) for p in generated_paths), generated_paths
assert not git("ls-files", "--others", "--exclude-standard")
for r in records:
    assert sha(safe(r["path"]).read_bytes()) == r["postimage_sha256"], r["path"]
for r in protected:
    actual = os.readlink(ROOT / r["path"]).encode() if r["mode"] == "120000" else (ROOT / r["path"]).read_bytes()
    assert blob(actual) == r["base_blob"], r["path"]
strict = json.loads((OUT / "strict.json").read_text())
assert strict["files"] == len(public) and strict["errors"] == 0
receipt = {
    "status": "Validated native continuation candidate; main publication is separate",
    "source_parent": BASE, "execution_commit": head, "execution_root": str(ROOT),
    "authored_records": len(canon), "public_detector_records": len(public),
    "strict_errors": strict["errors"], "review_candidates": strict["review_candidates"],
    "checks": RESULTS, "full_suite_exit": suite_exit, "full_suite_tail": suite[-15000:],
    "native_skip": expected_skip,
    "AIKit_scope": "Executable unavailable on this Linux runner; unchanged native conditional. Earlier actual eight-test local run is separate evidence, not this candidate's AIKit acceptance.",
    "deferred_failures": MANIFEST["deferred_failure_paths"],
    "deferred_quality_missing": missing_quality, "governing_dangles": [],
    "protected_files": len(protected), "protected_changes": [],
    "generated_paths": generated_paths, "new_changed_reader_problems": [],
    "scope": "Exact independently reviewed complete source operations; no global semantic closure, deferred movement or sovereign-manuscript acceptance."}
(OUT / "INTEGRATION-VALIDATION.json").write_text(json.dumps(receipt, indent=2) + "\n")
evidence_paths = []
for p in sorted(OUT.iterdir()):
    name = str(BATCH / "integration-checks" / p.name)
    safe(name).parent.mkdir(parents=True, exist_ok=True)
    safe(name).write_bytes(p.read_bytes())
    evidence_paths.append(name)
paths = sorted(canon | set(generated_paths) | {r["path"] for r in proofs} | set(evidence_paths) | {str(BATCH / "INPUTS.json")})
entries = []
for name in paths:
    data = safe(name).read_bytes()
    already = subprocess.run(["git", "rev-parse", "HEAD:" + name], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    existing_sha = already.stdout.decode().strip() if already.returncode == 0 else None
    if existing_sha == blob(data):
        object_sha = existing_sha
    else:
        result = api("git/blobs", {"encoding": "base64", "content": base64.b64encode(data).decode()})
        assert result["sha"] == blob(data), name
        object_sha = result["sha"]
    entries.append({"path": name, "mode": "100644", "type": "blob", "sha": object_sha})
tree = api("git/trees", {"base_tree": git("rev-parse", BASE + "^{tree}").decode().strip(), "tree": entries})
result = {"source_parent": BASE, "execution_commit": head, "tree_sha": tree["sha"], "entries": entries, "receipt": receipt}
(OUT / "candidate-tree.json").write_text(json.dumps(result, indent=2) + "\n")
print("CANDIDATE_TREE=" + tree["sha"], flush=True)
