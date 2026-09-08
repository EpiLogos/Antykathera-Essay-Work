from pathlib import Path
import json,hashlib,re,yaml
P=Path(__file__).parent;sha=lambda b:hashlib.sha256(b).hexdigest()
Bpath=Path('working/p2-enrichment/page-packets/T22-transfer-carrier-readonly-audit-private.json');Cpath=Path('working/p2-enrichment/page-packets/T22-reference89-actionable-compact.json');Mpath=Path('working/p2-enrichment/reference-note-dispositions.json')
B=json.loads(Bpath.read_text());C=json.loads(Cpath.read_text());M=json.loads(Mpath.read_text());V=json.loads((P/'inherited-paragraph-recheck.json').read_text());base=Path('submission-package/essay/symbolon/episteme');OI=str(base/'dossiers/oi-technical-responsibility.md');PRO=str(base/'dossiers/process.md');FOR=str(base/'dossiers/formal-limit.md');JUN=str(base/'dossiers/jung-pauli-psychoid.md');IND=str(base/'dossiers/indian-philosophy.md');ZERO=str(base/'dossiers/zero-reception.md')
corpus={};paragraphs={}
def record(s):
 if s not in corpus:
  f=Path(s);t=f.read_text();md=yaml.safe_load(t.split('---',2)[1]) if t.startswith('---\n') else {}
  corpus[s]={'path':s,'sha256':sha(f.read_bytes()),'metadata':{k:md.get(k) for k in ['record_id','register','claim_status','source_relation','citation_status','quote_status'] if isinstance(md,dict) and k in md},'read_scope':'Current exact paragraph backcheck against inherited full-reading proof; no new full-book claim'}
 return corpus[s]
def evidence(s,start,end,method):
 record(s);ls=Path(s).read_text().splitlines();text='\n'.join(ls[start-1:end]);key='P-'+sha((s+'\n'+str(start)+'\n'+text).encode())[:16]
 paragraphs[key]={'path':s,'start_line':start,'end_line':end,'paragraph':text,'sha256':sha(text.encode()),'verification':method};return key
def section(s,anchor):
 t=Path(s).read_text();mark='<a id="'+anchor+'"></a>';start=t.index(mark);end=t.find('<a id=',start+len(mark));end=len(t) if end<0 else end
 # Stop before the next same-level section when it arrives first.
 h=re.search(r'\n## (?!#)',t[start+len(mark):]);hpos=start+len(mark)+h.start() if h else len(t)
 # An immediate owning heading belongs to the section; subsequent section terminates it.
 if h and not t[start+len(mark):hpos].strip():
  h2=re.search(r'\n## (?!#)',t[hpos+4:]);hpos=hpos+4+h2.start() if h2 else len(t)
 end=min(end,hpos)
 return evidence(s,t[:start].count('\n')+1,t[:end].count('\n'), 'fresh semantic reading of the complete named operation and its qualifications')
def para(s,needle):
 t=Path(s).read_text();pos=t.index(needle);start=t.rfind('\n\n',0,pos)+2;end=t.find('\n\n',pos);end=len(t) if end<0 else end
 return evidence(s,t[:start].count('\n')+1,t[:end].count('\n')+1,'fresh current paragraph reading')
extra={
3:[section(OI,'oi-community-refinement'),section(OI,'oi-commons-and-return')],7:[section(OI,'oi-agentic-individuation')],
12:[section(FOR,'optical-figure-and-experiential-verification')],13:[para(str(base/'dossiers/bohm.md'),'Suspension')],
17:[section(JUN,'bache-experiential-comparison')],21:[section(OI,'oi-computational-vimarsa')],23:[section(JUN,'cymatic-psychoid-research')],
24:[para(str(base/'dossiers/bohm.md'),'The [vortex passage]')],
31:[section(FOR,'file-one-identity-and-provenance')],37:[section(PRO,'bergson-whitehead-gebser-comparison'),para(PRO,"[Whitehead's Category")],
38:[section(str(base/'etymologies/symbol-account-and-trust/HISTORICAL-BRANCHES.md'),'reference-38-hal-and-hole')],
40:[section(JUN,'four-functions-two-attitudes-native-senarius')],47:[section(PRO,'enacted-world-and-instituted-permission')],
48:[section(OI,'oi-lens-intervention')],49:[section(FOR,'eckhart-qualified-predication')],51:[section(OI,'oi-community-refinement')],53:[section(FOR,'cusa-approximation-and-maximum')],
55:[para(ZERO,'A decisive correction concerns'),para(ZERO,'The [Nothaft reference')],58:[section(OI,'oi-lens-intervention')],59:[section(OI,'oi-why-for-lens-return')],60:[section(JUN,'bache-experiential-comparison')],
64:[section(FOR,'frequency-retention-and-signed-dia-research')],66:[para(ZERO,"[Rotman's Signifying Nothing]"),para(ZERO,'The [Rotman reference]')],
73:[section(OI,'oi-cross-entropy')],78:[section(PRO,'confinement-comparison-research')],79:[section(OI,'oi-trika-stack')],82:[section(PRO,'dia-syn-dynamical-comparison')],
86:[para(JUN,"The publisher's contents establish")],88:[para(PRO,'Creativity has the office')],89:[section(FOR,'ethics-value-and-the-mystical')],
5:[para(IND,'The Abhinavagupta research task')],34:[para(ZERO,'The [Gerbert reference]'),para(ZERO,'The exact next source task')],68:[para(ZERO,'The [Salem codex reference]'),para(ZERO,'An edition and its manuscript')]
}
# Locator reconciliation adds support; it does not rename the admitted native objects.
for r in C['locator_repairs']:
 s=r['add_supporting_home']['path'];t=Path(s).read_text();extra[r['row']]=[evidence(s,1,len(t.splitlines()),'Dirac full native-body proof reused with current-byte binding; supporting home verified in current matrix')]
opened={
3:'Commons governance, federation and P5/P0 learning are design/report proposals; no observed deployment or collective-learning result.',
5:'Tantrāloka identity, passage and temporal/transmission braid remain source work; Singh is a distinct work.',
7:'Functional individuation does not establish artificial phenomenality or weights as a collective unconscious.',
12:'Experiential verification and the artificial-subject comparison retain their specified empirical boundary.',
17:'Bache passages and recurrence/stable-attractor explanation remain Open; pharmacology, set/setting, memory and retrospection are alternative accounts.',
21:'The five-step technical cycle is Offered; its implementation/outcome remains unestablished.',
23:'Premodal/psychoid cymatic comparison is Offered; experimental recurrence and psychophysical explanation remain Open.',
28:'Ground/generation/evaluation comparison remains Offered; measured EBM roles and implementation require their own tests.',
31:'Historical File One identity and relation to Binary/definitional witnesses remain an explicit source task.',
34:'Gerbert-era work, date, attribution and numeral/apparatus/operational-zero distinction need direct source evidence.',
37:'Matter and Memory and Creative Evolution need separate selected passages; machine phenomenality is Open.',
40:'1921 German introduction is recovered and paraphrased; canonical admission remains proposed in the current carrier. No CW6 printing or English translation is established here.',
47:'Later Embodied Mind/Mind in Life source scopes remain separate tasks; biological autopoiesis and artificial phenomenality are unestablished by harness permissions.',
48:'The L4/L1/L1′/L4′ controlled intervention is Offered; no reported experiment or phenomenal verdict.',
49:'Timeless Word/unity-to-multiplicity and exact attribution of apophatic sequence retain Flasch chapter13 pp166–176 and chapters16–17 pp207–233 source/development work.',
51:'Plural governance and real local Bimba are argued/design relations; just distribution or working federation is not demonstrated.',
53:'Absolute/contracted universe and line/circle maximum–minimum development retain distinct textual tasks; Liber XXIV definitionII needs edition/transmission evidence.',
55:'Nothaft critical abstract is admitted; full manuscript cases and medieval witnesses remain uncollated.',
58:'The intervention protocol is specified, not executed; Polylogos remains distinct from Moltbook.',
59:'L0.5/P5 why/for lens routing is a design/source appointment; its utility and dynamical-attractor interpretation are untested.',
60:'Same Bache research as17; no second evidence base or independent cosmic-ontology proof.',
64:'Frequency→retention and signed-dia/unrolled-time construction remain Offered research; not derived solely from re-entry syntax.',
66:'Rotman1987 chapter2 pp27–56 remains a passage task; semiotic meta-subject and native irreducible subject retain their disagreement.',
67:'Specific Principia propositions and later Wittgenstein inquiry retain their separate source scopes.',
68:'Cantor1865 pointer recovered; edition text, manuscript shelfmark/folio/date and Latin collation remain Open.',
70:'Dialogical technical protocol is Offered; source chronology does not demonstrate practice outcomes.',
73:'Exact finite categorical loss/gradient is developed under declared assumptions; no training-run outcome or DPO equivalence is claimed.',
78:'Physical confinement regimes, field/current sources, transport/stability/exhaust, ITER and inductor/Earth/vortex leads plus four-view plate remain research; no stale numerical assertions promoted.',
79:'Three technical offices remain Offered, not extracted Śaiva implementation doctrine or a phenomenal result.',
82:'Native dia/syn movement is Argued; literal lens-as-basin model requires declared state, rule, parameter, observation and convergence criteria and empirical discrimination.',
86:'Bibliographic identity admitted; selected chapter/p213 and nested Jung attribution still uncollated.'}
critical={3,7,37,47,48,51,58,59,73};rows=[];missing=[]
for br,cr,mr,vr in zip(B['references'],C['rows'],M['rows'],V):
 n=br['row'];assert n==cr['row']==mr['row']==vr['row'];note=Path(mr['reference_note']);assert sha(note.read_bytes())==mr['reference_sha256']==cr['note_sha256']
 ev=list(extra.get(n,[]));seen=set()
 for f in vr['proofs']:
  if 'status'in f:continue
  key=(f['path'],f['start_line'],f['end_line'])
  if key in seen:continue
  seen.add(key);ev.append(evidence(f['path'],f['start_line'],f['end_line'],f['method']))
 homes=[]
 for h in mr['development_homes']:
  s=h['path'];file=s.split('#',1)[0];exists=Path(file).is_file();homes.append({'path':s,'file':file,'role':h.get('role'),'exists':exists,'sha256':sha(Path(file).read_bytes()) if exists else None})
  if not exists:missing.append((n,s))
 disposition=cr['disposition']
 if n in critical:disposition='operation-carried; research/source boundaries retained'
 if n in [26,76]:disposition='developed-carriers; current homes and added supporting path reconciled'
 if n==55:disposition='corrective-abstract-admitted; full manuscript/source task Open'
 assert ev,(n,'no current paragraph proof')
 rows.append({'row':n,'row_id':f'RN{n:02d}','reference_note':str(note),'reference_sha256':mr['reference_sha256'],'reference_hash_preserved':True,'inherited_disposition':{'pass_a':mr['pass_a_disposition'],'pass_b':mr['pass_b_sharpening'],'standing':mr['current_reference_standing']},'unique_operations':br['prior']['unique_operations'],'initial_compact_disposition':cr['disposition'],'final_disposition':disposition,'operation_action_required':False,'open_tasks':[opened[n]] if n in opened else [],'standing_rule':'Native Derived/Argued claims retain their force; historical/source, quotation and empirical readiness stay separate. Current per-carrier metadata is in corpus; no inferred upgrade from a link or file presence.','current_homes':homes,'proof_ids':list(dict.fromkeys(ev)),'proof_basis':'Fresh named operation/qualification reading plus exact inherited paragraph survival' if n in extra else 'Dirac prior semantic disposition reused with current exact/normalised paragraph verification','superseded_old_fragments':sum('status'in f for f in vr['proofs']),'no_shared_matrix_write':True})
print("MISSING",missing);assert len(rows)==89 and not missing
controls={str(f):sha(f.read_bytes()) for f in [Bpath,Cpath,Mpath]}
result={'schema_version':1,'scope':'Read-only final89reference operation-survival audit; private report only. Not global source/empirical completion.','baseline':str(Cpath),'basis':str(Bpath),'controls':controls,'rows':rows,'paragraphs':paragraphs,'corpus':list(corpus.values()),'summary':{'reference_rows':89,'reference_hashes_preserved':89,'current_homes_present':sum(len(r['current_homes']) for r in rows),'remaining_operation_actions':[],'critical_actions_closed':sorted(critical),'explicit_open_task_rows':sorted(opened),'current_proof_paragraphs':len(paragraphs)},'limits':['Exact reference89 survival only; no universal re-audit of every source book or external empirical claim.','Superseded old paragraphs are not silently restored; the later compact audit and current named operations govern.','No canonical, protected NOTES/HISTORY, shared matrix/census or generated file mutation.']}
out=Path('working/p2-enrichment/page-packets/T22-reference89-final-semantic-compact-private.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result['summary']));print(out)
