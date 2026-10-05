---
title: Bring the ship surface to the expression law
label: wayfinder:task
status: closed
parent: ../maps/submission-day-readiness-2026-09-25.md
assignee: notation-agent-2026-09-25
blocked_by:
  - 035-reference-notes-quilt.md
  - 036-loose-concepts-reconciliation.md
created: 2026-09-25
---

# Bring the ship surface to the expression law

## Question

Enforce compliance with `submission-package/essay/quilt/ql-expression-grammar.md` (the expression law, 2026-07-29): `$$…$$` LaTeX display math for operated/derived relations; backticked Unicode tokens (`0/1`, `X/x`, `5→0`) for naming — Unicode inside backticks, never LaTeX commands; inline `\(…\)` retired everywhere; `X/x` remains Frank's authorial notation untouched.

Scope, in order:

1. `submission-package/essay/THE-RETURN-OF-ZERO.md` — the ~48 bare-Unicode lines (headings, prose arrows, footnote Ø/∅/S/s) and any surviving `\(…\)`. Bare *operated relations* become `$$…$$` display blocks (precedent: `working/sources-texts-references/10-7-2026-core-theorems-pithy.md`); bare *named tokens* get backticks; genuine prose arrows in ordinary sentences stay prose.
2. `section-rooms/` movements and room surfaces.
3. The canonical nodes (`section-rooms/arguments/`, `conjugate/`, `concepts/`, `products/`) — they barely use math; the work is backticking named tokens.
4. The matheme register (`symbolon/matheme/`).

Rules: this is transcription, not rewriting — nothing semantic changes. Where a token's operator/naming status is ambiguous, backtick it and leave the prose untouched, logging the line. Do NOT touch `working/` or `sources/`. Do not LaTeX-ify backticked tokens. No commits.

Verify: grep audits over touched files (zero `\(…\)` remaining; no bare occurrences of the known token set outside backticks/math), spot-diff 10 files.

Report → `.wayfinder/research/038-notation-report.md`: per-file conversion counts, logged ambiguities, verification output.

## Resolution

315 conversions (143 backticked tokens, 124 \(…\) retired, 48 display normalizations), 62 files, 20 ambiguities logged, X/x untouched; two manuscript section headings reverted to contract form by the integrator. Report: ../research/038-notation-report.md
