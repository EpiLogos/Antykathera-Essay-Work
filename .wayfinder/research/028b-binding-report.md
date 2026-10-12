# 028b — Vault binding pass report (2026-09-25)

Contract: every `.md` under `submission-package/essay/` binds exactly once in the aikit
wiki ingest, and every page has a visible link-path to the section movements. Deposited
content verbatim; only frontmatter and intake/return furniture added.

## 1. Files bound (Task 1) — 190 rewritten + 2 new index pages

Probe used: `aikit --json wiki ingest --file <tmp>/wiki.json --room-depth 2 --apply
submission-package/essay`, corpus shards diffed against all vault `.md`. Before: 820
bound / 190 unbound / 1010 files. After: **1012 bound = 1012 files** (1010 + 2 new
pages; `poetry/README.md` already existed), `skipped_unaddressable 0`,
`duplicate_record_id 0`, `duplicate_source_id 0`, `unparseable 0`.

| folder | bound | treatment |
|---|---|---|
| `symbolon/mytheme/poetry/` | 95 | 79 had an HTML-comment provenance envelope above original Notion frontmatter: envelope folded into a single leading YAML block (`origin_path`, `retrieved`, `format`, `lifecycle`, `author`), original Notion keys preserved verbatim (incl. `tags:` byte-for-byte and the Notion `source_id:` UUID), binding `source_id:` slug appended last (aikit binds last occurrence; verified empirically). 16 were already YAML-first: `source_id:` appended into the existing block. |
| `symbolon/episteme/aphorisms/` | 24 | `source_id:` slug + `tags:\n  - epi-logos/antikythera-essay` added into the existing frontmatter block. |
| `quilt/final-argument-quilt-2026-08-23/` | 28 | 13 had partial frontmatter (`source_id:` added into it); 15 had none. |
| `quilt/final-argument-quilt-2026-08-23/inherited-corpus-crosswalk/` | 39 | all had no frontmatter: prepended `title` (from first `#` heading, YAML-quoted), `source_id`, `authority: working-ledger-only`. |
| `quilt/conjugate-field-proposals/` | 2 | `source_id:` added into existing frontmatter (the third file, `EROS-OF-LOGOS-A-CANDIDACY.md`, was already bound via `record_id: A-EROS-OF-LOGOS-CANDIDACY`). |
| `quilt/pre-manuscript-refinement-inputs/` | 2 | `source_id:` added into existing frontmatter (both declared `record_type:` without ids). |

All 71 quilt ledgers carry a `> intake:` line; all received a `> Return:` line directly
under it: `> Return: [section rooms](../../section-rooms/README.md)` (one level deep) /
`../../../section-rooms/README.md` (`inherited-corpus-crosswalk/`, and `poetry/`,
`aphorisms/` — three levels). The 95 poems and 24 aphorisms each received one closing
`> Return: [section rooms](...)` line (the allowed one intake/return line per file),
which is what gives every deposited page an outgoing visible path into the movements
via `section-rooms/README.md`.

### source_id slugs

- Scheme: kebab-case of the filename stem; quilt UPPER names lower-cased.
- One collision avoided: `inherited-corpus-crosswalk/INDEX.md` would have taken
  `index` (already an id in the vault) → assigned `inherited-corpus-crosswalk-index`.
- Final sweep: 1091 distinct ids vault-wide, **no id on more than one file**; all 190
  assigned slugs verified present and unique.

## 2. Reachability (Task 2)

- `symbolon/mytheme/poetry/README.md` — **pre-existing canonical record restored, not
  replaced.** The first probe's shards carried the old file: it was a bound
  `register-domain` record (`record_id: mytheme-poetry`, `record_type: register-domain`,
  `register: mytheme`, `domain: poetry`) with authored prose. My initial write had
  overwritten it; the canonical frontmatter and prose were restored byte-for-byte from
  the probe shard and the per-file index (all 95 poems, grouped: Notion harvest 2024 —
  27 `collection:gaia-2024`; Notion harvest 2025 — 52 `collection:jan-feb-2025`; Nara
  journal — 8; site poems P0–P5 — 6; vault-root pieces — 2) appended to it, with a
  `> Return:` section-rooms line. **Deviation from the task text:** its record_id stays
  `mytheme-poetry` rather than `register-mytheme-poetry-index` — one file, one identity;
  the existing canonical id wins over the instruction's provisional id. Reachability was
  already served by `mytheme/README.md` line 72 (`[Poetry](poetry/README.md)`).
- `symbolon/episteme/aphorisms/README.md` — created; `record_id:
  register-episteme-aphorisms-index`, `record_type: register-index`, `register:
  episteme`; links *Investigation and Faith* (register entrance, unchanged) + all 24
  site-copy blocks grouped by origin file (23 + 1). `symbolon/episteme/README.md`'s
  Aphorisms line now links the index and keeps `investigation-and-faith.md` linked.
- `quilt/README.md` — created; `record_id: register-quilt-index`, `record_type:
  register-index`; links the six pre-existing top-level surfaces and all 72 absorbed
  ledger files grouped by subfolder. `submission-package/essay/README.md` gained one
  line in "The publication 4+2" pointing to it (nothing removed).

## 3. Verification tails

1. Ingest probe: `files_read 1012`, bound set == file set (no unbound, no phantom),
   `skipped_unaddressable 0`, `duplicate_record_id 0`, `duplicate_source_id 0`,
   `unparseable 0`, `tag_vocabulary 210`.
2. `tools/build-navigation.py` (62 surfaces) + `tools/audit-reader-navigation.py
   --output working/reader-navigation-audit-2026-09-25.json`:
   - pages 953 (1012 minus 59 generated `maps/navigation/` pages), reachable 890,
     admitted 288, missing_admitted 0, unreachable_admitted 0.
   - `unreachable` 63 and `no_visible_path_to_movement` 78 — **every entry is the
     pre-existing `section-rooms/arguments/concepts/reference-notes/` area**; none of
     today's 193 touched files appears in either tail.
   - problems tail: directory-link 6, title-or-alias-only 294, missing-vault-path 77,
     missing-fragment 9, ambiguous-filename 11 — pre-existing debts (alias-only links
     are declared portability debt; reference-notes is excluded from the link test).
3. `python3 -m unittest tests.test_aikit_wiki_parity tests.test_pre_manuscript_gate
   tests.test_submission_package` — **24/24 pass.**

## 4. Repairs beyond pure addition (each the specific cause of a failing gate)

- `quilt/final-argument-quilt-2026-08-23/OUGHT-BE-APHORISM-ARCHITECTURE.md` line 14:
  same-dir link `APHORISM-AND-PITHY-FORMULATION-LEDGER.md#…` dangled because that ledger
  was retired today to
  `working/_to_delete/2026-09-25-retire/final-argument-quilt-2026-08-23-signal-and-review/`.
  Href repointed to the ledger's actual location (makes `test_essay_body_wikilinks_and_relative_links_resolve`
  pass; audit now records it as outside-body, not missing). Wording untouched.
- `quilt/final-argument-quilt-2026-08-23/THREAD-INTAKE-002-…TECHNICAL-INTELLIGENCE.md`:
  three frontmatter `up:`/`related:` wikilinks and one body wikilink still pointed at
  the old `working/final-argument-quilt-2026-08-23/` location of files that were
  deposited into the vault; repathed to their new vault homes.
- `submission-package/essay/README.md`: restored the missing manuscript-status
  statement "The continuous manuscript awaits composition" to the manuscript paragraph,
  per `tests/test_pre_manuscript_gate.py::test_reader_entrance_contains_only_working_visible_destinations`,
  the repo README and the T24 receipt, which all state the reading root carries it.

## 5. Named debts (pre-existing or from today's retirement step, not this pass)

- `tools/build-section-rooms.py --check` reports `section-rooms/README.md` stale: the
  builder's generated text is plainer than the current richer hand-authored page ("The
  Return of Zero — The Rooms…"). Either the builder must be updated to emit the authored
  page or the page re-generated; rebuilding as-is would overwrite authored prose, so it
  was left untouched. Its sources (manuscript, section-rooms) were not modified by this
  pass. Not part of the three verify gates, which all pass.
- `tools/audit-pre-manuscript.py --output …` crashes: today's retirement moved
  `working/p2-enrichment/audits/T22-K-E-consumer-pairs-2026-09-08/proof.json` into
  `working/_to_delete/2026-09-25-retire/`. The tool is not among the three verify test
  modules.
- ~70 remaining `working/final-argument-quilt-2026-08-23/…` mentions inside deposited
  ledger bodies are prose/provenance references (most targets still exist under
  `working/`); only the two gate-breaking pointers above were repaired.
- Poems' Notion `source_id:` UUID keys are preserved verbatim per the binding rule; the
  binding slug is the last `source_id:` occurrence in those blocks (aikit and PyYAML
  both take the last).
