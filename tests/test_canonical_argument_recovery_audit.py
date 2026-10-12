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


    def complete(self, content="A distinction can return."):
        return "\n\n".join(f"## {h} — Local turn\n{content}" for h in self.mod.SIXFOLD)

    def test_real_c35_legacy_guard_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sentence = "Returning each account to its office makes self-reference more exact and preserves the open artificial-subjectivity question required by A26/A34."
            path = self.write(root, self.complete(sentence), "concept")
            self.assertTrue(any(f.code == "AI_CONSCIOUSNESS_GUARD" for f in self.mod.audit_file(root, path)))

    def test_guard_wrapped_over_lines_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, self.complete("The architecture does not\nestablish phenomenal subjectivity."))
            self.assertTrue(any(f.code == "AI_CONSCIOUSNESS_GUARD" for f in self.mod.audit_file(root, path)))

    def test_all_canonical_record_types_require_sixfold(self):
        for record_type in ("argument", "canonical-argument", "concept", "product"):
            with self.subTest(record_type=record_type), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                path = self.write(root, "## #0\nGround\n", record_type)
                self.assertEqual(5, sum(f.code == "SIXFOLD_BROKEN" for f in self.mod.audit_file(root, path)))

    def test_canonical_id_covers_records_without_record_type(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, "## #0\nGround\n", "unused")
            path.write_text(path.read_text().replace("record_type: unused", "record_id: C35"))
            self.assertTrue(any(f.code == "SIXFOLD_BROKEN" for f in self.mod.audit_file(root, path)))

    def test_duplicate_and_reordered_positions_fail(self):
        for body in (self.complete() + "\n## #3\nRepeated\n", self.complete().replace("## #1", "## #TMP").replace("## #2", "## #1").replace("## #TMP", "## #2")):
            with tempfile.TemporaryDirectory() as td:
                root = Path(td)
                path = self.write(root, body)
                self.assertTrue(any(f.code == "SIXFOLD_ORDER" for f in self.mod.audit_file(root, path)))

    def test_empty_declared_field_is_not_a_completed_section(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, self.complete() + "\n\n### Declared field\n")
            self.assertTrue(any(f.code == "EMPTY_SECTION" and f.text == "Declared field" for f in self.mod.audit_file(root, path)))

    def test_link_targets_are_not_reader_facing_addresses(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, self.complete("The [Copula](../concepts/C06-Copula.md) relates an instance through difference."))
            self.assertFalse(any(f.code == "ADDRESS_LEAK" for f in self.mod.audit_file(root, path)))
            path.write_text(path.read_text().replace("[Copula]", "[C06]"))
            self.assertTrue(any(f.code == "ADDRESS_LEAK" for f in self.mod.audit_file(root, path)))

    def test_reported_line_includes_frontmatter(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, self.complete() + "\n\nA26 is a navigation address.\n")
            expected = path.read_text().splitlines().index("A26 is a navigation address.") + 1
            self.assertTrue(any(f.code == "ADDRESS_LEAK" and f.line == expected for f in self.mod.audit_file(root, path)))

    def test_source_blockquote_is_reviewed_not_automatically_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, self.complete() + "\n\n> This does not establish phenomenal subjectivity.\n")
            guards = [f for f in self.mod.audit_file(root, path) if f.code == "AI_CONSCIOUSNESS_GUARD"]
            self.assertTrue(guards)
            self.assertTrue(all(f.severity == "review" for f in guards))

    def test_fenced_examples_are_not_public_prose(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, self.complete() + "\n\n```text\nA26 does not establish phenomenal subjectivity.\n```\n")
            self.assertFalse(any(f.code in {"ADDRESS_LEAK", "AI_CONSCIOUSNESS_GUARD"} for f in self.mod.audit_file(root, path)))

    def test_protected_source_cannot_be_selected_for_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self.write(root, "Protected authorial text")
            protected = path.with_name("NOTES.md")
            path.rename(protected)
            with self.assertRaises(ValueError):
                self.mod.resolve_paths(root, [str(protected)])

    def test_missing_corpus_is_not_a_zero_error_census(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                self.mod.discover(Path(td))

    def test_empty_directory_selection_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(ValueError):
                self.mod.resolve_paths(root, ["."])

    def test_public_etymology_history_stays_in_scope(self):
        path = Path("submission-package/essay/symbolon/episteme/etymologies/example/HISTORY.md")
        self.assertTrue(self.mod.is_public_argument_surface(path))


if __name__ == "__main__":
    unittest.main()
