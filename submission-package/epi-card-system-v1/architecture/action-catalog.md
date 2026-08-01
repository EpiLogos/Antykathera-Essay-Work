# Epi-Card Shared Action Catalogue

**Version:** 1.0.0  
**Normative relation:** implements `SPEC.md` §§9–11, 17–19, 22–24.

Every action is defined once in the shared action library and exposed through the CLI, HTTP boundary, studio, tests, and agent skill. The table below is the normative human-readable catalogue. `contracts/action-registry.yaml` is its normative machine-readable expansion and fixes all 66 action names, versions, side-effect classes, permissions, transaction classes, retry policies, audit requirements, and structured gates. `scripts/generate-action-registry.py` regenerates the registry and the two database seed files; generated files MUST NOT be hand-edited. Every material action has a full twelve-position QL audit unless the registry explicitly sets `audit_required: false`.

A gate is not inferred from the phrase in the table. The machine registry represents every gate as `{kind, stage, mode, when, requires}`. `contracts/gate-predicates.yaml` supplies the exact named-predicate semantics and typed arguments. `pre_execute` gates block side effects, `pre_commit` gates block successful completion, `pre_promote` gates allow candidate production but block canonical/approved use, and `pre_publish` gates block remote publication. `mode: always` applies to every invocation; `mode: conditional` applies only when its condition is true. The action-level `gate_mode` is `none`, `conditional`, or `required` and is derived from those explicit entries.

## Universal action rules

1. The caller supplies an `action-envelope.schema.json` request.
2. The runtime resolves the action in `contracts/action-registry.yaml`, validates the action-specific payload through `contracts/action-payloads.schema.json`, then validates permission, gates, disclosure, current state, context-ID equality, and idempotency before side effects.
3. A write/generate/render/publish action creates an `action_run`, `action_event` sequence, and QL `audit_tick`.
4. Generated or edited media are candidates until an acceptance/approval action promotes them.
5. External provider calls use a pinned `provider_capability` record and preserve the raw provider response.
6. Successful outputs are content-addressed; database writes and asset registration complete in a declared transaction/saga.
7. Retryable work resumes by run ID and provider cursor. It never repeats successful upstream actions.
8. Publication actions are separate from generation and rendering.

## Catalogue

| Action | Side effect | Required input | Output | Permission | Approval gate | Idempotency | Success condition |
|---|---|---|---|---|---|---|---|
| `pasu.create` | `write` | kind, public_handle?, locale?, timezone_default?, consent_profile | pasu_id | pasu:write | none | request key | Pasu row and creator audit committed |
| `pasu.snapshot` | `write` | pasu_id, attribute_ids?, disclosure, provider_scope | pasu_snapshot_id, included/redacted attributes | pasu:read | none | content hash | Immutable snapshot and disclosure receipt committed |
| `session.open` | `write` | pasu_id?, parent_session_id?, harness, harness_session_ref?, timezone, locale?, disclosure | session_id, one-time raw session_key | session:write | none | request key | UUIDv7 session and hashed 256-bit key stored |
| `session.resume` | `read` | session_id or raw session_key, last_event_sequence? | session state, active runs, continuation set | session:read | none | read idempotent | Credential verified; no state mutation except acknowledged sequence |
| `session.close` | `write` | session_id | ended_at, final state | session:write | none | session+close | Session closed once; repeated calls return same result |
| `temporal.capture` | `write` | session_id, event_time?, observed_at, timezone, location?, astronomy request?, astrology profile? | temporal_snapshot_id, raw facts, interpreted contribution refs | temporal:write | provider disclosure when external astronomy is used | fact-input hash | Facts and interpretations stored separately with provider/profile versions |
| `source.ingest` | `write` | engagement_id, source_kind, declared_arity?, source URI/file/value, disclosure | source_form_id, source_member_ids, asset_ids | source:write | provider disclosure when extraction leaves runtime | source hash | Native form and every source member stored before mapping |
| `recording.ingest` | `write` | session_id, engagement_id?, recording file, speaker map?, consent_state, disclosure | recording_id, source asset_id | recording:write | explicit consent state required | asset hash | Recording asset hashed and consent metadata present |
| `recording.transcribe` | `generate` | recording_id, provider profile, language hints?, diarisation settings | transcript_id, segment_ids, transcript asset | recording:transcribe | external-provider disclosure required | recording hash+provider+settings | Time-addressed segments, model version, confidence and digest stored |
| `evidence.link` | `write` | engagement_id, target kind/id, source kind/id/URI, selector, relation, register, note? | evidence_link_id | evidence:write | none | target+source+selector hash | Typed evidence edge resolves to an allowed source and target kind |
| `projection.materialize` | `write` | engagement_id, projection_kind, disclosure profile/version, source revision manifest, provider/purpose when applicable | projection_id, snapshot hash, included/redacted paths | projection:write | review required for shared, public, and provider projections | engagement revisions+profile+target hash | Immutable disclosure-scoped snapshot is stored; provider projection names provider and purpose |
| `projection.validate` | `read` | projection_id, validation profile/version | validation report, disclosure findings | projection:read | none | projection hash+validator version | Snapshot hash, allowed fields/assets, source revisions, and disclosure constraints validate without mutation |
| `attractor.create` | `write` | kind, label, description?, stable_key? | attractor_id, revision_id | attractor:write | none | stable_key or request key | Attractor and revision 1 committed without graph dependency |
| `basin.resolve` | `generate` | engagement/attractor revision, source forms, context, active lens/profile | candidate basin revision, members, exclusions, unresolved set | basin:write | review required before canonical use | input revision hash | Every member has relation, weight, register, rationale and evidence/audit |
| `basin.revise` | `write` | attractor_id, prior revision, patch operations, rationale | new attractor_revision_id, basin member set | basin:write | review when exclusions/essential members change | prior revision+patch hash | Immutable new revision; prior revision unchanged |
| `ql.initialize` | `write` | engagement_id | 12 ql_position ids, canonical relations | ql:write | none | engagement id | Exactly P0…P5 and P0′…P5′ plus relation seeds exist |
| `ql.map` | `generate` | engagement_id, source forms, basin revision, active lens/profile, mapping constraints | assignments, claims, occupancy, summaries for 12 positions | ql:write | review required | semantic input hash | No source member silently discarded; all claims registered/evidenced; full 6+6′ audit complete |
| `ql.reconcile` | `generate` | engagement_id, reconciliation scopes (conjugate/complement/partition/return) | reconciliation findings and proposed patches | ql:write | review required for content mutation | frame revision+scope | Six conjugates, six complement relations by phase and 4:2/3:3 partitions inspected |
| `ql.validate` | `read` | engagement_id, validation profile | validation_report_id, findings | ql:read | none | frame revision+validator version | Structural, semantic and evidence validators run without mutation |
| `ql.approve` | `write` | engagement_id, frame revision, validation_report_id, approval actor/comment | approval_id, approved frame revision | ql:approve | human or declared authorised actor | frame revision+actor | All blocking findings cleared and approval stored |
| `lock.acquire` | `write` | engagement_id, target kind/id, field path, lock type, reason, expiry? | resource_lock_id | lock:write | actor must hold lock permission for target | active target+path | One active lock exists for target/path and dependent actions receive conflict on mutation |
| `lock.release` | `write` | resource_lock_id, release reason | released lock record | lock:write | lock owner or authorised lock manager | lock id+release actor | Lock is released once with actor/time/reason; immutable lock history remains |
| `return.deposit` | `write` | engagement_id, self_implication, remainder, achieved_work?, external implications, next_ground, seeds, semantic/media delta, next engagement? | return_deposit_id, next tick link | return:write | review required | engagement+return content hash | 5′→0⁺ record complete; optional next engagement does not equal current |
| `resonance.resolve` | `generate` | engagement_id, correspondence profile set, source contribution proposals | aggregate and 12 position resonance_state ids, receipts | resonance:write | review for new open-extension contributions | inputs+profile versions | Circular phase and scalar/vector aggregates reproducible from persisted rows |
| `resonance.project` | `write` | resonance_state_ids, modality projection profile ids/versions | projected_parameter_set ids | resonance:write | none | state hash+profile version | Deterministic parameters and calculation receipts stored |
| `resonance.compare` | `read` | state ids or engagement ids, modalities? | component deltas, profile deltas, nearest/contrasting states | resonance:read | none | read idempotent | Comparison preserves circular phase and ratio-set semantics |
| `art-direction.resolve` | `generate` | engagement_id, projected parameters, constraints, references | art_direction_revision candidate | art:write | review required | resonance+constraints hash | All palette/type/geometry/motion/light choices trace to projections or registered extension |
| `palette.resolve` | `generate` | engagement_id, colour projection, accessibility/print constraints | semantic OKLCH tokens and fallbacks | art:write | review when canonical | projection+constraints hash | Required field/figure/boundary/bimba/pratibimba/accent/return/text tokens pass contrast checks |
| `typography.resolve` | `generate` | engagement_id, typography projection, text set, font inventory/licences | typography signature, font refs, outlined title plan | art:write | review when canonical | projection+inventory hash | Font licensing recorded; bespoke display text has outline path |
| `symbol.search` | `read` | engagement_id, operation/topology/resonance/basin query, exclusions | ranked symbol family/revision candidates and distances | symbol:read | none | query hash | Results expose matching dimensions and do not auto-select |
| `symbol.propose` | `generate` | engagement_id, search result, resolution mode, grammar constraints | candidate symbol revision and twelve-state plan | symbol:write | review required | semantic+constraint hash | Mode is one of reuse/parameterise/transform/combine/generate_new and has full audit |
| `symbol.generate` | `generate` | candidate grammar, vector/raster provider profile, references | candidate assets, generation receipt | symbol:generate | external-provider disclosure and later review | grammar+provider+seed/reference hash | Outputs remain candidate; provider/model/version/input hashes stored |
| `symbol.transform` | `generate` | source symbol revision, permitted operators, target resonance/grammar | candidate transformed revision/assets | symbol:write | review required | source hash+operator params | Invariant grammar constraints remain satisfied or action fails |
| `symbol.canonicalize` | `write` | candidate revision, reconstructed grammar, SVG, geometry report | validated symbol_revision and derivatives | symbol:write | human/authorised approval required | SVG hash+grammar hash | Sanitised script-free SVG passes geometry, print and alpha checks |
| `symbol.state.render` | `render` | approved symbol revision, 12 transformation states, output profile | 12 SVG states, transparent derivatives, mask assets | symbol:render | none | revision+state profile hash | Exactly one state per QL address; P5′ and P0 loop anchors recorded |
| `symbol.validate` | `read` | symbol revision/assets, validator profile | validation report and visual diff assets | symbol:read | none | asset hash+validator version | SVG sanitation, grammar, bounds, alpha, print and loop-anchor checks complete |
| `symbol.approve` | `write` | symbol revision, passing report, actor decision | approval id; revision status approved | symbol:approve | human or declared authorised actor | revision+actor | Canonical revision frozen; prior approval supersession explicit |
| `storyboard.plan` | `generate` | engagement_id, QL frame, art direction, symbol/audio states, duration profile | storyboard revision, six pairs, twelve atoms, storyboard assets | storyboard:write | review required | frame+art+duration hash | Exactly 6 pairs/12 atoms cover all addresses and fit timeline |
| `image.collect` | `write` | engagement_id, search/import request, rights requirements | reference asset ids, rights/provenance records | asset:collect | none unless external account access | content/import hash | Every asset has licence/rights/disclosure metadata |
| `image.generate` | `generate` | scene/symbol reference, provider profile, prompt plan, reference assets | candidate image assets, provider receipt | asset:generate | external-provider disclosure | request hash | Candidates only; exact symbol/type are not baked as canonical layers |
| `image.edit` | `generate` | input asset, edit instructions/mask, provider or deterministic mode | edited candidate/intermediate asset | asset:generate | provider disclosure if external | input hash+edit params | Derivation link and model/operation version stored |
| `image.alpha` | `generate` | input image, method/profile, edge constraints | transparent asset, alpha mask, matte report | asset:generate | review for canonical symbol | input hash+method | Alpha edge, fringing, hole and bounds tests pass |
| `scene.plan` | `write` | storyboard revision, position/pair patch, timing/camera/light/generation plan | new storyboard revision | storyboard:write | review if approved revision changed | prior revision+patch | Immutable revision maintains 6/12 coverage and timeline limits |
| `video.submit` | `generate` | scene atom/pair or full storyboard, provider capability version, prompt/reference allocation | provider_job id, request hash | video:generate | external-provider disclosure | provider request hash | Capability limits validated before submission; provider job stored |
| `video.poll` | `read` | provider_job id | status, progress, provider outputs or error | video:generate | none | provider job id | Provider status mapped to runtime state without losing raw response |
| `video.continue` | `generate` | accepted/candidate video asset, continuation plan, provider profile | provider job and continuation candidates | video:generate | provider disclosure | source hash+continuation plan | Continuity reference and derivation edge stored |
| `video.edit` | `generate` | video asset, edit/mask/time range, provider or deterministic method | edited video candidate/intermediate | video:generate | provider disclosure if external | source hash+edit params | Operation is time-addressed and input/output hashes recorded |
| `plate.accept` | `write` | scene atom id, candidate asset id, comparison report, actor decision | accepted plate link and approval/rejection record | plate:approve | review required | scene+asset+actor | Candidate matches intended atom; rejected candidates retained in audit |
| `modifier.apply` | `render` | input asset, operation/version/parameters, target role | output asset, modifier operation row | render:write | none; review for non-deterministic modifier | input hash+operation+params | Deterministic operations reproduce digest; AI modifiers include provider receipt/audit |
| `composition.render` | `render` | render plan id, output profile set | rendition ids and output assets | render:execute | final master review required after render | plan hash+renderer version | All exact symbol/type/audio layers composed; output hashes and logs stored |
| `loop.validate` | `read` | rendition or render plan, thresholds | visual/audio seam report and pass/fail | render:read | none | rendition hash+validator version | P5′→P0 visual/audio thresholds pass and semantic delta exists |
| `poster.select` | `generate` | master rendition, candidate sampling/profile, print constraints | selected frame asset, candidate sheet, audit | poster:write | review required | video hash+selection profile | Selected frame satisfies symbol legibility, print crop and QL audit |
| `audio.palette.resolve` | `generate` | engagement_id, resonance states, tuning/resonator/spatial profiles | audio_palette_revision and 12 parameter states | audio:write | review required | resonance+profiles hash | Ratio set/reference Hz distinction explicit; 12 states and conjugate relations present |
| `audio.render` | `render` | audio palette revision, QL Resonator version, output settings | 12 state assets and master layers | audio:render | none | palette hash+DSP version+settings | Offline Faust render completes without clipping and stores exact parameters |
| `audio.analyze` | `read` | audio asset ids, FFT/CQT/chroma/loop profile | analysis receipts, plots/data assets, findings | audio:read | none | asset hash+analysis version | Ratio, spectrum, loudness, clipping and discontinuity measurements stored |
| `audio.mix` | `render` | audio layers, video/incidental audio policy, gain/spatial plan | mixed master and stems | audio:render | review required for final mix | input hashes+mix plan | Loudness/peak targets and canonical drone audibility pass |
| `audio.loop.validate` | `read` | audio master, seam thresholds | loop report | audio:read | none | asset hash+threshold profile | Boundary discontinuity and decay/tail policy pass |
| `card.render.web` | `render` | engagement/rendition ids, disclosure profile, component version | web card data snapshot and static fallback assets | card:render | none | revision hashes+component version | Front/back/hex data resolve; 6 edges unfold both conjugate positions |
| `card.render.print` | `render` | approved poster, symbol, QL names/summaries, QR target, print profile | front/back PDF and previews | card:render | review required | content hashes+print profile | Bleed/safe area, vector symbol, QR and font outline checks pass |
| `card.package` | `render` | engagement id + expected revision, approved projection id/hash, approved QL frame revision/hash, active profile set/hash, selected approved renditions, OKF export, package profile | validated `.epicard` package asset, manifest file hash, package root SHA-256, manifest schema ID | package:write | review for shared/public package | manifest file hash + package root SHA-256 | SQLite, assets, renders, knowledge and reports have verified hashes and complete manifest closure |
| `okf.export` | `render` | engagement id, disclosure profile, export profile version | OKF bundle asset and manifest | okf:write | review for shared/public export | engagement revision+profile | Wiki artifact tree, YAML frontmatter, sources, lifecycle and provenance emitted |
| `okf.validate` | `read` | OKF bundle asset, OKF version/profile | validation report | okf:read | none | bundle hash+validator version | Links, frontmatter, source refs, lifecycle and attestation receipts pass |
| `publication.prepare` | `write` | rendition id, platform/account, metadata, disclosure manifest | publication id status prepared | publication:write | none | platform+account+rendition hash | No upload; platform constraints and disclosure checked |
| `publication.approve` | `write` | publication id, actor decision | approval id and publication status | publication:approve | human/authorised publisher | publication+actor | Approved render hash/metadata/disclosure frozen |
| `publication.execute` | `publish` | approved publication id, platform credentials ref | remote job/publication id and status | publication:execute | prior approval mandatory | publication idempotency key | Only approved immutable rendition uploaded; provider response stored |
| `publication.poll` | `read` | publication id | remote processing/public status | publication:read | none | publication id | Status updates are monotonic except explicit retry/revocation |

## Mandatory action-state transitions

```text
request accepted → queued → running
                         ├─→ awaiting_external → running
                         ├─→ awaiting_review → running
                         ├─→ failed_retryable → queued (resume)
                         ├─→ failed_terminal
                         ├─→ cancelled
                         └─→ succeeded
```

An action may move to `succeeded` only after its QL audit has twelve canonical positions, a selected outcome, remaining uncertainty, and next ground. Read-only actions that merely retrieve existing state may set `audit_required=false` in `action_definition`; any read action that ranks, interprets, selects, or recommends remains auditable.

## Transaction classes

| Class | Actions | Boundary |
|---|---|---|
| Atomic SQL | identity, mapping patches, evidence links, approvals, returns | One database transaction. |
| Asset saga | ingest, generation, editing, rendering, export | Reserve run → produce temporary asset → hash/validate → register asset and derivation → commit result; cleanup unregistered temporary output on failure. |
| External saga | provider jobs and publication | Persist request and idempotency key before submission; preserve external job ID; poll/resume; never infer success from timeout. |

## Versioning

Action names are stable. Breaking input/output or semantic changes increment the action major version. Provider changes do not alter the action version unless the provider-independent contract changes. The runtime may support several action versions concurrently while an engagement is in production.
