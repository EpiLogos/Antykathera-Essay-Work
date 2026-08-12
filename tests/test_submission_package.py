import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
ESSAY = PROJECT / "submission-package/essay"
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
    def test_essay_body_is_the_complete_sixfold_one_home(self):
        self.assertTrue((ESSAY / "README.md").is_file())
        self.assertTrue((ESSAY / "THE-RETURN-OF-ZERO.md").is_file())
        self.assertEqual(
            48,
            len(list((ESSAY / "section-rooms").glob("*/movements/*.md"))),
        )
        self.assertEqual(
            21,
            len(list((ESSAY / "section-rooms/arguments").glob("*.md"))),
        )
        self.assertEqual(
            8,
            len(list((ESSAY / "section-rooms").glob("*/ROOM.md"))),
        )
        self.assertEqual(
            22,
            len(
                [
                    path
                    for path in (ESSAY / "symbolon/episteme/concepts").glob("*.md")
                    if path.name not in {"index.md", "README.md"}
                ]
            ),
        )
        self.assertEqual(
            4,
            len(
                [
                    path
                    for path in (ESSAY / "symbolon/episteme/maps").glob("*.md")
                    if path.name != "README.md"
                ]
            ),
        )
        self.assertEqual(
            124,
            len(list((ESSAY / "symbolon/episteme/sources").rglob("SOURCE.md"))),
        )
        self.assertTrue((ESSAY / "symbolon/episteme/histories").is_dir())
        self.assertTrue((ESSAY / "symbolon/episteme/etymologies").is_dir())
        self.assertFalse(
            (PROJECT / "submission-package/epi-logos/resources/essay-okf").exists()
        )
        self.assertFalse((PROJECT / "symbolon").exists())
        self.assertFalse((PROJECT / "essay-workshop").exists())

    def test_essay_body_wikilinks_and_relative_links_resolve(self):
        import importlib.util
        import sys

        spec = importlib.util.spec_from_file_location(
            "return_of_zero_workspace", PROJECT / "tools/okf-workspace.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        workspace = module.Workspace(PROJECT)
        for path in ESSAY.rglob("*.md"):
            if "reference-notes" in path.parts or path.name == "AUTHORIAL-TEXT.md":
                continue
            text = path.read_text(encoding="utf-8")
            for raw in MARKDOWN_LINK.findall(text):
                target = raw.strip().strip("<>").split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:", "resource:")):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.is_file() or resolved.is_dir(), f"{path}: {raw}"
                )
            for raw in re.findall(r"\[\[([^\]|#]+)", text):
                try:
                    workspace.resolve(raw.replace("\\", ""))
                except KeyError:
                    self.fail(f"{path}: [[{raw}]]")

    def test_essay_body_preserves_status_and_quote_provenance(self):
        argument, _ = frontmatter(
            ESSAY / "section-rooms/arguments/02-objective-internality.md"
        )
        source, body = frontmatter(
            ESSAY
            / "symbolon/episteme/sources/psychology/le-bon/le-bon-1895-crowd-popular-mind/SOURCE.md"
        )
        self.assertEqual("Argued", argument["claim_status"])
        self.assertEqual("citation-ready", source["citation_status"])
        self.assertEqual("quotation-ready", source["quote_status"])
        self.assertIn("LB-03", body)
        self.assertIn("book I, ch. 1", body)

    def test_essay_body_keeps_kaplan_learning_material_in_the_sources_domain(self):
        source, body = frontmatter(
            ESSAY
            / "symbolon/episteme/sources/mathematics-logic/kaplan/kaplan-1999-nothing-that-is/SOURCE.md"
        )
        self.assertEqual(["§1 · narrative and learning spine"], source["main_source_for"])
        self.assertIn("## Scholarly reading and worked material", body)
        self.assertIn("## Historical reading spine", body)
        self.assertIn("## Mathematical workbench", body)

    def test_source_and_passage_routes_converge_on_one_canonical_house(self):
        section = (
            ESSAY / "section-rooms/02-return-of-zero/movements/14-s1-p1-sunya-operational.md"
        ).read_text(encoding="utf-8")
        self.assertIn("colebrooke-1817-brahmagupta-bhaskara", section)
        self.assertIn("`colebrooke-1817-brahmagupta-bhaskara-q001`", section)
        house = (
            ESSAY
            / "symbolon/episteme/sources/mathematics-logic/brahmagupta/colebrooke-1817-brahmagupta-bhaskara/SOURCE.md"
        )
        self.assertTrue(house.is_file())
        self.assertIn(
            '<a id="colebrooke-1817-brahmagupta-bhaskara-q001"></a>',
            house.read_text(encoding="utf-8"),
        )

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
            self.assertIn("symbolon/README.md", text)
        for text in (okf, walk, okf_format, okf_scan):
            self.assertNotIn("working/", text)
            self.assertNotIn("quote-ledger.md", text)
        self.assertIn("quote_status", okf)
        for text in (bootstrap, pedagogy, readme):
            self.assertNotIn("SessionStart hook", text)
        self.assertIn("symbolon/README.md", readme)
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
