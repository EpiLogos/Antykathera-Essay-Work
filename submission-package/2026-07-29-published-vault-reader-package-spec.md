# Published Vault and Reader Package Specification

**Date:** 2026-07-29
**Status:** Superseded design provenance
**Superseded by:** `../WRITING-PROTOCOL.md` on 2026-08-04
**Previously superseded:** the publication, navigation, and reader-package decisions in `2026-07-12-submission-package-design.md`

> This file records the preceding published-vault design. It no longer governs folder placement, writing phases, branch execution, register architecture, or public-release scope. The live protocol places direct Symbolon records at `symbolon/`, with `matheme/`, `mytheme/`, and `episteme/` beneath it and submission support outside that chain.

## 1. The work being made

The submission is a philosophical work whose native digital form is a published Obsidian vault. Its organisation exists to let the ideas be read at their proper depth and in more than one order. It is not a database demonstration, a fixed census of sections, or a visualisation of project administration.

The package is content-agnostic. Titles, section names, filenames, argument counts, concept counts, source counts, and curated paths may all change without requiring the reading architecture or companion skills to be rewritten.

The work has four mutually supporting forms:

1. **The main essay** — a lean, continuous, self-sufficient argument.
2. **The published vault** — the essay opened through linked movements, ideas, sources, paths, and static diagram assets.
3. **The reader companion** — a unified QL/MEF instrument for reading, teaching, following, questioning, and returning through the work.
4. **Reader encounters** — reader-owned traversal ledgers, with an optional Epi-Card form when an encounter deserves to become a portable object.

The main essay remains the primary encounter. The vault expands its depth without turning the essay into an index or making the reader learn the architecture before meeting the thought.

## 2. Publication form

Obsidian Publish is the intended public surface. The published vault should use ordinary Obsidian affordances well:

- readable Markdown pages;
- prose-framed wikilinks;
- hover previews;
- backlinks;
- local and global graph views;
- search;
- restrained navigation;
- embedded SVG, PNG, audio, and other static assets where the work calls for them;
- light custom CSS supporting the visual identity of the piece.

The built-in graph is sufficient because the prose explains why one page leads to another. The publication does not need a separate semantic-ontology renderer. A custom component is warranted only when it produces a reader experience that ordinary pages, links, diagrams, and the graph cannot.

The existing HTML material in the parent directory is an input to diagram production. Relevant views are extracted or redrawn as static diagram assets and embedded in Markdown. The published vault does not depend on a separate diagram runtime.

## 3. Vault assets

The vault should discover and present the assets that actually exist rather than require a predetermined folder or node census. Typical assets include:

- a reading root or invitation;
- the sovereign essay;
- movements or sections of the essay;
- idea and concept notes;
- source houses and further-reading notes;
- diagrams and other media;
- curated linear, transverse, or thematic paths;
- reader traversal ledgers where a private or copied vault permits them.

These are roles, not mandatory folders. A page may carry more than one role. The reading and teaching protocols discover pages from the vault entry, frontmatter type where present, ordinary links, backlinks, embeds, headings, and the reader's current location.

Links should occur where the prose genuinely opens onto a source, implication, related movement, diagram, or deeper treatment. Metadata supports discovery; it does not become the visible subject of the publication.

## 4. Holographic movement

Where the work uses the sixfold form, a movement can carry:

`0/1 → #0 → #1 → #2 → #3 → #4 → #5 → 5→0`

The middle six carry the differentiated development. `0/1` and `5→0` are additional layers with primarily functional work, but they may contain substantial prose.

- **`0/1` — threshold or binding:** what arrives, what is inherited, what question or pressure is being entered, and what relation is established with the reader.
- **`#0–#5` — sixfold development:** the local philosophical movement in its own appropriate proportions.
- **`5→0` — return:** what has changed, what the movement now implies, what remains unresolved, and which passages onward have become possible.

The same rhythm may recur at the scale of the whole work, a section, a diagram, a teaching encounter, or a reader traversal. It is holographic because the relation can recur through different scales and media, not because every page must fill the same form.

## 5. Reading modes

Linear and non-linear reading are equally native.

- **Linear reading** follows the essay or another declared sequence.
- **Radial reading** opens from a passage into an idea, source, diagram, or cluster of neighbours.
- **Transverse reading** follows a question or relation across distant parts of the work.
- **Toroidal reading** returns to an earlier asset or question with a changed understanding, so the return becomes a new opening rather than simple repetition.

No mode is treated as the advanced alternative to another. Readers may change modes at any point. The interface should always preserve a clear way to continue, go deeper, move across, and return.

## 6. Traversal ledger

A traversal ledger is a reader-owned account of an actual movement through the work. It is not a second canon and not an analytics log.

The ledger records:

- the publication release or vault state encountered;
- the reader's initial question, attraction, or pressure;
- the entry asset;
- the meaningful movements made through pages, blocks, diagrams, sources, and conversation;
- branches, revisits, rejoins, and returns;
- what changed in the reading;
- unresolved remainder and possible continuations.

The ledger uses stable asset identity when the vault provides it, together with the path, heading, or block reference visible at the time. Titles and slugs remain mutable. Its movement vocabulary is small: `enter`, `follow`, `branch`, `rejoin`, `revisit`, `question`, `response`, `annotate`, `return`, and `close`.

The ledger's event order preserves linear reading. Parent events and branch identities preserve non-linear movement. A return names the earlier event or asset being returned to and records the semantic difference produced by the circuit. This is how the toroidal shape becomes legible without assigning every page a topological coordinate.

The public Obsidian Publish vault is read-only for ordinary visitors. A ledger may therefore live in a reader's copied vault, in a companion session, or as an exported Markdown note. Recording is optional and private by default.

The operational contract and copyable note live at:

- `epi-logos/resources/reader/TRAVERSAL-LEDGER.md`
- `epi-logos/resources/reader/TRAVERSAL-TEMPLATE.md`

## 7. The reader companion

The reader meets one companion, not a menu that splits the work into competing systems.

QL and MEF operate as one instrument. Positional movement and lens-conditioned encounter are distinct aspects of the same act of reading. Tetralemma is an MEF lens within that instrument, as are the other specialist operations. Internal skill modules may remain separate for precision, but they do not become separate public theories or require the reader to choose between QL and MEF.

The companion supports four natural gestures:

1. **Read** — continue through a declared sequence at the scale the reader wants.
2. **Follow** — pursue an idea, image, source, implication, or related movement through the live links.
3. **Converse** — ask questions and receive teaching from the pages actually traversed.
4. **Return** — gather what changed, retain the remainder, and identify a possible next opening.

The companion begins from the reader's current location and live interest. It reads the page before classifying it, follows links before inventing relations, and uses QL/MEF to deepen the encounter rather than display machinery. Coordinates and lens names appear only when they help the thought become clearer.

The low-level wiki skill must be able to enter through any resolvable asset, including a linked diagram or heading. It discovers the current vault from its entry surface and actual links. It must not rely on a remembered title, fixed path filename, fixed number of movements, or enumerated list of concepts.

## 8. Epi-Card integration

The Epi-Card System v1 is an optional integration specification, not a required reading runtime. Its current package is contract-validated but does not include the `epicard` application assumed by its operating skill.

Its strongest use here is as a **reader-encounter capsule**:

`published vault → traversal ledger → unified QL/MEF reading → optional Epi-Card`

A frozen traversal can enter Epi-Card as a `vault-traversal` source form. The card may carry the reader's question, selected asset references, QL/MEF refraction, achieved movement, remainder, and next ground. It should package the encounter itself, not duplicate the entire vault.

The boundary is one-way:

- the vault and essay remain authoritative for the work;
- the ledger remains authoritative for the reader's path;
- the companion may interpret the path and prepare an encounter capsule;
- Epi-Card may crystallise that encounter and reopen its remainder;
- neither the card database nor its exported wiki may mutate or supersede the essay, source houses, vault architecture, or ledger history.

Ordinary reading must work when Epi-Card is absent. Media production, twelve-position audits, and publication gates from the full card system are not imposed on each link-follow or conversation.

## 9. Package manifest

`MANIFEST.json` is the inventory of submission artifacts and their real implementation status. The Claude marketplace manifest remains only an inventory of currently installable plugins. The card specification is therefore listed in the submission manifest and not falsely advertised as an installed plugin.

## 10. Development and acceptance

Development should improve the complete architecture rather than freeze provisional essay contents.

Acceptance concerns the reader experience:

- the essay reads cleanly without following links;
- the vault can discover its current assets without hard-coded counts or titles;
- links, backlinks, search, embeds, and static diagram assets work in Obsidian and Obsidian Publish;
- a reader can move linearly, branch, rejoin, revisit, and return without losing the thread;
- a traversal ledger can retain that movement and reopen it;
- the companion can read and teach from the pages actually encountered through one QL/MEF instrument;
- Epi-Card absence does not impair reading;
- any future card adapter consumes a frozen ledger snapshot without acquiring authority over the work.

The Obsidian CLI and package checks should verify these capabilities directly. They are supports for a germane, navigable presentation of the ideas, not an independent engineering spectacle.
