# 028 — Migration of the canonical A/C suite into section-rooms

Executed 2026-09-25 under Frank's ratified decision (central-plan amendment, same date). The first dispatch agent completed the physical migration, the governing-doc sweep and most reference updates, then timed out; the integrator finished the remainder. This report covers the whole ticket.

## What moved

| From (`symbolon/episteme/`) | To (`section-rooms/`) | Files |
|---|---|---|
| `arguments/` (A01–A36 + README) | `section-rooms/arguments/` | 37 |
| `conjugate/` (A01′–A36′ + README + AC.md) | `section-rooms/arguments/conjugate/` | 38 |
| `concepts/` (64 C-nodes, 22 loose topics, indexes, `reference-notes/`) | `section-rooms/arguments/concepts/` | 91 |
| `products/` (S, S0–S5, README) | `section-rooms/arguments/products/` | 8 |
| legacy 21 carriers (were in `section-rooms/arguments/`) | `working/legacy/section-rooms-arguments/` | 21 |

`episteme/` keeps: aphorisms, atlas, dossiers, etymologies, figures, histories, lenses, maps (+ `navigation/`), sources.

## References updated

- `the-return-of-zero-central-plan.md` — all path links rewritten; amendment appended ("The canonical A/C suite moves into the rooms"), ratified-voice, per the plan's convention.
- `AGENTS.md`, `WRITING-PROTOCOL.md`, `docs/REPOSITORY-SHAPE.md` — structural rows and prose updated to the ratified homes (incl. dialogues drop, see below).
- `tools/` — `build-section-rooms.py`, `build-navigation.py`, `okf-workspace.py`, `build-t25-refinement-admission.py`, `audit-reader-navigation.py` expectations updated; navigation class registry pruned of the retired dialogues entry.
- `tests/` + `tests/fixtures/retired-bkmr-coverage.json` — path rewrites applied.
- Node-level links — 14 files of path-style wikilinks/markdown links rewritten (`symbolon/episteme/{arguments,conjugate,concepts,products}` → `section-rooms/arguments/…`); the generated `maps/navigation/AUDIT.md` regenerates rather than hand-edits; the Neumann source `-NOTES.md` (protected) was left untouched by design.
- Residual stale references in the essay body and tooling: **0** (grep-verified).

## Repair beyond the letter of the ticket (named, not silent)

1. `working/p2-enrichment/receipts/` and `pre-manuscript-refinement-2026-09-10/T25-current-census-acceptance.json` had been retired by the desk-consolidation ticket as receipts, but they are load-bearing inputs of `tools/audit-reader-navigation.py` and `tools/build-t25-refinement-admission.py`. Restored to live paths; correction annotated in the retire manifest.
2. `build-t25-refinement-admission.py` inherited the pre-migration `canonical_home` values from the immutable T20–T21 baseline, leaving 137 admitted records unresolvable to the reader-navigation audit. The generator now applies the ratified home-translation (identities and bytes unchanged; standing text states this). Receipt regenerated: **288 admitted, 0 missing, 0 unreachable**.
3. The empty `episteme/dialogues/` register was dropped to `working/_to_delete/2026-09-25-retire/dialogues-register/` under ticket 039 (same-day Frank decision), with its own plan amendment and shape-doc/registry updates.

## Verification

- `build-section-rooms.py` + `--check` — 8 rooms, clean.
- `build-navigation.py` + `--check` — 62 generated surfaces, fresh.
- `build-source-projections.py` + `--check` — 3 projections, current.
- `audit-room-depth.py` — PASS across rooms (00–07).
- `audit-reader-navigation.py` — 288 admitted / 0 missing / 0 unreachable.
- Full unittest suite — see ticket resolution comment for the final run.
