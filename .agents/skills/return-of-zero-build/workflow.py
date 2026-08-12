#!/usr/bin/env python3
"""Return-of-Zero field-page build workflow helper.

Handles the deterministic parts of the build skill:
  - intake: reads quilting surfaces and emits an intake manifest;
  - hygiene: runs link/effect validation gates after page development.

The actual subagent dispatch is performed by the parent agent following the
return-of-zero-build SKILL.md; this script never invents content.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_QUILTS = [
    "submission-package/essay/quilt/2026-08-02-PARALLEL-HARMONISED-QUILT.md",
    "submission-package/essay/quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md",
]


def find_project_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "submission-package" / "essay" / "THE-RETURN-OF-ZERO.md").exists():
            return p
    return start


def read_quilt(path: Path) -> list[dict[str, Any]]:
    """Extract candidate elements from a quilting surface.

    This is intentionally conservative: it surfaces sections and XML contribution
    blocks with enough context for a parent agent to resolve canonical targets.
    """
    text = path.read_text(encoding="utf-8")
    elements: list[dict[str, Any]] = []

    # Markdown section headers
    for m in re.finditer(r"^##+\s+(.*)$", text, re.MULTILINE):
        title = m.group(1).strip()
        if any(k in title.lower() for k in ("quilt", "ledger", "session", "contribution")):
            continue
        elements.append(
            {
                "kind": "section",
                "title": title,
                "source_file": str(path.relative_to(find_project_root(path))),
                "source_offset": m.start(),
                "register": None,
                "canonical_home": None,
            }
        )

    # XML-style session contributions
    for m in re.finditer(r'<session_contribution[^>]*?contribution_id="([^"]+)"', text):
        elements.append(
            {
                "kind": "session_contribution",
                "contribution_id": m.group(1),
                "source_file": str(path.relative_to(find_project_root(path))),
                "source_offset": m.start(),
                "register": None,
                "canonical_home": None,
            }
        )

    return elements


def cmd_intake(args: argparse.Namespace) -> int:
    root = Path(args.project_root)
    manifest: dict[str, Any] = {
        "project_root": str(root),
        "quilts_read": [],
        "elements": [],
    }

    for rel in DEFAULT_QUILTS:
        path = root / rel
        if not path.exists():
            print(f"warning: quilt not found: {path}", file=sys.stderr)
            continue
        elements = read_quilt(path)
        manifest["quilts_read"].append(str(path.relative_to(root)))
        for el in elements:
            el["quilt"] = str(path.relative_to(root))
        manifest["elements"].extend(elements)

    out_path = Path(args.output)
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote intake manifest: {out_path} ({len(manifest['elements'])} candidate elements)")
    return 0


def run_okf(root: Path, *args: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "tools/okf-workspace.py", "--project-root", str(root), *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def cmd_hygiene(args: argparse.Namespace) -> int:
    root = Path(args.project_root)
    intake_path = Path(args.intake)
    if not intake_path.exists():
        print(f"error: intake manifest not found: {intake_path}", file=sys.stderr)
        return 1

    report: dict[str, Any] = {
        "project_root": str(root),
        "intake": str(intake_path),
        "gates": {},
    }

    # Gate 1: doctor
    doctor = run_okf(root, "doctor", "--json")
    report["gates"]["doctor"] = {
        "command": "okf-workspace.py doctor --json",
        "returncode": doctor.returncode,
        "stdout": doctor.stdout,
        "stderr": doctor.stderr,
    }

    # Gate 2: links (read-only link health)
    links = run_okf(root, "links", "--json")
    report["gates"]["links"] = {
        "command": "okf-workspace.py links --json",
        "returncode": links.returncode,
        "stdout": links.stdout,
        "stderr": links.stderr,
    }

    # Gate 3: effects on changed consumers (best-effort from intake)
    manifest = json.loads(intake_path.read_text(encoding="utf-8"))
    effects: list[dict[str, Any]] = []
    for el in manifest.get("elements", []):
        cid = el.get("contribution_id") or el.get("title")
        if not cid:
            continue
        proc = run_okf(root, "effects", cid, "--depth", "4", "--json")
        effects.append(
            {
                "target": cid,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            }
        )
    report["gates"]["effects"] = effects

    out_path = Path(args.output)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"wrote hygiene report: {out_path}")

    failures = sum(1 for g in [report["gates"]["doctor"], report["gates"]["links"]] if g["returncode"] != 0)
    if failures:
        print(f"hygiene failed {failures} gate(s); see report for details", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Return-of-Zero field-page build workflow helper")
    parser.add_argument("--project-root", default=str(find_project_root()), help="project root path")
    sub = parser.add_subparsers(dest="command", required=True)

    p_intake = sub.add_parser("intake", help="assemble intake manifest from quilting surfaces")
    p_intake.add_argument("--output", default="intake.json", help="output manifest path")
    p_intake.set_defaults(func=cmd_intake)

    p_hygiene = sub.add_parser("hygiene", help="run link/effect validation gates")
    p_hygiene.add_argument("--intake", default="intake.json", help="intake manifest path")
    p_hygiene.add_argument("--output", default="hygiene.json", help="output report path")
    p_hygiene.set_defaults(func=cmd_hygiene)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
