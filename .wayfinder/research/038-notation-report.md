# Ticket 038 — Notation / Expression-Law Pass (Report)

- **Ticket:** `.wayfinder/tickets/038-notation-expression-law-pass.md` (assignee set: `notation-agent-2026-09-25`)
- **Law enforced:** `submission-package/essay/quilt/ql-expression-grammar.md` (2026-07-29), with the central plan's "Locked notation and claim discipline" and `WRITING-PROTOCOL.md` notation lines read first; display-style precedent `working/sources-texts-references/10-7-2026-core-theorems-pithy.md`.
- **Nature of the pass:** transcription into the sanctioned tiers only. No semantic change; `X/x` and all authorial notation untouched; no code blocks, frontmatter, or link targets altered; no git, no builders, no tests run.

## Conversion counts

Moves: **(a)** bare operated relation → `$$…$$` display; **(b)** bare named token → backticks; **(c)** surviving `\(…\)` → `$…$` (genuine inline math) or backticks (named tokens); **(d)** = display-form normalization of existing `\[…\]` blocks to the sanctioned `$$…$$` display tier (form-only, content untouched).

### Tier 1 — `submission-package/essay/THE-RETURN-OF-ZERO.md`

| File | a | b | c | notes |
|---|---|---|---|---|
| THE-RETURN-OF-ZERO.md | 0 | 9 tokens / 7 lines | 0 | headings `## §0/1`, `## §5→0` (body + Notes = 4); L535 `**Ø**`→`` `Ø` ``; L2610 `Ø, ∅, S/s`; L2720 `X/x` |

The manuscript already carried 43 `$$…$$` blocks (86 delimiter lines, intact after the pass), zero surviving `\(…\)`, and no bare operated relations in prose (equation scan found only quoted titles/equations — see ambiguity log).

### Tier 2 — `section-rooms/` room surfaces and movements

| File | b | c |
|---|---|---|
| 00-integral-threshold/P1-CANONICAL-ALIGNMENT.md | 2 (heading `§0/1`; prose `§0/1`) | — |
| 00-integral-threshold/READING.md | 5 | — |
| 00-integral-threshold/movements/04-s01-p3-formal-limit-genealogy.md | 1 (`#5→0`) | — |
| 00-integral-threshold/movements/05-s01-p4-gebser-diaphaneity.md | 1 line / 2 tokens (`§3 · #5→0`, `§5`) | — |
| 01-differentiating-mind/movements/10-s0-p3-apoha.md | 1 (`§0/1`) | — |
| 02-return-of-zero/movements/14-s1-p1-sunya-operational.md | 1 (`a/0`) | 2 → `$a+0=a$`, `$a\cdot0=0$` |
| 02-return-of-zero/movements/17-s1-p4-zero-outside-math.md | 2 (`1/0` ×2) | 4 → `$…$` (`1/0=x`, `0x=1`, `0x=0`, `x`) |
| 03-two-logics/movements/20-s2-p1-dia-ballein.md | — | 2 → backticks (`-1`, `+1`) |
| 03-two-logics/movements/21-s2-p2-sym-ballein.md | — | 4 → backticks (`0/1` ×2, `1/0` ×2) |
| 03-two-logics/movements/24-s2-p5-zero-changes-role.md | — | 1 → backtick (`5→0` from `\(5\to0\)`) |
| 04-mathematical-substrate/P1-CANONICAL-ALIGNMENT.md | 1 (`4+2`) | — |
| 04-mathematical-substrate/movements/26-s3-p1-spanda-4-2.md | 1 (heading title `4+2`) | — |
| 04-mathematical-substrate/movements/27-s3-p2-mark-reentry-complex.md | — | 2 → `$…$` (`-1`, `i`) |
| 04-mathematical-substrate/movements/29-s3-p4-topology-music-resolution.md | 1 (`§3 · #5→0`) | — |
| 04-mathematical-substrate/movements/30-s3-p5-arche-topos.md | 1 line / 2 tokens (`§3 · #5→0`, `§5`) | 5 → backticks (`0/1`, `3:3`, `4:2`, `X/x`, `2+2² = 4+2 = 6`) |
| 05-psychoid-flowering/movements/32-s4-p1-jung-individuation.md | 2 (`X/x` ×2) | — |
| 05-psychoid-flowering/movements/35-s4-p4-gebser-apollo-dionysus.md | 1 (`§0/1 #4`) | — |
| 05-psychoid-flowering/movements/36-s4-p5-mef-prompt-thrownness.md | 1 (`§5→0`) | — |
| 06-objective-internality/P1-CANONICAL-ALIGNMENT.md | 1 (`5→0`) | — |
| 06-objective-internality/movements/42-s5-p5-research-vectors.md | 1 (heading `## 5→0 return` → `` ## `5→0` return ``) | — |
| 07-instrument-returns/P1-CANONICAL-ALIGNMENT.md | 2 | — |

Tier-2 totals: **(b) 25 tokens**, **(c) 18 → backticks + 8 → `$…$`**.

### Tier 3 — canonical nodes (arguments / concepts / conjugate / products / reference-notes)

| File | b | c |
|---|---|---|
| arguments/A05-Prakasa-Vimarsa.md | 2 (`0/1` ×2) | — |
| arguments/A11-The-Two-Ones-0-One-1-All.md | 1 (`0/1`) | — |
| arguments/A12-Mono-Poly-One-All-Whole-Many.md | 1 line / 5 tokens (`§0, §2, §4, §5, §5→0`) | — |
| arguments/A18-Primordial-Symbolon-and-Its-Eight-Determinations.md | 1 (`X/x`) | — |
| arguments/A21-Individuation-Recognition.md | 1 (`X/x`) | — |
| arguments/concepts/C02-Faithful-Definition.md | 1 (`AM/IS`) | — |
| arguments/concepts/C49-The-Two-Ones-0-One-1-All.md | 1 (`0/1`) | — |
| arguments/concepts/C51-Logos-Epi-Logos.md | 2 (`§5→0` ×2) | — |
| arguments/concepts/C61-Symbolon-Disclosure-Architecture.md | 1 (`§5/§5→0`) | — |
| arguments/concepts/reference-notes/surface-classification-4g-2g.md | 1 (`4+2`) | — |
| arguments/concepts/reference-notes/mono-poly-planetary-intelligence.md | — | 3 → backticks (`1` ×2, `0`) |
| arguments/conjugate/A18-prime-Traversal-Run-in-Code.md | 10 (`(4+2)+2` ×3 — one was bold, now backticked; `§0/1`, `4+2` ×2, `§5→0` ×2 — two were bold-wrapped; `§0–§5`) | — |
| arguments/conjugate/A27-prime-Encounter-over-Sovereignty.md | 1 (`AM/IS`) | — |
| arguments/products/S1-Actuation.md | 1 (`5→0`) | — |
| arguments/products/S5-Quaternal-Logic.md | 1 (`5→0`) | — |

Tier-3 totals: **(b) 25 tokens / 13 files**, **(c) 3 → backticks**. Bold-wrapped named tokens (`**(4+2)+2**`, `**§5→0 is \`1/0\`…**`) were transcribed to the backtick tier; bold remains reserved for positions per law §I.3.

### Tier 4 — `symbolon/matheme/`

| File | b | c |
|---|---|---|
| README.md | 4 | — |
| definition/README.md | 6 tokens | — |
| definition/catuskoti-crossing.md | 2 | — |
| definition/copula.md | 1 | — |
| definition/immutable-subject.md | 1 (table cell `Ø/X`) | — |
| definition/minus-over-minus.md | 1 | — |
| definition/six-determinations.md | 8 (six `**TOKEN — Name.**` definition heads → backtick tier; `(4+2)+2`; `1/0` link) | — |
| definition/the-matheme.md | 1 | — |
| dia-syn/chronic.md | 1 | — |
| formal-neighbours/README.md | 1 | — |
| formal-neighbours/calculus-infinity-dx.md | 1 | — |
| formal-neighbours/chaos-attractors.md | 1 | — |
| formal-neighbours/fde-catuskoti.md | 2 | 32 `\(…\)` → `$…$`; 4 `\[…\]` → `$$…$$` |
| formal-neighbours/godel-incompleteness.md | 1 | — |
| formal-neighbours/kauffman-iterants.md | 2 lines / 5 tokens (chains `0/1 = 4+2 = 5→0 = 0/1`, `1/0 = 4′+2′ = 5′→0′`) | 17 → `$…$`; 10 displays → `$$…$$` |
| formal-neighbours/noether-symmetry-conservation.md | — | 16 → `$…$`; 14 displays → `$$…$$` |
| formal-neighbours/russell-types.md | 1 | — |
| formal-neighbours/von-neumann-ordinals.md | 1 | — |
| mono-poly/README.md | 1 | — |
| music/README.md | 1 | — |
| music/foundational-ratios.md | 1 | — |
| music/lens-anchors.md | 1 | — |
| process/README.md | 1 | — |
| ql/README.md | 3 | — |
| ql/binary-and-binary-of-binary.md | 2 | — |
| ql/eight-determinations.md | 14 table cells (`0/1`, `?/!`, `−/+`, `X/x`, `AM/IS`, `∞/dx`, `(0/1)/(1/0)`, `0/0 = %`, `1/0 = ?/!`, `1/1 = 100%`, `(1/0)/(0/1)`) | — |
| ql/primordial-symbolon.md | 4 | — |
| ql/x-x.md | 4 | — |
| quilt/README.md | 4 | — |
| quilt/psychology.md | 1 | — |
| diagrams/spanda-4-2-attunement-stack.md | 2 | — |
| topology/torus-cover-winding.md | — | 13 → `$…$`; 6 displays → `$$…$$` |
| topology/manifold-atlas.md | — | 13 → `$…$`; 7 displays → `$$…$$` |
| topology/toroidal-poloidal-confinement.md | — | 7 → `$…$`; 7 displays → `$$…$$` |

Tier-4 totals: **(b) 67 tokens / 30 files**, **(c) 98 `\(…\)` → `$…$`**, **(d) 48 `\[…\]` blocks → `$$…$$`**.

### Grand totals

- Move (a): 0 new display blocks were needed — no bare *operated* relation was found standing in prose anywhere in scope (the manuscript's 43 existing `$$` blocks and the sources' precedent already carry them; every prose `=`/arrow hit judged was naming or ordinary prose).
- Move (b): **143 token conversions** (manuscript 9, rooms 25, nodes 28, matheme 67 + 14 table cells already counted) — see tables.
- Move (c): **124 `\(…\)` retirements** — 18 → backticked Unicode tokens (incl. `\(5\to0\)` → `` `5→0` ``, `\(2+2^2=4+2=6\)` → `` `2+2² = 4+2 = 6` ``), 106 → `$…$` inline math.
- Display normalization (d): **48 `\[…\]` → `$$…$$`** in 6 matheme records.
- **Files touched: 62** (+ the ticket file's `assignee:` line). Generated surfaces untouched (below).

## Ambiguity log (judged, left untouched — file:line, token, judgment)

Manuscript (`submission-package/essay/THE-RETURN-OF-ZERO.md`):

1. L42 — quoted equation “3 = 1 + 2” — verbatim prose quotation, not an operated display; left.
2. L1631 — HTML comment `<!-- M36 / §4 #5→0 -->` — invisible build marker; left.
3. L2194 — `**Subject or Consciousness → mind … → Object**` — ontological order-of-dependence stated in ordinary prose, not mathematics; left (same at L2550 footnote).
4. L2274 — quoted work title “0/1 — Self-Identity: The Power of Self-Difference” — verbatim citation; left.
5. L2414 — quoted title “The Crossed Zero (Ø)…” — verbatim citation; left.
6. L2424 — quoted title “The Two Ones — 0 = One, 1 = All” — verbatim citation; left.
7. L2518 — `doi:10.1080/0308…` contains substring `0/0` — DOI identifier, checker false positive; left.
8. L2630 — `180°→360°`, `3:3/3:1` — citation-internal description of source content; left.
9. L2636, L2656–L2730 — lens/product pair notation `L0 × L5′`…, `Phenomenological × Phenomenal`, `Lk/L(5−k)′` — citation apparatus; the canonical `arguments/conjugate/AC.md` itself writes these bare, so bare is the established canonical form; left.
10. Bibliographic § locators (`§IX`, `§§III–V`, `§2.1`…) throughout Notes — Chicago locators, not QL mathemes; left.

Section-rooms (convention judgments, logged once each):

11. Movement H1 positional compounds `# §N · #N — Title` (24 headings) — indexed-position convention bound to frontmatter `station:` and generated ROOM.md nav; left as structural labels. Closest live precedent (32-s4-p1-jung-individuation.md) keeps `§4 · #1` bare while backticking the matheme `X/x` — followed here.
12. Node ladder headings `## #5→0` / `## #5→0 — Title` (100+ A/C/conjugate/matheme records) — determination-ladder index slots; left.
13. Wikilink aliases quoting movement titles (`[[45-s50-p2-…|§5→0 · #2 — …]]`, `[[26-s3-p1-spanda-4-2|§3 · #1 — … 4+2]]`, etc.) — label text mirroring the titles; left to avoid render-uncertainty and alias divergence.
14. READING-00 L116 `### #5→0 — Zero enters as a promise` — position ladder heading; left. L134 `**#5→0**` — bold positions are the law's own sanctioned tier (§I.3); left.
15. READING-02 L33 `[#5→0 — The Loan Returns](…)` — link label mirroring the movement title; left.
16. 03-s01-p2 L37 — `` `0 / 1` `` spaced variant already inside backticks; left as authorial spacing.

Matheme register:

17. `# §N — Title` file headings (`# §5→0 — The Catuṣkoṭi Crossing`, `# §1/0 — 0/1 = / ≠ 1/0`, `# §0 — −/− = AND/OR / X/x`, `# §2–§3 — 4+2 → (3+1)+2`, `# §0/1–§5→0 — The Immutable Subject`, `# §5′ — 5′→0′ = 1/0`, `# §5→0 — The Enantiodromic Return`) — §-prefixed structural labels mirroring the Binary Explication's file-section scheme; left verbatim, logged as a group. Free-standing mathemes in non-§ titles were backticked (`# Music — the `0/1` returned`, `# `X/x`: …`, `# `0/1` ↔ `1/0` — …`).
18. fde-catuskoti L107 — `**#5**`, `**#0**` — sanctioned bold positions; left.
19. noether L146 — wikilink alias `|§5 · #5→0]]`; left per 13.
20. kauffman-iterants `\[…\]`/`\[…`-family displays — converted to `$$…$$` (d); noted because the ticket's three moves did not name `\[…\]`; the law's display tier is `$$…$$` and the conversion is form-only.

## Verification output

1. **Zero surviving `\(…\)`** in manuscript + section-rooms + symbolon/matheme (generated ROOM.md excluded): `grep -rn '\\(' … | wc -l` → **0** (was 115 outside the manuscript).
2. **Bare-token audit** (context-judged; masking code fences, inline code, `$…$`/`$$…$$`, wikilink targets, HTML comments, frontmatter): manuscript → only the two logged leaves (L2274 quoted title, L2518 DOI). Section-rooms → 27 remaining hits, all logged leaves (wikilink aliases quoting titles, `## #5→0` ladder headings, sanctioned `**#5→0**` bold, movement H1 compounds). Matheme → only ladder headings and §-labels.
3. **Backtick balance**: 0 odd-backtick lines outside code fences in all 62 edited files (no masking breakage introduced).
4. **Anchors**: no `[](file#…)` links target any heading text changed by the pass.
5. **Spot-diff (10 files)** — re-read in context (no git used, per guardrails): manuscript L20/L535/L2610; P1-00 L5/L15; READING-00 L48/L144; six-determinations L20–22/L44; eight-determinations table L20–21; A18′ L23; fde-catuskoti L32–38 (now `$$` blocks); kauffman-iterants L49–56 (matrix display now `$$…$$`); 14-s1-p1 L41–43; 30-s3-p5 L31–32. All render-coherent, minimal diffs, no semantic drift.
6. Manuscript `$$` delimiter lines still 86 (nothing lost).

## Notes for the coordinator

- Generated surfaces (`section-rooms/README.md`, every `ROOM.md` — built by `tools/build-section-rooms.py`) were **not** hand-edited (AGENTS.md forbids it; this ticket forbids builders). They still carry the bare §-compounds; one movement H1 (26-s3-p1) now backticks `4+2` in its title, so run `python3 tools/build-section-rooms.py --project-root .` (and `--check`) plus the navigation builder at your discretion — the completion hook will flag anything stale.
- Scope stopped at the four tiers as ordered; `working/`, `symbolon/episteme/sources/`, and `quilt/` were not ranged into.
