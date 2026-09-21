# P1 — S-seeded products corpus, wave 1: production receipts

**Date:** 2026-09-21 · **Owner:** issue #65 (EpiLogos/O-I), corpus-production obligation
**Follows:** the correction in `P1-PRODUCTS-CORPUS-PARENT-2026-09-21.md` §7 (the S register
recognised as the products' authored admission) · **Scope:** wave-1 seeding only — one
whole-first artifact per product, six material records bound per product. **This is not
corpus-complete;** the full-depth fan-out is estimated per product below.

**Landed:** Point-Cloud-Demo branch `corpus/s-products-wave1-20260921`, namespace
`production/s-products/` (namespace README with root law; `s-products-corpus-base` profile +
six family profiles; six binding records; six `oi.journey` v1 artifacts, 36 scenes; six
real-engine covers). One namespace-table row added to `production/README.md`. No shared
tooling modified; `production/return-of-zero/`, `production/epii-antichrist/` and
`production/bimba/` untouched.

## How the wave was seeded

For each product: the S record's own movement path (`#0 → #5→0`, read from the authored
bytes at Antykathera-Essay-Work `origin/main` `7d96ada2`) is the journey's whole — six
scenes in the record's order. Each scene binds (a) the S record by its exact movement
heading + sha256 (heading presence asserted against the bound bytes at generation time)
and (b) one material record from the product's frozen `P1-census-*.json` inventory,
chosen by the movement's named task (constitution ground, lens law, local A/C
constitution, relation, realised return). Scene texts compress and quote; product
cross-relations live in the S records' own argument/concept relations, not manufactured
graph edges. Product tints/grounds/term-rows are declared craft
(`s-products-corpus-base.profile.json`).

## Verification executed before generation

- All 36 bound material records re-hashed from **git object storage** at each receipt's
  frozen commit (product repos read-only; dirty trees never read) — 36/36 match the frozen
  receipt hashes.
- **Privacy check:** all 36 compared byte-wise against each repo's `origin/main` at fetch
  time — 36/36 byte-identical to the published remote. One candidate, ai-kit `README.md`,
  had drifted on `origin/main` (frozen `c5404b5ecdc6` vs main `3092263f3143`) and was
  **replaced in selection** by `docs/v2/01-PRODUCT-AND-OWNERSHIP.md` (public-identical)
  rather than bound. No unpublished bytes were consumed.
- All seven S-register records (S, S0–S5) re-hashed at `7d96ada2` — match the T25 census
  acceptance exactly; the generator re-asserts the pinned hashes at run time.

## Per-product receipts

### S0 Central — meaningful continuity (movement 37; L0 Quaternal / L5′ Divine Logos)

- **S record bound:** `S0-Central.md` (sha256 `8cfac85f…`), all 6 scenes, heading-anchored.
- **Artifact:** `central/sp-central.journey.json` (6 scenes) + cover + `bindings/sp-central.binding.json` + `profiles/family-central.profile.json`.
- **Material slice (6 of 61):** `README.md` (#0 front ground) · `docs/PRODUCT-GROUND-CONVENTION.md` (#1 ground sayable) · `docs/SOURCE-RETURN.md` (#2 disclosure/return) · `docs/PROJECTCENTRAL-AUTHORED-GROUND.md` (#3 authorship) · `docs/PERSONAL-WORLD-PROJECTION.md` (#4 Bimba/Pratibimba carried world) · `docs/RECOVERY-PROTOCOL.md` (#5→0 revisable continuity). Repo `EpiLogos/Central` @ `87341be4` (main), byte-identical to origin/main.
- **Remainder for full depth:** the other 55 records (docs surface + ctrl/defaults + skills) mapped to movements/admitted per record; est. **1–2 workers** (~2 journeys of ~32 scenes).

### S1 Actuation — living articulation (movement 38; L1 Causal / L4′ Scientific)

- **S record bound:** `S1-Actuation.md` (sha256 `ef4e2b59…`), all 6 scenes, heading-anchored.
- **Artifact:** `actuation/sp-actuation.journey.json` (6 scenes) + cover + binding + family profile.
- **Material slice (6 of 157):** `docs/ACTUATION-CONSTITUTION.md` (#0) · `docs/ACTUATION-STREAM.md` (#1 stream) · `docs/EPISTEMIC-CULTIVATION-AND-MODEL-INTERIOR-RESEARCH.md` (#2 act→knowledge) · `docs/MODEL-BEARING-AGENCY-RESEARCH-AND-MATERIALISATION.md` (#3 judgment world) · `docs/ACTUATION-RELATION.md` (#4 local constitution) · `docs/REALISED-ACTUATION-LOOP.md` (#5→0 returned judgment). Repo `EpiLogos/Actuation` @ `0ac23bf` (techne/deep-conjugate-allowance), byte-identical to origin/main. The repo carries a dirty in-flight research lane — untouched; only committed bytes consumed.
- **Remainder:** 151 records incl. the rust-refoundation and ql-runtime experiment surfaces (some experiment records may be owner-excluded — that disposition is open); est. **2–3 workers** (~5 journeys).

### S2 AIKit — potency (movement 39; L2 Logical / L3′ Chronological)

- **S record bound:** `S2-AIKit.md` (sha256 `2618122e…`), all 6 scenes, heading-anchored.
- **Artifact:** `aikit/sp-aikit.journey.json` (6 scenes) + cover + binding + family profile.
- **Material slice (6 of 104):** `docs/v2/01-PRODUCT-AND-OWNERSHIP.md` (#0; substituted for drifted `README.md`) · `docs/v2/15-MODEL-ROSTER-CAPABILITY-FIT.md` (#1 IS/IS-NOT) · `docs/adr/0003-user-baselines-and-skill-usage-overlays.md` (#2 temporal powers) · `docs/v2/02-RESOLUTION-AND-CONTEXT-COGNITION.md` (#3 possession ≠ disclosure) · `docs/v2/HARNESS-ADMISSION-AND-ADAPTER-SDK.md` (#4 entrusted power) · `docs/v2/21-PROJECT-REFLECTION-AND-LOCAL-ARTICULATION.md` (#5→0 horizon returns). Repo `EpiLogos/ai-kit` @ `23dea85` (techne/agency-mint); all six byte-identical to origin/main.
- **Remainder:** 98 records (docs/v2 corpus, ADRs, registry capsules); est. **2 workers** (~4 journeys).

### S3 Software Factory — transformation (movement 40; L3 Processual / L2′ Alchemical-Elemental)

- **S record bound:** `S3-Software-Factory.md` (sha256 `a0846487…`), all 6 scenes, heading-anchored.
- **Artifact:** `factory/sp-factory.journey.json` (6 scenes) + cover + binding + family profile.
- **Material slice (6 of 230):** `README.md` (#0) · `docs/canon/PRAXIS-PRIMITIVES.md` (#1 processual) · `docs/canon/QL-SOFTWARE-FACTORY-PRIMITIVE-RELATIONS.md` (#2 material grammar) · `docs/canon/RUN-CLOSURE-VERIFICATION-ALIGNMENT.md` (#3 gate/recognition) · `docs/canon/FACTORY-SELF-HOSTING-COMMISSION.md` (#4 labour/power) · `docs/canon/PROJECT-DEVELOPMENT-ORIENTATION-AND-RETURN.md` (#5→0 changed field). Repo `EpiLogos/Factory` @ `fbabaaa` (techne/telemetry-watch-compare-settings), byte-identical to origin/main; dirty lane untouched.
- **Remainder:** largest surface of the six — 224 records (canon, program, pstack, inkwell/sssf skill trees; the inkwell trees may deserve their own family split); est. **3–4 workers** (~8 journeys).

### S4 Workcell — situated existence (movement 41; L4 Phenomenological / L1′ Phenomenal)

- **S record bound:** `S4-Workcell.md` (sha256 `add7ce79…`), all 6 scenes, heading-anchored.
- **Artifact:** `workcell/sp-workcell.journey.json` (6 scenes) + cover + binding + family profile.
- **Material slice (6 of 30):** `README.md` (#0) · `docs/ARCHITECTURE.md` (#1 thrownness) · `docs/VISUAL-PRODUCT-UNDERSTANDING.md` (#2 aperture) · `docs/CANDIDATE-MATERIALISATION.md` (#3 demand/offer) · `docs/CROSS-CELL-CONNECTIONS.md` (#4 availability) · `docs/LIFECYCLE-RECONCILIATION.md` (#5→0 evidence returns). Repo `EpiLogos/Workcell` @ `5ddf156` (main), byte-identical to origin/main.
- **Remainder:** 24 records — the cheapest full-depth completion of the six; est. **1 worker** (1–2 journeys). Natural first pilot for the fan-out.

### S5 Quaternal Logic — Transcendent Relation (movement 42; L5 Para Vāk / L0′ Archetypal-Numerical)

- **S record bound:** `S5-Quaternal-Logic.md` (sha256 `36a4828c…`), all 6 scenes, heading-anchored.
- **Artifact:** `ql/sp-ql.journey.json` (6 scenes) + cover + binding + family profile.
- **Material slice (6 of 148):** `README.md` (#0) · `docs/QL-VAK-KERNEL-RECONCILIATION.md` (#1 Para Vāk) · `docs/KERNEL-RECURSIVE-M-REGISTRY.md` (#2 articulated whole) · `docs/HOLOGRAPHIC-KERNEL-FORMAL-REFERENCE.md` (#3 dia/syn) · `docs/QL-STRUCTURAL-CARRIER-CONTRACT-V1.md` (#4 formal constitution) · `docs/L5-TECHNE-INTEGRATED-DEVELOPMENT-WAYFINDER.md` (#5→0 co-internality). Repo `EpiLogos/Quaternal-Logic` @ `81d1af1` (session/k-aw-expression-production-2026-09-17), all six byte-identical to origin/main; the K/AW production lane is dirty and was untouched.
- **Remainder:** 142 records (kernel-rebuild, epi-logos integrations, geometry, fixtures); the Bimba product corpus remains the separate verified-existing lane (P1 map §2) — not duplicated here; est. **2–3 workers** (~5 journeys).

## Gates transcript (all executed 2026-09-21)

- **Generation (model API, validate + import in the loop):** `npx tsx /tmp/gen-s-products.mts` → six times `wrote production/s-products/<slug>/sp-<slug>.journey.json` + `import ok: "S-seeded products — S<0..5> <Product>" (6 scenes)`; the generator asserts each S record's pinned sha256 and each movement heading's presence in the bound bytes before staging.
- **Schema validator:** `node production/return-of-zero/tools/validate.mjs production/s-products/*/sp-*.journey.json` → `VALID … scenes=6 [s0-m0-ground,…]` (×6, scene ids listed per artifact) · `all artifacts valid`.
- **Cross-namespace import floor:** `npx tsx scripts/production-inventory.ts` → `production inventory OK: 4 namespace(s), every journey file imports, namespaces disjoint` (s-products/ joined bimba, return-of-zero, epii-antichrist).
- **Real-engine covers:** `node production/return-of-zero/tools/capture.mjs production/s-products/*/sp-*.journey.json` (SwiftShader) → `CAPTURED …` ×6, each visually inspected: term row + ground disc + bound-record glyph in the product tint, margin page carrying kicker, movement name, exact S-record heading, compression and bound-material identity. One restaging was done after first capture (term-glyph boxes collided; width now respects row spacing) and all six covers recaptured. Shared defect #2 stands: covers are first-scene renders (per-scene navigation unreliable, unpatched); the chrome dot bottom-left is catalogued defect #10.
- **Privacy:** 36/36 bound records byte-identical to each product repo's published `origin/main` (ai-kit README drift found and substituted before binding).

## What is verified vs not

- **Verified by execution:** the gates above; deterministic generation (fixed ids/stamps).
- **Verified by read-only inspection:** all repo revisions and hashes; no dirty tree touched, no branch switched in any product repo.
- **Not verified / not claimed:** mid-scene visuals (shared capture defect #2); corpus-completeness (wave-1 = 36 of 730 inventoried records bound); any owner admission beyond the S register's own census standing; T26 ratification of the S records (pending, owner).

## Full-depth fan-out (estimate)

~11–15 worker-passes total (Central 1–2, Actuation 2–3, AIKit 2, Factory 3–4, Workcell 1, QL 2–3), plus one open owner disposition per product: whether experiment/fixture-class records (Actuation ql-runtime runs, Factory inkwell trees, QL fixtures) are corpus members or excluded surface. Workcell first (cheapest), Factory last (largest, needs the family split decision).
