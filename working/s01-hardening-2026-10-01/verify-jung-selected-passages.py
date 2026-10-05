"""Read selected user-local witnesses; retain only bounded verification contexts.

This never edits sources or authorial text, and never copies a PDF into the repo.
"""
from pathlib import Path
import hashlib, json, re, sys
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
BOOKS = Path('/Users/admin/Documents/Books')
TARGETS = {
 'cw11': ('Volume 11_', ['immediate knowledge is psychic', 'Archimedean point', 'functions as a god', 'logical basis for any whole judgment', 'numinosum', 'Shakti']),
 'cw9ii': ('Volume 9_2', ['moral problem', 'beyond all possibility of doubt', 'Lucifer', 'empirical psychology', 'antimimon', 'complexio oppositorum par excellence', 'very reverse of dualism']),
 'cw6': ('Volume 6_', ['levelling down', 'broader collective relationships', 'relatively unknown fact']),
 'cw8': ('Volume 8 ', ['irrepresentable basic form', 'two or more irrepresentables', 'ultra-violet', 'not fixed in anything']),
 'cw9i': ('Volume 09 Part 1', ['axial system', 'purely formal', 'initial and a terminal', 'in-dividual']),
 'cw12': ('Volume 12_', ['without paradox', 'paradox', 'minimum number']),
 'cw13': ('Volume 13 ', ['letting things happen', 'wu wei', 'Wu wei']),
 'cw14': ('Volume 14 ', ['By Logos', 'Quinta Essentia', 'central fire', 'ignis gehennalis', 'right hand']),
 'cw15': ('Volume 15_', ['educating the spirit of the age', 'inadequacy and one-sidedness']),
 'cw18': ('Volume 18_', ['religious belief', 'conscience', 'beyond all doubt', 'behind these images']),
}

def norm(s):
    s=re.sub(r'([A-Za-z])[-\u2010\u2011]\s*\n\s*([a-z])',r'\1\2',s)
    return re.sub(r'\s+',' ',s).strip()

out=HERE/'quotation-verification'
out.mkdir(exist_ok=True)
for key in sys.argv[1:] or TARGETS:
    lead,phrases=TARGETS[key]
    fs=[p for p in BOOKS.iterdir() if p.is_file() and lead in p.name]
    if len(fs)!=1: raise RuntimeError((key,[str(p) for p in fs]))
    path=fs[0]; reader=PdfReader(path)
    record={'witness':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'pdf_pages':len(reader.pages),'frontmatter':[], 'hits':{p:[] for p in phrases}}
    for i,page in enumerate(reader.pages):
        raw=page.extract_text() or ''
        if i<7:record['frontmatter'].append({'pdf_page_1_based':i+1,'text':raw[:4500]})
        n=norm(raw)
        for p in phrases:
            pos=n.casefold().find(p.casefold())
            if pos<0: continue
            record['hits'][p].append({'pdf_page_1_based':i+1,
                'page_label':reader.page_labels[i] if reader.page_labels else None,
                'context':n[max(0,pos-900):min(len(n),pos+1700)],
                'page_start':n[:180],'page_end':n[-180:]})
    destination=out/(key+'-selected-contexts.json')
    destination.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(key,len(reader.pages),'pages', {p:[h['pdf_page_1_based'] for h in hs] for p,hs in record['hits'].items()},flush=True)
