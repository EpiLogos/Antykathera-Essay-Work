"""Build the bounded §0/1 submission from the six movement rewrites.

Outputs, beside the sovereign manuscript in submission-package/essay/:
  CONFRONTING-THE-LIMIT-S01.md    collated section, endnotes and sources by movement
  CONFRONTING-THE-LIMIT-S01.html  standalone reading edition
  CONFRONTING-THE-LIMIT-S01.pdf   print edition (headless Chrome)
With --manuscript it also replaces the §0/1 body and its notes block in
THE-RETURN-OF-ZERO.md, leaving the other seven sections untouched.

Prose is copied verbatim from the M0N-REWRITE.md files. Notes come from
S01-SUBMISSION-NOTES.json (reader-facing Chicago forms of the working notes).
Run with a Python that has markdown-it-py and mdit-py-plugins.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ESSAY = ROOT / "submission-package/essay"
OUT = ESSAY / "CONFRONTING-THE-LIMIT-S01"
MANUSCRIPT = ESSAY / "THE-RETURN-OF-ZERO.md"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TITLE = "Confronting the Limit"
SUBTITLE = "Determination, Subjectivity and Mind as Objective Internality"
AUTHOR = "Frank G. Taylor"
SECTION = "§0/1 — The Integral Threshold"
MAP_URL = "https://oi.epi-logos.org/essay/"
MOVEMENTS = [
    ("M01", "#0", "The Question Before the Mechanism"),
    ("M02", "#1", "Define the Subject Without Making It an Object"),
    ("M03", "#2", "Definition as Cut, Gift, and Danger"),
    ("M04", "#3", "The Formal-Limit Genealogy"),
    ("M05", "#4", "Gebserian Diaphaneity"),
    ("M06", "#5→0", "The Return to Zero"),
]
MARK = re.compile(r"\[\^([^\]]+)\](?!:)")


def prose_of(name: str) -> str:
    text = (HERE / f"{name}-REWRITE.md").read_text()
    anchor = text.index(f'<a id="{name}"></a>')
    body = text[anchor:]
    ends = [m.start() for m in (re.search(r"^\[\^[^\]]+\]:", body, re.M),
                                re.search(r"^---\s*$", body, re.M)) if m]
    body = body[: min(ends)]
    body = re.sub(r'<a id="M0\d"></a>\s*', "", body)
    body = re.sub(r"<!--.*?-->\s*", "", body, flags=re.S)
    return body.strip() + "\n"


def body_text(path: Path) -> str:
    text = path.read_text()
    if text.startswith("---\n"):
        text = text[text.index("\n---\n", 4) + 5:]
    return re.sub(r"^# .*\n", "", text.strip()).strip() + "\n"


def collate():
    notes = json.loads((HERE / "S01-SUBMISSION-NOTES.json").read_text())
    movements, n = [], 0
    for name, pos, title in MOVEMENTS:
        prose = prose_of(name)
        defs = notes[name]["notes"]
        order: dict[str, int] = {}

        def number(match):
            nonlocal n
            key = match[1]
            if key not in defs:
                raise SystemExit(f"{name}: no submission note for [^{key}]")
            if key not in order:
                n += 1
                order[key] = n
            return f"[^{order[key]}]"

        numbered = MARK.sub(number, prose)
        movements.append({
            "name": name, "pos": pos, "title": title, "raw": prose, "prose": numbered,
            "notes": [(num, defs[key]) for key, num in order.items()],
            "keys": order, "bibliography": notes[name].get("bibliography", []),
        })
    return movements


def write_markdown(movements, abstract: str, front: str) -> str:
    out = [
        "---",
        f'title: "{TITLE}: {SUBTITLE}"',
        "source_id: confronting-the-limit-s01",
        "page_type: submission-section",
        "ownership: frank-sovereign",
        f'author: "{AUTHOR}"',
        f'section: "{SECTION}"',
        'status: "submission — bounded foundation section"',
        'date: "2026-10-04"',
        "---",
        "",
        f"# {TITLE}: {SUBTITLE}",
        "",
        f"*{AUTHOR}*",
        "",
        "*[Section room](section-rooms/00-integral-threshold/ROOM-00-integral-threshold.md) · [Whole manuscript](THE-RETURN-OF-ZERO.md)*",
        "",
        "## Abstract",
        "",
        abstract.strip(),
        "",
        "## A note on the text",
        "",
        front.strip(),
        "",
        f"## {SECTION}",
        "",
    ]
    for m in movements:
        out += [f'<a id="{m["name"]}"></a>', "", f"### {m['pos']} · {m['title']}", "", m["prose"].strip(), ""]
    out += ["## Notes", ""]
    for m in movements:
        out += [f"### {m['pos']} · {m['title']}", ""]
        out += [f"[^{num}]: {text}\n" for num, text in m["notes"]]
    out += ["## Sources", ""]
    for m in movements:
        out += [f"### {m['pos']} · {m['title']}", ""]
        out += [f"- {entry}" for entry in m["bibliography"]] + [""]
    return "\n".join(out).rstrip() + "\n"


def renderer() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"typographer": False}).enable("table")
    dollarmath_plugin(md, double_inline=True)
    return md


def render_prose(md: MarkdownIt, text: str, refs: dict) -> str:
    text = MARK.sub(lambda m: f"FNREF{m[1]}FNEND", text)
    rendered = md.render(text)

    def sup(match):
        num = match[1]
        refs[num] = refs.get(num, 0) + 1
        rid = f"r{num}" if refs[num] == 1 else f"r{num}-{refs[num]}"
        return f'<sup class="fn" id="{rid}"><a href="#n{num}">{num}</a></sup>'

    return re.sub(r"FNREF(\d+)FNEND", sup, rendered)


def inline(md: MarkdownIt, text: str) -> str:
    return md.renderInline(text)


CSS = r"""
:root{--paper:#fbfaf6;--ink:#1f211e;--muted:#6a6d66;--rule:#dcdcd2;--accent:#3f5f50;--code:#f0efe7;
 --measure:38rem;font-size:18px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#171816;--ink:#e6e4dc;--muted:#9fa199;--rule:#33352f;--accent:#9cc3ad;--code:#22241f}}
:root[data-theme="dark"]{--paper:#171816;--ink:#e6e4dc;--muted:#9fa199;--rule:#33352f;--accent:#9cc3ad;--code:#22241f}
*{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,"Iowan Old Style",serif;line-height:1.62;
 font-feature-settings:"onum","kern";-webkit-font-smoothing:antialiased}
main{max-width:var(--measure);margin:0 auto;padding:5rem 16px 6rem}
a{color:var(--accent);text-underline-offset:.18em;text-decoration-thickness:1px}
header.title{text-align:center;margin:2rem 0 4.5rem}
header.title h1{font-weight:500;font-size:2.35rem;line-height:1.15;margin:0 0 .6rem;letter-spacing:-.01em}
header.title .subtitle{font-size:1.25rem;font-style:italic;color:var(--muted);margin:0 0 2.2rem}
header.title .author{font-variant:small-caps;letter-spacing:.06em;font-size:1.05rem}
header.title .section{margin-top:.4rem;color:var(--muted);font-size:.95rem}
header.title p{text-align:center}
h2{font-weight:500;font-size:1.45rem;margin:4.5rem 0 1.4rem;text-align:center;letter-spacing:.01em}
h3{font-weight:500;font-size:1rem;margin:3.6rem 0 1.4rem;text-align:center;font-variant:small-caps;letter-spacing:.07em;color:var(--muted)}
h3 .pos{font-variant:normal;font-family:"Source Code Pro",ui-monospace,monospace;font-size:.85em;margin-right:.5em;color:var(--accent)}
p{margin:0 0 1.05rem;hyphens:auto;-webkit-hyphens:auto;text-align:justify}
.abstract p,.note-on-text p{text-align:left;font-size:.95rem}
.abstract,.note-on-text{border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);padding:1.4rem 0 .4rem;margin:0 0 2.5rem}
.abstract h2,.note-on-text h2{margin:0 0 1rem;font-size:1rem;font-variant:small-caps;letter-spacing:.08em;color:var(--muted)}
code{font-family:"Source Code Pro",ui-monospace,monospace;font-size:.8em;background:var(--code);padding:.08em .3em;border-radius:3px;white-space:nowrap}
blockquote{margin:1.4rem 0 1.4rem 1.6rem;padding:0;font-size:.95rem}
.table-wrap{overflow-x:auto;margin:1.8rem 0}
table{border-collapse:collapse;font-size:.74rem;line-height:1.4;width:100%}
th,td{border-top:1px solid var(--rule);padding:.45rem .5rem;vertical-align:top;text-align:left}
th{font-weight:600;border-top:1.5px solid var(--ink)}
tr:last-child td{border-bottom:1.5px solid var(--ink)}
.math.block{margin:1.4rem 0;overflow-x:auto;overflow-y:hidden}
sup.fn{font-size:.62em;line-height:0;margin-left:.08em}
sup.fn a{text-decoration:none;font-family:system-ui,sans-serif}
section.notes ol,section.sources ul{padding-left:2.2rem;font-size:.82rem;line-height:1.5}
section.notes li,section.sources li{margin:0 0 .55rem}
section.sources ul{list-style:none;padding-left:1.6rem;text-indent:-1.6rem}
section.notes p{margin:0;text-align:left}
a.back{text-decoration:none;margin-left:.3em;font-family:system-ui,sans-serif;font-size:.85em}
.theme{position:fixed;top:12px;right:12px;font:12px system-ui,sans-serif;background:transparent;border:1px solid var(--rule);color:var(--muted);border-radius:4px;padding:4px 8px;cursor:pointer}
@media (max-width:640px){:root{font-size:16.5px}main{padding-top:3rem}header.title h1{font-size:1.8rem}p{text-align:left}}
@media print{
 :root{--paper:#fff;--ink:#000;--muted:#444;--accent:#000;--code:#f2f2f2;font-size:10.5pt}
 @page{size:A4;margin:24mm 22mm 24mm 22mm;@bottom-center{content:counter(page);font:9pt "Source Serif 4",Georgia,serif;color:#555}}
 @page:first{@bottom-center{content:none}}
 .theme{display:none}
 main{max-width:none;padding:0}
 header.title{margin:30mm 0 14mm;break-after:page}
 section.front{break-after:page}
 h2{break-before:page;margin-top:0}
 section.front h2,.abstract h2,.note-on-text h2{break-before:auto}
 h3{break-after:avoid}
 p{orphans:3;widows:3}
 a{text-decoration:none;color:inherit}
 sup.fn a{color:#000}
 table{font-size:7.5pt;break-inside:avoid}
 a.back{display:none}
}
"""

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Confronting the Limit</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;0,8..60,600;1,8..60,400&family=Source+Code+Pro:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<style>{css}</style></head><body>
<button class="theme" type="button" aria-label="Toggle light or dark theme">◐</button>
<main>
"""

TAIL = """</main>
<script>
document.querySelectorAll('table').forEach(t=>{const w=document.createElement('div');w.className='table-wrap';t.parentNode.insertBefore(w,t);w.appendChild(t)});
window.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('.math').forEach(el=>{try{katex.render(el.textContent,el,{displayMode:el.classList.contains('block'),throwOnError:false})}catch(e){}});
  document.body.dataset.mathReady='1';
});
const b=document.querySelector('.theme');b.addEventListener('click',()=>{const r=document.documentElement;
 const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
 r.dataset.theme=dark?'light':'dark';try{localStorage.setItem('ctl-theme',r.dataset.theme)}catch(e){}});
try{const t=localStorage.getItem('ctl-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}
</script>
</body></html>
"""


def write_html(movements, abstract: str, front: str) -> str:
    md = renderer()
    refs: dict = {}
    parts = [
        '<header class="title">',
        f"<h1>{TITLE}</h1>",
        f'<p class="subtitle">{SUBTITLE}</p>',
        f'<p class="author">{AUTHOR}</p>',
        f'<p class="section">{html.escape(SECTION)}</p>',
        "</header>",
        '<section class="front">',
        '<div class="abstract"><h2>Abstract</h2>', md.render(abstract), "</div>",
        '<div class="note-on-text"><h2>A note on the text</h2>', md.render(front), "</div>",
        "</section>",
        f'<h2 id="s01">{html.escape(SECTION)}</h2>',
    ]
    for m in movements:
        parts.append(f'<h3 id="{m["name"]}"><span class="pos">{html.escape(m["pos"])}</span>{html.escape(m["title"])}</h3>')
        parts.append(render_prose(md, m["prose"], refs))
    parts.append('<section class="notes"><h2 id="notes">Notes</h2>')
    for m in movements:
        parts.append(f'<h3><span class="pos">{html.escape(m["pos"])}</span>{html.escape(m["title"])}</h3>')
        start = m["notes"][0][0] if m["notes"] else 1
        parts.append(f'<ol start="{start}">')
        for num, text in m["notes"]:
            parts.append(f'<li id="n{num}">{inline(md, text)}<a class="back" href="#r{num}" aria-label="Back to text">↩</a></li>')
        parts.append("</ol>")
    parts.append("</section>")
    parts.append('<section class="sources"><h2 id="sources">Sources</h2>')
    for m in movements:
        parts.append(f'<h3><span class="pos">{html.escape(m["pos"])}</span>{html.escape(m["title"])}</h3><ul>')
        parts += [f"<li>{inline(md, e)}</li>" for e in m["bibliography"]]
        parts.append("</ul>")
    parts.append("</section>")
    desc = f"{TITLE}: {SUBTITLE}. {SECTION}, by {AUTHOR}."
    return HEAD.format(css=CSS, desc=html.escape(desc)) + "\n".join(parts) + TAIL


def write_pdf(html_path: Path, pdf_path: Path) -> None:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=20000", f"--print-to-pdf={pdf_path}",
                    html_path.as_uri()], check=True, capture_output=True)


def update_manuscript(movements) -> dict:
    text = MANUSCRIPT.read_text()
    start = text.index("<!-- section:s01:start -->")
    end = text.index("<!-- section:s01:end -->")
    old_block = text[start:end]
    keep = old_block[: old_block.index("## §0/1")]
    body = [keep.rstrip(), "", f"## {SECTION}", ""]
    for m in movements:
        prose = MARK.sub(lambda x: f"[^s01-{m['name'].lower()}-{x[1]}]", m["raw"])
        body += [f'<a id="{m["name"]}"></a>', f"<!-- movement:{m['name']} -->", "", prose.strip(), ""]
    new_block = "\n".join(body) + "\n"
    text = text[:start] + new_block + text[end:]
    # Notes block for §0/1: replace definitions, but keep any old s01 note still
    # referenced from another section.
    n_start = text.index("### §0/1 — The Integral Threshold", text.index("\n## Notes"))
    n_end = text.index("\n### ", n_start + 5)
    old_notes = text[n_start:n_end]
    outside = set(MARK.findall(text[:start] + text[start + len(new_block):n_start]))
    kept = [line for line in old_notes.splitlines()
            if (k := re.match(r"\[\^([^\]]+)\]:", line)) and k[1] in outside]
    lines = ["### §0/1 — The Integral Threshold", ""]
    for m in movements:
        lines += [f"#### {m['pos']} · {m['title']}", ""]
        keys = {num: key for key, num in m["keys"].items()}
        lines += [f"[^s01-{m['name'].lower()}-{keys[num]}]: {note}\n" for num, note in m["notes"]]
    if kept:
        lines += ["#### Retained for other sections", ""] + [k + "\n" for k in kept]
    text = text[:n_start] + "\n".join(lines).rstrip() + "\n" + text[n_end:]
    refs = set(MARK.findall(text))
    defs = re.findall(r"^\[\^([^\]]+)\]:", text, re.M)
    missing = sorted(refs - set(defs))
    MANUSCRIPT.write_text(text)
    return {"kept_for_other_sections": len(kept), "unresolved_markers": missing,
            "duplicate_definitions": sorted({d for d in defs if defs.count(d) > 1})}


def main() -> None:
    movements = collate()
    abstract = body_text(HERE / "ABSTRACT-PROPOSED-2026-10-04.md")
    front = (HERE / "S01-FRONT-NOTE.md").read_text()
    md_text = write_markdown(movements, abstract, front)
    OUT.with_suffix(".md").write_text(md_text)
    html_text = write_html(movements, abstract, front)
    OUT.with_suffix(".html").write_text(html_text)
    if "--no-pdf" not in sys.argv:
        write_pdf(OUT.with_suffix(".html"), OUT.with_suffix(".pdf"))
    report = {
        "words_prose": sum(len(m["raw"].split()) for m in movements),
        "notes": sum(len(m["notes"]) for m in movements),
        "sources": sum(len(m["bibliography"]) for m in movements),
        "outputs": [p.name for p in (OUT.with_suffix(".md"), OUT.with_suffix(".html"), OUT.with_suffix(".pdf")) if p.exists()],
    }
    if "--manuscript" in sys.argv:
        report["manuscript"] = update_manuscript(movements)
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
