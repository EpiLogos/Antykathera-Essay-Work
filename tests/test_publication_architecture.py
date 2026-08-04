import json
import re
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
SYMBOLON = PROJECT / "symbolon"


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end() :]


class PublicationArchitectureTests(unittest.TestCase):
    def test_symbolon_has_direct_root_and_exact_internal_registers(self):
        self.assertTrue((SYMBOLON / "README.md").is_file())
        self.assertFalse((SYMBOLON / "relations").exists())
        self.assertFalse((SYMBOLON / "INDEX.md").exists())

        registers = {"matheme", "mytheme", "episteme"}
        actual = {path.name for path in SYMBOLON.iterdir() if path.is_dir() and not path.name.startswith(".")}
        self.assertEqual(registers, actual)

        root_data, root_body = frontmatter(SYMBOLON / "README.md")
        self.assertEqual("symbolon", root_data["register"])
        self.assertEqual("publication-root", root_data["record_type"])
        self.assertIn("There is no `relations/` subdirectory", root_body)

        for register in registers:
            data, body = frontmatter(SYMBOLON / register / "README.md")
            self.assertEqual(register, data["register"])
            self.assertEqual("register-entry", data["record_type"])
            self.assertIn("Return to [[../README|Symbolon]]", body)

    def test_writing_protocol_governs_without_becoming_symbolon_content(self):
        protocol = PROJECT / "WRITING-PROTOCOL.md"
        self.assertTrue(protocol.is_file())
        self.assertFalse((SYMBOLON / "WRITING-PROTOCOL.md").exists())

        data, body = frontmatter(protocol)
        self.assertEqual("governing-writing-protocol", data["page_type"])
        self.assertIn("Phase P — preliminary work on `main`", body)
        self.assertIn("Phase W — isolated model writing branches", body)
        self.assertIn("Phase S — comparison, selection, and integration", body)
        self.assertIn("no `symbolon/relations/` directory", body)
        self.assertIn("Keep closed:", body)
        self.assertIn("authentic-voice-reference.md", body)
        self.assertIn("comparative and negation gate", body)
        self.assertIn("Frank's writings, poems, and first-person material", body)
        self.assertIn("Diagrams, plates, figures, and media", body)

    def test_manifest_points_to_real_repository_surfaces(self):
        manifest_path = PROJECT / "submission-package/MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual("repository-root", manifest["path_base"])
        self.assertEqual("WRITING-PROTOCOL.md", manifest["current_specification"])

        artifacts = {artifact["id"]: artifact for artifact in manifest["artifacts"]}
        self.assertEqual("symbolon/", artifacts["published-vault"]["path"])
        self.assertEqual("WRITING-PROTOCOL.md", artifacts["writing-protocol"]["path"])

        for artifact in artifacts.values():
            self.assertTrue((PROJECT / artifact["path"]).exists(), artifact)

    def test_obsidian_updates_wikilinks_when_records_move(self):
        settings = json.loads((SYMBOLON / ".obsidian/app.json").read_text(encoding="utf-8"))
        self.assertTrue(settings["alwaysUpdateLinks"])
        self.assertFalse(settings["useMarkdownLinks"])

    def test_old_vault_spec_is_explicitly_provenance(self):
        old = (PROJECT / "submission-package/2026-07-29-published-vault-reader-package-spec.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Status:** Superseded design provenance", old)
        self.assertIn("Superseded by:** `../WRITING-PROTOCOL.md`", old)


if __name__ == "__main__":
    unittest.main()
