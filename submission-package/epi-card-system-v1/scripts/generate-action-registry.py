#!/usr/bin/env python3
"""Generate the normative action registry and SQL seeds from the Markdown catalogue.

The Markdown table remains the human-readable action catalogue. This generator strips
presentation syntax, applies the explicit machine-policy maps below, emits a validated
YAML registry, and emits PostgreSQL/SQLite action_definition seed files.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "architecture" / "action-catalog.md"
REGISTRY = ROOT / "contracts" / "action-registry.yaml"
PG_SEED = ROOT / "database" / "action-definitions.postgres.sql"
SQLITE_SEED = ROOT / "database" / "action-definitions.sqlite.sql"

AUDIT_EXEMPT = {
    "session.resume",
    "projection.validate",
    "ql.validate",
    "symbol.validate",
    "video.poll",
    "loop.validate",
    "audio.analyze",
    "audio.loop.validate",
    "okf.validate",
    "publication.poll",
}

EXTERNAL_SAGA = {
    "temporal.capture",
    "recording.transcribe",
    "symbol.generate",
    "image.generate",
    "image.edit",
    "video.submit",
    "video.poll",
    "video.continue",
    "video.edit",
    "publication.execute",
    "publication.poll",
}

ASSET_SAGA = {
    "source.ingest",
    "recording.ingest",
    "projection.materialize",
    "symbol.canonicalize",
    "symbol.state.render",
    "image.collect",
    "image.alpha",
    "plate.accept",
    "modifier.apply",
    "composition.render",
    "poster.select",
    "audio.render",
    "audio.mix",
    "card.render.web",
    "card.render.print",
    "card.package",
    "okf.export",
}

PROVIDER_ACTIONS = {
    "temporal.capture",
    "source.ingest",
    "recording.transcribe",
    "symbol.generate",
    "image.collect",
    "image.generate",
    "image.edit",
    "video.submit",
    "video.poll",
    "video.continue",
    "video.edit",
    "modifier.apply",
    "publication.execute",
    "publication.poll",
}

# Each gate is explicit. No runtime is permitted to infer a gate from prose.
# stage: pre_execute blocks side effects; pre_commit blocks success; pre_promote
# allows candidate creation but blocks canonical/approved use; pre_publish blocks upload.
GATES: dict[str, list[dict[str, Any]]] = {
    "temporal.capture": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "astronomy"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "astronomy"}}}
    ],
    "source.ingest": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "source.extraction_leaves_runtime", "arguments": {}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "source_extraction"}}}
    ],
    "recording.ingest": [
        {"kind": "consent", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "consent.recording_allows_scope", "arguments": {}}}
    ],
    "recording.transcribe": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "transcription"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "transcription"}}}
    ],
    "projection.materialize": [
        {"kind": "human_review", "stage": "pre_commit", "mode": "conditional",
         "when": {"predicate": "projection.kind_in", "arguments": {"values": ["shared", "public", "provider"]}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "projection"}}},
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "projection.kind_is", "arguments": {"value": "provider"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "provider_projection"}}},
    ],
    "basin.resolve": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "canonical_basin"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "basin"}}}
    ],
    "basin.revise": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "basin.essential_or_excluded_changed", "arguments": {}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "basin_revision"}}}
    ],
    "ql.map": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "approved_ql_frame"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "ql_frame"}}}
    ],
    "ql.reconcile": [
        {"kind": "human_review", "stage": "pre_commit", "mode": "conditional",
         "when": {"predicate": "action.input_flag_true", "arguments": {"path": "/input/apply_content_mutation"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "ql_reconciliation"}}}
    ],
    "ql.approve": [
        {"kind": "actor_authorization", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "actor.has_permission", "arguments": {"permission": "ql:approve"}}}
    ],
    "lock.acquire": [
        {"kind": "actor_authorization", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "actor.has_permission", "arguments": {"permission": "lock:write"}}}
    ],
    "lock.release": [
        {"kind": "actor_authorization", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "actor.lock_release_authorized", "arguments": {}}}
    ],
    "return.deposit": [
        {"kind": "human_review", "stage": "pre_commit", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "return_deposit"}}}
    ],
    "resonance.resolve": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "resonance.open_extension_changed", "arguments": {}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "resonance_extension"}}}
    ],
    "art-direction.resolve": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "canonical_art_direction"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "art_direction"}}}
    ],
    "palette.resolve": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "action.input_flag_true", "arguments": {"path": "/input/canonical_use"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "palette"}}}
    ],
    "typography.resolve": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "action.input_flag_true", "arguments": {"path": "/input/canonical_use"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "typography"}}}
    ],
    "symbol.propose": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "canonicalization_candidate"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "symbol_proposal"}}}
    ],
    "symbol.generate": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "symbol_generation"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "symbol_generation"}}},
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "canonicalization_candidate"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "symbol_generation"}}},
    ],
    "symbol.transform": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "canonicalization_candidate"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "symbol_transform"}}}
    ],
    "symbol.canonicalize": [
        {"kind": "human_approval", "stage": "pre_commit", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "symbol_canonicalization"}}}
    ],
    "symbol.approve": [
        {"kind": "actor_authorization", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "actor.has_permission", "arguments": {"permission": "symbol:approve"}}}
    ],
    "storyboard.plan": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "production_storyboard"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "storyboard"}}}
    ],
    "image.collect": [
        {"kind": "account_authorization", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "request.external_account_access", "arguments": {}},
         "requires": {"predicate": "account.authorization_valid", "arguments": {}}}
    ],
    "image.generate": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "image_generation"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "image_generation"}}}
    ],
    "image.edit": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "image_edit"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "image_edit"}}}
    ],
    "image.alpha": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "target.role_equals", "arguments": {"value": "canonical_symbol"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "symbol_alpha"}}}
    ],
    "scene.plan": [
        {"kind": "human_review", "stage": "pre_commit", "mode": "conditional",
         "when": {"predicate": "storyboard.approved_revision_changed", "arguments": {}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "storyboard_change"}}}
    ],
    "video.submit": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "video_generation"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "video_generation"}}}
    ],
    "video.continue": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "video_continuation"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "video_continuation"}}}
    ],
    "video.edit": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "provider.is_external", "arguments": {"capability": "video_edit"}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "video_edit"}}}
    ],
    "plate.accept": [
        {"kind": "actor_authorization", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "actor.has_permission", "arguments": {"permission": "plate:approve"}}}
    ],
    "modifier.apply": [
        {"kind": "provider_disclosure", "stage": "pre_execute", "mode": "conditional",
         "when": {"predicate": "modifier.is_external_ai", "arguments": {}},
         "requires": {"predicate": "disclosure.provider_receipt_valid", "arguments": {"purpose": "media_modifier"}}},
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "modifier.is_nondeterministic", "arguments": {}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "nondeterministic_modifier"}}},
    ],
    "composition.render": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "approved_master"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "final_render"}}}
    ],
    "poster.select": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "approved_poster"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "poster"}}}
    ],
    "audio.palette.resolve": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "canonical_audio_palette"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "audio_palette"}}}
    ],
    "audio.mix": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "approved_final_mix"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "audio_mix"}}}
    ],
    "card.render.print": [
        {"kind": "human_review", "stage": "pre_promote", "mode": "conditional",
         "when": {"predicate": "promotion.requested", "arguments": {"target": "approved_print_master"}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "print_master"}}}
    ],
    "card.package": [
        {"kind": "human_review", "stage": "pre_commit", "mode": "conditional",
         "when": {"predicate": "disclosure.scope_in", "arguments": {"values": ["shared", "public"]}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "package_export"}}}
    ],
    "okf.export": [
        {"kind": "human_review", "stage": "pre_commit", "mode": "conditional",
         "when": {"predicate": "disclosure.scope_in", "arguments": {"values": ["shared", "public"]}},
         "requires": {"predicate": "approval.matches_payload", "arguments": {"approval_type": "okf_export"}}}
    ],
    "publication.approve": [
        {"kind": "actor_authorization", "stage": "pre_execute", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "actor.has_permission", "arguments": {"permission": "publication:approve"}}}
    ],
    "publication.execute": [
        {"kind": "prior_approval", "stage": "pre_publish", "mode": "always",
         "when": {"predicate": "always", "arguments": {}},
         "requires": {"predicate": "publication.approval_matches_hashes", "arguments": {}}}
    ],
}

def strip_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def parse_catalogue() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in CATALOGUE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            raise ValueError(f"Expected 8 cells, got {len(cells)}: {line}")
        rows.append(
            {
                "name": strip_code(cells[0]),
                "side_effect": strip_code(cells[1]),
                "required_input": cells[2],
                "output_contract": cells[3],
                "permission": strip_code(cells[4]),
                "gate_summary": cells[5],
                "idempotency_policy": cells[6],
                "success_condition": cells[7],
            }
        )
    if len(rows) != 66:
        raise ValueError(f"Expected 66 actions, found {len(rows)}")
    names = [row["name"] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("Action names are not unique")
    return rows


def transaction_class(name: str, side_effect: str) -> str:
    if name in EXTERNAL_SAGA:
        return "external_saga"
    if name in ASSET_SAGA:
        return "asset_saga"
    if side_effect == "read":
        return "read_only"
    return "atomic_sql"


def retry_policy(tx: str) -> dict[str, Any]:
    if tx == "external_saga":
        return {"max_attempts": 3, "backoff": "exponential_jitter", "resume": True}
    if tx == "asset_saga":
        return {"max_attempts": 2, "backoff": "fixed", "resume": True}
    return {"max_attempts": 1, "resume": False}


def gate_mode(gates: list[dict[str, str]]) -> str:
    if not gates:
        return "none"
    if any(g["mode"] == "conditional" or g["stage"] == "pre_promote" for g in gates):
        return "conditional"
    return "required"


def make_registry() -> dict[str, Any]:
    actions = []
    for row in parse_catalogue():
        name = row["name"]
        tx = transaction_class(name, row["side_effect"])
        gates = GATES.get(name, [])
        action = {
            "name": name,
            "version": "1.0.0",
            "side_effect": row["side_effect"],
            "required_input": row["required_input"],
            "output_contract": row["output_contract"],
            "permissions": [row["permission"]],
            "provider_dependencies": ["provider_capability"] if name in PROVIDER_ACTIONS else [],
            "gate_summary": row["gate_summary"],
            "gate_mode": gate_mode(gates),
            "gates": gates,
            "audit_required": name not in AUDIT_EXEMPT,
            "idempotency_policy": row["idempotency_policy"],
            "transaction_class": tx,
            "retry_policy": retry_policy(tx),
            "input_schema_ref": f"urn:epi-card:schema:action-payloads:1.0.0#/$defs/{name.replace('-', '_').replace('.', '_')}_input",
            "output_schema_ref": f"urn:epi-card:schema:action-payloads:1.0.0#/$defs/{name.replace('-', '_').replace('.', '_')}_output",
            "success_condition": row["success_condition"],
        }
        actions.append(action)
    return {"version": "1.0.0", "action_count": len(actions), "actions": actions}


def sql_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def generate_pg(registry: dict[str, Any]) -> str:
    cols = (
        "name,version,side_effect,input_schema_ref,output_schema_ref,required_permissions,"
        "provider_dependencies,audit_required,gate_mode,gate_policy,idempotency_policy,retry_policy,transaction_policy"
    )
    lines = ["-- Generated from contracts/action-registry.yaml; apply after database/postgres.sql.", "BEGIN;"]
    for a in registry["actions"]:
        perms = "ARRAY[" + ",".join(sql_quote(x) for x in a["permissions"]) + "]::text[]"
        providers = "ARRAY[" + ",".join(sql_quote(x) for x in a["provider_dependencies"]) + "]::text[]"
        gate_policy = json.dumps({"summary": a["gate_summary"], "gates": a["gates"]}, separators=(",", ":"), ensure_ascii=False)
        retry = json.dumps(a["retry_policy"], separators=(",", ":"))
        vals = ",".join(
            [
                sql_quote(a["name"]), sql_quote(a["version"]), sql_quote(a["side_effect"]),
                sql_quote(a["input_schema_ref"]), sql_quote(a["output_schema_ref"]), perms, providers,
                "true" if a["audit_required"] else "false", sql_quote(a["gate_mode"]),
                sql_quote(gate_policy) + "::jsonb", sql_quote(a["idempotency_policy"]),
                sql_quote(retry) + "::jsonb", sql_quote(a["transaction_class"]),
            ]
        )
        update_cols = [
            "side_effect", "input_schema_ref", "output_schema_ref", "required_permissions",
            "provider_dependencies", "audit_required", "gate_mode", "gate_policy",
            "idempotency_policy", "retry_policy", "transaction_policy",
        ]
        updates = ",".join(f"{c}=EXCLUDED.{c}" for c in update_cols)
        lines.append(f"INSERT INTO action_definition({cols}) VALUES ({vals}) ON CONFLICT (name,version) DO UPDATE SET {updates};")
    lines.extend(["COMMIT;", ""])
    return "\n".join(lines)


def generate_sqlite(registry: dict[str, Any]) -> str:
    cols = (
        "name,version,side_effect,input_schema_ref,output_schema_ref,required_permissions,"
        "provider_dependencies,audit_required,gate_mode,gate_policy,idempotency_policy,retry_policy,transaction_policy"
    )
    lines = ["-- Generated from contracts/action-registry.yaml; apply after database/sqlite.sql.", "BEGIN;"]
    for a in registry["actions"]:
        perms = json.dumps(a["permissions"], separators=(",", ":"))
        providers = json.dumps(a["provider_dependencies"], separators=(",", ":"))
        gate_policy = json.dumps({"summary": a["gate_summary"], "gates": a["gates"]}, separators=(",", ":"), ensure_ascii=False)
        retry = json.dumps(a["retry_policy"], separators=(",", ":"))
        vals = ",".join(
            [
                sql_quote(a["name"]), sql_quote(a["version"]), sql_quote(a["side_effect"]),
                sql_quote(a["input_schema_ref"]), sql_quote(a["output_schema_ref"]),
                sql_quote(perms), sql_quote(providers), "1" if a["audit_required"] else "0",
                sql_quote(a["gate_mode"]), sql_quote(gate_policy), sql_quote(a["idempotency_policy"]),
                sql_quote(retry), sql_quote(a["transaction_class"]),
            ]
        )
        update_cols = [
            "side_effect", "input_schema_ref", "output_schema_ref", "required_permissions",
            "provider_dependencies", "audit_required", "gate_mode", "gate_policy",
            "idempotency_policy", "retry_policy", "transaction_policy",
        ]
        updates = ",".join(f"{c}=excluded.{c}" for c in update_cols)
        lines.append(f"INSERT INTO action_definition({cols}) VALUES ({vals}) ON CONFLICT(name,version) DO UPDATE SET {updates};")
    lines.extend(["COMMIT;", ""])
    return "\n".join(lines)


def main() -> None:
    registry = make_registry()
    REGISTRY.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")
    PG_SEED.write_text(generate_pg(registry), encoding="utf-8")
    SQLITE_SEED.write_text(generate_sqlite(registry), encoding="utf-8")
    print(f"Generated {len(registry['actions'])} actions")


if __name__ == "__main__":
    main()
