import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
OKF = PROJECT / "tools/okf-workspace.py"
PROJECTIONS = PROJECT / "tools/build-source-projections.py"
BANK = PROJECT / "submission-package/essay/symbolon/episteme/sources"

sys.path.insert(0, str(PROJECT / "tools"))
from source_resolver import iter_source_houses, resolve_source_house


class SourceProjectionAndRetrievalTests(unittest.TestCase):
    maxDiff = None

    def okf(self, *args: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(OKF), "--project-root", str(PROJECT), *args, "--json"],
            cwd=PROJECT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_main_sources_are_generated_by_section_and_link_only_canonical_houses(self):
        subprocess.run(
            [sys.executable, str(PROJECTIONS), "--project-root", str(PROJECT)],
            cwd=PROJECT,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            [sys.executable, str(PROJECTIONS), "--project-root", str(PROJECT), "--check"],
            cwd=PROJECT,
            check=True,
            capture_output=True,
            text=True,
        )
        text = (BANK / "MAIN-SOURCES.md").read_text(encoding="utf-8")
        section_one = text.split("## §1 — Return of Zero", 1)[1].split("\n## ", 1)[0]
        self.assertIn("kaplan-1999-nothing-that-is", section_one)
        self.assertIn(
            resolve_source_house(PROJECT, "kaplan-1999-nothing-that-is")
            .relative_to(BANK)
            .as_posix(),
            section_one,
        )
        self.assertNotIn("source-bank/records/", text)
        self.assertNotIn("source-bank/quotes/", text)
        self.assertNotIn("_No main source declared._", text)
        projected_relations = re.findall(
            r"^- \[.+?\]\([^)#]+/SOURCE\.md\)", text, re.MULTILINE
        )
        canonical_relations = 0
        for source_house in iter_source_houses(PROJECT):
            source_text = source_house.read_text(encoding="utf-8")
            frontmatter = source_text.split("---", 2)[1]
            data = yaml.safe_load(frontmatter) or {}
            raw_relations = data.get("main_source_for") or []
            if isinstance(raw_relations, str):
                raw_relations = [raw_relations]
            canonical_relations += len(raw_relations)
        self.assertEqual(canonical_relations, len(projected_relations))

    def test_every_passage_projection_fragment_resolves_to_the_canonical_house(self):
        ledger = (BANK / "PASSAGE-LEDGER.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)#]+/SOURCE\.md)#([^)]+)\)", ledger)
        self.assertTrue(links)
        for relative, fragment in links:
            source = BANK / relative
            self.assertTrue(source.is_file(), relative)
            self.assertIn(f'<a id="{fragment}"></a>', source.read_text(encoding="utf-8"))

    def test_human_and_agent_route_from_section_to_movement_passage_and_reading(self):
        context = self.okf("section-context", "14-s1-p1-sunya-operational", "--depth", "2")
        self.assertEqual("14-s1-p1-sunya-operational", context["entry"]["id"])
        self.assertIn("reading-02-return-of-zero", {node["id"] for node in context["reading_paths"]})
        self.assertIn("room-02-return-of-zero", {node["id"] for node in context["rooms"]})
        passage = next(
            row
            for row in context["passages"]
            if row["passage_id"] == "colebrooke-1817-brahmagupta-bhaskara-q001"
        )["canonical"]
        self.assertTrue(passage["canonical_path"].endswith("/SOURCE.md"))
        self.assertEqual("#colebrooke-1817-brahmagupta-bhaskara-q001", passage["anchor"])
        self.assertTrue(passage["locator"])
        self.assertEqual("quotation-ready.", passage["quotation_status"])
        opened = self.okf("open", "colebrooke-1817-brahmagupta-bhaskara-q001")
        self.assertEqual(passage["canonical_path"], opened["canonical_path"])
        self.assertEqual(passage["locator"], opened["locator"])

        effects = self.okf("effects", "kaplan-1999-nothing-that-is", "--depth", "3")
        self.assertIn(
            "14-s1-p1-sunya-operational",
            {node["id"] for node in effects["consumers"]["sections"]},
        )
        self.assertIn(
            "12-core-theorem-bridge",
            {node["id"] for node in effects["consumers"]["arguments"]},
        )

    def test_doctor_clears_canonical_source_and_room_integrity_debts(self):
        doctor = self.okf("doctor")
        forbidden = {
            "duplicate-source-house",
            "duplicate-passage-id",
            "dangling-room-link",
            "dangling-room-fragment",
            "missing-passage-locator",
            "missing-passage-status",
            "missing-passage-provenance",
        }
        self.assertTrue(forbidden.isdisjoint(doctor["debt_counts"]), doctor["debt_counts"])

    def test_projection_check_marks_all_human_views_stale_after_a_real_source_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            (root / "submission-package/essay/symbolon/episteme/sources").mkdir(parents=True)
            subprocess.run(
                ["cp", "-R", str(BANK) + "/.", str(root / "submission-package/essay/symbolon/episteme/sources")],
                check=True,
            )
            subprocess.run(
                [sys.executable, str(PROJECTIONS), "--project-root", str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            kaplan = resolve_source_house(root, "kaplan-1999-nothing-that-is")
            self.assertIsNotNone(kaplan)
            kaplan.write_text(kaplan.read_text(encoding="utf-8") + "\n<!-- freshness probe -->\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(PROJECTIONS), "--project-root", str(root), "--check"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(1, result.returncode)
            for name in ("MAIN-SOURCES.md", "SOURCE-INDEX.md", "PASSAGE-LEDGER.md"):
                self.assertIn(f"stale:submission-package/essay/symbolon/episteme/sources/{name}", result.stderr)


if __name__ == "__main__":
    unittest.main()
