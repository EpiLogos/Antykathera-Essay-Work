import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]


def load():
    path = PROJECT / "tools" / "audit-canonical-argument-recovery.py"
    spec = importlib.util.spec_from_file_location("canonical_argument_recovery_audit_test", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CanonicalArgumentRecoveryAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load()

    def write(self, root: Path, body: str, record_type: str = "root-relation") -> Path:
        path = root / "submission-package" / "essay" / "symbolon" / "test.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            f"record_type: {record_type}\n"
            "---\n\n"
            + body,
            encoding="utf-8",
        )
        return path

    def test_root_requires_complete_sixfold_form(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, "## #0\nGround\n\n## #5→0\nReturn\n")
            findings = self.mod.audit_file(root, path)
            missing = {f.text for f in findings if f.code == "SIXFOLD_BROKEN"}
            self.assertEqual(
                {
                    "missing canonical sixfold section #1",
                    "missing canonical sixfold section #2",
                    "missing canonical sixfold section #3",
                    "missing canonical sixfold section #4",
                },
                missing,
            )

    def test_ai_consciousness_guard_is_hard_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = "\n\n".join(
                [
                    "## #0\nGround",
                    "## #1\nThe technical architecture does not establish phenomenal subjectivity.",
                    "## #2\nMovement",
                    "## #3\nPattern",
                    "## #4\nContext",
                    "## #5→0\nReturn",
                ]
            )
            path = self.write(root, body)
            findings = self.mod.audit_file(root, path)
            self.assertTrue(any(f.code == "AI_CONSCIOUSNESS_GUARD" and f.severity == "error" for f in findings))

    def test_positive_knower_means_known_claim_is_not_a_guard(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = "\n\n".join(
                [
                    "## #0\nGround",
                    "## #1\nSubjective Immediacy is the knower; Objective Internality is the means; World is the known; Life and Mind are the whole.",
                    "## #2\nThe inspectable means can become known without converting the knower-pole into another item of the inventory.",
                    "## #3\nPattern",
                    "## #4\nContext",
                    "## #5→0\nReturn",
                ]
            )
            path = self.write(root, body)
            findings = self.mod.audit_file(root, path)
            self.assertFalse(any(f.code == "AI_CONSCIOUSNESS_GUARD" for f in findings))


if __name__ == "__main__":
    unittest.main()
