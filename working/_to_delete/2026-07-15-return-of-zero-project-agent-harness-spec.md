---
title: "The Return of Zero — Implemented Project Agent and Trust Harness"
status: implemented
date: "2026-07-15"
scope: essay-local-agent-skills-hooks-continuity-and-verification
---

# The Return of Zero — Project Agent and Trust Harness

## Purpose

The harness lets a Codex session launched from `Antykathera-Essay-Work` converse, explore, retrieve, research, source, write, review, and change files while preserving the essay’s actual authority boundaries. It adds compact instructions at the points where they change behaviour and deterministic checks only where code can settle the predicate.

There is no mandatory file-change ritual. Ordinary conversation can remain in chat. Exploration may precede a file destination. Review is invoked explicitly. Repository checks scale with the surface changed.

## Runtime surface

Codex discovers the project from the Git root and loads:

```text
AGENTS.md
.codex/config.toml
.codex/hooks.json
.codex/hooks/return_zero_hook.py
.agents/skills/
  return-of-zero-orient/
  return-of-zero-source/
  return-of-zero-write/
  return-of-zero-review/
```

Project hooks require the repository to be trusted. Codex also requires review of a new or changed command-hook hash; use `/hooks` to inspect and trust the checked-in definitions. `.codex/config.toml` explicitly enables the stable `hooks` feature.

No project file claims dependable per-subagent model selection. Luna, Terra, and Sol are not project agents, models, or runtime tiers. Where a task needs a different degree of freedom, the prompt or relevant skill states the permitted action plainly: exact retrieval is narrow; context assembly permits relational judgement; composition permits interpretive and stylistic judgement.

## Project identity

The standing project position is carried compactly by `AGENTS.md` and the session-start hook:

> Enter as the project agent for *The Return of Zero*. Frank’s established conceptual architecture governs the essay. Recover the relevant proposition, register, inheritance, and movement at the grain required by the exchange. Sources deepen, historicise, test, and articulate that movement; they do not grant it permission to possess its own derivation. Own interpretations, choices, errors, and repository effects.

The hook does not duplicate the whole doctrine. It points to `AGENTS.md`, the four skills, the source-house boundary, the sovereign manuscript, chat freedom, and any deliberately retained active ideas.

## Project-local skills

### `return-of-zero-orient`

Use for project orientation, canonical retrieval, graph traversal, context assembly, effect mapping, native theorem-language recovery, and active-idea recall. It routes substantive retrieval through `tools/okf-workspace.py` and opens its detailed workspace contract only for schema, authority, adapter, or generated-surface work.

### `return-of-zero-source`

Use for source identity, bibliography, quotation, provenance, citation, comparison, and source-house edits. It works with one canonical `SOURCE.md` per recoverable object and forbids parallel record, quote, passage, or study systems.

### `return-of-zero-write`

Use for conversation, exploration, teaching, pair-writing, drafting, and revision. It opens the exact movement and the master manuscript, keeps generated rooms subordinate, and admits qualifications only when they are concretely live rather than manufacturing counterpressure.

### `return-of-zero-review`

Use for explicit prose review, source audit, propagation analysis, deterministic freshness, and repository review. It distinguishes conceptual fidelity, evidence relation, citation state, quotation state, freshness, and retrieval confidence.

Each skill has an `agents/openai.yaml` interface file and passes Codex’s `quick_validate.py`. The former `agent-skills/` architecture was removed only after its workspace contract and room auditor had migrated and the replacement tests passed.

## Canonical corpus

The harness preserves the existing design:

- one `SOURCE.md` per source house containing bibliography, scholarly record, passages/excerpts, provenance, relationships, and consumers;
- optional sibling `NOTES.md` containing Frank’s personal encounter notes and quotation leads;
- one sovereign manuscript at `submission-package/essay/THE-RETURN-OF-ZERO.md`;
- compact generated `ROOM.md` waypoints;
- deterministic `MAIN-SOURCES.md`, `SOURCE-INDEX.md`, and `PASSAGE-LEDGER.md` projections;
- BKMR as a disposable typed retrieval index, never canonical authority.

Agents may read `NOTES.md` but may not create, edit, append, normalise, migrate, index as canonical evidence, relocate, or delete it. Builds and verification discover notes as an authorial artifact but do not treat them as projection inputs or evidence debt.

The room auditor formerly bundled in the Sol-named skill now lives at `tools/audit-room-depth.py`. The graph workspace contract lives under `.agents/skills/return-of-zero-orient/references/`.

## Active ideas

`working/active-ideas.json` is the only project-agent continuity file introduced by this harness. It is optional and changed only by an explicit command. Each retained idea records:

- a stable ID and concise idea;
- provenance;
- local context;
- current relevance;
- optional next use;
- active or retired status and timestamps.

It is not an external representation of cognition, J-space, hidden reasoning, conversation history, a session ledger, or a compulsory work queue. The session hook injects only active entries, capped to a compact payload. Retirement preserves provenance without continuing to inject the idea.

```bash
python3 tools/project-agent-harness.py ideas add "<idea>" \
  --provenance "<where it arose>" \
  --context "<local context>" \
  --relevance "<why retain it>" \
  --next-use "<optional next use>" --json
python3 tools/project-agent-harness.py ideas list --json
python3 tools/project-agent-harness.py ideas amend <idea-id> --relevance "<new relevance>" --json
python3 tools/project-agent-harness.py ideas retire <idea-id> --reason "<reason>" --json
```

## Hooks

All handlers receive Codex’s JSON event object on stdin and return documented JSON hook output.

### `SessionStart`

Runs for startup, resume, clear, and compact. It injects the compact project identity, skill locations, chat freedom, source/notes boundary, master manuscript path, and active ideas when present. It does not crawl the repository.

### `PreToolUse` and `PostToolUse`

Run for Bash, `apply_patch`, Edit, and Write. When the tool input can address `NOTES.md` or destructively address one of its parent surfaces, the handler snapshots every existing source-house `NOTES.md` into session/turn/tool-keyed temporary state. After the tool, it restores changed or deleted notes and removes newly created notes. Unrelated writes do not create a snapshot, so a concurrent Frank edit is not mistaken for an agent mutation. When restoration occurs, `PostToolUse` returns `continue: false` with the exact paths and redirects evidence work to `SOURCE.md`.

The snapshot window is one tool call. This protects agent-authored mutations without making notes read-only to Frank outside the call.

### `Stop`

Runs source-projection and section-room freshness checks. A clean repository produces no payload. Stale generated outputs return `continue: false`, the builder failure, and the required rebuild direction. The hook does not decide prose quality or whether a conversation must become a file.

## Deterministic harness commands

The project harness provides three narrow utilities in addition to active ideas:

```bash
# Recover one exact passage with wording, locator, verification, relation, and path.
python3 tools/project-agent-harness.py passage <passage-id> --json

# Recover one canonical movement packet without generating prose or caveats.
python3 tools/project-agent-harness.py writing-context <movement-id> --json

# Run the real-corpus hook-on versus hook-off behavioural journeys.
python3 tools/project-agent-harness.py evaluate --project-root . --json
```

## Behavioural evaluation

The evaluation executes seven representative journeys against the real corpus or isolated copies of its real files:

1. open-ended discussion remains in chat;
2. source retrieval returns exact quotation provenance;
3. writing context preserves the canonical claim without manufactured counterpressure;
4. a real `NOTES.md` mutation is attempted and restored;
5. a real canonical `SOURCE.md` mutation makes projections stale and blocks completion;
6. an active idea is created and recovered in fresh-session context;
7. fresh-session orientation names the project and skill surface.

The implemented comparison scores hook-on at 7/7 and hook-off at 3/7. Both modes preserve chat freedom, exact retrieval, and canonical writing context. Hooks add four measured behaviours: note protection, propagation enforcement, active-idea recovery, and fresh-session orientation. The report records each check rather than claiming a general intelligence improvement.

The unit suite separately exercises idea creation/recovery/amendment/retirement, exact passage parsing, writing context, hook I/O, note restoration, skill discovery, and the hook comparison.

## General atomic skill-maker

The independent general skill lives outside the essay repository at:

`~/.agents/skills/unix-atomic-skill-maker/`

It accepts a JSON specification containing one concrete capability, triggers, non-triggers, authorised actions, outputs, and positive/negative validation cases. It validates all input before writing, creates a concise `SKILL.md` and machine-readable `validation/cases.json` in a temporary directory, atomically renames the complete skill into place, and refuses overwrite. It contains no Nara or Return of Zero doctrine.

```bash
python3 ~/.agents/skills/unix-atomic-skill-maker/scripts/create_skill.py \
  --spec /path/to/spec.json --output-root /path/to/skills
python3 -m unittest discover \
  -s ~/.agents/skills/unix-atomic-skill-maker/tests -v
```

## Verification

From the essay root:

```bash
python3 tools/project-agent-harness.py evaluate --project-root . --json
python3 tools/build-source-projections.py --project-root . --check
python3 tools/build-section-rooms.py --project-root . --check
python3 tools/okf-workspace.py --project-root . doctor --json
python3 -m unittest discover -s tests -v
```

Skill validation:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/return-of-zero-orient
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/return-of-zero-source
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/return-of-zero-write
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/return-of-zero-review
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.agents/skills/unix-atomic-skill-maker
```

`codex doctor --json` verifies local Codex configuration, Git-root detection, and that the hooks feature is enabled. A true fresh model session additionally depends on local provider/network policy; the checked-in behavioural tests do not require an external model call.
