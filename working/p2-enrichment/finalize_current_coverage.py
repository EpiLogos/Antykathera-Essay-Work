"""Materialise reviewed T20/T21 acceptance without rebinding historical packets."""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'working/p2-enrichment'


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def save(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    matrix_path = 'working/p2-enrichment/T21-e-field-consumer-coverage.json'
    archived = 'working/p2-enrichment/snapshots/T21-coverage-before-final-acceptance.json'
    if not (ROOT / archived).exists():
        (ROOT / archived).write_bytes((ROOT / matrix_path).read_bytes())
        (BASE / 'snapshots/T21-coverage-before-final-acceptance.md').write_bytes(
            (BASE / 'T21-e-field-consumer-coverage.md').read_bytes())
    old = read(archived)
    proposal_path = 'working/p2-enrichment/audits/T21-current-reconciliation/E4-source-case-refresh/proposed-row-updates.json'
    proposal = read(proposal_path)
    pair_path = 'working/p2-enrichment/audits/T22-K-E-consumer-pairs-2026-09-08/proof.json'
    pair = read(pair_path)
    all_path = 'working/p2-enrichment/audits/T22-K-E-consumer-pairs-2026-09-08/all272-denominator-supplement.json'
    all_pairs = read(all_path)
    assert all_pairs['counts']['dispositioned_instances'] == 1333
    assert all_pairs['counts']['held_unratified_instances'] == 1
    assert all_pairs['counts']['uncovered_unique_required_pairs'] == 0
    assert all_pairs['counts']['new_semantic_operation_gaps'] == 0
    all_rows = {r['row_id']: r for r in all_pairs['rows']}
    updates = {r['row_id']: r for r in proposal['rows']}
    assert len(updates) == len(old['rows']) == 272
    assert proposal['counts']['positive_local_semantic_witnesses'] == 271
    assert pair['counts']['accepted_pair_instances'] == 244
    assert pair['counts']['actual_missing_directions'] == pair['counts']['semantic_operation_gaps'] == 0
    operations = {r['row_id']: r for r in pair['operations']}
    rows = []
    for original in old['rows']:
        update = updates[original['row_id']]
        for key in ('operation', 'evidence_register'):
            assert original[key] == update[key], (original['row_id'], key)
        row = dict(original)
        row['intake_standing'] = {k: row.pop(k) for k in
            ('development_status', 'next_development_scope', 'coverage_standing', 'movement_route_standing') if k in row}
        row.update(update)
        row['all_consumer_disposition'] = {
            'proof': all_path,
            'consumer_count': all_rows[row['row_id']]['consumer_count'],
            'instance_ids': all_rows[row['row_id']]['consumer_instance_ids'],
            'standing': 'Every declared instance has an explicit typed disposition; historical and native operations retain their distinct warrants.'}
        if row['row_id'] in operations:
            row['development_status'] = 'developed; every declared operation-consumer instance accepted'
            row['operation_consumer_acceptance'] = operations[row['row_id']]
            row['operation_consumer_proof'] = pair_path
        home = row.get('canonical_home')
        row['current_canonical_sha256'] = sha(home) if home and (ROOT / home).is_file() else None
        rows.append(row)
    census = read('working/p2-enrichment/census.json')
    records = census['elements']
    assert len(records) == 281
    assert len({r['record_id'] for r in records}) == 281
    assert len({r['canonical_home'] for r in records}) == 281
    assert all((ROOT / r['canonical_home']).is_file() for r in records)
    baseline = read('working/p2-enrichment/receipts/T20-T21-start-baseline.json')
    assert len(baseline) == 150
    assert all(sha(p) == h for p, h in baseline.items())
    episteme = [r for r in records if r['register'] == 'episteme']
    assert len(episteme) == 163
    inventory = [{k: r[k] for k in ('record_id', 'record_type', 'canonical_home')} |
                 {'sha256': sha(r['canonical_home']), 'exists': True} for r in episteme]
    current = {k: old[k] for k in ('field_shapes', 'evidence_registers', 'generation_law', 'scope')}
    current.update({
        'schema_version': 3,
        'standing': 'Current reviewed development and semantic coverage; source/empirical research remains separately scoped.',
        'intake_snapshot': archived,
        'reviewed_row_proposal': {'path': proposal_path, 'sha256': sha(proposal_path)},
        'rows': rows,
        'counts': proposal['counts'],
        'whole_operation_consumer_proof': {'path': pair_path, 'sha256': sha(pair_path), 'counts': pair['counts']},
        'all_consumer_denominator_proof': {'path': all_path, 'sha256': sha(all_path), 'counts': all_pairs['counts']},
        'canonical_development_complete': True,
        'coverage_complete': True,
        'record_inventory': inventory,
        'canonical_record_counts': dict(Counter(r['record_type'] for r in episteme)),
        'reference_note_coverage': 'working/p2-enrichment/reference-note-current-coverage.md',
        'reference_note_dispositions': 'working/p2-enrichment/reference-note-dispositions.json',
        'movement_alignment': 'working/p2-enrichment/receipts/T22-K-combined-movement-traversal-proof-2026-09-08.json',
        'case_consumer_proof': 'working/p2-enrichment/receipts/T22-E4-comparative-case-consumer-return-proof.json',
        'transferred_39': {
            'authority_and_historical_rulings': archived + '#transferred_39',
            'etymology': 'six mature fields, historical branches and reviewed operation-consumer routes',
            'aphorism': 'one ratified complete Investigation and Faith form; withdrawn candidates not promoted',
            'section_alignment': '48 own P1 rows, 339 distinct programme pairs, 347 literal occurrences; M06/A36 forward-only retained',
        },
        'preservation': {'protected_baseline_files': 150, 'unchanged': True,
                         'status_only_continuation': 'working/p2-enrichment/receipts/T22-final-status-preservation.json'},
        'packet_standing': 'Original queue, packet and depth-review hashes remain historical execution evidence. No retrospective freshness rebinding.',
        'stop_boundary': 'T23/T24 and manuscript composition have not begun.',
    })
    save(matrix_path, current)
    def cell(value):
        return str(value or '—').replace('|', '\\|').replace('\n', ' ')
    lines = ['# T21 — Current E-field development and consumer coverage', '',
             'All 272 stable programme rows are dispositioned: 271 developed judgments and one unratified earth field retained without promotion. The 163 admitted Episteme records have one existing canonical home each.', '',
             'The 29 whole operations have 244 accepted operation-consumer instances across 197 distinct pairs. Explicit mediation remains visible; no direct-link or paragraph quota is inferred. Five E4 comparative cases have nine separate reciprocal consumer operations. Forty-eight Movements retain their own P1 routes and 339 distinct programme pairs.', '',
             'The full denominator contains 1,333 consumer instances: 1,332 developed or scoped dispositions and one unratified held instance. All 239 historical-branch instances join their exact whole-field operation. The typed proof preserves carrier, argument, Movement, conjugate and aphorism offices; no required pair or semantic operation is uncovered.', '',
             'Historical acquisition, quotation and empirical tasks retain their own standing. The machine-readable companion links the exact paragraph, source, route, preservation and per-batch T22 proofs. Historical intake and packet bindings remain archived without rebinding.', '',
             '| Stable row | Kind | Operation | Canonical home | Current coverage |',
             '|---|---|---|---|---|']
    for r in rows:
        home = r.get('canonical_home')
        link = f'[{Path(home).name}](../../{home})' if home else 'Explicit non-admission'
        lines.append('| ' + ' | '.join(map(cell, [r['row_id'], r['row_kind'], r['operation'], link, r['coverage_status']])) + ' |')
    (BASE / 'T21-e-field-consumer-coverage.md').write_text('\n'.join(lines) + '\n')
    save('working/p2-enrichment/receipts/T20-T21-current-census-acceptance.json', {
        'standing': 'Current identities and homes; reviewed scope receipts govern development acceptance.',
        'counts': dict(Counter(r['register'] for r in records)),
        'records': [{k: r[k] for k in ('record_id', 'register', 'record_type', 'canonical_home')} |
                    {'sha256': sha(r['canonical_home'])} for r in records],
        'protected_baseline_unchanged': 150,
        'historical_census_status_not_rebound': census['status'],
    })
    print('Materialised 272 stable coverage rows and 281 current canonical identities; 150 protected hashes unchanged.')


if __name__ == '__main__':
    main()
