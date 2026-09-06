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


if __name__ == '__main__':
    unittest.main()
