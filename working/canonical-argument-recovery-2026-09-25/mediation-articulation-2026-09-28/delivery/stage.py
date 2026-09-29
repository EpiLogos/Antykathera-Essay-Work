"""Validate the retained mediation patch; create a candidate tree, never update refs."""
from pathlib import Path, PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import base64, gzip, hashlib, importlib.util, json, lzma, os, re, subprocess, urllib.request

REPO = 'EpiLogos/Antykathera-Essay-Work'
ROOT = Path.cwd()
BATCH = 'working/canonical-argument-recovery-2026-09-25/mediation-articulation-2026-09-28/'
OUT = Path(os.environ['RUNNER_TEMP']) / 'mediation-publication'
OUT.mkdir(parents=True, exist_ok=True)
PARTS = [{'sha': '7e0ebabe5ccfe0ca35fbcd0532fc7b45cc96902f', 'size': 8500}, {'sha': '98d651874efeb2a15771d06e9385ae6669cd6010', 'size': 8500}, {'sha': '3677736077d3895043aa89492135078e5411a84f', 'size': 8500}, {'sha': '0d47a45c7dec0540babc6a4c6d5c1f24b3c9d068', 'size': 8500}, {'sha': '487e211ead485ac7843201834db3fa41e22768f9', 'size': 8501, 'base64_remove_index': 8016, 'restored_sha': 'c3f6a4a6afd9b3a2af0f595c67f2057752c3856d', 'restored_size': 8500}, {'sha': '147e502d9e72e0128b03eda27543452041b1aebe', 'size': 8500}, {'sha': 'b27329e4ba951b89c2e1f0e26dd3bb65ebf296d0', 'size': 8500}, {'sha': '1b836d00925d820c9fccde7520f0fb743af68c47', 'size': 8500}, {'sha': '5ab3bec8f4aa434528dfb7242a732d10cb1d2f50', 'size': 8500}, {'sha': '1dc69191421ce9f8826b7e11076e72ea35147223', 'size': 8500}, {'sha': '67c25e1b47ac5c7c992a8d11cadbf0583c855256', 'size': 8500}, {'sha': '4ce8cebb33a1c66b16350c1d68dfe85476655905', 'size': 2132}]
PACKED_SHA256 = '56334c002e14bb34a141c4bfe24f92527ec106acec4eaaad924a523f1da10f8e'
RAW_SHA256 = '774690451db2a761374bb48807dca5d7f1ac83dca4a39a0291ce61481f62f0ad'

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
    with urllib.request.urlopen(req, timeout=90) as response:
        return json.load(response)

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

def get_part(entry):
    result = api('git/blobs/'+entry['sha'])
    assert result['encoding'] == 'base64' and result['sha'] == entry['sha']
    data = base64.b64decode(result['content'])
    assert blob(data) == entry['sha'] and len(data) == entry['size']
    if 'base64_remove_index' in entry:
        s = base64.b64encode(data).decode()
        i = entry['base64_remove_index']
        assert s[i] == 'w'
        data = base64.b64decode(s[:i]+s[i+1:]+'=')
        assert len(data) == entry['restored_size'] and blob(data) == entry['restored_sha']
    return data

with ThreadPoolExecutor(max_workers=4) as pool:
    packed = b''.join(pool.map(get_part,PARTS))
assert len(packed) == 95632 and digest(packed) == PACKED_SHA256
raw = lzma.decompress(packed)
assert digest(raw) == RAW_SHA256
payload = json.loads(raw)
assert payload['base'] == 'ac55ed990878d5aa2a652d55d060816eee99c9cf'
assert len(payload['files']) == 17
canon = {x['path'] for x in payload['files']}
assert len(canon) == 17
assert all('/movements/' not in x and (x.startswith('submission-package/essay/symbolon/')
    or x == 'the-return-of-zero-central-plan.md') for x in canon)
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
# Binding manifest includes the two repaired etymological recipients at their final
# cold-reviewed state; all seventeen original preimages were verified above.
for source in payload['source_hashes']:
    assert digest(safe(source['path']).read_bytes()) == source['sha256'], ('source changed',source['path'])
seen = set(canon)
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
    target.write_bytes(gzip.compress(data,mtime=0))
    seen.add(target_name)

minute = BATCH+'FOUNDATIONAL-SCOPE-2026-09-29.md'
safe(minute).write_text("""# Foundational recovery — revised authorial scope

The author has deferred the complete eight-room/48-movement pass. He is editing the manuscript by hand; movement records will later be filled from that achieved manuscript. Continue and publish the foundational A/A′/C, A/C, S and generating depth-field recovery now. Do not alter the sovereign manuscript or movement bodies.

This integration admits seventeen non-movement authored postimages from the retained mediation/articulation/Māyā packet. Its four movement edits and old generated surfaces are excluded. Current generated navigation/room/source surfaces are rebuilt from the resulting field; rebuilding a room summary is not a movement rewrite or semantic acceptance.

The canonical-recovery, writing and pre-manuscript-refinement protocols were reread afresh, with the authorial minute, anti-anti-overclaim correction, complete paired product reading, relational Logos input, orientation, repository shape, execution map and project writing laws/rubric. The later authorial scope above governs the older movement schedule. Protected originals remain untouched.

The imported ledgers describe the earlier drafting and later same-agent cold review. Their historical unpublished status and former movement scope are preserved as execution evidence, not assertions of the present branch. Current checks and subsequent remote publication have separate receipts. No whole-field acceptance, independent peer review or new manuscript ratification is asserted.
""")
seen.add(minute)
public = sorted(canon-{'the-return-of-zero-central-plan.md'})
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
    'payload_sha256':digest(raw),'authored_records':17,'movement_bodies_changed':0,
    'strict':strict,'links_checked':len(checks),'full_suite_exit':suite_exit,
    'full_suite_tail':suite[-14000:],'generated_changes':sum(generated(x) for x in paths),
    'protected_or_unexpected_mutations':[],
    'acceptance':'Connected retained recovery only; all other shared/depth-field acceptance remains open.',
    'changed_records':[{'path':x,'git_blob':blob((ROOT/x).read_bytes())} for x in paths]}
receipt_path = BATCH+'INTEGRATION-VALIDATION.json'
safe(receipt_path).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
paths.append(receipt_path)
for name in ('full-suite.txt','links.json','detector-tests.txt','diff-check.txt'):
    destination = BATCH+'integration-checks/'+name
    target = safe(destination)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes((OUT/name).read_bytes())
    paths.append(destination)
def upload(name):
    data = (ROOT/name).read_bytes()
    expected = blob(data)
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
