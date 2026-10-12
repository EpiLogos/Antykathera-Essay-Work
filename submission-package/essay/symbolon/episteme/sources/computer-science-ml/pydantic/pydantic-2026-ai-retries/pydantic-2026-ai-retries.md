---
source_id: pydantic-2026-ai-retries
title: Pydantic — Retries (Pydantic AI documentation, accessed 2026)
title_full: Retries
author:
- Pydantic
container_title: Pydantic AI documentation (Pydantic Docs)
publisher: Pydantic Services Inc.
year: 2026
url: https://pydantic.dev/docs/ai/core-concepts/retries/
accessed: '2026-10-05'
primary_domain: computer-science-ml
node_type: source-house
record_type: software-documentation
ownership: canonical-source-house
schema_version: 1
source_role:
- practitioner-documentation
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
# Pydantic — Retries (Pydantic AI documentation, accessed 2026)

## Bibliographic identity

The "Retries" page in the Core Concepts section of the Pydantic AI documentation. The older address https://ai.pydantic.dev/retries/ redirects (fetched 2026-10-05) to https://pydantic.dev/docs/ai/core-concepts/retries/, which is the object consulted. The page has no named author, no version number and no visible date; the footer reads "© Pydantic Services Inc. 2025 to present." It is living documentation for an actively released library, so the access date is load-bearing: the layer table may change between releases.

## Citation and consulted object

**Full note:** Pydantic, "Retries," Pydantic AI documentation, accessed October 5, 2026, https://pydantic.dev/docs/ai/core-concepts/retries/.

**Short note:** Pydantic, "Retries."

**Bibliography:** Pydantic. "Retries." Pydantic AI documentation. Accessed October 5, 2026. https://pydantic.dev/docs/ai/core-concepts/retries/.

**Provenance:** Publisher HTML fetched 2026-10-05 and converted to text; wording below checked in that text. Locators are by section heading.

<a id="passages"></a>
## Passages and excerpts

<a id="pydantic-2026-ai-retries-p001"></a>
### pydantic-2026-ai-retries-p001 — "Seven different things … at seven different layers"

**Locator:** Opening paragraph under the page title "Retries."

> "Retry" means seven different things in an agent run, at seven different layers, and they don't share budgets. Mixing them up is the usual cause of a run that retries far more (or far less) than expected.

**Context and use boundary:** The page calls itself "the map; each layer links to the page that configures it in detail." Curly quotation marks and apostrophes on the page are rendered here as straight ones.

**Status:** quotation-ready.

**Verification:** Exact wording checked in publisher HTML; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #4 (reworked draft, 2026-10-05).

<a id="pydantic-2026-ai-retries-p002"></a>
### pydantic-2026-ai-retries-p002 — The seven layers as the page's own table lists them

**Locator:** Section "The layers," table (columns: Layer · What it re-attempts · Configured with · What it adds to message history), rows in page order.

1. **Transport** — "The same HTTP request to the provider"; configured with `AsyncHTTPX2TenacityTransport` on your HTTP client; adds nothing to message history.
2. **Provider SDK** — "The same HTTP request, re-issued by the provider SDK's own client"; configured in the SDK client itself; adds nothing.
3. **Durable execution** — "The whole model request, re-executed by the workflow engine"; unbounded by default on Temporal (`maximum_attempts=0`); configured with Temporal `retry_policy`, DBOS `max_attempts`, or Prefect `retries`; adds nothing ("the engine replays the step").
4. **Model fallback** — "The same request against a different model"; `FallbackModel`; adds "Only the winning response."
5. **Tool** — "One tool call, by asking the model to correct it"; `retries={'tools': N}` and per-tool limits; adds a `RetryPromptPart` in place of the tool's result.
6. **Output** — "The model's final answer, by asking it to correct it"; `retries={'output': N}` and `ToolOutput(max_retries=N)`; adds a `RetryPromptPart`.
7. **Model-request hooks** — the model request, from `before_model_request`, `after_model_request`, `wrap_model_request` or `on_model_request_error` raising `ModelRetry`; draws on the output budget; adds a new request carrying a `RetryPromptPart`.

Sentence under the table, exact:

> Only the last three are "agent retries" — they cost a model round trip each, because a retry is another request. The other four are invisible to the model: it never sees an attempt fail.

**Count:** seven, stated by the page and matched by seven table rows. The earlier draft's list (network transport, provider SDK, durable model requests, fallback model, tool retries, output-validation retries, hooks) matches the page's seven, with two wording drifts: the page's row is "Durable execution" (what it re-attempts is "the whole model request"), and its row is "Output," not "output-validation" (the Output retries section says output retries are triggered "by validation failures, by an output function or output validator raising ModelRetry, and by a model response with nothing actionable in it" — validation is one trigger among three).

**Limiting detail:** The page lists Model fallback as a layer but heads a later section "Model fallback is not a retry": `FallbackModel` "never re-attempts the same one" and should be paired with transport retries, not used as a substitute. A further section, "What is never retried," names `prepare` callbacks, tool exceptions other than `ModelRetry` and `ToolFailed`, and "Whole agent runs. Nothing re-runs an agent for you."

**Status:** quotation-ready for the quoted sentence and the row phrases in quotation marks; row summaries outside quotation marks are paraphrase.

**Verification:** Table and sections read in publisher HTML; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #4 (reworked draft, 2026-10-05).

<a id="pydantic-2026-ai-retries-p003"></a>
### pydantic-2026-ai-retries-p003 — Retry multiplication: the layers stack

**Locator:** Section "Retry multiplication," first paragraph and worked example.

> The layers don't share budgets, but they stack: a retry at one layer wraps the attempts of every layer nearer the wire.

**Context and use boundary:** The page models one logical call as up to N×M×K wire requests (N model requests per logical call, M SDK attempts per request, K transport attempts per wire request), with durable execution re-entering M and K, "unbounded unless you set maximum_attempts yourself" on Temporal. Its worked example: output retries 2, OpenAI SDK default `max_retries=2`, and `stop_after_attempt(2)` "can put 3 × 3 × 2 = 18 requests on the network." `UsageLimits` "bounds only N."

**Status:** quotation-ready (the sentence quoted); worked example paraphrased with its quoted figure.

**Verification:** Exact wording checked in publisher HTML; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #4 (reworked draft, 2026-10-05).

## Essay uses

A framework's own documentation showing that, inside one agent run, "retry" names seven separately budgeted mechanisms, three of which the model sees (as correction prompts) and four of which it never sees. The essay may say the page counts seven; it should name the third layer "durable execution" and the sixth "output" as the page does, and note the page's own caveat that fallback is not a retry of the same model.

## Open acquisition and verification

The page carries no version. If a stable citation is needed, pin the documentation source file at a tagged release of the pydantic-ai GitHub repository and record the tag.

## Returns

This source serves: [§5 · #4 — Workcell — Situated Existence](../../../../../../section-rooms/06-objective-internality/movements/41-s5-p4-bimba-energy-fields.md).
