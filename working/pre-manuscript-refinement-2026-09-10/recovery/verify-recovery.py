#!/usr/bin/env python3
"""Verify original R2.1 survivors, without admitting an incomplete batch."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import lzma
import re
from pathlib import Path
import sys

HOME = Path(__file__).resolve().parent
ROOT = HOME.parents[2]
FRAGMENT_SHA256 = "48c86f3199c8ea5271c0ec2df780b85a60fa0e18e3ee4d5ef7354ee06834a00f"
PATCH_SHA256 = "0907e6ef3e60c71f384eec010b413d2a9b61bfd7fa2c6e7267a72dad4e648514"
NAMES = {"S-World-and-Life.md", "S1-Actuation.md", "R2-PRODUCT-ALLOCATION.md", "R2-PRODUCT-RETURN.md"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify() -> dict:
    fragment = (HOME.parent / "batches/R2.1/01.xz64part").read_bytes()
    if sha256(fragment) != FRAGMENT_SHA256:
        raise ValueError("Original first-fragment hash changed")
    decoder = lzma.LZMADecompressor()
    prefix = decoder.decompress(base64.b64decode(b"".join(fragment.split()), validate=True)).decode("utf-8")
    fields = {}
    for key in ("batch", "source_main", "source_tree", "standing", "patch_sha256", "authored_preimages", "authored_postimages"):
        match = re.search(re.escape(json.dumps(key)) + r"\s*:\s*", prefix)
        if match is None:
            raise ValueError(f"Missing original manifest field: {key}")
        start = match.end()
        fields[key] = json.JSONDecoder().raw_decode(prefix, start)[0]
    pre, post = fields["authored_preimages"], fields["authored_postimages"]
    if len(pre) != 62 or set(pre) != set(post) or fields["patch_sha256"] != PATCH_SHA256:
        raise ValueError("Original authored-file manifest differs from the pinned batch")
    expected = {path for path in post if Path(path).name in NAMES}
    if len(expected) != 4:
        raise ValueError("Survivor names are not unique in the original manifest")
    recovered = {}
    for path in sorted(expected):
        original = HOME / "originals" / (Path(path).name + ".original")
        content = original.read_bytes()
        digest = sha256(content)
        if digest != post[path]:
            raise ValueError(f"Survivor is not the original postimage: {path}")
        recovered[path] = {"sha256": digest, "bytes": len(content), "recovery_path": original.relative_to(ROOT).as_posix()}
    missing = {path: digest for path, digest in post.items() if path not in recovered}
    preimage_conflicts = []
    for path, digest in pre.items():
        target = ROOT / path
        actual = sha256(target.read_bytes()) if target.is_file() else None
        if actual != digest:
            preimage_conflicts.append(path)
    return {
        "kind": "R2.1-original-custody-not-admission", "original_manifest": fields,
        "fragment_sha256": FRAGMENT_SHA256, "original_stream_complete": decoder.eof,
        "recovered": recovered, "unrecovered_postimages": missing,
        "recovered_count": len(recovered), "unrecovered_count": len(missing),
        "current_preimage_conflicts": preimage_conflicts,
        "admission_ready": False,
        "boundary": "Original complete patch and all postimages remain required. Custody is not R2 admission, R5 semantic review, or T26 ratification."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        report = verify()
    except (OSError, ValueError, lzma.LZMAError) as error:
        print(f"RECOVERY VERIFICATION FAILED: {error}", file=sys.stderr)
        return 1
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.require_complete:
        print("INCOMPLETE ORIGINAL BATCH: canonical admission refused", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
