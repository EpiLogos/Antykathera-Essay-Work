# Expression Corpus Production Map

**Owner:** issue #65  
**Standing:** submission production map, 16 September 2026.  
**Source authority:** current canonical authored world under `submission-package/essay/`, T17 census/build discipline, T25/T26 source revisions.  
**Cross-product seam:** O:I #306/#335/#352 + QL-MEF #201/PR #202.

This map does not define another essay ontology or Expression API. It converts the already-ratified authored world into source-bound Expression specifications/artifacts through the real O:I/Ta-Onta contracts.

---

## 1. Fixed target

The queue is generated from the current canonical authored-world census at a named Git revision. Its standing target includes:

```text
THE-RETURN-OF-ZERO.md / reading path
section-rooms/

symbolon/                    # Symbolon register
symbolon/matheme/            # Matheme register
symbolon/mytheme/            # Mytheme register
symbolon/episteme/           # Episteme register

A / A′ / C / A/C / S records
concept records
all other canonical page/carrier records admitted by the register census
```

Current T25 standing retains 144 A/A′/C/A/C/S records, but no worker hard-codes that count as source authority.

The four registers are **Symbolon · Matheme · Mytheme · Episteme**. Symbolon is the whole register/root relation, not a wrapper to be omitted from a three-register build.

---

## 2. Producer packet

Every worker receives one bounded packet, never the whole repository context by default.

```text
ExpressionBuildPacket {
  source_revision
  source_ref / canonical record_id
  canonical_home
  register
  record_type
  section / movement / argument refs where present
  exact source + claim + human-amplification standing

  incoming_relation_refs[]
  outgoing_relation_refs[]
  return_relation_refs[]
  bounded_local_whole

  profile_basis
  family_or_branch
  scene_role
  sequence_predecessor/successor refs[]
  branch_transition_refs[]

  native_carrier_refs[]
  portal/native Action refs[]
  required_visual_assets[]
  available_visual_assets[]

  output_expression_ref?
  build_receipt_ref?
}
```

Canonical declared relations enter as canonical. Agent-discovered local/proximate relations are emitted separately as proposals with evidence/standing; they never become graph truth merely because they are useful for composition.

---

## 3. Shared expression grammar

All lanes consume the same inheritance chain:

```text
O:I global
→ Epi global
→ Return-of-Zero corpus
→ register / M-family
→ repeated family / branch
→ record authored variant
→ scene override
```

The corpus profile carries continuity parameters: typography, framing/camera, baseline field/material state, particle/form scale, resource budgets, transition rhythm, motion/damping, reading HUD/aperture defaults, portal treatment and fallback policy.

Register/family profiles only override what genuinely differs. M branch colour/material differentiation is carried at the appropriate M-family/branch profile. Source-backed colour correspondence and navigational colour coding retain different standing.

---

## 4. Graph / Expression invariant

Every record is projected from the same declared relation field already used by the Wiki/minigraph:

```text
canonical current record
      ↓
bounded declared neighbourhood
      ↓
Expression entities / relation presentation / formations
```

Changing graph location changes the current Expression state. Focusing an Expression entity/relation updates the same canonical selected ref used by graph/page/Nara.

Constellation/harmonic layout may organise those exact refs where QL structural grammar legitimately applies. It does not create new semantic edges from visual placement.

---

## 5. Scene bodies / source Return

Scenes may use the generic O:I #352 scene carriers:

```text
live engine composition
Markdown/file/span
glyph / SVG / ASCII
image / media / diagram
generic file Thing
Wiki bounded local whole
authored HTML / WorldPresentation / native Surface
another Expression / Edition under recursion limits
```

A canonical source/page/file may be opened from a scene through a declarative portal/native Action trigger and must return/re-dock to the same Expression/scene/selection.

Unsupported file formats degrade to their real native Thing/open path rather than acquiring a fake renderer.

---

## 6. Production lanes

All lanes may start specification/procurement as soon as this map lands. Shared schema/profile edits are serialised through the integration lane.

| lane | source cut | output |
|---|---|---|
| **E0 integration** | current census + O:I/TA contracts | packet compiler, shared profiles, inventory, schema reconciliation |
| **E1 essay/rooms** | essay + `section-rooms/` | whole reading sequence + addressable section-room states |
| **E2 A** | current A records | one A-family grammar/Expression sequence; one addressable scene per current A record |
| **E3 A′** | current A′ records | repeated A′ family expression/specs |
| **E4 C** | current C records | repeated C family expression/specs |
| **E5 A/C** | current A/C records | repeated A/C family expression/specs |
| **E6 S** | current S records | complete S-family expression/specs |
| **E7 Concepts/Episteme** | canonical concepts + repeated Episteme record forms | concept field + typed repeated-family specs |
| **E8 Matheme** | canonical Matheme tree | formal/diagrammatic profile bindings and sequences |
| **E9 Symbolon** | root/spine/heads + root register carriers | Symbolon register Expression and root traversals |
| **E10 Mytheme** | Whole Mythemes + derivatives | one complete sequenced Expression per Whole where required; occurrence-linked derivatives |
| **E11 remainder census** | all canonical records not already owned | explicit disposition so queue remains bijective |
| **E12 visual assets** | asset-needs manifests from all lanes | sourced/rights-accounted glyph/image/ASCII/diagram/form bank + occurrence index |
| **E13 templates** | recurring page/scene forms | HTML/WorldPresentation templates and generic scene compositions |

E0 owns shared conflicts. Content workers never fork `oi.expression/v1`, Ta-Onta, graph identity or the visual-asset registry.

---

## 7. Mytheme special rule

The primary Mytheme carrier is the recovered **whole**.

A Whole Expression must preserve the story/work far enough that every active relation/transformation remains available and the ending/aftermath can qualify the beginning. This may require many scenes and authored sequencing.

Do not flatten Whole Mythemes to a single illustration.

Story-internal figures/objects/animals/plants/elements/places/actions/motifs, cross-story indexes and higher archetypal constellations retain reverse links to exact whole-story occurrences. Interpretive relations preserve `human-amplified: yes/no`.

The visual occurrence bank helps show where a Being/Thing/motif recurs across Whole Expressions without turning that recurrence into a fixed symbolic definition.

---

## 8. Asset procurement protocol

Each E1–E11 worker emits:

```text
asset_need {
  subject_ref
  scene_ref / intended role
  desired kind: glyph | svg | ascii | image | diagram | texture | generated-form | other
  source candidate refs[]
  required rights/provenance status
  required fallback
  priority: required | useful | optional
}
```

E12 deduplicates against the O:I asset index, procures missing items, records provenance/rights, creates or admits generated forms with generated standing, and writes occurrence links back to every using scene.

No worker silently downloads or embeds an untracked image merely to finish a scene.

---

## 9. Four passes

### P0 — specification now

Compile census and run E1–E13 in parallel. Output source-bound Expression specs, scene plans and asset manifests even where runtime APIs are not yet fully executable.

### P1 — live compilation

When O:I #352 and QL-MEF #201/TA0–TA2 expose the needed real seams, E0 compiles the prepared specifications through `oi.expression/v1` + Ta-Onta into live/revisioned Expressions and portable Editions where required.

No permanent shadow scene schema is introduced.

### P2 — source reconciliation

After T25/T26 or other accepted source changes:

```text
new census
→ diff record/relation/reading revisions
→ invalidate affected packets
→ rebuild affected Expressions/assets
→ retain still-valid authored variants
→ report retired/orphan bindings
```

### P3 — whole-corpus alignment

Run one final creative/technical pass over the corpus:

- shared profiles genuinely inherited;
- register/family forms coherent;
- M colour/material differentiation legible;
- typography/camera/motion/transition rhythm continuous;
- formation/pin/entity/physics vocabulary fully leveraged where it serves the subject;
- quiet scenes remain deliberately quiet;
- Mytheme wholes remain whole;
- canonical pop-outs and Return work;
- asset occurrence and provenance queries work;
- graph ↔ Expression focus is one state field;
- exceptional local choices are explicit profile variants, not accidental drift.

P3 may alter presentation only. Semantic source changes return to their native authoring path.

---

## 10. Generated inventory

E0 maintains a generated inventory, not a second semantic census:

```text
source identity + revision
register/type/home
Expression + revision
profile lineage
scenes / sequences / branches
bounded-whole + canonical relation refs
portal / Action refs
asset refs / missing status
packet / worker / build receipt
source-alignment status
continuity-review status
runtime-proof status
```

Completeness checks compare this inventory to the canonical authored-world census at the named source revision.

---

## 11. Gate

Issue #65 closes only when the canonical submission source revision has complete Expression coverage (apart from explicitly declared non-Expression carriers), the four registers and all section/argument/concept/S surfaces are present, Whole Mythemes remain narratively adequate, assets are attributable and occurrence-indexed, graph/Expression navigation is truly shared, canonical source pop-outs round-trip, corpus-wide profile continuity has been reviewed, and lived acceptance has been recorded at its real evidence standing.

This gate joins—but does not replace—the O:I product acceptance and environmental/material stress-test gates.