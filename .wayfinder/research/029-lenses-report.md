# Ticket 029 report — lenses register repair (2026-09-25)

Assignee: lenses-agent-2026-09-25. Scope held: no git, no builders, no test suite; edits only in `episteme/lenses/`, the two source houses and their consumption sections, plus repoint-only edits in nodes citing the two old lens files. `<source_id>-NOTES.md` files: none exist beside the affected houses; none created, none touched.

## 1. What was homed where

**Baudrillard.** The whole developed reading of the old `lenses/baudrillard.md` (record `lens-baudrillard`) is absorbed verbatim into the `baudrillard-1976-symbolic-exchange-death` house (`submission-package/essay/symbolon/episteme/sources/media-technology-philosophy/baudrillard/baudrillard-1976-symbolic-exchange-death/baudrillard-1976-symbolic-exchange-death.md`) as a new section **"Declared lens reading — Simulation and the Account's Return"** anchored `#baudrillard-lens-reading`, placed before "Superseded intake and retained research". Text unchanged apart from: headings demoted one level (movements `#0`–`#5→0` are now `###`), links re-based (own-house passage anchors `q001/q002/q003` now same-document), and an absorption note declaring the reading's status (`claim_status: Argued`; Paraphrased / Argued-from / Offered comparative extensions) and stating that A20/A24/A32/C27/C33/C38/C55 retain their native derivations. The house's "Essay uses" line now points at the in-house section. Influence stays a declared source relation: nothing presents Baudrillard as endorsing the essay's inference.

**Foucault.** The whole reading of the old `lenses/foucault.md` (record `lens-foucault`) is absorbed verbatim into `foucault-1976-history-sexuality-v1` (`.../sources/phenomenology-continental-philosophy/foucault/foucault-1976-history-sexuality-v1/foucault-1976-history-sexuality-v1.md`) as **"Declared lens reading — Knowledge, Power, and the Authority to Return"** anchored `#foucault-lens-reading`, before "Superseded intake claims and remaining source tasks". All six sublens anchors (`foucault-knowledge-object`, `-authorised-speech`, `-distributed-office`, `-scales-of-measure`, `-critique-return`, `-commission-return`) are preserved, so the house's five passage-card **Consumer** lines now point in-document (`#foucault-authorised-speech` etc.). The "Source scholarship and authorial relation" lens link points at the in-house section. The absorption note declares the reading's full status axes including its six `source_ids`.

House frontmatter: `consumed_by_lenses` set to `[]` in both houses (the consuming records are gone; the relation is now in-house material).

## 2. Links repointed (counts)

Body-link repoints, all verified resolving (0 broken relative links and 0 broken fragments across `lenses/`, `section-rooms/arguments/`, `etymologies/`, `sources/`):

- 9 path links to `lenses/baudrillard.md` → `baudrillard-1976-symbolic-exchange-death.md#baudrillard-lens-reading`: A20, A24, A32, C27, C33, C38, C55; symbol-account-and-trust WHOLE-FIELD + HISTORICAL-BRANCHES.
- 11 path links to `lenses/foucault.md#<fragment>` → `foucault-1976-history-sexuality-v1.md#<fragment>` (fragments preserved): A24, A25, A29, C27, C28, C29, C53; arbitration-hybris-regard-anamnesis WHOLE-FIELD + HISTORICAL-BRANCHES; trust-place-logos-nomos-natio-credere WHOLE-FIELD; apportionment-and-economy WHOLE-FIELD.
- In-house: 1 "Essay uses" link (baudrillard-1976), 1 scholarship link + 5 Consumer links (foucault-1976).
- 4 sibling Baudrillard houses (1977, 1981, 1983, 1990): their identical "This source **sources** the [Baudrillard lens](...)" body link now points to `../baudrillard-1976-symbolic-exchange-death/baudrillard-1976-symbolic-exchange-death.md#baudrillard-lens-reading`; their `consumed_by_lenses: [lens-baudrillard]` frontmatter entries set to `[]`.

Total: 32 canonical body-link instances repointed + 6 house frontmatter consumer entries cleared. **Judgment call named:** the four sibling houses' frontmatter `consumed_by_lenses` entries cited the retiring record by id, not by path; I removed them rather than leave a live declaration pointing at a nonexistent record. Alternative (leave frontmatter untouched for a later owner) was rejected because the ingest binds frontmatter declarations as-is.

## 3. Retire/replace decision per file

**Both retired** to `working/_to_delete/2026-09-25-retire/lenses-register/` (plain `mv`), with two manifest lines appended under a new "Lenses register repair 2026-09-25 (ticket 029)" heading in that batch's `MANIFEST.md`. Rationale: with the full readings now carried by their houses, keeping lens records would maintain a second home for the same text (divergence risk), and Frank's ratified direction is that the register come to hold the actual MEF lenses; every citing node was repointed to the houses regardless, so replaced records would have been unreferenced. **Alternative named for Frank:** keep each file as a compact source-linked lens record (frontmatter `source_ids`, body = pointer to the house section) if he wants the two readings to remain first-class register records alongside the MEF lenses.

## 4. The twelve MEF lens records

Built from the internal-corpus house `taylor-2026-mef-twelve-lenses` following **twelve files** (the house's own structure is §4's twelve integrated lens entries in three squares; it does not prescribe an index-plus-sections shape). Nothing is invented: each record carries the §4 entry of the house's recovered local object (`mef-12-lenses-sublens-reference.md`, 295 lines, 2026-06-22) — its SHA-256 was verified against the house's `local_copy_sha256` before use.

Files (naming follows the compilation; `′` = `prime` in filenames per repo convention, `′` in prose per the A01′/A05′ precedent):

- Square A — Articulation: `L0-quaternal.md`, `L0-prime-archetypal-numerical.md`, `L5-para-vak.md`, `L5-prime-divine-logos.md`
- Square B — Encounter: `L1-causal.md`, `L1-prime-phenomenal.md`, `L4-phenomenological.md`, `L4-prime-scientific.md`
- Square C — Becoming: `L2-logical.md`, `L2-prime-alchemical-elemental.md`, `L3-processual.md`, `L3-prime-chronological.md`

Each record: frontmatter `record_id: lens-L<n>-<slug>`, `record_type: lens`, `register: episteme`, `claim_status: Argued`, `source_relation: "Extracted from the internal-corpus house taylor-2026-mef-twelve-lenses ..."`, `source_ids: [taylor-2026-mef-twelve-lenses]`, `citation_status: internal-ready`, `quote_status: no-direct-quotation` (key set mirrors the neighbouring lens records); body carries the lens's square/face/index/tonic/ground-pair line, root/key-concept/element/Möbius line, intro, the six-sublens rotation with backticked `Name[note]`/`Power[note]` tags (expression law: math tokens backticked; no display equations were needed), the 8-fold/diatonic derivation at its index, the compilation's reading, and a Provenance section linking the house, flagging the compilation as a derived synthesis reference whose historical attributions keep their own public-source obligations, and noting that the house's declared consumers (C39, C38 and the argument records it lists) retain their own derivations — no new consumer edges propagated.

`lenses/README.md` rewritten (keeps `record_id: episteme-lenses`, `record_type: register-domain`): now indexes the twelve records by square with tonics/grounds, states the complement/Möbius relations per square, points the pre-lens `6² × 2 = 72`, the three grains and master tables back to the house instead of duplicating them, and records that the Baudrillard/Foucault readings were homed into their source houses on 2026-09-25.

## 5. Verification

- Twelve MEF lens records exist; each declares and links the house (script-checked).
- YAML frontmatter `yaml.safe_load` valid on all 37 touched/created files.
- 0 broken relative links, 0 broken `#` fragments into the two houses across the canonical tree checked.
- No path-style references to `lenses/baudrillard.md` / `lenses/foucault.md` remain in any canonical file.

## 6. Debts and stops

- **Generated projections now stale by design:** the seven files under `symbolon/episteme/maps/navigation/intents/` still mirror the old lens links (including the retired records). Hand-editing generated files is prohibited and builders were out of scope; they refresh on the next `tools/build-navigation.py` run (the completion hook will hold this until then).
- `working/p2-enrichment/receipts/T21-lens-foucault-completion.md`, `T22-*-consumer-closure.md` and the `_to_delete` snapshots still name the old paths: frozen provenance, deliberately untouched.
- The MEF house itself was not edited (outside ticket scope): the twelve records declare provenance one-way via `source_ids` and links. A later pass may add `consumed_by_lenses` entries naming the twelve records.
- Effects maps were run before wiring: `lens-baudrillard` (consumers A20/A24/A32/C27/C33/C38/C55), `foucault-1976` and `baudrillard-1976` (no declared outgoing consumers), `taylor-2026-mef-twelve-lenses` (declared consumers A05/A06/A09/A12/A14/A26/A31/A32, C38/C39) — all left intact; nothing severed, nothing merged.
- Nothing else stopped; no `<source_id>-NOTES.md` files were involved.
