---
name: return-of-zero-build
description: Use when turning a queue of Return of Zero field elements into their developed pages by subagent fan-out and hygiene.
---

# Build Return of Zero Field Pages

Turn a quilt of accumulated material into developed field pages deterministically: intake → dispatch → barrier → hygiene.

## When to use

- A quilting surface has produced enough material to build pages.
- Multiple field pages need development in one coordinated pass.
- A hygiene stage is required after page development to validate links and regenerate navigation.

Do not use for one-off page edits; use `return-of-zero-pages` for those.

## Steps

1. **Assemble the intake.** Run the intake helper:
   ```bash
   python3 .agents/skills/return-of-zero-build/workflow.py intake \
     --project-root /Users/admin/Documents/Nara-Personal/Antykathera-Essay-Work \
     --output intake.json
   ```
   It reads the quilting surfaces (`submission-package/essay/quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md`, `submission-package/essay/quilt/2026-08-02-PARALLEL-HARMONISED-QUILT.md`), resolves each element to its canonical home, and emits an intake manifest. *Done when `intake.json` lists every element with identity, home, register, and source inputs.*

2. **Dispatch one subagent per element.** For each element in the intake manifest, launch an independent agent with:
   - the element's quilt contribution(s);
   - its canonical source house, argument node, concept node, and reference-notes;
   - the register's README contract;
   - the `return-of-zero-pages` skill;
   - the `return-of-zero-links` skill;
   - `return-of-zero-visuals` if the element needs an asset.
   Agents must be blind to each other's drafts. *Done when every element has a drafted page in its canonical home.*

3. **Wait at the barrier.** No agent proceeds to hygiene until all element drafts are complete. *Done when the last agent reports its page written.*

4. **Run hygiene.** Execute:
   ```bash
   python3 .agents/skills/return-of-zero-build/workflow.py hygiene \
     --project-root /Users/admin/Documents/Nara-Personal/Antykathera-Essay-Work \
     --intake intake.json
   ```
   The hygiene stage runs:
   - `tools/okf-workspace.py doctor --json` for debt counts (missing-register, unresolved-link);
   - `tools/okf-workspace.py links --json` for link-health detail;
   - `tools/okf-workspace.py effects <source-or-concept> --depth 4 --json` for every changed consumer;
   - MOC/intents aggregation from written links only.
   *Done when the report lists no unresolved links, no alias capture by frozen stubs, and no unresolved one-home violations.*

5. **Report, don't certify.** The build ends with a hygiene report. It does not self-certify that the pages are correct — only that the deterministic gates passed.

## Essential and tangential

Every element receives the same development attention. A leaf page (for example, a media mytheme) and a dense braid (for example, a Spanda matheme) both get full development. Frontmatter weighting (`argument_weight`, `consumed_by`, `source_role`) decides how each turns up in mapping and navigation after the build.

## Common mistakes

- Dispatching agents who share drafts or read each other's outputs before the barrier.
- Generating the MOC or intents layer before the written links exist.
- Skipping hygiene because the pages "look fine."
- Treating the intake manifest as the source of truth rather than the quilts it reads.
