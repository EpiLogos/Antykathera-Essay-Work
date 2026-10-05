"""Verify the current derivative return; never mutate author/source inputs."""
from pathlib import Path
import json,hashlib,importlib.util,sys,urllib.parse
ROOT=Path(__file__).resolve().parents[2];W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('okf_workspace',ROOT/'tools/okf-workspace.py');mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
checks=[]
for name in ['CLAUDE-ABSTRACT-AND-ASSEMBLY-BRIEF.md','SOURCE-AND-VISUAL-APPARATUS.md','CONFRONTING-THE-LIMIT-S01-REVIEW.md','S01-QUOTATION-DISPOSITION-AND-AUTHOR-CORRECTIONS.md']:
 p=W/name;n=0
 for target,kind in mod.markdown_targets(p.read_text()):
  q=urllib.parse.unquote(target)
  if not q or q.startswith(('http:','https:')):continue
  assert (p.parent/q).resolve().is_file(),(name,q)
  n+=1
 checks.append({'file':name,'sha256':sha(p),'relative_targets_resolve':True,'checked_relative_targets':n})
r=json.loads((W/'S01-ASSEMBLY-RECEIPT.json').read_text());inputs=[]
for x in r['inputs']:
 actual=sha(ROOT/x['path']);inputs.append({'path':x['path'],'current_sha256':actual,'matches_assembly_input':actual==x['input_sha256']})
assert all(x['matches_assembly_input'] for x in inputs),'Active author input changed; refresh derivative assembly first'
patch=json.loads((W/'S01-QUOTATION-SOURCE-PATCH-RECEIPT.json').read_text())
abstract=W/'500-word-essay-abstract';abstractsha=sha(abstract);assert abstractsha==patch['protected_authorial_inputs'][str(abstract.relative_to(ROOT))]
protected=json.loads((W/'S01-CURRENT-AUTHOR-INPUT-HASHES.json').read_text())
assert all(sha(ROOT/rel)==expected for rel,expected in protected['inputs'].items()),'Protected author input advanced during derivative refresh'
addendum=ROOT/'working/publication-integration-2026-10-04/LATE-LOCATORS-APPLIED.json'
late=json.loads(addendum.read_text());applied=[]
for row in late['changes']:
    text=(ROOT/row['path']).read_text()
    for pid in row['passage_ids']:
        assert ('<a id="'+pid+'"></a>') in text,pid
        applied.append(pid)
overrides=json.loads((W/'S01-APPARATUS-OVERRIDES.json').read_text())
for marker in ['s01-jung-shadow','s01-god-image','s01-jung-child']:
    text=overrides[marker]['text']
    assert 'is now applied' in text and 'Review-only pending' not in text and 'unapplied to' not in text,marker
v={'date':'2026-10-04','checks':checks,'current_assembly_inputs':inputs,'authorial_body_words':r['authorial_body_words'],'notes':r['unique_note_definitions'],'source_bindings':len(r['source_bindings']),'differing_note_collisions':len(r['collisions']),'original_abstract_sha256':abstractsha,'original_abstract_words':len(abstract.read_text().split()),'protected_author_input_hashes_match_before_after':True,'late_cards_applied':applied,'applied_addendum':str(addendum.relative_to(ROOT)),'canonical_source_snapshot_verification':'owned by integration parent; initial source receipt is historical and superseded by applied addendum','standing':'current derivative artifact/link/input-hash verification; no authorial/canonical source writes or final prose/quotation acceptance'}
(W/'S01-WORKING-ARTIFACT-VERIFICATION.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'review_words':r['authorial_body_words'],'notes':r['unique_note_definitions'],'source_bindings':len(r['source_bindings']),'collisions':len(r['collisions']),'working_links_checked':sum(x['checked_relative_targets'] for x in checks),'six_current_input_hashes':{x['path']:x['current_sha256'] for x in inputs},'review_sha256':sha(W/r['output']),'abstract_original_unchanged':True,'protected_inputs_unchanged_during_refresh':True,'late_card_statuses_applied':True},ensure_ascii=False))
