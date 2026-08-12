---
title: "Field-Pages Skill Family — Design"
date: "2026-08-10"
status: design-provenance-pending-review
authority: non-governing design provenance
register: symbolon
audience: "orchestrator agents, page-building subagents, Frank"
supersedes: nothing
---

# Field-Pages Skill Family — Design

*A small skill family for developing the supporting-file pages of the publication field (`#1`–`#4`) so the field becomes the navigable surface of the whole — the essay (`#5`) the central product, the rooms (`#0`) the structured argument it stands on.*

This document is design provenance, not a governing structure. It describes intended skills and artifacts; it does not override the central plan, the live canonical nodes, or `WRITING-PROTOCOL.md`. The skill family, once built, is a development surface that must stay faithful to `AGENTS.md`, the orienting principles, the register READMEs, and the expression grammar.

---

## 1. Context and purpose

The publication body is the 4+2 with fixed offices: `#0` the rooms (each holding its six movements under `movements/` with the shared argument field under `arguments/` — the nested `0/1`), `#1` Symbolon, `#2` Matheme, `#3` Mytheme, `#4` Episteme, `#5` the sovereign essay. The four infer into the rooms; the enriched rooms improve the essay. The field pages are where each element of the four registers is developed so it stands on its own feet — and implicates through the web.

Before the final quilting passes, the field pages need canonical forms: per content type across matheme, mytheme, episteme and symbolon, plus the navigation craft that makes the graph genuinely guiding, plus the orchestration protocol that lets an orchestrator agent run developments with subagent workflows.

The four existing phase-skills (`return-of-zero-orient/source/write/review`) govern orientation, evidence, composition and audit. They do not govern the field-building layer. This family fills that gap as a **small new family alongside them** — not one integrated skill, not an extension of the phase-skills, not split-by-register.

The family must serve **both routes**:

- **Quilting-to-pages** — building the field from the working shelves (quilting surfaces, `reference-notes`, chat-logs, raw authorial stacks) *before* prose exists.
- **Writing-to-pages** — building pages from live canonical nodes as the rooms fill, tracking the writing.

## 2. What a page is (and is not)

A page is **the developed account of one element**, standing alone on its own feet *as much as* it implicates in the other files.

- A page is **not a duplicate** of the element's content elsewhere. It is the navigable surface for the various details: it declares the `0/1` admitted, develops the element through the QL skeleton, and returns through `5→0` — pointing at the canonical body it surfaces, carrying the element's account in prose.
- The prose **is the navigation**: relations are carried in the telling, not in a separate map layer.
- The raw source keeps its place. A source house (`SOURCE.md`) remains the evidence object — bibliographic identity, passages, provenance, quotation state. The page is the account built from the source *in our voice*, relative to the logics and QL details already spoken to in it. A myth, for example, needs its telling — in our voice, built by knowing the myth across our arguments and how we plan to quilt it in, not just what the myth is in the source. Its matheme and episteme connections are inherent to the mytheme, not added afterward.
- Each page has **one home** in the established sub-dir architecture of the symbolon system. Every type of file already has its place; the place drives the nature of the page within it. Records are admitted by moving, never copying; `working/` never becomes authority.

## 3. The family

Four skills, alongside the existing orient/source/write/review. Each skill has one clear purpose and is discoverable by both runtimes through the established `.agents/skills/` → `.claude/skills/` symlinked projection.

| Skill | Purpose |
|---|---|
| `return-of-zero-pages` | The canonical page forms. Carries the QL skeleton, the refraction mechanism, and the register record-form contracts as the material from which a type's titles are derived. |
| `return-of-zero-links` | The navigation craft: how links are written into pages so the local graph genuinely guides — the written relation, not the generated index. |
| `return-of-zero-visuals` | Plate/diagram/figure generation under the existing repo rules (LaTeX law, visual-domain contracts), useful for a cheaper model used via subagent at runtime. |
| `return-of-zero-build` | The orchestration skill + workflow script: deterministic fan-out of one independent subagent per element development, a barrier, then the hygiene stage. |

## 4. The QL page skeleton

Every record page is the QL sixfold. The titles are canonical; the **type refracts them**. The semantic titles are retroactive assignations — names positions *receive* after refraction through lenses — so the skeleton is the raw sixfold, and each type declares its own titles through the `pages` skill's mechanism rather than a pre-decided weighting.

- **#0 — In-quantum** *(the `0/1` incoming)*: the page opens the field. *"Insofar as we take all these things, then this page is true."* The presuppositional frame — and the place where the page's attached `#0`s are encapsulated upfront, with clarity: the section-rooms and argument nodes the page presumes, declared before the body. The admission channel.
- **#1 — Definition**: the page defines its object — first emergence of explicit form from the in-quantum ground.
- **#2 — Operation**: how the object moves, transforms, produces effects.
- **#3 — Pattern/Identity**: the kind, the type, the formal architecture — who/which/whereby.
- **#4 — Context**: the where/when/whither — the page and its object situated in their actual horizon. Aperture is one function of this position, not its fullness.
- **#5 — Quintessence** *(the `5→0` outgoing)*: performs the **analogia** — the relation to the one, *pros hen* focal meaning — and with it the page's return route to the whole. Salt; the Möbius return.

**The `0/1` and `5→0` are not positions among the six.** They are the page's **incoming and outgoing relation mechanisms to other `#0`s**. Every page declares what it admits (`0/1`, encapsulating its attached rooms and arguments) and what it returns toward (`5→0`, the analogia). This is what develops link health: every page has a declared entry and a declared return, and the mechanism is reciprocal across pages — not a one-way pointer.

The page form is the depth record of `WRITING-PROTOCOL.md` §5 made into a page: proposition → operation → exact targets → what the essay compresses → source/provenance → status → symbolon relation → return route.

## 5. Register page forms — semantic per-type variation

The per-type titles are **not** pre-specified here. They emerge from the refraction of the skeleton through each register's record-form contract, ratified on the first instance of each type, and then carried by `return-of-zero-pages` as the pattern. The discipline: derive the titles from (a) the QL skeleton above, (b) the register's `README.md` record form, (c) the element's actual material — never from a remembered gloss.

The register contracts already state what each record must do:

- **Symbolon** (`symbolon/README.md`) — root records of the whole relation (`0/1`, `1/0`, the slash, self-identity, mono–poly, complexio oppositorum, the eight determinations). A root record's page carries the relation the whole field turns on.
- **Matheme** (`matheme/README.md`) — exact operations: QL, Spanda, topology, harmonics, formal neighbours, computation. Diagrams land in `matheme/diagrams/`.
- **Mytheme** (`mytheme/README.md` + sub-domains) — lived forms: myth, narrative, poetry, media, art, music. Each sub-domain README specifies the telling: "identifies the scene, tells only the narrative required to follow it, and states what the figures do for the essay." Plates land in `mytheme/plates/`. Cross-register is the mytheme's default: the matheme connection is inherent (Hephaestus's net *figures* enclosure — the net is the matheme made scene), and variant/scholarly material routes through Episteme.
- **Episteme** (`episteme/README.md` + sub-domains) — instituted knowledge: sources, histories, etymologies, lenses, maps, dossiers, figures, concepts, dialogues. Figures land in `episteme/figures/`.

The `0/1` admission on each page names exactly which section-rooms and argument nodes it serves (`consumed_by_sections`, `consumed_by_arguments`), and the `5→0` return names its register-route back to Symbolon and into the essay.

## 6. Links and navigation craft

**The map is written, not generated.** The local graph is a *reading* surface — it renders the links the pages already carry. The craft lives in how links are written into pages, and the graph follows.

The Obsidian-native primitives we exploit, not rebuild:

- **Local graph** — renders a page's neighborhood. A well-written page has exactly the neighborhood it needs: 5–7 declared relations (the `WRITING-PROTOCOL.md` §14 minigraph), never an inferred fog.
- **Backlinks pane** — the inverse view: who points at this page. How the essay and rooms read their field.
- **Hover preview** — links land somewhere worth previewing: the target's `#0/#1` carries its identity in the first screen.
- **TOC/outline** — the six-fold skeleton gives every page a natural outline for free.
- **MOC as entry** — the register READMEs (matheme/mytheme/episteme/symbolon, the sources INDEX, the Concept Map) are the curated content-map entries: judgment-led, prose-woven.

**Link vocabulary and grain:**

- Every link is a declared relation from the 13-word vocabulary: `derives, grounds, defines, historicises, sources, qualifies, tests, figures, embodies, extends, compares, presages, returns-to`. The relation is recoverable from the prose around the link; a link without its relation is clutter.
- Grain goes to block anchors where the argument demands it (`^roz-s03-m27-claim04`) — links enter the essay and rooms at claim level, not just page level.
- **Inverse links**: the essay's §5 and each room's movements carry prose-framed return links to their field records; the backlinks pane completes the loop.
- **Naming discipline**: filename is identity; when a new live node supersedes a legacy stub it declares its own title as an alias, or the frozen stub keeps capturing the link. No orphan pages; no hubs that don't resolve to a real home.

**The derived MOC/intents layer.** After the written links exist, a simple aggregation produces contents lists **extended to intents** — how a file implicates through its web — for quick navigation. This is navigation-only, added after the fact; aggregation never precedes authorship. The written map stays curated; the MOC is its navigation surface. What a file implicates (its declared relations), not what it merely mentions, drives the intent entry.

**Essential vs tangential.** The skills are part of what separates and delineates essential and tangential pieces. Every element receives the same development attention; the weighting (already in frontmatter: `argument_weight`, `consumed_by`, `source_role`) — sorted out post-quilt — decides *how* the different things turn up in mapping and navigation. The Prisoner is a leaf mytheme page with light interior integration, explorable from outside the essay flow; the Spanda braid is dense with room and essay links. Both get full development; the mapping manages their presence.

## 7. Visuals

`return-of-zero-visuals` covers plate, diagram and figure generation, using the existing repo rules — the LaTeX law from `submission-package/essay/quilt/ql-expression-grammar.md` (display math `$…$` for operated/derived relations, backticked tokens for naming, inline `\(…\)` retired), the expression-grammar table shapes, and the concentric-mandala layout for QL units. It is useful for a cheaper model used via subagent at runtime.

All visuals have places to land in the established sub-dirs:

| Visual type | Operation | Home |
|---|---|---|
| Diagrams | formal | `matheme/diagrams/` |
| Plates | composed imaginal | `mytheme/plates/` |
| Figures | evidential | `episteme/figures/` |

Record + asset together, per the existing visual-domain contracts (`matheme/diagrams/README.md`, `mytheme/plates/README.md`, `episteme/figures/README.md`). No new homes.

## 8. Build and orchestration

`return-of-zero-build` is one skill + one workflow script. Its job: **turn a queue of elements into their developed pages**, deterministically, by subagent fan-out, on both routes.

### 8.1 Intake — the quilt is the queue

The queue is **not** a records manifest. The intake is the quilt. Two live quilting surfaces are already the main route:

- `submission-package/essay/quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md` — the session-contribution ledger: each contribution is a fully-marked block (provenance, inherited positions, new developments, source relations, register, canonical blast radius), pre-canonical by its own covenant.
- `submission-package/essay/quilt/2026-08-02-PARALLEL-HARMONISED-QUILT.md` — the target-keyed pre-propagation ledger: the whole-in-one-relation, the station ledger, the argument-node ledger, the concept/path/artifact ledger, the legacy second pass, the Tao layer. **This is the main route** — the quilt already organises its yield by canonical target.

The workflow reads the quilting surfaces, finds the elements that have accumulated material (per register, per canonical target), and assembles the intake. For each element it resolves: identity → canonical home → register → existing frontmatter → the accumulated yield (quilt contribution + source house + argument/concept nodes + reference-notes + any local copy).

### 8.2 Dispatch — one subagent per element development

Each subagent develops **one element across its whole web** — the quilt contribution(s), the source house, the argument node, the concept, the reference-notes — and builds the page in the register's form: standing alone, implicating, prose carrying the relations. Independence is the guarantee: each page is built from the element's full web, not from its neighbours' drafts. The workflow script encodes the deterministic fan-out following the corrected `/mef-refract` precedent (independent Agent dispatch per lens/subject, a barrier, then a synthesis/hygiene authority in the parent context); it never invents content.

Where a record requires an asset (a plate, diagram, figure), the `visuals` skill runs **in the same pass** to a cheaper-model subagent, landing the asset in its established home.

### 8.3 Essential and tangential — same attention, managed turn-up

The workflow does not skim tangential elements. A leaf page (The Prisoner: source house + argument node already half-woven, missing the mytheme/media page) receives the same development as a dense braid (First Spanda). The frontmatter weighting — post-quilt — decides how each turns up in the mapping and navigation. The skills delineate; the mapping manages presence.

### 8.4 Barrier, then hygiene — the derived layer

After the fan-out completes:

1. **Link validation** — dangling scan, `effects` map (`tools/okf-workspace.py effects … --depth 4 --json`), alias/title discipline, one-home rule.
2. **MOC/intents aggregation** — the after-the-fact contents lists and per-file intent webs, generated from the now-written links (§6).

Nothing ships single-pass; the hygiene stage is the workflow's final gate, and it reports — it does not self-certify.

## 9. Validation and gates

- Every page is drafted against the register's record-form contract and the QL skeleton; every claim carries `claim_status` (Derived/Argued/Offered/Open) and every source relation is named (Extracted/Paraphrased/Argued from/Resonant with).
- Citation readiness and quotation readiness remain separate; a source house's `NOTES.md` stays Frank-authored and untouched.
- The page never duplicates: it surfaces the canonical body (`SOURCE.md`, argument node, concept node, theorem spine) and carries the account.
- `return-of-zero-build`'s hygiene stage runs the workspace's existing validation tools (`okf-workspace.py`, source resolver, tests) as gates, not generators.
- Visuals follow the LaTeX law and the visual-domain contracts.

## 10. Non-goals

- No autogenerated map that precedes written links (the MOC/intents layer is post-hoc navigation only).
- No new content homes: every page lands in the established sub-dir architecture.
- No dilution of canonical content into "accessible" summaries on the page — the page *is* the account, at the register's full register.
- No fusion of distinct arguments because they meet at one institutional application.
- The skills do not replace the phase-skills; `orient/source/write/review` keep their offices.

## 11. Open decisions

- Per-type QL titles: ratified per first instance of each record type, then carried by `pages`. (Deliberately not pre-decided.)
- The `build` workflow's intake sources: which quilting surfaces are read in which order, and how a quilt element resolves to its canonical target — to be fixed against the live quilt when the skill is built.
- The Prisoner-type leaf pages: how light the interior integration should be, and how the essay-aside and page cross-link — pattern to be set by its first instance.

## 12. Build order

1. `return-of-zero-pages` — the QL skeleton + refraction mechanism + register contracts.
2. `return-of-zero-links` — the written-link craft + the derived MOC/intents aggregation.
3. `return-of-zero-visuals` — the LaTeX law + visual-domain contracts as an executable skill for a cheaper runtime model.
4. `return-of-zero-build` — intake → dispatch → barrier → hygiene workflow + skill.
5. First instances of each register type (symbolon root, matheme theorem, mytheme myth, mytheme media leaf, episteme concept) ratified with Frank before the family is used at scale.
