# P1 — the remaining Expression corpora: parent integration return

**Date:** 2026-09-21 · **Owner:** issue #65 (EpiLogos/O-I), corpus-production obligation
**Follows:** the proven E0 pattern (`docs/EXPRESSION-CORPUS-PRODUCTION-ALIGNMENT.md`, `E0-COMPLETION-REPORT.md`)
**Commission:** parent pass for the remaining corpora — the six products' corpora and the
distinct Epii M5-1/Antichrist corpus. Build, don't block: census frozen per corpus with
receipts, first production wave landed where material is ready, actionable coverage map for
the next fan-out.

---

## 1. Where the corpus enumeration comes from

The canonical corpus map is the corpus-production row of the W7 collection/source
continuation (`O-I .wayfinder/maps/techne-expression-mode.md`, mirrored in
`desktop/cradle/tests/collection-acceptance.md`), and O-I#65 comment 5751853578 names what
remains: *live Bimba/Atlas collections under the native collection law (needs a shape
proposal), the #417 publication tuple, and the six-products / Epii M5-1/Antichrist corpora.*

The six products are the canonical product field (`O-I docs/CANONICAL-PRODUCT-FIELD.md`):
Central (0), Actuation (1), AIKit (2), Software Factory (3), Workcell (4), Quaternal Logic (5).
O:I is the containing product; its own corpus is the Return-of-Zero corpus, **complete and
out of scope here** (92 committed native members at `0b18c11b`, full 288-record census
covered; census receipt refreshed and merged as Antykathera-Essay-Work #71 / `f2dcfc28`).

The Epii M5-1/Antichrist corpus is a distinct authored source per
`docs/experience/INHABITED-SYSTEM-ORIENTATION.md`; the O:I cradle names its ground
verbatim: *"The Epii M5-1 essay and the Antichrist vault are held outside this app"*
(`desktop/cradle/src/epilogos/sources.ts`).

## 2. Census receipts (frozen this pass)

Generator, rerunnable: `working/expression-corpus/build-p1-census.py` → one JSON receipt per
corpus, T25/E0 pattern (source revision, record count, per-record hashes). Product censuses
hash bytes straight out of git object storage at each repo's HEAD — dirty working trees are
never touched and never frozen.

| Receipt | Corpus | Ground | Status | Count |
|---|---|---|---|---|
| `P1-census-epii-antichrist.json` | Epii M5-1 / Antichrist | EpiLogos/research-canvas `antichrist-vault/` @ `7df35f8` (redemption-run-2) | **frozen** | 24 manifest-admitted records (2 episode-chats, 3 episode-scripts, 7 ql-units, 1 sourcebook, 9 research-reports, 2 ledgers) |
| `P1-census-bimba.json` | Bimba (Quaternal Logic product corpus) | Point-Cloud-Demo `production/bimba/` + QL-MEF `fixtures/kernel/m-tree-v1.json` | **verified-existing** (not re-frozen) | 19 corpus artifacts found = the M0-M5 manifest's 13 + 6 claim, byte-hashed; 32 binding records; import gate rerun OK |
| `P1-census-central.json` | Central | EpiLogos/Central @ `87341be4` (main) | frozen-census-basis | 61 committed .md records |
| `P1-census-actuation.json` | Actuation | EpiLogos/Actuation @ `0ac23bf` (techne/deep-conjugate-allowance) | frozen-census-basis | 157 records |
| `P1-census-aikit.json` | AIKit | EpiLogos/ai-kit @ `9ec7040` (techne/model-dispatch-generalization) | frozen-census-basis | 104 records |
| `P1-census-factory.json` | Software Factory | EpiLogos/Factory @ `fbabaaa` (techne/telemetry-watch-compare-settings) | frozen-census-basis | 230 records |
| `P1-census-workcell.json` | Workcell | EpiLogos/Workcell @ `5ddf156` (main) | frozen-census-basis | 30 records |
| `P1-census-quaternal-logic.json` | Quaternal Logic (repo prose) | EpiLogos/QL-MEF @ `81d1af1` (session/k-aw-expression-production-2026-09-17) | frozen-census-basis | 148 records |

Two honesty rules the receipts carry so they cannot be over-read:

1. **"frozen-census-basis" is not an admission.** No canonical authored-record census exists
   for any product's Expression corpus (unlike the essay's T25 census or the Bimba m-tree
   registry). Each product receipt freezes its committed authored-prose surface (.md at HEAD,
   sha256 over exact blob bytes) as the basis an owner or product lane can admit *from*.
   Which records are corpus members is an owner disposition, per product.
2. **The Epii/Antichrist admission boundary already exists** — the vault's own
   `knowledge-manifest.json` (schemaVersion 1, contentRevision 2) is the source programme's
   census seed; the receipt freezes its 24 admitted records against actual bytes. Every
   frozen record is byte-identical to the published remote (`origin/main` `038a8302`;
   zero drift), so the public receipt leaks nothing unpublished. Records on disk outside the
   manifest (positions 0–5, double-helix, supporting-bits essays) are explicitly *not*
   admitted this pass.

## 3. Wave 1 — produced through the full E0 gates

The one corpus whose material is complete and admitted per its own source: **Epii
M5-1/Antichrist**. Landed in Point-Cloud-Demo `production/epii-antichrist/` (new namespace,
root-law contract in its README; one row added to the shared namespace table), on branch
`corpus/epii-antichrist-wave1-20260921`.

| Artifact | Family | Scenes | Source records |
|---|---|---|---|
| `epii-ep1-ql-units.journey.json` | ep-1.1 QL units | 7 | the manifest's 7 ql-unit records, one scene per record, in the records' own dependency order (parent → ontological → solar system → social/power → deficiency → Devil's chain → Christ's chain) |
| `epii-ep1-naked-face.journey.json` | episode 1.0 whole | 10 | `Episode_0_1_The_Naked_Face_v9.md` (13,162 words), its ten movements in order — whole-first law: the quilting return qualifies the opening poem |

Gate transcripts (all executed 2026-09-21):

- **Generation (real model API):** `npx tsx /tmp/epii-antichrist-wave1.mts` →
  `epii-ep1-ql-units: validate ok (7 scenes), import ok` ·
  `epii-ep1-naked-face: validate ok (10 scenes), import ok` — `validateJourney` (strict
  schema) and `importDocuments` (the app's real Import gate) kept in the loop per the
  namespace root law.
- **Schema validator:** `node production/return-of-zero/tools/validate.mjs <both artifacts>`
  → `VALID … scenes=7 […]`, `VALID … scenes=10 […]`, `all artifacts valid` (shared tool,
  unmodified).
- **Cross-namespace import floor:** `npx tsx scripts/production-inventory.ts` →
  `production inventory OK: 3 namespace(s), every journey file imports, namespaces disjoint`.
- **Real-engine covers:** `node production/return-of-zero/tools/capture.mjs <artifacts>`
  (SwiftShader) → both covers captured and visually inspected: the units cover shows the
  four-prepositions-around-the-ground scene with its margin-column text; the episode cover
  shows the opening O of the poem movement.
- **Bindings:** `bindings/epii-ep1-ql-units.binding.json` (per-scene source bindings with
  sha256 at `7df35f8`) and `bindings/epii-ep1-naked-face.binding.json` (every scene binds
  the v9 script record; each scene's `source_ref` names its exact movement heading, verified
  present in the bound bytes at freeze time).
- **Profiles:** `profiles/epii-antichrist-corpus-base.profile.json` + `family-ql-unit` +
  `family-episode` (craft baselines + lineage only; no profile claim is a semantic claim).

Source law honoured: scene texts compress and quote the vault records, never invent claims;
relations staged only where the records name them (no manufactured graph edges); the
episode's "Held for 0.2/0.3" lists respected; presentation mappings (tints, formations,
forces) declared as craft in the artifacts' descriptions and binding notes.

**Shared defect reconfirmed live, not patched:** per-scene capture navigation is unreliable
(E0-POINT-CLOUD-DEFECTS #2) — `--scene-id` and `--all-scenes` runs render scene 1 and the
navigation throws (`Cannot read properties of undefined (reading 'transition')`; the
catalogued `openScene`-does-not-exist path). Covers therefore use the first-scene path the
defect list names reliable. Mid-scene *visual* inspection is not achievable with the shared
tool; scene correctness rests on the schema + import gates and the binding anchors.

## 4. Corpus-by-corpus coverage map

| Corpus | Material ground | Census | Production | Next dispatch |
|---|---|---|---|---|
| **O:I (Return-of-Zero)** | Antykathera-Essay-Work + Point-Cloud `production/return-of-zero/` | verified (T25 receipt refreshed, #71) | **complete** — 52 artifacts / 473 scenes; 92 committed native members @ `0b18c11b` | none here; Pass B runtime proving stays O:I-owned |
| **Bimba / collections / Atlas** (Quaternal Logic product corpus + O-I collection law) | QL-MEF `fixtures/kernel/m-tree-v1.json` (1,876 nodes / 21,083 relations); Point-Cloud `production/bimba/` | **verified** (19/19 artifacts, manifest claims true, gate rerun OK) | **in-flight, owned lane** — two cuts landed (13 + 6 artifacts); QL checkout carries the active K/AW production lane (`session/k-aw-expression-production-2026-09-17`, dirty) | the owning lane's third cut (depth-4 widening, covers via renderer); live Bimba/Atlas collections need the named shape proposal (O-I#65 comment 5751853578). This pass did not touch the lane |
| **Epii M5-1 / Antichrist** | research-canvas `antichrist-vault/` @ `7df35f8`, admitted by its knowledge manifest | **frozen** (24 records, zero published drift) | **wave-1 done** — 2 artifacts / 17 scenes through all gates + covers | next workers: (a) episode 2 whole ("The Fire of the Gods" v4 + its 9 research reports as a research-ledger family); (b) the Naked Face sourcebook (`The_Naked_Face_Full_Quotes_v7.md`) as a quotes/read-block family; (c) owner question first: admit the on-disk-but-unmanifested ql-units (positions 0–5, double-helix) and locate the M5-1 essay itself for the corpus's essay register |
| **Central** | EpiLogos/Central (authored docs surface) | frozen-census-basis (61 records @ `87341be4`) | not started | owner disposition first: what Central's corpus *is* (its product docs vs its authored governance ground — the latter is personal source and must not be published into a public namespace); then packet generation per the alignment doc §1 |
| **Actuation** | EpiLogos/Actuation | frozen-census-basis (157 @ `0ac23bf`) | not started | same owner disposition; the checkout is an active research lane — census only until it settles |
| **AIKit** | EpiLogos/ai-kit | frozen-census-basis (104 @ `9ec7040`) | not started | same owner disposition; docs/v2 design corpus is the natural candidate ground |
| **Software Factory** | EpiLogos/Factory | frozen-census-basis (230 @ `fbabaaa`) | not started | same owner disposition; largest authored surface of the six |
| **Workcell** | EpiLogos/Workcell | frozen-census-basis (30 @ `5ddf156`) | not started | same owner disposition; smallest surface — likely the cheapest first product-corpus pilot once admission exists |

**Blocker named honestly, not invented:** the five product corpora have no canonical
authored-record census or admission disposition anywhere in the sources read for this pass
(O-I#65 and its corpus comments, the alignment docs, the products' repos). Producing
Expression artifacts from a product's docs without that disposition would manufacture a
corpus nobody authored. The receipts give each product a hash-verified basis so the
disposition can be made record-by-record.

## 5. What is verified vs not

- **Verified by execution:** both wave-1 artifacts pass the real schema validator and the
  app's real import gate; the cross-namespace floor passes (3 namespaces, disjoint); both
  covers are real-engine renders inspected as images; all 24 epii/antichrist census records
  hash-verified and proven byte-identical to the published remote; all 19 bimba artifacts
  re-hashed and counted against the existing manifest; the census generator reruns.
- **Verified by read-only inspection:** every repo revision, branch and dirty-file count in
  this report was read live on 2026-09-21; no dirty tree was touched, no branch switched in
  any dirty checkout, nothing reset.
- **Not verified / not claimed:** mid-scene visuals of the wave-1 artifacts (shared capture
  defect #2 — reconfirmed with the exact error, returned unpatched); corpus-completeness of
  anything (wave-1 ≠ corpus-complete); any product-corpus admission; the Bimba lane's
  in-flight third cut; the QL-side registry pins (quoted from the bimba manifest, not
  re-derived — the QL checkout is a live lane).

## 6. Plumbing of this return

- Point-Cloud-Demo branch `corpus/epii-antichrist-wave1-20260921` — namespace
  `production/epii-antichrist/` (README, 2 artifacts, 2 covers, 2 bindings, 3 profiles) +
  one namespace-table row in `production/README.md`. No shared tooling modified.
- Antykathera-Essay-Work branch `corpus/p1-products-parent-20260921` (off `f2dcfc2`) —
  this report, the census generator, 8 receipts.
- Discussion return: O-I#65 comment with the corpus-by-corpus table.

---

## 7. CORRECTION (2026-09-21, appended after owner verification) — the S register IS the product-field admission

This file is a receipt, so the original text above stands unedited and this correction
appends. **The pass's central negative claim was wrong.** Section 2's honesty rule 1
("No canonical authored-record census exists for any product's Expression corpus") and
section 4's "Blocker named honestly, not invented" paragraph both asserted that the five/six
product corpora have no canonical authored-record census or admission disposition. They do.
The products' authored admission is the **S register of the Return-of-Zero essay corpus**,
and it was already frozen, covered and shipped when this pass was written.

### What the S register is (verified against the bytes, 2026-09-21)

Seven authored census records under register `episteme`, canonical home
`submission-package/essay/symbolon/episteme/products/`:

| Record | Type | Movement | MEF pair | Canonical home |
|---|---|---|---|---|
| `S` | product-field | — | — | `S-World-and-Life.md` (front-matter `members: [S0, S1, S2, S3, S4, S5]`) |
| `S0` | product | 37 | L0 Quaternal / L5′ Divine Logos | `S0-Central.md` |
| `S1` | product | 38 | L1 Causal / L4′ Scientific | `S1-Actuation.md` |
| `S2` | product | 39 | L2 Logical / L3′ Chronological | `S2-AIKit.md` |
| `S3` | product | 40 | L3 Processual / L2′ Alchemical-Elemental | `S3-Software-Factory.md` |
| `S4` | product | 41 | L4 Phenomenological / L1′ Phenomenal | `S4-Workcell.md` |
| `S5` | product | 42 | L5 Para Vāk / L0′ Archetypal-Numerical | `S5-Quaternal-Logic.md` |

Each carries `claim_status: Argued`, `register: episteme`, `product_parent: S`, dated
`source_ids` (the adopted commission, the native theorem, the O:I source projection, the
twelve-lens compilation), the product-local `A/C` constitution (S0/P0–P5 … S5/P0–P5),
`argument_relations` and `concept_relations` into the 36A/36A′/64C field, and the §5
movement assignment. Refinement standing is precise and varies: `S` and `S1` are
"T25 developed"; `S0`, `S2`, `S3`, `S4`, `S5` are "T25 reconstituted" (authorised
reconstitution after loss of the original transfer payload, not byte-identity claims).
All are pending T26 ratification — the admission is canonical census standing, not
manuscript-final prose.

Evidence chain, each verified 2026-09-21:

1. **T25 census membership.** `working/pre-manuscript-refinement-2026-09-10/T25-current-census-acceptance.json`
   (the frozen 288-record acceptance) admits `S` and `S0`–`S5` under register `episteme`
   with their canonical homes and sha256 values; all seven were re-hashed against the
   actual bytes at Antykathera-Essay-Work `origin/main` `7d96ada2` and match exactly.
2. **E0 coverage.** `production/return-of-zero/episteme/roz-s-products.journey.json`
   (Point-Cloud-Demo) covers the S register as the `roz-s-products` journey, 7 scenes.
3. **Native collection membership.** O-I commit `0b18c11b` (PR #452) committed
   `desktop/cradle/expressions-app/collections/return-of-zero/episteme/roz-s-products.journey.json`
   + cover as native collection members. (Note: the owner's convergence checkout is on a
   different line, so the file is not on that working disk — it is in the committed tree,
   verified via git objects.)
4. **Canonical product field.** O-I `docs/CANONICAL-PRODUCT-FIELD.md` (on `origin/main`)
   names the six products; the S records' product offices (Central S0, Actuation S1,
   AIKit S2, Software Factory S3, Workcell S4, Quaternal Logic S5) match it.

### What the census-basis receipts actually are

The `P1-census-{central,actuation,aikit,factory,workcell,quaternal-logic}.json` receipts
(61/157/104/230/30/148 records) are **candidate material inventories** — hash-verified
lists of a product's committed authored-prose surface that the corpus can be produced
*from*. What they lacked was not an admission for their corpus; it was their **provenance
connection to the S coordinates**: which admitted product office the material belongs
under, and which of the product's own records express that office's named task. That
connection is now made: see section 8 and the `S0`–`S5` production receipts named there.

### Restated production plan: seeded from S0–S5

Each product corpus is **seeded from its S record**. The S record names the product's
office, its paired lenses, its argument/concept relations and its local A/C constitution;
the product's material inventory binds *under* that coordinate. Wave 1 of that seeding
landed in Point-Cloud-Demo `production/s-products/` (branch `corpus/s-products-wave1-20260921`):
one whole-first journey per product, scene path = the S record's own #0 → #5→0 movement
structure, every scene binding its S record (path + sha256 at `7d96ada2`) plus one
public-identical record from the product's frozen inventory. Per-product receipts:
`working/expression-corpus/P1-S-products-wave1-2026-09-21.md`. Full corpus depth (the
whole inventory as scenes per product) remains the following fan-out — wave-1 is not
corpus-complete.

### What this correction does not change

- The receipts' hash work stands: every frozen record hash re-verified against git object
  bytes at the recorded commits (this correction re-verified all 36 wave-bound records the
  same way, plus public-identity against each repo's `origin/main` — 36/36 byte-identical;
  ai-kit `README.md` had drifted on main and was replaced in the wave selection by
  `docs/v2/01-PRODUCT-AND-OWNERSHIP.md`, which is public-identical).
- Section 3 (Epii wave-1), the Bimba verified-existing finding and the O:I
  complete-and-out-of-scope finding are unaffected.
- The caution that dirty working trees were never read or frozen stands; ownership and
  T26 ratification questions also stand — admitting corpus *content* is the S register's
  work; ratifying its *standing* remains the owner's.

## 8. Wave 1 of the S-seeded products corpus (2026-09-21)

Landed: Point-Cloud-Demo branch `corpus/s-products-wave1-20260921`, namespace
`production/s-products/` (README with root law, `s-products-corpus-base` + six per-product
family profiles, six bindings, six journeys, six real-engine covers). Six artifacts,
36 scenes, 36 material records bound (+7 S-register records bound in every scene of their
journey). Gates executed per artifact: `validate.mjs` VALID, `importDocuments` via
`scripts/production-inventory.ts` (4 namespaces, disjoint), covers via `capture.mjs`
(real renderer, SwiftShader, first-scene path — shared capture defect #2 stands unpatched).
Full detail, gate transcripts and per-product remainder estimates:
`P1-S-products-wave1-2026-09-21.md`.
