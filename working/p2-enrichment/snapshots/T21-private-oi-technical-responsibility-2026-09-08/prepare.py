from pathlib import Path
import json,hashlib,zipfile,subprocess
root=Path.cwd();out=root/'working/p2-enrichment/snapshots/T21-private-oi-technical-responsibility-2026-09-08';tech=out.parent/'T21-private-technology-politics-2026-09-08';inputs={}
def add(path,scope,reuse=None):
 f=Path(path);f=f if f.is_absolute() else root/f
 r={'path':str(f.relative_to(root)) if f.is_relative_to(root) else str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'read_scope':scope}
 if reuse:r['reuse_receipt']=reuse
 inputs[r['path']]=r
for r in json.loads((tech/'packet.json').read_text())['inputs']:
 if '/HISTORY.md' in r['path']:continue
 add(r['path'],r['read_scope']+'; unchanged semantic content reused',str(tech/'packet.json'))
for r in json.loads((out/'sources.json').read_text()):add(r['path'],'full canonical SOURCE or full protected NOTES; notes authorial intent and quotation leads only')
loc=json.loads((out/'locator.json').read_text())
for a in loc['minimum_declared_argument_depth']:
 for p in Path('submission-package/essay/symbolon/episteme/arguments').glob(a+'-*.md'):add(p,'full current canonical argument')
for r in json.loads((out/'reference-dispositions.json').read_text()):add(r['reference_note'],'full reference material and current disposition; legacy not independent authority')
for n in ['SOURCE-AND-AUTHORITY-MAP','SYMBOLON-OI-WIKI-CONTRACT','S5-S50-CAPSTONE-QUILT','CAPSTONE-QUILT-REGISTRATION-2026-08-19']:
 add('working/harmonisation-2026-08-18-objective-internality-capstone/'+n+'.md','full authored programme/contract; dated implementation reports not current shipping findings')
for p in ['working/sources-texts-references/Epi Paper Write-ups/Symbolon Dynamics — Archetype, Attractor, and Objective Internality.md','working/sources-texts-references/definition-of-god-working/revision-notes-trust-and-f-blocks.md']:
 add(p,'full actual raw local text; stale absolute SOURCE locator resolved read-only; historical proposals subject to later ratification')
for p in Path('submission-package/essay/section-rooms').glob('*/movements/*.md'):
 if p.name[:2] in ['32','33','35','47']:add(p,'full current Movement')
for p in loc['etymology_declared_targets']:
 add(p,'full current E whole; E4 fresh, E2/E3 reused from full law reading, E6 reused from technology reading')
for p in ['docs/CANONICAL-PRODUCT-FIELD.md','docs/OBJECTIVE-CO-INTERNALITY.md','docs/positions/FOUNDING-POSITIONS.md','shared-field/social.mjs']:
 add('/Users/admin/Central/Work/O-I/'+p,'full actual current local product source; code static scope plus private functional probe only')
# Source bindings plus exact input rows remain private. Shared census is untouched.
head=subprocess.check_output(['git','-C','/Users/admin/Central/Work/O-I','rev-parse','HEAD'],text=True).strip()
product=[]
for r in inputs.values():
 if r['path'].startswith('/Users/admin/Central/Work/O-I/') and '/projects/' not in r['path']:
  f=Path(r['path']);rel=str(f.relative_to('/Users/admin/Central/Work/O-I'));b=subprocess.check_output(['git','-C','/Users/admin/Central/Work/O-I','show',head+':'+rel]);r['git_head']=head;r['matches_committed_head']=b==f.read_bytes();product.append(r)
(out/'product-evidence.json').write_text(json.dumps(product,indent=2)+'\n')
packet={'record_id':'dossier-oi-technical-responsibility','target':loc['canonical_home'],'scope':'Only dossier plus this private packet/snapshot and development receipt; no source/consumer/shared files','date':'2026-09-08','inputs':list(inputs.values()),'product_head':head,'claim_boundary':'Native Argued claim and Offered engineering correspondence distinct. Current local product contracts, dated 2026-08-19 audit report and bounded 2026-09-08 validator execution separately typed. No whole deployment claim.'}
(out/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
with zipfile.ZipFile(out/'bound-inputs.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
 for r in inputs.values():
  f=Path(r['path']);f=f if f.is_absolute() else root/f
  z.write(f,('external/'+str(f).lstrip('/')) if Path(r['path']).is_absolute() else r['path'])
(out/'targets.json').write_text(json.dumps({'elements':[{'record_id':packet['record_id'],'canonical_home':loc['canonical_home'],'register':'episteme'}]},indent=2)+'\n')
print('frozen inputs',len(inputs),'product snapshots',[(r['path'],r['matches_committed_head']) for r in product])
