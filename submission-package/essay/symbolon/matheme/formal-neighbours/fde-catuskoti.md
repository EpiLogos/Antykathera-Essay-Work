---
record_id: matheme-fde-catuskoti
title: "FDE, four-valued logic and catuṣkoṭi"
record_type: matheme
register: matheme
claim_status: Argued
formal_standing: "Derived: four-valued operations and consequence; Argued: native crossing and comparative return"
source_relation: "Paraphrased: Priest's reconstruction; Argued from: Taylor's native crossing; Paraphrased at recorded reception depth: Priest 2018 and Kapsner 2020"
source_ids: [priest-2010-logic-catuskoti, priest-2018-fifth-corner, kapsner-2020-cutting-corners, taylor-2026-core-theorems-pithy, taylor-2026-binary-explication]
---
# FDE, four-valued logic and catuṣkoṭi

## #0 — Two independent supports

A proposition can have support for its truth, support for its falsity, both, or neither. FDE makes these possibilities exact by permitting the two supports to vary independently. Write a value as a pair of bits $(a_T,a_F)$, or equivalently a subset of $\{T,F\}$:

| Status | Set | Pair | Reading |
|---|---|---|---|
| $t$ | $\{T\}$ | $(1,0)$ | true only |
| $f$ | $\{F\}$ | $(0,1)$ | false only |
| $b$ | $\{T,F\}$ | $(1,1)$ | both |
| $n$ | $\varnothing$ | $(0,0)$ | neither |

The bits here record semantic support; they need not describe a person's beliefs. An ordinary FDE valuation assigns exactly one of these four statuses to each formula. Assigning $b$ is therefore one status assignment containing both supports, not two competing assignments. Assigning $n$ still assigns a value: the absence of both supports belongs inside the semantics.

[[symbolon/episteme/sources/mathematics-logic/priest/priest-2010-logic-catuskoti/priest-2010-logic-catuskoti#priest-2010-logic-catuskoti-q003|Priest's formal reconstruction]] supplies this fourfold neighbour of the catuṣkoṭi. Its first gain is a precise place for contradiction and indeterminacy within one calculus. Their different consequences can now be calculated.

## #1 — The diamond has a direction

Negation exchanges the two supports. Conjunction requires both truth supports but either falsity support; disjunction requires either truth support but both falsity supports:

$$
\neg(a_T,a_F)=(a_F,a_T),
$$
$$
a\land c=(a_T\land c_T,\ a_F\lor c_F),\qquad
 a\lor c=(a_T\lor c_T,\ a_F\land c_F).
$$

The operations on the right are ordinary Boolean operations on bits. They produce these complete tables:

| $a$ | $\neg a$ |
|---|---|
| $t$ | $f$ |
| $f$ | $t$ |
| $b$ | $b$ |
| $n$ | $n$ |

| $\land$ | $t$ | $f$ | $b$ | $n$ |
|---|---|---|---|---|
| $t$ | $t$ | $f$ | $b$ | $n$ |
| $f$ | $f$ | $f$ | $f$ | $f$ |
| $b$ | $b$ | $f$ | $b$ | $f$ |
| $n$ | $n$ | $f$ | $f$ | $n$ |

| $\lor$ | $t$ | $f$ | $b$ | $n$ |
|---|---|---|---|---|
| $t$ | $t$ | $t$ | $t$ | $t$ |
| $f$ | $t$ | $f$ | $b$ | $n$ |
| $b$ | $t$ | $b$ | $b$ | $t$ |
| $n$ | $t$ | $n$ | $t$ | $n$ |

Conjunction is meet and disjunction join in the **truth order**: $f$ is bottom, $t$ is top, and $b,n$ are incomparable between them. Formally, $a\leq_t c$ means $a_T\leq c_T$ and $c_F\leq a_F$. Increasing truth support and decreasing falsity support move upward.

Set inclusion gives a different, information order: $n$ is bottom, $b$ is top, and $t,f$ are incomparable. Confusing these diamonds changes the calculus. For example, FDE gives $b\land n=f$ and $b\lor n=t$; intersection and union of their support sets instead give $n$ and $b$. Truth combination does not simply accumulate information.

## #2 — Contradiction without arbitrary consequence

The designated values are $D=\{t,b\}$: those containing truth support. Semantic consequence preserves designation:

$$
\Gamma\models_{\mathrm{FDE}} A
\quad\Longleftrightarrow\quad
\text{every valuation designating every member of }\Gamma\text{ designates }A.
$$

Take $v(p)=b$ and $v(q)=n$. Both $p$ and $\neg p$ are designated, while $q$ is not. This one valuation proves

$$
p,\neg p\not\models_{\mathrm{FDE}}q.
$$

The contradiction is retained without licensing an unrelated conclusion. Conjunction elimination nevertheless survives: if $p\land q$ has truth support, the defining first coordinate requires truth support for each conjunct. Thus $p\land q\models p$. Nonexplosion has a determinate inferential shape, rather than suspending inference altogether.

The gap has its own consequence. At $v(p)=n$, both negation and disjunction return $n$, so $p\lor\neg p$ is not valid. The failure of excluded middle and the failure of explosion arise at different assignments. Four statuses preserve that difference.

They must also be distinguished from four object-language formulas. At $p=b$, the formulas $p$, $\neg p$, and $p\land\neg p$ are all designated. Their designation does not make them exclusive corners. Exclusivity belongs to the classification of a valuation as true-only, false-only, both, or neither. This separation of a status from an assertion about it is essential to the formal reconstruction.

## #3 — What adding a fifth changes

[[symbolon/episteme/sources/mathematics-logic/priest/priest-2010-logic-catuskoti/priest-2010-logic-catuskoti#priest-2010-logic-catuskoti-q004|Priest's further construction]] introduces an ineffable status $e$, outside the four-value lattice. In the infectious extension, $\neg e=e$, and a conjunction or disjunction with an $e$ input yields $e$. This is an additional semantic rule. Nothing in the preceding four-valued tables generates a fifth output or requires one.

In particular, $e\neq n$. The value $n$ already means neither truth nor falsity support within the specified fourfold. Introducing $e$ changes the range of evaluation to mark another status; it does not discover an unoccupied subset of $\{T,F\}$.

[[symbolon/episteme/sources/mathematics-logic/priest/priest-2010-logic-catuskoti/priest-2010-logic-catuskoti#priest-2010-logic-catuskoti-q005|Plurivalence changes a second feature]]: evaluation becomes a relation rather than a single-valued function. A formula can stand in that relation to both $t$ and $e$. The collection $\{t,e\}$ is a plurality of semantic statuses; it is not the original status $b=\{T,F\}$. One construction enlarges the available values; the other permits multiple value assignments. A consequence relation for the enlarged construction requires its own designation and preservation conditions. The FDE nonexplosion calculation above proves exactly what it states without deciding those further conditions.

## #4 — The crossing changes the relation to judgment

The [[symbolon/episteme/sources/internal-corpus/taylor/taylor-2026-binary-explication/taylor-2026-binary-explication|Binary Explication]] **sources** a crossing that begins before any proposition is tested. At #0 appearing is already known, and only afterwards does that situation become something to be asserted or denied. IS affirms that awareness and phenomenon are inseparable, and IS-NOT keeps their difference. BOTH holds identity and difference together, and NEITHER exposes the limit of treating that holding as a position from which the whole could be possessed.

These are four successive pressures on **0/1**, and the slash carries the changes of respect through which their assertions belong to one relation. FDE and the crossing answer different questions. FDE gives an exact account of simultaneous positive and negative support for a proposition. The crossing asks how the situation that supports assertion is itself encountered, through affirmation, negation, their conjunction and their limit. Through [[section-rooms/arguments/A13-Two-Logics-of-Two-Dia-Syn|Dia/Syn]], distinguishing and binding stay internally related operations in both. The four mathematical statuses keep their own formal definition beside the native relation.

The [[symbolon/episteme/sources/internal-corpus/taylor/taylor-2026-core-theorems-pithy/taylor-2026-core-theorems-pithy|native theorem]] holds the generating two inside **2+2²**, and FDE's four combinations of support bits **compare** exactly with the squared term, the four ways two terms can meet. The bits have a fixed office, truth support and falsity support, while the native One and All keep their own generating relation. The [[section-rooms/arguments/A18-Primordial-Symbolon-and-Its-Eight-Determinations|whole eight-determination traversal]] **grounds** the comparison by giving this local resemblance the relation within which it carries weight.

## #5→0 — SILENCE carries the crossing back

In the native definition SILENCE belongs at **#5**, Real-isation. It gathers the four corners as lived texture and returns to **#0**, encounter. It is called the fifth because it comes after the crossing, and it adds no fifth truth value. Neither $n$, the semantic gap, nor $e$, the added ineffable status, performs that return by being assigned to a formula, since the native **5→0** is an operation by which the same situation is encountered again with its distinctions included. The [[section-rooms/arguments/A34-Idealism-Order-of-Dependence|order of dependence]] **grounds** the difference: the field of appearing gives the situation in which logical values can be selected at all. [[section-rooms/arguments/A36-Advent-of-Integral-Zero|Integral recognition]] carries the achieved return, and counts no further object.

The historical comparison stays answerable to its evidence. [[symbolon/episteme/sources/mathematics-logic/kapsner/kapsner-2020-cutting-corners/kapsner-2020-cutting-corners#kapsner-2020-cutting-corners-q001|Kapsner's verified abstract]] challenges the fifth value and announces an alternative, and the abstract gives no details of that alternative. The [[symbolon/episteme/sources/mathematics-logic/priest/priest-2018-fifth-corner/priest-2018-fifth-corner|recorded reception of Priest's book]] also contains presupposition-failure readings and objections to treating the Buddhist contexts uniformly. That QL #0 is no value answers a particular conflation, and the separate historical questions stay open, so Priest's reconstruction is no consensus.

The enlargement of [[section-rooms/04-mathematical-substrate/movements/28-s3-p3-projective-dimensional-reframing|logical space]] specified here carries two independent supports, four statuses, exact connectives and truth-preserving consequence without explosion. Altering a calculus and accounting for its ground are different operations, as [[section-rooms/arguments/A03-Immutable-Gap-Formal-Limit|the formal-limit argument]] **derives**. The lived passage through SILENCE gathers the formal work back into the conscious circumstance in which judgment occurs.