from pathlib import Path
import json,hashlib,re
R=Path('working/p2-enrichment'); B=Path('submission-package/essay/symbolon/episteme'); lens=B/'lenses/baudrillard.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
q=json.loads((R/'snapshots/T21-lens-baudrillard-2026-09-08/bound-queue.json').read_text())['elements'][0]
prose=[
('A20',4,'A profile can help produce the conduct later offered as its confirmation. This efficacy leaves its fidelity to the person or encounter to be tested; possession begins when contrary testimony cannot reach the categories governing the profile. The Baudrillard lens returns that distinction through its account/source aperture.'),
('A24',3,'An explanatory account can expose decisions while preserving its own criterion as the unquestionable referent. The Baudrillard lens adds this reflexive test: can the governed participant contest what the analysis recognises as an answer, including the commission under which it judges?'),
('A32',3,'Baudrillard’s model precession makes the second motion difficult to overlook; it does not establish the third. The lens returns to initiated sourceward correction: an instrument’s causal influence and its capacity to revise its governing measure require distinct demonstrations.'),
('C27',3,'Compulsory disclosure can leave the office of revision inaccessible. Forget Foucault supplies the visibility pressure through the Baudrillard lens; the native protected-account criterion asks whether resistance can reach the authority competent to change scope or mandate.'),
('C33',2,'Differential sign-value can make an image effective without establishing the transformation of its interpreter. The Baudrillard lens returns this distinction to living valuation: what changed in attention and action, and what continuing encounter can revise the image’s assigned significance?'),
('C38',3,'Baudrillard reverses Borges’s map fable and then contests even its remaining map/territory distinction. The lens preserves the different positive account here: a made map genuinely serves as local Bimba within a Context Frame while remaining pratibimba toward wider sources, including sources that can revise that local reference.'),
('C55',2,'Simulation theory does not erase the difference among feedback, performativity and a self-fulfilling prediction. The Baudrillard lens returns the concrete test: a forecast can alter a world while remaining false, and initiated return additionally requires that consequences reach the criterion governing the next forecast.')]
rows=[]
for ident,pos,paragraph in prose:
 rel=next(x for x in q['relations'] if Path(x['path']).name.startswith(ident+'-'));p=Path(rel['path']);ls=p.read_text().splitlines();start=next(i+1 for i,l in enumerate(ls) if l.startswith('## #'+str(pos)))
 end=next((i for i in range(start,len(ls)) if ls[i].startswith('## ')),len(ls))
 rows.append({'row_id':'T22-baudrillard-'+ident,'path':str(p),'start_line':start,'end_line':end,'sha256':sha(p),'existing_fragment':'\n'.join(ls[start-1:end]),'operation':rel['operation'],'proposed_paragraph':paragraph,'return_path':str(lens),'status':'unapplied; Copernicus owns consumer integration'})
e4={'row_id':'T22-baudrillard-E4','path':str(B/'etymologies/symbol-account-and-trust/WHOLE-FIELD.md'),'anchor':'account-re-enters-source-field','operation':'Register-3 operational comparison retains all four generated operations; source correction changes the next account.','proposed_paragraph':'The Baudrillard lens tests an account that helps produce its later confirmation. Symbol answers to source keeps efficacy distinct from fidelity; Account does not replace source retains dependence within local authority; Trust keeps the return route active requires consequential correction; Account re-enters source-field allows that correction to reach the governing criterion. Historical orders, image phases and fractal value remain distinct source-specific sequences.','return_path':str(lens),'status':'unapplied; Laplace owns E4 integration'}
checks=json.loads((R/'receipts/T21-lens-baudrillard-local-checks.json').read_text());checks['files']={p:sha(Path(p)) for p in checks['files']};save(R/'receipts/T21-lens-baudrillard-local-checks-final.json',checks)
report={'status':'canonical development complete; consumer returns proposed','outputs':checks['files'],'packet':'working/p2-enrichment/page-packets/T21-lens-baudrillard-packet-r3.json','packet_check':'PASS after final source metadata changes','source_passages':{'symbolic_exchange':'2017 cached primary witness file36–44,94–98; no local scan; selected only','forget_foucault':'2007 scan printed29–43,55–67; no full essay/interview claim','simulacra':'Glaser reflow file3–9; cover visually checked;1994 print collation open','fatal_strategies':'2008 primary OCR closing chapter219–230 complete; no whole-book claim','transparency':'Benedict1993 primary preview3–6 and frontmatter; no full scan'},'source_card_count':16,'primary_paraphrase_cards':14,'editorial_dispositions':2,'reference_note_dispositions':{'assigned_rows':[],'standing':'No Baudrillard-specific reference-note rows in bound locator/recovery; no coverage invented.'},'consumer_proposals':rows,'E4_proposal':e4,'unratified':['four-phases/four-falls','fourth QL posture','perfect-crime/cohomology','prakasa-without-vimarsa doctrinal identity'],'projection_check':{'status':'blocked outside owned scope','remaining_invalid_main_source_for':['foucault-1976-history-sexuality-v1: lens-foucault','fanon-1952-peau-noire-masques-blancs: submission-package/essay/symbolon/mytheme/worlds/francophone-anticolonial/fanon-language-gaze-mask-recognition/WHOLE.md'],'generated_files_written':False},'protected_notes_changed':checks['protected_notes_changed'],'index_actions':'none; parent K exclusive window'}
save(R/'receipts/T21-lens-baudrillard-development.json',report)
# Candidate commit inventory: explicit four earlier units, six current bodies, owned evidence only.
files=list(checks['files'])
for id in ['dossier-formal-limit','history-mathematics','history-zero-subject-advent','dossier-zero-reception']:
 packet=R/f'page-packets/T21-{id}-packet.json'; target=json.loads(packet.read_text())['target']; home=target['canonical_home'];
 if id.startswith('history-'):home=str(Path(home).parent/'DEVELOPMENT.md')
 files.append(home)
 for p in [R/f'T21-{id}-census.json',R/f'T21-{id}-queue.json',packet,R/f'receipts/T21-{id}-development.md',R/f'receipts/T22-{id}-hygiene.json',R/f'receipts/T22-{id}-targets.json']:
  if p.exists():files.append(str(p))
for p in [R/'T21-dossier-zero-reception-external-provenance.json',R/'receipts/T22-dossier-formal-limit-foldback.md']:
 if p.exists():files.append(str(p))
for folder in [R/'raw/T21-baudrillard',R/'snapshots/T21-lens-baudrillard-2026-09-08']:
 files += [str(p) for p in folder.rglob('*') if p.is_file()]
for pattern in ['T21-lens-baudrillard*','T22-lens-baudrillard*']:
 for folder in [R/'receipts',R/'page-packets']:files += [str(p) for p in folder.glob(pattern) if p.is_file()]
missing=[p for p in files if not Path(p).exists()]
save(R/'receipts/T21-baudrillard-prior-four-commit-scope.json',{'status':'READY candidate scope; no staging until explicit index grant','commit_message':'Develop four Episteme records and source-bound Baudrillard lens','preservation':'Current zero-reception includes parent Nothaft q001 abstract-only correction; commit current body, never private before-image. Prior receipts retain historical hashes and debts.','files':[{'path':p,'sha256':sha(Path(p)),'bytes':Path(p).stat().st_size} for p in sorted(set(files)) if Path(p).exists()],'missing':missing,'excluded':'Other canonical files, NOTES, protected HISTORY, shared queue/census, parent consumer receipts, generated projections; no git add or commit performed.'})
print('Saved semantic receipt and scope',len(set(files)),'paths; missing',missing)
