---
title: "Chinese Remainder: Six as Two by Three"
record_id: matheme-crt-z6
record_type: matheme
register: matheme
claim_status: Derived
source_relation: "Explicit mathematical proof; argued native comparison"
---

# Chinese Remainder: Six as Two by Three

## #0 — State the rings and the map

Let `ℤ/nℤ` denote integer residue classes modulo `n`. Define

`φ:ℤ/6ℤ→ℤ/2ℤ×ℤ/3ℤ`, `φ([k]₆)=([k]₂,[k]₃)`.

This [Chinese-remainder construction](../../../section-rooms/arguments/concepts/reference-notes/chinese-remainder-theorem-z6.md) **compares** as an exact finite counterpart of the [native binary/ternary account](../../episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/taylor-2026-core-theorems-pithy.md), and the explicit map and proof below earn the comparison. A historical quotation of the theorem would need its own source.

## #1 — Enumerate all six images

| k mod 6 | mod 2 | mod 3 |
|---|---|---|
|0|0|0|
|1|1|1|
|2|0|2|
|3|1|0|
|4|0|1|
|5|1|2|

Every pair in the two-by-three product occurs exactly once. If a representative changes by a multiple of 6, both residues stay unchanged, so the map is well-defined.

## #2 — Construct the inverse

For `a mod2` and `b mod3`, set `ψ(a,b)=3a+4b mod6`. Modulo 2 this is `a`, and modulo 3 it is `b`. Changing `a` by 2 or `b` by 3 changes the expression by a multiple of 6, so this map is also well-defined.

For example, the pair `(1,2)` gives `3+8=11≡5 mod6`. The pair `(0,1)` gives 4. These recover the table's corresponding entries, proving surjectivity and a two-sided inverse.

## #3 — Preserve the operations

Reduction modulo 2 and modulo 3 each preserves integer addition and multiplication. Consequently `φ(k+l)=φ(k)+φ(l)` and `φ(kl)=φ(k)φ(l)`, with componentwise operations in the product. The map also preserves 1, making it a ring isomorphism.

Coprimality carries the result. With moduli 2 and 4, a residue's mod 2 value is forced by its mod 4 value, so the pair `(1 mod2,0 mod4)` cannot occur. The two coordinates are independent in the present construction because `gcd(2,3)=1`.

## #4 — Retain the algebraic boundary

`ℤ/6ℤ` is not a field: the nonzero classes 2 and 3 multiply to 0. Under `φ`, they become `(0,2)` and `(1,0)`, whose componentwise product is `(0,0)`. This exposes the product's zero-divisor structure directly.

The native sixfold can receive this as an exact binary/ternary decomposition. What the isomorphism says is that six residues form exactly the product ring of the coprime two-residue and three-residue systems. Assigning personhood, harmonic meaning or QL positions to the residues is a further step and needs its declared maps.

## #5→0 — Return the pair to one address

Passage runs both ways without loss: one mod 6 address becomes two independent residues, and `3a+4b` recovers the address. [Translations](../mono-poly/translations.md) thereby gain a concrete bijective example beside the maps that discard information.

The [native sixfold](../../../section-rooms/arguments/A18-Primordial-Symbolon-and-Its-Eight-Determinations.md) keeps its qualitative assignments through the declared coordinate mapping. [Perfect six](../harmonics/perfect-six.md) **compares** another route to the same number, the proper divisors `1+2+3=6`, and [the Spanda relation](../../../section-rooms/04-mathematical-substrate/movements/26-s3-p1-spanda-4-2.md) carries its own binary/ternary and ratio offices. In each comparison the coprime product ring preserves its addition and multiplication.