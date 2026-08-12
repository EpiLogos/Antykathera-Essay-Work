from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
BANK = PROJECT / "submission-package/essay/symbolon/episteme/sources"
SOURCES = BANK / "sources"

sys.path.insert(0, str(PROJECT / "tools"))
from source_resolver import iter_source_houses, resolve_source_house


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1]) or {}


class CanonicalSourceTests(unittest.TestCase):
    def test_optional_notes_do_not_change_or_invalidate_source_projections(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copied_bank = (
                root / "submission-package/essay/symbolon/episteme/sources"
            )
            shutil.copytree(BANK, copied_bank)
            house = resolve_source_house(root, "kaplan-1999-nothing-that-is")
            self.assertIsNotNone(house)
            note = house.parent / "NOTES.md"
            note.write_text(
                "# Frank's notes\n\nA provisional quotation and an unfinished insight.\n",
                encoding="utf-8",
            )
            before = hashlib.sha256(note.read_bytes()).hexdigest()

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT / "tools/build-source-projections.py"),
                    "--project-root",
                    str(root),
                    "--check",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(before, hashlib.sha256(note.read_bytes()).hexdigest())

    def test_every_source_has_one_clean_canonical_file(self) -> None:
        paths = sorted(iter_source_houses(PROJECT))
        self.assertGreaterEqual(len(paths), 83)
        ids: set[str] = set()
        for path in paths:
            data = frontmatter(path)
            source_id = data["source_id"]
            self.assertEqual(path.parent.name, source_id)
            self.assertNotIn(source_id, ids)
            ids.add(source_id)
            self.assertEqual("source-house", data["node_type"])
            self.assertEqual("canonical-source-house", data["ownership"])
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("SOURCE-HOUSE:", text)
            self.assertNotIn("migration_status", text)
            self.assertNotIn("Migration witnesses", text)

    def test_split_source_system_is_absent(self) -> None:
        for name in ("records", "quotes", "study-dossiers"):
            self.assertFalse((BANK / name).exists(), name)
        for name in (
            "quote-ledger.md",
            "quote-intake-template.md",
            "quote-intake-vaswani-et-al-2017-attention.md",
            "source-record-template.md",
        ):
            self.assertFalse((BANK / name).exists(), name)

    def test_all_projected_passages_resolve_once(self) -> None:
        ledger = (BANK / "PASSAGE-LEDGER.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)#]+/SOURCE\.md)#([^)]+)\)", ledger)
        self.assertTrue(links)
        seen: set[str] = set()
        for relative, passage_id in links:
            self.assertNotIn(passage_id, seen)
            seen.add(passage_id)
            text = (BANK / relative).read_text(encoding="utf-8")
            self.assertEqual(1, text.count(f'<a id="{passage_id}"></a>'))

    def test_kaplan_contains_bibliography_passage_and_full_reading_material(self) -> None:
        house = resolve_source_house(PROJECT, "kaplan-1999-nothing-that-is")
        self.assertIsNotNone(house)
        text = house.read_text(encoding="utf-8")
        for required in (
            "## Bibliographic identity",
            "## Chicago 18 forms",
            "kaplan-1999-nothing-that-is-q001",
            "## Scholarly reading and worked material",
            "## Historical reading spine",
            "### Division by zero: run the ordinary-field collapse",
            "### `0/1` and `1/0`: build the rational interval",
            "### Von Neumann ordinals: build three numbers from the empty set",
            "### Kaplan's NOR route",
        ):
            self.assertIn(required, text)

    def test_previously_missing_van_eenwyk_source_is_present(self) -> None:
        path = resolve_source_house(PROJECT, "van-eenwyk-1991-strange-attractors")
        self.assertIsNotNone(path)
        self.assertTrue(path.is_file())
        self.assertEqual("van-eenwyk-1991-strange-attractors", frontmatter(path)["source_id"])

    def test_source_projections_are_reproducible(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PROJECT / "tools/build-source-projections.py"), "--project-root", str(PROJECT), "--check"],
            cwd=PROJECT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
