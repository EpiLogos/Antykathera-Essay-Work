#!/usr/bin/env python3
"""Preservation tests: textual identity and notation, not proofs of philosophy."""
from pathlib import Path
import importlib.util,json,re,subprocess
A=Path(__file__).resolve().parent;ROOT=A.parents[2];W=A.parent
s=importlib.util.spec_from_file_location('build',A/'build_whole_pass.py');b=importlib.util.module_from_spec(s);s.loader.exec_module(b)
s=importlib.util.spec_from_file_location('edits',A/'editorial_revisions.py');e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
checks=[]
for k in b.KEYS:
 def formulas(t):return [(m.group(1) if m.group(1)is not None else m.group(2)).strip() for m in b.MATH.finditer(b.math_normalize(t))]
 assert formulas(e.initial[k])==formulas(e.texts[k]),('changed TeX',k)
 checks.append({'section':k,'all_TeX_expressions_preserved_in_order':True,'count':len(formulas(e.initial[k]))})
regions=[
 ('s01','The defining proposition takes that participation','The Śaiva articulation of knower','Subject proposition, self-application, failure/disclosure, fourth/fifth, God-direction and sphere'),
 ('s0','The Śaiva account is adopted here because','The Buddhist criticism of the fabricated proprietor','Complete five-pressure comparative adoption'),
 ('s0','The Huayan contemplation of Indra','The Huayan scene has made mutual','Complete primary Huayan narrative and its own qualification'),
 ('s1','Bhāskara retains the written expression.','Its mathematical proposal still needs','Bhāskara’s primary mathematical/metaphysical encounter'),
 ('s2','Demodocus takes up his lyre','Harmonia enters through a different telling.','Complete Homeric action, three liabilities, interpretation and release'),
 ('s3','<a id="s3-m26">','<a id="s3-m30">','M26–M29: inverse parents, full Spanda, phase, charts, topology and music'),
 ('s4',"Pauli's egg dream gives this relation a body.",'<!-- s4-calculation-care -->','Complete Pauli dream and mathematical/narrative consequences'),
 ('s4','Libido names the psychic investment','<!-- M33','Energetic, recognitive, prāṇic, Śāktic, plasmic and ethical development'),
 ('s4','<!-- M33','<!-- M34','Complete Aion movement and connected quaternia'),
 ('s4','<!-- s4-crossed-zero -->','<!-- M35','Complete crossed-zero, paper and personed recognition'),
 ('s4','In Ovid, the pursuit begins','The native `180°','Complete Ovidian story, recoil/apparent assent and authored Dionysian return'),
 ('s4','Meaningful continuity joins the Quaternal lens','<!-- s4-refraction-worked-return -->','All twelve lens bodies as six whole complementary pairs'),
 ('s50','<a id="s50-m44">','<a id="s50-m46">','Complete three-motion mirror and Antikythera material encounter'),
 ('s50','Job makes the difficulty impossible','<a id="s50-m48">','Complete Job encounter and irreparable loss')]
for k,start,end,name in regions:
 t=e.initial[k];i=t.index(start);j=t.index(end,i);span=t[i:j]
 assert span in e.texts[k],('preserved argument changed',k,name)
 checks.append({'section':k,'region':name,'source_start_line':t[:i].count('\n')+1,'source_end_line':t[:j].count('\n')+1,'sha256':b.sha(span.encode()),'unchanged_in_editorial_candidate':True})
source_paths=['submission-package/essay/symbolon/episteme/conjugate/AC.md','submission-package/essay/quilt/27-07-26-QUILTING-FOR-FULL-ARGUMENT.md','working/sources-texts-references/10-7-2026-core-theorems-pithy.md','working/sources-texts-references/definition-of-god-working/The Definition of God — Draft 3.md','submission-package/essay/symbolon/episteme/arguments/A05-Prakasa-Vimarsa.md','submission-package/essay/symbolon/episteme/arguments/A08-Apoha-Constitutive-Exclusion.md']
source_checks=[]
for path in source_paths:
 local=(ROOT/path).read_bytes();rec={'path':path,'ref':b.SOURCE_PIN,'git_blob':b.blob(local),'sha256':b.sha(local),'lines':len(local.decode().splitlines())}
 if (ROOT/'.git').exists():
  old=subprocess.check_output(['git','show',b.SOURCE_PIN+':'+path],cwd=ROOT);assert old==local,('source pin mismatch',path);rec['git_show_source_pin_matches']=True
 else:rec['git_show_source_pin_matches']=None
 source_checks.append(rec)
canonical=(A/'THE-RETURN-OF-ZERO.md').read_text()
end=canonical[canonical.index('<a id="M48">'):]
positions=[end.index('The return begins as `1/0`.'),end.index('What is it that knows?'),end.index('I am. The recognition'),end.index('My account can now be offered')]
assert positions==sorted(positions)
assert 'The God-definition attempted at the beginning' not in canonical
assert 'Subjective Internality' not in canonical
assert len(b.REPRISE.findall(canonical))==10
result={'standing':'Textual preservation and source identity checks; not an independent source audit or proof of philosophical claims.','checks':checks,'direct_source_pin_checks':source_checks,'terminal_order_preserved':True,'subject_led_callback_corrected':True,'knower_term_matches_AC':True,'controlled_reprises':10}
(A/'SEMANTIC-CHECKS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Passed',len(checks),'preservation checks; terminal order and source identities recorded.')
