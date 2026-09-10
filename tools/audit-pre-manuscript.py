#!/usr/bin/env python3
"""Check current admitted identities and saved proof routes without rebinding receipts.

This is a structural and evidence-preservation check, not a semantic certification.
Its output retains missing routes and changed passage witnesses for human review.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, importlib.util, json, re, sys

def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def plain(s):
 s=re.sub(r'\[\[([^]|]+)(?:\|([^]]+))?\]\]',lambda m:m[2] or m[1],s)
 s=re.sub(r'\[([^]]+)\]\((?:[^()]|\([^()]*\))*\)',r'\1',s)
 return re.sub(r'\s+',' ',s).strip()

def audit(root):
 root=root.resolve();reader=module('gate_reader',root/'tools/audit-reader-navigation.py');a=reader.ReaderAudit(root);report=a.run()
 rooms=module('gate_rooms',root/'tools/build-section-rooms.py');movements=rooms.load_movements(root)
 census=report['records']; ids=Counter(r['record_id'] for r in census);homes=Counter(r['canonical_home'] for r in census)
 expected={f'C{i:02}' for i in range(1,65)}|{f'A{i:02}' for i in range(1,37)}|{f'A{i:02}p' for i in range(1,37)}|{'A/C'}
 canonical=[];wrong=[];thin=[]
 for r in census:
  if r['record_id'] not in expected:continue
  p=root/r['canonical_home'];fm,body=rooms.parse_frontmatter(p.read_text())
  if fm.get('record_id')!=r['record_id']:wrong.append(r['canonical_home'])
  canonical.append(r['record_id'])
  if r['record_id']=='A/C':continue
  chunks=re.split(r'(?m)^##\s+(#[^\n]+)\n',body);sections=dict(zip(chunks[1::2],chunks[2::2]))
  for h in ['#0','#1','#2','#3','#4','#5→0']:
   text=next((v for k,v in sections.items() if k==h or k.startswith(h+' ')),None)
   if text is None or not re.search(r'\w',reader.visible_text(text)):thin.append({'id':r['record_id'],'position':h})
 alignment=[];next_missing=[];legacy=[]
 for m in movements:
  source=str(m['path'].relative_to(root));seq=m['sequence'];routes=rooms.load_canonical_routes(root,m['path'].parent.parent)
  alignment.append({'sequence':seq,'routes':[str(p.relative_to(root)) for _,p in routes.get(seq,[])]})
  targets={a.resolve(source,k)[0] for k in reader.links(m['path'].read_text()) if a.resolve(source,k)[1]=='ok'}
  expected_next=str(movements[seq%48]['path'].relative_to(root))
  if expected_next not in targets:next_missing.append(seq)
  legacy += [{'sequence':seq,'target':t} for t in targets if '/section-rooms/arguments/' in t]
 proofdir=root/'working/p2-enrichment/audits/T22-K-E-consumer-pairs-2026-09-08'
 proof=json.loads((proofdir/'proof.json').read_text());denom=json.loads((proofdir/'all272-denominator-supplement.json').read_text())
 route_checks=[]
 for r in denom['actual_route_evidence'].values():
  p=root/r['source']; targets={a.resolve(r['source'],k)[0] for k in reader.links(p.read_text()) if a.resolve(r['source'],k)[1]=='ok'}
  route_checks.append({'source':r['source'],'target':r['target'],'reader_route_present':r['target'] in targets,'prior_direct_evidence':bool(r.get('literal_paragraphs') or r.get('graph_edges'))})
 witnesses={}
 def visit(x):
  if isinstance(x,dict):
   if {'path','text'}<=x.keys() and isinstance(x['text'],str) and str(x['path']).startswith('submission-package/essay/'):
    witnesses[(x['path'],x['text'])]=x
   for v in x.values():visit(v)
  elif isinstance(x,list):
   for v in x:visit(v)
 visit(proof)
 changed=[];exact=equivalent=0
 for (path,text),row in witnesses.items():
  current=(root/path).read_text()
  if text in current:exact+=1
  elif plain(text) in plain(current):equivalent+=1
  else:changed.append({'path':path,'prior_text':text,'prior_start_line':row.get('start_line')})
 baseline=json.loads((root/'working/p2-enrichment/audits/T24-2026-09-09/start-hashes.json').read_text())
 # This baseline records publication bytes at T24 entry, including inherited uncommitted work.
 if 'hashes' in baseline:baseline=baseline['hashes']
 protected=[]
 for path,digest in baseline.items():
  if not isinstance(digest,str):continue
  if Path(path).name in {'NOTES.md','AUTHORIAL-TEXT.md','THE-RETURN-OF-ZERO.md','SCRATCH.md','READING.md','HISTORY.md'}:
   p=root/path
   if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:protected.append(path)
 return {'scope':__doc__.strip(),'census':report['counts'],'canonical_suite':{'count':len(canonical),'missing':sorted(expected-set(canonical)),'duplicate_ids':{k:v for k,v in ids.items() if v>1},'duplicate_homes':{k:v for k,v in homes.items() if v>1},'metadata_mismatches':wrong,'missing_sixfold_sections':thin},'movements':{'count':len(movements),'alignment':alignment,'missing_alignment':[r['sequence'] for r in alignment if not r['routes']],'missing_next_link':next_missing,'live_legacy_links':legacy},'preservation':{'changed_protected_since_T24_entry':protected},'prior_evidence':{'denominator_rows':len(denom['rows']),'consumer_instances':len(denom['consumer_instances']),'dispositions':dict(Counter(x['disposition'] for x in denom['consumer_instances'])),'checked_saved_routes':len(route_checks),'missing_reader_routes':[r for r in route_checks if r['prior_direct_evidence'] and not r['reader_route_present']],'saved_paragraphs':len(witnesses),'exact_paragraphs':exact,'same_text_after_link_normalisation':equivalent,'changed_witnesses_requiring_review':changed},'source_standing':dict(Counter(str(x.frontmatter.get('quote_status','undeclared')) for x in a.ws.artifacts.values() if x.artifact_type=='source-house'))}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project-root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path,required=True);args=p.parse_args();r=audit(args.project_root);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k in ['census','canonical_suite','preservation']},indent=2))
if __name__=='__main__':main()
