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


# ---- generator: twelve fifths against seven octaves, the Pythagorean comma (Return of Zero, M29) ----
import os, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pythagorean-comma-fifths-and-octaves.svg")
LOG_FIFTH = math.log2(1.5)                    # 0.5849625...
OCT12 = 12 * LOG_FIFTH                        # 7.019550...
COMMA = (3 / 2) ** 12 / 2 ** 7                # 531441/524288
CENTS = 1200 * math.log2(COMMA)               # 23.46
TITLE = "Twelve pure fifths overshoot seven octaves by the Pythagorean comma"
DESC = ("Left, the pitch-class circle, pitch reduced by whole octaves, with twelve equal steps ticked around it. Twelve pure "
        "fifths, each three halves, are plotted as a chain of points with chords; the twelfth lands a little beyond the "
        "starting point, and the red arc between them is the comma. Right, the same journey lifted to pitch height: seven "
        "octaves and twelve fifths drawn as two bars that differ by a sliver, then magnified on a ruler to show twelve fifths "
        "at 7.0196 octaves against seven octaves at exactly seven. The residual is 531441 over 524288, about 1.01364, or "
        "23.46 cents, and it is not the whole tone nine eighths. Beneath, twelve-tone equal temperament closes exactly with "
        "twelve steps of two to the power one twelfth, its fifth being 700 cents against 701.955 for the pure fifth.")
f = Fig(1100, 930, TITLE, DESC)
f.header("Diagram", "Twelve fifths, seven octaves, one comma", "the pitch-class circle closes on itself; the lifted height keeps the register difference")

# ------- left: pitch-class circle
cx, cy, R = 325, 440, 200
def pol(theta_deg, r):
    a = math.radians(theta_deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)
f.text(cx, 160, "pitch class:  log₂ f  mod 1", size=17, italic=True, fill=MUTED, anchor="middle")
f.circle(cx, cy, R, fill=PANEL, stroke=INK, sw=2)
for j in range(12):                              # equal-tempered ticks
    x1, y1 = pol(30 * j, R - 10); x2, y2 = pol(30 * j, R + 10)
    f.line(x1, y1, x2, y2, stroke=RULE, sw=2)
ang = [(k * LOG_FIFTH % 1) * 360 for k in range(13)]
for k in range(12):                              # chords of the fifths chain
    a, b = pol(ang[k], R), pol(ang[k + 1], R)
    col, sw = (RED, 2.6) if k == 11 else (MUTED, 1.1)
    f.line(*a, *b, stroke=col, sw=sw)
f.path("M " + "{:.1f} {:.1f}".format(*pol(ang[0], R + 14)) + " A {0} {0} 0 0 1 ".format(R + 14) + "{:.1f} {:.1f}".format(*pol(ang[12], R + 14)), stroke=RED, sw=5)
for k in range(13):
    x, y = pol(ang[k], R)
    f.circle(x, y, 6.5, fill=(RED if k in (0, 12) else INDIGO), stroke=INK, sw=1)
for k in range(1, 12):
    x, y = pol(ang[k], R + 28)
    f.text(x, y + 6, str(k), size=17, anchor="middle", fill=INDIGO)
x, y = pol(-5, R + 30); f.text(x, y + 6, "0", size=17, anchor="end", fill=RED, bold=True)
x, y = pol(12, R + 30); f.text(x, y + 6, "12", size=17, anchor="start", fill=RED, bold=True)
f.text(cx, cy - 8, "k fifths up,", size=16, anchor="middle", fill=MUTED)
f.text(cx, cy + 14, "octaves removed", size=16, anchor="middle", fill=MUTED)
f.text(cx, cy + R + 62, "grey ticks: twelve equal steps · red arc: where twelve fifths land past the start", size=15, anchor="middle", fill=MUTED)

# ------- right: the lifted height
X0, W = 650, 400
ps = W / 7.02
f.text(X0 + W / 2, 160, "lifted to pitch height, in octaves", size=17, italic=True, fill=MUTED, anchor="middle")
f.text(X0, 188, "seven octaves", size=15); f.text(X0 + W, 188, "2⁷ = 128", size=15, anchor="end", mono=True)
f.rect(X0, 194, ps * 7, 20, fill=RULE, stroke=INK, sw=1.4)
f.text(X0, 238, "twelve fifths", size=15, fill=RED); f.text(X0 + W, 238, "(3/2)¹² ≈ 129.75", size=15, anchor="end", mono=True, fill=RED)
f.rect(X0, 244, ps * OCT12, 20, fill="#d9a9a2", stroke=RED, sw=1.4)
# zoom ruler
rx0, rw = 690, 360
lo, hi = 6.995, 7.025
rs = rw / (hi - lo)
def rxp(v): return rx0 + (v - lo) * rs
ry = 400
f.line(X0 + ps * 7, 268, rx0, ry - 50, stroke=RULE, sw=1.2, dash="4 4")
f.line(X0 + ps * OCT12, 268, rx0 + rw, ry - 50, stroke=RULE, sw=1.2, dash="4 4")
f.text(rx0 + rw / 2, 330, "magnified: the last 0.03 octave", size=15, anchor="middle", fill=MUTED, italic=True)
f.line(rx0, ry, rx0 + rw, ry, stroke=INK, sw=2)
for v in (7.000, 7.005, 7.010, 7.015, 7.020, 7.025):
    f.line(rxp(v), ry - 7, rxp(v), ry + 7, stroke=INK, sw=1.5)
    f.text(rxp(v), ry + 28, f"{v:.3f}", size=14.5, anchor="middle", mono=True, fill=MUTED)
f.circle(rxp(7.0), ry, 8, fill=INK, stroke=INK)
f.text(rxp(7.0), ry - 20, "seven octaves", size=15, anchor="middle")
f.circle(rxp(OCT12), ry, 8, fill=RED, stroke=RED)
f.text(rxp(OCT12), ry - 20, "twelve fifths", size=15, anchor="middle", fill=RED)
f.line(rxp(7.0), ry + 62, rxp(OCT12), ry + 62, stroke=RED, sw=2.4, marker="ahr")
f.line(rxp(OCT12), ry + 62, rxp(7.0) + 6, ry + 62, stroke=RED, sw=2.4, marker="ahr")
f.text(rx0 + rw / 2, ry + 92, "(3/2)¹² / 2⁷ = 531441 / 524288", size=17, anchor="middle", mono=True, fill=RED, bold=True)
f.text(rx0 + rw / 2, ry + 116, f"≈ {COMMA:.5f}  ≈ {CENTS:.2f} cents", size=16, anchor="middle", mono=True, fill=RED)
f.text(rx0 + rw / 2, ry + 142, "the comma, not the whole tone 9/8", size=15, anchor="middle", fill=MUTED, italic=True)

# ------- bottom: equal temperament
by = 748
f.line(60, by, 1040, by, stroke=RULE, sw=1.2)
f.text(550, by + 32, "Twelve-tone equal temperament closes exactly by changing what it preserves", size=18, anchor="middle", italic=True)
for cxx, a, b in ((215, "12 steps of 2^(1/12)", "close at 2/1 exactly"), (550, "its fifth 2^(7/12) ≈ 1.4983", "700 cents"), (885, "the pure fifth 3/2", "701.955 cents")):
    f.text(cxx, by + 62, a, size=15.5, anchor="middle", mono=True)
    f.text(cxx, by + 82, b, size=15.5, anchor="middle", mono=True, fill=MUTED)
f.text(550, by + 116, "the question is which relationship the tuning serves and what adjustment it makes audible", size=15.5, anchor="middle", fill=MUTED)
f.save(OUT)
print("wrote", OUT)
