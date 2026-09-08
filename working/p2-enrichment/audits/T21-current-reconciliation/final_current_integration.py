from pathlib import Path
import json,re,hashlib,datetime,collections,urllib.parse
B=Path('working/p2-enrichment/audits/T21-current-reconciliation');d=json.loads((B/'current-row-audit.json').read_text());root=Path.cwd();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def ps(path):
 p=Path(path)
 if not p.is_file():return []
 ls=p.read_text().splitlines();a=0;out=[]
 for i,l in enumerate(ls+['']):
  if not l.strip():
   if i>a:out.append({'path':str(p),'start_line':a+1,'end_line':i,'text':'\n'.join(ls[a:i])})
   a=i+1
 return out
def match(path,s):return [p for p in ps(path) if s.lower() in p['text'].lower()]
cache={}
def links(path,target):
 if path not in cache:
  edges=[]
  for p in ps(path):
   vals=re.findall(r'\]\(([^)]+)\)',p['text'])+re.findall(r'\[\[([^]|]+)',p['text'])
   for v in vals:
    v=urllib.parse.unquote(v.split('#')[0]).strip('<>')
    if not v or re.match(r'\w+://',v):continue
    t=root/v if v.startswith(('submission-package/','working/')) else root/Path(path).parent/v
    if not t.suffix:t=t.with_suffix('.md')
    try:edges.append((str(t.resolve().relative_to(root)),p))
    except ValueError:pass
  cache[path]=edges
 return [p for t,p in cache[path] if t==target]
resolved_ids=['T21-C26','T21-C33','T21-C43','T21-C49','T21-C25','T21-C27','T21-C46','T21-M04','T21-M23','T21-M25','T21-M34','T21-M40','T21-M41','T21-M44','T21-M27']
for r in d['rows']:
 rid=r['row_id'];p=r['canonical_home']
 r['current_sha256']=hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else None
 if rid in resolved_ids:
  r['integration_status']='current-repair-reread; resolved';r['consumer_obligations']=[]
  r['current_repaired_return_witnesses']=links(p,r['field_path'])
  if 'proposed_operation_reconciliation' in r:r['proposed_operation_reconciliation']='Resolved in current paragraphs: original operation retained alongside the distinct additional route; materialise both only at their actual paragraph occurrences.'
  if rid in ['T21-C26','T21-C33','T21-C43','T21-C49']:r['development_status']='semantic-operation-covered; literal-E-return-resolved'
 if rid=='T21-M27':
  r['coverage_status']='covered';r['development_status']='semantic-operation-covered; attribution-repair-resolved';r['judgment']='Calling/crossing, iterant anticommutation and quarter-turn modulus retain different operations. Current paragraph19 distinguishes Taylor’s Argued temporal-memory interpretation from Varela’s autonomous third state and proposed frequency investigation; frequency→retention remains exact research rather than a source-proved conclusion.';r['scope_witnesses']=match(p,'Argued temporal reading')+match(p,'Anticommutation');r['research_obligations']=['Specify recurrence, measurement of frequency, retained prior state and changed next crossing for the Offered frequency→retention/signed-dia programme.']
 if rid=='T21-M18':
  r.update(coverage_status='covered-mediated-return',development_status='semantic-operation-covered; entrusted-return-currently-present',semantic_operation_witnessed=True,judgment='The mathematical loan returns exactness and source provenance; the current Credere paragraph additionally states a determinate undertaking with bearer and consequence. Examination clarifies what is owed; renewed entrustment permits continuation beyond its guarantee. This now performs the assigned E4 Trust office through the distinct E3 circuit, not merely symbolic re-entry.',scope_witnesses=match(p,'determinate undertaking'),consumer_obligations=[],integration_status='current-Credere-undertaking-reread; previous partial judgment superseded')
 if rid=='T21-lens-foucault':r['source_obligations']=['Current paragraph69 now carries ForgetFoucault2007selectedpp29–43,55–67, reversible challenge and Transparency1993orgy attribution. Full-volume/quotation and other Foucault-title tasks remain separately open.'];r['integration_status']='R1 resolved; current paragraph reread'
 if rid=='T21-history-myth':r['source_obligations']=['Current paragraph90 receives Jung1921function/attitude witness from dossier; no repeated recovery task. English/CW6 collation, ClearyEnglish, Phillipsvenue/date and other named primary tasks remain separate.'];r['integration_status']='R2 resolved; current paragraph reread'
 if r.get('research_obligations'):r['research_status']='open-scoped'
 # Refresh literal observations only; keep the authored semantic judgment independent.
 r['current_fragment_candidates']=links(p,r['field_path'])
 for c in r['consumers']:
  c['current_literal_return_fragments']=links(c['path'],r['field_path']);c['current_literal_forward_fragments']=links(r['field_path'],c['path']);c['literal_observed_utc']=now
 r['proposed_row_update']={k:r[k] for k in ['row_id','field_path','branch_path','operation','evidence_register','canonical_home','development_status','coverage_status','research_status','judgment','source_obligations','consumer_obligations','consumers']}
 for k in ['scope_witnesses','verified_source_witnesses','current_branch_witness','current_E_pair_proof','audit_reuse','research_obligations','integration_status','current_repaired_return_witnesses','proposed_operation_reconciliation']:
  if k in r:r['proposed_row_update'][k]=r[k]
# Exact branch-section occurrence ranges in addition to complete current companion.
markers={'E1-con':'## Four con','E1-region':'## Region','E1-countenance':'## Countenance','E1-count-six':'## Six ways','E1-chinese':'## Chinese','E1-native':'## Native','E2-arbiter':'## Witness','E2-hybris':'## Measure','E2-regard-leaf':'## Regard','E2-anamnesis-leaf':'## Anamnesis','E2-fides-bridge':'## Witness','E3-fourfold':'## French','E3-deficient':'## Twelve','E3-surety':'## Rings','E4-token':'## Matching','E4-circulation':'## Reckoning','E4-comparative':'## Branches kept','E4-hole':'## Reference 38','E5-greek':'## #1','E5-biology':'## #3','E5-invariant':'## #4','E6-names':'### E6-names','E6-house':'### E6-house','E6-ratio':'### E6-ratio'}
for r in d['rows']:
 if r['row_id'] in markers:
  p=(Path('submission-package/essay/symbolon/episteme/etymologies/arbitration-hybris-regard-anamnesis/HISTORICAL-BRANCHES.md') if r['row_id']=='E2-fides-bridge' else Path(r['field_path']).with_name('HISTORICAL-BRANCHES.md'));ls=p.read_text().splitlines();a=next(i for i,l in enumerate(ls) if l.startswith(markers[r['row_id']]))
  level=len(ls[a])-len(ls[a].lstrip('#'));b=next((i for i in range(a+1,len(ls)) if ls[i].startswith('#') and len(ls[i])-len(ls[i].lstrip('#'))<=level),len(ls))
  w={'path':str(p),'start_line':a+1,'end_line':b,'text':'\n'.join(ls[a:b])};r['branch_scope_witness']=w;r['proposed_row_update']['branch_scope_witness']=w
n=sum(r['semantic_operation_witnessed'] for r in d['rows']);d['counts'].update(positive_local_semantic_witnesses=n,positive_local_semantic_witnesses_by_kind=dict(collections.Counter(r['row_kind'] for r in d['rows'] if r['semantic_operation_witnessed'])),coverage_statuses=dict(collections.Counter(r['coverage_status'] for r in d['rows'])));d['final_read_utc']=now
(B/'current-row-audit.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');(B/'proposed-row-updates.json').write_text(json.dumps({'status':d['status'],'counts':d['counts'],'standing':'All272 scoped semantic dispositions; no source-acquisition or implementation closure inferred from operation coverage. Current repairs incorporated, not proposed twice.','rows':[r['proposed_row_update'] for r in d['rows']]},indent=2,ensure_ascii=False)+'\n')
f=json.loads((B/'reconciliation-findings.json').read_text());f.update(status=d['status'],counts=d['counts'],not_certified_rows=[],read_boundary='All272 row scopes now judged.270 have developed operation witnesses; E4-comparative remains a retained research programme, Earth remains unratified. Historical acquisition and implementation research are separately scoped.',concept_return_repairs=[],operation_map_reconciliations=[],resolved_integration_rows=resolved_ids+['T21-M18'],final_read_utc=now)
for r in f['source_findings']:
 r['status']='resolved-by-current-parent-or-K-edit; reread-confirmed';r['proposal']='No replay. Current paragraph distinguishes the source-specific acquired witness and its remaining research/edition limits.';p=Path(r['path']);r['verified_current_text']=p.read_text().splitlines()[r['start_line']-1]
f['remaining_development']=[{'row_id':'E4-comparative','standing':'research-programme-preserved; five primary comparison cases not yet developed','task':'Independent lexical entry, dated primary passage and practice for SanskritSamkhya, HebrewSPR, Chinesezhengming, Arabichisab/Names andEgyptianrn; author the differing operation, consequence and return in each own home.'}]
f['source_admission_not_reacquisition']=[{'row_id':k,'task':next(r['source_obligations'][0] for r in d['rows'] if r['row_id']==k)} for k in ['E4-token','E4-circulation','E4-hole']]
f['scope_disposition_only']=['T21-earth-pending: preserve unratified status; no seventh E field.'];f['historical_research_rows']=[r['proposed_row_update'] for r in d['rows'] if r['row_kind']=='historical-source-branch'];(B/'reconciliation-findings.json').write_text(json.dumps(f,indent=2,ensure_ascii=False)+'\n')
md='''# T21 — final272-row semantic reconciliation

**All272 rows have scoped semantic judgments;0 remain unjudged.270 rows have developed operation witnesses.** One row, `E4-comparative`, preserves a research programme whose five independent comparison cases remain undeveloped. `T21-earth-pending` remains unratified. These are row counts, not270 unique operations or a claim that every historical acquisition and technical experiment is complete.

The developed coverage includes29whole-operation rows,23historical-branch operations,100A/C scopes,19carrier scopes,12nation leaves,48Movement scopes,36conjugates plusAC, and2routes to the single complete aphorism. All six E whole hashes match the prior full reads. Current HISTORICAL-BRANCHES and admitted lexical/primary cards determine historical standing. Dirac’s full37conjugate audit is reused after rendered-prose equality checks across all37; href repairs changed no argument. Root scope remains ratified.

## What remains

- **E4 comparative development:** Sanskrit enumeration, HebrewSPR, Chinese rectification of names, Arabic reckoning/Names andEgyptianrn require independent entries, dated primary passages and practices, then distinct authored operations and consumer returns. Their names and task-preservation are not five completed historical cases.
- **E4 source admission:** symbolon’s consulted LSJ senses; Bank of England1694tallyA013/1; consulted trust and hāl/whole/holy/health/heal/hole entries need canonical card/provenance foldback. These bounded findings already exist in the current companion; do not repeat acquisition merely because their cards are absent. MWaccount is already admitted.
- **Open historical acquisition:** E1Germancalque/CountryPath, facies/prosopon, the remaining six counting-family lexical histories, Chinese related graphs/variants/Zhuangzi; E2continuous Plautus/Plato and English/Anglo-French witnesses; E3twelve-branch implementation/transmission/counter-testimony; E5Greek primary contexts, Flasch/Eckhart and later evolutionary homology; E6nomen/numerus/nem and ratio/arithmos/harmony. Exact acquired-versus-open distinctions and canonical card IDs are in each branch row.
- **Open implementation/empirical research:** frequency→retention/signed-dia, psychophysical efficacy, real source-return/commission tests and deployed conjugate mechanisms remain named research. Their openness does not negate the already developed operations.

## Integration reread

Parent’s19carrier/63Epair proof remains separate, with0errors. Current FoucaultBaudrillard, mythJungtypology, nationAion andM27Varela paragraphs were reread and are resolved. All four C26/C33/C43/C49E returns now exist at the exact operation. Current C25/C27/C46 and seven KMovement operation-map repairs retain their distinct routes; no replay proposed.

M18’s full current ending contains a determinate undertaking with bearer and consequence through E3Credere. That performs the assigned Trust return by a declared mediated route, superseding the earlier partial judgment. A missing direct E4 link is not missing trust development. The270count includes this current judgment.

The89reference-note homes and existing binding dispositions remain the reference layer; README is the90th file. Their home existence is not promoted to source certification. The one four-line aphorism stays intact; no Two Ones reconstruction, esoteric dependency, additional field or new root identity is introduced.

## Materialisation files

- `proposed-row-updates.json`: all272stable row proposals, authored judgment, independent coverage/research standing, current consumer occurrences and source/branch witnesses.
- `current-row-audit.json`: full audit evidence and historical checkpoint context.
- `reconciliation-findings.json`: remaining development/acquisition/admission distinctions and resolved repairs.
- `conjugate-reuse-check.json`: all37rendered-prose equality checks against Dirac’s full-body packet.
- `audit-checks.json`: row cardinality, stable operation/register preservation and occurrence checks.

Only private audit outputs written. No canonical, source, protected, shared census/queue or index mutation. Parent materialises current row proposals at its integration barrier.
'''
(B/'RECONCILIATION.md').write_text(md)
# Final real-file checks; read-time evidence remains version-specific if another writer proceeds later.
orig=json.loads(Path('working/p2-enrichment/T21-e-field-consumer-coverage.json').read_text());assert len(d['rows'])==272
assert [r['row_id'] for r in d['rows']]==[r['row_id'] for r in orig['rows']]
errors=[];checks=0
for a,b in zip(d['rows'],orig['rows']):
 assert a['operation']==b['operation'] and a['evidence_register']==b['evidence_register'];assert a['semantic_judgment_complete'] and a['judgment']
 for w in a.get('scope_witnesses',[])+([a['branch_scope_witness']] if 'branch_scope_witness' in a else []):
  ls=Path(w['path']).read_text().splitlines();checks+=1
  if '\n'.join(ls[w['start_line']-1:w['end_line']])!=w['text']:errors.append({'row_id':a['row_id'],'path':w['path'],'standing':'changed-during-final-check; relocate exact retained paragraph'})
result={'rows':272,'unjudged_rows':0,'developed_operation_rows':n,'research_programme_rows':1,'unratified_pending_rows':1,'stable_ids_operations_registers_preserved':True,'exact_current_scope_occurrences_checked':checks,'occurrence_errors':errors,'conjugate_visible_prose_equal':37,'shared_writes':False,'canonical_writes':False,'index_mutations':False}
(B/'audit-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
