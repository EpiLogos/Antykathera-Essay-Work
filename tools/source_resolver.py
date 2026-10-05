"""Shared source_id -> path resolution for the domain/author-nested source bank.

Each source house is a folder whose house file is the Markdown file whose stem
equals the folder's own name: sources/<domain>/<author>/<source_id>/<source_id>.md.
The file name carries the provenance of the house it governs. This module lets
callers resolve a source_id without hardcoding the nesting depth, so the bank
can be resorted (frontmatter primary_domain changes) without touching every
tool that looks up a source by id.
"""

from __future__ import annotations

from pathlib import Path


def source_bank_root(project_root: Path) -> Path:
    return project_root / "submission-package/essay/symbolon/episteme/sources"


def iter_source_houses(project_root: Path):
    """Yield every source-house file path under the source bank, any nesting depth.

    A house file is a Markdown file whose stem equals its parent folder's name
    (e.g. <source_id>/<source_id>.md).
    """
    return sorted(
        path
        for path in source_bank_root(project_root).rglob("*.md")
        if path.stem == path.parent.name
    )


def build_source_index(project_root: Path) -> dict[str, Path]:
    """Map source_id -> its house file path, keyed by directory name (source_id)."""
    index: dict[str, Path] = {}
    for path in iter_source_houses(project_root):
        index[path.parent.name] = path
    return index


def resolve_source_house(project_root: Path, source_id: str) -> Path | None:
    """Return the house file path for source_id, or None if not found."""
    return build_source_index(project_root).get(source_id)


def resolve_source_dir(project_root: Path, source_id: str) -> Path | None:
    house = resolve_source_house(project_root, source_id)
    return house.parent if house else None
