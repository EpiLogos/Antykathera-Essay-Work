# Epi-Card → Open Knowledge Format v0.2 Export Profile

**Profile ID:** `epi-card-okf`  
**Profile version:** `1.0.0`  
**Target format:** OKF `0.2`  
**Authority:** `SPEC.md` §23

## 1. Role and boundary

The OKF bundle is the wiki-like, portable knowledge expression of an Epi-Card engagement. It is generated from a frozen or current SQL revision. It is not used for action/job state, media storage, session authentication, provider resumption, approval enforcement, or relational integrity.

Every export records:

- engagement ID and revision;
- SQL schema version;
- export profile version;
- disclosure profile;
- generated-at timestamp;
- runtime and exporter versions;
- source asset and row digests;
- validation result.

A re-export creates a new bundle asset. It does not mutate an approved prior export.

## 2. Disclosure variants

| Variant | Purpose | Pasu/session content | Recordings/transcripts | Audits | Assets |
|---|---|---|---|---|---|
| `private-full` | Personal archive and full agent handoff | Full permitted snapshot; never raw session key | Full permitted transcripts and private references | Full audit payloads | Private package paths or authorised URIs |
| `shared-collaboration` | Named collaborators | Redacted snapshot chosen by share profile | Approved excerpts/segments | Decision structure and selected evidence; secrets removed | Shared assets and contact-sheet derivatives |
| `public-card` | Public card and QR destination | Public handle or omitted | Public excerpts only | Concise provenance and verification; no private prompts | Approved public renditions and symbol assets |

The exporter applies row- and asset-level disclosure before Markdown generation. Redaction is not a post-processing search-and-replace step.

## 3. Bundle structure

```text
knowledge/
├── index.md
├── log.md
├── engagement.md
├── attractor.md
├── pasu-context.md                    # variant-controlled
├── temporal-context.md                # variant-controlled
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
├── basin/
│   ├── index.md
│   └── <stable-local-key>.md
├── resonance/
│   ├── index.md
│   ├── aggregate.md
│   ├── contributions.md
│   ├── projections.md
│   └── computations/
│       ├── circular-phase.md
│       └── tuning.md
├── symbol/
│   ├── index.md
│   ├── grammar.md
│   ├── relations.md
│   └── states.md
├── film/
│   ├── index.md
│   ├── timeline.md
│   ├── pair-0.md
│   ├── pair-1.md
│   ├── pair-2.md
│   ├── pair-3.md
│   ├── pair-4.md
│   └── pair-5.md
├── audio/
│   ├── index.md
│   ├── palette.md
│   ├── states.md
│   └── analysis.md
├── sources/
│   ├── index.md
│   └── <source-key>.md
├── audit/
│   ├── index.md
│   └── <action-run-id>.md
├── renditions/
│   ├── index.md
│   └── <rendition-id>.md
└── return.md
```

Optional files are omitted cleanly; links to omitted private concepts must not remain in a lower-disclosure bundle.

## 4. Common frontmatter

Every generated concept uses this minimum frontmatter:

```yaml
type: <concept type>
title: <human title>
description: <one-line description>
resource: epicard://engagement/<engagement-id>/<resource-path>
tags: [epi-card, ql, ...]
status: draft | stable | deprecated
generated:
  by: epi-card-runtime/<runtime-version>
  at: <RFC3339 UTC>
  source_revision: <engagement-revision>
  exporter: epi-card-okf/1.0.0
sources: []
```

Use OKF v0.2 trust/lifecycle vocabulary when the data exists:

```yaml
verified:
  - by: process:ql-validator/<version>
    at: <RFC3339 UTC>
  - by: human:<public-or-package-local-actor-id>
    at: <RFC3339 UTC>
stale_after: <YYYY-MM-DD>
```

Rules:

1. `type` is always present.
2. `status` mirrors the source revision: proposed work is `draft`; approved current work is `stable`; superseded work is `deprecated`.
3. `verified` is emitted only from an actual passing validation report or approval. Generation alone is not verification.
4. `stale_after` is emitted only where a concept has temporal validity: astrological/temporal snapshots, provider capability records, publication status, and time-limited activations.
5. Custom keys are namespaced under `epi_card` when they are not part of OKF itself.

```yaml
epi_card:
  engagement_id: <uuid>
  disclosure: private | shared | public
  source_table: ql_position
  source_id: <uuid>
  source_digest: <sha256>
  register: ql_derived
  ql_address: P3
```

## 5. SQL-to-file mapping

| SQL source | File(s) | Body requirements |
|---|---|---|
| `engagement`, `attractor_revision` | `engagement.md` | Status, question, intention, active lens/profile set, revision and links to threshold/QL/return |
| `attractor`, `basin_member` | `attractor.md`, `basin/*.md` | Centre, definition, relation type, weight, register, rationale, evidence and explicit exclusions/unresolved field |
| `pasu_snapshot`, permitted attributes | `pasu-context.md` | Snapshot scope and temporally situated context; never session key/hash |
| `temporal_snapshot` | `temporal-context.md` | Event/observation/local time separated; raw astronomical facts separated from interpretations |
| engagement joins, activation, source set | `threshold.md` | The full `0/1` engagement boundary and disclosure profile |
| `ql_position` | one `ql/*.md` per address | Canonical/local names, occupancy, summaries, articulation, assignments, claims, resonance, media links and conjugate/complement links |
| `ql_relation` | `ql/index.md` | Traversal, six conjugates, complements, 4:2 and 3:3 partitions |
| `resonance_*`, profiles | `resonance/*` | Φ components, contribution rows, profile versions, calculation receipts and medium projections |
| `symbol_*` | `symbol/*` | Semantic operation, invariant grammar, mode, relation bank, twelve states, canonical asset digests |
| `storyboard_revision`, `scene_pair`, `scene_atom` | `film/*` | 6 pairs/12 atoms, timing, reciprocity, intent, accepted plate provenance and render links |
| `audio_palette_revision`, `audio_state` | `audio/*` | Reference Hz and ratio identity separated; instrument/tuning/spatial parameters and twelve states |
| `source_form`, `source_member`, evidence links | `sources/*` | Native arity/form, members, selectors and where each was assigned or deliberately unassigned |
| `audit_tick`, `audit_position`, `action_event` | `audit/*` | Threshold, 12 audit positions, candidates, evidence, outcome, remainder/uncertainty and next ground |
| `rendition`, `rendition_asset` | `renditions/*` | Frozen revisions/profiles/renderers/assets/hashes and approval status |
| `return_deposit` | `return.md` | Self-implication, remainder, achieved work, external implications, next ground, seeds and next engagement link |

## 6. QL position template

```markdown
---
type: Epi-Card QL Position
title: P3 — Logos
description: <short summary>
resource: epicard://engagement/<id>/ql/P3
tags: [epi-card, ql, bimba, p3, logos]
status: stable
generated:
  by: epi-card-runtime/<version>
  at: <time>
  source_revision: <revision>
  exporter: epi-card-okf/1.0.0
verified:
  - by: process:ql-validator/<version>
    at: <time>
sources:
  - id: <source-key>
    resource: ../sources/<source-key>.md
epi_card:
  ql_address: P3
  phase: bimba
  position_index: 3
  occupancy: present
  register: ql_derived
  source_id: <ql-position-id>
  source_digest: <sha256>
---

# P3 — Logos

## Question

Who? Which? Whereby?

## Local articulation

...

## Sources and assignments

...

## Conjugate

[[p3-prime-decision]]

## Complements and partitions

...

## Resonance, symbol, scene, and audio

...
```

## 7. Source references and citations

`source_member`, transcript segments, assets and external references receive stable package-local source keys. A selector is rendered explicitly:

```yaml
sources:
  - id: conversation-segment-07
    resource: ../sources/conversation-segment-07.md
    selector:
      start_ms: 91820
      end_ms: 104110
```

Public exports replace a private source body with an approved excerpt or an existence/provenance stub. They do not expose an inaccessible URI that reveals private identifiers.

## 8. Attested computations

The exporter may create computation concepts for deterministic operations, including:

- circular phase aggregation;
- bounded scalar/vector normalisation;
- rational reduction and audio frequency calculation;
- content hashes;
- render-plan digest;
- spectral/loop validation.

A computation concept records sanctioned inputs, executor/version, parameters, result, receipt asset and attester result. An LLM-generated explanation is not an attestation.

## 9. `index.md` and `log.md`

`index.md` gives the engagement's human-readable entry point and graph of major concepts. `log.md` is chronological and append-derived from approved action events and revisions. The export process sorts events by canonical sequence/time and never fabricates an event omitted from SQL.

## 10. Link validation

The OKF validator must confirm:

1. every internal Markdown link resolves;
2. every required file for the selected variant exists;
3. no link crosses into a higher disclosure class;
4. all source IDs are unique and resolvable;
5. every stable concept has verification or an explicit unverified state;
6. deprecated concepts link to their replacement when known;
7. `resource` URIs are unique in the bundle;
8. source digests match the exported SQL projection or asset;
9. computation receipts and attesters resolve;
10. the bundle root manifest records OKF version `0.2` and profile `epi-card-okf/1.0.0`.

A bundle with an error is not attached to an approved `.epicard` package.
