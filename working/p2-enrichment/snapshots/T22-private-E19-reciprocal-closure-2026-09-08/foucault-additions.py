from pathlib import Path
import json,hashlib
P=Path(__file__).parent
base=Path('submission-package/essay/symbolon/episteme')
rows=[]
def add(path,slot,text,field):rows.append(dict(path=str(base/path),slot=slot,paragraph=text,field=field,record_id='lens-foucault',evidence_register=3))
e2='etymologies/arbitration-hybris-regard-anamnesis/'
e3='etymologies/trust-place-logos-nomos-natio-credere/'
e6='etymologies/apportionment-and-economy/'
add(e2+'WHOLE-FIELD.md','<a id="con-text-through-diaphaneity">','The [Foucault lens](../../lenses/foucault.md#foucault-authorised-speech) **historicises** the admission procedures through which speech becomes an actionable case. Its selected modern European inquiry distinguishes discourse production, distributed power and different scales of intervention. At register 3, Arbitration-in-Crisis must examine whether an objection can change the criterion or commission, rather than being recorded as another confirmation of the evaluator’s categories. That consequence deepens the evidence needed for regard while preserving the native two conjugate sixfolds and six generated relations. The offered worker example supplies a question for institutional inquiry, not a reported empirical finding.','E2')
add(e2+'HISTORICAL-BRANCHES.md','## Register 4','The [Foucault lens](../../lenses/foucault.md#foucault-commission-return) **qualifies** institutional return at register 3: permission to speak and power to revise what speech counts as are different relations. A complaint can enter a record without reaching the office authorised to change its frame. The selected volume’s modern European analysis gives this comparison a situated source; it neither establishes a universal history of arbitration nor supplies Taylor’s native derivation.','E2')
add(e3+'WHOLE-FIELD.md','## #4 — Natio','The [Foucault lens](../../lenses/foucault.md#foucault-distributed-office) **extends** Nomos at register 3 by locating an office within distributed forms, resources and jurisdictions. Distribution explains how a decision becomes possible without dissolving the deciding office’s responsibility. An appeal returns effectively when it can reach the authority able to alter the rule or commission. Foucault’s relational method and Taylor’s covenant construction retain their distinct warrants; neither establishes the other’s theological histories.','E3')
add(e6+'WHOLE-FIELD.md','### Liability and release','The [Foucault lens](../../lenses/foucault.md#foucault-scales-of-measure) **qualifies** delegated labour at register 3 through the transformation of reports into categories and distributions which authorise further intervention. A completed output can conceal the expenditure of the people maintaining its account. Individual treatment and population policy therefore require different evidence: an aggregate improvement cannot by itself settle the authority exercised over each participant. Return must retain the transformation and identify whose work and consequence can change the next commission.','E6')
add('lenses/foucault.md','The route back to the essay accordingly','The lens **returns-to** [E3’s Nomos](../etymologies/trust-place-logos-nomos-natio-credere/WHOLE-FIELD.md#3--nomos-the-account-distributes-authority) through the jurisdiction that determines whether an appeal can alter a received rule. Its distributed conditions explain an office’s dependence without cancelling its responsibility. It **returns-to** [E6’s delegated labour](../etymologies/apportionment-and-economy/WHOLE-FIELD.md#delegated-labour-distributes-capacity-and-return) through the work of recording and maintaining comparisons which makes an assessable object available. These register-3 consequences distinguish a revised account from a revised commission; source analysis and contemporary empirical verification remain separate.','E3/E6')
manifest=[]
for i,s in enumerate(sorted({r['path'] for r in rows})):
 f=Path(s);b=f.read_bytes();t=b.decode();snap=f'before/foucault-{i}.md';(P/snap).write_bytes(b)
 for r in rows:
  if r['path']==s:
   assert t.count(r['slot'])==1,(s,r['slot']);assert r['paragraph'] not in t
   t=t.replace(r['slot'],r['paragraph']+'\n\n'+r['slot'],1)
 assert f.read_bytes()==b
 f.write_text(t);manifest.append(dict(path=s,before_sha256=hashlib.sha256(b).hexdigest(),after_sha256=hashlib.sha256(t.encode()).hexdigest(),snapshot=snap))
(P/'foucault-additions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(P/'foucault-before.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Applied',len(rows))
