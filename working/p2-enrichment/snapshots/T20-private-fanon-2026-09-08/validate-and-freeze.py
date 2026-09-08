import hashlib,json,re,subprocess,zipfile
from pathlib import Path
from urllib.parse import unquote
import yaml
root=Path.cwd();b=Path('working/p2-enrichment/snapshots/T20-private-fanon-2026-09-08');w=Path('submission-package/essay/symbolon/mytheme/worlds/francophone-anticolonial/fanon-language-gaze-mask-recognition/WHOLE.md')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,v): (b/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
p=json.loads((b/'packet.json').read_text());s=w.read_text();lines=s.splitlines();fail=[]
meta=yaml.safe_load(s.split('---',2)[1]);assert meta['record_id']==p['target']['record_id'];assert meta['claim_status']=='Argued'
heads=re.findall(r'^## (#(?:[0-4]|5→0)) — .+$',s,re.M);assert heads==['#0','#1','#2','#3','#4','#5→0']
anchors=re.findall(r'<a id="([^"]+)"',s);assert len(set(anchors))==len(anchors)
def slug(t):return re.sub(r'[^\w\- ]','',t.lower()).replace(' ','-')
links=[]
for label,url in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',s):
 if url.startswith('https:'):continue
 part,_,anchor=unquote(url).partition('#');dest=(w.parent/part).resolve() if part else w.resolve();okay=dest.exists()
 if okay and anchor:
  text=dest.read_text();ids=re.findall(r'<a id="([^"]+)"',text)+[slug(h) for h in re.findall(r'^#{1,6} (.+)$',text,re.M)];okay=anchor in ids
 links.append({'path':str(dest.relative_to(root)),'anchor':anchor,'resolved':okay})
 if not okay:fail.append('unresolved link '+url)
for field in ['Mask as adaptive interface','Category before encounter','Objective Co-Internality','Idol/image']:
 assert f'**{field} — human-amplified: no.**' in s
assert not re.search(r'human-amplified:\s*yes',s,re.I)
units=[('colonial-language-status','fanon-language'),('antillean-speaker','fanon-whole'),('metropolitan-french','fanon-language'),('white-gaze','fanon-racial-hail'),('lived-black-body','fanon-racial-hail'),('historico-racial-schema','fanon-racial-hail'),('epidermal-racial-schema','fanon-racial-hail'),('imposed-mask','fanon-mask'),('recognition-field','fanon-recognition')]
positions={a:next(i+1 for i,l in enumerate(lines) if f'id="{a}"' in l) for a in anchors};starts=[positions[a] for a in ['fanon-whole','fanon-language','fanon-racial-hail','fanon-mask','fanon-recognition','fanon-return']]+[len(lines)+1]
row=json.loads((b/'coverage-rows.json').read_text())['rows'][0];row['development_status']='developed-draft-audited-awaiting-parent-T22';row['occurrences']=[{'path':str(w),'start_line':1,'end_line':len(lines),'section':'whole sixfold','operation':row['authored_operation']}];row['semantic_subunits']=[{'unit_key':unit,'standing':'inherited subordinate figure; not a new record','occurrences':[{'path':str(w),'start_line':positions[a],'end_line':min(x for x in starts if x>positions[a])-1,'section':a,'operation':unit.replace('-',' ')}]} for unit,a in units];row['source_debt_current']=['Canonical Fanon SOURCE absent: parent owns source installation.','English edition/translation not selected or collated.','Chapters II/III gendered and sexual argument require their own complete source treatment before expansion.'];save('unit-crosswalk.json',{'rows':[row],'standing':'Private final backcheck only; shared census unchanged.'})
paths=set(i['path'] for i in p['required_inputs'])|set(i['path'] for i in p['argument_depth'])|set(p['binding']['quilt_hashes'])
paths|={p['binding'][k] for k in ['queue','census','depth_acceptance']}
for x in p['sources']:
 paths.add(x['source'])
 if x.get('notes'):paths.add(x['notes'])
paths|={'.wayfinder/maps/p2-enrichment-handoff.md','.wayfinder/maps/t20-t21-world-registers.md','AGENTS.md','docs/REPOSITORY-SHAPE.md','the-return-of-zero-central-plan.md','return-of-zero-orienting-principles.md','WRITING-PROTOCOL.md'}
paths|={str(x) for x in Path('working/p2-enrichment/argument-depth').glob('A[0-9][0-9].md')}
paths.discard(str(w));missing=[x for x in paths if not Path(x).is_file()];assert not missing,missing
oldzip=zipfile.ZipFile('working/p2-enrichment/snapshots/T20-private-taylor-authored-images-2026-09-08/bound-inputs.zip');oldnames=set(oldzip.namelist());manifest=[];reuse=[]
with zipfile.ZipFile(b/'bound-inputs.zip','w',zipfile.ZIP_DEFLATED) as z:
 for path in sorted(paths):
  h=sha(path);z.write(path,path);manifest.append({'path':path,'sha256':h,'bytes':Path(path).stat().st_size})
  if path in oldnames:
   oldhash=hashlib.sha256(oldzip.read(path)).hexdigest();reuse.append({'path':path,'previous_sha256':oldhash,'current_sha256':h,'unchanged':h==oldhash})
save('bound-inputs-manifest.json',{'files':manifest,'scope':'Frozen evidence; includes current consumer bytes for parent, not a claim to have read their concurrent changes.'})
with zipfile.ZipFile(b/'bound-inputs.zip') as z:
 assert z.testzip() is None
 for item in manifest:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
for item in p['required_inputs']+p['argument_depth']:
 if sha(item['path'])!=item['sha256']:fail.append('input drift '+item['path'])
source=json.loads((b/'source-recovery.json').read_text());save('reading-receipt.json',{'prior_reading_receipt':'working/p2-enrichment/snapshots/T20-private-taylor-authored-images-2026-09-08/reading-receipt.json','reuse_hash_comparisons':reuse,'reuse_policy':'Prior complete readings reused only where hashes agree; this list establishes byte continuity, not new semantic reading. Native eight/four supports, accepted A-depth and prior whole corpus readings carry forward.','fresh_reading':['Existing Fanon whole in WHOLE-before.md: complete.','Corrected map lines1–120; rest previous corpus reading.','Native020 MYTHEME-AND-DEEP-SOURCE-SEAMS.md lines495–535, with packet context475–532; full earlier corpus reading reused.','Primary French PDF ranges listed in source-recovery.json, each entire selected chapter.'],'source_recovery':source,'concurrent_inputs':json.loads((b/'concurrent-input-drift.json').read_text()),'protected_notes':'No Fanon house or NOTES found; core SOURCE sibling NOTES absent; no protected mutation.','effects':'Core source, A20, A27 and canonical whole path effects completed. Record-ID lookup failed; path resolution succeeded. Full declared transverse threads retained in required inputs.'})
save('semantic-audit-final.json',{'result':'pass: bounded whole draft ready for parent T22','whole_sha256':sha(w),'repairs':['F1 restored named objective-internal project comparison without attributing terminology to Fanon.','F2 restored inherited chameleon/comparison/return anchors.'],'gates':{'G1':'Inherited source whole and primary material distinguished from project comparisons; canonical source debt explicit.','G2':'Antillean speaker, metropolitan measure, racial hail, embodied person and recognising other retain distinct offices.','G3':'Language access→alien measure→racial hail/body schema→mask self-administration→recognition revision sequence preserved.','G4':'No resolved ending invented; ChapterV aftermath and conclusion material conditions qualify the return.','G5':'Fanon historical world, native QL, Neumann morphology, persona, chameleon and technical mirror remain distinct.','G6':'No eight-stage equation or generic sixfold glossary; section movements follow the owning field.','G7':'Qualifications correspond to actual inherited no flags, source absence, chapter scope and unequal history.','G8':'Sixfold moves from inherited colonial world through speech/body/mask/recognition to revisable encounter.','G9':'Nine named inherited figures, four no-comparisons and four cross-whole candidates retained; no new whole identity.','G10':'Connected explanatory prose, source locators, no invented quotations or fictional continuous plot.'}})
result=subprocess.run(['python3','.agents/skills/return-of-zero-build/workflow.py','verify-packet','--project-root','.','--packet',str(b/'packet.json')],capture_output=True,text=True)
if result.returncode:fail.append('verify-packet failed')
validation={'status':'pass' if not fail else 'fail','failures':fail,'whole_sha256':sha(w),'words':len(s.split()),'lines':len(lines),'sixfold':heads,'unique_explicit_anchors':len(anchors),'local_links':links,'semantic_subunits':len(units),'inherited_four_no_flags':'preserved','archive_files':len(manifest),'archive_integrity':'pass','reuse_unchanged':sum(x['unchanged'] for x in reuse),'reuse_changed':[x['path'] for x in reuse if not x['unchanged']],'workflow_returncode':result.returncode,'workflow_output':result.stdout+result.stderr,'scope':'Single-whole draft validation. Parent owns consumer review, source installation and aggregate T22.'};save('final-validation.json',validation);print(json.dumps(validation,indent=2));assert not fail
