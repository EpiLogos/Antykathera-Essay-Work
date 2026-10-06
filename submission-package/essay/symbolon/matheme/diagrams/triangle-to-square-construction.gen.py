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


# ---- generator: from the triangle to the square (Return of Zero, M25) ----
import os, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "triangle-to-square-construction.svg")
TITLE = "From the triangle to the square: the acquisition order N, E, W, S"
DESC = ("Three panels on one unit circle with stations N at the top, E at the right, W at the left and S at the bottom, "
        "centre O. First, a radius from O to N. Second, the triangle N, E, W: interior angles sum to 180 degrees, area one, "
        "stations acquired in the order N, E, W; the move from E to W crosses the diameter. Third, adding S and joining "
        "N, E, S, W gives the square: angle sum 360 degrees, area two; the former edge E to W is now an interior diagonal "
        "shared by the complementary triangles N-E-W and S-E-W.")
f = Fig(1100, 800, TITLE, DESC)
f.header("Diagram", "From the triangle to the square", "what bounded the figure now articulates its interior")

R = 96
panels = [(160, "1 · the first radius", "N = (0, 1)"), (550, "2 · the triangle", "N, E, W"), (920, "3 · the square", "N, E, S, W")]
cy = 330
def st(cx, name):
    return {"N": (cx, cy - R), "E": (cx + R, cy), "W": (cx - R, cy), "S": (cx, cy + R)}[name]
for cx, head, sub in panels:
    f.text(cx, 176, head, size=18, anchor="middle", italic=True)
    f.circle(cx, cy, R, fill="none", stroke=RULE, sw=1.6)
    f.circle(cx, cy, 4, fill=INK, stroke=INK)
    f.text(cx + 8, cy + 22, "O", size=15, fill=MUTED)

def label(cx, name, order, show=True, col=INK):
    x, y = st(cx, name)
    f.circle(x, y, 7, fill=col, stroke=col)
    dx, dy, anc = {"N": (0, -26, "middle"), "E": (24, 6, "start"), "W": (-24, 6, "end"), "S": (0, 34, "middle")}[name]
    f.text(x + dx, y + dy, name if not order else f"{name} ({order})", size=17, anchor=anc, mono=True, fill=col)

# panel 1
cx = 160
f.line(cx, cy, *st(cx, "N"), stroke=INK, sw=3)
label(cx, "N", 1)
f.text(cx, 506, "one radius fixes a centre and a direction", size=15.5, anchor="middle", fill=MUTED)

# panel 2: triangle N E W
cx = 550
tri = [st(cx, "N"), st(cx, "E"), st(cx, "W")]
f.polygon(tri, fill="#e7dcc4", stroke=INK, sw=2.6, opacity=0.9)
f.line(cx, cy, *st(cx, "E"), stroke=MUTED, sw=1.2)
f.line(cx, cy, *st(cx, "W"), stroke=MUTED, sw=1.2)
f.line(cx - R + 6, cy + 18, cx + R - 6, cy + 18, stroke=RED, sw=0)
label(cx, "N", 1); label(cx, "E", 2); label(cx, "W", 3)
f.text(cx, cy + R + 68, "E → W crosses the diameter;", size=15.5, anchor="middle", fill=RED)
f.text(cx, cy + R + 88, "it is not the next quarter-turn", size=15.5, anchor="middle", fill=RED)

# panel 3: square N E S W with diagonal E-W
cx = 920
upper = [st(cx, "N"), st(cx, "E"), st(cx, "W")]
lower = [st(cx, "S"), st(cx, "E"), st(cx, "W")]
f.polygon(upper, fill="#e7dcc4", stroke="none", sw=0, opacity=0.95)
f.polygon(lower, fill="#ecc9c2", stroke="none", sw=0, opacity=0.95)
f.polygon([st(cx, "N"), st(cx, "E"), st(cx, "S"), st(cx, "W")], fill="none", stroke=INK, sw=2.6)
f.line(*st(cx, "W"), *st(cx, "E"), stroke=RED, sw=2.6, dash="8 5")
label(cx, "N", 1); label(cx, "E", 2); label(cx, "W", 3); label(cx, "S", 4, col=RED)
f.text(cx, cy + R + 68, "E–W, once a bounding edge,", size=15.5, anchor="middle", fill=RED)
f.text(cx, cy + R + 88, "is now a shared interior diagonal", size=15.5, anchor="middle", fill=RED)

# measurement ledger
ly = 600
f.line(60, ly - 24, 1040, ly - 24, stroke=RULE, sw=1.2)
for cxx, lines in ((160, ["a radius, no area", "orientation only"]),
                   (550, ["interior angles: 180°", "area: 1", "acquired order: N, E, W"]),
                   (920, ["interior angles: 360°", "area: 2", "two complementary triangles", "N–E–W and S–E–W"])):
    f.lines(cxx, ly, lines, step=24, size=17, anchor="middle", mono=False)
f.text(550, 730, "Side count, angle sum, area and order of acquisition are different descriptions of one construction; the gain is the changed office of E–W.", size=15, anchor="middle", fill=MUTED, italic=True)
f.text(550, 756, "The angle sum makes the recontextualisation visible; it does not prove the account of the Subject.", size=15, anchor="middle", fill=MUTED, italic=True)
f.save(OUT)
print("wrote", OUT)
