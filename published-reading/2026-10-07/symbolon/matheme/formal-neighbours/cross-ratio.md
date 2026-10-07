---
title: "Cross-Ratio under Fractional-Linear Transformation"
record_id: matheme-cross-ratio
record_type: matheme
register: matheme
claim_status: Derived
source_relation: "Explicit mathematical construction; argued native comparison"
---

# Cross-Ratio under Fractional-Linear Transformation

## #0 — Fix the ordered convention

For four distinct finite complex points, define

`λ(z₁,z₂;z₃,z₄)=((z₁−z₃)(z₂−z₄))/((z₁−z₄)(z₂−z₃))`.

The order and convention are explicit because other conventions permute this value. [Bilinear invariance](../../episteme/sources/mathematics-logic/nist/nist-dlmf-2026-complex-variable/nist-dlmf-2026-complex-variable.md) **sources** the transformation class under which the cross-ratio stays unchanged. The [native ratio-of-ratios](../../episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/taylor-2026-core-theorems-pithy.md) holds the whole relation in its two obverse orientations, and the comparison developed below sets the two signatures side by side.

## #1 — State the transformation

Let `f(z)=(az+b)/(cz+d)` with complex coefficients and determinant `Δ=ad−bc≠0`. At finite points away from its pole,

`f(u)−f(v)=Δ(u−v)/((cu+d)(cv+d))`.

This follows by expanding the two numerators. The nonzero determinant prevents the map from collapsing to a constant and ensures that distinct projective points remain distinct.

## #2 — Cancel the shared factors

Substitute the difference identity into the four factors of λ. Two factors of Δ occur in the numerator and two in the denominator. Each factor `cz_i+d` also occurs once on both sides. All cancel, leaving the original λ.

The result extends to the sphere through homogeneous coordinates or the corresponding limits at ∞. It holds for the stated fractional-linear maps, and a nonlinear transformation of the plane in general does not preserve it.

## #3 — Work a quadruple and a permutation

For `(z₁,z₂,z₃,z₄)=(0,1,2,3)`, `λ=((-2)(-2))/((-3)(-1))=4/3`. Apply `f(z)=z+5`; every difference is unchanged, so the value remains 4/3.

Swapping the first two inputs instead gives 3/4, the reciprocal. Ordering therefore matters even though the underlying set of four points is unchanged. Taking `z₄→∞` in the chosen convention gives `λ=(z₁−z₃)/(z₂−z₃)`.

For a counterexample outside the transformation class, square the four real inputs. Their images are 0, 1, 4, 9, with cross-ratio `((-4)(-8))/((-9)(-3))=32/27`, different from 4/3. A transformation can preserve distinctness on this finite set without preserving its cross-ratio.

## #4 — Preserve the native comparison's boundary

The exact object is an ordered projective invariant. Its ratio-of-ratios form matches the native `(0/1)/(1/0)` at one stated level, that of nested ratios whose parts stand in an exact relation. Its entries are differences of distinct points with controlled denominators, whereas the native stroke deliberately keeps arithmetic's defined/undefined seam, so the two ratios of ratios differ in what they relate.

An identification of the two would have to map the objects and preserve the operations, and the look of nested fractions supplies no such map. [Complex orientation](../ql/complex-orientation.md) gives another invariant under a different group, the modulus under rotations, and its preservation law is likewise its own.

## #5→0 — Return the invariant through its group

The result is a quantity that survives a specified transformation and keeps its ordered relational information. Giving the map, the determinant condition and the quadruple makes the invariance checkable, and makes its failure outside that class equally exact.

[Projective reframing](../../../section-rooms/04-mathematical-substrate/movements/28-s3-p3-projective-dimensional-reframing.md) **extends** the invariant with its specific transformations. The [projective line](../topology/projective-line.md) **grounds** the containing-space construction, and [translation](../mono-poly/translations.md) **compares** these mathematical objects with the native relation by stating which operations correspond. The map and the operation it preserves are the measure of that comparison.