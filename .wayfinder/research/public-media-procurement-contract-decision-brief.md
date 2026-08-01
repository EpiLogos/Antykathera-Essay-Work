# Public image and video procurement contract — decision brief

**Status:** research brief for the open human decision in [Make public image and video procurement first-class](../tickets/006-public-media-procurement-contract.md)  
**Prepared:** 2026-08-01  
**Decision owner:** Frank  
**Normative basis:** `SPEC.md` §§9, 13, and 17; the action catalogue, registry, payload schemas, PostgreSQL/SQLite contracts, and acceptance tests  
**Source-adapter basis:** [Production public-media source surface](public-media-source-surface.md)

## Recommendation

Replace the canonical `image.collect` action with a media-general **`media.collect`** action while keeping the canonical runtime at **66 actions**. Retain `image.collect@1.0.0` only as a declared, deterministic compatibility alias for image requests; it must resolve to `media.collect` before dispatch and must never own a second handler, gate policy, or transaction path.

Keep `source.ingest` unchanged in purpose. It ingests a native semantic source form into an engagement so that its arity, members, disclosure, and evidence can enter QL mapping. `media.collect` procures image/video material into the asset and provenance field. If an acquired asset should also become a semantic source, a later explicit `source.ingest` invocation may reference its immutable asset ID. Acquisition alone must not silently make stock footage a source member.

This option gives images and videos the same production-grade search, resolution, acquisition, rights, rejection, provenance, and storage lifecycle while retaining typed video-only rendition and clip fields. It avoids both a misleading image-only name and a duplicated `video.collect` implementation.

This is a recommendation, not the human decision. No normative file should be changed until Frank accepts the contract boundary.

## The smallest decision Frank must make

One yes/no choice settles the architecture:

> **May the one canonical procurement action be renamed from `image.collect` to `media.collect`, with the active registry remaining at 66 actions and `image.collect@1.0.0` retained only as a declared compatibility alias for image requests?**

**Recommended answer: yes.**

If the answer is no, Frank must choose either a 67th canonical action (`video.collect`) or accept that public video procurement remains hidden inside a contract whose name and present payload both say image.

## What the current contracts actually say

The present package has three materially different lanes:

| Current action | Existing meaning | Why it should remain distinct |
|---|---|---|
| `source.ingest` | Creates `source_form`, `source_member`, source assets, native arity/hash, and disclosure state before QL mapping. | It is semantic/evidentiary ingestion, not a public-stock search and licensing workflow. |
| `image.collect` | Searches/imports external image resources with rights requirements and returns asset and rights-record IDs. | This is already the procurement slot, but its name and payload omit video rendition, duration, and clip semantics. |
| `image.generate` / `video.submit` | Sends plans and references to generative providers and records candidate outputs/provider jobs. | Generation is optional and probabilistic; public-media acquisition is source retrieval with third-party rights and immutable source bytes. |

The current `image.collect` payload permits only `mode: search|import`, a free-form `rights_requirements` object, generic resources, and account fields. Its output contains loosely typed asset IDs, rights-record IDs, and rejected objects. The SQL `asset` row has only a rights-status string, a licence string, provider fields, and generic metadata; there is no relational acquisition, provider snapshot, rendition, append-only rights-assessment, rights-review, or rejection model. The current acceptance suite checks general asset rights and derivation but never proves real public image/video search, upstream resolution, full-file acquisition, temporal clipping, or rights refresh.

The contract therefore needs more than allowing `video/*` in the existing resource field.

## Option comparison

| Criterion | Add `video.collect` (67 canonical actions) | Replace with `media.collect` + compatibility | Keep 66 and use `source.ingest` subcontracts |
|---|---|---|---|
| Semantic clarity | Clear per medium, but duplicates one procurement lifecycle. | **Strongest:** one action names the shared lifecycle; media-kind branches remain typed. | Weak: semantic source ingestion and stock-asset procurement become one overloaded act. |
| Image/video parity | Requires discipline to keep two handlers aligned. | Shared by construction. | Shared only by a broad nested contract that the action name does not reveal. |
| Video-specific operations | Natural to add, but likely copied beside image rights logic. | Explicit video rendition/clip branches in a discriminated payload. | Buried under generic source/resource shapes. |
| Fixed action count | Breaks the fixed 66-action registry and 132-payload invariant. | **Preserves 66 canonical actions and 132 canonical payload schemas.** | Preserves 66. |
| API/CLI stability | Adds a new endpoint name/command; old image clients unchanged. | Canonical name changes, but a declared one-way compatibility alias preserves old image clients. | Existing names remain, but clients cannot discover procurement semantics cleanly. |
| Migration size | Registry/schema/generator/count changes plus new domain tables. | Registry rename, alias resolver, typed payloads, and new domain tables. | Payload and handler expansion plus the same domain tables; `source.ingest` migrations become riskier. |
| Rights/provenance model | Likely parallel code and schema relations. | One append-only evidence model for both media kinds. | Risks conflating evidence-source provenance with media licence provenance. |
| Idempotency | Two policies and potential duplicate download paths. | One acquisition identity and one content-addressed path. | Source hash does not naturally cover search, rendition resolution, rights version, and acquisition receipt. |
| Acceptance legibility | Separate image/video suites, plus parity tests. | One contract suite with shared tests and video-only branches. | Hard to prove whether a “source ingest” test exercised public procurement rather than ordinary file import. |
| Future audio/other media | Another action or another duplication decision. | Can extend only after an explicit supported-media decision. | Technically generic but semantically opaque. |
| Recommendation | Viable fallback if Frank values separate verbs above count/stability. | **Recommended.** | Reject for production procurement. |

## Why not add `video.collect`

Adding `video.collect` is honest and preferable to hiding video inside `source.ingest`, but it creates two public-provider orchestration paths for the same lifecycle:

```text
search → resolve fresh provider record → assess rights → choose rendition
       → acquire whole bytes → probe/hash/store → accept/reject → refresh rights
```

The only material video-specific extension is the rendition/time domain: duration, codec/container, FPS, and optional local clip selection. Those belong in typed branches, not in a duplicated rights, provenance, retry, account, rate-limit, and storage implementation.

It would also force a versioned change to every assertion that currently fixes 66 actions: the catalogue, generator guard, registry schema, registry instance, action payload index, generated SQL seeds, package validator, acceptance `ACT-012`/`BLD-013`/`BLD-015`/`BLD-017`, examples, CLI help, and specification. The cost is justified only if Frank wants image and video procurement to be separately permissioned, audited, or operationally owned. No current requirement creates that distinction.

## Why not overload `source.ingest`

`source.ingest` currently guarantees that a native source form and every source member exist before QL mapping. Its idempotency is the source hash, its output is a source-form identity plus member IDs, and its SQL destination is `source_form`/`source_member`. Public procurement has different intermediate states and failure meanings:

- a search candidate is not yet an asset or source member;
- a provider result must be freshly resolved before acquisition;
- a selected rendition has an external identity distinct from the downloaded content hash;
- a downloaded source may be retained for provenance while rights remain under review or are later rejected;
- a time-selected video clip must point to the whole acquired video and exact deterministic derivation;
- rights can change without changing the asset bytes;
- rejecting a media candidate is not removing a semantic source member.

Putting those states inside `source.ingest` would either fabricate source forms for browsing candidates or hide the actual procurement state in generic JSON. It would also expand the security surface of a foundational QL/source action and make acceptance ambiguous.

## Proposed canonical action

### Registry entry

```yaml
- name: media.collect
  version: 1.0.0
  side_effect: write
  permissions: [asset:collect]
  provider_dependencies: [media_source_capability]
  audit_required: true
  transaction_class: asset_saga
  idempotency_policy: operation + provider identity + rendition identity + rights-policy hash + source/derivation hash
  retry_policy:
    max_attempts: 3
    backoff: exponential_jitter
    resume: true
  success_condition: >-
    Search/resolve evidence is immutable; acquired whole source bytes are in controlled
    content-addressed storage; rights state is explicit; any selected clip is linked by
    deterministic derivation; rejected candidates remain auditable.
```

The action is `write` even for search because a conforming search persists the request hash, provider/version, raw response snapshot hash, normalized candidates, expiry/cache information, and action evidence. A candidate returned only in transient UI memory is not production evidence.

### Operation model

Use one strict JSON Schema with a required discriminator and `oneOf` branches:

```text
operation:
  search
  resolve
  acquire
  refresh_rights
  review_rights
  reject
```

Clip selection is an optional video-only part of `acquire`, not a provider operation. The runtime first downloads, probes, and hashes the complete rendition, then creates the clip locally as a deterministic asset derivation. `video.edit` remains the later creative/editorial operation; acquisition clipping is only the precise selection of a source interval.

### Common request fields

```json
{
  "engagement_id": "uuid",
  "operation": "search|resolve|acquire|refresh_rights|review_rights|reject",
  "media_kind": "image|video",
  "disclosure": "secret|private|shared|public",
  "rights_policy_ref": {
    "profile_id": "public-media-default",
    "version": "1.0.0",
    "content_hash": "sha256"
  },
  "external_account_access": false,
  "account_ref": null
}
```

The envelope already carries actor, request, session, engagement, idempotency, and approval mode. Credentials never enter the payload; `account_ref` resolves through the secret/account boundary.

### `search` request and result

```json
{
  "engagement_id": "uuid",
  "operation": "search",
  "media_kind": "video",
  "source_profiles": [
    {"source": "pexels", "profile_version": "1.0.0"},
    {"source": "wikimedia-commons", "profile_version": "1.0.0"}
  ],
  "query": "two swans crossing on calm water",
  "filters": {
    "orientation": "portrait",
    "minimum_width": 1080,
    "minimum_duration_ms": 6000,
    "maximum_duration_ms": 60000,
    "safe_search": true
  },
  "rights_policy_ref": {
    "profile_id": "public-media-default",
    "version": "1.0.0",
    "content_hash": "sha256"
  },
  "disclosure": "private",
  "external_account_access": false,
  "account_ref": null
}
```

```json
{
  "search_id": "uuid",
  "request_hash": "sha256",
  "provider_snapshot_asset_ids": ["uuid"],
  "candidate_ids": ["uuid"],
  "provider_results": [
    {
      "source": "pexels",
      "capability_version": "1.0.0",
      "candidate_count": 20,
      "cache_expires_at": "date-time",
      "rate_limit": {"remaining": 197, "resets_at": "date-time"}
    }
  ],
  "warnings": []
}
```

Each candidate stores normalized browsing metadata plus the immutable raw provider-response asset. It is explicitly `not_acquired` and cannot be passed to a renderer.

### `resolve` request and result

```json
{
  "engagement_id": "uuid",
  "operation": "resolve",
  "media_kind": "video",
  "candidate_id": "uuid",
  "rights_policy_ref": {
    "profile_id": "public-media-default",
    "version": "1.0.0",
    "content_hash": "sha256"
  },
  "disclosure": "private",
  "external_account_access": false,
  "account_ref": null
}
```

```json
{
  "resolved_media_id": "uuid",
  "provider_snapshot_asset_id": "uuid",
  "resolved_at": "date-time",
  "expires_at": "date-time|null",
  "renditions": [
    {
      "rendition_id": "uuid",
      "provider_rendition_id": "foreign-id",
      "mime_type": "video/mp4",
      "width": 1920,
      "height": 1080,
      "duration_ms": 24000,
      "fps_num": 30000,
      "fps_den": 1001,
      "byte_length": 12345678
    }
  ],
  "rights_assessment_id": "uuid",
  "rights_status": "approved|review_required|rejected"
}
```

For Openverse, `resolve` must follow and snapshot the upstream source record; Openverse metadata alone can never produce an approved resolution. Openverse with `media_kind: video` fails capability validation before a network request.

### `acquire` request and result, including video clip selection

```json
{
  "engagement_id": "uuid",
  "operation": "acquire",
  "media_kind": "video",
  "resolved_media_id": "uuid",
  "rendition_id": "uuid",
  "expected_resolution_snapshot_sha256": "sha256",
  "clip_selection": {
    "start_ms": 3500,
    "end_ms": 11500,
    "audio_policy": "preserve|mute|replace",
    "transform_profile": {
      "profile_id": "public-video-clip",
      "version": "1.0.0",
      "content_hash": "sha256"
    }
  },
  "storage_policy": "controlled_local|object_store",
  "rights_policy_ref": {
    "profile_id": "public-media-default",
    "version": "1.0.0",
    "content_hash": "sha256"
  },
  "disclosure": "private",
  "external_account_access": false,
  "account_ref": null
}
```

```json
{
  "acquisition_id": "uuid",
  "source_asset_id": "uuid",
  "source_sha256": "sha256",
  "source_probe": {
    "mime_type": "video/mp4",
    "duration_ms": 24000,
    "width": 1920,
    "height": 1080,
    "fps_num": 30000,
    "fps_den": 1001
  },
  "derived_clip_asset_id": "uuid",
  "derivation_id": "uuid",
  "derived_sha256": "sha256",
  "effective_clip": {"start_ms": 3500, "end_ms": 11500},
  "rights_assessment_id": "uuid",
  "rights_status": "approved|review_required|rejected",
  "attribution_record_id": "uuid"
}
```

The request supplies semantic clip parameters and a versioned transform profile, not raw shell arguments. The result/derivation record stores the exact escaped FFmpeg invocation, FFmpeg version, probe reports, input/output hashes, and effective frame/time boundaries. Validation requires `0 <= start_ms < end_ms <= probed source duration`.

The whole source asset is always acquired and hashed before the clip. A remote URL with a time fragment is not a source asset.

### Rights refresh, human review, and rejection

```json
{
  "engagement_id": "uuid",
  "operation": "refresh_rights",
  "media_kind": "image",
  "acquisition_id": "uuid",
  "rights_policy_ref": {
    "profile_id": "public-media-default",
    "version": "1.0.0",
    "content_hash": "sha256"
  },
  "disclosure": "private",
  "external_account_access": false,
  "account_ref": null
}
```

```json
{
  "engagement_id": "uuid",
  "operation": "review_rights",
  "media_kind": "image",
  "rights_assessment_id": "uuid",
  "decision": "approve|reject",
  "decision_basis": "asset-specific review notes",
  "permitted_uses": ["internal_reference", "rendered_card", "public_web", "print"],
  "required_attribution_targets": ["web_details", "video_credits", "print_back", "package_ledger"],
  "approval_id": "uuid",
  "disclosure": "private",
  "external_account_access": false,
  "account_ref": null
}
```

```json
{
  "engagement_id": "uuid",
  "operation": "reject",
  "media_kind": "video",
  "target": {"kind": "candidate|resolved_media|acquisition", "id": "uuid"},
  "reason_codes": ["rights_conflict", "third_party_risk"],
  "rationale": "The upstream record contains an unresolved third-party credit.",
  "disclosure": "private",
  "external_account_access": false,
  "account_ref": null
}
```

Refresh creates a new append-only rights assessment; it never overwrites the acquisition-time record. Rejection creates an immutable rejection record and audit delta. Acquired bytes may remain in restricted provenance storage under retention policy, but rejected media cannot become a reference, plate, rendition, or export input.

## Required provider and data subcontracts

The action should call one source-neutral adapter interface:

```text
search(request) -> candidate page + raw response
resolve(provider_media_id) -> fresh media/renditions/rights snapshot
acquire(resolved_media, rendition_id, sink) -> streamed bytes + transport receipt
refresh_rights(acquisition) -> fresh rights snapshot
```

Pexels, Pixabay, Wikimedia Commons, and NASA implement image and video where available. Openverse implements image discovery only and must delegate final resolution to its upstream source. Imported or commissioned files use a local/import adapter with supplied rights evidence. Generated assets remain outside this contract.

The existing `provider_capability` contract is generation-shaped: it requires model IDs, duration/reference limits, and operations such as generate/edit/continue. Do not fake model identities for Pexels or NASA. Add a versioned `media_source_capability` contract/table (or version the provider-capability union) containing:

```text
source/profile/version/status/checked_at
supported_media_kinds
operations: search|resolve|acquire|refresh_rights
authentication mode and account scope
query/filter/page limits
rate-limit/cache/concurrency policy
rendition metadata support
rights metadata fields and upstream-authority rules
hotlink/storage requirements
terms snapshot reference
health/probe evidence
```

## Relational migration

Keep `asset` and `asset_derivation` as the immutable byte and derivation spine. Add normalized, append-only procurement tables in both PostgreSQL and portable SQLite where the records are part of a carried card:

```text
media_source_capability
media_search
media_candidate
media_provider_snapshot
media_resolution
media_rendition
media_acquisition
rights_assessment
rights_review
attribution_record
media_rejection
```

Minimum relationships:

```text
media_search 1─* media_candidate
media_candidate 1─* media_resolution
media_resolution 1─* media_rendition
media_resolution 1─* rights_assessment
media_acquisition → media_resolution + media_rendition + whole-source asset
rights_assessment 1─* rights_review
media_acquisition 1─* refreshed rights_assessment
attribution_record → rights_assessment + creator/source/licence facts
media_rejection → candidate | resolution | acquisition
derived clip asset ─asset_derivation→ whole-source asset
```

Provider metadata and Epi-Card interpretation remain separate. `media_provider_snapshot` points to a content-addressed JSON asset containing the raw response; normalized columns support policy and queries. Symbolic tags, QL addresses, and Pasu allusions belong to card annotations, never provider title/creator/licence fields.

The current `asset.rights_status` and `asset.licence` may remain an immutable acquisition-time summary for compatibility, but canonical rights decisions must resolve through linked assessments/reviews. Rights status can change while bytes and SHA-256 do not; mutating an asset row would violate §12.4.1.

## Registry and compatibility migration

Recommended contract migration:

1. Version the specification/contracts package (recommended contract revision `1.1.0`; product remains v1).
2. Replace `image.collect` with `media.collect` in §9.5, the action catalogue, generator policy sets, expected-name sets, CLI reference, Agent Skill, and studio labels.
3. Keep `action_count: 66`; generate exactly 66 active definitions and 132 active payload schemas.
4. Replace `image_collect_input/output` with strict `media_collect_input/output` schemas and their normalized shared definitions.
5. Add a validated action-alias registry and SQL `action_alias` table. An alias row names alias/version, canonical action/version, deterministic transform version, introduced/sunset versions, and status.
6. Resolve the alias before permission, gates, idempotency, and handler dispatch. Persist both requested alias/version and canonical action/version on the action run or its immutable request metadata.
7. The legacy transform accepts only the old image payload, sets `media_kind: image`, maps `mode: search` to `operation: search`, and maps `mode: import` to a local resolve/acquire request. Ambiguous legacy imports fail with a migration error rather than guessing rights or provider identity.
8. The alias uses the canonical `media.collect` permission, gates, transaction class, retry policy, audit, and implementation. It is not counted as a 67th action.
9. Update `BLD-010` to permit only aliases present in the validated alias registry; undeclared mutating names remain forbidden.
10. Preserve historical `image.collect` action definitions if a database already contains referenced action runs. Mark them inactive/retired through a new definition-status field rather than deleting FK targets. Clean v1 deployments need only the alias row and active 66 definitions.

The generic HTTP route `/actions/{actionName}` does not need a new endpoint. The CLI changes canonically from `epicard image collect` to `epicard media collect --kind image|video`; the old image command prints a deprecation warning on stderr while preserving JSON stdout and exit-code behaviour.

## Gate and policy consequences

The current `image.collect` gate checks only external-account authorization. The canonical media action needs:

- the same conditional account-authorization gate for credentialed sources;
- fresh source-resolution and URL/SSRF validation before any download;
- a pre-promotion human review when rights are `review_required` or when the requested promotion is an approved reference/plate;
- immutable rejection when rights are prohibited;
- rights-manifest validation on `plate.accept`, public render, package, and publication so later actions cannot rely on an old boolean;
- licence/attribution targets matched to the actual output profiles.

The fixed 22-predicate registry can remain unchanged if the existing `promotion.requested`, `disclosure.scope_in`, and `approval.matches_payload` predicates are used with exact rights-manifest hashes and approval types. URL policy and hash/probe checks are deterministic domain validation, not discretionary approvals. If implementation proves those predicates cannot express an exact rights set, the predicate registry must be versioned rather than smuggling the decision into prose.

Acquisition may succeed with `rights_status: review_required` because retaining source bytes and evidence is not approval for canonical/public use. Promotion, rendering, packaging, and publication must remain blocked until the relevant immutable rights assessment/review is approved.

## Real acceptance evidence to add

No release proof may replace providers, HTTP transfer, object storage, FFmpeg, or the rights database with mocks. Unit tests may exercise pure parsers and validators, but the following release tests require real functionality and immutable evidence:

| Proposed ID | Procedure | Pass condition |
|---|---|---|
| `MED-001` | Invoke canonical `media.collect` through library, CLI, HTTP, and studio. | All surfaces resolve the same registry version/handler and return schema-equivalent envelopes. |
| `MED-002` | Invoke legacy `image.collect@1.0.0` with a real image search/import. | Alias and canonical invocation produce the same normalized request hash/result identity; no second handler or action definition is used. |
| `MED-003` | Search active Pexels, Pixabay, Wikimedia Commons, and NASA adapters for image and video where supported. | Live responses are normalized and preserved byte-for-byte as content-addressed snapshots with adapter/version, request, timestamp, cache, and rate-limit evidence. |
| `MED-004` | Search Openverse for images, then resolve an accepted candidate upstream. Attempt Openverse video search. | Image acquisition records both hops and upstream rights authority; video fails capability validation before network dispatch. |
| `MED-005` | Acquire one real public image and one real public video rendition. | Whole bytes are streamed into controlled storage, probed, hashed, and disconnected from expiring/hotlinked URLs; source and acquisition receipts agree. |
| `MED-006` | Acquire the same rendition twice concurrently. | One content-addressed source asset is stored; separate requested relations/audits remain; no duplicate or partial canonical object exists. |
| `MED-007` | Interrupt a real video download, resume/retry, and corrupt one completed transfer. | Resume follows policy; partial files never become canonical; corruption fails expected hash/probe checks. |
| `MED-008` | Select a valid interval from a real acquired video and derive it twice with pinned FFmpeg/profile versions. | Whole source remains registered; both clip renders have the same hash in the same environment/profile; exact derivation and effective frames resolve. |
| `MED-009` | Request negative, reversed, zero-length, and out-of-bounds video intervals. | Validation fails before derivation and creates no output asset. |
| `MED-010` | Acquire records with approved, review-required, conflicting, removed, and unknown rights. | Append-only assessments retain source evidence; only approved use proceeds; unknown/conflicting/removed cases block canonical/public use. |
| `MED-011` | Refresh rights after an upstream licence/record change. | Acquisition-time assessment remains immutable; new assessment is linked; affected approvals/renditions become stale or blocked according to policy. |
| `MED-012` | Reject candidates before and after acquisition. | Rejection reason/audit persists; rejected media cannot become a reference/plate; retained bytes follow restricted retention policy. |
| `MED-013` | Render/package a work requiring attribution. | Web details, video credits, print back, OKF, and package ledger carry the required creator/source/licence data without leaking prohibited originals. |
| `MED-014` | Attempt public render/package with only a colour hue, crop, or resize of a Pixabay source. | Thin-transform policy routes to rights review and does not assume a conforming new creative work. |
| `MED-015` | Attempt acquisition from loopback, link-local, private-network, redirect-to-private, oversized, MIME-spoofed, and decompression-bomb resources. | URL/content policy blocks unsafe transfers with no internal response disclosure or canonical asset. |
| `MED-016` | Build `.epicard` from acquired media and inspect its closure. | Final derivatives and attribution/provenance ledger are present; stock originals are excluded unless the exact licence/package policy permits them. |
| `MED-017` | Use a collected asset as a semantic source. | No `source_form` exists after acquisition alone; explicit `source.ingest(asset_id)` creates the source form and preserves acquisition provenance. |
| `MED-018` | Disable every generative image/video adapter and complete `E2E-001`. | Real public/imported media still produce actual base and extended video renditions with full provenance. |

Provider-specific live tests should run only for adapters advertised as active and should respect their real quotas and terms. A provider outage can block that adapter's support evidence without invalidating the source-neutral runtime; it cannot be converted to a passing mocked result.

## Migration impact by option

### Recommended: `media.collect` + compatibility

- **Normative:** minor contract/spec revision; action count remains 66.
- **Generated artifacts:** regenerate registry, 132 payload schemas, PostgreSQL/SQLite action seeds, validation report, file manifest, TypeScript/CLI surfaces.
- **Database:** add procurement/rights tables and alias metadata; preserve immutable historical action definitions if any exist.
- **Runtime:** one adapter orchestration and asset-saga implementation; image/video branches share all non-temporal logic.
- **Clients:** canonical command/name changes; legacy image-only calls transform deterministically during a published compatibility window.
- **Tests:** add the real `MED-*` suite and update count/name/alias assertions.

### Alternative: add `video.collect`

- **Normative:** action registry becomes 67 and payload set becomes 134; every fixed-count assertion changes.
- **Database/runtime:** same procurement/rights tables, plus separate action definition, schemas, gate/retry policy, handler entry, command, and parity responsibility.
- **Clients:** least disruptive for existing image users.
- **Tests:** full image/video parity suite is mandatory to prevent semantic drift.

### Rejected: `source.ingest` typed acquisition subcontracts

- **Normative:** action count remains 66, but a foundational source contract changes meaning and version.
- **Database/runtime:** same procurement/rights tables plus complex conditional writes across source and asset aggregates.
- **Clients:** action name remains stable while behaviour becomes substantially less predictable.
- **Tests:** every source-ingestion, QL-mapping, rights, procurement, and failure path must prove that candidates do not accidentally become semantic members.
- **Risk:** highest domain coupling and least legible audit trail.

## Resulting boundary in one line

```text
media.collect procures and rights-governs immutable media;
source.ingest deliberately admits selected material into the semantic source field;
image.generate/video.submit create optional provider candidates;
video.edit/modifier.apply/composition.render transform accepted assets deterministically.
```

