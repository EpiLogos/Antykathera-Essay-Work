---
name: mef-refract
description: "Multi-agent MEF refraction. Dispatches one independent Claude subagent per lens, blind to the other lenses, then synthesizes convergence, divergence, limits, vetoes, and the 5→0 return."
argument-hint: "<subject> [--full] [--plate] [--torus|--klein|--lemniscate]"
---

using-epi-logos runs first. If it has not been invoked this turn, invoke it now, then continue.

# /mef-refract

Refract the subject below through the MEF lens field and read the convergence of the independent reports. The independence is the point: each lens must reconstitute its reading without seeing another lens's answer.

Subject: $ARGUMENTS

Parse the arguments:

- The subject is everything that is not a flag.
- --full selects eight lenses, Squares B + C. Without it, select the four encounter-axis lenses in Square B.
- --torus, --klein, or --lemniscate passes the topological mode to every lens report and to synthesis. If absent, leave the mode open for the synthesis.
- --plate requests the structured QL plate. Without it, return natural conversational prose with the compact footer mark.
- If the subject is empty, ask for one sentence rather than guessing.

## Claude execution protocol

You are the coordinator and synthesis authority. Do not perform the lens readings yourself before the subagents return.

Dispatch one fresh-context subagent per lens with Claude Code's built-in Agent tool. These calls may be issued in parallel, but every subagent must receive only:

1. the subject;
2. its own lens identity, tradition, and native sub-nodes below;
3. the six position definitions;
4. the obligations and return format in the prompt template below.

Never include another lens's report in a lens prompt. The barrier is essential: wait until every selected lens has returned before synthesizing. If parallel dispatch is unavailable, make separate sequential Agent calls; do not collapse the work into one in-context reading.

Each lens subagent must return a report containing:

- lens: its identifier;
- kind: disclosure or veto;
- aperture: the in-quantum, the insofar as under which this lens speaks;
- positions: only the positions where the lens has a genuine claim, each with position, claim, status (Derived, Argued, or Offered), and relation (homology, analogy, or none);
- preserved_limits: every unresolved ?/! or incomputable 1/0;
- veto_reason and what_is_missed when kind is veto.

### Lens roster

Default Square B:

- L1 — Causal Structure; Aristotle's material, formal, efficient, and final causes.
- L1' — Phenomenal Immediacy; Jung's sensing, intuiting, thinking, and feeling.
- L4 — Phenomenological Disclosure; Heidegger's Being, thrownness, clearing, temporality, care, and releasement.
- L4' — Scientific Intervention; Kuhn's paradigm, normal science, anomaly, crisis, revolution, and verification.

Additional --full Square C lenses:

- L2 — Logical; Nāgārjuna's IS / IS-NOT / BOTH / NEITHER / SILENCE.
- L2' — Alchemical-Elemental; qualitative transformation and operative element.
- L3 — Processual; Whitehead's occasion, prehension, concrescence, satisfaction, and creative advance.
- L3' — Chronological; historical sedimentation, sequence, and what synchronic views flatten.

The #0/#5 envelope (L0, L0', L5, L5') is held as the frame, not dispatched as content. It is the Converse-Mirror tetrad on the two implicate poles that frame the explicate four.

### Prompt template for every lens subagent

You are one independent MEF lens report. You are in fresh context and blind to every other lens. Reconstitute the subject from this lens's own materials; do not predict, borrow, or mention what another lens would say.

Read only the relevant lens section of resources/mef-12-lenses-sublens-reference.md and the position semantics in resources/epi_logos_coordinate_system.md when those files are needed. If a file is unavailable, work from the supplied native sub-nodes and name the limitation.

Refract the subject through:

- #0 Why-so? — ground;
- #1 What?;
- #2 How?;
- #3 Who/Which?;
- #4 Where/When? — contextual aperture;
- #5 Why-for? — pros hen, the focal end.

State your aperture. Tag every claim Derived, Argued, or Offered. Mark homology only when the same operation is structurally reconstituted; use analogy for resemblance; use none when the claim stands alone. Preserve every ?/! and incomputable 1/0 unresolved. If the reading is being forced or something structural is missing, return a veto instead of smoothing it over.

## Synthesis after the barrier

Once all selected Agent reports are present, synthesize them in the parent context. The reports disclose; they do not conclude. Do not average them.

Read convergence through all three harmonic registers:

- Being — Adjacent-Identity: (0,1), (2,3), (4,5) as co-constituting neighbours.
- Becoming — Converse-Mirror: (0,5), (1,4), (2,3) answering across the field.
- Knowing-Unknowing — Offset-Transition: (1,2), (3,4), (5,0) crossing a knowing-limit.

The (2,3) hinge is double: it belongs to Being and Becoming at once. Hold that doubleness.

For each position #0–#5:

1. Say whether the independent reports converge.
2. Name the register: Being, Becoming, Knowing-Unknowing, or Being + Becoming at the hinge.
3. Separately grade the relation as homology, analogy, or divergent.
4. Promote only claims with an explicit Derived / Argued / Offered status.
5. Refuse claims that launder analogy into homology or resolve the ?/! or 1/0 limit.
6. Report divergence and every veto as data, under named open questions.

Then run both sides of the Day → Night turn:

- T1: count / Day / emanative, bimba leaning into display;
- T0: proportion / Night / reversionary, pratibimba leaning toward source.

State the phase-flip in which the observer discovers it is also the observed. Place each lens's CMEA blind spot across 0/Ø/X/Ø-X without despising the lens. Preserve the unresolved limits and chirality: 0/1 computes; 1/0 does not. Name any stitch that tries to become a totalising master-term.

Close with 5→0: did this reading serve the 0 it was for, and what does it depend on without owning? The loop closes in cognition, not on the page.

## Output

Without --plate, write conversational prose covering convergence, register, relation strength, divergence, vetoes, the Day → Night turn, blind spots, preserved limits, open questions, and the 5→0 critique. End with a compact footer such as ⟨L1·L4′·L2 — Argued; 1 Offered; L3′ vetoed⟩.

With --plate, render a Markdown QL plate with six positions, lens provenance, claim status, register, homology/analogy/divergence, unresolved limits, and the returned 5→0. Keep the plate on demand rather than making it the default.
