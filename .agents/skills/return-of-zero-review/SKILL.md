---
name: return-of-zero-review
description: Use when explicitly reviewing Return of Zero prose, source integrity, argument propagation, generated freshness, or repository changes.
---

# Review Return of Zero Work

Review is explicit; do not silently impose it on generative conversation or writing. Recover the declared proposition, register, incoming inheritance, outgoing movement, source relation, and any genuinely live qualification before judging a passage.

Lead with concrete findings and canonical paths. Distinguish conceptual fidelity, source attribution, citation readiness, quotation readiness, generated freshness, and retrieval confidence. Missing external support does not downgrade an internally Derived or Argued claim.

For a load-bearing source, concept, theorem, or transverse thread, run `effects` and inspect every declared consumer. For repository review, check only the deterministic surfaces affected by the change; broad changes use:

```bash
python3 tools/build-source-projections.py --project-root . --check
python3 tools/build-section-rooms.py --project-root . --check
python3 tools/okf-workspace.py --project-root . doctor --json
python3 -m unittest discover -s tests -v
```

Never propose editing `NOTES.md`, generated `ROOM.md`, `MAIN-SOURCES.md`, `SOURCE-INDEX.md`, or `PASSAGE-LEDGER.md` directly. Name the canonical input and builder instead.
