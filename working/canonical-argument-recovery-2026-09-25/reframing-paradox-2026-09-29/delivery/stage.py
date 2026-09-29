"""Validate retained reframing/paradox recovery; create a candidate tree, never publish refs."""
from pathlib import Path, PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import base64, gzip, hashlib, importlib.util, json, lzma, os, re, subprocess, sys, time, urllib.request
from urllib.error import HTTPError

REPO = "EpiLogos/Antykathera-Essay-Work"
ROOT = Path.cwd()
BATCH = "working/canonical-argument-recovery-2026-09-25/reframing-paradox-2026-09-29/"
OUT = Path(os.environ["RUNNER_TEMP"]) / "reframing-paradox-publication"
OUT.mkdir(parents=True, exist_ok=True)
PAYLOAD_SHA256 = "bb8ccc4c9c8d13a86d9003f0a51596f0bf8ad406b25bc1f6ca7f73aea2f88101"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def safe(name):
    part = PurePosixPath(name)
    assert not part.is_absolute() and ".." not in part.parts
    path = ROOT / name
    assert not path.is_symlink()
    assert path.resolve().is_relative_to(ROOT.resolve())
    return path


def run(args, name, required=True):
    with (OUT / name).open("w") as stream:
        result = subprocess.run(args, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    print(name, result.returncode, flush=True)
    if required and result.returncode:
        raise RuntimeError(f"{name}: exit {result.returncode}; retained output identifies the fault")
    return result.returncode


def generated(name):
    ep = "submission-package/essay/symbolon/episteme/"
    return (name.startswith(ep + "maps/navigation/")
        or name in {ep + "sources/" + n for n in ("SOURCE-INDEX.md", "PASSAGE-LEDGER.md", "MAIN-SOURCES.md")}
        or name == "submission-package/essay/section-rooms/README.md"
        or bool(re.fullmatch(r"submission-package/essay/section-rooms/\d\d-[^/]+/ROOM\.md", name)))


def api(endpoint, value):
    req = urllib.request.Request("https://api.github.com/repos/" + REPO + "/" + endpoint,
        data=json.dumps(value).encode(), method="POST",
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
            "Accept": "application/vnd.github+json", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in (500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep((2, 8, 20)[attempt])


assert os.environ["GITHUB_REPOSITORY"] == REPO
assert os.environ["GITHUB_REF"] == "refs/heads/main"
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
base_tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], text=True).strip()
assert head == os.environ["GITHUB_SHA"]
assert not subprocess.check_output(["git", "status", "--porcelain"])
parts = sorted(safe(BATCH + "delivery/parts").glob("*.xz.part"))
assert len(parts) == 7
packed = b"".join(part.read_bytes() for part in parts)
assert digest(packed) == PAYLOAD_SHA256
payload = json.loads(lzma.decompress(packed))
canon = {entry["path"] for entry in payload["files"]}
assert len(canon) == 6
assert all(name.startswith("submission-package/essay/symbolon/") for name in canon)
assert sum("/concepts/" in name for name in canon) == 2
assert sum("/sources/" in name for name in canon) == 1
assert sum("/arguments/" in name for name in canon) == 2
assert sum("/histories/" in name for name in canon) == 1
assert not any("/movements/" in name or name.endswith("/NOTES.md") for name in canon)
for identity in ("C52", "C64", "A21"):
    run(["python3", "tools/okf-workspace.py", "--project-root", ".", "effects", identity, "--depth", "4", "--json"], identity + "-effects-before.json")
originals = {}
postimages = {}
for entry in payload["files"]:
    name = entry["path"]
    original = safe(name).read_bytes()
    assert blob(original) == entry["before"], ("preimage changed", name)
    originals[name] = original
    text = original.decode()
    last = len(text) + 1
    for start, end, replacement in reversed(entry["edits"]):
        assert 0 <= start <= end < last
        text = text[:start] + replacement + text[end:]
        last = start
    data = text.encode()
    assert blob(data) == entry["after"], ("postimage changed", name)
    postimages[name] = data
for name, data in postimages.items():
    safe(name).write_bytes(data)
for source in payload["source_hashes"]:
    assert digest(safe(source["path"]).read_bytes()) == source["sha256"], ("source changed", source["path"])
seen = set(canon)
for name, text in payload["evidence"].items():
    assert name.startswith(BATCH) and "/delivery/" not in name
    path = safe(name)
    assert not path.exists(), ("evidence already exists", name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    seen.add(name)
for name, data in originals.items():
    destination = BATCH + "integration-preimages/" + name + ".gz"
    path = safe(destination)
    assert not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(gzip.compress(data, mtime=0))
    seen.add(destination)
public = sorted(name for name in canon if "/sources/" not in name)
args = ["python3", "tools/audit-canonical-argument-recovery.py", "--strict", "--json"]
for name in public:
    args += ["--path", name]
run(args, "strict.json")
run(["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_canonical_argument_recovery_audit.py", "-v"], "detector-tests.txt")
for builder in ("build-source-projections.py", "build-section-rooms.py", "build-navigation.py"):
    run(["python3", "tools/" + builder], builder + ".build.txt")
    run(["python3", "tools/" + builder, "--check"], builder + ".check.txt")
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("reader_audit", ROOT / "tools/audit-reader-navigation.py")
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
audit = reader.ReaderAudit(ROOT)
checks = []
for name in sorted(canon):
    for link in reader.links(safe(name).read_text()):
        target, status = audit.resolve(name, link)
        assert "missing" not in status and "unresolved" not in status, (name, link, status)
        checks.append({"source": name, "href": link["href"], "status": status})
(OUT / "links.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")
rooms = ("00-integral-threshold", "01-differentiating-mind", "02-return-of-zero", "03-two-logics", "04-mathematical-substrate", "05-psychoid-flowering", "06-objective-internality", "07-instrument-returns")
args = ["python3", "tools/audit-room-depth.py", "--project-root", ".", "--require-deepened"]
for room in rooms:
    args += ["--room", room]
run(args, "room-depth.txt")
run(["python3", "tools/audit-pre-manuscript.py", "--project-root", ".", "--output", str(OUT / "pre-manuscript.json")], "pre-manuscript.txt")
tracked = [p for p in subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0") if p]
def snapshot():
    return {p: digest(safe(p).read_bytes()) for p in tracked if (ROOT/p).is_file() and not (ROOT/p).is_symlink()}
before_suite = snapshot()
suite_exit = run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], "full-suite.txt", False)
assert before_suite == snapshot(), "tracked files changed during frozen full suite"
suite = (OUT / "full-suite.txt").read_text()
if suite_exit:
    assert "Ran 132 tests" in suite and "FAILED (failures=1, skipped=1)" in suite, suite[-10000:]
    assert len(re.findall(r"^FAIL: ", suite, re.M)) == 1
    assert "FAIL: test_canonical_graph_has_no_missing_quality_surfaces_or_governing_dangles" in suite
run(["git", "diff", "--check"], "diff-check.txt")
changed = subprocess.check_output(["git", "diff", "--name-only", "-z"]).decode().split("\0")
added = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard", "-z"]).decode().split("\0")
paths = sorted(set(p for p in changed + added if p))
assert all(p in seen or generated(p) for p in paths), paths
assert not any("/movements/" in p or p.endswith("/THE-RETURN-OF-ZERO.md") for p in paths)
for name, data in postimages.items():
    assert safe(name).read_bytes() == data
strict = json.loads((OUT / "strict.json").read_text())
local_review = json.loads(payload["evidence"][BATCH + "NEGATION-REVIEW.json"])
assert strict["files"] == 5 and strict["errors"] == 0
assert strict["review_candidates"] == local_review["detector"]["review_candidates"]
review_keys = {(x["path"],x["line"],x["code"]) for x in local_review["detector"]["findings"]}
assert {(x["path"],x["line"],x["code"]) for x in strict["findings"]} == review_keys
receipt = {"status": "validated candidate; native ref publication remains separate", "parent_sha": head, "parent_tree": base_tree,
    "reviewed_source_base": payload["source_base"], "payload_sha256": digest(packed), "authored_records": 6,
    "complete_operation_bodies": 2, "bounded_supporting_records": 4, "movement_bodies_changed": 0,
    "strict": strict, "links_checked": len(checks), "full_suite_exit": suite_exit, "full_suite_tail": suite[-15000:],
    "frozen_tracked_files": len(before_suite), "frozen_content_digest": digest(json.dumps(before_suite,sort_keys=True).encode()),
    "generated_changes": sum(generated(p) for p in paths), "protected_or_unexpected_mutations": [],
    "acceptance": "Two complete concepts and four bounded repairs; inherited recipient findings remain scoped in the review, not broadly accepted.",
    "changed_records": [{"path": p, "git_blob": blob(safe(p).read_bytes())} for p in paths]}
name = BATCH + "INTEGRATION-VALIDATION.json"
safe(name).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
paths.append(name)
(OUT / "INTEGRATION-VALIDATION.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
for output in sorted(OUT.iterdir()):
    if output.name == "INTEGRATION-VALIDATION.json":
        continue
    name = BATCH + "integration-checks/" + output.name
    target = safe(name)
    assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(output.read_bytes())
    paths.append(name)
(OUT / "validated-paths.json").write_text(json.dumps([{"path": p, "mode": "100644", "type": "blob", "sha": blob(safe(p).read_bytes())} for p in paths], indent=2) + "\n")
def upload(name):
    data = safe(name).read_bytes()
    expected = blob(data)
    result = api("git/blobs", {"encoding": "base64", "content": base64.b64encode(data).decode()})
    assert result["sha"] == expected
    print("BLOB", name, expected, flush=True)
    return {"path": name, "mode": "100644", "type": "blob", "sha": expected}
with ThreadPoolExecutor(max_workers=4) as pool:
    entries = list(pool.map(upload, paths))
tree = api("git/trees", {"base_tree": base_tree, "tree": entries})
result = {"parent_sha": head, "tree_sha": tree["sha"], "entries": entries, "receipt": receipt}
(OUT / "candidate-tree.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print("CANDIDATE_TREE=" + tree["sha"], flush=True)
print("PARENT_COMMIT=" + head, flush=True)
