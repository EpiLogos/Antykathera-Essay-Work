# Epi-Card v1 Specification Package — Validation Report

**Result:** PASS  
**Package version:** 1.0.0  
**Validator:** `scripts/validate-spec-package.py`

This report validates the specification package itself: contracts, examples, the portable SQL schema, generated action seeds, registries, internal references, and release hygiene. PostgreSQL-specific execution remains part of implementation acceptance because this package environment does not run a PostgreSQL server.

| Check | Result | Detail |
|---|---:|---|
| `required_files` | PASS | `{"missing": [], "required_count": 44}` |
| `no_backup_files` | PASS | `{"found": []}` |
| `no_unresolved_markers` | PASS | `{}` |
| `no_invisible_control_characters` | PASS | `{}` |
| `google_adk_absent` | PASS | `{}` |
| `json_parse` | PASS | `{"errors": {}, "files": 14}` |
| `json_schema_meta_validation` | PASS | `{"errors": {}, "schemas": 8}` |
| `example_contract_validation` | PASS | `{}` |
| `yaml_parse` | PASS | `{"errors": {}, "files": 3}` |
| `action_registry` | PASS | `{"actions": 66, "errors": []}` |
| `action_payload_contracts` | PASS | `{"errors": [], "indexed_actions": 66}` |
| `gate_predicate_registry` | PASS | `{"errors": [], "predicates": 22}` |
| `gate_predicate_cross_references` | PASS | `{"declared": 22, "referenced": 22, "undeclared_references": [], "unreferenced": []}` |
| `canonical_ql_frame` | PASS | `{"positions": ["P0", "P1", "P2", "P3", "P4", "P5", "P0′", "P1′", "P2′", "P3′", "P4′", "P5′"], "traversal": ["P0", "P1", "P2", "P3", "P4", "P5", "P0′", "P1′", "P2′", "P3′", "P4′", "P5′", "P0+"]}` |
| `canonical_address_encoding` | PASS | `{"canonical": ["P0", "P1", "P2", "P3", "P4", "P5", "P0′", "P1′", "P2′", "P3′", "P4′", "P5′"], "errors": []}` |
| `package_manifest_semantics` | PASS | `{"errors": [], "files": 5}` |
| `specification_hash_alignment` | PASS | `{"errors": [], "specification_hash": "dfdaa496ef90261ba185510f2b65abde88e0ee6059dfd3fbbd47b7be3b07a902"}` |
| `sqlite_ddl_and_seed` | PASS | `{"seeded_actions": 66, "tables": 70}` |
| `sql_logical_schema_parity` | PASS | `{"errors": [], "postgres_tables": 70, "sqlite_tables": 70}` |
| `openapi_structure` | PASS | `{"missing_refs": [], "paths": 13, "version": "3.1.0"}` |
| `action_registry_reproducibility` | PASS | `{"hashes_unchanged": true, "returncode": 0, "stderr": "", "stdout": "Generated 66 actions"}` |
| `action_payload_reproducibility` | PASS | `{"hash_unchanged": true, "returncode": 0, "stderr": "", "stdout": "Generated 66 input and 66 output schemas"}` |
| `skill_wrapper_executable` | PASS | `{"mode": "0o755", "path": "skills/epi-card/scripts/run-epicard"}` |
| `skill_wrapper_syntax` | PASS | `{"executable": "/bin/bash", "returncode": 0, "stderr": ""}` |
| `agent_skill_frontmatter` | PASS | `{"errors": [], "name": "epi-card"}` |
| `typescript_ui_contract` | PASS | `{"executable": "/Users/admin/Documents/Epi-Logos/Idea/epi-claw/node_modules/.bin/tsc", "returncode": 0, "stderr": "", "stdout": ""}` |
| `local_markdown_links` | PASS | `[]` |
| `file_manifest_integrity` | PASS | `{"entries": 42, "errors": []}` |

## Result

All package-level checks passed.
