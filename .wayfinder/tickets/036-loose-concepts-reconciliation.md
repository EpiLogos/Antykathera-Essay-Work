---
title: Reconcile the 22 loose concept files with the canonical C-field
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: loose-concepts-agent-2026-09-25
blocked_by:
  - 035-reference-notes-quilt.md
created: 2026-09-25
---

# Reconcile the 22 loose concept files with the canonical C-field

## Question

`section-rooms/arguments/concepts/` holds the 64 canonical C-nodes beside 22 loose topic files and 3 indexes. Reconcile the loose layer so the canonical field is the only live surface.

- **Shadow duplicates** (files duplicating canonical titles/content — `agentworld.md`/`anthropomorphization.md` vs C57/C58; `apoha.md`→C18, `diaphaneity.md`→C09, etc., per `README.md`/`CANONICAL-INDEX.md`): merge any distinct points into the canonical node, then move the superseded file to `working/_to_delete/2026-09-25-retire/` (manifest entry). Nothing deleted outright.
- **No-counterpart files** (`parasociety`, `simulation`, `the-slash`, `register-grammar`, `centaur-societies`, `mathematical-artistic-image-register`, and any other without a canonical home): for each, propose a disposition — promote to canonical concept / fold into the nearest argument or concept that already bears the work / absorb into a dossier. Implement folds only where the target plainly bears it (run `okf-workspace effects` first); PROMOTIONS are listed for Frank's ratification, not enacted.
- `j-space.md` stays subordinate under C40 (documented disposition); `zero.md` is a retired identity — move to `_to_delete` per its documented disposition.
- `index.md` (pre-T09 Concept Map, provenance): after re-homing its still-live links (it links into the 21 legacy files that ticket 028 moved to `working/legacy/section-rooms-arguments/`), move it to `_to_delete` too. `README.md` and `CANONICAL-INDEX.md` stay, updated to the reconciled state.
- Never touch canonical C-node content beyond absorbing folded-in points; mark absorbed additions with their origin file as provenance.

No commits; no builders; no suite runs (integrator runs them).

Report → `.wayfinder/research/036-loose-concepts-report.md`: disposition table (merged/retired/folded/proposed-for-promotion), what came up, what changed.

## Resolution

21 loose files retired with carriers named; sub-offices absorbed into C57/C58/C62/C30/C24/C56; j-space stays under C40; zero promotions needed; ~115 links repointed; zero inbound links to retired basenames. Report: ../research/036-loose-concepts-report.md
