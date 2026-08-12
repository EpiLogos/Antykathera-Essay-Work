#!/usr/bin/env python3
"""Audit the compact Return of Zero room system against real workspace files."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_resolver import resolve_source_house


ROOM_ROOT = Path("submission-package/essay/section-rooms")
ALLOWED = {"ROOM.md", "READING.md", "SCRATCH.md", "VISUALS.md"}
LEGACY = {
    ".section-room.json", "00-SECTION-CONTEXT.md", "04-READING-PATH.md",
    "05-ROOM-DOSSIER.md", "10-FRANK-DRAFT.md", "20-SCHOLARLY-EDITION.md",
    "30-PLATE-AND-DIAGRAMS.md",
}
THRESHOLD_ROOM = "00-integral-threshold"
THRESHOLD_QUOTE_IDS = tuple(
    f"{source}-q{number:03d}"
    for source in (
        "bratton-2026-agentworld-brief",
        "pind-2009-dignaga-anyapoha-dissertation",
        "spinoza-1674-letter-50-jelles",
        "godel-1931-undecidable-propositions",
        "raatikainen-2026-godel-incompleteness-sep",
        "wittgenstein-1922-tractatus",
        "russell-1908-theory-types",
        "cusa-on-learned-ignorance",
        "maroski-2025-seeing-through-solid-words",
    )
    for number in (1, 2)
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--room", action="append", dest="rooms")
    parser.add_argument("--require-deepened", action="store_true", help="Compatibility flag; compact rooms are checked at their complete v2 contract.")
    return parser.parse_args()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def heading_slug(heading: str) -> str:
    heading = re.sub(r"[`*_~]", "", heading).casefold()
    heading = re.sub(r"[^\w\s-]", "", heading)
    return re.sub(r"[-\s]+", "-", heading).strip("-")


def fragment_resolves(path: Path, fragment: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if re.search(rf'<a\s+id=["\']{re.escape(fragment)}["\']\s*></a>', text):
        return True
    return any(
        heading_slug(match.group(1)) == fragment
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    )


def audit_threshold_reading(project: Path, room: Path) -> list[str]:
    """Verify that §0/1 is a real learning route, not a compact source inventory."""
    errors: list[str] = []
    path = room / "READING.md"
    if not path.is_file():
        return ["§0/1 is missing its protected READING.md learning surface"]
    text = path.read_text(encoding="utf-8")
    for field in (
        "page_type: room-reading-route",
        "reading_route_id: reading-s01-integral-threshold",
        "ownership: protected-learning-surface",
    ):
        if field not in text:
            errors.append(f"READING.md lacks frontmatter field: {field}")
    for heading in (
        "## Fifteen-minute entry",
        "## Full reading sequence",
        "### #0 — A system acts from a horizon it does not display",
        "### #1 — The subject appears through mediation",
        "### #2 — A definition gives by cutting",
        "### #3 — Formal closure meets differently constituted limits",
        "### #4 — Learned ignorance and diaphaneity change the response",
        "### #5→0 — Zero enters as a promise",
        "## Pair-writing handholds",
        "## What remains unresolved",
    ):
        if heading not in text:
            errors.append(f"READING.md lacks substantive route heading: {heading}")
    for field in ("**Exercise:**", "**Carry:**"):
        count = text.count(field)
        if count != 6:
            errors.append(f"READING.md has {count} {field} fields; expected six")
    for detail in (
        "two-column instrument panel",
        "I see x",
        "draw one finite figure",
        "four-row table",
        "add a transparency layer",
        "write two sentences",
        "manuscript anchor",
        "movement node",
        "exact passage anchors",
        "paragraph’s outgoing carry",
        "local claim",
        "source’s operation",
        "exact anchor and locator",
        "PSV V:11d card, p. 85",
        "vicious-circle card, §IV, p. 237",
        "proposition 4.1212 card, PDF p. 40",
        "Book I, ch. 1 card, margin 4, printed p. 6",
    ):
        if detail not in text:
            errors.append(f"READING.md lacks learning or pair-writing detail: {detail}")
    for quote_id in THRESHOLD_QUOTE_IDS:
        source_id = quote_id.rsplit("-q", 1)[0]
        source_house = resolve_source_house(project, source_id)
        if f"#{quote_id}" not in text:
            errors.append(f"READING.md does not link exact source passage: {quote_id}")
        elif not source_house or not source_house.is_file():
            errors.append(f"source house is missing for passage: {quote_id}")
        elif not fragment_resolves(source_house, quote_id):
            errors.append(f"source passage anchor does not resolve: {quote_id}")
    for destination in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        path_part, separator, fragment = destination.partition("#")
        target = (room / path_part).resolve()
        if not target.is_file():
            errors.append(f"READING.md link target is missing: {destination}")
        elif separator and not fragment_resolves(target, fragment):
            errors.append(f"READING.md link fragment does not resolve: {destination}")
    words = len(text.split())
    if words < 1600:
        errors.append(f"READING.md has {words} words; substantive §0/1 route expected at least 1600")
    if re.search(r"(?m)^>", text):
        errors.append("READING.md duplicates source quotation or callout text")
    for legacy_name in ("04-READING-PATH", "05-ROOM-DOSSIER", "10-FRANK-DRAFT"):
        if legacy_name in text:
            errors.append(f"READING.md points back into the legacy room system: {legacy_name}")
    return errors


def audit_room(project: Path, slug: str) -> list[str]:
    errors: list[str] = []
    room = project / ROOM_ROOT / slug
    if not room.is_dir():
        return [f"room directory is missing: {room}"]
    files = {path.name for path in room.iterdir() if path.is_file()}
    unexpected = files - ALLOWED
    if unexpected:
        errors.append("unexpected active files: " + ", ".join(sorted(unexpected)))
    if files & LEGACY:
        errors.append("legacy room system remains active: " + ", ".join(sorted(files & LEGACY)))
    for required in ("ROOM.md",):
        if required not in files:
            errors.append(f"required file is missing: {required}")
    if errors:
        return errors

    text = (room / "ROOM.md").read_text(encoding="utf-8")
    words = len(re.findall(r"\b[^\s]+\b", re.sub(r"---.*?---", "", text, count=1, flags=re.DOTALL)))
    if not 500 <= words <= 900:
        errors.append(f"ROOM.md has {words} words; expected 500–900")
    for heading in ("## Arrival", "## Section wager", "## Six waypoints", "## Release"):
        if heading not in text:
            errors.append(f"ROOM.md lacks {heading}")
    for field in ("**Incoming pressure:**", "**Earned position (", "**Carry-forward:**", "**Open:**"):
        count = text.count(field)
        if count != 6:
            errors.append(f"ROOM.md has {count} {field} fields; expected six")
    if re.search(r"(?m)^>", text):
        errors.append("ROOM.md embeds source quotation or callout text")
    if "THE-RETURN-OF-ZERO.md#section-" not in text:
        errors.append("ROOM.md does not link to its master-manuscript anchor")

    if slug == THRESHOLD_ROOM:
        errors.extend(audit_threshold_reading(project, room))
    return errors


def builder_check(project: Path, rooms: list[str]) -> str | None:
    command = [sys.executable, str(project / "tools/build-section-rooms.py"), "--project-root", str(project), "--check"]
    for room in rooms:
        command.extend(["--room", room])
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode == 0:
        return None
    return (result.stdout + result.stderr).strip() or "builder check failed"


def main() -> int:
    args = parse_args()
    project = args.project_root.resolve()
    roots = project / ROOM_ROOT
    rooms = args.rooms or sorted(path.name for path in roots.iterdir() if path.is_dir() and not path.name.startswith("."))
    failures = 0
    for slug in rooms:
        errors = audit_room(project, slug)
        if errors:
            failures += 1
            print(f"FAIL {slug}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {slug}")
    stale = builder_check(project, rooms)
    if stale:
        failures += 1
        print(f"FAIL generated ownership\n  - {stale}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
