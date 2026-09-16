# Expression Corpus Production Map

**Owner:** issue #65  
**Standing:** submission production map, revised 16 September 2026.  
**Source authority:** current canonical authored world under `submission-package/essay/`, T17 census/build discipline, T25/T26 source revisions.  
**Material atelier:** `EpiLogos/Point-Cloud-Demo` #6 / `AGENT_EXPRESSION_ATELIER_PROTOCOL.md`.  
**Cross-product seam:** O:I #306/#335/#352 + QL-MEF #201/PR #202.

This map does not define another essay ontology or Expression API. It routes the already-ratified authored world into the **actual running Expressions instrument**, where Agents craft, inspect, perform, criticise and admit the resulting artifacts through the real O:I/Ta-Onta system.

A source-bound scene specification may seed work. It is not the finished Expression. Production is complete only after the work has been made and encountered through the actual Point-Cloud-Demo editor/engine.

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

## 2. Producer packet — source ground, not a pre-authored artwork

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
  prior Expression/artifact refs[]
  prior admitted form/asset occurrences[]
  sequence_predecessor/successor refs[]
  branch_transition_refs[]

  native source/page/portal refs[]
  canonical Action refs[]

  atelier_session_ref?
  output_expression_ref?
  build_receipt_ref?
}
```

The packet says **what must remain answerable**. It does not pre-decide every glyph, image, colour, formation, pin, camera gesture, physics relation or scene transition. Those determinations are made and tested in the live Atelier.

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
→ scene override / live Atelier iteration
```

The corpus profile carries continuity parameters: typography, framing/camera, baseline field/material state, particle/form scale, resource budgets, transition rhythm, motion/damping, reading HUD/aperture defaults, portal treatment and fallback policy.

Register/family profiles only override what genuinely differs. M branch colour/material differentiation is carried at the appropriate M-family/branch profile. Source-backed colour correspondence and navigational/associative colour coding retain different standing.

Profile defaults are **starting relations**, not a substitute for live composition. Aletheia may later propose profile changes from repeated successful/failed use.

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

The live Atelier is therefore not detached from the graph. It is the material inhabitation of the same bounded relation state.

---

## 5. Scene bodies / source Return

Scenes may use the generic O:I scene carriers as they land:

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

These are carriers **inside the Atelier act**. They do not replace the live field as the place where the full Expression is composed.

---

## 6. One live Atelier service enables the fan-out

Point-Cloud-Demo #6 owns the enabling cut:

```text
one running Expressions application
    + structured local authoring service
    + actual editor/engine capability registry
    + revision-safe AtelierSessionRefs
    + repo-backed artifact Library
```

The structured service must operate the same Expression/Scene/Entity model and native engine used by the human UI. No corpus-only headless composer or second scene schema is accepted.

Parallel content workers may share the host through distinct Atelier sessions. A session maps to a real editor/engine instance or explicitly suspended working copy. Mutations remain serialized/revision-gated so subagents cannot invisibly race-write one Expression.

This service is also the live TA0–TA7 proving ground: Khora enters the target, Hen discloses the form horizon, Pleroma discloses the real editor powers, Chronos binds the exact iteration, Anima makes, and Aletheia returns actuality.

---

## 7. Production lanes

All content lanes follow the **same full Atelier loop**. There is no independent visual-procurement lane before production.

| lane | source cut | material production |
|---|---|---|
| **E0 integration** | current census + Atelier/O:I/TA contracts | packet compiler, shared profiles, Atelier/session binding, generated coverage inventory, shared conflicts |
| **E1 essay/rooms** | essay + `section-rooms/` | whole reading sequence + addressable room states crafted in Atelier |
| **E2 A** | current A records | A-family Expression/sequence with one addressable scene/state per current A record |
| **E3 A′** | current A′ records | repeated A′ family Expression through same live process |
| **E4 C** | current C records | repeated C family Expression through same live process |
| **E5 A/C** | current A/C records | repeated A/C family Expression through same live process |
| **E6 S** | current S records | complete S-family Expression through same live process |
| **E7 Concepts/Episteme** | canonical concepts + repeated Episteme record forms | concept field + typed repeated-family Expressions |
| **E8 Matheme** | canonical Matheme tree | formal/diagrammatic Expressions and sequences |
| **E9 Symbolon** | root/spine/heads + root register carriers | Symbolon register Expression and root traversals |
| **E10 Mytheme** | Whole Mythemes + derivatives | complete sequenced Expression per Whole where required; occurrence-linked derivatives |
| **E11 remainder census** | all canonical records not already owned | explicit live-Expression or declared non-Expression disposition so coverage remains bijective |

E0 owns shared schema/profile/integration conflicts. Content workers never fork `oi.expression/v1`, Ta-Onta, graph identity or the Point-Cloud authoring model.

### Every content lane performs this movement

```text
source packet
→ Khora/Hen/Pleroma/Chronos entry
→ AtelierSession
→ Anima composition/material/temporal work
→ content-local form/asset discovery as needed
→ actual playback/capture/inspection
→ Aletheia witness + critique
→ Anima revision
→ Aletheia curation into repo Library
→ Aletheia praxis candidate where something reusable was learned
```

A single capable Agent may embody several offices in sequence. Complex targets may use subagents. Office identity remains in receipts so the programme can learn which relational office produced which change.

---

## 8. Mytheme special rule

The primary Mytheme carrier is the recovered **whole**.

A Whole Expression must preserve the story/work far enough that every active relation/transformation remains available and the ending/aftermath can qualify the beginning. This may require many scenes and authored sequencing.

Do not flatten Whole Mythemes to a single illustration.

Story-internal figures/objects/animals/plants/elements/places/actions/motifs, cross-story indexes and higher archetypal constellations retain reverse links to exact whole-story occurrences. Interpretive relations preserve `human-amplified: yes/no`.

The actual need for images, glyphs, ASCII, diagrams or formed motifs emerges while the Whole is being composed. Their recurrence is indexed after use; it is not predeclared as a symbolic dictionary.

---

## 9. Content-arising visual forms and the local bank

The earlier separate asset-procurement lane is superseded.

Each lane discovers/creates/adapts what the actual Expression needs:

```text
content relation
→ concrete expressive need
→ glyph | SVG | ASCII | image | diagram | texture | generated form
→ source/rights/provenance check
→ test in the real Point-Cloud composition
→ accept | reject | retain as variant
→ Aletheia curator records admitted occurrence
```

No worker silently downloads or embeds an untracked image merely to finish a scene.

Admitted forms accumulate in the Point-Cloud repo and can then be resolved by Hen for later work. The useful lookup becomes empirical:

```text
subject / motif / figure
→ forms actually used
→ scenes where each form appeared
→ source / rights / standing
→ observed success / failure notes where present
```

This makes the visual bank a residue of the developing artistic practice rather than an abstract catalogue designed in advance.

---

## 10. Anima / Aletheia team protocol

The detailed live-team law is owned by Point-Cloud-Demo #6 and QL-MEF's `TA-ONTA-ANIMA-ALETHEIA-EXPRESSION-ATELIER.md`.

Minimum offices:

```text
ANIMA
  composition   whole / scene / hierarchy / quiet / sequence
  material      field / glyph / image / ASCII / physics / colour
  temporal      timing / camera / automation / performance
  integration   source/graph/profile/corpus coherence + mutation integration

ALETHEIA
  witness       what actually happened
  critic        fidelity / legibility / force / pacing / coherence
  curator       artifact / occurrence / provenance / variant admission
  praxis        reusable practice candidate + counterexamples
```

These offices are intentionally refinable across the programme. Stable IDs may remain while human-readable role boundaries change in response to evidence.

---

## 11. Artistic-learning Return

Corpus production is also the data source for the future **Anima Expression Skill**.

Meaningful iterations retain enough relation to compare:

```text
source/content burden
Anima office + operations
engine/profile generation
parameter / form / colour / sequence changes
observed material result
Aletheia critique
human response when available
accepted / rejected / variant / unresolved
scope and counterexamples
```

Colour observations retain why the colour is present:

```text
source-backed correspondence
M/register navigation
subject/figure association
affective choice
material/legibility
experimental association
```

Repeated use may become an authored or pedagogical convention. It does not become semantic truth through frequency.

Aletheia may return an `ExpressionPracticeCandidate`; promotion follows existing T/T′ / recognised `= name` / Skill/Method laws:

```text
practice candidate
→ examples + counterexamples + applicability
→ reuse on later target
→ works | fails | narrower-than-thought | revised
→ human/native Recognition
→ named Method / Anima Skill refinement
```

Do not freeze the first corpus wave into one giant style prompt.

---

## 12. Four passes

### P0 — Atelier enablement and pilot

Land the smallest Point-Cloud Agent Atelier service + repo Library seam, then run one real pilot target through Khora→Hen→Pleroma→Chronos→Anima→Aletheia.

The pilot exists to prove the production protocol, not to establish one privileged visual style.

### P1 — parallel live corpus production

Fan out E1–E11 through distinct Atelier sessions. Each worker produces **actual editable Expressions**, not merely specs/manifests.

Family-level workers may reuse successful profile/Method candidates, but must return failures and exceptions rather than force conformity.

### P2 — source reconciliation

After T25/T26 or other accepted source changes:

```text
new census
→ diff record/relation/reading revisions
→ invalidate affected packets/artifacts
→ reopen affected Atelier sessions
→ revise through live medium
→ retain still-valid authored variants
→ report retired/orphan bindings
```

### P3 — whole-corpus alignment and praxis review

Run one final creative/technical/Aletheia pass over the accumulated works:

- shared profiles genuinely inherited rather than copied;
- register/family forms coherent without flattening difference;
- M colour/material differentiation useful and correctly typed;
- typography/camera/motion/transition rhythm continuous where intended;
- formation/pin/entity/physics vocabulary used where it clarifies the object;
- quiet scenes remain deliberately quiet;
- Mytheme wholes remain whole;
- canonical pop-outs and Return work;
- form/asset occurrence and provenance queries work;
- graph ↔ Expression focus is one state field;
- useful artistic practices have examples **and counterexamples**;
- final Anima Skill/Method candidates name their scope and limits.

P3 may alter presentation/profile variants. Semantic source changes return to their native authoring path.

---

## 13. Generated inventory

E0 maintains a generated inventory, not a second semantic census:

```text
source identity + revision
register/type/home
Expression + revision
Point-Cloud editor/engine revision
profile lineage
AtelierSession / accepted build receipt
scenes / sequences / branches
bounded-whole + canonical relation refs
portal / Action refs
used form/asset refs + occurrence status
Anima/Aletheia receipts
source-alignment status
continuity-review status
runtime-proof status
praxis-candidate refs
```

Completeness checks compare this inventory to the canonical authored-world census at the named source revision.

---

## 14. Gate

Issue #65 closes only when the canonical submission source revision has complete live Expression coverage (apart from explicitly declared non-Expression carriers), the four registers and all section/argument/concept/S surfaces are present, Whole Mythemes remain narratively adequate, content-arising forms are attributable and occurrence-indexed, graph/Expression navigation is truly shared, canonical source pop-outs round-trip, corpus-wide profile continuity has been reviewed, Ta-Onta's Anima/Aletheia practice has been exercised under real creative load, and lived acceptance has been recorded at its real evidence standing.

This gate joins—but does not replace—the O:I product acceptance and environmental/material stress-test gates.