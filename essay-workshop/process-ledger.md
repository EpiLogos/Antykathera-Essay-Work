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
