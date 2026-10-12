# Ticket 040 — Type-prefix rename sweep (report)

Date: 2026-09-25. Assignee: rename-agent-2026-09-25.
Convention applied (Frank, ratified): TYPE as prefix, qualified by the immediate parent slug —
`ROOM-<room-slug>.md`, `HISTORY-<parent-slug>.md`, `READING-<parent-slug>.md`,
`WHOLE-FIELD-<parent-slug>.md`, `HISTORICAL-BRANCHES-<parent-slug>.md`, `DEVELOPMENT-<parent-slug>.md`.
No git commands were used; every rename was a plain `mv`. Nothing was committed.

## 1. Census (re-verified before work)

ROOM 8, READING 2, HISTORY 18, WHOLE-FIELD 7, HISTORICAL-BRANCHES 6, DEVELOPMENT 10 — 51 files, matching the ticket.

## 2. Full old→new table (all 51 files)

All under `submission-package/essay/`. Old name in each row is the pre-rename basename in that folder.

| Old | New | Folder |
|---|---|---|
| `READING.md` | `READING-00-integral-threshold.md` | `section-rooms/00-integral-threshold/` |
| `ROOM.md` | `ROOM-00-integral-threshold.md` | `section-rooms/00-integral-threshold/` |
| `ROOM.md` | `ROOM-01-differentiating-mind.md` | `section-rooms/01-differentiating-mind/` |
| `READING.md` | `READING-02-return-of-zero.md` | `section-rooms/02-return-of-zero/` |
| `ROOM.md` | `ROOM-02-return-of-zero.md` | `section-rooms/02-return-of-zero/` |
| `ROOM.md` | `ROOM-03-two-logics.md` | `section-rooms/03-two-logics/` |
| `ROOM.md` | `ROOM-04-mathematical-substrate.md` | `section-rooms/04-mathematical-substrate/` |
| `ROOM.md` | `ROOM-05-psychoid-flowering.md` | `section-rooms/05-psychoid-flowering/` |
| `ROOM.md` | `ROOM-06-objective-internality.md` | `section-rooms/06-objective-internality/` |
| `ROOM.md` | `ROOM-07-instrument-returns.md` | `section-rooms/07-instrument-returns/` |
| `HISTORICAL-BRANCHES.md` | `HISTORICAL-BRANCHES-apportionment-and-economy.md` | `symbolon/episteme/etymologies/apportionment-and-economy/` |
| `HISTORY.md` | `HISTORY-apportionment-and-economy.md` | `symbolon/episteme/etymologies/apportionment-and-economy/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-apportionment-and-economy.md` | `symbolon/episteme/etymologies/apportionment-and-economy/` |
| `HISTORICAL-BRANCHES.md` | `HISTORICAL-BRANCHES-arbitration-hybris-regard-anamnesis.md` | `symbolon/episteme/etymologies/arbitration-hybris-regard-anamnesis/` |
| `HISTORY.md` | `HISTORY-arbitration-hybris-regard-anamnesis.md` | `symbolon/episteme/etymologies/arbitration-hybris-regard-anamnesis/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-arbitration-hybris-regard-anamnesis.md` | `symbolon/episteme/etymologies/arbitration-hybris-regard-anamnesis/` |
| `HISTORY.md` | `HISTORY-earth-taste-wisdom.md` | `symbolon/episteme/etymologies/earth-taste-wisdom/` |
| `HISTORICAL-BRANCHES.md` | `HISTORICAL-BRANCHES-encounter-region-name-count.md` | `symbolon/episteme/etymologies/encounter-region-name-count/` |
| `HISTORY.md` | `HISTORY-encounter-region-name-count.md` | `symbolon/episteme/etymologies/encounter-region-name-count/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-encounter-region-name-count.md` | `symbolon/episteme/etymologies/encounter-region-name-count/` |
| `HISTORY.md` | `HISTORY-genesis-paradigm-project-epilogos.md` | `symbolon/episteme/etymologies/genesis-paradigm-project-epilogos/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-genesis-paradigm-project-epilogos.md` | `symbolon/episteme/etymologies/genesis-paradigm-project-epilogos/` |
| `HISTORICAL-BRANCHES.md` | `HISTORICAL-BRANCHES-homology-and-analogy.md` | `symbolon/episteme/etymologies/homology-and-analogy/` |
| `HISTORY.md` | `HISTORY-homology-and-analogy.md` | `symbolon/episteme/etymologies/homology-and-analogy/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-homology-and-analogy.md` | `symbolon/episteme/etymologies/homology-and-analogy/` |
| `HISTORICAL-BRANCHES.md` | `HISTORICAL-BRANCHES-symbol-account-and-trust.md` | `symbolon/episteme/etymologies/symbol-account-and-trust/` |
| `HISTORY.md` | `HISTORY-symbol-account-and-trust.md` | `symbolon/episteme/etymologies/symbol-account-and-trust/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-symbol-account-and-trust.md` | `symbolon/episteme/etymologies/symbol-account-and-trust/` |
| `HISTORICAL-BRANCHES.md` | `HISTORICAL-BRANCHES-trust-place-logos-nomos-natio-credere.md` | `symbolon/episteme/etymologies/trust-place-logos-nomos-natio-credere/` |
| `HISTORY.md` | `HISTORY-trust-place-logos-nomos-natio-credere.md` | `symbolon/episteme/etymologies/trust-place-logos-nomos-natio-credere/` |
| `WHOLE-FIELD.md` | `WHOLE-FIELD-trust-place-logos-nomos-natio-credere.md` | `symbolon/episteme/etymologies/trust-place-logos-nomos-natio-credere/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-myth.md` | `symbolon/episteme/histories/encounters-and-transmissions/myth/` |
| `HISTORY.md` | `HISTORY-myth.md` | `symbolon/episteme/histories/encounters-and-transmissions/myth/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-language-law-nation-centralisation.md` | `symbolon/episteme/histories/places-and-peoples/language-law-nation-centralisation/` |
| `HISTORY.md` | `HISTORY-language-law-nation-centralisation.md` | `symbolon/episteme/histories/places-and-peoples/language-law-nation-centralisation/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-ancient-philosophy.md` | `symbolon/episteme/histories/traditions-and-disciplines/ancient-philosophy/` |
| `HISTORY.md` | `HISTORY-ancient-philosophy.md` | `symbolon/episteme/histories/traditions-and-disciplines/ancient-philosophy/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-indian-philosophy.md` | `symbolon/episteme/histories/traditions-and-disciplines/indian-philosophy/` |
| `HISTORY.md` | `HISTORY-indian-philosophy.md` | `symbolon/episteme/histories/traditions-and-disciplines/indian-philosophy/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-language-symbol-dialogue.md` | `symbolon/episteme/histories/traditions-and-disciplines/language-symbol-dialogue/` |
| `HISTORY.md` | `HISTORY-language-symbol-dialogue.md` | `symbolon/episteme/histories/traditions-and-disciplines/language-symbol-dialogue/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-mathematics.md` | `symbolon/episteme/histories/traditions-and-disciplines/mathematics/` |
| `HISTORY.md` | `HISTORY-mathematics.md` | `symbolon/episteme/histories/traditions-and-disciplines/mathematics/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-process-systems-science.md` | `symbolon/episteme/histories/traditions-and-disciplines/process-systems-science/` |
| `HISTORY.md` | `HISTORY-process-systems-science.md` | `symbolon/episteme/histories/traditions-and-disciplines/process-systems-science/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-psychology.md` | `symbolon/episteme/histories/traditions-and-disciplines/psychology/` |
| `HISTORY.md` | `HISTORY-psychology.md` | `symbolon/episteme/histories/traditions-and-disciplines/psychology/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-technology-politics.md` | `symbolon/episteme/histories/traditions-and-disciplines/technology-politics/` |
| `HISTORY.md` | `HISTORY-technology-politics.md` | `symbolon/episteme/histories/traditions-and-disciplines/technology-politics/` |
| `DEVELOPMENT.md` | `DEVELOPMENT-zero-subject-advent.md` | `symbolon/episteme/histories/traditions-and-disciplines/zero-subject-advent/` |
| `HISTORY.md` | `HISTORY-zero-subject-advent.md` | `symbolon/episteme/histories/traditions-and-disciplines/zero-subject-advent/` |

## 3. Inbound-link sweep under `submission-package/essay`

Resolution semantics confirmed from `tools/audit-reader-navigation.py`: markdown links resolve
file-relative; wikilinks with `/` resolve vault-root-relative; bare wikilinks resolve by unique
basename. A repo-wide sweep found **zero bare wikilinks** to the six names (so no ambiguity
decisions were needed).

One sweep script repointed targets in all three forms (relative path links, absolute GitHub-URL
links as used in manuscript footnotes, and vault-path wikilinks), replacing only the final
basename with `TYPE-<resolved-parent-slug>.md` and preserving fragment/alias parts:

| Form | Occurrences repointed |
|---|---|
| `ROOM` | 587 |
| `READING` | 75 |
| `HISTORY` | 652 |
| `WHOLE-FIELD` | 1186 |
| `HISTORICAL-BRANCHES` | 255 |
| `DEVELOPMENT` | 696 |
| **Total** | **3451 occurrences across 349 files** |

Post-sweep verification: zero remaining path links or vault-wikilinks to the six old basenames
under the essay body.

## 4. Tools updated (reference class → count of edit sites)

| Tool | Sites | What changed |
|---|---|---|
| `tools/build-section-rooms.py` | 12 | `ROOM_FILE` constant replaced by `room_file(slug)` / `reading_file(slug)` helpers; `validate_links` default page; prev/next room links; reading-route link in room page; word-count error message; rooms-README table + reading-route link + start-here link; the two "What a room contains" prose bullets; build/check write paths; docstring. Generator then rebuilt all output — no generated file was hand-edited. |
| `tools/build-navigation.py` | 1 | `is_return_target` recognises `section-rooms/**/ROOM-*.md` (type prefix + `.md`) instead of `endswith("/ROOM.md")`. |
| `tools/build-source-projections.py` | 1 | `MAIN-SOURCES.md` "Open section room" link emits `ROOM-<room>.md`. |
| `tools/audit-room-depth.py` | 20 | `ALLOWED` set replaced by per-room `allowed_files(slug)` / `room_page(slug)` / `reading_page(slug)`; required-file check; room-page read and its 6 message strings; threshold-reading path and its 11 message strings (messages now carry the actual filename, keeping the asserted substrings intact). |
| `tools/okf-workspace.py` | 2 | `primary_id` room rule (`ROOM-*.md` → `room-<parent>` identity preserved); `dangling-room-link` debt scope (`ROOM-*.md` / `READING-*.md`). |
| `tools/audit-pre-manuscript.py` | 2 | (a) `home2026` now also translates recorded pre-rename basenames (`HISTORY.md` → `HISTORY-<parent>.md` etc.), mirroring the function's existing 2026-09-25 migration translations and its `NOTES.md → <parent>-NOTES.md` fallback; (b) the T24 protected-baseline exemption accepts the new `TYPE-<parent>.md` names alongside the old ones and applies the same translation, so preserved bytes still verify as preserved. |

## 5. Tests and fixture updated

| File | Sites | Change |
|---|---|---|
| `tests/test_build_section_rooms.py` | 8 | Expected room file name per slug; room-file set membership; manuscript link assertion now `section-rooms/{slug}/ROOM-{slug}.md` (same contract, new filename, per known collision #3); `READING-*` globs and copy paths. |
| `tests/test_learning_surfaces.py` | 6 | `THRESHOLD_READING` / `ZERO_READING` / `ZERO_ROOM` paths; routes glob; manuscript link assertion; `[reading route](READING-02-return-of-zero.md)` assertion. |
| `tests/test_audit_room_depth.py` | 2 | Tamper-target paths for room page and threshold reading page. |
| `tests/test_okf_workspace.py` | 1 | Kaplan backlink source path. |
| `tests/test_submission_package.py` | 2 | `glob("*/ROOM-*.md") == 8`; link-debt exemption now `path.name.startswith("HISTORY-")` (same protected/provenance semantics, new name form). |
| `tests/test_skill_contracts.py` | 2 | Required skill-doc strings updated to `ROOM-<room-slug>.md` / `READING-<room-slug>.md` / `` generated `ROOM-<room-slug>.md` `` (matching the skill-doc text updates below). |
| `tests/fixtures/retired-bkmr-coverage.json` | 10 paths | 8 ROOM + 2 READING paths repointed to the new names (locator record; carrier unchanged), keeping the 884-path parity contract true against a live ingest. |

**Not changed, deliberately:** `tests/test_pre_manuscript_gate.py`. Its dead-end exemption set
still names `HISTORY.md`/`READING.md`, which are now inert entries (no file carries those names).
Per instruction the test's semantics were not touched; instead the gate was re-run and verified
(see §7): no renamed page is a dead end, so the vanishing name exemption is moot. Flagging the
inert entries here as an observation for a later tidy-up.

## 6. Other live-surface mentions updated (mechanical)

- `.agents/skills/return-of-zero-write/SKILL.md` (1), `return-of-zero-review/SKILL.md` (1),
  `return-of-zero-orient/references/workspace-contract.md` (3) — new name forms in the surface
  contracts (`.claude/skills/` are symlinks to these).
- `AGENTS.md` (2), `CLAUDE.md` (3, live-description lines only; the dated T23 history entry was
  left as provenance), `docs/REPOSITORY-SHAPE.md` (2).
- `working/pre-manuscript-refinement-2026-09-10/T25-current-census-acceptance.json` — the 16
  `canonical_home` rows pointing at renamed files (10 `HISTORY.md`, 6 `WHOLE-FIELD.md`) were
  repointed (path-only locator repair; recorded T25 sha256 values untouched, consistent with the
  receipt's standing drift-disclosure role). This receipt is load-bearing: `ReaderAudit` asserts
  every admitted record `exists` and is reader-reachable.
- `working/p2-enrichment/census.json` (23 recorded paths: 17 `HISTORY.md`, 6 `WHOLE-FIELD.md`) and
  `working/p2-enrichment/dispatch-queue.json` (469 recorded `path` occurrences: 399 `WHOLE-FIELD.md`,
  70 `HISTORY.md`) — live shelves of the p2 build workflow, whose CLI validates every recorded path
  against the filesystem (`workflow.py`: "Input is not a file inside the project"). All recorded
  locators were repointed to the renamed carriers, and the queue's `census_sha256` binding was
  recomputed against the repaired census (the queue is the only live binder of census bytes;
  `depth_acceptance_sha256` binds a file this ticket did not touch). Before this repair the two
  `tests.test_p2_build_workflow` manifest-binding tests failed with the stale-path error; both pass
  after it.
- `submission-package/essay/quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md` — 4 stale filename
  mentions in code-span/path text (a room page in a "Canonical field" reading list, a history bank
  in a "Read in full" list, and two `path="…"` attributes in an embedded record block). These are
  not links and did not resolve, so the link sweep correctly skipped them; they were repaired as
  stale live-surface references (basename-only, no prose touched).

Working ledgers under `working/` (T21/T22/T24 snapshots, historical reports) and `.wayfinder/`
day ledgers were left untouched as provenance. `.obsidian/` config left app-managed.

## 7. Gate / dead-end check (known collision #6)

`no_visible_path_to_movement` diffed before vs after rename: **identical lists** (69 entries, no
additions, no removals). None of the 51 renamed pages is a dead end, so **no return-route lines
were needed** and the gate test's exemption semantics were preserved untouched. Reader-audit
problem profile is byte-identical before/after: `directory-link 6, title-or-alias-only 281,
missing-fragment 10, missing-vault-path 67, ambiguous-filename 2` — the sweep introduced no
unresolved link; reachable stayed 952/956; `missing_admitted`/`unreachable_admitted` returned to
0 after the receipt repair.

## 8. Builder / audit outcomes

- `tools/build-section-rooms.py --project-root .` — Built 8 room(s); `--check` — fresh.
  (This rebuild also absorbed three rooms that were already stale before this ticket started —
  01, 04, 05 — from earlier canonical work today.)
- `tools/build-source-projections.py --project-root . --check` — "Source projections current: 3 files."
- `tools/build-navigation.py --project-root . --check` — "navigation layer fresh: 62 generated surfaces"
  (rebuild: 956/956 pages reachable, 0 orphans).
- `tools/audit-room-depth.py --project-root .` — PASS ×8, exit 0.
- `tools/audit-reader-navigation.py --project-root . --output working/reader-navigation-audit-2026-09-25.json`
  — problems identical to pre-ticket profile, `missing_admitted: 0`.

## 9. Stopped / named items (not hacked)

1. **`tools/audit-pre-manuscript.py` crashes on the lens homing (pre-existing, not ticket 040).**
   The gate's T22 route-check stage reads `symbolon/episteme/lenses/baudrillard.md` and
   `.../foucault.md`, which were homed into their source houses on 2026-09-25 by the lens-homing
   migration (documented in `symbolon/episteme/lenses/README.md`); the recorded T22 source paths
   were never translated, so the gate tool breaks independently of the rename. Repairing it means
   mapping the two old lens paths to their new source-house homes in `home2026` — the lens-homing
   ticket's debt. No test or hook invokes `audit-pre-manuscript.py` (`tests/` and
   `.codex/hooks/return_zero_hook.py` verified), so the suite acceptance is unaffected. Ticket
   040's own `home2026` extension (recorded `HISTORY.md`-style paths → renamed carriers) is in
   and works.

2. **Sovereign manuscript is mid-composition by a concurrent writing ticket (pre-existing in the
   baseline run).** `test_master_manuscript_is_the_only_active_writing_surface` asserts eight
   `## §` headings; the manuscript currently carries six — the anchors `section-s01` (§0/1) and
   `section-s50` (§5→0) have no `## §` heading at present, i.e. those two sections are being
   rewritten concurrently. This failure appears identically in the pre-ticket baseline run
   (17 failures there), involves no renamed name, and is the writer ticket's live surface; the
   rename sweep does not touch prose. Not repaired here by design.

3. **Quilt-hash staleness in `working/p2-enrichment/receipts/depth-acceptance.json` (pre-existing).**
   All six pinned quilt hashes are already stale against current quilt bytes — earlier tickets
   edited quilt files today without refreshing the acceptance record. Ticket 040's only quilt edit
   (the four filename mentions above) did not change this standing: the binding was stale before
   and after. The `tests.test_p2_build_workflow` tests recompute quilt hashes in their setup and
   pass regardless. Refreshing the acceptance record belongs to whoever owns the quilt edits.

## 10. Suite tail (verbatim)

Captured from `python3 -m unittest discover -s tests -v` after all changes — see the verbatim
block appended below (final run). Baseline note: the same suite was already red before this
ticket (17 failures, dominated by the concurrent manuscript composition and other tickets' work
today). Ticket-040-attributable failures (the two p2 manifest-binding tests, via stale recorded
paths) were repaired and pass; all remaining failures, if any, are the named pre-existing items
in §9.

Final run: **123 tests, 1 failure** — `test_master_manuscript_is_the_only_active_writing_surface`
only (manuscript mid-composition by the concurrent writer, §9.2; 6 `## §` headings at run time,
failed identically in the pre-ticket baseline). All 122 other tests pass.

```
----------------------------------------------------------------------
Ran 123 tests in 391.394s

FAILED (failures=1)
exit=1
```

---

*Report generated by ticket 040 execution, 2026-09-25.*
