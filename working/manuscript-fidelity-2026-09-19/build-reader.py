#!/usr/bin/env python3
"""Rebuild the pinned eight-section private reader without changing prose.
Requires Python 3.10+, pandoc 3+, beautifulsoup4. No network is used.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import html
import json
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from bs4 import BeautifulSoup

HOME = Path(__file__).resolve().parent
STYLE = '''
:root{--paper:#faf8f2;--ink:#262a29;--soft:#64706d;--rule:#deded5;--accent:#3e6860;color-scheme:light}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:28px}body{margin:0;background:var(--paper);color:var(--ink);font:19px/1.76 Georgia,'Times New Roman',serif}a{color:var(--accent);text-underline-offset:.2em;overflow-wrap:anywhere}nav{position:fixed;width:260px;inset:0 auto 0 0;overflow:auto;border-right:1px solid var(--rule);padding:35px 24px;background:#f0f1e9;font:14px/1.5 system-ui,sans-serif}nav strong{display:block;font-size:18px;margin-bottom:12px}nav small{display:block;color:var(--soft);margin-bottom:25px}nav a{display:block;color:var(--ink);text-decoration:none;padding:10px 0;border-top:1px solid var(--rule)}button{margin-top:24px;padding:10px;border:1px solid var(--rule);background:transparent;cursor:pointer}main{margin-left:260px;padding:60px;max-width:1040px}header{padding-bottom:40px;border-bottom:1px solid var(--rule)}h1{font-size:52px;line-height:1.15;font-weight:400;letter-spacing:-.03em}h2{font-size:35px;line-height:1.25;font-weight:400;margin:20px 0 34px}h3{font-size:26px;line-height:1.35;font-weight:400;margin:42px 0 20px}h4{font-size:21px}p{margin:0 0 1.15em}.chapter{padding-top:56px;margin-top:35px;border-top:1px solid var(--rule)}.provenance,footer{font:12px/1.6 system-ui,sans-serif;color:var(--soft)}blockquote{margin:25px 0;padding-left:24px;border-left:2px solid var(--accent)}pre{padding:18px;background:#f0f1e9;overflow:auto;font-size:14px;line-height:1.5}code{font-size:.84em}p code{background:#efeee7;padding:2px 4px}table{border-collapse:collapse;font-size:15px;display:block;overflow:auto;margin:25px 0}td,th{border-bottom:1px solid var(--rule);padding:10px;vertical-align:top}th{text-align:left}.footnotes{font-size:14px;line-height:1.65;margin-top:35px}sup{line-height:0;font-size:.7em}math[display=block]{display:block;overflow-x:auto;padding:20px 0;margin:20px 0;font-size:1.1em}.paragraph-mark{display:none;font:10px system-ui;color:var(--soft);float:right;margin-left:8px}.show-ids .paragraph-mark{display:block}footer{margin-top:55px;padding-top:20px;border-top:1px solid var(--rule)}@media(max-width:950px){nav{position:relative;width:auto;border-right:0;border-bottom:1px solid var(--rule);padding:24px}nav .links{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}main{margin-left:0;padding:35px 7vw}body{font-size:18px}h1{font-size:42px}}@media print{nav,.paragraph-mark,button{display:none!important}body{background:white;color:black;font-size:11pt;line-height:1.5}main{margin:0;padding:0;max-width:none}header{break-after:page}.chapter{break-before:page;border:0;padding-top:0}h2{font-size:24pt}h3{font-size:16pt;break-after:avoid}p{orphans:3;widows:3}a{color:inherit;text-decoration:none}.footnotes{font-size:9pt}}
'''

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def github(commit: str, path: str, fragment: str='') -> str:
    return 'https://github.com/EpiLogos/Antykathera-Essay-Work/blob/'+commit+'/'+quote(path,safe='/')+('#'+fragment if fragment else '')

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    manifest=json.loads((HOME/'INPUTS.json').read_text())
    args.out.mkdir(parents=True,exist_ok=True)
    chapters=[]; navigation=[]; paragraphs=[]; warnings=[]; checks=[]
    for item in manifest['selected']:
        key=item['section']; path=item['path']; commit=item['commit']
        data=(args.root/path).read_bytes()
        if blob(data)!=item['blob']:
            raise ValueError('Input changed from the review baseline: '+path)
        md=data.decode('utf-8')
        if key=='s5':
            a=md.index('## §5 — Objective Internality and Agentic Research')
            z=md.index('<a id="section-s50-instrument-returns">',a)
            md=md[a:z].strip()+'\n'
            md=re.sub(r'^(#{2,6}) ',lambda m:m[1][1:]+' ',md,flags=re.M)
        md=re.sub(r'(?m)[ \t]+\^(roz-[A-Za-z0-9_-]+)[ \t]*$',r' <a id="\1"></a>',md)
        run=subprocess.run(['pandoc','--from=markdown+footnotes+tex_math_dollars+tex_math_single_backslash+raw_html','--to=html5','--mathml','--wrap=none'],input=md,text=True,capture_output=True,check=True)
        if run.stderr.strip(): warnings.append({'section':key,'message':run.stderr.strip()})
        soup=BeautifulSoup(run.stdout,'html.parser')
        title=soup.find('h1').get_text(' ',strip=True)
        for tag in soup.find_all(re.compile('^h[1-6]$')):
            tag.name='h'+str(min(6,int(tag.name[1])+1))
        targets={}
        for tag in soup.find_all(id=True):
            old=tag['id']
            if old in targets: raise ValueError('Duplicate input target: '+key+' '+old)
            targets[old]=key+'--'+old;tag['id']=targets[old]
        for tag in soup.find_all(href=True):
            uri=tag['href']
            if uri.startswith('#'):
                tag['href']='#'+targets.get(uri[1:],key+'--'+uri[1:])
            elif not urlsplit(uri).scheme:
                u=urlsplit(uri)
                resolved=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(u.path)))
                tag['href']=github(commit,resolved,u.fragment)
        for attr in ('aria-describedby','aria-labelledby'):
            for tag in soup.find_all(attrs={attr:True}):
                tag[attr]=' '.join(targets.get(v,v) for v in tag[attr].split())
        n=0
        for p in soup.find_all('p'):
            if p.find_parent(class_='footnotes') or not p.get_text(strip=True):continue
            n+=1;pid=f'{key}-p{n:03}'
            if p.get('id'):p.insert(0,soup.new_tag('span',id=p['id']))
            p['id']=pid
            paragraphs.append({'id':pid,'section':key,'path':path,'commit':commit,'blob':item['blob'],'text':p.get_text(' ',strip=True)})
            mark=soup.new_tag('a',href='#'+pid,attrs={'class':'paragraph-mark','aria-label':'Paragraph '+pid});mark.string=pid;p.insert(0,mark)
        chapters.append(f'<article class="chapter" id="{key}"><div class="provenance">{item["movements"]} · <a href="{github(commit,path)}">Exact source draft</a> · {commit[:8]}</div>{soup}</article>')
        navigation.append(f'<a href="#{key}">{html.escape(title)}</a>')
        checks.append({'section':key,'blob_verified':True,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'paragraphs':n,'rendered_notes':len(soup.select('.footnotes > ol > li'))})
    document='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>The Return of Zero — collated manuscript</title><style>'+STYLE+'</style></head><body><nav aria-label="Contents"><strong>The Return of Zero</strong><small>PRIVATE REVIEW COPY<br>19 September 2026</small><div class="links">'+''.join(navigation)+'</div><button type="button" onclick="document.body.classList.toggle(\'show-ids\')">Show / hide paragraph references</button></nav><main><header><div class="provenance">FIRST COMPLETE COLLATION · AUTHORIAL FIDELITY REVIEW</div><h1>The Return of Zero</h1><p>Eight section drafts in their canonical sequence. Their prose is unchanged; collation does not ratify the drafts or resolve their differences, repetitions and source debts.</p></header>'+''.join(chapters)+'<footer>Private reading projection, not a replacement sovereign manuscript or a public release. Source bytes are verified against INPUTS.json. Mechanical changes are confined to heading hierarchy, browser/footnote targets, repository-link resolution and mathematical rendering. The earlier competing opening is preserved as provenance but is not selected. Protected raw sources are not reproduced here.</footer></main></body></html>'
    soup=BeautifulSoup(document,'html.parser');ids=[t['id'] for t in soup.find_all(id=True)]
    duplicate=[k for k,v in collections.Counter(ids).items() if v>1]
    broken=[t['href'] for t in soup.find_all(href=True) if t['href'].startswith('#') and t['href'][1:] not in set(ids)]
    if duplicate or broken:raise ValueError({'duplicate_ids':duplicate,'broken_fragments':broken})
    out=args.out/'The-Return-of-Zero-Collated-2026-09-19.html';out.write_text(document,encoding='utf-8')
    report={'kind':'unaltered-private-manuscript-collation','inputs':checks,'chapters':len(chapters),'paragraphs':len(paragraphs),'mathml_elements':len(soup.find_all('math')),'duplicate_ids':duplicate,'broken_fragments':broken,'warnings':warnings,'html_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'prose_rewritten':False,'sources_changed':False}
    (args.out/'COLLATION-MANIFEST.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (args.out/'PARAGRAPH-MAP.json').write_text(json.dumps(paragraphs,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
