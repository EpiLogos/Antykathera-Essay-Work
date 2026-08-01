import hashlib
import re
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


PROJECT = Path(__file__).resolve().parents[1]
KAPLAN = PROJECT / "essay-workshop/sources-texts-references/source-bank/sources/kaplan-1999-nothing-that-is/SOURCE.md"
COLEBROOKE = PROJECT / "essay-workshop/sources-texts-references/source-bank/sources/colebrooke-1817-brahmagupta-bhaskara/SOURCE.md"
THRESHOLD_READING = PROJECT / "essay-workshop/section-rooms/00-integral-threshold/READING.md"
ZERO_READING = PROJECT / "essay-workshop/section-rooms/02-return-of-zero/READING.md"
ZERO_ROOM = PROJECT / "essay-workshop/section-rooms/02-return-of-zero/ROOM.md"
MANUSCRIPT = PROJECT / "essay-workshop/THE-RETURN-OF-ZERO.md"
RAW_KAPLAN_NOTE = PROJECT / "essay-workshop/sources-texts-references/The Nothing That Is - Robert Kaplan.md"


def parse_markdown(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end() :]


def heading_slug(heading: str) -> str:
    heading = re.sub(r"[`*_~]", "", heading).casefold()
    heading = re.sub(r"[^\w\s-]", "", heading)
    return re.sub(r"[-\s]+", "-", heading).strip("-")


def fragment_resolves(path: Path, fragment: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if re.search(rf'<a\s+id=["\']{re.escape(fragment)}["\']\s*></a>', text):
        return True
    return any(
        heading_slug(match.group(1)) == fragment
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    )


class LearningSurfaceContractTests(unittest.TestCase):
    def test_kaplan_source_house_is_the_complete_learning_object(self) -> None:
        frontmatter, body = parse_markdown(KAPLAN)
        self.assertEqual(frontmatter["node_type"], "source-house")
        self.assertEqual(frontmatter["source_id"], "kaplan-1999-nothing-that-is")
        self.assertEqual(frontmatter["citation_status"], "citation-ready")
        self.assertEqual(frontmatter["quote_status"], "excerpts-unverified")
        self.assertEqual(frontmatter["consumed_by_sections"], ["§1"])
        for heading in (
            "## Bibliographic identity",
            "## Passages and excerpts",
            "## Scholarly reading and worked material",
            "## Why this book is load-bearing",
            "## Historical reading spine",
            "## Read the book through five questions",
            "## Mathematical workbench",
            "## Passage and provenance ledger",
            "## Return to the essay",
        ):
            self.assertIn(heading, body)
        for detail in (
            "printed pp. 4–13",
            "printed pp. 14–27",
            "printed pp. 36–75",
            "printed pp. 90–115",
            "printed pp. 203–215",
            "ordinary field laws collapse every number",
            "### Kaplan's NOR route",
            "### Modern NAND workbench",
            "No Kaplan passage is quotation-ready",
        ):
            self.assertIn(detail, body)

    def test_primary_passages_are_housed_with_real_stable_anchors(self) -> None:
        frontmatter, body = parse_markdown(COLEBROOKE)
        self.assertEqual(frontmatter["source_id"], "colebrooke-1817-brahmagupta-bhaskara")
        self.assertEqual(frontmatter["citation_status"], "citation-ready")
        self.assertEqual(frontmatter["quote_status"], "quotation-ready")
        for quote_id in (
            "colebrooke-1817-brahmagupta-bhaskara-q001",
            "colebrooke-1817-brahmagupta-bhaskara-q002",
            "colebrooke-1817-brahmagupta-bhaskara-q003",
        ):
            self.assertIn(quote_id, body)
            self.assertTrue(fragment_resolves(COLEBROOKE, quote_id))
        self.assertIn("public-domain", body)
        self.assertIn("PDF pp. 435–436", body)

    def test_two_admitted_reading_routes_are_human_routes_with_resolvable_sources(self) -> None:
        routes = sorted((PROJECT / "essay-workshop/section-rooms").glob("*/READING.md"))
        self.assertEqual(routes, [THRESHOLD_READING, ZERO_READING])
        for path in routes:
            frontmatter, body = parse_markdown(path)
            self.assertEqual(frontmatter["page_type"], "room-reading-route")
            self.assertEqual(frontmatter["ownership"], "protected-learning-surface")
            self.assertNotRegex(body, r"(?m)^>")
            for destination in re.findall(r"\[[^]]+\]\(([^)]+)\)", body):
                path_part, separator, fragment = destination.partition("#")
                target = (path.parent / path_part).resolve()
                self.assertTrue(target.is_file(), destination)
                if separator:
                    self.assertTrue(fragment_resolves(target, fragment), destination)
        zero = ZERO_READING.read_text(encoding="utf-8")
        self.assertIn("Kaplan supplies the narrative spine", zero)
        self.assertIn("Work the ordinary-field cancellation argument", zero)
        self.assertIn("mediant construction", zero)
        self.assertIn("NOR/NAND distinction", zero)

    def test_threshold_route_teaches_all_six_movements_and_supports_pair_writing(self) -> None:
        frontmatter, body = parse_markdown(THRESHOLD_READING)
        expected_movements = [
            "01-s01-p0-question-before-mechanism",
            "02-s01-p1-define-subject",
            "03-s01-p2-definition-cut-gift-danger",
            "04-s01-p3-formal-limit-genealogy",
            "05-s01-p4-gebser-diaphaneity",
            "06-s01-p5-return-zero",
        ]
        expected_quote_ids = [
            f"{source}-q{number:03d}"
            for source in (
                "bratton-2026-agentworld-brief",
                "pind-2009-dignaga-anyapoha-dissertation",
                "spinoza-1674-letter-50-jelles",
                "godel-1931-undecidable-propositions",
                "raatikainen-2026-godel-incompleteness-sep",
                "wittgenstein-1922-tractatus",
                "russell-1908-theory-types",
                "cusa-on-learned-ignorance",
                "maroski-2025-seeing-through-solid-words",
            )
            for number in (1, 2)
        ]
        self.assertEqual(frontmatter["movement_ids"], expected_movements)
        self.assertCountEqual(frontmatter["quote_ids"], expected_quote_ids)
        for heading in (
            "## Fifteen-minute entry",
            "## Full reading sequence",
            "### #0 — A system acts from a horizon it does not display",
            "### #1 — The subject appears through mediation",
            "### #2 — A definition gives by cutting",
            "### #3 — Formal closure meets differently constituted limits",
            "### #4 — Learned ignorance and diaphaneity change the response",
            "### #5→0 — Zero enters as a promise",
            "## Pair-writing handholds",
            "## What remains unresolved",
        ):
            self.assertIn(heading, body)
        self.assertEqual(body.count("**Exercise:**"), 6)
        self.assertEqual(body.count("**Carry:**"), 6)
        for quote_id in expected_quote_ids:
            source_id = quote_id.rsplit("-q", 1)[0]
            source_house = PROJECT / f"essay-workshop/sources-texts-references/source-bank/sources/{source_id}/SOURCE.md"
            self.assertIn(f"#{quote_id}", body)
            self.assertTrue(fragment_resolves(source_house, quote_id), quote_id)
        for learning_detail in (
            "two-column instrument panel",
            "I see x",
            "draw one finite figure",
            "four-row table",
            "add a transparency layer",
            "write two sentences",
            "manuscript anchor",
            "movement node",
            "exact passage anchors",
            "paragraph’s outgoing carry",
            "local claim",
            "source’s operation",
            "exact anchor and locator",
            "PSV V:11d card, p. 85",
            "vicious-circle card, §IV, p. 237",
            "proposition 4.1212 card, PDF p. 40",
            "Book I, ch. 1 card, margin 4, printed p. 6",
        ):
            self.assertIn(learning_detail, body)
        self.assertGreaterEqual(len(body.split()), 1600)
        self.assertNotRegex(body, r"(?m)^>")
        for legacy_name in ("04-READING-PATH", "05-ROOM-DOSSIER", "10-FRANK-DRAFT"):
            self.assertNotIn(legacy_name, body)

    def test_human_and_agent_journey_reaches_granular_kaplan_material(self) -> None:
        manuscript = MANUSCRIPT.read_text(encoding="utf-8")
        room = ZERO_ROOM.read_text(encoding="utf-8")
        reading = ZERO_READING.read_text(encoding="utf-8")
        source = KAPLAN.read_text(encoding="utf-8")
        self.assertIn("section-rooms/02-return-of-zero/ROOM.md", manuscript)
        self.assertIn("[reading route](READING.md)", room)
        self.assertIn("kaplan-1999-nothing-that-is/SOURCE.md", room)
        self.assertIn("#historical-reading-spine", reading)
        self.assertIn("#mathematical-workbench", reading)
        self.assertIn("### Division by zero: run the ordinary-field collapse", source)
        self.assertIn("### `0/1` and `1/0`: build the rational interval", source)
        self.assertIn("## Passage and provenance ledger", source)

    def test_current_raw_marginalia_are_substantive_linked_and_build_immutable(self) -> None:
        raw = RAW_KAPLAN_NOTE.read_text(encoding="utf-8")
        for detail in ("page 73", "page 173/4", "chapter 15", "we are bees of teh invisible"):
            self.assertIn(detail, raw)
        self.assertIn("[[The Nothing That Is - Robert Kaplan]]", KAPLAN.read_text(encoding="utf-8"))
        before = hashlib.sha256(RAW_KAPLAN_NOTE.read_bytes()).hexdigest()
        result = subprocess.run(
            [sys.executable, str(PROJECT / "tools/build-section-rooms.py"), "--project-root", str(PROJECT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(hashlib.sha256(RAW_KAPLAN_NOTE.read_bytes()).hexdigest(), before)

if __name__ == "__main__":
    unittest.main()
