"""Refresh only derived section review, its apparatus briefs and verification."""
from pathlib import Path
import hashlib,importlib.util,json,re,sys
W=Path(__file__).resolve().parent
ROOT=W.parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
protected=list(sorted(W.glob('M0*-REWRITE.md')))+[W/'500-word-essay-abstract']
before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
(W/'S01-CURRENT-AUTHOR-INPUT-HASHES.json').write_text(json.dumps({'date':'2026-10-04','standing':'Protected author inputs captured before derivative-only refresh; no originals written','inputs':before},ensure_ascii=False,indent=2)+'\n')
a=load('s01_assembly',W/'assemble-s01-review.py');sys.argv=[str(W/'assemble-s01-review.py')];a.main()
r=json.loads((W/'S01-ASSEMBLY-RECEIPT.json').read_text());words=f'{r["authorial_body_words"]:,}';notes=r['unique_note_definitions'];bindings=len(r['source_bindings'])
p=W/'CLAUDE-ABSTRACT-AND-ASSEMBLY-BRIEF.md';s=p.read_text();s,n=re.subn(r'At the refreshed capture it has [\d,]+ authorial body words, \d+ notes and \d+ explicit source bindings\.',f'At the refreshed capture it has {words} authorial body words, {notes} notes and {bindings} explicit source bindings.',s);assert n==1;p.write_text(s)
p=W/'S01-QUOTATION-DISPOSITION-AND-AUTHOR-CORRECTIONS.md';s=p.read_text();s,n=re.subn(r'\*\*[\d,]+ authorial body words\*\*, \*\*\d+ consolidated notes\*\*, \*\*\d+ explicit source bindings\*\*',f'**{words} authorial body words**, **{notes} consolidated notes**, **{bindings} explicit source bindings**',s);assert n==1;p.write_text(s)
sys.argv=[str(W/'assemble-s01-review.py'),'--check'];a.main()
load('s01_working_verification',W/'verify-s01-working-return.py')
