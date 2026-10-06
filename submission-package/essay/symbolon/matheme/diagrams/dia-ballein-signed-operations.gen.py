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


# ---- generator: dia-ballein, one polar axis under three operations (Return of Zero, M20) ----
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dia-ballein-signed-operations.svg")
TITLE = "Dia-ballein: one polar axis held, summed and differenced"
DESC = ("A horizontal axis through a common zero carries the pole minus one at the left and plus one at the right, written "
        "(minus one) over (plus one): held polarity. Below, three operations on the same two signed units. Their sum, "
        "minus one plus plus one, is zero: the two meet at the common zero and give a net value. The difference taken from "
        "minus one, plus one minus minus one, is plus two: an arrow across the whole span from left to right. The "
        "difference taken from plus one, minus one minus plus one, is minus two: the same span in the opposite orientation. "
        "A red band states the error of appropriation: promoting a result into authority over the relation that made it possible.")
f = Fig(1100, 800, TITLE, DESC)
f.header("Diagram", "One polar axis, three operations", "the same two signed units held, summed and differenced: the operation decides what the result is about")

def axis(cx, y, half, labels=True, size=17, show_pole_labels=True):
    f.line(cx - half - 30, y, cx + half + 30, y, stroke=INK, sw=2)
    for dx, name in ((-half, "−1"), (0, "0"), (half, "+1")):
        f.line(cx + dx, y - 9, cx + dx, y + 9, stroke=INK, sw=2)
        if labels:
            f.text(cx + dx, y + 34, name, size=size, anchor="middle", mono=True)

def pole(cx, y, kind, r=15):
    if kind == "+":
        f.circle(cx, y, r, fill=INK, stroke=INK, sw=2)
    else:
        f.circle(cx, y, r, fill=PAPER, stroke=INK, sw=2.5)

# --- top: held polarity
cx, ay = 550, 218
f.text(cx, 160, "held polarity   (−1)/(+1)", size=20, anchor="middle", mono=True)
axis(cx, ay, 250, labels=False)
pole(cx - 250, ay, "-"); pole(cx + 250, ay, "+")
f.circle(cx, ay, 9, fill=PAPER, stroke=RED, sw=2.5)
f.text(cx - 250, ay + 40, "(−1)", size=17, anchor="middle", mono=True)
f.text(cx + 250, ay + 40, "(+1)", size=17, anchor="middle", mono=True)
f.text(cx, ay + 40, "common zero: the axis", size=16, fill=RED, anchor="middle")
f.text(cx, ay + 70, "the stroke retains a polarity: each direction means something through the axis and its counter-direction", size=15.5, fill=MUTED, anchor="middle", italic=True)

# --- three operations
cols = [200, 550, 900]
heads = [("sum: cancellation", "(−1)+(+1)=0"),
         ("difference taken from −1", "(+1)−(−1)=+2"),
         ("difference taken from +1", "(−1)−(+1)=−2")]
notes = [["a net value: a deposit and a withdrawal", "leave a zero balance without making", "the two acts one, or their effects nothing"],
         ["the whole span, measured from the", "−1 endpoint and oriented towards +1"],
         ["the same span, measured from the", "+1 endpoint and oriented towards −1"]]
top = 360
for i, (cxx, (h, expr)) in enumerate(zip(cols, heads)):
    f.rect(cxx - 165, top - 40, 330, 345, fill=PANEL, stroke=RULE, sw=1.4, rx=6)
    f.text(cxx, top - 12, h, size=17, anchor="middle", italic=True, fill=MUTED)
    ly = top + 160
    half = 95
    axis(cxx, ly, half, labels=False)
    for dx in (-half, 0, half):
        pass
    pole(cxx - half, ly, "-", r=13); pole(cxx + half, ly, "+", r=13)
    f.text(cxx - half, ly + 36, "−1", size=16, anchor="middle", mono=True)
    f.text(cxx, ly + 36, "0", size=16, anchor="middle", mono=True)
    f.text(cxx + half, ly + 36, "+1", size=16, anchor="middle", mono=True)
    if i == 0:
        f.line(cxx - half + 16, ly - 30, cxx - 12, ly - 30, stroke=INDIGO, sw=2.4, marker="ahb")
        f.line(cxx + half - 16, ly - 30, cxx + 12, ly - 30, stroke=INDIGO, sw=2.4, marker="ahb")
        f.circle(cxx, ly, 9, fill=PAPER, stroke=RED, sw=2.5)
        f.text(cxx, ly - 50, "meet at 0", size=15, fill=INDIGO, anchor="middle")
    elif i == 1:
        f.path(f"M {cxx - half} {ly - 22} C {cxx - half + 40} {ly - 78}, {cxx + half - 40} {ly - 78}, {cxx + half - 6} {ly - 24}", stroke=RED, sw=2.6, marker="ahr")
        f.text(cxx, ly - 76, "+2", size=24, fill=RED, anchor="middle", mono=True)
    else:
        f.path(f"M {cxx + half} {ly - 22} C {cxx + half - 40} {ly - 78}, {cxx - half + 40} {ly - 78}, {cxx - half + 6} {ly - 24}", stroke=RED, sw=2.6, marker="ahr")
        f.text(cxx, ly - 76, "−2", size=24, fill=RED, anchor="middle", mono=True)
    f.text(cxx, top + 24, expr, size=20, anchor="middle", mono=True)
    f.lines(cxx, ly + 76, notes[i], step=21, size=14.5, fill=MUTED, anchor="middle")

# --- guard band
by = 692
f.rect(60, by, 980, 84, fill="#f1dcd6", stroke=RED, sw=1.6, rx=6)
f.text(550, by + 28, "Appropriation is a further step, and the error is in the promotion, not in the minus sign.", size=17, fill=RED, anchor="middle", bold=True)
f.text(550, by + 54, "Cancellation is read as 'the relation has gone', or a pole takes the span it was measured across as its own magnitude and authority.", size=15, fill=INK, anchor="middle")
f.text(550, by + 73, "A difference can be calculated impeccably and then used to conceal who chose the comparison and what it excluded.", size=15, fill=INK, anchor="middle")
f.save(OUT)
print("wrote", OUT)
