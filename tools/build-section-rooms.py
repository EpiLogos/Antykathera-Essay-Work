#!/usr/bin/env python3
"""Build eight compact Return of Zero section rooms from the live essay graph.

The builder owns ROOM.md and its hidden provenance receipt.  It never writes
the master manuscript, READING.md, SCRATCH.md, or VISUALS.md.  Rooms are
waypoints into canonical nodes and source houses, not parallel essays.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_resolver import build_source_index


BUILDER_VERSION = "2.0.0"
ROOM_FILE = "ROOM.md"
MANUSCRIPT = "submission-package/essay/THE-RETURN-OF-ZERO.md"
ROOM_ROOT = "submission-package/essay/section-rooms"
STATIONS = ("§0/1", "§0", "§1", "§2", "§3", "§4", "§5", "§5→0")


@dataclass(frozen=True)
class RoomSpec:
    station: str
    slug: str
    title: str
    manuscript_anchor: str


ROOMS = (
    RoomSpec("§0/1", "00-integral-threshold", "The Integral Threshold — The Subject at the Formal Limit", "section-s01-integral-threshold"),
    RoomSpec("§0", "01-differentiating-mind", "Differentiating Mind — Tattvic Descent and Objective Internality", "section-s0-differentiating-mind"),
    RoomSpec("§1", "02-return-of-zero", "The Return of Zero — History, Empty Set, and Symbolic Linkage", "section-s1-return-of-zero"),
    RoomSpec("§2", "03-two-logics", "Two Logics of Two — Dia-ballein and Sym-ballein", "section-s2-two-logics"),
    RoomSpec("§3", "04-mathematical-substrate", "Mathematical Substrate — From 0/1 to the Arche-Topos", "section-s3-mathematical-substrate"),
    RoomSpec("§4", "05-psychoid-flowering", "Psychoid Flowering — Jung, Pauli, Lacan, and Gebser", "section-s4-psychoid-flowering"),
    RoomSpec("§5", "06-objective-internality", "Objective Internality and Agentic Research", "section-s5-objective-internality"),
    RoomSpec("§5→0", "07-instrument-returns", "Epi-Logos and 4:2 Technē — The Instrument Returns", "section-s50-instrument-returns"),
)


class BuildError(RuntimeError):
    pass


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise BuildError(f"required input is missing: {path}") from exc


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise BuildError("unclosed YAML frontmatter")
    return text[4:end], text[end + 5 :]


def scalar(value: str) -> Any:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inside = value[1:-1].strip()
        return [] if not inside else [scalar(item) for item in inside.split(",")]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    raw, body = split_frontmatter(text)
    result: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", lines[index])
        if not match:
            index += 1
            continue
        key, inline = match.group(1), (match.group(2) or "")
        if inline:
            result[key] = scalar(inline)
            index += 1
            continue
        items: list[Any] = []
        cursor = index + 1
        while cursor < len(lines):
            item = re.match(r"^\s+-\s+(.+)$", lines[cursor])
            if not item:
                break
            items.append(scalar(item.group(1)))
            cursor += 1
        result[key] = items
        index = cursor
    return result, body


def section(body: str, headings: tuple[str, ...]) -> str:
    names = "|".join(re.escape(item) for item in headings)
    match = re.search(
        rf"^##\s+(?:{names})\s*$\n(.*?)(?=^##\s+|\Z)",
        body,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return ""
    paragraphs = [re.sub(r"\s+", " ", item).strip() for item in re.split(r"\n\s*\n", match.group(1))]
    prose = [
        item for item in paragraphs
        if item and not item.startswith(("|", "- ", "$$", "\\["))
    ]
    if not prose:
        return ""
    if prose[0].endswith(":") and len(prose) > 1:
        return f"{prose[0]} {prose[1]}"
    return prose[0]


def first_body_section(body: str) -> str:
    match = re.search(r"^##\s+[^\n]+\n(.*?)(?=^##\s+|\Z)", body, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def sentence_excerpt(text: str, maximum_sentences: int = 1, maximum_words: int = 48) -> str:
    """Keep complete opening sentences; never cut a proposition mid-sentence."""
    clean = re.sub(r"\[\[([^]|]+)(?:\|([^]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    clean = re.sub(r"\s+", " ", clean).strip()
    clean = re.sub(r"^\*\*[^*]+:\*\*\s*", "", clean)
    if not clean:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-ÖØ-Þ§*`])", clean)
    chosen: list[str] = []
    for item in sentences:
        if len(chosen) >= maximum_sentences:
            break
        if chosen and len(" ".join(chosen + [item]).split()) > maximum_words:
            break
        chosen.append(item)
    return " ".join(chosen or [sentences[0]])


def parse_plan(path: Path) -> dict[str, dict[str, str]]:
    text = read_text(path)
    pattern = re.compile(r"^##\s+(§0/1|§0|§1|§2|§3|§4|§5→0|§5)\.\s+(.+)$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    plans: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.end() : end]
        claim = re.search(r"^\*\*Section claim:\*\*\s*(.+)$", block, re.MULTILINE)
        burden = re.search(r"^\*\*Primary burden:\*\*\s*(.+)$", block, re.MULTILINE)
        if claim and burden:
            plans[match.group(1)] = {
                "title": match.group(2).strip(),
                "claim": claim.group(1).strip(),
                "burden": burden.group(1).strip(),
            }
    missing = set(STATIONS) - plans.keys()
    if missing:
        raise BuildError(f"central plan lacks stations: {', '.join(sorted(missing))}")
    return plans


CLAIM_HEADINGS = ("Claim", "Movement thesis", "Derivation")
WARRANT_HEADINGS = (
    "Warrant", "Argumentative force", "Argumentative consequence",
    "Process-ontology warrant", "Technical consequence", "Formal payload",
    "Formal and psychoanalytic payload", "Mathematical and psychological force",
    "Symbolic and technical force",
)
TRANSITION_HEADINGS = (
    "Transition", "Anchor and transition", "Anchor and return", "Audit boundary and transition",
    "Release into §2", "Release into §3", "Return into psyche", "Handoff",
)


def load_movements(project: Path) -> list[dict[str, Any]]:
    movements: list[dict[str, Any]] = []
    for path in sorted((project / "submission-package/essay/section-rooms").glob("*/movements/*.md")):
        metadata, body = parse_frontmatter(read_text(path))
        required = ("title", "station", "position", "sequence", "claim_status")
        if not all(key in metadata for key in required):
            continue
        claim = section(body, CLAIM_HEADINGS) or first_body_section(body)
        if not claim:
            raise BuildError(f"movement has no claim: {path}")
        movements.append(
            {
                **metadata,
                "path": path,
                "body": body,
                "claim": claim,
                "warrant": section(body, WARRANT_HEADINGS),
                "transition": section(body, TRANSITION_HEADINGS),
                "source_ids": list(metadata.get("source_ids", [])),
                "quote_ids": list(metadata.get("quote_ids", [])),
            }
        )
    movements.sort(key=lambda item: int(item["sequence"]))
    if [item["sequence"] for item in movements] != list(range(1, 49)):
        raise BuildError("canonical section nodes must provide movement sequences 1–48 exactly once")
    return movements


def aliases(metadata: dict[str, Any], path: Path) -> set[str]:
    values = {path.stem, str(metadata.get("title", path.stem))}
    extra = metadata.get("aliases", [])
    if not isinstance(extra, list):
        extra = [extra]
    values.update(str(item) for item in extra if item)
    return {item.casefold() for item in values}


def load_argument_relations(project: Path, movements: list[dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    relation: dict[str, list[dict[str, str]]] = {Path(item["path"]).stem: [] for item in movements}
    movement_alias: dict[str, str] = {}
    for movement in movements:
        stem = Path(movement["path"]).stem
        movement_alias[stem.casefold()] = stem
        movement_alias[str(movement["title"]).casefold()] = stem
    argument_alias: dict[str, dict[str, str]] = {}
    arguments: list[tuple[Path, dict[str, Any], str]] = []
    for path in sorted((project / "submission-package/essay/section-rooms/arguments").glob("*.md")):
        metadata, body = parse_frontmatter(read_text(path))
        item = {"path": path.relative_to(project).as_posix(), "title": str(metadata.get("title", path.stem))}
        for name in aliases(metadata, path):
            argument_alias[name] = item
        arguments.append((path, metadata, body))
        for target in re.findall(r"\[\[([^]|#]+)", body):
            stem = movement_alias.get(target.casefold())
            if stem and item not in relation[stem]:
                relation[stem].append(item)
    for movement in movements:
        stem = Path(movement["path"]).stem
        for target in re.findall(r"\[\[([^]|#]+)", movement["body"]):
            item = argument_alias.get(target.casefold())
            if item and item not in relation[stem]:
                relation[stem].append(item)
        relation[stem].sort(key=lambda item: item["title"].casefold())
    return relation


def source_file(project: Path, source_id: str) -> Path:
    house = build_source_index(project).get(source_id)
    if house and house.is_file():
        return house
    raise BuildError(f"source_id has no canonical source: {source_id}")


def relative_link(from_dir: Path, target: Path, label: str, anchor: str = "") -> str:
    relative = os.path.relpath(target, from_dir).replace(os.sep, "/")
    return f"[{label}]({relative}{anchor})"


def heading_slug(heading: str) -> str:
    heading = re.sub(r"[`*_~]", "", heading).casefold()
    heading = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
    return re.sub(r"[-\s]+", "-", heading).strip("-")


def has_fragment(path: Path, fragment: str) -> bool:
    text = read_text(path)
    if re.search(rf'<a\s+id=["\']{re.escape(fragment)}["\']\s*></a>', text):
        return True
    return any(
        heading_slug(match.group(1)) == fragment
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    )


def validate_links(project: Path, room_dir: Path, text: str) -> None:
    errors: list[str] = []
    for destination in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        path_part, separator, fragment = destination.partition("#")
        target = (room_dir / path_part).resolve() if path_part else room_dir / ROOM_FILE
        try:
            target.relative_to(project)
        except ValueError:
            errors.append(f"link leaves project: {destination}")
            continue
        if not target.is_file():
            errors.append(f"link target is missing: {destination}")
            continue
        if separator and not has_fragment(target, fragment):
            errors.append(f"link fragment does not resolve: {destination}")
    if errors:
        raise BuildError(f"{room_dir.name}/{ROOM_FILE} has invalid links:\n  - " + "\n  - ".join(errors))


def movement_links(
    project: Path,
    room_dir: Path,
    movement: dict[str, Any],
    argument_relations: dict[str, list[dict[str, str]]],
) -> tuple[str, list[Path]]:
    inputs: list[Path] = [movement["path"]]
    node = relative_link(room_dir, movement["path"], "movement")
    arguments = []
    for item in argument_relations[Path(movement["path"]).stem]:
        path = project / item["path"]
        inputs.append(path)
        arguments.append(relative_link(room_dir, path, item["title"]))
    source_ids = list(movement["source_ids"])
    known_sources = build_source_index(project)
    for target in re.findall(r"\[\[([^]|#]+)", movement["body"]):
        if target in known_sources and target not in source_ids:
            source_ids.append(target)
    source_paths = {source_id: source_file(project, source_id) for source_id in source_ids}
    inputs.extend(source_paths.values())
    passages: list[str] = []
    used_sources: set[str] = set()
    for quote_id in movement["quote_ids"]:
        source_id = next((sid for sid in source_paths if quote_id.startswith(f"{sid}-")), "")
        if not source_id:
            continue
        target = source_paths[source_id]
        if not has_fragment(target, quote_id):
            raise BuildError(f"source house lacks stable passage anchor #{quote_id}: {target}")
        anchor = f"#{quote_id}"
        passages.append(relative_link(room_dir, target, quote_id, anchor))
        used_sources.add(source_id)
    for source_id, target in source_paths.items():
        if source_id not in used_sources:
            passages.append(relative_link(room_dir, target, source_id))
    fields = [node]
    if arguments:
        fields.append("arguments: " + ", ".join(arguments))
    if passages:
        fields.append("sources: " + ", ".join(passages))
    return " · ".join(fields), inputs


def clean_title(value: str) -> str:
    return re.sub(r"^§[^·]+\s*·\s*#[^—]+—\s*", "", value).strip()


def render_room(
    project: Path,
    spec: RoomSpec,
    plan: dict[str, str],
    movements: list[dict[str, Any]],
    all_movements: list[dict[str, Any]],
    argument_relations: dict[str, list[dict[str, str]]],
) -> tuple[str, list[Path]]:
    room_dir = project / ROOM_ROOT / spec.slug
    start = movements[0]["sequence"] - 1
    prior = all_movements[start - 1] if start else None
    following = all_movements[start + 6] if start + 6 < len(all_movements) else None
    arrival = sentence_excerpt((prior or movements[0])["transition"] or (prior or movements[0])["claim"])
    release = sentence_excerpt(movements[-1]["transition"] or (following or movements[-1])["claim"])
    manuscript = project / MANUSCRIPT
    inputs: list[Path] = [
        project / "the-return-of-zero-central-plan.md",
        manuscript,
    ]
    lines = [
        "---",
        f'title: "{spec.station} Room — {spec.title}"',
        "page_type: section-room-waypoint",
        f'station: "{spec.station}"',
        f'room: "{spec.slug}"',
        f'generated_by: "build-section-rooms.py v{BUILDER_VERSION}"',
        "ownership: generated",
        "---",
        "",
        f"# {spec.station} — {spec.title}",
        "",
        f"**Write here:** {relative_link(room_dir, manuscript, 'sovereign master manuscript', '#' + spec.manuscript_anchor)}",
    ]
    reading = room_dir / "READING.md"
    scratch = room_dir / "SCRATCH.md"
    companions = []
    if reading.is_file():
        companions.append("[reading route](READING.md)")
        inputs.append(reading)
    if scratch.is_file():
        companions.append("[section scratchpad](SCRATCH.md)")
        inputs.append(scratch)
    if companions:
        lines.extend(["", "**Open beside it:** " + " · ".join(companions)])
    lines.extend(
        [
            "",
            "## Arrival",
            "",
            arrival,
            "",
            "## Section wager",
            "",
            sentence_excerpt(plan["claim"], maximum_sentences=2, maximum_words=72),
            "",
            f"**Present burden:** {sentence_excerpt(plan['burden'], maximum_sentences=1, maximum_words=55)}",
            "",
            "## Six waypoints",
            "",
        ]
    )
    for index, movement in enumerate(movements):
        previous = prior if index == 0 else movements[index - 1]
        if previous:
            incoming = relative_link(
                room_dir,
                previous["path"],
                f"{previous['station']} {previous['position']} · {clean_title(str(previous['title']))}",
            )
        else:
            incoming = "the opening question"
        earned = sentence_excerpt(movement["claim"], maximum_sentences=2, maximum_words=58)
        warrant = sentence_excerpt(movement["warrant"], maximum_sentences=1, maximum_words=48)
        outgoing = sentence_excerpt(movement["transition"] or (movements[index + 1]["claim"] if index < 5 else release))
        links, movement_inputs = movement_links(project, room_dir, movement, argument_relations)
        inputs.extend(movement_inputs)
        lines.extend(
            [
                f"### {movement['position']} · {clean_title(str(movement['title']))}",
                "",
                f"**Incoming pressure:** {incoming}",
                "",
                f"**Earned position ({movement['claim_status']}):** {earned}",
                "",
                *([f"**Why this move:** {warrant}", ""] if warrant else []),
                f"**Carry-forward:** {outgoing}",
                "",
                f"**Open:** {links}",
                "",
            ]
        )
    lines.extend(["## Release", "", release, ""])
    text = "\n".join(lines)
    word_count = len(re.findall(r"\b[^\s]+\b", re.sub(r"---.*?---", "", text, count=1, flags=re.DOTALL)))
    if not 500 <= word_count <= 900:
        raise BuildError(f"{spec.slug}/{ROOM_FILE} has {word_count} words; required range is 500–900")
    validate_links(project, room_dir, text)
    return text, sorted(set(inputs))


def root_readme() -> str:
    return """# Return of Zero — Section Rooms

The essay is written in [`THE-RETURN-OF-ZERO.md`](../THE-RETURN-OF-ZERO.md). These eight rooms are compact section-local waypoints into the canonical argument and source houses.

Each room requires only `ROOM.md`, which is generated and should not be edited. A room may also contain `READING.md` when cross-source order genuinely teaches the section, `SCRATCH.md` for temporary writing, or `VISUALS.md` for an admitted visual argument. Full quotation, source teaching, bibliographic detail and worked examples belong in the linked `SOURCE.md` houses.

```bash
python3 tools/build-section-rooms.py --project-root .
python3 tools/build-section-rooms.py --project-root . --check
```
"""


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def compare(path: Path, expected: str, stale: list[str], project: Path) -> None:
    if not path.is_file() or read_text(path) != expected:
        stale.append(path.relative_to(project).as_posix())


def validate_manuscript(project: Path) -> None:
    manuscript = project / MANUSCRIPT
    text = read_text(manuscript)
    for spec in ROOMS:
        marker = f'<a id="{spec.manuscript_anchor}"></a>'
        if text.count(marker) != 1:
            raise BuildError(f"master manuscript must contain one {marker}")


def build(project: Path, check: bool, selected_rooms: list[str] | None) -> None:
    validate_manuscript(project)
    plan_path = project / "the-return-of-zero-central-plan.md"
    plans = parse_plan(plan_path)
    all_movements = load_movements(project)
    relations = load_argument_relations(project, all_movements)
    known = {spec.slug for spec in ROOMS}
    selected = set(selected_rooms or known)
    unknown = selected - known
    if unknown:
        raise BuildError(f"unknown room slug(s): {', '.join(sorted(unknown))}")
    root = project / ROOM_ROOT
    stale: list[str] = []
    readme = root_readme()
    if check:
        compare(root / "README.md", readme, stale, project)
    else:
        atomic_write(root / "README.md", readme)
    for spec in ROOMS:
        if spec.slug not in selected:
            continue
        movements = [item for item in all_movements if item["station"] == spec.station]
        if len(movements) != 6:
            raise BuildError(f"{spec.station} has {len(movements)} movements; expected six")
        text, _inputs = render_room(project, spec, plans[spec.station], movements, all_movements, relations)
        room_dir = root / spec.slug
        if check:
            compare(room_dir / ROOM_FILE, text, stale, project)
        else:
            atomic_write(room_dir / ROOM_FILE, text)
    if stale:
        detail = "\n".join(f"  - {item}" for item in stale)
        raise BuildError(f"section rooms are stale or incomplete:\n{detail}")
    action = "Checked" if check else "Built"
    print(f"{action} {len(selected)} compact section room(s); manuscript and protected companions unchanged.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--room", action="append", dest="rooms")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        build(args.project_root.resolve(), args.check, args.rooms)
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
