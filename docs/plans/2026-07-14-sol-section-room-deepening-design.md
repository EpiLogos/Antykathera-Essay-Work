# Sol Section Room Deepening — Design Contract

## Purpose

The section room is the human collation surface for writing *Return of Zero*. It must hold enough depth that Frank can enter a section, feel its argument and resonance as a whole, and write by tone, pressure, and intuition without reopening the entire vault graph.

Luna and Sol have distinct responsibilities:

- **Luna** acquires and verifies evidence. It owns source identity, locators, quotation readiness, and the evidence board.
- **High-freedom composition** performs section-scale synthesis. It turns the canonical movement graph and verified evidence into a deep room dossier, a first scholarly form, and a visual argument programme.
- **Frank** owns the prose. `10-FRANK-DRAFT.md` is sovereign and must remain byte-for-byte unchanged unless Frank explicitly requests prose editing.

## Artifact flow

```text
canonical nodes + source bank + Luna evidence
                    |
                    v
          05-ROOM-DOSSIER.md       protected Sol synthesis
             /          \
            v            v
00-SECTION-CONTEXT.md   20-SCHOLARLY-EDITION.md
 generated refraction   protected editorial form
                         \
                          v
                   30-PLATE-AND-DIAGRAMS.md
                   protected visual argument
```

The builder owns `00-SECTION-CONTEXT.md` and `.section-room.json`. Sol never edits either directly: it deepens the protected dossier and then invokes the builder to refract that work into the generated context and provenance manifest.

## Required depth

Every room must preserve all six movements while making their cumulative logic readable. For each movement Sol reconstructs:

1. claim;
2. warrant;
3. counterpressure or limit;
4. evidence function and readiness;
5. paragraph burden;
6. incoming dependency and outgoing transition.

Relations are typed as `dependency`, `seed`, `echo`, `development`, `payoff`, `counterpressure`, or `resonance`. Resonance is never promoted into warrant.

The scholarly surface is not a summary. It is an initial publishable architecture: section headings, paragraph sequence, evidence deployment, quote slots, proof boundaries, plate calls, and editorial debts.

The plate surface is not an illustration wishlist. Each plate must name its argumentative consumer, logical job, visual relation, caption proposition, accessibility description, source or rights burden, status, and failure modes.

## Runtime truth

The work requires explicit permission for high-freedom section-scale synthesis. It does not depend on, record, or claim a selectable subagent model identity.

## Baseline finding

An unskilled baseline produced substantial argument, scholarly, and plate material but exposed the architectural failure this skill must prevent: it wrote directly into the generated context, created no protected synthesis/provenance layer, and left the room manifest stale. The skill therefore optimises for both intellectual depth and correct ownership. Neither is sufficient without the other.

## Completion gates

- Frank's draft hash is unchanged.
- The dossier, scholarly surface, and plate programme cover all six movements.
- The generated context is rebuilt from the dossier and `--check` reports no stale room.
- Every quotation resolves to a quotation-ready Luna artifact; citation-ready material is not silently treated as quotable.
- Every plate is attached to a named argumentative burden.
- The room records what changed, what remains unresolved, and what should be handed back to Luna.
- No canonical claim, source relation, or cross-room dependency is silently inflated.
