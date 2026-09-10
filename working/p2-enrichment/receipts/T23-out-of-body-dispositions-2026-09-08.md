# Out-of-body link dispositions — full census

Built from `tools/okf-workspace.py` (`Workspace.artifacts`, walking `.outgoing` edges) over every artifact whose path starts with `submission-package/essay/`, excluding `submission-package/essay/symbolon/episteme/maps/navigation/` (the audit generator itself). Edges are deduped per source artifact by `(target, relation, origin)`, so counts here are **link-instances after in-file dedup**, not raw occurrence counts (raw occurrences of the Agentworld title alone run to ~325 in-body, see the dedicated note below).

Totals: **61 distinct out-of-body targets, 375 deduped edges, from a full read of `ws.artifacts`/`ws.lookup`** (not just the audit's top-8-per-root sample).

## Disposition legend

- **RESONANCE-KEEP** — legitimately outside the body (dev ledger, cross-project material, plugin/canon resource shared across surfaces).
- **HOUSE-EXISTS-REPOINT** — a canonical `SOURCE.md` house already exists inside the body for this file; links should resolve there.
- **MISPLACED-NEEDS-HOUSE** — no house exists; file should get one.
- **GOVERNING-DOC** — central plan / orienting principles / README / wayfinder map.
- **OTHER** — mixed/ambiguous, explained inline.

## Table

| Target | Count (n src) | Raw forms (sample) | What it is | Existing house? | Disposition | Note |
|---|---|---|---|---|---|---|
| `the-return-of-zero-central-plan.md` | 76 (75) | `[[the-return-of-zero-central-plan]]` etc. | Repo-root v3.1 central structural plan — sole live authority | n/a | **GOVERNING-DOC** | Correctly outside the body; the plan governs the body, so it can never itself be housed inside it without an authority inversion. |
| `README.md` (repo root) | 14 (14) | `[[Antykathera-Essay-Work/README]]` etc. | Repo entry point / orientation doc | n/a | **GOVERNING-DOC** | Same reasoning as the plan — a wayfinder to the whole repo, structurally prior to the body. |
| `.wayfinder/maps/t20-t21-world-registers.md` | 3 (3) | markdown-link | Dated development map, "subordinate to central plan Amendment 2026-09-08" | n/a | **GOVERNING-DOC** | Explicitly a wayfinder/development map, self-declared subordinate — belongs beside the plan, not in the body. |
| `working/antykathera-resources/Antikythera Agentworld Brief.md` | 30 (27) deduped edges; **~325 raw wikilink occurrences** in-body | `[[Antikythera Agentworld Brief]]`, `#Source PDF page N` anchors | Frank's raw transcription of Bratton's Agentworld brief (the venue's own commissioning essay) | **YES** — `submission-package/essay/symbolon/episteme/sources/media-technology-philosophy/bratton/bratton-2026-agentworld-brief/SOURCE.md` (`local_copy: '[[Antikythera Agentworld Brief]]'`) | **HOUSE-EXISTS-REPOINT** | See dedicated finding below — this is the single highest-value repoint in the whole audit. |
| `working/sources-texts-references/10-7-2026-core-theorems-pithy.md` | 45 (43) | wikilink/markdown-link | The source spine: Frank's QL derivations, Theorems I–X | **YES** — `.../internal-corpus/taylor/taylor-2026-core-theorems-pithy/SOURCE.md` (`local_copy: [[working/sources-texts-references/10-7-2026-core-theorems-pithy]]`) | **HOUSE-EXISTS-REPOINT** | Second-largest target after the plan and the Agentworld brief; house already exists and is correctly wired via `local_copy` — links from body pages should resolve to the house, not the raw file. |
| `working/sources-texts-references/Epi Paper Write-ups/Symbolon Dynamics — Archetype, Attractor, and Objective Internality.md` | 14 (14) | wikilink | Taylor internal-corpus essay draft | **YES** — `.../internal-corpus/taylor/taylor-2026-symbolon-dynamics/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/sources-texts-references/Epi Paper Write-ups/Mono-Poly — The Two Ones and the Whole Field.md` | 13 (13) | wikilink/markdown-link | Taylor internal-corpus essay draft | **YES** — `.../internal-corpus/taylor/taylor-2026-mono-poly-two-ones/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/final-argument-quilt-2026-08-23/MYTHEME-AND-DEEP-SOURCE-SEAMS.md` | 13 (13) | wikilink/markdown-link | Quilt-programme seam ledger (T06D / GH #41), "active whole-form recovery" | none needed | **RESONANCE-KEEP** | Development ledger per CLAUDE.md's `working/` carve-out (non-publication development surfaces). |
| `working/sources-texts-references/Epi Paper Write-ups/source-extraction-definition-god-draft3.md` | 12 (12) | wikilink | `node_type: source-extraction` — internal passage-locator ledger for Draft 3 | House exists for the *underlying* work (see next row); this file is the extraction ledger, not the source | **HOUSE-EXISTS-REPOINT** | Should repoint to `taylor-2026-definition-god-draft3`'s verified passage cards, not the raw extraction ledger. |
| `working/sources-texts-references/definition-of-god-working/The Definition of God — Draft 3.md` | 12 (12) | wikilink/markdown-link | Draft 3 of "The Definition of God" (Taylor internal corpus) | **YES** — `.../internal-corpus/taylor/taylor-2026-definition-god-draft3/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/sources-texts-references/Epi Paper Write-ups/source-extraction-core-theorems.md` | 9 (6) | wikilink | `node_type: source-extraction`, "ready-for-source-record-ingestion" | House exists for underlying theorems file (see above) | **HOUSE-EXISTS-REPOINT** | Same pattern as the Draft-3 extraction ledger. |
| `working/final-argument-quilt-2026-08-23/COVENANT-ARBITRATION-AND-MEDIATING-OFFICES-SEAM.md` | 8 (8) | wikilink/markdown-link | Quilt seam ledger | none needed | **RESONANCE-KEEP** | Development ledger. |
| `working/sources-texts-references/definition-of-god-working/revision-notes-trust-and-f-blocks.md` | 8 (8) | markdown-link | Taylor revision-process notes | **YES** — `.../internal-corpus/taylor/taylor-2026-revision-notes-trust/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/conjugate-field/EROS-OF-LOGOS-A-CANDIDACY.md` | 8 (6) | markdown-link/wikilink | Conjugate-field candidacy draft | none needed | **RESONANCE-KEEP** | Development ledger (Pass-2 harmonisation family). |
| `working/final-argument-quilt-2026-08-23/PRE-39-SIGNAL-LINK-TATTVA-WORLD-AGENCY-CONFORMANCE.md` | 7 (7) | wikilink | Quilt seam ledger | none needed | **RESONANCE-KEEP** | |
| `working/sources-texts-references/Epi Paper Write-ups/P5 - Gebser.md` | 6 (6) | markdown-link/wikilink | Frank's page-numbered reading notes on Gebser | Public house exists for the actual work: `.../phenomenology-continental-philosophy/gebser/gebser-1985-ever-present-origin/` | **HOUSE-EXISTS-REPOINT** | Same pattern as P0/P1/P2/P3 below — raw reading notes on a work that already has a public `SOURCE.md`; the notes should feed that house's passage cards, links should target the house. |
| `working/sources-texts-references/QL-Essay-Rewrite.md` | 5 (5) | wikilink | ~35.5k-word long-form working draft, explicitly "underlies the plan; it is not the submission draft" (per project CLAUDE.md) | none needed | **RESONANCE-KEEP** | CLAUDE.md states this directly. |
| `working/sources-texts-references/epi-logos-plugin-resources-copy-10-07/resources/updated-ql-mef/mef-12-lenses-sublens-reference.md` | 5 (5) | markdown-link | July-10 convenience copy of the plugin's `resources/` tree, "not canon" per CLAUDE.md | Canonical version lives inside body-adjacent plugin path (see next row) | **OTHER** | Superseded-in-place by the canonical plugin copy below; not a body-misplacement, but should be repointed to the canonical copy rather than the snapshot, ahead of the snapshot's expected retirement. |
| `submission-package/epi-logos/resources/mef-12-lenses-sublens-reference.md` | 3 (3) | markdown-link/wikilink | Canonical plugin copy of the 12-lens reference | **YES** — `.../internal-corpus/taylor/taylor-2026-mef-twelve-lenses/SOURCE.md` (`local_copy` points at the *working copy*, not this canonical plugin path) | **HOUSE-EXISTS-REPOINT** | The house's `local_copy` itself should probably be updated to prefer this canonical plugin path over the July-10 snapshot. |
| `working/sources-texts-references/claude-fable-full-chat-end-12-7-2026.md` | 5 (5) | wikilink | Derivational conversation record — "never sufficient as public citation" | **YES** — `.../internal-corpus/taylor/chat-logs/taylor-claude-2026-derivational-chat/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/conjugate-field/PASS2-CHARTER.md` | 5 (5) | markdown-link | Binding charter for the conjugate-field Pass 2 harmonisation | none needed | **RESONANCE-KEEP** | Development ledger. |
| `working/sources-texts-references/Epi Paper Write-ups/P1 - Jorjani - Prometheus and Atlas.md` | 4 (4) | markdown-link/wikilink | Reading notes on Jorjani | Public house exists: `.../media-technology-philosophy/jorjani/jorjani-2016-prometheus-atlas/` | **HOUSE-EXISTS-REPOINT** | |
| `working/sources-texts-references/epi-logos-plugin-resources-copy-10-07/resources/updated-ql-mef/non-dual-binary/the-immutable-subject-and-the-matheme-of-its-recognition.md` | 4 (4) | markdown-link/wikilink | Plugin-resources snapshot content (theory file) | none inside body | **RESONANCE-KEEP (flagged)** | Same "not canon" snapshot family as above; keep for now, expect retirement when the minimal plugin build lands. |
| `working/antykathera-resources/antykathera-site-copy.md` | 4 (3) | wikilink | Antikythera venue site copy transcription | **YES** — `.../media-technology-philosophy/antikythera/antikythera-2026-site-copy/SOURCE.md` (`local_copy: [[antykathera-site-copy]]`) | **HOUSE-EXISTS-REPOINT** | Same class of fix as the Agentworld brief, smaller scale. |
| `working/final-argument-quilt-2026-08-23/ETYMOLOGICAL-ARCHAEOLOGY-TREE-SEAMS.md` | 4 (4) | markdown-link/wikilink | Quilt seam ledger | none needed | **RESONANCE-KEEP** | |
| `working/final-argument-quilt-2026-08-23/MYTHEME-WHOLE-STORY-AMPLIFICATION-LAW.md` | 4 (4) | markdown-link/wikilink | Quilt seam ledger | none needed | **RESONANCE-KEEP** | |
| `working/sources-texts-references/Epi Paper Write-ups/P2 - Para Trisika Vivarana Notes - Abhinavagupta and Jaideva Singh - Introduction.md` | 3 (2) | wikilink | Reading notes on Abhinavagupta/Singh | **YES** — `.../indian-philosophy/abhinavagupta/abhinavagupta-singh-1988-paratrisika-vivarana/SOURCE.md` (`local_copy: [[P2 - Para Trisika...]]`) | **HOUSE-EXISTS-REPOINT** | |
| `.wayfinder/maps/t20-t21-world-registers.md` | (listed above) | | | | | |
| `working/sources-texts-references/epi-logos-plugin-resources-copy-10-07/resources/deep/MEF Full Research - Oct 21 2025.md` | 3 (3) | wikilink | Raw gdrive-ingested MEF research dump (plugin snapshot) | none | **RESONANCE-KEEP (flagged)** | Plugin snapshot family. |
| `working/sources-texts-references/The Nothing That Is - Robert Kaplan.md` | 3 (2) | wikilink | Frank's copy/notes on Kaplan's *The Nothing That Is* | **YES** — `.../mathematics-logic/kaplan/kaplan-1999-nothing-that-is/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/sources-texts-references/Franki Taylor — Internal Corpus Argument Candidates.md` | 2 (2) | wikilink | Internal-corpus argument-candidate quilt | none needed | **RESONANCE-KEEP** | Raw authorial shelf, not itself a citable source object. |
| `submission-package/epi-logos/resources/canon/ql-musical-derivation-v3.md` | 2 (2) | wikilink | Canon excerpt of the musical-derivation grammar, shipped inside the plugin surface | n/a (canon excerpt, not a citable "source") | **RESONANCE-KEEP** | Cross-surface canon shared by essay + plugin (per CLAUDE.md's refraction ledger); legitimately lives under `submission-package/epi-logos/`, a sibling surface, not the essay body. |
| `working/sources-texts-references/Epi Paper Write-ups/The Advent of Zero — Subject, Psyche, and Integral Logic.md` | 2 (2) | markdown-link | Taylor internal-corpus essay draft | **YES** — `.../internal-corpus/taylor/taylor-2026-advent-zero-subject/SOURCE.md` | **HOUSE-EXISTS-REPOINT** | |
| `working/final-argument-quilt-2026-08-23/APHORISM-AND-PITHY-FORMULATION-LEDGER.md` | 2 (2) | markdown-link | Quilt ledger | none | **RESONANCE-KEEP** | |
| `working/sources-texts-references/Epi Paper Write-ups/P3 - Beyond Para-Trisika.md` | 2 (2) | wikilink | Reading notes continuing the Abhinavagupta engagement | Same house as P2 above | **HOUSE-EXISTS-REPOINT** | |
| `working/sources-texts-references/epi-logos-plugin-resources-copy-10-07/resources/updated-ql-mef/non-dual-binary/canonical-candidate/file-three-quilting.md` | 2 (2) | wikilink | Plugin snapshot theory file | none | **RESONANCE-KEEP (flagged)** | |
| `working/sources-texts-references/definition-of-god-working/corpus-sweep-2-crux-staging.md` | 2 (2) | markdown-link | Explicitly "UNMERGED STAGING... do not draft essay prose from this file directly" | none | **RESONANCE-KEEP** | Self-declared staging material. |
| `working/conjugate-field/DESCARTES-LANDING-PROPOSAL.md` | 2 (2) | markdown-link | Conjugate-field proposal draft | none | **RESONANCE-KEEP** | |
| `working/final-argument-quilt-2026-08-23/RELATIONAL-FORM-GROWTH-GRAMMAR.md` | 2 (2) | wikilink | Quilt ledger | none | **RESONANCE-KEEP** | |
| `working/sources-texts-references/the-meal-video-essay-outline.md` | 2 (2) | markdown-link/wikilink | Video-essay script outline, a separate authorial project | none | **RESONANCE-KEEP** | Cross-project raw shelf. |
| `working/final-argument-quilt-2026-08-23/NATIVE-020-DEEP-SEAM-RECONCILIATION.md` | 2 (2) | markdown-link/wikilink | Quilt ledger | none | **RESONANCE-KEEP** | |
| `working/sources-texts-references/epi-logos-plugin-resources-copy-10-07/resources/updated-ql-mef/non-dual-binary/file-slash/binary-explication-processual-seed.md` | 2 (2) | wikilink | Plugin snapshot theory file | none | **RESONANCE-KEEP (flagged)** | |
| `working/sources-texts-references/definition-of-god-working/harmonisation-plan.md` | 2 (2) | markdown-link | Self-declared "PLAN ONLY — no edits... awaits Frank's verification" | none | **RESONANCE-KEEP** | |
| — (18 further singleton targets, count = 1 each) | 1 (1) each | mixed | See family notes below | mixed | mixed | See below |

### The 18 singleton (count = 1) targets, grouped by family

- **`working/p2-enrichment/receipts/T20-job-biblical-source-acquisition.md`, `T20-mytheme-the-prisoner-development.md`, `T20-valentinian-source-acquisition.md`, `T21-dossier-oi-technical-responsibility-development.md`, `T22-current-migration-preservation-proof.md`** (5 files) — dated append-only receipts of prior enrichment work. **RESONANCE-KEEP** — receipts are process evidence, not body content.
- **`working/harmonisation-2026-08-18-objective-internality-capstone/CANONICAL-FIELD-CENSUS-PASS-A.md`** — "complete census candidate for T07 ratification; not yet canonical propagation." **RESONANCE-KEEP** (explicitly pre-canonical).
- **`working/final-argument-quilt-2026-08-23/DEVELOPMENTAL-QUILT-LEDGER.md`, `OUGHT-BE-APHORISM-ARCHITECTURE.md`** — quilt-programme ledgers. **RESONANCE-KEEP**.
- **`working/conjugate-field/CONCEPT-REHARMONISATION-PROPOSAL.md`, `FLIPSIDE-PACKAGE.md`** — conjugate-field proposal drafts. **RESONANCE-KEEP**.
- **`working/sources-texts-references/Epi Paper Write-ups/P0 - Jung and Pauli - Atom and Archetype.md`** — reading notes; public house exists at `.../psychology/jung/jung-pauli-meier-2001-atom-archetype/`. **HOUSE-EXISTS-REPOINT**.
- **`working/sources-texts-references/Epi Paper Write-ups/source-extraction-fable-chat.md`** — extraction ledger for the derivational chat, which already has a house (`taylor-claude-2026-derivational-chat`). **HOUSE-EXISTS-REPOINT**.
- **`working/sources-texts-references/chat-logs-for-quilting/07-08-2026-jung-marie-skenfrith-cope.md`** — raw Taylor-internal-corpus transcript. **YES**, house exists: `.../internal-corpus/taylor/chat-logs/taylor-2026-skenfrith-cope-jung-ql/SOURCE.md` (`local_copy` points straight at this file). **HOUSE-EXISTS-REPOINT** (this is also the representative of the whole `chat-logs-for-quilting/*` shelf that CLAUDE.md names — each conversation house resolves the same way).
- **`working/sources-texts-references/epi-logos-plugin-resources-copy-10-07/resources/methods/source-grounding.md`, `.../non-dual-binary/binary-explication-complete-plan.md`, `.../non-dual-binary/canonical-candidate/file-two-processual.md`, `.../non-dual-binary/file-one/the-self-proving-self.md`, `.../updated-ql-mef/self-identity.md`** (5 files) — all part of the July-10 plugin-resources convenience copy, which CLAUDE.md states directly is "not canon" and "expect this to be superseded." **RESONANCE-KEEP (flagged)** — same family as the other plugin-snapshot rows above; not misplaced relative to the essay body (they are plugin-surface material, a different register), but the copy itself is provisional and due for replacement by the minimal-plugin build; links should ideally target the eventual minimal-plugin path once it ships, not this snapshot.
- **`working/sources-texts-references/primary-texts/oi/oi-2026-responsibility-source-projection/OBJECTIVE-CO-INTERNALITY.md`** — belongs to the separate O:I project's relational-grammar work ("extends `docs/SHARED-FIELD.md`"). **RESONANCE-KEEP** — genuine cross-project resonance, not a Return-of-Zero source at all.

---

## Agentworld Brief — the exact resolver finding

**File:** `working/antykathera-resources/Antikythera Agentworld Brief.md` — Frank's own transcription of Bratton's *Agentworld* brief, with `title: "Antikythera Agentworld Brief"` and `aliases: ["Agentworld brief", "Agentworld — Benjamin Bratton"]` in its own frontmatter.

**House:** `submission-package/essay/symbolon/episteme/sources/media-technology-philosophy/bratton/bratton-2026-agentworld-brief/SOURCE.md` — fully verified (`metadata_status: verified`, `citation_status: citation-ready`, `quote_status: quotation-ready`), with `local_copy: '[[Antikythera Agentworld Brief]]'` pointing straight at the raw file, and `consumed_by_sections`/`consumed_by_arguments` populated across `§0/1, §0, §2, §4, §5, §5→0` and 8 arguments. Its own `title` field is `"Bratton — Antikythera Agentworld Brief (2026)"` and it carries **no `aliases:` field**.

**Why the resolver prefers the raw working file, mechanically confirmed:**

`Workspace._resolve()` looks up a bare wikilink target by `normalise(stem)` in `ws.lookup`, a dict built (around the artifact-loading pass) from each artifact's own `title` plus any `aliases` and `source_id_aliases` in its frontmatter (`tools/okf-workspace.py` lines ~348–371). I ran the exact lookup:

```
normalise("Antikythera Agentworld Brief") -> "antikytheraagentworldbrief"
ws.lookup["antikytheraagentworldbrief"] == ["working/antykathera-resources/Antikythera Agentworld Brief.md"]
```

**Only one candidate exists** for that key — the raw working file, because its own `title:` frontmatter is exactly `"Antikythera Agentworld Brief"`. The SOURCE.md house's `title` is a different string (`"Bratton — Antikythera Agentworld Brief (2026)"`, which normalises to a different key), and the house declares no `aliases:` entry for the bare title, so it never enters the candidate list at all. This means the priority table at `_resolve` (source-house priority 3 vs. document priority 10, lines ~547–556) **never gets a chance to run** — there's no tie to break, because the house isn't a candidate in the first place. The `local_copy: '[[Antikythera Agentworld Brief]]'` field in the house's frontmatter is documentation only; it is not consumed by `_build_edges`/`_resolve` to register a reverse alias.

**Exact fix:** add `aliases: ["Antikythera Agentworld Brief"]` (and optionally `"Agentworld brief"`, `"Agentworld — Benjamin Bratton"` to mirror the raw file's own aliases) to the frontmatter of `submission-package/essay/symbolon/episteme/sources/media-technology-philosophy/bratton/bratton-2026-agentworld-brief/SOURCE.md`. Once that alias is registered, `ws.lookup["antikytheraagentworldbrief"]` will contain both the house and the raw file, and `_resolve`'s priority ordering (`source-house` = 3, ahead of `document` = 10) will pick the house automatically — no changes needed to any of the ~325 individual `[[Antikythera Agentworld Brief]]` links in body pages. This is a one-line frontmatter edit that resolves the single largest concrete out-of-body target in the whole audit (30 deduped edges / 27 distinct source pages / ~325 raw occurrences).

---

## Summary of disposition classes

- **GOVERNING-DOC**: 3 targets (`the-return-of-zero-central-plan.md`, `README.md`, `.wayfinder/maps/t20-t21-world-registers.md`) — 93 deduped edges.
- **HOUSE-EXISTS-REPOINT**: 20 targets — the Agentworld brief, the core-theorems spine, the antikythera site-copy, all 8 internal-corpus Taylor essay drafts/notes (Symbolon Dynamics, Mono-Poly, Advent of Zero, Definition of God Draft 3 + its extraction ledger + revision notes + corpus-sweep staging is kept separate as RESONANCE, the derivational chat + its extraction ledger, the Skenfrith-Cope chat log, the MEF-12-lenses canonical plugin copy), and the 6 Epi-Paper-Write-ups reading-note files on already-housed public scholars (Jung/Pauli, Jorjani, Gebser, Abhinavagupta ×2, Kaplan).
- **MISPLACED-NEEDS-HOUSE**: 0 targets found. Every out-of-body file that is a genuine "work" either already has a canonical house wired via `local_copy`, or is legitimately a development ledger/governing doc/cross-project file rather than a citable source.
- **RESONANCE-KEEP**: ~30 targets — the quilt-programme ledgers (`working/final-argument-quilt-2026-08-23/*`, 9 files), the conjugate-field Pass-2 family (5 files), the p2-enrichment receipts (5 files), the harmonisation census, `QL-Essay-Rewrite.md`, `Franki Taylor — Internal Corpus Argument Candidates.md`, the video-essay outline, the O:I cross-project file, the canonical plugin `ql-musical-derivation-v3.md` excerpt, and the July-10 plugin-resources snapshot family (6 files, flagged as provisional/superseded-pending).
- **OTHER**: 1 (the July-10 snapshot copy of `mef-12-lenses-sublens-reference.md`, which should repoint to the canonical in-plugin copy rather than the snapshot — a repoint between two out-of-body files, not into the body).

## Ten largest targets and their disposition

1. `the-return-of-zero-central-plan.md` — 76 edges — **GOVERNING-DOC**
2. `working/sources-texts-references/10-7-2026-core-theorems-pithy.md` — 45 edges — **HOUSE-EXISTS-REPOINT** (`taylor-2026-core-theorems-pithy`)
3. `working/antykathera-resources/Antikythera Agentworld Brief.md` — 30 edges (~325 raw) — **HOUSE-EXISTS-REPOINT** (`bratton-2026-agentworld-brief`, needs the alias fix above)
4. `working/sources-texts-references/Epi Paper Write-ups/Symbolon Dynamics...` — 14 edges — **HOUSE-EXISTS-REPOINT** (`taylor-2026-symbolon-dynamics`)
5. `README.md` — 14 edges — **GOVERNING-DOC**
6. `working/sources-texts-references/Epi Paper Write-ups/Mono-Poly...` — 13 edges — **HOUSE-EXISTS-REPOINT** (`taylor-2026-mono-poly-two-ones`)
7. `working/final-argument-quilt-2026-08-23/MYTHEME-AND-DEEP-SOURCE-SEAMS.md` — 13 edges — **RESONANCE-KEEP**
8. `working/sources-texts-references/Epi Paper Write-ups/source-extraction-definition-god-draft3.md` — 12 edges — **HOUSE-EXISTS-REPOINT** (`taylor-2026-definition-god-draft3`)
9. `working/sources-texts-references/definition-of-god-working/The Definition of God — Draft 3.md` — 12 edges — **HOUSE-EXISTS-REPOINT** (`taylor-2026-definition-god-draft3`)
10. `working/sources-texts-references/Epi Paper Write-ups/source-extraction-core-theorems.md` — 9 edges — **HOUSE-EXISTS-REPOINT** (`taylor-2026-core-theorems-pithy`)
