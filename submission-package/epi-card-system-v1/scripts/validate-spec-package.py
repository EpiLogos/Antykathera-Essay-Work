#!/usr/bin/env python3
"""Validate the Epi-Card v1 specification package.

This validator checks machine-readable contracts and package consistency. It does not
claim to execute PostgreSQL-specific DDL; PostgreSQL deployment validation remains an
implementation acceptance test. SQLite DDL is executed in-memory as the portable-store
syntax and referential-integrity smoke test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
from typing import Any

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing validator dependency. Install PyYAML and jsonschema before running."
    ) from exc

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SPEC.md",
    "README.md",
    "architecture/action-catalog.md",
    "architecture/module-contracts.md",
    "architecture/decision-register.md",
    "acceptance/ACCEPTANCE_TESTS.md",
    "api/openapi.yaml",
    "contracts/action-envelope.schema.json",
    "contracts/action-payloads.schema.json",
    "contracts/action-registry.schema.json",
    "contracts/action-registry.yaml",
    "contracts/gate-predicates.schema.json",
    "contracts/gate-predicates.yaml",
    "contracts/provider-capability.schema.json",
    "contracts/package-manifest.schema.json",
    "contracts/ql-frame.schema.json",
    "contracts/render-plan.schema.json",
    "database/postgres.sql",
    "database/sqlite.sql",
    "database/action-definitions.postgres.sql",
    "database/action-definitions.sqlite.sql",
    "examples/action-request.json",
    "examples/minimal-ql-frame.json",
    "examples/minimal-render-plan.json",
    "examples/seedance-provider-capability.json",
    "examples/minimal-package-manifest.json",
    "okf/EXPORT_PROFILE.md",
    "research/CURRENT_TECH_BASIS.md",
    "release/FILE_MANIFEST.sha256",
    "skills/epi-card/SKILL.md",
    "skills/epi-card/scripts/run-epicard",
    "skills/epi-card/references/audit.md",
    "skills/epi-card/references/cli-reference.md",
    "skills/epi-card/references/media-pipeline.md",
    "skills/epi-card/references/privacy-and-approval.md",
    "skills/epi-card/references/provider-adapters.md",
    "skills/epi-card/references/ql-frame.md",
    "skills/epi-card/references/resonance.md",
    "scripts/generate-action-payloads.py",
    "scripts/generate-action-registry.py",
    "scripts/validate-spec-package.py",
    "release/VALIDATION_REPORT.json",
    "release/VALIDATION_REPORT.md",
    "ui/epi-card.d.ts",
]

EXAMPLE_SCHEMA_PAIRS = [
    ("examples/minimal-ql-frame.json", "contracts/ql-frame.schema.json"),
    ("examples/minimal-render-plan.json", "contracts/render-plan.schema.json"),
    ("examples/action-request.json", "contracts/action-envelope.schema.json"),
    (
        "examples/seedance-provider-capability.json",
        "contracts/provider-capability.schema.json",
    ),
    (
        "examples/minimal-package-manifest.json",
        "contracts/package-manifest.schema.json",
    ),
]

CANONICAL_ADDRESSES = [
    "P0",
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
    "P0′",
    "P1′",
    "P2′",
    "P3′",
    "P4′",
    "P5′",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sql_table_columns(text: str) -> dict[str, list[str]]:
    """Extract CREATE TABLE column names for PostgreSQL/SQLite parity checks.

    This is intentionally a structural scanner, not a general SQL parser. It tracks
    parentheses and SQL string literals so commas inside CHECK/default expressions do
    not split columns. Table constraints are excluded.
    """
    tables: dict[str, list[str]] = {}
    table_re = re.compile(
        r"^CREATE TABLE\s+(?:IF NOT EXISTS\s+)?([a-z_][a-z0-9_]*)\s*\(",
        re.IGNORECASE | re.MULTILINE,
    )
    for match in table_re.finditer(text):
        name = match.group(1)
        i = match.end()
        depth = 1
        in_single = False
        in_double = False
        j = i
        while j < len(text) and depth:
            ch = text[j]
            if in_single:
                if ch == "'":
                    if j + 1 < len(text) and text[j + 1] == "'":
                        j += 1
                    else:
                        in_single = False
            elif in_double:
                if ch == '"':
                    in_double = False
            else:
                if ch == "'":
                    in_single = True
                elif ch == '"':
                    in_double = True
                elif ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
            j += 1
        body = text[i : j - 1]

        parts: list[str] = []
        start = 0
        depth = 0
        in_single = False
        in_double = False
        k = 0
        while k < len(body):
            ch = body[k]
            if in_single:
                if ch == "'":
                    if k + 1 < len(body) and body[k + 1] == "'":
                        k += 1
                    else:
                        in_single = False
            elif in_double:
                if ch == '"':
                    in_double = False
            else:
                if ch == "'":
                    in_single = True
                elif ch == '"':
                    in_double = True
                elif ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                elif ch == "," and depth == 0:
                    parts.append(body[start:k])
                    start = k + 1
            k += 1
        parts.append(body[start:])

        columns: list[str] = []
        for part in parts:
            item = part.strip()
            token_match = re.match(r"([a-z_][a-z0-9_]*)\b", item, re.IGNORECASE)
            if not token_match:
                continue
            token = token_match.group(1).lower()
            if token in {"primary", "unique", "check", "foreign", "constraint", "exclude"}:
                continue
            columns.append(token)
        tables[name] = columns
    return tables


def validate() -> dict[str, Any]:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    def record(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})
        if not passed:
            failures.append(f"{name}: {detail}")

    missing = [item for item in REQUIRED_FILES if not (ROOT / item).is_file()]
    record("required_files", not missing, {"missing": missing, "required_count": len(REQUIRED_FILES)})

    backup_files = sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.bak"))
    record("no_backup_files", not backup_files, {"found": backup_files})

    forbidden_terms: dict[str, list[int]] = {}
    term_re = re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE)
    marker_scan_exclusions = {
        ROOT / "scripts/validate-spec-package.py",
    }
    for path in ROOT.rglob("*"):
        if path in marker_scan_exclusions or "release" in path.relative_to(ROOT).parts:
            continue
        if not path.is_file() or path.suffix.lower() not in {".md", ".sql", ".yaml", ".yml", ".json", ".ts", ".py"}:
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [idx + 1 for idx, line in enumerate(lines) if term_re.search(line)]
        # The acceptance test names the terms intentionally; exclude that self-test line.
        if path.name == "ACCEPTANCE_TESTS.md":
            hits = [n for n in hits if "Search normative source files" not in lines[n - 1]]
        if hits:
            forbidden_terms[str(path.relative_to(ROOT))] = hits
    record("no_unresolved_markers", not forbidden_terms, forbidden_terms)

    invisible_chars = {
        "\u200b": "ZERO WIDTH SPACE",
        "\u200c": "ZERO WIDTH NON-JOINER",
        "\u200d": "ZERO WIDTH JOINER",
        "\ufeff": "BYTE ORDER MARK",
        "\u202a": "LEFT-TO-RIGHT EMBEDDING",
        "\u202b": "RIGHT-TO-LEFT EMBEDDING",
        "\u202d": "LEFT-TO-RIGHT OVERRIDE",
        "\u202e": "RIGHT-TO-LEFT OVERRIDE",
        "\u2066": "LEFT-TO-RIGHT ISOLATE",
        "\u2067": "RIGHT-TO-LEFT ISOLATE",
        "\u2068": "FIRST STRONG ISOLATE",
        "\u2069": "POP DIRECTIONAL ISOLATE",
    }
    invisible_hits: dict[str, dict[str, int]] = {}
    for path in ROOT.rglob("*"):
        if "release" in path.relative_to(ROOT).parts or not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".sql", ".yaml", ".yml", ".json", ".ts", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        found = {name: text.count(char) for char, name in invisible_chars.items() if char in text}
        if found:
            invisible_hits[str(path.relative_to(ROOT))] = found
    record("no_invisible_control_characters", not invisible_hits, invisible_hits)

    adk_hits: dict[str, list[int]] = {}
    adk_re = re.compile(r"\b(?:Google\s+)?ADK\b", re.IGNORECASE)
    for path in ROOT.rglob("*"):
        if "release" in path.relative_to(ROOT).parts:
            continue
        if not path.is_file() or path.suffix.lower() not in {".md", ".sql", ".yaml", ".yml", ".json", ".ts"}:
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = [idx + 1 for idx, line in enumerate(lines) if adk_re.search(line)]
        if hits:
            adk_hits[str(path.relative_to(ROOT))] = hits
    record("google_adk_absent", not adk_hits, adk_hits)

    json_files = sorted(ROOT.rglob("*.json"))
    json_data: dict[Path, Any] = {}
    json_errors: dict[str, str] = {}
    for path in json_files:
        try:
            json_data[path] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            json_errors[str(path.relative_to(ROOT))] = str(exc)
    record("json_parse", not json_errors, {"files": len(json_files), "errors": json_errors})

    schema_errors: dict[str, str] = {}
    schema_files = sorted(ROOT.rglob("*.schema.json"))
    for path in schema_files:
        try:
            Draft202012Validator.check_schema(json_data[path])
        except Exception as exc:  # noqa: BLE001
            schema_errors[str(path.relative_to(ROOT))] = str(exc)
    record("json_schema_meta_validation", not schema_errors, {"schemas": len(schema_files), "errors": schema_errors})

    example_errors: dict[str, list[str]] = {}
    for example_rel, schema_rel in EXAMPLE_SCHEMA_PAIRS:
        example = json_data[ROOT / example_rel]
        schema = json_data[ROOT / schema_rel]
        errs = sorted(
            Draft202012Validator(schema).iter_errors(example),
            key=lambda err: list(err.absolute_path),
        )
        if errs:
            example_errors[example_rel] = [
                f"{list(err.absolute_path)}: {err.message}" for err in errs
            ]
    record("example_contract_validation", not example_errors, example_errors)

    yaml_files = sorted(list(ROOT.rglob("*.yaml")) + list(ROOT.rglob("*.yml")))
    yaml_data: dict[Path, Any] = {}
    yaml_errors: dict[str, str] = {}
    for path in yaml_files:
        try:
            yaml_data[path] = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            yaml_errors[str(path.relative_to(ROOT))] = str(exc)
    record("yaml_parse", not yaml_errors, {"files": len(yaml_files), "errors": yaml_errors})

    registry_errors: list[str] = []
    registry = yaml_data.get(ROOT / "contracts/action-registry.yaml")
    registry_schema = json_data.get(ROOT / "contracts/action-registry.schema.json")
    if registry is not None and registry_schema is not None:
        registry_errors = [
            f"{list(err.absolute_path)}: {err.message}"
            for err in sorted(
                Draft202012Validator(registry_schema).iter_errors(registry),
                key=lambda err: list(err.absolute_path),
            )
        ]
    record(
        "action_registry",
        not registry_errors and isinstance(registry, dict) and len(registry.get("actions", [])) == 66,
        {"actions": len(registry.get("actions", [])) if isinstance(registry, dict) else None, "errors": registry_errors},
    )

    payload_schema = json_data.get(ROOT / "contracts/action-payloads.schema.json")
    payload_ref_errors: list[str] = []
    payload_index_count = None
    if isinstance(registry, dict) and isinstance(payload_schema, dict):
        defs = payload_schema.get("$defs", {})
        index = payload_schema.get("x-action-index", {})
        payload_index_count = len(index) if isinstance(index, dict) else None
        expected_prefix = "urn:epi-card:schema:action-payloads:1.0.0#/$defs/"
        for action in registry.get("actions", []):
            name = action.get("name")
            indexed = index.get(name) if isinstance(index, dict) else None
            for direction, registry_key in (("input", "input_schema_ref"), ("output", "output_schema_ref")):
                schema_ref = action.get(registry_key)
                if not isinstance(schema_ref, str) or not schema_ref.startswith(expected_prefix):
                    payload_ref_errors.append(f"{name}.{direction}: invalid ref {schema_ref!r}")
                    continue
                def_name = schema_ref[len(expected_prefix):]
                if def_name not in defs:
                    payload_ref_errors.append(f"{name}.{direction}: missing $defs/{def_name}")
                if not isinstance(indexed, dict) or indexed.get(direction) != schema_ref:
                    payload_ref_errors.append(f"{name}.{direction}: x-action-index mismatch")
        registry_names = {item.get("name") for item in registry.get("actions", [])}
        index_names = set(index) if isinstance(index, dict) else set()
        if registry_names != index_names:
            payload_ref_errors.append(
                f"action-name mismatch: registry-only={sorted(registry_names-index_names)}, "
                f"payload-only={sorted(index_names-registry_names)}"
            )
    else:
        payload_ref_errors.append("registry or action-payload schema unavailable")
    record(
        "action_payload_contracts",
        not payload_ref_errors and payload_index_count == 66,
        {"indexed_actions": payload_index_count, "errors": payload_ref_errors},
    )

    predicate_errors: list[str] = []
    predicates = yaml_data.get(ROOT / "contracts/gate-predicates.yaml")
    predicate_schema = json_data.get(ROOT / "contracts/gate-predicates.schema.json")
    if predicates is not None and predicate_schema is not None:
        predicate_errors = [
            f"{list(err.absolute_path)}: {err.message}"
            for err in sorted(
                Draft202012Validator(predicate_schema).iter_errors(predicates),
                key=lambda err: list(err.absolute_path),
            )
        ]
    predicate_count = len(predicates.get("predicates", [])) if isinstance(predicates, dict) else None
    record(
        "gate_predicate_registry",
        not predicate_errors and predicate_count == 22,
        {"predicates": predicate_count, "errors": predicate_errors},
    )

    predicate_xref_errors: list[str] = []
    predicate_by_name = {
        item.get("name"): item
        for item in predicates.get("predicates", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    } if isinstance(predicates, dict) else {}
    declared_predicates = set(predicate_by_name)
    referenced_predicates: set[str] = set()
    if isinstance(registry, dict):
        for action in registry.get("actions", []):
            for gate_index, gate in enumerate(action.get("gates", [])):
                for key in ("when", "requires"):
                    call = gate.get(key, {})
                    name = call.get("predicate") if isinstance(call, dict) else None
                    if isinstance(name, str):
                        referenced_predicates.add(name)
                        if name not in declared_predicates:
                            predicate_xref_errors.append(
                                f"{action.get('name')}.gates[{gate_index}].{key}: undeclared predicate {name}"
                            )
                            continue
                        argument_schema = predicate_by_name[name].get("arguments_schema", {})
                        try:
                            Draft202012Validator.check_schema(argument_schema)
                        except Exception as exc:  # noqa: BLE001
                            predicate_xref_errors.append(
                                f"predicate {name}: invalid arguments_schema: {exc}"
                            )
                            continue
                        arguments = call.get("arguments", {}) if isinstance(call, dict) else {}
                        arg_errors = sorted(
                            Draft202012Validator(argument_schema).iter_errors(arguments),
                            key=lambda err: list(err.absolute_path),
                        )
                        for err in arg_errors:
                            predicate_xref_errors.append(
                                f"{action.get('name')}.gates[{gate_index}].{key}.arguments{list(err.absolute_path)}: {err.message}"
                            )
    unreferenced_predicates = sorted(declared_predicates - referenced_predicates)
    record(
        "gate_predicate_cross_references",
        not predicate_xref_errors and not unreferenced_predicates,
        {
            "declared": len(declared_predicates),
            "referenced": len(referenced_predicates),
            "undeclared_references": predicate_xref_errors,
            "unreferenced": unreferenced_predicates,
        },
    )

    ql_example = json_data.get(ROOT / "examples/minimal-ql-frame.json", {})
    ql_positions = list(ql_example.get("positions", {}).keys())
    traversal = ql_example.get("relations", {}).get("traversal", [])
    record(
        "canonical_ql_frame",
        ql_positions == CANONICAL_ADDRESSES
        and traversal == CANONICAL_ADDRESSES + ["P0+"],
        {"positions": ql_positions, "traversal": traversal},
    )

    # Canonical machine identifiers use Unicode PRIME U+2032, never ASCII apostrophe.
    address_encoding_errors: list[str] = []
    if isinstance(payload_schema, dict):
        defs = payload_schema.get("$defs", {})
        payload_addresses = defs.get("qlAddress", {}).get("enum")
        if payload_addresses != CANONICAL_ADDRESSES:
            address_encoding_errors.append(
                f"action payload qlAddress enum differs: {payload_addresses!r}"
            )
        map_required = defs.get("positionUuidMap", {}).get("required")
        if map_required != CANONICAL_ADDRESSES:
            address_encoding_errors.append(
                f"positionUuidMap required keys differ: {map_required!r}"
            )
    for ddl_rel in ("database/postgres.sql", "database/sqlite.sql"):
        ddl_text = (ROOT / ddl_rel).read_text(encoding="utf-8")
        for address in CANONICAL_ADDRESSES:
            if address not in ddl_text:
                address_encoding_errors.append(f"{ddl_rel}: missing canonical address {address}")
        if "address" not in ddl_text:
            address_encoding_errors.append(f"{ddl_rel}: canonical address column absent")
    record(
        "canonical_address_encoding",
        not address_encoding_errors,
        {"canonical": CANONICAL_ADDRESSES, "errors": address_encoding_errors},
    )

    # The manifest fixture exercises cross-field invariants JSON Schema cannot express.
    package_manifest = json_data.get(ROOT / "examples/minimal-package-manifest.json", {})
    package_manifest_errors: list[str] = []
    package_paths: list[str] = []
    if isinstance(package_manifest, dict):
        entries = package_manifest.get("files", [])
        if not isinstance(entries, list):
            package_manifest_errors.append("files is not an array")
            entries = []
        path_to_entry: dict[str, dict[str, Any]] = {}
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
                package_manifest_errors.append("files contains an entry without a string path")
                continue
            path = entry["path"]
            package_paths.append(path)
            if path in path_to_entry:
                package_manifest_errors.append(f"duplicate file path: {path}")
            path_to_entry[path] = entry
        entrypoints = package_manifest.get("entrypoints", {})
        if isinstance(entrypoints, dict):
            for name, path in entrypoints.items():
                if path is not None and path not in path_to_entry:
                    package_manifest_errors.append(
                        f"entrypoint {name} does not resolve to files[]: {path}"
                    )
        for rendition in package_manifest.get("renditions", []) if isinstance(package_manifest.get("renditions", []), list) else []:
            if not isinstance(rendition, dict):
                continue
            path = rendition.get("primary_path")
            entry = path_to_entry.get(path)
            if entry is None:
                package_manifest_errors.append(f"rendition path absent from files[]: {path}")
            elif entry.get("sha256") != rendition.get("sha256"):
                package_manifest_errors.append(f"rendition/file digest mismatch: {path}")
        digest_lines = []
        for path in sorted(path_to_entry):
            digest = path_to_entry[path].get("sha256")
            if isinstance(digest, str):
                digest_lines.append(f"{digest}  {path}\n")
        computed_root = hashlib.sha256("".join(digest_lines).encode("utf-8")).hexdigest()
        declared_root = package_manifest.get("integrity", {}).get("root_sha256") if isinstance(package_manifest.get("integrity"), dict) else None
        if computed_root != declared_root:
            package_manifest_errors.append(
                f"root digest mismatch: declared={declared_root}, computed={computed_root}"
            )
    else:
        package_manifest_errors.append("fixture is not an object")
    record(
        "package_manifest_semantics",
        not package_manifest_errors,
        {"files": len(package_paths), "errors": package_manifest_errors},
    )

    specification_hash = sha256(ROOT / "SPEC.md")
    hash_alignment_errors: list[str] = []
    for ddl_rel in ("database/postgres.sql", "database/sqlite.sql"):
        ddl_text = (ROOT / ddl_rel).read_text(encoding="utf-8")
        hashes = re.findall(r"[0-9a-f]{64}", ddl_text)
        if specification_hash not in hashes:
            hash_alignment_errors.append(
                f"{ddl_rel}: schema_revision does not contain SPEC.md hash {specification_hash}"
            )
    record(
        "specification_hash_alignment",
        not hash_alignment_errors,
        {"specification_hash": specification_hash, "errors": hash_alignment_errors},
    )

    sqlite_detail: dict[str, Any] = {}
    try:
        con = sqlite3.connect(":memory:")
        con.execute("PRAGMA foreign_keys = ON")
        con.executescript((ROOT / "database/sqlite.sql").read_text(encoding="utf-8"))
        con.executescript(
            (ROOT / "database/action-definitions.sqlite.sql").read_text(encoding="utf-8")
        )
        sqlite_detail["tables"] = con.execute(
            "SELECT count(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchone()[0]
        # The seed must carry the same 66 action definitions as the YAML registry.
        sqlite_detail["seeded_actions"] = con.execute(
            "SELECT count(*) FROM action_definition"
        ).fetchone()[0]
        con.close()
        sqlite_ok = sqlite_detail["tables"] == 70 and sqlite_detail["seeded_actions"] == 66
    except Exception as exc:  # noqa: BLE001
        sqlite_ok = False
        sqlite_detail["error"] = str(exc)
    record("sqlite_ddl_and_seed", sqlite_ok, sqlite_detail)

    pg_tables = sql_table_columns((ROOT / "database/postgres.sql").read_text(encoding="utf-8"))
    sq_tables = sql_table_columns((ROOT / "database/sqlite.sql").read_text(encoding="utf-8"))
    parity_errors: list[str] = []
    for table_name in sorted(set(pg_tables) | set(sq_tables)):
        if table_name not in pg_tables:
            parity_errors.append(f"SQLite-only table: {table_name}")
            continue
        if table_name not in sq_tables:
            parity_errors.append(f"PostgreSQL-only table: {table_name}")
            continue
        if pg_tables[table_name] != sq_tables[table_name]:
            parity_errors.append(
                f"{table_name}: PostgreSQL columns={pg_tables[table_name]!r}; "
                f"SQLite columns={sq_tables[table_name]!r}"
            )
    record(
        "sql_logical_schema_parity",
        not parity_errors and len(pg_tables) == len(sq_tables) == 70,
        {"postgres_tables": len(pg_tables), "sqlite_tables": len(sq_tables), "errors": parity_errors},
    )

    openapi = yaml_data.get(ROOT / "api/openapi.yaml")
    ref_missing: list[str] = []
    ref_re = re.compile(r"\$ref:\s*[\"']?([^\"'\s]+)")
    openapi_text = (ROOT / "api/openapi.yaml").read_text(encoding="utf-8")
    for ref in ref_re.findall(openapi_text):
        if ref.startswith("#") or "://" in ref:
            continue
        target = ref.split("#", 1)[0]
        if not (ROOT / "api" / target).resolve().exists():
            ref_missing.append(ref)
    openapi_ok = (
        isinstance(openapi, dict)
        and str(openapi.get("openapi", "")).startswith("3.1")
        and isinstance(openapi.get("paths"), dict)
        and not ref_missing
    )
    record(
        "openapi_structure",
        openapi_ok,
        {
            "version": openapi.get("openapi") if isinstance(openapi, dict) else None,
            "paths": len(openapi.get("paths", {})) if isinstance(openapi, dict) else None,
            "missing_refs": ref_missing,
        },
    )

    generator = ROOT / "scripts/generate-action-registry.py"
    generated = [
        ROOT / "contracts/action-registry.yaml",
        ROOT / "database/action-definitions.postgres.sql",
        ROOT / "database/action-definitions.sqlite.sql",
    ]
    before = {str(p.relative_to(ROOT)): sha256(p) for p in generated}
    try:
        proc = subprocess.run(
            [sys.executable, str(generator)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        after = {str(p.relative_to(ROOT)): sha256(p) for p in generated}
        generator_ok = proc.returncode == 0 and before == after
        generator_detail = {
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "hashes_unchanged": before == after,
        }
    except Exception as exc:  # noqa: BLE001
        generator_ok = False
        generator_detail = {"error": str(exc)}
    record("action_registry_reproducibility", generator_ok, generator_detail)

    payload_generator = ROOT / "scripts/generate-action-payloads.py"
    payload_generated = ROOT / "contracts/action-payloads.schema.json"
    payload_before = sha256(payload_generated)
    try:
        proc = subprocess.run(
            [sys.executable, str(payload_generator)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        payload_after = sha256(payload_generated)
        payload_generator_ok = proc.returncode == 0 and payload_before == payload_after
        payload_generator_detail = {
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "hash_unchanged": payload_before == payload_after,
        }
    except Exception as exc:  # noqa: BLE001
        payload_generator_ok = False
        payload_generator_detail = {"error": str(exc)}
    record("action_payload_reproducibility", payload_generator_ok, payload_generator_detail)

    wrapper = ROOT / "skills/epi-card/scripts/run-epicard"
    record(
        "skill_wrapper_executable",
        wrapper.is_file() and os.access(wrapper, os.X_OK),
        {"path": str(wrapper.relative_to(ROOT)), "mode": oct(wrapper.stat().st_mode & 0o777) if wrapper.exists() else None},
    )

    bash_path = shutil.which("bash")
    if bash_path:
        bash_proc = subprocess.run(
            [bash_path, "-n", str(wrapper)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        bash_ok = bash_proc.returncode == 0
        bash_detail = {
            "executable": bash_path,
            "returncode": bash_proc.returncode,
            "stderr": bash_proc.stderr.strip(),
        }
    else:
        bash_ok = False
        bash_detail = {"error": "bash executable not found"}
    record("skill_wrapper_syntax", bash_ok, bash_detail)

    skill_path = ROOT / "skills/epi-card/SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    skill_frontmatter_errors: list[str] = []
    skill_meta: Any = None
    if not skill_text.startswith("---\n") or "\n---\n" not in skill_text[4:]:
        skill_frontmatter_errors.append("SKILL.md lacks delimited YAML frontmatter")
    else:
        frontmatter = skill_text.split("\n---\n", 1)[0][4:]
        try:
            skill_meta = yaml.safe_load(frontmatter)
        except Exception as exc:  # noqa: BLE001
            skill_frontmatter_errors.append(str(exc))
        if not isinstance(skill_meta, dict):
            skill_frontmatter_errors.append("frontmatter is not a mapping")
        else:
            if skill_meta.get("name") != "epi-card":
                skill_frontmatter_errors.append("name must equal epi-card")
            description = skill_meta.get("description")
            if not isinstance(description, str) or not (1 <= len(description) <= 1024):
                skill_frontmatter_errors.append("description must contain 1..1024 characters")
            version = skill_meta.get("metadata", {}).get("version") if isinstance(skill_meta.get("metadata"), dict) else None
            if version != "1.0.0":
                skill_frontmatter_errors.append("metadata.version must equal 1.0.0")
    record(
        "agent_skill_frontmatter",
        not skill_frontmatter_errors,
        {"name": skill_meta.get("name") if isinstance(skill_meta, dict) else None, "errors": skill_frontmatter_errors},
    )

    tsc_path = shutil.which("tsc")
    if tsc_path:
        tsc_proc = subprocess.run(
            [tsc_path, "--noEmit", "--strict", "--skipLibCheck", "--lib", "ES2022,DOM", "ui/epi-card.d.ts"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        tsc_ok = tsc_proc.returncode == 0
        tsc_detail = {
            "executable": tsc_path,
            "returncode": tsc_proc.returncode,
            "stdout": tsc_proc.stdout.strip(),
            "stderr": tsc_proc.stderr.strip(),
        }
    else:
        tsc_ok = False
        tsc_detail = {"error": "TypeScript compiler (tsc) not found"}
    record("typescript_ui_contract", tsc_ok, tsc_detail)

    local_link_errors: list[str] = []
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in link_re.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / target).resolve().exists():
                local_link_errors.append(f"{path.relative_to(ROOT)} -> {target}")
    record("local_markdown_links", not local_link_errors, local_link_errors)

    manifest_path = ROOT / "release/FILE_MANIFEST.sha256"
    manifest_errors: list[str] = []
    manifest_entries: dict[str, str] = {}
    if manifest_path.is_file():
        for line_no, raw_line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw_line.strip():
                continue
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", raw_line)
            if not match:
                manifest_errors.append(f"line {line_no}: invalid manifest syntax")
                continue
            digest, rel = match.groups()
            if rel in manifest_entries:
                manifest_errors.append(f"line {line_no}: duplicate path {rel}")
                continue
            manifest_entries[rel] = digest
            target = ROOT / rel
            if not target.is_file():
                manifest_errors.append(f"missing file: {rel}")
            elif sha256(target) != digest:
                manifest_errors.append(f"hash mismatch: {rel}")
        excluded = {
            "release/FILE_MANIFEST.sha256",
            "release/VALIDATION_REPORT.json",
            "release/VALIDATION_REPORT.md",
        }
        actual_files = {
            str(path.relative_to(ROOT))
            for path in ROOT.rglob("*")
            if path.is_file() and str(path.relative_to(ROOT)) not in excluded
        }
        listed_files = set(manifest_entries)
        missing_from_manifest = sorted(actual_files - listed_files)
        extra_in_manifest = sorted(listed_files - actual_files)
        if missing_from_manifest:
            manifest_errors.append(f"unlisted files: {missing_from_manifest}")
        if extra_in_manifest:
            manifest_errors.append(f"non-package entries: {extra_in_manifest}")
    else:
        manifest_errors.append("manifest missing")
    record(
        "file_manifest_integrity",
        not manifest_errors,
        {"entries": len(manifest_entries), "errors": manifest_errors},
    )

    report = {
        "package": "Epi-Card QL Conjugate System",
        "version": "1.0.0",
        "validator": "scripts/validate-spec-package.py",
        "passed": not failures,
        "checks": checks,
        "failures": failures,
    }
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Epi-Card v1 Specification Package — Validation Report",
        "",
        f"**Result:** {'PASS' if report['passed'] else 'FAIL'}  ",
        f"**Package version:** {report['version']}  ",
        f"**Validator:** `{report['validator']}`",
        "",
        "This report validates the specification package itself: contracts, examples, the portable SQL schema, generated action seeds, registries, internal references, and release hygiene. PostgreSQL-specific execution remains part of implementation acceptance because this package environment does not run a PostgreSQL server.",
        "",
        "| Check | Result | Detail |",
        "|---|---:|---|",
    ]
    for check in report["checks"]:
        detail = json.dumps(check["detail"], ensure_ascii=False, sort_keys=True)
        if len(detail) > 240:
            detail = detail[:237] + "…"
        detail = detail.replace("|", "\\|")
        lines.append(f"| `{check['name']}` | {'PASS' if check['passed'] else 'FAIL'} | `{detail}` |")
    lines.extend(["", "## Result", ""])
    if report["passed"]:
        lines.append("All package-level checks passed.")
    else:
        lines.append("The following checks failed:")
        lines.extend(f"- {failure}" for failure in report["failures"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--markdown", dest="markdown_path", type=Path)
    args = parser.parse_args()

    report = validate()
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.markdown_path:
        args.markdown_path.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_path.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
