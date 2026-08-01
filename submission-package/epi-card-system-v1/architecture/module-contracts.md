# Epi-Card Module Contracts and Dependency Rules

**Version:** 1.0.0  
**Normative relation:** supplements `SPEC.md` §30.

This file fixes module ownership and dependency direction. A package may not reach around another package's public interface to write its tables, mutate its assets, or reproduce its rules.

## Dependency direction

```text
apps/studio ─┐
apps/gallery ├─→ card-component / action-client
apps/worker ─┘

cli / HTTP adapter / Agent Skill
             ↓
          actions
             ↓
 ┌───────────┼──────────────────────────────────────────────────────┐
 domain   profiles   projections   locks   ql   audit   resonance   assets
                                      ↓          ↓        ↓          ↓
                          correspondences  symbols  audio  providers
                                      └────→ render-remotion / render-print
                                                   ↓
                                         okf-export / packaging
             └──────────────────→ validation ←─────┘
                                  ↓
                              database
```

`domain` has no product-package dependency. `database` depends on `domain` types and migrations only. UI packages depend on read projections and action clients, never database repositories.

## Module registry

| Module | Owns | Public exports | Allowed dependencies | Forbidden responsibilities |
|---|---|---|---|---|
| `packages/domain` | IDs, enums, value objects, domain errors, disclosure and status types | TypeScript types, codecs, pure value validators | standard library and schema runtime | SQL, providers, rendering, prompts, UI |
| `packages/database` | PostgreSQL/SQLite migrations, repositories, transactions, outbox/events, row-level disclosure filters | repository interfaces, unit-of-work, migration runner | `domain` | semantic mapping, provider calls, media transforms |
| `packages/profiles` | configuration profiles, profile sets, profile membership, hashes, effective dates, profile resolution | profile registry, set resolver, compatibility/diff validators | `domain`, `database` | interpreting a profile outside its owning semantic module; hidden environment-only symbolic configuration |
| `packages/projections` | immutable private/shared/public/provider engagement snapshots, redaction receipts, provider disclosure manifests | materialise, validate, approve, resolve projection | `domain`, `profiles`, `database`, `assets` read interfaces | ad hoc provider/public data assembly; provider submission; rendering |
| `packages/locks` | persisted object/field/asset locks, conflict resolution, expiry, release history | acquire, release, list, assertMutable | `domain`, `database` | silently overriding a lock; mutating the protected target |
| `packages/actions` | action registry, all action input/output payload schemas, action envelopes, permission checks, named gate predicates, idempotency, job state, saga orchestration | `invoke`, `resume`, `cancel`, `inspect`, registry/payload loaders, gate evaluator, action metadata | all domain services through interfaces; `database` | inferring gates from prose; duplicate provider logic; UI-specific behaviour |
| `packages/ql` | canonical 12 addresses, traversal, relations, source mapping, occupancy, frame validation, return shape | frame initializer, mapper interfaces, relation builder, validators | `domain`, `profiles`, `database` repository interfaces, `audit` interface | colour/audio/video decisions; Bimba-map dependency |
| `packages/audit` | 12-position decision audits, nested audit tree, evidence attachment, completion rules | audit templates, writer, validator, projection | `domain`, `database`, `ql` canonical-address constants | hidden chain-of-thought storage; flat rationale substitution |
| `packages/correspondences` | versioned astrology/element/chakra/colour/type and cross-register rules | profile loader, rule evaluator, profile diff, provenance | `domain`, `database` | hard-coded renderer values; unversioned prompt mappings |
| `packages/resonance` | Φ contribution model, aggregation, ratio normalisation, modality projection receipts | aggregate, project, compare, verify | `domain`, `correspondences`, `database` | calling image/video/audio providers; interpreting raw sky without a profile |
| `packages/assets` | content-addressed store, SHA-256, metadata, rights, disclosure, derivation graph, temp-file promotion | put/get/stat/derive/export APIs | `domain`, `database`, object-store driver | deciding semantic acceptance; mutating an existing digest |
| `packages/symbols` | symbol bank, grammar, search, SVG construction/sanitisation, state derivation, alpha/mask plan | search/propose/canonicalise/render-state/validate | `domain`, `ql`, `resonance`, `assets`, provider interface | final video composition; approving its own canonical revision |
| `packages/audio` | QL Resonator parameter model, Faust invocation, tuning, 12 states, spectral analysis, mix plans | palette resolver, renderer, analyser, loop validator | `domain`, `ql`, `resonance`, `assets` | choosing visual art direction; treating provider audio as canonical tuning |
| `packages/providers/core` | provider capability registry, adapter interface, request/response normalisation, external job persistence | capability lookup, submit/poll/resume/cancel | `domain`, `assets`, `database` | silently clipping requests to provider limits |
| `packages/providers/seedance` | Seedance-specific request mapping and response decoding | `VideoProviderAdapter` implementation | `providers/core` | owning storyboard meaning or final composition |
| `packages/providers/image` | selected image generation/edit/background-removal adapters | `ImageProviderAdapter` implementations | `providers/core` | canonical SVG authority |
| `packages/providers/transcription` | STT/diarisation adapters | `TranscriptionProviderAdapter` implementations | `providers/core` | editing transcript meaning or QL mapping |
| `packages/providers/publication` | upload/status/delete adapters | `PublicationAdapter` implementations | `providers/core` | publication approval decisions |
| `packages/render-remotion` | deterministic scene composition, exact layers, output profiles, render logs | render plan compiler and renderer | `domain`, `assets`, `symbols`, `audio` | generating semantic content; uploading output |
| `packages/render-print` | physical card layout, colour/bleed/safe-area/QR checks, PDF output | print renderer and proof validator | `domain`, `assets`, `symbols` | changing card semantics or QR target |
| `packages/card-component` | `<epi-card>` state machine, front/back/hex UI, read projection, accessibility | custom element, framework wrappers, events | `domain` read DTOs, browser media APIs | direct database access; automatic write actions |
| `packages/okf-export` | OKF v0.2 wiki tree, frontmatter mapping, links, provenance/trust/lifecycle/attestation export | exporter, validator, disclosure variants | `domain`, repositories through read interfaces, `assets` | operational state; replacing SQL |
| `packages/packaging` | `.epicard` assembly/import, normative manifest, package-relative path policy, file closure, root digest, offline SQLite/assets/rendition/OKF carriage | package builder, manifest writer/validator, importer, conflict/remap plan | `domain`, `database`, `assets`, `projections`, `okf-export`, render read interfaces, `validation` | mutating canonical assets; ad hoc disclosure assembly; accepting unlisted or traversal paths |
| `packages/validation` | structural, semantic, media, package and export validators; report/finding format | validator registry, report runner, receipts | pure read interfaces across packages | mutating target state or approving it |
| `packages/cli` | command parsing, request file loading, stdout/stderr discipline, exit codes | `epicard` executable | `actions`, action client | alternate business logic; interactive prompts in agent mode |
| `apps/worker` | queue consumption, resource scheduling, process supervision | worker entrypoint | `actions`, render/provider/audio packages | domain decisions outside actions |
| `apps/studio` | production workspace, agent stream, revisions, reviews, locks, approvals | web application | action HTTP/client and read projections | direct SQL writes; local copies of domain logic |
| `apps/gallery` | public card routes, public projections, share/embed pages | web application | public read service, `card-component` | accessing private data at render time |

## Required interfaces

```ts
export interface RepositoryUnitOfWork {
  transaction<T>(fn: (repos: Repositories) => Promise<T>): Promise<T>;
}

export interface ActionRegistry {
  invoke(request: ActionRequest): Promise<ActionResult>;
  resume(runId: string, actor: ActorContext): Promise<ActionResult>;
  cancel(runId: string, actor: ActorContext): Promise<void>;
  inspect(runId: string, actor: ActorContext): Promise<ActionResult>;
}

export interface GatePredicateRegistry {
  evaluate(call: GatePredicateCall, context: GateEvaluationContext): Promise<boolean>;
  definition(name: string): GatePredicateDefinition;
}

export interface GateEvaluator {
  evaluate(action: ActionDefinition, stage: GateStage, context: GateEvaluationContext): Promise<GateDecision[]>;
  assertPass(decisions: GateDecision[]): void;
}

export interface ProviderAdapter<Request, NativeResponse> {
  capability(): ProviderCapability;
  validate(request: Request): ValidationFinding[];
  submit(request: Request, context: ProviderContext): Promise<ProviderJob>;
  poll(job: ProviderJob, context: ProviderContext): Promise<ProviderPollResult<NativeResponse>>;
  resume?(job: ProviderJob, context: ProviderContext): Promise<ProviderPollResult<NativeResponse>>;
  cancel?(job: ProviderJob, context: ProviderContext): Promise<void>;
}

export interface ContentAddressedStore {
  stage(source: ReadableSource): Promise<StagedAsset>;
  commit(staged: StagedAsset, metadata: AssetMetadata): Promise<Asset>;
  open(assetId: string, disclosure: DisclosureContext): Promise<ReadableSource>;
  verify(assetId: string): Promise<HashVerification>;
}
```

## Write authority

Only the shared action layer may coordinate writes spanning more than one module. Every mutating action invokes `LockService.assertMutable` before side effects and obtains an approved projection before any disclosure-scoped provider or public operation. Individual modules may write their own aggregate through a repository passed by the action transaction. Provider callbacks are converted to action events before any domain mutation.

## Event authority

All action events carry `run_id`, monotonically increasing `sequence_no`, timestamp, event type, and JSON payload. UI clients treat the sequence as authoritative and reconnect with `after=<last sequence>`. Providers do not emit directly to the user interface.

## Lock authority

Locks are rows owned by the action/domain layer. A module must ask `LockService.assertMutable(target)` before writing a protected field or selecting an asset. There is no local “force” flag. Unlocking is itself an approved action.

## Configuration authority

- Environment variables contain deployment and secret references only.
- Symbolic correspondences, rendering profiles, provider capabilities, validator thresholds, and audio tunings are versioned records/files loaded through their owning package.
- Prompts may reference configuration; they may not be the sole location of configuration.
- A frozen rendition records every profile and implementation version that influenced it.
