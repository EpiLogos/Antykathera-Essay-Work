#!/usr/bin/env python3
"""Build the generated navigation layer of *The Return of Zero* from authored links.

The publication body (``submission-package/essay/``) is navigated through relations
that authors wrote into pages. This tool never invents a relation. It reads every
link in the body, recovers the relation word the surrounding sentence names
(``derives``, ``grounds``, ``defines``, ``historicises``, ``sources``, ``qualifies``,
``tests``, ``figures``, ``embodies``, ``presages``, ``extends``, ``compares``,
``returns-to``), and projects three generated, non-authoritative surfaces under
``submission-package/essay/symbolon/episteme/maps/navigation/``:

* ``MOC.md`` — the map of content: the publication 4+2, every class of page,
  its entrance, and the authored-relation totals;
* ``intents/<class>.md`` — for each page, what it implicates (outgoing relations
  grouped by relation word) and what reaches it (incoming relations), the text
  equivalent of the local minigraph the writing protocol requires;
* ``AUDIT.md`` and ``audit.json`` — reachability from the reading root, orphans,
  pages without a route back into the essay, links leaving the publication body,
  unresolved targets, unnamed links, and the curated paths with their declared
  thread membership.

``--check`` regenerates in memory and fails when the on-disk surfaces differ, so a
canonical change can never leave the navigation layer silently stale.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

BUILDER_VERSION = "1.1.0"
BODY = "submission-package/essay/"
NAV_ROOT = "submission-package/essay/symbolon/episteme/maps/navigation"
READING_ROOT = "submission-package/essay/README.md"
MANUSCRIPT = "submission-package/essay/THE-RETURN-OF-ZERO.md"

VOCAB = [
    "derives",
    "grounds",
    "defines",
    "historicises",
    "sources",
    "qualifies",
    "tests",
    "figures",
    "embodies",
    "extends",
    "compares",
    "presages",
    "returns-to",
]
VERB_ALIASES = {
    "returns to": "returns-to",
    "historicise": "historicises",
    "historicizes": "historicises",
    "historicize": "historicises",
}
BOLD_VERB_RE = re.compile(
    r"\*\*(" + "|".join(re.escape(v) for v in VOCAB + list(VERB_ALIASES)) + r")\*\*",
    re.IGNORECASE,
)
PLAIN_VERB_RE = re.compile(
    r"(?<![\w-])(" + "|".join(re.escape(v) for v in VOCAB + list(VERB_ALIASES)) + r")(?![\w-])",
    re.IGNORECASE,
)
PLAIN_VERB_REACH = 60  # a plain relation word counts only when it sits beside the link
LINK_RE = re.compile(r"\[\[([^\]]+)\]\]|\[([^\]]*)\]\(([^)\s]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

# Navigation classes: (key, label, publication position, entrance page)
CLASSES: list[tuple[str, str, str, str]] = [
    ("essay", "The sovereign essay", "#5", MANUSCRIPT),
    ("rooms", "The rooms — waypoints, alignments, reading routes", "#0", "submission-package/essay/section-rooms/README.md"),
    ("movements", "The 48 movements", "#0", "submission-package/essay/section-rooms/README.md"),
    ("argument-shelf", "The historical argument shelf (01–21)", "#0", "submission-package/essay/section-rooms/README.md"),
    ("symbolon-root", "Symbolon — the twelvefold root", "#1", "submission-package/essay/symbolon/README.md"),
    ("matheme", "Matheme — exact operations", "#2", "submission-package/essay/symbolon/matheme/README.md"),
    ("mytheme", "Mytheme — whole lived images", "#3", "submission-package/essay/symbolon/mytheme/README.md"),
    ("episteme-root", "Episteme — the register root", "#4", "submission-package/essay/symbolon/episteme/README.md"),
    ("episteme-arguments", "Episteme · Arguments A01–A36", "#4", "submission-package/essay/symbolon/episteme/arguments/README.md"),
    ("episteme-conjugate", "Episteme · Conjugate arguments A01′–A36′", "#4", "submission-package/essay/symbolon/episteme/conjugate/README.md"),
    ("episteme-concepts", "Episteme · Concepts C01–C64 and provenance", "#4", "submission-package/essay/symbolon/episteme/concepts/README.md"),
    ("episteme-etymologies", "Episteme · Etymology whole-fields", "#4", "submission-package/essay/symbolon/episteme/etymologies/README.md"),
    ("episteme-histories", "Episteme · Histories", "#4", "submission-package/essay/symbolon/episteme/histories/README.md"),
    ("episteme-sources", "Episteme · Source houses", "#4", "submission-package/essay/symbolon/episteme/sources/README.md"),
    ("episteme-dossiers", "Episteme · Dossiers", "#4", "submission-package/essay/symbolon/episteme/dossiers/README.md"),
    ("episteme-lenses", "Episteme · Lenses", "#4", "submission-package/essay/symbolon/episteme/lenses/README.md"),
    ("episteme-maps", "Episteme · Maps and curated paths", "#4", "submission-package/essay/symbolon/episteme/maps/README.md"),
    ("episteme-atlas", "Episteme · Atlas", "#4", "submission-package/essay/symbolon/episteme/atlas/README.md"),
    ("episteme-aphorisms", "Episteme · Aphorisms", "#4", "submission-package/essay/symbolon/episteme/aphorisms/investigation-and-faith.md"),
    ("episteme-figures", "Episteme · Figures", "#4", "submission-package/essay/symbolon/episteme/figures/README.md"),
    ("episteme-dialogues", "Episteme · Dialogues", "#4", "submission-package/essay/symbolon/episteme/dialogues/README.md"),
    ("quilt", "Supporting quilt ledgers (non-canonical)", "support", "submission-package/essay/quilt/ql-expression-grammar.md"),
]
CLASS_INDEX = {key: (label, position, entrance) for key, label, position, entrance in CLASSES}
SPLIT_ABOVE = 60  # classes with more pages than this split into sub-pages by the next path segment
SPLIT_DEPTH = {  # how many path segments under the body identify a sub-page group
    "episteme-sources": 3,   # symbolon/episteme/sources/<domain>
    "episteme-concepts": 3,  # symbolon/episteme/concepts/<C-page | reference-notes>
    "movements": 1,          # section-rooms/<room>
    "matheme": 2,            # symbolon/matheme/<domain>
}


def load_workspace_module(project: Path):
    spec = importlib.util.spec_from_file_location("okf_workspace", project / "tools/okf-workspace.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("tools/okf-workspace.py could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules["okf_workspace"] = module
    spec.loader.exec_module(module)
    return module


def nav_class(path: str) -> str | None:
    if not path.startswith(BODY):
        return None
    if path.startswith(NAV_ROOT):
        return None
    rel = path[len(BODY):]
    parts = rel.split("/")
    if rel == "THE-RETURN-OF-ZERO.md":
        return "essay"
    if rel == "README.md":
        return "rooms"  # the reading root is listed with the rooms entrance
    if parts[0] == "quilt":
        return "quilt"
    if parts[0] == "section-rooms":
        if len(parts) > 1 and parts[1] == "arguments":
            return "argument-shelf"
        if "movements" in parts:
            return "movements"
        return "rooms"
    if parts[0] == "symbolon":
        if len(parts) == 2:
            return "symbolon-root"
        if parts[1] in ("matheme", "mytheme"):
            return parts[1]
        if parts[1] == "episteme":
            if len(parts) == 3:
                return "episteme-root"
            return f"episteme-{parts[2]}"
    return "quilt"


def is_return_target(path: str) -> bool:
    """A direct writing route, excluding historical carriers and incidental room files."""
    return (
        path == MANUSCRIPT
        or (path.startswith(BODY + "section-rooms/") and ("/movements/" in path or path.endswith("/ROOM.md")))
        or path.startswith(BODY + "symbolon/episteme/arguments/")
        or path.startswith(BODY + "symbolon/episteme/conjugate/")
    )


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub("", text, count=1)


def sentence_window(text: str, start: int, end: int) -> tuple[str, int]:
    """Return the sentence containing [start, end) and the link's offset inside it."""
    left_candidates = [text.rfind(sep, 0, start) for sep in ("\n", ". ", "; ")]
    left = max(left_candidates)
    left = 0 if left < 0 else left + 1
    right_candidates = [pos for pos in (text.find("\n", end), text.find(". ", end), text.find("; ", end)) if pos >= 0]
    right = min(right_candidates) if right_candidates else len(text)
    return text[left:right], start - left


def relation_word(window: str, offset: int) -> str | None:
    """The relation word nearest the link inside its sentence; bold wins over plain."""
    best: tuple[int, str] | None = None
    for pattern, plain in ((BOLD_VERB_RE, False), (PLAIN_VERB_RE, True)):
        for match in pattern.finditer(window):
            word = match.group(1).casefold()
            word = VERB_ALIASES.get(word, word)
            distance = abs(match.start() - offset)
            if plain and distance > PLAIN_VERB_REACH:
                continue
            if best is None or distance < best[0]:
                best = (distance, word)
        if best is not None:
            return best[1]
    return None


def relpath(from_path: str, to_path: str) -> str:
    from_dir = Path(from_path).parent
    target = Path(to_path)
    try:
        return target.relative_to(from_dir).as_posix()
    except ValueError:
        pass
    parts_from = from_dir.parts
    parts_to = target.parts
    common = 0
    for a, b in zip(parts_from, parts_to):
        if a != b:
            break
        common += 1
    up = [".."] * (len(parts_from) - common)
    return "/".join(up + list(parts_to[common:]))


class NavigationModel:
    def __init__(self, project: Path) -> None:
        self.project = project
        self.okf = load_workspace_module(project)
        self.ws = self.okf.Workspace(project)
        reader_spec = importlib.util.spec_from_file_location("reader_navigation", project / "tools/audit-reader-navigation.py")
        reader_module = importlib.util.module_from_spec(reader_spec)
        reader_spec.loader.exec_module(reader_module)
        self.reader_report = reader_module.ReaderAudit(project, ws=self.ws).run()
        self.body = {
            path: artifact
            for path, artifact in self.ws.artifacts.items()
            if path.startswith(BODY) and not path.startswith(NAV_ROOT)
        }
        self.classes: dict[str, str] = {}
        self.outgoing: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        self.incoming: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        self.out_of_body: collections.Counter[str] = collections.Counter()
        self.out_of_body_targets: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
        self.unresolved: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
        self.unnamed_samples: dict[str, list[str]] = collections.defaultdict(list)
        self._scan()

    # -- scanning ---------------------------------------------------------

    def _scan(self) -> None:
        for path, artifact in self.body.items():
            cls = nav_class(path)
            if cls is None:
                continue
            self.classes[path] = cls
            text = strip_frontmatter(artifact.body)
            seen: set[tuple[str, str]] = set()
            for match in LINK_RE.finditer(text):
                if match.group(1) is not None:
                    raw = match.group(1).split("|", 1)[0].strip()
                    fragment = raw.split("#", 1)[1] if "#" in raw else ""
                    raw = raw.split("#", 1)[0].strip()
                else:
                    raw_full = match.group(3).strip().strip("<>")
                    if raw_full.startswith(("http://", "https://", "mailto:", "data:")):
                        continue
                    raw, _, fragment = raw_full.partition("#")
                    raw = raw.strip()
                if not raw:
                    continue
                window, offset = sentence_window(text, match.start(), match.end())
                verb = relation_word(window, offset)
                target = self.ws._resolve(raw, source=artifact)
                if target is None:
                    self.unresolved[cls][raw] += 1
                    continue
                if not target.startswith(BODY) or target.startswith(NAV_ROOT):
                    top = "/".join(target.split("/")[:2]) if "/" in target else target
                    self.out_of_body[top] += 1
                    self.out_of_body_targets[top][target] += 1
                    continue
                if target == path:
                    continue
                key = (target, verb or "")
                if key in seen:
                    continue
                seen.add(key)
                edge = {
                    "source": path,
                    "target": target,
                    "relation": verb or "unnamed",
                    "fragment": fragment,
                }
                self.outgoing[path].append(edge)
                self.incoming[target].append(edge)
                if verb is None and len(self.unnamed_samples[cls]) < 3:
                    self.unnamed_samples[cls].append(window.strip()[:160])
            # Declared frontmatter relations are authored too; keep them with their origin as the word.
            for edge in artifact.outgoing:
                if edge.origin in ("markdown-link", "wikilink") or edge.target is None:
                    continue
                if not edge.target.startswith(BODY) or edge.target == path:
                    continue
                word = {
                    "source_ids": "sources (declared)",
                    "movement_ids": "returns-to (declared)",
                    "consumed_by_arguments": "consumed-by (declared)",
                    "quote_ids": "sources (declared passage)",
                    "source-companion": "companion notes (declared)",
                }.get(edge.origin)
                if word is None:
                    continue
                key = (edge.target, word)
                if key in seen:
                    continue
                seen.add(key)
                declared = {"source": path, "target": edge.target, "relation": word, "fragment": ""}
                self.outgoing[path].append(declared)
                self.incoming[edge.target].append(declared)

    # -- analysis ---------------------------------------------------------

    def reachability(self) -> dict[str, int]:
        depth = {READING_ROOT: 0}
        frontier = [READING_ROOT]
        while frontier:
            current = frontier.pop(0)
            for edge in self.outgoing.get(current, ()):
                target = edge["target"]
                if target not in depth:
                    depth[target] = depth[current] + 1
                    frontier.append(target)
        return depth

    def audit(self) -> dict[str, Any]:
        depth = self.reachability()
        per_class: dict[str, dict[str, Any]] = {}
        orphans: list[str] = []
        no_return: list[str] = []
        unreachable: list[str] = []
        for path, cls in self.classes.items():
            stats = per_class.setdefault(
                cls,
                {"pages": 0, "links": 0, "named": 0, "unnamed": 0, "orphans": 0, "no_return": 0, "unreachable": 0},
            )
            stats["pages"] += 1
            outs = self.outgoing.get(path, [])
            body_links = [e for e in outs if "(declared" not in e["relation"]]
            stats["links"] += len(body_links)
            stats["named"] += sum(1 for e in body_links if e["relation"] != "unnamed")
            stats["unnamed"] += sum(1 for e in body_links if e["relation"] == "unnamed")
            if not self.incoming.get(path):
                stats["orphans"] += 1
                orphans.append(path)
            if not is_return_target(path) and not any(is_return_target(e["target"]) for e in outs):
                stats["no_return"] += 1
                no_return.append(path)
            if path not in depth:
                stats["unreachable"] += 1
                unreachable.append(path)
        relation_totals: collections.Counter[str] = collections.Counter()
        for edges in self.outgoing.values():
            for edge in edges:
                relation_totals[edge["relation"]] += 1
        paths = []
        for path, artifact in sorted(self.body.items()):
            if not path.startswith(BODY + "symbolon/episteme/maps/") or Path(path).name == "README.md":
                continue
            fm = artifact.frontmatter
            thread_id = fm.get("thread_id")
            members = []
            if thread_id:
                for other, art in self.body.items():
                    threads = art.frontmatter.get("transverse_threads") or []
                    if isinstance(threads, str):
                        threads = [threads]
                    if thread_id in threads and other != path:
                        members.append(other)
            linked_movements = sorted(
                {e["target"] for e in self.outgoing.get(path, []) if self.classes.get(e["target"]) == "movements"}
            )
            paths.append(
                {
                    "path": path,
                    "title": artifact.title,
                    "thread_id": thread_id,
                    "thread_kind": fm.get("thread_kind"),
                    "linked_movements": len(linked_movements),
                    "declared_members": len(members),
                }
            )
        depth_histogram = collections.Counter(depth.values())
        return {
            "builder_version": BUILDER_VERSION,
            "scope": "Workspace-resolved graph, including declared metadata relations. Reader-valid links are audited separately.",
            "reader_links": self.reader_report["counts"],
            "reading_root": READING_ROOT,
            "pages": len(self.classes),
            "reachable_from_root": len([p for p in depth if p in self.classes]),
            "depth_histogram": {str(k): v for k, v in sorted(depth_histogram.items())},
            "max_depth": max(depth.values()) if depth else 0,
            "relation_totals": dict(relation_totals.most_common()),
            "per_class": per_class,
            "orphans": sorted(orphans),
            "no_return": sorted(no_return),
            "unreachable": sorted(unreachable),
            "out_of_body": {
                top: {"count": count, "targets": dict(self.out_of_body_targets[top].most_common(8))}
                for top, count in self.out_of_body.most_common()
            },
            "unresolved": {cls: dict(counter.most_common(12)) for cls, counter in self.unresolved.items()},
            "unnamed_samples": dict(self.unnamed_samples),
            "paths": paths,
        }

    # -- rendering --------------------------------------------------------

    def digest(self) -> str:
        hasher = hashlib.sha256(BUILDER_VERSION.encode("utf-8"))
        for path in sorted(self.body):
            hasher.update(path.encode("utf-8"))
            hasher.update(self.body[path].sha256.encode("utf-8"))
        return hasher.hexdigest()

    def header(self, title: str, digest: str, page_type: str, source_id: str) -> list[str]:
        # A generated navigation page still declares an identity, namespaced
        # `navigation-*` so a locator page can never collide with the authored
        # page it points at — `episteme/atlas/README.md` and the atlas intent
        # page otherwise both derive `episteme-atlas`. Without one,
        # AIKit's corpus ingest sets it aside and every link into it is
        # disclosed as unresolved — and these are the pages the vault navigates
        # by. The value is the output's own stem, which is the identity this
        # repo's `primary_id` rule already gives it; emitting it here keeps it
        # true across regeneration, where an edit to the output would not.
        return [
            "---",
            f'title: "{title}"',
            f"source_id: {source_id}",
            f"page_type: {page_type}",
            "generated: true",
            f'generator: "tools/build-navigation.py v{BUILDER_VERSION}"',
            "authority: generated-locator",
            f'source_digest: "{digest}"',
            "---",
            "",
            "<!-- Generated from authored links in the publication body. Do not edit by hand; edit the pages, then rebuild. -->",
            "",
        ]

    def link(self, from_path: str, to_path: str, label: str | None = None, fragment: str = "") -> str:
        text = label or self.body[to_path].title if to_path in self.body else (label or to_path)
        text = text.replace("[", "(").replace("]", ")")
        href = relpath(from_path, to_path)
        if fragment:
            href += "#" + fragment
        return f"[{text}]({href})"

    def breadcrumb(self, from_path: str) -> str:
        crumbs = [
            self.link(from_path, READING_ROOT, "Reading root"),
            self.link(from_path, BODY + "symbolon/episteme/README.md", "#4 Episteme"),
            self.link(from_path, BODY + "symbolon/episteme/maps/README.md", "Maps"),
            self.link(from_path, NAV_ROOT + "/MOC.md", "Navigation"),
        ]
        return "**Where you are:** " + " › ".join(crumbs)

    def marks(self, path: str) -> str:
        fm = self.body[path].frontmatter
        parts = []
        for key in ("register", "record_type", "claim_status"):
            value = fm.get(key)
            if value:
                parts.append(f"`{value}`")
        return " · ".join(parts)

    def groups_for(self, cls: str) -> dict[str, list[str]]:
        """Sub-page groups for a large class, keyed by a readable segment name."""
        pages = sorted((p for p, c in self.classes.items() if c == cls), key=lambda p: (self.body[p].title.casefold(), p))
        if len(pages) <= SPLIT_ABOVE or cls not in SPLIT_DEPTH:
            return {}
        depth = SPLIT_DEPTH[cls]
        groups: dict[str, list[str]] = collections.defaultdict(list)
        for path in pages:
            parts = path[len(BODY):].split("/")
            segment = parts[depth] if len(parts) > depth + 1 else "root"
            if cls == "episteme-concepts" and segment != "reference-notes":
                segment = "canonical-C01-C64" if re.match(r"C\d\d-", segment) else "developed-provenance"
            groups[segment].append(path)
        return dict(sorted(groups.items()))

    def render_intents(self, cls: str, digest: str, group: str | None = None, pages: list[str] | None = None) -> str:
        label, position, entrance = CLASS_INDEX[cls]
        out_path = f"{NAV_ROOT}/intents/{cls}.md" if group is None else f"{NAV_ROOT}/intents/{cls}--{group}.md"
        if group is None and pages is None:
            groups = self.groups_for(cls)
            if groups:
                lines = self.header(f"Intents — {label}", digest, "navigation-intents", f"navigation-{cls}")
                lines += [
                    f"# Intents — {label}",
                    "",
                    self.breadcrumb(out_path) + f" › {label}",
                    "",
                    f"Position {position}. Entrance: {self.link(out_path, entrance)}. "
                    "This class is large, so its intents are split by the folder that files it:",
                    "",
                ]
                for name, members in groups.items():
                    lines.append(f"- {self.link(out_path, f'{NAV_ROOT}/intents/{cls}--{name}.md', name)} — {len(members)} pages")
                return "\n".join(lines).rstrip() + "\n"
        lines = self.header(f"Intents — {label}", digest, "navigation-intents", f"navigation-{cls}" if group is None else f"navigation-{cls}--{group}")
        lines += [
            f"# Intents — {label}",
            "",
            self.breadcrumb(out_path) + f" › {label}",
            "",
            f"Position {position}. Entrance: {self.link(out_path, entrance)}. "
            "Each entry names what the page **implicates** through its written relations and what **reaches** it. "
            "The relation word is the one the sentence around the link names; `unnamed` marks a link whose sentence names none. "
            "This is a mirror of the written graph, never its substitute.",
            "",
        ]
        if pages is None:
            pages = sorted((p for p, c in self.classes.items() if c == cls), key=lambda p: (self.body[p].title.casefold(), p))
        if group is not None:
            lines[-1] = f"Group: `{group}` · back to {self.link(out_path, f'{NAV_ROOT}/intents/{cls}.md', label)}."
            lines.append("")
        for path in pages:
            lines.append(f"### {self.link(out_path, path)}")
            marks = self.marks(path)
            if marks:
                lines.append("")
                lines.append(marks)
            outs = self.outgoing.get(path, [])
            ins = self.incoming.get(path, [])
            lines.append("")
            lines.append(self._relation_line(out_path, "Implicates", outs, "target"))
            lines.append("")
            lines.append(self._relation_line(out_path, "Reached from", ins, "source"))
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def _relation_line(self, out_path: str, heading: str, edges: list[dict[str, Any]], end: str, cap: int = 12) -> str:
        if not edges:
            return f"**{heading}:** none written."
        grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        for edge in edges:
            grouped[edge["relation"]].append(edge)
        order = [v for v in VOCAB] + sorted(k for k in grouped if k not in VOCAB and k != "unnamed") + ["unnamed"]
        parts = []
        for word in order:
            if word not in grouped:
                continue
            items = grouped[word]
            seen: set[str] = set()
            rendered = []
            for edge in items:
                other = edge[end]
                if other in seen:
                    continue
                seen.add(other)
                rendered.append(self.link(out_path, other, fragment=edge["fragment"] if end == "target" else ""))
            shown = rendered[:cap]
            more = len(rendered) - len(shown)
            tail = f" (+{more} more)" if more > 0 else ""
            parts.append(f"*{word}* → " + ", ".join(shown) + tail if end == "target" else f"*{word}* ← " + ", ".join(shown) + tail)
        return f"**{heading}:** " + " · ".join(parts)

    def render_moc(self, audit: dict[str, Any], digest: str) -> str:
        out_path = f"{NAV_ROOT}/MOC.md"
        lines = self.header("Map of Content — The Return of Zero", digest, "navigation-moc", "navigation-moc")
        lines += [
            "# Map of Content",
            "",
            self.breadcrumb(out_path),
            "",
            "This map is generated from the relations authors wrote into the publication body. "
            "It shows where every class of page stands in the publication 4+2, how to enter it, and how many written relations carry it. "
            f"The {self.link(out_path, READING_ROOT, 'reading root')} is the authored front door; this map is its mirror.",
            "",
            "## The publication 4+2",
            "",
            "| Position | Class | Pages | Written relations out | Named | Entrance | Intents |",
            "|---|---|---|---|---|---|---|",
        ]
        per_class = audit["per_class"]
        for key, label, position, entrance in CLASSES:
            stats = per_class.get(key)
            if not stats:
                continue
            named_pct = f"{100 * stats['named'] / stats['links']:.0f}%" if stats["links"] else "—"
            lines.append(
                f"| {position} | {label} | {stats['pages']} | {stats['links']} | {named_pct} | "
                f"{self.link(out_path, entrance)} | {self.link(out_path, f'{NAV_ROOT}/intents/{key}.md', 'intents')} |"
            )
        lines += [
            "",
            "## Four reading movements",
            "",
            f"- **Linear** — open {self.link(out_path, MANUSCRIPT)} and follow the eight stations in order.",
            f"- **Radial** — enter a room from {self.link(out_path, BODY + 'section-rooms/README.md', 'the rooms')}, open one movement, and follow its written relations into the field.",
            f"- **Transverse** — follow a curated path from {self.link(out_path, BODY + 'symbolon/episteme/maps/README.md', 'Maps')}; each path exists only for a whole movement that local relations cannot reconstruct.",
            f"- **Toroidal** — return through any *returns-to* relation listed in the intents pages; the essay's return routes are counted below.",
            "",
            "## Written relations across the body",
            "",
            "| Relation | Count |",
            "|---|---|",
        ]
        for word, count in audit["relation_totals"].items():
            lines.append(f"| {word} | {count} |")
        lines += [
            "",
            "## Standing of the surface",
            "",
            f"- Workspace-resolved graph: {audit['reachable_from_root']}/{audit['pages']} reachable, including metadata relations. Conservative visible-link audit: {audit['reader_links']['reachable']}/{audit['reader_links']['pages']}. See the audit for the distinction.",
            f"- Orphans (no written inbound relation): {len(audit['orphans'])}. Pages with no written route back into the essay: {len(audit['no_return'])}.",
            f"- Full findings with page lists: {self.link(out_path, f'{NAV_ROOT}/AUDIT.md', 'navigation audit')}.",
            "",
        ]
        return "\n".join(lines).rstrip() + "\n"

    def render_audit(self, audit: dict[str, Any], digest: str) -> str:
        out_path = f"{NAV_ROOT}/AUDIT.md"
        lines = self.header("Navigation Audit — The Return of Zero", digest, "navigation-audit", "navigation-audit")
        lines += [
            "# Navigation Audit",
            "",
            self.breadcrumb(out_path) + " › Audit",
            "",
            "Generated findings about the written navigation of the publication body. "
            "A finding here is a locator for authored repair or for an explicit disposition; it never rewrites a page.",
            "",
            "## Reader links and workspace lookup",
            "",
            f"Visible, independently resolved links reach {audit['reader_links']['reachable']} of {audit['reader_links']['pages']} pages. All {audit['reader_links']['admitted']} admitted records are checked: {audit['reader_links']['missing_admitted']} missing and {audit['reader_links']['unreachable_admitted']} unreachable.",
            "",
            "This conservative reader check validates file-relative Markdown, vault-path or unique-filename wikilinks, and heading anchors. Title/alias-only links are portability debt, not proof of failure in Obsidian. Frontmatter and code do not count as reader routes. [Full reader findings](reader-audit.json) retain every location and unresolved destination.",
            "",
            f"Workspace lookup reaches {audit['reachable_from_root']} of {audit['pages']} pages. The tables below describe that larger graph, including metadata relations and resolver fallbacks; its depths are graph hops, not a certified reader click count.",
            "",
            "| Depth (clicks) | Pages |",
            "|---|---|",
        ]
        for depth, count in audit["depth_histogram"].items():
            lines.append(f"| {depth} | {count} |")
        lines += ["", "## By class", "", "| Class | Pages | Links | Named | Unnamed | Orphans | No return | Unreachable |", "|---|---|---|---|---|---|---|---|"]
        for key, label, _position, _entrance in CLASSES:
            stats = audit["per_class"].get(key)
            if not stats:
                continue
            lines.append(
                f"| {label} | {stats['pages']} | {stats['links']} | {stats['named']} | {stats['unnamed']} | "
                f"{stats['orphans']} | {stats['no_return']} | {stats['unreachable']} |"
            )
        lines += ["", "## Curated paths", "", "| Path | Thread | Kind | Movements linked | Pages declaring the thread |", "|---|---|---|---|---|"]
        for item in audit["paths"]:
            lines.append(
                f"| {self.link(out_path, item['path'])} | {item['thread_id'] or '—'} | {item['thread_kind'] or 'spine'} | "
                f"{item['linked_movements']} | {item['declared_members']} |"
            )
        lines += ["", "## Links leaving the publication body", "", "Targets outside `submission-package/essay/` resolve in the repository but not in a published vault.", "", "| Target root | Links | Most linked |", "|---|---|---|"]
        for top, info in audit["out_of_body"].items():
            most = "; ".join(f"`{t}` ({n})" for t, n in list(info["targets"].items())[:3])
            lines.append(f"| `{top}` | {info['count']} | {most} |")
        lines += ["", "## Unresolved targets", ""]
        if not audit["unresolved"]:
            lines.append("None.")
        for cls, targets in audit["unresolved"].items():
            label = CLASS_INDEX[cls][0]
            lines.append(f"- **{label}:** " + "; ".join(f"`{t}` ({n})" for t, n in targets.items()))
        lines += ["", "## Orphans — no written inbound relation", ""]
        lines += [f"- {self.link(out_path, p)}" for p in audit["orphans"]] or ["None."]
        lines += ["", "## No written route back into the essay", "", "Pages outside the rooms with no link to the manuscript, a room surface, or a canonical Argument.", ""]
        lines += [f"- {self.link(out_path, p)}" for p in audit["no_return"]] or ["None."]
        lines += ["", "## Unreachable from the reading root", ""]
        lines += [f"- {self.link(out_path, p)}" for p in audit["unreachable"]] or ["None."]
        lines += ["", "## Unnamed-link samples by class", ""]
        for cls, samples in audit["unnamed_samples"].items():
            label = CLASS_INDEX[cls][0]
            for sample in samples:
                safe = sample.replace("`", "'").replace("|", "/").replace("](", "] (")
                lines.append(f"- **{label}:** `{safe}`")
        return "\n".join(lines).rstrip() + "\n"

    def render_all(self) -> dict[str, str]:
        digest = self.digest()
        audit = self.audit()
        outputs = {
            f"{NAV_ROOT}/reader-audit.json": json.dumps(self.reader_report, indent=2, ensure_ascii=False) + "\n",
            f"{NAV_ROOT}/MOC.md": self.render_moc(audit, digest),
            f"{NAV_ROOT}/AUDIT.md": self.render_audit(audit, digest),
            f"{NAV_ROOT}/audit.json": json.dumps({"source_digest": digest, **audit}, indent=2, ensure_ascii=False) + "\n",
        }
        for key, *_ in CLASSES:
            if any(c == key for c in self.classes.values()):
                outputs[f"{NAV_ROOT}/intents/{key}.md"] = self.render_intents(key, digest)
                for name, members in self.groups_for(key).items():
                    outputs[f"{NAV_ROOT}/intents/{key}--{name}.md"] = self.render_intents(key, digest, group=name, pages=members)
        return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--check", action="store_true", help="fail when the generated navigation layer is stale")
    parser.add_argument("--json", action="store_true", help="print the audit as JSON instead of writing files")
    args = parser.parse_args()
    project = Path(args.project_root).resolve()
    model = NavigationModel(project)
    if args.json:
        print(json.dumps(model.audit(), indent=2, ensure_ascii=False))
        return 0
    outputs = model.render_all()
    nav_dir = project / NAV_ROOT
    if args.check:
        stale = []
        for rel, content in outputs.items():
            target = project / rel
            if not target.is_file() or target.read_text(encoding="utf-8") != content:
                stale.append(rel)
        expected = set(outputs)
        for existing in list((nav_dir / "intents").glob("*.md")) if nav_dir.is_dir() else []:
            rel = existing.relative_to(project).as_posix()
            if rel not in expected:
                stale.append(rel + " (unexpected)")
        if stale:
            print("stale navigation layer:\n  " + "\n  ".join(stale))
            return 1
        print(f"navigation layer fresh: {len(outputs)} generated surfaces")
        return 0
    (nav_dir / "intents").mkdir(parents=True, exist_ok=True)
    for rel, content in outputs.items():
        (project / rel).write_text(content, encoding="utf-8")
    for existing in (nav_dir / "intents").glob("*.md"):
        if existing.relative_to(project).as_posix() not in outputs:
            existing.unlink()
    audit = model.audit()
    print(
        f"navigation layer written: {len(outputs)} surfaces; {audit['reachable_from_root']}/{audit['pages']} pages reachable; "
        f"{len(audit['orphans'])} orphans; {len(audit['no_return'])} without return route"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
