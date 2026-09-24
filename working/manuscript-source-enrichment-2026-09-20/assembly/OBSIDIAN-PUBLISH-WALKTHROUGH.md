# Obsidian Publish — expose the existing publication 4+2

Date: 2026-09-24
Standing: corrected publication integration design
Repository branch: `codex/manuscript-source-enrichment-2026-09-20`

## Governing fact

The Obsidian publication surface already exists.

`submission-package/essay/` is the publication body and is already an Obsidian vault, with `.obsidian/app.json` at its root. Its topology, links, authored reading routes, generated navigation mirrors and return relations were built for exactly this kind of traversal.

Obsidian Publish should therefore publish **this body itself**, not generate a second vault, a second taxonomy, or a layer of explanatory walkthrough pages over it.

The publication-level 4+2 is the site:

- **#0 — Rooms:** `section-rooms/`
- **#1 — Symbolon:** `symbolon/` root and root records
- **#2 — Matheme:** `symbolon/matheme/`
- **#3 — Mytheme:** `symbolon/mytheme/`
- **#4 — Episteme:** `symbolon/episteme/`
- **#5 — Essay:** `THE-RETURN-OF-ZERO.md`

The rooms and essay remain parallel to the Symbolon root. Matheme, Mytheme and Episteme remain held within Symbolon as the descending registers. Publish must expose that relation rather than flatten it into a conventional documentation hierarchy.

## The front door already exists

Use `submission-package/essay/README.md` as the Publish index/home page.

It is already the authored reading root. Its entrances are the walkthrough:

- **Begin at the beginning** — enter Movement 01 and follow the 48-movement sequence.
- **Enter one station** — open one of the eight rooms and its six movements.
- **Follow a thread** — enter one of the curated transverse paths.
- **Go to the root** — enter Symbolon and the native relation.
- **Enter through a question** — use the existing question-led entrances into movements, Mythemes, arguments and return paths.

No further "walkthrough layer" is required. Where the reading root needs updating after the enriched manuscript is authorially accepted, edit the reading root itself so that its entrances describe the current work.

## The four reading movements are the site behaviour

The repository already defines four ways to read the same work:

### Linear

Read `THE-RETURN-OF-ZERO.md`, or follow the complete 48-movement braided traversal through the eight rooms.

### Radial

Open a claim or movement into its actual derivation, concept, source, history, Matheme or Mytheme, then follow its declared route back.

Obsidian Publish's stacked pages, hover previews and backlinks directly support this movement: the depth can open beside the present page without replacing the path the reader was following.

### Transverse

Follow the existing curated paths under `symbolon/episteme/maps/`.

These paths exist only where the whole relation cannot be reconstructed safely from local links alone. They are already the intended long-range walkthroughs:

- Return of Zero — Braided Traversal
- Mono–Poly and the Two Ones
- Trust, Faith and the Formal Limit
- The Advent of Zero, Subject and Integral Logic

The path is part of the field, not a guide layered above it.

### Toroidal

Follow the authored `returns-to` relations and the backlinks produced by those relations, arriving again at an earlier movement or root after the circuit has changed its meaning.

This is where Publish's backlinks and stacked pages should make the topology feel alive: return without losing the traversed field.

## Graph

The published graph should be the graph latent in the canonical publication body.

The repository already contains authored Markdown/wikilinks and relation-bearing pages. The generated navigation MOC currently resolves the publication body into hundreds of canonical pages and thousands of written relations. Publish should expose those links directly.

The graph is therefore not a new model of the field. It is another view of the field already written into the files.

Enable the global Publish graph.

The existing `symbolon/episteme/maps/navigation/MOC.md` remains a generated textual mirror of the same relation set. It is useful for explicit orientation and auditing, but it is not the front door and should not be turned into a replacement map for the graph.

The protocol also calls for restrained local minigraphs on substantive pages. Where those are already materialised, preserve them. Where the canonical records expose the required declared relations but a visual minigraph has not yet been rendered, the later Publish polish can derive a small local visual from those same relations. It must not create new semantic edges.

## Navigation

Set the site home to:

`README.md`

The visible root should preserve the publication structure rather than invent editorial categories around it.

At the top level the reader needs immediate access to:

1. the Reading Root;
2. `#0` Rooms;
3. `#1` Symbolon and its nested `#2` Matheme, `#3` Mytheme and `#4` Episteme field;
4. `#5` the Essay.

The authored links inside those surfaces do the deeper navigation.

The generated Navigation MOC, intents pages, source projections and audits remain available where useful, but the reading root and canonical records stay primary.

## What is actually published

The Obsidian vault root is:

`submission-package/essay/`

That is already the designated publication body.

The public site follows the existing public-release discipline of that body. Canonical publication records are published in place. Non-public support/provenance surfaces already identified by the writing protocol remain outside the public selection even where they share the vault root.

There is no generated `working/publish-vault/` and no maintained duplicate of canonical Markdown.

After authorial acceptance of the enriched manuscript, the accepted essay is promoted to the sovereign `submission-package/essay/THE-RETURN-OF-ZERO.md`, generated navigation/freshness surfaces are rebuilt, and that same publication body is the Publish source.

## Obsidian-native configuration

The vault already contains:

`submission-package/essay/.obsidian/app.json`

with automatic link updating enabled and wikilinks as the native link format.

For Publish, enable the capabilities that expose the topology already written into the vault:

- navigation;
- search;
- graph;
- table of contents;
- backlinks;
- hover previews;
- stacked/sliding pages;
- theme toggle.

Use `README.md` as the index file.

The headless client can bind directly to the existing vault:

```bash
cd submission-package/essay
ob publish-setup --site "<site>"
ob publish-site-options \
  --index-file README.md \
  --show-navigation true \
  --show-graph true \
  --show-outline true \
  --show-search true \
  --show-backlinks true \
  --show-hover-preview true \
  --show-theme-toggle true \
  --sliding-window true
ob publish --dry-run
```

The exact include/exclude selection should follow the repository's existing publication/public-status rules rather than invent a second classification.

## Styling

Add a root `publish.css` to this vault when the public presentation is ready.

Its job is to let the existing ontology read clearly:

- essay as the long-form reading surface;
- rooms as traversable stations;
- Symbolon root as the holding relation;
- Matheme, Mytheme and Episteme visually distinguishable without becoming separate sites;
- backlinks, hover cards and graph visibly subordinate to the prose while remaining close at hand;
- mathematics and source detail comfortable on desktop and mobile;
- stacked pages readable as a traversal across the field.

CSS changes presentation only. It does not move or rename the ontology.

## Expressions relation

Expressions remains useful as the more composed encounter above this substrate.

The O:I site's existing Library / Expressions experience can present the work through pages, scenes, visual composition and the already generated Expression material.

Obsidian Publish then supplies the complete inspectable written field beneath it.

The relation is:

```
O:I / Expressions encounter
        ↓
canonical subject / scene / essay location
        ↓
Obsidian Publish — the actual 0–5 publication body
        ↔
essay · rooms · Symbolon · Matheme · Mytheme · Episteme
```

Expressions should deep-link to stable Publish locations for the canonical subjects it is expressing. Publish links can return outward where an Expressions scene exists. Both consume the same canonical subject identities; neither creates a second essay ontology.

This preserves the original order of development: the Obsidian publication body is the canonical linked work; Expressions is a later expressive presentation of that work.

## Immediate implementation

The next local implementation pass should work on the actual vault, not on a surrogate.

1. Fetch the enriched manuscript branch and inspect `submission-package/essay/` as an Obsidian vault.
2. Complete authorial acceptance/promotion of the new essay before making the live Publish site authoritative at #5.
3. Rebuild the existing generated room/navigation/source projections from their current builders.
4. Run the repository's link/navigation/public-release audits on the actual publication body.
5. Open `submission-package/essay/` in Obsidian and inspect the existing graph, rooms, transverse paths, backlinks and return routes as one field.
6. Configure an Obsidian Publish site directly against that vault, initially as a non-public or passworded preview if desired.
7. Set `README.md` as the index and enable navigation, graph, outline, search, backlinks, hover previews and stacked pages.
8. Add presentation CSS only after the native traversal has been inspected.
9. Test the four intended movements — linear, radial, transverse, toroidal — through the actual published field.
10. Connect existing Expressions subjects/scenes to their canonical Publish locations.

## Current Obsidian Publish capabilities used here

Current official Obsidian documentation confirms:

- a vault can be published directly through Obsidian Publish;
- headless Publish can bind to an existing vault path;
- `publish: true` and include/exclude filters can control automated publication;
- a site can declare its index file and navigation order;
- navigation, graph, outline, search, backlinks, hover previews, theme toggle and sliding-window/stacked-page reading are native site options;
- custom `publish.css` can style the site;
- permalinks can provide stable public URLs.

Official references:

- https://obsidian.md/help/publish
- https://obsidian.md/help/publish/publish
- https://obsidian.md/help/publish/sites
- https://obsidian.md/help/publish/customize
- https://obsidian.md/help/publish/headless
- https://obsidian.md/help/publish/limitations
- https://obsidian.md/help/properties
