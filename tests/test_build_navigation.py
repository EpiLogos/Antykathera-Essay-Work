"""Real-workspace tests for the generated navigation layer.

The navigation layer is a projection of the relations authors wrote into the
publication body. These tests exercise the actual repository: freshness of the
generated surfaces, resolution of every link they emit, the reading root's
reach, and the rule that a generated page never acquires canonical authority.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
BUILDER = PROJECT / "tools/build-navigation.py"
NAV = PROJECT / "submission-package/essay/symbolon/episteme/maps/navigation"
BODY = PROJECT / "submission-package/essay"
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def run(command: list[str], ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if ok and result.returncode:
        raise AssertionError(f"command failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


def load_builder():
    spec = importlib.util.spec_from_file_location("build_navigation", BUILDER)
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_navigation"] = module
    spec.loader.exec_module(module)
    return module


class NavigationLayerTests(unittest.TestCase):
    def test_real_workspace_navigation_is_fresh(self) -> None:
        run([sys.executable, str(BUILDER), "--project-root", str(PROJECT), "--check"])

    def test_generated_surfaces_declare_generated_locator_authority(self) -> None:
        pages = list(NAV.glob("*.md")) + list((NAV / "intents").glob("*.md"))
        self.assertGreater(len(pages), 20)
        for page in pages:
            head = page.read_text(encoding="utf-8")[:600]
            self.assertIn("generated: true", head, page)
            self.assertIn("authority: generated-locator", head, page)
            self.assertIn("Do not edit by hand", head, page)

    def test_every_generated_link_resolves_inside_the_repository(self) -> None:
        pages = list(NAV.glob("*.md")) + list((NAV / "intents").glob("*.md"))
        for page in pages:
            text = page.read_text(encoding="utf-8")
            for destination in MARKDOWN_LINK.findall(text):
                if destination.startswith(("http://", "https://", "mailto:")):
                    continue
                path_part = destination.partition("#")[0]
                target = (page.parent / path_part).resolve()
                self.assertTrue(target.is_file(), f"{page.relative_to(PROJECT)} -> {destination}")

    def test_reading_root_reaches_the_canonical_field(self) -> None:
        audit = json.loads((NAV / "audit.json").read_text(encoding="utf-8"))
        self.assertEqual("submission-package/essay/README.md", audit["reading_root"])
        # Every canonical class must be fully reachable from the front door by written links.
        for key in (
            "essay", "rooms", "movements", "argument-shelf", "symbolon-root", "matheme", "mytheme",
            "episteme-root", "episteme-arguments", "episteme-conjugate", "episteme-etymologies",
            "episteme-histories", "episteme-dossiers", "episteme-lenses", "episteme-maps",
        ):
            stats = audit["per_class"][key]
            self.assertEqual(0, stats["unreachable"], f"{key}: {stats}")
        self.assertLessEqual(audit["max_depth"], 8)

    def test_curated_paths_are_declared_threads_or_the_spine(self) -> None:
        audit = json.loads((NAV / "audit.json").read_text(encoding="utf-8"))
        self.assertEqual(4, len(audit["paths"]))
        for item in audit["paths"]:
            self.assertGreater(item["linked_movements"], 0, item)
            if item["thread_kind"] == "transverse":
                self.assertGreater(item["declared_members"], 0, item)

    def test_relation_word_detection_prefers_bold_and_stays_beside_the_link(self) -> None:
        builder = load_builder()
        window = "The [root](0-1.md) **grounds** this claim; sources are listed elsewhere."
        offset = window.index("[root]")
        self.assertEqual("grounds", builder.relation_word(window, offset))
        far = "It sources the reading " + ("x " * 40) + "[far](a.md) at the end."
        self.assertIsNone(builder.relation_word(far, far.index("[far]")))
        near = "This record returns to [M24](m24.md) at its close."
        self.assertEqual("returns-to", builder.relation_word(near, near.index("[M24]")))

    def test_generated_navigation_is_not_classified_as_a_canonical_path(self) -> None:
        spec = importlib.util.spec_from_file_location("okf_workspace_under_test", PROJECT / "tools/okf-workspace.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules["okf_workspace_under_test"] = module
        spec.loader.exec_module(module)
        rel = Path("submission-package/essay/symbolon/episteme/maps/navigation/MOC.md")
        self.assertEqual("navigation-projection", module.classify(rel, {}))
        self.assertEqual("generated-locator", module.AUTHORITY_ORDER["navigation-projection"])
        self.assertEqual("path", module.classify(Path("submission-package/essay/symbolon/episteme/maps/mono-poly-two-ones.md"), {}))


if __name__ == "__main__":
    unittest.main()
