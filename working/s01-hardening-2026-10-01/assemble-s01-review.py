"""Collate current M01–M06 review bodies without changing their authorial prose.

This makes a review artifact, never writes the sovereign manuscript, and records
the exact input bytes. Notes with the same marker retain their complete supplied
definitions in a single review note; no source status is silently promoted.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from source_resolver import build_source_index

TITLE = "Confronting the Limit: Determination, Subjectivity and Mind as Objective Internality."
DESTINATION = "submission-package/essay/CONFRONTING-THE-LIMIT-S01.md"
REVIEW = HERE / "CONFRONTING-THE-LIMIT-S01-REVIEW.md"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract(path: Path) -> tuple[str, list[tuple[str, str]], dict]:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    start = re.search(r'<a id="M0[1-6]"></a>', text)
    if start is None:
        raise ValueError(f"No movement anchor in {path.name}")
    # M01 alone carries the section heading immediately before its anchor.
    if path.name.startswith("M01"):
        start_at = text.rfind("## §0/1", 0, start.start())
        if start_at < 0:
            raise ValueError("M01 section heading absent")
    else:
        start_at = start.start()
    remaining = text[start_at:]
    note_start = re.search(r'^\[\^[^\]]+\]:', remaining, re.M)
    if note_start is None:
        raise ValueError(f"No note section in {path.name}")
    prose = remaining[:note_start.start()]
    # M05/M06 have a rule and a Draft notes heading before the definitions.
    prose = re.sub(r'\n---\n(?:\s*### Draft notes[^\n]*\n)?\s*$', '\n', prose)
    prose = prose.rstrip() + "\n"
    note_area = remaining[note_start.start():]
    note_end = re.search(r'^---\s*$', note_area, re.M)
    if note_end:
        note_area = note_area[:note_end.start()]
    notes = []
    for match in re.finditer(r'^\[\^([^\]]+)\]:\s*(.*?)(?=\n\[\^|\Z)', note_area, re.M | re.S):
        notes.append((match[1], match[2].strip()))
    refs = re.findall(r'\[\^([^\]]+)\]', prose)
    defined = {key for key, _ in notes}
    if set(refs) - defined:
        raise ValueError(f"Unresolved note markers in {path.name}: {set(refs)-defined}")
    return prose, notes, {
        "path": str(path.relative_to(ROOT)),
        "input_sha256": digest(raw),
        "prose_sha256": digest(prose.encode()),
        "prose_words": len(prose.split()),
        "note_markers": len(refs),
        "note_definitions": len(notes),
    }


def main() -> None:
    check_only = "--check" in sys.argv
    source_index = build_source_index(ROOT)
    sections, inputs, definitions, consumed = [], [], {}, {}
    for movement in range(1, 7):
        name = f"M{movement:02d}"
        prose, notes, receipt = extract(HERE / f"{name}-REWRITE.md")
        sections.append(prose)
        inputs.append(receipt)
        for marker, text in notes:
            definitions.setdefault(marker, []).append({"movement": name, "text": text})
        for marker in re.findall(r'\[\^([^\]]+)\]', prose):
            consumed.setdefault(marker, []).append(name)

    header = (
        "---\n"
        f'title: "{TITLE}"\n'
        'status: "assembly-for-author-review; not accepted sovereign prose"\n'
        'scope: "§0/1 — The Integral Threshold"\n'
        f'intended_publication_path: "{DESTINATION}"\n'
        'date: "2026-10-04"\n'
        "---\n\n"
        f"# {TITLE}\n\n"
        "<!-- Assembly for review: the six current working movement bodies are copied "
        "verbatim, in order. Draft wrappers and after-matter are excluded. Notes retain "
        "their supplied source standing; a resolving marker is not a verified quotation. "
        "See S01-ASSEMBLY-RECEIPT.json and SOURCE-AND-VISUAL-APPARATUS.md. -->\n\n"
    )
    body = "\n\n".join(sections)
    override_path = HERE / "S01-APPARATUS-OVERRIDES.json"
    overrides = json.loads(override_path.read_text()) if override_path.exists() else {}
    note_lines, bindings, collisions = [], [], []
    for marker, supplied in definitions.items():
        unique = list(dict.fromkeys(item["text"] for item in supplied))
        if len(unique) > 1:
            # Preserve differing definitions as review apparatus, not an editor's
            # unsupported choice about which source/edition the author intended.
            note = " ".join(
                f"[{', '.join(item['movement'] for item in supplied if item['text']==text)}] {text}"
                for text in unique
            )
            collisions.append({"marker": marker, "supplied": supplied, "resolution": "one marker; all differing supplied definitions retained with movement labels"})
        else:
            note = unique[0]
        original_note = note
        if marker in overrides:
            note = overrides[marker]["text"]
        matches = [sid for sid in source_index if re.search(r'(?<![a-z0-9-])'+re.escape(sid)+r'(?:-q\d+)?(?![a-z0-9-])', note)]
        links = []
        for sid in matches:
            relative = source_index[sid].relative_to(ROOT).as_posix()
            current = "../../" + relative
            future = source_index[sid].relative_to(ROOT / "submission-package/essay").as_posix()
            links.append(f"[{sid}]({current})")
            bindings.append({"marker": marker, "source_id": sid, "canonical_path": relative,
                             "working_href": current, "submission_href": future,
                             "source_sha256": digest(source_index[sid].read_bytes()),
                             "relation": "explicit source identity in supplied note; quotation standing not inferred"})
        if links:
            note += " Source houses: " + "; ".join(links) + "."
        note_lines.append(f"[^{marker}]: {note}")

    result = header + body + "\n\n## Notes\n\n" + "\n\n".join(note_lines) + "\n"
    refs = set(re.findall(r'\[\^([^\]]+)\](?!:)', result))
    defs = re.findall(r'^\[\^([^\]]+)\]:', result, re.M)
    if refs != set(defs) or len(defs) != len(set(defs)):
        raise ValueError("Collated note coverage or uniqueness failed")
    expected_prose = re.sub(r'\s+', ' ', body).strip()
    extracted_sections = result[result.index("## §0/1"):result.index("\n\n## Notes\n\n")]
    if re.sub(r'\s+', ' ', extracted_sections).strip() != expected_prose:
        raise ValueError("Collated body differs from inputs")
    for row in bindings:
        if not (HERE / row["working_href"]).resolve().is_file():
            raise ValueError(f"Source target absent: {row['working_href']}")
        if not (ROOT / "submission-package/essay" / row["submission_href"]).is_file():
            raise ValueError(f"Future source target absent: {row['submission_href']}")
    receipt = {
        "standing": "mechanically collated review; no whole-section prose acceptance claimed",
        "title": TITLE, "date": "2026-10-04", "intended_publication_path": DESTINATION,
        "inputs": inputs, "authorial_body_words": sum(r["prose_words"] for r in inputs),
        "output": REVIEW.name, "output_sha256": digest(result.encode()),
        "assembly_prose_sha256": digest(body.encode()),
        "unique_note_definitions": len(defs), "unresolved_note_markers": sorted(refs-set(defs)),
        "unused_note_definitions": sorted(set(defs)-refs),
        "collisions": collisions, "source_bindings": bindings,
        "apparatus_overrides": overrides,
        "verification": {"exact_movement_prose_preserved": True, "unique_note_ids": True,
                         "all_note_markers_resolve": True, "working_source_links_resolve": True,
                         "future_submission_source_links_resolve": True},
        "publication": "not promoted; reviewer apparatus includes original unverified quotation and locator debts",
    }
    if check_only:
        if not REVIEW.exists() or REVIEW.read_text() != result:
            raise SystemExit("Review assembly stale; regenerate from current authorial files")
        old = json.loads((HERE / "S01-ASSEMBLY-RECEIPT.json").read_text())
        if old["inputs"] != inputs:
            raise SystemExit("Input receipt stale")
    else:
        REVIEW.write_text(result)
        (HERE / "S01-ASSEMBLY-RECEIPT.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"mode": "check" if check_only else "write", "words": receipt["authorial_body_words"],
                      "notes": len(defs), "source_bindings": len(bindings), "collisions": len(collisions),
                      "prose_preserved": True, "output": REVIEW.name}, ensure_ascii=False))


if __name__ == "__main__":
    main()
