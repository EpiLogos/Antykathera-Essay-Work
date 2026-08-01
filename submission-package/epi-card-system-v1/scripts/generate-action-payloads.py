#!/usr/bin/env python3
"""Generate the complete v1 action input/output JSON Schema registry.

Every shared action has one input payload schema and one output payload schema. The
generic action envelope selects these definitions by the refs stored in the action registry.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "contracts" / "action-payloads.schema.json"
SCHEMA_ID = "urn:epi-card:schema:action-payloads:1.0.0"


def ref(name: str) -> dict[str, str]:
    return {"$ref": f"#/$defs/{name}"}


def arr(items: dict[str, Any], *, min_items: int | None = None, unique: bool = False) -> dict[str, Any]:
    out: dict[str, Any] = {"type": "array", "items": items}
    if min_items is not None:
        out["minItems"] = min_items
    if unique:
        out["uniqueItems"] = True
    return out


def obj(props: dict[str, Any], required: list[str] | None = None, *, additional: bool = False, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"type": "object", "additionalProperties": additional, "properties": props}
    if required:
        out["required"] = required
    out.update(extra)
    return out


def nullable(schema: dict[str, Any]) -> dict[str, Any]:
    return {"anyOf": [schema, {"type": "null"}]}


def str_enum(*values: str) -> dict[str, Any]:
    return {"type": "string", "enum": list(values)}


def string(min_len: int = 1, max_len: int | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"type": "string", "minLength": min_len}
    if max_len is not None:
        out["maxLength"] = max_len
    return out


def id_output(name: str, *, extra: dict[str, Any] | None = None, required_extra: list[str] | None = None) -> dict[str, Any]:
    props = {name: ref("uuid")}
    if extra:
        props.update(extra)
    req = [name] + (required_extra or [])
    return obj(props, req)


COMMON: dict[str, Any] = {
    "uuid": {"type": "string", "format": "uuid"},
    "nullableUuid": {"type": ["string", "null"], "format": "uuid"},
    "uuidList": arr(ref("uuid"), unique=True),
    "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "semver": {"type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$"},
    "instant": {"type": "string", "format": "date-time"},
    "timezone": {"type": "string", "minLength": 1, "maxLength": 100},
    "locale": {"type": "string", "pattern": "^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$"},
    "disclosure": str_enum("secret", "private", "shared", "public"),
    "projectionKind": str_enum("private", "shared", "public", "provider"),
    "evidenceRegister": str_enum("exact_identity", "ql_derived", "canonical_symbolic", "cross_register", "archetypal_reception", "open_extension"),
    "qlAddress": str_enum("P0", "P1", "P2", "P3", "P4", "P5", "P0′", "P1′", "P2′", "P3′", "P4′", "P5′"),
    "qlPhase": str_enum("bimba", "pratibimba"),
    "qlOccupancy": str_enum("present", "latent", "missing", "unknown", "withheld", "conflicted", "overdetermined"),
    "positionUuidMap": obj({
        "P0": ref("uuid"), "P1": ref("uuid"), "P2": ref("uuid"), "P3": ref("uuid"), "P4": ref("uuid"), "P5": ref("uuid"),
        "P0′": ref("uuid"), "P1′": ref("uuid"), "P2′": ref("uuid"), "P3′": ref("uuid"), "P4′": ref("uuid"), "P5′": ref("uuid")
    }, ["P0", "P1", "P2", "P3", "P4", "P5", "P0′", "P1′", "P2′", "P3′", "P4′", "P5′"]),
    "versionedProfileRef": obj({
        "profile_id": ref("uuid"), "kind": string(), "version": ref("semver"), "content_hash": ref("sha256")
    }, ["profile_id", "kind", "version", "content_hash"]),
    "providerProfileRef": obj({
        "provider": string(), "capability": string(), "model": string(), "profile_id": ref("uuid"),
        "capability_version": ref("semver"), "execution_boundary": str_enum("local", "managed_private", "external")
    }, ["provider", "capability", "model", "profile_id", "capability_version", "execution_boundary"]),
    "resourceInput": {
        "type": "object",
        "additionalProperties": False,
        "required": ["kind"],
        "properties": {
            "kind": str_enum("asset", "uri", "path", "inline_text", "inline_json"),
            "asset_id": ref("uuid"), "uri": {"type": "string", "format": "uri"}, "path": string(),
            "inline_text": {"type": "string"}, "inline_json": {}, "media_type": nullable(string()),
            "filename": nullable(string())
        },
        "allOf": [
            {"if": {"properties": {"kind": {"const": "asset"}}}, "then": {"required": ["asset_id"]}},
            {"if": {"properties": {"kind": {"const": "uri"}}}, "then": {"required": ["uri"]}},
            {"if": {"properties": {"kind": {"const": "path"}}}, "then": {"required": ["path"]}},
            {"if": {"properties": {"kind": {"const": "inline_text"}}}, "then": {"required": ["inline_text"]}},
            {"if": {"properties": {"kind": {"const": "inline_json"}}}, "then": {"required": ["inline_json"]}}
        ]
    },
    "assetRef": obj({
        "asset_id": ref("uuid"), "sha256": ref("sha256"), "media_type": string(), "role": string(),
        "uri": nullable(string()), "byte_length": {"type": ["integer", "null"], "minimum": 0}
    }, ["asset_id", "sha256", "media_type", "role"]),
    "location": obj({
        "latitude": {"type": "number", "minimum": -90, "maximum": 90},
        "longitude": {"type": "number", "minimum": -180, "maximum": 180},
        "altitude_m": {"type": ["number", "null"]}, "precision_m": {"type": ["number", "null"], "minimum": 0},
        "label": nullable(string())
    }, ["latitude", "longitude"]),
    "patchOperation": obj({
        "op": str_enum("add", "remove", "replace", "move", "copy", "test"),
        "path": {"type": "string", "pattern": "^/"}, "from": nullable({"type": "string", "pattern": "^/"}), "value": {}
    }, ["op", "path"]),
    "selector": obj({
        "type": str_enum("json_pointer", "text_quote", "time_range", "page", "region", "uri_fragment"),
        "value": {}
    }, ["type", "value"]),
    "targetRef": obj({"kind": string(), "id": ref("uuid")}, ["kind", "id"]),
    "sourceRef": obj({
        "kind": string(), "id": ref("nullableUuid"), "uri": nullable({"type": "string", "format": "uri"}), "sha256": nullable(ref("sha256"))
    }, ["kind"], oneOf=[{"required": ["id"]}, {"required": ["uri"]}, {"required": ["sha256"]}]),
    "validationFinding": obj({
        "severity": str_enum("info", "warning", "error", "fatal"), "code": string(),
        "path": nullable(string()), "message": string(), "evidence": {"type": "object"}
    }, ["severity", "code", "message", "evidence"]),
    "validationResult": obj({
        "validation_report_id": ref("uuid"), "passed": {"type": "boolean"},
        "findings": arr(ref("validationFinding"))
    }, ["validation_report_id", "passed", "findings"]),
    "approvalDecision": obj({
        "decision": str_enum("approve", "reject", "revoke"), "comment": nullable({"type": "string"}),
        "candidate_hash": nullable(ref("sha256"))
    }, ["decision"]),
    "sourceMemberRef": obj({
        "source_member_id": ref("uuid"), "ordinal": {"type": ["integer", "null"], "minimum": 0}, "member_key": nullable(string())
    }, ["source_member_id"]),
    "mappingConstraint": obj({
        "kind": str_enum("require", "forbid", "prefer", "lock", "leave_unresolved"),
        "target_address": nullable(ref("qlAddress")), "source_member_id": ref("nullableUuid"),
        "rule": string(), "weight": {"type": "number", "minimum": 0, "maximum": 1}
    }, ["kind", "rule", "weight"]),
    "resonanceVector": obj({
        "phase": {"type": "number", "minimum": 0, "exclusiveMaximum": 1},
        "register_log2": {"type": "number"}, "pulse_per_tick": {"type": "number", "minimum": 0},
        "amplitude": {"type": "number", "minimum": 0, "maximum": 1},
        "coherence": {"type": "number", "minimum": 0, "maximum": 1},
        "bandwidth": {"type": "number", "minimum": 0, "maximum": 1},
        "polarity": {"type": "number", "minimum": -1, "maximum": 1},
        "ratios": arr({"type": "string", "pattern": "^[1-9][0-9]*/[1-9][0-9]*$"}, min_items=1, unique=True)
    }, ["phase", "register_log2", "pulse_per_tick", "amplitude", "coherence", "bandwidth", "polarity", "ratios"]),
    "resonanceContribution": obj({
        "source_system": string(), "source_feature": string(), "weight": {"type": "number", "minimum": 0, "maximum": 1},
        "component_vector": ref("resonanceVector"), "register": ref("evidenceRegister"), "rationale": string(),
        "evidence_link_ids": ref("uuidList"), "ql_address": nullable(ref("qlAddress"))
    }, ["source_system", "source_feature", "weight", "component_vector", "register", "rationale", "evidence_link_ids"]),
    "promptPlan": obj({
        "intent": string(), "positive": string(), "negative": {"type": "string"},
        "reference_roles": {"type": "object", "additionalProperties": {"type": "string"}},
        "seed": {"type": ["integer", "null"], "minimum": 0}, "provider_overrides": {"type": "object"}
    }, ["intent", "positive", "negative", "reference_roles"]),
    "rationalTime": obj({
        "value": {"type": "integer", "minimum": 0}, "rate_num": {"type": "integer", "minimum": 1}, "rate_den": {"type": "integer", "minimum": 1}
    }, ["value", "rate_num", "rate_den"]),
    "timeRange": obj({"start": ref("rationalTime"), "duration": ref("rationalTime")}, ["start", "duration"]),
    "outputProfileRef": obj({"profile_id": ref("uuid"), "version": ref("semver"), "role": string()}, ["profile_id", "version", "role"]),
    "providerJobStatus": str_enum("queued", "running", "succeeded", "failed_retryable", "failed_terminal", "cancelled"),
    "modifierSpec": obj({
        "operation": string(), "version": ref("semver"), "parameters": {"type": "object"},
        "determinism_class": str_enum("deterministic", "seeded_best_effort", "nondeterministic")
    }, ["operation", "version", "parameters", "determinism_class"]),
    "publicationMetadata": obj({
        "title": string(), "description": {"type": "string"}, "tags": arr(string(), unique=True),
        "privacy": str_enum("private", "unlisted", "public"), "scheduled_at": nullable(ref("instant")),
        "platform_fields": {"type": "object"}
    }, ["title", "description", "tags", "privacy", "platform_fields"]),
}

A: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}

# 1–12: situated context, sources, and projections
A["pasu.create"] = (
    obj({"kind": str_enum("human", "collective", "anonymous", "other"), "public_handle": nullable(string()),
         "locale": nullable(ref("locale")), "timezone_default": nullable(ref("timezone")), "consent_profile": {"type": "object"}},
        ["kind", "consent_profile"]),
    id_output("pasu_id", extra={"created_at": ref("instant")}, required_extra=["created_at"]),
)
A["pasu.snapshot"] = (
    obj({"pasu_id": ref("uuid"), "attribute_ids": ref("uuidList"), "disclosure": ref("disclosure"),
         "provider_scope": {"type": "object"}}, ["pasu_id", "disclosure", "provider_scope"]),
    obj({"pasu_snapshot_id": ref("uuid"), "snapshot_hash": ref("sha256"), "included_paths": arr(string(), unique=True),
         "redacted_paths": arr(string(), unique=True)}, ["pasu_snapshot_id", "snapshot_hash", "included_paths", "redacted_paths"]),
)
A["session.open"] = (
    obj({"pasu_id": ref("nullableUuid"), "parent_session_id": ref("nullableUuid"), "harness": string(),
         "harness_session_ref": nullable(string()), "timezone": ref("timezone"), "locale": nullable(ref("locale")),
         "disclosure": ref("disclosure")}, ["harness", "timezone", "disclosure"]),
    obj({"session_id": ref("uuid"), "session_key": {"type": "string", "minLength": 32}, "started_at": ref("instant")},
        ["session_id", "session_key", "started_at"]),
)
A["session.resume"] = (
    obj({"session_id": ref("nullableUuid"), "session_key": nullable({"type": "string", "minLength": 32}),
         "last_event_sequence": {"type": ["integer", "null"], "minimum": -1}}, oneOf=[{"required": ["session_id"]}, {"required": ["session_key"]}]),
    obj({"session_id": ref("uuid"), "session_state": {"type": "object"}, "active_run_ids": ref("uuidList"),
         "continuation_actions": arr(string(), unique=True)}, ["session_id", "session_state", "active_run_ids", "continuation_actions"]),
)
A["session.close"] = (
    obj({"session_id": ref("uuid")}, ["session_id"]),
    obj({"session_id": ref("uuid"), "ended_at": ref("instant"), "final_state": {"type": "object"}}, ["session_id", "ended_at", "final_state"]),
)
A["temporal.capture"] = (
    obj({"session_id": ref("uuid"), "observed_at": ref("instant"), "event_time": nullable(ref("instant")),
         "timezone": ref("timezone"), "location": nullable(ref("location")), "astronomy_request": {"type": "object"},
         "astrology_profile": nullable(ref("versionedProfileRef")), "provider_profile": nullable(ref("providerProfileRef")),
         "disclosure_receipt_id": ref("nullableUuid")}, ["session_id", "observed_at", "timezone", "astronomy_request"]),
    obj({"temporal_snapshot_id": ref("uuid"), "astronomical_facts": {"type": "object"},
         "interpretive_contribution_ids": ref("uuidList"), "captured_at": ref("instant")},
        ["temporal_snapshot_id", "astronomical_facts", "interpretive_contribution_ids", "captured_at"]),
)
A["source.ingest"] = (
    obj({"engagement_id": ref("uuid"), "source_kind": string(), "declared_arity": {"type": ["integer", "null"], "minimum": 0},
         "source": ref("resourceInput"), "disclosure": ref("disclosure"), "extraction_mode": str_enum("none", "local", "provider"),
         "provider_profile": nullable(ref("providerProfileRef")), "disclosure_receipt_id": ref("nullableUuid")},
        ["engagement_id", "source_kind", "source", "disclosure", "extraction_mode"]),
    obj({"source_form_id": ref("uuid"), "source_member_ids": ref("uuidList"), "asset_ids": ref("uuidList"),
         "native_form_hash": ref("sha256")}, ["source_form_id", "source_member_ids", "asset_ids", "native_form_hash"]),
)
A["recording.ingest"] = (
    obj({"session_id": ref("uuid"), "engagement_id": ref("nullableUuid"), "recording": ref("resourceInput"),
         "speaker_map": {"type": "object", "additionalProperties": {"type": "string"}},
         "consent_state": str_enum("explicit", "participant", "third_party_restricted", "revoked"),
         "disclosure_scope": ref("disclosure")}, ["session_id", "recording", "consent_state", "disclosure_scope"]),
    obj({"recording_id": ref("uuid"), "asset_id": ref("uuid"), "sha256": ref("sha256")}, ["recording_id", "asset_id", "sha256"]),
)
A["recording.transcribe"] = (
    obj({"recording_id": ref("uuid"), "provider_profile": ref("providerProfileRef"),
         "language_hints": arr(ref("locale"), unique=True), "diarisation_settings": {"type": "object"},
         "disclosure_receipt_id": ref("nullableUuid")}, ["recording_id", "provider_profile", "language_hints", "diarisation_settings"]),
    obj({"transcript_id": ref("uuid"), "segment_ids": ref("uuidList"), "transcript_asset_id": ref("uuid"),
         "language": nullable(ref("locale")), "model_version": string()}, ["transcript_id", "segment_ids", "transcript_asset_id", "model_version"]),
)
A["evidence.link"] = (
    obj({"engagement_id": ref("uuid"), "target": ref("targetRef"), "source": ref("sourceRef"),
         "selector": ref("selector"), "relation": string(), "register": ref("evidenceRegister"), "note": nullable({"type": "string"})},
        ["engagement_id", "target", "source", "selector", "relation", "register"]),
    id_output("evidence_link_id"),
)
A["projection.materialize"] = (
    obj({"engagement_id": ref("uuid"), "projection_kind": ref("projectionKind"), "disclosure_profile": ref("versionedProfileRef"),
         "source_revision_manifest": {"type": "object", "minProperties": 1}, "provider": nullable(string()), "purpose": nullable(string()),
         "disclosure_receipt_id": ref("nullableUuid"), "approval_id": ref("nullableUuid")},
        ["engagement_id", "projection_kind", "disclosure_profile", "source_revision_manifest"]),
    obj({"projection_id": ref("uuid"), "snapshot_hash": ref("sha256"), "included_paths": arr(string(), unique=True),
         "redacted_paths": arr(string(), unique=True), "status": str_enum("draft", "approved")},
        ["projection_id", "snapshot_hash", "included_paths", "redacted_paths", "status"]),
)
A["projection.validate"] = (
    obj({"projection_id": ref("uuid"), "validation_profile": ref("versionedProfileRef")}, ["projection_id", "validation_profile"]),
    ref("validationResult"),
)

# 13–23: attractor, basin, QL, locks, and return
A["attractor.create"] = (
    obj({"kind": string(), "label": string(), "description": nullable({"type": "string"}), "stable_key": nullable(string())}, ["kind", "label"]),
    obj({"attractor_id": ref("uuid"), "revision_id": ref("uuid"), "revision_no": {"const": 1}}, ["attractor_id", "revision_id", "revision_no"]),
)
A["basin.resolve"] = (
    obj({"engagement_id": ref("uuid"), "attractor_revision_id": ref("uuid"), "source_form_ids": ref("uuidList"),
         "context": {"type": "object"}, "lens_profile": ref("versionedProfileRef"), "mapping_constraints": arr(ref("mappingConstraint")),
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["engagement_id", "attractor_revision_id", "source_form_ids", "context", "lens_profile", "mapping_constraints"]),
    obj({"attractor_revision_id": ref("uuid"), "basin_member_ids": ref("uuidList"), "excluded_member_ids": ref("uuidList"),
         "unresolved_member_ids": ref("uuidList"), "status": str_enum("candidate", "canonical")},
        ["attractor_revision_id", "basin_member_ids", "excluded_member_ids", "unresolved_member_ids", "status"]),
)
A["basin.revise"] = (
    obj({"attractor_id": ref("uuid"), "prior_revision_id": ref("uuid"), "patch_operations": arr(ref("patchOperation"), min_items=1),
         "rationale": string(), "approval_id": ref("nullableUuid")}, ["attractor_id", "prior_revision_id", "patch_operations", "rationale"]),
    obj({"attractor_revision_id": ref("uuid"), "revision_no": {"type": "integer", "minimum": 2}, "basin_member_ids": ref("uuidList")},
        ["attractor_revision_id", "revision_no", "basin_member_ids"]),
)
A["ql.initialize"] = (
    obj({"engagement_id": ref("uuid")}, ["engagement_id"]),
    obj({"position_ids": ref("positionUuidMap"), "relation_ids": ref("uuidList"), "traversal": arr(ref("qlAddress"), min_items=12)},
        ["position_ids", "relation_ids", "traversal"]),
)
A["ql.map"] = (
    obj({"engagement_id": ref("uuid"), "source_form_ids": ref("uuidList"), "basin_revision_id": ref("uuid"),
         "lens_profile": ref("versionedProfileRef"), "mapping_constraints": arr(ref("mappingConstraint")),
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["engagement_id", "source_form_ids", "basin_revision_id", "lens_profile", "mapping_constraints"]),
    obj({"frame_revision_id": ref("uuid"), "assignment_ids": ref("uuidList"), "claim_ids": ref("uuidList"),
         "occupancy_summary": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 0}},
         "unresolved_source_member_ids": ref("uuidList"), "status": str_enum("candidate", "approved")},
        ["frame_revision_id", "assignment_ids", "claim_ids", "occupancy_summary", "unresolved_source_member_ids", "status"]),
)
A["ql.reconcile"] = (
    obj({"engagement_id": ref("uuid"), "frame_revision_id": ref("uuid"),
         "scopes": arr(str_enum("conjugate", "complement", "partition_4_2", "partition_3_3", "return"), min_items=1, unique=True),
         "apply_content_mutation": {"type": "boolean"}, "approval_id": ref("nullableUuid")},
        ["engagement_id", "frame_revision_id", "scopes", "apply_content_mutation"]),
    obj({"findings": arr(ref("validationFinding")), "proposed_patch": arr(ref("patchOperation")),
         "new_frame_revision_id": ref("nullableUuid")}, ["findings", "proposed_patch"]),
)
A["ql.validate"] = (
    obj({"engagement_id": ref("uuid"), "frame_revision_id": ref("nullableUuid"), "validation_profile": ref("versionedProfileRef")},
        ["engagement_id", "validation_profile"]),
    ref("validationResult"),
)
A["ql.approve"] = (
    obj({"engagement_id": ref("uuid"), "frame_revision_id": ref("uuid"), "validation_report_id": ref("uuid"),
         "decision": ref("approvalDecision")}, ["engagement_id", "frame_revision_id", "validation_report_id", "decision"]),
    obj({"approval_id": ref("uuid"), "frame_revision_id": ref("uuid"), "status": str_enum("approved", "rejected")},
        ["approval_id", "frame_revision_id", "status"]),
)
A["lock.acquire"] = (
    obj({"engagement_id": ref("uuid"), "target_kind": string(), "target_id": ref("uuid"),
         "field_path": {"type": "string", "pattern": "^/"}, "lock_type": str_enum("exclusive", "advisory"),
         "reason": string(), "expires_at": nullable(ref("instant"))},
        ["engagement_id", "target_kind", "target_id", "field_path", "lock_type", "reason"]),
    obj({"resource_lock_id": ref("uuid"), "acquired_at": ref("instant"), "expires_at": nullable(ref("instant"))},
        ["resource_lock_id", "acquired_at"]),
)
A["lock.release"] = (
    obj({"resource_lock_id": ref("uuid"), "release_reason": string()}, ["resource_lock_id", "release_reason"]),
    obj({"resource_lock_id": ref("uuid"), "released_at": ref("instant"), "release_reason": string()},
        ["resource_lock_id", "released_at", "release_reason"]),
)
A["return.deposit"] = (
    obj({"engagement_id": ref("uuid"), "self_implication": string(), "remainder": string(), "achieved_work": nullable({"type": "string"}),
         "external_implications": arr(string()), "next_ground": string(), "seeds": arr({"type": "object"}),
         "semantic_delta": {"type": "object", "minProperties": 1}, "media_delta": {"type": "object"},
         "next_engagement_id": ref("nullableUuid"), "approval_id": ref("uuid")},
        ["engagement_id", "self_implication", "remainder", "external_implications", "next_ground", "seeds", "semantic_delta", "media_delta", "approval_id"]),
    obj({"return_deposit_id": ref("uuid"), "next_engagement_id": ref("nullableUuid"), "deposited_at": ref("instant")},
        ["return_deposit_id", "deposited_at"]),
)

# 24–29: resonance and art direction
A["resonance.resolve"] = (
    obj({"engagement_id": ref("uuid"), "correspondence_profile_set_id": ref("uuid"),
         "contributions": arr(ref("resonanceContribution"), min_items=1), "approval_id": ref("nullableUuid")},
        ["engagement_id", "correspondence_profile_set_id", "contributions"]),
    obj({"aggregate_state_id": ref("uuid"), "position_state_ids": ref("positionUuidMap"),
         "calculation_receipt_ids": ref("uuidList")}, ["aggregate_state_id", "position_state_ids", "calculation_receipt_ids"]),
)
A["resonance.project"] = (
    obj({"resonance_state_ids": ref("uuidList"), "projection_profiles": arr(ref("versionedProfileRef"), min_items=1)},
        ["resonance_state_ids", "projection_profiles"]),
    obj({"projected_parameter_set_ids": ref("uuidList"), "calculation_receipt_ids": ref("uuidList")},
        ["projected_parameter_set_ids", "calculation_receipt_ids"]),
)
A["resonance.compare"] = (
    obj({"resonance_state_ids": ref("uuidList"), "engagement_ids": ref("uuidList"),
         "modalities": arr(str_enum("audio", "colour", "geometry", "typography", "motion", "editing", "lighting"), unique=True)},
        oneOf=[{"required": ["resonance_state_ids"]}, {"required": ["engagement_ids"]}]),
    obj({"comparisons": arr(obj({"left_id": ref("uuid"), "right_id": ref("uuid"), "component_delta": {"type": "object"},
                                 "profile_delta": {"type": "object"}}, ["left_id", "right_id", "component_delta", "profile_delta"])),
         "nearest_ids": ref("uuidList"), "contrasting_ids": ref("uuidList")}, ["comparisons", "nearest_ids", "contrasting_ids"]),
)
A["art-direction.resolve"] = (
    obj({"engagement_id": ref("uuid"), "projected_parameter_set_ids": ref("uuidList"),
         "constraint_profiles": arr(ref("versionedProfileRef"), min_items=1), "reference_asset_ids": ref("uuidList"),
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["engagement_id", "projected_parameter_set_ids", "constraint_profiles", "reference_asset_ids"]),
    obj({"art_direction_revision_id": ref("uuid"), "status": str_enum("candidate", "canonical"),
         "decision_audit_tick_ids": ref("uuidList")}, ["art_direction_revision_id", "status", "decision_audit_tick_ids"]),
)
A["palette.resolve"] = (
    obj({"engagement_id": ref("uuid"), "colour_projection_id": ref("uuid"), "constraint_profile": ref("versionedProfileRef"),
         "canonical_use": {"type": "boolean"}, "approval_id": ref("nullableUuid")},
        ["engagement_id", "colour_projection_id", "constraint_profile", "canonical_use"]),
    obj({"palette_revision_id": ref("uuid"), "tokens": {"type": "object", "minProperties": 8},
         "contrast_report_id": ref("uuid"), "status": str_enum("candidate", "canonical")},
        ["palette_revision_id", "tokens", "contrast_report_id", "status"]),
)
A["typography.resolve"] = (
    obj({"engagement_id": ref("uuid"), "typography_projection_id": ref("uuid"), "text_set": {"type": "object", "minProperties": 1},
         "font_inventory_asset_ids": ref("uuidList"), "licence_constraints": {"type": "object"},
         "canonical_use": {"type": "boolean"}, "approval_id": ref("nullableUuid")},
        ["engagement_id", "typography_projection_id", "text_set", "font_inventory_asset_ids", "licence_constraints", "canonical_use"]),
    obj({"typography_revision_id": ref("uuid"), "font_asset_ids": ref("uuidList"), "title_outline_plan": {"type": "object"},
         "status": str_enum("candidate", "canonical")}, ["typography_revision_id", "font_asset_ids", "title_outline_plan", "status"]),
)

# 30–37: symbol bank and exact symbol production
A["symbol.search"] = (
    obj({"engagement_id": ref("uuid"), "operation_terms": arr(string(), unique=True), "topology_terms": arr(string(), unique=True),
         "resonance_state_id": ref("nullableUuid"), "basin_revision_id": ref("nullableUuid"),
         "excluded_symbol_family_ids": ref("uuidList"), "limit": {"type": "integer", "minimum": 1, "maximum": 100}},
        ["engagement_id", "operation_terms", "topology_terms", "excluded_symbol_family_ids", "limit"]),
    obj({"candidates": arr(obj({"symbol_family_id": ref("uuid"), "symbol_revision_id": ref("uuid"),
                                 "operation_distance": {"type": "number", "minimum": 0},
                                 "topology_distance": {"type": "number", "minimum": 0},
                                 "resonance_distance": {"type": "number", "minimum": 0},
                                 "basin_overlap": {"type": "number", "minimum": 0, "maximum": 1}},
                                ["symbol_family_id", "symbol_revision_id", "operation_distance", "topology_distance", "resonance_distance", "basin_overlap"])),
         "query_hash": ref("sha256")}, ["candidates", "query_hash"]),
)
A["symbol.propose"] = (
    obj({"engagement_id": ref("uuid"), "source_symbol_revision_ids": ref("uuidList"),
         "resolution_mode": str_enum("reuse", "parameterise", "transform", "combine", "generate_new"),
         "grammar_constraints": {"type": "object", "minProperties": 1}, "promotion_target": nullable(string()),
         "approval_id": ref("nullableUuid")}, ["engagement_id", "source_symbol_revision_ids", "resolution_mode", "grammar_constraints"]),
    obj({"symbol_revision_id": ref("uuid"), "state_plan_id": ref("uuid"), "status": str_enum("candidate", "canonicalization_candidate")},
        ["symbol_revision_id", "state_plan_id", "status"]),
)
A["symbol.generate"] = (
    obj({"symbol_revision_id": ref("uuid"), "provider_profile": ref("providerProfileRef"),
         "prompt_plan": ref("promptPlan"), "reference_asset_ids": ref("uuidList"),
         "disclosure_receipt_id": ref("nullableUuid"), "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["symbol_revision_id", "provider_profile", "prompt_plan", "reference_asset_ids"]),
    obj({"candidate_asset_ids": ref("uuidList"), "provider_job_id": ref("uuid"), "generation_receipt_id": ref("uuid")},
        ["candidate_asset_ids", "provider_job_id", "generation_receipt_id"]),
)
A["symbol.transform"] = (
    obj({"source_symbol_revision_id": ref("uuid"), "operators": arr(obj({"operator": string(), "parameters": {"type": "object"}}, ["operator", "parameters"]), min_items=1),
         "target_resonance_state_ids": ref("uuidList"), "grammar_constraints": {"type": "object"},
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["source_symbol_revision_id", "operators", "target_resonance_state_ids", "grammar_constraints"]),
    obj({"symbol_revision_id": ref("uuid"), "candidate_asset_ids": ref("uuidList"), "geometry_delta": {"type": "object"}},
        ["symbol_revision_id", "candidate_asset_ids", "geometry_delta"]),
)
A["symbol.canonicalize"] = (
    obj({"candidate_revision_id": ref("uuid"), "grammar": {"type": "object", "minProperties": 1}, "svg_asset_id": ref("uuid"),
         "geometry_report_id": ref("uuid"), "approval_id": ref("uuid")},
        ["candidate_revision_id", "grammar", "svg_asset_id", "geometry_report_id", "approval_id"]),
    obj({"symbol_revision_id": ref("uuid"), "derivative_asset_ids": ref("uuidList"), "status": {"const": "canonical"}},
        ["symbol_revision_id", "derivative_asset_ids", "status"]),
)
A["symbol.state.render"] = (
    obj({"symbol_revision_id": ref("uuid"), "state_profile": ref("versionedProfileRef"), "output_profile": ref("outputProfileRef")},
        ["symbol_revision_id", "state_profile", "output_profile"]),
    obj({"state_asset_ids": ref("positionUuidMap"), "mask_asset_ids": ref("uuidList"),
         "loop_anchors": obj({"p5_prime_asset_id": ref("uuid"), "p0_asset_id": ref("uuid")}, ["p5_prime_asset_id", "p0_asset_id"])},
        ["state_asset_ids", "mask_asset_ids", "loop_anchors"]),
)
A["symbol.validate"] = (
    obj({"symbol_revision_id": ref("uuid"), "asset_ids": ref("uuidList"), "validator_profile": ref("versionedProfileRef")},
        ["symbol_revision_id", "asset_ids", "validator_profile"]),
    obj({"validation_report_id": ref("uuid"), "passed": {"type": "boolean"}, "findings": arr(ref("validationFinding")),
         "visual_diff_asset_ids": ref("uuidList")}, ["validation_report_id", "passed", "findings", "visual_diff_asset_ids"]),
)
A["symbol.approve"] = (
    obj({"symbol_revision_id": ref("uuid"), "validation_report_id": ref("uuid"), "decision": ref("approvalDecision")},
        ["symbol_revision_id", "validation_report_id", "decision"]),
    obj({"approval_id": ref("uuid"), "symbol_revision_id": ref("uuid"), "status": str_enum("approved", "rejected")},
        ["approval_id", "symbol_revision_id", "status"]),
)

# 38–52: storyboards, image/video generation, modifiers, composition
A["storyboard.plan"] = (
    obj({"engagement_id": ref("uuid"), "frame_revision_id": ref("uuid"), "art_direction_revision_id": ref("uuid"),
         "symbol_revision_id": ref("uuid"), "audio_palette_revision_id": ref("nullableUuid"),
         "duration_profile": ref("versionedProfileRef"), "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["engagement_id", "frame_revision_id", "art_direction_revision_id", "symbol_revision_id", "duration_profile"]),
    obj({"storyboard_revision_id": ref("uuid"), "scene_pair_ids": {"type": "array", "minItems": 6, "maxItems": 6, "items": ref("uuid"), "uniqueItems": True},
         "scene_atom_ids": {"type": "array", "minItems": 12, "maxItems": 12, "items": ref("uuid"), "uniqueItems": True},
         "storyboard_asset_ids": ref("uuidList"), "status": str_enum("candidate", "production")},
        ["storyboard_revision_id", "scene_pair_ids", "scene_atom_ids", "storyboard_asset_ids", "status"]),
)
A["image.collect"] = (
    obj({"engagement_id": ref("uuid"), "mode": str_enum("search", "import"), "query": nullable(string()),
         "resources": arr(ref("resourceInput")), "rights_requirements": {"type": "object", "minProperties": 1},
         "account_ref": nullable(string()), "external_account_access": {"type": "boolean"}},
        ["engagement_id", "mode", "rights_requirements", "external_account_access"]),
    obj({"asset_ids": ref("uuidList"), "rights_record_ids": ref("uuidList"), "rejected_resources": arr({"type": "object"})},
        ["asset_ids", "rights_record_ids", "rejected_resources"]),
)
A["image.generate"] = (
    obj({"engagement_id": ref("uuid"), "scene_atom_id": ref("nullableUuid"), "symbol_revision_id": ref("nullableUuid"),
         "provider_profile": ref("providerProfileRef"), "prompt_plan": ref("promptPlan"), "reference_asset_ids": ref("uuidList"),
         "disclosure_receipt_id": ref("nullableUuid")},
        ["engagement_id", "provider_profile", "prompt_plan", "reference_asset_ids"],
        oneOf=[{"required": ["scene_atom_id"]}, {"required": ["symbol_revision_id"]}]),
    obj({"candidate_asset_ids": ref("uuidList"), "provider_job_id": ref("uuid"), "generation_receipt_id": ref("uuid")},
        ["candidate_asset_ids", "provider_job_id", "generation_receipt_id"]),
)
A["image.edit"] = (
    obj({"input_asset_id": ref("uuid"), "instructions": string(), "mask_asset_id": ref("nullableUuid"),
         "method": str_enum("deterministic", "provider"), "provider_profile": nullable(ref("providerProfileRef")),
         "disclosure_receipt_id": ref("nullableUuid")}, ["input_asset_id", "instructions", "method"]),
    obj({"output_asset_id": ref("uuid"), "derivation_id": ref("uuid"), "provider_job_id": ref("nullableUuid")},
        ["output_asset_id", "derivation_id"]),
)
A["image.alpha"] = (
    obj({"input_asset_id": ref("uuid"), "method_profile": ref("versionedProfileRef"), "edge_constraints": {"type": "object", "minProperties": 1},
         "target_role": string(), "approval_id": ref("nullableUuid")}, ["input_asset_id", "method_profile", "edge_constraints", "target_role"]),
    obj({"transparent_asset_id": ref("uuid"), "alpha_mask_asset_id": ref("uuid"), "matte_report_id": ref("uuid")},
        ["transparent_asset_id", "alpha_mask_asset_id", "matte_report_id"]),
)
A["scene.plan"] = (
    obj({"storyboard_revision_id": ref("uuid"), "scene_pair_id": ref("nullableUuid"), "scene_atom_id": ref("nullableUuid"),
         "patch_operations": arr(ref("patchOperation"), min_items=1), "approval_id": ref("nullableUuid")},
        ["storyboard_revision_id", "patch_operations"], oneOf=[{"required": ["scene_pair_id"]}, {"required": ["scene_atom_id"]}]),
    obj({"storyboard_revision_id": ref("uuid"), "scene_pair_ids": ref("uuidList"), "scene_atom_ids": ref("uuidList")},
        ["storyboard_revision_id", "scene_pair_ids", "scene_atom_ids"]),
)
A["video.submit"] = (
    obj({"storyboard_revision_id": ref("uuid"), "scope": str_enum("full_storyboard", "scene_pairs", "scene_atoms", "bimba_pass", "pratibimba_pass"),
         "scene_pair_ids": ref("uuidList"), "scene_atom_ids": ref("uuidList"), "provider_profile": ref("providerProfileRef"),
         "prompt_reference_allocation": {"type": "object", "minProperties": 1}, "disclosure_receipt_id": ref("nullableUuid")},
        ["storyboard_revision_id", "scope", "provider_profile", "prompt_reference_allocation"]),
    obj({"provider_job_id": ref("uuid"), "request_hash": ref("sha256"), "status": ref("providerJobStatus")},
        ["provider_job_id", "request_hash", "status"]),
)
A["video.poll"] = (
    obj({"provider_job_id": ref("uuid")}, ["provider_job_id"]),
    obj({"provider_job_id": ref("uuid"), "status": ref("providerJobStatus"), "progress": {"type": "number", "minimum": 0, "maximum": 1},
         "output_asset_ids": ref("uuidList"), "error": nullable({"type": "object"}), "raw_response_asset_id": ref("nullableUuid")},
        ["provider_job_id", "status", "progress", "output_asset_ids"]),
)
A["video.continue"] = (
    obj({"source_video_asset_id": ref("uuid"), "continuation_plan": {"type": "object", "minProperties": 1},
         "provider_profile": ref("providerProfileRef"), "disclosure_receipt_id": ref("nullableUuid")},
        ["source_video_asset_id", "continuation_plan", "provider_profile"]),
    obj({"provider_job_id": ref("uuid"), "candidate_asset_ids": ref("uuidList"), "request_hash": ref("sha256")},
        ["provider_job_id", "candidate_asset_ids", "request_hash"]),
)
A["video.edit"] = (
    obj({"video_asset_id": ref("uuid"), "instructions": string(), "mask_asset_id": ref("nullableUuid"),
         "time_range": nullable(ref("timeRange")), "method": str_enum("deterministic", "provider"),
         "provider_profile": nullable(ref("providerProfileRef")), "disclosure_receipt_id": ref("nullableUuid")},
        ["video_asset_id", "instructions", "method"]),
    obj({"output_asset_id": ref("uuid"), "derivation_id": ref("uuid"), "provider_job_id": ref("nullableUuid")},
        ["output_asset_id", "derivation_id"]),
)
A["plate.accept"] = (
    obj({"scene_atom_id": ref("uuid"), "candidate_asset_id": ref("uuid"), "comparison_report_id": ref("uuid"),
         "decision": ref("approvalDecision")}, ["scene_atom_id", "candidate_asset_id", "comparison_report_id", "decision"]),
    obj({"plate_link_id": ref("uuid"), "approval_id": ref("uuid"), "status": str_enum("accepted", "rejected")},
        ["plate_link_id", "approval_id", "status"]),
)
A["modifier.apply"] = (
    obj({"input_asset_id": ref("uuid"), "modifier": ref("modifierSpec"), "target_role": string(),
         "provider_profile": nullable(ref("providerProfileRef")), "disclosure_receipt_id": ref("nullableUuid"),
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["input_asset_id", "modifier", "target_role"]),
    obj({"output_asset_id": ref("uuid"), "modifier_operation_id": ref("uuid"), "derivation_id": ref("uuid")},
        ["output_asset_id", "modifier_operation_id", "derivation_id"]),
)
A["composition.render"] = (
    obj({"render_plan_id": ref("uuid"), "output_profiles": arr(ref("outputProfileRef"), min_items=1),
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["render_plan_id", "output_profiles"]),
    obj({"rendition_ids": ref("uuidList"), "output_asset_ids": ref("uuidList"), "render_log_asset_id": ref("uuid"),
         "status": str_enum("rendered_candidate", "approved_master")}, ["rendition_ids", "output_asset_ids", "render_log_asset_id", "status"]),
)
A["loop.validate"] = (
    obj({"rendition_id": ref("nullableUuid"), "render_plan_id": ref("nullableUuid"), "threshold_profile": ref("versionedProfileRef")},
        ["threshold_profile"], oneOf=[{"required": ["rendition_id"]}, {"required": ["render_plan_id"]}]),
    obj({"validation_report_id": ref("uuid"), "passed": {"type": "boolean"}, "visual_metrics": {"type": "object"},
         "audio_metrics": {"type": "object"}, "semantic_delta_present": {"type": "boolean"},
         "findings": arr(ref("validationFinding"))},
        ["validation_report_id", "passed", "visual_metrics", "audio_metrics", "semantic_delta_present", "findings"]),
)
A["poster.select"] = (
    obj({"rendition_id": ref("uuid"), "sampling_profile": ref("versionedProfileRef"), "print_constraints": {"type": "object", "minProperties": 1},
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["rendition_id", "sampling_profile", "print_constraints"]),
    obj({"poster_asset_id": ref("uuid"), "candidate_sheet_asset_id": ref("uuid"), "selected_time": ref("rationalTime"),
         "status": str_enum("candidate", "approved")}, ["poster_asset_id", "candidate_sheet_asset_id", "selected_time", "status"]),
)

# 53–57: QL Resonator and audio finishing
A["audio.palette.resolve"] = (
    obj({"engagement_id": ref("uuid"), "resonance_state_ids": ref("uuidList"), "tuning_profile": ref("versionedProfileRef"),
         "resonator_profile": ref("versionedProfileRef"), "spatial_profile": ref("versionedProfileRef"),
         "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["engagement_id", "resonance_state_ids", "tuning_profile", "resonator_profile", "spatial_profile"]),
    obj({"audio_palette_revision_id": ref("uuid"), "state_parameter_set_ids": ref("positionUuidMap"),
         "reference_frequency_hz": {"type": "number", "exclusiveMinimum": 0}, "ratio_set": arr({"type": "string"}, min_items=1, unique=True),
         "status": str_enum("candidate", "canonical")},
        ["audio_palette_revision_id", "state_parameter_set_ids", "reference_frequency_hz", "ratio_set", "status"]),
)
A["audio.render"] = (
    obj({"audio_palette_revision_id": ref("uuid"), "resonator_version": ref("semver"), "output_settings": {"type": "object", "minProperties": 1}},
        ["audio_palette_revision_id", "resonator_version", "output_settings"]),
    obj({"state_asset_ids": ref("positionUuidMap"), "master_layer_asset_ids": ref("uuidList"), "render_receipt_id": ref("uuid")},
        ["state_asset_ids", "master_layer_asset_ids", "render_receipt_id"]),
)
A["audio.analyze"] = (
    obj({"audio_asset_ids": ref("uuidList"), "analysis_profile": ref("versionedProfileRef")}, ["audio_asset_ids", "analysis_profile"]),
    obj({"validation_report_id": ref("uuid"), "analysis_data_asset_ids": ref("uuidList"), "plot_asset_ids": ref("uuidList"),
         "findings": arr(ref("validationFinding"))}, ["validation_report_id", "analysis_data_asset_ids", "plot_asset_ids", "findings"]),
)
A["audio.mix"] = (
    obj({"layer_asset_ids": ref("uuidList"), "video_audio_policy": str_enum("discard", "retain_low", "retain_full", "sidechain", "replace"),
         "mix_plan": {"type": "object", "minProperties": 1}, "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["layer_asset_ids", "video_audio_policy", "mix_plan"]),
    obj({"master_asset_id": ref("uuid"), "stem_asset_ids": ref("uuidList"), "loudness_report_id": ref("uuid"),
         "status": str_enum("candidate", "approved")}, ["master_asset_id", "stem_asset_ids", "loudness_report_id", "status"]),
)
A["audio.loop.validate"] = (
    obj({"audio_asset_id": ref("uuid"), "threshold_profile": ref("versionedProfileRef")}, ["audio_asset_id", "threshold_profile"]),
    obj({"validation_report_id": ref("uuid"), "passed": {"type": "boolean"}, "boundary_metrics": {"type": "object"},
         "findings": arr(ref("validationFinding"))}, ["validation_report_id", "passed", "boundary_metrics", "findings"]),
)

# 58–66: card renditions, packages, OKF, and publication
A["card.render.web"] = (
    obj({"engagement_id": ref("uuid"), "rendition_ids": ref("uuidList"), "projection_id": ref("uuid"),
         "component_version": ref("semver")}, ["engagement_id", "rendition_ids", "projection_id", "component_version"]),
    obj({"web_snapshot_asset_id": ref("uuid"), "static_fallback_asset_ids": ref("uuidList"), "public_slug": nullable(string())},
        ["web_snapshot_asset_id", "static_fallback_asset_ids"]),
)
A["card.render.print"] = (
    obj({"poster_asset_id": ref("uuid"), "symbol_revision_id": ref("uuid"), "ql_names": {"type": "object", "minProperties": 12},
         "ql_summaries": {"type": "object", "minProperties": 12}, "qr_target": {"type": "string", "format": "uri"},
         "print_profile": ref("versionedProfileRef"), "promotion_target": nullable(string()), "approval_id": ref("nullableUuid")},
        ["poster_asset_id", "symbol_revision_id", "ql_names", "ql_summaries", "qr_target", "print_profile"]),
    obj({"front_pdf_asset_id": ref("uuid"), "back_pdf_asset_id": ref("uuid"), "preview_asset_ids": ref("uuidList"),
         "proof_report_id": ref("uuid"), "status": str_enum("candidate", "approved")},
        ["front_pdf_asset_id", "back_pdf_asset_id", "preview_asset_ids", "proof_report_id", "status"]),
)
A["card.package"] = (
    obj({"engagement_id": ref("uuid"), "engagement_revision_no": {"type": "integer", "minimum": 1},
         "projection_id": ref("uuid"), "projection_hash": ref("sha256"),
         "ql_frame_revision_id": ref("uuid"), "ql_frame_hash": ref("sha256"),
         "profile_set_id": ref("uuid"), "profile_set_hash": ref("sha256"),
         "rendition_ids": ref("uuidList"), "okf_export_id": ref("uuid"),
         "package_profile": ref("versionedProfileRef"), "disclosure_scope": str_enum("private", "shared", "public"),
         "approval_id": ref("nullableUuid")},
        ["engagement_id", "engagement_revision_no", "projection_id", "projection_hash",
         "ql_frame_revision_id", "ql_frame_hash", "profile_set_id", "profile_set_hash",
         "rendition_ids", "okf_export_id",
         "package_profile", "disclosure_scope"]),
    obj({"package_export_id": ref("uuid"), "package_asset_id": ref("uuid"), "manifest_hash": ref("sha256"),
         "package_root_sha256": ref("sha256"),
         "manifest_schema_id": {"const": "urn:epi-card:schema:package-manifest:1.0.0"},
         "validation_report_id": ref("uuid")},
        ["package_export_id", "package_asset_id", "manifest_hash", "package_root_sha256", "manifest_schema_id", "validation_report_id"]),
)
A["okf.export"] = (
    obj({"engagement_id": ref("uuid"), "projection_id": ref("uuid"), "export_profile_version": ref("semver"),
         "disclosure_scope": str_enum("private", "shared", "public"), "approval_id": ref("nullableUuid")},
        ["engagement_id", "projection_id", "export_profile_version", "disclosure_scope"]),
    obj({"okf_export_id": ref("uuid"), "bundle_asset_id": ref("uuid"), "manifest_hash": ref("sha256")},
        ["okf_export_id", "bundle_asset_id", "manifest_hash"]),
)
A["okf.validate"] = (
    obj({"bundle_asset_id": ref("uuid"), "okf_version": ref("semver"), "validation_profile": ref("versionedProfileRef")},
        ["bundle_asset_id", "okf_version", "validation_profile"]),
    ref("validationResult"),
)
A["publication.prepare"] = (
    obj({"rendition_id": ref("uuid"), "platform": string(), "account_ref": string(), "metadata": ref("publicationMetadata"),
         "projection_id": ref("uuid"), "disclosure_manifest_hash": ref("sha256")},
        ["rendition_id", "platform", "account_ref", "metadata", "projection_id", "disclosure_manifest_hash"]),
    obj({"publication_id": ref("uuid"), "status": {"const": "prepared"}, "preflight_report_id": ref("uuid")},
        ["publication_id", "status", "preflight_report_id"]),
)
A["publication.approve"] = (
    obj({"publication_id": ref("uuid"), "decision": ref("approvalDecision")}, ["publication_id", "decision"]),
    obj({"approval_id": ref("uuid"), "publication_id": ref("uuid"), "status": str_enum("approved", "rejected", "revoked")},
        ["approval_id", "publication_id", "status"]),
)
A["publication.execute"] = (
    obj({"publication_id": ref("uuid"), "credential_ref": string()}, ["publication_id", "credential_ref"]),
    obj({"publication_id": ref("uuid"), "remote_job_id": nullable(string()), "remote_publication_id": nullable(string()),
         "status": str_enum("submitting", "processing", "published")}, ["publication_id", "status"]),
)
A["publication.poll"] = (
    obj({"publication_id": ref("uuid")}, ["publication_id"]),
    obj({"publication_id": ref("uuid"), "status": str_enum("processing", "published", "failed_retryable", "failed_terminal", "revoked"),
         "remote_publication_id": nullable(string()), "published_at": nullable(ref("instant")), "remote_status": {"type": "object"},
         "raw_response_asset_id": ref("nullableUuid")}, ["publication_id", "status", "remote_status"]),
)


def build() -> dict[str, Any]:
    expected = {
        "pasu.create", "pasu.snapshot", "session.open", "session.resume", "session.close", "temporal.capture", "source.ingest",
        "recording.ingest", "recording.transcribe", "evidence.link", "projection.materialize", "projection.validate", "attractor.create",
        "basin.resolve", "basin.revise", "ql.initialize", "ql.map", "ql.reconcile", "ql.validate", "ql.approve", "lock.acquire",
        "lock.release", "return.deposit", "resonance.resolve", "resonance.project", "resonance.compare", "art-direction.resolve",
        "palette.resolve", "typography.resolve", "symbol.search", "symbol.propose", "symbol.generate", "symbol.transform",
        "symbol.canonicalize", "symbol.state.render", "symbol.validate", "symbol.approve", "storyboard.plan", "image.collect",
        "image.generate", "image.edit", "image.alpha", "scene.plan", "video.submit", "video.poll", "video.continue", "video.edit",
        "plate.accept", "modifier.apply", "composition.render", "loop.validate", "poster.select", "audio.palette.resolve", "audio.render",
        "audio.analyze", "audio.mix", "audio.loop.validate", "card.render.web", "card.render.print", "card.package", "okf.export",
        "okf.validate", "publication.prepare", "publication.approve", "publication.execute", "publication.poll"
    }
    if set(A) != expected:
        raise ValueError(f"Action schema mismatch. Missing={sorted(expected-set(A))}, extra={sorted(set(A)-expected)}")
    defs = dict(COMMON)
    action_index: dict[str, Any] = {}
    for name in sorted(A):
        slug = name.replace("-", "_").replace(".", "_")
        input_name, output_name = f"{slug}_input", f"{slug}_output"
        defs[input_name], defs[output_name] = A[name]
        action_index[name] = {
            "input": f"{SCHEMA_ID}#/$defs/{input_name}",
            "output": f"{SCHEMA_ID}#/$defs/{output_name}",
        }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "Epi-Card Shared Action Payload Schemas",
        "description": "Input and output payloads selected by the validated action registry.",
        "type": "object",
        "additionalProperties": False,
        "properties": {"action": {"type": "string", "enum": sorted(A)}, "payload": {"type": "object"}},
        "required": ["action", "payload"],
        "x-action-index": action_index,
        "$defs": defs,
    }


def main() -> None:
    schema = build()
    OUT.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated {len(A)} input and {len(A)} output schemas")


if __name__ == "__main__":
    main()
