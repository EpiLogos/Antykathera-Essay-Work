import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SKILLS = PROJECT / ".agents/skills"


class DevelopmentSkillContractTests(unittest.TestCase):
    def skill(self, name: str) -> str:
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_codex_discovers_four_focused_project_skills(self):
        names = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(names, {
            "return-of-zero-orient",
            "return-of-zero-source",
            "return-of-zero-write",
            "return-of-zero-review",
        })
        for name in names:
            self.assertTrue((SKILLS / name / "agents/openai.yaml").is_file())

    def test_orientation_preserves_graph_and_native_language_gates(self):
        text = self.skill("return-of-zero-orient")
        for required in (
            "okf-workspace.py",
            "context",
            "effects",
            "transverse thread",
            "never infer a relation from shared vocabulary",
            "whole eight-determination field",
            "never call the relation Jungian",
            "Never introduce a strawman",
            "active ideas",
        ):
            self.assertIn(required.casefold(), text.casefold())

    def test_source_skill_uses_one_house_and_protects_author_notes(self):
        text = self.skill("return-of-zero-source")
        for required in (
            "sources/<source_id>/SOURCE.md",
            "NOTES.md",
            "never create, edit, append, normalise, migrate, relocate, index as canonical evidence, or delete it",
            "stable passage ID",
            "quotation readiness",
            "build-source-projections.py",
            "project-agent-harness.py passage",
        ):
            self.assertIn(required, text)
        for dead_surface in ("records/<source_id>", "quotes/<source_id>", "study-dossiers/"):
            self.assertNotIn(dead_surface, text)

    def test_writing_skill_targets_master_manuscript_without_compulsory_file_work(self):
        text = self.skill("return-of-zero-write")
        for required in (
            "may remain in chat",
            "essay-workshop/THE-RETURN-OF-ZERO.md",
            "ROOM.md",
            "READING.md",
            "SCRATCH.md",
            "VISUALS.md",
            "writing-guidance-tools/README.md",
            "WRITING-RUBRIC.md",
            "fresh-eyes",
            "ship-note",
            "do not soften",
            "manufacture counterpressure",
        ):
            self.assertIn(required, text)

    def test_review_skill_checks_effects_and_generated_freshness(self):
        text = self.skill("return-of-zero-review")
        for required in (
            "Review is explicit",
            "effects",
            "build-source-projections.py",
            "build-section-rooms.py",
            "doctor --json",
            "NOTES.md",
            "generated `ROOM.md`",
        ):
            self.assertIn(required, text)

    def test_no_skill_claims_named_model_routing_or_runtime_tiers(self):
        combined = "\n".join(self.skill(path.parent.name) for path in SKILLS.glob("*/SKILL.md"))
        for forbidden in ("GPT-5.6 Luna", "GPT-5.6 Terra", "GPT-5.6 Sol", "Runtime model"):
            self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()
