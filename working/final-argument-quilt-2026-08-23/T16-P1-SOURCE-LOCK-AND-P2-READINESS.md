# T16 — P1 Source Lock and P2 Readiness

**Issue:** #17 / T16.  
**Accepted P1 input:** T09 canonical foundation at `a2312156feabb529a4462329683664ced47d5f4e`.  
**P1 propagation branch:** `agent/t10-t16-p1-propagation`.  
**Purpose:** state exactly what is stable enough for P2 field-page enrichment and what remains deliberately Open.

## Lock result

The source substrate is **locked for P2 at identity, authority and readiness-boundary level**.

That means P2 may rely on:

- stable canonical `SOURCE.md` houses and `source_id` identity;
- the authority typing in `working/harmonisation-2026-08-18-objective-internality-capstone/SOURCE-AND-AUTHORITY-MAP.md`;
- the T09 A01–A36 / C01–C64 / Etymology census;
- the P1 48-Movement propagation routes;
- existing passage/quotation readiness exactly where each `SOURCE.md` says it is ready;
- the T15 debt dispositions in `T15-SOURCE-DEBT-DISPOSITION-AND-P2-BOUNDARY.md`;
- `Depth Restoration: pending` as an explicit enrichment queue rather than an evidence claim.

P2 may **not** silently upgrade an Open source/debt item to evidence, silently add a new external source identity, or treat current product state beyond its recorded evidence pin as timeless fact.

## Exact-head non-mutation proof

A compare from the accepted T09 head `a2312156feabb529a4462329683664ced47d5f4e` to the P1 pre-lock head `b9b724c173915f92adcb627218cafc75df9e5b5f` shows exactly eleven changed files:

- eight room-local `P1-CANONICAL-ALIGNMENT.md` supplements;
- `submission-package/essay/section-rooms/README.md`;
- `P1-48-MOVEMENT-CANONICAL-PROPAGATION.md`;
- `T15-SOURCE-DEBT-DISPOSITION-AND-P2-BOUNDARY.md`.

**No `submission-package/essay/symbolon/episteme/sources/**/SOURCE.md` file changed.** Therefore P1 did not invalidate the existing deterministic source projections by changing their canonical input.

## Current executable source contract

The current repository source skill, `.agents/skills/return-of-zero-source/SKILL.md`, defines the live source workflow:

```text
canonical evidence = SOURCE.md
resolve stable source_id = tools/source_resolver.py
retrieve passage = tools/project-agent-harness.py passage <passage-id> --json
```

After an actual `SOURCE.md` change, the live local checks are:

```bash
python3 tools/build-source-projections.py --project-root .
python3 tools/build-source-projections.py --project-root . --check
python3 tools/okf-workspace.py --project-root . doctor --json
```

T16/#17 still mentions `verify-source-bank.py`, but **that tool does not exist in the current `tools/` directory and is not present in repository code search**. That acceptance line is stale programme text and is not replaced by an invented checker.

## Deferred mechanical hygiene

By explicit authorial/user decision on 2026-09-06, the global `okf-workspace.py doctor --json` / `dangling` gate is deferred as ordinary wiki/link hygiene. It remains useful local maintenance and can be run before or during P2, but it no longer blocks programme progression.

Likewise, generated section-room checks remain available locally:

```bash
python3 tools/build-section-rooms.py --project-root . --check
```

P1 deliberately did not hand-edit generated `ROOM.md` / `READING.md` files, so no generated projection has been made authoritative by omission of that check.

## What remains Open after source lock

The detailed families are enumerated in T15. In summary, Open work includes passage/edition/locator depth for Taylor direct carriers, Jung/Pauli/Neumann, Śaiva/Buddhist primaries, Gebser, Bohm, Van Eenwyk, Aristotle/Eckhart, selected French/Giegerich/cultural claims, formal-neighbour proofs/citations, detailed Antikythera mechanics, and empirical trust/deepfake work.

These are **P2 enrichment and Depth Restoration opportunities**, not hidden P1 blockers. Any external attribution must remain within its actual ready evidence until restored.

## P2 entry law

P2 starts at **T17 / GitHub #18**.

Its queue is not a historical directory count and not the old quilt inventory. It must be assembled from:

```text
T07 ratification
  → T09 canonical A/C/E foundation
  → P1 48-Movement propagation
  → T15/T16 source readiness
  → T17 deterministic build queue
```

Every P2 page begins from the raw QL chassis:

```markdown
## #0
## #1
## #2
## #3
## #4
## #5→0
```

but **the semantics of those positions are derived from the page’s own operation**. No universal Definition/Operation/Pattern/Context/Quintessence glossary is to be imposed.

Structural discoveries during enrichment return through T22 fold-back. They do not create new canonical records by stealth.

## T16 acceptance

P1 source identity and authority are stable enough for P2. Remaining evidence debt is named and bounded. No source house changed during P1 propagation. The obsolete checker name is explicitly identified. Deferred mechanical wiki hygiene is recorded rather than falsely reported green.

**Next gate: T17 / #18 — P2 enrichment harness and queue assembly.**
