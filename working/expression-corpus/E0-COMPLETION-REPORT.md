# E0 — Return-of-Zero Expression corpus: parent integration return

**Date:** 2026-09-17 · **Owner:** issue #65 (EpiLogos/Antykathera-Essay-Work)
**Execution:** one parent session (E0) + exactly six content-production subagents, per
`docs/EXPRESSION-CORPUS-PRODUCTION-ALIGNMENT.md` §7 and `.wayfinder/maps/expression-corpus-production.md`.
**Material authoring surface:** EpiLogos/Point-Cloud-Demo `production/return-of-zero/`.

## 1. Canonical census revision

- **Source:** Antykathera-Essay-Work main @ `dbf3b17` (fast-forwarded 211 commits at session start).
- **Census:** `working/pre-manuscript-refinement-2026-09-10/T25-current-census-acceptance.json` — 288 records
  (36 A + 36 A′ + A/C + 64 C + 7 S-family + 80 Matheme + 13 Symbolon + 25 Whole Mythemes + 10 histories
  + 7 dossiers + 6 etymologies + 2 lenses + 1 aphorism), plus publication surfaces #0/#5
  (sovereign essay, reading root, 8 rooms, 48 movements).
- **Finding returned to the T25/T26 owners:** the receipt's sha256 values are stale at HEAD for
  **163/288 records** (content moved at `5c22906` without a receipt rebuild; the builder's `--check`
  does not verify base-record hashes). All corpus bindings therefore carry actual-bytes hashes
  computed at `dbf3b17`. The receipt refresh belongs to the pre-manuscript programme before T26
  ratification — not silently done here, because that receipt is the packet the owner is being asked
  to ratify.

## 2. Six worker statuses

| Worker | Scope | Status |
|---|---|---|
| E1 essay-rooms | sovereign essay + 8 rooms + 48 movements | complete — 9 artifacts, 57 scenes, validated + captured |
| E2 arguments | A01–A36 + A01′–A36′ | complete — 2 artifacts, 72 scenes, validated + captured |
| E3 episteme | C01–C64 + A/C + S/S0–S5 + histories/dossiers/etymologies/lenses/aphorism | complete (second dispatch; first died on a rate limit) — 8 artifacts, 102 scenes |
| E4 matheme | Matheme register, 12 domains | complete — 6 artifacts, 80 scenes |
| E5 symbolon | twelvefold root + spine-index + whole/register relation | complete — 2 artifacts, 19 scenes |
| E6 mytheme-wholes | 25 Whole Mythemes | complete — 25 artifacts, 143 scenes |

Durable worker returns: `production/return-of-zero/bindings/E{1..6}-return.md`.

## 3. Source → artifact inventory

Generated, rerunnable: `working/expression-corpus/build-inventory.py` →
`E0-INVENTORY.json` (record-level: source id, type, register, canonical home, actual sha256,
assigned family, artifact + scene id, hash verification, coverage; artifact-level: journey,
scenes, cover, binding, profile lineage) + `E0-COVERAGE.md` (readable summary).
This is the Pass-C reconciliation tool: rerun after any accepted source change; it diffs and
reopens only affected artifacts.

## 4. Corpus

- **52 Expression artifacts** (all `oi.journey` v1), **473 scenes**, every artifact validated
  against the real schema (`tools/validate.mjs`), passed through the app's real import gate
  (`scripts/production-inventory.ts` — 2 namespaces, all import, namespaces disjoint), and covered
  by a real-engine capture (`tools/capture.mjs`, SwiftShader render).
- **52 binding records** with per-scene source bindings (record id, canonical path, sha256),
  verbatim declared relations, assets with provenance, craft notes.
- **12 profile documents** under `profiles/` (corpus base + register + family granularities).
- No HTML companions were admitted as load-bearing this pass (E4 evaluated and skipped as
  redundant); the form remains available when O:I #352 scene bodies land.

## 5. Coverage

| Family | Covered |
|---|---|
| Essay + rooms (E1) | 9/9 artifacts; 8 rooms × 6 movement scenes; essay path §0/1→§5→0 + return |
| A / A′ (E2) | 72/72 records |
| Episteme (E3) | 98/98 records (64 C + A/C + 7 S + 26 other carriers) |
| Matheme (E4) | 80/80 records |
| Symbolon (E5) | 13/13 records + whole/register staging |
| Whole Mythemes (E6) | 25/25 wholes, sequenced whole-arc journeys |
| Publication surfaces | 57/57 (essay, reading root, 8 rooms, 48 movements) |
| **Census** | **288/288 records covered, hash-verified** |

Explicit dispositions (non-Expression this pass): source houses (evidence class, bound through
consumers' `source_ids`), maps, dialogues, figures, atlas — none are in the 288-record admission.

## 6. Preservation highlights (spot-checked by E0 acceptance)

E0 ran an acceptance pass over covers and sent three targeted repair tasks back to the
workers; all landed before close: E1 re-laid the essay/room text-and-formation relation
(formation shift + stacked route block; 7 mid-path scenes spot-checked clean, 9 covers
re-captured), E2 gave all 72 A/A′ scenes a three-layer text grammar and cleared A30/A30′
by vertical nesting (6 scenes spot-checked, both covers re-captured), E6 found the root
cause (screen-inverted world-y plus `autoFitSizes` refitting), set it false, and ran a
model-verified clearance pass over all 143 mytheme scenes (23/25 artifacts adjusted,
25 covers re-captured). Final sweep: all 52 artifacts valid, import gate clean, 52/52 covers.

- Rooms: canonical slugs/titles verbatim; previous/next and the M48→M01 Return carried as data;
  withholdings hold in imagery (no Antikythera mechanism before movement-45, no `0/1` before
  movement-18, `Ø` exactly once with its one job at movement-16).
- A/A′: one family grammar each; every record addressable (scene ids `a01…a36`, `a01p…a36p`);
  other-face, A/C-root, room/movement service and declared relations preserved verbatim; A′ given
  its own registered treatment (print/cool) as the technological face.
- Episteme: five distinct grammars (concept / product with both lens bodies per pair / history /
  dossier / etymology); A/C's frozen *Respect for Experience* ethic carried by reference, never restated.
- Matheme: derivations shown as operations — mandala plate per the canonical geometry, both Spanda
  equations, crossed-zero step sequence, `2+2²=4+2`, torus cover/winding, `16/9·9/8=2/1` with cymatic
  material; claim-status bands ride every kicker.
- Symbolon: containment staged (whole holds the three registers, distinct, no fourth sibling);
  twelvefold spine order `−/− → 0/1 → ?/! → −/+ → X/x → AM/IS → ∞/dx → 1/0` with four-head traversals.
- Mythemes: whole-first honoured — every artifact runs situation→relation→transformation→ending;
  derivative occurrences indexed (never cards); `human-amplified` flags carried; only declared
  cross-story relations admitted.

## 7. Profile / family continuity

`roz-corpus-base` (stage/material/typography/rhythm baselines + register differentiations) →
register profiles (essay/print-episteme/dark-matheme/round-mytheme/deep-symbolon) → family profiles
(section-room positional chassis, argument/conjugate, concept/product/history/dossier/etymology,
hellenic/frank-taylor worlds) → per-scene overrides recorded in bindings. Craft baselines only;
no profile claim is a semantic claim.

## 8. Content-arising visual vocabulary

Authored forms only (provenance clean by construction; no external imagery admitted): the notation
glyphs (`0/1`, `1/0`, `Ø`, `X/x`, `/ = −/−`, `(0/1)/(1/0)`, `4+2`), the positional chassis
(disc/text/triangle/yantra/square/ring), the concentric mandala geometry, stream-and-stations
(histories), evidential plate (dossiers), centre-envelope-six-operations (etymologies), occurrence-indexed
story fields (mythemes). Occurrence refs are in the bindings' `assets` fields; repetition confers no
semantic standing.

## 9. Returned expressive-practice evidence

Recorded in the worker returns for the existing Aletheia/Epii/Skill path: the 10-formation grammar
consolidation (density forces compositional choices), fit-to-box glyph rasterisation, sequence-still
phase dependence, dark-scene ink behaviour, margin-column layouts as the reliable text/field relation,
quiet pages staying quiet, "no repaired marriage ends it" — story endings qualifying beginnings as
scene sequencing, not epilogue text. No corpus runtime, no corpus personas, no new scene schema.

## 10. Point-Cloud shared defects

Consolidated list for Point-Cloud-Demo #6:
`production/return-of-zero/bindings/E0-POINT-CLOUD-DEFECTS.md` (12 items; headline: validator/runtime
32-vs-10 formation mismatch, capture scene navigation, fit-to-box glyph rasterisation). None patched
per-lane; three unrelated editor defects were already repaired once by the parallel enablement
session (`9de1105`) and are noted as landed.

## 11. QL semantic defects

None found against the canon this pass. The one semantic-adjacent finding is the essay-side census
receipt staleness (§1), returned to the T25/T26 owners.

## 12. Remaining submission gaps

1. **Pass B / runtime proving:** artifacts are sandbox-authored `oi.journey` files; loading them
   through the O:I desktop cradle's integrated engine, scene bodies, portals and the graph↔Expression
   shared-ref field (O:I #352, #306, #335) remains O:I-owned and unexercised here.
2. **T26 reconciliation:** Frank's ratification will change sources; rerun
   `working/expression-corpus/build-inventory.py`, diff, and reopen only affected artifacts.
3. **Census receipt refresh** before T26 (T25 owners).
4. **Owner review:** treatments are authored and craft-checked; Recognition of the corpus's
   expressive standing is Frank's act.
5. **Non-Expression carriers** (sources/maps/dialogues/figures/atlas) keep their disposition unless
   the owner admits them into a later tranche.
