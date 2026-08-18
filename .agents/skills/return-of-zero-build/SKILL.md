---
name: return-of-zero-build
description: Use when turning a ratified census of Return of Zero field elements into their developed pages by subagent fan-out and hygiene.
---

# Build Return of Zero Field Pages

Turn the ratified authored field into developed pages deterministically: census lock → intake → dispatch → barrier → hygiene.

The build is **not** itself the canonical census. It consumes the census produced by quilting, harmonisation, ratification, and propagation. A heading scanner or the current contents of one directory can never prove that the authored field is complete.

## When to use

- The quilt has been ratified and propagated into a current canonical field census.
- Multiple field pages need development in one coordinated pass.
- A hygiene stage is required after page development to validate links and regenerate navigation.

Do not use for one-off page edits; use `return-of-zero-pages` for those. Do not use before the ratification/propagation gate to decide how many arguments, concepts, roots, paths, histories, dossiers, figures, or other pages ought to exist.

## Steps

1. **Lock the ratified census.** Read the final T07/propagation decisions and enumerate every admitted publication-body record across root Symbolon, Matheme, Mytheme, and Episteme. The census must include dispositions for:
   - the former/live argument inventory;
   - all developed concept nodes;
   - the recovered `symbolon/episteme/concepts/reference-notes/` shelf;
   - roots, paths/maps, histories, etymologies, dossiers, figures, dialogues, plates/media, theorem/formal-neighbour records, and source-facing depth where ratified;
   - every newly created/split/merged/rehomed record from the final quilt.

   Historical counts are evidence of former state, never quotas. A recovered reference note is not automatically a concept; it must nevertheless have an explicit surviving carrier or disposition. *Done when every candidate-bearing item in the ratified field has a named canonical home or an explicit merge/redundancy disposition.*

2. **Assemble the intake.** Run the intake helper:
   ```bash
   python3 .agents/skills/return-of-zero-build/workflow.py intake \
     --project-root /Users/admin/Documents/Nara-Personal/Antykathera-Essay-Work \
     --output intake.json
   ```
   The helper reads the quilting surfaces as discovery inputs. Treat its output as a mechanical aid and reconcile it against the ratified census from Step 1. The current helper is intentionally conservative and **must not be used as completeness proof**. Add any ratified record absent from its scan before dispatch. *Done when `intake.json` and the ratified census agree on every page to be developed, with identity, home, register, and source inputs.*

3. **Dispatch one subagent per element.** For each element in the reconciled intake manifest, launch an independent agent with:
   - the element's ratified quilt/census decision and relevant contribution(s);
   - its canonical source house, argument node, concept/reference-note material, and transverse relations as applicable;
   - the register's README contract;
   - the `return-of-zero-pages` skill, including its raw QL six-position page-form law;
   - the `return-of-zero-links` skill;
   - `return-of-zero-visuals` if the element needs an asset.
   Agents must be blind to each other's drafts. *Done when every admitted element has a drafted page in its canonical home.*

4. **Wait at the barrier.** No agent proceeds to hygiene until all element drafts are complete. *Done when the last agent reports its page written.*

5. **Run hygiene.** Execute:
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

6. **Run the census-backcheck.** Compare the developed Symbolon directory back against the ratified census, not merely against `intake.json`. Every ratified record must exist once at its canonical home; every old/recovered candidate must have the disposition recorded at Step 1; no page may have appeared merely because a stale historical inventory named it. *Done when the publication body and the ratified census are bijective at record identity level, allowing explicitly declared non-page carriers.*

7. **Report, don't certify.** The build ends with a hygiene + census report. It does not self-certify philosophical or compositional correctness — only that the deterministic gates and ratified record census were respected.

## Essential and tangential

Every admitted element receives full development attention appropriate to its register. A leaf page and a dense braid can both be complete while carrying different publication weight. Frontmatter weighting (`argument_weight`, `consumed_by`, `source_role`, and ratified equivalents) decides how each turns up in mapping and navigation after the build.

The preservation law remains active: not belonging in linear essay prose is never itself grounds for deletion. Radial-depth and supporting-visible records are first-class publication work.

## Common mistakes

- Treating the old `21 arguments`, `22 concepts`, or any other historical count as a target inventory.
- Forgetting the recovered reference-note shelf because those files are not yet developed concepts.
- Letting `workflow.py intake` define the authored field from Markdown headings/XML blocks.
- Dispatching agents who share drafts or read each other's outputs before the barrier.
- Generating the MOC or intents layer before the written links exist.
- Skipping hygiene because the pages "look fine."
- Treating the intake manifest as the source of truth rather than the ratified quilt/census it serves.
