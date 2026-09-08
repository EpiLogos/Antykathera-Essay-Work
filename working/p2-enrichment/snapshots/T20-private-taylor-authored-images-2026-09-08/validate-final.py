from pathlib import Path
import json,re,hashlib,zipfile,subprocess,sys
import yaml
b=Path('working/p2-enrichment/snapshots/T20-private-taylor-authored-images-2026-09-08');p=Path('submission-package/essay/symbolon/mytheme/worlds/frank-taylor/taylor-authored-images/WHOLE.md');s=p.read_text();h=lambda x:hashlib.sha256(x).hexdigest();write=lambda name,x:(b/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');errors=[]
source=Path('submission-package/essay/symbolon/episteme/sources/internal-corpus/taylor/taylor-2026-personal-poetry-corpus/SOURCE.md');src=source.read_text();poems=[]
for n in range(1,24):
 original=re.search(r'<a id="taylor-2026-personal-poetry-corpus-q%03d"></a>\n(.*?)(?=\n<a id=|\n## Provenance and exclusions|\Z)'%n,src,re.S).group(1)
 quote=re.search(r'(^>.*?)(?=\n\n- \*\*Locator:)',original,re.M|re.S).group(1)
 section=re.search(r'<a id="taylor-ft-p%02d"></a>\n(.*?)(?=\n<a id=|\Z)'%n,s,re.S).group(1)
 actual=re.search(r'(^>.*?)(?=\n\n\[Complete source witness\])',section,re.M|re.S).group(1)
 ok=quote==actual and s.count('<a id="taylor-ft-p%02d"></a>'%n)==1
 poems.append({'unit':f'FT-P{n:02d}','exact_bytes':ok,'quote_sha256':h(quote.encode()),'quote_lines':len(quote.split('\n'))})
 if not ok:errors.append(f'Poem mismatch {n}')
anchors=re.findall(r'<a id="([^"]+)"></a>',s);assert len(anchors)==len(set(anchors))==39
heads=re.findall(r'^## (#\S+)',s,re.M);assert heads==['#0','#1','#2','#3','#4','#5→0'],heads
meta=yaml.safe_load(s.split('---',2)[1]);assert meta['record_id']=='mytheme-taylor-authored-images' and meta['poem_units']==23 and meta['admitted_image_units']==14
links=[]
for dest in re.findall(r'\]\(([^)]+)\)',s):
 f,_,a=dest.strip('<>').partition('#');target=(p.parent/f).resolve() if f else p.resolve();ok=target.is_file()
 if ok and a:ok=f'id="{a}"' in target.read_text()
 links.append({'destination':dest,'resolved':ok})
 if not ok:errors.append('Link unresolved '+dest)
manifest=json.loads((b/'bound-inputs-manifest.json').read_text());archive=[];live=[]
with zipfile.ZipFile(b/'bound-inputs.zip') as z:
 assert z.testzip() is None
 for x in manifest:
  ok=h(z.read(x['archive_member']))==x['sha256'];archive.append({'path':x['path'],'matched':ok});now=Path(x['path']);same=now.exists() and h(now.read_bytes())==x['sha256'];live.append({'path':x['path'],'matched':same})
  if not ok:errors.append('Archive mismatch '+x['path'])
  if not same:errors.append('Live stale '+x['path'])
rows=json.loads((b/'unit-crosswalk.json').read_text())['rows'];inherited={r['row_id']:r for r in json.loads((b/'coverage-rows.json').read_text())['rows']};lines=s.split('\n')
for r in rows:
 assert r['disposition']==inherited[r['row_id']]['disposition']
 a=r['draft_anchor']
 if a:
  start=next(i for i,l in enumerate(lines,1) if l==f'<a id="{a}"></a>');end=next((i-1 for i,l in enumerate(lines,1) if i>start and l.startswith('<a id=')),len(lines));r['draft_occurrence']={'path':str(p),'start_line':start,'end_line':end,'anchor':a}
assert len(rows)==40
write('unit-crosswalk.json',{'rows':rows,'counts':{'whole':1,'poems':23,'admitted_image_subunits':14,'held':2}})
assert sum(r['disposition']=='admitted-individual-poem' for r in rows)==23
assert sum(r['disposition']=='admitted-subordinate-unit' for r in rows)==14
assert all(r['draft_anchor'] is None for r in rows if not r['disposition'].startswith('admitted'))
external=json.loads((b/'external-witnesses.json').read_text());externalchecks=[{'path':x['original_path'],'unchanged':Path(x['original_path']).exists() and h(Path(x['original_path']).read_bytes())==x['sha256']} for x in external]
assert all(x['unchanged'] for x in externalchecks)
packet=json.loads((b/'packet.json').read_text());sourcechecks=[]
for x in packet['sources']:
 sp=Path(x['source']);np=sp.with_name('NOTES.md');sourcechecks.append({'path':str(sp),'unchanged':h(sp.read_bytes())==x['source_sha256'],'notes_absent_as_bound':not np.exists() and x['notes'] is None})
assert all(x['unchanged'] and x['notes_absent_as_bound'] for x in sourcechecks)
cmd=[sys.executable,'.agents/skills/return-of-zero-build/workflow.py','verify-packet','--project-root','.','--packet',str(b/'packet.json')];res=subprocess.run(cmd,capture_output=True,text=True)
if res.returncode:errors.append('packet freshness failed')
report={'status':'passed' if not errors else 'failed','whole':str(p),'whole_sha256':h(p.read_bytes()),'words':len(s.split()),'lines':len(lines),'poems':poems,'headings':heads,'anchors':len(anchors),'links':links,'archive_files':len(archive),'archive_validation':archive,'live_bindings':live,'sources':sourcechecks,'external_witnesses':externalchecks,'coverage_rows':40,'held_dispositions_preserved':True,'packet_validation':{'returncode':res.returncode,'stdout':res.stdout,'stderr':res.stderr},'errors':errors,'scope':'Single-whole draft validation only; no parent E2/T22/consumer/hygiene claim'}
write('final-validation.json',report);print(json.dumps({k:report[k] for k in ['status','whole_sha256','words','lines','anchors','archive_files','coverage_rows','errors']}));assert not errors
