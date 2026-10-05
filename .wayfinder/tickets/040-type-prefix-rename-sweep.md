---
title: Rename the 51 same-name files with type-prefix convention
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: rename-agent-2026-09-25
blocked_by:
  - 038-notation-expression-law-pass.md
created: 2026-09-25
---

# Rename the 51 same-name files with type-prefix convention

## Question

Frank's convention (ratified 2026-09-25): the TYPE is the prefix, qualified by its parent — so files stop being indistinguishable by name.

Census (2026-09-25): `ROOM.md` ×8 → `ROOM-<room-slug>.md`; `HISTORY.md` ×18 → `HISTORY-<parent-slug>.md`; `READING.md` ×2 → `READING-<parent-slug>.md`; `WHOLE-FIELD.md` ×7 → `WHOLE-FIELD-<parent-slug>.md`; `HISTORICAL-BRANCHES.md` ×6 → `HISTORICAL-BRANCHES-<parent-slug>.md`; `DEVELOPMENT.md` ×10 → `DEVELOPMENT-<parent-slug>.md`. Slugs are the immediate parent folder's name.

Method:

1. `ROOM.md` is GENERATED: change `tools/build-section-rooms.py` (the naming lives in generator source), then rebuild — never hand-edit generated output. Also update `tools/build-navigation.py`, `tools/audit-room-depth.py`, `tools/build-source-projections.py`, `tools/audit-pre-manuscript.py`, `tools/okf-workspace.py` wherever they reference the old names.
2. Update the 8 test files that reference these names and `tests/fixtures/retired-bkmr-coverage.json` paths (locator record — updated with the move).
3. `git mv` for every hand-authored file; sweep inbound path-style links repo-wide (basename wikilinks break for same-name files — check how links actually resolve before assuming).
4. Rebuild all generated surfaces, run each builder `--check`, run the room-depth and reader-navigation audits, then `python3 -m unittest discover -s tests -v`.

No commits. If a test cannot pass without a design decision, STOP and name the debt.

Report → `.wayfinder/research/040-rename-report.md`: full old→new table, every tool/test/reference class updated with counts, suite tail.

## Resolution

51 renames (type-prefix), 3,451 links repointed across 349 files, generator + 5 tools + 6 tests + fixture updated, all builders green. Report: ../research/040-rename-report.md
