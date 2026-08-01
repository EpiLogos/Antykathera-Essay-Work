#!/usr/bin/env python3
"""Build the shipped Return of Zero OKF reader bundle from canonical files.

The exporter never edits the workspace canon. It selects the live argument and
canonical source-house layers, converts internal wikilinks to portable
Markdown links, adds OKF `type` and provenance fields, and derives reader braid
nodes from the canonical transverse-thread list.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import re
import shutil
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml


WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]]+)\]\]")
EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")
TRANSVERSE_RE = re.compile(r"^- \*\*(.+?):\*\*\s*(.+)$", re.MULTILINE)
GENERATOR_VERSION = "2"
LOCAL_AUTHORING_FIELDS: set[str] = set()


def load_workspace_module(project_root: Path):
    path = project_root / "tools/okf-workspace.py"
    spec = importlib.util.spec_from_file_location("return_of_zero_okf_workspace", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def slug(value: str) -> str:
    value = value.casefold().replace("–", "-").replace("—", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "node"


def heading_slug(value: str) -> str:
    value = re.sub(r"[*_`]", "", value).casefold()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def okf_type(artifact) -> str:
    if artifact.artifact_type == "document" and artifact.frontmatter.get("node_type"):
        return str(artifact.frontmatter["node_type"])
    return {
        "section": "section",
        "argument": "claim",
        "argument-map": "map",
        "concept": "concept",
        "path": "path",
        "source-house": "source-house",
        "source-governance": "authorial-text",
        "document": "supporting-document",
    }[artifact.artifact_type]


def destination_for(artifact) -> Path:
    name = Path(artifact.path).name
    return {
        "section": Path("sections") / name,
        "argument": Path("arguments") / name,
        "argument-map": Path("maps") / name,
        "concept": Path("concepts") / name,
        "path": Path("paths") / name,
        "source-house": Path("references/sources") / f"{artifact.id}.md",
        "source-governance": (
            Path("supporting")
            / f"{Path(artifact.path).parent.name}-{slug(Path(artifact.path).stem)}.md"
        ),
        "document": Path("supporting") / f"{slug(Path(artifact.path).stem)}.md",
    }[artifact.artifact_type]


def split_link(raw: str) -> tuple[str, str, str]:
    target_part, separator, label = raw.partition("|")
    target, anchor_separator, anchor = target_part.partition("#")
    display = label if separator else (anchor if anchor_separator else target)
    return target.strip(), anchor.strip(), display.strip()


def relative_link(source: Path, target: Path, anchor: str = "") -> str:
    rel = Path(os.path.relpath(target, source.parent)).as_posix()
    return rel + (f"#{heading_slug(anchor)}" if anchor else "")


def transform_text(text: str, source_artifact, source_dest: Path, workspace, destinations) -> str:
    def embed(match: re.Match[str]) -> str:
        target_text, anchor, label = split_link(match.group(1))
        resolved = workspace._resolve(target_text, source=source_artifact)
        display = label or anchor or target_text
        if resolved and resolved in destinations:
            href = relative_link(source_dest, destinations[resolved], anchor)
            return f"[{display}]({href})"
        return display

    def wiki(match: re.Match[str]) -> str:
        target_text, anchor, label = split_link(match.group(1))
        resolved = workspace._resolve(target_text, source=source_artifact)
        if resolved and resolved in destinations:
            href = relative_link(source_dest, destinations[resolved], anchor)
            return f"[{label}]({href})"
        return label

    def markdown(match: re.Match[str]) -> str:
        label, raw = match.group(1), match.group(2).strip().strip("<>")
        if raw.startswith(("http://", "https://", "mailto:", "data:", "resource:")):
            return match.group(0)
        target_text, _, anchor = raw.partition("#")
        resolved = workspace._resolve(target_text, source=source_artifact)
        if resolved and resolved in destinations:
            return f"[{label}]({relative_link(source_dest, destinations[resolved], anchor)})"
        return label

    text = EMBED_RE.sub(embed, text)
    text = MARKDOWN_LINK_RE.sub(markdown, text)
    return WIKILINK_RE.sub(wiki, text)


def transform_value(value: Any, source_artifact, source_dest: Path, workspace, destinations):
    if isinstance(value, str):
        return transform_text(value, source_artifact, source_dest, workspace, destinations)
    if isinstance(value, list):
        return [transform_value(item, source_artifact, source_dest, workspace, destinations) for item in value]
    if isinstance(value, dict):
        return {
            key: transform_value(item, source_artifact, source_dest, workspace, destinations)
            for key, item in value.items()
        }
    return value


def dump_node(frontmatter: dict[str, Any], body: str) -> bytes:
    encoded = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    ).rstrip()
    return f"---\n{encoded}\n---\n\n{body.rstrip()}\n".encode("utf-8")


def select_artifacts(workspace):
    selected = {
        path: artifact
        for path, artifact in workspace.artifacts.items()
        if artifact.artifact_type
        in {"section", "argument", "argument-map", "concept", "path", "source-house"}
    }

    # Canonical argument nodes sometimes rely on a small number of in-house
    # theorem or venue documents. Include only those directly linked supports;
    # source-governance maps and frozen notes remain development-only.
    core_types = {"section", "argument", "argument-map", "concept", "path"}
    for artifact in list(selected.values()):
        if artifact.artifact_type not in core_types | {"source-house"}:
            continue
        for edge in artifact.outgoing:
            if not edge.target:
                continue
            target = workspace.artifacts[edge.target]
            if target.authority == "supporting-document":
                selected[target.path] = target
            elif (
                artifact.artifact_type == "source-house"
                and target.artifact_type == "source-governance"
                and Path(target.path).name == "AUTHORIAL-TEXT.md"
            ):
                selected[target.path] = target
    return selected


def braid_nodes(workspace, destinations: dict[str, Path]) -> dict[Path, bytes]:
    traversal_path = "essay-workshop/nodes/paths/return-of-zero-braided-traversal.md"
    traversal = workspace.artifacts[traversal_path]
    files: dict[Path, bytes] = {}
    for title, line in TRANSVERSE_RE.findall(traversal.body):
        members: list[tuple[str, str]] = []
        for raw in WIKILINK_RE.findall(line):
            target, _, label = split_link(raw)
            resolved = workspace._resolve(target, source=traversal)
            if resolved and resolved in destinations and (resolved, label) not in members:
                members.append((resolved, label))
        if not members:
            continue
        dest = Path("braids") / f"{slug(title)}.md"
        body = [f"# {title}", "", "Derived from the canonical transverse-thread path. Follow the members in order; the braid does not replace their local claims or statuses.", ""]
        for resolved, label in members:
            body.append(f"- [{label}]({relative_link(dest, destinations[resolved])})")
        fm = {
            "title": title,
            "type": "braid",
            "status": "derived-index",
            "canonical_path": traversal.path,
            "canonical_sha256": traversal.sha256,
            "members": [relative_link(dest, destinations[resolved]) for resolved, _ in members],
        }
        files[dest] = dump_node(fm, "\n".join(body))
    return files


def index_node(files: dict[Path, bytes], source_digest: str) -> bytes:
    groups: dict[str, list[Path]] = defaultdict(list)
    for path in sorted(files):
        groups[path.parts[0]].append(path)
    labels = {
        "sections": "48-movement day spine",
        "arguments": "Argument network",
        "concepts": "Concept homes",
        "paths": "Traversal paths",
        "braids": "Transverse braids",
        "maps": "Argument maps",
        "references": "Canonical source houses",
        "supporting": "In-house supporting documents",
    }
    body = [
        "# The Return of Zero — OKF Index",
        "",
        "Begin with the path for the whole essay, a braid for one argument across stations, or a concept matching the reader's question. Every claim retains its status; every reference retains separate citation and quotation readiness.",
        "",
    ]
    for group in ("paths", "braids", "concepts", "arguments", "sections", "maps", "references", "supporting"):
        if group not in groups:
            continue
        body.extend([f"## {labels[group]}", ""])
        for path in groups[group]:
            body.append(f"- [{path.stem.replace('-', ' ').title()}]({path.as_posix()})")
        body.append("")
    fm = {
        "title": "The Return of Zero — OKF Index",
        "type": "index",
        "format": "OKF v0.1-compatible Markdown bundle",
        "source_digest": source_digest,
    }
    return dump_node(fm, "\n".join(body))


def log_node(source_digest: str, count: int) -> bytes:
    fm = {"title": "Return of Zero OKF Build Log", "type": "log", "source_digest": source_digest}
    body = (
        "# Build log\n\n"
        f"- Generator version: `{GENERATOR_VERSION}`\n"
        f"- Source digest: `{source_digest}`\n"
        f"- Exported nodes excluding index/log: `{count}`\n"
        "- Canonical Markdown remained unchanged; this directory is a generated reader snapshot.\n"
    )
    return dump_node(fm, body)


def render_bundle(project_root: Path) -> dict[Path, bytes]:
    module = load_workspace_module(project_root)
    workspace = module.Workspace(project_root)
    selected = select_artifacts(workspace)
    destinations = {path: destination_for(artifact) for path, artifact in selected.items()}
    if len(set(destinations.values())) != len(destinations):
        raise RuntimeError("Export destination collision")

    files: dict[Path, bytes] = {}
    for canonical_path, artifact in sorted(selected.items()):
        dest = destinations[canonical_path]
        fm = dict(artifact.frontmatter)
        fm.pop("node_type", None)
        if artifact.artifact_type == "source-house":
            for field in LOCAL_AUTHORING_FIELDS:
                fm.pop(field, None)
        fm["type"] = okf_type(artifact)
        fm["canonical_path"] = artifact.path
        fm["canonical_sha256"] = artifact.sha256
        if artifact.artifact_type == "section" and not fm.get("coordinates"):
            fm["coordinates"] = [fm.get("station"), fm.get("position")]
        fm = transform_value(fm, artifact, dest, workspace, destinations)
        body = transform_text(artifact.body, artifact, dest, workspace, destinations)
        files[dest] = dump_node(fm, body)

    files.update(braid_nodes(workspace, destinations))
    source_digest = hashlib.sha256(
        "\n".join(
            f"{path}:{workspace.artifacts[path].sha256}"
            for path in sorted(selected)
        ).encode("utf-8")
    ).hexdigest()
    files[Path("index.md")] = index_node(files, source_digest)
    files[Path("log.md")] = log_node(source_digest, len(files))
    return files


def check_bundle(output: Path, expected: dict[Path, bytes]) -> list[str]:
    actual_paths = {
        path.relative_to(output)
        for path in output.rglob("*.md")
    } if output.exists() else set()
    expected_paths = set(expected)
    debts = [f"missing:{path}" for path in sorted(expected_paths - actual_paths)]
    debts.extend(f"extra:{path}" for path in sorted(actual_paths - expected_paths))
    for path in sorted(expected_paths & actual_paths):
        if (output / path).read_bytes() != expected[path]:
            debts.append(f"stale:{path}")
    return debts


def write_bundle(output: Path, files: dict[Path, bytes]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="essay-okf-", dir=output.parent) as temp:
        staging = Path(temp) / "bundle"
        for path, content in files.items():
            target = staging / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        if output.exists():
            shutil.rmtree(output)
        shutil.move(str(staging), str(output))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("submission-package/epi-logos/resources/essay-okf"),
    )
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.project_root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    files = render_bundle(root)
    if args.check:
        debts = check_bundle(output, files)
        if debts:
            print("OKF bundle is not current:", file=sys.stderr)
            for debt in debts:
                print(f"- {debt}", file=sys.stderr)
            return 1
        print(f"OKF bundle current: {len(files)} Markdown files.")
        return 0
    write_bundle(output, files)
    print(f"Built {len(files)} Markdown files at {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
