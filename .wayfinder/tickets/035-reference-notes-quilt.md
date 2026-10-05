---
title: Quilt the 90 reference-notes into the live field
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: quilt-agent-2026-09-25
blocked_by:
  - 028-migrate-canonical-suite-into-section-rooms.md
  - 029-lenses-register-repair.md
created: 2026-09-25
---

# Quilt the 90 reference-notes into the live field

## Question

All 90 files in `section-rooms/arguments/concepts/reference-notes/` are uniformly `deprecated-legacy` ~25-line bibliography seeds. Their recorded disposition (`docs/REPOSITORY-SHAPE.md`, 2026-08-08 recovery note) is: granular points resolve into the concept nodes and source houses on quilting. Execute that.

- For each note: recover its granular points; route each point to its lawful target — concept node (`concepts/C##-*.md`), source house (resolve with `tools/source_resolver.py`; never assume nesting depth), argument node, or movement. A point with no recoverable home is logged as debt — never invented.
- Before wiring into any target, run `python3 tools/okf-workspace.py effects <source-or-concept> --depth 4 --json`, reopen the returned canonical consumers, and read the whole declared transverse thread. No association by shared vocabulary, tags or folder adjacency.
- Absorption means adding the point into the target's existing structure where it genuinely bears, with the reference-note named as provenance pointer — NOT rewriting targets, NOT creating new canonical records.
- Keep a per-note ledger `.wayfinder/research/035-quilt-ledger.md`: note → points → target(s) → disposition (absorbed / debt / duplicate-of-existing).
- The notes themselves are NOT deleted or moved in this ticket — retirement of the emptied shelf is Frank's later ratification.
- Source-house `<source_id>-NOTES.md` files are never touched.

No commits; no builders. Do not edit section prose in `movements/` — routing a point to a movement means adding it to that movement's own node only if it plainly belongs; otherwise log it as an enrichment pointer in the report.

Report → `.wayfinder/research/035-reference-notes-report.md` in Frank's plain format: what came up, what was incorporated where, which sections/nodes are worth a look.

## Resolution

89/89 notes dispositioned: 75 already quilted (verified), 5 absorbed (C49 formula, blind-spot house stratification, C34 crosswalk, C54 offices, C44 counterfeit), 9 named debts, nothing invented. Ledger + report: ../research/035-quilt-ledger.md, ../research/035-reference-notes-report.md
