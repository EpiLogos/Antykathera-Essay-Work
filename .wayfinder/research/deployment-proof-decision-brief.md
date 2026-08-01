# Epi-Card v1 deployment-proof decision brief

**Status:** research brief for the open human decision in [Choose the first release deployment proof](../tickets/003-choose-deployment-proof.md)  
**Prepared:** 2026-08-01  
**Decision owner:** Frank  
**Normative basis:** `submission-package/epi-card-system-v1/SPEC.md` §§29–32 and `acceptance/ACCEPTANCE_TESTS.md`

## Recommendation

For v1, make **both the local creator profile and the collaborative single-node profile actually deployed and exercised**. Treat the collaborative single-node deployment as the **first integration and production proof**, then prove that its frozen output exports to and round-trips through the local/portable profile. Keep the scaled hosted profile as a **documented, explicitly unsupported topology** until it has been deployed on real managed infrastructure and has passed its own resilience, scale, security, and recovery evidence.

This is the smallest honest supported surface that satisfies the existing specification:

- The specification fixes PostgreSQL 18+ as operational production truth (`D-012`) and defines the `PG` acceptance environment as PostgreSQL, object store, worker, and renderer.
- It separately requires SQLite and package-local assets for portable/offline carriage (`D-013`, `SQ`, and `E2E-005`).
- The local creator profile in §29.1 is more than an archive viewer: it includes SQLite, local files, a worker, CLI, web studio, and local Remotion/FFmpeg/Faust.
- The collaborative single-node profile in §29.2 supplies the production relational/object/queue/auth boundary needed for PostgreSQL migration, concurrency, worker recovery, backup/restore, and server-to-portable round-trip tests.
- Nothing in the current Definition of Done requires autoscaling or a managed cloud control plane. Calling the scaled hosted topology “supported” would add a large evidence burden without adding a missing v1 semantic capability.

The proposed release claim is therefore:

> Epi-Card v1 supports a local creator deployment and a collaborative single-node deployment. A scaled hosted architecture is described for future operation but is not a supported v1 deployment profile.

## The smallest decision Frank must make

One yes/no decision is sufficient:

> **Should v1 support and prove exactly the local creator and collaborative single-node profiles, with scaled hosted documented but explicitly unsupported?**

**Recommended answer: yes.**

If the answer is no, Frank must name the changed support set. Choosing local creator only conflicts with the present PostgreSQL production requirement and several release blockers unless the normative specification is versioned and changed. Choosing scaled hosted as supported creates a real cloud-deployment programme, not a documentation task.

## What “actually deployed and exercised” means

A profile is actually deployed only when all of the following are true:

1. A release candidate is launched from a clean checkout or signed release bundle by a documented, repeatable command or installer.
2. The declared components are distinct, live processes/services with the declared persistence and network boundaries. Merely having their libraries installed is insufficient.
3. Real migrations run against the declared database and the product performs real reads, writes, asset storage, queueing, rendering, export, and import. In-memory substitutions and mocked services are not evidence.
4. At least one complete, non-placeholder card traverses the profile through the shared actions, producing actual video/audio/web/print/OKF/`.epicard` outputs and immutable hashes.
5. The profile is stopped, restarted, and recovered. In-flight work, idempotency, persisted assets, and approved revisions remain correct.
6. The acceptance subset declared for the profile passes against the running deployment, with the mandatory `validation_report` fields, logs, artifact references, versions, timestamps, and actor/service identities.
7. Another operator can reproduce the result from the release instructions without relying on undeclared workstation state.

An attractive screen recording, a static component, a container manifest that was never launched, schema linting, or a test harness with service mocks does not meet this definition.

## Supported profile versus documented topology

| Property | Supported profile | Documented topology |
|---|---|---|
| Runtime | Release artifact actually launched | Diagram, manifest, example configuration, or runbook only |
| Dependencies | Exact versions and boundaries recorded from live services | Intended vendors/components named |
| Data | Real schema migrations and persisted card state | Schema compatibility inferred |
| Media | Real worker and renderer produce inspected MP4/WebM/audio/print artifacts | Render path described or locally substituted |
| Failure | Restart, interrupted action, retry/idempotency, and recovery exercised | Failure behaviour stated |
| Security | Authentication, secret handling, disclosure boundary, SSRF/log-redaction checks exercised | Controls listed |
| Recovery | Backup restored into a clean environment and reconciled with object hashes | Backup/PITR design described |
| Capacity | Declared reference load and queue backpressure measured | Scaling intent or sizing estimate supplied |
| Evidence | Immutable, replayable bundle tied to one implementation revision | Design review record |
| Release language | “Supported and tested” | “Reference topology; not supported in v1” |

A documented topology remains valuable. It can establish component boundaries, portability assumptions, configuration contracts, threat model, expected metrics, backup policy, and migration path. It cannot inherit the word **supported** from another profile.

## Profile proof matrix

### 1. Local creator profile — must be deployed and exercised

**Declared runtime**

- SQLite 3.45+;
- local content-addressed asset tree;
- one worker process;
- `epicard` CLI;
- local web studio;
- local Remotion, FFmpeg, and Faust targets;
- credentials, when used, read from the local secret store.

**Minimum credible evidence**

- Install/start from a clean supported workstation profile; record OS/architecture and exact dependency versions.
- Apply and reapply the SQLite migration safely (`BLD-002`, `BLD-004`, `BLD-015`).
- Run the complete flow through CLI and studio using the same action library (`ACT-001`, `ACT-002`, `ACT-011`).
- Exercise an interrupted local/media action and recovery, not merely a normal shutdown (`ACT-006`, `ACT-014`, relevant parts of `SEC-008`).
- Produce real 6–12 second and 40–60 second films, twelve-state audio, interactive web card, print proof, OKF, and `.epicard` package from accepted plates. A public-media asset path is sufficient; a generative provider is not required (`E2E-001`, `E2E-003`).
- Open the resulting package with networking disabled and prove SQLite/files/hash resolution (`PKG-003`, `PKG-004`, `E2E-005`).
- Exercise private-to-public projection and verify that local secrets and private material do not enter exports or logs (`E2E-004`, `SEC-006`).
- Retain outputs, hashes, logs, screenshots/recordings for human review, and machine-readable validation reports.

**Initial supported boundary**

Name the exact desktop OS/architecture actually exercised. Do not claim cross-platform desktop support merely because Node, SQLite, and FFmpeg are portable.

### 2. Collaborative single-node profile — must be deployed and exercised; recommended first proof

**Declared runtime**

- PostgreSQL 18+;
- S3-compatible object store such as MinIO;
- web studio;
- durable worker queue;
- one or more real render workers;
- reverse proxy, authentication, and secret injection.

The components may share one physical or virtual host, but they must remain independently restartable and must communicate over the real boundaries the product will use.

**Minimum credible evidence**

- Build and launch a version-pinned single-node release stack from a clean host or VM. Record image/binary digests, configuration hashes, dependency versions, and exposed boundaries.
- Apply `database/postgres.sql` to a real PostgreSQL 18 instance and run parity and registry seed checks (`BLD-001`, `BLD-003`, `BLD-004`, `BLD-015`).
- Store and retrieve immutable content-addressed assets through the actual S3-compatible API. Verify SQL/object consistency after restart.
- Drive one complete engagement through HTTP, studio, CLI, and direct shared-action entry points (`ACT-001`) and retain real artifacts for `E2E-001` through `E2E-006` as applicable.
- Exercise simultaneous idempotent requests, queue cancellation, worker crash boundaries, persisted provider cursors, and reconnection to the event stream (`ACT-004`–`ACT-006`, `ACT-013`–`ACT-015`).
- Run 20 real concurrent media jobs at the configured capacity and demonstrate backpressure and no silent loss (`PERF-004`). Lower-powered hardware may take longer; it may not replace the jobs with no-op work.
- Back up PostgreSQL and the object store, destroy or isolate the original stack, restore into a clean stack, and reconcile engagements, revisions, actions, audits, asset hashes, and recovery lag (`SEC-007`).
- Export a complete `.epicard`, open it in the local/offline profile, then re-import it without semantic or hash loss (`PKG-006`, `E2E-005`). This is the bridge proving that the two supported profiles implement one contract.
- Exercise actual authentication, permission denial, publication approval, disclosure manifests, SSRF policy, log redaction, and public/private URL separation.

**Why this should be the first integration proof**

It exposes the hardest fixed v1 boundaries early: PostgreSQL correctness, transactional actions, object-store consistency, queue recovery, authentication, concurrency, and backup/restore. The local profile can then prove that the same frozen semantic object travels offline. Starting with local-only functionality would defer production failures until late while still leaving the required `PG` environment unproved.

“First” here means the first deployment target used to integrate the whole runtime. It does not mean the local creator proof is optional at release.

### 3. Scaled hosted profile — document for v1; do not claim support

**Document in v1**

- managed PostgreSQL and migration/PITR assumptions;
- managed object storage/CDN and content-address/cache rules;
- queue semantics and autoscaling signals;
- separate CPU/GPU worker pool contracts;
- secret-manager integration boundary;
- metrics, logs, traces, alerting, and audit retention;
- backup, restore, regional failure, data residency, and cost model;
- promotion path from the single-node release and version-skew policy.

**Evidence required before later support may be claimed**

- A deployment into a real named hosted environment using the managed services that the support claim names. A laptop Compose stack or local Kubernetes cluster is not equivalent.
- At least two application/worker instances where horizontal behaviour is claimed, with load balancing and distributed queue leases exercised.
- Autoscaling up and down under real media work; separate CPU/GPU scheduling if that is advertised.
- Failure of a worker and an application instance without duplicate canonical output or lost work.
- Managed database/object backup and point-in-time recovery into a clean environment, with application-level reconciliation.
- External ingress, TLS, authentication, secret rotation, log redaction, observability, alarms, and incident evidence.
- Measured capacity, latency, and cost envelope for a declared reference workload.

Until those tests exist, the topology should carry the release label: **“documented future profile; not deployed, exercised, or supported by Epi-Card v1.”**

## Release evidence bundle

Keep one immutable deployment-proof bundle per supported profile. At minimum it should contain:

```text
deployment-manifest/
  release revision and source digest
  build lockfile and artifact/image digests
  sanitized configuration and topology
  OS/runtime/service versions
acceptance/
  machine-readable validation reports
  test-to-profile matrix
  timestamps, actors, inputs, observed/expected values
artifacts/
  card/video/audio/web/print/OKF/epicard outputs and SHA-256 digests
operations/
  startup, health, restart, interruption, queue, and recovery logs
  backup/restore receipt and reconciliation report
security/
  auth/permission/disclosure/SSRF/redaction findings
performance/
  reference workload, p50/p95/p99, resource use, queue depth, and job outcomes
review/
  human approvals and recorded visual/audio/print inspection
```

The bundle must use the evidence fields required by acceptance §0.3 and be tied to one implementation commit, schema revision, and profile-version set. Recordings supplement the structured evidence; they do not replace it.

## Acceptance interpretation that should be fixed during implementation

The acceptance document uses environment codes (`PG`, `SQ`, `WEB`, `CLI`, `HERMES`, `MEDIA`, `PRINT`) rather than §29 deployment-profile names, and many tests say `all`. The implementation test manifest should therefore declare the mapping explicitly:

- `local-creator-v1` supplies `SQ`, `CLI`, local `WEB`, local `MEDIA`, and the offline portions of package/end-to-end tests;
- `collaborative-single-node-v1` supplies `PG`, object store, queue, server/worker, authenticated `WEB`, production `MEDIA`, recovery, and server-side concurrency;
- browser-family and print tests are cross-profile release environments, not evidence of scaled hosting;
- `HERMES` exercises the shared action/CLI boundary against at least the primary collaborative deployment, with any local-only run recorded separately;
- a test marked `all` must be assigned to every environment whose declared boundary it can materially test, not silently run once on the easiest profile;
- provider-specific tests apply only to adapters advertised as supported, while `E2E-001` must succeed without an external generative-video provider.

This mapping should be executable metadata in the acceptance runner, not only prose, so no release blocker disappears between profile names and environment codes.

## Present workspace reality

This machine currently provides a plausible build substrate, not deployment proof:

- macOS 26.5.2 on ARM64;
- SQLite 3.51.0;
- Node.js 24.16.0, npm 11.13.0, and pnpm 10.25.0;
- FFmpeg/FFprobe 8.1.1;
- Docker client 29.2.1 and Compose 5.0.2, with the Docker daemon demonstrably running unrelated containers.

No local `psql`, PostgreSQL server, Faust executable, or browser executable was found on the command path during this inspection. More importantly, the Epi-Card package presently contains normative specifications, DDL, contracts, examples, and package validators but no runtime workspace, Dockerfile, Compose deployment, or hosted infrastructure definition. Its own validation report explicitly says that PostgreSQL-specific execution remains implementation acceptance.

Therefore none of the three §29 profiles is currently deployed or supported. The existing passing validation report proves the **specification package**, not the Epi-Card runtime or any deployment topology.

## Consequence of each possible choice

| Frank's choice | Consequence |
|---|---|
| Local creator + collaborative single-node; scaled documented | **Recommended.** Meets fixed production and portable boundaries with bounded infrastructure scope. |
| Local creator only | Requires a normative v1 change or leaves `PG`, object-store, concurrency, recovery, and server round-trip blockers unsatisfied. |
| Collaborative single-node only | Leaves the declared local creator profile and offline/local workflow unsupported; `.epicard` offline proof alone is not the complete §29.1 runtime. |
| All three supported | Valid, but commits v1 to real cloud infrastructure, hosted security/operations, autoscaling, managed recovery, and ongoing support evidence. |
| All three documented only | Not a runtime release; cannot satisfy the complete-runtime destination or acceptance requirements. |

