"""Functional checks against the real publication corpus and workspace CLI."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '.agents/skills/return-of-zero-build/workflow.py'
spec = importlib.util.spec_from_file_location('p2_workflow', SCRIPT)
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class P2WorkflowTests(unittest.TestCase):
    def test_every_live_quilt_is_discovered_and_anchors_recover_actual_text(self):
        files = workflow.live_quilts(ROOT)
        self.assertEqual(files, sorted(p for p in (ROOT / workflow.QUILT_DIRECTORY).iterdir() if p.is_file()))
        self.assertGreaterEqual(len(files), 6)
        found = 0
        for path in files:
            body = path.read_text()
            lines = body.splitlines()
            for candidate in workflow.read_quilt(path, ROOT):
                found += 1
                line = lines[candidate['source_line'] - 1]
                if candidate['kind'] == 'section':
                    self.assertEqual(line.lstrip('#').strip(), candidate['title'])
                else:
                    self.assertIn(candidate['contribution_id'], body[candidate['source_offset']:].split('>', 1)[0])
                self.assertEqual(body.count('\n', 0, candidate['source_offset']) + 1, candidate['source_line'])
        self.assertGreater(found, 100)

    def test_discovery_candidates_cannot_enter_hygiene_as_canonical_targets(self):
        candidates = workflow.read_quilt(workflow.live_quilts(ROOT)[0], ROOT)
        with self.assertRaisesRegex(ValueError, 'census-reconciled'):
            workflow.canonical_targets(ROOT, {'elements': candidates})

    def test_real_canonical_home_runs_links_and_effects_from_another_cwd(self):
        home = 'submission-package/essay/symbolon/episteme/arguments/A01-Subject-God-and-Faithful-Definition.md'
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / 'target.json'
            report = Path(temporary) / 'hygiene.json'
            manifest.write_text(json.dumps({'elements': [{'canonical_home': home, 'register': 'episteme'}]}))
            proc = subprocess.run([sys.executable, str(SCRIPT), 'hygiene', '--project-root', str(ROOT), '--intake', str(manifest), '--output', str(report)], cwd=temporary, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(report.read_text())
            self.assertEqual(result['targets'], [home])
            self.assertEqual(result['gates']['links'][0]['data']['root']['path'], home)
            self.assertEqual(result['gates']['effects'][0]['returncode'], 0)
            self.assertIn('debt_counts', result['gates']['doctor']['data'])

    def test_target_slice_recovers_real_lines_and_rejects_whole_quilt(self):
        path = workflow.live_quilts(ROOT)[0]
        lines = path.read_text().splitlines()
        item = {'path': str(path.relative_to(ROOT)), 'start_line': 3, 'end_line': 8,
                'relation': 'recovery-anchor-verification', 'provenance': 'actual-developmental-quilt'}
        result = workflow.extract_slice(ROOT, item)
        self.assertEqual(result['text'], '\n'.join(lines[2:8]))
        self.assertEqual(len(result['sha256']), 64)
        with self.assertRaisesRegex(ValueError, 'whole-quilt'):
            workflow.extract_slice(ROOT, {**item, 'start_line': 1, 'end_line': len(lines)})
        with self.assertRaisesRegex(ValueError, 'Invalid source range'):
            workflow.extract_slice(ROOT, {**item, 'end_line': len(lines) + 1})

    def test_actual_unresolvable_identity_is_a_command_failure(self):
        result = workflow.command_result(workflow.run_okf(ROOT, 'links', 'p2-deliberately-unresolvable-negative-control', '--json'))
        self.assertNotEqual(result['returncode'], 0)
        self.assertIn('No artifact resolves', result['stderr'])

    def test_hygiene_rejects_duplicate_admissions_at_real_canonical_homes(self):
        first = {'record_id': 'A01', 'register': 'episteme', 'canonical_home':
                 'submission-package/essay/symbolon/episteme/arguments/A01-Subject-God-and-Faithful-Definition.md'}
        second = {'record_id': 'A02', 'register': 'episteme', 'canonical_home':
                  'submission-package/essay/symbolon/episteme/arguments/A02-Copula-Self-Identity-through-Difference.md'}
        self.assertEqual(len(workflow.canonical_targets(ROOT, {'elements': [first, second]})), 2)
        with self.assertRaisesRegex(ValueError, 'one canonical home'):
            workflow.canonical_targets(ROOT, {'elements': [first, {**first, 'record_id': 'A02'}]})
        with self.assertRaisesRegex(ValueError, 'multiple canonical homes'):
            workflow.canonical_targets(ROOT, {'elements': [first, {**second, 'record_id': 'A01'}]})


class P2ManifestBindingTests(unittest.TestCase):
    """Exercise the actual CLI with the real census, recovered depth and pilot inputs."""

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="p2-binding-test-", dir=ROOT / 'working')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.queue_path = self.directory / 'queue.json'
        self.acceptance_path = self.directory / 'acceptance.json'
        self.packet_path = self.directory / 'packet.json'
        census_path = ROOT / 'working/p2-enrichment/census.json'
        self.queue = json.loads((ROOT / 'working/p2-enrichment/dispatch-queue.json').read_text())
        self.queue['elements'] = [next(e for e in self.queue['elements'] if e['record_id'] == 'A01')]
        self.queue['census_sha256'] = workflow.file_hash(census_path)
        self.acceptance = json.loads((ROOT / self.queue['depth_acceptance']).read_text())
        self.acceptance['quilt_hashes'] = workflow.quilt_hashes(ROOT)
        self.queue['depth_acceptance'] = str(self.acceptance_path.relative_to(ROOT))
        self.save_acceptance()

    def save_acceptance(self):
        self.acceptance_path.write_text(json.dumps(self.acceptance))
        self.queue['depth_acceptance_sha256'] = workflow.file_hash(self.acceptance_path)
        self.save_queue()

    def save_queue(self):
        self.queue_path.write_text(json.dumps(self.queue))

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--project-root', str(ROOT), *args],
                              cwd=self.directory, capture_output=True, text=True)

    def packet(self):
        return self.run_cli('packet', '--queue', str(self.queue_path), '--target', 'A01',
                            '--output', str(self.packet_path))

    def test_packet_binds_real_corpus_and_verifies_from_another_cwd(self):
        proc = self.packet()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        packet = json.loads(self.packet_path.read_text())
        self.assertEqual(packet['binding']['queue_sha256'], workflow.file_hash(self.queue_path))
        self.assertEqual(packet['binding']['census_sha256'], self.queue['census_sha256'])
        self.assertEqual(packet['binding']['quilt_hashes'], workflow.quilt_hashes(ROOT))
        for item in packet['slices']:
            lines = (ROOT / item['path']).read_text().splitlines()
            self.assertEqual(item['text'], '\n'.join(lines[item['start_line'] - 1:item['end_line']]))
        verified = self.run_cli('verify-packet', '--packet', str(self.packet_path))
        self.assertEqual(verified.returncode, 0, verified.stderr)

    def test_stale_census_and_acceptance_bindings_block_output(self):
        for field in ('census_sha256', 'depth_acceptance_sha256'):
            with self.subTest(field=field):
                original = self.queue[field]
                self.queue[field] = '0' * 64
                self.save_queue()
                proc = self.packet()
                self.assertNotEqual(proc.returncode, 0)
                self.assertIn('binding is absent or stale', proc.stderr)
                self.assertFalse(self.packet_path.exists())
                self.queue[field] = original

    def test_domain_readme_change_invalidates_packet(self):
        live_queue = json.loads((ROOT / 'working/p2-enrichment/dispatch-queue.json').read_text())
        element = dict(next(e for e in live_queue['elements']
                            if e['record_id'] == 'matheme-music-foundational-ratios'))
        domain = self.directory / 'README.md'
        domain.write_bytes((ROOT / element['register_contract_domain']).read_bytes())
        element['register_contract_domain'] = str(domain.relative_to(ROOT))
        self.queue['elements'] = [element]
        self.save_queue()
        proc = self.run_cli('packet', '--queue', str(self.queue_path),
                            '--target', element['record_id'], '--output', str(self.packet_path))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        packet = json.loads(self.packet_path.read_text())
        bound = {item['path']: item['sha256'] for item in packet['required_inputs']}
        self.assertEqual(bound[element['register_contract_domain']], workflow.file_hash(domain))
        proc = self.run_cli('verify-packet', '--packet', str(self.packet_path))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        domain.write_text(domain.read_text() + '\nAdditional domain constraint.\n')
        proc = self.run_cli('verify-packet', '--packet', str(self.packet_path))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('stale or altered', proc.stderr)

    def test_depth_review_cannot_survive_changed_quilt_or_depth_receipt(self):
        path = next(iter(self.acceptance['quilt_hashes']))
        self.acceptance['quilt_hashes'][path] = '0' * 64
        self.save_acceptance()
        proc = self.packet()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('quilt binding', proc.stderr)
        self.acceptance['quilt_hashes'] = workflow.quilt_hashes(ROOT)
        self.acceptance['argument_depth'][0]['sha256'] = '0' * 64
        self.save_acceptance()
        proc = self.packet()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('current packet hashes', proc.stderr)

    def test_unadmitted_or_duplicate_identity_is_rejected(self):
        original = dict(self.queue['elements'][0])
        for field, value in [('record_id', 'not-admitted'), ('register', 'mytheme'),
                             ('record_type', 'invented-type'),
                             ('canonical_home', 'submission-package/essay/symbolon/README.md')]:
            with self.subTest(field=field):
                self.queue['elements'] = [{**original, field: value}]
                self.save_queue()
                proc = self.packet()
                self.assertNotEqual(proc.returncode, 0)
                self.assertIn('disagrees with census', proc.stderr)
        self.queue['elements'] = [original, original]
        self.save_queue()
        proc = self.packet()
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('Duplicate admitted identity', proc.stderr)

    def test_verifier_rejects_altered_packet_and_queue(self):
        proc = self.packet()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        packet = json.loads(self.packet_path.read_text())
        packet['slices'][0]['text'] += ' alteration'
        self.packet_path.write_text(json.dumps(packet))
        proc = self.run_cli('verify-packet', '--packet', str(self.packet_path))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('stale or altered', proc.stderr)
        self.assertEqual(self.packet().returncode, 0)
        self.queue['elements'][0]['operation_to_develop'] = 'Changed after packet generation'
        self.save_queue()
        proc = self.run_cli('verify-packet', '--packet', str(self.packet_path))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('stale or altered', proc.stderr)


if __name__ == '__main__':
    unittest.main()
