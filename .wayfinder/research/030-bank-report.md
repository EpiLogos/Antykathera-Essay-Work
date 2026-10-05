# Ticket 030 — Own-voice bank report (poems → mytheme, aphorisms → episteme)

Executed 2026-09-25 by bank-agent-2026-09-25. No git commands, no builders, no suite runs.
Nothing at any origin was modified; Nara-Personal and personal/writing were read-only.

**Total files created: 120** — 96 in `submission-package/essay/symbolon/mytheme/poetry/`,
24 in `submission-package/essay/symbolon/episteme/aphorisms/`.

## Envelope convention

Every deposited file carries a provenance envelope at the very top with exactly:
`origin_path`, `retrieved: 2026-09-25`, `format`, `lifecycle: bank-unreviewed`,
`author: Frank G. Taylor`. Below the envelope the original content is byte-exact
(machine-verified: deposited bytes end with the source bytes for all 91 whole-file copies;
all 23 site-map block bodies and all 6 poems.js extracts verified verbatim against source).
No typos fixed, nothing curated or improved.

- Files that already carried YAML frontmatter at origin (the 79 Notion poems) take an
  **HTML-comment envelope** at the top so their original frontmatter survives verbatim below it.
- All other deposits take a **YAML frontmatter envelope**. None of the envelopes declare
  `record_id` or `source_id`, so nothing in the bank is curated by ingest.
- Site-map block files additionally carry `block_status:` (live / proposed) and the map's own
  verbatim status bracket as `status_note:` — the ticket's requirement, and both LIVE and
  PROPOSED blocks were included for weeding.
- Deposited filenames: kept identical to origin except where the origin name contained spaces
  or underscores, which were slugified (`Poems and Notes France Trip - 24-08-2026.md` →
  `poems-and-notes-france-trip-24-08-2026.md`; `poem p4 lines rewrite.md` →
  `poem-p4-lines-rewrite.md`; `tarot_journey_complete.md` → `tarot-journey-complete.md`).
  **No name collisions occurred between any deposit groups, so no origin-slug prefixes were
  needed.**

## Deposits to `symbolon/mytheme/poetry/` (96 files)

| Source | Count | Notes |
|---|---|---|
| (a) `/Users/admin/Central/Work/personal/writing/poetry/` | 79 | All 79 `.md` pieces copied (Gaia-2024 27 + Jan–Feb-2025 52). Manifest note: the `_index/notion-harvest-manifest.md` provenance file actually lives at `/Users/admin/Central/Work/personal/writing/_index/notion-harvest-manifest.md` — a sibling of `poetry/`, not inside it (the ticket's `poetry/_index/` path did not exist). Not copied: it documents the harvest, and the deposited files already carry the full Notion provenance in their own frontmatter (`source_url`, `notion_created/edited`, per-file SHA-able text). |
| (b) `/Users/admin/Central/Work/personal/Nara-Personal/journal/` | 8 | All 8 pieces: `consequence-inconsequential-april-2026`, `history-march-to-june-2026`, `infinite-infinitessimal-may-2026`, `poem-07-06-2026`, `spanda-karikas-arguments-april-2026`, `spiritual-isolation-may-2026`, `structure-of-present-march-2026`, `what-is-it-to-feel-may-2026`. Note: several are long working journals (up to 583 KB) mixing poems, dialogue records and argument work — deposited whole per "all 8 pieces"; Frank weeds. |
| (c) Nara-Personal vault root | 3 → poetry | `poems-and-notes-france-trip-24-08-2026.md`, `poem-p4-lines-rewrite.md`, `tarot-journey-complete.md`. |
| (d) `test-site/src/poems.js` | 6 | `site-poem-p0.md` … `site-poem-p5.md`, one per site poem, extracted verbatim from the JavaScript string literals (escapes decoded; verified character-exact). |

### 1d note — prose explication coverage

The ticket said the six site poems come "each with prose explication". In the actual
`poems.js` only **P1** carries a `detail` block (lede + two paragraphs) — extracted into
`site-poem-p1.md` under an `Explication` heading. The comment in the source records that this
explication was displaced from the Hero on 2026-06-23 and is pending rehoming; the file notes
nothing invented, and no explication was fabricated for P0/P2/P3/P4/P5, which carry none in
the source. P4 is rendered using Frank's own `stanzas` array (verified to reconstruct his
single-line `lines` string exactly, space-for-space). P0's matheme lines are wrapped in a
fenced block solely to preserve the multiple-space alignment of the original literals.

## Deposits to `symbolon/episteme/aphorisms/` (24 files, beside `investigation-and-faith.md`)

| Source | Count | Notes |
|---|---|---|
| (a) `test-site/docs/site-content-map-2.md` | 23 | Per-block/per-section files `site-a1-hero.md` … `site-c8-closing.md`: A1–A6 (Hero, Heart incl. its three cards, What Is Epi-Logos For, The Question, Install, Portal/Doorway close), B1–B9 (all Doorway stations), C1–C8 (Grammar: page intro, What QL Is, The Giving, Positions in depth, Lenses, Harmonics, Orchestration, Closing). LIVE blocks: A1–A6, B1–B9, C1, C8. PROPOSED blocks: C2–C7. The revision-note sections and implementation queues (Parts D–G) are not site copy and were not deposited; the "Voice palette" line-list inside Part E quotes Frank's phrases but as curation notes, not copy blocks — the phrases also live inside the deposited A/B/C blocks or in the papers listed below. |
| (b) Vault pieces reading as short prose / aphorism | 1 | `site-content-passages-june-15-21.md` — compiled verbatim `[F]` site-copy passages, 15–21 June 2026; routed to aphorisms (short prose) rather than poetry. Judgment call recorded here. |

## 3. `working/sources-texts-references/Epi Paper Write-ups/` — listed, NOT moved

16 files. Their lawful home is internal-corpus source houses (provenance of thinking, not
public warrant); disposition left to Frank.

- `Methodological Aside.md` — short methodological note: long-excerpt "integral stenography" as the project's way of philosophising through faithful re-contextualisation.
- `Mono-Poly — The Two Ones and the Whole Field.md` — authorial paper developing mono-poly, the two ones and the whole field, as the nature of wholeness.
- `P0 - Jung and Pauli - Atom and Archetype.md` — page-by-page extraction notes on Jung/Pauli's *Atom and Archetype* (archetypes as ideas, Unus Mundus, the empty mandala centre).
- `P1 - Jorjani - Prometheus and Atlas.md` — extraction notes on Jorjani's *Prometheus and Atlas*: technoscience, the return of the gods, epi-logos as the after-word of philosophy.
- `P2 - Para Trisika Vivarana Notes - Abhinavagupta and Jaideva Singh - Introduction.md` — extraction notes on the Parātriśikā Vivaraṇa introduction (Kashmir Shaivism as culmination of the Logos movement; the 4th-that-is-the-3).
- `P3 - Beyond Para-Trisika.md` — authorial continuation beyond the Parātriśikā: com-prehension and concrescence, Antichrist qua technoscience as nascent Aquarian spirit.
- `P3.1 - Perennial Philosophy Excerpt.md` — Huxley *Perennial Philosophy* extract (ritual/white-magic passage) with mono-poly theism commentary.
- `P4 - Christ and Mono-Poly Theory.md` — authorial paper: Christ's symbolic monopolisation of Divine Sonship, the Paraclete, Sophia, and Anti-Christ as fossilised truth.
- `P5 - Gebser.md` — authorial paper on Gebser: perspective vs context, the 4th-person integral structure, the absent-Father logic of the mental-rational.
- `PN - Swedenborg - Divine Love and Wisdom.md` — extraction notes on Swedenborg's *Divine Love and Wisdom* (finite from infinite, pure motion as conatus-to-create).
- `Symbolon Dynamics — Archetype, Attractor, and Objective Internality.md` — authorial paper on archetype/attractor dynamics and objective internality.
- `The Advent of Zero — Subject, Psyche, and Integral Logic.md` — authorial paper: subject, psyche and integral logic, the advent of Zero.
- `source-extraction-argument-audit.md` — source-extraction and argument-wiring audit across the write-ups.
- `source-extraction-core-theorems.md` — source-extraction ledger for the core theorems and the write-ups.
- `source-extraction-definition-god-draft3.md` — source extraction for the Definition of God, draft 3.
- `source-extraction-fable-chat.md` — internal passage ledger from the fable chat of 12 July 2026.

## Skipped / unreadable / anomalies

- No unreadable or binary files encountered; all sources were valid UTF-8/ASCII text.
- `_index/notion-harvest-manifest.md` not deposited — path correction and rationale above.
- No name collisions, hence no origin-slug prefixes; slugified filenames listed above.
- No content fabricated: where the ticket's description and the source differed (poems.js
  explications; manifest location), the source as found governs and the difference is recorded.
