# Fresh-Session Return of Zero Project-Agent Evaluation

Run this prompt in a brand-new Codex session whose working directory is the `Antykathera-Essay-Work` Git root.

Do not edit the canonical corpus, generated projections, project instructions, skills, hooks, active ideas, or any `NOTES.md`. Temporary files under the system temporary directory are allowed. Do not read the harness specification until the final audit phase; this is a behavioural test of what the fresh session actually discovers.

Work through the following journey and finish with one compact evaluation report.

## 1. Fresh-session inheritance

Before opening project files, report:

- the project identity and constraints supplied to this session;
- every project-local skill Codex exposes from this repository, with its discovered path;
- any hook-provided orientation or active-idea context you can observe;
- whether the project hook definitions are active or awaiting trust review.

Do not infer missing capabilities. Report only what the session actually exposes.

## 2. Open-ended discussion

Answer this briefly in chat without creating or editing a file:

> In what sense might zero return rather than merely recur?

This is deliberately exploratory. Do not impose a destination, workflow ledger, evidence audit, or completion ritual on it.

## 3. Exact source journey

Use the appropriate project-local source capability to retrieve `colebrooke-1817-brahmagupta-bhaskara-q002` from its canonical source house. Return:

- exact wording;
- exact locator;
- quotation status;
- verification and provenance;
- source relation and use boundary;
- canonical path.

Then open the real Van Eenwyk 1997 source house and its sibling `NOTES.md`. Explain what authority each file has. Record the note file's SHA-256 before and after reading it and confirm whether it changed. Never write to the note.

## 4. Canonical writing journey

Use the appropriate project-local writing and orientation capabilities to recover movement `14-s1-p1-sunya-operational` and its manuscript context. Compose one paragraph of 100–140 words in chat that could advance that movement.

Preserve the movement's actual proposition and status. Do not manufacture generic counterpressure, downgrade the essay's derivation because a source has a narrower attribution boundary, or make the source endorse the essay's inference. Name a qualification only if the recovered canonical material makes it locally consequential.

Do not edit the manuscript.

## 5. Hook and propagation journey

Run the implemented real-corpus behavioural evaluation:

```bash
python3 tools/project-agent-harness.py evaluate --project-root . --json
```

Report the hook-on and hook-off scores and name only the behaviours the recorded comparison actually improves.

Run the deterministic checks:

```bash
python3 tools/build-source-projections.py --project-root . --check
python3 tools/build-section-rooms.py --project-root . --check
python3 tools/okf-workspace.py --project-root . doctor --json
```

## 6. Final evaluation

Report:

- which project-local skills actually triggered for each phase;
- what the session-start hook added that was not obtained from later manual reads;
- whether open-ended discussion remained file-free;
- whether exact quotation provenance remained joined to the quotation;
- whether `NOTES.md` remained byte-identical;
- whether the writing paragraph preserved the canonical claim without synthetic caveats;
- hook-on versus hook-off results;
- deterministic check results;
- every file changed during this session, with `none` as the expected result;
- any discrepancy between the implemented specification and observed runtime behaviour.

Do not call the evaluation successful unless every claim is supported by output observed in this fresh session.
