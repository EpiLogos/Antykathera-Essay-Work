---
source_id: agent-skills-2025-specification
title: Agent Skills — Specification (open standard, 2025–)
title_full: Specification
author:
- Agent Skills
container_title: Agent Skills
publisher: Agent Skills (agentskills.io; format originally developed by Anthropic)
year: 2025
url: https://agentskills.io/specification
accessed: '2026-10-05'
primary_domain: computer-science-ml
node_type: source-house
record_type: technical-specification
ownership: canonical-source-house
schema_version: 1
source_role:
- technical-standard
metadata_status: object-verified
edition_status: living-document-access-dated
citation_status: citation-ready
quote_status: quotation-ready
chicago_ready: true
citation_style: chicago-notes-bibliography-18
passage_surface: '#passages'
consumed_by_sections:
- §5
---
# Agent Skills — Specification (open standard, 2025–)

## Bibliographic identity

The "Specification" page of the Agent Skills site (agentskills.io), subtitled on the page "The complete format specification for Agent Skills." The site states, under "Open development" on its overview page (https://agentskills.io/home): "The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products." It points to a GitHub organisation (github.com/agentskills/agentskills) and Discord for contributions. No named author, version number or visible date appears on the specification page. The page's embedded metadata gives `dateModified` 2026-08-04T22:53:14Z; this is not displayed text, so the citation uses the access date.

Release date of the open standard: Anthropic's engineering post "Equipping Agents for the Real World with Agent Skills" (published October 16, 2025) carries the line "Update: We've published Agent Skills as an open standard for cross-platform portability. (December 18, 2025)." That post is a separate object; cite it separately if the date is used in prose.

## Citation and consulted object

**Full note:** Agent Skills, "Specification," accessed October 5, 2026, https://agentskills.io/specification.

**Short note:** Agent Skills, "Specification."

**Bibliography:** Agent Skills. "Specification." Accessed October 5, 2026. https://agentskills.io/specification.

**Provenance:** Specification and overview pages fetched as HTML 2026-10-05 and converted to text; wording below checked in that text. Locators are by section heading.

<a id="passages"></a>
## Passages and excerpts

<a id="agent-skills-2025-specification-p001"></a>
### agent-skills-2025-specification-p001 — A skill is a directory with SKILL.md

**Locator:** Specification, "Directory structure" and "SKILL.md format."

> A skill is a directory containing, at minimum, a SKILL.md file:

> The SKILL.md file must contain YAML frontmatter followed by Markdown content.

**Context and use boundary:** The directory diagram marks `SKILL.md` "Required: metadata + instructions" and `scripts/` ("executable code"), `references/` ("documentation") and `assets/` ("templates, resources") as optional. The frontmatter table makes `name` (max 64 characters; lowercase letters, numbers, hyphens) and `description` (max 1024 characters; "Describes what the skill does and when to use it") required; `license`, `compatibility`, `metadata` and `allowed-tools` (marked "Experimental") are optional. The section headed "Optional directories" calls its conventions "recommendations."

**Status:** quotation-ready.

**Verification:** Exact wording checked in the page text; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

<a id="agent-skills-2025-specification-p002"></a>
### agent-skills-2025-specification-p002 — Progressive disclosure: only name and description at startup

**Locator:** Specification, "Progressive disclosure."

> Agents load skills progressively, pulling in more detail only as a task calls for it.

> Metadata (~100 tokens): The name and description fields are loaded at startup for all skills

> Instructions (< 5000 tokens recommended): The full SKILL.md body is loaded when the skill is activated

> Resources (as needed): Files (e.g. those in scripts/, references/, or assets/) are loaded only when required

**Context and use boundary:** The three-tier list is stated as the structure skills "should" take advantage of; the token figures are approximate ("~100") or recommendations ("< 5000 tokens recommended"). The section adds "Keep your main SKILL.md under 500 lines." The overview page names the same stages Discovery, Activation and Execution. How a given agent product implements loading is outside the specification's text.

**Status:** quotation-ready.

**Verification:** Exact wording checked in the page text (list items carry no terminal punctuation on the page); agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

<a id="agent-skills-2025-specification-p003"></a>
### agent-skills-2025-specification-p003 — Origin and openness (overview page)

**Locator:** Agent Skills overview (https://agentskills.io/home), "Open development."

> The Agent Skills format was originally developed by Anthropic, released as an open standard, and has been adopted by a growing number of agent products. The standard is open to contributions from the broader ecosystem.

**Context and use boundary:** Self-description by the standard's own site; the adoption claim is the site's, not independently measured. This sentence is on the overview page, a sibling page of the same site; cite it as Agent Skills, "Agent Skills Overview," accessed October 5, 2026, https://agentskills.io/home (page title "Agent Skills Overview") if quoted.

**Status:** quotation-ready.

**Verification:** Exact wording checked in the overview page text; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #2 (reworked draft, 2026-10-05).

## Essay uses

The format in which standing procedure is packaged for an agent: a folder whose required file carries a short name and description loaded up front, with the body and any bundled scripts or references read only when a task calls for them. The essay's reading of this as the institutional shape of agent know-how is its own.

## Open acquisition and verification

If the essay states the December 18, 2025 open-standard date, open a house for Anthropic's engineering post (https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills), where the dated update line was read 2026-10-05.

## Returns

This source serves: [§5 · #2 — AIKit — Potency](../../../../../../section-rooms/06-objective-internality/movements/39-s5-p2-j-space.md).
