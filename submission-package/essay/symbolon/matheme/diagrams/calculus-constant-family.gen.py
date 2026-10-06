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


# ---- generator: a derivative that cannot recover its constant (Return of Zero, M25) ----
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calculus-constant-family.svg")
TITLE = "One derivative, a family of antiderivatives, one condition that selects"
DESC = ("A plot of the parabolas F of x equals x squared plus C for C equal to minus one, zero, one, two, three and four. "
        "At x equal to one each curve carries a short tangent segment of slope two: the same derivative, two x, for every "
        "member. The curve with C equal to three is drawn in red and passes through the marked point x zero, F zero equals three: "
        "the condition that selects one member of the family. A text column states that the derivative was exact throughout and "
        "lacked only the information needed to select the additive constant.")
f = Fig(1100, 760, TITLE, DESC)
f.header("Diagram", "What the derivative cannot recover", "local exactness can be complete as local exactness and still leave the constant open")

# plot area
px0, py0 = 100, 140            # top-left pixel of the plot box
sx, sy = 120, 48              # px per unit
xmin, xmax, ymin, ymax = -2.0, 2.4, -1.6, 8.6
W, H = (xmax - xmin) * sx, (ymax - ymin) * sy
def P(x, y): return px0 + (x - xmin) * sx, py0 + (ymax - y) * sy
f.rect(px0, py0, W, H, fill=PANEL, stroke=RULE, sw=1.2)
f.line(*P(xmin, 0), *P(xmax, 0), stroke=MUTED, sw=1.2)
f.line(*P(0, ymin), *P(0, ymax), stroke=MUTED, sw=1.2)
for v in (-2, -1, 1, 2):
    f.text(P(v, 0)[0], P(v, 0)[1] + 20, str(v), size=14.5, anchor="middle", fill=MUTED, mono=True)
f.text(P(xmax, 0)[0] - 6, P(xmax, 0)[1] - 8, "x", size=16, anchor="end", italic=True, fill=MUTED)
f.text(P(0, ymax)[0] + 10, P(0, ymax)[1] + 20, "F", size=16, italic=True, fill=MUTED)
Cs = [-1, 0, 1, 2, 3, 4]
for C in Cs:
    pts = []
    n = 80
    for i in range(n + 1):
        x = xmin + (xmax - xmin) * i / n
        y = x * x + C
        if ymin <= y <= ymax: pts.append(P(x, y))
    sel = (C == 3)
    d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts)
    f.path(d, stroke=(RED if sel else INDIGO), sw=(3.4 if sel else 1.7))
    # tangent at x = 1
    x1 = 1.0; y1 = x1 * x1 + C; dx = 0.45
    f.line(*P(x1 - dx, y1 - 2 * dx), *P(x1 + dx, y1 + 2 * dx), stroke=(RED if sel else INK), sw=2.4)
    f.circle(*P(x1, y1), 4.5, fill=(RED if sel else INK), stroke=(RED if sel else INK))
    f.text(px0 - 8, P(-2.0, 4.0 + C)[1] + 5, f"C = {C}", size=14.5, anchor="end", mono=True, fill=(RED if sel else INDIGO), bold=sel)
f.circle(*P(0, 3), 8, fill=PAPER, stroke=RED, sw=3)

# text column
tx = 640
f.text(tx, 176, "the family", size=17, italic=True, fill=MUTED)
f.text(tx, 210, "F(x) = x² + C", size=24, mono=True)
f.text(tx, 252, "the same slope at every x", size=17, italic=True, fill=MUTED)
f.text(tx, 286, "F′(x) = 2x, for every C", size=22, mono=True)
f.text(tx, 322, "the short black segments, all slope 2 at x = 1", size=15.5, fill=MUTED)
f.text(tx, 372, "integrating 2x returns the family,", size=17)
f.text(tx, 396, "not one function", size=17)
f.text(tx, 446, "a condition selects one member (the red ring, x = 0)", size=17, italic=True, fill=MUTED)
f.text(tx, 480, "F(0) = 3  ⟹  C = 3", size=22, mono=True, fill=RED)
f.rect(tx - 14, 520, 440, 118, fill="none", stroke=RULE, sw=1.2, rx=6, dash="6 5")
f.lines(tx + 6, 548, ["The derivative was exact throughout.", "What it lacked was the information needed", "to select the additive constant."], step=24, size=16.5)
f.text(550, 690, "The family statement holds on an interval; disconnected domains can carry separate constants.", size=15, anchor="middle", fill=MUTED, italic=True)
f.text(550, 716, "QL reads this dependence as a demand that local determination remain related to its provenance, not as a defect of precision.", size=15, anchor="middle", fill=MUTED, italic=True)
f.save(OUT)
print("wrote", OUT)
