# Wikilink forms audit — `submission-package/essay/` as prospective vault root

Method: scripted scan (`audit.py`, same directory) over every `.md` file under
`submission-package/essay/`, excluding the generated
`symbolon/episteme/maps/navigation/` tree (per instruction). 824 `.md` files
exist in the vault; 764 were scanned as **link sources** (navigation excluded
as source, but still counted as a valid link **target**, since Obsidian would
resolve into it). Basename and alias maps were built over all 824 files.
`title:` frontmatter values were tracked separately (Obsidian does **not**
resolve on `title:`). Raw data: `wikilink-forms-audit.json` (per-link records)
in this same directory.

**Headline finding:** rooting the vault at `submission-package/essay/` breaks
the *majority* of wikilinks in this corpus, for two independent and roughly
equal-sized reasons: (1) 936 wikilinks are written as
`submission-package/essay/...` repo-absolute paths, which is the correct
absolute path *today* only because the repo root is currently the vault's
open point — once the vault root is `submission-package/essay/` itself, every
one of these needs its `submission-package/essay/` prefix stripped or the
link rewritten; and (2) roughly 1,197 link instances (146 distinct targets)
target a node by its human-readable **`title:`** value (e.g.
`[[Immutable Gap and Meta-Sign]]`) rather than by filename or a declared
`aliases:` entry — Obsidian never falls back to `title:`, so these are dead
links regardless of where the vault root sits.

---

## 1. Totals

Total wikilinks scanned: **4,292**

### By form

| Form | Count | % |
|---|---:|---:|
| BASENAME (no `/`) | 3,286 | 76.6% |
| REPO-ABSOLUTE (`submission-package/…`, `working/…`, etc.) | 936 | 21.8% |
| FILE-RELATIVE-PATH (`../…`, `./…`) | 40 | 0.9% |
| VAULT-RELATIVE-PATH (contains `/`, not repo-absolute, not `../`/`./`) | 30 | 0.7% |

### By resolution class (all forms combined)

| Resolution | Count |
|---|---:|
| resolves-unique (basename, exactly one match) | 1,205 |
| unresolved-title-only (target matches only a `title:`, no filename/alias match) | 1,197 |
| unresolved (no basename/alias/path match at all) | 888 |
| resolves (path-form link, path resolves under vault root) | 783 |
| out-of-body (repo-absolute link resolving outside `submission-package/essay/`, to a real file elsewhere in the repo — e.g. `working/…`) | 129 |
| broken (FILE-RELATIVE-PATH; Obsidian does not resolve `../`/`./` as file-relative, and none of these happen to also resolve as a literal vault-root path) | 40 |
| ambiguous (basename matches ≥2 files, or alias+basename collide) | 22 |
| alias-only (basename has no file match but exactly one `aliases:` match) | 21 |
| out-of-body-missing (repo-absolute link, target doesn't exist anywhere in the repo — genuinely dangling) | 7 |

Note on VAULT-RELATIVE-PATH: **all 30 are unresolved**, and roughly half of
them are not really path links at all — they are wikilink targets whose text
happens to contain a literal `/` (e.g. `[[Dia/Syn]]`, `[[The Slash (AND/OR)]]`,
`[[Paśu / Bounded Subject-Position]]`, `[[A/C — Argument / Concept — Root of
the Conjugate Field]]`). Obsidian's rule (per this audit's brief) treats *any*
target containing `/` as a vault-root path attempt with no basename fallback,
so these decorative slashes make an otherwise-resolvable concept name into a
guaranteed dead link. The other half are genuine (broken) path attempts,
including several that embed the whole `Antykathera-Essay-Work/…` repo folder
name — i.e. an absolute-from-one-level-too-high path, a third, rarer breakage
pattern distinct from the `submission-package/essay/…` repo-absolute case.

---

## 2. By source-page class

`n` = wikilinks originating in that class. Forms/resolutions below `n` may
not sum across categories that had zero hits (omitted for brevity).

| Source class | n | Dominant form | Dominant resolution(s) |
|---|---:|---|---|
| section-rooms/movements | 216 | BASENAME 192, REPO-ABS 24 | resolves-unique 105, unresolved-title-only 51, unresolved 36, resolves 15 |
| section-rooms/arguments | 322 | BASENAME 305, REPO-ABS 16 | unresolved-title-only 180, resolves-unique 83, unresolved 41, resolves 10 |
| symbolon-root | 6 | REPO-ABS 6 | resolves 6 |
| matheme | 75 | REPO-ABS 75 | resolves 75 |
| mytheme | 79 | REPO-ABS 66, FILE-REL 13 | resolves 57, broken 13, out-of-body 9 |
| episteme/arguments | 489 | REPO-ABS 253, BASENAME 234 | resolves 240, resolves-unique 234, out-of-body 13, broken 2 |
| episteme/concepts | 791 | BASENAME 493, REPO-ABS 293 | resolves-unique 266, resolves 259, unresolved 170, unresolved-title-only 63, out-of-body 19, ambiguous 9 |
| episteme/concepts/reference-notes | 345 | BASENAME 329, REPO-ABS 13 | unresolved 192, unresolved-title-only 126, resolves-unique 14, out-of-body 8, out-of-body-missing 5 |
| episteme/conjugate | 148 | REPO-ABS 109, BASENAME 30, VAULT-REL 9 | resolves 105, unresolved 19, alias-only 18, out-of-body 4 |
| episteme/etymologies | 39 | BASENAME 26, FILE-REL 8 | unresolved-title-only 22, broken 8, out-of-body 4, resolves-unique 4 |
| episteme/histories | 12 | FILE-REL 4, BASENAME 7 | broken 4, unresolved-title-only 7, out-of-body 1 |
| episteme/maps | 118 | BASENAME 115 | resolves-unique 92, unresolved-title-only 17, unresolved 6 |
| episteme/sources | 1,430 | BASENAME 1,392, VAULT-REL 15 | **unresolved-title-only 686**, resolves-unique 402, unresolved 311, resolves 15, ambiguous 8 |
| episteme/sources/**/AUTHORIAL-TEXT.md | 93 | REPO-ABS 51, BASENAME 41 | out-of-body 49, unresolved 21, unresolved-title-only 18, alias-only 2, out-of-body-missing 2 |
| episteme/dialogues | 1 | FILE-REL 1 | broken 1 |
| episteme/dossiers | 1 | FILE-REL 1 | broken 1 |
| episteme/figures | 3 | FILE-REL 3 | broken 3 |
| episteme/lenses | 1 | FILE-REL 1 | broken 1 |
| quilt | 123 | BASENAME 122 | unresolved 91, unresolved-title-only 25, resolves-unique 4, ambiguous 2 |

Reading this table:

- **`episteme/sources` is the single worst-behaved class** (1,430 links,
  686 of them `unresolved-title-only`): source houses link to argument/
  concept nodes almost entirely by the node's readable title
  (`[[Core Theorem Bridge]]`, `[[Objective Internality]]`, …), which is a
  frontmatter `title:`, not a filename or alias.
- **`episteme/arguments` and `matheme`/`symbolon-root` are the best-behaved**
  classes — nearly everything there is either a clean `resolves-unique`
  basename hit or a `resolves` repo-absolute path that, once the
  `submission-package/essay/` prefix is mechanically stripped, becomes a
  clean vault-relative path.
- **`mytheme` and several `episteme/*` README trees** carry the `../README`
  family of FILE-RELATIVE-PATH links (all `broken`) — these were clearly
  authored assuming file-relative resolution, which Obsidian does not do for
  wikilinks.
- **`quilt`** (venue-facing concordance + grammar docs) has a high raw
  `unresolved` rate (91/123) — its BASENAME links skew toward targets that
  don't exist as filenames in the vault at all (distinct from the
  title-only pattern dominant elsewhere).

---

## 3. Top 30 unresolved / ambiguous targets

Counted by (form, target, resolution) triple across all instances; one
example source shown per row (full list in the JSON).

| Count | Form/Resolution | Target | Example source |
|---:|---|---|---|
| 97 | BASENAME/unresolved-title-only | Immutable Gap and Meta-Sign | `section-rooms/07-instrument-returns/movements/48-s50-p5-ahi-planetary-return.md` |
| 93 | BASENAME/unresolved-title-only | Core Theorem Bridge | `section-rooms/arguments/16-bohmian-enfoldment-dialogical-return.md` |
| 91 | BASENAME/unresolved-title-only | Arche-Topos as Differential Field | `section-rooms/05-psychoid-flowering/movements/31-s4-p0-psychoid-problem.md` |
| 90 | BASENAME/unresolved | Antikythera Agentworld Brief | `section-rooms/00-integral-threshold/movements/01-s01-p0-question-before-mechanism.md` |
| 90 | BASENAME/unresolved | Return of Zero Source Bank Index | `symbolon/episteme/concepts/reference-notes/jungian-quaternity.md` |
| 77 | BASENAME/unresolved-title-only | Computational Process Ontology | `section-rooms/01-differentiating-mind/movements/09-s0-p2-vikalpa-samkalpa.md` |
| 74 | BASENAME/unresolved-title-only | Sym-Ballein | `section-rooms/03-two-logics/movements/21-s2-p2-sym-ballein.md` |
| 70 | BASENAME/unresolved-title-only | Paradox as Cross-Register Hinge | `section-rooms/arguments/04-arche-topos-topology-music.md` |
| 51 | BASENAME/unresolved-title-only | Objective Internality | `section-rooms/01-differentiating-mind/movements/12-s0-p5-objective-internality.md` |
| 50 | BASENAME/unresolved | The Return of Zero — Central Argument Plan | `quilt/agentworld-response-matrix.md` |
| 45 | BASENAME/unresolved-title-only | Tattvic Differential Field | `section-rooms/01-differentiating-mind/movements/12-s0-p5-objective-internality.md` |
| 40 | BASENAME/unresolved-title-only | Agent Subjectivity Must Remain Open | `section-rooms/07-instrument-returns/movements/48-s50-p5-ahi-planetary-return.md` |
| 36 | BASENAME/unresolved-title-only | Mono-Poly: Whole and Many | `section-rooms/07-instrument-returns/movements/46-s50-p3-4-2-mono-poly.md` |
| 35 | BASENAME/unresolved-title-only | Artificial Hybrid Intelligence as Reflective Field | `section-rooms/07-instrument-returns/movements/48-s50-p5-ahi-planetary-return.md` |
| 31 | BASENAME/unresolved-title-only | Prakāśa-Vimarśa | `section-rooms/01-differentiating-mind/movements/07-s0-p0-awareness-bends-display.md` |
| 31 | BASENAME/unresolved-title-only | Trust, Faith, and the Formal Limit | `section-rooms/07-instrument-returns/movements/46-s50-p3-4-2-mono-poly.md` |
| 25 | BASENAME/unresolved-title-only | Toroidal Circulation and the Arche-Topos | `symbolon/episteme/concepts/reference-notes/torus-circulation-magnetic-confinement.md` |
| 18 | BASENAME/unresolved | Hephaestus and the Net | `section-rooms/05-psychoid-flowering/movements/35-s4-p4-gebser-apollo-dionysus.md` |
| 18 | BASENAME/unresolved-title-only | Vāk | `section-rooms/arguments/09-prakasa-vimarsa.md` |
| 17 | BASENAME/unresolved-title-only | Deferential Intelligence | `section-rooms/06-objective-internality/movements/42-s5-p5-research-vectors.md` |
| 17 | BASENAME/unresolved-title-only | The Two Ones — Mono–Poly Matheme | `section-rooms/arguments/09-prakasa-vimarsa.md` |
| 15 | BASENAME/unresolved | The Nothing That Is - Robert Kaplan | `symbolon/episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/AUTHORIAL-TEXT.md` |
| 14 | BASENAME/unresolved-title-only | Prompt Thrownness | `section-rooms/05-psychoid-flowering/movements/36-s4-p5-mef-prompt-thrownness.md` |
| 14 | BASENAME/unresolved-title-only | The Advent of Zero, Subject, and Integral Logic | `section-rooms/arguments/03-two-logics-and-sym-ballein.md` |
| 14 | BASENAME/unresolved | Antikythera Agentworld Brief#Source PDF page 4 | `quilt/agentworld-response-matrix.md` |
| 14 | FILE-RELATIVE-PATH/broken | ../README | `symbolon/mytheme/README.md` |
| 13 | BASENAME/unresolved-title-only | Bohmian Enfoldment and Dialogical Return | `section-rooms/arguments/19-two-ones-mono-poly-matheme.md` |
| 13 | BASENAME/unresolved | Antikythera Agentworld Brief#Source PDF page 41 | `quilt/agentworld-response-matrix.md` |
| 12 | BASENAME/unresolved-title-only | Agentworld | `symbolon/episteme/concepts/centaur-societies.md` |
| 11 | BASENAME/unresolved | Antikythera Agentworld Brief#Source PDF page 5 | `section-rooms/arguments/14-computational-process-ontology.md` |

Confirmed spot check: every `unresolved-title-only` target above (e.g.
"Immutable Gap and Meta-Sign", "Core Theorem Bridge", "Sym-Ballein",
"Objective Internality") is the exact `title:` frontmatter value of a real
argument node whose filename is its numbered slug
(`section-rooms/arguments/01-immutable-gap-and-meta-sign.md`,
`.../12-core-theorem-bridge.md`, `.../03-two-logics-and-sym-ballein.md`,
`.../02-objective-internality.md`) — none of these nodes currently carries an
`aliases:` entry equal to its title. Combined, `unresolved` +
`unresolved-title-only` cover 431 distinct targets across 2,085 link
instances.

**"Antikythera Agentworld Brief" (90 hits)** and **"Return of Zero Source
Bank Index" (90 hits)** are two more of the very highest-volume targets —
both appear to be links to venue/source-index material that either was never
created as a filename/alias inside the vault, or lives only as a `title:` on
a node elsewhere; not confirmed further here (out of scope for the mechanical
pass — flag for the source-bank owner). The `#Source PDF page N` variants are
the same "Antikythera Agentworld Brief" target with a heading/page fragment
appended, compounding the base miss.

### Ambiguous targets (5 unique, 22 instances)

| Target | Candidates | Example source |
|---|---|---|
| `j-space` | `symbolon/episteme/concepts/j-space.md`, `symbolon/matheme/computation/j-space.md` | `section-rooms/06-objective-internality/movements/42-s5-p5-research-vectors.md` |
| `mathematical-artistic-image-register` | `symbolon/episteme/concepts/mathematical-artistic-image-register.md`, `symbolon/episteme/concepts/reference-notes/mathematical-artistic-image-register.md` | `quilt/ql-expression-grammar.md` |
| `bimba-pratibimba` | `symbolon/episteme/concepts/bimba-pratibimba.md`, `symbolon/episteme/concepts/reference-notes/bimba-pratibimba.md` | `symbolon/episteme/concepts/world-picture-to-world-atlas.md` |
| `apoha` | (2 basename collisions in vault) | see JSON |
| `the-slash` | (2 basename collisions in vault) | see JSON |

Each is a `concepts/X.md` vs `concepts/reference-notes/X.md` (or
`matheme/computation/X.md`) filename collision — the reference-notes shelf
duplicates the primary concept-node basename in four of five cases.

### Alias-only (21 instances, resolve today only via `aliases:`)

Mostly links to the numbered `C##-Name` concept nodes by their plain name
(`Diaphaneity` → `C09-Diaphaneity.md`, `Pratyabhijñā` → `C19-Pratyabhijna-
Recognition.md`, `Severance` → `C23-Severance.md`, `Fusion` →
`C24-Fusion.md`, `Operative Measure` → `C14-Maya-Operative-Measure.md`).
These currently work because the target file declares the plain name as an
`aliases:` entry — fragile (a single alias, no basename fallback) but not
broken.

---

## 4. Markdown-link `#fragment` check

2,182 markdown links `[label](path#fragment)` were found with a `#` fragment
(all of them — not sampled, since 2,182 was cheap to check exhaustively by
script: resolve `path` relative to the *linking file's directory* per
standard Markdown-link semantics, then test whether `fragment` matches a
heading in the target file, case/whitespace/hyphen-insensitively, or an
`<a id="…">`/`^blockid` anchor).

| Outcome | Count |
|---|---:|
| fragment found (heading or anchor match) | 1,810 |
| target file missing (path doesn't resolve to a file in the vault) | 302 |
| fragment not found in an existing target | 70 |

The 302 "target file missing" cases are markdown links whose relative `path`
component doesn't resolve under the linking file's own directory — worth a
separate relative-markdown-link path audit if the vault-root move also wants
markdown-link hygiene fixed, but out of scope for this wikilink-only task
(recorded in the JSON as `markdown_link_fragments`, `target_exists: false`).
The 70 "fragment not found" cases are candidates for stale-heading drift
(heading text changed after the link was written) — see JSON for the full
list (`fragment_found: false`, `target_exists: true`).

---

## 5. Proposed mechanical rewrite plan

**A. REPO-ABSOLUTE, resolves (783 instances) — deterministic, safe to
script.** Strip the leading `submission-package/essay/` from the wikilink
target. `[[submission-package/essay/symbolon/episteme/concepts/apoha]]` →
`[[symbolon/episteme/concepts/apoha]]`. A single regex substitution across
the corpus (`\[\[submission-package/essay/` → `[[`, applied only inside
`[[...]]` spans, careful of the `|label` and `#heading` tails) handles all
783 in one pass. Purely mechanical; no target-page changes needed.

**B. REPO-ABSOLUTE, out-of-body (129 instances) — genuinely out-of-body,
cannot be rewritten to resolve.** These point at `working/…` and similar
paths outside `submission-package/essay/`. Once the vault root moves, they
cannot become wikilinks at all (no `../` escape in Obsidian's wikilink
resolution). Mechanical options, in order of fidelity: (1) convert to a
standard Markdown link `[label](../../working/…)` computed relative to the
*linking file's actual directory* (Markdown links do resolve file-relative,
per this task's own note) — fully scriptable since both the source file path
and the intended repo-absolute target are known; (2) if the material should
be *inside* the vault (i.e., it's really provenance for a claim that belongs
in-body), that's an editorial call, not a mechanical one — flag rather than
rewrite. Recommend (1) as the default mechanical rewrite, with the resulting
list of converted links handed back for a provenance review pass.

**B2. REPO-ABSOLUTE, out-of-body-missing (7 instances) — dangling regardless.**
Six of seven point at `working/sources-texts-references/reference-notes/{apoha,
bimba-pratibimba}` which does not exist anywhere in the repo (the real files
live at `symbolon/episteme/concepts/reference-notes/apoha.md` /
`bimba-pratibimba.md` under `submission-package/essay/`, i.e. inside the
vault). These are simple mis-paths, not out-of-body content — mechanically
correctable to `[[symbolon/episteme/concepts/reference-notes/apoha]]` etc.
Not part of the 783 in bucket A because the raw path didn't parse as
in-vault; worth a manual regex carve-out (7 known targets, listed in JSON).

**C. REPO-ABSOLUTE, unresolved (17 instances) — needs individual triage.**
Mix of (i) trailing stray backslashes in the link text (`…prompt-thrownness\`,
`…godel-1931-undecidable-propositions\`) — mechanical fix, strip the
backslash, then re-resolve (most become bucket A); and (ii) genuine gaps —
links into a `symbolon/episteme/sources/quotes/` shelf that does not exist in
the current tree (`vaswani-et-al-2017-attention`, `kauffman-2014-…`,
`atmanspacher-2020-…`, `pind-2009-…`, `bratton-2026-agentworld-brief`,
`maroski-2025-…`) — these need the quote shelf built or the links
re-targeted to the actual `SOURCE.md` house; not mechanical.

**D. FILE-RELATIVE-PATH (40 instances, all `broken`) — deterministic once a
policy is picked.** All 40 are `../…`/`./…` links, overwhelmingly `../README`
family links between README index files, plus a handful in
`episteme/etymologies/`/`episteme/histories/` HISTORY cross-links. Since
Obsidian doesn't resolve these as file-relative, two mechanical options: (1)
rewrite to the equivalent vault-relative wikilink by resolving `../` against
the *linking file's* real directory (fully computable — the script already
does this to test for "resolves-by-coincidence", and can instead just emit
the corrected vault-relative form); or (2) convert to standard Markdown
relative links (`[README](../README.md)`), which Obsidian resolves
file-relative for real. Recommend (2) for the README-to-README family
specifically, since these are pure navigation scaffolding, not
citation-bearing prose links; (1) for the etymologies/histories HISTORY
cross-links, which read as content wikilinks. Either way this is
mechanical — no ambiguity, all 40 targets are recoverable from the linking
file's path alone.

**E. VAULT-RELATIVE-PATH (30 instances, all `unresolved`) — split into two
mechanically distinct groups.** (i) ~15 genuine path attempts, several
embedding the whole `Antykathera-Essay-Work/…` folder name (one level too
high) or a `working/…`/`submission-package/epi-logos/…` target outside the
vault — treat exactly like bucket B/C above, case by case (targets listed in
JSON, `form: VAULT-RELATIVE-PATH`). (ii) ~15 are not real paths at all: a
concept name that happens to contain a literal `/` (`The Slash (AND/OR)`,
`Dia/Syn`, `Paśu / Bounded Subject-Position`, `Script / Frozen Conditioned
Will`, `A/C — Argument / Concept — Root of the Conjugate Field`, `Living
Symbol / Idol`, `Cultural Individuation / Epi-Logos-as-Culture`, `Pratyabhijñā
/ Recognition`, `Antaḥkaraṇa / Inner Instrument`). **These need an editorial
decision, not a mechanical rewrite**: either escape/rename so the `/` no
longer triggers Obsidian's path-mode parsing (impossible to fully avoid if
the concept's real name contains a slash), or — the recommended fix —
require the target concept node to declare that exact slash-bearing string
as an `aliases:` entry and rewrite the link to the node's plain filename
target instead (e.g. `[[The Slash (AND/OR)]]` → `[[the-slash|The Slash (AND/OR)]]`
provided `the-slash.md` carries `aliases: ["The Slash (AND/OR)", "Dia/Syn", …]`
as appropriate) — mechanical rewrite once the alias is authored, not before.

**F. BASENAME, resolves-unique (1,205) and alias-only (21) — no action
needed.** These already work at any vault root, since Obsidian's basename/
alias fallback is root-independent. Leave as-is.

**G. BASENAME, ambiguous (22 instances / 5 targets) — needs target-side
disambiguation, not link-side rewriting.** Each collision is a
`concepts/X.md` vs `concepts/reference-notes/X.md` (or `matheme/computation/
X.md`) basename duplicate. Two mechanical paths once Frank picks the
canonical home per pair: (1) rename the non-canonical file to a
disambiguated basename (e.g. `reference-notes/apoha.md` → `reference-notes/
apoha-reference-note.md`) so the basename map is unique again — no link edits
required, all currently-ambiguous links resolve; or (2) rewrite every
instance to an explicit vault-relative path pointing at the intended file.
(1) is lower-touch (5 file renames vs 22 link edits) and is recommended.

**H. BASENAME, unresolved-title-only (1,197 instances / 146 unique targets)
— the largest bucket, needs a target-side alias-authoring pass, then a fully
mechanical link-relabel.** Once each of the 146 title-only targets gets an
`aliases:` entry equal to its exact `title:` string on its owning node (a
scripted pass: for each unique title-only target, `find_title_owner()` — as
demonstrated in this audit — already locates the exact file deterministically
for the overwhelming majority, since Obsidian's basename/alias resolution is
root-independent and each `title:` value is close to unique per spot-check),
**no link text needs to change at all** — the wikilinks already read
`[[Exact Title]]` and will resolve the instant the alias exists on the
target. This converts the largest broken bucket into a target-metadata
patch (146 files, one `aliases:` line each) rather than 1,197 individual
link edits. Recommend generating the full 146-target → owning-file mapping
as a first deliverable (script already proven on the top-30 sample above),
then adding aliases in one batch.

**I. BASENAME, unresolved (888 instances / remaining ~285 of the 431 unique
unresolved+title-only targets) — needs per-target triage, not a single
mechanical rule.** Some are the same class as H but the title search found
no owner at all (content genuinely doesn't exist yet, e.g. "Antikythera
Agentworld Brief", "Return of Zero Source Bank Index" — both very
high-frequency and worth prioritizing); others are typos or renamed-since
targets. Recommend: run the same `find_title_owner`-style search plus a
fuzzy basename search (e.g. slug-normalized comparison) over all 888 to
split into "owner found, needs alias" (folds into bucket H) vs "no owner
anywhere in the vault" (needs either the missing node authored or the link
retired) before any rewrite.

### Summary of what's mechanical vs what needs judgment

| Bucket | Instances | Mechanical? |
|---|---:|---|
| A: REPO-ABSOLUTE prefix strip | 783 | Yes — one scripted pass |
| B2: REPO-ABSOLUTE mis-path (in-vault target, wrong prefix) | 7 | Yes — 7 known corrections |
| D: FILE-RELATIVE-PATH → vault-relative or MD link | 40 | Yes — path is computable from source location |
| F: BASENAME already resolving | 1,226 | N/A — no change needed |
| H: BASENAME title-only, once aliases added | 1,197 | Yes, *after* a one-time alias-authoring pass (146 files) |
| B: REPO-ABSOLUTE out-of-body → MD relative link | 129 | Mechanical rewrite, but is an editorial acknowledgment that content stays out-of-body |
| C: REPO-ABSOLUTE unresolved | 17 | Partly (backslash strip); partly needs a missing-source decision |
| E: VAULT-RELATIVE-PATH | 30 | Half mechanical (real mis-paths), half needs alias authoring (slash-bearing titles) |
| G: BASENAME ambiguous | 22 | Mechanical once one of 5 collisions is renamed |
| I: BASENAME unresolved, no title owner | remainder of 888 | Needs per-target triage; not mechanical |

Total link instances that resolve today or become resolvable through a
purely mechanical rewrite (A+B2+D+F+H+G, once the one-time alias/rename
prep lands): **3,275 of 4,292 (~76%)**. The remaining ~1,017 split between
out-of-body acknowledgments (B, 129 — content intentionally outside the
vault), genuinely missing content or typos (C, I), and slash-in-title cases
needing an alias decision (E, ~15).

---

## Files produced

- `wikilink-forms-audit.md` — this report
- `wikilink-forms-audit.json` — per-link records: `{source, source_class,
  raw_target, target, form, resolution, resolved_file, candidates?}` for all
  4,292 wikilinks, plus `markdown_link_fragments` for all 2,182 markdown
  links carrying a `#fragment`
- `audit.py` — the scan script (re-runnable; regenerates both files)
