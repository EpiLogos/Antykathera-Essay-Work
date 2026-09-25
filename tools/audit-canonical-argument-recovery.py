#!/usr/bin/env python3
"""Audit canonical essay prose for argument-recovery regressions.

This tool does not rewrite prose. It distinguishes hard recovery failures from
candidate passages that require human semantic review.

Use --strict with explicit --path arguments while repairing records. Whole-field
strict mode is intentionally allowed to fail until the current recovery is complete.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import json
import re
import sys


ROOT_RELATION_TYPES = {"root-relation", "spine-index"}
SIXFOLD = ("#0", "#1", "#2", "#3", "#4", "#5→0")

HARD_PATTERNS = [
    (
        "AI_CONSCIOUSNESS_GUARD",
        re.compile(
            r"(?:does not|doesn't|cannot|can not|neither .* nor .*|leaves? .*|remains?)"
            r".{0,90}(?:artificial|machine|agent|software|technical).{0,80}"
            r"(?:phenomen|conscious|subjectiv|sentien)",
            re.I,
        ),
    ),
    (
        "AI_CONSCIOUSNESS_GUARD",
        re.compile(
            r"(?:phenomenal(?:ity| status| subjectivity)|machine consciousness|artificial consciousness)"
            r".{0,100}(?:open|undecided|unresolved|not established|not proved|not inferred|not settled)",
            re.I,
        ),
    ),
    (
        "AGENT_META",
        re.compile(
            r"(?:Depth Restoration:|Unresolved Delta:|P1 consumers?:|No Movement prose changes|"
            r"batch backcheck|current runtime|restored from .* packet)",
            re.I,
        ),
    ),
]

CANDIDATE_PATTERNS = [
    (
        "PROVENANCE_THEATRE",
        re.compile(
            r"(?:native|authorial).{0,70}(?:notation|language|derivation|claim)|"
            r"(?:not|never).{0,70}(?:attributed to|originate|source of that notation)|"
            r"independent (?:historical|philosophical|lexical) (?:route|warrant)",
            re.I,
        ),
    ),
    (
        "DEFENSIVE_NEGATION",
        re.compile(
            r"\b(?:does not|cannot|is not|are not|not merely|not simply|never)\b",
            re.I,
        ),
    ),
    (
        "STATUS_LEAK",
        re.compile(
            r"\b(?:Derived|Argued|Offered|Open|Extracted|Paraphrased|Resonant with)\b"
        ),
    ),
    (
        "ADDRESS_LEAK",
        re.compile(r"\b(?:A\d{2}(?:′|p)?|C\d{2}|M\d{2}|P1|R\d+|T\d+)\b"),
    ),
]


@dataclass
class Finding:
    path: str
    line: int
    severity: str
    code: str
    text: str


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    raw = text[4:end].splitlines()
    fm: dict[str, str] = {}
    for line in raw:
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, value = line.split(":", 1)
        fm[key.strip()] = value.strip().strip('"').strip("'")
    return fm, text[end + 5 :]


def sixfold_headings(body: str) -> set[str]:
    found: set[str] = set()
    for line in body.splitlines():
        m = re.match(r"^##\s+(#(?:5→0|[0-4]))(?:\s|$)", line)
        if m:
            found.add(m.group(1))
    return found


def is_public_argument_surface(path: Path) -> bool:
    parts = path.parts
    if path.suffix.lower() != ".md":
        return False
    if "submission-package" not in parts or "essay" not in parts:
        return False
    if "sources" in parts:
        return False
    if path.name in {"README.md", "CANONICAL-INDEX.md"}:
        return False
    return True


def discover(root: Path) -> list[Path]:
    base = root / "submission-package" / "essay"
    return sorted(p for p in base.rglob("*.md") if is_public_argument_surface(p))


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def audit_file(root: Path, path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    rel = str(path.relative_to(root))
    findings: list[Finding] = []

    if fm.get("record_type") in ROOT_RELATION_TYPES:
        present = sixfold_headings(body)
        for heading in SIXFOLD:
            if heading not in present:
                findings.append(
                    Finding(
                        rel,
                        1,
                        "error",
                        "SIXFOLD_BROKEN",
                        f"missing canonical sixfold section {heading}",
                    )
                )

    for code, pattern in HARD_PATTERNS:
        for match in pattern.finditer(body):
            line = line_for_offset(body, match.start())
            snippet = body.splitlines()[line - 1].strip()
            findings.append(Finding(rel, line, "error", code, snippet[:500]))

    for code, pattern in CANDIDATE_PATTERNS:
        for match in pattern.finditer(body):
            line = line_for_offset(body, match.start())
            snippet = body.splitlines()[line - 1].strip()
            findings.append(Finding(rel, line, "review", code, snippet[:500]))

    return findings


def resolve_paths(root: Path, raw_paths: list[str]) -> list[Path]:
    if not raw_paths:
        return discover(root)
    resolved: list[Path] = []
    for raw in raw_paths:
        p = Path(raw)
        if not p.is_absolute():
            p = root / p
        p = p.resolve()
        if p.is_dir():
            resolved.extend(sorted(x for x in p.rglob("*.md") if is_public_argument_surface(x)))
        elif p.is_file():
            resolved.append(p)
        else:
            raise FileNotFoundError(raw)
    seen: set[Path] = set()
    out: list[Path] = []
    for p in resolved:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    ap.add_argument(
        "--path",
        action="append",
        default=[],
        help="Repository-relative file or directory. Repeatable. Defaults to all public essay Markdown.",
    )
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = args.project_root.resolve()
    paths = resolve_paths(root, args.path)
    findings: list[Finding] = []
    for path in paths:
        findings.extend(audit_file(root, path))

    errors = [f for f in findings if f.severity == "error"]
    reviews = [f for f in findings if f.severity == "review"]
    report = {
        "files": len(paths),
        "errors": len(errors),
        "review_candidates": len(reviews),
        "findings": [asdict(f) for f in findings],
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(
            f"canonical argument recovery audit: {len(paths)} files, "
            f"{len(errors)} errors, {len(reviews)} review candidates"
        )
        for f in findings:
            print(f"{f.severity.upper():6} {f.code:28} {f.path}:{f.line}  {f.text}")

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
