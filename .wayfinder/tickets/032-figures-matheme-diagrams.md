---
title: Figures production I — matheme diagrams
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: diagrams-agent-2026-09-25
blocked_by:
  - 028-migrate-canonical-suite-into-section-rooms.md
created: 2026-09-25
---

# Figures production I — matheme diagrams

## Question

Produce the first real diagram set in `submission-package/essay/symbolon/matheme/diagrams/` (currently an empty contract-bearing home), per `.agents/skills/return-of-zero-visuals/SKILL.md` and that directory's README contract.

- Resolve the matheme-side legacy image briefs from `working/legacy/v1/nodes/images/` (promissory glyph plate `(0/1)/(1/0)`, Sheffer stroke reduction, re-entry/projective fork, 4-2 attunement stack), plus diagram needs arising from the matheme register and the essay's operated relations — e.g. the notation chain `` `0 → Ø → X → Ø/X → (0/Ø)/(1/X) → 1 → 0/1` ``, the atlas-of-charts display in §5, and the concentric-mandala layout for QL units that `quilt/ql-expression-grammar.md` canonises.
- Each figure is a record `.md` + asset pair, co-located. The record declares: proposition, inputs, transformations, invariant, proof boundary, essay blocks (NAMED movements under `section-rooms/<room>/movements/` — read them first so the anchor is genuine), caption, alt text, source dependencies, rights (original own-work).
- Assets are generated originals — SVG via Python/graphviz or hand-authored SVG. No scraped images; no rights risk.
- Target 4–6 diagrams this pass. Embedding into sections is NOT this ticket — produce the wiring list in the report.
- Display math inside records follows the expression law: `$$…$$`, backticked Unicode tokens for naming.

No commits; no builders; no suite runs.

Report → `.wayfinder/research/032-diagrams-report.md`: records landed, the movement-anchored wiring list, briefs left unresolved and why.

## Resolution

6 diagram record+asset pairs landed, render-checked, movement-anchored; wiring list in report. Report: ../research/032-diagrams-report.md
