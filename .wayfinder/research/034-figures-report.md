# Ticket 034 — Episteme figures: report

**Ticket:** `.wayfinder/tickets/034-figures-episteme-figures.md` (assignee set: `figures-agent-2026-09-25`)
**Date:** 2026-09-25
**Home:** `submission-package/essay/symbolon/episteme/figures/`
**Contract sources read first:** `.agents/skills/return-of-zero-visuals/SKILL.md`; `episteme/figures/README.md`; `quilt/ql-expression-grammar.md`

## Records landed

Four figure pairs (record + asset), all original own-work SVG, all anchored to named canonical records read before drawing:

| Figure | Asset | Record | Governing record anchored |
|---|---|---|---|
| The straight Vāk layering of the four registers | `vak-register-layering.svg` | `vak-register-layering.md` | central plan (mythic rule + Amendment 2026-09-07); A06 — Vāk; A06′ |
| Objective Internality: the six paired product disclosures | `objective-internality-paired-disclosures.svg` | `objective-internality-paired-disclosures.md` | S0–S5 frontmatter (`mef_pair`, `movement`); A/C root C face; central plan §5; §5 P1-CANONICAL-ALIGNMENT |
| Bimba / pratibimba: the relational office | `bimba-pratibimba-relational-office.svg` | `bimba-pratibimba-relational-office.md` | C38; retained carrier `concepts/bimba-pratibimba.md`; A32, C55, A34, C60, A26, A22; M44, M48 |
| The canonical A/C suite and its traversal by the rooms | `ac-suite-field-shape.svg` | `ac-suite-field-shape.md` | A/C root ("inherited 137-record shared suite"); rooms README (8×6=48); the eight P1-CANONICAL-ALIGNMENT files; directory census performed 2026-09-25 |

Each record carries: proposition, declared data (inputs), construction method/transformations, invariant, proof boundary and omissions, status (Derived/Argued/Offered vocabulary, compound where honest), anchored records, caption carrying the operation, alt text, rights (original own-work). The ticket's blocked_by (028) is satisfied: the canonical suite now lives at `section-rooms/arguments/` and all anchors resolve there.

## Verification performed

- Frontmatter YAML-parses for all four records; required fields present.
- All four SVGs are well-formed XML and were rendered (Chrome headless + Quick Look) and visually corrected: label collisions removed, status-band overflows split, right-rail connectors extended, long lens names shrunk to fit their boxes.
- Every markdown link in every record resolves to an existing file (link depth corrected: records sit three levels under `essay/`).
- Census for figure 4 verified by directory count on 2026-09-25: 36 A files, 36 conjugate files, 64 canonical `C##-` records, 1 A/C root, 48 movement files, 8 P1 alignments, 7 product records.
- No existing files edited; no builders run; no commits. The only touched existing file is the ticket itself (assignee).

## Wiring list (embedding is NOT done — for the owning agents)

1. **vak-register-layering** → `symbolon/README.md` (register overview); `section-rooms/README.md` (generated — wire via `build-section-rooms.py` source, not hand edit); M44 if the register/Vāk relation is named; manuscript framing if it states the register architecture.
2. **objective-internality-paired-disclosures** → `06-objective-internality/P1-CANONICAL-ALIGNMENT.md` (beside the section-burden list); `arguments/products/S-World-and-Life.md`; `THE-RETURN-OF-ZERO.md` §5 if it renders the six products.
3. **bimba-pratibimba-relational-office** → C38 §#2–#3; `concepts/bimba-pratibimba.md` (formalises its plain-text office schema); M44; A32 or the Instrument-Returns alignment.
4. **ac-suite-field-shape** → `section-rooms/arguments/README.md`; rooms README "The canonical argument field" (generated — wire via builder source); A/C root "Hangs beneath it" declaration; `symbolon/episteme/README.md` canonical-field section.

## Notes and debts

- Figure 2's index-sum invariant (`n + (5−n) = 5`) is declared in its record as this record's Derived checksum over the declared pairs, not a canonical derivation.
- Figure 2 inherits the product records' standing: T25 developed/reconstituted, **T26 ratification pending** — stated in the record and the figure's status band.
- Figure 3 keeps the compound status honest: mirror Derived within QL; Śaiva exegesis Argued from source-matched, not quotation-verified, passages; Bimba Map Offered.
- Figure 4's annex renders the declared rule that S + S0–S5 (7 records; 144 shared records once materialised) stay outside the 137.
- Nothing stopped; all four candidates from the ticket were produced (3–5 targeted).
