"""Apply the explicitly released, bounded source apparatus pass; never rewrite prose.

Books witnesses with unregistered rights retain locator-only standing. The source
patches contain bibliographic/locator derivatives, never copied book pages.
"""
from pathlib import Path
import hashlib, json, os, re
import yaml

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
BANK=ROOT/'submission-package/essay/symbolon/episteme/sources'
DATE='2026-10-04'
changes=[]
protected={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
           for p in list(WORK.glob('M0*-REWRITE.md'))+[WORK/'500-word-essay-abstract']}

def save(path,text,kind):
    before=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text)
    changes.append({'path':str(path.relative_to(ROOT)),'operation':kind,'preimage_sha256':before,
                    'postimage_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})

def consumer(path,movement,note):
    f=WORK/(movement+'-REWRITE.md')
    return f'Current working [{movement}]({os.path.relpath(f,path.parent)}) note `{note}`. This is a final-read draft consumer; no accepted manuscript or movement body is changed.'

def card(path,sid,number,title,locator,topic,qualifier,movement,note,provenance,status='locator-verified; acquisition required before quotation admission'):
    pid=f'{sid}-p{number:03d}'
    return f'\n<a id="{pid}"></a>\n### {pid} — {title}\n\n**Locator:** {locator}.\n\n**Located operation:** {topic}\n\n**Context and use boundary:** {qualifier}\n\n**Status:** {status}.\n\n**Provenance:** {provenance}\n\n**Relation:** source-specific locator support; the essay\'s philosophical continuation remains authorial.\n\n**Consumer:** {consumer(path,movement,note)}\n'

JUNG=[
 ('cw6','jung-1976-psychological-types-cw6','Psychological Types',1976,'Hull revision of the H. G. Baynes translation; first Princeton/Bollingen paperback printing, with corrections, 1976. Copyright 1971.','Princeton University Press','6',[
  ('Individuation and collective relations','¶758; user-local PDF page 409','Prevention by collective levelling and the distinction between individuation and isolation are located together.','Jung describes intensified collective relations. This passage does not license a rejection of collective standards as such.','M04','s01-jung-individuation'),
  ('Symbol and sign','¶814, Definition 51, Symbol; user-local PDF page 430','The best possible formulation of a relatively unknown fact is distinguished from signs denoting a known object.','The railway badge and land-sale token supply the contrasting semiotic examples; the essay\'s symbolon operation remains its own.','M06','s01-jung-symbol')]),
 ('cw8','jung-1975-structure-dynamics-psyche-cw8','The Structure and Dynamics of the Psyche',1975,'Second edition copyright 1969; third printing with corrections, 1975, as recorded in the consulted copyright page.','Princeton University Press','8',[
  ('The archetype and its representations','¶417, On the Nature of the Psyche; user-local PDF pages 225–226 (printed pp.213–214)','The irrepresentable basic form, psychoid/ultraviolet analogy and possibility of one factor behind several irrepresentables are located in the same numbered paragraph.','The two-irrepresentables sentence is still ¶417, not ¶418. ¶418 begins on PDF page 227 (print p.215). Jung names the model an analogy and hypothesis; it is not an independently established identity of psyche and matter.','M06','s01-jung-archetype'),
  ('Mana citation','¶52 n.44; user-local PDF page 75','Jung\'s Codrington-mediated mana reference is located.','The Codrington passage is a mediated witness here; independent anthropological attribution needs Codrington\'s own edition. The further n.123 lead is not newly certified by this card.','M05','s01-mana')]),
 ('cw9i','jung-cw9i-hull-routledge-second-edition','The Archetypes and the Collective Unconscious',None,'The consulted title page identifies second edition, Hull translation, Routledge, London. The visible opening leaves do not establish its printing year; the filename\'s 1981 is not treated as evidence.','Routledge','9, part 1',[
  ('Archetype as formal possibility','¶155; user-local PDF page 90 (printed p.79)','The crystal-axis comparison and formal possibility are located.','Content becomes determinate through conscious experience; the prior formal possibility does not carry a ready-made inherited image. The scan has broken-word OCR, so no quotation transcription is admitted.','M06','s01-jung-archetype'),
  ('Individuation and the whole','¶490; user-local PDF page 286 (printed p.275)','Individuation\'s indivisible whole is located at the opening of Conscious, Unconscious, and Individuation.','Jung distinguishes the ego\'s conscious contents from psychological totality; the essay\'s Subject-pole comparison is separate.','M04','s01-jung-individuation')]),
 ('cw12','jung-1980-psychology-alchemy-cw12','Psychology and Alchemy',1980,'Second edition, completely revised, 1968; first Princeton/Bollingen paperback printing, 1980.','Princeton University Press','12',[
  ('Religious paradox','¶¶18–19; user-local PDF pages 47–48','Paradox, non-contradiction and Tertullian\'s religious certainty are located in their connected discussion.','Jung also discusses the danger of paradoxes taken up without sufficient cultivation. The passage is not an abolition of logical discrimination.','M04','s01-jung-paradox'),
  ('Four determinants and vacillation','¶31; user-local PDF page 56','The minimum four determinants of a whole judgment and recurring alchemical vacillation between three and four are located together.','This reports Jung\'s psychological reading and does not derive QL\'s 4+2 structure.','M06','s01-jung-quaternity')]),
 ('cw13','jung-1983-alchemical-studies-cw13','Alchemical Studies',1983,'Copyright 1967; first Princeton/Bollingen paperback printing, 1983.','Princeton University Press','13',[
  ('Letting things happen','¶20, Commentary on The Secret of the Golden Flower; user-local PDF page 30 (printed p.16)','Wu wei and permitting a fragment of fantasy to develop are located.','The preceding passage warns against turning this into a mechanical recipe. The commentary is Jung\'s psychological reception, not a primary Chinese-text translation.','M04','s01-golden-flower')]),
 ('cw14','jung-1977-mysterium-coniunctionis-cw14','Mysterium Coniunctionis',1977,'Second edition copyright 1970; first Princeton/Bollingen paperback printing, 1977.','Princeton University Press','14',[
  ('Logos and Eros','¶224; user-local PDF page 133','Discrimination/judgment/insight and the capacity to relate are located in Jung\'s own stated gendered comparison.','The following ¶225 immediately discusses counterexamples. The source retains its historical gender schema; the essay\'s two-operation interpretation is not attributed to Jung as a gender-free formulation.','M04','s01-jung-logos-eros'),
  ('The fifth from the four','¶439; user-local PDF page 233','Square, circle and quintessence occur together in the commentary on Ripley\'s vessel and son.','This is an alchemical-symbolic unity relation; QL #5 Quintessence and #5→#0 remain native continuation, not a quoted Jung theorem.','M06','s01-jung-five')]),
 ('cw15','jung-1971-spirit-man-art-literature-cw15','The Spirit in Man, Art, and Literature',1971,'Copyright 1966; first Princeton/Bollingen paperback printing, 1971.','Princeton University Press','15',[
  ('Art and compensation','¶130; user-local PDF page 74','Art\'s educative and compensatory social role is located within the archetypal-image discussion.','Jung describes activation and shaping of an image into a finished work; the author\'s present cultural application is distinct.','M05','s01-jung-art')]),
 ('cw18','jung-1976-symbolic-life-cw18','The Symbolic Life: Miscellaneous Writings',1976,'The consulted volume copyright page runs through 1976 and identifies CW18; the filename\'s 1953 is not a publication date for this volume.','Princeton University Press','18',[
  ('Image and inaccessible original','¶1589, Jung and Religious Belief, Questions to Jung and His Answers, question 3; user-local PDF page 654','God-images and an inaccessible original are located within the answer.','Jung distinguishes his personal conviction from what he can prove as a scientist. This is a different source from the 1959 BBC interview; the Listener letter is not certified by this card.','M04','s01-jung-know')]),
]

for key,sid,title,year,edition,publisher,volume,cards in JUNG:
    witness=json.loads((WORK/'quotation-verification'/(key+'-selected-contexts.json')).read_text())
    path=BANK/'psychology/jung'/sid/(sid+'.md')
    if path.exists():raise RuntimeError(f'Unexpected existing new source: {path}')
    meta={'source_id':sid,'title':f'Jung — {title}, CW {volume} (consulted carrier)',
       'title_full':title,'author':['C. G. Jung'],'translator':['R. F. C. Hull'],
       'publisher':publisher,'year':year,'edition_detail':edition,
       'container_title':f'Collected Works of C. G. Jung, vol. {volume}',
       'primary_domain':'psychology','node_type':'source-house','record_type':'book',
       'ownership':'canonical-source-house','schema_version':1,
       'metadata_status':'title-and-copyright-page-read' if year else 'title-page-read; printing-date-unresolved',
       'edition_status':'consulted-carrier-identified','citation_status':'citation-ready-for-identified-carrier',
       'quote_status':'locator-verified; rights-provenance-unregistered; no-quotation-admitted',
       'citation_style':'chicago-notes-bibliography-18','accessed':DATE,
       'local_copy':witness['witness'],'passage_surface':'#passages','consumed_by_sections':['§0/1']}
    if key=='cw6':meta['translator']=['H. G. Baynes','R. F. C. Hull']
    date=year if year else 'n.d.'
    translation='rev. R. F. C. Hull from H. G. Baynes' if key=='cw6' else 'trans. R. F. C. Hull'
    text='---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---\n'
    text+=f'# {meta["title"]}\n\n## Bibliographic identity and actual carrier\n\n{edition}\n\n**Full note:** C. G. Jung, *{title}*, {translation}, *Collected Works*, vol. {volume} ({publisher}, {date}), {{paragraph}}.\n\n**Short note:** Jung, *{title}*, {{paragraph}}.\n\n**Bibliography:** Jung, C. G. *{title}*. {translation.capitalize()}. *Collected Works*, vol. {volume}. {publisher}, {date}.\n\n## Provenance and standing\n\nThe user-local PDF declared in `local_copy` was opened; title/copyright leaves and the selected passage contexts were read by s01-apparatus on {DATE}. PDF SHA-256: `{witness["sha256"]}`; {witness["pdf_pages"]} digital pages. Digital PDF pages below are **one-based**, not silently converted to print pagination. No complete-book reading is claimed. No sibling NOTES existed; none was created.\n\nThe Books pool is a discovery/locator witness. Its rights provenance is not registered. Under AGENTS.md, this permits locator recovery but **does not admit new quotations or redistribute the PDF**. Located wording can be compared privately with the current draft; quotation readiness remains separate. The source record supplies the actual reference and bounded passage locations, with no equivalence to another printing inferred.\n\n<a id="passages"></a>\n## Passages and excerpts\n'
    prov=f'User-local PDF identified above, SHA-256 `{witness["sha256"]}`; selected page context read with pypdf extraction by s01-apparatus, {DATE}. OCR/text extraction is not a certified quotation transcription; rights provenance remains unregistered.'
    for n,c in enumerate(cards,1):text+=card(path,sid,n,*c,prov)
    save(path,text,'create-source-house')

for sid,rows in [
 ('jung-1969-psychology-religion-cw11',[
 ('Immediate psychic knowledge','¶¶16,18; user-local PDF page 23','The psychic mode of immediate knowledge and the absence of an external Archimedean point are located.','¶17 intervenes with practical examples of imagined conditions having real effects. This does not establish the physical world\'s non-existence.','M02','s01-jung-psyche'),
 ('The psychologically dominant god','¶137; user-local PDF page 75','The strongest psychological value and a god losing effective power are located in the mandala/religion discussion.','The referent is a psychic fact and religious relation; the essay\'s ontological God/Subject identity is separately argued.','M02','s01-jung-god'),
 ('Numinosity','¶6; user-local PDF pages 19–20','Numinosum is discussed as an effect not produced by arbitrary will.','This locates Jung\'s Otto-derived description, not an independent verification of Otto or a proof of divine agency.','M04','s01-numinous'),
 ('Fourfold judgment','¶246; user-local PDF page 140','Quaternity, four orientation functions and completeness are located together.','The account is Jung\'s. Its references to Pythagoras, Buddhism and Schopenhauer remain mediated historical witnesses.','M06','s01-jung-quaternity')]),
 ('jung-1978-aion-cw9-2',[
 ('Shadow and projection','¶¶14,16; 1979 consulted carrier PDF pages 20–21 (printed pp.8–9)','Moral recognition of the shadow and projection onto the other person are located.','Recognition is a task involving resistance and affect; this does not certify every interpersonal conflict as a projection.','M03','s01-aion-shadow'),
 ('Privatio boni in the empirical register','¶¶74–75; 1979 consulted carrier PDF pages 53–54 (printed pp.41–42)','The contrast between theological privation and psychologically effective evil is located.','The source is explicit about the plane of empirical psychology. Metaphysical endorsement remains a different claim.','M05','s01-privatio'),
 ('Antichrist as symbolic compensation','¶¶76–78; 1979 consulted carrier PDF pages 54–55 (printed pp.42–43)','Shadow of the Self, counterstroke and Christian psychological symbolism are located together.','Jung\'s historical-theological reconstruction is an interpretation; it is not independent corroboration of every mediated ancient source.','M05','s01-aion-antichrist'),
 ('Antimimon in two contexts','¶67, PDF page 47 (printed p.35), and continuation of ¶75, PDF page 54 (printed p.42), in the 1979 carrier','The contemporary false-spirit description and the Antichrist-as-imitating-spirit passage have distinct locations.','Do not collapse the two passages or cite ¶75 for the ¶67 list. Greek OCR on page 54 is not a verified transcription.','M05','s01-antimimon'),
 ('Lucifer as a shared symbol','¶127; 1979 carrier PDF page 84 (printed p.72)','The Morning Star is reported as a Christ and devil symbol, in the chapter on fishes.','The note refers to Church Fathers and symbol/allegory; it is not an identity claim about Christ and the devil.','M05','s01-lucifer'),
 ('The central archetype and dualism','Chapter V, n.74; 1979 carrier PDF page 73 (printed p.61)','Jung\'s reply to Victor White stresses unity of the Self.','The footnote distinguishes psychological argument from ecclesiastical metaphysics. It does not establish the essay\'s Śaiva/QL identification.','M06','s01-jung-self')])]:
    path=next(BANK.rglob(sid+'.md'));text=path.read_text()
    marker='## Current §0/1 locator collation — 2026-10-04'
    if marker in text:raise RuntimeError('Already applied')
    key='cw11' if 'cw11' in sid else 'cw9ii'
    wit=json.loads((WORK/'quotation-verification'/(key+'-selected-contexts.json')).read_text())
    text+='\n'+marker+'\n\nThe actual user-local carrier and selected passage contexts were reopened. These additions preserve the existing source identity, passage IDs and historical reading. **Standing is locator-verified only; no new book quotation is admitted while rights provenance is unregistered.** Current working §0/1 consumers remain draft consumers.\n'
    if key=='cw9ii':text+='\nFor these new cards, the consulted carrier is the **1979 Princeton/Bollingen paperback reprint**, ISBN 0-691-01826-X, as its copyright page states. Cite that carrier when using these locators: Jung, *Aion*, 2nd ed., trans. R. F. C. Hull (Princeton University Press, 1979), {paragraph/page}. The house\'s selected 1978 hardcover remains distinct; no independent collation to it is claimed.\n'
    prov=f'Actual declared user-local {"1973 second printing of the 1969 second edition" if key=="cw11" else "1979 paperback reprint"} PDF; SHA-256 `{wit["sha256"]}`; title/copyright and selected contexts read with pypdf by s01-apparatus, {DATE}. Rights provenance unregistered; extraction not a certified quotation transcription.'
    for n,c in enumerate(rows,7 if key=='cw11' else 17):text+=card(path,sid,n,*c,prov)
    if key=='cw11':text+='\n**Existing q001 refinement:** its Sophia/Logos/Śakti comparison is specifically at ¶610, digital PDF page 317. This narrows its already recovered ¶¶609–613 locator; the original card and its source-specific/paraphrase standing are retained.\n'
    save(path,text,'append-locator-cards')

DOCS=[
 ('wired-2026-dialog-exposed','wired',['Dell Cameron','Yulia Almazova'],'Leak Exposes Members of Peter Thiel’s Secretive ‘Dialog’ Society','WIRED','2026-06-16','https://www.wired.com/story/leak-exposes-members-of-peter-thiels-secretive-dialog-society/','Publisher article dated June 16, 2026, 4:21 PM; access 2026-10-04.','Opening six paragraphs; 2026 registration-list paragraph','Reports a leaked invitation-network directory and separately a retreat registration list.','The registration list distinguishes active members and guests. A directory appearance cannot establish membership.','M03','s01-dialog'),
 ('wired-2026-dialog-rankings','wired',['Dell Cameron','Dhruv Mehrotra','Yulia Almazova'],'How the Peter Thiel-Linked Dialog Club Secretly Ranks Its Members','WIRED','2026-06-18','https://www.wired.com/story/how-peter-thiels-private-dialog-club-secretly-ranks-its-members/','Publisher article dated June 18, 2026, 6:12 PM; correction June18, update June19; access 2026-10-04.','Paragraphs distinguishing membership from retreats; grading discussion','Reports staff/algorithm grading and differentiates members from other event participants.','Names in the looser directory include nonmembers. The essay uses offices and sectors; institutional concealment is its own argument.','M03','s01-dialog'),
 ('kinzer-2026-mkultra-house-testimony','kinzer',['Stephen Kinzer'],'Testimony to the Task Force on the Declassification of Federal Secrets','United States House Committee on Oversight and Government Reform','2026-06-30','https://oversight.house.gov/wp-content/uploads/2026/06/Kinzer-Written-Testimony.pdf','Official House-hosted three-page submitted testimony, dated June30 on page1; all three pages read 2026-10-04.','pp.1–3; destruction and financial-record recovery at p.2','The written testimony locates Gottlieb, secrecy, the 1973 destruction and surviving financial records.','This is witness testimony. It does not itself contain the draft’s claim of no prosecution or compensation. Its p.2 discusses possible present research as a question, not an established current programme.','M05','s01-mkultra-2026'),
 ('senate-1977-project-mkultra-hearing','united-states-senate',['United States Senate Select Committee on Intelligence','United States Senate Subcommittee on Health and Scientific Research'],'Project MKULTRA, the CIA’s Program of Research in Behavioral Modification','United States Government Printing Office','1977-08-03','https://www.intelligence.senate.gov/sites/default/files/hearings/95mkultra.pdf','Official Senate-hosted 173-page scan, 95th Congress, first session, August3,1977; selected opening statements and Turner testimony read 2026-10-04.','Kennedy opening statement, print p.3 (PDF page7); Turner prepared statement print pp.4–6 (PDF pages8–10)','Records the 1973 destruction order and the nature of the surviving finance folders.','The recovered folders are not a complete operational archive. This selected read does not separately identify Cameron/Subproject68; do not cite it as verified support for that exact attribution.','M05','s01-mkultra'),
 ('doj-2025-epstein-production-letter','united-states-doj',['Todd Blanche'],'December 19, 2025 Letter to Congress on Epstein Files Production','United States Department of Justice','2025-12-19','https://www.justice.gov/opa/media/1434851/dl','Official DOJ six-page signed letter; all six pages and redaction-process description read 2026-10-04.','pp.1–4, especially p.2 redaction categories and p.3 EFTA Bates-number explanation','Establishes the December19 production, redaction review and EFTA identification scheme.','The Department’s compliance and victim-protection assertions are attributed claims. This letter alone cannot establish selective protection of co-conspirators or every alleged release failure.','M03','s01-epstein-redaction')]

for sid,owner,authors,title,publisher,pubdate,url,prov,locator,topic,boundary,movement,note in DOCS:
    path=BANK/'political-theory-institutions'/owner/sid/(sid+'.md')
    if path.exists():raise RuntimeError('Unexpected existing documentary source')
    meta={'source_id':sid,'title':title,'title_full':title,'author':authors,'publisher':publisher,
      'year':int(pubdate[:4]),'publication_date':pubdate,'url':url,'accessed':DATE,
      'primary_domain':'political-theory-institutions','node_type':'source-house','record_type':'article' if owner=='wired' else 'document',
      'ownership':'canonical-source-house','schema_version':1,'metadata_status':'object-verified',
      'edition_status':'dated-public-object','citation_status':'citation-ready','quote_status':'paraphrase-only',
      'citation_style':'chicago-notes-bibliography-18','passage_surface':'#passages','consumed_by_sections':['§0/1']}
    text='---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True)+'---\n'
    authorstring=', '.join(authors)
    text+=f'# {title}\n\n## Citation and consulted object\n\n**Full note:** {authorstring}, “{title},” {publisher}, {pubdate}, {url}.\n\n**Short note:** {authors[0]}, “{title},” {{locator}}.\n\n**Bibliography:** {authorstring}. “{title}.” {publisher}, {pubdate}. {url}.\n\n**Provenance:** {prov}\n\nThe public object is linked; no full article or PDF is republished. Citation readiness is separate from exact quotation readiness.\n\n<a id="passages"></a>\n## Passages and excerpts\n'
    text+=card(path,sid,1,'Current §0/1 support',locator,topic,boundary,movement,note,prov+' '+url,'paraphrase-only; located context verified')
    if owner=='kinzer':text+='\n**Hearing identity:** [Official hearing page](https://oversight.house.gov/hearing/mind-control-and-accountability-uncovering-the-truth-of-the-cias-mkultra-project/), *Mind Control and Accountability: Uncovering the Truth of the CIA’s MKULTRA Project*, June30,2026, Rayburn2154,10:00AM. The draft’s July1 date and “Experiments” title require author correction. O’Neill and Ginexi are separately listed witnesses; their testimony is not attributed to Kinzer.\n'
    save(path,text,'create-documentary-source-house')

for sid in ['bai-2022-constitutional-ai','bengio-2003-neural-probabilistic-language-model','chalmers-1995-facing-up-consciousness','plato-jowett-phaedrus']:
    p=next(BANK.rglob(sid+'.md'))
    changes.append({'path':str(p.relative_to(ROOT)),'operation':'add-q002-access-provenance',
       'postimage_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})

for rel,sha in protected.items():
    assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha,rel
receipt={'date':DATE,'scope':'released source apparatus only; authorial prose and NOTES preserved',
 'changes':changes,'protected_authorial_inputs':protected,
 'books_status':'real carrier/paragraph locations recovered; rights provenance unregistered, no new quotation admitted',
 'generated_projections':'parent owns one source/room/navigation rebuild after final hashes'}
(WORK/'S01-QUOTATION-SOURCE-PATCH-RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_paths':len(changes),'new_houses':sum(x['operation'].startswith('create') for x in changes),'protected_authorial_inputs':len(protected),'receipt':str(WORK/'S01-QUOTATION-SOURCE-PATCH-RECEIPT.json')},indent=2))
