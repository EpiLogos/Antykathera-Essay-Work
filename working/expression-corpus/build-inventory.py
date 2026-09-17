#!/usr/bin/env python3
"""E0 source→artifact inventory for the Return-of-Zero Expression corpus.

Rerunnable reconciliation tool (issue #65 Pass C): recompute the canonical
record hashes at the current HEAD, walk the Point-Cloud binding records, and
emit the generated inventory (E0-INVENTORY.json) plus a readable coverage
summary (E0-COVERAGE.md). The generated inventory never supersedes the
canonical authored-world census; it is the accounting view over it.

Usage: python3 working/expression-corpus/build-inventory.py [--point-cloud PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CENSUS = ROOT / "working/pre-manuscript-refinement-2026-09-10/T25-current-census-acceptance.json"
DEFAULT_PC = Path("/Users/admin/Central/Work/Point-Cloud-Demo/production/return-of-zero")

FAMILY_BY_TYPE = {
    "argument": "E2-arguments",
    "canonical-argument": "E2-conjugates",
    "concept": "E3-concepts",
    "product": "E3-products",
    "product-field": "E3-products",
    "history": "E3-histories",
    "dossier": "E3-dossiers",
    "etymology-whole": "E3-etymologies",
    "lens": "E3-lenses-aphorism",
    "aphorism": "E3-lenses-aphorism",
    "matheme": "E4-matheme",
    "root-relation": "E5-symbolon",
    "spine-index": "E5-symbolon",
    "whole-mytheme": "E6-mytheme-wholes",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_bindings(pc: Path) -> dict[str, dict]:
    bindings = {}
    for path in sorted((pc / "bindings").glob("*.binding.json")):
        data = json.loads(path.read_text())
        bindings[data.get("artifact", path.stem)] = data
    return bindings


def scene_index(binding: dict) -> dict[str, dict]:
    """Map source_ref (and record-side ids) to scene entries for one artifact."""
    index = {}
    for scene in binding.get("scenes", []):
        for key in ("source_ref", "record_id", "phase"):
            value = scene.get(key)
            if isinstance(value, str) and value:
                index.setdefault(value, scene)
    return index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--point-cloud", type=Path, default=DEFAULT_PC)
    args = parser.parse_args()
    pc = args.point_cloud

    census = json.loads(CENSUS.read_text())
    bindings = load_bindings(pc)

    # Artifact-level view, validated on disk.
    by_artifact = {b["artifact"]: b for b in bindings.values()}
    binding_file = {b["artifact"]: f"bindings/{p.name}" for p in (pc / "bindings").glob("*.binding.json")
                    for b in [json.loads(p.read_text())]}
    artifacts = []
    for artifact_path in sorted(pc.glob("*/*.journey.json")):
        rel = artifact_path.relative_to(pc).as_posix()
        binding = by_artifact.get(rel)
        journey = json.loads(artifact_path.read_text())
        cover = artifact_path.with_name(artifact_path.stem + ".cover.png")
        artifacts.append({
            "artifact": rel,
            "worker": (binding or {}).get("worker"),
            "family": (binding or {}).get("family"),
            "scenes": len(journey.get("scenes", [])),
            "scene_ids": [s.get("id") for s in journey.get("scenes", [])],
            "cover": cover.name if cover.exists() else None,
            "binding": binding_file.get(rel),
            "binding_status": (binding or {}).get("status"),
            "profile_lineage": (binding or {}).get("profile_lineage"),
        })

    # Scene lookup tables per binding artifact.
    scene_maps = {rel: scene_index(by_artifact[rel]) for rel in by_artifact}

    def find_scene(record_id: str, candidates: list[str]):
        for artifact in candidates:
            sm = scene_maps.get(artifact, {})
            for key in (record_id, record_id.lower(), record_id.lower().removesuffix("p") + "p"):
                if key in sm:
                    return artifact, sm[key]
        return None, None

    # Records.
    stale_receipt = 0
    records_out = []
    for record in census["records"]:
        record_id = record["record_id"]
        path = ROOT / record["canonical_home"]
        actual = sha256(path)
        receipt_fresh = actual == record["sha256"]
        stale_receipt += 0 if receipt_fresh else 1
        family = FAMILY_BY_TYPE.get(record["record_type"], "UNASSIGNED")
        candidates = {
            "E2-arguments": ["arguments-a/roz-a-arguments.journey.json"],
            "E2-conjugates": ["conjugates-a-prime/roz-a-prime-conjugates.journey.json"],
            "E3-concepts": ["episteme/roz-c-concepts-1.journey.json", "episteme/roz-c-concepts-2.journey.json"],
            "E3-products": ["episteme/roz-s-products.journey.json"],
            "E3-histories": ["episteme/roz-histories.journey.json"],
            "E3-dossiers": ["episteme/roz-dossiers.journey.json"],
            "E3-etymologies": ["episteme/roz-etymologies.journey.json"],
            "E3-lenses-aphorism": ["episteme/roz-lenses-aphorism.journey.json", "episteme/roz-ac-root.journey.json"],
            "E5-symbolon": ["symbolon/roz-symbolon-spine.journey.json"],
        }.get(family)
        if record_id == "A/C":
            candidates = ["episteme/roz-ac-root.journey.json"]
        artifact, scene = find_scene(record_id, candidates or [])
        if record["record_type"] == "whole-mytheme":
            slug = record_id.removeprefix("mytheme-")
            artifact = f"mytheme/roz-mytheme-{slug}.journey.json"
            scene = {"scene_id": "whole-artifact"} if (pc / artifact).exists() else None
        if record["record_type"] == "matheme":
            for rel, sm in scene_maps.items():
                if rel.startswith("matheme/") and record_id in sm:
                    artifact, scene = rel, sm[record_id]
                    break
        if record["record_type"] in ("root-relation", "spine-index"):
            short = record_id.removeprefix("symbolon-")
            for rel in ("symbolon/roz-symbolon-spine.journey.json", "symbolon/roz-symbolon-whole.journey.json"):
                sm = scene_maps.get(rel, {})
                if record_id in sm or short in sm:
                    artifact, scene = rel, sm.get(record_id) or sm.get(short)
                    break
        # Hash confidence: scene-level entry, else the binding's record-level block.
        hash_verified = bool(
            scene and any(scene.get(k) == actual for k in ("sha256", "sha256_working_dbf3b17"))
        )
        if not hash_verified and artifact and artifact in by_artifact:
            hash_verified = any(
                r.get("record_id") == record_id and r.get("sha256") == actual
                for r in by_artifact[artifact].get("source_revision", {}).get("records", [])
            )
        records_out.append({
            "record_id": record_id,
            "record_type": record["record_type"],
            "register": record["register"],
            "canonical_home": record["canonical_home"],
            "sha256_actual": actual,
            "sha256_receipt": record["sha256"],
            "receipt_fresh_at_head": receipt_fresh,
            "assigned": family,
            "artifact": artifact,
            "scene_id": (scene or {}).get("scene_id"),
            "binding_hash_verified": hash_verified,
            "coverage": "covered" if (artifact and (pc / artifact).exists() and scene) else "MISSING",
        })

    # Publication surfaces (#0/#5) from the E1 bindings.
    surfaces = []
    e1_rows = [
        ("essay/roz-essay-reading.journey.json", "submission-package/essay/THE-RETURN-OF-ZERO.md", "sovereign essay reading path"),
        ("rooms/roz-room-00-integral-threshold.journey.json", "submission-package/essay/section-rooms/00-integral-threshold", "room §0/1"),
        ("rooms/roz-room-01-differentiating-mind.journey.json", "submission-package/essay/section-rooms/01-differentiating-mind", "room §0"),
        ("rooms/roz-room-02-return-of-zero.journey.json", "submission-package/essay/section-rooms/02-return-of-zero", "room §1"),
        ("rooms/roz-room-03-two-logics.journey.json", "submission-package/essay/section-rooms/03-two-logics", "room §2"),
        ("rooms/roz-room-04-mathematical-substrate.journey.json", "submission-package/essay/section-rooms/04-mathematical-substrate", "room §3"),
        ("rooms/roz-room-05-psychoid-flowering.journey.json", "submission-package/essay/section-rooms/05-psychoid-flowering", "room §4"),
        ("rooms/roz-room-06-objective-internality.journey.json", "submission-package/essay/section-rooms/06-objective-internality", "room §5"),
        ("rooms/roz-room-07-instrument-returns.journey.json", "submission-package/essay/section-rooms/07-instrument-returns", "room §5→0"),
    ]
    movement_files = sorted(ROOT.glob("submission-package/essay/section-rooms/*/movements/*.md"))
    room_scenes = {}
    for artifact, home, label in e1_rows:
        sm = scene_maps.get(artifact, {})
        journey = json.loads((pc / artifact).read_text())
        room_scenes[artifact] = journey
        surfaces.append({
            "surface": home,
            "kind": label,
            "artifact": artifact,
            "scenes": len(journey["scenes"]),
            "scene_ids": [s["id"] for s in journey["scenes"]],
            "coverage": "covered" if (pc / artifact).exists() else "MISSING",
        })
    movement_rows = []
    for mf in movement_files:
        room = mf.parts[-3]
        artifact = f"rooms/roz-room-{room}.journey.json"
        journey = room_scenes.get(artifact) or json.loads((pc / artifact).read_text())
        idx = int(re.match(r"(\d+)", mf.name).group(1))
        scene_id = f"movement-{idx:02d}"
        scene_ids = journey and [s["id"] for s in journey["scenes"]]
        movement_rows.append({
            "surface": str(mf.relative_to(ROOT)),
            "artifact": artifact,
            "scene_id": scene_id,
            "coverage": "covered" if scene_id in (scene_ids or []) else "MISSING",
        })

    covered = sum(1 for r in records_out if r["coverage"] == "covered")
    inventory = {
        "standing": "generated inventory (issue #65) — accounting view, never the canonical census",
        "generated_by": "working/expression-corpus/build-inventory.py",
        "source_revision": {
            "repo": "EpiLogos/Antykathera-Essay-Work",
            "commit": "dbf3b1771724bd56663e4e3410df13e9d3ae681b",
            "census_receipt": str(CENSUS.relative_to(ROOT)),
            "census_records": len(census["records"]),
            "census_receipt_hashes_fresh_at_head": len(census["records"]) - stale_receipt,
            "census_receipt_hashes_stale_at_head": stale_receipt,
            "note": "receipt hashes predate the T23/T24 content repair; actual-bytes hashes are authoritative here",
        },
        "point_cloud_revision": "f257de5 (collection written on top; collection files untracked at inventory time)",
        "counts": {
            "records": len(records_out),
            "records_covered": covered,
            "records_missing": len(records_out) - covered,
            "publication_surfaces": len(surfaces) + len(movement_rows),
            "surfaces_covered": sum(1 for r in surfaces + movement_rows if r["coverage"] == "covered"),
            "artifacts": len(artifacts),
            "scenes_total": sum(a["scenes"] for a in artifacts),
        },
        "artifacts": artifacts,
        "records": records_out,
        "publication_surfaces": surfaces + movement_rows,
    }
    out = ROOT / "working/expression-corpus/E0-INVENTORY.json"
    out.write_text(json.dumps(inventory, indent=1))

    # Readable coverage summary.
    from collections import Counter
    by_family = Counter((r["assigned"], r["coverage"]) for r in records_out)
    lines = [
        "# E0 coverage summary (generated)",
        "",
        f"Source revision: dbf3b17 · census 288 records · covered {covered}/288 · "
        f"receipt hashes stale at head: {stale_receipt}/288",
        f"Publication surfaces covered: {inventory['counts']['surfaces_covered']}/{inventory['counts']['publication_surfaces']}",
        f"Artifacts: {len(artifacts)} · scenes: {inventory['counts']['scenes_total']}",
        "",
        "| family | covered | missing |",
        "|---|---|---|",
    ]
    families = sorted({r["assigned"] for r in records_out})
    for family in families:
        c = by_family.get((family, "covered"), 0)
        m = by_family.get((family, "MISSING"), 0)
        lines.append(f"| {family} | {c} | {m} |")
    missing = [r for r in records_out if r["coverage"] == "MISSING"]
    if missing:
        lines += ["", "## Missing", ""] + [f"- `{r['record_id']}` ({r['record_type']}) → {r['canonical_home']}" for r in missing]
    hash_unverified = [r for r in records_out if r["coverage"] == "covered" and not r["binding_hash_verified"]]
    if hash_unverified:
        lines += ["", "## Covered but binding hash not matched against actual bytes (informational)", ""] + [
            f"- `{r['record_id']}` → {r['artifact']} #{r['scene_id']}" for r in hash_unverified[:40]
        ]
    (ROOT / "working/expression-corpus/E0-COVERAGE.md").write_text("\n".join(lines) + "\n")
    print(f"inventory: {out}")
    print(f"covered {covered}/288 records; {inventory['counts']['surfaces_covered']}/{inventory['counts']['publication_surfaces']} surfaces; "
          f"{len(artifacts)} artifacts, {inventory['counts']['scenes_total']} scenes; receipt-stale {stale_receipt}/288")
    if missing:
        print("MISSING:", ", ".join(r["record_id"] for r in missing))


if __name__ == "__main__":
    main()
