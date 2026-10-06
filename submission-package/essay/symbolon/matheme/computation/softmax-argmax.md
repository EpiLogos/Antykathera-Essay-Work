---
title: "Softmax and Argmax"
record_id: matheme-softmax-argmax
record_type: matheme
register: matheme
claim_status: Derived
source_relation: "Exact technical construction; argued native relation and offered experimental application"
---

# Softmax and Argmax

## #0 — Declare the finite score field

Let `z=(z₁,…,z_n)` be finite real logits with `n≥1`, and let temperature `T>0`. Define

`p_i=exp(z_i/T)/Σ_j exp(z_j/T)`.

[PyTorch 2.9’s operators](../../episteme/sources/computer-science-ml/pytorch/pytorch-2-9-softmax-argmax-api/pytorch-2-9-softmax-argmax-api.md) separate three operations: softmax, which normalises the logits into a distribution; argmax, which selects an index; and the tie rule by which argmax takes the first maximal index. This record **sources** its mathematics there. The question it asks of that mathematics is the [native one about selection and the retained field](../../episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/taylor-2026-core-theorems-pithy.md): whether a selected result stays related to the alternatives and the rule through which it became determinate.

## #1 — Normalise and shift

Every exponential is positive and their finite sum is positive, so `p_i>0` and `Σ_i p_i=1`. Adding a common real constant `c` to every logit changes numerator and denominator by the same factor `exp(c/T)`; it therefore leaves every probability unchanged.

For a stable numerical implementation, subtract `max(z)` before exponentiation. This is the same invariance used to prevent overflow, not an approximation to another distribution. Finite-precision underflow can still set extremely small computed entries to zero even though the mathematical probabilities remain positive.

## #2 — Work one distribution

At `T=1`, take `z=(0,ln2,ln4)`. Exponentiation gives weights `(1,2,4)`, hence `p=(1/7,2/7,4/7)`. Adding 10 to all logits yields the same distribution. At `T=2`, the weights become `(1,√2,2)`, changing the probabilities while retaining their ordering.

Argmax returns a maximum index, here the third coordinate. Sampling from the distribution can return any coordinate, with its stated probability. The distribution, maximum selection and random draw are three different outputs.

## #3 — Resolve the limiting cases

Let `M=max(z)` and let `k` entries attain M. Rewrite the probabilities using `z_i−M`. As `T→0+`, maximal entries have numerator 1 and all others tend to 0, so each maximum receives mass `1/k`. A unique maximum gives a one-hot limit; tied maxima do not.

For `z=(0,0,−1)`, the limit is `(1/2,1/2,0)`. PyTorch's documented argmax instead chooses the first maximal index. As `T→∞`, all exponentials approach 1 and the distribution tends to uniform `1/n`. These are limits of the family; the defining expression does not set `T=0`.

## #4 — Retain the field around the cut

Choosing the index `k` out of `n` is a cut in the sense of dia-ballein: the other `n−1` coordinates are set aside, and so is the margin by which `k` won. What travels with the cut decides whether the answer can be examined afterwards. If we keep the logits or probabilities, the temperature, the candidate set and the selection rule, the chosen index can be checked against the field it came from. If we keep only the index, most of that field has been discarded and the answer arrives without its conditions. [Preference gauge](preference-gauge.md) **extends** the same concern one level up, to the invariance of comparisons between answers.

Two boundaries come from the sources. The API source establishes operators and nothing about a deployed LLM pipeline, so it cannot establish that softmax is apoha, and what an output token means depends on its actual model, context and use. And the quilt's proposal to cool the temperature toward selection and then reopen it is a technical candidate whose effect has to be tested, because changing the temperature alone revises neither the representation nor the evaluator.

## #5→0 — Return with the selection rule visible

Softmax and argmax together give an exact distinction between a retained distribution and an actual cut. The distribution holds all `n` probabilities in their order; the cut holds one index. A returned decision can therefore state what was selected, from which field, and under which temperature and tie or sampling rule, and its correctness can be examined without taking the selected index to contain its own conditions.

The movement on [apoha and softmax](../../../section-rooms/06-objective-internality/movements/38-s5-p1-apoha-softmax.md) is where this specified selection **grounds** a comparison with the apoha account of meaning, each side keeping its own semantic or technical warrant. In the two logics, [dia-ballein](../dia-syn/dia.md) makes the cut actual, which is argmax, and [syn-ballein](../dia-syn/syn.md) retains and gathers the field through which the result can return, which is the distribution kept beside the choice. [Operational parity](operational-parity.md) **tests** the engineering side: retained information has to change behaviour before any advantage is claimed for keeping it.
