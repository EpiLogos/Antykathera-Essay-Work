---
name: return-of-zero-build
description: Use when turning a ratified census of Return of Zero field elements into their developed pages by subagent fan-out and hygiene.
---

# Build Return of Zero Field Pages

Turn the ratified authored field into developed pages deterministically: census lock → **A01–A36 depth recovery** → intake → dispatch → barrier → hygiene.

The build is **not** itself the canonical census. It consumes the census produced by quilting, harmonisation, ratification, and propagation. A heading scanner or the current contents of one directory can never prove that the authored field is complete.

The build is also **not recursive summarisation**. The T09 A/C pages are first materialisations and routing authorities, not substitutes for the developmental corpus from which P2 must recover depth.

## When to use

- The quilt has been ratified and propagated into a current canonical field census.
- Multiple field pages need development in one coordinated pass.
- A hygiene stage is required after page development to validate links and regenerate navigation.

Do not use for one-off page edits; use `return-of-zero-pages` for those. Do not use before the ratification/propagation gate to decide how many arguments, concepts, roots, paths, histories, dossiers, figures, or other pages ought to exist.

## Mandatory companion contract

Before queue assembly read:

`working/final-argument-quilt-2026-08-23/P2-A01-A36-DEPTH-RECOVERY-CONTRACT.md`

That contract governs the **Argument-depth axis** beneath the register batches. Every A01–A36 recovery track must touch every current file in `submission-package/essay/quilt/`, read every materially implicated canonical `SOURCE.md` house and sibling protected `NOTES.md` where present, and distinguish recoverable Taylor-authored signal from later AI developmental synthesis where provenance permits.

## Steps

1. **Lock the ratified census.** Read the final T07/propagation decisions and enumerate every admitted publication-body record across root Symbolon, Matheme, Mytheme, and Episteme. The census must include dispositions for:
   - A01–A36 and the historical/live argument inventory that bears their provenance;
   - C01–C64 and all developed/legacy concept nodes;
   - the recovered `symbolon/episteme/concepts/reference-notes/` shelf;
   - Etymology whole-fields;
   - roots, paths/maps, histories, dossiers, figures, dialogues, plates/media, theorem/formal-neighbour records, and source-facing depth where ratified;
   - every newly created/split/merged/rehomed record from the final quilt.

   Historical counts are evidence of former state, never quotas. A recovered reference note is not automatically a concept; it must nevertheless have an explicit surviving carrier or disposition. *Done when every candidate-bearing item in the ratified field has a named canonical home or an explicit merge/redundancy disposition.*

2. **Build the 36 Argument-depth packets before bulk dispatch.** Create one working recovery packet for every A01–A36 according to `P2-A01-A36-DEPTH-RECOVERY-CONTRACT.md`.

   Each packet must:
   - begin from the current canonical A page but not stop there;
   - recover its historical Argument/developmental carriers and named direct Taylor/theorem/source carriers;
   - inspect **every current file** in `submission-package/essay/quilt/` and record distinct yield or `no distinct yield`;
   - treat `27-07-26-QUILTING-FOR-FULL-ARGUMENT.md` as the primary additive developmental quilt rather than letting later harmonisations erase its unique contributions;
   - open every materially implicated canonical `SOURCE.md` and read sibling protected `NOTES.md` where present;
   - use `NOTES.md` for Frank's authorial encounter/intention/quotation leads while keeping it read-only and distinct from external evidence;
   - recover original formulations, images, asymmetries, qualifications and operations that later AI summaries flattened where provenance permits;
   - route recovered material to the correct A/C/E/root/Matheme/Mytheme/Episteme/publication office rather than stuffing everything into the A page;
   - record genuine structural pressure for T22 rather than silently changing the census.

   These packets are working derivational receipts, not 36 new canonical identities. *Done when all A01–A36 have a recovery packet and the packet set demonstrates complete live quilt coverage.*

3. **Assemble the intake.** Run the intake helper with the actual repository root:
   ```bash
   python3 .agents/skills/return-of-zero-build/workflow.py intake \
     --project-root <LOCAL_REPO_ROOT> \
     --output intake.json
   ```
   The helper reads quilting surfaces as discovery inputs. Treat its output as a mechanical aid and reconcile it against the ratified census from Step 1 **and the 36 depth packets from Step 2**. The current helper is intentionally conservative and **must not be used as completeness proof**. Add any ratified record absent from its scan before dispatch. *Done when `intake.json`, the ratified census and the A-depth packet set agree on every page to be developed, with identity, home, register, source inputs and Argument-depth provenance.*

4. **Dispatch one subagent per element.** For each element in the reconciled intake manifest, launch an independent agent with:
   - the element's ratified quilt/census decision and relevant contribution(s);
   - every materially bearing A-depth packet, not merely the shortest or nearest Argument summary;
   - its canonical source house(s), including protected `NOTES.md` read-only when present and relevant;
   - direct Taylor/authored/developmental carriers identified by the depth packet;
   - concept/reference-note material and transverse relations as applicable;
   - the register's README contract;
   - the `return-of-zero-pages` skill, including its raw QL six-position page-form law;
   - the `return-of-zero-links` skill;
   - `return-of-zero-visuals` if the element needs an asset.

   The writing question is **not** “how can I expand the canonical summary?” It is “what developed operation, source relation, image, formal structure or authored pressure must this record make available without duplicating another office?”

   Agents must be blind to each other's drafts. *Done when every admitted element has a drafted/deepened page in its canonical home.*

5. **Wait at the barrier.** No agent proceeds to hygiene until all element drafts in the batch are complete. *Done when the last agent reports its page written.*

6. **Run hygiene.** Execute:
   ```bash
   python3 .agents/skills/return-of-zero-build/workflow.py hygiene \
     --project-root <LOCAL_REPO_ROOT> \
     --intake intake.json
   ```
   The hygiene stage runs:
   - `tools/okf-workspace.py doctor --json` for debt counts (missing-register, unresolved-link);
   - `tools/okf-workspace.py links --json` for link-health detail;
   - `tools/okf-workspace.py effects <source-or-concept> --depth 4 --json` for every changed consumer;
   - MOC/intents aggregation from written links only.
   *Done when the report lists no unresolved links, no alias capture by frozen stubs, and no unresolved one-home violations.*

7. **Run Argument-depth backcheck and T22 fold-back.** After each register batch, compare the drafted pages back against the A-depth packets:
   - which recovered operations were actually surfaced;
   - which canonical A pages need substantive enrichment or provenance restoration;
   - which material correctly landed in another register instead;
   - which `Depth Restoration` debts were discharged;
   - which source debts remain Open;
   - which genuine structural pressures require T22.

   Do not wait until the end of all P2 batches to discover that a rich original formulation was compressed away. *Done when every affected A packet has a batch result and all structural pressure has an explicit fold-back disposition.*

8. **Run the census-backcheck.** Compare the developed Symbolon directory back against the ratified census, not merely against `intake.json`. Every ratified record must exist once at its canonical home; every old/recovered candidate must have the disposition recorded at Step 1; no page may have appeared merely because a stale historical inventory named it. *Done when the publication body and the ratified census are bijective at record identity level, allowing explicitly declared non-page carriers.*

9. **Report, don't certify.** The build ends with a hygiene + census + Argument-depth report. It does not self-certify philosophical or compositional correctness. It must, however, demonstrate that the deterministic gates, ratified record census, full quilt corpus and per-Argument depth recovery were respected.

## Essential and tangential

Every admitted element receives full development attention appropriate to its register. A leaf page and a dense braid can both be complete while carrying different publication weight. Frontmatter weighting (`argument_weight`, `consumed_by`, `source_role`, and ratified equivalents) decides how each turns up in mapping and navigation after the build.

The preservation law remains active: not belonging in linear essay prose is never itself grounds for deletion. Radial-depth and supporting-visible records are first-class publication work.

The authorial-recovery law is equally active: later AI harmonisation is a map and interpretive aid, not permission to erase a distinct Taylor-authored operation merely because a newer summary is shorter or smoother.

## Common mistakes

- Treating the old `21 arguments`, `22 concepts`, or any other historical count as a target inventory.
- Treating T09 A/C first-materialisation pages as sufficient enrichment source material.
- Forgetting the recovered reference-note shelf because those files are not yet developed concepts.
- Failing to touch every live file under `submission-package/essay/quilt/` for every A-depth track.
- Reading `SOURCE.md` but ignoring a relevant sibling `NOTES.md`, thereby losing the authorial reason the source entered the work.
- Treating protected `NOTES.md` as external evidence or editing it.
- Preferring a polished AI paraphrase over a materially richer recoverable authorial formulation.
- Attributing mixed chat/dialogue language to Taylor when user/assistant provenance cannot be distinguished.
- Letting `workflow.py intake` define the authored field from Markdown headings/XML blocks.
- Dispatching agents who share drafts or read each other's outputs before the barrier.
- Generating the MOC or intents layer before the written links exist.
- Skipping hygiene because the pages "look fine."
- Treating the intake manifest as the source of truth rather than the ratified quilt/census and Argument-depth recovery it serves.
