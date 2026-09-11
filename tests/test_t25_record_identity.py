"""Regressions against the actual publication field, not placeholder canon."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/okf-workspace.py"

class DeclaredRecordIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("t25_workspace", TOOL)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        cls.workspace = module.Workspace(ROOT)

    def test_c41_declared_identity_and_old_slug_agree(self):
        record = self.workspace.resolve("C41")
        self.assertEqual(record.path, self.workspace.resolve("C41-Objective-Internality").path)
        self.assertEqual(record.compact()["record_id"], "C41")
        self.assertEqual(record.id, "C41-Objective-Internality")

    def test_slash_root_resolves_as_identity(self):
        root = self.workspace.resolve("A/C")
        self.assertTrue(root.path.endswith("conjugate/AC.md"))
        self.assertEqual(root.artifact_type, "argument-map")

    def test_conjugate_identity_keeps_its_own_face(self):
        argument = self.workspace.resolve("A26")
        conjugate = self.workspace.resolve("A26p")
        self.assertNotEqual(argument.path, conjugate.path)
        self.assertTrue(conjugate.path.endswith("A26-prime-The-Essay-Inside-the-Film.md"))

    def test_real_effects_command_retains_root(self):
        result = subprocess.run([sys.executable, str(TOOL), "effects", "C41", "--depth", "4", "--json"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["root"]["record_id"], "C41")
        paths = {item["path"] for item in payload["downstream"]["paths"]}
        self.assertIn(self.workspace.resolve("A/C").path, paths)

if __name__ == "__main__":
    unittest.main()
