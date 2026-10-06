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


# ---- generator: a path on the torus with winding (2, -1), and when a flow returns (Return of Zero, M29) ----
import os, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "torus-path-winding-and-return.svg")
TITLE = "A closed path on the torus carries winding (2, −1); a linear flow returns only for a rational ratio"
DESC = ("Left, the covering plane with its integer lattice and the straight path from the origin to the point two, minus one; "
        "the endpoints differ in the plane. An arrow labelled quotient by whole-number steps leads to the unit square on the right, "
        "where the same path appears as two parallel segments, from the top-left corner to the middle of the right edge and from "
        "the middle of the left edge to the bottom-right corner. All four corners are one point of the torus, so the path closes; "
        "its winding class, two turns one way and one back, is retained. Beneath, two linear flows drawn in the unit square: with "
        "rates in the ratio three to two the path closes at time one; with rates in the ratio one to the square root of two it never "
        "closes and keeps filling the square.")
f = Fig(1100, 904, TITLE, DESC)
f.header("Diagram", "A return that keeps its winding", "the surface-address recurs; the lifted path retains a displacement")

def wrap_segments(alpha, beta, T):
    """Split the line t -> (alpha t, beta t), 0<=t<=T, at integer crossings; yield unit-square segments (y up)."""
    ts = {0.0, T}
    for a in (alpha, beta):
        if a != 0:
            lo, hi = sorted((0.0, a * T))
            for n in range(math.floor(lo) , math.ceil(hi) + 1):
                tt = n / a
                if 0 < tt < T: ts.add(tt)
    ts = sorted(ts)
    segs = []
    for t0, t1 in zip(ts, ts[1:]):
        tm = (t0 + t1) / 2
        ox, oy = math.floor(alpha * tm), math.floor(beta * tm)
        segs.append(((alpha * t0 - ox, beta * t0 - oy), (alpha * t1 - ox, beta * t1 - oy)))
    return segs

# ---------- left: covering plane
s = 150
ox, oy = 120, 250                       # pixel position of plane (0, 0)
def P(x, y): return (ox + s * x, oy - s * y)
x0p, y0p = P(-0.35, 0.35); x1p, y1p = P(2.35, -1.35)
f.rect(x0p, y0p, x1p - x0p, y1p - y0p, fill=PANEL, stroke=RULE, sw=1.2)
for gx in (0, 1, 2):
    f.line(*P(gx, 0.35), *P(gx, -1.35), stroke=RULE, sw=1.2)
for gy in (0, -1):
    f.line(*P(-0.35, gy), *P(2.35, gy), stroke=RULE, sw=1.2)
f.text(x0p, y0p - 14, "covering plane  R²", size=17, italic=True, fill=MUTED)
for gx in (0, 1, 2):
    for gy in (0, -1):
        px, py = P(gx, gy)
        f.circle(px, py, 6, fill=PAPER, stroke=INDIGO, sw=2)
(sx, sy), (ex, ey) = P(0, 0), P(2, -1)
f.line(sx, sy, ex - 6, ey - 3, stroke=RED, sw=3.2, marker="ahr")
f.circle(sx, sy, 8, fill=RED, stroke=RED)
f.circle(ex, ey, 8, fill=PAPER, stroke=RED, sw=3)
mx, my = P(1, -0.5)
f.circle(mx, my, 5, fill=RED, stroke=RED)
f.text(sx + 12, sy - 14, "(0, 0)", size=16, anchor="start", mono=True)
f.text(ex + 4, ey + 30, "(2, −1)", size=16, anchor="middle", mono=True)
f.text(mx + 10, my - 14, "leaves the first unit square", size=14.5, fill=RED, anchor="start")
f.text(mx + 10, my + 4, "at the midpoint", size=14.5, fill=RED, anchor="start")

# arrow between panels
f.line(540, 250, 640, 250, stroke=INK, sw=2, marker="ah")
f.text(590, 238, "quotient by", size=15, anchor="middle", fill=MUTED)
f.text(590, 276, "whole steps", size=15, anchor="middle", fill=MUTED)

# ---------- right: the torus square
q = 250; qx, qy = 700, 135
def Q(x, y): return (qx + q * x, qy + q * (1 - y))
f.rect(qx, qy, q, q, fill=PANEL, stroke=INK, sw=2)
f.text(qx, qy - 16, "the torus, as one unit square", size=17, italic=True, fill=MUTED)
for seg in wrap_segments(2, -1, 1):
    (a, b), (c, d) = seg
    f.line(*Q(a, b), *Q(c, d), stroke=RED, sw=3.2)
for cx_, cy_ in ((0, 0), (1, 0), (0, 1), (1, 1)):
    f.circle(*Q(cx_, cy_), 7, fill=INDIGO, stroke=INDIGO)
f.text(qx + q + 18, qy + q + 6, "all four corners:", size=14.5, fill=INDIGO)
f.text(qx + q + 18, qy + q + 24, "one point", size=14.5, fill=INDIGO)
f.text(qx + q / 2, qy + q + 40, "the path starts and ends at that point", size=15.5, fill=RED, anchor="middle")
f.text(qx + q / 2, qy + q + 60, "(two segments; the right edge continues the left)", size=14.5, fill=MUTED, anchor="middle")

# winding statement
f.rect(60, 482, 980, 74, fill="none", stroke=RULE, sw=1.2, rx=6)
f.text(550, 510, "lifted endpoints differ; quotient endpoints coincide; the pair (2, −1) is retained", size=18, anchor="middle")
f.text(550, 536, "two turns one way and one back; no deformation keeping the loop based can erase it:  π₁(T²) = ℤ × ℤ", size=16, anchor="middle", fill=MUTED)

# ---------- bottom: when does a flow return?
f.text(550, 600, "even on one torus, the law of motion decides what return means:  [αt, βt] returns at T > 0 only if Tα and Tβ are both integers", size=16.5, anchor="middle", italic=True)
sq = 170
for (cx_, alpha, beta, Tmax, lab1, lab2, col) in ((330, 3, 2, 1, "α : β = 3 : 2", "exact return at T = 1, winding (3, 2)", INDIGO),
                                                  (770, 1, math.sqrt(2), 14, "α : β = 1 : √2", "no exact return at any T > 0", RED)):
    bx, by = cx_ - sq / 2, 628
    f.rect(bx, by, sq, sq, fill=PANEL, stroke=INK, sw=1.8)
    for seg in wrap_segments(alpha, beta, Tmax):
        (a, b), (c, d) = seg
        f.line(bx + sq * a, by + sq * (1 - b), bx + sq * c, by + sq * (1 - d), stroke=col, sw=(2.4 if Tmax == 1 else 1.1))
    f.circle(bx, by + sq, 6, fill=INK, stroke=INK)
    f.text(cx_, by + sq + 26, lab1, size=17, anchor="middle", mono=True)
    f.text(cx_, by + sq + 48, lab2, size=15.5, anchor="middle", fill=col)
f.text(550, 880, "a bounded space need not give a periodic trajectory: compactness, periodicity and winding are distinct properties", size=15, anchor="middle", fill=MUTED, italic=True)
f.save(OUT)
print("wrote", OUT)
