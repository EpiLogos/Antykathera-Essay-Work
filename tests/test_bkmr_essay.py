import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
TOOL = PROJECT / "tools" / "bkmr-essay"
ADAPTERS = PROJECT / ".bkmr" / "adapters"
MANIFEST = PROJECT / ".bkmr" / "manifest.tsv"

sys.path.insert(0, str(PROJECT / "tools"))
from source_resolver import iter_source_houses, resolve_source_house


def source_relative(source_id: str) -> str:
    return resolve_source_house(PROJECT, source_id).relative_to(PROJECT).as_posix()


class BkmrEssayIntegrationTests(unittest.TestCase):
    maxDiff = None

    def run_tool(self, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [str(TOOL), *args],
            cwd=PROJECT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(
            result.returncode,
            expected,
            f"command failed: {' '.join(args)}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def adapter_text(self, collection: str) -> str:
        return "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ADAPTERS / collection).glob("*.md"))
        )

    def test_argument_adapters_include_the_authored_argument_body(self):
        self.run_tool("sync", "arguments", "--dry-run")
        text = self.adapter_text("arguments")
        self.assertIn("An artificial agent's internality is a **nomological complex**", text)
        self.assertIn("Context becoming diaphanous", text)

    def test_section_adapters_include_claim_warrant_tension_and_transition(self):
        self.run_tool("sync", "sections", "--dry-run")
        text = self.adapter_text("sections")
        self.assertIn("Circumscription without circumstance", text)
        self.assertIn("Preference Models and the Hidden Zero", text)

    def test_concepts_are_a_first_class_full_body_collection(self):
        self.run_tool("sync", "concepts", "--dry-run")
        text = self.adapter_text("concepts")
        self.assertIn("relational field of an agent's active judgments", text)
        self.assertIn("The shifting landscape", text)

    def test_passage_adapters_point_to_canonical_source_house_anchors_without_transcription(self):
        self.run_tool("sync", "passages", "--dry-run")
        text = self.adapter_text("passages")
        self.assertIn(source_relative("le-bon-1895-crowd-popular-mind"), text)
        self.assertIn("passage_id: le-bon-1895-crowd-popular-mind-lb-01", text)
        self.assertIn("canonical_path#le-bon-1895-crowd-popular-mind-lb-01", text)
        self.assertNotIn("a combination followed by the creation of new characteristics", text)
        self.assertNotIn("canonical_path: submission-package/essay/symbolon/episteme/sources/quote-ledger.md", text)

        adapters = {
            path.stem: path.read_text(encoding="utf-8")
            for path in (ADAPTERS / "passages").glob("*.md")
        }
        ledger = (
            PROJECT
            / "submission-package/essay/symbolon/episteme/sources/PASSAGE-LEDGER.md"
        ).read_text(encoding="utf-8")
        expected = len(
            re.findall(r"\]\([^)#]+/SOURCE\.md#[^)]+\)", ledger)
        )
        self.assertEqual(expected, len(adapters))
        for source in iter_source_houses(PROJECT):
            body = source.read_text(encoding="utf-8")
            anchors = list(re.finditer(r'<a id="([^"]+)"></a>', body))
            for index, anchor in enumerate(anchors):
                passage_id = anchor.group(1)
                if passage_id not in adapters:
                    continue
                adapter = adapters[passage_id]
                # Title metadata (the frontmatter) may carry an authorial
                # first-line name for untitled poems; the locator surface
                # itself must never transcribe the passage.
                adapter_body = adapter.split("---", 2)[-1]
                end = anchors[index + 1].start() if index + 1 < len(anchors) else len(body)
                card = body[anchor.end() : end]
                transcribed_lines = [
                    line.removeprefix(">").strip().strip("“”\"")
                    for line in card.splitlines()
                    if line.startswith(">") and len(line.removeprefix(">").strip()) >= 20
                ]
                for transcription in transcribed_lines:
                    self.assertNotIn(transcription, adapter_body, passage_id)

    def test_manifest_hash_matches_each_canonical_full_body_input(self):
        self.run_tool("sync", "arguments", "--dry-run")
        rows = MANIFEST.read_text(encoding="utf-8").splitlines()
        target = next(
            row
            for row in rows
            if row.split("\t", 3)[1] == "arguments" and "02-objective-internality.md" in row
        )
        fields = target.split("\t")
        canonical_path = PROJECT / fields[2]
        self.assertEqual(fields[8], hashlib.sha256(canonical_path.read_bytes()).hexdigest())
        adapter = ADAPTERS / "arguments" / "arguments-02-objective-internality.md"
        self.assertEqual(fields[9], hashlib.sha256(adapter.read_bytes()).hexdigest())

    def test_doctor_reports_adapter_and_database_freshness_separately(self):
        self.run_tool("sync", "arguments", "--dry-run")
        result = self.run_tool("doctor", "arguments", "--json")
        self.assertIn('"adapter_fresh":true', result.stdout.replace(" ", ""))
        self.assertIn('"database_state":', result.stdout.replace(" ", ""))

    def test_real_sync_imports_every_generated_adapter(self):
        self.run_tool("sync", "concepts")
        result = json.loads(self.run_tool("doctor", "concepts", "--json").stdout)
        self.assertEqual(result["database_state"], "fresh")
        self.assertEqual(result["database_count"], result["adapter_count"])

    def test_kaplan_learning_material_is_retrievable_from_its_canonical_source_house(self):
        self.run_tool("sync", "records")
        text = self.adapter_text("records")
        self.assertIn(
            source_relative("kaplan-1999-nothing-that-is"),
            text,
        )
        self.assertIn("main_source_for: §1 · narrative and learning spine", text)

        result = self.run_tool("search", "records", "Kaplan", "--limit", "10")
        self.assertIn(source_relative("kaplan-1999-nothing-that-is"), result.stdout)
        doctor = json.loads(self.run_tool("doctor", "records", "--json").stdout)
        self.assertEqual(doctor["database_state"], "fresh")
        self.assertEqual(doctor["database_count"], doctor["adapter_count"])

    def test_literal_hyphenated_search_terms_do_not_leak_fts_column_syntax(self):
        self.run_tool("sync", "records")
        result = self.run_tool(
            "search", "records", "Zero-Divided", "--limit", "5"
        )
        self.assertIn(source_relative("dutta-2023-zero-divided-numbers-india"), result.stdout)


if __name__ == "__main__":
    unittest.main()
