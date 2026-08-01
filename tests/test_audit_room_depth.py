from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
AUDITOR = PROJECT / "tools/audit-room-depth.py"
BUILDER = PROJECT / "tools/build-section-rooms.py"


class CompactRoomAuditTests(unittest.TestCase):
    def run_audit(self, project: Path, room: str = "02-return-of-zero", ok: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(AUDITOR), "--project-root", str(project), "--room", room, "--require-deepened"],
            text=True,
            capture_output=True,
            check=False,
        )
        if ok and result.returncode:
            self.fail(result.stdout + result.stderr)
        return result

    def test_real_kaplan_room_passes(self) -> None:
        result = self.run_audit(PROJECT)
        self.assertIn("PASS 02-return-of-zero", result.stdout)

    def test_real_threshold_room_passes_substantive_learning_audit(self) -> None:
        result = self.run_audit(PROJECT, room="00-integral-threshold")
        self.assertIn("PASS 00-integral-threshold", result.stdout)

    def test_tampered_room_fails_real_freshness_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "Antykathera-Essay-Work"
            for relative in (
                "essay-workshop/nodes/sections",
                "essay-workshop/nodes/arguments",
                "essay-workshop/section-rooms/02-return-of-zero",
                "essay-workshop/sources-texts-references/source-bank/sources",
            ):
                shutil.copytree(PROJECT / relative, copy / relative)
            for relative in (
                "essay-workshop/the-return-of-zero-central-plan.md",
                "essay-workshop/THE-RETURN-OF-ZERO.md",
                "essay-workshop/section-rooms/README.md",
            ):
                target = copy / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(PROJECT / relative, target)
            tools = copy / "tools"
            tools.mkdir(parents=True, exist_ok=True)
            shutil.copy2(BUILDER, tools / BUILDER.name)

            room = copy / "essay-workshop/section-rooms/02-return-of-zero/ROOM.md"
            room.write_text(room.read_text(encoding="utf-8") + "\n> fabricated room quotation\n", encoding="utf-8")
            result = self.run_audit(copy, ok=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("embeds source quotation", result.stdout)
            self.assertIn("stale", result.stdout.casefold())

    def test_threshold_route_fails_when_a_real_learning_movement_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "Antykathera-Essay-Work"
            for relative in (
                "essay-workshop/nodes/sections",
                "essay-workshop/nodes/arguments",
                "essay-workshop/section-rooms/00-integral-threshold",
                "essay-workshop/sources-texts-references/source-bank/sources",
            ):
                shutil.copytree(PROJECT / relative, copy / relative)
            for relative in (
                "essay-workshop/the-return-of-zero-central-plan.md",
                "essay-workshop/THE-RETURN-OF-ZERO.md",
                "essay-workshop/section-rooms/README.md",
            ):
                target = copy / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(PROJECT / relative, target)
            tools = copy / "tools"
            tools.mkdir(parents=True, exist_ok=True)
            shutil.copy2(BUILDER, tools / BUILDER.name)

            reading = copy / "essay-workshop/section-rooms/00-integral-threshold/READING.md"
            reading.write_text(
                reading.read_text(encoding="utf-8").replace("**Exercise:**", "**Exercise removed:**", 1),
                encoding="utf-8",
            )
            result = self.run_audit(copy, room="00-integral-threshold", ok=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("has 5 **Exercise:** fields; expected six", result.stdout)


if __name__ == "__main__":
    unittest.main()
