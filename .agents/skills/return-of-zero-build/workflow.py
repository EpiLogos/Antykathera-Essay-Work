#!/usr/bin/env python3
"""Return-of-Zero field-page build workflow helper.

Handles the deterministic parts of the build skill:
  - intake: reads quilting surfaces and emits an intake manifest;
  - hygiene: runs link/effect validation gates after page development.

The actual subagent dispatch is performed by the parent agent following the
return-of-zero-build SKILL.md; this script never invents content.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

QUILT_DIRECTORY = Path("submission-package/essay/quilt")
DEPTH_DIRECTORY = Path("working/p2-enrichment/argument-depth")


def live_quilts(root: Path) -> list[Path]:
    """Admit every live file; a historical list cannot delimit recovery."""
    return sorted(p for p in (root / QUILT_DIRECTORY).iterdir() if p.is_file())


def depth_inputs(root: Path, quilts: list[Path]) -> list[dict[str, str]]:
    """Check presence/coverage only, never certify the quality of recovery."""
    receipts = []
    errors = []
    for number in range(1, 37):
        identity = f"A{number:02d}"
        path = root / DEPTH_DIRECTORY / f"{identity}.md"
        if not path.is_file():
            errors.append(f"{identity}: missing recovery packet")
            continue
        body = path.read_text(encoding="utf-8")
        for quilt in quilts:
            if quilt.name not in body:
                errors.append(f"{identity}: quilt coverage not recorded: {quilt.name}")
        receipts.append({"argument_id": identity, "path": str(path.relative_to(root)),
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    if errors:
        raise ValueError("Argument-depth preflight failed:\n" + "\n".join(errors))
    return receipts


def find_project_root(start: Path | None = None) -> Path:
    start = start or Path.cwd()
    for p in [start, *start.parents]:
        if (p / "submission-package" / "essay" / "THE-RETURN-OF-ZERO.md").exists():
            return p
    return start


def read_quilt(path: Path, root: Path | None = None) -> list[dict[str, Any]]:
    """Extract candidate elements from a quilting surface.

    This is intentionally conservative: it surfaces sections and XML contribution
    blocks with enough context for a parent agent to resolve canonical targets.
    """
    text = path.read_text(encoding="utf-8")
    root = root or find_project_root(path.parent)
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
                "source_file": str(path.relative_to(root)),
                "source_offset": m.start(),
                "source_line": text.count("\n", 0, m.start()) + 1,
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
                "source_file": str(path.relative_to(root)),
                "source_offset": m.start(),
                "source_line": text.count("\n", 0, m.start()) + 1,
                "register": None,
                "canonical_home": None,
            }
        )

    return elements


def cmd_intake(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    try:
        quilts = live_quilts(root)
        if not quilts:
            raise ValueError("The live quilt corpus is empty")
        depth = depth_inputs(root, quilts)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    manifest: dict[str, Any] = {
        "schema_version": 2,
        "authority": "discovery-only; requires census reconciliation and semantic review",
        "project_root": str(root),
        "argument_depth": depth,
        "quilt_hashes": {},
        "quilts_read": [],
        "elements": [],
    }

    for path in quilts:
        elements = read_quilt(path, root)
        manifest["quilt_hashes"][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest["quilts_read"].append(str(path.relative_to(root)))
        for el in elements:
            el["quilt"] = str(path.relative_to(root))
        manifest["elements"].extend(elements)

    out_path = Path(args.output)
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote intake manifest: {out_path} ({len(manifest['elements'])} candidate elements)")
    return 0


def input_file(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"Input is not a file inside the project: {relative}")
    return path


def extract_slice(root: Path, item: dict[str, Any]) -> dict[str, Any]:
    path = input_file(root, item["path"])
    lines = path.read_text(encoding="utf-8").splitlines()
    start, end = item["start_line"], item["end_line"]
    if not isinstance(start, int) or not isinstance(end, int) or not 1 <= start <= end <= len(lines):
        raise ValueError(f"Invalid source range: {item}")
    if path.parent == root / QUILT_DIRECTORY and start == 1 and end == len(lines):
        raise ValueError("Page packets use target-keyed quilt slices, never whole-quilt dumps")
    if not item.get("relation") or not item.get("provenance"):
        raise ValueError("Every source slice needs its relation and provenance")
    return {**item, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "text": "\n".join(lines[start - 1:end])}


def cmd_packet(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    try:
        depth = depth_inputs(root, live_quilts(root))
        queue = json.loads(Path(args.queue).read_text(encoding="utf-8"))
        if queue.get("status") != "reconciled":
            raise ValueError("Page packets require a reconciled census queue")
        acceptance = json.loads(input_file(root, queue["depth_acceptance"]).read_text(encoding="utf-8"))
        if acceptance.get("status") != "accepted" or acceptance.get("argument_depth") != depth:
            raise ValueError("Argument-depth review is absent or stale against current packet hashes")
        matches = [e for e in queue["elements"] if e.get("record_id") == args.target]
        if len(matches) != 1:
            raise ValueError(f"Target must have exactly one admitted identity: {args.target}")
        element = matches[0]
        for field in ("canonical_home", "register", "record_type", "authority", "argument_depth", "direct_carriers", "source_houses", "source_slices", "relations", "register_contract"):
            if field not in element:
                raise ValueError(f"Target missing required input field: {field}")
        if not element["argument_depth"] or not element["direct_carriers"] or not element["source_slices"]:
            raise ValueError("Target needs recovered Argument depth, direct carriers, and target-keyed slices")
        accepted = {d["argument_id"]: d for d in depth}
        selected_depth = [accepted[identity] for identity in element["argument_depth"]]
        inputs = []
        for relative in [*element["direct_carriers"], element["register_contract"],
                         ".agents/skills/return-of-zero-pages/SKILL.md", ".agents/skills/return-of-zero-links/SKILL.md"]:
            path = input_file(root, relative)
            inputs.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        sources = []
        for relative in element["source_houses"]:
            source = input_file(root, relative)
            if source.name != "SOURCE.md":
                raise ValueError(f"Source-house input must name SOURCE.md: {relative}")
            notes = source.with_name("NOTES.md")
            sources.append({"source": relative, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                            "notes": str(notes.relative_to(root)) if notes.is_file() else None,
                            "notes_sha256": hashlib.sha256(notes.read_bytes()).hexdigest() if notes.is_file() else None,
                            "notes_policy": "read in full; authorial provenance; never mutate"})
        packet = {"schema_version": 1, "target": element, "argument_depth": selected_depth,
                  "required_inputs": inputs, "sources": sources,
                  "slices": [extract_slice(root, item) for item in element["source_slices"]],
                  "raw_skeleton": "# " + element.get("title", args.target) + "\n\n" + "\n\n".join("## " + p for p in ["#0", "#1", "#2", "#3", "#4", "#5→0"]),
                  "standing": "Writer must read inputs and derive page-specific sixfold; this packet certifies neither prose nor external evidence"}
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    output = Path(args.output)
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote target packet: {output}")
    return 0


def run_okf(root: Path, *args: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "tools/okf-workspace.py", "--project-root", str(root), *args]
    return subprocess.run(cmd, cwd=root, capture_output=True, text=True)


def canonical_targets(root: Path, manifest: dict[str, Any]) -> list[str]:
    """Require explicit reconciled homes; never resolve a heading as an identity."""
    targets = []
    for element in manifest.get("elements", []):
        if element.get("disposition") in {"merged", "redundant", "non-page", "superseded"}:
            if not element.get("disposition_reason"):
                raise ValueError("Non-page dispositions need an explicit reason")
            continue
        home = element.get("canonical_home")
        if not home or not element.get("register"):
            raise ValueError("Hygiene requires census-reconciled canonical_home and register for every page")
        path = (root / home).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"Canonical home does not exist inside project: {home}")
        target = str(path.relative_to(root))
        if target not in targets:
            targets.append(target)
    if not targets:
        raise ValueError("No reconciled page targets supplied")
    return targets


def command_result(proc: subprocess.CompletedProcess) -> dict[str, Any]:
    result = {"returncode": proc.returncode, "stderr": proc.stderr}
    try:
        result["data"] = json.loads(proc.stdout)
    except json.JSONDecodeError:
        result["stdout"] = proc.stdout
        if proc.returncode == 0:
            result["returncode"] = 1
            result["stderr"] += " Expected JSON from workspace command."
    return result


def cmd_hygiene(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    intake_path = Path(args.intake)
    try:
        manifest = json.loads(intake_path.read_text(encoding="utf-8"))
        targets = canonical_targets(root, manifest)
    except (OSError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report: dict[str, Any] = {
        "schema_version": 2,
        "project_root": str(root),
        "intake": str(intake_path),
        "scope": "reconciled targets; global doctor debt is reported separately",
        "targets": targets,
        "gates": {},
    }
    doctor = command_result(run_okf(root, "doctor", "--json"))
    report["gates"]["doctor"] = doctor
    failures = int(doctor["returncode"] != 0)
    report["gates"]["links"] = []
    report["gates"]["effects"] = []
    for target in targets:
        links = command_result(run_okf(root, "links", target, "--json"))
        links["target"] = target
        edges = links.get("data", {}).get("edges", [])
        links["unresolved"] = [edge for edge in edges if not edge.get("resolved")]
        links["frozen_targets"] = [edge for edge in edges if
            edge.get("target", "") and edge["target"].startswith("working/legacy/")]
        failures += int(links["returncode"] != 0 or bool(links["unresolved"]) or bool(links["frozen_targets"]))
        report["gates"]["links"].append(links)
        effects = command_result(run_okf(root, "effects", target, "--depth", "4", "--json"))
        effects["target"] = target
        failures += int(effects["returncode"] != 0)
        report["gates"]["effects"].append(effects)
    report["failures"] = failures
    out_path = Path(args.output)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote hygiene report: {out_path}")
    if failures:
        print(f"hygiene failed {failures} target/command gate(s); see report", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Return-of-Zero field-page build workflow helper")
    parser.add_argument("--project-root", default=str(find_project_root()), help="project root path")
    sub = parser.add_subparsers(dest="command", required=True)

    p_intake = sub.add_parser("intake", help="assemble intake manifest from quilting surfaces")
    p_intake.add_argument("--project-root", default=argparse.SUPPRESS, help="project root path")
    p_intake.add_argument("--output", default="intake.json", help="output manifest path")
    p_intake.set_defaults(func=cmd_intake)

    p_packet = sub.add_parser("packet", help="extract a target-keyed packet from a reviewed census queue")
    p_packet.add_argument("--project-root", default=argparse.SUPPRESS)
    p_packet.add_argument("--queue", required=True)
    p_packet.add_argument("--target", required=True)
    p_packet.add_argument("--output", required=True)
    p_packet.set_defaults(func=cmd_packet)

    p_hygiene = sub.add_parser("hygiene", help="run link/effect validation gates")
    p_hygiene.add_argument("--project-root", default=argparse.SUPPRESS, help="project root path")
    p_hygiene.add_argument("--intake", default="intake.json", help="intake manifest path")
    p_hygiene.add_argument("--output", default="hygiene.json", help="output report path")
    p_hygiene.set_defaults(func=cmd_hygiene)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
