"""Validate the reviewed return/dependence patch; create a candidate tree, never update refs."""
from pathlib import Path, PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import base64, gzip, hashlib, importlib.util, json, lzma, os, re, subprocess, urllib.request

REPO = 'EpiLogos/Antykathera-Essay-Work'
ROOT = Path.cwd()
BATCH = 'working/canonical-argument-recovery-2026-09-25/return-dependence-2026-09-29/'
OUT = Path(os.environ['RUNNER_TEMP']) / 'return-dependence-publication'
OUT.mkdir(parents=True, exist_ok=True)
EXPECTED_RECORD_BLOBS = ['b519147be610f713608366f196dca8482272353f','92a434a619b1d31329534cc0253614a31a1c6b70','6bebc21f7561e76fcab22352fa29a097570ce1f2','b506448dcf9c706aae88c94033b28517e0bb5885','7ff6ba72f045041a6d7885361fea53e58e743ec1','ab0dde2cb1d75017dfb6ce4f9541fb0f8acab297','f06fd4df052300b497c08b9884f5ba90f58ff6a4','1c854a81bab810366d23589fc345222745c3349f']

def digest(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def api(endpoint, value=None):
    req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/' + endpoint,
        data=None if value is None else json.dumps(value).encode(),
        method='GET' if value is None else 'POST',
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'})
    import time
    from urllib.error import HTTPError
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=90) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code not in (500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep((2, 8, 20)[attempt])

def run(args, name, required=True):
    with (OUT/name).open('w') as stream:
        result = subprocess.run(args, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    if required and result.returncode:
        raise RuntimeError(f'{name}: exit {result.returncode}; inspect retained output')
    return result.returncode

def safe(name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts
    assert not (ROOT/name).is_symlink()
    return ROOT/name

def generated(name):
    ep = 'submission-package/essay/symbolon/episteme/'
    return (name.startswith(ep+'maps/navigation/')
        or name in {ep+'sources/'+n for n in ('SOURCE-INDEX.md','PASSAGE-LEDGER.md','MAIN-SOURCES.md')}
        or name == 'submission-package/essay/section-rooms/README.md'
        or bool(re.fullmatch(r'submission-package/essay/section-rooms/\d\d-[^/]+/ROOM\.md',name)))

assert os.environ['GITHUB_REPOSITORY'] == REPO
assert os.environ['GITHUB_REF'] == 'refs/heads/main'
head = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
base_tree = subprocess.check_output(['git','rev-parse','HEAD^{tree}'],text=True).strip()
assert head == os.environ['GITHUB_SHA']
assert not subprocess.check_output(['git','status','--porcelain'])

record_paths = sorted((ROOT/BATCH/'delivery/records').glob('*.json'))
assert len(record_paths) == 8
assert [blob(p.read_bytes()) for p in record_paths] == EXPECTED_RECORD_BLOBS
raw = b''.join(p.read_bytes() for p in record_paths)
payload = {'base':'4f21127fae76070611f228ac16c62d8242fe310f',
    'files':[json.loads(p.read_text()) for p in record_paths],
    'source_hashes':json.loads((ROOT/BATCH/'SOURCE-SCOPE.json').read_text())['sources'],
    'evidence':{}}
canon = {x['path'] for x in payload['files']}
assert len(canon) == 8
assert all('/movements/' not in x and (x.startswith('submission-package/essay/symbolon/')
    or x == 'the-return-of-zero-central-plan.md') for x in canon)
for identity in ('A17','A34','C60'):
    run(['python3','tools/okf-workspace.py','--project-root','.',
         'effects',identity,'--depth','4','--json'],identity+'-effects-before.json')
originals = {}
postimages = {}
for entry in payload['files']:
    name = entry['path']
    original = safe(name).read_bytes()
    assert blob(original) == entry['before'], ('preimage changed',name)
    originals[name] = original
    text = original.decode()
    previous_start = len(text)+1
    for start,end,replacement in reversed(entry['edits']):
        assert 0 <= start <= end < previous_start
        text = text[:start]+replacement+text[end:]
        previous_start = start
    post = text.encode()
    assert blob(post) == entry['after'], ('postimage mismatch',name)
    postimages[name] = post
for name,data in postimages.items():
    safe(name).write_bytes(data)
# Source manifest includes the exact current Hatcher paraphrase postimage.
# All eight original preimages and every repaired postimage were verified above.
for source in payload['source_hashes']:
    assert digest(safe(source['path']).read_bytes()) == source['sha256'], ('source changed',source['path'])
seen = set(canon)
for filename, expected in (
    ('COLD-REVIEW-CORRECTIONS.json','61402398507f61548e2d729e4befabf1a76fbd2a'),
    ('NEGATION-REVIEW.json','eb04e964d359b550b1d707863f12ca6b3296baeb')):
    data = safe(BATCH+'delivery/review/'+filename).read_bytes()
    assert blob(data) == expected
    json.loads(data)
    destination = BATCH+filename+'.gz'
    target = safe(destination)
    assert not target.exists()
    target.write_bytes(gzip.compress(data,mtime=0))
    assert gzip.decompress(target.read_bytes()) == data
    seen.add(destination)
for name,text in payload['evidence'].items():
    assert name.startswith(BATCH)
    target = safe(name)
    assert not target.exists(), ('existing evidence',name)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text)
    seen.add(name)
for name,data in originals.items():
    target_name = BATCH+'integration-preimages/'+name+'.gz'
    target = safe(target_name)
    assert not target.exists()
    target.parent.mkdir(parents=True,exist_ok=True)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(gzip.compress(data,mtime=0))
    seen.add(target_name)

public = sorted(x for x in canon if x != 'the-return-of-zero-central-plan.md' and '/sources/' not in x)
assert len(public) == 6
args = ['python3','tools/audit-canonical-argument-recovery.py','--strict','--json']
for name in public:
    args += ['--path',name]
run(args,'strict.json')
run(['python3','-m','unittest','discover','-s','tests','-p',
     'test_canonical_argument_recovery_audit.py','-v'],'detector-tests.txt')
for builder in ('build-source-projections.py','build-section-rooms.py','build-navigation.py'):
    run(['python3','tools/'+builder],builder+'.build.txt')
    run(['python3','tools/'+builder,'--check'],builder+'.check.txt')
spec = importlib.util.spec_from_file_location('reader_audit',ROOT/'tools/audit-reader-navigation.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
audit = reader.ReaderAudit(ROOT)
checks = []
for name in sorted(canon):
    targets = reader.links((ROOT/name).read_text())
    if name == 'the-return-of-zero-central-plan.md':
        old = {x['href'] for x in reader.links(originals[name].decode())}
        targets = [x for x in targets if x['href'] not in old]
    for link in targets:
        target,status = audit.resolve(name,link)
        assert 'missing' not in status and 'unresolved' not in status,(name,link,status)
        checks.append({'source':name,'href':link['href'],'status':status})
(OUT/'links.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
run(['python3','tools/audit-room-depth.py','--project-root','.',
     '--require-deepened'],'room-depth.json')
run(['python3','tools/audit-pre-manuscript.py','--project-root','.',
     '--output',str(OUT/'pre-manuscript.json')],'pre-manuscript.txt')
suite_exit = run(['python3','-m','unittest','discover','-s','tests','-v'],'full-suite.txt',False)
suite = (OUT/'full-suite.txt').read_text()
if suite_exit:
    assert 'Ran 132 tests' in suite and 'FAILED (failures=1, skipped=1)' in suite, suite[-8000:]
    assert 'test_canonical_graph_has_no_missing_quality_surfaces_or_governing_dangles' in suite, suite[-8000:]
run(['git','diff','--check'],'diff-check.txt')
changed = subprocess.check_output(['git','diff','--name-only','-z']).decode().split('\0')
added = subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0')
paths = sorted(set(x for x in changed+added if x))
assert all(x in seen or generated(x) for x in paths), paths
assert not any('/movements/' in x or x.endswith('/THE-RETURN-OF-ZERO.md') for x in paths)
assert all((ROOT/x).is_file() and not (ROOT/x).is_symlink() for x in paths)
for name,data in postimages.items():
    assert (ROOT/name).read_bytes() == data
strict = json.loads((OUT/'strict.json').read_text())
receipt = {'status':'validated candidate; native ref publication remains separate',
    'parent_sha':head,'parent_tree':base_tree,'reviewed_source_base':payload['base'],
    'payload_sha256':digest(raw),'authored_records':8,'complete_operation_bodies':5,'bounded_supporting_records':3,'movement_bodies_changed':0,
    'strict':strict,'links_checked':len(checks),'full_suite_exit':suite_exit,
    'full_suite_tail':suite[-14000:],'generated_changes':sum(generated(x) for x in paths),
    'protected_or_unexpected_mutations':[],
    'acceptance':'Connected retained recovery only; all other shared/depth-field acceptance remains open.',
    'changed_records':[{'path':x,'git_blob':blob((ROOT/x).read_bytes())} for x in paths]}
receipt_path = BATCH+'INTEGRATION-VALIDATION.json'
safe(receipt_path).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
paths.append(receipt_path)
for name in ('full-suite.txt','links.json','detector-tests.txt','diff-check.txt','strict.json',
    'A17-effects-before.json','A34-effects-before.json','C60-effects-before.json',
    'room-depth.json','pre-manuscript.json','pre-manuscript.txt'):
    destination = BATCH+'integration-checks/'+name
    target = safe(destination)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes((OUT/name).read_bytes())
    paths.append(destination)
(OUT/'INTEGRATION-VALIDATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
(OUT/'validated-paths.json').write_text(json.dumps(
    [{'path':name,'mode':'100644','type':'blob','sha':blob((ROOT/name).read_bytes())} for name in paths],
    ensure_ascii=False,indent=2)+'\n')
def upload(name):
    data = (ROOT/name).read_bytes()
    expected = blob(data)
    print('UPLOAD',name,len(data),expected,flush=True)
    result = api('git/blobs',{'encoding':'base64','content':base64.b64encode(data).decode()})
    assert result['sha'] == expected
    return {'path':name,'mode':'100644','type':'blob','sha':expected}
with ThreadPoolExecutor(max_workers=4) as pool:
    entries = list(pool.map(upload,paths))
tree = api('git/trees',{'base_tree':base_tree,'tree':entries})
result = {'parent_sha':head,'tree_sha':tree['sha'],'entries':entries,
          'source_base':payload['base'],'receipt':receipt}
(OUT/'candidate-tree.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('CANDIDATE_TREE='+tree['sha'])
print('PARENT_COMMIT='+head)
print('STAGED_FILES='+str(len(entries)))
