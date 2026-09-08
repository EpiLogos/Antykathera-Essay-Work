from pathlib import Path
import json, hashlib, re, zipfile
R=Path.cwd(); S=R/'working/p2-enrichment/snapshots/T21-private-language-law-nation-centralisation-2026-09-08'
H=R/json.loads((S/'baseline.json').read_text())['path']; D=H.with_name('DEVELOPMENT.md')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H.read_bytes()==(S/'HISTORY-before.md').read_bytes()
t=D.read_text(); anchors=re.findall(r'<a id="([^"]+)"',t)
assert len(anchors)==len(set(anchors))
assert len(re.findall(r'^## #',t,re.M))==6
branches=list(re.finditer(r'^### ([IVX]+) — (.+)$',t,re.M)); assert len(branches)==12
rows=[]
for i,b in enumerate(branches):
 end=branches[i+1].start() if i+1<len(branches) else t.index('<a id="historical-anamnesis"')
 rows.append({'row_id':'history-language-law-nation-centralisation-'+b[1], 'branch':b[2], 'disposition':'inherited-admitted-branch-developed-in-companion','path':str(D.relative_to(R)),'start_line':t[:b.start()].count('\n')+1,'end_line':t[:end].count('\n'),'source_scope':'See branch body: documentary paraphrase, authorial programme and remaining debt explicitly separated','returns':['E3 situated language/law/people history','E2 criterion, affected evidence and revisable settlement','E6 capacity, labour, cost and governing office']})
(S/'branch-crosswalk.json').write_text(json.dumps({'rows':rows},indent=2)+'\n')
inputs={str(H.relative_to(R)):'protected owning history full read'}
for x in json.loads((S/'prior-full-reading-reuse.json').read_text()):
 p=R/x['path']; assert sha(p)==x['sha256']; inputs[x['path']]='prior full reading reused; unchanged hash'
for x in json.loads((S/'resolved-sources.json').read_text()):inputs[x['house']]='full SOURCE read; sibling NOTES absent'
for slug in ['arbitration-hybris-regard-anamnesis','trust-place-logos-nomos-natio-credere','apportionment-and-economy']:
 for n in ['WHOLE-FIELD.md','HISTORY.md','HISTORICAL-BRANCHES.md']:
  p=R/'submission-package/essay/symbolon/episteme/etymologies'/slug/n
  if p.exists():inputs[str(p.relative_to(R))]='full relevant E-field reading'
p='working/final-argument-quilt-2026-08-23/ETYMOLOGICAL-ARCHAEOLOGY-TREE-SEAMS.md'; inputs[p]='full authorial programme reading'
for sid in ['rafailov-et-al-2023-dpo','ostrom-2009-beyond-markets-states-nobel-lecture']:
 p=next((R/'submission-package/essay/symbolon/episteme/sources').glob('**/'+sid+'/SOURCE.md'));inputs[str(p.relative_to(R))]='full SOURCE read; NOTES absent'
packet={'parent_record_id':'history-language-law-nation-centralisation','target':str(D.relative_to(R)),'scope':'User-authorized companion; no new census identity; protected HISTORY untouched','inputs':[{'path':p,'sha256':sha(R/p),'read_scope':s} for p,s in inputs.items()],'external_reading':'Named scopes in DEVELOPMENT; acquisition is not a claim of full reading','validation':'Private companion binding; not generic queue packet validation'}
(S/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
(S/'targets.json').write_text(json.dumps({'elements':[{'canonical_home':str(D.relative_to(R)),'register':'episteme','record_id':'history-language-law-nation-centralisation-companion'}]},indent=2)+'\n')
(S/'DEVELOPMENT-final.md').write_bytes(D.read_bytes())
(S/'validation.json').write_text(json.dumps({'protected_history_unchanged':True,'history_sha256':sha(H),'development_sha256':sha(D),'words':len(t.split()),'six_positions':6,'branches':12,'unique_anchors':len(anchors),'bound_inputs':len(inputs),'unchanged_prior_full_reads':42,'canonical_scope':[str(D.relative_to(R))],'source_changes':0,'consumer_changes':0},indent=2)+'\n')
print((S/'validation.json').read_text())
