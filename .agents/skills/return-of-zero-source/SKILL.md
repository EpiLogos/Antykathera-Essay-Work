---
name: return-of-zero-source
description: Use when identifying, retrieving, verifying, citing, quoting, comparing, or editing a scholarly source or passage for The Return of Zero.
---

# Work With Return of Zero Sources

Use one recoverable object or edition at a time. Its only canonical evidence surface is:

`submission-package/essay/symbolon/episteme/sources/<primary_domain>/<author>/<source_id>/SOURCE.md`

Sources are filed by epistemic domain (the work's own discipline, e.g. `psychology`, `mathematics-logic`, `indian-philosophy`) and then by author, so multiple works by one author sit together. Resolve a `source_id` to its path with `tools/source_resolver.py` (or any tool built on it) rather than assuming the nesting depth — the domain/author placement can be resorted independently of the stable `source_id`.

Open the complete `SOURCE.md`. If a sibling `NOTES.md` exists, read it for Frank’s encounter, intention, and quotation leads, but never create, edit, append, normalise, migrate, relocate, index as canonical evidence, or delete it. Verify any lead independently before placing it in `SOURCE.md`.

Authorial dialogue records under `internal-corpus/taylor/chat-logs/` are typed `dialogue-record`: provenance of thinking, never evidence. They carry no citation or quotation authority; quotations of a dialogue are quotations of the conversation, never of the named works. Resolve them by `source_id` like any house.

Keep bibliographic identity, edition, citation readiness, quotation readiness, source relation, provenance, locator, and consumers distinct. A quotation-ready passage needs one stable passage ID, exact transcription, exact locator, selected edition or version, verification method/date, provenance, relation, and named use boundary. Do not create parallel record, quote, passage, or study systems.

For exact retrieval:

```bash
python3 tools/project-agent-harness.py passage <passage-id> --json
```

After changing `SOURCE.md`, rebuild and check the deterministic projections:

```bash
python3 tools/build-source-projections.py --project-root .
python3 tools/build-source-projections.py --project-root . --check
python3 tools/okf-workspace.py --project-root . doctor --json
```
