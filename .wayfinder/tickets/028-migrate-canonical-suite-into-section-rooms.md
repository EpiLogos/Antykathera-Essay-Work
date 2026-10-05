---
title: Migrate the canonical A/C suite into section-rooms
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: migration-agent-2026-09-25 (+ integrator completion)
blocked_by: []
created: 2026-09-25
---

# Migrate the canonical A/C suite into section-rooms

## Question

Execute Frank's ratified physical migration (2026-09-25): the canonical argument field moves into the rooms and replaces the legacy 21.

Target shape (exact):

- `submission-package/essay/section-rooms/arguments/` ← `symbolon/episteme/arguments/` (A01–A36 + README.md)
- `submission-package/essay/section-rooms/arguments/conjugate/` ← `symbolon/episteme/conjugate/` (36 A-prime files + README.md + AC.md — "it all moves")
- `submission-package/essay/section-rooms/arguments/concepts/` ← `symbolon/episteme/concepts/` (64 C-nodes, 22 loose topic files, indexes, `reference-notes/` — it travels with the folder)
- `submission-package/essay/section-rooms/arguments/products/` ← `symbolon/episteme/products/` (S0–S5, S-World-and-Life, README.md)
- The 21 legacy files currently in `section-rooms/arguments/` move FIRST to `working/legacy/section-rooms-arguments/` (frozen provenance, typed `legacy-argument`).
- `episteme/` keeps: aphorisms, atlas, dossiers, etymologies, figures, histories, lenses, maps (+ navigation), sources.

Method: `git mv` only; move legacy out before moving the suites in. Then sweep every reference:

1. `tools/*.py`, `tests/*.py`, and `tests/fixtures/retired-bkmr-coverage.json` (the fixture is a locator record — update its paths with the move; script the rewrite).
2. Governing docs: `the-return-of-zero-central-plan.md` (rewrite path links; append one dated amendment line recording Frank's 2026-09-25 ratification, in the plan's established amendment voice), `AGENTS.md`, `WRITING-PROTOCOL.md`, `docs/REPOSITORY-SHAPE.md`, README surfaces.
3. `.agents/skills/return-of-zero-*/SKILL.md` path references (`.claude/skills/` are symlinks — do not edit).
4. Node-level links: repo-wide grep for `episteme/arguments`, `episteme/conjugate`, `episteme/concepts`, `episteme/products`; rewrite path-style markdown links and path-style wikilinks. Basename wikilinks (`[[C41-...]]`) survive — leave them.
5. Check the generators for hardcoded assumptions about the `section-rooms/` layout (`tools/build-section-rooms.py` generates the README/ROOM layer): update GENERATOR SOURCE where needed, then rebuild. Never hand-edit generated output.
6. Rebuild all generated surfaces, run each builder `--check`, run `tools/audit-room-depth.py` and `tools/audit-reader-navigation.py`, then `python3 -m unittest discover -s tests -v`.

Do NOT touch: `episteme/sources`, `lenses`, `maps`, `figures`, `dossiers`, `etymologies`, `histories`, `aphorisms`; the content of any moved file (not even `reference-notes/`); no prose edits; no git commits. If a test or audit cannot pass without a design decision, STOP and name the debt in the report.

Report → `.wayfinder/research/028-migration-report.md`: what moved (counts), every reference class updated with counts, verbatim tail of the suite run, anything stopped.

## Resolution

Closed 2026-09-25 by the integrator. Full report at `.wayfinder/research/028-migration-report.md` (plus the binding annex `028b-binding-report.md`). Final state: all four suites moved (174 records + shelves), 21 legacy carriers frozen in `working/legacy/section-rooms-arguments/`, zero stale `episteme/{arguments,conjugate,concepts,products}` references, all builders `--check` clean, reader-navigation 288 admitted / 0 missing / 0 unreachable, today's 190 deposits bound and reachable, and the **full unittest suite green: 123 tests, OK**. Repairs beyond the letter of the ticket (all named in the report): restored the load-bearing p2 receipts/audits the desk retirement had moved; translated pre-migration homes in the T25 receipt generator, dispatch queue and census; refined `live_quilts` to treat the quilt register index as navigation rather than recovery input; ported the hand-polished section-rooms and symbolon README prose into their lawful generator sources; restored the manuscript's section-room reading routes and removed an assembly-duplicated anchor.
