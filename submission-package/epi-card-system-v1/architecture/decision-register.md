# Epi-Card v1 — Explicit Design Decision Register

**Version:** 1.0.0  
**Normative relation:** this register explains the fixed decisions in `SPEC.md`; it does not override the specification.  

The register exists to prevent an implementation team from mistaking an unstated preference for a requirement or treating a configurable symbolic correspondence as immutable ontology. Each decision states its authority class, adopted behaviour, reason, permitted variation, and change boundary. Mention of a non-adopted option records v1 scope only; it is not a general judgement against that option.

## Decision classes

| Class | Change rule |
|---|---|
| `REQ` — product requirement | Change requires a new product major version. |
| `V1` — fixed v1 implementation | Change requires a versioned decision, migration impact review, and equivalent acceptance evidence. |
| `CFG` — configurable profile | May vary by named versioned profile without changing the product contract. |
| `EXT` — explicit v1 exclusion | May enter only through a later scoped decision; implementers MUST NOT infer it now. |

## Register

| ID | Class | Decision | Product reason | Permitted variation | Change boundary |
|---|---|---|---|---|---|
| `D-001` | `REQ` | Every final engagement has twelve first-class QL addresses, `P0…P5` and `P0′…P5′`. | Bimba and Pratibimba jointly form the proper conjugate body. | Local names, lens content, occupancy, media treatment. | Reducing the canonical frame is a major product change. |
| `D-002` | `REQ` | Traversal is Bimba sixfold, twist, Pratibimba sixfold, enriched return to the next ground. | The object is one complete Spanda tick rather than two unrelated lists. | Timing, interaction order for exploration, visual choreography. | Address/traversal semantics require major version. |
| `D-003` | `REQ` | `P0⁺` is a next-tick role, not a thirteenth stored position. | Return carries semantic delta into a new engagement while preserving the completed one. | A next engagement may be created immediately or only offered as a seed. | Adding a permanent thirteenth address is a major version. |
| `D-004` | `REQ` | The back is a six-edge hexagon whose edges each bind `Pn↔Pn′`. | Six interactive edges express paired conjugacy without flattening the twelvefold. | Edge ordering/orientation and unfolding animation may be profiled. | Replacing edge-pair meaning is a major product change. |
| `D-005` | `REQ` | Film contains twelve scene atoms organised as six reciprocal pairs. | Every QL address receives a temporal/media articulation while the short object remains graspable. | Pair choreography and whether atoms are simultaneous, sequential, masked, or contrapuntal. | Omitting a face from the final film is non-conforming. |
| `D-006` | `REQ` | QL mapping retains missing, latent, unknown, withheld, conflicted, overdetermined, and unassigned states. | QL organises a source without fabricating a cosmetically complete one. | Mapping profile and review tolerance. | Forced completion is prohibited. |
| `D-007` | `REQ` | Every material agent decision has a full twelve-position QL audit. | The generative process must be inspectable in the same conjugate grammar as its product. | Audit-lens wording and nested audit depth. | Six-slot or generic rationale-only audit is non-conforming. |
| `D-008` | `REQ` | Claim/evidence registers remain typed and visible. | Exact identity, derivation, canon, harmonisation, reception, and extension carry different epistemic relations. | New registers may be added through schema/profile evolution. | Collapsing registers is a major semantic change. |
| `D-009` | `REQ` | The universal cross-modal abstraction is a dimensionless resonance state plus versioned modality projections. | Sound, colour, shape, pace, astrology, element, and chakra need a common field without reducing them to one literal physical unit. | Components and profiles may be extended with versioning. | Treating one modality’s unit as universal requires a major redesign. |
| `D-010` | `CFG` | Astrology, elemental, chakral, semantic, and other correspondences are named versioned profiles. | Correspondence content belongs in inspectable canon/configuration rather than hidden prompts. | Any authored profile with sources, register, weights, dates, and approval. | Core runtime does not select one profile as universal. |
| `D-011` | `REQ` | Ratio identity and absolute audio reference frequency are stored separately. | Musical structure must survive transposition/reference changes. | Reference Hz, tuning profile, temperament/projection. | Conflation is invalid. |
| `D-012` | `V1` | Operational truth is relational SQL; production uses PostgreSQL 18+. | Transactions, constraints, concurrency, revisions, audit, jobs, and provider state require a durable operational substrate. | Deployment topology and index tuning. | Engine replacement requires full contract/test parity and migration plan. |
| `D-013` | `REQ` | Portable `.epicard` packages contain SQLite plus content-addressed files. | A complete card must travel and open offline without requiring the hosted service. | Disclosure variant and included rendition set. | Removing offline relational carriage is a major product change. |
| `D-014` | `REQ` | Assets are SHA-256 content-addressed and immutable. | Derivation, deduplication, reproducibility, and package verification depend on stable content identity. | Physical backend and URI scheme. | Mutable canonical asset URLs are non-conforming. |
| `D-015` | `REQ` | The OKF output is a generated wiki artifact set. | The full depth object needs a portable linked knowledge expression for human/agent reading. | Complete, shared, and public export profiles. | OKF does not become operational state. |
| `D-016` | `V1` | OKF export targets v0.2. | v0.2 provides the current provenance/trust/lifecycle/attested-computation basis. | Later export-profile version may coexist. | Upgrade requires explicit migration/compatibility profile. |
| `D-017` | `REQ` | One action implementation serves agent, CLI, studio, HTTP adapter, tests, and permitted card actions. | Divergent surfaces would produce inconsistent permissions, audits, and state. | Surface-specific presentation only. | Duplicated business implementations are prohibited. |
| `D-018` | `V1` | The portable agent boundary is Agent Skills plus the `epicard` CLI. | A small progressively disclosed skill can drive the whole system in shell-capable harnesses. | Additional adapters may call same actions. | Replacing boundary requires equivalent portability. |
| `D-019` | `V1` | Hermes is the first supported harness profile. | It supplies an immediately usable skill/tool/TUI/memory context while leaving state in Epi-Card. | Other harnesses may be added. | Hermes is not canonical state or runtime. |
| `D-020` | `EXT` | MCP is not part of v1. | The skill/CLI/shared-action boundary is sufficient. | None in v1. | Later protocol adapter cannot replace core actions without major decision. |
| `D-021` | `EXT` | The Bimba map is not required for attractor identity or basin storage. | The v1 attractor contract is local and self-contained; external graph identifiers are represented as optional links and do not participate in local identity. | Optional later external links may be attached as ordinary references. | No v1 action/schema may require graph coordinates. |
| `D-022` | `V1` | Seedance 2.0 is the first reference video provider adapter. | Its multimodal short-form and continuation capabilities match the base/extended production workflows. | Any provider can conform through capability registry. | Provider is never semantic/render authority. |
| `D-023` | `REQ` | Provider limits live in versioned capability records. | Models and limits change; completed plans must remain reproducible and new plans must validate before submission. | Provider/model-specific limits. | Hard-coding provider limits into QL is prohibited. |
| `D-024` | `REQ` | Generative video produces plates; final composition is deterministic. | Exact symbols, typography, QR, audio, timing, masks, safe frame, and loop must not depend on probabilistic fidelity. | A future provider may produce more accepted layers, but each remains separately validated. | Generated final-master authority is non-conforming. |
| `D-025` | `V1` | Remotion + FFmpeg are the reference compositor. | They provide typed/programmatic composition and mature media filtering/encoding. | Equivalent renderer may pass same render-plan and acceptance contracts. | Semantic/render-plan contracts remain fixed. |
| `D-026` | `REQ` | Canonical symbols are sanitised SVG families with twelve states. | Symbols must be exact, scalable, printable, bankable, editable, and usable as masks. | Raster candidates and approved exception profiles may inform reconstruction. | Unvalidated opaque raster cannot silently become canonical. |
| `D-027` | `REQ` | Symbol bank is local relational storage, not a required external graph. | The relational symbol-bank contract directly represents reuse, conjugacy, topology, operation, resonance, and return relations. | Later graph export/linking. | External graph dependency is excluded v1. |
| `D-028` | `V1` | The canonical sound engine is a custom Faust QL Resonator. | The system needs deterministic, ratio-exact, automatable browser/offline drone and bell material. | DSP profiles, resonator models, and later DSP major versions. | Proprietary-only canonical render is prohibited. |
| `D-029` | `CFG` | Chromaphone, Kaivo, Surge XT, recorded bells, and other instruments may be used for audition/design/assets. | Professional depth can be discovered or supplied through studio tools while preserving a deployable core. | Any licensed tool/recording. | Rights and reproducibility must be recorded. |
| `D-030` | `REQ` | Sound is a restrained drone/resonance palette with minimal movement rather than a generic score. | The sonic object is an emblematic harmonic field aligned with the card, not background music. | Degree of motion, excitation, decay, partial density by profile. | A composition-heavy score may be an extension, not the canonical default. |
| `D-031` | `REQ` | Base video is 6–12 seconds; extended video is 40–60 seconds. | These are the requested encounter and contemplative forms. | Named additional duration profiles may be added. | Canonical base/extended outputs remain required. |
| `D-032` | `REQ` | Visual media can loop while semantic state advances. | Full Spanda return is recurrence with retained remainder, not a flat GIF repeat. | Loop seam method and return delta. | Empty semantic return is non-conforming. |
| `D-033` | `REQ` | Front face is video/still world plus exact symbol overlay or mask and canonical sound. | The card’s emblem stays structurally exact while the surrounding world moves. | Overlay, cutout, luma/alpha mask, window, matte, rim treatment. | Baked-only symbol is not sufficient. |
| `D-034` | `REQ` | Printed front uses approved poster frame plus symbol; printed back uses conjugate hex, names, return, QR. | The digital object needs a complete quaint physical projection. | Card dimensions/stock through named print profiles. | QR cannot expose private session keys. |
| `D-035` | `V1` | Reference card size is 70×120 mm with 3 mm bleed and 5 mm safe area. | It gives a concrete build/proof target while preserving the long-card character. | Additional print profiles may coexist. | Reference profile remains an acceptance target. |
| `D-036` | `REQ` | Rendering and publication are separate actions; publication is approval-gated. | A finished artefact and an external upload have different permissions and consequences. | Platform-specific approval roles. | Render action must never upload implicitly. |
| `D-037` | `REQ` | Pasu, session, temporal, activation, recording, and transcript context are first-class and disclosure-scoped. | The card is situated and potentially talismanic rather than context-free. | Which fields are present for a given engagement. | Private context cannot leak through public/provider projections. |
| `D-038` | `REQ` | Talismanic intent is operational metadata used by the object and pipeline. | Encounter, cadence, activation, placement, review, and return shape the generated form. | Local activation practices/profile content. | The runtime preserves declared intent as an operational field referenced by activation, rendering, review, and return actions. |
| `D-039` | `REQ` | Every mutable semantic/creative object is revisioned; approved revisions are immutable. | Collaboration, audit, reproducibility, and return require historical identity. | Retention policy and UI presentation. | In-place mutation of approved state is prohibited. |
| `D-040` | `REQ` | Locks apply to explicit semantic/JSON paths and participate in dependency invalidation. | Collaborators must be able to freeze invariants while regenerating variable layers. | Lock ownership, expiry, and review policy. | Model instructions alone are not a lock. |
| `D-041` | `REQ` | Public/private/provider projections are materialised from disclosure rules, not prompt promises. | Privacy must be enforceable before export/provider/publish actions. | Named disclosure profiles. | An agent’s assertion of redaction is insufficient without validated projection. |
| `D-042` | `REQ` | The browser product exposes a framework-neutral `<epi-card>` contract. | Cards must embed in ordinary web environments without making one framework the data format. | Internal implementation may use React/Qwik/Svelte/etc. | Public contract changes require component major version. |
| `D-043` | `REQ` | The studio and agent expose visible, interruptible action progress and review points. | Generative production is a sequence of meaningful operations, not one opaque request. | UI styling and grouping. | Hidden auto-publication or uninspectable material action is prohibited. |
| `D-044` | `REQ` | Acceptance is defined by executable/objective tests, including incomplete mappings and privacy projections. | Build teams need pass/fail evidence rather than interpretive completion claims. | Additional tests and budgets. | Release cannot waive blockers without spec/version change. |
| `D-045` | `REQ` | Action input/output, audit, transaction, retry, provider, and gate behaviour is loaded from the validated 66-action registry and 132 payload schemas; gates use the validated 22-predicate registry. | Runtime behaviour must not be reverse-engineered from table prose or action names. | New action/predicate versions may coexist through explicit registry evolution. | Hand-coded or prose-inferred gate behaviour is non-conforming. |
| `D-046` | `REQ` | Every `.epicard` package uses the normative package manifest contract, complete file closure, and the specified path-sorted SHA-256 root digest. | Offline carriage, import, disclosure verification, and reproducibility require one exact inventory and integrity algorithm rather than exporter-specific conventions. | Included rendition set and disclosure projection remain selectable. | Unlisted files, path aliases, alternate root-digest algorithms, or ad hoc manifests are non-conforming. |
| `D-047` | `REQ` | Package construction uses a non-circular staged sequence; the portable database omits the current package self-record and final archive identity. | A file cannot contain its own final digest without a self-reference cycle. Detached production receipts preserve complete identity without weakening package integrity. | Deterministic ZIP metadata is the reference profile; another container profile must still preserve manifest/root semantics. | Embedding the current package root/archive hash in a root-hashed package file is non-conforming. |

## Configuration authority

The following belong to named profile data and MUST NOT be inferred as fixed universal constants by an implementation team:

- astrological-to-elemental/chakral/QL correspondences;
- elemental/chakral baselines and phase positions;
- colour projection curves and palette constraints;
- absolute reference pitch;
- temperament/tuning and ratio selection beyond the canonical available ratio vocabulary;
- material/resonator choices;
- typography historical/visual qualities;
- camera, lighting, motion, and pair choreography presets;
- Pasu-derived weighting and consent/disclosure rules;
- talismanic activation practice;
- provider capabilities and cost/limit policies;
- media validation thresholds and performance budgets.

Each profile carries stable ID, semantic version, author/authority, evidence/register, effective dates, status, and migration notes.

## Implementation discretion

Teams retain discretion only where the normative documents explicitly leave it, including:

- internal programming language and package implementation, provided action/schema contracts pass;
- UI framework behind `<epi-card>` and the studio;
- object-store vendor;
- queue/worker implementation;
- SQL index/partition tuning;
- cloud/on-prem deployment topology;
- additional provider adapters;
- internal code organisation beneath the required module ownership boundaries.

Discretion does not permit a module to own data assigned to another module, bypass actions, skip audits/approvals, flatten the QL frame, or reinterpret profile content as an implementation constant.

**End of decision register.**
