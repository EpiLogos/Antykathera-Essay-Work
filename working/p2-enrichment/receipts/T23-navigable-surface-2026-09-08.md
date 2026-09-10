# T23 — navigable surface: what was built, what the audit found, what is open

**Ticket:** [T23 / #24](https://github.com/EpiLogos/Antykathera-Essay-Work/issues/24). **Branch:** `main`, uncommitted at the time of this receipt. **Authorised by:** Frank, 2026-09-08, after the T20–T21 acceptance. **STOP before T24** until Frank has reviewed the surface and decided the three proposals at the end.

## Method

The ticket's order was kept: audit the written relations first, then author the entry pages, then generate the post-hoc MOC/intents layer from the written links only. No relation was inferred from vocabulary, tags or folder adjacency. Link resolution reused the project's own `Workspace` (aliases, priorities); a second regex resolver over-reported dangling links by three orders of magnitude and was discarded.

## Built

- **Reading root** — `submission-package/essay/README.md`, authored. The four ways in (linear, radial, transverse, toroidal) each with a concrete first step; the 4+2 with live links; the eight stations with burden, room and first movement; how a page reads (status marks, source relations, the raw sixfold, the thirteen relation words, return); the navigation aids. Before this pass the root carried no links at all.
- **Rooms index** — `section-rooms/README.md`, now rendered by `tools/build-section-rooms.py` (v2.1.0): the eight rooms with all 48 movements, reading routes and canonical alignments; the pre-T09 `arguments/` carriers listed as provenance only. Every generated `ROOM.md` carries a "where you are" line (reading root · rooms · station · room *n* of 8 · previous · next) and every waypoint now names its **canonical route** (the A/C links from the room's authored `P1-CANONICAL-ALIGNMENT.md`) before its provenance carriers. Frank's mid-session correction: the historical count of 21 must not be presented as the rooms' argument field; the implicate `0` of the rooms is A01–A36 / C01–C64.
- **Register entry pages** — `symbolon/mytheme/README.md`, `symbolon/episteme/README.md` and `episteme/histories/README.md` rewritten so the reader lands on the register's proposition and entrances; the dated programme notes that opened them are moved to a `Standing` footer with their links intact. Mytheme's seven medium facets are linked as browse routes (they were orphans). `episteme/conjugate/README.md` now lists all 37 conjugate pages (A26′ was an orphan). `concepts/README.md` and `sources/README.md` had their shelf/admin references made into live links.
- **Curated paths** — `episteme/maps/README.md` states the whole-thread reason for each of the four paths and points at the generated layer.
- **Generated navigation layer** — `episteme/maps/navigation/` built by the new `tools/build-navigation.py`: `MOC.md` (the 4+2 by class with page and written-relation counts, entrances, intents), `intents/<class>.md` (per page: what it implicates and what reaches it, grouped by relation word; large classes split by folder), `AUDIT.md` and `audit.json`. Relation words are read from the sentence around each link: a bold word anywhere in the sentence, a plain word only within 60 characters. Frontmatter `source_ids`, `consumed_by_arguments`, `movement_ids`, `quote_ids` and companion notes are carried as declared relations. `--check` fails on staleness and is wired into the completion hook beside the room and source projections. `tools/okf-workspace.py` types the layer `navigation-projection` with `generated-locator` authority so it never counts as a canonical path.
- **Hygiene** — two Levinas source-house links (`[[Compassion]]`, `[[Reflective Field]]`) repointed to A35 and A32. Doctor unresolved links in the body: 4 → 2 (the remaining two are `Dreamcode`, a deliberate naming-debt marker in the Descartes house, and `Antykathera Essay Work` in Frank's authorial core-theorems text). Retrieval adapters resynced.
- **Tests** — `tests/test_build_navigation.py` (7 real-workspace tests: freshness, generated-locator authority on every surface, every generated link resolves, the reading root reaches every canonical class, the four paths are declared threads or the spine, relation-word detection, classification). Full suite: the eleven inherited failures/errors recorded in the T22 log remain and no new failure was introduced; the room, audit, source-projection and navigation modules pass.
- **Skills and maps** — `.agents/skills/return-of-zero-links/SKILL.md` step 6 now names the builder; `docs/REPOSITORY-SHAPE.md`, `CLAUDE.md` and the wayfinder handoff record T23; a process-ledger entry records the lessons.

## What the audit found

| Measure | Before | After |
|---|---|---|
| Pages reachable from the reading root by written links | 1 of 764 | 717 of 764 |
| Deepest page (clicks from root) | — | 6; 556 pages within two clicks |
| Orphans (no written inbound) | 49 | 36 (34 reference-notes shelf, `SOURCE-TEMPLATE.md`, `research-intake-inbox.md`) |
| Pages with no written route back into the essay | 202 | 199 |
| Doctor unresolved links in the body | 4 | 2 |
| Body links carrying a relation word in their sentence | — | 3,806 of 8,503 (45%) |

Unreachable after this pass: 45 reference-notes (the quilt-pending provenance shelf, whose README does not list them; the generated intents page does) and the two source admin files.

The 199 pages without a written return route: 79 in source houses (bibliographic records whose consumers are declared only from the consuming side), 55 reference-notes, 40 domain README pages, 25 others (register READMEs, atlas pages, two etymology histories, one dossier-free lens, A11 and the conjugate root). The generated intents pages supply the inverse for every one of them, so a cold reader can get back; the authored debt stays visible for T24.

Named-relation ratio by class: Symbolon root 83%, Arguments 82%, dossiers 88%, etymologies 76%, histories 68%, matheme 63%, mytheme 62%, conjugate 52%, concepts 49%, movements 48%; source houses 9%, historical argument carriers 4%, maps 2%. The low classes are structural (bibliographic lists, pre-vocabulary prose, path lists), not careless.

## Open — Frank's decisions

1. **Vault root.** The Obsidian configuration sits at `symbolon/.obsidian/` (`useMarkdownLinks: false`, shortest link format), so the rooms and the sovereign essay are outside the vault and repo-absolute wikilinks (`[[submission-package/essay/…]]`, 3,029 wikilinks in the body use mixed forms) cannot resolve in it. The publication body is `submission-package/essay/`; the vault root should move there or the protocol should say why not. `tests/test_publication_architecture.py` pins the current location.
2. **Links that leave the body.** 332 links resolve by title to the raw Agentworld brief transcription in `working/antykathera-resources/` (330 are the bare `[[Antikythera Agentworld Brief]]`), 255 to `working/sources-texts-references/`, 79 to the central plan, 45 to the final-quilt ledgers, 20 to `working/conjugate-field/`. In a published vault every one breaks. Proposal: give the canonical house `bratton-2026-agentworld-brief` the alias and let the workspace resolver prefer the source house; decide per ledger whether the plan and quilt links become source-house or provenance references.
3. **Return routes.** Whether the 79 source houses should write their own `## Return to the essay` routes (as the Kaplan house does) or continue to rely on declared consumers plus the generated inverse; and whether the reference-notes shelf README should list its notes so the shelf is reachable by an authored link.

Also noted, outside the essay: the Mac data volume is at 100% with 1.8 GiB free; `/private/tmp/claude-501/` holds 39 GB of old session scratch (one session directory alone is 27 GB). Nothing was deleted.

## Commands

```bash
python3 tools/build-navigation.py --project-root .
python3 tools/build-navigation.py --project-root . --check
python3 tools/build-section-rooms.py --project-root . --check
python3 -m unittest tests.test_build_navigation tests.test_build_section_rooms tests.test_audit_room_depth
```

## Second act, 2026-09-08 (evening) — vault root and the link pass

Frank's directions after the first receipt: sort the vault, sort the arguments, house the Agentworld brief, and disposition every link that leaves the body as either a genuine resonance or evidence of a misplaced file. Three Sonnet subagents supplied the detail (scratch reports: `out-of-body-dispositions.md`, `carrier-successor-map.md`, `wikilink-forms-audit.md`).

**Done**

- **Vault root** moved from `symbolon/.obsidian/` to `submission-package/essay/.obsidian/` (git mv). Rooms, essay and field are now one vault. `tests/test_publication_architecture.py` repointed. `tools/okf-workspace.py` gained a `VAULT_ROOT` and resolves slash-bearing wikilinks from it, so `[[symbolon/...]]` and `[[section-rooms/...]]` resolve in the tool exactly as they will in Obsidian.
- **Mechanical link pass**, href-only, 189 files, ledger in this receipt's scratch: 778 repo-absolute wikilinks stripped to vault-relative (`[[submission-package/essay/X]]` → `[[X]]`); 39 file-relative wikilinks (`[[../README|…]]`, which Obsidian never resolves) converted to markdown links; 33 path-form links to raw files that already have source houses rewritten to the house `SOURCE.md`. No prose, label, anchor or frontmatter body was changed. Excluded by rule: `reference-notes/`, `AUTHORIAL-TEXT.md`, `NOTES.md`, the generated navigation layer.
- **Agentworld brief.** Its house `bratton-2026-agentworld-brief` already existed and was quotation-ready; its `local_copy` named the raw file but declared no alias, so the resolver never saw it as a candidate. The bare title is now an alias on the house; all ~330 `[[Antikythera Agentworld Brief]]` links resolve there without edits. The same alias fix was applied to the site-copy, derivational-chat, core-theorems and Definition-of-God houses.
- **Out-of-body census** (61 targets, 375 edges): 20 already had houses (now repointed or aliased); ~30 are legitimate development ledgers and governing documents (central plan 79, final-quilt ledgers 45, conjugate-field drafts 20, wayfinder 3); **0 were misplaced works needing a new house**. Remaining out-of-body links: 221 to `working/sources-texts-references/` (raw chat-log shelf reached through `local_copy`, Frank's P0–P5 reading notes, the Kaplan notes) and the governing/ledger set.

**Measured after the pass**

| Measure | Before second act | After |
|---|---|---|
| Links resolving to the raw Agentworld transcription | 332 | 0 |
| Out-of-body edges into `working/sources-texts-references/` | 255 | 221 |
| Doctor unresolved links in the body | 2 | 2 |
| Reachable from the reading root | 717 | 717 |
| Inherited test failures | 11 | 11, none new |

**The arguments: what the successor map found.** 21 historical carriers in `section-rooms/arguments/`; 57 bare-title links from the 48 movements and ~1,200 title-only wikilinks in all reach them because the resolver types them `argument` (top priority) and Obsidian will not match a `title:` at all. The T09 ledger's own "Historical Argument 01–21" table is internally scrambled (row numbers do not match file contents), so the map was rebuilt by content against the recensus A/C tables.

| Carrier | Successor | Standing |
|---|---|---|
| 01 Immutable Gap and Meta-Sign | A03 | clean |
| 02 Objective Internality | A26 | clean (A26/C41 name twin) |
| 03 Two Logics and Sym-Ballein | A13 | **decide** — carrier may hold unique Sym-Ballein development |
| 04 Arche-Topos, Topology, Music | A16 | clean |
| 05 Agent Subjectivity Must Remain Open | none minted | **decide** — ratified as cross-cutting Concept but no C-ID exists |
| 06 Computational Vimarśa / AHI | A32 (AHI half), C43 (Vimarśa half) | **decide** — two-way carrier |
| 07 Hephaestus and the Net | none; rehomed to Mytheme | explicit, leave |
| 08 Deferential Intelligence | A31 | clean |
| 09 Prakāśa-Vimarśa | A05 | clean; six-way alias bundle to split |
| 10 Vāk | A06 | clean |
| 11 Mono-Poly: Whole and Many | A12 | clean |
| 12 Core Theorem Bridge | none; retained as navigation, "not an Argument" | explicit, leave |
| 13 Tattvic Differential Field | A09 (C16 secondary) | clean; alias bundle to split |
| 14 Computational Process Ontology | A14 | clean; 11 movement links, highest impact |
| 15 Paradox as Cross-Register Hinge | C64 | clean (a Concept) |
| 16 Bohmian Enfoldment and Dialogical Return | none found in any T09 table | **decide** — un-crosswalked; 6 movement links |
| 17 Toroidal Circulation | A17 | clean |
| 18 Trust, Faith, and the Formal Limit | A23 | clean; 7 movement links |
| 19 Two Ones — Mono–Poly Matheme | A11 | clean |
| 20 Advent of Zero, Subject, Integral Logic | A10 (A34/A36 secondary) | **decide** — split |
| 21 The Prisoner and the Politics of the Count | none; rehomed to Mytheme | explicit, leave |

Proposed mechanism once the five decisions are made: (1) type the carriers `legacy-argument` in the resolver, below `argument`/`concept` in priority; (2) add each carrier's title as an alias on its successor A/C page, never on the carrier; (3) rewrite the 57 movement bare-title links to explicit vault-relative paths so the movement prose no longer depends on resolution order; (4) correct the scrambled T09 table with a dated note. Not executed: it changes where authored prose resolves, and three carriers may still carry content no A page holds.

**Still open after this act:** ~50 `[[Antikythera Agentworld Brief#Source PDF page N]]` links now reach the house but the page anchors live only in the raw transcription (decide whether the house carries page anchors); the P0–P5 reading notes and the Kaplan notes are reached by title from Frank's texts and have public houses for the works but no house for the notes themselves; ~15 wikilinks whose target is a concept title containing `/` (`Dia/Syn`, `The Slash (AND/OR)`) which Obsidian reads as paths; 302 markdown links whose path does not resolve from the linking file and 70 stale heading fragments, listed in the wikilink audit; the `stale-bkmr-adapter` count after the pass (adapters resynced per collection).

## Third act, 2026-09-08 (night) — the arguments re-routed

Frank's decisions: 03 → A13 with its richness carried; 05 → no Concept node; 06 → A32/C43 split; 16 → fold into field contents; 20 → A10. `working/` is not part of the submission, so links into it are acknowledged resonances, never rewritten.

**Done**

- `tools/okf-workspace.py`: the 21 pre-T09 carriers in `section-rooms/arguments/` are typed `legacy-argument` (authority `historical-provenance`, resolved after every canonical page); the canonical A01–A36 and A01′–A36′ pages are typed `argument` (they were falling through to `submission-artifact`); `AC.md` is the field's `argument-map`; the doctor's argument-quality check recognises the sixfold chassis (`#0`–`#5→0`, Unresolved Delta, Depth Restoration) so developed A pages are no longer "thin".
- Each carrier's title and aliases are now aliases of its successor (60 alias entries across 18 canonical pages; the generic alias `subjectivity` was not moved; carriers 07, 12 and 21 keep their own resolution by explicit disposition). Bare-title links reach the canonical page in both the tool and Obsidian.
- 35 bare-title wikilinks in 17 movement pages rewritten to explicit vault-relative paths with their labels preserved, so movement prose no longer depends on resolution order.
- Carried content: A13 #5→0 gains the native superposition and its formal neighbours, the attractor-space of *pros hen* analogia, the sourced mass-formation reading and the seam diagnostic (from carrier 03); A26 gains the five-question separation, the "humanity of the gaps" boundary and the disclosure rule for agent-generated terms (from carrier 05). Carrier 16's whole (enfoldment, dialogue, return) is the Bohm dossier and its running-true carrier is `matheme/ql/complex-orientation.md`; the title now routes to the dossier.
- The T09 ledger carries a dated correction with the content-verified successor table.
- Tests: `test_okf_workspace`, `test_ontology_registers` and `test_source_projections_and_retrieval` expectations moved from the carriers to the canonical A pages; the register census now counts the A/A′ pages as declared. Full suite: 113 tests, 11 inherited failures remain (domain-shape, wikilink-in-vault, skill-discovery and doctor-surface assertions predating this work), none new.

**Measured after the act:** `status` counts `argument: 73`, `legacy-argument: 21`; `missing-register` debt 70 → 49 (the carriers no longer count as canonical); `thin-argument` 0; unresolved links in the body 2 (Dreamcode, Frank's authorial text); navigation layer, rooms and source projections fresh; reachability 717 of 764 unchanged.

**Still open:** the ~50 `#Source PDF page N` anchors on the Agentworld house; Frank's P0–P5 and Kaplan reading notes reached by title with no house of their own; ~15 slash-bearing concept titles as wikilink targets; 302 unresolved markdown paths and 70 stale fragments in the wikilink audit; the 47 reference-notes and two source admin files unreachable by authored link; 206 field pages without a written return route.
