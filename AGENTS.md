# Return of Zero development instructions

This subtree develops *The Return of Zero*, its source bank, its authoring rooms, and its submission artifacts. Do not invoke or import skills from the installed S5 Epi-Logos plugin. In particular, never use the installed `epi-logos-voice`: it governs a different essay. Use only the local development skills and tools in this subtree.

## Wiki-first development

Codex discovers this project's four focused skills under `.agents/skills/`: `return-of-zero-orient`, `return-of-zero-source`, `return-of-zero-write`, and `return-of-zero-review`. Use `tools/okf-workspace.py` when a task needs canonical retrieval, traversal, effects, or source context. Ordinary conversation and exploration can remain in chat until canonical material becomes relevant. Do not fall back to an essay skill outside this Git root. Sections, arguments, concepts, paths, plans, rooms, canonical sources, governing documents, and submission files retain their own names, types, authority, and status.

For the one-file functional map of the whole repository — every surface, its authority, its entry point, and its final home under the symbolon shape — read `docs/REPOSITORY-SHAPE.md` before exploring. It exists so agents do not have to reconstruct the repo from scattered reads.

An index, generated context, BKMR hit, room summary, or model memory is a locator, never authority. Before a canonical change, recover the positive proposition, local operation, inherited position, outgoing movement, source task, and any qualification that is genuinely live. If essential context cannot be recovered, name the debt and continue retrieval.

## Continuity and effect mapping

When a source, concept, theorem, or transverse thread bears the work of a change, run `python3 tools/okf-workspace.py --project-root . effects <source-or-concept> --depth 4 --json` before writing. The result maps declared consumers, downstream canonical paths, and declared transverse thread membership. It is an effect map, not a semantic guesser: never infer a relation from shared vocabulary, tags, or folder adjacency.

Read the whole declared transverse thread before changing one of its members. Preserve the local movement's exact role in the complete movement; do not sever a connection merely because it passes from formal, phenomenological, psychic, social, mythic, or technical registers. Equally, do not merge distinct wholes merely because they meet at one point. Check `local_copy` on internal canonical sources before describing material as unavailable; a stale source-locality claim is a provenance debt to repair from the actual local object.

## Authority order

1. `the-return-of-zero-central-plan.md` is the sole live structural authority.
2. `return-of-zero-orienting-principles.md` is mandatory orientation and subordinate to the plan.
3. Live section, argument, concept, and traversal nodes carry the canonical granular argument.
4. `submission-package/essay/symbolon/episteme/sources/<primary_domain>/<author>/<source_id>/SOURCE.md` is the one canonical source house for work identity, passages, learning material, citation, quotation, provenance, and consumption. Sources are filed by epistemic domain and then by author; resolve `source_id` to a path via `tools/source_resolver.py`, never by assuming nesting depth.
5. An optional `NOTES.md` beside a source is Frank's authorial encounter with that work. Agents read it whenever they open the source and never create, edit, append, normalise, or relocate it. Its copied quotations are leads until independently verified in `SOURCE.md`; its insights disclose authorial intent without becoming source attribution.
6. `submission-package/essay/THE-RETURN-OF-ZERO.md` is the sovereign manuscript. Generated `ROOM.md` files are compact authoring refractions; protected `READING.md` files are optional cross-source learning routes. Neither rooms nor retrieval adapters supersede canonical nodes.
7. `working/legacy/` is frozen provenance and governs nothing. Raw chat transcripts under `working/sources-texts-references/chat-logs-for-quilting/` are the `local_copy` shelf for the Taylor dialogue records under `submission-package/essay/symbolon/episteme/sources/internal-corpus/taylor/chat-logs/`; those records are typed `dialogue-record` — provenance of thinking, never evidence.
8. Submission design documents describe intended artifacts; they do not override the live essay or developer workflow.

`WRITING-PROTOCOL.md` is the live workflow and publication-shape authority for the multi-model written edition and ontology-led vault. It is subordinate to the central plan and canonical argument. Dated files in `submission-package/` are provenance unless the protocol explicitly promotes them. The publication body has one home: `submission-package/essay/` — the rooms (`#0`), the field (`#1`–`#4`, `symbolon/` inside it), and the sovereign essay (`#5`). `working/` holds the non-publication development surfaces (ledgers, raw authorial shelves, legacy, working drafts). Nothing is maintained as a generated duplicate of the canonical body.

## Status and voice

Keep these axes independent:

- `claim_status`: Derived, Argued, Offered, or Open.
- source relation: Extracted, Paraphrased, Argued from, or Resonant with.
- citation and quotation readiness.
- artifact authority and freshness.
- current agent retrieval confidence.

Missing citation or quotation readiness never downgrades an internally Derived or Argued position. Scope the claim accurately and preserve its earned force. Use `may`, `might`, `perhaps`, or `could` only for a named modal, causal, empirical, or genuinely open uncertainty. Never turn the essay's position into a merely acceptable neighbouring position.

For authored prose, use the project-local `return-of-zero-write` skill when its writing guidance is needed. Frank's `[F]` blocks, the master manuscript, and any Frank-authored `SCRATCH.md` are sovereign.

Preliminary publication work occurs on `main` without new writing worktrees. Model-written versions begin only from one ratified base commit and use sequential `codex/write-<model-slug>` branches under the common execution receipt defined in `WRITING-PROTOCOL.md`.

## Hooks and optional continuity

Trusted project hooks in `.codex/hooks.json` load compact orientation at session start, restore any agent mutation of source-house `NOTES.md`, and stop completion when canonical source or room changes leave generated projections stale. The hook handler is `.codex/hooks/return_zero_hook.py`; inspect active hooks with `/hooks` in Codex.

`working/active-ideas.json` is an optional, explicit continuity surface. Add an idea only when Frank and the agent deliberately choose to retain it; keep its provenance, context, current relevance, and optional next use. It is not a session ledger or a place for reasoning traces. Manage it with `python3 tools/project-agent-harness.py ideas --help`.

## Argument sovereignty and skill routing

Use only project-local essay skills for this work. Invoke retrieval, source, writing, or review guidance according to the actual task; do not impose a compulsory pipeline on conversation or exploration.

Before advising on, revising, or evaluating an argument, recover the author's declared proposition and its register. Treat that proposition as the working claim. Keep separate: (1) whether the project licenses an operation in its stated derived, argued, offered, matheme, mytheme, or applied register; and (2) what a source can establish about historical attribution. An evidence debt in (2) never authorises replacement of (1) with a safer adjacent thesis.

At the matheme/mytheme register, identify the formal operation the image performs. Do not collapse that operation into a question of authorial intention unless the user asks the historical question. A caveat is admissible only for a concrete false attribution, material conflation, invalid inference, or genuinely Open empirical question; it must state what survives the caveat. If the intended operation cannot be recovered, ask for it rather than choosing a different argument.

## Native theorem-language and field conduct

The notation, determinations, and derivational operations in `working/sources-texts-references/10-7-2026-core-theorems-pithy.md` and their designated supporting files are Frank's native QL language. They are not borrowed doctrines waiting to be validated by Jung, calculus, theology, music, topology, or any other neighbouring discourse. Those fields can refract, witness, or qualify a QL operation only after their distinct relation has been recovered.

In particular, **`X/x` is authorial QL notation**. It works in the algebraic register, where `x` is the indefinite particular, and at once in the mythematical, musical, narrative, psychic, and ontological registers that the matheme opens. Never call `X/x` Jungian, or present it as Jung's notation. A Jungian register may be mapped only as a named cross-register refraction after the authorial derivation has been read first.

When an inquiry touches one determination, theorem, or braid, recover the whole active field before interpreting a local token: the core theorem spine, **all eight determinations**, their sequence and inversions, and the directly declared supporting files. Do not answer from the nearest phrase, a local node, or a remembered gloss. The task is to locate the question in the living system, not to make a competent paraphrase of one of its surfaces.

Do not turn an established authorial operation into an agent's discovery, achievement, “win,” or introductory lesson; **do not present it as a discovery** when the author has already established it. Begin from the live pressure in the question; state the precise relation already established; then follow the unresolved movement through its neighbouring determinations, registers, and inversions. **Never introduce a strawman**—a conservative default, a fake binary, or an unnamed weaker view—merely to restate an established claim as a victory. If a comparison is necessary, name its actual source, operation, and local consequence. Preserve the intuitive continuity of the work; do not bury it under administrative enumeration or generic connective prose.

## Development and testing

Use tests that exercise the real workspace and real commands. Do not satisfy audits with placeholder prose or mocked graph behaviour. Generated indexes and BKMR databases are disposable; canonical Markdown is not. Repair canonical nodes only from existing governing material, never by inventing missing argument content.
