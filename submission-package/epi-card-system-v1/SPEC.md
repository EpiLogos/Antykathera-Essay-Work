# Epi-Card QL Conjugate System

## Complete Product and Build Specification

**Version:** 1.0.0  
**Status:** normative implementation specification  
**Product name:** Epi-Card  
**Runtime name:** Epi-Card Runtime  
**CLI name:** `epicard`  
**Portable package extension:** `.epicard`  
**Canonical production store:** PostgreSQL 18 or later  
**Portable store:** SQLite plus content-addressed files  
**Knowledge-artifact export:** Open Knowledge Format v0.2  
**Canonical QL frame:** full `6 + 6′` Bimba–Pratibimba conjugate traversal

---

## 0. Normative language, design authority, and document use

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are normative. A conforming build satisfies every MUST and MUST NOT. SHOULD identifies the reference behaviour; departure requires an explicit implementation note and a passing equivalent acceptance test. MAY identifies a supported extension point.

This specification separates four kinds of statement so that implementation choices do not enter silently:

| Class | Meaning |
|---|---|
| **Product requirement** | A property directly required by the intended Epi-Card experience and QL architecture. |
| **Fixed v1 implementation** | A concrete implementation selected for the first complete build. It may change only through a versioned design decision. |
| **Configurable profile** | A parameter or correspondence that the system exposes as named, versioned configuration rather than hard-coding as universal. |
| **Explicitly excluded v1 integration** | A known adjacent system that is not part of this product version and is not to be inferred into the build. |

The specification is intended to be sufficient for a product, design, frontend, backend, agent, media, audio, and infrastructure team to implement the whole system without inventing missing architecture. Symbolic correspondence content remains versioned data, but the mechanism by which that content is stored, derived, audited, rendered, and revised is fully specified.

---

## 1. Product definition

### 1.1 Product statement

Epi-Card is a QL-native symbolic media system that transforms a situated engagement into a compact, talismanic, printable, playable, and deeply inspectable constellation object.

An engagement combines:

- a **Pasu**, meaning the situated participant or recipient for whom the object is generated;
- an **attractor**, meaning any concept, entity, event, question, relation, situation, image, text, dream, person, place, or other centre of concern;
- an **attractor basin**, meaning the weighted field that constitutes, contextualises, opposes, limits, and excludes around that attractor;
- a **session lineage** and exact **temporal snapshot**;
- optional recordings, transcripts, documents, images, audio, video, astronomical or astrological facts, identity metadata, and prior Epi-Cards;
- the full twelve-position QL conjugate frame;
- a universal resonance-frequency state projected into symbol, colour, typography, sound, shape, pace, camera, motion, material, and light;
- an agent-run production pipeline whose decisions and transformations are themselves QL-auditable;
- a `5′→0⁺` return that deposits the achieved object as the enriched ground of another engagement.

The principal human-facing result is a card-like object with:

1. a moving **front face**: short vertical film, exact transparent symbol or symbol-mask, bespoke lettering, and a restrained drone/bell harmonic palette;
2. an interactive **back face**: a hexagonal surface whose six edges each address one Bimba–Pratibimba pair and unfold the full inner form of both positions;
3. a **deep object**: the twelve-position semantic body, source links, resonance derivation, media assets, production history, QL audits, and return;
4. a **printed form**: poster frame plus symbol on the front, static conjugate hexagon plus names and QR code on the back;
5. an **OKF wiki artifact set**: a portable human- and agent-readable knowledge expression generated from the operational record.

### 1.2 The product is generated through an agentic skill pipeline

The canonical creative process is not a form submitted once to a model. It is a resumable sequence of typed actions executed by an agent with a dedicated Epi-Card skill and CLI. The agent may run in Hermes or any other harness capable of reading an Agent Skill, invoking a command-line program, and handling structured JSON results.

The runtime exposes the same action definitions to:

- the agent;
- the CLI;
- the production studio UI;
- the public card UI where an action is permitted;
- automated tests and scheduled jobs;
- an HTTP action boundary.

The model chooses, sequences, and revises actions. Deterministic code owns validation, database writes, content hashing, rendering parameters, permission enforcement, and publication gates.

### 1.3 Product identity and data identity

The Epi-Card visual component is a projection of an operational SQL record. The canonical object is a **Constellation Engagement** and its immutable **Renditions**. The product does not use JSON-LD as its primary store. JSON and JSON Schema remain action, provider, and interchange contracts. The OKF bundle is a generated wiki artifact set. Media assets remain content-addressed files.

### 1.4 Explicit v1 boundaries

The following boundaries are fixed:

- The Bimba map is not part of the v1 product data model and is not required for attractor identity, relation storage, retrieval, or inference.
- An attractor is a local domain object and may later be linked to another graph without changing its v1 identity.
- The Open Knowledge Format is an exported wiki-like artifact set, not an operational database.
- MCP is not part of the architecture.
- Hermes is the first supported harness profile, not the canonical runtime.
- The canonical agent boundary is Agent Skills plus the `epicard` CLI and shared action library.
- The full `6 + 6′` conjugate form is mandatory. A single-face sixfold is not a conforming final engagement.

---

## 2. Fixed design decisions and reasons

| Area | Fixed v1 decision | Reason carried by the product |
|---|---|---|
| QL form | Twelve first-class positions: `P0…P5` and `P0′…P5′` | Bimba and Pratibimba are the complete conjugate body, not an optional advanced mode. |
| Sequence | `P0→P1→P2→P3→P4→P5→P0′→P1′→P2′→P3′→P4′→P5′→P0⁺` | This preserves the Day traversal, Klein twist, Night traversal, and enriched return. |
| Card back | Six clickable hexagonal edges, each edge binding `Pn↔Pn′` | The hexagon presents the paired structure without reducing the stored twelvefold. |
| Film model | Twelve scene atoms organised into six reciprocal scene pairs | Every QL position receives a media articulation while short formats retain legibility. |
| Base duration | 6–12 seconds | One to two seconds per reciprocal pair fits current short-form generation and looping. |
| Extended duration | 40–60 seconds | The same twelve atoms can breathe as a contemplative or explanatory form. |
| Loop | Last state returns visually to the first while the semantic tick advances | Full Spanda return is cyclic recurrence with retained difference, not flat replay. |
| Data store | PostgreSQL 18 or later in deployment; SQLite 3.45 or later in portable packages | SQL provides transactional operational state; SQLite provides self-contained offline carriage. |
| Media store | Content-addressed files keyed by SHA-256 | Assets remain deduplicated, inspectable, immutable, and reproducible. |
| Agent boundary | Agent Skill + CLI + shared actions | A small portable skill can operate the full system in any competent harness. |
| Video generation | Provider adapter registry; Seedance 2.0 is the reference first adapter | The system uses current multimodal generation while retaining provider independence. |
| Composition | Remotion plus FFmpeg reference renderer | Generated plates, exact SVG symbols, typography, audio, masks, and timing require deterministic finishing. |
| Symbol master | Sanitised SVG construction plus transparent derivatives | Symbols must remain exact, scalable, printable, bankable, and usable as masks. |
| Audio core | Custom Faust QL Resonator; commercial instruments used for audition and design | The canonical sound must be deterministic, ratio-exact, automatable, and deployable in browser/offline contexts. |
| Knowledge export | OKF v0.2 bundle | The deep object becomes a portable wiki artifact set with provenance, trust, lifecycle, and cross-links. |
| Publication | Separate approval-gated action | Rendering and uploading are distinct production events with different permissions. |

Every configurable symbolic correspondence is stored as a named profile with version, source register, author, and effective dates. The runtime never hides an unversioned mapping inside model prompts.

---

## 3. Canonical QL conjugate frame

### 3.1 Twelve addresses

The system SHALL create exactly twelve position records for every engagement.

#### Bimba / Day phase

| Address | Canonical QL unit | Archetypal question | Structural role |
|---|---|---|---|
| `P0` | Truth | Why? | Ground / source / ever-present origin |
| `P1` | Mind | What? | First definition / material articulation |
| `P2` | Word | How? | Dynamis / operation / energetic expression |
| `P3` | Logos | Who? Which? Whereby? | Pattern / identity / ordering relation |
| `P4` | Son | Where? When? Whither? | Context / horizon / situated embodiment |
| `P5` | Image | Why-for? Why-not? | Synthesis / integration / manifested whole |

#### Pratibimba / Night phase

| Address | Canonical QL unit | Inverted question | Structural role |
|---|---|---|---|
| `P0′` | Play | Why, through groundlessness? | Abyss, freedom, ungrounded source condition |
| `P1′` | Need | What hidden form or trace remains? | Residue, evidence, demand, concealed definition |
| `P2′` | Sacrifice | How does operation meet obstruction and cost? | Resistance, shadow, exchange, necessary loss |
| `P3′` | Decision | Which pattern operates beneath the recognised pattern? | Cut, counter-pattern, recurrence, governing choice |
| `P4′` | Love | Which sources and missed contexts reopen the horizon? | Context examining itself, care, embrace, reframing |
| `P5′` | Work | What crystallises from the conjugate passage? | Verified expression, public work, completed recognition |

Local lenses MAY add names, questions, and descriptions. They SHALL NOT replace or renumber the twelve canonical addresses.

Canonical Pratibimba addresses SHALL use the Unicode PRIME character `′` (`U+2032`), not an ASCII apostrophe. SQL rows, action payloads, JSON contracts, OKF files, package manifests, UI state, and public URLs SHALL therefore use `P0′…P5′`. A provider adapter MAY translate these addresses to a transport-only alias such as `N0…N5` when an external provider cannot preserve the prime glyph; the adapter SHALL record the reversible mapping in the provider request and SHALL restore canonical addresses before any response enters operational state. Transport aliases are not valid canonical identifiers.

### 3.2 Traversal edges

The runtime SHALL materialise the following edges:

```text
Bimba adjacency:
P0→P1→P2→P3→P4→P5

Klein twist:
P5→P0′

Pratibimba adjacency:
P0′→P1′→P2′→P3′→P4′→P5′

Enriched return:
P5′→P0⁺
```

`P0⁺` is not a thirteenth stored position. It is the next engagement tick’s `P0`, linked through a return deposit carrying semantic and media delta.

### 3.3 Conjugate, complement, and partition relations

Every engagement SHALL expose four simultaneous relation systems:

1. **Conjugate pairs:** `P0↔P0′`, `P1↔P1′`, …, `P5↔P5′`.
2. **Complement pairs within Bimba:** `P0↔P5`, `P1↔P4`, `P2↔P3`.
3. **Complement pairs within Pratibimba:** `P0′↔P5′`, `P1′↔P4′`, `P2′↔P3′`.
4. **Partitions:**
   - `4:2`: explicate `P1,P2,P3,P4`; implicate `P0,P5`, and correspondingly primed;
   - `3:3`: physical/emanative triad `P1,P2,P3`; contextual/return triad `P4,P5,P0`, and correspondingly primed.

These relations are computed from position addresses and stored in the QL profile registry for inspection and rendering.

### 3.4 Threshold and return

The full object is framed by two non-position records:

- **Threshold `0/1`:** binds the Pasu, session, temporal field, attractor, basin, intention, source material, permissions, and the emblematic operation about to be generated.
- **Return `5′→0⁺`:** records self-implication, remainder, achieved work, external implications, next seeds, changed resonance, and the relationship between the loop’s final and first media states.

Threshold and return MUST be represented in data, audit, media timing, and OKF export. They are transitions around the twelve positions, not extra slots inserted into the address set.

### 3.5 Occupancy and incomplete source forms

QL organises source material without pretending that every source arrives as a complete sixfold.

Each position articulation SHALL carry one occupancy state:

```text
present
latent
missing
unknown
withheld
conflicted
overdetermined
```

The source-to-QL mapping SHALL use explicit assignment roles:

```text
direct        one source member primarily occupies one position
distributed   one source member contributes to several positions
condensed     several source members are integrated into one position
supporting    a member evidences or enriches a primary assignment
counterposed  a member supplies the conjugate, limit, or opposition
unassigned    a member remains outside the current mapping
```

A fivefold form may therefore produce five supported allocations and one `missing` or `unknown` position. A sevenfold form may distribute or condense members while retaining an unassigned remainder. The mapper MUST NOT create unsupported content merely to make the display look complete. The twelve QL addresses remain present as structure; their occupancy communicates the actual state of the constellation.

---

## 4. Core domain model

### 4.1 Pasu

A Pasu is the situated participant or recipient relative to whom an Epi-Card engagement has meaning. The record supports:

- a human individual;
- a collective or relationship;
- an anonymous or pseudonymous participant;
- another declared situated subject type.

A Pasu record contains only stable identity and consent metadata. Context that can change is captured in a per-engagement Pasu snapshot.

Required fields:

```text
id
kind
public_handle
private_profile_reference
locale
timezone_default
consent_profile
created_at
updated_at
```

Optional structured identity fields are stored as typed `pasu_attribute` rows, including birth data, preferred names, acquired names, symbolic systems, self-descriptions, current practices, and profile references. Every attribute declares privacy class, source, temporal validity, and whether it may be sent to an external generation provider.

### 4.2 Session

A session is an operational continuity container. It is not identical to an engagement.

A session SHALL contain:

- an application-generated UUIDv7 identifier;
- a 256-bit opaque session key presented once to the initiating client;
- a stored cryptographic hash of the session key;
- Pasu reference;
- parent session and continuation references;
- harness name and external harness session reference;
- start/end timestamps, timezone, locale, and privacy class;
- resumable state and last acknowledged event sequence.

One session may contain several engagements. One engagement may be continued by several sessions through an explicit join table. The session key SHALL never appear in public URLs, QR codes, exported OKF files, or provider prompts.

### 4.3 Temporal snapshot

Generation is relative to exact time. A temporal snapshot SHALL separate:

- event time;
- observation time;
- local civil time;
- timezone;
- location and precision;
- astronomical fact provider and version;
- astrological calculation profile and version;
- raw astronomical facts;
- interpreted symbolic contributions.

The same astronomical facts MAY be reinterpreted under a different correspondence profile without recomputing the sky.

### 4.4 Talismanic activation

An engagement MAY carry a talismanic activation record containing:

```text
intent_statement
recipient_pasu_id
activation_scope
activation_at
activation_event
review_at
expiry_condition
return_condition
handling_or_placement_notes
private_phrase_reference
witness_actor_ids
cadence_or_repetition
```

These fields govern how the object is meant to be encountered, revisited, carried, placed, printed, watched, or sounded. Activation metadata participates in resonance and scene planning when its profile permits.

### 4.5 Attractor

An attractor is any concept or entity around which a constellation is being formed. It has no dependency on the Bimba map.

Required fields:

```text
id
kind
label
description
stable_key optional
created_by
created_at
```

`kind` is extensible and may include concept, person, place, event, question, relation, work, image, dream, situation, process, symbol, or another producer-defined value.

### 4.6 Attractor basin

The basin defines the attractor through weighted relations. Every basin member has:

- a stable local key;
- label and description;
- relation type;
- weight from `0` to `1`;
- evidence register;
- source references;
- temporal validity;
- inclusion rationale;
- optional QL candidate addresses.

Relation types are:

```text
essential       without this, the attractor would cease to be this attractor
constitutive    a part, property, or necessary relation
contextual      situation, horizon, environment, or observer condition
resonant        analogy, affinity, or neighbouring symbolic charge
counterpole     an active polarity required to define the field
boundary        the edge or threshold of the basin
excluded        explicitly outside the current constellation
unresolved      relevant but not yet placed
```

The basin resolver SHALL preserve exclusions and unresolved members. They are rendered in the Night phase and return where relevant rather than being dropped.

### 4.7 Engagement

The Constellation Engagement is the central operational object. It joins:

```text
Pasu snapshot
originating and continuing sessions
temporal snapshot
attractor and basin version
question and intention
talismanic activation
source forms and source assets
full twelve-position QL frame
resonance-frequency state
symbol family and states
film scene atoms and pair choreography
audio palette and rendered layers
agent runs and QL audits
renditions, publications, OKF exports, and return deposit
```

Engagement status values are:

```text
draft
mapping
art_direction
production
review
approved
rendered
published
returned
archived
```

State transitions are action-controlled and audit-recorded.

### 4.8 Source forms and evidence

A source form records the native organisation of an input before QL mapping. It MAY be arity-zero/unstructured, dyadic, triadic, fivefold, sixfold, twelvefold, or another declared form.

Supported evidence objects include:

- text documents and fragments;
- images and regions;
- audio/video and time ranges;
- recordings and transcript segments;
- structured data rows;
- astronomical facts;
- user-entered statements;
- prior Epi-Card positions, symbols, scenes, or returns;
- generated candidates.

Every claim, mapping, resonance contribution, and decision can link to evidence through a single typed evidence-link table.

---

## 5. Recording and transcript system

### 5.1 Recording ingestion

The runtime SHALL support audio and audiovisual recordings attached to a session or engagement. A recording record contains:

```text
asset_id
session_id
engagement_id optional
recorded_at
speaker_map
consent_state
privacy_class
language hints
capture device metadata optional
```

### 5.2 Transcription

Transcription is a provider action. The result SHALL store:

- provider, model, and model version;
- language;
- diarisation map;
- segment start/end milliseconds;
- speaker reference;
- text;
- confidence;
- redaction state;
- transcript asset and digest.

### 5.3 Semantic linking

A transcript segment MAY evidence:

- an attractor basin member;
- a QL position or mapping assignment;
- a resonance contribution;
- a symbol decision;
- a scene instruction;
- an audio state;
- an audit position;
- a return implication.

The studio SHALL allow a user to select a transcript range and attach it to one or more of these targets. The agent MAY propose links; each proposal is stored as an auditable action.

### 5.4 Public projection

Public renditions and public OKF exports SHALL contain only transcript excerpts permitted by the disclosure profile. Private recordings remain addressable from the operational engagement without being copied into the public package.

---

## 6. Universal resonance-frequency architecture

### 6.1 Definition

The system uses **frequency** as the universal abstraction for recurrence, phase, interval, intensity, density, and return across symbolic media. Physical Hertz is one modality projection of this field. Colour angle, geometric orientation, animation pace, scene density, typographic rhythm, astrological contribution, elemental charge, and chakra placement are other projections.

The canonical dimensionless state is the resonance-frequency coordinate:

\[
\Phi = (\theta, \rho, \tau, a, c, \beta, p, R, E, C)
\]

with:

| Component | Domain | Meaning |
|---|---:|---|
| `θ` phase | `[0,1)` | cyclic location within the twelvefold field |
| `ρ` register | real | logarithmic scale/octave/register displacement |
| `τ` pulse | non-negative real | event density or motion rate per Spanda tick |
| `a` amplitude | `[0,1]` | expressive force, contrast, loudness, salience |
| `c` coherence | `[0,1]` | ordered integration, harmonicity, regularity |
| `β` bandwidth | `[0,1]` | complexity, inharmonic spread, textural width |
| `p` polarity | `[-1,1]` | Bimba–Pratibimba orientation and directional bias |
| `R` ratio set | rational list | interval and proportional identities |
| `E` elemental vector | named weighted vector | elemental/material charge under a versioned profile |
| `C` chakra vector | named weighted vector | vertical/energetic charge under a versioned profile |

Every position has a baseline `Φ`, and every engagement has aggregate and per-position states. Bimba and Pratibimba states share the same position index while carrying conjugate polarity, phase, ratio, and contextual adjustments.

### 6.2 Twelvefold phase baseline

The reference musical phase profile uses the two interlocked whole-tone helices:

```text
Bimba pitch-class offsets:      0, 2, 4, 6, 8, 10
Pratibimba pitch-class offsets: 1, 3, 5, 7, 9, 11
```

The tonic is configurable. Corresponding `Pn↔Pn′` positions differ by one semitone in this projection. Complement positions within one helix differ by the profile’s tritone mirror. The ratio field retains the foundational family `4/3`, `3/4`, `2/3`, `3/2`, the epogdoon `9/8`, totality `16/9`, octave `2/1`, and unison `1/1` where the active musical profile calls them.

### 6.3 Source-to-resonance contribution

Every contributing system is represented by versioned correspondence rules:

```text
source system
source selector
source value or condition
target resonance components
component vector
weight
evidence register
rationale
source citation/reference
effective version and date
```

Supported source systems include:

- QL position and lens;
- attractor basin semantics;
- Pasu identity and current situation;
- declared intention and talismanic activation;
- astrology and astronomical facts;
- elemental and chakra profiles;
- transcript and audio analysis;
- prior card return;
- direct human art direction.

An LLM MAY propose contribution rows. The deterministic resonance aggregator SHALL calculate the final state from persisted contributions and profiles.

### 6.4 Circular and scalar aggregation

Phase uses a weighted circular mean:

\[
\theta = \frac{1}{2\pi}\operatorname{atan2}
\left(
\sum_i w_i\sin 2\pi\theta_i,
\sum_i w_i\cos 2\pi\theta_i
\right) \pmod 1.
\]

Scalar components use bounded weighted means followed by profile-specific transforms. Ratio sets use weighted union plus reduction to canonical rational form. Elemental and chakra vectors are normalised independently so that their weights sum to `1` when at least one contribution is present.

### 6.5 Modality projection profiles

A projection profile is a versioned transformation from `Φ` into one medium. The runtime SHALL ship reference profiles for:

- audio;
- colour;
- geometry;
- typography;
- motion;
- editing pace;
- light/material;
- spatial composition.

Each profile declares its parameters, transforms, clamps, defaults, and inverse-inspection labels. A renderer SHALL record the exact profile version used.

#### Audio projection

```text
θ        pitch-class/phase emphasis
ρ        octave or resonator-size register
τ        strike or modulation density
a        loudness and excitation force
c        harmonic-to-inharmonic balance and tuning stability
β        modal spread, noise, and resonance complexity
p        stereo, phase, and Bimba/Pratibimba body weighting
R        exact fundamental and partial ratios
E        material/resonator family
C        vertical register, spectral centre, and spatial height
```

#### Colour projection

The reference renderer uses OKLCH:

```text
θ        hue angle relative to profile hue origin
ρ        lightness/register curve
a        chroma and contrast
c        palette regularity and gradient coherence
β        local colour variance and texture
p        conjugate direction, hue rotation sign, or figure/field exchange
E        palette/material bias
C        vertical gradient and luminous centre
```

The hue origin is a required profile parameter; it is not hidden as a universal correspondence.

#### Geometry projection

```text
θ        rotation/orientation phase
ρ        scale and spatial register
a        stroke/area force
c        symmetry and closure
β        vertex count, texture, and edge complexity
p        mirror, winding, inside/outside, or figure/ground direction
R        proportional construction ratios
E        material and primitive preference
C        vertical axis and centre-of-force placement
```

#### Motion and pace projection

```text
τ        edit density and animation speed
a        displacement magnitude
c        smoothness and continuity
β        turbulence and microvariation
p        inward/outward, clockwise/anticlockwise, reveal/conceal
R        duration ratios and repeated temporal subdivisions
```

### 6.6 Correspondence profile governance

Every astrology, elemental, chakra, colour, or cross-media mapping SHALL be stored as data. A correspondence profile contains:

```text
profile_id
version
status
scope
source register
author and reviewers
rules
change log
effective dates
```

The runtime may ship several profiles. An engagement records exactly which profiles were active. A profile update never retroactively alters a frozen rendition.

---

## 7. QL mapping engine

### 7.1 Purpose

The QL mapping engine converts the attractor basin and source forms into the full conjugate frame. It is the semantic centre of the system and runs before art direction.

### 7.2 Mapping stages

The mapper SHALL execute these stages:

1. **Threshold assembly:** gather Pasu snapshot, time, intention, attractor, basin, source forms, permissions, and profile set.
2. **Native-form reading:** identify source members, native arity, relations, gaps, and explicit exclusions without imposing QL labels.
3. **Bimba allocation:** assign source members and claims across `P0…P5` using the active lens and mapping constraints.
4. **Pratibimba derivation:** examine each Bimba position and the whole basin through `P0′…P5′`, resolving groundlessness, evidence, obstruction, hidden pattern, missed context, and crystallised work.
5. **Cross-pair reconciliation:** make every `Pn↔Pn′` relation explicit.
6. **Complement reconciliation:** inspect the `0/5`, `1/4`, and `2/3` pairs in each phase.
7. **Occupancy declaration:** mark missing, latent, conflicted, withheld, or overdetermined positions.
8. **Return proposal:** state self-implication, remainder, next ground, and external implications.
9. **Validation:** verify structural completeness, evidence links, unsupported assertions, and source exclusions.
10. **Human/agent revision loop:** modify assignments through explicit actions until approved.

### 7.3 Position content contract

Every QL position SHALL contain:

```text
canonical address and phase
canonical unit name
active local label and question
short summary
extended articulation
occupancy state
salience
source assignments
claims and evidence links
resonance state
symbol-state reference
scene-atom reference
audio-state reference
card-edge reference
audit status
```

### 7.4 Claim registers

Claims use the project’s differentiated registers:

```text
exact_identity
ql_derived
canonical_symbolic
cross_register
archetypal_reception
open_extension
```

A claim may have several evidence links. The register is not inferred from confidence; it declares the kind of relation being asserted.

### 7.5 Mapping validation rules

The validator SHALL fail finalisation when:

- fewer or more than twelve position records exist;
- a position lacks phase or index;
- a non-missing claim has no source, derivation, or explicit open-extension register;
- a source member is silently discarded rather than assigned or marked unassigned;
- Bimba and Pratibimba are textually duplicated without a declared conjugate transformation;
- an exclusion is reintroduced as positive content without a revision event;
- return lacks remainder or next ground;
- the active lens/profile is absent.

---

## 8. QL audit architecture for agent decisions

### 8.1 Principle

Every material agent decision and every non-trivial media transformation SHALL have a QL audit tick. A flat rationale log is insufficient.

Material decisions include:

- attractor/basin resolution;
- QL mapping;
- correspondence-profile selection;
- resonance contributions;
- symbol reuse, transformation, combination, or generation;
- palette and typography selection;
- scene and storyboard planning;
- provider selection and prompt construction;
- generated asset acceptance or rejection;
- modifier application;
- poster-frame selection;
- audio tuning and rendering;
- final render approval;
- publication metadata and execution;
- OKF export and verification.

### 8.2 Audit frame

An audit tick contains the threshold, twelve audit positions, and return.

#### Bimba audit roles

| Address | Audit role |
|---|---|
| `P0` | decision ground, permission scope, and initiating question |
| `P1` | defined objective, target, or candidate field |
| `P2` | proposed operation, transformation, or generation action |
| `P3` | selection pattern, rule, test, or success criterion |
| `P4` | Pasu, temporal, production, medium, and contextual constraints |
| `P5` | provisional integrated outcome |

#### Pratibimba audit roles

| Address | Audit role |
|---|---|
| `P0′` | ungrounded assumptions, unknowns, and freedom not captured by the objective |
| `P1′` | traces, evidence, residual details, and provenance of the provisional result |
| `P2′` | obstruction, failure, cost, artifact, or sacrifice introduced by the action |
| `P3′` | counter-pattern, alternative interpretation, or hidden selection bias |
| `P4′` | missed context, accessibility issue, Pasu mismatch, or wider horizon |
| `P5′` | verified work, accepted revision, approval state, and deposited output |

The audit return records:

```text
selected outcome
rejected candidates
remaining uncertainty
semantic and media delta
next corrective or generative ground
```

### 8.3 Audit evidence

Audit positions SHALL reference observable material:

- inputs and hashes;
- candidates and scores;
- constraints;
- tool calls and provider responses;
- deterministic measurements;
- review comments;
- comparison images/audio/video;
- validation results;
- actor approvals.

The system stores inspectable decision structure, not hidden model chain-of-thought.

### 8.4 Nested and recursive audits

An audit tick MAY have a parent audit tick. A complex run therefore contains a full engagement-level audit with nested audits for symbol, each scene pair, audio, composition, and publication. The studio shows this as a tree whose nodes each unfold into the same twelve-position audit surface.

### 8.5 Audit completion

A material action cannot reach `succeeded` until:

- all twelve audit positions exist;
- absent positions declare why they are absent;
- deterministic validators pass;
- the return records the selected output and next ground;
- any required human approval is attached.

---

## 9. Shared action runtime

### 9.1 One action definition across product surfaces

The runtime SHALL define each operation once in a shared action library. The same implementation is used by the agent, CLI, HTTP boundary, studio buttons, tests, and scheduled jobs. This follows the current agent-native pattern in which app and agent share actions rather than duplicating a UI API and a separate tool API.

### 9.2 Action contract

Every action declares:

```text
name and semantic version
input JSON Schema
output JSON Schema
required permissions
idempotency behaviour
transaction class and saga boundary
side-effect class
provider dependencies
expected twelve-position audit requirement
retry and resume policy
structured gate policy
```

The normative machine registry is `contracts/action-registry.yaml`. It contains exactly 66 actions and is generated from the human catalogue by `scripts/generate-action-registry.py`. `contracts/action-payloads.schema.json`, generated by `scripts/generate-action-payloads.py`, contains the 66 input and 66 output payload schemas selected by that registry. The generated PostgreSQL and SQLite `action_definition` seeds are applied after the base schemas. Implementations MUST reject a registry whose action names, count, versions, side-effect values, gate policy, or payload references fail validation.

A gate has four mandatory fields:

```text
kind       provider_disclosure | consent | human_review | human_approval | actor_authorization | account_authorization | prior_approval
stage      pre_execute | pre_commit | pre_promote | pre_publish
mode       always | conditional
when       a named activation predicate and typed arguments
requires   a named satisfaction predicate and typed arguments
```

`pre_execute` blocks side effects; `pre_commit` blocks `succeeded`; `pre_promote` permits a candidate result but blocks canonical/approved use; `pre_publish` blocks remote upload. `contracts/gate-predicates.yaml` defines the 22 permitted predicates, the state each reads, its typed argument schema, exact truth condition, and failure code. A runtime MUST evaluate those named predicates and MUST NOT infer gating from prose, side-effect class, or action name.

Conceptual TypeScript interface:

```ts
export interface EpiAction<I, O> {
  name: string;
  version: string;
  permissions: Permission[];
  sideEffect: "read" | "write" | "generate" | "render" | "publish";
  inputSchema: JsonSchema;
  outputSchema: JsonSchema;
  run(input: I, context: ActionContext): Promise<ActionResult<O>>;
  resume(runId: string, context: ActionContext): Promise<ActionResult<O>>;
  cancel(runId: string, context: ActionContext): Promise<void>;
}
```

### 9.3 Action envelope

All external invocations use:

```json
{
  "action": "ql.map",
  "action_version": "1.0.0",
  "request_id": "UUIDv7",
  "idempotency_key": "opaque-string",
  "actor": {
    "kind": "agent",
    "id": "harness-agent-id",
    "harness": "hermes"
  },
  "session_id": "UUIDv7",
  "engagement_id": "UUIDv7",
  "input": {},
  "options": {
    "dry_run": false,
    "approval_mode": "required-when-declared"
  }
}
```

Before invocation, the runtime resolves the action/version in the registry and validates `input` against its exact payload schema. The top-level `session_id` and `engagement_id` are routing/context fields; where the selected action payload also carries either ID, the two values MUST be byte-identical or the request fails with `CONTEXT_ID_MISMATCH`. After execution, `result` is validated against the selected output payload schema before the run may succeed. The result envelope also contains run ID, status, assets, audit tick, warnings, next actions, and retry metadata.

### 9.4 Job state machine

Long-running actions use:

```text
queued
running
awaiting_external
awaiting_review
succeeded
failed_retryable
failed_terminal
cancelled
```

Every transition is event-sourced in `action_event`. Runs preserve provider job IDs and resume cursors. A process restart SHALL not require the agent to repeat successful upstream actions.

Every gate evaluation is persisted in `action_gate_evaluation` with the action run, registry gate index, evaluation number, stage, kind, activation predicate and arguments/result, requirement predicate and arguments/result, decision, failure code, context hash, predicate-registry version, and evaluator version. A run cannot become `succeeded` while a `pre_execute`, `pre_commit`, or `pre_publish` gate lacks an evaluation or is blocked. A `pre_promote` gate may leave the producing action successful as a candidate, but the candidate cannot receive a canonical/approved status until its matching gate passes. Re-evaluation appends a new evaluation number; prior decisions are never overwritten.

### 9.5 Core action catalogue

#### Context and source

```text
pasu.create
pasu.snapshot
session.open
session.resume
session.close
temporal.capture
source.ingest
recording.ingest
recording.transcribe
evidence.link
projection.materialize
projection.validate
```

#### Attractor and QL

```text
attractor.create
basin.resolve
basin.revise
ql.initialize
ql.map
ql.reconcile
ql.validate
ql.approve
lock.acquire
lock.release
return.deposit
```

#### Resonance and art direction

```text
resonance.resolve
resonance.project
resonance.compare
art-direction.resolve
palette.resolve
typography.resolve
```

#### Symbol

```text
symbol.search
symbol.propose
symbol.generate
symbol.transform
symbol.canonicalize
symbol.state.render
symbol.validate
symbol.approve
```

#### Image/video

```text
storyboard.plan
image.collect
image.generate
image.edit
image.alpha
scene.plan
video.submit
video.poll
video.continue
video.edit
plate.accept
modifier.apply
composition.render
loop.validate
poster.select
```

#### Audio

```text
audio.palette.resolve
audio.render
audio.analyze
audio.mix
audio.loop.validate
```

#### Card, package, knowledge, publication

```text
card.render.web
card.render.print
card.package
okf.export
okf.validate
publication.prepare
publication.approve
publication.execute
publication.poll
```

A complete action table with inputs, outputs, permissions, and acceptance rules is supplied in `architecture/action-catalog.md`; the exact audit, gate, transaction, provider, and retry flags are supplied in `contracts/action-registry.yaml`.

---

## 10. Agent Skill and harness independence

### 10.1 Skill format

The operating capability SHALL be distributed as an Agent Skills-compatible directory:

```text
skills/epi-card/
├── SKILL.md
├── scripts/
│   └── run-epicard
├── references/
│   ├── ql-frame.md
│   ├── audit.md
│   ├── resonance.md
│   ├── media-pipeline.md
│   ├── provider-adapters.md
│   ├── privacy-and-approval.md
│   └── cli-reference.md
└── assets/
    ├── render-templates/
    ├── print-templates/
    └── profile-seeds/
```

`SKILL.md` contains only trigger conditions, operating sequence, hard invariants, CLI usage, and reference-loading instructions. Detailed canon and provider material remain in `references/` for progressive disclosure.

### 10.2 Agent operating rules

The skill SHALL instruct the agent to:

1. inspect or create a session and engagement;
2. load the QL frame and active profiles;
3. use actions through the CLI rather than writing SQL directly;
4. keep Bimba and Pratibimba complete as twelve addressed positions;
5. record missing, withheld, and unresolved positions explicitly;
6. create QL audits for every material decision;
7. use generated media as candidate plates and preserve exact symbols/type/audio in deterministic composition;
8. inspect action results and resume failed jobs by run ID;
9. request declared approvals before canonical symbol acceptance, final rendering, public export, or publication;
10. deposit `5′→0⁺` after approval.

### 10.3 Hermes profile

Hermes is the first supported harness because it can load Agent Skills, maintain sessions and memory, expose a TUI/CLI, transcribe voice memos, and execute shell tools. The Epi-Card database remains the canonical state. Hermes memory may help the agent work but does not replace Pasu, session, engagement, evidence, audit, or asset records.

### 10.4 Other harnesses

Any harness is conforming when it can:

- read the Agent Skill;
- call `epicard` non-interactively;
- pass JSON or file references;
- receive JSON/JSONL output;
- preserve run and session IDs;
- surface review requests and progress.

No harness-specific data is required beyond an optional adapter name and external session reference.

---

## 11. CLI specification

### 11.1 Command shape

```text
epicard <domain> <action> [options]
```

Every command supports:

```text
--json
--jsonl
--request @file.json
--session <id>
--engagement <id>
--idempotency-key <value>
--dry-run
--resume <run-id>
--wait
--output <path>
```

Agent use defaults to non-interactive structured output. Human use may add `--interactive`.

### 11.2 Principal commands

```text
epicard session open
epicard engage create
epicard source ingest
epicard projection materialize
epicard attractor resolve
epicard ql map
epicard ql inspect
epicard lock acquire
epicard lock release
epicard resonance resolve
epicard symbol resolve
epicard storyboard plan
epicard media generate
epicard audio render
epicard compose render
epicard validate engagement
epicard card package
epicard okf export
epicard publish prepare
epicard publish execute
epicard return deposit
```

A pipeline convenience command MAY orchestrate actions without hiding them:

```bash
epicard run \
  --engagement "$ENGAGEMENT_ID" \
  --through render \
  --resume \
  --jsonl
```

It SHALL emit every underlying action and audit tick as separate events.

### 11.3 Exit codes

| Code | Meaning |
|---:|---|
| `0` | success |
| `2` | request or schema validation error |
| `3` | permission, disclosure, or authentication failure |
| `4` | state or idempotency conflict |
| `5` | external provider failure |
| `6` | retryable failure |
| `7` | human review or approval required |
| `8` | cancelled |
| `9` | internal runtime failure |

### 11.4 Output discipline

The CLI SHALL never mix human prose into JSON output. Logs go to stderr; results go to stdout. Secret values are redacted. Asset results use stable IDs and paths rather than base64 payloads.

---

## 12. Storage and persistence architecture

### 12.1 Production topology

```text
PostgreSQL                 operational and semantic state
S3-compatible object store content-addressed media and exports
worker queue               long-running generation/render jobs
render workers             Remotion, FFmpeg, Faust, image tools
web application            studio and public card surface
action service             shared action HTTP boundary
```

### 12.2 Portable package

A `.epicard` package is a ZIP or directory:

```text
<slug>.epicard/
├── manifest.json
├── card.sqlite
├── assets/
│   └── sha256/<prefix>/<digest>.<ext>
├── renders/
│   ├── master-9x16.mp4
│   ├── loop.webm
│   ├── poster.webp
│   ├── audio.flac
│   ├── print-front.pdf
│   └── print-back.pdf
├── knowledge/
│   └── <OKF v0.2 bundle>
└── reports/
    ├── validation.json
    └── audit-summary.json
```

The package contains a public, shared, or private disclosure profile. The manifest states which profile was used.

#### 12.2.1 Normative package manifest

`manifest.json` SHALL validate against `contracts/package-manifest.schema.json`. It identifies the exact engagement revision number, immutable QL frame revision and hash, profile set and hash, schema/specification versions, disclosure projection, entrypoints, renditions, and every packaged file. Each `files[]` member records package-relative path, SHA-256, byte length, media type, semantic role, disclosure class, and associated asset/rendition IDs where applicable.

Package paths SHALL use UTF-8 and forward slashes, SHALL be relative to the package root, and SHALL NOT contain backslashes, empty segments, absolute prefixes, or `.`/`..` path segments. Each path SHALL occur exactly once. Every entrypoint and rendition path SHALL resolve to one `files[]` member; every physical file other than `manifest.json` SHALL occur in `files[]`; no listed file may be absent.

The root digest is computed independently of JSON serialisation. Sort `files[]` by path in Unicode code-point order. For each entry append the lowercase hexadecimal SHA-256, two U+0020 spaces, the path, and U+000A. The SHA-256 of the resulting UTF-8 byte sequence is `integrity.root_sha256`. `manifest.json` is excluded because its file hash is stored externally in the package action result and operational database. Importers SHALL verify individual files, the root digest, specification hash, schema version, projection hash, and disclosure manifest before opening the package.

The reference instance is `examples/minimal-package-manifest.json`. Implementations SHALL additionally enforce uniqueness and path/file closure, because JSON Schema alone cannot express every cross-item and filesystem invariant.

The operational `package_export` row persists the engagement revision number, approved projection/hash, approved QL frame revision/hash, active profile set/hash, OKF export, schema/specification hash, manifest schema ID, manifest file hash, package root digest, package asset, and passing validation report. `package_export_rendition` records every approved rendition included. SQL consistency guards require all referenced records to belong to the same engagement and disclosure projection before the package can be committed. The `card.package` request supplies the expected immutable IDs and hashes so a concurrent semantic or disclosure revision fails rather than silently changing package contents.

Package creation SHALL use this non-circular sequence:

1. preallocate `package_id` and freeze the request IDs/hashes;
2. materialise `card.sqlite` from the approved disclosure projection, excluding the current package's `package_export`, `package_export_rendition`, package-archive asset, manifest asset, and any value derived from the yet-unknown package root;
3. write all selected assets, renditions, OKF files, the audit summary, and a **content-validation report** that validates those inputs but does not embed the manifest hash, package root, archive hash, or its own file hash;
4. hash every physical file except `manifest.json`, compute the path-sorted root digest, and write `manifest.json`;
5. hash `manifest.json`, assemble the directory/ZIP, verify archive path closure and every declared digest, then commit the archive as a content-addressed asset;
6. create the production `package_export` and `package_export_rendition` rows using the preallocated ID and the completed hashes.

The package archive cannot contain its own archive hash, and `card.sqlite` cannot contain the current package record, because either would create a self-hash cycle. The production record and action result are the detached receipt for the archive and manifest. Importers MAY persist a new local import receipt after verification; they SHALL NOT alter the immutable bytes whose digest was verified.

The reference ZIP profile is deterministic: entries are emitted in Unicode code-point path order; names use UTF-8; explicit directory entries, archive comments, symlinks, and platform-specific extra fields are omitted; every file uses ZIP method `STORE` because the major media are already compressed; the DOS timestamp is `1980-01-01 00:00:00`; the Unix external mode is `0644`; and ZIP64 fields are used only when size/offset limits require them. A different container profile MAY be introduced only as a versioned package profile. Its archive hash may differ, but its unpacked file hashes, normative manifest, and root digest SHALL be identical.

### 12.3 Content addressing

Every asset uses SHA-256. The canonical object path is:

```text
sha256/<first-two>/<next-two>/<full-digest>.<extension>
```

An asset is immutable. An edit creates a new asset with a new digest and a derivation link to its input.

### 12.4 Database revisions

Mutable design work is expressed through revision rows and action events. The normalised `ql_position`, `ql_assignment`, `claim`, and `ql_relation` rows are the active working projection used by the mapper and studio; every proposed or approved semantic checkpoint is frozen as an immutable `ql_frame_revision` containing the complete threshold, twelve-position frame, relations, assignments, claims, profile set, and return proposal plus its canonical hash. An engagement may name a current QL frame revision only when that revision is approved. Approved and superseded frame contents cannot be edited or deleted.

All active configuration is selected through a versioned `profile_set`. Profile members identify their registry, ID, version, precedence, and whether they are required. The set hash becomes part of the engagement and rendition dependency manifest.

Private, shared, public, and provider-facing data are materialised as immutable `engagement_projection` snapshots. Public routes and QR targets read an approved public projection; external provider actions read an approved provider projection. They do not assemble disclosure ad hoc while making a request.

Mutable design work is protected by persisted `resource_lock` records addressing an object and optional field path. Lock acquisition and release are shared actions, and every write action checks active locks before mutation.

Action definitions, their structured gate policies, and every gate evaluation are persisted alongside run events. The database enforces complete operational-stage gate evaluation before action success; the runtime additionally enforces promotion-stage gates against candidate/canonical status transitions.

An approved rendition references immutable revision IDs. Database migrations use semantic schema versions and include both PostgreSQL and SQLite transformations.

#### 12.4.1 Immutability and lifecycle matrix

The following mutation rules are normative and SHALL be enforced by the shared actions and database guards. “Body” means every field except the explicitly permitted status/timestamp fields. Child rows named below are part of the parent body.

| Aggregate | Mutable state(s) | Permitted forward transitions | Freeze boundary and required revision behaviour |
|---|---|---|---|
| `asset` and `asset_derivation` | none after insertion | no status transition | Asset bytes, SHA-256, metadata, rights snapshot, and derivation edges are append-only. A correction creates a new asset/edge. |
| `engagement_projection` | `draft` | `draft→approved`; `approved→superseded|expired` | Snapshot, source revision manifest, hash, kind, provider, purpose, and disclosure freeze at approval. Non-draft rows cannot be deleted. |
| `configuration_profile`, `correspondence_profile`, `projection_profile` | `draft` | `draft→active`; `active→deprecated|retired`; `deprecated→retired` | Content, hash, identity, version, source/change records, and effective range freeze when active. Any content change creates a new semantic version. |
| `provider_capability` | active record may be deactivated only | `active=true→false` | Provider/model/version/capability version, limits, features, constraints, terms snapshot, and checked time are immutable. A refreshed capability is a new version row. |
| `profile_set` plus `profile_set_member` | parent `draft` | `draft→active`; `active→deprecated|retired`; `deprecated→retired` | Set identity, hash, description, and complete membership freeze when active. Membership changes create a new profile-set version and hash. |
| `ql_frame_revision` | `proposed` before approval | `proposed→approved`; `approved→superseded` | Threshold/frame snapshot, relations, assignments, claims, profile set, return proposal, and hash freeze at approval. The existing database guard prohibits approved/superseded content edits or deletion. |
| `art_direction_revision` | `draft|proposed` | `draft→proposed→approved`; `approved→superseded` | Palette, typography, geometry, motion, material/light direction, constraints, and locks freeze at approval. Revisions are linked by engagement/revision number. |
| `symbol_revision` plus `symbol_state` | `candidate|validated` | `candidate→validated→approved`; `approved→superseded` | Grammar, canonical/monochrome assets, resolution mode, and all twelve states freeze at approval. Any changed state or SVG creates a new symbol revision. |
| `storyboard_revision` plus `scene_pair` and `scene_atom` | `draft` | `draft→approved`; `approved→superseded` | Profile, canvas, frame rate, duration, twelve atoms, six pair choreographies, timing, intent, generation plans, and accepted plates freeze at approval. A plate replacement creates a new storyboard revision. |
| `audio_palette_revision` plus `audio_state` | `draft` | `draft→approved`; `approved→superseded` | Reference frequency, ratio set, tuning/resonator/spatial profiles, and all twelve address states freeze at approval. |
| `render_plan` | none after insertion | none | The plan JSON/hash, exact input revision IDs/hashes, renderer, and renderer version are immutable. Any input or compiler change creates a new plan. |
| `rendition` plus `rendition_asset` | `rendering|candidate` | `rendering→candidate|failed`; `candidate→approved|failed`; `approved→superseded` | Manifest, input dependency set, and attached assets freeze at approval. Prior approved output remains queryable after supersession. |
| `provider_disclosure_manifest` | `proposed` | `proposed→approved|rejected`; `approved→used|expired`; `used→expired` | Projection, provider/model, purpose, transmitted fields/assets, privacy summary, retention expectation, and consent receipt freeze at approval. |
| `approval` | pending decision only | `requested→approved|rejected`; `approved→revoked` | Target identity/hash, actor scope, request basis, and decision evidence are append-only; revocation records time/reason without rewriting the original decision basis. |
| `action_event`, completed `audit_tick`, `audit_position`, validation evidence | append-only until owning run/tick completion where applicable | terminal status only through registered action transition | Existing event/evidence rows are never rewritten to alter history. Corrections append superseding events, audits, or reports. |
| `okf_export`, `package_export`, `publication` prepared payload | draft/preparation action only | export rows are final; publication follows its declared status machine | Export manifests/assets are immutable. Publication metadata/rendition/disclosure hashes freeze before approval; any change invalidates approval and requires a new prepared revision. |

A database implementation MAY use row triggers, append-only tables, restricted repository methods, or a combination, but it SHALL produce the same rejection and revision behaviour. Direct SQL roles used by application processes SHALL NOT possess privileges that bypass these guards.

### 12.5 Disclosure classes

Every sensitive row and asset declares:

```text
secret
private
shared
public
```

An export or provider request is created under a disclosure profile that selects allowed classes and may substitute redacted derivatives.

---

## 13. Asset registry and provenance

### 13.1 Asset roles

The asset registry supports:

```text
source
reference
candidate
canonical
intermediate
rendition
poster
mask
symbol
font-outline
audio-layer
transcript
storyboard
print
knowledge-export
validation-report
```

### 13.2 Required metadata

Every asset SHALL carry:

```text
id
sha256
URI or local path
media type
role
byte length
width/height/duration where applicable
alpha mode
colour profile
sample rate/bit depth where applicable
rights status and licence
creator/producer actor
provider/model/version where generated
input asset links
created_at
privacy class
```

### 13.3 Derivation graph

Asset derivation is stored relationally:

```text
source → generated plate → colour-modified plate → masked composition → encoded rendition
```

Every modifier step records operation name, version, parameters, input digest, and output digest.

---

## 14. Symbol system

### 14.1 Symbol family

A symbol family is a bankable, relational identity with:

- semantic operation;
- invariant construction grammar;
- primary canonical SVG;
- Bimba and Pratibimba articulations;
- twelve positional states;
- monochrome and print variants;
- resonance signature;
- relation links to other symbol families;
- revision and approval history.

### 14.2 Construction grammar

The reference grammar supports primitives:

```text
point
line
ray
arc
circle
ellipse
polygon
spiral
aperture
field
knot
mask
glyph
path
```

and operators:

```text
repeat
mirror
rotate
invert
intersect
contain
cross
braid
cut
open
close
phase-shift
fold
unfold
return
```

A grammar record declares proportions, anchors, symmetry axes, winding, stroke rules, open seams, required apertures, figure/field status, and permitted variation.

### 14.3 Search and generation

The symbol resolver searches the bank by:

- operation and grammar overlap;
- topology;
- resonance distance;
- QL occupancy and position salience;
- attractor basin overlap;
- conjugate relation;
- prior use and exclusion rules.

It then audits one of five actions:

```text
reuse
parameterise
transform
combine
generate-new
```

### 14.4 Canonicalisation pipeline

Preferred pipeline:

```text
symbol grammar proposal
→ constructive SVG generation
→ geometry validation
→ sanitisation
→ Bimba/Pratibimba transformation
→ twelve state derivation
→ human/agent review
→ canonical revision
→ raster and motion-mask derivatives
```

Fallback for raster-generated candidates:

```text
controlled-background or transparent generation
→ alpha matting/background removal
→ edge cleanup
→ vectorisation
→ primitive and constraint reconstruction
→ geometry validation
→ approval
```

The raster candidate never becomes the canonical symbol merely because it is visually attractive.

### 14.5 Twelve symbol states

Every position has a symbol state. States MAY alter visibility, phase, rotation, aperture, repetition, boundary, stroke, or internal relation while retaining family invariants. `P5′` SHALL be capable of transitioning into the next tick’s `P0` state without a discontinuity in the loop profile.

### 14.6 Alpha and mask outputs

Required derivatives:

```text
SVG master
SVG monochrome
PNG/WebP transparent at standard sizes
WebM alpha animation
ProRes 4444 alpha master where production requires
luma mask
alpha mask
print vector
```

---

## 15. Colour and typographic art direction

### 15.1 Palette tokens

Each engagement palette SHALL define semantic tokens:

```text
field
figure
boundary
bimba
pratibimba
accent
return
shadow
light
text
```

The working colour representation is OKLCH plus sRGB and CMYK/ICC derivatives. Palette generation is a resonance projection followed by contrast and print validation.

### 15.2 Palette derivation record

Each token records:

```text
resonance input
projection profile and version
pre-adjustment value
accessibility/print adjustment
final value
manual override if any
QL audit tick
```

### 15.3 Typography signature

The font and bespoke lettering system uses a structured signature:

```text
weight
width
contrast
serifness
curvature
corner hardness
terminal openness
stroke modulation
rhythm
historical temperature
mechanical/organic balance
```

A font bank stores these features, licensing, variable axes, supported glyphs, and permitted embedding. The resolver selects or combines candidates using resonance and product constraints.

### 15.4 Bespoke card lettering

Per-card work is normally a title wordmark or limited glyph set, not a complete redistributable font. Approved lettering is stored as SVG outlines. Body text uses a licensed, embeddable system font with fallbacks. The print and web renderers SHALL never depend on a font file that the package is not licensed to distribute.

---

## 16. Film and scene architecture

### 16.1 Canonical scene model

Every engagement SHALL have exactly twelve scene atoms:

```text
P0 P1 P2 P3 P4 P5
P0′ P1′ P2′ P3′ P4′ P5′
```

For clarity in data, the Pratibimba atoms use addresses `N0…N5` internally only when a provider cannot accept prime glyphs; canonical display remains `P0′…P5′`.

Each `Pn` and `Pn′` forms one reciprocal scene pair. A scene pair contains both atoms, their relation, and one choreography mode.

### 16.2 Scene atom contract

Every scene atom contains:

```text
QL address and articulation reference
duration in frames and rational frame rate
semantic intent
attractor/basin members expressed
required symbol state
visual action
subject and environment
camera framing and movement
light and material direction
Bimba/Pratibimba polarity
continuity in/out
forbidden imagery or transformations
reference assets
generation provider request
accepted plate asset
audio state
caption/transcript relation
```

Examples in production prompts SHALL be generated from the actual engagement content or from an explicitly selected, versioned profile. A production prompt MUST NOT introduce example motifs, entities, correspondences, or symbolic claims that are absent from those inputs.

### 16.3 Pair choreography modes

Supported modes:

```text
phase-flip       one face becomes its conjugate
masked-reveal    one face is visible through the other’s symbol/mask
interleaved      rapid alternation within the pair duration
split-field      simultaneous spatial opposition
crossfade        gradual conjugate exchange
conjugate-cut    exact edit from one to the other
figure-ground    foreground and background swap roles
sound-image      one face is visual, the other primarily sonic
```

The chosen mode is stored per pair and QL-audited.

### 16.4 Timeline profiles

#### Base micro-film

```text
duration: 6–12 seconds
aspect: 9:16 master
fps: 24 or 30, declared per rendition
pair duration: approximately 1–2 seconds
atom duration: approximately 0.5–1 second or simultaneous within pair
```

The reference base choreography is pairwise interlaced because it makes conjugacy visible within the available duration. Serial and simultaneous profiles remain supported.

#### Extended film

```text
duration: 40–60 seconds
aspect: 9:16 primary; optional 16:9 and 1:1 derivatives
pair duration: approximately 6.5–10 seconds
atom duration: approximately 3–5 seconds
```

The extended profile may include spoken transcript excerpts, multiple shots within a scene atom, and slower audio development.

### 16.5 Full Spanda loop

A loop is valid when:

- the last visual state joins the first within configured pixel and motion thresholds;
- audio loop points meet amplitude and phase continuity thresholds;
- `P5′` visibly or structurally deposits into `P0`;
- the return record contains the semantic delta that distinguishes the next tick;
- the loop can render as MP4/WebM and optionally GIF.

The media may repeat the same frames; the engagement tick count and return lineage advance in data.

### 16.6 Storyboard pack

The storyboard action SHALL produce:

- twelve frame boards;
- six pair boards;
- full strip in chosen choreography order;
- symbol state sheet;
- palette/material board;
- camera/motion board;
- audio cue sheet;
- provider-ready reference manifest.

---

## 17. Video and image generation pipeline

### 17.1 Provider independence

Video, image, transcription, and publication providers are adapters. The core stores capability profiles and chooses an adapter based on the render plan.

A video provider capability profile declares:

```text
supported inputs: text/image/video/audio
maximum reference counts
minimum/maximum duration
resolution and aspect ratios
audio generation
video continuation
editing/inpainting
seed support
negative instruction support
job API and polling
content policy constraints
cost estimation
```

### 17.2 Seedance 2.0 reference adapter

The first adapter targets Seedance 2.0 because its current official interface supports text, image, audio, and video references, multi-shot generation, editing/continuation, and up-to-fifteen-second output. The base 6–12 second Epi-Card therefore fits inside one generation task, while the 40–60 second profile is assembled from several tasks.

The adapter SHALL expose the model’s current capability data through the provider registry rather than hard-code assumptions into scene planning.

### 17.3 Generation strategies

#### Single-task base generation

One provider task receives the complete storyboard/reference pack and generates the base clip. This is useful for stylistic and motion continuity.

#### Pair-task base generation

Six short tasks generate one reciprocal pair each, or three tasks generate two pairs each. This gives tighter positional control.

#### Dual-helix generation

One Bimba clip and one Pratibimba clip are generated separately, then interlaced or masked deterministically.

#### Extended generation

One task per position or pair, with continuation references and shared style assets, followed by deterministic assembly.

The art-direction action selects a strategy and records why in the QL audit.

### 17.4 Reference allocation

The system SHALL reserve provider reference slots deliberately. A reference manifest can include:

```text
symbol master
symbol state sheet
Bimba storyboard
Pratibimba storyboard
palette/material board
typography/graphic board
Pasu visual reference with permission
location/object references
motion/camera reference clips
QL audio palette or bell strike
continuity clip
```

### 17.5 Provider output status

Generated outputs enter as `candidate` assets. An acceptance action compares them against:

- scene intent;
- continuity;
- symbol and shape fidelity where relevant;
- forbidden content;
- Pasu likeness constraints;
- technical quality;
- loop suitability;
- Bimba/Pratibimba distinction.

Acceptance, rejection, or edit creates a QL audit tick.

### 17.6 Image pipeline

The image pipeline supports:

```text
collection and licensing
text-to-image generation
image-to-image editing
regional editing
background-free generation
background removal and matting
upscaling
denoising
vectorisation
palette and texture modification
poster preparation
```

Symbols use the dedicated vector-first path. Illustrative subjects and textures may remain raster.

### 17.7 Deterministic modifier stack

Modifiers are ordered, versioned nodes:

```text
trim
retime
crop
scale
stabilise
colour transform
contrast
texture/grain
alpha cleanup
mask
blend
symbol overlay
type overlay
caption overlay
noise reduction
audio replacement
audio mix
loudness normalisation
loop seam
encode
```

The same inputs and modifier versions SHALL reproduce the same output digest, except where a declared nondeterministic external provider is called.

---

## 18. Audio system: QL Resonator

### 18.1 Sonic intention

The canonical sound is a restrained, bell-like, materially rich harmonic field: drone rather than song, resonance rather than constant melodic motion, and gradual change of excitation, damping, spatial relation, and spectral emphasis across the twelve positions.

### 18.2 Instrument architecture

The custom **QL Resonator** SHALL have three coupled layers:

1. **Ratio drone body** — stable oscillators or resonant modes tuned to the active rational ratio set.
2. **Modal bell/plate body** — physically modelled or modal resonators producing metal, bowl, plate, bar, membrane, string, tube, and mineral-like responses.
3. **Spatial return field** — stereo phase, convolution or algorithmic tail, body distance, and Bimba/Pratibimba exchange.

The instrument contains two linked resonator banks:

```text
Bimba bank        standing illumination and primary body
Pratibimba bank   conjugate articulation, reflected excitation, and return body
```

### 18.3 Faust implementation

The canonical DSP SHALL be implemented in Faust so that one source definition can compile to:

- offline command-line renderer;
- WebAssembly/WebAudio browser node;
- native library or plugin target;
- deterministic test renderer.

The first instrument version SHALL expose:

```text
reference frequency
ratio set
register
drone partial count
modal material
modal frequencies and decays
harmonic/inharmonic balance
body size
excitation type
strike/bow/breath hardness
excitation position
damping
bandwidth
Bimba/Pratibimba balance
stereo phase and spread
reverb/tail
loop length
```

### 18.4 Tuning

Exact musical identity is ratio-first:

\[
f_i=f_{ref}\,2^{\rho}r_i,\qquad r_i\in R.
\]

`f_ref` is engagement/profile data. It may be a conventional concert reference, a Pasu voice-derived reference, an instrument sample’s measured fundamental, an astrological profile output, or a human-set tone. Its source is always stored.

### 18.5 Twelve audio states

Each position has an automation state. Pitch changes are optional; the default drone profile changes:

- excitation;
- modal body;
- amplitude;
- damping;
- spectral centre;
- stereo orientation;
- phase;
- resonance tail;
- harmonic/inharmonic balance.

This lets a six-second film remain one sonic object rather than twelve disconnected notes.

### 18.6 External sound-design instruments

The production workflow SHOULD use:

- AAS Chromaphone 3 for rapid audition of coupled physically modelled resonators;
- Madrona Labs Kaivo for granular/physical, spatial, and unusual environmental bodies;
- Surge XT for Scala/MTS-ESP tuning, analysis, and rapid exact-ratio audition.

Presets or stems created with these tools can inform or accompany the Faust instrument, subject to licensing and render reproducibility. The automated server path remains Faust-based.

### 18.7 Audio render and delivery

Required outputs:

```text
48 kHz / 24-bit WAV master
FLAC archival master
Opus or AAC web/social derivative
optional stems: drone, Bimba body, Pratibimba body, bell, ambience
```

Reference delivery target:

```text
integrated loudness: approximately -16 LUFS for the card master
true peak: no higher than -1 dBTP
```

Profiles MAY override these values for platform requirements.

### 18.8 Spectral verification

The validator SHALL calculate:

- FFT/STFT for spectral energy and clipping/noise;
- CQT for logarithmic pitch structure;
- chroma for twelvefold pitch-class distribution;
- ratio deviation in cents;
- loop discontinuity;
- loudness and true peak;
- Bimba/Pratibimba separation metrics.

Audio validation reports are stored as assets and linked into the audit.

---

## 19. Deterministic composition and rendering

### 19.1 Render plan

The composition engine consumes a frozen render plan containing:

```text
engagement revision
rendition profile
frame size and frame rate
twelve scene atoms and six pair choreographies
accepted plate assets
symbol state timeline
palette and type tokens
audio assets and automation
captions
modifier graph
loop seam
output variants
```

### 19.2 Reference renderer

Remotion is the high-level compositor; FFmpeg performs encoding, lower-level filtering, masking, muxing, and validation. Exact symbol geometry, typography, QR codes, and canonical audio are added after generative video.

### 19.3 Output profiles

Required:

```text
9:16 H.264/AAC MP4 master
9:16 VP9/Opus WebM
silent lightweight loop WebM
poster WebP/PNG
transparent symbol animation WebM
print front PDF
print back PDF
OKF bundle
.epicard package
```

Production optional:

```text
ProRes 422 HQ edit master
ProRes 4444 alpha overlay
16:9 and 1:1 derivatives
GIF preview
individual scene/pair stems
```

### 19.4 Safe composition frame

The 9:16 master SHALL contain a central `70:120` physical-card safe frame. Important symbol, title, and QR-independent visual content SHALL stay within this safe region so the same composition can generate the printed card front without a second layout geometry.

---

## 20. Digital card product design

### 20.1 Front face

The front face contains:

- generated video plate;
- exact transparent symbol or symbol-shaped mask;
- limited bespoke title lettering;
- optional coordinate/edition mark;
- QL drone;
- play, sound, and flip controls that recede when not in use.

The symbol may act as overlay, cutout, alpha mask, luma mask, window between conjugate plates, transition matte, or boundary. Its role is declared in the render plan.

### 20.2 Back face: conjugate hexagon

The back is a regular hexagon with edges numbered `0…5` clockwise. Each edge is a single clickable/focusable control that represents the pair `Pn↔Pn′`.

The centre contains the primary symbol and phase control.

Required interactions:

```text
click/tap edge       open pair drawer for Pn and Pn′
keyboard arrows      move between edges
Enter/Space          open active edge
phase toggle/centre  rotate or flip Bimba ↔ Pratibimba presentation
play scene           play the pair’s scene range
open depth           navigate to full position page
return seam          expose P5′→P0⁺ return
Escape/back          close drawer or reduce depth
```

### 20.3 Edge drawer content

Each edge drawer contains, in order:

1. canonical and local names for `Pn`;
2. canonical and local names for `Pn′`;
3. concise reciprocal statement;
4. Bimba articulation and sources;
5. Pratibimba articulation and sources;
6. occupancy/gap state;
7. symbol states;
8. scene pair preview;
9. audio state;
10. nested QL form where present;
11. audit and provenance access;
12. deep OKF/web link.

### 20.4 Nested inner form

A position may unfold into another full QL frame. The UI represents nesting as a new hexagonal depth level with breadcrumb lineage. Nested frames retain the same twelve-position conjugate contract, use a new hexagonal depth level, and preserve breadcrumb lineage. A generic accordion is not the conforming primary representation of a nested QL frame.

### 20.5 Component contract

The browser component SHALL be a standards-based custom element `<epi-card>`. React, Qwik, Svelte, Vue, and other wrappers use the same core parser and state model.

Primary states:

```text
face: front | back
phase: bimba | pratibimba | paired
activePosition: 0..5 | null
depth: integer
playing: boolean
muted: boolean
reducedMotion: boolean
```

### 20.6 Accessibility

The card SHALL provide:

- keyboard operation for all edges and controls;
- visible focus states;
- reduced-motion still or crossfade mode;
- captions/transcript for speech;
- text descriptions of symbol and scene intent;
- sufficient text contrast;
- a static back view that preserves all six pair names;
- audio mute and volume controls.

---

## 21. Printed card specification

### 21.1 Reference format

```text
finished size: 70 × 120 mm
orientation: portrait
bleed: 3 mm
safe area: 5 mm
resolution: 300 dpi minimum for raster material
colour: CMYK using declared print ICC profile
```

The print profile is configurable, but the reference templates and acceptance tests use these dimensions.

### 21.2 Printed front

The front contains:

- approved poster frame;
- canonical symbol;
- outlined title/wordmark;
- optional edition, date, or coordinate mark.

No UI chrome appears.

### 21.3 Printed back

The back contains:

- static conjugate hexagon;
- six Bimba and six Pratibimba names positioned by edge;
- centre symbol;
- visible return seam between edge `5` and edge `0`;
- concise threshold or return line;
- QR code to the public digital twin;
- immutable public ID or truncated content digest.

### 21.4 QR requirements

The QR SHALL:

- contain only a public rendition URL or public immutable ID;
- exclude session keys and private tokens;
- have at least the required quiet zone;
- be at least 14 mm square in the reference profile;
- pass scanning tests from printed proof under ordinary indoor light.

### 21.5 Poster selection

Poster-frame selection is a QL-audited action that evaluates symbol legibility, scene representation, Pasu/attractor fidelity, print contrast, and visual return—not a generic aesthetic score alone.

---

## 22. Studio application

### 22.1 Workspace modules

The production studio SHALL include:

1. **Session and Pasu** — identity snapshot, privacy, consent, time, activation.
2. **Attractor Basin** — centre, members, weights, relations, exclusions, unresolved field.
3. **QL Conjugate Mapper** — twelve positions, evidence assignment, occupancy, pair and complement views.
4. **Resonance Lab** — contributions, profile versions, aggregate state, modality projections.
5. **Symbol Bank** — search, candidate comparison, grammar editor, twelve states, approval.
6. **Art Direction** — palette, typography, material, light, motion, provider strategy.
7. **Storyboard and Scene Pairs** — twelve atoms, six pair choreographies, continuity.
8. **Asset Tray** — source, candidate, accepted, derivative, rights, disclosure.
9. **Audio Lab** — ratio set, instrument parameters, twelve states, spectrum, loop.
10. **Render Timeline** — deterministic composition and output profiles.
11. **Audit Inspector** — nested twelve-position audit tree, evidence, events, approvals.
12. **Review and Approval** — comparison, comments, locks, final acceptance.
13. **Print Preview** — front/back proof, QR test, colour warning.
14. **Knowledge Export** — OKF tree preview and trust/lifecycle fields.
15. **Publication** — metadata, account, privacy, approval, remote status.
16. **Return** — self-implication, remainder, external implications, next seed.

### 22.2 Live agent surface

The agent chat/workspace SHALL show streaming actions and tool results. The user can stop, redirect, lock, reject, or revise without losing completed state. UI changes and agent actions converge on the same action library and database revisions.

### 22.3 Locks

Locks operate at field or asset level:

```text
semantic lock
symbol geometry lock
palette token lock
type lock
scene intent lock
plate lock
audio tuning lock
render lock
publication lock
```

Locks are persisted as `resource_lock` rows with engagement, target kind/ID, optional field path, lock type, reason, actor, acquisition time, optional expiry, and release actor/time/reason. Only one active lock may exist for a target/path. `lock.acquire` and `lock.release` are the only mutation actions for lock state. Every semantic, generation, asset-selection, render, and publication action resolves applicable object, ancestor, asset, and field-path locks before beginning side effects.

An action attempting to change a locked target fails with exit code `4` / HTTP `409` and identifies the lock ID and protected path. An authorised actor must call `lock.release`; there is no implicit model override or local force flag.

---

## 23. OKF v0.2 wiki artifact export

### 23.1 Role

OKF is the readable knowledge expression of an engagement. It is generated from SQL after or during production and may be version-controlled, browsed as a wiki, indexed, or handed to another agent.

### 23.2 Bundle tree

The reference export is:

```text
knowledge/
├── index.md
├── log.md
├── engagement.md
├── attractor.md
├── pasu-context.md              # omitted or redacted in public profile
├── threshold.md
├── ql/
│   ├── index.md
│   ├── p0-truth.md
│   ├── p1-mind.md
│   ├── p2-word.md
│   ├── p3-logos.md
│   ├── p4-son.md
│   ├── p5-image.md
│   ├── p0-prime-play.md
│   ├── p1-prime-need.md
│   ├── p2-prime-sacrifice.md
│   ├── p3-prime-decision.md
│   ├── p4-prime-love.md
│   └── p5-prime-work.md
├── resonance/
│   ├── index.md
│   ├── aggregate.md
│   ├── contributions.md
│   └── projections.md
├── symbol/
│   ├── index.md
│   ├── grammar.md
│   └── states.md
├── film/
│   ├── index.md
│   ├── timeline.md
│   └── pair-0.md ... pair-5.md
├── audio/
│   ├── index.md
│   ├── palette.md
│   └── analysis.md
├── sources/
│   └── ...
├── audit/
│   ├── index.md
│   └── ...
└── return.md
```

### 23.3 Frontmatter mapping

Each concept uses OKF v0.2 fields where applicable:

```yaml
type: Epi-Card QL Position
title: P3 — Logos
description: ...
resource: epicard://engagement/<id>/ql/bimba/3
tags: [epi-card, ql, bimba, p3]
generated: { by: epi-card-runtime/1.0.0, at: 2026-07-28T00:00:00Z }
verified:
  - { by: process:ql-validator, at: 2026-07-28T00:00:00Z }
status: stable
sources:
  - id: source-key
    resource: ../sources/source-key.md
```

Human approval adds a `human:<id>` verification event. Draft, stable, and deprecated states mirror engagement revisions.

### 23.4 Attested computations

Resonance aggregation, audio tuning, hashes, and other deterministic calculations MAY export as OKF Attested Computation concepts referencing the sanctioned executor and attester. OKF records the computation and verification interface; the Epi-Card runtime performs it.

### 23.5 Export variants

The exporter SHALL support:

```text
private-full
shared-collaboration
public-card
```

Each variant is deterministic from a disclosure profile and produces a validation report.

---

## 24. Publication system

### 24.1 Publication targets

The adapter system supports:

```text
YouTube Shorts
TikTok
Instagram Reels where API access is available
static web gallery
object storage/public CDN
manual export package
```

### 24.2 Publication separation

Publication is never implicit in rendering. The workflow is:

```text
prepare metadata
→ render platform derivative
→ verify duration/aspect/audio/caption
→ human approval
→ upload
→ poll remote processing
→ store remote ID/status
```

### 24.3 Metadata

Publication records contain:

```text
platform
account reference
rendition asset
caption/title
tags
privacy/visibility
scheduled time optional
approval ID
remote publication ID
remote status
published_at
```

### 24.4 Retry and idempotency

Upload actions use idempotency keys and resumable provider APIs where available. A network failure SHALL not create duplicate publications without an explicit conflict-resolution action.

---

## 25. Privacy, consent, permissions, and provider disclosure

### 25.1 Permission classes

Actors receive scoped permissions:

```text
read-private
edit-semantic
generate-media
modify-assets
approve-symbol
approve-rendition
export-private
publish
manage-pasu
manage-consent
```

### 25.2 Provider disclosure manifest

Before external generation, `projection.materialize` creates a provider-specific `engagement_projection` naming the provider, model family when known, and purpose. `projection.validate` verifies every included field and asset against Pasu consent, source rights, engagement disclosure, and the selected provider policy.

The external action then creates a `provider_disclosure_manifest` linked to the approved provider projection and action run. It lists every transmitted field path and asset ID, privacy summary, purpose, provider/model, retention expectation, and consent receipt. A provider call cannot begin until the projection and manifest are approved under the active disclosure profile. The used manifest is immutable and remains attached to the provider job.

### 25.3 Public derivation

Public cards and QR targets use an approved `engagement_projection` whose kind is `public`. Its canonical snapshot hash and source-revision manifest are recorded in every web/print/publication rendition. Public routes do not query private semantic tables at render time. A change to approved source data invalidates the projection and requires a new revision, validation, and approval.

### 25.4 Deletion and revocation

A Pasu can revoke provider permission, public publication, or retained media. The runtime records revocation, unpublishes where adapters allow, and marks derived artifacts according to retention policy. Immutable audit records retain non-sensitive event facts while sensitive payloads can be cryptographically erased or removed under the configured policy.

---

## 26. API boundary

### 26.1 Minimal HTTP surface

The harness-neutral service exposes:

```text
POST /v1/actions/{actionName}
GET  /v1/runs/{runId}
POST /v1/runs/{runId}/resume
POST /v1/runs/{runId}/cancel
GET  /v1/engagements/{engagementId}
GET  /v1/engagements/{engagementId}/events
GET  /v1/projections/{projectionId}
GET  /v1/public/cards/{slug}
POST /v1/approvals
GET  /v1/assets/{assetId}
GET  /v1/renditions/{renditionId}
```

The API is an adapter over the same action registry. It does not define an alternate domain model. `GET /projections/{projectionId}` returns an immutable disclosure-scoped snapshot only when the caller is authorised for that projection. `GET /public/cards/{slug}` is the unauthenticated QR/gallery route and resolves only an approved public projection; it never assembles a response from private working tables.

### 26.2 Event stream

Clients MAY subscribe by Server-Sent Events or WebSocket to:

```text
/v1/runs/{runId}/events
/v1/engagements/{engagementId}/events
```

Events include progress, tool calls, external job state, review requests, asset creation, and audit completion.

---

## 27. Validation system

### 27.1 Structural validators

Required validators:

```text
SQL referential integrity
JSON Schema contracts
exact twelve-position QL frame
position and pair relation integrity
source assignment integrity
asset hash verification
render-plan completeness
OKF v0.2 structure and links
public disclosure validation
```

### 27.2 Semantic validators

Required semantic checks:

- Bimba and Pratibimba differ through declared conjugate operations rather than paraphrase alone.
- Every scene atom performs its assigned QL articulation.
- Every pair has a choreography mode.
- Missing source structure remains visible.
- Symbol states preserve family invariants.
- Resonance projections record their profile and inputs.
- Agent decisions have complete QL audits.
- Return carries remainder and next ground.

### 27.3 Media validators

Video:

```text
duration and aspect
frame rate
black/frozen frames
loop seam
symbol alpha and legibility
caption safe area
encoding compatibility
```

Audio:

```text
sample rate and bit depth
ratio tolerance
loudness and true peak
clipping
spectral distribution
loop continuity
```

Print:

```text
finished size and bleed
safe area
image resolution
font outlining/embedding
CMYK profile
QR scanning
```

### 27.4 Human review gates

Human approval is REQUIRED for:

- canonical new symbol or destructive symbol revision;
- final Pasu likeness where a real person is depicted;
- public disclosure of private-derived material;
- final rendition;
- print proof;
- publication.

Other approvals are profile-configurable.

---

## 28. Observability and reproducibility

The runtime SHALL emit structured logs, metrics, and traces for:

```text
action latency and status
provider latency/cost/failure
asset generation and render duration
queue depth
validation failures
approval wait state
publication status
```

Every rendition can be reproduced from:

- frozen engagement revision;
- profile versions;
- action and audit records;
- asset digests;
- provider request/response metadata;
- deterministic modifier and render versions.

Where an external provider cannot reproduce the same generative output, the accepted candidate asset itself is the immutable input to later deterministic steps.

---

## 29. Deployment profiles

### 29.1 Local creator profile

```text
SQLite
local content-addressed files
single worker process
CLI
local web studio
local Remotion/FFmpeg/Faust
provider API keys in local secret store
```

### 29.2 Collaborative single-node profile

```text
PostgreSQL
S3-compatible object store such as MinIO
web studio
worker queue
one or more render workers
reverse proxy and authentication
```

### 29.3 Scaled hosted profile

```text
managed PostgreSQL
managed object storage/CDN
queue and autoscaled workers
separate CPU/GPU worker pools
secret manager
observability backend
backup and point-in-time recovery
```

All profiles use the same action contracts and domain schema.

---

## 30. Repository and module layout

```text
epi-card/
├── apps/
│   ├── studio/
│   ├── gallery/
│   └── worker/
├── packages/
│   ├── domain/
│   ├── database/
│   ├── actions/
│   ├── cli/
│   ├── ql/
│   ├── audit/
│   ├── resonance/
│   ├── correspondences/
│   ├── symbols/
│   ├── assets/
│   ├── audio/
│   ├── providers/
│   │   ├── seedance/
│   │   ├── image/
│   │   ├── transcription/
│   │   └── publication/
│   ├── render-remotion/
│   ├── render-print/
│   ├── card-component/
│   ├── okf-export/
│   ├── packaging/
│   └── validation/
├── dsp/
│   └── ql-resonator.dsp
├── skills/
│   └── epi-card/
├── migrations/
├── profiles/
│   ├── ql/
│   ├── resonance/
│   ├── elemental/
│   ├── chakra/
│   ├── astrology/
│   ├── colour/
│   ├── typography/
│   └── render/
└── tests/
    ├── unit/
    ├── integration/
    ├── golden/
    └── acceptance/
```

### 30.1 Package responsibilities

`domain` owns types and invariants.  
`database` owns migrations and repositories.  
`actions` owns shared operations and job orchestration.  
`ql` owns the twelve-position frame, relations, mapping, and validation.  
`audit` owns nested QL audit ticks and evidence.  
`resonance` owns aggregation and projections.  
`correspondences` owns versioned symbolic mapping profiles.  
`symbols` owns bank, grammar, generation, and canonicalisation.  
`assets` owns content addressing, rights, and derivation.  
`audio` owns the Faust interface, tuning, render, and analysis.  
`providers` own external API adapters.  
`render-remotion` and `render-print` own deterministic output.  
`card-component` owns the front/back runtime and hexagonal interaction.  
`okf-export` owns the wiki artifact set.  
`packaging` owns `.epicard` assembly/import, the normative manifest, path closure, root-digest verification, and offline package round-trip.  
`validation` owns automated conformance.

---

## 31. Development sequence and completion gates

### Phase 1 — Operational QL core

Build:

- database schema and migrations;
- Pasu, session, temporal snapshot, attractor, basin, source forms;
- mandatory twelve-position frame;
- source assignments and occupancy;
- nested twelve-position audit;
- shared actions and CLI;
- Agent Skill.

Gate: an agent can ingest a fivefold source and transcript, map it into the full conjugate form, leave the unsupported position explicit, resume after interruption, and produce a complete audit.

### Phase 2 — Resonance, symbol, and card shell

Build:

- correspondence profiles;
- resonance aggregation/projections;
- symbol bank and SVG grammar;
- twelve symbol states;
- front still/placeholder;
- interactive back hexagon;
- print template and QR;
- public/private projections.

Gate: one complete hand-resolved card works digitally and in print without generated video.

### Phase 3 — QL Resonator

Build:

- Faust instrument;
- two resonator banks;
- twelve audio states;
- offline and browser renderers;
- FFT/CQT/chroma validation;
- audio mixing and loop checks.

Gate: one resonance state deterministically produces the declared audio palette and twelve-state drone with a seamless loop.

### Phase 4 — AI media production

Build:

- provider capability registry;
- Seedance adapter;
- image adapter;
- storyboard/reference pack;
- twelve scene atoms and six pair choreographies;
- modifier stack;
- Remotion/FFmpeg renderer;
- base and extended profiles.

Gate: a 6–12 second loop and a 40–60 second extended film are generated, audited, compositionally exact, and reproducible from accepted plates.

### Phase 5 — Knowledge, packaging, and publication

Build:

- OKF v0.2 exporter;
- `.epicard` package;
- validation reports;
- public gallery;
- publication adapters and approvals;
- return deposition and next-engagement creation.

Gate: a complete engagement can be exported, printed, published, opened offline, read as OKF, and resumed from its return.

---

## 32. Definition of done

The product is complete when all of the following are true:

1. Every engagement has exactly twelve QL positions and the four relation systems defined in §3.
2. A source of arbitrary native arity can be mapped without fabricated completion.
3. Every material agent decision has a full Bimba–Pratibimba QL audit.
4. Pasu, session, temporal, recording, transcript, and activation context are resumable and privacy-scoped.
5. Astrology, element, chakra, semantic, and user inputs converge through versioned resonance contributions rather than untracked prose.
6. The same resonance state projects into inspectable colour, geometry, typography, motion, scene pace, and audio parameters.
7. Symbols are exact SVG families with twelve states and transparent/mask derivatives.
8. The base 6–12 second film and extended 40–60 second film use twelve scene atoms and six reciprocal pair relations.
9. The final film can loop from `P5′` to `P0` while recording an enriched semantic return.
10. The QL Resonator produces a professional, rich, drone/bell palette with spectral verification.
11. The front card plays film and sound with exact symbol overlay/mask.
12. The back hexagon has six individually clickable edges that unfold both conjugate positions.
13. The printed card contains the approved poster frame, symbol, conjugate hexagon, names, and scannable QR.
14. The Agent Skill and CLI can run the complete process in Hermes and any shell-capable harness.
15. The studio and agent invoke one shared action library.
16. The SQL database, content-addressed assets, OKF bundle, and `.epicard` package agree on IDs and hashes.
17. Public exports exclude non-approved private data.
18. Rendering is distinct from publication and publication requires approval.
19. Every frozen rendition identifies the exact engagement revision, profile versions, assets, renderer versions, and audit chain.
20. The return can create the next engagement without flattening the prior loop into simple repetition.

---

## 33. Normative supplements

The following package files make the specification directly actionable:

- `database/postgres.sql`
- `database/sqlite.sql`
- `database/action-definitions.postgres.sql`
- `database/action-definitions.sqlite.sql`
- `contracts/ql-frame.schema.json`
- `contracts/action-envelope.schema.json`
- `contracts/action-payloads.schema.json`
- `contracts/action-registry.yaml`
- `contracts/action-registry.schema.json`
- `contracts/gate-predicates.yaml`
- `contracts/gate-predicates.schema.json`
- `contracts/render-plan.schema.json`
- `contracts/provider-capability.schema.json`
- `contracts/package-manifest.schema.json`
- `scripts/generate-action-registry.py`
- `scripts/generate-action-payloads.py`
- `scripts/validate-spec-package.py`
- `examples/minimal-ql-frame.json`
- `examples/minimal-render-plan.json`
- `examples/action-request.json`
- `examples/seedance-provider-capability.json`
- `examples/minimal-package-manifest.json`
- `architecture/action-catalog.md`
- `architecture/module-contracts.md`
- `architecture/decision-register.md`
- `api/openapi.yaml`
- `skills/epi-card/SKILL.md`
- `ui/epi-card.d.ts`
- `okf/EXPORT_PROFILE.md`
- `acceptance/ACCEPTANCE_TESTS.md`
- `research/CURRENT_TECH_BASIS.md`
- `release/VALIDATION_REPORT.md`
- `release/VALIDATION_REPORT.json`

---

## 34. Canonical recognition

The Epi-Card is one completed Spanda tick made portable. Its Bimba phase gives the attractor an articulated symbolic body; its Pratibimba phase turns that body through evidence, obstruction, hidden pattern, widened context, and achieved work; its symbol compresses the whole without exhausting it; its video moves the twelvefold through time; its drone gives the same ratios a resonant body; its printed form lets the object become quaint, physical, and carried; its OKF set lets the deep structure become a wiki; its audit lets every agent decision be inspected in the same grammar as the thing produced; and its return lets the achieved object become the next ground.

The full product therefore has one coherent operational form:

```text
Pasu + time + session + attractor/basin + sources
                         ↓
                       0/1
                         ↓
          P0→P1→P2→P3→P4→P5
                         ↓ twist
      P0′→P1′→P2′→P3′→P4′→P5′
                         ↓ return
                       P0⁺
                         ↓
 symbol + resonance + film + sound + card + wiki + next tick
```

**End of normative specification.**
