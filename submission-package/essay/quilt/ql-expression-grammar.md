---
title: "QL Expression Grammar"
page_type: expression-grammar
authority: subordinate-to-central-plan
status: live
date: "2026-07-29"
tags:
  - epi-logos/antikythera-essay
  - planning-v3/expression
---

# QL Expression Grammar

> [!important] What this file is
> The expression law for core theorems, QL units, tables, and figures across every surface of this corpus — essay prose, section and argument nodes, plates and figures, the published vault, and the plugin. It governs **form only**: it adds no claims, restates no canon, and where any statement here touches content, [[the-return-of-zero-central-plan|the central plan]] and [[working/sources-texts-references/10-7-2026-core-theorems-pithy|the core theorem spine]] win. It canonizes conventions the corpus already uses; the source of every rule is an existing surface, cited in place. Changes to expression conventions land here first, then propagate.

## I. Inline notation — the three tiers

The core theorem file already runs a consistent three-tier convention. It is now law on every surface:

1. **Display math (`$$…$$`)** when a relation is being *operated on* — derived, transformed, equated. LaTeX, as in the theorem file's seventeen display blocks. `\boxed{}` only for a declared operator (the cross-comparison operator at theorem file L74 is the precedent), and any boxed form that is not ordinary arithmetic says so in adjacent prose.
2. **Backticked tokens** when a matheme is being *named* in prose or tables: `0/1`, `1/0`, `?/!`, `−/+`, `X/x`, `AM/IS`, `∞/dx`, `−/−`, `4+2`, `5→0`, `(+1)/(−1)`, `(0/1)/(1/0)`. Unicode inside the backticks (`∞`, `→`, `−`), never LaTeX commands.
3. **Bold positions** — `**#0**` … `**#5**`, `**#5→0**` — in table first-columns and wherever a position is indexed rather than discussed.

Inline LaTeX (`\(…\)`) is retired everywhere: Obsidian does not render it, and naming is backtick work. (Drift repaired 2026-07-29 in `nodes/sections/25-s3-p0-eight-determinations.md`, which now matches its own later sections and the theorem source of record.) Where genuinely inline mathematics must render — rare; prefer display blocks — use `$…$`.

The two logics always appear in their locked full expressions on first use in any surface: **dia-ballein `(+1)/(−1)`**, **sym-ballein `(0/1)/(1/0)`** (orienting principles §II; central plan notation lock).

## II. Table canon

Three table shapes are canonical, each already established in the corpus. A new table should be one of these or say why not.

- **Shape A — position × attribute** (the workhorse). Rows are `**#0**`–`**#5**` (with `−/−` parent and `1/0` return-switch rows where the eight-turn traversal is shown); columns are attribute slots. Source of record for the determinations: the eight-row table in the core theorem file §II(c). Widest precedent: the cheat sheet's nine-column Day table.
- **Shape B — sub-lens ladder.** Three columns (`Sub | Name | <lens-specific>`), six rows, for L-family internals (cheat sheet L62–120).
- **Shape C — rotation / index matrix.** Rows as cyclic shifts or indexed soundings (the 6×6 rotation matrix and hexad tables in `mef-12-lenses-sublens-reference.md`).
- **Compressed form** — the three-column `Turn | Expression | Work performed` reduction (central plan L373) when a full Shape A table would overload the surface. Figure captions and plates use this scale.

Three rules ride on every table:

1. **Status marking.** A table whose rows are not uniformly Derived carries either a status column (`Status and use`, as in the [[mathematical-artistic-image-register|image register]]) or a status callout directly above it (`> [!important] Scope and epistemic status`, as on the tattvic unit). Compound statuses are legitimate and preferred over false uniformity: "Derived topology; QL reading Argued" (substrate ledger precedent).
2. **Source of record.** Any table that re-expresses a canonical table closes with a source-of-record line linking the original (precedent: node 25's closing line to the theorem table). One table owns each canonical content; every other rendering declares itself a refraction.
3. **Guard clause encouraged.** The determinations table's fourth column — *what remains invariant through the change* — is the corpus's strongest defense against dilution in re-expression. Where a table carries operations that downstream surfaces will compress, add the guard column.

## III. Figures and plates

Plates are **figures**: static SVG or PNG diagrams embedded in Markdown, produced like any other figure, with no runtime and no schema layer. Their *content* is governed by the central plan's plate specification (L822–834: proposition, six movements, two implicate thresholds and four explicit relations, status band, one mathematical anchor and one mythemic or phenomenological image, audible anchor where relevant, research prompt and deep links) and by the [[mathematical-artistic-image-register|image register]], which assigns each admitted image one exact argumentative job under the one test: *does the image run true?*

**The concentric mandala is the canonical layout for QL-unit figures.** Its geometry is already derived, not invented here:

- **Centre** — the `0/1` threshold and the figure's governing proposition. The centre of the mandala is empty of object: it carries the ground–mark relation, never a summary badge.
- **Four cardinal stations** — the explicate four `#1`–`#4`, at the compass positions, carrying their determinations and constructions (warrant: the core theorem §II(a) table — centre `#0`, N/E/W/S quarter-turns, Point→Line→Angle→Triangle→Square→Circle).
- **Enclosing ring** — the `#0`/`#5` envelope as circumference: frame, never content (warrant: the held-envelope rule in `/mef-refract` and the harmonic-families correction — the two implicate poles frame the explicate four).
- **Status band** — an outer or corner band marking Derived / Argued / Offered per element, rendered identically to the badges on every other surface.
- The form's standing warrant is topological: the mandala is the torus's flat projection (fundamental polygon, four quarters + centre + enclosing ground = `4+2`), so the concentric layout is itself a refraction of the arche-topos, not decoration.

 the assignment of `#1`–`#4` to specific compass points is the theorem §II(a) degree table (N 0° · E 90° · W 270° · S 180°) 


## IV. Citation wiring

One chain, all of it already built, links every expression surface to its evidence:

1. **The figure or table** carries its status marking (§II.1, §III) and closes with a **caption block**: the proposition, the status band, and a prose-framed source-of-record link — `Source of record: [[<canonical surface>]]` — plus any consumed passage IDs in backticks (`colebrooke-1817-brahmagupta-bhaskara-q001` form).
2. **The source house** (`source-bank/sources/<domain>/<author>/<source_id>/SOURCE.md`) carries the Chicago 18 forms and the stable passage anchors the caption cites. Internal-corpus houses give theorems and QL units their provenance; any historical, textual, mathematical, or technical fact leaving the internal corpus routes to a public source (source-bank protocol rules 7–8).
3. **Node surfaces** wire quotes through the established pattern: `source_ids` and `quote_ids` in frontmatter, a `## Source boundary` section naming each backticked quote ID and its single job (precedent: node 14-s1-p1).
4. **The sovereign essay** cites in Chicago 18 notes and prose-framed links only. On the published vault, metadata supports discovery and never becomes the visible subject (vault spec §3): status bands live on plates and node pages, not as dashboard chrome on the reading surface.

The status vocabulary is one vocabulary everywhere: **Derived / Argued / Offered** for claims; **Extracted / Paraphrased / Argued-from / Resonant-with** for evidential relations — rendered identically in essay prose, tables, figure captions, plugin outputs, and vault displays (CLAUDE.md refraction ledger §5).

## V. Update rules

1. Expression-convention changes land in this file first, then propagate to surfaces; content changes never originate here.
2. A surface that must break a rule states the exception in place and names what the break achieves (the same discipline as writing law L7).
3. This file cites precedents rather than restating them; if a precedent moves, update the pointer, not the rule.
4. Conflicts between this file and the central plan, the orienting principles, or the theorem spine resolve against this file.
