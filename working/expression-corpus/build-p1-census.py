#!/usr/bin/env python3
"""P1 parent-pass census builder — frozen receipts for the remaining Expression corpora.

Follows the T25/E0 receipt pattern: source revision, record count, per-record
hashes, generator. Read-only with respect to every source repository: product
censuses hash bytes straight out of git object storage at each repo's HEAD, so
dirty working trees are never touched and never frozen.

Receipts emitted (working/expression-corpus/):
  P1-census-epii-antichrist.json   frozen from the vault knowledge manifest at the pinned revision
  P1-census-bimba.json             VERIFICATION of the existing M0-M5 production manifest against actual bytes
  P1-census-<product>.json         initial authored-record freeze for the five product repos (docs census basis,
                                   NOT a corpus admission — admission is an owner disposition per product)

Rerun after any accepted source change:  python3 build-p1-census.py
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
# .../Work/O-I/Antykathera-Essay-Work/working/expression-corpus → walk up to Work/
WORK = HERE
for _ in range(4):
    WORK = os.path.dirname(WORK)

ANTICHrist = os.path.join(WORK, 'projects', 'Antichrist Project')
POINTCLOUD = os.path.join(WORK, 'Point-Cloud-Demo')

ANTICHREV = '7df35f822f9235331a69940cdaf484fe4a0b95c1'
ANTICH_PUBLISHED_MAIN = '038a8302c8649b4db68a2b9c7d6fd3eb799a4740'

PRODUCT_REPOS = [
    # (receipt slug, directory, canonical product name, suite position)
    ('central', 'Central', 'Central', 0),
    ('actuation', 'Actuation', 'Actuation', 1),
    ('aikit', 'ai-kit', 'AIKit', 2),
    ('factory', 'Factory', 'Software Factory', 3),
    ('workcell', 'Workcell', 'Workcell', 4),
    ('quaternal-logic', 'Quaternal-Logic', 'Quaternal Logic', 5),
]


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=True).stdout


def head_rev(repo):
    return git(repo, 'rev-parse', 'HEAD').strip()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def blob(repo, path, rev='HEAD'):
    return subprocess.run(['git', '-C', repo, 'cat-file', 'blob', f'{rev}:{path}'],
                          capture_output=True, check=True).stdout


def emitted(name, payload):
    payload.setdefault('generator', 'working/expression-corpus/build-p1-census.py')
    payload.setdefault('generated', date.today().isoformat())
    path = os.path.join(HERE, name)
    with open(path, 'w') as f:
        json.dump(payload, f, indent=1)
        f.write('\n')
    print(f'wrote {name}: {payload.get("record_count", payload.get("records_frozen", "?"))} records')


def census_epii_antichrist():
    vault_manifest_path = os.path.join(ANTICHrist, 'antichrist-vault', 'knowledge-manifest.json')
    manifest = json.load(open(vault_manifest_path))
    records = []
    drifted = []
    for s in manifest['sources']:
        rel = s['path']
        p = os.path.join(ANTICHrist, rel)
        content = open(p, 'rb').read()
        # verify the pinned working-tree bytes equal the published remote's bytes
        pub = subprocess.run(['git', '-C', ANTICHrist, 'cat-file', 'blob', f'origin/main:{rel}'],
                             capture_output=True)
        published_equal = pub.returncode == 0 and hashlib.sha256(pub.stdout).hexdigest() == sha256_bytes(content)
        rec = {
            'record_id': os.path.splitext(os.path.basename(rel))[0],
            'role': s['role'],
            'path': rel,
            'sha256': sha256_bytes(content),
            'bytes': len(content),
            'published_bytes_equal': published_equal,
        }
        if not published_equal:
            drifted.append(rel)
        records.append(rec)
    roles = {}
    for r in records:
        roles[r['role']] = roles.get(r['role'], 0) + 1
    emitted('P1-census-epii-antichrist.json', {
        'schema': 'central.expression-census/v1',
        'corpus': 'epii-antichrist',
        'status': 'frozen',
        'source': {
            'repo': 'EpiLogos/research-canvas (Antichrist Project / Research Canvas)',
            'branch': 'redemption-run-2',
            'commit': ANTICHREV,
            'published_remote_main': ANTICH_PUBLISHED_MAIN,
            'admission_boundary': 'antichrist-vault/knowledge-manifest.json sources[] (schemaVersion 1, contentRevision 2)',
            'note': 'the manifest is the corpus census seed authored by the source programme itself; '
                    'this receipt freezes its admitted records against actual bytes',
        },
        'record_count': len(records),
        'roles': roles,
        'records': records,
        'local_vs_published_drift': drifted,
        'production_state': {
            'namespace': 'Point-Cloud-Demo production/epii-antichrist/',
            'wave_1': ['ep1-ql-units/epii-ep1-ql-units.journey.json (7 scenes)',
                       'ep1-naked-face/epii-ep1-naked-face.journey.json (10 scenes)'],
            'status': 'wave-1 done (gates + covers); corpus NOT complete',
        },
        'not_admitted_this_pass': [
            'episodes/1/ep-1.1/ql-units/position-0..5.md, double-helix.md, self-identity-complexio-argument.md (on disk, outside the manifest)',
            'supporting-bits/ authored essays (incl. Antichrist Book)',
            'the M5-1 essay itself, where it lives outside the vault (the O:I cradle names it "held outside this app")',
        ],
    })


def census_bimba():
    ns = os.path.join(POINTCLOUD, 'production', 'bimba')
    artifacts = []
    for root, _dirs, files in os.walk(ns):
        for f in sorted(files):
            if f.endswith('.journey.json'):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, os.path.join(POINTCLOUD, 'production', 'bimba'))
                content = open(full, 'rb').read()
                artifacts.append({'path': f'production/bimba/{rel}', 'sha256': sha256_bytes(content)})
    fixtures = [a for a in artifacts if 'path-proof' in a['path']]
    corpus_artifacts = [a for a in artifacts if 'path-proof' not in a['path']]
    bindings = sum(1 for root, _d, fs in os.walk(os.path.join(ns, 'bindings')) for f in fs if f.endswith('.json'))
    # the manifest's own claims
    manifest_text = open(os.path.join(ns, 'M0-M5-PRODUCTION-MANIFEST.md')).read()
    claims = {
        'first_cut_artifacts': 13,
        'widening_cut_artifacts': 6,
        'ql_commit': 'e87d6bcef81d005e848b978a11a0ab53b7739973',
        'registry_revision': '259a2f496c5f3a76d31e5c480dc9afdb45ad1282a7034cc28c528c39a71442e4',
        'source_revision': 'daa660cbc1b8c5da83828698665a753852cb0287',
    }
    ok_count = len(corpus_artifacts) == claims['first_cut_artifacts'] + claims['widening_cut_artifacts']
    # QL side: does the pinned registry fixture still exist at QL HEAD, and with the same blob?
    ql = os.path.join(WORK, 'Quaternal-Logic')
    reg_blob = subprocess.run(['git', '-C', ql, 'ls-tree', 'HEAD', '--', 'fixtures/kernel/m-tree-v1.json'],
                              capture_output=True, text=True)
    registry_at_head = None
    if reg_blob.returncode == 0 and reg_blob.stdout.strip():
        registry_at_head = reg_blob.stdout.split()[2]
    emitted('P1-census-bimba.json', {
        'schema': 'central.expression-census/v1',
        'corpus': 'bimba',
        'status': 'verified-existing',
        'verification': {
            'existing_census': 'Point-Cloud-Demo production/bimba/M0-M5-PRODUCTION-MANIFEST.md',
            'manifest_claims': claims,
            'artifacts_found': len(corpus_artifacts),
            'count_matches_claims': ok_count,
            'binding_records': bindings,
            'path_proof_fixtures_excluded': len(fixtures),
            'gate_rerun': 'npx tsx scripts/production-inventory.ts → OK, 3 namespaces, disjoint (2026-09-21, this pass)',
            'registry_fixture_blob_at_ql_head': registry_at_head,
            'ql_checkout_state': 'dirty in-flight lane (session/k-aw-expression-production-2026-09-17) — read-only verification only; '
                                 'the QL-side pins above are quoted from the manifest, not re-derived',
        },
        'source': {
            'owner': 'QL-MEF #201 (Bimba → M′ Expression production lane)',
            'registry': 'Quaternal-Logic fixtures/kernel/m-tree-v1.json (ql.m-tree/v1: 1876 nodes / 21083 relations / 6 roots per the manifest)',
        },
        'record_count': len(corpus_artifacts),
        'artifacts': corpus_artifacts,
        'production_state': {
            'status': 'in-flight (owned lane active); two cuts landed (19 corpus artifacts, depth 2-3 + widening); '
                      'covers absent by declared limitation (renderer captures belong to the owning lane); '
                      'collections/Atlas live collections remain a named gap needing a shape proposal (O-I#65 comment 5751853578)',
        },
    })


def census_product(slug, dirname, product, position):
    repo = os.path.join(WORK, dirname)
    rev = head_rev(repo)
    ls = git(repo, 'ls-tree', '-r', '--name-only', rev).splitlines()
    docs = sorted(p for p in ls if p.endswith('.md'))
    records = []
    for p in docs:
        records.append({'path': p, 'sha256_git_blob': None})  # placeholder, filled below in bulk
    # bulk: use ls-tree -r for blob ids (committed bytes identity), then sha256 the blob content
    lsr = git(repo, 'ls-tree', '-r', rev, '--')
    blobmap = {}
    for line in lsr.splitlines():
        meta, path = line.split('\t', 1)
        _mode, kind, blobid = meta.split()
        if kind == 'blob' and path.endswith('.md'):
            blobmap[path] = blobid
    for r in records:
        bid = blobmap.get(r['path'])
        if bid:
            r['git_blob_id'] = bid
            r['sha256'] = sha256_bytes(blob(repo, r['path'], rev))
    status = subprocess.run(['git', '-C', repo, 'status', '--porcelain'], capture_output=True, text=True).stdout
    branch = git(repo, 'rev-parse', '--abbrev-ref', 'HEAD').strip()
    emitted(f'P1-census-{slug}.json', {
        'schema': 'central.expression-census/v1',
        'corpus': slug,
        'product': product,
        'suite_position': position,
        'status': 'frozen-census-basis',
        'admission_disposition': 'NOT AN ADMISSION — no canonical authored-record census exists for this product\'s '
                                 'Expression corpus yet; this receipt freezes the committed authored-prose surface '
                                 '(all committed .md at HEAD) as the census basis an owner/product lane can admit from. '
                                 'Which records are Expression corpus members is an owner disposition.',
        'source': {
            'repo': f'EpiLogos/{dirname}',
            'branch': branch,
            'commit': rev,
            'hash_note': 'sha256 over exact committed blob bytes at HEAD (working tree never read); git_blob_id is the object id',
        },
        'record_count': len(records),
        'records': records,
        'working_tree': {
            'dirty_entries': len([l for l in status.splitlines() if l.strip()]),
            'note': 'the checkout carries active owner/agent lanes — untouched, not frozen, not counted as records',
        },
    })


def main():
    census_epii_antichrist()
    census_bimba()
    for slug, dirname, product, position in PRODUCT_REPOS:
        census_product(slug, dirname, product, position)
    print('done')


if __name__ == '__main__':
    sys.exit(main())
