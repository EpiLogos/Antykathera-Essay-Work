---
title: 'Shumailov et al. — AI Models Collapse When Trained on Recursively Generated Data (2024)'
source_id: shumailov-et-al-2024-model-collapse
node_type: source-house
ownership: canonical-source-house
record_type: journal-article
source_role:
- technical-primary
citation_style: chicago-notes-bibliography-18
metadata_status: verified
edition_status: not-applicable
citation_status: citation-ready
quote_status: quotation-ready
chicago_ready: true
author:
- 'Ilia Shumailov'
- 'Zakhar Shumaylov'
- 'Yiren Zhao'
- 'Nicolas Papernot'
- 'Ross Anderson'
- 'Yarin Gal'
title_full: 'AI Models Collapse When Trained on Recursively Generated Data'
container_title: 'Nature'
year: '2024'
volume: '631'
page_range: '755–759'
doi: '10.1038/s41586-024-07566-y'
url: 'https://doi.org/10.1038/s41586-024-07566-y'
consumed_by_sections:
- §5→0
consumed_by_arguments: []
primary_domain: computer-science-ml
schema_version: 1
passage_surface: '#passages'
tags:
- epi-logos/antikythera-essay
- source-bank/record
---

# Shumailov et al. — AI Models Collapse When Trained on Recursively Generated Data (2024)

## Bibliographic identity

Open-access article, *Nature* 631 (25 July 2024): 755–59. Publisher PDF downloaded from nature.com on 2026-10-05; masthead, authors, volume and first page read from p. 755.

## Chicago 18 forms

**Full note:** Ilia Shumailov et al., "AI Models Collapse When Trained on Recursively Generated Data," *Nature* 631 (2024): {page}, https://doi.org/10.1038/s41586-024-07566-y.

**Shortened note:** Shumailov et al., "AI Models Collapse," {page}.

**Bibliography:** Shumailov, Ilia, Zakhar Shumaylov, Yiren Zhao, Nicolas Papernot, Ross Anderson, and Yarin Gal. "AI Models Collapse When Trained on Recursively Generated Data." *Nature* 631 (2024): 755–59. https://doi.org/10.1038/s41586-024-07566-y.

## Source scholarship

The paper trains successive generations of generative models (Gaussian mixtures, variational autoencoders, language models) on data produced by earlier generations and shows a degenerative process it names model collapse: the tails of the original distribution disappear first and later generations converge toward a narrow estimate.

<a id="passages"></a>
## Passages and excerpts

<a id="shumailov-et-al-2024-model-collapse-q001"></a>
## Passage card — `shumailov-et-al-2024-model-collapse-q001` — Tails of the original distribution disappear
^shumailov-et-al-2024-model-collapse-q001

> "We find that indiscriminate use of model-generated content in training causes irreversible defects in the resulting models, in which tails of the original content distribution disappear. We refer to this effect as ‘model collapse’ and show that it can occur in LLMs as well as in variational autoencoders (VAEs) and Gaussian mixture models (GMMs)."

- **Locator:** p. 755, abstract.
- **Status:** quotation-ready.
- **Verification:** agent, 2026-10-05; transcribed from the publisher's born-digital PDF.
- **Source relation:** Extracted.
- **Evidential action:** supports.
- **Consumers:** §5→0 · #0 (reworked draft, 2026-10-05).
- **Use boundary:** A finding about recursive training on generated data under the paper's conditions; the reading of collapse as cancellation of the origin is the essay's.

<a id="shumailov-et-al-2024-model-collapse-q002"></a>
## Passage card — `shumailov-et-al-2024-model-collapse-q002` — Access to the original distribution is crucial
^shumailov-et-al-2024-model-collapse-q002

> "We note that access to the original data distribution is crucial: in learning tasks in which the tails of the underlying distribution matter, one needs access to real human-produced data."

- **Locator:** p. 755, introduction.
- **Status:** quotation-ready.
- **Verification:** agent, 2026-10-05; born-digital PDF.
- **Source relation:** Extracted.
- **Evidential action:** qualifies (the remedy is access to the origin, not a better summary).
- **Consumers:** §5→0 · #0 (reworked draft, 2026-10-05).
- **Use boundary:** Technical remedy within the paper's setting.

## Essay uses

§5→0 · #0 (reworked draft, 2026-10-05): a handover that hands on only the handover.

## Open acquisition and verification

None for the essay's use.

## Returns

This source serves: [§5→0 · #0 — From Theory to Vocation](../../../../../../section-rooms/07-instrument-returns/movements/43-s50-p0-theory-vocation-compassion.md).
