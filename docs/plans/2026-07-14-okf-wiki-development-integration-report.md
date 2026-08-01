# OKF Wiki Development Integration — Execution Report (2026-07-14, late evening)

Companion to `2026-07-14-okf-wiki-development-integration.md`. Execution ran across two threads: the main session (Tasks 1–4 before its restart; Tasks 5, 7, 8 and the room-redesign closeout after) and Frank's concurrent Sol/Luna rebuild, which re-architected the developer skill surface while this report's work was in flight. Everything below states what is verified on disk, with the exact evidence.

## Task status

1. **Isolate from the installed S5 skill set — done.** `Antykathera-Essay-Work/AGENTS.md` declares authority order, wiki-first entry, the five independent status axes, and the `epi-logos-voice` prohibition. `~/Documents/Nara-Personal/.codex/config.toml` disables every installed S5 Epi-Logos skill and parses (`tomllib` check passes).
2. **Real failing wiki tests — done.** `tests/test_okf_workspace.py`, `tests/test_bkmr_essay.py` exercise the real workspace (no mocked nodes); `tests/test_skill_contracts.py` (from the Sol/Luna rebuild) gates the skill locations and wiring.
3. **Read-only workspace graph crawler — done.** `tools/okf-workspace.py`: `status · find · open · links · backlinks · neighbourhood · path · trace · context · doctor`, all with `--json`; ~453 typed artifacts across 17 types and 13 authority classes. Two fixes landed tonight: the quality assessor no longer discards the first heading of nodes without an H1 (it skips only a true title heading), and `transition-surface` now also accepts an explicit link to the next movement in sequence (note 13's real transition had been flagged as missing).
4. **BKMR indexes the authored intelligence — done.** Six collections (`records · passages · arguments · sections · concepts · rooms`) generated from full authored bodies and canonical quote dossiers; staleness refusal verified live (a stale `sections` collection refused to search until synced). All six report **fresh** as of this report.
5. **`okf-wiki` rewrite — done, re-architected.** The operative developer skill lives at the workspace skill root: `~/Documents/Nara-Personal/.agents/skills/okf-wiki/SKILL.md` (Frank's rebuild), with `.agents/skills/return-of-zero-writing/` as the prose skill. The submission-package `okf-wiki` was rewritten as the shipped statement of the same protocol: stale schemas removed (void A/B/C tiers, `reference-notes/` as a live layer, the hard `using-epi-logos` gate), the REPL loop (orient → find → open → expand → trace → assemble → verify → act) and trace-before-drafting rule documented, the five independent axes and live source-bank states taught, and the development register explicitly deferring to the workspace-root skill. `references/okf-format.md` now teaches the live workspace schema (artifact types, authority classes, source-bank states, evidential relations); `references/okf-scan.py` is retired to a foreign-bundle fallback. Command-level pressure scenarios ran against the real workspace: `find` (canonical-full-body), `open` by title alias, `trace 38-s5-p1-apoha-softmax` → `records/vaswani-et-al-2017-attention.md`, `path 25 → 30`, `context 21 --depth 1` — all correct; one invented example caught and corrected during validation.
6. **Sol/Luna rewired through the wiki — done by Frank's concurrent rebuild.** Both skills point at `../.agents/skills/okf-wiki`, the `epi-logos-voice` dependency is gone, and Sol routes authored prose through `return-of-zero-writing`; `tests/test_skill_contracts.py` (4 tests) verifies all of it. **A review pass on the redone Sol/Luna skills is owed when Frank calls for it** — including applying the room-redesign proposal's rubric items (Teaching axis hard-gated at 2, teaching-first dossier duties, orienting-principles pre-load) if the rebuild has not already absorbed them, then re-deepening room 00 under the new spec (redesign migration steps 3–4).
7. **Doctor-driven node repairs — done within the invention boundary.** Eight governance/record files gained the exact title aliases their inbound links use (wave reports, consumption matrix, intake queue, resolution register; Atmanspacher, Smythe, Courtney, Nietzsche records) — 17 unresolved links cleared. Remaining doctor output is honest debt, not noise (below).
8. **Integration blockers + system verification — done.** Details below.

## Quote-state repairs (Task 8.1 — at the authoritative source)

The ledger (the public-quotation gate) is now aligned with the quote dossiers that certify it:

- **Le Bon** rows re-IDed `…-lb-01/02/03` in dossier order (was `q001–q003` with swapped fragments) — the named blocker.
- **Desmet** rows → `…-md-01/02/03`; **Jung** rows → `…-jus-02/03/04` (dossier JUS-01 is paraphrase-only — no blockquote — and stays correctly ungated). Same rule applied everywhere: ledger row IDs match dossier passage IDs.
- **Vaswani q001–q004 restored to the ledger.** The dossier is Luna-verified quotation-ready (2026-07-14, official NeurIPS PDF, full locators) and the record is citation-ready, but the gate had lost its rows — room 06 showed "no verified passages" despite verified transcriptions. Rows restored from the dossier evidence; room 06 carries its verified passages again.

Old-style IDs survived nowhere outside regenerable projections (rooms rebuilt; adapters regenerated).

## Test-fixture repairs (Task 8.2)

`test_build_section_rooms.py` and `test_audit_room_depth.py` fixtures now copy `source-bank/quotes/` (the live transcription layout the builder's fallback reads — its absence was failing every builder-invoking test). Assertions updated from pre-redesign semantics to the accepted room redesign: 20-/30- surfaces are asserted absent on first build and seeded via `--seed-surface`; the dossier is asserted linked, not embedded; the verified-quote check now covers both transcription layouts (vaswani via old intake file, le-bon via dossier fallback) instead of a two-ID whitelist; the depth-audit helper seeds the editorial surfaces before marking a room deepened.

## Verification evidence (Task 8.3)

- **Full suite: 36/36 OK** (`unittest discover -s tests`): builder 10, depth-audit 5, okf-workspace 10, bkmr 7, skill contracts 4.
- **`build-section-rooms.py --check`: passes** on all eight rooms (slug gate, locked-expression gate, staleness gate); movements 1–48 uniquely assigned; protected surfaces preserved.
- **`bkmr-essay status`: all six collections fresh**; FTS spot-check (`epogdoon` → section 26) correct.
- **`okf-scan.py`** (foreign-bundle fallback) still runs over `essay-workshop/nodes` (85 nodes).
- **`.codex/config.toml` parses.**
- **End-to-end crawl:** `context 21-s2-p2-sym-ballein --depth 1 --json` assembles a ~27 KB traceable context with canonical paths and statuses.

## Remaining canonical content debts (named, not filled)

- **Doctor, unresolved links (5):** all in the central plan, all to targets outside the crawler's markdown scope — `essay-argument-map` (.canvas), `refs-sources-args.base`, `Antikythera Essay Structure Legacy` (excluded legacy), `The Self Proving Self_ Exposition` (monorepo), `sym-dia-ballein-views` (root-level HTML). The plan is sovereign; these are resolver-scope reports, not defects.
- **Doctor, thin quality surfaces:** 16 sections/arguments with no explicit tension/counterpressure heading (their tension rides in prose — e.g. note 10's "apoha becomes amnesia"), note 23's warrant under its "Apollo–Dionysus safeguard" heading, and `dimensional-reframing-at-zero-and-infinity` with no source-record anchor (its *khahara* wording is explicitly flagged verification work). Content-level; writing them would be inventing argument — they stay named.
- **Intake:** Schopenhauer/Kastrup/Śaiva records for note 47 (queued); a live home for cymatics; note 19's Śrīharṣa body wiring at the section pass (dossier passage already names note 19 as consumer).
- **Room 00 content debts** (Trika analysis, paradox-hinge paragraph, Gebser's atmosphere, immutable gap in the dossier/scholarly surfaces): land with the re-deepening under the redone Sol skill.

## Handoffs

1. **Sol/Luna review pass** when Frank calls it: verify the rebuilt skills against the redesign proposal's items 6–8 and the orienting principles, then re-run the room-00 deepening (migration steps 3–4) and validate against the 2026-07-14 audit findings.
2. **Source intake families** remain per the audit and queue.
3. The two okf-wiki statements (workspace-root operative, submission-package shipped) intentionally describe one protocol — if the crawl's CLI changes, update both.
