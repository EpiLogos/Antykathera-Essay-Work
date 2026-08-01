import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT = Path(__file__).resolve().parents[1]
BUILDER = PROJECT / "tools/build-section-rooms.py"
ROOMS = (
    "00-integral-threshold",
    "01-differentiating-mind",
    "02-return-of-zero",
    "03-two-logics",
    "04-mathematical-substrate",
    "05-psychoid-flowering",
    "06-objective-internality",
    "07-instrument-returns",
)
LEGACY_NAMES = {
    ".section-room.json",
    "00-SECTION-CONTEXT.md",
    "04-READING-PATH.md",
    "05-ROOM-DOSSIER.md",
    "10-FRANK-DRAFT.md",
    "20-SCHOLARLY-EDITION.md",
    "30-PLATE-AND-DIAGRAMS.md",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if ok and result.returncode:
        raise AssertionError(f"command failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


class SectionRoomV2Tests(unittest.TestCase):
    def test_real_workspace_is_fresh(self) -> None:
        run([sys.executable, str(BUILDER), "--project-root", str(PROJECT), "--check"])

    def test_active_rooms_are_compact_and_complete(self) -> None:
        root = PROJECT / "essay-workshop/section-rooms"
        for slug in ROOMS:
            room = root / slug
            files = {path.name for path in room.iterdir() if path.is_file()}
            self.assertIn("ROOM.md", files)
            self.assertFalse(files & LEGACY_NAMES)
            self.assertTrue(files <= {"ROOM.md", "READING.md", "SCRATCH.md", "VISUALS.md"})

            text = (room / "ROOM.md").read_text(encoding="utf-8")
            words = len(re.findall(r"\b[^\s]+\b", re.sub(r"---.*?---", "", text, count=1, flags=re.DOTALL)))
            self.assertGreaterEqual(words, 500)
            self.assertLessEqual(words, 900)
            self.assertEqual(text.count("**Incoming pressure:**"), 6)
            self.assertEqual(text.count("**Earned position ("), 6)
            self.assertEqual(text.count("**Carry-forward:**"), 6)
            self.assertNotRegex(text, r"(?m)^>")


    def test_master_manuscript_is_the_only_active_writing_surface(self) -> None:
        manuscript = PROJECT / "essay-workshop/THE-RETURN-OF-ZERO.md"
        text = manuscript.read_text(encoding="utf-8")
        self.assertEqual(text.count('ownership: frank-sovereign'), 1)
        self.assertEqual(text.count('<a id="section-'), 8)
        self.assertEqual(len(re.findall(r"^## §", text, re.MULTILINE)), 8)
        for slug in ROOMS:
            self.assertIn(f"section-rooms/{slug}/ROOM.md", text)

    def test_builder_never_changes_manuscript_or_reading_routes(self) -> None:
        protected = [PROJECT / "essay-workshop/THE-RETURN-OF-ZERO.md"]
        protected.extend((PROJECT / "essay-workshop/section-rooms").glob("*/READING.md"))
        before = {path: digest(path) for path in protected}
        run([sys.executable, str(BUILDER), "--project-root", str(PROJECT)])
        self.assertEqual(before, {path: digest(path) for path in protected})

    def test_real_room_links_and_fragments_resolve(self) -> None:
        run([sys.executable, str(BUILDER), "--project-root", str(PROJECT), "--check"])
        for reading in (PROJECT / "essay-workshop/section-rooms").glob("*/READING.md"):
            text = reading.read_text(encoding="utf-8")
            for destination in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                path_part, _, _fragment = destination.partition("#")
                self.assertTrue((reading.parent / path_part).resolve().is_file(), destination)

    def test_canonical_change_makes_a_real_room_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            copy = Path(temporary) / "Antykathera-Essay-Work"
            for relative in (
                "essay-workshop/nodes/sections",
                "essay-workshop/nodes/arguments",
                "essay-workshop/sources-texts-references/source-bank/sources",
            ):
                shutil.copytree(PROJECT / relative, copy / relative)
            for relative in (
                "essay-workshop/the-return-of-zero-central-plan.md",
                "essay-workshop/THE-RETURN-OF-ZERO.md",
            ):
                target = copy / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(PROJECT / relative, target)
            for slug in ("00-integral-threshold", "02-return-of-zero"):
                source = PROJECT / "essay-workshop/section-rooms" / slug / "READING.md"
                if source.is_file():
                    target = copy / "essay-workshop/section-rooms" / slug / "READING.md"
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)

            run([sys.executable, str(BUILDER), "--project-root", str(copy)])
            node = copy / "essay-workshop/nodes/sections/13-s1-p0-sign-migrates.md"
            node.write_text(
                node.read_text(encoding="utf-8").replace(
                    "Zero converges several historically distinct inventions",
                    "Zero gathers several historically distinct inventions",
                    1,
                ),
                encoding="utf-8",
            )
            stale = run([sys.executable, str(BUILDER), "--project-root", str(copy), "--check"], ok=False)
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("stale", (stale.stdout + stale.stderr).casefold())
            run([sys.executable, str(BUILDER), "--project-root", str(copy)])
            run([sys.executable, str(BUILDER), "--project-root", str(copy), "--check"])

if __name__ == "__main__":
    unittest.main()
