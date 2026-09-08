from pathlib import Path
import json,hashlib,re,zipfile,os
root=Path.cwd();o=root/'working/p2-enrichment/snapshots/T21-private-oi-technical-responsibility-2026-09-08';d=root/'submission-package/essay/symbolon/episteme/dossiers/oi-technical-responsibility.md'; rel=str(d.relative_to(root))
# Exact consumer proposals: authorial obligations, no claim these reciprocal links were installed.
ops={
'A14':('oi-six-responsibility-centres','Separate compositional formal structure, product responsibility and actual executed transition; no product count supplies a native proof.'),
'A21':('oi-agentic-individuation','Return model potential, active-context nucleation, laminated persona and trans-individuation to differentiated formation; trace changed conditions rather than persona consistency.'),
'A26':('oi-inherited-relation','Inspect sources, permissions, evaluators and material supports as conditions of a constituted act; retain world/model and phenomenal question distinctions.'),
'A28':('oi-source-and-commission','Return evidence to intention/formulated commission and distinguish training, institution and runtime delegation; prompt remains 1.'),
'A29':('oi-commons-and-return','Make cost, refusal, revision, exit/reconnection and rule-changing standing reach the authority receiving the product.'),
'A30':('oi-source-projection-contribution-route','Retain independent source worlds through Projection, Contribution and Encounter without a super-subject or universal graph.'),
'A31':('oi-computational-vimarsa','Require encountered difference to change criterion, permission, frame or commission, including refusal; no sycophantic simulation of return.'),
'A32':('oi-computational-vimarsa','Carry three motions and instrument-initiated return; local Bimba can genuinely be original while wider Pratibimba; causal initiative does not confer ontological priority.'),
'A33':('oi-evidence-standing','Distinguish six current constructor checks from Offered six-vector experiments and complete source-acceptance workflow.'),
'C34':('oi-agentic-individuation','Distinguish functional agentic formation from psychic individuation and persona hardening.'),
'C38':('oi-source-projection-contribution-route','Preserve recursive real local original and its wider source dependence; return can revise Bimba itself.'),
'C39':('oi-six-responsibility-centres','Keep lens/refraction office separate from source, reference original, product namespace and capability-target projection.'),
'C40':('oi-source-and-commission','Locate actual operative source, evaluator, memory, permission and infrastructure rather than an output-only self-story.'),
'C42':('oi-source-projection-contribution-route','Retain independently grounded worlds and attributable mutual conditioning; Encounter does not certify understanding.'),
'C43':('oi-computational-vimarsa','Retain selected/excluded field, prompt/source/lens/evaluator, counter-reading, limit and revised determination with provenance; no luminous-awareness claim.'),
'C44':('oi-source-and-commission','Distinguish availability, disclosure and authority in a horizon whose commission is already determinate.'),
'C45':('oi-evidence-standing','Promote only the six bounded local behaviours actually exercised; retain hypotheses and null outcomes for unexecuted research.'),
'C53':('oi-commons-and-return','Return product and sustaining labour/cost to commissioning power, with an effective revising office.'),
'C54':('oi-commons-and-return','Compare Ostrom and the17-page4:2 design with rule change, recourse and exit; do not assert successful commons deployment.'),
'C55':('oi-computational-vimarsa','Preserve exteriorisation, image-as-human-measure, initiating return; Bratton talking mirror is a distinct witness.')}
proposals=[]
for ident,(anchor,operation) in ops.items():
 folder='arguments' if ident.startswith('A') else 'concepts';p=next((root/'submission-package/essay/symbolon/episteme'/folder).glob(ident+'-*.md'))
 proposals.append({'target':str(p.relative_to(root)),'record_id':ident,'relation':'returns-to','dossier_anchor':rel+'#'+anchor,'operation':operation,'standing':'proposal only; no consumer mutation'})
E={
'encounter-region-name-count':('oi-source-projection-contribution-route','Counted participant can answer beyond attributed profile; selective mediation retains source, bearer and absence.'),
'arbitration-hybris-regard-anamnesis':('oi-source-and-commission','Crisis/Decision-Hybris, Con-text/Diaphaneity-Regard and Resolution/Reconciliation-Anamnesis make the criterion revisable while retaining its decision.'),
'trust-place-logos-nomos-natio-credere':('oi-source-and-commission','Fides/Topos/Logos/Nomos/Natio/Credere retain prior reliance, situation, articulated account, executable office, inherited belonging and renewed undertaking.'),
'symbol-account-and-trust':('oi-commons-and-return','All four operations: Symbol answers to source; Account does not replace source; Trust keeps return active; Account re-enters source-field.'),
'homology-and-analogy':('oi-agentic-individuation','Native derivation, psychic/Śaiva witnesses, software correspondence and implementation evidence keep stated respects and distinct warrants.'),
'apportionment-and-economy':('oi-commons-and-return','Five power/apportionment/labour/commons/planetary-economy operations plus four Name/Power consequences: expenditure, course, affected other, result/cost/correction rights.')}
for folder,(anchor,operation) in E.items():
 proposals.append({'target':'submission-package/essay/symbolon/episteme/etymologies/'+folder+'/WHOLE-FIELD.md','relation':'returns-to','evidence_register':3,'dossier_anchor':rel+'#'+anchor,'operation':operation,'standing':'proposal only; existing lexical/HISTORY/HISTORICAL-BRANCHES untouched'})
(o/'consumer-return-proposals.json').write_text(json.dumps(proposals,indent=2,ensure_ascii=False)+'\n')
mops={1:'Question before mechanism; instrument does not supply the Subject.',12:'Operative internality as constituted field rather than model-only interior.',20:'Keep selected source and excluded relation through the cut.',21:'Gathering retains source seam and effective return.',22:'Capture/account does not perform entrusted release; no legal or deployment inference from myth.',23:'Symbolic response alters interpreter and interpretive field; dynamic model remains a distinct register.',32:'Formation becomes transparent to conditions rather than a hardened persona; native X/x belongs to Taylor.',33:'Native4+2 derivation remains distinct from six product centres and product144-face accounting.',35:'A perspective can receive returned difference at its criterion; no total surveillance completion.',36:'MEF mediation and prompt-as-determination retain sourced horizon and scope.',37:'Numerical, linguistic and actionable conditions remain inspectable together.',38:'Retained alternatives and selection conditions distinguish return from winner-only report.',39:'J-space records commission, affordances, uncertainty and authority separately.',40:'Gauge, labour and cost reach the office able to revise the criterion.',41:'Local Bimba really occupies original office; wider dependence and downstream revision both survive.',42:'Compare six Offered vectors under baselines, ablations and null outcomes; six constructor checks do not execute these experiments.',43:'Instrument returns to origins, exclusions and affected worlds through consequential conduct.',44:'Source/Projection/Contribution/KnowledgeRoute, QL/MEF/Bimba/harness retain different offices.',45:'Finite attunement instrument retains observer, source and material conditions; does not become its ground.',46:'Commons rule change, recourse, refusal, exit and reconnection retain locally governed worlds.',47:'Positive Argued ontological order remains separate from Offered technical horizon and Open phenomenal localisation.',48:'Return achieved determination to source/alterity/consequence without a super-subject or erasing its work.'}
ms=[]
for n,op in mops.items():
 p=next((root/'submission-package/essay/section-rooms').glob('*/movements/'+str(n).zfill(2)+'-*.md'))
 ms.append({'target':str(p.relative_to(root)),'movement':'M'+str(n).zfill(2),'relation':'returns-to','dossier_anchor':rel+'#oi-commons-and-return','operation':op,'standing':'proposal only; Movement unchanged'})
(o/'movement-return-proposals.json').write_text(json.dumps(ms,indent=2,ensure_ascii=False)+'\n')
text=d.read_text();bad=[];links=[]
for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text):
 if target.startswith(('http:','https:')):continue
 path,sep,anchor=target.partition('#');a=(d.parent/path).resolve();b=(root/path).resolve();f=a if a.exists() else b
 if not f.exists():bad.append({'link':target,'error':'missing path'});continue
 if sep and f.suffix=='.md':
  t=f.read_text();ids=re.findall(r'<a id="([^"]+)"',t)
  for h in re.findall(r'^#{1,6} (.+)$',t,re.M):
   ids.append(re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-'))
  if anchor not in ids:bad.append({'link':target,'error':'missing anchor'})
 links.append(target)
packet=json.loads((o/'packet.json').read_text());changed=[];protected=[]
for r in packet['inputs']:
 p=Path(r['path']);p=p if p.is_absolute() else root/p
 if hashlib.sha256(p.read_bytes()).hexdigest()!=r['sha256']:changed.append(r['path'])
 if p.name=='NOTES.md':protected.append({'path':r['path'],'sha256':r['sha256'],'unchanged':r['path'] not in changed})
validation={'record_id':'dossier-oi-technical-responsibility','sha256':hashlib.sha256(d.read_bytes()).hexdigest(),'words':len(text.split()),'six_positions':re.findall(r'^## (#\S+)',text,re.M),'explicit_anchors':re.findall(r'<a id="([^"]+)"',text),'checked_local_links':len(links),'link_errors':bad,'inputs':len(packet['inputs']),'input_hash_deltas_after_freeze':changed,'protected_notes':protected,'reference_rows':[3,7,21,79],'consumer_proposals':len(proposals),'movement_proposals':len(ms),'source_or_consumer_writes':False}
(o/'validation.json').write_text(json.dumps(validation,indent=2,ensure_ascii=False)+'\n');(o/'DOSSIER-final.md').write_bytes(d.read_bytes());print(json.dumps(validation,indent=2,ensure_ascii=False))
