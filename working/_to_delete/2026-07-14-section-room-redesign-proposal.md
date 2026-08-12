---
title: "Section-Room Redesign Proposal"
status: implemented-builder-side
date: "2026-07-14"
tags:
  - epi-logos/antikythera-essay
  - planning-v3/room-redesign
---

# Section-Room Redesign Proposal — 2026-07-14

> [!important] Status — approved by Frank and implemented (builder side) 2026-07-14
> Builder items 1–5 are live in `build-section-rooms.py` v1.4.0: full movement content with display math flows into the contexts (room 03 carries both locked expressions, room 04 the torus quotient); the dossier embed, duplicate arc, and duplicate debt ledgers are gone (every line appears once; contexts run 221–315 lines, the long ones from real derivations, not repetition); 20-/30- surfaces are on-demand via `--seed-surface` and the 14 pure-template files were verified and deleted (room 00's deepened pair kept); `--check` now gates invented room slugs and the locked expressions; the seed-placeholder leak is fixed for future seeds. The Sol-skill items (6–8, including the hard-gated **Teaching** axis) are **deferred**: Frank is redoing the Sol skill; a review pass on the new skill will apply them when he prompts for it. The standing decisions below were all ruled on 2026-07-14: `−/−` adjudicated into the plan; theorem content ported into notes 25/26; the live layer fully unhooked from the deprecated reference-notes (nine concepts promoted to live nodes, three alias-absorptions, 174 links rewired, Concept Map rerouted, zero legacy-resolving links on final scan).

## The diagnosis in one paragraph

The room layer fails not because a model was careless but because the tooling specifies the failure. The builder truncates every movement claim at the first plain paragraph — amputating display math, so the two-logics room never shows `(+1)/(−1)` or `(0/1)/(1/0)`, the room's entire subject — then embeds the Sol dossier verbatim into the generated context and repeats the movement arc and the debt ledger again, so a deepened room states each movement two to three times at increasing dilution (~120 of room 00's 351 context lines are duplicates). The Sol skill mandates an eight-field metadata lattice per movement and a dossier made of claim/warrant/counterpressure/evidence-function/typed-relation slots, and its depth rubric scores eight axes — wager, braid, typed relations, evidence functions, proof ceilings, visual admittance — **none of which is "a reader of this file now understands the texts and concepts."** One axis actively rewards visible debts. A model optimising against that rubric produces exactly what room 00 contains: maximal status-bureaucracy, minimal teaching, hedges sitting where philosophy should be. Nothing validates cross-room references, so five invented slugs shipped in one pass. Meanwhile seven of eight rooms carry speculative scholarly/plate scaffolds for drafts that do not exist.

## The design principle

A room is a **teaching surface**. Its acceptance test: *after reading the room, Frank has working understanding of the station's texts, concepts, and argument — what each says, what work it does here, why this movement — and knows in one glance what remains owed.* Status discipline marks the audit boundary once; it never rations content (orienting principles, lock 4). Everything that is machine-coordination rather than understanding (source tables, quote states, debt matrices) lives in `.section-room.json` or one collapsed appendix, not in the reading flow.

## Proposed room shape — five files become three roles

| File | Role | Change |
|---|---|---|
| `00-SECTION-CONTEXT.md` | Generated, lean orientation | **One pass** of the six movements — each carrying the canonical node's full Claim/Warrant/Tension/Transition *including display math*, plus a single status+source line. Living centre and arrival/release kept. Doorway kept. Dossier embed, duplicate arc, and open-support ledger removed (debts collapse to one linked appendix block). Target: ≤160 lines. |
| `05-ROOM-DOSSIER.md` | Protected Sol synthesis, **re-specced as teaching brief** | First duty: teach. Per movement, the named texts and concepts at working depth, with the plan's own station prose as the explicit floor ("if your output holds less philosophy than the plan's prose for that station, it is not done"). The station wager/braid through-line — the one part of the current format worth keeping — stays. Hedges collapse to one audit-boundary block. Typed continuity only where it earns its place, slugs validated. |
| `10-FRANK-DRAFT.md` | Sovereign | Unchanged. |
| `20-SCHOLARLY-EDITION.md`, `30-PLATE-AND-DIAGRAMS.md` | Deferred | **Not seeded.** Created on demand once a draft exists in that room (for 7 of 8 rooms they are currently speculation ahead of any prose — created once, never updated, guaranteed drift). When built, keep room 00's paragraph-burden/proof-boundary pattern, attached to taught content. **[F-decide]** |

## Tooling changes

**`tools/build-section-rooms.py`:**
1. Carry whole Claim/Warrant/Tension/Transition sections with display math and tables; delete the first-paragraph truncation (`normalise_prose`) and the `contextual_claim()` apology sentence ("*The displayed formal derivation continues…*").
2. Drop the verbatim dossier embed and the duplicated six-movement arc + open-support ledger; link the dossier instead.
3. Stop seeding `20-`/`30-` surfaces; create on demand.
4. Extend `--check`: scan all protected surfaces for room-slug-shaped references and fail on anything outside the eight canonical slugs; verify any §↔room pairing stated in prose; verify the station's locked expressions appear where the plan's station carries them (e.g. room 03 must contain `(+1)/(−1)` and `(0/1)/(1/0)`).
5. Fix the seeded-dossier placeholder leak: instructions-to-Sol ("Sol must recover…") come from the builder's parse-whitelist misses and currently ship as Frank-facing content; widen the whitelist or render misses as a single "not yet parsed" line.

**`agent-skills/sol-section-room-deepening/SKILL.md` + depth rubric:**
6. Mandatory pre-load: `return-of-zero-orienting-principles.md`; the coverage table must reproduce §V's station↔room map; references that cannot be verified on disk do not ship (rule 4).
7. Re-spec the dossier's §3 duties: teaching first (texts and concepts at working depth, plan prose as floor, every imported term taught in place per the writing rubric), lattice second and compressed — one status marking per movement, not distributed hedges (rules 1–3).
8. Add a ninth depth-rubric axis, **Teaching**, scored 0–3 and hard-gated at 2: "a reader with no other file open gains working understanding of this station's texts and concepts." Rebalance axis 4 so visible debts stop outscoring resolved understanding.

## Migration order

1. Patch the builder (items 1–5); regenerate all eight contexts; run `--check`.
2. Re-spec the Sol skill (items 6–8).
3. Re-run the deepening on room 00 under the new spec; validate against the 2026-07-14 audit findings (the room must now carry the Trika presage, the paradox-hinge material, Gebser's atmosphere, the immutable gap, and zero invented references).
4. Only then deepen the remaining rooms in the plan's dependency order (§0/1 → §0 → §1 → §2 → §3 → §4 → §5 → §5→0).

## Standing decisions surfaced by the audit **[F-decide]**

- **Frozen-layer routing:** ~15 of the 24 §3–§5→0 notes (and several §0/1–§2 notes) route body warrants through `reference-notes/` files stamped `deprecated-legacy` (Laws of Form, re-entry, iterants, psychoid number, apoha, MEF, 36 Tattvas, Prompt Thrownness…). Either these terms get live concept/argument homes (the concepts/ layer is the natural landing) or the links stay and the deprecation is softened to "frozen provenance, still linkable for understanding." One rule, applied everywhere.
- **Notation adjudication:** the plan's §3 · #0 table writes the unmarked field as `−−`; the theorem spine §II(c) writes `−/−` ("two present marks held in one expression"). Canon-level inconsistency; the notes inherit whichever is chosen.
- **Theorem ports:** notes 25 (eight determinations) and 26 (Spanda 4+2) are designated "full derivation" homes but carry materially less than theorems §II(c)/§I (invariant column, Being/Becoming/Knowing-unKnowing grammar, Essence/Constitution/Text-Texture folds; 3:3 bimba/pratibimba table, standing identity, Whiteheadian lure, tetraktys carrier). Port the missing content, or repoint the plan's delegation to the theorem file.
- **Gaps-reversal placement:** the humanity/God-of-the-gaps error lands at note 16 (§1 · #3) while the plan carries it in governing intent with §1 · #4 taking the mathematical form — check against `01-immutable-gap-and-meta-sign` so it doesn't land twice.
- **Small wiring:** note 47 cites only Berkeley (named triad is Schopenhauer/Kastrup/Śaivism — records may need intake); note 19 carries an unused Śrīharṣa source id; `concepts/index.md` `[[deferential-intelligence]]` and `[[vak]]` link forms need `okf-scan.py --dangling` confirmation; note 20's `[[Dia-ballein]]` resolves into the frozen layer against the Title-Case concept policy.
