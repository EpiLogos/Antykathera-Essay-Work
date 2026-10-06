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


# ---- generator: a pair of dice, counted three ways (Return of Zero, M02) ----
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dice-pair-ordered-and-unordered-counts.svg")
TITLE = "A pair of dice counted three ways: 36 ordered states, 21 unordered outcomes, 11 totals"
DESC = ("A six-by-six grid of die A against die B holds the thirty-six ordered states of the pair. The six doubles lie on the "
        "diagonal; the thirty other cells fold across it into fifteen mirrored pairs. The pair A=1,B=2 and A=2,B=1 is "
        "highlighted: two ordered states with the same values and the same total of three. Three ledgers to the right "
        "give the counts under three accounts: thirty-six when each die is tracked, twenty-one when the labels are "
        "dropped, eleven when only the total is recorded.")
f = Fig(1100, 800, TITLE, DESC)
f.header("Diagram", "A pair of dice, counted three ways", "the account changes what it retains, and the count changes with it")

# grid
x0, y0, c = 150, 205, 66
f.text(x0 + 3 * c, 178, "B shows", size=16, fill=MUTED, anchor="middle", italic=True)
f.text(x0 - 70, y0 + 3 * c + 6, "A shows", size=16, fill=MUTED, anchor="middle", italic=True)
for i in range(6):
    f.text(x0 + i * c + c / 2, y0 - 8, str(i + 1), size=16, fill=MUTED, anchor="middle")
    f.text(x0 - 14, y0 + i * c + c / 2 + 6, str(i + 1), size=16, fill=MUTED, anchor="end")
for a in range(1, 7):
    for b in range(1, 7):
        x, y = x0 + (b - 1) * c, y0 + (a - 1) * c
        pair = {a, b} == {1, 2}
        if a == b:
            fill, st, sw = "#d9cfba", INK, 1.2
        elif pair:
            fill, st, sw = "#ecc9c2", RED, 2.4
        else:
            fill, st, sw = PANEL, RULE, 1.2
        f.rect(x, y, c, c, fill=fill, stroke=st, sw=sw)
        col = RED if pair else (INK if a == b else MUTED)
        f.text(x + c / 2, y + c / 2 + 6, f"{a}·{b}", size=17, fill=col, anchor="middle", bold=pair)
# legend
ly = y0 + 6 * c + 36
f.rect(x0, ly - 15, 22, 22, fill="#d9cfba", stroke=INK, sw=1.2)
f.text(x0 + 32, ly + 2, "double (the diagonal): one state, its own mirror", size=15)
f.rect(x0, ly + 18, 22, 22, fill=PANEL, stroke=RULE, sw=1.2)
f.text(x0 + 32, ly + 35, "mirrored pair: two ordered states, one unordered outcome", size=15)
f.rect(x0, ly + 51, 22, 22, fill="#ecc9c2", stroke=RED, sw=2)
f.text(x0 + 32, ly + 68, "the essay's pair: (A=1, B=2) and (A=2, B=1), both with total 3", size=15, fill=RED)

# ledgers
X = 640
rows = [
    ("keep which die is which", "36", "ordered states (A, B)", "6 doubles + 30 off-diagonal cells", INK),
    ("stop caring which die is which", "21", "unordered outcomes", "6 doubles + 15 mirrored pairs", INK),
    ("record only the total", "11", "totals, from 2 to 12", "the total 3 keeps (1,2) and (2,1) as one entry", RED),
]
ys = [190, 380, 570]
for (lab, n, what, how, col), y in zip(rows, ys):
    f.rect(X, y, 410, 130, fill=PANEL, stroke=RULE, sw=1.5, rx=6)
    f.text(X + 20, y + 32, lab, size=17, italic=True, fill=MUTED)
    f.text(X + 62, y + 98, n, size=58, fill=col, anchor="middle")
    f.text(X + 124, y + 74, what, size=18)
    f.text(X + 124, y + 100, how, size=15, fill=MUTED)
for y0_, lab in ((320, "drop the labels: 30 cells fold in pairs"), (510, "drop the values: keep the total")):
    f.line(X + 62, y0_ - 2, X + 62, y0_ + 52, stroke=RED, sw=1.8, marker="ahr")
    f.text(X + 80, y0_ + 30, lab, size=15, fill=RED)

f.text(550, 770, "Nothing mysterious has happened: the account has changed what it retains, so the number answers a different question each time.", size=15, fill=MUTED, anchor="middle", italic=True)
f.save(OUT)
print("wrote", OUT)
