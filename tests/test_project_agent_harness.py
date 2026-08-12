import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
HARNESS = PROJECT / "tools/project-agent-harness.py"
HOOK = PROJECT / ".codex/hooks/return_zero_hook.py"
IDEAS = PROJECT / "working/active-ideas.json"

sys.path.insert(0, str(PROJECT / "tools"))
from source_resolver import resolve_source_house


NOTES = resolve_source_house(
    PROJECT, "van-eenwyk-1997-archetypes-strange-attractors"
).parent / "NOTES.md"


def run_json(command, *, cwd=PROJECT, env=None, input_data=None, check=True):
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        input=json.dumps(input_data) if input_data is not None else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and completed.returncode:
        raise AssertionError(
            f"command failed ({completed.returncode}): {' '.join(map(str, command))}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed, json.loads(completed.stdout or "{}")


class ActiveIdeasTests(unittest.TestCase):
    def test_create_recover_amend_and_retire_an_explicit_idea(self):
        with tempfile.TemporaryDirectory() as tmp:
            ideas = Path(tmp) / "ideas.json"
            base = [sys.executable, HARNESS, "ideas", "--file", ideas]

            _, created = run_json(
                base
                + [
                    "add",
                    "zero as a changed relation",
                    "--provenance",
                    "discussion 2026-07-15",
                    "--context",
                    "the division braid",
                    "--relevance",
                    "keeps the mathematical and metaphysical registers distinct",
                    "--next-use",
                    "reopen at movement 17",
                    "--json",
                ]
            )
            idea_id = created["idea"]["id"]
            self.assertEqual(created["idea"]["status"], "active")

            _, recovered = run_json(base + ["list", "--json"])
            self.assertEqual([idea_id], [idea["id"] for idea in recovered["ideas"]])
            self.assertNotIn("reasoning", recovered["ideas"][0])

            _, amended = run_json(
                base
                + [
                    "amend",
                    idea_id,
                    "--relevance",
                    "now bears the return from movement 18",
                    "--next-use",
                    "test against the manuscript transition",
                    "--json",
                ]
            )
            self.assertEqual(
                amended["idea"]["relevance"],
                "now bears the return from movement 18",
            )

            _, retired = run_json(
                base + ["retire", idea_id, "--reason", "absorbed into the manuscript", "--json"]
            )
            self.assertEqual(retired["idea"]["status"], "retired")
            self.assertEqual(retired["idea"]["retirement_reason"], "absorbed into the manuscript")
            _, active = run_json(base + ["list", "--json"])
            self.assertEqual(active["ideas"], [])
            _, all_ideas = run_json(base + ["list", "--all", "--json"])
            self.assertEqual(len(all_ideas["ideas"]), 1)


class CanonicalJourneyTests(unittest.TestCase):
    def test_exact_passage_retrieval_keeps_wording_locator_and_provenance_together(self):
        _, result = run_json(
            [
                sys.executable,
                HARNESS,
                "passage",
                "colebrooke-1817-brahmagupta-bhaskara-q002",
                "--json",
            ]
        )
        self.assertEqual(result["source_id"], "colebrooke-1817-brahmagupta-bhaskara")
        self.assertEqual(result["status"], "quotation-ready")
        self.assertEqual(
            result["text"],
            "a quantity, divided by cipher, becomes a fraction the denominator of which is cipher.",
        )
        self.assertIn("printed p. 137", result["locator"])
        self.assertIn("rendered scan", result["verification"])
        self.assertEqual(result["source_relation"], "extracted")
        self.assertTrue(Path(result["canonical_path"]).samefile(
            resolve_source_house(PROJECT, "colebrooke-1817-brahmagupta-bhaskara")
        ))

    def test_writing_context_preserves_the_canonical_claim_without_generic_counterpressure(self):
        _, result = run_json(
            [
                sys.executable,
                HARNESS,
                "writing-context",
                "14-s1-p1-sunya-operational",
                "--json",
            ]
        )
        self.assertEqual(result["movement_id"], "14-s1-p1-sunya-operational")
        self.assertTrue(result["claim"])
        self.assertIn("warrant", result)
        self.assertEqual(result["qualification_policy"], "only-when-canonically-live")
        self.assertNotIn("manufactured_counterpressure", result)
        self.assertTrue(Path(result["canonical_path"]).is_file())


class HookBehaviourTests(unittest.TestCase):
    def hook_env(self, root, state):
        env = os.environ.copy()
        env["RETURN_ZERO_PROJECT_ROOT"] = str(root)
        env["RETURN_ZERO_HOOK_STATE"] = str(state)
        return env

    def test_session_start_injects_orientation_skills_and_only_active_ideas(self):
        event = {
            "session_id": "fresh-session",
            "cwd": str(PROJECT),
            "hook_event_name": "SessionStart",
            "source": "startup",
        }
        completed, result = run_json(
            [sys.executable, HOOK],
            env=self.hook_env(PROJECT, Path(tempfile.gettempdir()) / "roz-hook-test"),
            input_data=event,
        )
        self.assertEqual(completed.returncode, 0)
        context = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("Return of Zero orientation", context)
        self.assertIn("AGENTS.md", context)
        self.assertIn(".agents/skills", context)
        self.assertNotIn("model routing", context.casefold())

    def test_pre_and_post_tool_hooks_restore_user_authored_notes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            note = root / NOTES.relative_to(PROJECT)
            note.parent.mkdir(parents=True)
            shutil.copy2(NOTES, note)
            original = note.read_bytes()
            state = Path(tmp) / "state"
            env = self.hook_env(root, state)
            event = {
                "session_id": "notes-session",
                "turn_id": "turn-1",
                "cwd": str(root),
                "tool_name": "apply_patch",
                "tool_input": {"patch": f"*** Update File: {note}\n"},
            }

            event["hook_event_name"] = "PreToolUse"
            run_json([sys.executable, HOOK], env=env, input_data=event)
            note.write_text("agent-overwrite\n", encoding="utf-8")
            event["hook_event_name"] = "PostToolUse"
            completed, result = run_json(
                [sys.executable, HOOK], env=env, input_data=event, check=False
            )

            self.assertEqual(completed.returncode, 0)
            self.assertEqual(note.read_bytes(), original)
            self.assertFalse(result["continue"])
            self.assertIn("restored", result["stopReason"].casefold())

    def test_unrelated_agent_write_does_not_revert_a_concurrent_user_note_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            note = root / NOTES.relative_to(PROJECT)
            note.parent.mkdir(parents=True)
            shutil.copy2(NOTES, note)
            source = note.with_name("SOURCE.md")
            source.write_text("canonical source\n", encoding="utf-8")
            env = self.hook_env(root, Path(tmp) / "state")
            event = {
                "session_id": "concurrent-user-session",
                "turn_id": "turn-1",
                "cwd": str(root),
                "tool_name": "apply_patch",
                "tool_input": {"patch": f"*** Update File: {source}\n"},
            }
            event["hook_event_name"] = "PreToolUse"
            run_json([sys.executable, HOOK], env=env, input_data=event)
            note.write_text("Frank concurrent edit\n", encoding="utf-8")
            event["hook_event_name"] = "PostToolUse"
            _, result = run_json([sys.executable, HOOK], env=env, input_data=event)
            self.assertEqual(result, {})
            self.assertEqual(note.read_text(encoding="utf-8"), "Frank concurrent edit\n")

    def test_hook_on_off_evaluation_records_actual_improvements(self):
        _, report = run_json(
            [sys.executable, HARNESS, "evaluate", "--project-root", PROJECT, "--json"]
        )
        names = {journey["name"] for journey in report["journeys"]}
        self.assertEqual(
            names,
            {
                "open-ended-discussion",
                "exact-source-retrieval",
                "canonical-writing",
                "protected-notes",
                "canonical-propagation",
                "active-idea-lifecycle",
                "fresh-session-orientation",
            },
        )
        self.assertGreater(report["hooks_enabled"]["score"], report["hooks_disabled"]["score"])
        improved = {item["name"] for item in report["improvements"]}
        self.assertTrue(
            {"protected-notes", "canonical-propagation", "fresh-session-orientation"}.issubset(improved)
        )
        self.assertEqual(report["hooks_enabled"]["notes_sha256"], hashlib.sha256(NOTES.read_bytes()).hexdigest())
        self.assertEqual(report["hooks_disabled"]["chat_file_changes"], [])


class ProjectSkillDiscoveryTests(unittest.TestCase):
    def test_codex_discovery_surface_contains_only_the_four_focused_project_skills(self):
        skills = PROJECT / ".agents/skills"
        names = {path.parent.name for path in skills.glob("*/SKILL.md")}
        self.assertEqual(
            names,
            {
                "return-of-zero-orient",
                "return-of-zero-source",
                "return-of-zero-write",
                "return-of-zero-review",
            },
        )
        combined = "\n".join(path.read_text(encoding="utf-8") for path in skills.glob("*/SKILL.md"))
        self.assertNotIn("GPT-5.6 Luna", combined)
        self.assertNotIn("GPT-5.6 Terra", combined)
        self.assertNotIn("GPT-5.6 Sol", combined)
        self.assertIn("NOTES.md", combined)
        self.assertIn("master manuscript", combined.casefold())
        self.assertFalse((PROJECT / "agent-skills/luna-source-quote-swarm").exists())
        self.assertFalse((PROJECT / "agent-skills/sol-section-room-deepening").exists())


if __name__ == "__main__":
    unittest.main()
