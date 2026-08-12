from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOL = PROJECT_ROOT / "tools" / "curate-main-source-relations.py"
SECTIONS = {"§0/1", "§0", "§1", "§2", "§3", "§4", "§5", "§5→0"}

sys.path.insert(0, str(PROJECT_ROOT / "tools"))
from source_resolver import iter_source_houses


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
        for path in iter_source_houses(PROJECT_ROOT):
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
