# 033 — Figures production II: mytheme plates — report

Date: 2026-09-25 · Assignee: plates-agent-2026-09-25 · Status: complete (5 plates landed)

## What was produced

The first real plate set in `submission-package/essay/symbolon/mytheme/plates/` — five
record + asset pairs. All assets are original programmatic SVG (Python-generated vector
geometry, rendered and visually verified at 900 px); rights for every plate: original
own-work, no scanned, stock, scraped or third-party imagery of any kind. Each record carries
proposition, invariant, proof boundary, composition/reading order, ship-text caption carrying
the operation, alt text, repo-root-relative anchors, source dependencies, and a wiring list
(embedding deliberately NOT performed here).

| # | Record | Asset | Anchored movements / records |
|---|---|---|---|
| 1 | `crossed-zero-stroke-does-not-fill.md` (`mytheme-plate-crossed-zero-stroke-does-not-fill`, Offered) | `crossed-zero-stroke-does-not-fill.svg` | M16 `16-s1-p3-crossed-zero`; manuscript §1 "The crossed zero", §4 "The stroke becomes visible" |
| 2 | `two-nets-indra-hephaestus.md` (`mytheme-plate-two-nets-indra-hephaestus`, Argued) | `two-nets-indra-hephaestus.svg` | M22 `22-s2-p3-ares-aphrodite-harmonia`; WHOLEs `mytheme-indra-net`, `mytheme-ares-aphrodite-hephaestus-poseidon` |
| 3 | `mechanism-gearing-non-closure.md` (`mytheme-plate-mechanism-gearing-non-closure`, Offered, `human-amplified: yes` scope carried from the whole) | `mechanism-gearing-non-closure.svg` | M45 `45-s50-p2-antikythera-attunement`; WHOLE `mytheme-antikythera-attunement` |
| 4 | `psychoid-field-one-seam.md` (`mytheme-plate-psychoid-field-one-seam`, Argued) | `psychoid-field-one-seam.svg` | M31 `31-s4-p0-psychoid-problem`, M40 `40-s5-p3-preference-hidden-zero`; A16 `A16-Arche-Topos-as-Differential-Field` |
| 5 | `salem-sign-migration-field.md` (`mytheme-plate-salem-sign-migration-field`, Derived for the migration; Argued discipline from the dossier) | `salem-sign-migration-field.svg` | M13 `13-s1-p0-sign-migrates`; `episteme/dossiers/zero-reception.md` § #3 |

The two-nets plate carries the ticket's `0/1` vs `(-1)+/-(+1)` operation, drawn from
Movement 22's own text ("Indra's net as the image of `0/1` … Hephaestus's mesh figures
polarity arrested into `(-1)+/-(+1)`" — the "two technical destinies" phrasing itself lives
only in a retired `_to_delete` draft and was NOT treated as authority; the live movement
record is).

## Verification

- Frontmatter YAML parses for all five records; required keys present (title, record_id,
  record_type: plate, register: mytheme, domain: plates, claim_status, asset, rights,
  anchored_movements, anchored_records, essay_blocks, source_ids, status).
- All five SVGs parse as XML and were rendered (qlmanage) and visually inspected; layout
  collisions fixed in a second pass.
- Every frontmatter anchor resolves to an existing file at repo root; every body-relative
  link resolves from `plates/`.
- Each record names its asset; each asset has its record. No floating assets.
- No existing file edited; no git operations; no builders run; no suite runs.

## Wiring list (embedding NOT performed by this ticket)

1. Plate 1 → manuscript §1 "The crossed zero" (beside the movement's opening paragraph);
   room route `section-rooms/02-return-of-zero/` M16.
2. Plate 2 → manuscript §2 M22 "The net and the pledge"; room route
   `section-rooms/03-two-logics/` M22. Possible secondary display for A23.
3. Plate 3 → manuscript §5→0 M45 (beside the "different cycles into one readable
   arrangement" paragraph); room route `section-rooms/07-instrument-returns/` M45.
4. Plate 4 → manuscript §4 opening; room route `section-rooms/05-psychoid-flowering/` M31.
5. Plate 5 → manuscript §1 "A sign migrates between worlds" and/or dossier
   `zero-reception.md` § #3; room route `section-rooms/02-return-of-zero/` M13.
6. After wiring: `aikit wiki ingest` re-run so the five `record_id` records compile into the
   Wiki, and the generated navigation/source projections rebuilt with `--check` (the
   completion hook will hold until then).

## Legacy briefs resolved / left open

- `image-01-mechanism-gearing-as-non-closure` — resolved as an authored emblem. The brief's
  first ask (a documented reconstruction diagram) cannot be a mytheme plate: it is an
  evidential visualisation with rights-bearing imaging. Its caption demand (separate
  physical evidence from interpretive attunement) is carried by the plate's proof boundary
  and open frame. **Left open as an `episteme/figures/` task**: a rights-cleared
  reconstruction figure for the 2006/2021 studies.
- `image-04-salem-manuscript-field` — resolved by the brief's own fallback (typographic /
  structural treatment): the dossier records shelfmark, folio and collation as unverified,
  so no manuscript image can honestly exist; the codex is drawn as an empty dashed frame
  beside the recovered edition pointer. **Left open, and correctly so**: any facsimile plate
  waits for the dossier's source task to complete.
- `image-07-psychoid-artifact-field` — partially resolved. The plate takes the psychoid
  field itself (the brief's "no anthropomorphic AI imagery" discipline governs it). **Left
  open**: the softmax-distribution / preference-difference-gauge diagram is a formal or
  evidential visualisation and belongs in `matheme/diagrams/` or `episteme/figures/`, not
  here.
- `image-02-promissory-glyph-plate` — NOT resolved. The brief asks for a sparer object than
  plate 1: a bare typographic plate for `(0/1)/(1/0)` introduced without explanatory
  apparatus until its coda return. The crossed-zero plate performs a different operation
  (occlusion and recognition), so the brief remains open for a future minimal typographic
  asset. Named rather than silently absorbed.
- `image-09-unmarked-axle-and-comma` — NOT resolved (outside the ticket's candidate list).
  Its operation — "the ground is not another gear," via axle and a minimal comma mark —
  belongs to the legacy "Coda" section, which has no live counterpart in the current
  manuscript structure (the mechanism's live home is M45). If wanted, it should be re-briefed
  against M45/M48 before any asset exists.
- `image-03`, `image-05`, `image-06`, `image-08` — not in this ticket's scope (self-inquiry
  scene, Sheffer stroke, re-entry fork, 4+2 attunement stack); untouched.

## Status notes

- Plate claim statuses follow their anchored movements: M16 Offered, M22 Argued, M45
  Offered, M31 Argued, M13 Derived. No plate claims a quotation; no external text appears in
  any asset; the essay's own notation lines (`0 → Ø → …`, `0/1`, `(-1)+/-(+1)`) are the
  essay's internal corpus and are carried as such in the records.
- Plate 5's `human_amplification` marks the empty-frame emblem as the plate's own authored
  image awaiting Frank's encounter; its historical content stays inside M13 + dossier.
- Nothing canonical outside `mytheme/plates/` was changed; the generated projections are now
  stale by design until the wiring pass runs the builders.
