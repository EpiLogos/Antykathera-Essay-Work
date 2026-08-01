# Epi-Card QL Conjugate System v1.0

This package contains the normative, implementation-ready product and system specification for the Epi-Card platform. Its invariant semantic frame is the full conjugate traversal `P0…P5 → P0′…P5′ → P0⁺`; the six visible hexagon edges bind the six pairs `Pn↔Pn′`, while film, symbol, audio, audit, and return preserve all twelve addresses.

## Primary document

- `SPEC.md` — complete product, domain, data, agent, media, interaction, production, deployment, and acceptance specification.

## Machine-oriented supplements

- `database/postgres.sql` — canonical production relational schema.
- `database/sqlite.sql` — portable/offline package schema.
- `contracts/` — the QL/render/provider/package/envelope schemas, all 132 action payload schemas, the 66-action runtime registry, and the 22-predicate gate registry.
- `examples/` — schema-valid reference instances for the QL frame, action request, render plan, provider capability, and portable package manifest.
- `api/openapi.yaml` — harness-neutral action service boundary.
- `architecture/action-catalog.md` — normative shared action catalogue.
- `database/action-definitions.postgres.sql` and `database/action-definitions.sqlite.sql` — generated action registry seeds.
- `scripts/generate-action-registry.py` and `scripts/generate-action-payloads.py` — reproducible contract generators; generated files are not hand-edited.
- `architecture/module-contracts.md` — module ownership, dependencies, and interfaces.
- `architecture/decision-register.md` — explicit requirement/fixed/configuration/scope decision register.
- `skills/epi-card/` — Agent Skills-compatible operating skill and reference layout.
- `ui/epi-card.d.ts` — framework-neutral Web Component/TypeScript contract.
- `okf/EXPORT_PROFILE.md` — SQL-to-OKF v0.2 wiki artifact export profile.
- `acceptance/ACCEPTANCE_TESTS.md` — build-completion test matrix.
- `research/CURRENT_TECH_BASIS.md` — dated implementation research basis.

## Normative precedence

1. `SPEC.md`
2. Database DDL and contract schemas
3. Action/API catalogues
4. Reference skill and UI declarations
5. Examples and research notes

Where a supplement conflicts with `SPEC.md`, the specification governs and the supplement must be corrected.

## Release verification

- `release/VALIDATION_REPORT.md` and `release/VALIDATION_REPORT.json` — generated package-validation evidence.
- `release/FILE_MANIFEST.sha256` — SHA-256 manifest for every packaged source/contract file other than generated validation reports and the manifest itself.
- `scripts/validate-spec-package.py` — validates required files, release hygiene, JSON/YAML/schema contracts, all examples, the 66-action registry, all 132 action payload contracts, the 22 gate predicates, the canonical twelve-address frame, the `.epicard` package manifest, SQLite DDL and seeds, OpenAPI references, generator reproducibility, executable skill wrapper, manifest integrity, and local Markdown links.

Reproduce the release checks from the package root:

```bash
python scripts/generate-action-registry.py
python scripts/generate-action-payloads.py
python scripts/validate-spec-package.py \
  --json release/VALIDATION_REPORT.json \
  --markdown release/VALIDATION_REPORT.md
```

