# --- figkit: shared construction helpers, inlined at the head of every generator ---
from xml.sax.saxutils import escape
import math

PAPER, PANEL = "#f5f0e6", "#efe8da"
INK, MUTED, RULE = "#211d18", "#6f6659", "#b9ae9c"
RED, INDIGO, GOLD = "#8a2f2b", "#2e3a59", "#a5822c"
SERIF = "Georgia, 'Times New Roman', serif"
MONO = "'Courier New', Courier, monospace"


class Fig:
    def __init__(self, w, h, title, desc):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=16, fill=INK, anchor="start", italic=False, mono=False,
             bold=False, ls=None, opacity=None):
        a = [f'x="{x:g}"', f'y="{y:g}"', f'font-size="{size:g}"', f'fill="{fill}"', f'text-anchor="{anchor}"']
        if italic: a.append('font-style="italic"')
        if bold: a.append('font-weight="bold"')
        if mono: a.append(f'font-family="{MONO}"')
        if ls: a.append(f'letter-spacing="{ls}"')
        if opacity: a.append(f'opacity="{opacity}"')
        self.add(f'<text {" ".join(a)}>{escape(s)}</text>')

    def lines(self, x, y, strings, step=22, **kw):
        for i, s in enumerate(strings):
            self.text(x, y + i * step, s, **kw)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.5, rx=0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, cap="butt", marker=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        self.add(f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{stroke}" stroke-width="{sw:g}" stroke-linecap="{cap}"{d}{m}/>')

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"{d}/>')

    def path(self, d, fill="none", stroke=INK, sw=1.5, dash=None, marker=None, cap="round", join="round"):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{marker})"' if marker else ""
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}" stroke-linecap="{cap}" stroke-linejoin="{join}"{dd}{m}/>')

    def polygon(self, pts, fill="none", stroke=INK, sw=1.5, dash=None, opacity=None):
        p = " ".join(f"{x:g},{y:g}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{opacity}"' if opacity else ""
        self.add(f'<polygon points="{p}" fill="{fill}"{o} stroke="{stroke}" stroke-width="{sw:g}" stroke-linejoin="round"{d}/>')

    def header(self, kind, title, subtitle):
        self.text(self.w / 2, 64, f"{kind} · {title}".upper(), size=20, anchor="middle", ls=4)
        self.text(self.w / 2, 94, subtitle, size=16, fill=MUTED, anchor="middle", italic=True)

    def save(self, path):
        defs = ('<defs>'
                f'<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
                f'<marker id="ahr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker>'
                f'<marker id="ahm" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
                f'<marker id="ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INDIGO}"/></marker>'
                '</defs>')
        head = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" font-family="{SERIF}" role="img" aria-labelledby="t d">\n'
                f'<title id="t">{escape(self.title)}</title>\n<desc id="d">{escape(self.desc)}</desc>\n{defs}\n'
                f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="{PAPER}"/>\n')
        with open(path, "w", encoding="utf-8") as f:
            f.write(head + "\n".join(self.parts) + "\n</svg>\n")
# --- end figkit ---


# ---- generator: syn-ballein, the retained relation (Return of Zero, M21) ----
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syn-ballein-retained-relation.svg")
TITLE = "Syn-ballein: (0/1)/(1/0) retains the relation, as a broken token keeps its fit"
DESC = ("Top: two boxes, zero over one and one over zero, joined by a double arrow reading zero over one equals one over zero: "
        "one relation under opposite orientations. Zero over one is the ground becoming articulate in a determination; one over "
        "zero is the determination turned toward the ground it cannot enclose. A long outer stroke beneath both relates the two "
        "readings; AND retains participation in one event, OR retains the difference through which either orientation can be "
        "taken. A strip notes that ordinary arithmetic keeps the asymmetry: zero over one is defined and one over zero is not. "
        "Bottom: three states of a broken token. Two halves fitted along matching jagged edges: recognition through the maintained "
        "break. One half alone beside a dashed empty outline: a lost piece, so no matching can occur (severance). One unbroken "
        "lump: both melted, the seam that could authenticate the relation is gone (fusion).")
f = Fig(1100, 940, TITLE, DESC)
f.header("Diagram", "Syn-ballein, the retained relation", "the outer stroke holds both orientations; the fit of a broken token holds its two halves")

# --- top: the two orientations
bw, bh, by = 300, 130, 150
lx, rx = 120, 680
for x, expr, l1, l2 in ((lx, "0/1", "the ground becoming articulate", "in a determination"),
                        (rx, "1/0", "the determination turned toward", "the ground it cannot enclose")):
    f.rect(x, by, bw, bh, fill=PANEL, stroke=INK, sw=2, rx=8)
    f.text(x + bw / 2, by + 62, expr, size=46, anchor="middle", mono=True)
    f.text(x + bw / 2, by + 94, l1, size=15.5, fill=MUTED, anchor="middle")
    f.text(x + bw / 2, by + 114, l2, size=15.5, fill=MUTED, anchor="middle")
f.line(lx + bw + 12, by + 52, rx - 12, by + 52, stroke=RED, sw=2.2, marker="ahr")
f.line(rx - 12, by + 84, lx + bw + 12, by + 84, stroke=RED, sw=2.2, marker="ahr")
f.text(550, by + 72, "0/1 = 1/0", size=17, fill=RED, anchor="middle", mono=True)
f.text(550, by + 108, "one relation, opposite orientations", size=14.5, fill=RED, anchor="middle")

# outer stroke
oy = by + bh + 34
f.line(lx, oy, rx + bw, oy, stroke=INK, sw=4, cap="round")
f.text(550, oy + 34, "(0/1)/(1/0)", size=24, anchor="middle", mono=True)
f.text(550, oy + 60, "the outer stroke relates the two readings; the inner strokes keep ground and manifestation", size=15.5, fill=MUTED, anchor="middle", italic=True)
f.text(lx + 90, oy + 98, "AND", size=19, fill=INDIGO, anchor="middle", bold=True)
f.text(lx + 150, oy + 98, "retains participation in one event", size=16, anchor="start")
f.text(rx + 20, oy + 98, "OR", size=19, fill=INDIGO, anchor="middle", bold=True)
f.text(rx + 50, oy + 98, "retains the difference through which", size=16, anchor="start")
f.text(rx + 50, oy + 120, "either orientation can be taken", size=16, anchor="start")

# arithmetic strip
ay = oy + 150
f.rect(120, ay, 860, 52, fill="none", stroke=RULE, sw=1.2, rx=6, dash="6 5")
f.text(550, ay + 22, "ordinary arithmetic keeps the asymmetry: 0/1 is defined, 1/0 is not. The return adds no numerical object to complete it;", size=15, fill=MUTED, anchor="middle")
f.text(550, ay + 42, "it changes how the achieved form is held.", size=15, fill=MUTED, anchor="middle")

# --- bottom: the symbolon
ty = 748
f.text(550, 590, "the symbolon: recognition happens through the maintained break", size=19, anchor="middle", italic=True)
f.line(60, 608, 1040, 608, stroke=RULE, sw=1.2)

import math
def zig(cx, y_top, y_bot, amp=9, n=7):
    pts = []
    for i in range(n + 1):
        y = y_top + (y_bot - y_top) * i / n
        pts.append((cx + (0 if i in (0, n) else (amp if i % 2 else -amp)), y))
    return pts
def half(cx, cy, r, side, gap):
    # side = -1 left half, +1 right half; fracture centred on cx + side*gap/2
    fx = cx + side * gap / 2
    zs = zig(fx, cy - r, cy + r)
    d = "M " + " L ".join(f"{x:g} {y:g}" for x, y in zs)
    sweep = 1 if side < 0 else 0
    d += f" A {r} {r} 0 0 {sweep} {zs[0][0]:g} {zs[0][1]:g} Z"
    return d
r = 62
# state 1: fitted
c1 = 190
f.path(half(c1, ty, r, -1, 14), fill=PANEL, stroke=INK, sw=2.2)
f.path(half(c1, ty, r, +1, 14), fill=PANEL, stroke=INK, sw=2.2)
f.text(c1, ty + 100, "fitted halves", size=17, anchor="middle", bold=True)
f.text(c1, ty + 122, "the fit authenticates the relation", size=14.5, fill=MUTED, anchor="middle")
f.text(c1, ty + 142, "through their difference", size=14.5, fill=MUTED, anchor="middle")
f.text(c1, ty - 84, "syn-ballein", size=15.5, fill=INDIGO, anchor="middle", italic=True)
# state 2: lost piece
c2 = 550
f.path(half(c2, ty, r, -1, 14), fill=PANEL, stroke=INK, sw=2.2)
d2 = half(c2, ty, r, +1, 14)
f.path(d2, fill="none", stroke=RULE, sw=2, dash="7 6")
f.text(c2, ty + 100, "a lost half", size=17, anchor="middle", bold=True)
f.text(c2, ty + 122, "no matching can occur;", size=14.5, fill=MUTED, anchor="middle")
f.text(c2, ty + 142, "the fracture still has its shape", size=14.5, fill=MUTED, anchor="middle")
f.text(c2, ty - 84, "severance", size=15.5, fill=RED, anchor="middle", italic=True)
# state 3: lump
c3 = 910
f.path(f"M {c3 - r} {ty} C {c3 - r} {ty - 70}, {c3 + 10} {ty - r - 14}, {c3 + r} {ty - 20} C {c3 + r + 12} {ty + 40}, {c3 + 30} {ty + r + 6}, {c3 - 10} {ty + r} C {c3 - 50} {ty + r - 4}, {c3 - r} {ty + 40}, {c3 - r} {ty} Z", fill=PANEL, stroke=INK, sw=2.2)
f.text(c3, ty + 100, "one lump", size=17, anchor="middle", bold=True)
f.text(c3, ty + 122, "the seam that could authenticate", size=14.5, fill=MUTED, anchor="middle")
f.text(c3, ty + 142, "the relation has disappeared", size=14.5, fill=MUTED, anchor="middle")
f.text(c3, ty - 84, "fusion", size=15.5, fill=RED, anchor="middle", italic=True)
f.save(OUT)
print("wrote", OUT)
