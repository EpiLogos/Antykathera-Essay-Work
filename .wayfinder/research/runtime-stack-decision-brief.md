# Runtime stack and workspace foundation — decision brief

Research date: 2026-08-01

Status: decision support for the HITL ticket **Choose the runtime stack and workspace foundation**. This brief recommends a choice; it does not make Frank's decision or resolve the ticket.

## The decision in one sentence

The smallest decision is whether the single authoritative Epi-Card action/domain engine should be **strict TypeScript on Node.js 24 LTS** (recommended), so the CLI, HTTP boundary, workers, Remotion renderer and browser contracts share one language and generated contract set, or whether v1 should accept a permanent native-core/TypeScript boundary.

If Frank approves the TypeScript engine, the rest of the recommended foundation can be adopted as one coherent consequence rather than grilled as a dozen independent preferences.

## Fixed ground recovered from the specification

The stack does not get to choose or reinterpret these constraints:

- PostgreSQL 18+ is operational truth; SQLite 3.45+ plus package-local content-addressed files is the portable/offline store.
- Exactly 66 registered action definitions, 132 payload schemas and 22 named gate predicates drive every agent, CLI, HTTP, studio and test invocation.
- One action implementation owns cross-module writes, idempotency, resumption, approvals, event sequencing and saga state.
- All mutable semantic/creative objects are revisioned; approved revisions and SHA-256 assets are immutable.
- Remotion plus FFmpeg is the reference deterministic compositor; Faust is the canonical audio engine.
- The public card is a framework-neutral `<epi-card>` custom element even if studio and renderer use React.
- The fixed package ownership and dependency direction in `architecture/module-contracts.md` remain intact.
- Tests execute real PostgreSQL, SQLite, object storage, workers, browsers, CLI, Remotion, FFmpeg, Faust, offline package round-trip and print proof. A mocked substitute cannot become release evidence.

The architectural pressure is therefore not generic “full-stack application” selection. It is keeping one action/domain implementation while coordinating SQL, browsers, deterministic media subprocesses, portable packages and external providers.

## Current workspace facts

There is no prior application stack to preserve:

- The repository still has no Git `HEAD`; every file is untracked. No implementation branch can be isolated until the version-control baseline is authorised.
- No `package.json`, lockfile, workspace file, `Cargo.toml`, `go.mod`, `pyproject.toml`, application source tree or migration runner exists under the Epi-Card package.
- Installed foundations are Node.js `24.16.0`, pnpm `10.25.0`, Python `3.13.0`, SQLite `3.51.0`, FFmpeg/ffprobe `8.1.1`, Docker `29.2.1`, Rust `1.94.0`, Go `1.24.4`, and Bun. The Node project currently identifies v24 as LTS and recommends LTS lines for production ([official Node release page](https://nodejs.org/en/about/previous-releases)).
- `faust` and `psql` are not currently installed. PostgreSQL 18 and MinIO can be exercised through Docker, but Faust provisioning is an explicit foundation task.
- The existing Python registry/payload generators and specification validator are real normative build inputs. They should remain callable in the workspace until a replacement demonstrates byte-identical output; rewriting them is not required to begin the runtime.

This is genuinely greenfield at the application layer. Choosing a second backend language now would be an adopted architectural cost, not an inherited necessity.

## Option A — TypeScript/Node monorepo (recommended)

### Exact foundation

| Concern | Choice |
|---|---|
| Production language/runtime | Strict TypeScript compiled to ESM on pinned Node.js 24 LTS |
| Workspace/package tool | pnpm workspaces with one frozen lockfile; Turborepo for the build/test task graph and cache |
| Contract runtime | AJV Draft 2020-12 loads the normative registry and JSON Schemas; generated TypeScript types are build artefacts, never alternate schemas |
| Server | Fastify action/read service with JSON Schema validation, OpenAPI adapter, SSE action-event stream and explicit auth/projection hooks |
| CLI | Bundled Node executable using Commander for parsing; all commands invoke the same `packages/actions` entry point or action client |
| Studio/gallery | React + Vite applications; no domain logic in React state |
| Public card | Lit-based standards custom element backed by a framework-free TypeScript state machine; React wrappers only adapt props/events |
| Database access | Kysely repository layer over `pg` and `better-sqlite3`; dialect-specific SQL remains private to `packages/database` |
| Migrations | Umzug as the runner for checksum-pinned, paired PostgreSQL/SQLite SQL migrations; checked-in bootstrap snapshots remain synchronised and are tested both from empty and by upgrade path |
| Queue | The normative `action_run`/`action_event` state is the durable queue. A shared `RunQueue` port uses PostgreSQL leases plus `FOR UPDATE SKIP LOCKED` in collaborative/hosted profiles and a single-process SQLite lease/poller locally. No Redis or shadow job truth in v1. |
| Object storage | `ContentAddressedStore` with local-filesystem and S3-compatible drivers; AWS S3 client against MinIO in real integration tests |
| Media | Remotion/React package plus supervised FFmpeg/ffprobe and Faust processes; binary/tool versions enter rendition and test evidence |
| Unit/integration tests | Vitest for pure and process-level tests; Testcontainers for real PostgreSQL 18 and MinIO; actual file-backed SQLite for portable tests |
| Browser tests | Playwright for Chromium/Firefox/WebKit development coverage, plus current macOS Safari through `safaridriver`/WebDriver for the normative Safari-family acceptance lane |
| CLI/media/print acceptance | Spawn the built `epicard` executable; invoke real Remotion, FFmpeg, ffprobe and Faust; rasterise/inspect print PDFs at 300 dpi and retain produced evidence |

### Why this fits the fixed product

Remotion already makes Node/React a required production build and render surface. The browser custom element and its declared TypeScript contract create another TypeScript surface. Keeping the action engine, schemas, CLI, HTTP boundary and workers in the same language eliminates a cross-language copy of every action envelope, payload, canonical QL address, event, gate and error.

Node is not being asked to implement codecs or DSP. CPU-heavy work runs in isolated Remotion, FFmpeg and Faust worker processes; Node owns orchestration, validation, durable state and streams. Worker processes are split by declared resource class and concurrency, so an encode cannot block the action service event loop.

The database-backed queue follows the schema's existing authority. `action_run` already contains the state machine, idempotency identity, retry metadata, provider resume cursor and output. `action_event` already owns ordered progress. Adding queue name/resource class, availability, lease owner/expiry, heartbeat and attempt fields through paired migrations is less risky than reconciling those records with BullMQ/Celery/another queue's separate state. PostgreSQL supplies concurrent claiming; SQLite keeps the specified single-worker profile.

### Costs and controls

- A TypeScript type can appear safer than the database actually is. The control is real dual-database integration testing, parameterised repositories, runtime schema validation and database constraints—not an ORM-generated schema.
- Native media subprocess supervision needs deliberate cancellation, timeout, log redaction, temp-file promotion and orphan cleanup. Those behaviours are product requirements anyway and belong in `apps/worker` plus `packages/assets`.
- `better-sqlite3` is a native dependency. Pin it and build/test it on every release OS; do not substitute an in-memory database.
- React plus Lit is two view libraries, but they do not own the same surface: React owns studio/gallery composition and Remotion; Lit owns the public custom element. One framework-free card state machine prevents semantic duplication.
- Turborepo does not enforce package direction. Add TypeScript project references, package `exports`, ESLint restricted imports and a dependency-boundary test generated from `module-contracts.md`.

## Option B — Rust operational core plus TypeScript media/web

### Exact foundation

| Concern | Choice |
|---|---|
| Core | Rust Cargo workspace; Axum server, Clap CLI, Tokio workers, SQLx repositories, native SQL lease queue |
| Web/media workspace | pnpm workspace for React/Vite studio/gallery, Lit `<epi-card>`, and Remotion renderer |
| Contracts | Normative JSON Schemas generate/validate both Rust and TypeScript DTOs; HTTP/JSONL is the process boundary |
| Migrations | SQLx/refinery-style paired raw SQL migrations with PostgreSQL and SQLite upgrade tests |
| Tests | Rust unit/integration plus Testcontainers; TypeScript browser/render tests; black-box cross-runtime contract and CLI tests |

### Advantages

- Strong process supervision, bounded concurrency and a compact distributable CLI/worker binary.
- Excellent control over streaming, hashes, files, ZIP assembly and long-running worker recovery.
- SQLx can catch more SQL/type mismatches in the core build than a dynamic Node driver.

### Costs

- Node remains mandatory for Remotion, React and the browser component, so Rust does not remove the JavaScript production surface.
- Every one of the 66 actions, 132 payload types, 22 gates, event envelopes and read DTOs crosses a generated Rust/TypeScript boundary. The schemas prevent arbitrary divergence, but generated types, error mappings and Unicode-prime handling must be tested twice.
- The CLI can call Rust actions directly, while studio/render workers call through HTTP or a process protocol. This makes “same implementation” achievable but introduces a boundary at precisely the product's most interconnected layer.
- Development and CI matrices grow before any Epi-Card capability exists. The benefit appears mainly under worker load or packaging performance that has not yet been demonstrated as a Node bottleneck.

### When to choose it

Choose this only if Frank values a native authoritative CLI/core enough to accept the permanent two-language contract boundary in v1. It is a viable production architecture, but not the shortest route to complete acceptance.

## Option C — Go operational core plus TypeScript media/web

### Exact foundation

| Concern | Choice |
|---|---|
| Core | Go workspace; `net/http`/Chi action service, Cobra CLI, pgx PostgreSQL driver, SQLite driver, SQL lease workers |
| Web/media workspace | The same pnpm React/Vite, Lit and Remotion workspace as Option A/B |
| Contracts/migrations | Generated Go/TypeScript DTOs from normative schemas; golang-migrate-style paired raw SQL migrations |
| Tests | Go test plus real containers/files, then TypeScript browser/media lanes and black-box end-to-end tests |

### Advantages

- Simple deployment binaries, good process/network concurrency and straightforward operational profiling.
- Lower native-build complexity than Rust while retaining a strong worker/server runtime.

### Costs

- The same permanent Go/TypeScript schema and action boundary as Option B, with less type-level expression for the QL/profile algebra than either strict TypeScript or Rust.
- Remotion, React, Lit and browser types still require the pnpm workspace, so Go adds rather than replaces a toolchain.
- The current workspace has no Go implementation to preserve and no product requirement that benefits uniquely from Go.

### When to choose it

Choose this only if operating a small Go service/CLI binary is itself a governing deployment preference. Nothing currently recovered from the specification makes it the natural v1 default.

## Recommendation

Adopt **Option A: strict TypeScript on Node.js 24 LTS** as the one authoritative application runtime.

Use pnpm workspaces, Fastify, React/Vite, a Lit custom element, Kysely repositories, paired raw-SQL migrations under Umzug, a database-native `action_run` lease queue, Vitest/Testcontainers, and real-browser/media acceptance lanes. Pin exact dependency versions only when the initial lockfile is created; the decision should fix roles and boundaries, not copy today's package patch versions into product architecture.

This recommendation is not based on TypeScript being universally preferable. It follows the actual dependency shape: Node/React is already present at Remotion, TypeScript is already the public UI contract, and the product's central risk is duplicated action/domain logic. A native core introduces a permanent bridge before evidence shows that the orchestration layer needs native performance.

Do not choose Bun as the v1 production runtime. It can remain a developer experiment, but Node LTS is the compatibility reference for Remotion, the provider SDK surface and the acceptance toolchain. Do not add Redis/BullMQ in v1: the action tables and event stream are already authoritative job state, and the three required profiles can be served by PostgreSQL/SQLite lease adapters without a second durable truth.

## Implications for every fixed module

| Fixed module | Recommended implementation consequence |
|---|---|
| `packages/domain` | Pure strict TypeScript, no Node-only imports; canonical IDs/enums/errors plus generated schema-facing types and pure invariant checks. |
| `packages/database` | Kysely-backed repository interfaces, `pg` and file-backed SQLite dialects, Umzug runner, paired SQL, transactions, outbox/events and disclosure filters. No domain decisions. |
| `packages/profiles` | Versioned JSON/SQL records loaded through repositories and validated by AJV; no profile meaning hidden in environment variables. |
| `packages/projections` | Pure materialisation service over repositories/assets; produces immutable provider/shared/public/private snapshots before any external action. |
| `packages/locks` | Transactional lock service invoked by every mutating action; PostgreSQL/SQLite parity tests cover path conflicts and history. |
| `packages/actions` | The sole authoritative action registry loader, gate evaluator, `invoke/resume/cancel/inspect`, saga coordinator, idempotency owner and event writer. Fastify, CLI and studio only adapt it. |
| `packages/ql` | Pure algorithms plus repository ports; canonical Unicode PRIME constants defined once and reused in SQL/JSON/UI/packaging tests. |
| `packages/audit` | Typed 12-position audit writer/validator; stores inspectable evidence, never hidden reasoning traces. |
| `packages/correspondences` | Versioned rule evaluator; pure execution against named profile data and provenance. |
| `packages/resonance` | Deterministic numeric aggregation/projection with golden vectors and cross-platform tolerance policy. |
| `packages/assets` | Streaming content-addressed store, local and S3 drivers, staging/commit promotion, rights and derivation graph; no whole-media buffering in action service. |
| `packages/symbols` | SVG parser/sanitiser and deterministic state generation; browser-independent geometry tests plus real render/print tests. |
| `packages/audio` | TypeScript parameter/tuning model supervising pinned Faust offline/browser builds, analysis tools and FFmpeg mixing; same DSP source/version for both targets. |
| `packages/providers/core` | Fetch-based adapter contract, capability registry and persisted external jobs; provider calls receive approved projections only. |
| `packages/providers/*` | Thin native API mappings. Public-media adapters join the same provider core; no provider owns story meaning, clipping or final composition. |
| `packages/render-remotion` | React/Remotion render-plan consumer in isolated worker process; FFmpeg finish/inspection; accepts only approved immutable inputs. |
| `packages/render-print` | Deterministic layout/PDF pipeline with real font, bleed, safe-area, QR, gamut and rasterised-proof validation. |
| `packages/card-component` | Framework-free state machine plus Lit `<epi-card>` element and generated declaration; React wrapper is presentation glue only. |
| `packages/okf-export` | Node filesystem exporter over read interfaces with parse/link/frontmatter/attestation validation; no SQL writes. |
| `packages/packaging` | Streaming deterministic ZIP/directory builder and importer, portable SQLite construction, exact path closure and root digest implementation. |
| `packages/validation` | AJV plus structural/media/package validators over read-only interfaces; invokes real ffprobe/PDF/browser checks where required and writes immutable reports through actions. |
| `packages/cli` | Commander parser and JSON/JSONL stdout discipline; direct in-process action engine locally or authenticated HTTP action client remotely, never alternate business logic. |
| `apps/worker` | Database lease consumer, heartbeat/cancel/recovery supervisor, resource-class concurrency and subprocess isolation. |
| `apps/studio` | React/Vite action client and read projections with SSE resume by sequence number; no repository imports. |
| `apps/gallery` | Public projection/read service and `<epi-card>` embed/share routes; cannot resolve private state at render time. |

## Real-test consequences of the recommendation

The foundation should define test lanes before implementation packages proliferate:

1. **Pure contract lane:** schemas, generators, 66/132/22 counts, canonical Unicode addresses, registry loading and package-manifest invariants. Existing Python generators remain part of this lane.
2. **Dual SQL lane:** apply checked-in bootstrap SQL to empty real PostgreSQL 18 and real file-backed SQLite; run upgrade migrations from every supported schema revision; compare logical portable inventory.
3. **Action surface lane:** call one real action implementation in process, through built CLI, live Fastify HTTP and studio client; compare result envelopes and persisted events.
4. **Queue/recovery lane:** run concurrent PostgreSQL workers and single SQLite worker; kill processes at the exact crash points in `ACT-014/015`; prove lease recovery and absence of duplicate side effects.
5. **Storage lane:** real local content store and real MinIO; corrupt bytes, interrupt promotion, restore PostgreSQL/object-store backup and verify hashes/relations.
6. **Media lane:** compile actual Faust targets; render actual Remotion compositions; invoke FFmpeg/ffprobe; verify alpha, duration, loop, loudness, spectral results and source/derived hashes.
7. **Browser lane:** built `<epi-card>` against current Chromium, Firefox and actual Safari release family, including keyboard, audio gesture, reduced motion, offline state and custom events.
8. **Print lane:** create actual PDF, inspect page/trim/bleed boxes, rasterise at 300 dpi, test fonts/glyphs/gamut and scan QR from physical and screen proofs.
9. **Package lane:** build a real `.epicard`, disconnect network, open/query SQLite/assets/renders/OKF, verify root digest, corrupt/traverse, and re-import to real PostgreSQL/object storage.
10. **Live provider lane:** advertised public/generative/publication adapters make controlled real calls under credentials and record capability/provenance evidence. Deterministic local test adapters can exercise the action engine during development but cannot satisfy provider release blockers.

Each lane emits the evidence fields required by `ACCEPTANCE_TESTS.md`; Vitest is the orchestration/reporting shell, not an excuse to replace infrastructure or media tools with test doubles.

## Foundation sequence unlocked by approval

Once Frank approves the TypeScript engine, the first implementation foundation can be specified without further aesthetic or product decisions:

1. authorise and create the version-control baseline;
2. create the pnpm workspace and exact Node/pnpm pins;
3. establish package exports/project references and enforce the fixed dependency graph;
4. load and validate normative schemas/registries and generate TypeScript DTOs;
5. establish the paired migration runner and real PostgreSQL 18/SQLite bootstrap tests;
6. implement the action envelope, one small real action, event stream and database lease worker as the vertical foundation;
7. prove that same action through library, CLI and HTTP before broadening the catalogue;
8. provision pinned Remotion/FFmpeg/Faust and real browser test environments.

## The single question for Frank

**Approve strict TypeScript on Node.js 24 LTS as the sole authoritative action/domain runtime for Epi-Card v1, with Rust/Go excluded from the core unless later measured evidence establishes a native module need?**

An answer of **yes** adopts Option A and the coherent foundation above. An answer of **no** means the next decision must choose Rust or Go as the authoritative native core and explicitly accept the permanent schema/action boundary to the TypeScript web and Remotion workspace.
