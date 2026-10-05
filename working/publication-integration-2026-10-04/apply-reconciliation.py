#!/usr/bin/env python3
"""Receive reviewed published bodies at ratified local homes without discarding drafts."""
from pathlib import Path
import importlib.util, json, os, re, subprocess
import yaml

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('reconcile', HERE/'reconcile-local.py')
m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
plan = json.loads((HERE/'RECONCILIATION-PLAN.json').read_text())
preservation = json.loads((HERE/'PRESERVATION.json').read_text())
assert m.git('rev-parse','HEAD').decode().strip() == plan['old_head']
assert m.git('rev-parse',preservation['ref']).decode().strip() == preservation['commit']
rows = plan['rows']
needed = sorted({r['published_blob'] for r in rows})
raw = m.git('cat-file','--batch',data=('\n'.join(needed)+'\n').encode());blobs={};at=0
for sha in needed:
    end=raw.index(b'\n',at);size=int(raw[at:end].decode().split()[2]);at=end+1
    blobs[sha]=raw[at:at+size];at+=size+1

def generated(path):
    return ('/maps/navigation/' in path or Path(path).name in ('SOURCE-INDEX.md','MAIN-SOURCES.md','PASSAGE-LEDGER.md')
            or path == 'submission-package/essay/section-rooms/README.md'
            or Path(path).name.startswith('ROOM-') or path.endswith('T25-current-census-acceptance.json'))

def preserve_metadata(received, local):
    if not local: return received
    try:
        a,b=received.decode(),local.decode()
        if not a.startswith('---\n') or not b.startswith('---\n'):return received
        ae=a.index('\n---',4);be=b.index('\n---',4)
        af=yaml.safe_load(a[4:ae]) or {};bf=yaml.safe_load(b[4:be]) or {}
        extra={k:v for k,v in bf.items() if k not in af}
        if not extra:return received
        return (a[:ae]+'\n'+yaml.safe_dump(extra,sort_keys=False,allow_unicode=True).rstrip()+a[ae:]).encode()
    except (UnicodeError,ValueError,yaml.YAMLError):return received

updates=[];retained=[]
for r in rows:
    path=r['local_path'];target=m.ROOT/path
    before=target.read_bytes() if target.is_file() and not target.is_symlink() else None
    if m.digest(before)!=r['preimage_sha256']:raise RuntimeError('concurrent change: '+path)
    if (r['decision']=='preserve-authorial' or generated(path) or path in
        ('.github/workflows/r3-field-snapshot.yml','tools/build-t25-refinement-admission.py','submission-package/essay/README.md')
        or path.startswith(('working/sources-texts-references/','definition-of-god-working/'))):
        retained.append(dict(path=path,sha256=m.digest(before),reason='Authorial source or ratified local presentation/tooling; generated locators rebuild from received canon'))
        continue
    data=(HERE/'.legacy-candidates'/path).read_bytes()
    disposition=r['decision']
    if path=='the-return-of-zero-central-plan.md':
        text=data.decode()
        text=re.sub(r'<<<<<<<[^\n]*\n(.*?)\n=======\n(.*?)\n>>>>>>>[^\n]*',lambda x:x[2],text,flags=re.S)
        data=text.encode();disposition='Receive published torus and subject/means corrections; retain ratified local structural amendments'
    elif path.startswith('submission-package/essay/'):
        # These are the complete independently reviewed published operations,
        # received without reviving the earlier local paraphrases. Only links move.
        data=m.relocate(blobs[r['published_blob']],r['published_path'],path)
        data=preserve_metadata(data,before)
        disposition='Receive complete reviewed published body at ratified home; retain additional local identity metadata'
    elif r['decision']=='conflict':
        raise RuntimeError('Unclassified conflict: '+path)
    if not path.startswith('working/') and re.search(rb'^(<<<<<<< |>>>>>>> )',data,re.M):raise RuntimeError('markers: '+path)
    updates.append((target,before,data,r,disposition))

for target,before,data,r,disposition in updates:
    now=target.read_bytes() if target.is_file() else None
    if now!=before:raise RuntimeError('concurrent write: '+str(target))
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    target.chmod(0o755 if r['mode']=='100755' else 0o644)

# The saved snapshot and original index retain every earlier byte/staged move.
# HEAD now names published main; remaining local migration/drafts stay visible.
m.git('read-tree',plan['incoming_main'])
m.git('update-ref','refs/heads/main',plan['incoming_main'])
m.git('symbolic-ref','HEAD','refs/heads/main')
receipt=dict(schema='essay.local-recovery-receipt/v1',published_main=plan['incoming_main'],preservation=preservation,
    written=[dict(path=r['local_path'],published_path=r['published_path'],published_blob=r['published_blob'],before_sha256=m.digest(before),after_sha256=m.digest(data),disposition=disposition) for target,before,data,r,disposition in updates],retained=retained,
    standing='Published recovery received into ratified local layout; authorial working changes retained, not newly accepted or published')
(HERE/'LOCAL-CONVERGENCE.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(head=m.git('rev-parse','HEAD').decode().strip(),written=len(updates),retained=len(retained),preserved=preservation['ref'])))
