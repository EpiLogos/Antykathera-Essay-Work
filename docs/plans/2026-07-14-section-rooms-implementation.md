# Return of Zero Section Rooms Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development while implementing each behavior and superpowers:verification-before-completion before claiming completion.

**Goal:** Build eight habitable, section-scale writing rooms that collate the existing 48-movement argument and source architecture without replacing its canonical files or overwriting Frank's prose.

**Architecture:** A deterministic Python standard-library builder reads the live movement nodes, granular source map, source records, quote ledger, argument nodes, and central plan. It writes only agent-owned room surfaces (`00-SECTION-CONTEXT.md` and first-run templates), preserves author-owned and editorial surfaces on every rebuild, and produces a manifest that makes provenance and validation explicit. The eight rooms are author-facing refractions of the existing graph: [[P0]]–[[P5]] remain the inner movement, the current nodes remain canonical, and the room is the [[Square B]] encounter surface where lived composition can meet verifiable scholarly work.

**Tech Stack:** Python 3.13 standard library, `unittest`, Markdown/YAML frontmatter, Obsidian wikilinks.

---

### Task 1: Specify the room contract with failing integration tests

**Files:**
- Create: `Antykathera-Essay-Work/tests/test_build_section_rooms.py`

**Step 1: Write a real temporary-vault integration test**

Copy the minimum canonical fixture tree into a temporary directory, execute the actual builder as a subprocess, and assert that it creates exactly eight room directories with four human-facing files and one manifest.

**Step 2: Test the canonical movement contract**

Assert that the generated manifests collectively contain sequences 1–48 exactly once and that every room contains six movements in traversal order.

**Step 3: Test the sovereignty contract**

Write distinctive prose into `10-FRANK-DRAFT.md`, rerun the builder, and assert byte-for-byte preservation. Apply the same check to `20-SCHOLARLY-EDITION.md` and `30-PLATE-AND-DIAGRAMS.md`.

**Step 4: Test source and quotation truthfulness**

Assert that a source can appear as citation-ready without being shown as quotation-ready, and that only quote-ledger rows with `quotation-ready` status appear in the verified-passage section.

**Step 5: Run the tests and observe the expected failure**

Run: `python3 -m unittest Antykathera-Essay-Work/tests/test_build_section_rooms.py -v`

Expected: FAIL because `tools/build-section-rooms.py` does not exist.

### Task 2: Implement the deterministic builder

**Files:**
- Create: `Antykathera-Essay-Work/tools/build-section-rooms.py`

**Step 1: Implement canonical input validation**

Require eight known stations, six movement nodes per station, unique sequence values 1–48, resolvable source records, and a parseable quote ledger. Fail with actionable messages instead of emitting partial rooms.

**Step 2: Implement safe write ownership**

Always refresh `00-SECTION-CONTEXT.md` and `.section-room.json`. Create the draft, scholarly edition, and plate files only when absent. Use atomic replacement for generated files.

**Step 3: Compile the human-readable context**

For each station, render: living centre; arrival and release; six-movement arc; argument and concept constellation; source field with independent citation/quotation states; verified passages; open support; continuity and presaging; and today's doorway.

**Step 4: Emit provenance**

Record the canonical movement paths, source IDs, argument links, previous/next rooms, builder version, and input fingerprints in `.section-room.json`.

**Step 5: Run the tests until green**

Run: `python3 -m unittest Antykathera-Essay-Work/tests/test_build_section_rooms.py -v`

Expected: all tests pass.

### Task 3: Generate the live section rooms

**Files:**
- Create: `Antykathera-Essay-Work/essay-workshop/section-rooms/README.md`
- Generate: `Antykathera-Essay-Work/essay-workshop/section-rooms/<eight-room-directories>/**`

**Step 1: Run the builder against the real vault**

Run: `python3 Antykathera-Essay-Work/tools/build-section-rooms.py`

Expected: eight rooms created; 48 movements accounted for; no canonical files changed.

**Step 2: Inspect one early, one middle, and one late room**

Verify the contexts for `§0/1`, `§3`, and `§5→0` read coherently, expose the correct source debt, and carry previous/next continuity.

**Step 3: Run idempotence and preservation checks**

Hash the protected files, rerun the builder, and confirm the hashes are unchanged.

### Task 4: Document and verify the operating rhythm

**Files:**
- Modify: `Antykathera-Essay-Work/CLAUDE.md`
- Modify: `Antykathera-Essay-Work/essay-workshop/section-rooms/README.md`

**Step 1: Document room ownership**

State that the context and manifest are generated; Frank's draft is sovereign; scholarly edition and plate surfaces are agent-maintained but never rebuilt automatically.

**Step 2: Document the daily loop**

Arrival → write → harvest → scholarly pass → author review, with quote and claim-status gates preserved.

**Step 3: Run complete verification**

Run:

```bash
python3 -m unittest discover -s Antykathera-Essay-Work/tests -v
python3 Antykathera-Essay-Work/tools/build-section-rooms.py --check
```

Expected: all tests pass; check mode reports eight valid rooms and 48 uniquely assigned movements with no stale generated files.

