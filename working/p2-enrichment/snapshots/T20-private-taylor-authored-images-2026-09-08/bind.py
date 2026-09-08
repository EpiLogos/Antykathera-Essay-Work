from pathlib import Path
import json,hashlib,re,subprocess,sys,zipfile
b=Path('working/p2-enrichment/snapshots/T20-private-taylor-authored-images-2026-09-08');q=json.loads((b/'queue.json').read_text());r=q['elements'][0];h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
cor=[]
for name,ranges,units,op in [
 ('history-march-to-june-2026.md',[(202,204),(421,455)],['FT-P17','FT-P18'],'Immediate authorial pressure and final revised complete poem; earlier draft not substituted'),
 ('consequence-inconsequential-april-2026.md',[(4,5),(65,65),(326,326),(442,442)],['FT-P19','FT-P20'],'Withheld referent; separate encapsulation; authored context-before-silence revision and derive-not-slot correction'),
 ('infinite-infinitessimal-may-2026.md',[(1,1),(26,26),(42,42),(81,81),(124,124),(180,180)],['FT-P21'],'Complete sentence, static/processual and two full multiplicative/divisional passes, substantive calculus demand'),
 ('what-is-it-to-feel-may-2026.md',[(1,12),(17,17)],['FT-P22'],'Complete poem plus precise self-emotion/feeler/boots correction'),
 ('poem-07-06-2026.md',[(1,len((b/'raw-witnesses/journal/poem-07-06-2026.md').read_text().splitlines()))],['FT-P23'],'Complete final poem and stanza order')]:
 p=b/'raw-witnesses/journal'/name;lines=p.read_text().split('\n')
 for a,z in ranges:
  item={'path':str(p),'start_line':a,'end_line':z,'units':units,'operation':op,'exact_LF_text':'\n'.join(lines[a-1:z]),'sha256':h(p)};cor.append(item)
  # source helper uses Unicode splitlines; preserve LF addresses and exact text in ledger, translate helper range explicitly.
  start=len('\n'.join(lines[:a-1]).splitlines())+1;end=start+len(item['exact_LF_text'].splitlines())-1
  r['source_slices'].append({'path':str(p),'start_line':start,'end_line':end,'relation':op+'; original LF lines '+str(a)+'–'+str(z),'provenance':'Read-only Taylor authorial witness; conversation interlocutor text is not authorial evidence'})
write(b/'authorial-corrections.json',cor)
for p in b.glob('effects*.json'):
 for t in json.loads(p.read_text())['transverse_threads']:r['additional_required_inputs'].append(t['path'])
r['additional_required_inputs']+= [str(b/'authorial-corrections.json'),str(b/'mytheme-inputs.json')]
r['additional_required_inputs']=list(dict.fromkeys(r['additional_required_inputs']))
# Enrich private input record with the same complete target, retain original separately within private input object.
inp=json.loads((b/'mytheme-inputs.json').read_text());inp['inherited_element']=inp['elements'][0];inp['elements']=[{**r,'additional_required_inputs':[p for p in r['additional_required_inputs'] if p!=str(b/'mytheme-inputs.json')]}];write(b/'mytheme-inputs.json',inp)
write(b/'queue.json',q)
for sid in ['abhinavagupta-singh-1988-paratrisika-vivarana']:
 x=subprocess.run([sys.executable,'tools/okf-workspace.py','--project-root','.','effects',sid,'--depth','4','--json'],capture_output=True,text=True);assert x.returncode==0,x.stderr;(b/('effects-'+sid+'.json')).write_text(x.stdout)
p=subprocess.run([sys.executable,'.agents/skills/return-of-zero-build/workflow.py','packet','--project-root','.','--queue',str(b/'queue.json'),'--target',r['record_id'],'--output',str(b/'packet.json')],capture_output=True,text=True);print(p.stdout,p.stderr);assert p.returncode==0
p=subprocess.run([sys.executable,'.agents/skills/return-of-zero-build/workflow.py','verify-packet','--project-root','.','--packet',str(b/'packet.json')],capture_output=True,text=True);write(b/'packet-validation-before-draft-review.json',{'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});print(p.stdout,p.stderr);assert p.returncode==0
packet=json.loads((b/'packet.json').read_text());paths={i['path'] for i in packet['required_inputs']};paths.update(s['path'] for s in packet['slices']);paths.update(s['source'] for s in packet['sources']);paths.update(s['notes'] for s in packet['sources'] if s['notes']);paths.update(x['path'] for x in packet['argument_depth']);
for x in packet['binding']['quilt_hashes']: paths.add(x['path'])
paths.add(q['depth_acceptance'])
# All 36 accepted depth files remain frozen as global acceptance proof, although 27 are assigned.
accept=json.loads(Path(q['depth_acceptance']).read_text());paths.update(x['path'] for x in accept['argument_depth'])
manifest=[]
with zipfile.ZipFile(b/'bound-inputs.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for p in sorted(paths):
  path=Path(p);z.write(path,p);manifest.append({'path':p,'sha256':h(path),'bytes':path.stat().st_size,'archive_member':p,'read_scope':'hash binding and immutable byte preservation; reading standing is specified in reading-receipt.json'})
write(b/'bound-inputs-manifest.json',manifest)
print('archived',len(paths))
