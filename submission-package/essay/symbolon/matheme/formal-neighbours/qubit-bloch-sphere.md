---
title: "A Pure Qubit and the Bloch Sphere"
record_id: matheme-qubit-bloch-sphere
record_type: matheme
register: matheme
claim_status: Derived
source_relation: "Explicit mathematical construction; argued native comparison"
---

# A Pure Qubit and the Bloch Sphere

## #0 — State the state-space model

Take a normalized complex vector `|ψ⟩=α|0⟩+β|1⟩`, with `|α|²+|β|²=1`, and identify vectors differing by a common phase `e^{iγ}`. This defines pure qubit rays, the projective space `ℂP¹`. The [legacy qubit provenance](../../../section-rooms/arguments/concepts/reference-notes/qubit-bloch-sphere.md) **historicises** the presence of this geometry beside the native field, and as a bibliography seed it adds no physical or historical result.

The [NIST house](../../episteme/sources/mathematics-logic/nist/nist-dlmf-2026-complex-variable/nist-dlmf-2026-complex-variable.md) **sources** the complex sphere and nothing of quantum physics. The equations on this page specify the quantum state model directly, and any experimental or historical claim about quantum mechanics needs a source beyond that geometric house.

## #1 — Remove the common phase

A ray can be represented as

`|ψ⟩=cos(θ/2)|0⟩+e^{iφ}sin(θ/2)|1⟩`,

with `0≤θ≤π` and `φ` modulo `2π`. At the poles the azimuth is irrelevant. Its Bloch vector is

`r=(sinθ cosφ,sinθ sinφ,cosθ)`.

The squared components sum to 1. Thus the pure states form a sphere, with computational basis states at opposite poles. The poles are a coordinate choice, and they make no identification of the native zero and one with physical substances.

## #2 — Work phase and probability separately

For `|+⟩=(|0⟩+|1⟩)/√2`, the Bloch vector is `(1,0,0)`. For `|−⟩=(|0⟩−|1⟩)/√2`, it is `(−1,0,0)`. Both give squared amplitudes 1/2 and 1/2 in the computational basis, but their relative phase distinguishes orthogonal rays.

A global minus sign changes neither ray nor Bloch vector. A relative minus sign can change both. Saying only “half zero and half one” therefore loses state information and confuses a coherent pure state with a probability mixture.

## #3 — Distinguish the ball of mixed states

A density matrix for a qubit has the form `ρ=(I+r·σ)/2`, with Pauli matrices `σ`. Its eigenvalues are `(1±|r|)/2`, so positivity requires `|r|≤1`. Pure states lie on the boundary `|r|=1`; interior points are mixed states.

The equal mixture `ρ=I/2` has `r=0`, whereas `|+⟩⟨+|` has `r=(1,0,0)`. Both have equal diagonal entries in the computational basis, but the pure state's off-diagonal terms retain coherence. The sphere and ball are consequently different state spaces.

## #4 — Locate the exact geometric relation

On the chart `α≠0`, use `z=β/α`; the other chart uses `w=α/β`. In this Bloch convention, `r_z=(1−|z|²)/(1+|z|²)`, so `z=0` is the north pole. The companion Riemann-sphere page uses the opposite sign for its vertical coordinate; the two sphere displays differ by that reflection. Their overlap has `w=1/z`, the [projective-line](../topology/projective-line.md) transition. Antipodal Bloch vectors represent orthogonal pure states, whereas opposite normalized vectors in Hilbert space represent the *same* ray, so “opposite” carries two different meanings here and the two must be kept apart.

The [quilt's explicit correction](../../../quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md) **qualifies** the comparison by separating quantum superposition from `0/0` potency and from the native AND/OR operation. The geometry is a formal neighbour of the [core's](../../episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/taylor-2026-core-theorems-pithy.md) ontology, observerhood and subjectivity, and it neither originates them nor offers empirical proof of them.

## #5→0 — Return through the representation

The result is a complete parameterisation of pure states and an explicit boundary for mixed states. The coordinate poles, the common phase and the relative phase each do a different job, and keeping them apart is what makes the comparison usable.

[Dimensional reframing](../../../section-rooms/04-mathematical-substrate/movements/28-s3-p3-projective-dimensional-reframing.md) **returns-to** this page for a pure-state ray whose representation ignores common phase and responds to relative phase. [The Riemann sphere](../topology/riemann-sphere.md) **compares** as the geometric neighbour with its own chart convention, and [translations](../mono-poly/translations.md) record the change of convention and the separate mixed-state boundary. The native comparison inherits this separation of operations. A physical experiment or a historical account of quantum theory would each need its own witness, and the derived state-space construction supplies neither.
