# Essay Readability Pass Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the Quartz essay at `/essay` calm to read and easy to traverse: no dumped metadata, generous spacing, fadable sidebars, a legible explorer, and tags gone from the page with a tag filter living in the fullscreen graph instead.

**Architecture:** All work is in the vendored Quartz tree (`site/vendor/quartz/`) — layout choices in `quartz.layout.ts`, two new micro-components for the sidebar fades, explorer options already supported upstream (`mapFn`), and night-skin spacing in `quartz/styles/custom.scss`. Verification extends the project's own smoke harness (`site/tests/essay-host-smoke.py`) with new assertions written first so they fail, then pass. Same deploy path as before: `npm run build:public` → PR → self-merge → `vercel deploy --prod --archive=tgz` from `site/dist`.

**Tech Stack:** TypeScript/Preact (Quartz components), SCSS (custom.scss), Python Playwright smoke, Node test runner.

**Ground rules carried from the hard brief:** no stub pages, no meta-refresh; `/` stays Plate A; the build still fails without the Quartz publication; tests tell the truth; land via self-merged PR (branch protection requires a PR, 0 approvals).

---

### Task 1: Remove the metadata dump from every page

The tags row (`#epi-logos/antikythera-essay #argument-map/live …`) and the meta line (`Sep 25, 2026, 2 min read` — the date is the staging timestamp, meaningless) go. Breadcrumbs and article title stay.

**Files:**
- Modify: `site/vendor/quartz/quartz.layout.ts` (beforeBody arrays, both layouts)

**Step 1: Write the failing smoke assertions**

In `site/tests/essay-host-smoke.py`, inside the status-200 branch, add:

```python
assert page.locator('.tags').count() == 0, 'tag dump still on the page'
assert page.locator('.content-meta').count() == 0, 'content meta still on the page'
```

**Step 2: Run to verify failure**

Run: `python3 site/tests/essay-host-smoke.py`
Expected: FAIL — `.tags` present on reading pages.

**Step 3: Remove the components from the layout**

In `quartz.layout.ts`, delete `Component.TagList(),` and `Component.ContentMeta(),` from `defaultContentPageLayout.beforeBody` (they are the only metadata emitters there; `Breadcrumbs` and `ArticleTitle` remain).

**Step 4: Rebuild and verify pass**

Run: `cd site && npm run build:public && python3 tests/essay-host-smoke.py`
Expected: PASS, all checks.

**Step 5: Commit**

`git commit -m "Essay pages: stop emitting the tag dump and content meta line"`

---

### Task 2: Reading comfort — spacing and density

Night-serif text at 1.6rem line-height in a dense column reads squashed. Fix in `site/vendor/quartz/quartz/styles/custom.scss` (our skin file — no upstream edits).

**Files:**
- Modify: `site/vendor/quartz/quartz/styles/custom.scss`

**Step 1: Write the failing smoke assertion**

In the smoke's status-200 branch:

```python
line_height = page.evaluate('parseFloat(getComputedStyle(document.querySelector(".article-title")).lineHeight) / parseFloat(getComputedStyle(document.querySelector(".article-title")).fontSize)')
assert line_height >= 1.5, f'article line-height too tight: {line_height}'
```

**Step 2: Run to verify failure**

Run: `python3 site/tests/essay-host-smoke.py` → Expected: FAIL (~1.15).

**Step 3: Write the spacing skin**

Append to `custom.scss`:

```scss
// Reading comfort — the essay breathes.
article {
  line-height: 1.75;
  p, li { line-height: 1.75; }
  p { margin-block: 1.1em; }
  h1 { margin-top: 2.2rem; margin-bottom: 1rem; }
  h2, h3 { margin-top: 2rem; margin-bottom: 0.8rem; }
  hr { margin-block: 2.5rem; }
  blockquote { margin-block: 1.5rem; padding-inline: 1.2rem; }
  ul, ol { padding-left: 1.6rem; }
}
.article-title { margin-bottom: 1.4rem; line-height: 1.3; }
.breadcrumbs { margin-bottom: 0.6rem; }
.center, article { padding-inline: clamp(1.2rem, 4vw, 3rem); }
```

**Step 4: Verify** — smoke PASS; screenshot the movement page at 1440 and eyeball: air around headings, paragraph separation, nothing touching the rails.

**Step 5: Commit** — `git commit -m "Essay reading comfort: line-height, spacing, title margins"`

---

### Task 3: Tiny icons to fade the explorer and the right rail

Two 28px ghost buttons pinned to the outer edges: one in the left sidebar header row (chevron-left), one floating at the right viewport edge (chevron-right). Each toggles a body class (`rail-hidden`, `explorer-hidden`), collapses the grid column to 0 with a 300ms transition, remembers state in `localStorage`, and its aria-pressed reflects state. The reading column widens when either is hidden.

**Files:**
- Create: `site/vendor/quartz/quartz/components/FadeToggles.tsx` (one component, renders both buttons, hydrates from `contentIndex`-independent inline script)
- Modify: `site/vendor/quartz/quartz/layout.ts` — add `<FadeToggles />` via `sharedPageComponents.header`? No — render inside both `left` and `right` arrays is wrong; instead add to `sharedPageComponents` is not supported for body-level. Place: append the component in `defaultContentPageLayout.left` and `right` is wrong too. **Concrete:** register the component and append it to `Component.Flex({...})`? Simplest correct: emit both buttons from ONE component added to `beforeBody` and position them with `position: fixed` CSS (left button vertically centered at left edge, right button at right edge).
- Modify: `site/vendor/quartz/quartz/styles/custom.scss` (fixed positioning, ghost styling `opacity .35 → 1 on hover`, grid column collapse rules)
- Modify: `site/tests/essay-host-smoke.py` (assertions)

**Step 1: Write failing smoke assertions**

```python
left_btn = page.locator('button[aria-label="Toggle explorer"]')
right_btn = page.locator('button[aria-label="Toggle graph rail"]')
expect(left_btn).to_be_visible()
left_btn.click()
expect(page.locator('.explorer')).to_be_hidden()
left_btn.click()  # restore for later cases
```

**Step 2: Verify failure** — smoke FAIL (buttons absent).

**Step 3: Implement `FadeToggles.tsx`**

Static Preact component returning two `<button>`s (inline SVG chevrons, `aria-label` as above) + `FadeToggles.afterDOMLoaded` script: read `localStorage.oi-fades`, apply body classes before paint (inline in `beforeBody` via `FadeToggles.beforeDOMLoaded` to avoid flash), wire click handlers to toggle class + storage.

**Step 4: Styling** — fixed, 28px circular ghost buttons, gold on hover; `.explorer-hidden .sidebar.left { display:none }`-style rules with grid-template transition on `#quartz-body .page`.

**Step 5: Verify** — smoke PASS; manual: desktop click both, page widens, state survives reload.

**Step 6: Commit** — `git commit -m "Essay: tiny fade toggles for explorer and graph rail"`

---

### Task 4: Explorer legibility — hierarchy, contrast, less repetition

Problems: folder and file text share near-identical color; movement names repeat their station prefix (`§0/1 · #0 — …`) under the station they already sit in; no indent guides, so nesting boundaries blur.

**Files:**
- Modify: `site/vendor/quartz/quartz.layout.ts` — Explorer options: add `mapFn` (upstream-supported) stripping `§x/y · ` prefixes from displayed names (keep `#N — Title`), and dropping the `.md`-style numeric folder prefixes in display (`00-integral-threshold` → `Integral Threshold` — humanize slug segment: strip `^\d+-`, replace `-` with space, on FOLDERS only).
- Modify: `site/vendor/quartz/quartz/styles/custom.scss` — explorer hierarchy: folders `color: var(--secondary)`, weight 600, folder icon visible; files `color: var(--darkgray)` at 0.9em; active file `color: var(--tertiary)` + gold left-rule; indent guides via `border-left: 1px solid var(--lightgray)` on nested `ul` with 0.9rem indent steps; increase item spacing to `0.35rem`.

**Step 1: Write failing smoke assertions**

```python
folder = page.locator('.explorer .folder-container').first
file = page.locator('.explorer a').nth(1)
folder_color = folder.evaluate('el => getComputedStyle(el).color')
file_color = file.evaluate('el => getComputedStyle(el).color')
assert folder_color != file_color, 'explorer folders and files share one color'
labels = page.locator('.explorer ul a').all_text_contents()
assert not any('§0/1 ·' in t for t in labels), 'station prefix repetition still in explorer'
```

**Step 2: Verify failure.**

**Step 3: Implement mapFn + hierarchy scss.** `mapFn` mutates `node.displayName` only (slugs/URLs untouched — routing unchanged).

**Step 4: Verify** — smoke PASS; screenshot: folders read as containers, movement rows start with `#0`, `#1`; guides show where one room ends and the next begins.

**Step 5: Commit** — `git commit -m "Explorer: display hierarchy, contrast, de-repeated movement names"`

---

### Task 5: Tags out of the graph by default; filter control in fullscreen

Quartz's graph renders tag pages as nodes — that is the `#` noise. Default: tag nodes excluded. Fullscreen: a small "filter" button beside the graph's fullscreen button opens a chip row (one chip per top-level tag namespace, e.g. `argument-map`, `station`, `epi-logos`); chips toggle which namespaces are included, persisted in `localStorage`; a master chip re-enables all tag nodes.

**Files:**
- Modify: `site/vendor/quartz/quartz/components/Graph.tsx` (data step: skip nodes whose slug starts `tags/` unless filters include their namespace; fullscreen overlay: render chip row)
- Modify: `site/vendor/quartz/quartz/components/styles/graph.scss` (chip row styling, night ghost buttons)
- Modify: `site/tests/essay-host-smoke.py`

**Step 1: Write failing smoke assertions**

```python
graph_btn = page.locator('.global-graph-icon')
graph_btn.click()
expect(page.locator('.global-graph-outer')).to_be_visible()
assert page.locator('.global-graph-outer .tag-filter').count() == 1, 'no tag filter in fullscreen graph'
chip = page.locator('.global-graph-outer .tag-filter button').first
chip.click()  # toggle a namespace on
# local graph on reading pages carries no tag nodes:
page.goto(reading_url, wait_until='load')
# (graph is canvas — assert via the emitted filter state instead)
assert page.evaluate('localStorage.getItem("oi-graph-tags")') is not None
```

**Step 2: Verify failure.**

**Step 3: Implement.** In the graph data build, partition nodes into pages and `tag:` nodes (slug prefix `tags/`), derive namespaces from each tag node's first segment; render chips; filter the sim's node set on chip toggle. If upstream already exposes a `showTags`-style option, use it as the default-off switch and build only the chip row.

**Step 4: Verify** — smoke PASS; manual: fullscreen graph shows pages only by default, chips pull namespaces in, state persists.

**Step 5: Commit** — `git commit -m "Graph: tags out by default, fullscreen namespace filter"`

---

### Task 6: Full verification, ship, confirm in production

**Step 1:** `cd site && npm run build:public` (build + finalize contract)
**Step 2:** `npm run test:essay && npm run test:library` — all green
**Step 3:** `python3 tests/essay-host-smoke.py` — all green including new assertions
**Step 4:** Browser pass at 1440 and 390: reading page calm, toggles work, explorer legible, graph fullscreen filter works
**Step 5:** Branch → PR → self-merge (branch protection) → `vercel deploy --prod --yes --archive=tgz` from `site/dist` (deploy config restored by the build)
**Step 6:** Production curl matrix + browser confirmation; NOW return for the essay lane

**Evidence standing after this plan:** the movement page shows title → text, no chrome; sidebars fade on demand; explorer reads as a tree; the graph is page-shaped, with tags available on request in fullscreen.
