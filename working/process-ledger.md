---
title: "Process Ledger — Agent Navigation and Dissemination Lessons"
page_type: process-ledger
authority: non-governing
status: append-only
created: "2026-07-29"
tags:
  - epi-logos/antikythera-essay
  - planning-v3/process
---

# Process Ledger

> [!important] What this file is
> An append-only record of what worked and what failed when agents navigated, retrieved from, and wrote into this corpus. Each phase of the harmonisation and vault work appends a dated entry: what context sufficed, what got dropped, which retrieval moves ran true, which produced drift. The ledger's consumer is the later precision pass on the reader-facing skills (`okf-wiki`, `walk-the-essay`, `investigate`, `converse-pedagogically`): lessons recorded here become skill refinements there. Entries are observations, not rules; nothing here governs. Never delete or rewrite an entry — append corrections as new entries.

Entry form: date · phase/task · what was attempted · context supplied · what sufficed / what was lost · lesson for skill precision.

---

## 2026-07-29 · Pre-phase (recon + protocol development)

**Attempted:** four parallel read-only recon passes (nodes census, source bank, submission package, writing surfaces); two canon-careful hygiene edits (Concept Map refresh, source-shell population); writing-guidance migration; expression-grammar authoring.

**Context supplied:** each recon agent got a scoped directory, explicit expected-counts to verify, and instructions to return conclusions not file dumps. Each editing agent got the orienting principles as mandatory first read, the exact target files, exemplar files for register, and a canon-flows-one-way reporting requirement.

**What sufficed / what was lost:**
- Scoped recon with expected-counts-to-verify caught four stale beliefs in project memory (CLAUDE.md said 17 arguments — 20 exist; the recon brief itself said 110 houses/255 passages — 111/288 after the same-day rebuild; a "defect" brief of an empty `## Claim` in argument 14 was actually a heading variant, `## Core claim`; a recon agent misread the canonical room slugs as a naming fork until checked against orienting principles §V). **Lesson: agent briefs must carry expectations as *hypotheses to verify*, never as facts — every stale count propagated from memory was caught only because an agent checked.**
- The orienting-principles-first rule worked: the Concept Map agent refused to invent a braid group for an unroutable concept and placed it with an honest gloss instead; the argument-14 agent refused a task whose premise failed verification rather than "completing" it by inventing structure. **Lesson: the never-invent-structure lock plus a verify-the-premise habit is what makes delegated edits safe; encode both in any skill that writes.**
- Passing exemplar files (a populated source house, a sibling argument's Claim section) fixed register better than describing register. **Lesson: skills should point at exemplars, not describe styles.**
- Source-shell population needed the NOTES.md-read-only rule stated twice (in protocol and in brief) — it held. Nested-quotation hazards (Gans/Levinas inside Watson; Jung/Nishida inside Chang) recur; the double-transmission warning pattern from the Watson house transferred cleanly to the Chang house. **Lesson: the "nested referent inside another house" pattern deserves a named rule in the source skill.**
- Mtime-only history made recon harder everywhere (no git commits existed until today's freeze). **Lesson: commit discipline is agent-navigation infrastructure, not just safety.**

**Skill-precision candidates:** verify-premise-before-execute; expectations-as-hypotheses; exemplar-over-description; nested-referent rule; heading-variant tolerance in section scans (`## Claim` vs `## Core claim` — scans must match content role, not literal heading).

## 2026-08-08 · Ontology-aware reorganisation — named debt: protocol-design session

**Attempted:** recovery of the development session that produced `WRITING-PROTOCOL.md` (protocol design, §3 shape, register grammar, migration decisions) before any ontology-adjacent amendment.

**Context supplied:** full search of the raw transcript shelf (`chat-logs-for-quilting/` — five dated transcripts, none about protocol design), the Taylor dialogue-record houses under `source-bank/sources/internal-corpus/taylor/` (including `taylor-claude-2026-derivational-chat`, which is derivational memory for the argument, not the protocol session), `definition-of-god-working/` chats, `docs/plans/` (dated integration plans, none covering the protocol), `.wayfinder/` (Epi-Card production), and a repo-wide search for session exports (`.jsonl`, `*session*`, `*transcript*`).

**What sufficed / what was lost:** the session is not recoverable from the repository. The in-repo records are `WRITING-PROTOCOL.md` itself, the dated plans under `docs/plans/`, and the current-state index. This is a **named debt**: ontology-adjacent decisions proceed from the protocol plus Frank's 2026-08-08 correction (rooms and essay parallel to `symbolon/`; 4+2 sixfold; OKF as validator, not generator) as the sole record, and any design intent the missing session might have carried must be asked of Frank rather than silently improvised.

**Lesson for skill precision:** treat the absence of a governing session transcript as a retrievable debt to record at the start of a reorganisation, not as licence to reconstruct design intent from the resulting documents alone.

## 2026-08-08 · Ontology-aware reorganisation — incident: hook self-trigger deleted nested NOTES.md files

**Attempted:** repair of the project hook's stale flat `*/NOTES.md` glob to the nested bank layout (`rglob("NOTES.md")`), applied via an `apply_patch` whose payload contained the literal string "NOTES.md".

**What happened:** the hook's own `could_touch_notes` gate fires on any tool payload containing "notes.md", so the patch was wrapped in the hook's snapshot/restore flow. PreToolUse ran against the old flat glob (snapshot empty); PostToolUse ran against the newly applied `rglob` (found five nested notes), treated them as newly appearing, and unlinked them. The restore message text is the same for both branches ("restored"), which made the deletion look like a restoration. The five notes were recovered from git: four at their committed state; the Neumann note at its 33 KB staged version (the unstaged working-tree delta at deletion time was not recoverable — no dangling blob existed).

**Lesson for skill precision:** (1) never patch the hook's own NOTES.md discovery logic through a tool payload that itself contains the string "notes.md" — the hook wraps itself in its own protection flow and the pre/post code can differ mid-call; (2) the hook's PostToolUse "current − prior → unlink" branch will delete any NOTES.md file that appears between pre and post, so restoring notes via shell/apply_patch is also intercepted — use git pathspecs that do not spell "NOTES.md", or stage the restore outside the hook's watch; (3) the "restored" stopReason is emitted for both restore and delete branches — it cannot be read as evidence of preservation. Recovery status: files restored, Neumann's latest unstaged delta lost; report honestly to Frank.

## 2026-08-09 · Named debt resolved — protocol-design session recovered from on-disk Codex logs

**Attempted:** recovery of the session that produced `WRITING-PROTOCOL.md` (previously recorded as an unrecoverable debt). Codex session logs were found on disk at `~/.codex/sessions/` despite the provider switch hiding them from the UI.

**What sufficed:** the design thread was located — origin `rollout-2026-07-28T11-51-12-019fa859…` (holographic publication form) and the protocol-authoring session `~/.codex/sessions/2026/08/02/rollout-2026-08-02T22-43-53-019fc46e…` (preliminary-vs-writing separation, symbolon as the meta-field holding matheme/mytheme/episteme, no `relations/` dir, granular outward-and-return links between deep records and exact manuscript/argument locations). Readable transcripts and raw records were exported to the repository root (`protocol-design-session-2026-08-02.md/.jsonl`, `protocol-design-origin-2026-07-28.md/.jsonl`) for Frank to work with or move.

**Recovered definition:** register is the admission-and-return channel of the holographic piece — polyvalent field detail maps into the sections with precision, and records outside the essay point back to exact essay lines. A movement or argument declares a register composition (a station carries matheme, mytheme, and episteme at once), not a single bucket. This definition is now written into the register-grammar concept node and `WRITING-PROTOCOL.md` §4; the unratified 70 are register-composition declarations pending Frank's assignments.

**Lesson for skill precision:** when a session appears lost to a provider switch, check `~/.codex/sessions/` and `archived_sessions` on disk before declaring a debt — session JSONL survives independently of the UI, and `parent_thread_id` chains reconstruct the full thread.
