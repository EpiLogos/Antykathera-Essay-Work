import json
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
CLAUDE = PROJECT / ".claude"
PACKAGE = PROJECT / "submission-package" / "epi-logos"


class ClaudeCompatibilityTests(unittest.TestCase):
    def test_project_skills_are_exposed_to_claude_without_duplicate_bodies(self):
        names = {
            "return-of-zero-orient",
            "return-of-zero-source",
            "return-of-zero-write",
            "return-of-zero-review",
        }
        for name in names:
            projected = CLAUDE / "skills" / name
            source = PROJECT / ".agents" / "skills" / name
            self.assertTrue(projected.is_symlink(), projected)
            self.assertEqual(projected.resolve(), source.resolve())
            self.assertTrue((projected / "SKILL.md").is_file())

    def test_claude_settings_register_shared_hook_with_claude_tool_names(self):
        settings = json.loads((CLAUDE / "settings.json").read_text(encoding="utf-8"))
        hooks = settings["hooks"]
        self.assertEqual(
            set(hooks),
            {"SessionStart", "PreToolUse", "PostToolUse", "Stop"},
        )
        for event in ("SessionStart", "PreToolUse", "PostToolUse", "Stop"):
            command = hooks[event][0]["hooks"][0]["command"]
            self.assertIn(
                chr(36) + "{CLAUDE_PROJECT_DIR}/.codex/hooks/return_zero_hook.py",
                command,
            )
        self.assertEqual(hooks["PreToolUse"][0]["matcher"], "Bash|Edit|Write")
        self.assertEqual(hooks["PostToolUse"][0]["matcher"], "Bash|Edit|Write")
        self.assertNotIn("apply_patch", json.dumps(hooks))

    def test_marketplace_is_rooted_at_submission_package(self):
        marketplace_path = PROJECT / "submission-package" / ".claude-plugin" / "marketplace.json"
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "epi-logos-submission")
        self.assertEqual(marketplace["plugins"][0]["source"], "./epi-logos")
        self.assertFalse((PACKAGE / ".claude-plugin" / "marketplace.json").exists())

    def test_plugin_contains_claude_discoverable_skills(self):
        manifest = json.loads(
            (PACKAGE / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["name"], "epi-logos")
        skills = sorted((PACKAGE / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 13)
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"), skill)
            self.assertIn("description:", text.split("---\n", 2)[1])

    def test_mef_refract_is_claude_native(self):
        command = (PACKAGE / "commands" / "mef-refract.md").read_text(encoding="utf-8")
        self.assertIn("Agent", command)
        self.assertIn("one fresh-context subagent per lens", command)
        self.assertIn("synthesis", command)
        self.assertNotIn("Workflow tool", command)
        self.assertNotIn("scriptPath", command)
        self.assertNotIn("workflows/mef-refract.js", command)
        self.assertFalse((PACKAGE / "workflows" / "mef-refract.js").exists())

    def test_readme_documents_both_local_install_paths(self):
        readme = (PACKAGE / "README.md").read_text(encoding="utf-8")
        self.assertIn("/path/to/submission-package", readme)
        self.assertIn("--plugin-dir", readme)
        self.assertIn("epi-logos:mef-refract", readme)


if __name__ == "__main__":
    unittest.main()
