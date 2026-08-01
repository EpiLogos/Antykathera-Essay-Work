#!/usr/bin/env python3
"""Build disposable human source projections from canonical SOURCE.md houses."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_resolver import iter_source_houses


SECTIONS = (
    ("§0/1", "Integral Threshold", "00-integral-threshold"),
    ("§0", "Differentiating Mind", "01-differentiating-mind"),
    ("§1", "Return of Zero", "02-return-of-zero"),
    ("§2", "Two Logics", "03-two-logics"),
    ("§3", "Mathematical Substrate", "04-mathematical-substrate"),
    ("§4", "Psychoid Flowering", "05-psychoid-flowering"),
    ("§5", "Objective Internality", "06-objective-internality"),
    ("§5→0", "Instrument Returns", "07-instrument-returns"),
)
SECTION_CODES = {code for code, _, _ in SECTIONS}
SECTION_RE = re.compile(r"§(?:0/1|5→0|[0-5])")
HEADING_RE = re.compile(r"(?m)^(#{2,6})\s+(.+?)\s*$")
FULL_PASSAGE_ID_RE = re.compile(
    r"(?i)([a-z0-9][a-z0-9-]*(?:-q\d{3,}|-p\d{3,}))"
)
SHORT_PASSAGE_ID_RE = re.compile(r"\b([A-Z]{2,}-\d{2,})\b")
OUTPUT_NAMES = ("MAIN-SOURCES.md", "SOURCE-INDEX.md", "PASSAGE-LEDGER.md")


def parse_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        raise ValueError(f"frontmatter is not a mapping: {path}")
    return data, text[match.end() :]


def heading_slug(value: str) -> str:
    value = re.sub(r"[*_`]", "", value).casefold()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def field_from_card(content: str, names: tuple[str, ...]) -> str:
    for name in names:
        match = re.search(
            rf"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?{re.escape(name)}\s*:\s*(?:\*\*)?\s*(.+?)\s*$",
            content,
        )
        if match:
            return match.group(1).strip().strip("`")
    return ""


def legacy_row_fields(content: str, passage_id: str) -> tuple[str, str, str]:
    for line in content.splitlines():
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[0] == passage_id:
            return cells[2], cells[3], cells[4]
    return "", "", ""


def source_provenance(body: str) -> str:
    match = re.search(
        r"(?im)^(?:access_provenance|edition_consulted|edition)\s*:\s*[\"']?(.+?)[\"']?\s*$",
        body,
    )
    return match.group(1).strip().strip("\"'") if match else ""


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    path: Path
    relative: str
    data: dict[str, Any]
    body: str
    sha256: str


@dataclass(frozen=True)
class Passage:
    passage_id: str
    source: Source
    heading: str
    anchor: str
    locator: str
    status: str
    provenance: str


def load_sources(root: Path) -> list[Source]:
    sources: list[Source] = []
    seen: dict[str, Path] = {}
    for path in iter_source_houses(root):
        if path.stat().st_size == 0:
            print(f"skipping empty intake stub: {path}", file=sys.stderr)
            continue
        data, body = parse_markdown(path)
        source_id = str(data.get("source_id") or "").strip()
        if not source_id:
            raise ValueError(f"SOURCE.md lacks source_id: {path}")
        if source_id in seen:
            raise ValueError(f"duplicate source_id {source_id}: {seen[source_id]} and {path}")
        seen[source_id] = path
        sources.append(
            Source(
                source_id=source_id,
                title=str(data.get("title") or source_id).removeprefix("Source House — "),
                path=path,
                relative=path.relative_to(root).as_posix(),
                data=data,
                body=body,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            )
        )
    if not sources:
        raise ValueError("no canonical SOURCE.md houses found")
    return sources


def passages(source: Source) -> list[Passage]:
    result: list[Passage] = []
    headings = list(HEADING_RE.finditer(source.body))
    default_status = str(
        source.data.get("quotation_status")
        or source.data.get("quote_status")
        or "unspecified"
    )
    anchors = re.finditer(
        r"(?i)<a\s+(?:[^>]*?\s)?id=[\"']([^\"']+)[\"'][^>]*></a>",
        source.body,
    )
    for anchor in anchors:
        passage_id = anchor.group(1)
        if not passage_id.casefold().startswith(source.source_id.casefold() + "-"):
            continue
        match = next((heading for heading in headings if heading.start() > anchor.end()), None)
        if not match:
            raise ValueError(f"passage anchor has no following heading: {source.source_id}#{passage_id}")
        level = len(match.group(1))
        end = len(source.body)
        for candidate in headings:
            if candidate.start() <= match.start():
                continue
            if len(candidate.group(1)) <= level:
                end = candidate.start()
                break
        card = source.body[match.end() : end].strip()
        row_locator, row_status, row_provenance = legacy_row_fields(source.body, passage_id)
        result.append(
            Passage(
                passage_id=passage_id,
                source=source,
                heading=match.group(2).replace("`", "").strip(),
                anchor=passage_id,
                locator=field_from_card(card, ("Locator", "Edition locator"))
                or row_locator,
                status=field_from_card(
                    card, ("Quotation status", "Quote status", "Status")
                )
                or row_status
                or default_status,
                provenance=field_from_card(
                    card,
                    ("Provenance", "Carrier", "Verification", "Access provenance"),
                )
                or row_provenance
                or source_provenance(source.body),
            )
        )
    return result


def header(title: str, digest: str) -> list[str]:
    return [
        "---",
        f'title: "{title}"',
        "generated: true",
        "generator: tools/build-source-projections.py",
        f'source_digest: "{digest}"',
        "---",
        "",
        "<!-- Generated from canonical SOURCE.md houses. Do not edit by hand. -->",
        "",
    ]


def source_link(output: Path, source: Source, fragment: str = "") -> str:
    rel = Path(os.path.relpath(source.path, output.parent)).as_posix()
    return rel + (f"#{fragment}" if fragment else "")


def render(root: Path) -> dict[Path, bytes]:
    sources = load_sources(root)
    digest = hashlib.sha256(
        "\n".join(f"{source.source_id}:{source.sha256}" for source in sources).encode()
    ).hexdigest()
    bank = root / "essay-workshop/sources-texts-references/source-bank"
    outputs = {name: bank / name for name in OUTPUT_NAMES}

    main_rows: dict[str, list[tuple[Source, str]]] = {code: [] for code in SECTION_CODES}
    invalid_relations: list[str] = []
    for source in sources:
        raw_relations = source.data.get("main_source_for") or []
        if isinstance(raw_relations, str):
            raw_relations = [raw_relations]
        for raw in raw_relations:
            match = SECTION_RE.search(str(raw))
            if not match or match.group(0) not in SECTION_CODES:
                invalid_relations.append(f"{source.source_id}: {raw}")
                continue
            main_rows[match.group(0)].append((source, str(raw)))
    if invalid_relations:
        raise ValueError("unresolved main_source_for relations: " + "; ".join(invalid_relations))
    empty_sections = [code for code, rows in main_rows.items() if not rows]
    if empty_sections:
        raise ValueError(
            "sections without a declared main source: " + ", ".join(sorted(empty_sections))
        )

    main = header("Return of Zero — Main Sources by Section", digest)
    main.extend(
        [
            "# Main Sources by Section",
            "",
            "Main source is a declared relation to an essay section, not a second copy of a work.",
            "",
        ]
    )
    for code, title, room in SECTIONS:
        room_path = root / f"essay-workshop/section-rooms/{room}/ROOM.md"
        room_rel = Path(os.path.relpath(room_path, outputs["MAIN-SOURCES.md"].parent)).as_posix()
        main.extend([f"## {code} — {title}", "", f"[Open section room]({room_rel})", ""])
        rows = sorted(main_rows[code], key=lambda row: (row[0].title.casefold(), row[0].source_id))
        if not rows:
            main.extend(["_No main source declared._", ""])
        for source, relation in rows:
            link = source_link(outputs["MAIN-SOURCES.md"], source)
            main.append(f"- [{source.title}]({link}) — `{source.source_id}` — {relation}")
        if rows:
            main.append("")

    index = header("Return of Zero — Canonical Source Index", digest)
    index.extend(["# Canonical Source Index", ""])
    for source in sorted(sources, key=lambda item: (item.title.casefold(), item.source_id)):
        link = source_link(outputs["SOURCE-INDEX.md"], source)
        status = source.data.get("citation_status") or source.data.get("bibliographic_status") or "unspecified"
        index.append(f"- [{source.title}]({link}) — `{source.source_id}` — {status}")
    index.append("")

    all_passages = [passage for source in sources for passage in passages(source)]
    duplicate_passages: dict[str, list[Passage]] = {}
    for passage in all_passages:
        duplicate_passages.setdefault(passage.passage_id, []).append(passage)
    duplicate_passages = {
        passage_id: rows
        for passage_id, rows in duplicate_passages.items()
        if len(rows) > 1
    }
    if duplicate_passages:
        detail = "; ".join(
            f"{passage_id}: {', '.join(row.source.source_id for row in rows)}"
            for passage_id, rows in sorted(duplicate_passages.items())
        )
        raise ValueError("duplicate passage IDs: " + detail)

    ledger = header("Return of Zero — Passage Locator Ledger", digest)
    ledger.extend(
        [
            "# Passage Locator Ledger",
            "",
            "This projection carries locators and statuses only. Passage text remains in its single canonical source house.",
            "",
            "| Passage ID | Source | Locator | Quotation state | Provenance |",
            "|---|---|---|---|---|",
        ]
    )
    for passage in sorted(all_passages, key=lambda item: item.passage_id):
        link = source_link(outputs["PASSAGE-LEDGER.md"], passage.source, passage.anchor)
        values = [passage.locator, passage.status, passage.provenance]
        values = [value.replace("|", "\\|").replace("\n", " ") or "—" for value in values]
        ledger.append(
            f"| [`{passage.passage_id}`]({link}) | `{passage.source.source_id}` | {values[0]} | {values[1]} | {values[2]} |"
        )
    ledger.append("")

    return {
        outputs["MAIN-SOURCES.md"]: "\n".join(main).encode("utf-8"),
        outputs["SOURCE-INDEX.md"]: "\n".join(index).encode("utf-8"),
        outputs["PASSAGE-LEDGER.md"]: "\n".join(ledger).encode("utf-8"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    try:
        expected = render(root)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    stale = [path for path, content in expected.items() if not path.exists() or path.read_bytes() != content]
    if args.check:
        if stale:
            for path in stale:
                print(f"stale:{path.relative_to(root)}", file=sys.stderr)
            return 1
        print(f"Source projections current: {len(expected)} files.")
        return 0
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temp:
            temp.write(content)
            temp_path = Path(temp.name)
        temp_path.replace(path)
    print(f"Built {len(expected)} source projections.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
