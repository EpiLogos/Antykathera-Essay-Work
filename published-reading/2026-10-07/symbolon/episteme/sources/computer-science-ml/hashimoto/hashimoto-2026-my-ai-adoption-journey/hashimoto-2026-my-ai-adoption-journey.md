---
source_id: hashimoto-2026-my-ai-adoption-journey
title: Hashimoto — My AI Adoption Journey (2026)
title_full: My AI Adoption Journey
author:
- Mitchell Hashimoto
container_title: Mitchell Hashimoto (blog)
publisher: Mitchell Hashimoto
year: 2026
publication_date: '2026-02-05'
url: https://mitchellh.com/writing/my-ai-adoption-journey
accessed: '2026-10-05'
primary_domain: computer-science-ml
node_type: source-house
record_type: blog-post
ownership: canonical-source-house
schema_version: 1
source_role:
- practitioner-testimony
metadata_status: object-verified
edition_status: dated-public-object
citation_status: citation-ready
quote_status: quotation-ready
chicago_ready: true
citation_style: chicago-notes-bibliography-18
passage_surface: '#passages'
consumed_by_sections:
- §5
---
# Hashimoto — My AI Adoption Journey (2026)

## Bibliographic identity

A first-person blog post by Mitchell Hashimoto (co-founder of HashiCorp; author of the Ghostty terminal), published on his personal site. The page header and footer both carry the date February 5, 2026; no update notice appears. The post states that it was "fully written by hand." It is organised as six numbered steps ("Drop the Chatbot", "Reproduce Your Own Work", "End-of-Day Agents", "Outsource the Slam Dunks", "Engineer the Harness", "Always Have an Agent Running") and a closing "Today" section, with four footnotes. Metadata and text were verified from the publisher's HTML, fetched 2026-10-05.

## Citation and consulted object

**Full note:** Mitchell Hashimoto, "My AI Adoption Journey," *Mitchell Hashimoto* (blog), February 5, 2026, https://mitchellh.com/writing/my-ai-adoption-journey.

**Short note:** Hashimoto, "My AI Adoption Journey."

**Bibliography:** Hashimoto, Mitchell. "My AI Adoption Journey." *Mitchell Hashimoto* (blog), February 5, 2026. https://mitchellh.com/writing/my-ai-adoption-journey.

**Provenance:** Publisher HTML fetched 2026-10-05 and converted to text; wording below checked in that text. Web page, no pagination; locators are by step heading and paragraph.

<a id="passages"></a>
## Passages and excerpts

<a id="hashimoto-2026-my-ai-adoption-journey-p001"></a>
### hashimoto-2026-my-ai-adoption-journey-p001 — Doing the work twice

**Locator:** "Step 2: Reproduce Your Own Work," second paragraph.

> Instead of giving up, I forced myself to reproduce all my manual commits with agentic ones. I literally did the work twice. I'd do the work manually, and then I'd fight an agent to produce identical results in terms of quality and function (without it being able to see my manual solution, of course).

**Context and use boundary:** The method was a learning device, adopted after he "initially wasn't impressed" with Claude Code; he calls it "excruciating." The same step adds that he "found the edges of what agents -- at the time -- were good at," and that part of the gain was "understanding when not to reach for an agent." He reports reaching parity, not speed-up, at this stage.

**Status:** quotation-ready.

**Verification:** Exact wording checked in publisher HTML; transcription by text conversion of the HTML, line breaks removed; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

<a id="hashimoto-2026-my-ai-adoption-journey-p002"></a>
### hashimoto-2026-my-ai-adoption-journey-p002 — What the doubled work taught: planning, task size, verification

**Locator:** "Step 2: Reproduce Your Own Work," the three lessons following "But, expertise formed."

> Break down sessions into separate clear, actionable tasks. Don't try to "draw the owl" in one mega session.

> For vague requests, split the work into separate planning vs. execution sessions.

> If you give an agent a way to verify its work, it more often than not fixes its own mistakes and prevents regressions.

**Context and use boundary:** He presents these as things he "discovered for myself from first principles" that "others were already saying." They are practitioner findings, not measured results.

**Status:** quotation-ready.

**Verification:** Exact wording checked in publisher HTML; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

<a id="hashimoto-2026-my-ai-adoption-journey-p003"></a>
### hashimoto-2026-my-ai-adoption-journey-p003 — Protecting attention: notifications off

**Locator:** "Step 4: Outsource the Slam Dunks," fourth paragraph.

> Very important at this stage: turn off agent desktop notifications. Context switching is very expensive. In order to remain efficient, I found that it was my job as a human to be in control of when I interrupt the agent, not the other way around. Don't let the agent notify you.

**Context and use boundary:** The paragraph continues: "During natural breaks in your work, tab over and check on it, then carry on." The next paragraph ties working on something else to the "skill formation" question (he refers to an Anthropic paper without naming it); footnote 3 says skill formation "particularly in juniors" deeply worries him. At this stage he ran background agents "one at a time, not in parallel."

**Status:** quotation-ready.

**Verification:** Exact wording checked in publisher HTML; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

<a id="hashimoto-2026-my-ai-adoption-journey-p004"></a>
### hashimoto-2026-my-ai-adoption-journey-p004 — Harness engineering: instructions written from failures, tools that tell the agent it is wrong

**Locator:** "Step 5: Engineer the Harness," first, second and fourth paragraphs and the two listed forms.

> The most sure-fire way to achieve this is to give the agent fast, high quality tools to automatically tell it when it is wrong.

> It is the idea that anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again.

> Each line in that file is based on a bad agent behavior, and it almost completely resolved them all.

**Context and use boundary:** "That file" is the AGENTS.md of Ghostty, which he links. He names two forms: "Better implicit prompting (AGENTS.md)" and "Actual, programmed tools," for example "scripts to take screenshots, run filtered tests." He coins "harness engineering" tentatively ("I don't know if there is a broad industry-accepted term for this yet"). The step closes on a double aim: preventing the agent from repeating "a Bad Thing" and letting agents "verify they're doing a Good Thing."

**Status:** quotation-ready.

**Verification:** Exact wording checked in publisher HTML; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

<a id="hashimoto-2026-my-ai-adoption-journey-p005"></a>
### hashimoto-2026-my-ai-adoption-journey-p005 — Limiting passage: one agent, a goal not yet met

**Locator:** "Step 6: Always Have an Agent Running," third and fourth paragraphs.

**Located operation (paraphrase):** He is not running multiple agents and does not currently want to; one agent balances deep manual work against "babysitting" it. The always-running goal is "still just a goal": by his estimate a background agent runs for 10 to 20 percent of a normal working day.

**Status:** paraphrase-only (located and read; captured as paraphrase for the qualifying use).

**Verification:** Read in publisher HTML; agent, 2026-10-05.

**Relation:** Paraphrased.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

## Essay uses

A practitioner's own account of how competence with agents was formed: doing the work twice to learn where an agent helps; explicit planning and task size; standing instructions written in answer to observed failures; tools that let the agent find its own errors; and the human deciding when to look. p005 limits the testimony: one engineer, one agent at a time, a stated personal practice, not a study. The essay's reading of these practices is its own.

## Open acquisition and verification

None required for the cards above. If the essay names the Anthropic skill-formation paper he alludes to, that paper needs its own house.

## Returns

This source serves: [§5 · #2 — AIKit — Potency](../../../../../../section-rooms/06-objective-internality/movements/39-s5-p2-j-space.md).
