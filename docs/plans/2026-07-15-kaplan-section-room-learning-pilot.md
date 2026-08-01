---
title: "Kaplan and §0/1 Learning-Surface Pilot"
page_type: implementation-plan
status: active
date: 2026-07-15
---

# Kaplan and §0/1 Learning-Surface Pilot

## Outcome

Prove one complete source-to-writing path in which a reader can learn from Robert Kaplan without mistaking marginalia for verified quotation, and one complete room-to-reading path in which §0/1 can be inhabited as an argument rather than scanned as an inventory. The same surfaces must be recoverable by the OKF graph and BKMR lexical index, so an agent entering a movement can retrieve the relevant reading sequence, source record, study commentary, exact quote status, and canonical consumer.

## Authority model

- The source record remains the authority for Kaplan's bibliographic identity, readiness, essay use, and claim boundary.
- A quote dossier remains the only authority for exact Kaplan text. No Kaplan quote dossier will be invented while the fixed-page edition is unavailable.
- The study dossier is a learning refraction: it may organise Frank's marginalia, publisher or catalogue routes, worked mathematics, reading questions, and essay consumers, but it must expose the provenance and status of each item.
- The room reading path is a learning refraction over canonical movement nodes, source records, and quote dossiers. Generated room context may embed it; the embedded copy remains replaceable.
- `10-FRANK-DRAFT.md` and the raw Kaplan note remain byte-for-byte unchanged.

## Test-first implementation sequence

1. Add failing section-room builder tests proving that an optional protected `04-READING-PATH.md` is embedded in generated context, hashed in the room manifest, never overwritten, and participates in stale-state detection.
2. Add failing OKF tests proving that `source-study` and `room-reading-path` are distinct artifact types; Kaplan's study is discoverable by full-body search and appears in the §1 movement context; the §0/1 path appears in its movement context; record/study backlinks resolve.
3. Add failing BKMR tests for a first-class `studies` collection and real lexical search against the synced Kaplan dossier. Keep room reading paths in the existing `rooms` collection.
4. Add a real surface-contract test that resolves every `source_id`, quoted passage ID, movement link, and canonical path named by the pilot artifacts, and rejects quotation-ready language for Kaplan.
5. Implement the builder, workspace schema, adapters, source-bank view, Kaplan study dossier, §0/1 reading path, source-record link, and source-bank front-door link.
6. Rebuild only §0/1 first, then check all rooms. Sync and search the real BKMR collections. Run OKF `find`, `open`, `context`, `trace`, `links`, `backlinks`, and `doctor` against the two pilot entries.
7. Run the writing-rubric and comparison/negation sweeps, then a fresh-eyes audit of the newly authored study prose and reading path. Revise until the surfaces teach without catalogue compression, false authority, or generic model cadence.

## Acceptance criteria

- A human opening §0/1 context encounters a short orientation, a deliberate reading order, exact passages or direct source routes, the question each reading answers, the movement it serves, and a prompt for returning to the argument.
- A human opening the Kaplan study dossier can distinguish: what the book or publisher page establishes; what Frank's note remembers; what mathematics can be worked independently; where each lead enters §1; and what still requires the fixed edition.
- An agent entering `13-s1-p0-sign-migrates` receives the Kaplan study dossier in its bounded context and can trace it back to the source record and forward to named consumers.
- An agent entering `01-s01-p0-question-before-mechanism` receives the §0/1 reading path in its bounded context and can reopen every canonical source and passage it names.
- BKMR lexical search returns the study dossier with canonical path, stable ID, readiness state, and content hash; OKF remains the authority used to reopen it.
- No unverified Kaplan wording is marked quotation-ready, no historical priority claim is promoted beyond the source boundary, and no raw note or sovereign draft changes.
- The full test suite, room-builder check, BKMR doctors, OKF doctor, link checks, protected-file hashes, and prose audits pass or name their remaining debt precisely.
