# Epi-Card QL Conjugate System — Acceptance Test Specification

**Version:** 1.0.0  
**Normative relation:** implements `SPEC.md` §§3–32.  
**Purpose:** define objective pass/fail evidence for a complete v1 build.  

This document is not a sample QA checklist. Every test marked **Release blocker** is required for conformance. Tests may be automated, instrumented, or performed through a recorded human review, but every result MUST produce a `validation_report`, immutable evidence, implementation version, execution timestamp, and actor or service identity.

## 0. Test conventions

### 0.1 Test environments

| Code | Environment | Required implementation |
|---|---|---|
| `PG` | Production relational profile | PostgreSQL 18 or later, object store, worker, renderer |
| `SQ` | Portable/offline profile | SQLite 3.45 or later, package-local asset tree |
| `WEB` | Browser product | Current Chromium, Firefox, and Safari release families |
| `CLI` | Shell action boundary | POSIX shell plus `epicard` executable |
| `HERMES` | First harness profile | Hermes with the Epi-Card Agent Skill installed |
| `MEDIA` | Production media host | FFmpeg, Remotion renderer, Faust offline renderer |
| `PRINT` | Print proof workflow | PDF/X-capable proof or rasterised inspection at 300 dpi |

### 0.2 Result states

```text
pass
fail
blocked
not_applicable
```

`not_applicable` is valid only for optional provider-specific tests. It is never valid for a release blocker.

### 0.3 Evidence requirements

Every result MUST record:

```text
test_id
specification_version
implementation_commit
schema_revision
profile_versions
started_at
completed_at
environment
input_fixture_ids
observed_values
expected_values
artifact_refs
log_refs
actor_id
result
finding_ids
```

### 0.4 Standard fixtures

The release suite SHALL include these canonical fixtures:

| Fixture | Definition |
|---|---|
| `FX-EMPTY` | New engagement with no mapped source content |
| `FX-5` | Five-member source form with one intentionally unsupported QL location |
| `FX-6` | Six-member source form capable of a complete Bimba mapping but not automatically a complete conjugate reading |
| `FX-7` | Seven-member source form requiring condensation, distribution, or unassigned remainder |
| `FX-12` | Twelve-member source form with explicit Bimba–Pratibimba assignments |
| `FX-CONFLICT` | Sources that support contradictory assignments and claims |
| `FX-WITHHELD` | One private source member excluded from provider and public disclosure |
| `FX-REC` | Two-speaker recording with timed transcript, redaction, and consent boundaries |
| `FX-ASTRO` | Fixed astronomical facts plus two versioned interpretive correspondence profiles |
| `FX-SYMBOL` | Approved SVG symbol family with twelve states and loop anchors |
| `FX-VIDEO` | Six accepted reciprocal plate pairs with known frame timing |
| `FX-AUDIO` | Ratio-exact twelve-state QL Resonator palette with known analysis targets |
| `FX-PUBLIC` | Approved public disclosure profile and public URL |
| `FX-PRIVATE` | Private Pasu attributes, recording, and non-exportable source excerpts |
| `FX-RETURN` | Engagement whose `P5′→P0⁺` return seeds a second engagement |

---

## 1. Build, schema, and migration acceptance

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `BLD-001` | Release blocker | `PG` | Apply `database/postgres.sql` to an empty PostgreSQL 18 database. | Script completes in one controlled migration; all objects are created; no unresolved dependency or syntax error occurs. |
| `BLD-002` | Release blocker | `SQ` | Execute `database/sqlite.sql` against an empty SQLite database. | Script completes; 12 canonical QL rows, 12 canonical audit rows, four validation views, the action gate evaluation table, and one schema revision exist. |
| `BLD-003` | Release blocker | `PG`,`SQ` | Compare logical table inventory and required columns. | Every portable semantic record has a SQLite representation; documented production-only operational columns are the only permitted differences. |
| `BLD-004` | Release blocker | `PG`,`SQ` | Apply the same initial schema twice. | Second invocation fails safely or is explicitly migration-runner guarded; it does not duplicate canonical seeds or corrupt state. |
| `BLD-005` | Release blocker | all | Validate every JSON Schema with a Draft 2020-12 meta-schema validator. | All schemas are valid; all external references resolve within the package. |
| `BLD-006` | Release blocker | all | Parse `api/openapi.yaml` as OpenAPI 3.1 and resolve local schema references. | Parse succeeds; every operation has an action name, request schema, response schema, security declaration, and error response. |
| `BLD-007` | Release blocker | `CLI` | Parse `skills/epi-card/SKILL.md` frontmatter and check referenced files. | Name, description, and all referenced scripts/references resolve; no missing resource exists. |
| `BLD-008` | Release blocker | `CLI` | Run shell syntax validation on `skills/epi-card/scripts/run-epicard`. | Wrapper is syntactically valid, executable, and propagates the CLI exit code. |
| `BLD-009` | Release blocker | all | Search normative source files for placeholder hashes, TODO markers, zero-width characters, and unresolved sample domains. | No release-blocking placeholder remains; any example value is explicitly marked fixture/example. |
| `BLD-010` | Release blocker | all | Compare action names in `SPEC.md`, action catalogue, CLI help, HTTP boundary, and runtime registry. | Stable action names match exactly; no surface exposes an undeclared mutating action. |
| `BLD-011` | Release blocker | all | Create a schema revision whose hash equals the packaged normative `SPEC.md`. | Stored SHA-256 equals the file digest and is included in package manifest. |
| `BLD-012` | Release blocker | all | Build all workspace packages from a clean checkout with lockfile enforcement. | Build succeeds without network-fetched unpinned code at runtime; generated types are current. |
| `BLD-013` | Release blocker | all | Validate `contracts/action-registry.yaml` against `contracts/action-registry.schema.json`; compare action names with the catalogue. | Exactly 66 unique actions validate; side effects contain no Markdown syntax; catalogue and registry name/order sets are identical. |
| `BLD-014` | Release blocker | all | Validate `contracts/gate-predicates.yaml` against its schema and resolve every action gate predicate. | Exactly 22 unique predicates validate; every `when` and `requires` call names a registered predicate and its arguments validate against that predicate’s argument schema. |
| `BLD-015` | Release blocker | `PG`,`SQ` | Regenerate the action registry/seeds, apply base schema then generated seed, and query `action_definition`. | Generated files are byte-identical to packaged files; 66 definitions load; `gate_mode`, JSON gate policy, audit flag, transaction class, provider dependencies, and retry policy match the registry. |
| `BLD-016` | Release blocker | all | Exercise at least one gate at each stage (`pre_execute`, `pre_commit`, `pre_promote`, `pre_publish`) in pass and fail states. | The named predicate produces the specified failure code; no action advances beyond its blocked stage; successful candidate creation remains possible for `pre_promote` gates. |
| `BLD-017` | Release blocker | all | Validate `contracts/action-payloads.schema.json`; resolve every input/output ref from the action registry; generate one valid and one invalid payload fixture for every action. | Exactly 66 input and 66 output schemas resolve; all valid fixtures pass; every invalid fixture fails at the intended path; envelope/payload session and engagement mismatches return `CONTEXT_ID_MISMATCH`. |
| `BLD-018` | Release blocker | all | Compare canonical QL address enums, SQL seeds/generated columns, examples, render contract, UI declarations, OKF exporter, and action payloads. | Every canonical Pratibimba identifier uses Unicode PRIME `U+2032`; ASCII-apostrophe and provider transport aliases cannot enter canonical state. |
| `BLD-019` | Release blocker | all | Validate `contracts/package-manifest.schema.json` and its reference instance. | Schema is valid Draft 2020-12; fixture passes schema and cross-field root-digest/entrypoint/rendition checks. |
| `BLD-020` | Release blocker | `WEB` | Compile `ui/epi-card.d.ts` under strict TypeScript with DOM and ES2022 libraries. | Declaration compiles without error and exposes the complete public custom-element state/event/action contract. |

---

## 2. Pasu, consent, session, and temporal context

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `CTX-001` | Release blocker | `PG`,`SQ` | Execute `pasu.create` for human, collective, anonymous, and custom kinds. | Stable Pasu records are created without forcing person-only fields. |
| `CTX-002` | Release blocker | `PG` | Store private and public `pasu_attribute` rows with validity windows. | Query at a given engagement time returns only temporally valid attributes and respects privacy class. |
| `CTX-003` | Release blocker | all | Execute `pasu.snapshot` with private, provider-safe, shared, and public disclosure profiles. | Each immutable snapshot includes only permitted fields and records included/redacted attribute IDs. |
| `CTX-004` | Release blocker | `CLI` | Execute `session.open`. | UUIDv7 session is returned with one-time 256-bit raw key; database stores only a cryptographic hash. |
| `CTX-005` | Release blocker | `CLI` | Re-request or inspect a session after opening. | Raw session key cannot be retrieved from SQL, logs, API responses, package, or audit. |
| `CTX-006` | Release blocker | all | Resume by valid and invalid session keys. | Valid key resolves correct session; invalid key fails with auth error and creates no new session. |
| `CTX-007` | Release blocker | all | Link a child session and continuation session to one engagement. | Lineage and engagement joins are retained without merging session identities. |
| `CTX-008` | Release blocker | all | Capture a temporal snapshot with event time distinct from observation time. | Both times, local time, timezone, location precision, provider, and profile versions remain distinct. |
| `CTX-009` | Release blocker | all | Use `FX-ASTRO`; reinterpret the same facts under profile B. | Raw astronomical facts retain identity; a new interpretive contribution set is created without mutating facts. |
| `CTX-010` | Release blocker | all | Create talismanic activation with review/return conditions and private phrase reference. | Activation metadata is stored, privacy-scoped, and available to permitted resonance/scene actions. |
| `CTX-011` | Release blocker | all | Attempt provider submission containing a non-provider-safe Pasu attribute. | Submission is blocked before network call and finding names the offending attribute/disclosure policy. |
| `CTX-012` | Release blocker | all | Export or publish a card containing `FX-PRIVATE`. | Session key, private phrase, raw birth/location precision, private attributes, and unapproved transcript content are absent. |
| `CTX-013` | Release blocker | all | Execute `projection.materialize` for private, shared, public, and provider targets. | Four immutable snapshots have distinct disclosure scopes, source revision manifests, hashes, and target metadata. |
| `CTX-014` | Release blocker | all | Validate a provider projection containing a prohibited field and asset. | `projection.validate` fails before any provider job; findings name exact field path/asset and consent/profile rule. |
| `CTX-015` | Release blocker | all | Use an approved provider projection in an external action. | One immutable `provider_disclosure_manifest` links projection, action run, provider/model/purpose, exact transmitted paths/assets, retention expectation, and consent receipt. |
| `CTX-016` | Release blocker | all | Change source revision after public projection approval. | Existing projection becomes stale/superseded for new renders; public route continues serving the frozen approved snapshot until a replacement is approved. |

---

## 3. Attractor, basin, source forms, recordings, and evidence

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `SRC-001` | Release blocker | all | Create attractors of concept, person, event, relation, dream, and custom kinds. | All receive local identities with no Bimba-map or external-graph dependency. |
| `SRC-002` | Release blocker | all | Resolve basin for a fixture containing essential, constitutive, contextual, resonant, counterpole, boundary, excluded, and unresolved members. | Every member has type, weight, register, rationale, evidence, and revision identity. |
| `SRC-003` | Release blocker | all | Approve basin revision, then revise an exclusion. | Immutable new revision is created; approved prior revision remains queryable. |
| `SRC-004` | Release blocker | all | Ingest arity 0, 2, 5, 6, 7, and 12 source forms. | Native arity and every native member are retained before QL mapping. |
| `SRC-005` | Release blocker | all | Ingest two identical files. | One content-addressed asset is reused; both source relations remain distinct. |
| `SRC-006` | Release blocker | all | Ingest file with changed bytes but same filename. | New asset identity is created from content hash; filename does not determine identity. |
| `SRC-007` | Release blocker | all | Ingest `FX-REC` recording with consent state. | Recording is rejected without consent state; accepted record retains asset, speakers, privacy, and session/engagement relation. |
| `SRC-008` | Release blocker | all | Transcribe `FX-REC`. | Timed diarised segments, provider/model/version, confidence, digest, and redaction fields are present. |
| `SRC-009` | Release blocker | all | Link a 2.4-second transcript range to basin member, QL position, scene atom, and audit position. | Four typed evidence links resolve and preserve the exact selector. |
| `SRC-010` | Release blocker | all | Redact one transcript segment after it was used as evidence. | Private operational link remains auditable; public projection removes content and displays permitted redaction/provenance state. |
| `SRC-011` | Release blocker | all | Attempt evidence link to an unsupported target kind. | Action fails validation and creates no orphan link. |
| `SRC-012` | Release blocker | all | Remove a source from an unapproved engagement. | Source relation may be removed through versioned change; immutable asset/provenance record and prior audit remain. |

---

## 4. Canonical twelve-position QL frame

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `QLF-001` | Release blocker | all | Execute `ql.initialize` on a new engagement. | Exactly `P0,P1,P2,P3,P4,P5,P0′,P1′,P2′,P3′,P4′,P5′` exist once each. |
| `QLF-002` | Release blocker | all | Inspect traversal relations. | Six Bimba/Night adjacencies, one `P5→P0′` twist, and one `P5′→P0⁺` return definition are present as specified. |
| `QLF-003` | Release blocker | all | Inspect conjugate relations. | Six and only six `Pn↔Pn′` pairs resolve. |
| `QLF-004` | Release blocker | all | Inspect complement relations. | `0↔5`, `1↔4`, `2↔3` exist independently for both phases. |
| `QLF-005` | Release blocker | all | Inspect `4:2` and `3:3` partitions. | Every canonical address has the correct partition membership and no duplicate/conflicting membership. |
| `QLF-006` | Release blocker | all | Validate `contracts/ql-frame.schema.json` with a conforming fixture. | Fixture passes. |
| `QLF-007` | Release blocker | all | Remove one primed position and validate. | Validation fails and explicitly identifies the missing address. |
| `QLF-008` | Release blocker | all | Add a thirteenth stored `P0⁺` position. | Database/contract rejects it; return remains a transition to a next engagement. |
| `QLF-009` | Release blocker | all | Map `FX-5`. | Twelve structural addresses remain; unsupported articulation is `missing` or `unknown` with reason; no invented claim is present. |
| `QLF-010` | Release blocker | all | Map `FX-7`. | All source members are direct/distributed/condensed/supporting/counterposed/unassigned; none silently disappears. |
| `QLF-011` | Release blocker | all | Map `FX-CONFLICT`. | Conflicting claims are retained with `conflicted` occupancy or explicit claim relation; system does not collapse them without audit. |
| `QLF-012` | Release blocker | all | Mark one position `withheld`. | Position remains structurally present while content is excluded from disallowed projections. |
| `QLF-013` | Release blocker | all | Create multiple strong assignments at one position. | Position is marked `overdetermined` or explicitly resolved through approved reconciliation; assignments remain inspectable. |
| `QLF-014` | Release blocker | all | Run conjugate reconciliation. | Each pair reports relation, agreement/difference, evidence asymmetry, and unresolved remainder. |
| `QLF-015` | Release blocker | all | Run complement reconciliation. | Both phase-local complement systems are evaluated without substituting conjugate pairing. |
| `QLF-016` | Release blocker | all | Approve a frame with a blocking structural finding. | Approval is rejected. |
| `QLF-017` | Release blocker | all | Approve a structurally valid but intentionally incomplete frame. | Approval succeeds only when incompleteness is explicitly registered, evidenced, and accepted by the review profile. |
| `QLF-018` | Release blocker | all | Deposit `FX-RETURN`. | Return stores self-implication, remainder, achieved work, next ground, seeds, semantic/media deltas, and a non-self next-engagement link. |
| `QLF-019` | Release blocker | all | Freeze a proposed QL mapping. | Immutable `ql_frame_revision` contains complete threshold/frame/relations/assignments/claims/profile set/return proposal and canonical hash. |
| `QLF-020` | Release blocker | all | Approve a frame revision and select it on the engagement. | Selected revision belongs to engagement, is `approved`, has approval actor/time, and passes validation. |
| `QLF-021` | Release blocker | all | Attempt to edit or delete approved/superseded frame content. | Database/action rejects mutation; a new revision with prior-revision link is required. |
| `QLF-022` | Release blocker | all | Modify active working QL rows after frame approval. | Approved revision remains byte-equivalent; engagement becomes dirty/stale until a new proposed/approved revision is frozen. |

---

## 5. Claim registers and semantic evidence

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `CLM-001` | Release blocker | all | Create claims in all six registers. | `exact_identity`, `ql_derived`, `canonical_symbolic`, `cross_register`, `archetypal_reception`, and `open_extension` are preserved as distinct values. |
| `CLM-002` | Release blocker | all | Submit claim without register. | Action fails. |
| `CLM-003` | Release blocker | all | Submit `exact_identity` claim without exact evidence/receipt. | Semantic validation blocks approval. |
| `CLM-004` | Release blocker | all | Submit `open_extension` with rationale but no source claim. | Claim is permitted and visibly marked as extension rather than canon or derivation. |
| `CLM-005` | Release blocker | all | Change a claim register after approval. | Immutable claim revision or superseding claim is created; original remains in audit. |
| `CLM-006` | Release blocker | all | Export public OKF and card details. | Claim register is present wherever the claim is displayed or cited. |
| `CLM-007` | Release blocker | all | Follow an evidence link from rendered detail to source selector. | Selector resolves to exact document fragment, transcript range, media range, region, row, or structured input. |
| `CLM-008` | Release blocker | all | Delete/revoke source permission. | Public claim presentation is withdrawn or redacted according to policy while historical internal derivation remains access-controlled. |

---

## 6. Resonance-frequency and correspondence profiles

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `RES-001` | Release blocker | all | Resolve a state with components `θ,ρ,τ,a,c,β,p,R,E,C`. | Every component is validated, units/profile are explicit, and calculation receipt exists. |
| `RES-002` | Release blocker | all | Aggregate phases `0.99` and `0.01` with equal weights. | Circular result is near `0/1`, not `0.5`. |
| `RES-003` | Release blocker | all | Aggregate scalar/vector contributions with zero and non-zero weights. | Result equals documented weighted formula; zero-weight contribution remains in provenance but does not alter output. |
| `RES-004` | Release blocker | all | Use `FX-ASTRO` with two interpretation profiles. | Same facts yield two versioned, reproducible contribution sets; neither is treated as raw astronomical fact. |
| `RES-005` | Release blocker | all | Add elemental, chakral, semantic, Pasu, temporal, and source-form contributions. | Each contribution states source system/feature, vector, weight, register, rationale, profile/version, and evidence. |
| `RES-006` | Release blocker | all | Add an unregistered correspondence mapping. | Resolution rejects it or stores it as a new review-gated `open_extension` profile revision. |
| `RES-007` | Release blocker | all | Resolve global and twelve position-specific states. | One aggregate engagement state and exactly twelve address states are stored. |
| `RES-008` | Release blocker | all | Project one state to colour, geometry, typography, motion, pace, lighting, and audio. | All projected parameter sets reference same source state and named profile versions; each includes calculation receipt. |
| `RES-009` | Release blocker | all | Repeat deterministic projection. | Parameter values and canonical JSON digest are identical. |
| `RES-010` | Release blocker | all | Change projection profile version without changing state. | New parameter-set revision is produced; original remains reproducible. |
| `RES-011` | Release blocker | all | Compare Bimba and Pratibimba state pairs. | Signed polarity, phase, ratios, and component deltas are represented without naïve linear phase subtraction. |
| `RES-012` | Release blocker | all | Attempt to store colour wavelength or audio Hz as universal frequency identity without profile. | Validation rejects unqualified cross-modal identity. |
| `RES-013` | Release blocker | all | Resolve audio reference frequency and ratios. | Ratio identity and absolute reference Hz are separate fields with separate provenance. |
| `RES-014` | Release blocker | all | Export resonance calculations to OKF. | Inputs, profile versions, formula/receipt, outputs, and attestation hashes are present. |
| `RES-015` | Release blocker | `PG`,`SQ` | Activate configuration, correspondence, projection, provider-capability, and profile-set fixtures, then attempt body/member mutation. | Mutation is rejected; allowed status deprecation/retirement remains append-only; changed content requires a new version/hash. |

---

## 7. QL audit of agent decisions

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `AUD-001` | Release blocker | all | Run a material generate/write/render action. | One `audit_tick` is created with threshold, twelve positions, outcome, remainder, and next ground. |
| `AUD-002` | Release blocker | all | Inspect Bimba audit positions. | Target, prediction, difference/energy, correction/gradient, lens weighting, and verifier anchor are present under their canonical address mapping. |
| `AUD-003` | Release blocker | all | Inspect Pratibimba audit positions. | Conjugate target, inverse/counter prediction, recognition difference, inverse correction, reweighting, and renewed verifier are present. |
| `AUD-004` | Release blocker | all | Complete action with only six audit positions. | Action cannot become `succeeded`. |
| `AUD-005` | Release blocker | all | Execute pure read action with `audit_required=false`. | No full audit is required, but access event is recorded where policy demands. |
| `AUD-006` | Release blocker | all | Execute ranking/read action such as `symbol.search`. | Selection/ranking evidence is auditable even though source data are not mutated. |
| `AUD-007` | Release blocker | all | Create child audit for one disputed colour decision. | Parent-child relationship is navigable and child outcome can supersede the parent slot without erasing it. |
| `AUD-008` | Release blocker | all | Record model/provider tool events. | Provider, model/version, prompt/parameter hashes, input/output hashes, timing, status, and result refs are present; hidden chain-of-thought is absent. |
| `AUD-009` | Release blocker | all | Change decision after human review. | Rejected candidate, review rationale, selected replacement, and supersession chain remain. |
| `AUD-010` | Release blocker | all | Resume failed action. | Existing audit/run is resumed or explicitly superseded; successful upstream events are not duplicated. |
| `AUD-011` | Release blocker | all | Export public audit summary. | Private prompts/evidence are redacted while decision basis, register, versions, and visible outcome remain intelligible. |
| `AUD-012` | Release blocker | all | Attempt action success with blocking uncertainty but no remainder. | Audit completion validator fails. |

---

## 8. Shared actions, CLI, HTTP, jobs, and harness portability

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `ACT-001` | Release blocker | all | Invoke same action through direct library, CLI, HTTP, and studio. | All paths use same action definition/version and produce schema-equivalent result envelopes. |
| `ACT-002` | Release blocker | `CLI` | Run every principal command with `--help` and `--json`. | Help documents required inputs; machine mode emits no decorative text on stdout. |
| `ACT-003` | Release blocker | `CLI` | Trigger validation, auth, permission, retryable, terminal provider, and internal failures. | Exit codes match the normative CLI table and structured error has stable code. |
| `ACT-004` | Release blocker | all | Submit identical idempotent request twice concurrently. | One side effect occurs; both callers receive same run/result identity. |
| `ACT-005` | Release blocker | all | Interrupt provider job after submission and resume. | Runtime uses persisted external job ID/cursor and does not resubmit. |
| `ACT-006` | Release blocker | all | Cancel queued, running-local, and awaiting-external jobs. | State transition follows policy; partial unregistered files are cleaned; external cancellation is attempted/recorded. |
| `ACT-007` | Release blocker | all | Invoke action without permission. | No side effect or provider call occurs; denial is audited. |
| `ACT-008` | Release blocker | all | Invoke publish action without prior approval. | Action fails before upload. |
| `ACT-009` | Release blocker | all | Modify an approved immutable revision directly. | Write is rejected; caller must create superseding revision. |
| `ACT-010` | Release blocker | `HERMES` | Install skill, ask agent to create and run an engagement through render using CLI. | Hermes discovers skill, invokes structured actions, resumes state, respects review gates, and returns rendition/package IDs. |
| `ACT-011` | Release blocker | `CLI` | Run same flow without Hermes using shell/scripted client. | Full product flow succeeds; no harness-specific database state is required. |
| `ACT-012` | Release blocker | all | Compare runtime action registry to 66-row normative catalogue. | Every required action exists with matching side effect, permission, approval, idempotency, and success contract. |
| `ACT-013` | Release blocker | all | Execute event stream during long run. | Monotonic sequence includes state changes, tool/provider activity, review request, completion/failure; reconnect resumes from cursor. |
| `ACT-014` | Release blocker | all | Crash worker between asset creation and SQL commit. | Recovery removes or reclaims temporary asset; no unregistered canonical output is exposed. |
| `ACT-015` | Release blocker | all | Crash after SQL request persistence but before external submission response. | Recovery uses idempotency key/provider lookup; duplicate external job is not silently created. |
| `ACT-016` | Release blocker | all | Execute `lock.acquire` for semantic object and nested field path. | One active `resource_lock` is created with target/path/type/reason/actor/time and appears in studio/action conflict checks. |
| `ACT-017` | Release blocker | all | Attempt write beneath an active object or field lock. | Action fails before side effects with conflict code, lock ID, and protected path. |
| `ACT-018` | Release blocker | all | Attempt implicit model/admin force override. | No force path exists; only authorised `lock.release` can clear the lock. |
| `ACT-019` | Release blocker | all | Release then re-acquire a lock. | Historical lock row retains release actor/time/reason; new lock has new identity; active uniqueness holds. |
| `ACT-020` | Release blocker | `PG`,`SQ` | Exercise every aggregate in the §12.4.1 lifecycle matrix through mutable, frozen, superseded/deprecated, and delete attempts. | Only declared forward status transitions succeed; frozen body/children and append-only evidence remain byte-identical; each prohibited mutation returns a stable conflict code. |

---

## 9. Asset registry, rights, and derivation

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `AST-001` | Release blocker | all | Register image, audio, video, SVG, font reference, PDF, JSON, and text assets. | Required media metadata and SHA-256 are stored; role-specific fields validate. |
| `AST-002` | Release blocker | all | Attempt public use of asset with unknown/prohibited rights. | Public render/package/publish is blocked by rights validator. |
| `AST-003` | Release blocker | all | Apply deterministic modifier twice. | Same input, operation version, and parameters produce same output hash. |
| `AST-004` | Release blocker | all | Apply AI modifier. | Provider receipt, model/version, inputs, output, prompt plan hash, and derivation edge are stored. |
| `AST-005` | Release blocker | all | Traverse derivation from final video to all source plates, symbol, audio, type outlines, and modifiers. | Complete acyclic provenance graph resolves; no canonical asset lacks an origin. |
| `AST-006` | Release blocker | all | Corrupt one package asset byte. | Manifest verification fails and names asset path/hash mismatch. |
| `AST-007` | Release blocker | all | Import remote asset into portable package. | Package contains local immutable copy or explicit unresolved remote reference according to package profile; manifest reflects choice. |
| `AST-008` | Release blocker | all | Delete an unreferenced temporary asset. | Garbage collection removes it without affecting any registered derivation. |

---

## 10. Symbol family, construction, alpha, and twelve states

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `SYM-001` | Release blocker | all | Search symbol bank by operation, topology, resonance, basin, and exclusions. | Ranked results expose component scores and do not auto-promote a candidate. |
| `SYM-002` | Release blocker | all | Propose each resolution mode: reuse, parameterise, transform, combine, generate_new. | Mode and constraints are explicit and QL-audited. |
| `SYM-003` | Release blocker | all | Canonicalise approved vector candidate. | Sanitised SVG contains no script, remote executable reference, or disallowed embedded content; geometry report passes. |
| `SYM-004` | Release blocker | all | Submit raster-only candidate as canonical symbol. | It remains candidate until vector reconstruction/approval or an explicitly versioned raster exception profile is approved. |
| `SYM-005` | Release blocker | all | Validate construction grammar primitives/operators. | Every path element is attributable to permitted primitive/operator or documented bespoke path exception. |
| `SYM-006` | Release blocker | all | Violate required aperture/open seam/invariant relation. | Geometry validator fails with invariant-specific finding. |
| `SYM-007` | Release blocker | all | Render twelve states from `FX-SYMBOL`. | Exactly one SVG/transparent derivative per address is produced and linked to its QL position. |
| `SYM-008` | Release blocker | all | Compare `P5′` loop anchor to `P0`. | Declared visual return transform is recorded and usable by compositor. |
| `SYM-009` | Release blocker | all | Generate alpha/mask derivatives. | Transparent edges have no unacceptable matte fringe, holes, clipping, or unexpected opacity; straight/premultiplied mode is declared. |
| `SYM-010` | Release blocker | `PRINT` | Render approved SVG at small card and large poster sizes. | Form remains legible; stroke/negative-space thresholds pass; no rasterisation at canonical print layer. |
| `SYM-011` | Release blocker | all | Approve new revision after prior canonical revision. | Both remain immutable; one is active under date/profile; supersession is explicit. |
| `SYM-012` | Release blocker | all | Use exact symbol as overlay and as alpha/luma mask. | Compositor output preserves approved geometry pixel-aligned to declared transform. |

---

## 11. Colour, typography, and art direction

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `ART-001` | Release blocker | all | Resolve semantic palette tokens. | Field, figure/mark, boundary, Bimba, Pratibimba, accent, return, text, and optional shadow tokens exist in OKLCH plus output fallbacks. |
| `ART-002` | Release blocker | `WEB`,`PRINT` | Run contrast and gamut validation. | Required text/UI contrast passes; print conversion has documented gamut handling; failures block canonical approval. |
| `ART-003` | Release blocker | all | Trace a palette token to resonance/profile/extension. | Complete derivation exists; no unversioned “vibe” value is canonical. |
| `ART-004` | Release blocker | all | Resolve typography signature. | Weight, width, contrast, geometry, terminal/openness, historical register, font refs, licences, fallbacks, and variable axes are present. |
| `ART-005` | Release blocker | all | Create bespoke display lettering. | Approved text is stored as reusable vector outlines with source string and revision; font binary redistribution is not required. |
| `ART-006` | Release blocker | all | Attempt to package unlicensed font binary. | Rights validator blocks package or selects permitted fallback/outline profile. |
| `ART-007` | Release blocker | all | Resolve complete art direction. | Palette, type, geometry, material, light, motion, camera, and compositing instructions all trace to projections or registered extensions. |
| `ART-008` | Release blocker | all | Lock symbol invariant and palette boundary token, then rerun art direction. | Locked paths remain byte/semantic equivalent; alternatives target only permitted paths. |

---

## 12. Storyboard, twelve scene atoms, and generation providers

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `VID-001` | Release blocker | all | Execute `storyboard.plan` for base profile. | Six scene pairs and twelve atoms cover every canonical address exactly once. |
| `VID-002` | Release blocker | all | Inspect each atom. | Intent, face/address, timing, visual action, camera, light, material, symbol/audio state refs, generation plan, references, and transitions are present. |
| `VID-003` | Release blocker | all | Validate base 6-second and 12-second plans. | Durations fall within base profile; no zero-duration atom/pair; exact frame arithmetic closes. |
| `VID-004` | Release blocker | all | Validate 40-second and 60-second plans. | Durations fall within extended profile and retain 12-address coverage. |
| `VID-005` | Release blocker | all | Attempt 13-second plan under base profile. | Validation fails or explicitly requires a different profile. |
| `VID-006` | Release blocker | all | Exercise each choreography mode: phase flip, crossfade, interleaved, split field, masked reveal, conjugate cut. | Renderer/provider plan expresses both atoms and mode-specific timing with no dropped face. |
| `VID-007` | Release blocker | all | Register provider capability and submit job within limits. | Request accepted; capability version and allocation are pinned. |
| `VID-008` | Release blocker | all | Submit request exceeding image/video/audio/duration limits. | Runtime blocks request before provider call and suggests permissible partition strategy. |
| `VID-009` | Provider blocker | external | Use Seedance reference adapter with multimodal reference pack and 6–12 second plan. | Job request/response, references, model/version, output candidates, and status are fully registered. |
| `VID-010` | Release blocker | all | Provider returns output with baked incorrect text/symbol. | Plate may be accepted only as background/world plate; final exact text/symbol layers remain deterministic. |
| `VID-011` | Release blocker | all | Generate Bimba and Pratibimba plates independently then pair. | Each plate is linked to correct atom; pair timing/transition is deterministic. |
| `VID-012` | Release blocker | all | Continue a clip for extended plan. | Continuation source, temporal overlap, provider settings, and continuity audit are stored. |
| `VID-013` | Release blocker | all | Accept/reject several candidate plates. | Accepted link is explicit; rejected candidates and reasons remain; approval cannot reference missing comparison report. |
| `VID-014` | Release blocker | all | Apply crop, scale, grade, grain, mask, overlay, time trim/stretch, and loop modifier. | Ordered modifier chain is deterministic and individually inspectable. |
| `VID-015` | Release blocker | all | Replace one accepted plate after storyboard approval. | New storyboard/render revision is created; dependent render plan becomes stale until regenerated. |
| `VID-016` | Release blocker | all | Complete generation with a deliberately `missing` QL position. | Media plan represents missingness intentionally (absence, hold, field, silence, withheld mark, or approved treatment) rather than inventing narrative content. |

---

## 13. QL Resonator and audio production

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `AUDO-001` | Release blocker | `MEDIA` | Compile canonical Faust DSP for offline and browser targets. | Both builds succeed from same DSP version; parameter names/ranges match contract. |
| `AUDO-002` | Release blocker | all | Resolve palette from `FX-AUDIO`. | Reference frequency, ratio set, register, two resonator banks, excitation, damping, inharmonicity, spatial field, and twelve states are explicit. |
| `AUDO-003` | Release blocker | all | Render twelve state assets and master drone. | Exactly twelve address states plus required stems/master are produced with deterministic hashes for same environment/profile. |
| `AUDO-004` | Release blocker | all | Verify ratio targets by FFT/CQT. | Measured partial/fundamental frequencies are within configured cent/Hz tolerance. |
| `AUDO-005` | Release blocker | all | Verify Bimba–Pratibimba semitone/conjugate relation under selected musical profile. | Expected pitch-class or ratio relation is detected and reported per pair. |
| `AUDO-006` | Release blocker | all | Verify within-helix tritone mirror where enabled. | Chromagram/pitch-class report matches declared mirror relation. |
| `AUDO-007` | Release blocker | all | Render with excessive movement fixture. | Motion-density validator flags violation of drone/minimal-movement profile. |
| `AUDO-008` | Release blocker | all | Render clipping fixture. | Peak/clipping validator fails; canonical approval blocked. |
| `AUDO-009` | Release blocker | all | Mix canonical drone with provider incidental audio. | Policy records keep/duck/remove/transform; drone remains measurable above minimum audibility threshold. |
| `AUDO-010` | Release blocker | all | Validate audio loop. | Boundary discontinuity, phase/tail policy, loudness, and decay fall within named thresholds. |
| `AUDO-011` | Release blocker | `WEB` | Resume browser audio after user gesture and mute/unmute. | Browser policy is respected; state resumes without restarting semantic position unless configured. |
| `AUDO-012` | Release blocker | all | Use commercial sound-design instrument in audition workflow. | Result can inform approved parameter/profile, but unattended canonical render does not depend on unlicensed/non-automatable plugin. |

---

## 14. Deterministic composition, loop, and output renditions

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `RND-001` | Release blocker | all | Validate `render-plan.schema.json` with complete plan. | Exact 12 atoms/6 pairs, approved inputs, renderer versions, safe frame, layers, outputs, and loop anchors validate. |
| `RND-002` | Release blocker | all | Remove exact symbol layer and render. | Final-master validation fails even if generated plate contains a symbol-like mark. |
| `RND-003` | Release blocker | all | Render 9:16 master, silent loop, transparent symbol animation, poster candidate sheet, square preview, print assets, audio masters, and captions. | Every required profile completes and is registered with hash/metadata. |
| `RND-004` | Release blocker | all | Repeat render with same plan, versions, and deterministic inputs. | Output hashes are identical or a documented codec nondeterminism profile supplies equivalent bitstream-independent verification. |
| `RND-005` | Release blocker | all | Change one approved input. | New render-plan digest and rendition revision are produced; prior master remains immutable. |
| `RND-006` | Release blocker | all | Validate `P5′→P0` visual seam. | Pixel/perceptual motion/colour thresholds pass under loop profile; report includes exact measurements. |
| `RND-007` | Release blocker | all | Validate semantic return. | Seam pass alone is insufficient; render also links to non-empty return deposit and media delta. |
| `RND-008` | Release blocker | all | Render reduced-motion fallback. | Static/poster or low-motion alternative preserves symbol, QL navigation, and accessible content. |
| `RND-009` | Release blocker | all | Render captioned extended film with transcript excerpts. | Captions are timed, disclosure-safe, and do not obscure safe composition area. |
| `RND-010` | Release blocker | all | Render alpha WebM symbol animation. | Alpha channel exists, edges validate, and file plays/composites correctly in target browsers. |
| `RND-011` | Release blocker | all | Attempt final master from unapproved plate/symbol/audio revision. | Renderer blocks canonical output or labels it non-canonical preview. |
| `RND-012` | Release blocker | all | Inspect frozen rendition. | It identifies engagement/frame/resonance/art/symbol/storyboard/audio/render revisions, all input assets, renderer versions, and audit chain. |

---

## 15. Digital front, conjugate hexagonal back, and accessibility

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `UI-001` | Release blocker | `WEB` | Load `<epi-card>` from a public snapshot. | Front renders poster immediately and transitions to film without layout shift beyond threshold. |
| `UI-002` | Release blocker | `WEB` | Play front with audio. | Exact symbol overlay/mask, video, lettering, and canonical audio remain synchronised. |
| `UI-003` | Release blocker | `WEB` | Flip to back. | Hexagonal surface displays six edges, not twelve disconnected controls. |
| `UI-004` | Release blocker | `WEB` | Activate each edge. | Each opens one `Pn↔Pn′` pair and exposes both distinct articulations, scene/audio/symbol states, claims, and source access allowed by disclosure. |
| `UI-005` | Release blocker | `WEB` | Toggle global Bimba/Pratibimba orientation. | Centre operation changes orientation while retaining active pair/address and relation context. |
| `UI-006` | Release blocker | `WEB` | Open nested inner form from a position. | Nested data loads recursively with depth indicator and path back; parent state is retained. |
| `UI-007` | Release blocker | `WEB` | Navigate entire card by keyboard. | Flip, six edges, conjugate toggle, play/mute, details, and close controls are reachable in logical order and have visible focus. |
| `UI-008` | Release blocker | `WEB` | Inspect accessible names/roles. | Controls expose meaningful labels including QL pair names; SVG/video alternatives and textual summaries exist. |
| `UI-009` | Release blocker | `WEB` | Enable `prefers-reduced-motion`. | Autoplay/motion policy follows profile and preserves functional content. |
| `UI-010` | Release blocker | `WEB` | Enable high zoom and narrow viewport. | Content remains usable without clipped controls or unreadable text; hex edge hit areas meet target minimum. |
| `UI-011` | Release blocker | `WEB` | Load a card with missing/withheld position. | UI shows defined missing/withheld state and does not fabricate summary/media. |
| `UI-012` | Release blocker | `WEB` | Disconnect after initial public snapshot load. | Allowed cached/static card content and fallback remain usable; private/action features fail safely. |
| `UI-013` | Release blocker | `WEB` | Listen for custom element events. | View, position, QL face, play state, relation follow, action request, and asset error events match TypeScript contract. |
| `UI-014` | Release blocker | `WEB` | Test Chromium, Firefox, Safari. | Required front/back/film/audio/hex interactions pass in all three release families. |

---

## 16. Printed object and QR

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `PRN-001` | Release blocker | `PRINT` | Render reference 70×120 mm card with 3 mm bleed and 5 mm safe area. | PDF page/trim/bleed boxes and safe-area checks pass. |
| `PRN-002` | Release blocker | `PRINT` | Inspect front. | Approved poster frame, exact vector symbol, outlined title, and restrained version/edition mark are present. |
| `PRN-003` | Release blocker | `PRINT` | Inspect back. | Static six-edge conjugate hexagon, both pair names/keys, return line, QR, and immutable public identifier/hash are present. |
| `PRN-004` | Release blocker | `PRINT` | Scan QR from screen, office print, and 300-dpi proof at intended size. | All scans resolve immutable public rendition URL; no session/private credential appears. |
| `PRN-005` | Release blocker | `PRINT` | Select poster frame through `poster.select`. | Candidate sheet and QL audit show symbol legibility, composition, print crop, and rationale. |
| `PRN-006` | Release blocker | `PRINT` | Convert to target print colour profile. | Conversion report exists; critical colours/contrast remain within configured tolerances. |
| `PRN-007` | Release blocker | `PRINT` | Open PDF on machine without project fonts. | Display title is outlined and body text embeds licensed fonts or uses declared fallback; no missing-glyph substitution. |
| `PRN-008` | Release blocker | `PRINT` | Print card detached from web product. | Object remains semantically usable: symbol, pair names, return, identity, and QR are legible without app chrome. |

---

## 17. Studio and collaborative workflow

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `STD-001` | Release blocker | `WEB` | Open engagement workspace. | Context, sources, attractor/basin, QL frame, resonance, symbol, storyboard, media, audio, card, audit, validation, and publication modules are accessible. |
| `STD-002` | Release blocker | `WEB` | Run action from agent surface and inspect event stream. | Tool/action steps, state, provider job, audit, candidates, and review request are visible and interruptible. |
| `STD-003` | Release blocker | `WEB` | Lock JSON/semantic paths, rerun upstream generation. | Locked values are preserved; dependent stale results are identified. |
| `STD-004` | Release blocker | `WEB` | Two collaborators edit same revision concurrently. | Optimistic concurrency detects conflict; no silent last-write overwrite occurs. |
| `STD-005` | Release blocker | `WEB` | Compare two immutable revisions. | Semantic, profile, parameter, asset, and audit differences are shown. |
| `STD-006` | Release blocker | `WEB` | Approve/reject candidate from studio. | Actor, role, target revision/hash, comment, timestamp, and decision are stored. |
| `STD-007` | Release blocker | `WEB` | Attempt approval by actor lacking role. | Operation is blocked. |
| `STD-008` | Release blocker | `WEB` | Resume engagement in new session/harness. | Studio loads same canonical state and active runs from SQL, not prior chat memory. |

---

## 18. OKF v0.2 wiki artifact export

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `OKF-001` | Release blocker | all | Export complete/private OKF bundle. | Required wiki tree, Markdown, YAML frontmatter, links, lifecycle, provenance, and attested computations are emitted. |
| `OKF-002` | Release blocker | all | Export shared and public variants. | Disclosure-specific content differs as specified while stable public IDs and permitted links remain. |
| `OKF-003` | Release blocker | all | Inspect QL content tree. | Twelve separate position pages plus threshold, return, conjugate index, and six pair pages exist. |
| `OKF-004` | Release blocker | all | Inspect source/provenance links. | Permitted claims link to exact source/evidence pages/selectors; private sources are redacted or omitted by profile. |
| `OKF-005` | Release blocker | all | Validate frontmatter. | Required OKF/profile fields, IDs, versions, trust/freshness/lifecycle data, hashes, and relations parse. |
| `OKF-006` | Release blocker | all | Validate internal links and anchors. | No broken local link or unresolved required target exists. |
| `OKF-007` | Release blocker | all | Verify attested resonance/mapping computation. | Receipt input hashes, profile/version, algorithm, output hash, and runtime identity reproduce or verify. |
| `OKF-008` | Release blocker | all | Edit exported Markdown manually and re-import as source. | It is treated as a new source/wiki artifact, not a silent mutation of operational SQL truth. |
| `OKF-009` | Release blocker | all | Remove SQL/database from package and open OKF directory. | Wiki remains readable/navigation-complete as an artifact set, while clearly not claiming operational resumability. |
| `OKF-010` | Release blocker | all | Run `okf.validate`. | Bundle passes tree, frontmatter, links, source, lifecycle, trust, and attestation checks. |

---

## 19. Portable `.epicard` package

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `PKG-001` | Release blocker | all | Build private complete package. | Contains `card.sqlite`, manifest, content-addressed assets, selected renders, OKF bundle, reports, and profile metadata. |
| `PKG-002` | Release blocker | all | Build public package. | Contains only public projection; private SQL rows/assets/content cannot be recovered from package. |
| `PKG-003` | Release blocker | `SQ` | Open package offline in reference viewer. | Card front/back, details, selected media, OKF, audits allowed by profile, and hashes resolve without network. |
| `PKG-004` | Release blocker | `SQ` | Query portable SQLite validators. | QL/audit/storyboard validation views report complete canonical structures. |
| `PKG-005` | Release blocker | all | Verify manifest. | Every packaged file has path, role, size, media type, SHA-256, disclosure, and provenance ref; no unlisted file exists except permitted packaging metadata. |
| `PKG-006` | Release blocker | all | Round-trip package to server import. | Stable semantic IDs, revisions, hashes, and relations are preserved; duplicate assets are reused. |
| `PKG-007` | Release blocker | all | Import package with conflicting local ID but different content. | Import detects conflict and uses namespace/remap policy; no overwrite occurs. |
| `PKG-008` | Release blocker | all | Package with remote-only optional asset. | Manifest marks availability and fallback; offline viewer degrades according to profile without false hash success. |
| `PKG-009` | Release blocker | all | Validate `manifest.json` against `contracts/package-manifest.schema.json`, then run filesystem closure checks. | Schema passes; paths are unique, relative, traversal-free, and forward-slash-only; every entrypoint/rendition resolves; every physical file except the manifest is listed exactly once; no listed file is absent. |
| `PKG-010` | Release blocker | all | Recompute package root digest from the manifest file list. | Sorting by Unicode code-point path and hashing each `sha256␠␠path\n` record exactly reproduces `integrity.root_sha256`; altering any path, byte, disclosure projection, or listed digest fails verification. |
| `PKG-011` | Release blocker | all | Export and import a package containing `P0′…P5′`. | Unicode PRIME `U+2032` survives SQL, JSON, ZIP paths/metadata, OKF, and UI round-trip; ASCII apostrophe or transport aliases are rejected as canonical addresses. |
| `PKG-012` | Release blocker | all | Inspect the packaged `card.sqlite`, content-validation report, manifest, and production `package_export` row. | `card.sqlite` omits the current package/archive/manifest self-records; the included report contains no package-root/archive/self-hash dependency; the detached production row/action result contains final manifest, root, and archive identity. |
| `PKG-013` | Release blocker | all | Re-run package assembly from the same frozen inputs while varying ZIP container metadata only. | Manifest file set and root digest remain identical; archive asset hash may differ only when non-canonical ZIP metadata is permitted by profile, and the production receipt records the actual archive hash. Reference packaging uses deterministic ZIP metadata and therefore produces the same archive hash. |

---

## 20. Publication, privacy, deletion, and revocation

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `PUB-001` | Release blocker | all | Prepare publication. | No upload occurs; platform constraints, metadata, immutable rendition hash, account ref, and disclosure manifest are frozen. |
| `PUB-002` | Release blocker | all | Approve publication then change metadata/rendition. | Approval becomes stale; execution is blocked until new approval. |
| `PUB-003` | Release blocker | all | Execute approved publication twice. | Idempotency prevents duplicate post or returns same remote publication identity. |
| `PUB-004` | Release blocker | all | Poll remote processing. | Raw provider response and mapped status are stored; no timeout is interpreted as success. |
| `PUB-005` | Release blocker | all | Publish fixture containing private asset relation. | Preflight blocks publication and identifies exact disclosure leak. |
| `PUB-006` | Release blocker | all | Revoke public rendition. | Public access/publication status changes according to connector capability; revocation event and limitations are recorded. |
| `PUB-007` | Release blocker | all | Delete Pasu private content under policy. | Deletable content is erased/crypto-shredded; retained legal/audit records are minimised and clearly tombstoned. |
| `PUB-008` | Release blocker | all | Revoke provider consent after candidate generation. | Future submissions are blocked; existing assets are handled by recorded consent/retention policy. |
| `PUB-009` | Release blocker | all | Inspect provider disclosure manifest before each external call. | Exact data categories/assets/text excerpts/provider/purpose/retention settings are displayed and logged. |
| `PUB-010` | Release blocker | all | Verify public URL/QR after internal session rotation. | Public identity remains stable and private session credentials remain unrelated. |

---

## 21. Security, resilience, and performance

| ID | Level | Environment | Procedure | Pass condition |
|---|---|---|---|---|
| `SEC-001` | Release blocker | all | Upload malicious SVG containing script/event handler/external executable ref. | Sanitiser rejects/removes it; canonical asset never serves active content. |
| `SEC-002` | Release blocker | all | Attempt path traversal in package asset path. | Export/import rejects path; no file escapes package root. |
| `SEC-003` | Release blocker | all | Supply SQL/meta-command text through source fields. | Stored as data; actions use parameterised queries; no injection occurs. |
| `SEC-004` | Release blocker | all | Supply prompt-injection text in imported source. | Content remains evidence/data; agent skill requires action permissions and does not execute source instructions as authority. |
| `SEC-005` | Release blocker | all | Attempt SSRF through remote asset URL/provider webhook. | URL policy and network boundary reject disallowed destinations. |
| `SEC-006` | Release blocker | all | Inspect logs/telemetry for secrets and private content. | Session keys, connector credentials, private phrases, raw provider secrets, and prohibited content are redacted. |
| `SEC-007` | Release blocker | all | Restore PostgreSQL/object-store backup to clean environment. | Engagements, content hashes, revisions, actions, audits, and assets are consistent; recovery point/object lag is reported. |
| `SEC-008` | Release blocker | all | Resume 100 interrupted local/external actions. | No duplicate canonical output/publication; all runs resolve to terminal or review state. |
| `PERF-001` | Release blocker | `WEB` | Load public card over reference broadband/mobile profile. | Poster and controls meet product performance budget; large film/audio lazy-load without blocking back/details. |
| `PERF-002` | Release blocker | all | Query full 12-position engagement with sources/audits/assets. | API meets documented p95 budget under reference data volume. |
| `PERF-003` | Release blocker | all | Export/package a reference full card. | Completes within documented budget and bounded memory/disk; progress events remain responsive. |
| `PERF-004` | Release blocker | all | Run 20 concurrent media jobs under configured worker capacity. | Backpressure/queueing works; database and object store remain consistent; no silent job loss. |

---

## 22. End-to-end release scenarios

### `E2E-001` — Hand-resolved complete card

**Level:** Release blocker  
**Fixture:** `FX-12`, `FX-SYMBOL`, `FX-AUDIO`, accepted still/video plates  

Procedure:

1. Create Pasu/session/temporal snapshot and engagement.
2. Create attractor and approved basin.
3. Ingest sources and initialise/map/approve the full conjugate frame.
4. Resolve/project resonance; approve art direction.
5. Approve symbol family and twelve states.
6. Plan storyboard, attach accepted plates, resolve/render audio.
7. Render web card, print card, base/extended films, OKF, and package.
8. Validate and approve final rendition.
9. Deposit return.

Pass condition: all Definition of Done items can be demonstrated without an external generative-video provider.

### `E2E-002` — Agent-generated base card in Hermes

**Level:** Release blocker  
**Fixture:** situated prompt, `FX-5`, one recording, provider-safe references  

Procedure:

1. Initiate through Hermes using the installed skill.
2. Agent operates only through shared actions/CLI.
3. Agent resolves incomplete QL mapping without filling unsupported position.
4. Human reviews basin, mapping, art direction, symbol, plates, mix, and final rendition.
5. System generates a 6–12 second loop, web/print card, OKF, package, and return.

Pass condition: the workflow survives interruption/resume, all material decisions have 12-position audits, and no harness-only state is required.

### `E2E-003` — Dual-helix extended film

**Level:** Release blocker  
**Fixture:** complete 12-position engagement  

Pass condition: independent Bimba and Pratibimba plate passes assemble into a 40–60 second film, each address is temporally locatable, conjugate relations are visible/audible, and `P5′→P0` loop plus semantic return validate.

### `E2E-004` — Private talismanic engagement and public projection

**Level:** Release blocker  
**Fixture:** `FX-PRIVATE`, `FX-REC`, private activation phrase  

Pass condition: complete private package contains permitted private depth; public card/OKF/package/QR expose only approved projection; generated provider requests contain only provider-authorised snapshot fields.

### `E2E-005` — Portable offline round trip

**Level:** Release blocker  

Pass condition: `.epicard` created on production profile opens offline from SQLite/files, validates, renders in reference viewer, and re-imports without semantic/hash loss.

### `E2E-006` — Recursive return

**Level:** Release blocker  
**Fixture:** `FX-RETURN`  

Pass condition: first card’s `P5′→P0⁺` deposit creates a second engagement whose threshold cites the prior return, carries declared semantic/media delta, and does not mutate the first card.

---

## 23. Release decision

A release candidate is conforming only when:

1. every Release blocker passes in its declared environment;
2. provider-specific blockers pass for every provider adapter advertised as supported;
3. no open severity-1 or severity-2 finding remains;
4. every SHOULD departure has a versioned implementation note and equivalent test;
5. the package manifest, schema revision, normative specification hash, action registry, and generated API/types agree;
6. one complete evidence bundle for each end-to-end scenario is retained.

**End of acceptance specification.**
