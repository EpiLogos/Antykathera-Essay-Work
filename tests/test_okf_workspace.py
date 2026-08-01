import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
TOOL = PROJECT / "tools" / "okf-workspace.py"


class OkfWorkspaceTests(unittest.TestCase):
    maxDiff = None

    def run_tool(self, *args: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(TOOL), "--project-root", str(PROJECT), *args, "--json"],
            cwd=PROJECT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return json.loads(result.stdout)

    def test_optional_source_notes_are_readable_without_becoming_verification_debt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_dir = (
                root
                / "essay-workshop/sources-texts-references/source-bank/sources/example-work"
            )
            source_dir.mkdir(parents=True)
            (source_dir / "SOURCE.md").write_text(
                "---\n"
                "title: Example Work\n"
                "source_id: example-work\n"
                "node_type: source-house\n"
                "ownership: canonical-source-house\n"
                "---\n"
                "# Example Work\n",
                encoding="utf-8",
            )
            (source_dir / "NOTES.md").write_text(
                "# My encounter with this source\n\n"
                "This may become important through [[an unfinished relation]].\n\n"
                "> A copied passage whose locator I have not checked yet.\n",
                encoding="utf-8",
            )

            def run(*args: str) -> dict:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(TOOL),
                        "--project-root",
                        str(root),
                        *args,
                        "--json",
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                return json.loads(result.stdout)

            note = run("open", "notes-example-work")
            self.assertEqual("source-notes", note["artifact_type"])
            self.assertEqual("authorial-notes", note["authority"])
            self.assertIn("unfinished relation", note["body"])

            links = run("links", "example-work")
            self.assertIn(
                (
                    "essay-workshop/sources-texts-references/source-bank/sources/"
                    "example-work/NOTES.md",
                    "has-notes",
                ),
                {(edge["target"], edge["relation"]) for edge in links["edges"]},
            )

            doctor = run("doctor")
            self.assertFalse(
                any(debt["path"].endswith("/NOTES.md") for debt in doctor["debts"]),
                doctor["debts"],
            )

    def test_status_discovers_the_real_typed_workspace(self):
        result = self.run_tool("status")
        counts = result["counts"]
        self.assertEqual(
            counts["section"],
            len(list((PROJECT / "essay-workshop/nodes/sections").glob("*.md"))),
        )
        self.assertEqual(
            counts["argument"],
            len(list((PROJECT / "essay-workshop/nodes/arguments").glob("*.md"))),
        )
        self.assertGreaterEqual(counts["concept"], 9)
        self.assertNotIn("source-record", counts)
        source_count = len(
            list(
                (
                    PROJECT
                    / "essay-workshop/sources-texts-references/source-bank/sources"
                ).glob("*/SOURCE.md")
            )
        )
        self.assertEqual(counts["source-house"], source_count)
        self.assertEqual(result["canonical_source_count"], source_count)
        ledger = (
            PROJECT
            / "essay-workshop/sources-texts-references/source-bank/PASSAGE-LEDGER.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(
            result["passage_count"],
            len(re.findall(r"\]\(sources/[^)#]+/SOURCE\.md#[^)]+\)", ledger)),
        )
        self.assertNotIn("quote-dossier", counts)
        self.assertNotIn("source-study", counts)
        self.assertNotIn("source-migration-witness", counts)
        # Active room surfaces only; archived room scaffolds are deliberately excluded.
        self.assertEqual(counts["room-artifact"], 9)
        self.assertEqual(counts["room-reading-path"], 2)
        self.assertGreaterEqual(counts["governing-document"], 2)
        self.assertTrue(result["authority_classes"])

    def test_find_searches_substantive_bodies_not_only_metadata(self):
        result = self.run_tool("find", "circumscription without circumstance", "--limit", "10")
        paths = {hit["path"] for hit in result["hits"]}
        self.assertIn("essay-workshop/nodes/sections/39-s5-p2-j-space.md", paths)
        self.assertIn("essay-workshop/nodes/concepts/j-space.md", paths)
        self.assertTrue(all(hit["matched_fields"] for hit in result["hits"]))

    def test_links_and_backlinks_resolve_across_node_types(self):
        outgoing = self.run_tool("links", "39-s5-p2-j-space")
        self.assertIn(
            "essay-workshop/nodes/sections/40-s5-p3-preference-hidden-zero.md",
            {edge["target"] for edge in outgoing["edges"]},
        )

        incoming = self.run_tool("backlinks", "39-s5-p2-j-space")
        self.assertIn(
            "essay-workshop/nodes/concepts/j-space.md",
            {edge["source"] for edge in incoming["edges"]},
        )

    def test_neighbourhood_crosses_section_concept_argument_and_source_relations(self):
        result = self.run_tool("neighbourhood", "j-space", "--depth", "2")
        types = {node["artifact_type"] for node in result["nodes"]}
        paths = {node["path"] for node in result["nodes"]}
        self.assertIn("section", types)
        self.assertIn("argument", types)
        self.assertIn("concept", types)
        self.assertIn("source-house", types)
        self.assertIn("essay-workshop/nodes/arguments/02-objective-internality.md", paths)
        self.assertIn("essay-workshop/nodes/sections/40-s5-p3-preference-hidden-zero.md", paths)

    def test_path_follows_the_live_argument_graph(self):
        result = self.run_tool(
            "path", "39-s5-p2-j-space", "40-s5-p3-preference-hidden-zero", "--max-depth", "3"
        )
        self.assertTrue(result["found"])
        self.assertEqual(result["path"][0]["id"], "39-s5-p2-j-space")
        self.assertEqual(result["path"][-1]["id"], "40-s5-p3-preference-hidden-zero")

    def test_trace_recovers_claim_status_dependencies_and_source_records(self):
        result = self.run_tool("trace", "02-objective-internality")
        self.assertEqual(result["root"]["claim_status"], "Argued")
        self.assertIn(
            "essay-workshop/nodes/arguments/01-immutable-gap-and-meta-sign.md",
            {node["path"] for node in result["dependencies"]},
        )
        self.assertIn(
            "essay-workshop/sources-texts-references/source-bank/sources/lecun-et-al-2006-energy-based-learning/SOURCE.md",
            {node["path"] for node in result["sources"]},
        )
        self.assertIn("Claim", result["root"]["headings"])
        self.assertIn("Warrant", result["root"]["headings"])

    def test_effects_maps_a_source_into_its_consuming_argument_and_transverse_thread(self):
        result = self.run_tool("effects", "taylor-2026-revision-notes-trust", "--depth", "4")
        self.assertEqual(result["root"]["id"], "taylor-2026-revision-notes-trust")
        self.assertIn(
            "essay-workshop/nodes/sections/22-s2-p3-ares-aphrodite-harmonia.md",
            {node["path"] for node in result["consumers"]["sections"]},
        )
        self.assertIn(
            "essay-workshop/nodes/arguments/18-trust-faith-formal-limit.md",
            {node["path"] for node in result["consumers"]["arguments"]},
        )
        self.assertIn(
            "trust-faith-formal-limit",
            {thread["id"] for thread in result["transverse_threads"]},
        )
        self.assertGreaterEqual(len(result["transverse_threads"]), 1)
        self.assertTrue(result["downstream"]["paths"])

    def test_context_assembles_a_traceable_section_working_set(self):
        result = self.run_tool("context", "39-s5-p2-j-space", "--depth", "2")
        self.assertEqual(result["entry"]["sequence"], 39)
        self.assertEqual(result["previous"]["id"], "38-s5-p1-apoha-softmax")
        self.assertEqual(result["next"]["id"], "40-s5-p3-preference-hidden-zero")
        self.assertIn("j-space", {node["id"] for node in result["concepts"]})
        self.assertIn("02-objective-internality", {node["id"] for node in result["arguments"]})
        self.assertIn(
            "lecun-et-al-2006-energy-based-learning",
            {node["id"] for node in result["sources"]},
        )
        self.assertTrue(result["trace"])
        self.assertTrue(result["authority"])
        self.assertIn("claim_status", result["status_axes"])
        self.assertIn("quote_status", result["status_axes"])

    def test_context_retains_authority_hubs_without_crawling_through_the_entire_vault(self):
        result = self.run_tool(
            "context", "01-s01-p0-question-before-mechanism", "--depth", "2"
        )
        self.assertTrue(result["governing_documents"])
        self.assertLess(len(result["arguments"]), 10)
        self.assertLess(len(result["concepts"]), 10)
        self.assertIn(
            "01-immutable-gap-and-meta-sign",
            {node["id"] for node in result["arguments"]},
        )

    def test_source_houses_and_reading_routes_are_traceable_in_bounded_context(self):
        status = self.run_tool("status")
        self.assertEqual(
            status["counts"]["source-house"],
            len(
                list(
                    (
                        PROJECT
                        / "essay-workshop/sources-texts-references/source-bank/sources"
                    ).glob("*/SOURCE.md")
                )
            ),
        )
        self.assertEqual(status["counts"]["room-reading-path"], 2)

        source = self.run_tool("open", "kaplan-1999-nothing-that-is")
        self.assertEqual(source["artifact_type"], "source-house")
        self.assertEqual(source["authority"], "source-authority")
        self.assertEqual(source["frontmatter"]["ownership"], "canonical-source-house")
        self.assertEqual(source["frontmatter"]["quote_status"], "excerpts-unverified")

        found = self.run_tool("find", "ordinary field laws collapse every number", "--limit", "10")
        self.assertIn(
            "essay-workshop/sources-texts-references/source-bank/sources/kaplan-1999-nothing-that-is/SOURCE.md",
            {hit["path"] for hit in found["hits"]},
        )

        kaplan_context = self.run_tool("context", "13-s1-p0-sign-migrates", "--depth", "2")
        self.assertIn("kaplan-1999-nothing-that-is", {node["id"] for node in kaplan_context["sources"]})

        operational_context = self.run_tool(
            "context", "14-s1-p1-sunya-operational", "--depth", "2"
        )
        self.assertTrue(
            {
                "kaplan-1999-nothing-that-is",
                "colebrooke-1817-brahmagupta-bhaskara",
                "dutta-2023-zero-divided-numbers-india",
            }.issubset({node["id"] for node in operational_context["sources"]})
        )
        self.assertEqual(
            {
                "colebrooke-1817-brahmagupta-bhaskara-q001",
                "colebrooke-1817-brahmagupta-bhaskara-q002",
                "colebrooke-1817-brahmagupta-bhaskara-q003",
            },
            {
                passage["quote_id"]
                for passage in operational_context["passages"]
                if passage["quote_id"].startswith(
                    "colebrooke-1817-brahmagupta-bhaskara-"
                )
            },
        )
        self.assertTrue(
            all(
                passage["canonical"]["canonical_path"].endswith("/SOURCE.md")
                and passage["canonical"]["locator"]
                and passage["canonical"]["quotation_status"]
                for passage in operational_context["passages"]
            )
        )
        self.assertIn(
            "reading-02-return-of-zero",
            {node["id"] for node in operational_context["reading_paths"]},
        )

        threshold_context = self.run_tool(
            "context", "01-s01-p0-question-before-mechanism", "--depth", "2"
        )
        self.assertIn(
            "reading-00-integral-threshold",
            {node["id"] for node in threshold_context["reading_paths"]},
        )
        self.assertIn(
            "raatikainen-2026-godel-incompleteness-sep-q001",
            {passage["quote_id"] for passage in threshold_context["passages"]},
        )
        path_links = self.run_tool("links", "reading-00-integral-threshold")
        self.assertTrue(
            any(
                edge["raw_target"] == "raatikainen-2026-godel-incompleteness-sep-q001"
                and edge["relation"] == "uses-passage"
                for edge in path_links["edges"]
            )
        )

        record_backlinks = self.run_tool("backlinks", "kaplan-1999-nothing-that-is")
        self.assertIn(
            "essay-workshop/section-rooms/02-return-of-zero/READING.md",
            {edge["source"] for edge in record_backlinks["edges"]},
        )

    def test_doctor_names_real_context_and_graph_debts(self):
        result = self.run_tool("doctor")
        thin_paths = {
            debt["path"] for debt in result["debts"] if debt["kind"] == "thin-argument"
        }
        self.assertFalse(thin_paths)
        # Different heading vocabularies must not be mistaken for missing thought.
        self.assertNotIn("essay-workshop/nodes/arguments/02-objective-internality.md", thin_paths)
        self.assertNotIn("essay-workshop/nodes/arguments/11-mono-poly-trust.md", thin_paths)
        self.assertNotIn("essay-workshop/nodes/arguments/14-computational-process-ontology.md", thin_paths)
        self.assertNotIn("essay-workshop/nodes/arguments/17-toroidal-circulation-arche-topos.md", thin_paths)
        self.assertNotIn("unresolved-link", result["debt_counts"])
        self.assertTrue(all("authority" in debt for debt in result["debts"]))
        self.assertFalse(
            any(
                debt["path"].startswith("submission-package/")
                for debt in result["debts"]
                if debt["kind"] == "unresolved-link"
            )
        )

        assessments = {row["path"]: row for row in result["quality_assessments"]}
        deferential = assessments[
            "essay-workshop/nodes/arguments/08-deferential-intelligence.md"
        ]
        self.assertEqual(deferential["artifact_type"], "argument")
        self.assertTrue(all(deferential["dimensions"].values()))
        self.assertTrue(deferential["dependencies"])
        self.assertTrue(deferential["consumers"])
        self.assertTrue(deferential["sources"])

    def test_canonical_argument_and_concept_repairs_clear_known_quality_debts(self):
        result = self.run_tool("doctor")
        thin_paths = {
            debt["path"] for debt in result["debts"] if debt["kind"] == "thin-argument"
        }
        repaired = {
            f"essay-workshop/nodes/arguments/{name}.md"
            for name in (
                "05-agent-subjectivity-open",
                "06-computational-vimarsa-ahi",
                "07-hephaestus-and-the-net",
                "08-deferential-intelligence",
                "09-prakasa-vimarsa",
                "10-vak",
            )
        }
        self.assertTrue(repaired.isdisjoint(thin_paths), thin_paths & repaired)
        self.assertNotIn(
            "essay-workshop/nodes/concepts/planetary-computation.md",
            {debt["path"] for debt in result["debts"] if debt["kind"] == "missing-status"},
        )

    def test_canonical_graph_has_no_missing_quality_surfaces_or_governing_dangles(self):
        result = self.run_tool("doctor")
        missing = {
            item["path"]: item["missing"]
            for item in result["quality_assessments"]
            if item["missing"]
        }
        self.assertEqual({}, missing)
        governing_dangles = [
            debt
            for debt in result["debts"]
            if debt["kind"] == "unresolved-link"
            and debt["authority"] == "governing"
        ]
        self.assertEqual([], governing_dangles)


if __name__ == "__main__":
    unittest.main()
