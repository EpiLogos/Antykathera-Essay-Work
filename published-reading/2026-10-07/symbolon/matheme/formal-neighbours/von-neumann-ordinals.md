---
title: "Von Neumann Ordinals — The Predecessors Retained"
record_id: matheme-von-neumann-ordinals
record_type: matheme
register: matheme
claim_status: "Derived (finite construction); Argued (QL relation)"
source_relation: "Paraphrased mathematical workbench; Argued from native QL"
source_ids:
  - kaplan-1999-nothing-that-is
  - taylor-2026-core-theorems-pithy
  - taylor-2026-mono-poly-two-ones
---

# Von Neumann Ordinals — The Predecessors Retained

## #0 — A zero that can be a member

The finite von Neumann construction begins with an exact object: the empty set, written `∅`. A set is determined by its members; the empty set has none. We represent the natural number zero by this set and define a successor operation:

$$
0:=\varnothing,\qquad S(n):=n\cup\{n\}.
$$

Braces form a set: `{n}` has the single member `n`. Union, `∪`, gathers the members of its two operands. Thus `n ∪ {n}` retains every member of `n` and adjoins `n` itself as one further member. These two operations, enclosure and union, do different work. Their composition makes each new number hold the entire preceding number alongside all its predecessors.

[Kaplan's housed mathematical workbench](../../episteme/sources/mathematics-logic/kaplan/kaplan-1999-nothing-that-is/kaplan-1999-nothing-that-is.md#reading) sources the essay's encounter with the nested construction, locating it at printed p.211 of the selected 2000 OUP printing. The explicit successor rule is worked here from its definition. Kaplan quotation and the primary historical attribution retain the source house's verification debt; no copied Kaplan wording is used.

## #1 — The first enclosure changes the count

Apply the rule to zero:

$$
S(0)=\varnothing\cup\{\varnothing\}
=\{\varnothing\}=:1.
$$

The result has one member, although that member has no members. The distinction lies between the set and what belongs to it. The emptiness of the member does not empty the containing set. Writing `|A|` for the number of members of a finite set `A`, we obtain

$$
|0|=0,\qquad |1|=1,\qquad 0\in1,\qquad 0\ne1.
$$

Membership, `∈`, is therefore already different from equality. It is also different from inclusion, `⊆`: `A ⊆ B` means every member of `A` is a member of `B`. The empty set is a subset of every set, including itself, because it has no member that could violate that condition. Yet `0 ∉ 0`, while `0 ∈ 1`. The first enclosure gives zero a new office without altering the object represented by zero.

This makes the count available to inspection. There is no hidden positive item inside the empty set. The positive count belongs to the singleton, whose one member is exactly that empty set.

## #2 — Successor keeps what enclosure alone would lose

Apply the same rule again:

$$
\begin{aligned}
2:=S(1)&=1\cup\{1\}\\
&=\{0\}\cup\{1\}\\
&=\{0,1\}=\{\varnothing,\{\varnothing\}\}.
\end{aligned}
$$

The two members are distinct: zero has no members, whereas one has zero as its member. Enclosing one by itself would instead give `{1} = {{∅}}`, a set with only one member. That repeated singleton is not the ordinal two. Successor must retain the preceding contents as well as enclose their whole.

The next steps expose the pattern:

$$
\begin{aligned}
3:=S(2)&=\{0,1\}\cup\{2\}=\{0,1,2\},\\
4:=S(3)&=\{0,1,2\}\cup\{3\}=\{0,1,2,3\}.
\end{aligned}
$$

Each result includes the preceding number in two distinct respects: `n ⊆ S(n)` because its members are retained, and `n ∈ S(n)` because the preceding whole is newly admitted as a member. This double retention is the construction's exact generative operation. Repetition neither consumes zero nor replaces all earlier numbers with an opaque container.

## #3 — The number is its ordered inheritance

At every finite stage,

$$
n=\{0,1,\ldots,n-1\},\qquad |n|=n.
$$

For zero the list is empty. If a stage contains exactly its distinct predecessors, adjoining that stage yields the list with one new entry. The induction also retains the sizes of the preceding stages. The constructed stage is not already one of its predecessors: it has `n` members, while each earlier stage has fewer. The successor therefore increases cardinality by one. This gives the induction from the empty starting case to every finite stage.

The ordering is internal to these objects. For finite ordinals `m` and `n`, `m < n` exactly when `m ∈ n`. In `3 = {0,1,2}`, the earlier numbers retain their own membership relations: zero belongs to one and two; one belongs to two. Three consequently holds its predecessors with the order already realised among them. Its displayed enumeration can be rearranged on the page without changing the set or that membership order.

This is an exact representation of the finite natural numbers. The worked construction supplies any specified finite stage. Taking the collection of all finite stages as a set requires the further set-theoretic provision for infinity; no such collection is needed for the finite claims made here.

## #4 — The numerical floor of the linking one

Taylor's [Mono–Poly manuscript](../../episteme/sources/internal-corpus/taylor/taylor-2026-mono-poly-two-ones/taylor-2026-mono-poly-two-ones.md) argues from this operation. The first positive one carries zero inside it, and the next step gathers zero and one while keeping their difference. The [core theorem spine](../../episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/taylor-2026-core-theorems-pithy.md), in §IX's linking-one synthesis, gives the relation its native symbolic reach: a determination carries an inherited condition inside the form through which it becomes countable. The singleton is the exact mathematical instance from which that comparison starts.

The correspondence concerns **retention through determination**, and its two objects belong to different registers. Here zero is an entirely specified set, available as an object of proof. In [A11, The Two Ones](../../../section-rooms/arguments/A11-The-Two-Ones-0-One-1-All.md), `0` bears the singular One, the non-objectifiable condition of determination, and `1` bears the polyvalent All. Set membership supplies neither that ontological assignment nor any proof that awareness is the empty set. It supplies an exact operation against which the native assignment can be compared.

The core's compression `2 = 0/1` reads the holding-together of zero and one symbolically, and its set-theoretic floor is `2 = {0,1}`. The slash of the compression names a retained relation, whereas ordinary division would give `0/1 = 0`. Keeping the two readings explicit leaves the author's comparison its full Argued force, and [Homology and Analogy](../../episteme/etymologies/homology-and-analogy/WHOLE-FIELD-homology-and-analogy.md) **qualifies** it by requiring the common operation and the different objects to stay in view together.

[Identification through difference](../../../section-rooms/arguments/A02-Copula-Self-Identity-through-Difference.md) **grounds** counting as an act: a new occurrence is distinguishable while the preceding count remains available. In [Mono/Poly](../../../section-rooms/arguments/A12-Mono-Poly-One-All-Whole-Many.md) a whole becomes legible through its real expressions while their containing relation stays. The set construction supplies the particular comparative operation, in which the earlier field persists when its whole becomes a new participant, and the further native operations have their own grounds beyond successor.

## #5→0 — The empty set remains exact on return

The [generation of one through the empty set](../../../section-rooms/02-return-of-zero/movements/15-s1-p2-empty-set-generates-one.md) **returns-to** this page for membership, inclusion and cardinality with their differences intact, and the linking-one relation keeps its mathematical floor recoverable step by step. In the [advent of zero](../../../section-rooms/arguments/A10-Advent-of-Zero.md), successor holds its own place among the generative procedures, beside the empty product, mediants and NOR, each under its own law.

[§1 · #5→0, The Loan Returns](../../../section-rooms/02-return-of-zero/movements/18-s1-p5-loan-returns.md), **extends** the achieved exactness. Zero stays present in every positive finite ordinal and acquires no members of its own, because the containing sets differ at each stage and the empty set does not gather their contents. The authorial return follows the condition through its determinations with that difference kept.

The [native eight-determination traversal](../../../section-rooms/arguments/A18-Primordial-Symbolon-and-Its-Eight-Determinations.md) carries the relation beyond this finite construction, and [Integral recognition](../../../section-rooms/arguments/A36-Advent-of-Integral-Zero.md) brings the acquired symbolic force back to the exact mathematical sign. The ordinal remains a set of predecessors, and its construction makes explicit the relation carried onward, that the next determination retains the field from which its count becomes possible.