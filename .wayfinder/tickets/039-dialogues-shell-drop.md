---
title: Drop the empty dialogues register from the ship surface
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: integrator-2026-09-25
blocked_by: []
created: 2026-09-25
---

# Drop the empty dialogues register from the ship surface

## Question

`symbolon/episteme/dialogues/` holds only a README describing a record schema — zero records (confirmed 2026-09-25). Frank's decision: drop it. His actual chat logs stay where they lawfully live, `working/sources-texts-references/chat-logs-for-quilting/` (the `local_copy` shelf; dialogue records are provenance, never public evidence).

- Move `episteme/dialogues/` to `working/_to_delete/2026-09-25-retire/dialogues-register/` (manifest entry).
- Repo-wide grep for `episteme/dialogues` references; update or remove stale links. The central plan names "dialogues" among Episteme's contents — append one dated amendment line recording the 2026-09-25 drop, in the plan's established amendment voice. Same for any other governing/locator doc that lists it (`docs/REPOSITORY-SHAPE.md` row "dialogue records migrate to episteme/dialogues/").

No commits. Report: the move + every reference updated, as a comment on this ticket (integrator resolves it).

## Resolution

Executed by the integrator, 2026-09-25. Folder moved to `working/_to_delete/2026-09-25-retire/dialogues-register/`; manifest line appended. Central plan gained its own amendment ("The empty dialogues register drops from the ship surface"). `docs/REPOSITORY-SHAPE.md` updated (four-class row, chat-logs row). `tools/build-navigation.py` class registry pruned of the `episteme-dialogues` intent; the Episteme register README's dialogues link removed; navigation rebuilt (62 surfaces, `--check` fresh). No other live references remain.
