# Epi-Card v1 — Current Technology and Standards Basis

**Research date:** 28 July 2026  
**Status:** informative implementation basis; `SPEC.md` remains normative  
**Scope:** only technologies that materially determine the v1 action, skill, media, knowledge-export, storage, audio, and rendering design.

This document distinguishes what an external technology currently supports from what Epi-Card chooses to do with it. A cited capability does not transfer architectural authority to that technology. Provider and framework details are pinned in the `provider_capability`, action-definition, and projection-profile registries so that later changes do not silently alter completed engagements.

---

## 1. Builder.io / Steve Sewell — agent-native shared actions

**Primary source:** Steve Sewell, “Agent Native Apps,” Builder.io, 21 April 2026.  
**Source URL:** https://www.builder.io/blog/agent-native-apps

### Current source-supported points

Builder’s agent-native architecture centres on two elements: tools/actions that expose application capabilities and an agent loop that selects and invokes them. The article’s practical architectural move is to make an application action available to both the ordinary product UI and the agent rather than creating a second, divergent agent-only implementation.

### Epi-Card consequence

Epi-Card adopts **one shared action definition** for CLI, studio, agent skill, HTTP adapter, tests, and permitted public interactions. The action implementation—not a prompt—owns schema validation, permissions, transactional writes, provider submission, content hashing, approvals, and terminal success.

### What this source does not decide

It does not require Epi-Card to use Builder’s runtime, frontend, storage model, or agent framework. Epi-Card adopts the shared-action pattern while retaining its own SQL model, QL audit, CLI, skill, renderer, and UI.

---

## 2. Agent Skills — portable skill boundary

**Primary sources:** Agent Skills overview and specification.  
**Source URLs:**

- https://agentskills.io/
- https://agentskills.io/specification

### Current source-supported points

The Agent Skills format uses a skill directory with a required `SKILL.md` and optional scripts, references, and assets. It is designed for progressive disclosure: a harness can discover a concise skill description and load deeper resources only when the task requires them.

### Epi-Card consequence

The canonical agent-facing package is:

```text
skills/epi-card/
├── SKILL.md
├── scripts/run-epicard
├── references/
└── assets/
```

`SKILL.md` explains when to use Epi-Card, the invariant `6+6′` frame, required review stops, privacy rules, and the action sequence. The skill invokes the `epicard` CLI; it does not duplicate domain logic in prompt prose.

### What this source does not decide

It does not define the Epi-Card database, QL semantics, action catalogue, audit, UI, or media pipeline. Those remain product-owned.

---

## 3. Hermes Agent — first supported harness profile

**Primary source:** Nous Research, `hermes-agent` official repository and documentation.  
**Source URLs:**

- https://github.com/NousResearch/hermes-agent
- https://hermes-agent.nousresearch.com/docs/user-guide/tui/

### Current source-supported points

Hermes provides a terminal interface, messaging surfaces, persistent memory/session facilities, voice-memo transcription paths, tool execution, and Agent Skills compatibility. These capabilities make it a practical first harness for a skill-driven CLI workflow.

### Epi-Card consequence

Hermes is the first conformance profile for agent operation:

```text
Hermes discovers Epi-Card skill
       ↓
agent invokes epicard CLI/actions
       ↓
canonical state persists in Epi-Card SQL/assets
       ↓
Hermes may retain auxiliary conversational memory
```

Canonical Pasu, session, engagement, audit, and media state remain in Epi-Card storage so the work can resume in another harness.

### What this source does not decide

Hermes does not become the canonical runtime, database, session ontology, or user interface. No Epi-Card record may depend on an opaque Hermes-only memory to be complete.

---

## 4. Open Knowledge Format v0.2 — wiki artifact export

**Primary source:** Google Cloud, “Open Knowledge Format v0.2,” published 24 July 2026.  
**Source URLs:**

- https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf

### Current source-supported points

OKF v0.2 is a file-based knowledge format built around Markdown, YAML frontmatter, links, provenance, trust/freshness/lifecycle metadata, and attested computation. It is intended to make knowledge portable and legible to humans and agents without requiring one database or runtime.

### Epi-Card consequence

Epi-Card exports the deep constellation as a wiki artifact set containing:

- threshold and return pages;
- twelve QL position pages;
- six conjugate-pair pages;
- attractor/basin and Pasu-safe context;
- source/provenance pages;
- resonance calculations and attestations;
- symbol, scene, audio, rendition, and audit pages;
- chronological/lifecycle logs.

The operational source of truth remains SQL and content-addressed media. OKF is a generated, portable knowledge expression with complete/private, shared, and public disclosure variants.

### What this source does not decide

OKF is not used as a transactional store, job queue, provider-state store, media registry, lock manager, permission system, or render database. Manual edits to an exported OKF set become new source material or an explicit import revision; they never silently overwrite operational truth.

---

## 5. Seedance 2.0 — reference multimodal video provider

**Primary sources:** ByteDance Seed official Seedance 2.0 launch and product materials, 12 February 2026 onward.  
**Source URLs:**

- https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0
- https://seed.bytedance.com/en/seedance2_0

### Current source-supported points

Seedance 2.0 supports multimodal text, image, video, and audio conditioning; official launch material describes multiple image/video/audio references, native audio-video generation, multi-shot generation, editing, and continuation, with a generation window suitable for short clips.

### Epi-Card consequence

Seedance 2.0 is the **reference first provider adapter** for generated world plates and moving material. Its capability record is versioned and validated before job submission. The base 6–12 second card may be produced as:

1. one multi-shot request;
2. six reciprocal pair requests;
3. separate Bimba and Pratibimba passes;
4. a hybrid of generated stills, edits, and continuation.

Generated output remains a plate. Exact symbol geometry, typography, QR, QL timing, canonical drone, masks, and final loop are applied by deterministic composition.

### What this source does not decide

Seedance does not own the semantic frame, storyboard truth, exact symbol, final sound, card UI, or master rendition. Stated provider limits are never hard-coded into QL; they live in versioned capability records so a later provider/model can use a different allocation.

---

## 6. Remotion and FFmpeg — deterministic finishing

**Primary sources:** Remotion transparent-video and composition documentation; FFmpeg project documentation.  
**Source URLs:**

- https://www.remotion.dev/docs/transparent-videos
- https://www.remotion.dev/docs/artifacts
- https://ffmpeg.org/documentation.html

### Current source-supported points

Remotion renders programmatic video compositions from React/TypeScript and supports transparent WebM workflows when an alpha-capable codec/pixel format is selected. It can also emit supplementary render artifacts. FFmpeg provides the underlying media transforms, masks, overlays, audio mixing, filters, inspection, and encoding required for deterministic finishing.

### Epi-Card consequence

The reference renderer uses:

```text
approved render plan
      ↓
Remotion composition graph
      ↓
FFmpeg masks/filters/mix/encode/inspection
      ↓
content-addressed renditions and reports
```

Generated plates never receive authority over exact SVG, typography, QR, captions, safe areas, canonical audio, or frame-accurate loop timing.

### What these sources do not decide

React/Remotion is not the data format, semantic runtime, or public component requirement. Another renderer may conform if it consumes the same render-plan contract and passes equivalent deterministic acceptance tests.

---

## 7. Faust — canonical QL Resonator implementation

**Primary sources:** Faust language and official physical-modelling library documentation.  
**Source URLs:**

- https://faust.grame.fr/
- https://faustlibraries.grame.fr/libs/physmodels/

### Current source-supported points

Faust is a functional DSP language that can compile a single signal-processing definition to multiple native, plugin, WebAudio, and offline targets. Its official physical-modelling library includes waveguide, mass-spring, string, membrane, bar, modal percussion, and resonant-system building blocks.

### Epi-Card consequence

The canonical instrument is a custom Faust QL Resonator with:

- ratio-exact drone oscillator/body;
- coupled Bimba and Pratibimba resonator banks;
- modal bell/plate/bar/bowl material;
- excitation, strike position, body size, damping, inharmonic spread, and tail controls;
- address-specific twelve-state automation;
- offline master rendering and browser playback from the same DSP version.

The source DSP and exact parameter state are part of rendition provenance.

### What this source does not decide

Faust supplies implementation capability; it does not define the QL ratios, elemental/chakral correspondence, or artistic values. Those come from Epi-Logos profiles and audited engagement state.

---

## 8. Professional physical-modelling instruments — reference and audition layer

### 8.1 AAS Chromaphone 3

**Source URL:** https://www.applied-acoustics.com/chromaphone-3/manual/

Chromaphone 3 provides physically modelled resonators such as plates, bars, membranes, strings, tubes, and drumhead-like bodies, with coupled resonator design. It is the strongest immediate studio instrument for discovering the material register of the QL bell/drone palette.

### 8.2 Madrona Labs Kaivo

**Source URL:** https://madronalabs.com/products/kaivo

Kaivo combines granular excitation with physical modelling and two-dimensional vibrating bodies. It is useful for liminal, organic, slowly evolving material and spatial exploration.

### 8.3 Surge XT

**Source URL:** https://surge-synthesizer.github.io/manual-xt/

Surge XT supports microtuning workflows including Scala `SCL/KBM`, MTS-ESP, and internal tuning tools. It is useful for auditioning exact ratio-derived or custom pitch structures before they are encoded in the canonical Faust instrument.

### Epi-Card consequence

These instruments are human sound-design references and optional studio tools. Their presets/renders can be used when licensing and automation permit, but the server/browser canonical render cannot depend on a proprietary plugin that is unavailable in the target environment. Approved discoveries are translated into versioned QL Resonator profiles or licensed audio assets.

---

## 9. PostgreSQL 18 and SQLite — operational and portable stores

**Primary sources:** PostgreSQL 18 release and UUID documentation; SQLite documentation.  
**Source URLs:**

- https://www.postgresql.org/docs/18/functions-uuid.html
- https://www.postgresql.org/about/news/postgresql-18-released-3142/
- https://www.sqlite.org/docs.html

### Current source-supported points

PostgreSQL 18 provides core UUIDv7 generation through `uuidv7()`, alongside mature transactional, constraint, indexing, JSON, and concurrency facilities. SQLite provides a self-contained relational database suitable for portable/offline packages.

### Epi-Card consequence

- Production profile requires PostgreSQL 18 or later and uses UUIDv7 for locality/time-sortable operational identifiers.
- Portable profile uses SQLite 3.45 or later; UUIDv7 values are generated by the application and stored as canonical text.
- Media remain content-addressed files rather than large opaque database blobs.
- Logical semantic IDs, revisions, and hashes round-trip between the two profiles.

### What these sources do not decide

The database engines do not define Epi-Card ontology, QL mapping, or package disclosure. The DDL and action library do.

---

## 10. Technology selection table

| Product concern | v1 implementation | Binding level | Replaceable through |
|---|---|---|---|
| Agent operation | Agent Skills + `epicard` CLI | Fixed v1 boundary | New skill/CLI-compatible harness profile |
| First harness | Hermes | Supported profile | Additional harness profile; no semantic change |
| Shared capabilities | One action library | Product requirement | Only versioned action-major redesign |
| Operational store | PostgreSQL 18+ | Fixed v1 implementation | Major storage adapter preserving contracts/tests |
| Portable store | SQLite 3.45+ | Product requirement for `.epicard` | Compatible portable relational adapter only in later major version |
| Wiki artifact | OKF v0.2 | Fixed v1 export | Versioned export profile |
| Video provider | Seedance 2.0 reference adapter | Provider profile | Capability adapter registry |
| Final video | Remotion + FFmpeg | Reference implementation | Equivalent render-plan consumer passing tests |
| Canonical audio | Faust QL Resonator | Fixed v1 implementation | DSP-major revision preserving parameter/provenance contract |
| Sound audition | Chromaphone, Kaivo, Surge XT | Optional studio tooling | Any licensed instrument/reference |
| Browser card | Custom element contract | Product requirement | Internal framework change preserving `epi-card.d.ts` |

---

## 11. Explicit non-selections

The following are not part of v1:

- MCP;
- Bimba-map identity or graph dependency;
- JSON-LD as the primary store;
- OKF as a database or task runtime;
- a provider-generated final symbol, title, QR, or canonical audio layer;
- a six-position-only final engagement;
- a harness-specific memory as canonical engagement state.

These are scope boundaries, not general judgements about the excluded technologies.

---

## 12. Refresh policy

Before a minor or major implementation release, maintainers SHALL review:

1. Agent Skills specification changes;
2. Hermes skill/CLI/tool compatibility;
3. OKF version and migration guidance;
4. Seedance and all advertised provider capability/terms changes;
5. Remotion/FFmpeg alpha, codec, and renderer changes;
6. Faust target and physical-model library changes;
7. PostgreSQL/SQLite supported versions;
8. commercial instrument licensing relevant to automated renders.

A changed external capability produces a new provider/profile/adapter version. It never retroactively changes an approved engagement or rendition.

**End of current technology basis.**
