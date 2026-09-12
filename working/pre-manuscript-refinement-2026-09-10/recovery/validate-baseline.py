#!/usr/bin/env python3
"""Regenerate and test the admitted R1 baseline; never apply the missing R2 batch."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

HOME = Path(__file__).resolve().parent
ROOT = HOME.parents[2]
EP = "submission-package/essay/symbolon/episteme/"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected() -> dict[str, str]:
    paths = {p for p in ROOT.rglob("NOTES.md") if p.is_file() and not p.is_symlink()}
    paths.update(p for p in (ROOT / "working/sources-texts-references").rglob("*") if p.is_file() and not p.is_symlink())
    paths.add(ROOT / "submission-package/essay/THE-RETURN-OF-ZERO.md")
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(paths)}


def generated(path: str) -> bool:
    return (
        path in {EP + "sources/" + name for name in ("SOURCE-INDEX.md", "PASSAGE-LEDGER.md", "MAIN-SOURCES.md")}
        or path in {EP + "maps/navigation/" + name for name in ("MOC.md", "AUDIT.md", "audit.json", "reader-audit.json")}
        or re.fullmatch(re.escape(EP) + r"maps/navigation/intents/[^/]+\.md", path) is not None
        or path == "submission-package/essay/section-rooms/README.md"
        or re.fullmatch(r"submission-package/essay/section-rooms/\d\d-[^/]+/ROOM\.md", path) is not None
    )


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate-baseline.py OUTPUT_DIRECTORY_OUTSIDE_REPOSITORY")
    out = Path(sys.argv[1]).resolve()
    if out == ROOT or ROOT in out.parents:
        raise ValueError("Evidence must be written outside the repository")
    out.mkdir(parents=True, exist_ok=True)
    report = {"kind": "R1-baseline-regeneration-not-R2-admission", "starting_commit": git("rev-parse", "HEAD"), "commands": [], "admission_ready": False, "completed": False}

    def run(name: str, args: list[str], required: bool = True) -> None:
        started = time.monotonic()
        with (out / (name + ".log")).open("w", encoding="utf-8") as stream:
            result = subprocess.run(args, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=False)
        report["commands"].append({"name": name, "command": args, "exit_code": result.returncode, "seconds": round(time.monotonic() - started, 3), "required": required})
        if required and result.returncode:
            raise RuntimeError(f"{name} failed: exit {result.returncode}")

    try:
        if git("status", "--porcelain"):
            raise ValueError("Refuse a dirty starting checkout")
        run("custody", [sys.executable, str(HOME / "verify-recovery.py"), "--output", str(out / "custody.json")])
        custody = json.loads((out / "custody.json").read_text())
        if custody["current_preimage_conflicts"]:
            raise ValueError("Original R2 preimages changed; do not replay this bounded baseline repair")
        before = protected()
        if len(before) != 472:
            raise ValueError(f"Expected original 472 protected files; found {len(before)}")
        (out / "protected-before.json").write_text(json.dumps(before, indent=2) + "\n")
        ac = ROOT / EP / "conjugate/AC.md"
        ac_before = digest(ac)
        for tool in ("build-source-projections", "build-section-rooms", "build-navigation"):
            run(tool, [sys.executable, f"tools/{tool}.py"])
        run("unittest", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
        for tool in ("build-source-projections", "build-section-rooms", "build-navigation"):
            run(tool + "-check", [sys.executable, f"tools/{tool}.py", "--check"])
        rooms = sorted(p.name for p in (ROOT / "submission-package/essay/section-rooms").iterdir() if p.is_dir() and re.match(r"^\d\d-", p.name))
        if len(rooms) != 8:
            raise ValueError("Expected all eight actual rooms")
        # Current main's default also visits the historical arguments/ shelf.
        # Name all eight real rooms explicitly; do not silently discard a room.
        run("room-depth", [sys.executable, "tools/audit-room-depth.py", "--project-root", str(ROOT), *[item for room in rooms for item in ("--room", room)]])
        run("effects-C41", [sys.executable, "tools/okf-workspace.py", "effects", "C41", "--depth", "4", "--json"])
        for name in ("reader-navigation", "pre-manuscript"):
            run(name, [sys.executable, f"tools/audit-{name}.py", "--project-root", str(ROOT), "--output", str(out / (name + ".json"))], required=False)
        after = protected()
        if before != after or digest(ac) != ac_before:
            raise ValueError("Protected authorial content or A/C changed")
        changed = git("diff", "HEAD", "--name-only").splitlines()
        if any(not generated(path) for path in changed):
            raise ValueError(f"Non-generated mutation: {[p for p in changed if not generated(p)]}")
        if git("ls-files", "--others", "--exclude-standard"):
            raise ValueError("Unexpected untracked files after validation")
        if changed:
            subprocess.run(["git", "add", "--", *changed], cwd=ROOT, check=True)
        subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, check=True)
        if git("diff", "--name-only"):
            raise ValueError("Unstaged changes remain")
        report.update({"completed": True, "protected_files_unchanged": len(before), "ac_sha256_unchanged": ac_before, "rooms_checked": rooms, "generated_paths": changed, "tested_tree": git("write-tree")})
        (out / "generated.patch").write_text(git("diff", "--cached", "--binary") + "\n", encoding="utf-8")
        return 0
    except Exception as error:
        report["error"] = str(error)
        print(str(error), file=sys.stderr)
        return 1
    finally:
        (out / "baseline-validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: value for key, value in report.items() if key not in ("commands", "generated_paths")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
