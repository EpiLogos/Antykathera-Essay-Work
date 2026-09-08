from pathlib import Path
import json,re,hashlib,datetime
root=Path.cwd();base=Path('working/p2-enrichment/audits/T21-current-reconciliation');d=json.loads((base/'current-row-audit.json').read_text());out=[]
def paras(path):
 p=Path(path)
 if not p.is_file(): return []
 lines=p.read_text().splitlines(); a=[];start=0
 for i,line in enumerate(lines+['']):
  if not line.strip():
   if i>start:a.append({'path':str(p),'start_line':start+1,'end_line':i,'text':'\n'.join(lines[start:i])})
   start=i+1
 return a
for r in d['rows']:
 field=Path(r['field_path']).parent.name; home=r['canonical_home'];ps=paras(home)
 candidates=[p for p in ps if field in p['text']]
 out.append({'row_id':r['row_id'],'path':home,'operation':r['operation'],'field':field,'sha256':hashlib.sha256(Path(home).read_bytes()).hexdigest() if Path(home).is_file() else None,'return_candidates':candidates,'standing':'Literal current paragraphs selected by link destination; no semantic certification.'})
(base/'current-fragment-locators.json').write_text(json.dumps({'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':out},indent=2,ensure_ascii=False)+'\n')
