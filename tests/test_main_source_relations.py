from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOL = PROJECT_ROOT / "tools" / "curate-main-source-relations.py"
SOURCE_ROOT = PROJECT_ROOT / "essay-workshop" / "sources-texts-references" / "source-bank" / "sources"
SECTIONS = {"§0/1", "§0", "§1", "§2", "§3", "§4", "§5", "§5→0"}


class MainSourceRelationTests(unittest.TestCase):
    def test_curation_is_current_and_covers_every_section(self) -> None:
        result = subprocess.run(
            [sys.executable, str(TOOL), "--project-root", str(PROJECT_ROOT), "--check"],
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        covered: set[str] = set()
        for path in SOURCE_ROOT.glob("*/SOURCE.md"):
            text = path.read_text(encoding="utf-8")
            payload = text.split("---", 2)[1]
            data = yaml.safe_load(payload) or {}
            for relation in data.get("main_source_for", []):
                section, separator, function = str(relation).partition(" · ")
                self.assertEqual(separator, " · ", (path, relation))
                self.assertTrue(function.strip(), (path, relation))
                covered.add(section)
        self.assertEqual(covered, SECTIONS)


if __name__ == "__main__":
    unittest.main()
