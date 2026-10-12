"""Publish no refs: validate the retained repair and create an exact candidate tree."""
from pathlib import Path, PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import base64, gzip, hashlib, importlib.util, json, lzma, os, re, subprocess, urllib.request

REPO = 'EpiLogos/Antykathera-Essay-Work'
ROOT = Path.cwd()
BATCH = 'working/canonical-argument-recovery-2026-09-25/formation-return-2026-09-27/'
OUT = Path(os.environ['RUNNER_TEMP']) / 'formation-publication'
OUT.mkdir(parents=True, exist_ok=True)
PARTS = ['9471cf770ebc792bb077ad1b316f09c108206893',
         'c565247a0b5e1f4a09b54709c90e072ee52c3f0d',
         '5813dac319e3568020f2683ae8aaa44cb98da28f',
         '58ff669e3fc0a2120893c7aa8dad3297e405b1e8',
         '1049cb2c21bc4053590f460e1bb189b95dad68d6',
         '88f40e53c3d7703a5d16035f3918c08d1ee05125']
CANON = {
    'submission-package/essay/symbolon/episteme/concepts/C17-Vikalpa-Samkalpa.md',
    'submission-package/essay/symbolon/episteme/concepts/C12-Script-Frozen-Conditioned-Will.md',
    'submission-package/essay/symbolon/episteme/arguments/A07-Vikalpa-Samkalpa-Script-Frozen-Conditioned-Will.md',
    'submission-package/essay/section-rooms/01-differentiating-mind/movements/09-s0-p2-vikalpa-samkalpa.md',
    'submission-package/essay/symbolon/episteme/concepts/vikalpa-samkalpa.md',
    'submission-package/essay/symbolon/episteme/arguments/A31-Deferential-Intelligence.md',
    'submission-package/essay/symbolon/episteme/concepts/C47-Deferential-Intelligence.md',
    'submission-package/essay/symbolon/episteme/maps/mono-poly-two-ones.md',
    'submission-package/essay/symbolon/episteme/maps/trust-faith-formal-limit.md',
    'submission-package/essay/symbolon/episteme/maps/zero-subject-advent.md',
    'submission-package/essay/symbolon/episteme/etymologies/genesis-paradigm-project-epilogos/WHOLE-FIELD.md',
}

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def api(endpoint, value=None):
    req = urllib.request.Request(
        'https://api.github.com/repos/' + REPO + '/' + endpoint,
        data=None if value is None else json.dumps(value).encode(),
        method='GET' if value is None else 'POST',
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json',
                 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)

def run(args, name):
    with (OUT / name).open('w') as stream:
        result = subprocess.run(args, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'{name}: exit {result.returncode}; see retained output')

def generated(name):
    ep = 'submission-package/essay/symbolon/episteme/'
    return (name.startswith(ep + 'maps/navigation/')
            or name in {ep + 'sources/' + n for n in
                        ('SOURCE-INDEX.md', 'PASSAGE-LEDGER.md', 'MAIN-SOURCES.md')}
            or name == 'submission-package/essay/section-rooms/README.md'
            or bool(re.fullmatch(r'submission-package/essay/section-rooms/\d\d-[^/]+/ROOM\.md', name)))

assert os.environ['GITHUB_REPOSITORY'] == REPO
assert os.environ['GITHUB_REF'] == 'refs/heads/main'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
base_tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip()
assert head == os.environ['GITHUB_SHA']
assert not subprocess.check_output(['git', 'status', '--porcelain'])

def get_part(sha):
    result = api('git/blobs/' + sha)
    assert result['encoding'] == 'base64' and result['sha'] == sha
    data = base64.b64decode(result['content'])
    assert blob(data) == sha
    return data

with ThreadPoolExecutor(max_workers=4) as pool:
    packed = b''.join(pool.map(get_part, PARTS))
assert len(packed) == 50916
assert sha256(packed) == '659cac659ca75f643479ad220c6fa3cd88d6e2a1bfdd772162327206fe5d1553'
raw = lzma.decompress(packed)
assert sha256(raw) == '10564ce77b40bc659fe91a309713ec39df24b6f3e963e917ab96172e9b04316f'
payload = json.loads(raw)
assert payload['base'] == '27bcc5fcd915b3c6fc6b4c74f3ff29bfc2ad2d3e'
assert len(payload['files']) == 28 and len(payload['preimages']) == 11
seen = set()
originals = {}
for entry in payload['files']:
    name = entry['path']
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and name not in seen
    assert name in CANON or (name.startswith(BATCH) and p.parent.as_posix() + '/' == BATCH)
    target = ROOT / name
    assert not target.is_symlink()
    seen.add(name)
    if entry['before'] is None:
        assert not target.exists(), name
    else:
        assert name in CANON
        data = target.read_bytes()
        assert blob(data) == entry['before'], ('source changed', name)
        originals[name] = data
    assert blob(entry['content'].encode()) == entry['after'], ('payload changed', name)
assert set(originals) == CANON
readings_entry = next(x for x in payload['files'] if x['path'] == BATCH + 'SOURCE-READINGS.json')
source_readings = json.loads(readings_entry['content'])['readings']
for reading in source_readings:
    if reading['path'] not in CANON:
        assert sha256((ROOT / reading['path']).read_bytes()) == reading['sha256'], ('generating source changed', reading['path'])

for entry in payload['files']:
    target = ROOT / entry['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(entry['content'].encode())
for entry in payload['preimages']:
    assert entry['original_path'] in CANON and entry['path'].startswith(BATCH + 'before/')
    assert '..' not in PurePosixPath(entry['path']).parts
    data = originals[entry['original_path']]
    assert blob(data) == entry['before']
    compressed = bytearray(gzip.compress(data, mtime=0))
    compressed[9] = 255  # Match the retained Python 3.13 deterministic gzip header.
    compressed = bytes(compressed)
    assert blob(compressed) == entry['after'] and sha256(compressed) == entry['sha256']
    target = ROOT / entry['path']
    assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(compressed)
    seen.add(entry['path'])

args = ['python3', 'tools/audit-canonical-argument-recovery.py', '--strict', '--json']
for name in sorted(CANON):
    args += ['--path', name]
run(args, 'strict.json')
run(['python3', '-m', 'unittest', 'discover', '-s', 'tests', '-p',
     'test_canonical_argument_recovery_audit.py', '-v'], 'detector-tests.txt')
for builder in ('build-source-projections.py', 'build-section-rooms.py', 'build-navigation.py'):
    run(['python3', 'tools/' + builder], builder + '.build.txt')
    run(['python3', 'tools/' + builder, '--check'], builder + '.check.txt')

spec = importlib.util.spec_from_file_location('reader_audit', ROOT / 'tools/audit-reader-navigation.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
audit = reader.ReaderAudit(ROOT)
checks = []
for name in sorted(CANON):
    for link in reader.links((ROOT / name).read_text()):
        target, status = audit.resolve(name, link)
        assert 'missing' not in status and 'unresolved' not in status, (name, link, status)
        checks.append({'source': name, 'href': link['href'], 'status': status})
assert len(checks) == 143
(OUT / 'links.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2) + '\n')
run(['git', 'diff', '--check'], 'diff-check.txt')
changed = subprocess.check_output(['git', 'diff', '--name-only', '-z']).decode().split('\0')
added = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z']).decode().split('\0')
paths = sorted(set(x for x in changed + added if x))
assert all(x in seen or generated(x) for x in paths), paths
assert all((ROOT / x).is_file() and not (ROOT / x).is_symlink() for x in paths)
for entry in payload['files']:
    assert blob((ROOT / entry['path']).read_bytes()) == entry['after']

strict = json.loads((OUT / 'strict.json').read_text())
receipt = {
    'status': 'native-checks-passed; candidate-tree-prepared; ref-publication-separate',
    'staging_parent': head, 'staging_parent_tree': base_tree,
    'reviewed_source_base': payload['base'],
    'payload_sha256': sha256(raw),
    'authored_records': len(CANON), 'preserved_preimages': len(payload['preimages']),
    'generating_source_hashes_checked': len(source_readings),
    'strict_files': strict['files'], 'strict_errors': strict['errors'],
    'strict_review_candidates': strict['review_candidates'],
    'detector_tests': 17, 'links_checked': len(checks),
    'generated_freshness': 'all three native builders pass',
    'generated_changes': sum(generated(x) for x in paths),
    'unexpected_mutations': [], 'protected_source_mutations': [],
    'validation_scope': 'Fresh scoped recovery, detector, link, builder and whitespace checks. No new full-suite execution or whole-field semantic acceptance is asserted.',
    'historical_full_suite': 'Retained FULL-SUITE.txt records 132 tests, one global quality-coverage failure and one AIKit-unavailable skip.',
    'changed_records': [{'path': x, 'git_blob': blob((ROOT / x).read_bytes())} for x in paths],
}
receipt_path = BATCH + 'PUBLICATION-RECEIPT.json'
(ROOT / receipt_path).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
paths.append(receipt_path)

# Independent immutable blobs are uploaded concurrently; no branch ref is changed here.
def upload(name):
    data = (ROOT / name).read_bytes()
    expected = blob(data)
    result = api('git/blobs', {'encoding': 'base64', 'content': base64.b64encode(data).decode()})
    assert result['sha'] == expected
    return {'path': name, 'mode': '100644', 'type': 'blob', 'sha': expected}
with ThreadPoolExecutor(max_workers=4) as pool:
    entries = list(pool.map(upload, paths))
tree = api('git/trees', {'base_tree': base_tree, 'tree': entries})
result = {'parent_sha': head, 'tree_sha': tree['sha'], 'entries': entries,
          'source_base': payload['base'], 'receipt': receipt}
(OUT / 'candidate-tree.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print('CANDIDATE_TREE=' + tree['sha'])
print('PARENT_COMMIT=' + head)
print('STAGED_FILES=' + str(len(entries)))
