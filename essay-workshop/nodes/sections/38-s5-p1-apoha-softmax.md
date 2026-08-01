---
title: "§5 · #1 — Apoha, Softmax, and Argmax"
node_type: section
page_type: section-movement
station: "§5"
position: "#1"
sequence: 38
claim_status: Argued
evidence_status: technical-analogy
source_ids: [vaswani-et-al-2017-attention, siderits-tillemans-chakrabarti-2011-apoha, mcgilchrist-2022-resist-machine-apocalypse]
tags: [epi-logos/antikythera-essay, argument-map/live, argument-map/section, station/s5, position/p1]
---
# §5 · #1 — Apoha, Softmax, and Argmax

## Claim
A model output is constituted locally by alternatives it excludes: logits form a differential field, softmax produces relative weights, and sampling or argmax makes a mark.

## Warrant
The selection sequence is technically inspectable; [[Antykathera-Essay-Work/essay-workshop/sources-texts-references/source-bank/quotes/vaswani-et-al-2017-attention|Vaswani et al.]] anchors the attention-based architectural context. The sequence supplies a bounded analogue to [[Antykathera-Essay-Work/essay-workshop/nodes/concepts/apoha]] at the level of differential determination; it is not a historical or doctrinal identity.

## Exclusion that remembers

The Buddhist side deepens the analogy where it matters. Dignāga makes a term determinate through exclusion — "a word talks about entities only as they are qualified by the negation of other things" (*Sāmānyaparīkṣā*, via Tillemans) — and the double negation carries real weight: "cow" as *not non-cow* does not collapse into plain affirmation, because the two negations are of different kinds, nominally and verbally bound, so the excluded field is retained inside the meaning rather than cancelled by it. Apoha is exclusion that remembers. The technical fork in a language model runs the same distinction at the width of one operation: softmax retains the entire excluded field as a weighted distribution — every alternative present, ranked, recoverable — while argmax or sampling collapses it to the bare selected mark, and preference training then operates on the record of collapses. Exclusion that remembers against exclusion that cancels: the two logics of two at operation-width. To our knowledge the apoha–selection comparison has no peer-reviewed precedent (searches this cycle found none; the nearest item is an unrefereed preprint, deliberately not admitted as a source), so it is carried as the essay's own **Argued** bridge. It brings one further asymmetry the research vectors exploit: **argmax has no gradient**. Learning cannot flow through the bare cut; it flows through the retained field around the cut — the technical face of the claim that the meditative dimension is generative of the computational, and the design ground for treating objective internality's two modalities as distinct offices with a return between them: a calculative office that selects, a meditative office that keeps the excluded field, the provenance, and the ground. McGilchrist's essayistic observation that AI replicates "the functions of the left hemisphere at frightening speed" is the contemporary witness of what a selection-only office looks like when it runs ungoverned, and enters only as such.

## Tension / limit
The analogy is licensed at the level of differential selection: each output remains defined against alternatives represented in a probability field. Semantic, social, and soteriological meaning require further registers and sources, while provenance requires the system to retain how alternatives, gauges, prompts, and contexts shaped the selection rather than merely retaining every token. Source debt: softmax, sampling, and the apoha comparison require their own fixed technical and primary-text passages before quotation.

## Anchor and transition
**QL trace:** selected `1`, relevant excluded field `0`, and the contextual slash that made the contrast operative. This turns “reasoning” from a retrospective story into a partially inspectable differentiation history. Those contrasts inhabit [[39-s5-p2-j-space|§5 · #2 — J-Space]].
