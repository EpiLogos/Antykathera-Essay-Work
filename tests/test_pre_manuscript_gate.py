"""Regressions against the real accepted field and actual reader destinations."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PROJECT = Path(__file__).resolve().parents[1]

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, PROJECT / 'tools' / file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

class PreManuscriptGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = load('gate_reader_test', 'audit-reader-navigation.py')
        cls.audit = cls.reader.ReaderAudit(PROJECT)
        cls.report = cls.audit.run()
        cls.rooms = load('gate_rooms_test', 'build-section-rooms.py')

    def test_complete_admitted_field_is_present_unique_and_reader_reachable(self):
        rows = self.report['records']
        self.assertEqual(281, len(rows))
        self.assertEqual(len(rows), len({r['record_id'] for r in rows}))
        self.assertEqual(len(rows), len({r['canonical_home'] for r in rows}))
        for r in rows:
            self.assertTrue(r['exists'], r)
            self.assertIsNotNone(r['reader_depth'], r)
        suite = {f'C{i:02}' for i in range(1,65)} | {f'A{i:02}' for i in range(1,37)} | {f'A{i:02}p' for i in range(1,37)} | {'A/C'}
        self.assertTrue(suite <= {r['record_id'] for r in rows})
        for r in rows:
            if r['record_id'] in suite:
                fm, _ = self.rooms.parse_frontmatter((PROJECT/r['canonical_home']).read_text())
                self.assertEqual(r['record_id'], fm['record_id'])

    def test_all_48_movements_have_valid_alignment_and_reader_next_step(self):
        movements = self.rooms.load_movements(PROJECT)
        self.assertEqual(list(range(1,49)), [m['sequence'] for m in movements])
        for m in movements:
            routes = self.rooms.load_canonical_routes(PROJECT, m['path'].parent.parent)
            self.assertTrue(routes[m['sequence']])
            source = str(m['path'].relative_to(PROJECT))
            targets = {self.audit.resolve(source,k)[0] for k in self.reader.links(m['path'].read_text()) if self.audit.resolve(source,k)[1]=='ok'}
            self.assertIn(str(movements[m['sequence']%48]['path'].relative_to(PROJECT)), targets)
            self.assertFalse(any('/section-rooms/arguments/' in p for p in targets))

    def test_source_page_landings_and_raw_provenance_are_real(self):
        source = 'submission-package/essay/symbolon/episteme/sources/media-technology-philosophy/bratton/bratton-2026-agentworld-brief/SOURCE.md'
        fm, body = self.rooms.parse_frontmatter((PROJECT/source).read_text())
        self.assertEqual('working/antykathera-resources/Antikythera Agentworld Brief.md', fm['local_copy'])
        self.assertTrue((PROJECT/fm['local_copy']).is_file())
        for n in range(1,61):
            self.assertEqual((source,'ok'), self.audit.resolve(source, {'kind':'wiki','href':f'#Source PDF page {n}'}))
        self.assertIn('No passage card', body)
        self.assertIn('bratton-2026-agentworld-brief-q042', body)

    def test_reader_entrance_contains_only_working_visible_destinations(self):
        source = 'submission-package/essay/README.md'
        for k in self.reader.links((PROJECT/source).read_text()):
            target, status = self.audit.resolve(source,k)
            self.assertIn(status, {'ok','external'}, k)
        self.assertIn('awaits composition', (PROJECT/source).read_text())

    def test_live_reading_pages_offer_a_visible_return_to_the_movements(self):
        protected = {'NOTES.md', 'AUTHORIAL-TEXT.md', 'HISTORY.md', 'READING.md', 'SCRATCH.md'}
        dead_ends = [p for p in self.report['no_visible_path_to_movement']
                    if '/concepts/reference-notes/' not in p
                    and Path(p).name not in protected | {'SOURCE-TEMPLATE.md'}]
        self.assertEqual([], dead_ends)

    def test_reader_audit_does_not_silently_repair_a_wrong_relative_path(self):
        source='submission-package/essay/symbolon/episteme/conjugate/A01-prime-Faithful-Definition-of-the-Agent.md'
        _, status=self.audit.resolve(source, {'kind':'markdown','href':'submission-package/essay/symbolon/episteme/arguments/A01-Subject-God-and-Faithful-Definition.md'})
        self.assertEqual('missing-path',status)
        target,status=self.audit.resolve(source, {'kind':'markdown','href':'../arguments/A01-Subject-God-and-Faithful-Definition.md'})
        self.assertEqual('ok',status)
        self.assertTrue((PROJECT/target).is_file())

    def test_argument_pair_links_work_in_both_directions(self):
        base=PROJECT/'submission-package/essay/symbolon/episteme'
        for n in range(1,37):
            a=next((base/'arguments').glob(f'A{n:02}-*.md'))
            b=next((base/'conjugate').glob(f'A{n:02}-prime-*.md'))
            for source,other in [(a,b),(b,a)]:
                rel=str(source.relative_to(PROJECT))
                targets={self.audit.resolve(rel,k)[0] for k in self.reader.links(source.read_text()) if self.audit.resolve(rel,k)[1]=='ok'}
                self.assertIn(str(other.relative_to(PROJECT)),targets)

if __name__=='__main__':unittest.main()
