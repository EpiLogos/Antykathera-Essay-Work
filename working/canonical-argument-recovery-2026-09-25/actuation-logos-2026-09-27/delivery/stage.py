"""Transport hash-verified recovery edits to unattached Git objects; never publish a ref."""
from pathlib import Path, PurePosixPath
import base64, hashlib, importlib.util, json, lzma, os, re, subprocess, urllib.request

ROOT = Path.cwd()
BATCH = 'working/canonical-argument-recovery-2026-09-25/actuation-logos-2026-09-27/'
CANON = {
    'the-return-of-zero-central-plan.md',
    'submission-package/essay/symbolon/episteme/products/S1-Actuation.md',
    'submission-package/essay/symbolon/episteme/concepts/C40-Model-Internality-Judgment-Field.md',
    'submission-package/essay/section-rooms/06-objective-internality/movements/38-s5-p1-apoha-softmax.md',
}
OUT = Path(os.environ['RUNNER_TEMP']) / 'actuation-stage'
OUT.mkdir(parents=True, exist_ok=True)

def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def generated(path):
    ep = 'submission-package/essay/symbolon/episteme/'
    return (path.startswith(ep + 'maps/navigation/')
            or path in {ep + 'sources/' + n for n in ['SOURCE-INDEX.md', 'PASSAGE-LEDGER.md', 'MAIN-SOURCES.md']}
            or path == 'submission-package/essay/section-rooms/README.md'
            or bool(re.fullmatch(r'submission-package/essay/section-rooms/[^/]+/ROOM\.md', path)))

assert os.environ['GITHUB_REPOSITORY'] == 'EpiLogos/Antykathera-Essay-Work'
assert os.environ['GITHUB_REF'] == 'refs/heads/main'
encoded = ''.join((ROOT / BATCH / 'delivery' / f'part-{i:02}.b64').read_text() for i in range(6))
packed = base64.b64decode(encoded, validate=True)
assert digest(packed) == 'c3f271dd1fd529c45ec944cc6924c13af1585bc3a2fbbbca61a5da92ba6cf1db'
payload = json.loads(lzma.decompress(packed))
assert payload['version'] == 1 and payload['copy_unit'] == 'unicode-codepoint'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
run(['git', 'merge-base', '--is-ancestor', payload['source_base'], head])
seen = set()
for entry in payload['files']:
    name = entry['path']; p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and name not in seen
    assert name in CANON or name.startswith(BATCH)
    seen.add(name); target = ROOT / name
    if entry['before_sha256'] is None:
        assert not target.exists(), name
        old = ''
    else:
        data = target.read_bytes(); assert digest(data) == entry['before_sha256'], name
        old = data.decode('utf-8')
    parts = []
    for item in entry['pieces']:
        if item[0] == 'copy':
            _, start, size = item
            assert 0 <= start <= start + size <= len(old)
            parts.append(old[start:start + size])
        else:
            assert item[0] == 'text' and isinstance(item[1], str)
            parts.append(item[1])
    result = ''.join(parts).encode('utf-8')
    assert digest(result) == entry['after_sha256'], name
    target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(result)
assert CANON <= seen
for entry in payload['preimages']:
    assert entry['path'] in CANON and entry['archive'].startswith(BATCH + 'before/')
    data = subprocess.check_output(['git', 'cat-file', 'blob', entry['git_blob']])
    assert digest(data) == entry['sha256']
    target = ROOT / entry['archive']; assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)

public = payload['public_paths']
assert set(public) == CANON - {'the-return-of-zero-central-plan.md'}
args = ['python3', 'tools/audit-canonical-argument-recovery.py', '--strict', '--json']
for name in public: args += ['--path', name]
with (OUT / 'strict.json').open('w') as f: run(args, stdout=f)
with (OUT / 'detector-tests.txt').open('w') as f:
    run(['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_canonical_argument_recovery_audit.py', '-v'], stdout=f, stderr=subprocess.STDOUT)
for builder in ['build-source-projections.py', 'build-section-rooms.py', 'build-navigation.py']:
    run(['python3', 'tools/' + builder]); run(['python3', 'tools/' + builder, '--check'])

spec = importlib.util.spec_from_file_location('reader_audit', ROOT / 'tools/audit-reader-navigation.py')
reader = importlib.util.module_from_spec(spec); spec.loader.exec_module(reader)
audit = reader.ReaderAudit(ROOT); checked = []
for name in public:
    for link in reader.links((ROOT / name).read_text()):
        target, status = audit.resolve(name, link)
        assert 'missing' not in status and 'unresolved' not in status, (name, link, status)
        checked.append({'source': name, 'href': link['href'], 'status': status})
assert len(checked) == 81
run(['git', 'diff', '--check'])
changed = subprocess.check_output(['git', 'diff', '--name-only', '-z']).decode().split('\0')
added = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
paths = sorted(set(p for p in changed + added if p))
assert all(p in CANON or p.startswith(BATCH) or generated(p) for p in paths), paths
assert all((ROOT / p).is_file() and not (ROOT / p).is_symlink() for p in paths)
for entry in payload['files']:
    assert digest((ROOT / entry['path']).read_bytes()) == entry['after_sha256'], entry['path']
receipt = {'staging_head': head, 'source_base': payload['source_base'],
           'strict': json.loads((OUT / 'strict.json').read_text()), 'detector_tests': 17,
           'links_checked': len(checked), 'generated_freshness': 'all three builders pass',
           'changed_paths': paths, 'unexpected_mutations': [],
           'whole_suite': 'The retained FULL-SUITE.txt records the local native run with three inherited failures; this staging run does not assert a green whole suite.',
           'ref_publication': 'none; candidate objects only, awaiting connector comparison and publication'}
receipt_path = BATCH + 'NATIVE-STAGE.json'
(ROOT / receipt_path).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n'); paths.append(receipt_path)

def post(endpoint, value):
    req = urllib.request.Request('https://api.github.com/repos/' + os.environ['GITHUB_REPOSITORY'] + '/git/' + endpoint,
            data=json.dumps(value).encode(), method='POST', headers={
                'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
                'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=60) as response: return json.load(response)

entries = []
existing_blobs = {x['git_blob'] for x in payload['preimages']}
for name in paths:
    data = (ROOT / name).read_bytes(); expected = git_blob(data)
    if expected not in existing_blobs:
        response = post('blobs', {'encoding': 'base64', 'content': base64.b64encode(data).decode()})
        assert response['sha'] == expected
    entries.append({'path': name, 'mode': '100644', 'type': 'blob', 'sha': expected})
base_tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
tree = post('trees', {'base_tree': base_tree, 'tree': entries})
result = {'parent_sha': head, 'tree_sha': tree['sha'], 'entries': entries, 'source_base': payload['source_base']}
(OUT / 'candidate-tree.json').write_text(json.dumps(result, indent=2) + '\n')
print('CANDIDATE_TREE=' + tree['sha'])
print('PARENT_COMMIT=' + head)
print('STAGED_FILES=' + str(len(entries)))
