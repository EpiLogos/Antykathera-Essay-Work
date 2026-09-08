from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path('.').resolve()))
from tools.source_resolver import resolve_source_house
# Admission was executed once, with the existing-house writes followed by the taxonomy-resolved new house.
# This evidence script is not an idempotent migration; do not replay against admitted cards.
r=Path('.');d=r/'working/p2-enrichment/snapshots/T22-private-E4-comparative-integration-2026-09-08'
E='submission-package/essay/symbolon/episteme/etymologies/symbol-account-and-trust/'
lsj=resolve_source_house(r,'lsj-1940-greek-english-lexicon');mw=resolve_source_house(r,'merriam-webster-online-dictionary')
provenance='Selected online witness read on 2026-09-08 in the T21 E4 development; bounded finding and full-reading receipt retained in working/p2-enrichment/receipts/T21-etymology-symbol-account-and-trust-development.md and the historical companion. This admission reuses that completed consultation; no new retrieval, archived webpage, print collation or exact quotation is claimed.'
def card(id,n,title,body,loc,url,bound):
 return f'\n<a id="{id}-q{n:03d}"></a>\n### q{n:03d} — {title}\n\n**Paraphrase:** {body}\n\n**Locator:** {loc}\n\n**Access:** [consulted online witness]({url}).\n\n**Verification:** {provenance}\n\n**Use boundary:** {bound}\n'
body=lsj.read_text();assert 'lsj-1940-greek-english-lexicon-q010' not in body
body+=card(lsj.parent.name,10,'Symbolon — counterpart, guarantee and civic token','The entry distinguishes a token whose corresponding pieces enable subsequent recognition, a guarantee, and civic tokens used for entitlement or payment. Its listed ancient witnesses include Herodotus 6.86, Euripides Medea 613 and Plato Symposium 191d. Those citations identify different contexts; the dictionary supplies the verified semantic witness here.','s.v. σύμβολον, I.1, I.3 and I.5.','https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionaries.v1:lsj-n98312/','Register 2, selected senses only. The cited ancient passages are not independently collated. Correspondence does not establish justice, future performance or a historical derivation of native QL.')
body+=f'\nThe symbolon entry **sources** [E4’s token branch]({E}HISTORICAL-BRANCHES.md#matching-tokens-and-institutional-recognition); [Symbol answering to source]({E}WHOLE-FIELD.md#symbol-answers-to-source) develops the authorial operation at register 3.\n'
lsj.write_text(body)
entries=[
('Trust','Middle English trust is given a probably Scandinavian origin, with Old Norse traust and Old English trēowe named as related forms. Reliance, contingent hope, custody or responsible office, and credit for future payment remain distinct senses.','Word History and selected reliance, custody/office and credit senses (1, 4–5).','Registers 1 and 2 remain distinct. Preserve the dictionary’s probability qualification. This entry does not derive faith under formal limit, prove trustworthiness or supply a covenant history.'),
('Whole','Middle English hool continues Old English hāl; the selected meanings concern soundness, freedom from injury and entirety.','Word History and selected soundness/entirety senses.','Dictionary-reported descent at register 1 and selected meanings at register 2; no primary Old English text collation or theory of sealed integrity.'),
('Holy','The entry traces the word to Old English hālig and states kinship with hāl.','Word History.','Register 1. The reported kinship is not a complete derivational demonstration or a historical claim that sacredness reduces to bodily health.'),
('Health','Middle English helthe continues Old English hǣlth, derived from hāl.','Word History.','Register 1, dictionary-reported descent; no independent early-text collation or clinical outcome claim.'),
('Heal','Middle English helen continues Old English hǣlan; the entry relates that form to hāl.','Word History.','Register 1, dictionary-reported descent. The authorial return through correction is a separate register-3 operation.'),
('Hole','Middle English hole or holle continues Old English hol, the hollow-place noun associated with the adjective for hollowness. This is a separate historical line from hāl.','Word History, noun and associated hollow adjective.','Register 1. English hole/whole permits the authorial poetic crossing at register 4; no descent arrow joins hol to hāl and no topology theorem follows from the sound-match.')]
body=mw.read_text();assert 'merriam-webster-online-dictionary-q007' not in body
body=body.replace('Merriam-Webster.com Dictionary — selected E1 entries','Merriam-Webster.com Dictionary — selected E1 and E4 entries').replace('# Selected E1 lexical witnesses','# Selected E1 and E4 lexical witnesses').replace('The six named online entries were checked','The named online entries were checked')
for n,(title,claim,loc,bound) in enumerate(entries,7):body+=card(mw.parent.name,n,title,claim,f's.v. {title.lower()}, {loc}',f'https://www.merriam-webster.com/dictionary/{title.lower()}',bound)
body+=f'\nThe account and trust entries **source** [E4’s historical companion]({E}HISTORICAL-BRANCHES.md); the five hāl/hol entries **source** its [reference-38 distinction]({E}HISTORICAL-BRANCHES.md#reference-38-hal-and-hole). The [whole-field return]({E}WHOLE-FIELD.md#opening-and-integrity) preserves the authorial operational and poetic registers independently.\n'
mw.write_text(body)
id='bank-of-england-2019-payments-through-time'
assert resolve_source_house(r,id) is None
p=r/f'submission-package/essay/symbolon/episteme/sources/economics-political-economy/bank-of-england/{id}/SOURCE.md'
# Use an existing primary domain, verified against the actual source-bank taxonomy.
bank=r/'submission-package/essay/symbolon/episteme/sources'; domains=[x.name for x in bank.iterdir() if x.is_dir()]
if 'economics-political-economy' not in domains:
 assert 'political-theory-institutions' in domains
 p=bank/'political-theory-institutions'/'bank-of-england'/id/'SOURCE.md'
p.parent.mkdir(parents=True,exist_ok=True)
domain=p.parents[2].name
body=f'''---
title: Bank of England Museum — Payments through time, wooden tally A013/1
source_id: {id}
primary_domain: {domain}
node_type: source-house
record_type: museum-object-record
ownership: canonical-source-house
schema_version: 1
author:
- Bank of England Museum
title_full: Payments through time
year: 2019
metadata_status: identified-online-museum-record
edition_status: selected-object-description-consulted-2026-09-08
citation_status: citation-ready-for-named-object-description
quote_status: paraphrase-ready; no-exact-quotation
source_relation: Paraphrased
passage_surface: '#passages'
---

# Payments through time — wooden tally A013/1

Bank of England Museum, “Payments through time,” 325 years exhibition (2019), selected object description for wooden tally A013/1. The object is dated 1694; that object date is distinct from the exhibition date and the online access date, 8 September 2026. The selected museum description supplies the material attribution. No complete exhibition, archival loan register or independent examination of the object is claimed.

<a id="passages"></a>
## Selected material witness
'''
body+=card(id,1,'A013/1 — a split record of the 1694 government loan','The museum identifies wooden tally A013/1 with one of the Bank’s first loans to the Government in 1694. Its notched hazelwood was split lengthwise so each party retained a record of the debt. The split record makes the two parties’ reckoning materially comparable.','“Wooden tally stick” object description, accession A013/1, object dated 1694; unpaginated exhibition webpage.','https://www.bankofengland.co.uk/museum/whats-on/2019/325-years-exhibition/payments-through-time','A single museum-attributed material practice. The object description does not establish repayment, moral legitimacy, the entire Exchequer system, a universal history of money or transmission from Greek symbolon practices.')
body+=f'\nThe object record **sources** [E4’s debt-record branch]({E}HISTORICAL-BRANCHES.md#reckoning-report-and-a-split-debt-record). [Account not replacing source]({E}WHOLE-FIELD.md#account-does-not-replace-source) develops the difference between a record, an undertaking and the material conditions of fulfilment at authorial register 3.\n'
p.write_text(body)
# Fold only consulted URLs into their exact canonical cards.
h=r/E/'HISTORICAL-BRANCHES.md';body=h.read_text()
import os
bindings={'https://atlas.perseus.tufts.edu/dictionaries/entry/urn:cite2:scaife-viewer:dictionaries.v1:lsj-n98312/':(lsj,10),'https://www.bankofengland.co.uk/museum/whats-on/2019/325-years-exhibition/payments-through-time':(p,1),'https://www.merriam-webster.com/dictionary/account':(mw,6)}
for n,(title,*_) in enumerate(entries,7):bindings['https://www.merriam-webster.com/dictionary/'+title.lower()]=(mw,n)
for url,(src,n) in bindings.items():
 assert body.count('('+url+')')==1,(url,body.count(url))
 body=body.replace('('+url+')','('+os.path.relpath(src,h.parent)+'#'+src.parent.name+f'-q{n:03d})')
h.write_text(body)
manifest=[{'path':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in [lsj,mw,p,h]]
(d/'consulted-admissions.json').write_text(json.dumps({'status':'admitted-selected-prior-consultation; no-new-acquisition','new_cards':8,'existing_account_card_reused':True,'paths':manifest,'bindings':{url:{'source':str(src),'passage_id':src.parent.name+f'-q{n:03d}'} for url,(src,n) in bindings.items()},'provenance':provenance},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
