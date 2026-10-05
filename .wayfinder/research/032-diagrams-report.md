---
title: "Ticket 032 — Matheme diagrams report"
label: wayfinder:research
ticket: ../tickets/032-figures-matheme-diagrams.md
created: 2026-09-25
assignee: diagrams-agent-2026-09-25
---

# 032 — Figures production I: matheme diagrams — report

Six record+asset pairs landed in `submission-package/essay/symbolon/matheme/diagrams/`
(the directory's only prior file, its `README.md` contract, is untouched). All assets are
hand-authored original SVG, created for the essay; no scraped or downloaded material; no
rights risk. Every record's frontmatter parses (`yaml.safe_load`), every declared asset
exists, every anchored movement path and every path-form source dependency was verified to
exist, and every SVG is well-formed XML. All six were render-checked. Nothing was embedded
into any section; no builders, no suite, no git; no existing file was edited (except the
ticket's own `assignee:` line, as instructed).

## Records landed

| Slug | Proposition (one line) | Anchored movements |
|---|---|---|
| `crossed-zero-recognition-chain` | The seven-stage native recognition sequence `0 → Ø → X → Ø/X → (0/Ø)/(1/X) → 1 ↷ 0/1`, each office named, the return drawn as a distinct operation. | `05-psychoid-flowering/movements/34-s4-p3-lacan-matheme-mytheme.md` (primary; M34 states the chain and its offices), `02-return-of-zero/movements/16-s1-p3-crossed-zero.md` (guard: M16 deliberately withholds the full chain). |
| `sheffer-nor-reduction` | One connective (NOR) generates every Boolean truth function — and the seam: functional completeness holds within a defined field; the QL slash is not another Boolean input and is not generated. | `02-return-of-zero/movements/15-s1-p2-empty-set-generates-one.md` (primary; the spare-beginning operation family, manuscript M15 carries the NOR display), `02-return-of-zero/movements/17-s1-p4-zero-outside-math.md` (the container-disclosing boundary). |
| `re-entry-projective-fork` | Two formal neighbours of the native fork in comparative adjacency — mark/re-entry with iterants (`(Dη)²=−I`) beside the projective charts `u=x/y`, `v=y/x` with overlap `v=1/u` — the dashed divider itself asserting non-equivalence. | `04-mathematical-substrate/movements/27-s3-p2-mark-reentry-complex.md`, `04-mathematical-substrate/movements/28-s3-p3-projective-dimensional-reframing.md`. |
| `spanda-4-2-attunement-stack` | The Second Spanda vertical accounting `100% = 2⁶+6² = 64+36` → (declared operation) `16/9 = 2⁴/3²` → `4+2`, with the sixfold side-railed from `2+2²=6`, the declared operator `ℋ_QL(4:2,3:3):=(4/3,2/3)`, the ratio family, and the exact completion `16/9·9/8 = 2/1`. | `04-mathematical-substrate/movements/26-s3-p1-spanda-4-2.md` (sole anchor; the bands reproduce its four-warrant table arrow by arrow). |
| `atlas-two-chart-circle` | Two charts `u=x/(1−y)`, `v=x/(1+y)` on the unit circle joined by `uv=1, v=1/u`; the motion test (`du/dt=2 → dv/dt=−2/9`, yet `dy/dt=6/25` by either route) shows the translation doing real work; no global chart exists. | `04-mathematical-substrate/movements/28-s3-p3-projective-dimensional-reframing.md` (the atlas passage lives in M28's span of the manuscript); jigsaw/atlas whole as framing provenance. |
| `ql-unit-mandala-eight-determinations` | The canonical concentric QL-unit layout: centre `0/1` (ground–mark relation, empty of object), four stations at the degree-table compass points with their constructions, `∞/dx` as enclosing ring, `/ = −/−` and `1/0` as frame; forward folds and the east–west phase-flip drawn, nothing else implied. | `04-mathematical-substrate/movements/25-s3-p0-eight-determinations.md` (whose drafting payload calls for the contemplative QL plate). |

## Wiring list (for the later embedding ticket)

1. `ql-unit-mandala-eight-determinations.svg` → `section-rooms/04-mathematical-substrate/movements/25-s3-p0-eight-determinations.md`, beside the determinations table.
2. `spanda-4-2-attunement-stack.svg` → `section-rooms/04-mathematical-substrate/movements/26-s3-p1-spanda-4-2.md`, beside the vertical accounting; it already satisfies M26's explicit demand that a plate state the QL-composition rule beside `0/1 + 1/0 = 1/1 = 100%`.
3. `re-entry-projective-fork.svg` → the M27→M28 join in room 04 (either at the end of 27's transition or at 28's opening); it spans both movements' operations.
4. `atlas-two-chart-circle.svg` → `section-rooms/04-mathematical-substrate/movements/28-s3-p3-projective-dimensional-reframing.md`, where the manuscript displays the circle charts (manuscript lines ~1231–1251).
5. `sheffer-nor-reduction.svg` → `section-rooms/02-return-of-zero/movements/15-s1-p2-empty-set-generates-one.md` (where the manuscript displays the NOR scene). The room's `READING.md` routes the NOR/NAND material toward M16/M17 as "material field"; if the embedding ticket prefers that route, M16/M17 are acceptable — but the diagram must not land at or after the two-logics room, where the seam has already been crossed.
6. `crossed-zero-recognition-chain.svg` → `section-rooms/05-psychoid-flowering/movements/34-s4-p3-lacan-matheme-mytheme.md`, beside the sequence display. Hard constraint: never at or before M16 — M16 deliberately withholds `Ø/X`, `(0/Ø)/(1/X)` and the return, and early embedding would falsify the essay's staging.

## Briefs left unresolved, and why

- **image-02 — promissory glyph plate `(0/1)/(1/0)`.** Not produced here. (a) The live essay no longer carries the glyph at the briefed threshold station; its first locked use is M19, and M06's zero is explicitly promissory with warrants "deliberately deferred". (b) The brief's own operation is "a spare typographic plate introduced without explanatory diagram" — a formal diagram at that station would falsify the promissory gesture it exists to perform. (c) Per the visuals skill's domain routes, a composed typographic plate is plate-work (`mytheme/plates/`), not a matheme diagram. The glyph's formal anatomy is nevertheless now carried by three landed diagrams (mandala centre, attunement stack, crossed-zero chain). Recommend: resolve as a typographic treatment in the manuscript, or a `mytheme/plates` ticket.
- **image-09 — unmarked axle and comma.** A coda brief joining the Antikythera mechanism's axle with the Pythagorean comma ("the ground is not another gear"). This is a composed imaginal argument, not a formal derivation; its home is `mytheme/plates/` (or `episteme/figures/` for the mechanism evidence), and it needs artifact-imagery decisions outside this ticket's originals-only SVG scope.
- **image-01 (mechanism gearing), image-03 (self-inquiry stripping scene), image-04 (Salem manuscript field), image-07 (psychoid artifact field).** Not matheme-side: gearing is evidential (`episteme/figures/`), the other three are composed imaginal arguments (`mytheme/plates/`). Out of domain for this ticket.

## Deviations declared

- **Sheffer brief said NAND; the diagram draws NOR.** The essay displays the dual NOR (Peirce down-arrow) scene from Kaplan and explicitly declines the historical Peirce–Sheffer–Wittgenstein priority claim; the diagram follows the essay's actual display, and the record states the resolution. NAND appears nowhere in the asset because the essay does not display it.
- The attunement stack omits the Offered material (Śaiva naming, tetraktys amplification) by design: M26 excludes it from the proof spine.
- The mandala draws only the declared forward folds; the complementary folds (Essence `0+5`, Constitution `1+4`, Text-Texture `2+3`) are real in the source but their omission from the figure is declared in the record's proof boundary.
- Records declare `record_id` (curated Wiki nodes on next ingest) and vault-relative `essay_blocks`/`source_dependencies` paths chosen to be machine-checkable; no builders were run.
