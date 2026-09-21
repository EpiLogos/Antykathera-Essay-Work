#!/usr/bin/env python3
"""Build the authorised whole-pass candidate without changing any source lane."""
from __future__ import annotations
import argparse, hashlib, html, importlib.util, json, os, re, subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import quote, unquote
import mistune
KEYS=['s01','s0','s1','s2','s3','s4','s5','s50']
WAVE=Path('working/manuscript-source-enrichment-2026-09-20')
INPUT_REF='19a1d5d58a104ed27359d952aff6e7edc781816a'
SOURCE_PIN='26e42cbbbaa795ecc7dcc480a10c40393f5a8352'
REPO='EpiLogos/Antykathera-Essay-Work'
DATE='2026-09-22'
EXPECTED={
's01':('76bd1a770cc86d64ac8944ba61bea29e5a8f8aa7','d4c94bab369de836253277e873e98d00b9bebc70','dac3983b67e3d6b7b4cee346d7ce0c1b0055a658d19fe0222facb77be8ea1f53'),
's0':('0b6ee55ad6ba927eeccfc77fdef29dd84abed4fb','d8c49cda75a76c19ac08f48e142e51b54de00dca','4f7a201d54448322d63a60b787865f907f7e8bd4c16805ce2ad5e3e04143687f'),
's1':('fc3dfb01a51520242730c69fc99700f1913e88f1','cedf4a7681ac6869152baec75ad35010cf1a9b1e','f3efb9957632880d2257c2c9a7307777695d64cc0f630f0a8ff5925d5f851ce2'),
's2':('3d6bb1e130fe3b661f72018bdfd8a134a1e54683','0d8ea05264a0bb804a80e93eab1fd59b9c3c55e3','b9d6e8b27f67af0e05f1613815421cf3d381670708d3a923d9af75cd7f416e4b'),
's3':('3e3671f937a5a27884ec4dffeedef2dff9196d44','066355fcfa278f60679c275867e3381cd38a748e','3bde426da89e3f6685a8026d78b3487fb0cbc90a18e55b7d07cdb6d675f6a5ec'),
's4':('d908662b307a4bf1466cb2449b232405a3880d89','a3b8d2ab6720f62f9c190ad92bf7804d3452d225','0c0b1da20be705432b1bd6776ace7de9e116c5737260caa258e0b0fa82e55a7f'),
's5':('ba240c276b9aa5aa18bee0f774c336af941484b9','34d7f0680a5fd6686eea5a7a5fec1fcc24541721','170fcaec0d942bc1aadb38017cb900b8a815bd5be7075f90ae7c53e1a3ba6ab1'),
's50':('7cd656c36aa3f76d87699b5ae18698b00da304d3','72d5fd19cb0f1d05da25f8737425010862ec5491','d2d8dc1390338babc25290d2cd2e7f154cf2746c021b0264e18f51ca24799e12')}
TITLES={'s01':'§0/1 — The Integral Threshold','s0':'§0 — Differentiating Mind','s1':'§1 — The Return of Zero','s2':'§2 — Two Logics of Two','s3':'§3 — Mathematical Substrate','s4':'§4 — Psychoid Flowering','s5':'§5 — Objective Internality and Agentic Research','s50':'§5→0 — Epi-Logos and the Instrument’s Return'}
MATH=re.compile(r'\$\$([\s\S]*?)\$\$|(?<!\\)\$([^$\n]+?)(?<!\\)\$')
REPRISE=re.compile(r'<!-- reprise:([^: ]+):start \| (.*?) -->\n([\s\S]*?)<!-- reprise:\1:end -->')
NOTE=re.compile(r'^\[\^([^\]]+)\]:[ \t]*(.*)',re.M)
LINK=re.compile(r'(?<!!)\[([^\]\n]+)\]\(([^)\n]+)\)')
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def dump(p,v):save(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def read(p):return p.read_text(encoding='utf-8')
def parts(t):
    matches=list(NOTE.finditer(t));assert matches,'No source notes'
    body=t[:matches[0].start()]
    body=re.split(r'^## (?:Source notes|Notes)\s*$',body,flags=re.M)[0].rstrip()
    body=re.sub(r'\n---\s*$','',body).rstrip();notes={}
    for i,m in enumerate(matches):
        key=m.group(1);assert key not in notes,('duplicate note',key)
        end=matches[i+1].start() if i+1<len(matches) else len(t)
        notes[key]=re.split(r'\n### §',t[m.start(2):end])[0].strip()
    return body,notes
def math_normalize(t):
    chunks=re.split(r'(`+[^`\n]*`+)',t)
    for i in range(0,len(chunks),2):
        chunks[i]=re.sub(r'\\\[\s*([\s\S]*?)\s*\\\]',lambda m:'$$\n'+m.group(1)+'\n$$',chunks[i])
        chunks[i]=re.sub(r'\\\((.*?)\\\)',lambda m:'$'+m.group(1)+'$',chunks[i])
    return ''.join(chunks)
def count_words(t):
    t=parts(t)[0] if NOTE.search(t) else t
    t=re.sub(r'<!--.*?-->|<[^>]+>','',t,flags=re.S)
    t=re.sub(r'^#{1,6}[^\n]*','',t,flags=re.M)
    t=re.sub(r'\[\^[^\]]+\]','',t);t=LINK.sub(lambda m:m.group(1),t)
    t=re.sub(r'\\[A-Za-z]+',' ',t)
    return len(re.findall(r"\b\w+(?:[’'–-]\w+)*\b",t))
def movement_ids(t):return [f'M{int(n):02d}' for n in re.findall(r'<a id="M(\d+)"',t)]
def structural(k,body):
    body=re.sub(r'^#{1,3}\s+§[^\n]*\n?','',body,count=1,flags=re.M).strip()
    body=re.sub(r'^#{2,3}\s+','### ',body,flags=re.M)
    wanted=[f'M{i:02d}' for i in range(KEYS.index(k)*6+1,KEYS.index(k)*6+7)]
    for mid in wanted:
        if f'<a id="{mid}"></a>' in body:continue
        num=int(mid[1:]);found=None
        for pat in [rf'<!--\s*(?:movement:)?{mid}\b[^>]*-->',rf'<a id="{k}-m{num}(?:-[^"]*)?"></a>']:
            found=re.search(pat,body)
            if found:break
        assert found,('missing movement',k,mid)
        body=body[:found.start()]+f'<a id="{mid}"></a>\n'+body[found.start():]
    assert movement_ids(body)==wanted,(k,movement_ids(body))
    return f'## {TITLES[k]}\n\n'+body+'\n'
def rebase_links(root,k,t,problems):
    origin=root/WAVE/'sections'/k
    def fn(m):
        label,url=m.groups()
        if url.startswith(('http:','https:','mailto:','#','data:')):return m.group()
        dest,sep,frag=url.partition('#');p=(origin/unquote(dest)).resolve()
        try:rel=p.relative_to(root.resolve())
        except ValueError:problems.append({'section':k,'link':url,'reason':'outside repository'});return m.group()
        if not p.exists():problems.append({'section':k,'link':url,'resolved':str(rel),'reason':'missing inherited target'})
        return f'[{label}](https://github.com/{REPO}/blob/{SOURCE_PIN}/{quote(str(rel),safe="/")}{sep}{frag})'
    return LINK.sub(fn,t)
def baseline(root,k):
    p=root/WAVE/'baseline'/('s5-source-container.md' if k=='s5' else k+'.md');b=p.read_bytes();t=b.decode()
    if k=='s5':t=t[t.index('<a id="section-s5-objective-internality"'):t.index('<a id="section-s50-instrument-returns"')]
    return b,t
CSS=r'''
:root{color-scheme:light dark;--paper:#f6f4ee;--ink:#242723;--muted:#63675f;--rule:#d6d9ce;--accent:#426353;--wash:#e9ede5;font-size:16px}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Georgia,"Iowan Old Style","Palatino Linotype",serif}a{color:var(--accent);text-underline-offset:.19em}button,summary,nav,.kicker,.toolbar,.metadata,.note-label{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button{border:1px solid var(--rule);background:transparent;color:var(--ink);border-radius:5px;padding:.48em .7em;cursor:pointer;font-size:.8rem}button:hover{background:var(--wash)}.toolbar{position:sticky;top:0;z-index:6;padding:.65rem 1.2rem;background:var(--paper);border-bottom:1px solid var(--rule);display:flex;gap:.5rem;align-items:center;flex-wrap:wrap;font-size:.78rem}.brand{margin-right:auto;color:var(--muted)}.layout{display:grid;grid-template-columns:245px minmax(0,1fr)}nav{position:sticky;top:65px;align-self:start;height:calc(100vh - 75px);overflow:auto;padding:2.7rem 1.3rem;font-size:.79rem;line-height:1.5}nav a{display:block;text-decoration:none;margin:0 0 1rem}nav .nav-notes{border-top:1px solid var(--rule);padding-top:1rem}main{width:100%;max-width:900px;padding:4rem 3.2rem 7rem;margin:auto}.title-page{margin:0 0 5rem}.kicker{text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;color:var(--muted)}h1{font-weight:400;font-size:clamp(2.8rem,6vw,4.9rem);line-height:1.07;letter-spacing:-.04em;margin:1.15rem 0}.subtitle{font-size:1.35rem;line-height:1.6}.metadata{color:var(--muted);font-size:.76rem;line-height:1.6}.author{margin:2rem 0}.essay-section{font-size:1.21rem;line-height:1.78}.essay-section+section{margin-top:5rem}h2{font-weight:400;font-size:2rem;line-height:1.24;margin:0 0 2.2rem;padding-top:1rem;border-top:1px solid var(--rule)}h3{font-weight:400;font-size:1.44rem;line-height:1.35;margin:3rem 0 1.3rem}p{margin:0 0 1.18em}strong{font-weight:600}blockquote{margin:1.6rem 0;padding:.2rem 1.4rem;border-left:2px solid var(--accent)}pre{overflow:auto;font-size:.86rem;line-height:1.55;padding:1rem;background:var(--wash)}code{font-size:.81em;overflow-wrap:anywhere}a[id],section[id],li[id]{scroll-margin-top:6rem}.note-call{line-height:0;font-size:.62em;vertical-align:super;margin-left:.1em}.note-call a{text-decoration:none;padding:.1em}.math-display{overflow-x:auto;overflow-y:hidden;padding:1.1rem .15rem;margin:.4rem 0 1.5rem;text-align:center;font-size:1.1rem}.math-inline{white-space:normal}math{font-family:"Cambria Math","STIX Two Math",math}.reprise{margin:1.1rem 0 1.6rem;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:.6rem 0}.reprise summary{font-size:.78rem;line-height:1.5;color:var(--muted);cursor:pointer;list-style-position:outside;margin-left:1.05rem}.reprise[open] summary{margin-bottom:1.2rem}.reprise-body{padding:.25rem .2rem 0}.reprise-badge{display:block;font-size:.68rem;font-weight:400;margin-top:.15rem;color:var(--muted)}.notes{font-size:.88rem;line-height:1.7;margin-top:6rem;overflow-wrap:anywhere}.notes h3{font-size:1.2rem;margin:2rem 0 1rem}.notes ol{padding-left:2.4rem}.notes li{padding-left:.4rem;margin-bottom:1.2rem}.note-back{font-family:system-ui;font-size:.74rem;white-space:nowrap}.notes li p{margin:0}.notes code{word-break:break-word}hr{border:0;border-top:1px solid var(--rule);margin:2rem 0}table{border-collapse:collapse;font-size:.84em;width:100%;margin:1.3rem 0}td,th{text-align:left;padding:.45rem;border-bottom:1px solid var(--rule);vertical-align:top}.hidden,[hidden]{display:none!important}.note-pop{position:fixed;inset:auto 1rem 1rem auto;width:min(620px,calc(100vw - 2rem));max-height:60vh;overflow:auto;background:var(--paper);color:var(--ink);border:1px solid var(--rule);box-shadow:0 8px 45px #0003;padding:1.3rem 1.5rem;z-index:20;font-size:.92rem;line-height:1.65}.note-pop button{float:right;margin:0 0 .5rem .7rem}.note-pop p{overflow-wrap:anywhere}.standalone-help{display:none}.standalone .standalone-help{display:block}.standalone main{padding-top:2.4rem}.standalone .title-page{margin-bottom:2rem}.change{font-size:.95rem;margin:2rem 0}.change h3{margin:0 0 .6rem}.change pre{white-space:pre-wrap;overflow-wrap:anywhere}.change .reason{font-family:system-ui;font-size:.84rem}.print-only{display:none}
@media(prefers-color-scheme:dark){:root{--paper:#171b19;--ink:#e2e4dc;--muted:#a6afa6;--rule:#37423a;--accent:#a9cbb5;--wash:#222b25}}html[data-theme=light]{color-scheme:light;--paper:#f6f4ee;--ink:#242723;--muted:#63675f;--rule:#d6d9ce;--accent:#426353;--wash:#e9ede5}html[data-theme=dark]{color-scheme:dark;--paper:#171b19;--ink:#e2e4dc;--muted:#a6afa6;--rule:#37423a;--accent:#a9cbb5;--wash:#222b25}
@media(max-width:1050px){.layout{grid-template-columns:185px minmax(0,1fr)}nav{padding:2rem 1rem;font-size:.74rem}main{padding:3rem 2rem 6rem}}@media(max-width:760px){.layout{display:block}nav{display:none;position:fixed;left:0;right:0;top:var(--toolbar-height,55px);height:auto;max-height:75vh;background:var(--paper);z-index:8;border-bottom:1px solid var(--rule);padding:1.5rem}body.show-nav nav{display:block}main{padding:2.5rem 1.3rem 5rem}.essay-section{font-size:1.11rem;line-height:1.73}h2{font-size:1.7rem}h3{font-size:1.3rem}.title-page{margin-bottom:3rem}.toolbar{padding:.5rem .7rem;gap:.35rem}.brand{display:none}.math-display{font-size:.97rem}.notes{font-size:.85rem}h1{font-size:3rem}}
@media print{:root{color-scheme:light;--paper:white;--ink:black;--muted:#444;--rule:#bbb;--accent:#222;--wash:#eee}.toolbar,nav,.note-pop,.no-print{display:none!important}.layout{display:block}main{max-width:none;padding:0}.essay-section{font-size:11pt;line-height:1.55}h1{font-size:32pt}.essay-section{page-break-before:always}h2,h3{break-after:avoid}.math-display,blockquote{break-inside:avoid}a{color:inherit;text-decoration:none}.notes{font-size:8pt}.title-page{margin-bottom:1cm}.print-only{display:block}}
'''
JS=r'''
const root=document.documentElement;let notePop=null;const sections=[...document.querySelectorAll('section.essay-section')];
function closeNote(){if(notePop)notePop.remove();notePop=null;}
document.addEventListener('click',e=>{const a=e.target.closest('a[data-note]');if(!a)return;e.preventDefault();closeNote();const li=document.getElementById(a.dataset.note);notePop=document.createElement('aside');notePop.className='note-pop';notePop.setAttribute('role','dialog');notePop.setAttribute('aria-label','Source note');notePop.innerHTML='<button type="button" aria-label="Close source note">Close</button>'+li.innerHTML;notePop.querySelector('button').onclick=closeNote;document.body.appendChild(notePop);notePop.querySelector('button').focus()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeNote()});
function setView(standalone,update=true){document.body.classList.toggle('standalone',standalone);sections.forEach(s=>s.hidden=standalone&&s.dataset.section!=='s5');document.querySelectorAll('.note-group').forEach(s=>s.hidden=standalone&&s.dataset.section!=='s5');document.querySelectorAll('nav a[data-section]').forEach(a=>a.hidden=standalone&&a.dataset.section!=='s5');document.querySelectorAll('details.reprise').forEach(d=>d.open=standalone);document.getElementById('view').textContent=standalone?'Read whole manuscript':'Read §5 alone';document.getElementById('expand').textContent=standalone?'Fold reprises':'Expand reprises';if(update){const u=new URL(location.href);if(standalone)u.searchParams.set('section','s5');else u.searchParams.delete('section');try{history.replaceState(null,'',u)}catch(e){};document.getElementById(standalone?'section-s5':'top').scrollIntoView();}}
document.getElementById('view').onclick=()=>setView(!document.body.classList.contains('standalone'));
document.getElementById('expand').onclick=()=>{const ds=[...document.querySelectorAll('details.reprise')];const open=ds.some(d=>!d.open);ds.forEach(d=>d.open=open);document.getElementById('expand').textContent=open?'Fold reprises':'Expand reprises'};
document.getElementById('menu').onclick=()=>document.body.classList.toggle('show-nav');document.querySelectorAll('nav a').forEach(a=>a.onclick=()=>document.body.classList.remove('show-nav'));
document.getElementById('theme').onclick=()=>{const dark=root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;root.dataset.theme=dark?'light':'dark'};
let prior=[];window.addEventListener('beforeprint',()=>{prior=[...document.querySelectorAll('details.reprise')].map(d=>d.open);document.querySelectorAll('details.reprise').forEach(d=>d.open=true)});window.addEventListener('afterprint',()=>document.querySelectorAll('details.reprise').forEach((d,i)=>d.open=prior[i]));
setView(new URL(location.href).searchParams.get('section')==='s5',false);
new ResizeObserver(()=>root.style.setProperty('--toolbar-height',document.querySelector('.toolbar').offsetHeight+'px')).observe(document.querySelector('.toolbar'));
'''
def build(root,draft=False):
    out=root/WAVE/'assembly';out.mkdir(exist_ok=True);inputs=[];source_texts={};protected={}
    for k in KEYS:
        p=root/WAVE/'sections'/k/'SECTION.md';b=p.read_bytes();c,g,h=EXPECTED[k]
        assert(blob(b),sha(b))==(g,h),('input changed',k)
        status=json.loads(read(p.with_name('STATUS.json')));rb,bt=baseline(root,k)
        inputs.append(dict(key=k,path=str(p.relative_to(root)),read_ref=INPUT_REF,prose_commit=c,git_blob=g,sha256=h,bytes=len(b),reported_state=status['state'],baseline_path=str(WAVE/'baseline'/('s5-source-container.md' if k=='s5' else k+'.md')),baseline_blob=blob(rb),baseline_sha256=sha(rb),baseline_body_words=count_words(bt),submitted_body_words=count_words(b.decode())))
        source_texts[k]=b.decode();protected[str(p.relative_to(root))]=h
    spec=importlib.util.spec_from_file_location('editorial_revisions',out/'editorial_revisions.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    revised=mod.texts;edits=mod.edits;assert mod.initial==source_texts
    normalized={};notes={};link_problems=[];migration={};note_sections={}
    for k in KEYS:
        t=math_normalize(revised[k]);body,ns=parts(t);m={old:(old if old.startswith(k+'-') else k+'-'+old) for old in ns};migration[k]=m
        t=re.sub(r'\[\^([^\]]+)\]',lambda q:'[^'+m.get(q.group(1),q.group(1))+']',t)
        body,ns=parts(t);body=structural(k,body);body=rebase_links(root,k,body,link_problems);ns={n:rebase_links(root,k,v,link_problems) for n,v in ns.items()}
        calls=re.findall(r'\[\^([^\]]+)\]',body);assert set(calls)==set(ns),(k,'note mismatch',set(calls)^set(ns));assert not set(ns)&set(notes)
        normalized[k]=body;notes.update(ns);note_sections.update({n:k for n in ns})
        inputs[KEYS.index(k)]['assembled_body_words']=count_words(body);inputs[KEYS.index(k)]['continuous_body_words']=count_words(REPRISE.sub('',body))
    order=list(dict.fromkeys(n for k in KEYS for n in re.findall(r'\[\^([^\]]+)\]',normalized[k])));numbers={n:i+1 for i,n in enumerate(order)}
    manuscript='# The Return of Zero\n\nFrank G. Taylor\n\n<!-- Whole-manuscript model-composed candidate; 22 September 2026. Authorial acceptance pending. -->\n\n'
    for k in KEYS:manuscript+=f'<!-- section:{k}:start -->\n\n<a id="section-{k}"></a>\n\n'+normalized[k]+f'\n<!-- section:{k}:end -->\n\n'
    manuscript+='## Notes\n\n'
    for k in KEYS:
        manuscript+='### '+TITLES[k]+'\n\n'
        for n in order:
            if note_sections[n]==k:manuscript+=f'[^{n}]: {notes[n]}\n\n'
    save(out/'THE-RETURN-OF-ZERO.md',manuscript.rstrip()+'\n')
    canonical=read(out/'THE-RETURN-OF-ZERO.md');parsed={k:re.search(rf'<!-- section:{k}:start -->\n([\s\S]*?)<!-- section:{k}:end -->',canonical).group(1).strip() for k in KEYS}
    _,canonical_notes=parts(canonical);assert canonical_notes==notes
    math_items={}
    for t in list(parsed.values())+list(notes.values()):
        for m in MATH.finditer(t):
            tex=(m.group(1) if m.group(1)is not None else m.group(2)).strip();display=m.group(1)is not None;key=sha((str(display)+'\0'+tex).encode());math_items[key]={'tex':tex,'display':display}
    cache_path=out/'MATHML.json';cache=json.loads(read(cache_path)) if cache_path.exists() else {};missing={k:v for k,v in math_items.items() if k not in cache}
    if missing:
        module=os.environ.get('ROZ_KATEX_MODULE')
        if module:
            node="const fs=require('fs'),k=require(process.argv[1]);const x=JSON.parse(fs.readFileSync(0,'utf8'));const o={};for(const [id,v] of Object.entries(x))o[id]=k.renderToString(v.tex,{displayMode:v.display,output:'mathml',throwOnError:true,strict:'ignore',trust:false});process.stdout.write(JSON.stringify(o));"
            result=subprocess.run(['node','-e',node,module],input=json.dumps(missing),text=True,capture_output=True,check=True);cache.update(json.loads(result.stdout));dump(cache_path,cache)
        elif not draft:raise RuntimeError('MathML cache missing; set ROZ_KATEX_MODULE to katex 0.16.22, or use --draft-render for an explicitly provisional preview.')
    assert draft or all(k in cache for k in math_items)
    md=mistune.create_markdown(escape=False,plugins=['table','strikethrough']);ref_counts=Counter();backrefs={n:[] for n in order};rendered_source={}
    def fragment(t):
        slots={}
        def math_sub(m):
            tex=(m.group(1) if m.group(1)is not None else m.group(2)).strip();display=m.group(1)is not None;key=sha((str(display)+'\0'+tex).encode())
            value=cache.get(key,'<code class="unrendered-math">'+html.escape(tex)+'</code>');token='ROZMATHPLACEHOLDER'+str(len(slots))+'Z';tag='div' if display else 'span';cls='math-display' if display else 'math-inline'
            slots[token]=f'<{tag} class="{cls}" data-math-key="{key}">{value}</{tag}>';return '\n\n'+token+'\n\n' if display else token
        t=MATH.sub(math_sub,t)
        def note_sub(m):
            n=m.group(1);ref_counts[n]+=1;rid=f'ref-{n}-{ref_counts[n]}';backrefs[n].append(rid)
            return f'<sup class="note-call" id="{rid}"><a href="#note-{n}" data-note="note-{n}" aria-label="Source note {numbers[n]}">{numbers[n]}</a></sup>'
        t=re.sub(r'\[\^([^\]]+)\]',note_sub,t);result=md(t)
        for token,value in slots.items():result=result.replace('<p>'+token+'</p>',value).replace(token,value)
        return result
    def body_render(t):
        bits=[];a=0
        for m in REPRISE.finditer(t):
            bits.append(fragment(t[a:m.start()]));name,title,inner=m.groups()
            bits.append(f'<details class="reprise" id="reprise-{name}"><summary>{html.escape(title)}<span class="reprise-badge">Earlier development retained for standalone reading</span></summary><div class="reprise-body">'+fragment(inner)+'</div></details>');a=m.end()
        bits.append(fragment(t[a:]));return ''.join(bits)
    sections=[]
    for k in KEYS:
        sections.append(f'<section class="essay-section" id="reading-{k}" data-section="{k}">'+body_render(parsed[k])+'</section>');rendered_source[k]=sha(parsed[k].encode())
    note_html=['<section class="notes" id="notes"><h2>Notes</h2><p class="metadata">Notes retain whole-manuscript numbering in the §5 standalone view. Source-specific edition and publication limits remain attached to the claims they qualify.</p>']
    for k in KEYS:
        note_html.append(f'<div class="note-group" data-section="{k}"><h3>{html.escape(TITLES[k])}</h3><ol>')
        for n in order:
            if note_sections[n]!=k:continue
            backlinks=' '.join(f'<a href="#{rid}" aria-label="Return to reference {j+1}">↩{j+1 if len(backrefs[n])>1 else ""}</a>' for j,rid in enumerate(backrefs[n]))
            note_html.append(f'<li id="note-{n}" value="{numbers[n]}">'+fragment(notes[n])+f' <span class="note-back">{backlinks}</span></li>')
        note_html.append('</ol></div>')
    note_html.append('</section>')
    nav=''.join(f'<a href="#section-{k}" data-section="{k}">{html.escape(TITLES[k])}</a>' for k in KEYS)
    title='<header class="title-page" id="top"><div class="kicker">Whole-manuscript candidate · 22 September 2026</div><h1>The Return<br>of Zero</h1><p class="author">Frank G. Taylor</p><p class="subtitle">Eight sections, read as one work.</p><p class="metadata">The third relational pass over the source-led section submissions.<br>Authorial acceptance and final publication clearance remain open.</p><p class="metadata standalone-help">§5 is shown from the same canonical text. Its grounding, lens and narrative reprises are expanded for this reading.</p></header>'
    reader='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>The Return of Zero — Whole-manuscript candidate</title><style>'+CSS+'</style></head><body><div class="toolbar"><span class="brand">THE RETURN OF ZERO</span><button id="menu">Contents</button><button id="view">Read §5 alone</button><button id="expand">Expand reprises</button><button id="theme">Light / dark</button></div><div class="layout"><nav aria-label="Manuscript contents">'+nav+'<a class="nav-notes" href="#notes">Notes</a><a href="THE-RETURN-OF-ZERO.md">Editable Markdown</a><a href="WHOLE-PASS-CHANGES.html">Whole-pass changes</a></nav><main>'+title+''.join(sections)+''.join(note_html)+'<footer class="metadata"><hr>Input snapshot '+INPUT_REF[:12]+' · Source snapshot '+SOURCE_PIN[:12]+'<br>The submitted section files and sovereign manuscript are preserved.</footer></main></div><script>'+JS+'</script></body></html>\n'
    ids=re.findall(r'\bid="([^"]+)"',reader);assert len(ids)==len(set(ids)),('duplicate HTML IDs',[x for x,c in Counter(ids).items() if c>1])
    internal=re.findall(r'href="#([^"]+)"',reader);assert not(set(internal)-set(ids)),('unresolved HTML anchors',set(internal)-set(ids))
    assert movement_ids(canonical)==[f'M{i:02d}' for i in range(1,49)]
    assert not re.search(r'\b(?:TODO|TBD|FIXME)\b',canonical)
    assert 'instrument panel with which' not in canonical
    assert canonical.index('What is it that knows?')<canonical.rindex('What is it that knows?')
    save(out/'THE-RETURN-OF-ZERO.html',reader)
    dump(out/'WHOLE-PASS-EDITS.json',{'input_ref':INPUT_REF,'source_pin':SOURCE_PIN,'edits':edits})
    rows=''.join('<tr><td>'+html.escape(TITLES[i['key']])+'</td><td>'+str(i['baseline_body_words'])+'</td><td>'+str(i['submitted_body_words'])+'</td><td>'+str(i['assembled_body_words'])+'</td><td>'+str(i['continuous_body_words'])+'</td></tr>' for i in inputs)
    changes='<h1>Whole-pass changes</h1><p>The selected baseline, submitted section and assembled candidate are counted by one method. Counts describe extent, not literary quality. Full candidate counts retain every controlled reprise; continuous reading counts omit only those explicitly expandable §5 blocks.</p><table><thead><tr><th>Section</th><th>Baseline</th><th>Submitted</th><th>Full candidate</th><th>Continuous reading</th></tr></thead><tbody>'+rows+'</tbody></table>'
    for e in edits:changes+=f'<article class="change"><h3>{html.escape(e["id"])} · {html.escape(e["section"])}</h3><p class="reason">{html.escape(e["reason"])}</p><details><summary>Exact before / after</summary><h4>Before</h4><pre>{html.escape(e["old"])}</pre><h4>After</h4><pre>{html.escape(e["new"])}</pre></details></article>'
    save(out/'WHOLE-PASS-CHANGES.html','<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Whole-pass changes</title><style>'+CSS+'</style></head><body><main><p><a href="THE-RETURN-OF-ZERO.html">Return to the manuscript</a></p>'+changes+'</main></body></html>\n')
    check={'input_hashes_match':True,'movements':movement_ids(canonical),'note_definitions':len(notes),'note_calls':sum(ref_counts.values()),'note_id_migration':migration,'html_ids_unique':True,'internal_links_resolve':True,'controlled_reprises':[x[0] for x in REPRISE.findall(canonical)],'math_expressions':len(math_items),'static_mathml_complete':all(k in cache for k in math_items),'relative_link_problems':link_problems,'rendered_section_source_sha256':rendered_source,'draft_render':draft};dump(out/'CHECKS.json',check)
    for rel,h in protected.items():assert sha((root/rel).read_bytes())==h,('protected lane changed',rel)
    outputs={}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name not in {'ASSEMBLY-MANIFEST.json','ADMISSION-CHECK-2026-09-21.md','editorial-edits.json','whole-pass-edits.json'}:
            b=p.read_bytes();outputs[p.name]={'sha256':sha(b),'git_blob':blob(b),'bytes':len(b)}
    manifest={'edition_date':DATE,'standing':'Model-composed whole-manuscript candidate; authorial acceptance pending','input_ref':INPUT_REF,'source_pin':SOURCE_PIN,'branch':'codex/manuscript-source-enrichment-2026-09-20','inputs':inputs,'outputs':outputs,'editorial_operations':len(edits),'mathematical_renderer':'KaTeX 0.16.22, static MathML only; no bundled fonts','markdown_renderer':'Mistune '+mistune.__version__,'body_count_method':'Cut notes; remove HTML/comments, headings, footnote calls and link destinations; remove TeX command names; count Unicode word sequences with internal apostrophes/hyphens. Inline numbers and native notation remain. Identical preprocessing for all three versions.','scope':'Only assembly outputs; original section, baseline, source and sovereign manuscript untouched. s4 admitted with explicitly retained source-audit limits; no status overwritten.','tests':check};dump(out/'ASSEMBLY-MANIFEST.json',manifest)
    print(json.dumps({'sections':len(inputs),'movements':48,'notes':len(notes),'edits':len(edits),'math':len(math_items),'draft':draft,'links_needing_review':link_problems,'words':{k:sum(x[k] for x in inputs) for k in ['baseline_body_words','submitted_body_words','assembled_body_words','continuous_body_words']}},ensure_ascii=False,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--draft-render',action='store_true');a=p.parse_args();build(a.root,a.draft_render)
