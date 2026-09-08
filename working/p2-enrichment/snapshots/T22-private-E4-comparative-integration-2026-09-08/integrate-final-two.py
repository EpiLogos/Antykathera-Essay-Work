from pathlib import Path
import json
r=Path('.');d=r/'working/p2-enrichment/snapshots/T22-private-E4-comparative-integration-2026-09-08';E=r/'submission-package/essay/symbolon/episteme/etymologies/symbol-account-and-trust'
# Run after the source-owner's scoped T22 release is verified.
ps=[r/f'working/p2-enrichment/page-packets/T22-E4-{name}-proposal-2026-09-08.json' for name in ['sanskrit-enumeration','hebrew-spr']]
x=[json.loads(p.read_text()) for p in ps]
h=E/'HISTORICAL-BRANCHES.md';b=h.read_text();insert='<a id="chinese-rectification-of-names"></a>'
assert b.count(insert)==1
branches=[]
for row in x:
 s=row['exact_branch_markdown'].replace('\n## ','\n### ',1)
 s+='\n**Remaining source scope:** '+' '.join(row['remaining_source_debts'])+'\n'
 branches.append(s)
b=b.replace(insert,'\n\n'.join(branches)+'\n'+insert)
b=b.replace(' Sanskrit and Hebrew integrations remain pending their source owners’ completed proposals.','')
old='This branch work changes the whole field in three precise ways: token correspondence now has an independently checked lexical witness; a named material tally locates the record/reliance distinction; and reference 38 can return through separate histories and an explicitly poetic seam. Remaining historical leaves stay visible as tasks rather than acquiring the standing of these findings.'
new='The five comparisons give the source-return different work: discriminative classification must retain its warrants; an entrusted record must remain answerable to material purpose; a political designation must sustain practicable speech; a religious enumeration must retain its act and attributed promise; a funerary name must preserve the particular person and provision it records. The Greek token, English tally and hāl/hol distinction remain independently sourced branches. These acquired relations complete the initial comparative development at their stated registers. The named primary collation, chronology, reception and empirical tasks remain Open; the comparison neither requires nor supplies a universal genealogy.'
assert b.count(old)==1;b=b.replace(old,new)
h.write_text(b)
p=E/'WHOLE-FIELD.md';b=p.read_text();marker='[A15, Ratio / Rationality]';assert b.count(marker)==1
new='\n\n'.join(row['whole_field_proposal']['exact_markdown'] for row in x)+'\n\n'
b=b.replace(marker,new+marker)
b=b.replace('HISTORICAL-BRANCHES supplies the bounded lexical and material acquisitions, including reference 38; its remaining primary and comparative tasks remain explicit.','HISTORICAL-BRANCHES supplies the bounded lexical and material acquisitions, including reference 38 and five independently developed comparative cases; its named primary collation, chronology, reception and empirical tasks remain explicit.')
p.write_text(b)
(d/'final-two-integration.json').write_text(json.dumps({'proposal_paths':[str(q) for q in ps],'cases':[row['case'] for row in x],'consumer_proposals':[{'case':row['case'],**c} for row in x for c in row['consumer_proposals']],'status':'E4 integration complete; consumer reverses parent-owned'},indent=2,ensure_ascii=False)+'\n')
print('Five E4 cases integrated; two E4 files written')
