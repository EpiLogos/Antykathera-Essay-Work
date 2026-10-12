---
source_id: deepseek-ai-2025-deepseek-r1-model-card
title: DeepSeek-AI — DeepSeek-R1 model card (Hugging Face, 2025)
title_full: DeepSeek-R1
author:
- DeepSeek-AI
container_title: Hugging Face
publisher: Hugging Face (repository deepseek-ai/DeepSeek-R1)
year: 2025
publication_date: '2025-01-20'
revision: 56d4cbbb4d29f4355bab4b9a39ccb717a14ad5ad (2025-03-27)
url: https://huggingface.co/deepseek-ai/DeepSeek-R1
accessed: '2026-10-05'
primary_domain: computer-science-ml
node_type: source-house
record_type: model-card
ownership: canonical-source-house
schema_version: 1
source_role:
- primary-technical-release
metadata_status: object-verified
edition_status: revision-pinned
citation_status: citation-ready
quote_status: quotation-ready
chicago_ready: true
citation_style: chicago-notes-bibliography-18
passage_surface: '#passages'
consumed_by_sections:
- §5
---
# DeepSeek-AI — DeepSeek-R1 model card (Hugging Face, 2025)

## Bibliographic identity

The model card (README.md) of the Hugging Face repository `deepseek-ai/DeepSeek-R1`. The Hugging Face API (queried 2026-10-05) gives the repository as created 2025-01-20 (commit "Release DeepSeek-R1," 2025-01-20) and the current `main` revision as `56d4cbb` ("Small fix," 2025-03-27); the card text read here is the README at `main`. The repository's metadata tags the license as `mit`. The card's sections are numbered 1–9; "7. License" is the section carded below. The accompanying technical report is linked from the card ("Paper Link") and is a separate object.

## Citation and consulted object

**Full note:** DeepSeek-AI, "DeepSeek-R1," model card, Hugging Face, January 20, 2025, revised March 27, 2025, https://huggingface.co/deepseek-ai/DeepSeek-R1.

**Short note:** DeepSeek-AI, "DeepSeek-R1."

**Bibliography:** DeepSeek-AI. "DeepSeek-R1." Model card. Hugging Face, January 20, 2025. Revised March 27, 2025. https://huggingface.co/deepseek-ai/DeepSeek-R1.

**Provenance:** Raw README fetched 2026-10-05 from https://huggingface.co/deepseek-ai/DeepSeek-R1/raw/main/README.md; revision and dates from the Hugging Face model and commits API the same day. The README carries its own Markdown links; the link targets are given in the context notes, not in the quotations.

<a id="passages"></a>
## Passages and excerpts

<a id="deepseek-ai-2025-deepseek-r1-model-card-p001"></a>
### deepseek-ai-2025-deepseek-r1-model-card-p001 — Code and weights under MIT; commercial use and distillation allowed

**Locator:** Section "7. License," first two sentences.

> This code repository and the model weights are licensed under the MIT License. DeepSeek-R1 series support commercial use, allow for any modifications and derivative works, including, but not limited to, distillation for training other LLMs.

**Context and use boundary:** "MIT License" links to https://github.com/deepseek-ai/DeepSeek-R1/blob/main/LICENSE. The licence sentence names the code repository and the weights; the card says nothing about releasing or licensing training data. The sentence is followed by "Please note that:" and the three distilled-model clauses in p002.

**Status:** quotation-ready.

**Verification:** Exact wording checked in the raw README at revision 56d4cbb; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #1 (reworked draft, 2026-10-05).

<a id="deepseek-ai-2025-deepseek-r1-model-card-p002"></a>
### deepseek-ai-2025-deepseek-r1-model-card-p002 — Distilled models keep their base models' licences

**Locator:** Section "7. License," the three bullet points after "Please note that:".

> - DeepSeek-R1-Distill-Qwen-1.5B, DeepSeek-R1-Distill-Qwen-7B, DeepSeek-R1-Distill-Qwen-14B and DeepSeek-R1-Distill-Qwen-32B are derived from Qwen-2.5 series, which are originally licensed under Apache 2.0 License, and now finetuned with 800k samples curated with DeepSeek-R1.
> - DeepSeek-R1-Distill-Llama-8B is derived from Llama3.1-8B-Base and is originally licensed under llama3.1 license.
> - DeepSeek-R1-Distill-Llama-70B is derived from Llama3.3-70B-Instruct and is originally licensed under llama3.3 license.

**Context and use boundary:** The card states the origin licences of the bases ("originally licensed under"); it does not itself say which licence governs the fine-tuned distilled checkpoints. Each distilled model has its own repository and card, which should be checked before any claim about the distills' current licence. Section "3. Model Downloads" gives the base of the Qwen 1.5B and 7B distills as Qwen2.5-Math-1.5B and Qwen2.5-Math-7B, which the licence section groups under "Qwen-2.5 series."

**Status:** quotation-ready.

**Verification:** Exact wording checked in the raw README at revision 56d4cbb (Markdown link syntax removed); agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #1 (reworked draft, 2026-10-05).

<a id="deepseek-ai-2025-deepseek-r1-model-card-p003"></a>
### deepseek-ai-2025-deepseek-r1-model-card-p003 — What was opened

**Locator:** Section "1. Introduction," final paragraph.

> To support the research community, we have open-sourced DeepSeek-R1-Zero, DeepSeek-R1, and six dense models distilled from DeepSeek-R1 based on Llama and Qwen.

**Status:** quotation-ready.

**Verification:** Exact wording checked in the raw README at revision 56d4cbb; agent, 2026-10-05.

**Relation:** Extracted.

**Consumer:** §5 · #1 (reworked draft, 2026-10-05).

## Essay uses

A reasoning model released with code and weights under the MIT License, with commercial use and "distillation for training other LLMs" explicitly allowed, while the card notes that the six distilled models derive from bases originally licensed under Apache 2.0 (Qwen-2.5) and the llama3.1 and llama3.3 licences. The essay's political reading of open weights is its own; "open-sourced" is the card's word and a licence on code and weights is not a release of training data, which the card does not mention.

## Open acquisition and verification

If the essay states the licence of a specific distilled checkpoint, read that checkpoint's own Hugging Face card and LICENSE.

## Returns

This source serves: [§5 · #1 — Actuation — Living Articulation](../../../../../../section-rooms/06-objective-internality/movements/38-s5-p1-apoha-softmax.md).
