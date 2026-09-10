import json
import re
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
SYMBOLON = PROJECT / "submission-package/essay/symbolon"
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end() :]


class PublicationArchitectureTests(unittest.TestCase):
    REGISTER_DOMAINS = {
        "matheme": {
            "definition", "process", "quilt", "music", "dia-syn", "mono-poly",
            "ql",
            "spanda",
            "topology",
            "harmonics",
            "formal-neighbours",
            "computation",
            "diagrams",
        },
        "mytheme": {"worlds", "archetypal-ground", "atlas", "myth", "narrative", "poetry", "media", "art", "music", "plates"},
        "episteme": {
            "arguments", "conjugate", "atlas", "aphorisms",
            "sources",
            "histories",
            "etymologies",
            "lenses",
            "maps",
            "dossiers",
            "figures",
            "concepts",
            "dialogues",
        },
    }

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
        self.assertIn("0/1", root_body)
        self.assertIn("eight-determinations.md", root_body)

        for register in registers:
            data, body = frontmatter(SYMBOLON / register / "README.md")
            self.assertEqual(register, data["register"])
            self.assertEqual("register-root", data["record_type"])
            # Dated programme standing can remain below the reader entrance.
            self.assertIn("# ", body)

    def test_each_register_has_the_complete_functional_domain_shape(self):
        for register, expected_domains in self.REGISTER_DOMAINS.items():
            root = SYMBOLON / register
            actual_domains = {path.name for path in root.iterdir() if path.is_dir()}
            self.assertEqual(expected_domains, actual_domains, register)

            for domain in expected_domains:
                entrance = root / domain / ("investigation-and-faith.md" if domain == "aphorisms" else "README.md")
                self.assertTrue(entrance.is_file(), entrance)
                data, body = frontmatter(entrance)
                self.assertTrue(body.strip(), entrance)
                # Field indexes have distinct schemas; do not relabel them as concepts.
                if data.get("register"):
                    self.assertEqual(register, data["register"], entrance)

    def test_symbolon_root_describes_actual_core_records_and_page_anatomy(self):
        _, body = frontmatter(SYMBOLON / "README.md")
        for record in (
            "THE-RETURN-OF-ZERO.md",
            "0-1.md",
            "1-0.md",
            "the-slash.md",
            "self-identity.md",
            "mono-poly.md",
            "complexio-oppositorum.md",
            "eight-determinations.md",
        ):
            self.assertIn(record, body)
        self.assertIn("## Page anatomy", body)
        self.assertIn("## Four reading movements", body)
        for administrative_word in ("preliminary", "ratification", "migration", "transition"):
            self.assertNotIn(administrative_word, body.casefold())

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
        self.assertEqual("submission-package/essay/", artifacts["published-vault"]["path"])
        self.assertEqual(
            "one-home-canonical-body",
            artifacts["published-vault"]["status"],
        )
        self.assertEqual("WRITING-PROTOCOL.md", artifacts["writing-protocol"]["path"])

        for artifact in artifacts.values():
            self.assertTrue((PROJECT / artifact["path"]).exists(), artifact)

    def test_obsidian_updates_wikilinks_when_records_move(self):
        # The vault root is the publication body itself: rooms, essay and field in one vault.
        settings = json.loads((SYMBOLON.parent / ".obsidian/app.json").read_text(encoding="utf-8"))
        self.assertFalse((SYMBOLON / ".obsidian").exists())
        self.assertTrue(settings["alwaysUpdateLinks"])
        self.assertFalse(settings["useMarkdownLinks"])
        self.assertEqual("./", settings["attachmentFolderPath"])
        self.assertEqual("current", settings["newFileLocation"])

    def test_old_vault_spec_is_explicitly_provenance(self):
        old = (PROJECT / "submission-package/2026-07-29-published-vault-reader-package-spec.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Status:** Superseded design provenance", old)
        self.assertIn("Superseded by:** `../WRITING-PROTOCOL.md`", old)

    def test_every_symbolon_wikilink_resolves_inside_the_vault(self):
        import importlib.util
        import sys

        spec = importlib.util.spec_from_file_location(
            "return_of_zero_workspace", PROJECT / "tools/okf-workspace.py"
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        workspace = module.Workspace(PROJECT)
        rs = importlib.util.spec_from_file_location("reader_audit", PROJECT / "tools/audit-reader-navigation.py")
        reader = importlib.util.module_from_spec(rs)
        rs.loader.exec_module(reader)
        for path in SYMBOLON.rglob("*.md"):
            if "reference-notes" in path.parts or path.name == "AUTHORIAL-TEXT.md":
                continue  # quilt-pending working shelf, not vault content
            for target in WIKILINK.findall(reader.visible_text(path.read_text(encoding="utf-8"))):
                try:
                    workspace.resolve(target.replace("\\", ""))
                except KeyError:
                    if target == "Dreamcode" and path.parent.name == "descartes-1641-meditations":
                        continue  # explicitly held, unmaterialised inquiry; no invented house
                    self.fail(f"{path}: [[{target}]]")


if __name__ == "__main__":
    unittest.main()
