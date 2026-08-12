#!/usr/bin/env python3
"""Read-only Return of Zero workspace graph and retrieval CLI.

The canonical Markdown files remain authoritative. This tool discovers their
typed relations, resolves links, and assembles traceable working contexts. It
never rewrites canonical material or treats a generated index as authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


WIKILINK_RE = re.compile(r"(?<!\\)\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
WORD_RE = re.compile(r"[\wÀ-žĀ-ſḀ-ỿŚśṢṣṚṛṜṝṆṇÑñĪīŪūĀāḷḹ]+", re.UNICODE)

EXCLUDED_PARTS = {
    ".git",
    ".bkmr",
    "__pycache__",
    "node_modules",
    "legacy",
    "build",
    "dist",
}

AUTHORITY_ORDER = {
    "governing-document": "governing",
    "section": "canonical-argument",
    "argument": "canonical-argument",
    "argument-map": "canonical-argument",
    "concept": "canonical-argument",
    "path": "canonical-argument",
    "source-house": "source-authority",
    "source-notes": "authorial-notes",
    "room-reading-path": "learning-refraction",
    "quote-index": "generated-locator",
    "room-artifact": "authoring-refraction",
    "plan": "development-plan",
    "skill": "development-method",
    "submission-artifact": "submission-refraction",
    "source-governance": "source-authority",
    "index": "locator",
    "document": "supporting-document",
    "legacy-reference": "frozen-provenance",
}


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def strip_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    match = re.match(r"^---\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data, text[match.end() :]


def scalar_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from scalar_strings(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            yield from scalar_strings(item)


def markdown_targets(text: str) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    for match in WIKILINK_RE.finditer(text):
        raw = match.group(1)
        target = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if target:
            targets.append((target, "wikilink"))
    for match in MARKDOWN_LINK_RE.finditer(text):
        target = match.group(2).strip().strip("<>")
        if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        target = target.split("#", 1)[0]
        if target:
            targets.append((target, "markdown-link"))
    return targets


def markdown_fragment_targets(text: str) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    for match in WIKILINK_RE.finditer(text):
        raw = match.group(1).split("|", 1)[0].strip()
        path, marker, fragment = raw.partition("#")
        if marker and path.strip() and fragment.strip():
            targets.append((path.strip(), fragment.strip()))
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw = match.group(2).strip().strip("<>")
        if raw.startswith(("http://", "https://", "mailto:", "data:")):
            continue
        path, marker, fragment = raw.partition("#")
        if marker and path.strip() and fragment.strip():
            targets.append((path.strip(), fragment.strip()))
    return targets


def classify(rel: Path, fm: dict[str, Any]) -> str:
    posix = rel.as_posix()
    name = rel.name
    declared = str(fm.get("node_type") or fm.get("type") or fm.get("page_type") or "").casefold()

    if posix in {
        "the-return-of-zero-central-plan.md",
        "return-of-zero-orienting-principles.md",
    }:
        return "governing-document"
    if "/nodes/sections/" in f"/{posix}" or (
        "/section-rooms/" in f"/{posix}" and "/movements/" in f"/{posix}"
    ):
        return "section"
    if "/nodes/arguments/" in f"/{posix}" or "/section-rooms/arguments/" in f"/{posix}":
        return "argument"
    if "/nodes/concepts/" in f"/{posix}" or (
        "/symbolon/episteme/concepts/" in f"/{posix}"
        and "/reference-notes/" not in f"/{posix}"
    ):
        if name in {"index.md", "README.md"}:
            return "index" if name == "index.md" else "document"
        return "concept"
    if "/nodes/paths/" in f"/{posix}" or (
        "/symbolon/episteme/maps/" in f"/{posix}" and name != "README.md"
    ):
        return "path"
    if (
        ("/source-bank/sources/" in f"/{posix}" or "/episteme/sources/" in f"/{posix}")
        and name == "SOURCE.md"
        and fm.get("source_id")
    ):
        return "source-house"
    if (
        ("/source-bank/sources/" in f"/{posix}" or "/episteme/sources/" in f"/{posix}")
        and name == "NOTES.md"
    ):
        return "source-notes"
    if "/source-bank/" in f"/{posix}" or "/episteme/sources/" in f"/{posix}":
        return "source-governance"
    if "/symbolon/episteme/concepts/reference-notes/" in f"/{posix}":
        return "legacy-reference"
    if "/section-rooms/" in f"/{posix}" and declared in {
        "room-reading-path",
        "room-reading-route",
    }:
        return "room-reading-path"
    if "/section-rooms/" in f"/{posix}":
        return "room-artifact"
    if posix.startswith("docs/plans/"):
        return "plan"
    if name == "SKILL.md" or "/.agents/skills/" in f"/{posix}":
        return "skill"
    if posix.startswith("submission-package/"):
        return "submission-artifact"
    if declared in {"section", "section-movement"}:
        return "section"
    if declared in {"claim", "synthesis", "warrant", "question"}:
        return "argument"
    if declared == "argument-map":
        return "argument-map"
    if declared == "concept":
        return "concept"
    if declared in {"path", "braid"}:
        return "path"
    return "document"


def primary_id(rel: Path, fm: dict[str, Any], artifact_type: str) -> str:
    if artifact_type == "source-house" and fm.get("source_id"):
        return str(fm["source_id"])
    if artifact_type == "source-notes":
        return f"notes-{rel.parent.name}"
    if artifact_type == "room-reading-path":
        return str(fm.get("reading_path_id") or f"reading-{rel.parent.name}")
    if artifact_type == "room-artifact" and rel.name == "ROOM.md":
        return f"room-{rel.parent.name}"
    return rel.stem


def title_for(rel: Path, fm: dict[str, Any], body: str) -> str:
    if fm.get("title"):
        return str(fm["title"])
    heading = HEADING_RE.search(body)
    if heading:
        return re.sub(r"[*_`]", "", heading.group(1)).strip()
    return rel.stem.replace("-", " ").strip().title()


@dataclass
class Artifact:
    path: str
    abs_path: Path
    artifact_type: str
    authority: str
    id: str
    title: str
    aliases: list[str]
    frontmatter: dict[str, Any]
    body: str
    headings: list[str]
    sha256: str
    outgoing: list["Edge"] = field(default_factory=list)

    def status(self, key: str) -> Any:
        return self.frontmatter.get(key)

    def compact(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "title": self.title,
            "path": self.path,
            "artifact_type": self.artifact_type,
            "authority": self.authority,
            "headings": self.headings,
            "sha256": self.sha256,
        }
        for key in (
            "claim_status",
            "evidence_status",
            "citation_status",
            "quote_status",
            "quotation_status",
            "source_status",
            "bibliographic_status",
            "study_status",
            "locator",
            "main_source_for",
            "station",
            "position",
            "sequence",
            "coordinates",
            "register",
            "tags",
        ):
            if key in self.frontmatter:
                result[key] = self.frontmatter[key]
        return result


@dataclass(frozen=True)
class Edge:
    source: str
    target: str | None
    raw_target: str
    relation: str
    origin: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "raw_target": self.raw_target,
            "relation": self.relation,
            "origin": self.origin,
            "resolved": self.target is not None,
        }


@dataclass(frozen=True)
class Passage:
    passage_id: str
    source_id: str
    canonical_path: str
    title: str
    locator: str
    quotation_status: str
    provenance: str
    content: str

    def compact(self) -> dict[str, Any]:
        return {
            "passage_id": self.passage_id,
            "source_id": self.source_id,
            "canonical_path": self.canonical_path,
            "anchor": f"#{self.passage_id}",
            "title": self.title,
            "locator": self.locator,
            "quotation_status": self.quotation_status,
            "provenance": self.provenance,
        }


def heading_slug(value: str) -> str:
    value = re.sub(r"[*_`]", "", value).casefold()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", value).strip("-")


class Workspace:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.artifacts: dict[str, Artifact] = {}
        self.lookup: dict[str, list[str]] = defaultdict(list)
        self.passages: dict[str, list[Passage]] = defaultdict(list)
        self.quote_passage_lookup: dict[str, str] = {}
        self.incoming: dict[str, list[Edge]] = defaultdict(list)
        self._discover()
        self._build_lookup()
        self._build_passage_lookup()
        self._build_edges()

    def _discover(self) -> None:
        markdown_paths = sorted(self.root.rglob("*.md"))
        for path in markdown_paths:
            rel = path.relative_to(self.root)
            if any(
                part in EXCLUDED_PARTS or part.startswith(".legacy")
                for part in rel.parts
            ):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except FileNotFoundError:
                continue
            fm, body = strip_frontmatter(text)
            artifact_type = classify(rel, fm)
            posix = rel.as_posix()
            source_id = str(fm.get("source_id") or "")
            ident = primary_id(rel, fm, artifact_type)
            aliases = [str(value) for value in fm.get("aliases", [])] if isinstance(fm.get("aliases"), list) else []
            source_aliases = fm.get("source_id_aliases") or []
            if isinstance(source_aliases, str):
                source_aliases = [source_aliases]
            aliases.extend(str(value) for value in source_aliases)
            artifact = Artifact(
                path=rel.as_posix(),
                abs_path=path,
                artifact_type=artifact_type,
                authority=AUTHORITY_ORDER.get(artifact_type, "supporting-document"),
                id=ident,
                title=title_for(rel, fm, body),
                aliases=aliases,
                frontmatter=fm,
                body=body,
                headings=[re.sub(r"[*_`]", "", h).strip() for h in HEADING_RE.findall(body)],
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            self.artifacts[artifact.path] = artifact

    def _add_lookup(self, key: str, path: str) -> None:
        norm = normalise(key)
        if norm and path not in self.lookup[norm]:
            self.lookup[norm].append(path)

    def _build_lookup(self) -> None:
        for artifact in self.artifacts.values():
            rel = Path(artifact.path)
            for key in {
                artifact.id,
                artifact.title,
                rel.stem,
                artifact.path,
                artifact.path.removesuffix(".md"),
                *artifact.aliases,
            }:
                self._add_lookup(key, artifact.path)
            source_id = artifact.frontmatter.get("source_id")
            if source_id:
                self._add_lookup(str(source_id), artifact.path)

    def _canonicalise_source_path(self, path: str) -> str:
        return path

    @staticmethod
    def _field_from_card(content: str, names: tuple[str, ...]) -> str:
        for name in names:
            match = re.search(
                rf"(?im)^\s*(?:[-*]\s*)?(?:\*\*)?{re.escape(name)}\s*:\s*(?:\*\*)?\s*(.+?)\s*$",
                content,
            )
            if match:
                return match.group(1).strip().strip("`")
        return ""

    @staticmethod
    def _legacy_row_fields(content: str, passage_id: str) -> tuple[str, str, str]:
        for line in content.splitlines():
            cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
            if len(cells) >= 5 and cells[0] == passage_id:
                return cells[2], cells[3], cells[4]
        return "", "", ""

    @staticmethod
    def _source_provenance(body: str) -> str:
        match = re.search(
            r"(?im)^(?:access_provenance|edition_consulted|edition)\s*:\s*[\"']?(.+?)[\"']?\s*$",
            body,
        )
        return match.group(1).strip().strip("\"'") if match else ""

    def _build_passage_lookup(self) -> None:
        for artifact in self.artifacts.values():
            if artifact.artifact_type != "source-house":
                continue
            headings = list(re.finditer(r"(?m)^(#{2,6})\s+(.+?)\s*$", artifact.body))
            source_id = str(artifact.frontmatter.get("source_id") or artifact.id)
            default_status = str(
                artifact.frontmatter.get("quotation_status")
                or artifact.frontmatter.get("quote_status")
                or "unspecified"
            )
            candidates: list[tuple[str, re.Match[str]]] = []
            anchors = re.finditer(
                r"(?i)<a\s+(?:[^>]*?\s)?id=[\"']([^\"']+)[\"'][^>]*></a>",
                artifact.body,
            )
            for anchor in anchors:
                passage_id = anchor.group(1)
                if not passage_id.casefold().startswith(source_id.casefold() + "-"):
                    continue
                match = next((heading for heading in headings if heading.start() > anchor.end()), None)
                if match:
                    candidates.append((passage_id, match))

            for passage_id, match in candidates:
                level = len(match.group(1))
                end = len(artifact.body)
                for candidate in headings:
                    if candidate.start() <= match.start():
                        continue
                    if len(candidate.group(1)) <= level:
                        end = candidate.start()
                        break
                content = artifact.body[match.end() : end].strip()
                row_locator, row_status, row_provenance = self._legacy_row_fields(
                    artifact.body, passage_id
                )
                passage = Passage(
                    passage_id=passage_id,
                    source_id=source_id,
                    canonical_path=artifact.path,
                    title=re.sub(r"`", "", match.group(2)).strip(),
                    locator=self._field_from_card(content, ("Locator", "Edition locator"))
                    or row_locator,
                    quotation_status=self._field_from_card(
                        content, ("Quotation status", "Quote status", "Status")
                    )
                    or row_status
                    or default_status,
                    provenance=self._field_from_card(
                        content,
                        ("Provenance", "Carrier", "Verification", "Access provenance"),
                    )
                    or row_provenance
                    or self._source_provenance(artifact.body),
                    content=content,
                )
                self.passages[passage_id].append(passage)

        for passage_id, candidates in self.passages.items():
            preferred = sorted(
                candidates,
                key=lambda passage: (
                    self.artifacts[passage.canonical_path].artifact_type != "source-house",
                    passage.canonical_path,
                ),
            )[0]
            self.quote_passage_lookup[passage_id] = preferred.canonical_path

    def passage(self, passage_id: str) -> Passage | None:
        candidates = self.passages.get(passage_id, [])
        if not candidates:
            return None
        return sorted(
            candidates,
            key=lambda passage: (
                self.artifacts[passage.canonical_path].artifact_type != "source-house",
                passage.canonical_path,
            ),
        )[0]

    @staticmethod
    def _has_fragment(artifact: Artifact, fragment: str) -> bool:
        expected = fragment.casefold().lstrip("#")
        heading_anchors = {heading_slug(heading) for heading in artifact.headings}
        explicit_anchors = {
            match.casefold()
            for match in re.findall(
                r"(?i)<a\s+(?:[^>]*?\s)?(?:id|name)=[\"']([^\"']+)[\"']",
                artifact.body,
            )
        }
        return expected in heading_anchors or expected in explicit_anchors

    def _resolve(self, raw: str, source: Artifact | None = None, preferred: str | None = None) -> str | None:
        cleaned = raw.strip().strip("<>").replace("\\", "")
        if not cleaned:
            return None
        cleaned = cleaned.split("#", 1)[0]
        if cleaned.endswith(".md") or "/" in cleaned:
            if source:
                candidate_abs = (source.abs_path.parent / cleaned).resolve()
                try:
                    candidate = candidate_abs.relative_to(self.root).as_posix()
                except ValueError:
                    candidate = ""
                if candidate in self.artifacts:
                    return self._canonicalise_source_path(candidate)
            direct = cleaned.lstrip("./")
            if direct in self.artifacts:
                return self._canonicalise_source_path(direct)
            if not direct.endswith(".md") and f"{direct}.md" in self.artifacts:
                return self._canonicalise_source_path(f"{direct}.md")
        candidates = self.lookup.get(normalise(Path(cleaned).stem), [])
        if not candidates:
            candidates = self.lookup.get(normalise(cleaned), [])
        if not candidates:
            return None
        if preferred:
            preferred_matches = [p for p in candidates if self.artifacts[p].artifact_type == preferred]
            if preferred_matches:
                return sorted(preferred_matches)[0]
            if preferred == "source-house":
                legacy_matches = [
                    p for p in candidates if self.artifacts[p].artifact_type == "source-record"
                ]
                if legacy_matches:
                    return sorted(legacy_matches)[0]
        priority = {
            "argument": 0,
            "section": 1,
            "concept": 2,
            "source-house": 3,
            "source-record": 4,
            "quote-dossier": 5,
            "source-study": 6,
            "room-reading-path": 7,
            "path": 6,
            "governing-document": 7,
            "room-artifact": 8,
            "legacy-reference": 9,
            "document": 10,
        }
        return self._canonicalise_source_path(
            sorted(candidates, key=lambda p: (priority.get(self.artifacts[p].artifact_type, 10), p))[0]
        )

    def resolve(self, raw: str, preferred: str | None = None) -> Artifact:
        passage = self.passage(raw)
        if passage:
            return self.artifacts[passage.canonical_path]
        path = self._resolve(raw, preferred=preferred)
        if not path:
            raise KeyError(f"No artifact resolves from: {raw}")
        return self.artifacts[path]

    def _relation_for_body_target(self, body: str, target: str, origin: str) -> str:
        index = body.find(f"[[{target}")
        context = body[max(0, index - 100) : index + len(target) + 40].casefold() if index >= 0 else ""
        if "depends on:" in context:
            return "depends-on"
        if "related:" in context or "related to:" in context:
            return "related"
        if "transition" in context or "opens" in context:
            return "opens-to"
        return origin

    def _edge(self, source: Artifact, raw: str, relation: str, origin: str, preferred: str | None = None) -> Edge:
        target = self._resolve(raw, source=source, preferred=preferred)
        return Edge(source.path, target, raw, relation, origin)

    def _quote_dossier_for(self, quote_id: str) -> str | None:
        return self.quote_passage_lookup.get(quote_id)

    def _build_edges(self) -> None:
        for artifact in self.artifacts.values():
            edges: list[Edge] = []
            seen: set[tuple[str | None, str, str]] = set()

            for raw, origin in markdown_targets(artifact.body):
                relation = self._relation_for_body_target(artifact.body, raw, origin)
                edge = self._edge(artifact, raw, relation, origin)
                key = (edge.target, edge.raw_target, edge.relation)
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)

            for raw_text in scalar_strings(artifact.frontmatter):
                for raw, origin in markdown_targets(raw_text):
                    edge = self._edge(artifact, raw, "frontmatter-link", origin)
                    key = (edge.target, edge.raw_target, edge.relation)
                    if key not in seen:
                        seen.add(key)
                        edges.append(edge)

            source_ids = artifact.frontmatter.get("source_ids") or []
            if isinstance(source_ids, str):
                source_ids = [source_ids]
            for source_id in source_ids:
                edge = self._edge(artifact, str(source_id), "supported-by", "source_ids", preferred="source-house")
                key = (edge.target, edge.raw_target, edge.relation)
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)

            movement_ids = artifact.frontmatter.get("movement_ids") or []
            if isinstance(movement_ids, str):
                movement_ids = [movement_ids]
            for movement_id in movement_ids:
                edge = self._edge(
                    artifact,
                    str(movement_id),
                    "consumed-by",
                    "movement_ids",
                    preferred="section",
                )
                key = (edge.target, edge.raw_target, edge.relation)
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)

            consumed_by_arguments = artifact.frontmatter.get("consumed_by_arguments") or []
            if isinstance(consumed_by_arguments, str):
                consumed_by_arguments = [consumed_by_arguments]
            for argument_id in consumed_by_arguments:
                edge = self._edge(
                    artifact,
                    str(argument_id),
                    "consumed-by",
                    "consumed_by_arguments",
                    preferred="argument",
                )
                key = (edge.target, edge.raw_target, edge.relation)
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)

            quote_ids = artifact.frontmatter.get("quote_ids") or []
            if isinstance(quote_ids, str):
                quote_ids = [quote_ids]
            for quote_id in quote_ids:
                raw_quote_id = str(quote_id)
                edge = Edge(
                    artifact.path,
                    self._quote_dossier_for(raw_quote_id),
                    raw_quote_id,
                    "uses-passage",
                    "quote_ids",
                )
                key = (edge.target, edge.raw_target, edge.relation)
                if key not in seen:
                    seen.add(key)
                    edges.append(edge)

            if artifact.artifact_type == "source-house":
                notes_path = Path(artifact.path).with_name("NOTES.md").as_posix()
                if notes_path in self.artifacts:
                    edge = Edge(
                        artifact.path,
                        notes_path,
                        notes_path,
                        "has-notes",
                        "source-companion",
                    )
                    key = (edge.target, edge.raw_target, edge.relation)
                    if key not in seen:
                        seen.add(key)
                        edges.append(edge)
            elif artifact.artifact_type == "source-notes":
                source_path = Path(artifact.path).with_name("SOURCE.md").as_posix()
                if source_path in self.artifacts:
                    edge = Edge(
                        artifact.path,
                        source_path,
                        source_path,
                        "notes-for",
                        "source-companion",
                    )
                    key = (edge.target, edge.raw_target, edge.relation)
                    if key not in seen:
                        seen.add(key)
                        edges.append(edge)

            artifact.outgoing = edges
            for edge in edges:
                if edge.target:
                    self.incoming[edge.target].append(edge)

    def node(self, artifact: Artifact) -> dict[str, Any]:
        return artifact.compact()

    def canonical_source_artifacts(self) -> list[Artifact]:
        """Return the canonical source files, one per source_id."""
        return sorted(
            (
                artifact
                for artifact in self.artifacts.values()
                if artifact.artifact_type == "source-house"
            ),
            key=lambda artifact: artifact.id,
        )

    def status(self) -> dict[str, Any]:
        counts = Counter(a.artifact_type for a in self.artifacts.values())
        authorities = Counter(a.authority for a in self.artifacts.values())
        canonical_register_types = {"section", "argument", "concept", "path", "argument-map"}
        register_canonical = [
            artifact
            for artifact in self.artifacts.values()
            if artifact.artifact_type in canonical_register_types
        ]
        registers = Counter(
            str(artifact.frontmatter.get("register") or "undeclared")
            for artifact in register_canonical
        )
        declared = [
            artifact
            for artifact in register_canonical
            if artifact.frontmatter.get("register")
        ]
        return {
            "project_root": str(self.root),
            "artifact_count": len(self.artifacts),
            "canonical_source_count": len(self.canonical_source_artifacts()),
            "passage_count": len(self.passages),
            "counts": dict(sorted(counts.items())),
            "authority_classes": dict(sorted(authorities.items())),
            "registers": dict(sorted(registers.items())),
            "register_census": {
                "canonical_nodes": len(register_canonical),
                "declared": len(declared),
                "missing": len(register_canonical) - len(declared),
                "missing_paths": sorted(
                    artifact.path
                    for artifact in register_canonical
                    if not artifact.frontmatter.get("register")
                ),
            },
        }

    def find(self, query: str, limit: int, register: str | None = None) -> dict[str, Any]:
        query_fold = query.casefold().strip()
        terms = [term.casefold() for term in WORD_RE.findall(query)]
        hits: list[tuple[float, Artifact, list[str], str]] = []
        for artifact in self.artifacts.values():
            if artifact.artifact_type == "submission-artifact":
                continue
            if register:
                declared = str(artifact.frontmatter.get("register") or "")
                if normalise(declared) != normalise(register):
                    continue
            fields = {
                "title": artifact.title,
                "aliases": " ".join(artifact.aliases),
                "body": artifact.body,
                "frontmatter": json.dumps(artifact.frontmatter, ensure_ascii=False, default=str),
            }
            matched: list[str] = []
            score = {
                "governing": 20.0,
                "canonical-argument": 18.0,
                "source-authority": 10.0,
                "quotation-authority": 10.0,
                "learning-refraction": 7.0,
                "authoring-refraction": 5.0,
                "frozen-provenance": -20.0,
            }.get(artifact.authority, 0.0)
            excerpt = ""
            for name, value in fields.items():
                folded = value.casefold()
                if query_fold and query_fold in folded:
                    matched.append(name)
                    score += {"title": 30, "aliases": 20, "body": 15, "frontmatter": 8}[name]
                    if name == "body":
                        pos = folded.index(query_fold)
                        excerpt = re.sub(r"\s+", " ", value[max(0, pos - 100) : pos + len(query) + 180]).strip()
                term_hits = sum(min(folded.count(term), 3) for term in terms)
                if term_hits:
                    score += term_hits * {"title": 5, "aliases": 4, "body": 1, "frontmatter": 0.5}[name]
                    if name not in matched:
                        matched.append(name)
            if matched:
                hits.append((score, artifact, matched, excerpt))
        hits.sort(key=lambda row: (-row[0], row[1].path))
        return {
            "query": query,
            "search_scope": "canonical-full-body",
            "register": register,
            "hits": [
                {
                    **artifact.compact(),
                    "score": score,
                    "matched_fields": matched,
                    "excerpt": excerpt,
                }
                for score, artifact, matched, excerpt in hits[:limit]
            ],
        }

    def links(self, artifact: Artifact) -> dict[str, Any]:
        return {"root": artifact.compact(), "edges": [edge.as_dict() for edge in artifact.outgoing]}

    def backlinks(self, artifact: Artifact) -> dict[str, Any]:
        return {"root": artifact.compact(), "edges": [edge.as_dict() for edge in self.incoming[artifact.path]]}

    def neighbours(self, path: str) -> list[tuple[str, Edge]]:
        result: list[tuple[str, Edge]] = []
        for edge in self.artifacts[path].outgoing:
            if edge.target:
                result.append((edge.target, edge))
        for edge in self.incoming[path]:
            result.append((edge.source, edge))
        return result

    def neighbourhood(self, artifact: Artifact, depth: int) -> dict[str, Any]:
        distance = {artifact.path: 0}
        queue = deque([artifact.path])
        traversed: list[dict[str, Any]] = []
        while queue:
            current = queue.popleft()
            if distance[current] >= depth:
                continue
            for neighbour, edge in self.neighbours(current):
                traversed.append(edge.as_dict())
                if neighbour not in distance:
                    distance[neighbour] = distance[current] + 1
                    queue.append(neighbour)
        nodes = []
        for path, dist in sorted(distance.items(), key=lambda item: (item[1], item[0])):
            node = self.artifacts[path].compact()
            node["distance"] = dist
            nodes.append(node)
        return {"root": artifact.compact(), "depth": depth, "nodes": nodes, "edges": traversed}

    def working_neighbourhood(self, artifact: Artifact, depth: int) -> dict[str, Any]:
        """Build a bounded authoring set without traversing through authority hubs.

        The entry node may discover both its links and direct consumers. Beyond
        that first hop, traversal follows outgoing relations only and expands
        canonical graph nodes only. Governing documents, canonical sources,
        and rooms remain visible as context but cannot flood the set with every
        object they index.
        """
        # Path nodes are useful maps but are intentionally terminal here: a
        # braided traversal can index the entire essay and would otherwise turn
        # a local context request back into a vault dump.
        # Learning surfaces are bounded curations rather than authority hubs,
        # so expanding them one hop exposes their exact source and passage
        # contract without flooding a local context with the whole vault.
        expandable = {
            "section",
            "argument",
            "argument-map",
            "concept",
            "room-reading-path",
        }
        distance = {artifact.path: 0}
        queue = deque([artifact.path])
        traversed: list[dict[str, Any]] = []
        while queue:
            current = queue.popleft()
            current_distance = distance[current]
            if current_distance >= depth:
                continue
            current_artifact = self.artifacts[current]
            if current != artifact.path and current_artifact.artifact_type not in expandable:
                continue
            if current == artifact.path:
                candidates = self.neighbours(current)
            else:
                candidates = [
                    (edge.target, edge)
                    for edge in current_artifact.outgoing
                    if edge.target is not None
                ]
            for neighbour, edge in candidates:
                if neighbour is None:
                    continue
                traversed.append(edge.as_dict())
                if neighbour not in distance:
                    distance[neighbour] = current_distance + 1
                    queue.append(neighbour)
        nodes = []
        for path, dist in sorted(distance.items(), key=lambda item: (item[1], item[0])):
            node = self.artifacts[path].compact()
            node["distance"] = dist
            nodes.append(node)
        return {"root": artifact.compact(), "depth": depth, "nodes": nodes, "edges": traversed}

    def path(self, start: Artifact, end: Artifact, max_depth: int) -> dict[str, Any]:
        queue = deque([start.path])
        previous: dict[str, tuple[str, Edge] | None] = {start.path: None}
        depth = {start.path: 0}
        while queue:
            current = queue.popleft()
            if current == end.path:
                break
            if depth[current] >= max_depth:
                continue
            for neighbour, edge in self.neighbours(current):
                if neighbour not in previous:
                    previous[neighbour] = (current, edge)
                    depth[neighbour] = depth[current] + 1
                    queue.append(neighbour)
        if end.path not in previous:
            return {"found": False, "start": start.compact(), "end": end.compact(), "path": [], "edges": []}
        paths = []
        edges = []
        cursor = end.path
        while cursor != start.path:
            paths.append(cursor)
            prior, edge = previous[cursor]  # type: ignore[misc]
            edges.append(edge.as_dict())
            cursor = prior
        paths.append(start.path)
        paths.reverse()
        edges.reverse()
        return {
            "found": True,
            "start": start.compact(),
            "end": end.compact(),
            "path": [self.artifacts[p].compact() for p in paths],
            "edges": edges,
        }

    def trace(self, artifact: Artifact) -> dict[str, Any]:
        dependencies: dict[str, Artifact] = {}
        sources: dict[str, Artifact] = {}
        related: dict[str, Artifact] = {}
        unresolved = []
        for edge in artifact.outgoing:
            if not edge.target:
                unresolved.append(edge.as_dict())
                continue
            target = self.artifacts[edge.target]
            if target.artifact_type == "source-house":
                sources[target.path] = target
            elif edge.relation == "depends-on":
                dependencies[target.path] = target
            else:
                related[target.path] = target
        return {
            "root": artifact.compact(),
            "dependencies": [a.compact() for a in dependencies.values()],
            "sources": [a.compact() for a in sources.values()],
            "related": [a.compact() for a in related.values()],
            "unresolved": unresolved,
        }

    def context(self, artifact: Artifact, depth: int) -> dict[str, Any]:
        neighbourhood = self.working_neighbourhood(artifact, depth)
        nodes = [self.artifacts[node["path"]] for node in neighbourhood["nodes"]]

        def of_type(kind: str) -> list[dict[str, Any]]:
            return [node.compact() for node in nodes if node.artifact_type == kind and node.path != artifact.path]

        source_nodes: dict[str, Artifact] = {}
        for node in nodes:
            if node.artifact_type != "source-house":
                continue
            source_nodes[node.id] = node

        previous = next_node = None
        sequence = artifact.frontmatter.get("sequence")
        if isinstance(sequence, int):
            for candidate in self.artifacts.values():
                if candidate.artifact_type != "section":
                    continue
                if candidate.frontmatter.get("sequence") == sequence - 1:
                    previous = candidate.compact()
                elif candidate.frontmatter.get("sequence") == sequence + 1:
                    next_node = candidate.compact()

        status_axes: dict[str, list[Any]] = {}
        for key in (
            "claim_status",
            "evidence_status",
            "citation_status",
            "quote_status",
            "source_status",
            "register",
        ):
            values = []
            for node in nodes:
                value = node.frontmatter.get(key)
                if value is not None and value not in values:
                    values.append(value)
            status_axes[key] = values

        passages: list[dict[str, Any]] = []
        seen_passages: set[tuple[str, str]] = set()
        for edge in neighbourhood["edges"]:
            if edge["relation"] != "uses-passage" or not edge["target"]:
                continue
            key = (edge["raw_target"], edge["target"])
            if key in seen_passages:
                continue
            seen_passages.add(key)
            passage = self.passage(edge["raw_target"])
            passages.append(
                {
                    "quote_id": edge["raw_target"],
                    "passage_id": edge["raw_target"],
                    "canonical": passage.compact() if passage else None,
                    "source": self.artifacts[edge["target"]].compact(),
                    "relation": "uses-passage",
                }
            )

        return {
            "entry": artifact.compact(),
            "register": str(artifact.frontmatter.get("register") or "undeclared"),
            "previous": previous,
            "next": next_node,
            "arguments": of_type("argument"),
            "concepts": of_type("concept"),
            "sections": of_type("section"),
            "sources": [node.compact() for _, node in sorted(source_nodes.items())],
            "source_notes": of_type("source-notes"),
            "passages": passages,
            "reading_paths": of_type("room-reading-path"),
            "rooms": of_type("room-artifact"),
            "governing_documents": [
                node.compact()
                for node in self.artifacts.values()
                if node.artifact_type == "governing-document"
            ],
            "trace": neighbourhood["edges"],
            "authority": artifact.authority,
            "status_axes": status_axes,
            "context_debts": [
                edge.as_dict()
                for node in nodes
                for edge in node.outgoing
                if edge.target is None
            ],
        }

    def effects(self, artifact: Artifact, depth: int) -> dict[str, Any]:
        """Map the canonical consequences of a source, concept, or argument.

        This deliberately follows declared graph relations and transverse-thread
        metadata. It does not infer a relation from shared vocabulary.
        """
        canonical_types = {"section", "argument", "concept", "path"}
        direct_paths = {
            edge.target
            for edge in artifact.outgoing
            if edge.target and self.artifacts[edge.target].artifact_type in canonical_types
        }
        distance = {artifact.path: 0}
        queue = deque([artifact.path])
        traversed: list[dict[str, Any]] = []
        while queue:
            current = queue.popleft()
            current_distance = distance[current]
            if current_distance >= depth:
                continue
            for edge in self.artifacts[current].outgoing:
                if not edge.target:
                    continue
                target = self.artifacts[edge.target]
                if target.artifact_type not in canonical_types:
                    continue
                traversed.append(edge.as_dict())
                if edge.target not in distance:
                    distance[edge.target] = current_distance + 1
                    queue.append(edge.target)

        thread_ids: set[str] = set()
        for path in distance:
            declared = self.artifacts[path].frontmatter.get("transverse_threads", [])
            if isinstance(declared, str):
                declared = [declared]
            thread_ids.update(str(item) for item in declared)
        threads = [
            candidate.compact()
            for candidate in self.artifacts.values()
            if candidate.frontmatter.get("thread_id") in thread_ids
            and not (
                candidate.path.startswith("submission-package/")
                and not candidate.path.startswith("submission-package/essay/")
            )
        ]
        consumers = {
            f"{kind}s": [
                self.artifacts[path].compact()
                for path in sorted(direct_paths)
                if self.artifacts[path].artifact_type == kind
            ]
            for kind in ("section", "argument", "concept", "path")
        }
        downstream_paths = [
            self.artifacts[path].compact()
            for path in sorted(distance, key=lambda item: (distance[item], item))
            if path != artifact.path
        ]
        return {
            "root": artifact.compact(),
            "method": "declared canonical graph and transverse-thread metadata only",
            "depth": depth,
            "consumers": consumers,
            "downstream": {"paths": downstream_paths, "edges": traversed},
            "transverse_threads": threads,
            "registers": {
                "root": str(artifact.frontmatter.get("register") or "undeclared"),
                "carriers": [
                    {
                        "path": path,
                        "register": str(
                            self.artifacts[path].frontmatter.get("register") or "undeclared"
                        ),
                    }
                    for path in sorted(distance, key=lambda item: (distance[item], item))
                    if path != artifact.path
                ],
            },
        }

    @staticmethod
    def _has_heading_surface(artifact: Artifact, terms: tuple[str, ...]) -> bool:
        headings = [normalise(heading) for heading in artifact.headings]
        # Skip the document-title heading only when it actually is one; a node
        # without an H1 keeps its first section heading assessable.
        if headings and headings[0] == normalise(artifact.title):
            headings = headings[1:]
        return any(any(normalise(term) in heading for term in terms) for heading in headings)

    def _links_next_movement(self, artifact: Artifact) -> bool:
        sequence = artifact.frontmatter.get("sequence")
        if not isinstance(sequence, int):
            return False
        return any(
            edge.target
            and self.artifacts[edge.target].artifact_type == "section"
            and self.artifacts[edge.target].frontmatter.get("sequence") == sequence + 1
            for edge in artifact.outgoing
        )

    def _quality_assessment(self, artifact: Artifact) -> dict[str, Any] | None:
        if artifact.artifact_type not in {"argument", "section", "concept"}:
            return None

        dependency_paths = sorted(
            edge.target
            for edge in artifact.outgoing
            if edge.target and edge.relation == "depends-on"
        )
        consumer_paths = sorted(
            {
                edge.source
                for edge in self.incoming[artifact.path]
                if self.artifacts[edge.source].artifact_type in {"section", "argument", "concept"}
            }
            | {
                edge.target
                for edge in artifact.outgoing
                if edge.target
                and self.artifacts[edge.target].artifact_type in {"section", "argument", "concept"}
                and edge.relation in {"opens-to", "wikilink", "related"}
            }
        )
        source_paths = sorted(
            edge.target
            for edge in artifact.outgoing
            if edge.target
            and self.artifacts[edge.target].artifact_type == "source-house"
        )

        if artifact.artifact_type == "argument":
            dimensions = {
                "claim-surface": self._has_heading_surface(
                    artifact, ("claim", "thesis", "proposition")
                ),
                "warrant-surface": self._has_heading_surface(
                    artifact,
                    (
                        "warrant",
                        "derivation",
                        "matheme",
                        "test",
                        "register",
                        "architecture",
                        "runtime",
                        "account",
                        "lineage",
                        "braid",
                        "perspective",
                        "running true",
                    ),
                ),
                "counterpressure-surface": self._has_heading_surface(
                    artifact,
                    (
                        "tension",
                        "limit",
                        "boundary",
                        "boundaries",
                        "shadow",
                        "discipline",
                        "silence",
                        "proof status",
                        "research vector",
                        "process test",
                    ),
                ),
            }
        elif artifact.artifact_type == "section":
            dimensions = {
                "proposition-surface": self._has_heading_surface(
                    artifact, ("claim", "thesis", "proposition")
                ),
                "warrant-surface": self._has_heading_surface(
                    artifact,
                    (
                        "warrant",
                        "derivation",
                        "structural",
                        "payload",
                        "synthesis",
                        "consequence",
                        "force",
                        "architecture",
                        "technical warning",
                        "bridge",
                        "topological display",
                        "energetic circulation",
                        "plate",
                        "musical resolution",
                        "established",
                        "primary displays",
                    ),
                ),
                "counterpressure-surface": self._has_heading_surface(
                    artifact,
                    (
                        "tension",
                        "limit",
                        "boundary",
                        "proof",
                        "discipline",
                        "remainder",
                        "technical warning",
                        "claim structure",
                    ),
                ),
                "transition-surface": self._has_heading_surface(
                    artifact, ("transition", "return", "release", "anchor")
                )
                or self._links_next_movement(artifact),
            }
        else:
            dimensions = {
                "definition-surface": self._has_heading_surface(
                    artifact, ("definition", "method proposition", "rule of use")
                ),
                "argument-role-surface": self._has_heading_surface(
                    artifact,
                    (
                        "in the argument",
                        "method it gives",
                        "withheld payoff",
                        "case ledger",
                        "governing artistic relation",
                    ),
                ),
                "source-anchors": bool(source_paths)
                or self._has_heading_surface(artifact, ("source",)),
                "claim-status": bool(artifact.frontmatter.get("claim_status")),
            }

        return {
            "path": artifact.path,
            "artifact_type": artifact.artifact_type,
            "authority": artifact.authority,
            "dimensions": dimensions,
            "missing": [name for name, present in dimensions.items() if not present],
            "dependencies": dependency_paths,
            "consumers": consumer_paths,
            "sources": source_paths,
        }

    def doctor(self) -> dict[str, Any]:
        debts: list[dict[str, Any]] = []
        quality_assessments: list[dict[str, Any]] = []
        unresolved_authorities = {
            "governing",
            "canonical-argument",
            "source-authority",
            "quotation-authority",
        }
        for artifact in self.artifacts.values():
            base = {"path": artifact.path, "authority": artifact.authority}
            assessment = self._quality_assessment(artifact)
            if assessment:
                quality_assessments.append(assessment)
                surface_missing = [
                    item for item in assessment["missing"] if item.endswith("-surface")
                ]
                if artifact.artifact_type == "argument" and len(surface_missing) >= 2:
                    debts.append(
                        {
                            **base,
                            "kind": "thin-argument",
                            "detail": f"missing reusable surfaces: {', '.join(surface_missing)}",
                            "missing": surface_missing,
                        }
                    )
                elif artifact.artifact_type == "section" and len(surface_missing) >= 2:
                    debts.append(
                        {
                            **base,
                            "kind": "thin-section",
                            "detail": f"missing movement surfaces: {', '.join(surface_missing)}",
                            "missing": surface_missing,
                        }
                    )
                elif artifact.artifact_type == "concept" and len(assessment["missing"]) >= 2:
                    debts.append(
                        {
                            **base,
                            "kind": "thin-concept",
                            "detail": f"missing concept surfaces: {', '.join(assessment['missing'])}",
                            "missing": assessment["missing"],
                        }
                    )
            if artifact.artifact_type in {"section", "argument", "concept"} and not artifact.frontmatter.get("claim_status"):
                debts.append({**base, "kind": "missing-status", "detail": "claim_status is absent"})
            if artifact.artifact_type in {
                "section", "argument", "concept", "path", "argument-map",
            }:
                declared = str(artifact.frontmatter.get("register") or "").strip()
                if not declared:
                    debts.append(
                        {
                            **base,
                            "kind": "missing-register",
                            "detail": "unratified-register-census",
                        }
                    )
                else:
                    declared_fold = declared.casefold()
                    if (
                        declared_fold not in {"symbolon", "matheme", "mytheme", "episteme"}
                        and "/" not in declared_fold
                        and "," not in declared_fold
                    ):
                        debts.append(
                            {
                                **base,
                                "kind": "invalid-register",
                                "detail": declared,
                            }
                        )
                    if (
                        artifact.artifact_type in {"concept", "path"}
                        and declared_fold != "episteme"
                    ):
                        debts.append(
                            {
                                **base,
                                "kind": "register-domain-mismatch",
                                "detail": (
                                    f"{artifact.artifact_type} must declare register "
                                    f"episteme, found {declared}"
                                ),
                            }
                        )
            if (
                artifact.frontmatter.get("record_type") == "dialogue-record"
                and any(
                    artifact.frontmatter.get(key)
                    for key in ("citation_status", "quote_status", "quotation_status")
                )
            ):
                debts.append(
                    {
                        **base,
                        "kind": "dialogue-record-evidence-status",
                        "detail": "dialogue records carry no citation or quotation status",
                    }
                )
            if artifact.authority in unresolved_authorities:
                for edge in artifact.outgoing:
                    if edge.target is None:
                        debts.append({**base, "kind": "unresolved-link", "detail": edge.raw_target, "relation": edge.relation})
            if (
                artifact.artifact_type in {"room-artifact", "room-reading-path"}
                and Path(artifact.path).name in {"ROOM.md", "READING.md"}
            ):
                for edge in artifact.outgoing:
                    if edge.target is None:
                        debts.append(
                            {
                                **base,
                                "kind": "dangling-room-link",
                                "detail": edge.raw_target,
                                "relation": edge.relation,
                            }
                        )
                for raw_target, fragment in markdown_fragment_targets(artifact.body):
                    target_path = self._resolve(raw_target, source=artifact)
                    if target_path and not self._has_fragment(
                        self.artifacts[target_path], fragment
                    ):
                        debts.append(
                            {
                                **base,
                                "kind": "dangling-room-fragment",
                                "detail": f"{raw_target}#{fragment}",
                                "relation": "markdown-fragment",
                            }
                        )

        source_houses: dict[str, list[Artifact]] = defaultdict(list)
        for artifact in self.artifacts.values():
            if artifact.artifact_type == "source-house":
                source_houses[artifact.id].append(artifact)
        for source_id, houses in sorted(source_houses.items()):
            if len(houses) > 1:
                for house in houses:
                    debts.append(
                        {
                            "path": house.path,
                            "authority": house.authority,
                            "kind": "duplicate-source-house",
                            "detail": source_id,
                        }
                    )

        for passage_id, candidates in sorted(self.passages.items()):
            canonical_candidates = [
                passage
                for passage in candidates
                if self.artifacts[passage.canonical_path].artifact_type == "source-house"
            ]
            if len(canonical_candidates) > 1:
                for passage in canonical_candidates:
                    debts.append(
                        {
                            "path": passage.canonical_path,
                            "authority": "source-authority",
                            "kind": "duplicate-passage-id",
                            "detail": passage_id,
                        }
                    )
            for passage in canonical_candidates:
                if not passage.locator:
                    debts.append(
                        {
                            "path": passage.canonical_path,
                            "authority": "source-authority",
                            "kind": "missing-passage-locator",
                            "detail": passage_id,
                        }
                    )
                if not passage.quotation_status or passage.quotation_status == "unspecified":
                    debts.append(
                        {
                            "path": passage.canonical_path,
                            "authority": "source-authority",
                            "kind": "missing-passage-status",
                            "detail": passage_id,
                        }
                    )
                if not passage.provenance:
                    debts.append(
                        {
                            "path": passage.canonical_path,
                            "authority": "source-authority",
                            "kind": "missing-passage-provenance",
                            "detail": passage_id,
                        }
                    )

        manifest = self.root / ".bkmr" / "manifest.tsv"
        if manifest.exists():
            rows = manifest.read_text(encoding="utf-8", errors="replace").splitlines()[1:]
            for row in rows:
                fields = row.split("\t")
                if len(fields) < 9:
                    continue
                canonical = self.root / fields[2]
                if canonical.exists() and hashlib.sha256(canonical.read_bytes()).hexdigest() != fields[8]:
                    debts.append({"path": fields[2], "authority": "generated-locator", "kind": "stale-bkmr-adapter", "detail": fields[0]})
        counts = Counter(debt["kind"] for debt in debts)
        missing_dimensions = Counter(
            dimension
            for assessment in quality_assessments
            for dimension in assessment["missing"]
        )
        return {
            "debt_counts": dict(sorted(counts.items())),
            "quality_summary": dict(sorted(missing_dimensions.items())),
            "quality_assessments": quality_assessments,
            "debts": debts,
        }


def add_json_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    commands = root.add_subparsers(dest="command", required=True)

    add_json_flag(commands.add_parser("status"))

    find = commands.add_parser("find")
    find.add_argument("query")
    find.add_argument("--limit", type=int, default=20)
    find.add_argument("--register", dest="register")
    add_json_flag(find)

    open_cmd = commands.add_parser("open")
    open_cmd.add_argument("artifact")
    add_json_flag(open_cmd)

    for name in ("links", "backlinks", "trace"):
        command = commands.add_parser(name)
        command.add_argument("artifact")
        add_json_flag(command)

    neighbourhood = commands.add_parser("neighbourhood")
    neighbourhood.add_argument("artifact")
    neighbourhood.add_argument("--depth", type=int, default=1)
    add_json_flag(neighbourhood)

    path = commands.add_parser("path")
    path.add_argument("start")
    path.add_argument("end")
    path.add_argument("--max-depth", type=int, default=6)
    add_json_flag(path)

    for name in ("context", "section-context"):
        context = commands.add_parser(name)
        context.add_argument("artifact")
        context.add_argument("--depth", type=int, default=2)
        add_json_flag(context)

    effects = commands.add_parser("effects")
    effects.add_argument("artifact")
    effects.add_argument("--depth", type=int, default=3)
    add_json_flag(effects)

    add_json_flag(commands.add_parser("doctor"))
    return root


def main() -> int:
    args = parser().parse_args()
    workspace = Workspace(args.project_root)
    try:
        if args.command == "status":
            result = workspace.status()
        elif args.command == "find":
            result = workspace.find(args.query, args.limit, args.register)
        elif args.command == "open":
            passage = workspace.passage(args.artifact)
            if passage:
                result = {
                    **passage.compact(),
                    "artifact_type": "passage",
                    "content": passage.content,
                }
            else:
                artifact = workspace.resolve(args.artifact)
                result = {**artifact.compact(), "frontmatter": artifact.frontmatter, "body": artifact.body}
        elif args.command == "links":
            result = workspace.links(workspace.resolve(args.artifact))
        elif args.command == "backlinks":
            result = workspace.backlinks(workspace.resolve(args.artifact))
        elif args.command == "neighbourhood":
            result = workspace.neighbourhood(workspace.resolve(args.artifact), args.depth)
        elif args.command == "path":
            result = workspace.path(workspace.resolve(args.start), workspace.resolve(args.end), args.max_depth)
        elif args.command == "trace":
            result = workspace.trace(workspace.resolve(args.artifact))
        elif args.command in {"context", "section-context"}:
            result = workspace.context(workspace.resolve(args.artifact), args.depth)
        elif args.command == "effects":
            result = workspace.effects(workspace.resolve(args.artifact), args.depth)
        elif args.command == "doctor":
            result = workspace.doctor()
        else:
            raise AssertionError(args.command)
    except KeyError as error:
        print(str(error), file=sys.stderr)
        return 2

    if args.json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
