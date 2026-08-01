# OKF Wiki Development Integration Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the developer-side `okf-wiki` skill the tested operating surface for crawling, searching, tracing, and assembling working context across the complete Return of Zero workspace.

**Architecture:** Preserve every existing artifact as its own typed and authoritative file. Build one read-only workspace graph from frontmatter, Markdown links, stable IDs, tags, and explicit relations; use BKMR only as a disposable full-content search index beneath that graph. Sol, Luna, writing, and review must enter through the same wiki crawl and receive traceable canonical context rather than independent summaries.

**Tech stack:** Python 3 standard library, Markdown/YAML frontmatter, Ruby adapter generation already embedded in `tools/bkmr-essay`, BKMR CLI, `unittest`, Codex skills, project `.codex/config.toml`.

---

### Task 1: Isolate the project from the installed Epi-Logos skill set

**Files:**
- Modify: `.codex/config.toml`
- Create: `Antykathera-Essay-Work/AGENTS.md`

1. Add project-local `[[skills.config]]` entries disabling every skill under the installed S5 Epi-Logos plugin.
2. Add scoped instructions declaring the live authority order, wiki-first entry, anti-memory and anti-hedging rules, and the prohibition on the unrelated installed voice skill.
3. Verify the TOML parses and every installed Epi skill path is covered.

### Task 2: Establish real failing wiki tests

**Files:**
- Create: `Antykathera-Essay-Work/tests/test_okf_workspace.py`
- Create: `Antykathera-Essay-Work/tests/test_bkmr_essay.py`

1. Test the real workspace, not mocked nodes.
2. Require discovery of sections, arguments, concepts, paths, rooms, source records, quote dossiers, plans, and governing documents as typed artifacts.
3. Require substantive full-body search for known phrases that metadata-only BKMR currently misses.
4. Require typed outgoing links, backlinks, neighbourhood expansion, path traversal, claim-to-source traces, context assembly, authority/status reporting, stale-index detection, and thin-node diagnostics.
5. Run the tests and record the expected RED failures.

### Task 3: Implement the read-only workspace graph crawler

**Files:**
- Create: `Antykathera-Essay-Work/tools/okf-workspace.py`

1. Discover Markdown artifacts under the project root while excluding legacy, cache, generated database, and build directories according to explicit policy.
2. Parse frontmatter, headings, Markdown links, wikilinks, tags, stable IDs, source IDs, argument IDs, section IDs, consumers, and status fields.
3. Resolve links against paths, stems, titles, aliases, and stable IDs without changing canonical files.
4. Implement `status`, `find`, `open`, `links`, `backlinks`, `neighbourhood`, `path`, `trace`, `context`, and `doctor` commands with JSON output.
5. Run each failing test until GREEN.

### Task 4: Make BKMR index the authored intelligence

**Files:**
- Modify: `Antykathera-Essay-Work/tools/bkmr-essay`
- Test: `Antykathera-Essay-Work/tests/test_bkmr_essay.py`

1. Generate adapters for sections, arguments, and concepts from their full authored bodies plus canonical metadata.
2. Add collections for concepts and workspace artifacts where the real crawl shows they are necessary.
3. Read the canonical quote index/dossiers rather than the obsolete ledger contract.
4. Record canonical content hashes and refuse searches against stale collections.
5. Add an all-collection search mode used by `okf-workspace find` while preserving collection-specific search.
6. Verify known substantive queries return the correct canonical artifacts.

### Task 5: Establish discoverable developer-side wiki and writing skills

**Files:**
- Create: `.agents/skills/okf-wiki/SKILL.md`
- Create: `.agents/skills/okf-wiki/references/workspace-contract.md`
- Create: `.agents/skills/return-of-zero-writing/SKILL.md`
- Modify: `Antykathera-Essay-Work/AGENTS.md`

1. Keep developer tools separate from the eventual submission-package plugin being developed and tested.
2. Make workspace `okf-wiki` the mandatory development entry for substantive essay work.
3. Teach the REPL loop: orient, find, open, expand, trace, assemble, verify, act.
4. Separate authority, claim status, evidence readiness, quotation readiness, and retrieval confidence.
5. Require canonical trace output before drafting or synthesis.
6. Add a subordinate Return of Zero writing skill that loads the local voice, rubric, and comparison gate only after wiki orientation.
7. Validate both skill structures and run realistic command-level pressure scenarios.

### Task 6: Route Sol and Luna through the wiki

**Files:**
- Modify: `Antykathera-Essay-Work/agent-skills/sol-section-room-deepening/SKILL.md`
- Modify: `Antykathera-Essay-Work/agent-skills/sol-section-room-deepening/references/fresh-session-execution-prompt.md`
- Modify: `Antykathera-Essay-Work/agent-skills/sol-section-room-deepening/references/depth-rubric.md`
- Modify: `Antykathera-Essay-Work/agent-skills/luna-source-quote-swarm/SKILL.md`
- Modify: `Antykathera-Essay-Work/agent-skills/luna-source-quote-swarm/references/fresh-session-execution-prompt.md`

1. Remove the installed `epi-logos-voice` dependency.
2. Require a wiki-generated context trace for every section-room pass.
3. Require detailed angles per section movement, argument, concept, source relation, counterpressure, and transition.
4. Make missing context a named debt rather than a place for fluent inference.
5. Preserve protected author surfaces and existing source-verification discipline.

### Task 7: Diagnose and repair low-grade graph nodes

**Files:**
- Modify only canonical argument, concept, or section nodes proven deficient by the doctor and required traversal tests.

1. Report nodes that lack substantive propositions, warrants, tensions, consumers, incoming/outgoing relations, aliases, or source relations.
2. Repair explicit relations from existing canonical material; do not invent argument content.
3. Generate backlinks and aggregate views rather than duplicating prose into new manual summaries.
4. Re-run graph integrity and context traces after every repair group.

### Task 8: Repair integration blockers and verify the complete system

**Files:**
- Modify the canonical quote state responsible for the existing quotation-ready mismatch, based on the actual dossier evidence.
- Modify existing tests only where their fixtures incorrectly depend on mutable production state or accept placeholder semantics.

1. Reproduce and repair the Le Bon quote-state mismatch at its authoritative source.
2. Replace placeholder-shaped room audit assertions with substantive real-artifact checks.
3. Run the new wiki/BKMR tests, existing builder tests, room audit, skill validators, TOML parse, BKMR sync/search tests, and representative end-to-end context crawls.
4. Report exact pass/fail evidence and any remaining canonical content debts.
