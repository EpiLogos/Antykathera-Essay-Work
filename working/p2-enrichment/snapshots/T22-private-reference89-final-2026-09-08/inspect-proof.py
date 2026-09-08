from pathlib import Path
import json,re,hashlib
p=Path(__file__).parent;b=json.loads(Path('working/p2-enrichment/page-packets/T22-transfer-carrier-readonly-audit-private.json').read_text());c=json.loads(Path('working/p2-enrichment/page-packets/T22-reference89-actionable-compact.json').read_text());m=json.loads(Path('working/p2-enrichment/reference-note-dispositions.json').read_text());remap={h['previous_path']:h['path'] for r in m['rows'] for h in r['development_homes'] if 'previous_path' in h}
def norm(t):
 t=re.sub(r'\[([^\]\n]+)\]\((?:<[^>]+>|[^)\n]+)\)',r'\1',t)
 t=re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]',r'\2',t)
 return re.sub(r'\s+',' ',t).strip()
rows=[]
for r in b['references']:
 result=[];matches=0
 for f in r['prior']['consumer_fragments']:
  s=remap.get(f['path'],f['path']);file=Path(s)
  if not file.exists():result.append({'path':s,'status':'missing-path','old_fragment':f['fragment']});continue
  t=file.read_text();parts=[a for a in re.split(r'\n\s*\n',f['fragment']) if a.strip() and not a.lstrip().startswith('#')]
  if not parts:continue
  paras=[]
  for v in re.finditer(r'\S[\s\S]*?(?=\n\s*\n|\Z)',t):
   if v.group().lstrip().startswith('#'):continue
   paras.append((v.group(),t[:v.start()].count('\n')+1,t[:v.end()].count('\n')+1))
  for part in parts:
   found=[v for v in paras if norm(part)==norm(v[0])]
   if found:
    v=found[0];result.append({'path':s,'start_line':v[1],'end_line':v[2],'paragraph':v[0],'method':'exact inherited paragraph' if part==v[0] else 'same text after whitespace/link-destination normalization','prior_evidence_id':f['evidence_id']});matches+=1
   else:result.append({'path':s,'status':'paragraph-changed-or-superseded','old_fragment':part,'prior_evidence_id':f['evidence_id']})
 rows.append({'row':r['row'],'prior_status':c['rows'][r['row']-1]['disposition'],'verified_count':matches,'proofs':result})
(p/'inherited-paragraph-recheck.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
for r in rows:
 bad=[x for x in r['proofs'] if 'status'in x]
 print(r['row'],r['verified_count'],'changed',len(bad),r['prior_status'])
