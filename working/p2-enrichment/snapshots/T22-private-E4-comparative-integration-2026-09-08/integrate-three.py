from pathlib import Path
import json,hashlib
r=Path('.');d=r/'working/p2-enrichment/snapshots/T22-private-E4-comparative-integration-2026-09-08'
E=r/'submission-package/essay/symbolon/episteme/etymologies/symbol-account-and-trust'
for id in ['moe-2021-revised-mandarin-dictionary','analects-ctext-legge','lane-arabic-english-lexicon-online','quran-arberry-corpus-selected','bukhari-sahih-sunnah-online','tla-hieroglyphic-hieratic-lexicon','reri-ptolemaic-funerary-papyrus']:
 x=json.loads((d/f'effects-{id}.json').read_text());assert x['root']['id']==id;assert not x['transverse_threads']
ch=r/'working/p2-enrichment/receipts/T21-chinese-zhengming/CASE-PROPOSAL.md'
s=ch.read_text().split('*Zhèngmíng* supplies',1)[1].split('\nSource links for insertion:',1)[0]
s='\n<a id="chinese-rectification-of-names"></a>\n### Chinese rectification of names — speech must sustain its office\n\n*Zhèngmíng* supplies'+s
s=s.replace('The Ministry of Education dictionary records','The [Ministry of Education dictionary](../../sources/classical-philology/ministry-of-education-taiwan/moe-2021-revised-mandarin-dictionary/SOURCE.md#moe-2021-revised-mandarin-dictionary-q001) **sources** the lexical case: it records')
s=s.replace('In the received exchange, Zilu asks','In the [received exchange, Analects 13.3](../../sources/chinese-philosophy/confucius/analects-ctext-legge/SOURCE.md#analects-ctext-legge-q001), Zilu asks')
s=s.replace('Analects 13.15 offers a particular comparison','[Analects 13.15](../../sources/chinese-philosophy/confucius/analects-ctext-legge/SOURCE.md#analects-ctext-legge-q002) **qualifies** the return with a particular comparison')
s+='\n\nThe comparison **returns-to** [Account’s source relation](WHOLE-FIELD.md#account-does-not-replace-source) through [A15](../../arguments/A15-Ratio-Rationality-Measure-Reckoning-Harmony-Account.md): the measure must retain the office and obligations it judges. It **returns-to** [Trust’s continuing route](WHOLE-FIELD.md#trust-keeps-the-return-route-active) through [C27](../../concepts/C27-Protected-Account-Occupied-Zero-Source-Claim.md): warranted stable counsel remains distinct from an office immune to correction. These are authorial consequences for the existing consumers, with their proposed new case-specific reverse paragraphs still separately owned. Critical manuscript collation, a selected Legge print edition, a specific Wei succession dispute and historical implementation or reception remain Open.\n'
parts=[s];whole=[]
for label in ['Arabic','Egyptian']:
 p=r/f'working/p2-enrichment/page-packets/T22-E4-{label}-case-proposal.md';t=p.read_text()
 branch=t.split('## Proposed HISTORICAL-BRANCHES insertion\n',1)[1].split('\n## Exact WHOLE-FIELD return proposal',1)[0].strip()
 if label=='Arabic':branch=branch.replace('[Lane’s selected entries](../../sources/classical-philology/lane/lane-arabic-english-lexicon-online/SOURCE.md#passages)','[Lane’s ḥisāb entry](../../sources/classical-philology/lane/lane-arabic-english-lexicon-online/SOURCE.md#lane-arabic-english-lexicon-online-p001) and [separate aḥṣā entry](../../sources/classical-philology/lane/lane-arabic-english-lexicon-online/SOURCE.md#lane-arabic-english-lexicon-online-p002)')
 if label=='Arabic':branch+='\n\nThe case **returns-to** [A15](../../arguments/A15-Ratio-Rationality-Measure-Reckoning-Harmony-Account.md) with the counted object, textual warrant and further act specified; it **returns-to** [A23](../../arguments/A23-Trust-Faith-and-the-Formal-Limit.md) with the undertaking distinguished from empirical verification of its promised outcome. Their native arguments are not derived from the numerical formula. Complete Names lists, particular recitation technologies and the historical dating of the individual Qur’anic verses remain outside this acquired scope.'
 else:branch+='\n\nThe case **returns-to** [C21](../../concepts/C21-Living-Symbol-Idol.md) with a preserved sign’s office distinguished from possession of its bearer. Material survival alone decides neither living symbol nor idol. Full spell transcription and translation remain Open; the admitted object and attributed funerary provision do not depend on inventing them.'
 parts.append(branch)
 w=t.split('## Exact WHOLE-FIELD return proposal\n',1)[1].split('\n## Exact consumer proposal',1)[0]
 if label=='Arabic':w=w.split('\n\nThe [Arabic',1)[1];w='The [Arabic'+w
 whole.append(w.strip())
h=E/'HISTORICAL-BRANCHES.md';b=h.read_text();old='The protected HISTORY also retains Sanskrit enumeration, Hebrew counting/writing, Chinese rectification of names, Arabic reckoning and Egyptian naming. These remain independent language and institutional inquiries. Each needs its own lexical entry, primary passage and dated practice before any comparison is enlarged. They do not supply hidden roots for the three English terms and are not new E4 primitives. Their operational comparisons must return with the difference of source and practice still visible.'
assert b.count(old)==1
intro='The protected HISTORY retains five independent comparisons: Sanskrit enumeration, Hebrew counting/writing, Chinese rectification of names, Arabic reckoning and Egyptian naming. Each has its own lexical and textual or material practice. They supply no hidden roots for the three English terms and introduce no new E4 primitives. The developed cases below return through the four existing operations, retaining which practice is textually prescribed, which object survives, and which consequence belongs to the essay. Sanskrit and Hebrew integrations remain pending their source owners’ completed proposals.'
b=b.replace(old,intro+'\n\n'+'\n\n'.join(parts))
h.write_text(b)
p=E/'WHOLE-FIELD.md';b=p.read_text();marker='Historical **register 1** warrants specified descent;'
assert b.count(marker)==1
cw='The [Chinese rectification case](HISTORICAL-BRANCHES.md#chinese-rectification-of-names) **qualifies** the account through a political sequence from names and speech to affairs, ritual and punishment. Its consequences return to the persons who must act under the designation. Analects 13.15 distinguishes sound counsel from bad counsel protected against contradiction. E4 requires the return to reach the governing office; that Argued requirement retains its difference from the received text and supplies no new lexical translation for Trust.'
b=b.replace(marker,cw+'\n\n'+'\n\n'.join(whole)+'\n\n'+marker)
p.write_text(b)
(d/'three-case-integration.json').write_text(json.dumps({'status':'three-case-canonical-integration; Sanskrit/Hebrew pending','proposal_paths':[str(ch)]+[f'working/p2-enrichment/page-packets/T22-E4-{label}-case-proposal.md' for label in ['Arabic','Egyptian']],'owned_outputs':[str(h),str(p)],'consumer_proposals':'A15/C27 Chinese; A15/A23 Arabic; C21 Egyptian; exact reverse insertions remain parent-owned','cardinalities':'three terms; four operations; five independent comparison cases; first three now integrated'},indent=2)+'\n')
