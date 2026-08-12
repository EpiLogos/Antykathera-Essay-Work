"""Real ontology tests for the register layer of the Return of Zero workspace.

The register is the content's own anatomy, declared in frontmatter and
independent of node type. These tests exercise the real workspace and the real
tool commands: the unratified register census, register-carrying status,
context, effects, and find outputs, the concept/path-to-episteme domain rule,
dialogue-record evidence boundaries, and the writing-context packet.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
TOOL = PROJECT / "tools/okf-workspace.py"
HARNESS = PROJECT / "tools/project-agent-harness.py"

sys.path.insert(0, str(PROJECT / "tools"))
from source_resolver import iter_source_houses  # noqa: E402


def run_tool(tool: Path, root: Path, *args: str) -> dict:
    if tool == HARNESS:
        command = [sys.executable, str(tool), args[0], "--project-root", str(root), *args[1:]]
    else:
        command = [sys.executable, str(tool), "--project-root", str(root), *args]
    result = subprocess.run(
        [*command, "--json"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"tool failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return json.loads(result.stdout)


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = text.split("---", 2)
    if len(match) < 3:
        return {}
    return yaml.safe_load(match[1]) or {}


def build_fixture(root: Path) -> None:
    """A real minimal canonical tree exercising register mechanics."""
    section_dir = root / "submission-package/essay/section-rooms/00-integral-threshold/movements"
    argument_dir = root / "submission-package/essay/section-rooms/arguments"
    concept_dir = root / "symbolon/episteme/concepts"
    path_dir = root / "symbolon/episteme/maps"
    for directory in (section_dir, argument_dir, concept_dir, path_dir):
        directory.mkdir(parents=True)

    (section_dir / "01-s01-p0-question-before-mechanism.md").write_text(
        "---\n"
        "title: Fixture Movement\n"
        "node_type: section\n"
        "register: episteme\n"
        "sequence: 1\n"
        "---\n"
        "# Fixture Movement\n\n"
        "## Movement thesis\n\nThe fixture movement is claimed in the episteme register.\n\n"
        "The movement depends on [[zero]] and opens [[apoha]] at the boundary.\n",
        encoding="utf-8",
    )
    (argument_dir / "01-fixture-argument.md").write_text(
        "---\n"
        "title: Fixture Argument\n"
        "node_type: claim\n"
        "register: matheme\n"
        "claim_status: Argued\n"
        "---\n"
        "# Fixture Argument\n\n"
        "## Claim\n\nThe claim is derived in the matheme register.\n\n"
        "## Warrant\n\nThe warrant is stated locally.\n",
        encoding="utf-8",
    )
    (concept_dir / "zero.md").write_text(
        "---\n"
        "title: Zero\n"
        "node_type: concept\n"
        "register: episteme\n"
        "claim_status: Argued\n"
        "---\n"
        "# Zero\n\n"
        "## Definition\n\nZero is the sign for no-counted-thing.\n\n"
        "## In the argument\n\nZero grounds the fixture movement and opens "
        "[[fixture-path]] and [[01-fixture-argument]].\n",
        encoding="utf-8",
    )
    (concept_dir / "apoha.md").write_text(
        "---\n"
        "title: Apoha\n"
        "node_type: concept\n"
        "register: matheme\n"
        "claim_status: Argued\n"
        "---\n"
        "# Apoha\n\n"
        "## Definition\n\nDetermination through exclusion.\n\n"
        "## In the argument\n\nThe fixture movement opens it.\n",
        encoding="utf-8",
    )
    (path_dir / "fixture-path.md").write_text(
        "---\n"
        "title: Fixture Path\n"
        "node_type: path\n"
        "register: episteme\n"
        "---\n"
        "# Fixture Path\n\n"
        "A declared route through the fixture.\n",
        encoding="utf-8",
    )


class RegisterCensusTests(unittest.TestCase):
    def test_register_census_is_a_real_unratified_debt(self) -> None:
        status = run_tool(TOOL, PROJECT, "status")
        census = status["register_census"]
        expected = (
            status["counts"]["section"]
            + status["counts"]["argument"]
            + status["counts"]["concept"]
            + status["counts"]["path"]
            + status["counts"]["argument-map"]
        )
        self.assertEqual(census["canonical_nodes"], expected)
        # Concepts and paths are ratified to episteme; the 48 movements, 21
        # arguments and the argument map still await Frank's per-node register.
        declared = status["counts"]["concept"] + status["counts"]["path"]
        self.assertEqual(census["declared"], declared)
        self.assertEqual(census["missing"], expected - declared)

        doctor = run_tool(TOOL, PROJECT, "doctor")
        missing_paths = {
            debt["path"]
            for debt in doctor["debts"]
            if debt["kind"] == "missing-register"
        }
        self.assertEqual(missing_paths, set(census["missing_paths"]))


class RegisterFlowTests(unittest.TestCase):
    def test_register_flows_through_status_find_context_and_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_fixture(root)

            status = run_tool(TOOL, root, "status")
            self.assertEqual(status["register_census"]["declared"], 5)
            self.assertEqual(status["register_census"]["missing"], 0)
            self.assertEqual(status["registers"]["episteme"], 3)
            self.assertEqual(status["registers"]["matheme"], 2)

            matheme_hits = run_tool(
                TOOL, root, "find", "apoha", "--register", "matheme"
            )
            self.assertEqual(
                {hit["path"] for hit in matheme_hits["hits"]},
                {"symbolon/episteme/concepts/apoha.md"},
            )
            episteme_hits = run_tool(
                TOOL, root, "find", "zero", "--register", "episteme"
            )
            self.assertIn(
                "symbolon/episteme/concepts/zero.md",
                {hit["path"] for hit in episteme_hits["hits"]},
            )
            self.assertNotIn(
                "symbolon/episteme/concepts/apoha.md",
                {hit["path"] for hit in episteme_hits["hits"]},
            )

            context = run_tool(
                TOOL, root, "context", "01-s01-p0-question-before-mechanism"
            )
            self.assertEqual(context["entry"]["register"], "episteme")
            self.assertEqual(context["register"], "episteme")
            self.assertIn("register", context["status_axes"])
            self.assertIn("episteme", context["status_axes"]["register"])

            effects = run_tool(TOOL, root, "effects", "zero")
            self.assertEqual(effects["registers"]["root"], "episteme")
            self.assertTrue(effects["registers"]["carriers"])

    def test_concept_and_path_domain_rule_is_enforced_and_compositions_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_fixture(root)
            (root / "submission-package/essay/section-rooms/arguments/02-fixture-cross.md").write_text(
                "---\n"
                "title: Fixture Cross\n"
                "node_type: claim\n"
                "register: matheme/mytheme\n"
                "claim_status: Argued\n"
                "---\n"
                "# Fixture Cross\n\n"
                "## Claim\n\nA declared cross-register composition.\n",
                encoding="utf-8",
            )

            doctor = run_tool(TOOL, root, "doctor")
            mismatches = {
                debt["path"]: debt["detail"]
                for debt in doctor["debts"]
                if debt["kind"] == "register-domain-mismatch"
            }
            self.assertEqual(
                mismatches,
                {
                    "symbolon/episteme/concepts/apoha.md": (
                        "concept must declare register episteme, found matheme"
                    )
                },
            )
            invalid = {
                debt["path"]
                for debt in doctor["debts"]
                if debt["kind"] == "invalid-register"
            }
            self.assertNotIn(
                "submission-package/essay/section-rooms/arguments/02-fixture-cross.md", invalid
            )
            self.assertNotIn(
                "symbolon/episteme/concepts/zero.md", mismatches
            )

            (root / "submission-package/essay/section-rooms/arguments/03-fixture-invalid.md").write_text(
                "---\n"
                "title: Fixture Invalid\n"
                "node_type: claim\n"
                "register: topological\n"
                "claim_status: Argued\n"
                "---\n"
                "# Fixture Invalid\n\n"
                "## Claim\n\nA register value outside the declared vocabulary.\n",
                encoding="utf-8",
            )
            doctor = run_tool(TOOL, root, "doctor")
            invalid = {
                debt["path"]
                for debt in doctor["debts"]
                if debt["kind"] == "invalid-register"
            }
            self.assertIn(
                "submission-package/essay/section-rooms/arguments/03-fixture-invalid.md", invalid
            )

    def test_writing_context_packet_carries_register(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_fixture(root)
            packet = run_tool(
                HARNESS,
                root,
                "writing-context",
                "01-s01-p0-question-before-mechanism",
            )
            self.assertEqual(packet["register"], "episteme")
            self.assertTrue(packet["claim"])

        real_packet = run_tool(
            HARNESS, PROJECT, "writing-context", "14-s1-p1-sunya-operational"
        )
        self.assertIn("register", real_packet)


class DialogueRecordBoundaryTests(unittest.TestCase):
    def test_dialogue_records_carry_no_citation_or_quote_status(self) -> None:
        dialogue_houses = [
            house
            for house in iter_source_houses(PROJECT)
            if frontmatter(house).get("record_type") == "dialogue-record"
        ]
        self.assertTrue(dialogue_houses)
        for house in dialogue_houses:
            data = frontmatter(house)
            self.assertEqual(data.get("dialogue_role"), "provenance-of-thinking")
            self.assertEqual(data.get("evidence_status"), "never-evidence")
            for key in ("citation_status", "quote_status", "quotation_status"):
                self.assertNotIn(key, data, f"{house}: {key}")

        doctor = run_tool(TOOL, PROJECT, "doctor")
        self.assertNotIn("dialogue-record-evidence-status", doctor["debt_counts"])


if __name__ == "__main__":
    unittest.main()
