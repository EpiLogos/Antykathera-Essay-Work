# Return of Zero — repository instructions

This repository develops *The Return of Zero*, Frank's submission to **Agentworld**, a
special issue of the *Antikythera: Journal for the Philosophy of Planetary Computation*
(MIT Press). It advances Quaternal Logic (QL), the Meta-Epistemic Framework (MEF) and
Epi-Logos. It holds the publication body, the source bank that body draws on, the
authoring rooms, the working desk, and the tooling that keeps them consistent.

Two rules hold everywhere below. Frank's written words — his `[F]` blocks, the sovereign
manuscript, any `SCRATCH.md` he has written — are ground truth: you propose against them,
you never replace them. And nothing canonical is invented. If the material a change needs
cannot be recovered, name the debt and keep retrieving; never write the missing argument
yourself.

## Read in this order

1. `README.md` — orientation and the argument in brief.
2. `AGENTS.md` — this file.
3. `WRITING-PROTOCOL.md` — workflow and publication-shape authority.
4. `the-return-of-zero-central-plan.md` — the sole structural authority.
5. `return-of-zero-orienting-principles.md` — mandatory before touching any section, argument, room, or dossier.
6. `docs/REPOSITORY-SHAPE.md` — the one-file functional map: every surface, its authority, its entry point, its final home. Read it before exploring, so the repository does not have to be reconstructed from scattered reads.

## Authority order

1. `the-return-of-zero-central-plan.md` is the sole live structural authority.
2. `return-of-zero-orienting-principles.md` is mandatory orientation, subordinate to the plan.
3. Live section, argument, concept and traversal nodes carry the canonical granular argument.
4. `submission-package/essay/symbolon/episteme/sources/<domain>/<author>/<source_id>/SOURCE.md` is the one canonical source house for work identity, passages, learning material, citation, quotation, provenance and consumption. Resolve `source_id` to a path through `tools/source_resolver.py`; never assume nesting depth.
5. An optional `NOTES.md` beside a source is Frank's authorial encounter with that work. Read it whenever you open the source; never create, edit, append, normalise or relocate it. Its quotations are leads until independently verified in `SOURCE.md`, and its insights disclose intent without becoming source attribution.
6. `submission-package/essay/THE-RETURN-OF-ZERO.md` is the sovereign manuscript. Generated `ROOM.md` files are compact authoring refractions; protected `READING.md` files are optional cross-source learning routes. Neither supersedes a canonical node.
7. `working/legacy/` is frozen provenance and governs nothing. Raw chat transcripts under `working/sources-texts-references/chat-logs-for-quilting/` are the `local_copy` shelf for the Taylor dialogue records under `episteme/sources/internal-corpus/taylor/chat-logs/`; those records are typed `dialogue-record` — provenance of thinking, never evidence.
8. Dated design documents describe intended artifacts; they never override the live essay, the live nodes, or the developer workflow.

`WRITING-PROTOCOL.md` is the live workflow and publication-shape authority for the written
edition and the ontology-led vault. It is subordinate to the central plan and the canonical
argument. Dated files under `submission-package/` are provenance unless the protocol
promotes them.

## The publication body, the rooms, and the field

The publication body has exactly one home: `submission-package/essay/`. It carries three
things.

- The **sovereign essay**, `THE-RETURN-OF-ZERO.md`, parallel to the field.
- The **field**, `symbolon/`, in the 4+2 with fixed offices: `#1` Symbolon, `#2` Matheme,
  `#3` Mytheme, `#4` Episteme, with `#0` the rooms and `#5` the essay framing them. The
  four infer into the rooms; the rooms improve the essay. `register` is the content's own
  anatomy, declared in frontmatter, independent of node type.
- The **rooms**, `section-rooms/`: eight rooms of six movements each — 48 in order, each
  naming its previous and next step, with M48 returning to M01.

The rooms' implicate ground is the **canonical A/C suite** in Episteme: 36 arguments
(A01–A36), 36 conjugates (A01′–A36′), 64 concepts (C01–C64) and the A/C root — 137 records
in one home. Each room's `P1-CANONICAL-ALIGNMENT.md` is the per-movement route into it.
The 21 historical files under `section-rooms/arguments/` are **provenance**: earlier
carriers, typed `legacy-argument` with `authority: historical-provenance`, each pointing at
its developed successor. They are not the rooms' argument field, and their count is not a
census of anything live. `submission-package/essay/README.md` is the authored reading root.

`working/` holds the non-publication surfaces only: ledgers, raw authorial shelves, legacy,
working drafts, the deletion queue. It never becomes authority, and nothing is maintained as
a generated duplicate of the publication body.

## Conduct

- **Propose, do not overwrite.** Frank authors what he states or commissions. You author what you infer, and you mark it as inferred. For anything beyond a small, unambiguous correction to what he asked for: name the target, the change, and the consequential tradeoff first.
- **Do not stage established work as your discovery.** No "win", no achievement framing, no introductory lesson. Begin from the live pressure in the question, state the relation already established, then follow the unresolved movement into its neighbouring determinations, registers and inversions.
- **Never introduce a strawman** — a conservative default, a fake binary, an unnamed weaker view — to restate an established claim as a victory. If a comparison is needed, name its actual source, its operation and its local consequence.
- **Keep the status axes independent.** `claim_status` is Derived (proof), Argued (reasoned cross-domain), or Offered (generative conjecture). The source relation is Extracted, Paraphrased, Argued from, or Resonant with. Citation readiness and quotation readiness are further, separate states, as are artifact authority and your own retrieval confidence.
- **Missing citation readiness never downgrades an internally Derived or Argued position.** Scope the claim accurately and preserve its earned force. Use `may`, `might`, `perhaps` or `could` only for a named modal, causal, empirical, or genuinely open uncertainty — never to soften the essay's position into an acceptable neighbouring one.
- **A relation that bears the work must be recovered before you write.** Run `python3 tools/okf-workspace.py effects <source-or-concept> --depth 4 --json`, reopen every returned canonical consumer, and read the whole declared transverse thread. The map follows declared links and thread metadata only; it is never a licence for association by shared vocabulary, tags or folder adjacency. Do not sever a connection because it passes from formal, phenomenological, psychic, social, mythic or technical registers; and do not merge distinct wholes because they meet at one point.
- **Check `local_copy` before saying material is unavailable.** A stale source-locality claim is a provenance debt to repair from the actual local object.
- **The prose register has its own gate.** `writing-guidance-tools/README.md` is the entry point for all authored prose; its load contract governs — draft cold with only `references/WRITING-LAWS.md` and `references/WRITING-RUBRIC.md` open, audit against the rubric with `references/comparative-and-negation-gate.md` in the same pass, and only then calibrate selectively. Calibration files are never pre-loaded. No single-pass prose ships.

## Sources and evidence

`submission-package/essay/symbolon/episteme/sources/README.md` is the governing protocol.
It holds in full; these are its load-bearing points.

1. **A source is a recoverable object** — one book, edition, article, transcript, dataset or internal manuscript, with one stable `source_id` and one canonical `SOURCE.md`. Never create a source for a person, a concept or an argument.
2. **Chicago 18 Notes and Bibliography**, citing the exact edition consulted. Prefer DOI URLs for articles.
3. **Citation readiness never licenses a quotation.** A quotation requires exact transcription, edition, locator, context check, transcription method, verifier and date, and a named consuming claim.
4. **No evidence tiers.** No `A`/`B`/`C`, no "primary tier", no single ordinal standing in for analysis. Track `source_role`, `metadata_status`, `edition_status`, `citation_status`, `quote_status` and exact consumption independently.
5. **Keep developed synthesis in its owning argument.** A source file may carry sustained scholarship and its consumers; the essay's developed inference belongs in an argument or concept node.
6. **Name the evidential relation**, and never make a source author endorse the essay's inference. Gödel does not prove QL; Bohm does not formulate the tattvas; a tokamak does not prove the arche-topos.
7. **The internal corpus is first-class provenance, not public warrant.** It establishes origin and content for in-house claims; anything historical, textual, mathematical or technical leaving it needs a public source.
8. **The derivational chat is never a public citation.** Resolve every attribution, quotation, fact and etymology to a source record; resolve every original inference to its argument node.
9. **Acquire passages in pairs** — one supporting and one limiting or qualifying — so the bank never becomes an anthology of convenient lines.
10. **Intake before prose.** New leads enter the intake queue; only verified passages are wired into section prose.

`/Users/admin/Documents/Books/` is an external deep-reference pool for discovery and
locating material Frank holds. It is not a licence to quote or redistribute. Verify the
edition in the source bank and keep citation and quotation readiness separate; a copy with
unclear rights provenance is a locator lead only.

## Retrieval

Retrieval runs through AIKit — one seam, no second index.

```bash
aikit wiki ingest --room-depth 2 submission-package/essay   # compile the vault into the Wiki + SourcePool
aikit knowledge search "<query>"                            # what the search faculty reads, incl. tag:<value>
AIKIT_BIN=<path> python3 -m unittest tests.test_aikit_wiki_parity -v
```

A file declaring `record_id` becomes a curated Wiki node; a file declaring `source_id`
becomes a SourcePool binding carrying its authored `tags:`; citing a source never curates
it. The former local shim — `tools/bkmr-essay`, its adapters and the SQLite databases under
`.bkmr/` — was a second index over the same corpus and is **retired**. The six collections
it covered (884 canonical paths) are frozen in `tests/fixtures/retired-bkmr-coverage.json`
and asserted against a live ingest by `tests/test_aikit_wiki_parity.py`, which skips rather
than fails when `aikit` is absent. Lexical search is local; semantic indexing stays opt-in
and may carry only lawful, non-sensitive derivative metadata. A retrieval suggestion never
makes a citation or quotation verified.

## Native theorem-language and field conduct

The notation, determinations and derivations in
`working/sources-texts-references/10-7-2026-core-theorems-pithy.md` and their designated
supporting files are Frank's native QL language. They are not borrowed doctrines awaiting
validation from Jung, calculus, theology, music or topology. Those fields may refract,
witness or qualify a QL operation only after their distinct relation has been recovered.

**`X/x` is authorial QL notation.** It works in the algebraic register, where `x` is the
indefinite particular, and at once in the mythematical, musical, narrative, psychic and
ontological registers the matheme opens. Never call it Jungian or present it as Jung's
notation; map a Jungian register only as a named cross-register refraction, after the
authorial derivation has been read first.

Before interpreting a local token, recover the whole active field: the core theorem spine,
**all eight determinations**, their sequence and inversions, and the directly declared
supporting files. Do not answer from the nearest phrase, a local node or a remembered gloss.

## Authored and generated surfaces

Some surfaces are written by hand and some are built. Never hand-edit a generated file;
change its source and rebuild.

| Surface | Built by |
|---|---|
| `section-rooms/README.md` and every `ROOM.md` | `tools/build-section-rooms.py` |
| `symbolon/episteme/maps/navigation/` — `MOC.md`, `intents/`, `AUDIT.md`, `audit.json` | `tools/build-navigation.py` |
| source projections (`SOURCE-INDEX.md`, `PASSAGE-LEDGER.md`, `MAIN-SOURCES.md`) | `tools/build-source-projections.py` |
| room-depth and reader-navigation audits | `tools/audit-room-depth.py`, `tools/audit-reader-navigation.py` |
| pre-manuscript gate | `tools/audit-pre-manuscript.py` |

Generated surfaces carry locator authority, never canonical authority. Each builder takes
`--check`, and the stale projections are wired into the completion hook, so a canonical
change that leaves a generated surface stale stops completion rather than shipping. OKF is
a formatter and validator over the vault, not a generator.

## Skills and runtimes

Eight project skills live under `.agents/skills/`: `return-of-zero-orient`, `-source`,
`-write`, `-review`, `-links`, `-pages`, `-build`, `-visuals`. Use them for this work, and
do not fall back to an essay skill outside this Git root.

**Do not invoke or import skills from the installed S5 Epi-Logos plugin.** In particular
never use the installed `epi-logos-voice`: it governs a different essay.

Claude Code discovers the same eight skills through `.claude/skills/`, which are symlinked
projections of `.agents/skills/` rather than a second editable copy. Both runtimes register
the same handler — Codex through `.codex/hooks.json`, Claude through `.claude/settings.json`
— calling `.codex/hooks/return_zero_hook.py`. That handler loads compact orientation at
session start, restores any agent mutation of a source-house `NOTES.md`, and stops
completion when canonical changes have left generated projections stale.

`working/active-ideas.json` is an optional continuity surface, not a session ledger. Add an
idea only when Frank and the agent deliberately choose to retain one; manage it with
`python3 tools/project-agent-harness.py ideas --help`.

## Development and testing

```bash
python3 -m unittest discover -s tests -v      # the suite; exercises the real workspace
```

Tests use the real workspace and real commands. Never satisfy an audit with placeholder
prose or mocked graph behaviour: a test that passes against a fixture proves nothing about
the essay. Generated indexes and retrieval databases are disposable; canonical Markdown is
not. Repair a canonical node only from existing governing material.

## Writing branches

Preliminary publication work happens on `main`, in the ordinary working directory, with no
new writing worktrees. A model-written version begins only from one ratified base commit
and uses a sequential `codex/write-<model-slug>` branch under the common execution receipt
defined in `WRITING-PROTOCOL.md` (§7). Model branches are never rebased on, merged from, or
shown each other's prose before comparison.
