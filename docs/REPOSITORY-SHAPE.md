---
title: "Repository Shape — Functional Map"
page_type: repository-map
authority: non-governing locator
status: living
date: "2026-08-08"
---

# Repository Shape — Functional Map

This is the one-file map of the whole repository: what each surface **is**, what authority it carries, where a reader or agent enters it, and where it lands in the final shape. It exists so the repo does not have to be reconstructed from scattered reads. The final shape and its rules are fixed in `WRITING-PROTOCOL.md` (§3–§5, §14) and governed by `AGENTS.md`; this file only maps them onto the current tree.

## Read-first order

1. `README.md` — orientation and the argument in brief.
2. `AGENTS.md` — agent conduct, authority order, skill routing.
3. `WRITING-PROTOCOL.md` — workflow and publication-shape authority.
4. `the-return-of-zero-central-plan.md` — sole structural authority.
5. `return-of-zero-orienting-principles.md` — mandatory pre-load before touching any section, argument, room, or dossier.
6. This map — where everything sits and where it is going.

## The four classes

Every content record belongs to one of the four classes, and the classes organise the writing and content itself:

| Class | What it carries | Home |
|---|---|---|
| **Symbolon** | The whole relation and its root records: `0/1`, `1/0`, the slash, self-identity, mono–poly, complexio oppositorum, the eight determinations. | `submission-package/essay/symbolon/` root |
| **Matheme** | Exact operations: QL, Spanda, topology, harmonics, formal neighbours, computation, diagrams. | `submission-package/essay/symbolon/matheme/` |
| **Mytheme** | Lived forms: myth, narrative, poetry, media, art, music, plates. | `submission-package/essay/symbolon/mytheme/` |
| **Episteme** | Instituted knowledge: sources, histories, etymologies, lenses, maps, dossiers, figures, concept nodes, dialogues. | `submission-package/essay/symbolon/episteme/` |

Sources are the evidence class inside Episteme (`submission-package/essay/symbolon/episteme/sources/<domain>/<author>/<source_id>/SOURCE.md`). Placement is by operation, not by folder wish; a record's `register` is declared metadata independent of its node type.

The sovereign essay and the authoring rooms sit **parallel to the symbolon root**, not inside the field. The publication-level sixfold is the 4+2 with fixed offices: `#0` the rooms (each holds its movements with the shared argument field as a nested `0/1`), `#1` Symbolon, `#2` Matheme, `#3` Mytheme, `#4` Episteme, `#5` the essay. The four infer into the rooms; the enriched rooms improve the essay and enable file-by-file generation of the inner stacks under `#1`–`#4` as the holographic world of the piece — the repo operates as the logic. OKF is a formatter/validator over the vault, not a generator; the writing protocol generates the files.

## Current map — surface by surface

| Path | What it is | Authority | Entry | Final home |
|---|---|---|---|---|
| `README.md` | Orientation + argument in brief | non-governing | — | stays |
| `AGENTS.md` | Agent conduct and authority order | governing | — | stays |
| `WRITING-PROTOCOL.md` | Workflow + publication-shape authority | governing, subordinate to plan | — | stays |
| `CLAUDE.md` | Companion orientation (Claude-facing) | non-governing | — | stays |
| `docs/REPOSITORY-SHAPE.md` | This map | non-governing | — | stays |
| `docs/plans/` | Dated development plans | provenance | — | stays |
| `submission-package/essay/` | **THE publication body** — the one home: rooms `#0`, the field `#1`–`#4`, essay `#5` | canonical publication body | `README.md` | stays (final home) |
| `the-return-of-zero-central-plan.md` | Sole structural authority | governing | — | stays governing |
| `return-of-zero-orienting-principles.md` | Mandatory orientation | governing, subordinate | — | stays |
| `submission-package/essay/THE-RETURN-OF-ZERO.md` | Sovereign manuscript | sovereign | — | parallel to `symbolon/` (publication 4+2, position `#5`) |
| `submission-package/essay/section-rooms/` | The rooms (`#0`): each room holds its six movements under `movements/` (the `1`s) with the shared argument field under `arguments/` (the `0`) — the nested `0/1` of the essay's structured potential | canonical granular argument | `section-rooms/README.md` | publication `#0`, parallel to `symbolon/` |
| `submission-package/essay/section-rooms/arguments/` | The 21 argument nodes — the implicate `0`-field of the rooms | canonical granular argument | — | stays with the rooms (`#0`) |
| `submission-package/essay/section-rooms/<room>/movements/` | The 48 section movements, six per room — the explicate `1`s | canonical granular argument | each room's `ROOM.md` | stays with the rooms (`#0`) |
| `submission-package/essay/symbolon/episteme/concepts/` | The 22 concept nodes + Concept Map (`index.md`) | canonical granular argument | `index.md` | stays (`episteme/concepts/`) |
| `submission-package/essay/symbolon/episteme/concepts/reference-notes/` | 90 reference notes recovered from git HEAD, 2026-08-08 | quilt-pending working shelf | `README.md` | quilted into the concept layer |
| `submission-package/essay/symbolon/episteme/maps/` | The 4 transverse paths | canonical granular argument | `return-of-zero-braided-traversal.md` | stays (`episteme/maps/`) |
| `submission-package/essay/symbolon/episteme/sources/` | 124 canonical source houses + projections | canonical evidence | `SOURCE-INDEX.md` | `symbolon/episteme/sources/` |
| `working/sources-texts-references/chat-logs-for-quilting/` | Raw Taylor chat transcripts | raw provenance | houses under `internal-corpus/taylor/chat-logs/` | stays as `local_copy` shelf; dialogue records migrate to `episteme/dialogues/` |
| `working/sources-texts-references/Epi Paper Write-ups/` | Frank-authored papers (P0–P5, Symbolon Dynamics, Advent of Zero, …) | authorial internal corpus | their `SOURCE.md` houses | internal-corpus houses → `episteme/sources/`; mythemic operations → `mytheme/` |
| `working/sources-texts-references/Epi Phone Writings/` | Raw Frank fragments | authorial raw | — | internal corpus or `mytheme/` (poetry/narrative) — placement by Frank |
| `working/sources-texts-references/` root files | Core theorems, QL rewrite, poem set, Kaplan notes, lecture notes, meal outline | authorial/raw/working | — | internal houses or `mytheme/` by operation |
| `submission-package/essay/symbolon/episteme/histories/` | 10 history clusters | living canonical histories | `HISTORY.md` files | `symbolon/episteme/histories/` |
| `submission-package/essay/symbolon/episteme/etymologies/` | 5 etymology clusters (protected learning surface) | protected | `README.md` | `symbolon/episteme/etymologies/` |
| `submission-package/essay/quilt/agentworld-response-matrix.md` | Venue concordance | supporting | — | `episteme/maps/` |
| `submission-package/essay/quilt/ql-expression-grammar.md` | Expression law (form only) | subordinate | — | carries into Matheme records |
| `working/process-ledger.md` | Append-only agent-navigation lessons | non-governing | — | stays (mined for skills) |
| `submission-package/essay/quilt/2026-08-02-PARALLEL-HARMONISED-QUILT.md` | Live pre-propagation ledger | working ledger | — | stays live through quilt review |
| `submission-package/essay/quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md` | Append-only session contribution ledger | superseded working surface | — | frozen after harmonised quilt ratification |
| `working/_to_delete/` | Frank's live deletion queue | — | — | his call |
| `working/legacy/` | v1/v2 structures | frozen provenance | — | stays frozen |
| `working/` | Non-publication development surfaces: ledgers, raw authorial shelves, working drafts, deletion queue | non-canonical | `README` | stays as working desk |
| `submission-package/` | Manifest, Epi-Logos plugin, Epi-Card, essay body, design provenance | submission artifacts | `README.md` | ships; the essay body is its own home |
| `writing-guidance-tools/` | Writing laws, rubric, calibration | load contract | `README.md` | stays |
| `tools/` | Retrieval, generation, freshness, resolution | tooling | — | stays; operates on the essay body |
| `tests/` | Real workspace + publication checks | verification | — | stays; source-path expectations updated to resolver |
| `definition-of-god-working/` | Raw authoring area for Definition of God drafts and chats | authorial raw | its `SOURCE.md` houses (`local_copy` points here) | stays as raw shelf |
| `epi-logos-plugin-resources-copy-10-07/` | Reference copy (central plan `resource:` target) | reference | — | stays while the plan references it |
| `refs-sources-args.base` | Obsidian Base over the evidence field | locator | — | replaced by the vault graph at migration |
| `.wayfinder/` | Separate wayfinding tracker | external tool state | — | classify or remove — Frank's call |

## Debris removed and recovered — 2026-08-08

- `essay-workshop/sources-texts-references/reference-notes/` (90 files) — deleted on 2026-08-08, then **recovered the same day** under the concept system at `submission-package/essay/symbolon/episteme/concepts/reference-notes/` as a quilt-pending working shelf (Frank's direction). Its granular points resolve into the concept nodes and source houses on quilting.
- `Antykathera Essay Work.md` and `Antykathera Concept Index.md` — deleted. The README and the Concept Map (`nodes/concepts/index.md`) supersede them. Recoverable in git history.

Seven wikilinks in the authorial core-theorems file (`10-7-2026-core-theorems-pithy.md`) now dangle against the deleted layer. The file is Frank-authored, so the corrections are his edit (or his call for the agent to make); proposed live targets:

| Line | Dangling link | Proposed live home |
|---|---|---|
| 17 | `[[Antykathera Essay Work]]` | `[[README]]` |
| 138 | `[[Bohm–Krishnamurti Dialogues — Running True and the Observer-Observed]]` | `[[bohm-krishnamurti-1975-05-18-dialogue]]` or argument `[[Bohmian Enfoldment and Dialogical Return]]` |
| 460 | `[[Torus — Circulation, Magnetic Confinement, and Energy]]` | argument `[[Toroidal Circulation and the Arche-Topos]]` or house `[[ITER — What Is a Tokamak]]` |
| 518 | `[[David Bohm — Implicate Order, Explicate Order, and Holomovement]]` | argument `[[Bohmian Enfoldment and Dialogical Return]]` or house `[[Bohm — Wholeness and the Implicate Order (1980)]]` |
| 576 | `[[Henri Bergson — Duration and Creative Evolution|Bergson]]` | no live home yet — open acquisition debt |
| 576 | `[[Whitehead Creativity|Whitehead]]` | house `[[Whitehead — Process and Reality (1978 corrected edition)]]` |
| 576 | `[[Jean Gebser|Gebser]]` | house `[[Gebser — The Ever-Present Origin (1985)]]` |

The two `reference-notes/apoha` and `reference-notes/bimba-pratibimba` links noted in the earlier draft were already resolved to their live concept nodes and do not dangle.

## One-home rule

The essay body at `submission-package/essay/` is the final home. Content is added by ratifying and **moving** (never copying); links, authority declarations, retrieval tools, and tests are updated with the move. `working/` never becomes authority, and nothing is maintained as a generated duplicate of the essay body. The retired `essay-okf` bundle and its builder have been removed.

## Open placement decisions (Frank's calls)

- `Epi Phone Writings` — internal corpus houses vs `mytheme/poetry` / `mytheme/narrative`.
- `_to_delete/` — contents of the deletion queue.
- `.wayfinder/` — keep, classify, or remove.
- Core-theorems dangling links — correction by Frank or by agent on his word.
- Per-node `register` composition on the 48 movements, 21 arguments, and the argument map — which registers each node admits and carries (concepts and paths are ratified to `episteme`; the rooms lineage awaits Frank's register-composition assignments).
- The single home for the OKF schema (root-level spec vs plugin reference).
