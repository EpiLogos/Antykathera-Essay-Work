from pathlib import Path
import json,re,hashlib,os
r=Path('.').resolve();d=r/'working/p2-enrichment/snapshots/T22-private-E4-comparative-integration-2026-09-08';E=r/'submission-package/essay/symbolon/episteme/etymologies/symbol-account-and-trust';h=E/'HISTORICAL-BRANCHES.md';w=E/'WHOLE-FIELD.md'
text=h.read_text();whole=w.read_text();ops=['Symbol answers to source','Account does not replace source','Trust keeps the return route active','Account re-enters source-field']
assert len(re.findall(r'^## #',whole,re.M))==6
assert all(whole.count('### '+op)==1 for op in ops)
anchors=['sanskrit-enumeration-and-discriminative-practice','hebrew-spr-counting-writing-and-entrusted-work','chinese-rectification-of-names','arabic-reckoning-and-names','egyptian-rn-reri']
cases=['Sanskrit enumeration','Hebrew SPR','Chinese rectification of names','Arabic reckoning and Names','Egyptian rn']
judgments=[
'Enumerated principles retain four causal descriptions; three means warrant the account; practiced discrimination changes appropriation while inactive purusa and isolating liberation remain source-specific.',
'Counting, telling, scribe and book retain lexical offices; separate roots name believing and reckoning; failed repair changes arrangements and an answer changes a commission, without certifying execution.',
'Names constrain practicable speech and government; unopposed good and bad counsel differ; revisable office is the authorial return, not a modern procedure attributed to the Analects.',
'Reckoning, invocation and enumerative undertaking retain distinct roots and textual carriers; divine judgment is not a human revisable ledger and promised efficacy is not an observed result.',
'Rn identifies name; dated Reri provision makes remembrance available; surviving papyrus, intended afterlife efficacy and present interpretive answerability remain distinct.']
open_debts=[
['Dictionary and constituent print collation','precise ancient date and full reception history','no empirical liberation certification'],
['BDB print/typesetting and qualified etymologies','absolute event/composition dating','execution of narrated commissions and archaeological verification'],
['critical manuscripts/selected Legge print edition','specific Wei accession setting','implementation and dated reception'],
['individual Quranic verse chronology','complete Names list or later recitation technology','devotional/afterlife efficacy'],
['full hieratic spell25 transcription/translation','afterlife efficacy','no full corpus or universal personhood doctrine']]
proposals=[]
for name in ['sanskrit-enumeration','hebrew-spr']:
 p=r/f'working/p2-enrichment/page-packets/T22-E4-{name}-proposal-2026-09-08.json';x=json.loads(p.read_text())
 proposals.extend({'case':name,**c,'proposal_file':str(p.relative_to(r))} for c in x['consumer_proposals'])
ch=json.loads((r/'working/p2-enrichment/receipts/T21-chinese-zhengming/case-proposal.json').read_text())
proposals.extend({'case':'Chinese rectification of names',**c,'proposal_file':'working/p2-enrichment/receipts/T21-chinese-zhengming/CASE-PROPOSAL.md'} for c in ch['consumers'])
for label,ids in [('Arabic',['A15','A23']),('Egyptian',['C21'])]:
 p=r/f'working/p2-enrichment/page-packets/T22-E4-{label}-case-proposal.md';s=p.read_text();part=s.split('## Exact consumer proposal',1)[1].split('## Exact remaining scope',1)[0]
 for id in ids:
  m=re.search(r'\b'+id+r',.*?\n\n(.*?)(?=\n\n(?:A\d|C\d)|\Z)',part,re.S);assert m,id
  base=r/'submission-package/essay/symbolon/episteme'/('arguments' if id.startswith('A') else 'concepts');target=next(base.glob(id+'-*.md'))
  proposals.append({'case':label,'record_id':id,'path':str(target.relative_to(r)),'exact_markdown':m.group(1).strip(),'status':'proposal-only; parent owns reverse','proposal_file':str(p.relative_to(r))})
assert len(proposals)==9
rows=[]
for i,anchor in enumerate(anchors):
 start=text.index(f'<a id="{anchor}"></a>');end=text.index(f'<a id="{anchors[i+1]}"></a>') if i+1<len(anchors) else text.index('The five comparisons give the source-return')
 s=text[start:end];assert all(op in s for op in ops)
 cards=[]
 for url in re.findall(r'\]\(([^)]+SOURCE\.md#[^)]+)\)',s):
  path,anc=url.split('#');p=(h.parent/path).resolve();assert p.exists(),url;body=p.read_text();assert f'id="{anc}"' in body,(p,anc)
  cards.append({'path':str(p.relative_to(r)),'passage_id':anc,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 assert cards
 wp=next(p for p in whole.split('\n\n') if f'HISTORICAL-BRANCHES.md#{anchor}' in p)
 rows.append({'row_id':'E4-comparative:'+anchor,'parent_row_id':'E4-comparative','case':cases[i],'development_status':'developed-source-specific-comparison; E4 integration complete','claim_standing':'historical/lexical attributed scope register2; authorial operational homology register3; no shared descent or empirical implementation claim','disposition':judgments[i],'occurrences':[{'path':str(h.relative_to(r)),'start_line':text[:start].count('\n')+1,'end_line':text[:end].count('\n'),'section':anchor,'operation':ops},{'path':str(w.relative_to(r)),'start_line':whole[:whole.index(wp)].count('\n')+1,'end_line':whole[:whole.index(wp)+len(wp)].count('\n')+1,'section':'Account does not replace source' if i<2 else 'Opening and integrity','operation':judgments[i]}],'source_passages':cards,'source_houses':sorted(set(c['path'] for c in cards)),'remaining_source_research':open_debts[i],'consumer_reverse_status':'separate nine-proposal list; no A/C/Movement writes by integrator'})
assert sum(len(x['source_passages']) for x in rows)==22
before=json.loads((d/'before-manifest.json').read_text());pres=[]
for row in before[:2]:
 old=(r/row['snapshot']).read_text();new=(r/row['path']).read_text();pat=r'\]\(([^\s)]+)'
 dest=lambda s:set(re.findall(pat,s));lost=[u for u in dest(old)-dest(new) if not u.startswith('https://')];assert not lost
 cp=[p for p in old.split('\n\n') if any(t in p for t in ['/dossiers/','/histories/','/lenses/'])];assert all(p in new for p in cp)
 pres.append({'path':row['path'],'prior_carrier_paragraphs_byte_preserved':len(cp),'lost_canonical_destinations':lost})
hist=next(x for x in before if x['path'].endswith('/HISTORY.md'));assert hashlib.sha256((r/hist['path']).read_bytes()).hexdigest()==hist['sha256']
for id in ['C33','C43','C49']:
 assert re.search(r'\]\(../../concepts/'+id+'-',whole),id
# Verify the other owner's admitted sources stayed unchanged since their complete read.
reads=json.loads((d/'received-source-reads.json').read_text());changed=[]
for row in reads:
 if hashlib.sha256((r/row['path']).read_bytes()).hexdigest()!=row['sha256']:changed.append(row['path'])
report={'status':'final semantic and preservation validation complete; scoped T22 report bound separately','rows':rows,'consumer_proposals':proposals,'counts':{'comparison_cases':5,'case_source_cards':22,'case_source_houses':11,'own_new_foldback_cards':8,'existing_account_card_reused':1,'case_consumer_proposals':9,'case_unique_consumers':len(set(x['path'] for x in proposals)),'inherited_concept_forward_repairs':3,'native_terms':3,'native_operations':4,'development_positions':6},'preservation':pres,'protected_HISTORY_unchanged':hist,'received_sources_changed_since_read':changed,'own_mutation_scope':'E4WHOLE/HISTORICAL,LSJ,MW,newBankSOURCE and privateproofs only; no index/sharedcoverage/consumer/generated/NOTES writes','shared_63_pair_scope':'All pre-existing E4 carrier paragraphs and destinations retained; other five E fields and every consumer body left untouched. Prior63 pair proof remains separate; no blanket recertification of concurrently edited carriers.','remaining_actions':'Parent owns nine consumer proposal decisions/integration, shared272 row update, aggregate source projections and commit grant.'}
(d/'final-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps(report['counts']));print('source changed after read',changed)
