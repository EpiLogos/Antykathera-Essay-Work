#!/usr/bin/env python3
"""Build/check the T25 refinement admission receipt.

The September-9 T20/T21 receipt remains immutable historical baseline. T25
adds exactly the seven commissioned S-family Episteme records, preserving the
prior 281 accepted identities/homes while binding the seven new canonical
bodies to their current bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "working/p2-enrichment/receipts/T20-T21-current-census-acceptance.json"
OUTPUT = ROOT / "working/pre-manuscript-refinement-2026-09-10/T25-current-census-acceptance.json"
PRODUCT_ROOT = ROOT / "submission-package/essay/symbolon/episteme/products"
PRODUCTS = (
    ("S", "product-field", "S-World-and-Life.md"),
    ("S0", "product", "S0-Central.md"),
    ("S1", "product", "S1-Actuation.md"),
    ("S2", "product", "S2-AIKit.md"),
    ("S3", "product", "S3-Software-Factory.md"),
    ("S4", "product", "S4-Workcell.md"),
    ("S5", "product", "S5-Quaternal-Logic.md"),
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"unclosed frontmatter: {path}")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError(f"invalid frontmatter: {path}")
    return data


def build() -> dict:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    records = list(base["records"])
    base_ids = {row["record_id"] for row in records}
    if len(records) != 281 or len(base_ids) != 281:
        raise ValueError("historical baseline is not the expected unique 281-record receipt")
    if base_ids & {item[0] for item in PRODUCTS}:
        raise ValueError("historical baseline already contains an S-family identity")

    added = []
    for record_id, record_type, filename in PRODUCTS:
        path = PRODUCT_ROOT / filename
        if not path.is_file():
            raise ValueError(f"missing commissioned product body: {path}")
        fm = frontmatter(path)
        if fm.get("record_id") != record_id:
            raise ValueError(f"declared identity mismatch: {path}")
        if fm.get("record_type") != record_type or fm.get("register") != "episteme":
            raise ValueError(f"declared type/register mismatch: {path}")
        added.append(
            {
                "record_id": record_id,
                "register": "episteme",
                "record_type": record_type,
                "canonical_home": path.relative_to(ROOT).as_posix(),
                "sha256": digest(path),
            }
        )

    records.extend(added)
    if len(records) != 288 or len({row["record_id"] for row in records}) != 288:
        raise ValueError("T25 admission must contain exactly 288 unique records")
    if len({row["canonical_home"] for row in records}) != 288:
        raise ValueError("T25 admission contains duplicate canonical homes")

    counts = dict(base["counts"])
    counts["episteme"] = int(counts["episteme"]) + 7
    if sum(int(value) for value in counts.values()) != 288:
        raise ValueError("register census does not total 288")

    return {
        "standing": (
            "T25 refinement admission: preserves the September-9 281-record accepted baseline "
            "and admits exactly S/S0–S5 as seven new Episteme records. Semantic refinement and "
            "T26 authorial ratification remain distinct from this identity/home admission."
        ),
        "base_receipt": BASE.relative_to(ROOT).as_posix(),
        "counts": counts,
        "records": records,
    }


def render() -> str:
    return json.dumps(build(), ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    args = parser.parse_args()
    if args.project_root.resolve() != ROOT.resolve():
        raise SystemExit("this builder currently binds the repository containing the script")
    expected = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
            print(f"stale or missing: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        report = build()
        print(json.dumps({"admitted": len(report["records"]), "counts": report["counts"]}, indent=2))
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")
    report = build()
    print(json.dumps({"admitted": len(report["records"]), "counts": report["counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
