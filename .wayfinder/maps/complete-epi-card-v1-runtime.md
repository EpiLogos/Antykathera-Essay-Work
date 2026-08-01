---
title: Complete Epi-Card v1 Runtime
label: wayfinder:map
status: open
created: 2026-08-01
tracker: ../TRACKER.md
---

# Complete Epi-Card v1 Runtime

## Destination

Build the complete Epi-Card v1 runtime in place: all normative modules and 66 action contracts operating over PostgreSQL and portable SQLite; adaptive Pasu encounter; full `6+6′` QL semantics and audit; public and optional generative media acquisition; real MP4/WebM and extended-film rendering; Faust audio; production interactive and print cards; OKF export; `.epicard` packaging; publication and return; and immutable evidence for every release-blocking acceptance test.

## Notes

- This effort explicitly overrides Wayfinder's planning-only default. The map remains active through implementation, integration, deployment proof, and release acceptance.
- Orchestration override: one Wayfinder session equals one claimed subagent run. The root agent coordinates all frontier tickets, runs independent tickets concurrently, and refills capacity as agents finish. HITL tickets may receive agent research and prototypes, but their human decisions remain Frank's.
- Governing project instructions: `AGENTS.md`. Do not use the installed S5 Epi-Logos plugin or `epi-logos-voice`.
- Normative product authority: `submission-package/epi-card-system-v1/SPEC.md`, followed by its database schemas and contracts, action/API catalogues, skill/UI declarations, and examples.
- Acceptance authority: `submission-package/epi-card-system-v1/acceptance/ACCEPTANCE_TESTS.md`. Tests must exercise real functionality. Mocks, decorative fixtures, placeholder implementations, and contact-sheet substitutes are not release evidence.
- Already fixed: PostgreSQL 18+, portable SQLite, content-addressed assets, full twelve-address QL frame, 66 registered actions, 22 gates, Remotion plus FFmpeg, Faust QL Resonator, web/print/OKF/`.epicard` outputs, and provider independence.
- Media acquisition has plural production lanes. Public image and public video collection/procurement with rights and provenance are first-class; imported or commissioned assets remain valid; Seedance 2.0/2.5 or another capable generative provider is an optimal optional adapter, not the condition for a valid video rendition.
- The adaptive encounter carries QL internally through an opening frame, four primary natural questions, and an open return frame. Turns do not map rigidly one-to-one to positions; compilation may populate the whole `6+6′` field. Relevant Pasu memory must enter through consented context and disclosure controls.
- Refer to maps and tickets by linked title in all human-facing narration.
- The repository currently has no Git `HEAD`; research branches cannot exist until the version-control baseline ticket is resolved.

## Decisions so far

- [Establish the production public-media source surface](../tickets/004-research-public-media-sources.md) — Use a source-neutral acquisition layer with Pexels, Pixabay, Wikimedia Commons, and NASA as production image/video adapters, Openverse as image discovery only, runtime-owned clipping, rights gates, controlled storage, and complete derivation provenance.
- [Establish the current optional generative-video provider surface](../tickets/005-research-generative-video-providers.md) — Keep generation optional and provider-independent; Seedance 2.0 is callable through BytePlus or Runway, Seedance 2.5 remains inactive until an official API probe succeeds, and every selectable provider requires exact capability, lifecycle, billing, policy, provenance, and health records.

## Not yet specified

- The operational-core implementation can be decomposed only after the workspace stack and first deployment proof are fixed.
- The exact implementation waves for the action engine, QL mapping/reconciliation, audit/gates, projections, provider orchestration, and worker recovery remain behind the stack decision.
- Media acquisition, editing, storyboard, composition, loop validation, and rendition execution remain behind the public-media contract and current-provider research.
- The Faust instrument, browser/offline audio targets, and deterministic analysis suite require implementation decomposition after workspace/toolchain selection.
- Studio, gallery, `<epi-card>`, print proof, OKF export, packaging/import, publication, and return need build tickets after the interaction and deployment decisions settle their boundaries.
- Security, performance, observability, backup, migration, browser-family, offline round-trip, and final acceptance work will graduate when the release environments are fixed.

## Out of scope

- Rewriting the sovereign essay or changing its canonical argument merely to serve the runtime.
- Treating the discarded contact-sheet panel as implementation or acceptance evidence.
- Unrelated submission-package surfaces unless a declared Epi-Card integration requires them.
