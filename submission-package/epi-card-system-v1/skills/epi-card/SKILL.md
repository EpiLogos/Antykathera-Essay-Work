---
name: epi-card
description: >-
  Operate the Epi-Card QL Conjugate System for situated symbolic-media
  engagements: Pasu/session context, attractor basins, full 6+6′
  Bimba–Pratibimba mapping, QL-audited art direction and agent decisions,
  symbol banking/generation, reciprocal short-film production, QL resonator
  audio, interactive/print card rendering, OKF wiki export, packaging, and
  approval-gated publication. Use this skill whenever a task creates,
  resumes, inspects, revises, renders, exports, or publishes an Epi-Card,
  even when the user describes it only as a symbolic card, sigil, talismanic
  media object, six/twelve-part video, or constellation engagement.
license: "Proprietary project skill; implementation dependencies retain their own licences."
metadata:
  version: 1.0.0
  product: Epi-Card
  cli: epicard
---

# Epi-Card operating skill

## Purpose

Use the installed `epicard` CLI to operate the full Epi-Card Runtime. Do not write directly to its SQL database, invent alternate storage, or substitute a prose-only workflow for typed actions.

The canonical object is a situated Constellation Engagement with a full twelve-position QL conjugate frame:

```text
P0→P1→P2→P3→P4→P5→P0′→P1′→P2′→P3′→P4′→P5′→P0⁺
```

Bimba and Pratibimba are mandatory first-class positions. The six card-back edges bind `Pn↔Pn′`; they do not reduce the data model to six positions.

## Hard invariants

1. Work through registered CLI actions. Never issue arbitrary SQL.
2. Preserve the native source form before mapping it into QL.
3. Initialise and maintain exactly twelve positions: six Bimba and six Pratibimba.
4. Record missing, latent, unknown, withheld, conflicted, and overdetermined positions explicitly. Never fill a gap merely to complete the appearance.
5. Preserve basin exclusions and unresolved members.
6. Give every material decision and non-trivial transformation a twelve-position QL audit and `5′→0⁺` return.
7. Treat AI-generated images, video, audio, and symbols as candidates until validation and the declared approval gate succeed.
8. Keep canonical symbols vector-first and exact. Add them, typography, QR codes, and canonical audio during deterministic composition rather than trusting a video generator to reproduce them.
9. Use content-addressed assets and preserve provider/model/version, inputs, parameters, rights, disclosure, and derivation.
10. Do not send data to an external provider until `projection.materialize` and `projection.validate` have produced an approved provider projection and the action has attached a provider disclosure manifest.
11. Respect persisted object/field/asset locks. Never invent a force override; use `lock.release` with an authorised actor.
12. Rendering never implies publication. Publication requires its own prepared record and approval.
13. Deposit self-implication, remainder, achieved work, next ground, semantic delta, and media delta before marking an engagement returned.

## Start or resume

For any production task:

1. Identify or open the Pasu/session.
2. Resume the engagement when one exists; otherwise create it.
3. Inspect active profiles, approvals, failed/retryable runs, and current revision.
4. Read only the references required for the next operation.

```bash
scripts/run-epicard session resume --session "$SESSION_ID" --json
scripts/run-epicard ql inspect --engagement "$ENGAGEMENT_ID" --json
```

Load `references/ql-frame.md` before mapping or revising semantic content.
Load `references/audit.md` before making or accepting a material choice.
Load `references/resonance.md` before deriving cross-media parameters.
Load `references/media-pipeline.md` before symbol, image, video, audio, or render work.
Load `references/provider-adapters.md` before any external generation request.
Load `references/privacy-and-approval.md` before using Pasu data, exporting, or publishing.
Load `references/cli-reference.md` when constructing commands or handling a failure.

## Standard whole-run sequence

Execute only stages needed by the request, but retain this dependency order:

```text
session/pasu/temporal context
→ source ingestion and transcript linking
→ attractor and basin revision
→ private working projection and lock inspection
→ ql.initialize
→ ql.map
→ ql.reconcile
→ ql.validate
→ ql.approve
→ resonance.resolve/project
→ art direction, palette, typography
→ symbol search/propose/generate/canonicalise/approve
→ audio palette/render/analyse
→ storyboard.plan
→ approved provider projection/disclosure manifest
→ image/video candidate generation and plate acceptance
→ deterministic modifiers
→ composition.render
→ loop/audio/media validation
→ poster selection
→ approved shared/public projection
→ web/print card
→ OKF export
→ .epicard package
→ publication preparation/approval/execution when requested
→ return.deposit
```

## CLI invocation

Use structured input files for non-trivial actions:

```bash
scripts/run-epicard <domain> <action> \
  --request @request.json \
  --session "$SESSION_ID" \
  --engagement "$ENGAGEMENT_ID" \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --json
```

For a resumable pipeline:

```bash
scripts/run-epicard run \
  --engagement "$ENGAGEMENT_ID" \
  --through render \
  --resume \
  --jsonl
```

Do not hide the underlying actions: preserve and inspect each event and audit tick.

## Review handling

When a result is `awaiting_review`:

1. Inspect the candidate set, validation report, audit positions, rejected alternatives, and disclosure manifest.
2. Present the review material through the host surface.
3. Invoke the named approval action only after an authorised actor decides.
4. Resume the run by run ID; do not resubmit the provider job or repeat prior stages.

## Failure handling

- `failed_retryable`: inspect retry metadata, provider state, and resume cursor, then use `--resume`.
- `failed_terminal`: inspect validation findings and QL audit; revise the relevant upstream object through a new immutable revision.
- Asset mismatch: do not overwrite; create a new candidate and derivation edge.
- Missing QL content: preserve its occupancy state and reason.
- Provider capability mismatch: choose a capability record that satisfies the plan or revise the plan; never exceed limits opportunistically.

## Completion

Before declaring an Epi-Card complete, confirm:

- twelve semantic positions, twelve audit positions per material action, twelve symbol states, and twelve scene atoms;
- six reciprocal scene pairs and a passing `P5′→P0` loop seam;
- exact symbol, outlined display lettering, canonical QL drone, and QR applied deterministically;
- approved private/shared/public/provider projections exist wherever their target operations require them;
- active locks were respected and lock history is retained;
- web card, print card, master/loop assets, OKF bundle, `.epicard` package, and validation reports exist as required;
- return deposit exists and the next tick is identified or deliberately left as a seed.
