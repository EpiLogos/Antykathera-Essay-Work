import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
BUILDER = PROJECT / "tools/build-essay-okf.py"
PACKAGE = PROJECT / "submission-package/epi-logos"
SUBMISSION = PROJECT / "submission-package"
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end() :]


class SubmissionPackageTests(unittest.TestCase):
    def build(self, output: Path):
        subprocess.run(
            ["python3", str(BUILDER), "--project-root", str(PROJECT), "--output", str(output)],
            cwd=PROJECT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_export_builds_a_complete_typed_reader_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "essay-okf"
            self.build(output)

            self.assertTrue((output / "index.md").is_file())
            self.assertTrue((output / "log.md").is_file())
            self.assertEqual(
                len(list((PROJECT / "essay-workshop/nodes/sections").glob("*.md"))),
                len(list((output / "sections").glob("*.md"))),
            )
            self.assertEqual(
                len(list((PROJECT / "essay-workshop/nodes/arguments").glob("*.md"))),
                len(list((output / "arguments").glob("*.md"))),
            )
            self.assertEqual(
                len(
                    [
                        path
                        for path in (PROJECT / "essay-workshop/nodes/concepts").glob("*.md")
                        if path.name != "index.md"
                    ]
                ),
                len(list((output / "concepts").glob("*.md"))),
            )
            canonical_records = PROJECT / "essay-workshop/sources-texts-references/source-bank/sources"
            self.assertEqual(
                len(
                    [
                        path
                        for path in canonical_records.rglob("SOURCE.md")
                        if path.read_text(encoding="utf-8").strip()
                    ]
                ),
                len(list((output / "references/sources").glob("*.md"))),
            )
            self.assertFalse((output / "references/quotes").exists())
            self.assertGreater(len(list((output / "braids").glob("*.md"))), 0)

            record, body = frontmatter(output / "references/sources/le-bon-1895-crowd-popular-mind.md")
            extraction, _ = frontmatter(output / "supporting/source-extraction-core-theorems.md")
            authorial_text = (
                output / "supporting/taylor-2026-core-theorems-pithy-authorial-text.md"
            )
            self.assertEqual("source-house", record["type"])
            self.assertEqual("canonical-source-house", record["ownership"])
            self.assertIn("le-bon-1895-crowd-popular-mind-lb-03", body)
            self.assertEqual("source-extraction", extraction["type"])
            self.assertTrue(authorial_text.is_file())
            theorem_source = (
                output / "references/sources/taylor-2026-core-theorems-pithy.md"
            ).read_text(encoding="utf-8")
            self.assertIn(
                "../../supporting/taylor-2026-core-theorems-pithy-authorial-text.md",
                theorem_source,
            )

            for path in output.rglob("*.md"):
                data, _ = frontmatter(path)
                self.assertIn("type", data, path)
                self.assertNotIn("[[", path.read_text(encoding="utf-8"), path)
                if path.name not in {"index.md", "log.md"}:
                    self.assertIn("canonical_path", data, path)
                    self.assertRegex(data["canonical_sha256"], r"^[0-9a-f]{64}$", path)

            section, _ = frontmatter(output / "sections/01-s01-p0-question-before-mechanism.md")
            self.assertEqual(["§0/1", "#0"], section["coordinates"])

    def test_every_exported_internal_link_resolves_and_index_reaches_every_node(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "essay-okf"
            self.build(output)
            index_text = (output / "index.md").read_text(encoding="utf-8")

            for path in output.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                for raw in MARKDOWN_LINK.findall(text):
                    target = raw.strip().strip("<>").split("#", 1)[0]
                    if not target or target.startswith(("http://", "https://", "mailto:", "resource:")):
                        continue
                    resolved = (path.parent / target).resolve()
                    self.assertTrue(resolved.is_file(), f"{path}: {raw}")

                if path.name not in {"index.md", "log.md"}:
                    relative = path.relative_to(output).as_posix()
                    self.assertIn(f"({relative})", index_text, relative)

            subprocess.run(
                [
                    "python3",
                    str(BUILDER),
                    "--project-root",
                    str(PROJECT),
                    "--output",
                    str(output),
                    "--check",
                ],
                cwd=PROJECT,
                check=True,
                capture_output=True,
                text=True,
            )

    def test_export_preserves_status_and_quote_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "essay-okf"
            self.build(output)
            argument, _ = frontmatter(output / "arguments/02-objective-internality.md")
            source, body = frontmatter(output / "references/sources/le-bon-1895-crowd-popular-mind.md")

            self.assertEqual("Argued", argument["claim_status"])
            self.assertEqual("citation-ready", source["citation_status"])
            self.assertEqual("quotation-ready", source["quote_status"])
            self.assertIn("LB-03", body)
            self.assertIn("book I, ch. 1", body)

    def test_canonical_source_house_keeps_kaplan_learning_material_together(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "essay-okf"
            self.build(output)
            source, body = frontmatter(
                output / "references/sources/kaplan-1999-nothing-that-is.md"
            )

            self.assertFalse((output / "references/studies").exists())
            self.assertEqual(["§1 · narrative and learning spine"], source["main_source_for"])
            self.assertIn("## Scholarly reading and worked material", body)
            self.assertIn("## Historical reading spine", body)
            self.assertIn("## Mathematical workbench", body)

    def test_source_and_passage_routes_converge_on_one_canonical_house(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "essay-okf"
            self.build(output)
            section = (
                output / "sections/14-s1-p1-sunya-operational.md"
            ).read_text(encoding="utf-8")
            self.assertIn(
                "[Colebrooke — Brahmagupta and Bhāskara (1817)]"
                "(../references/sources/colebrooke-1817-brahmagupta-bhaskara.md)",
                section,
            )
            self.assertIn("`colebrooke-1817-brahmagupta-bhaskara-q001`", section)
            self.assertFalse((output / "references/quotes").exists())

    def test_reader_skills_use_only_the_shipped_bundle_contract(self):
        okf = (PACKAGE / "skills/okf-wiki/SKILL.md").read_text(encoding="utf-8")
        walk = (PACKAGE / "skills/walk-the-essay/SKILL.md").read_text(encoding="utf-8")
        bootstrap = (PACKAGE / "skills/using-epi-logos/SKILL.md").read_text(encoding="utf-8")
        pedagogy = (PACKAGE / "skills/converse-pedagogically/SKILL.md").read_text(encoding="utf-8")
        okf_format = (PACKAGE / "skills/okf-wiki/references/okf-format.md").read_text(encoding="utf-8")
        okf_scan = (PACKAGE / "skills/okf-wiki/references/okf-scan.py").read_text(encoding="utf-8")
        readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
        canon_readme = (PACKAGE / "resources/canon/README.md").read_text(encoding="utf-8")

        for text in (okf, walk, pedagogy):
            self.assertIn("resources/essay-okf/index.md", text)
        for text in (okf, walk, okf_format, okf_scan):
            self.assertNotIn("essay-workshop/", text)
            self.assertNotIn("quote-ledger.md", text)
        self.assertIn("quote_status", okf)
        for text in (bootstrap, pedagogy, readme):
            self.assertNotIn("SessionStart hook", text)
        self.assertIn("resources/essay-okf/index.md", readme)
        self.assertNotIn("once regenerated", readme)
        for text in (bootstrap, pedagogy):
            self.assertNotIn("resources/persona/epii.md", text)
            self.assertNotIn("resources/prompt-package/", text)
        for missing_resource in (
            "resources/updated-ql-mef/",
            "resources/topologicals/",
            "resources/ql-prompt-package.md",
            "resources/mef-prompt-package.md",
            "resources/pedagogy/",
        ):
            self.assertNotIn(missing_resource, canon_readme)

    def test_reader_protocol_is_content_agnostic_and_traversal_led(self):
        walk = (PACKAGE / "skills/walk-the-essay/SKILL.md").read_text(encoding="utf-8")
        bootstrap = (PACKAGE / "skills/using-epi-logos/SKILL.md").read_text(encoding="utf-8")
        pedagogy = (PACKAGE / "skills/converse-pedagogically/SKILL.md").read_text(
            encoding="utf-8"
        )
        ledger = (
            PACKAGE / "resources/reader/TRAVERSAL-LEDGER.md"
        ).read_text(encoding="utf-8")
        template_path = PACKAGE / "resources/reader/TRAVERSAL-TEMPLATE.md"
        template_data, template = frontmatter(template_path)

        self.assertEqual("reader-traversal", template_data["type"])
        self.assertIn("vault_release", template_data)
        self.assertIn("entry_asset", template_data)
        self.assertIn("## 0/1 — Binding", template)
        self.assertIn("## Movement", template)
        self.assertIn("## 5→0 — Return", template)

        for movement in (
            "enter",
            "follow",
            "branch",
            "rejoin",
            "revisit",
            "return",
        ):
            self.assertIn(f"`{movement}`", ledger)

        for protocol in (walk, pedagogy):
            self.assertNotIn("The Return of Zero", protocol)
            self.assertNotRegex(protocol, r"\b(?:48-movement|eight stations|seven transverse)\b")
            self.assertIn("TRAVERSAL-LEDGER.md", protocol)
            self.assertIn("unified QL/MEF", protocol)

        self.assertNotIn("primarily **QL**", bootstrap)
        self.assertNotIn("primarily **MEF**", bootstrap)
        self.assertIn("one QL/MEF instrument", bootstrap)

    def test_submission_manifest_keeps_card_integration_status_honest(self):
        manifest = json.loads((SUBMISSION / "MANIFEST.json").read_text(encoding="utf-8"))
        artifacts = {artifact["id"]: artifact for artifact in manifest["artifacts"]}

        self.assertEqual("primary-publication", artifacts["published-vault"]["role"])
        self.assertEqual("reader-companion", artifacts["epi-logos"]["role"])

        card = artifacts["epi-card-system-v1"]
        self.assertEqual("optional-integration-specification", card["kind"])
        self.assertEqual("reader-encounter-capsule", card["role"])
        self.assertEqual("contract-validated-runtime-not-included", card["status"])
        self.assertEqual(
            ["published-vault", "traversal-ledger", "epi-logos"],
            card["integrates_with"],
        )

        marketplace = json.loads(
            (SUBMISSION / ".claude-plugin/marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(["epi-logos"], [plugin["name"] for plugin in marketplace["plugins"]])

    def test_superseded_submission_spec_retains_obsidian_design_provenance(self):
        spec = (
            SUBMISSION / "2026-07-29-published-vault-reader-package-spec.md"
        ).read_text(encoding="utf-8")
        spec_lower = spec.lower()

        self.assertIn("Obsidian Publish", spec)
        self.assertIn("content-agnostic", spec_lower)
        self.assertIn("traversal ledger", spec_lower)
        self.assertIn("linear and non-linear", spec_lower)
        self.assertIn("static diagram", spec_lower)
        self.assertIn("Superseded design provenance", spec)
        self.assertIn("../WRITING-PROTOCOL.md", spec)
        self.assertNotIn("Quartz", spec)
        self.assertNotIn("symbol-engine", spec)
