from pathlib import Path
import json,re,hashlib,urllib.parse
P=Path(__file__).parent;root=Path.cwd();rows=json.loads((P/'carrier-list.json').read_text());base=Path('submission-package/essay/symbolon/episteme/etymologies')
E={i+1:p for i,p in enumerate([base/n for n in ['encounter-region-name-count','arbitration-hybris-regard-anamnesis','trust-place-logos-nomos-natio-credere','symbol-account-and-trust','homology-and-analogy','apportionment-and-economy']])}
primary=[5,1,3,4,5,5,4,2,6,4,5,4,5,4,1,1,6,4,2]
paths=[Path(r['path']) for r in rows]+[p/n for p in E.values() for n in ['WHOLE-FIELD.md','HISTORICAL-BRANCHES.md']]
text={str(p):p.read_text() for p in paths}
def outgoing(f):
 t=text[str(f)];result=[]
 for m in re.finditer(r'\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)',t):
  u=m.group(1).strip('<>');u=urllib.parse.unquote(u)
  if ':' in u.split('/')[0]:continue
  path,_,anchor=u.partition('#');target=(f.parent/path).resolve() if path else f.resolve()
  try:rel=str(target.relative_to(root))
  except ValueError:continue
  start=t.rfind('\n\n',0,m.start())+2;end=t.find('\n\n',m.end());end=len(t) if end<0 else end
  result.append({'target':rel,'anchor':anchor,'start_line':t[:start].count('\n')+1,'end_line':t[:end].count('\n')+1,'paragraph':t[start:end]})
 return result
edges={str(f):outgoing(f) for f in paths}
proof=[];missing=[]
for r,prim in zip(rows,primary):
 p=r['path'];rec={'record_id':r['record_id'],'path':p,'primary_field':'E'+str(prim),'sha256':hashlib.sha256(text[p].encode()).hexdigest(),'relations':[]}
 for e,ep in E.items():
  w=str(ep/'WHOLE-FIELD.md');b=str(ep/'HISTORICAL-BRANCHES.md')
  fw=[x for x in edges[w] if x['target']==p];br=[x for x in edges[b] if x['target']==p];back=[x for x in edges[p] if x['target'] in [w,b]]
  if fw or br or back:
   rec['relations'].append({'field':'E'+str(e),'whole_forward':fw,'branch_forward':br,'carrier_return':back,'primary':e==prim})
   if not fw or not back:missing.append({'record':r['record_id'],'field':e,'forward':bool(fw),'back':bool(back),'branch':bool(br)})
 if not any(x['primary'] and x['whole_forward'] and x['carrier_return'] for x in rec['relations']):missing.append({'record':r['record_id'],'primary_missing':True})
 proof.append(rec)
(P/'E19-actual-graph-semantic-proof.json').write_text(json.dumps({'basis':'Actual current Markdown destinations with complete operation paragraphs, not vocabulary inference','rows':proof,'missing_directions':missing},ensure_ascii=False,indent=2)+'\n')
print('19 records; primary complete',sum(any(x['primary'] and x['whole_forward'] and x['carrier_return'] for x in r['relations']) for r in proof));print('Relations',sum(len(r['relations']) for r in proof));print(json.dumps(missing,indent=2))
