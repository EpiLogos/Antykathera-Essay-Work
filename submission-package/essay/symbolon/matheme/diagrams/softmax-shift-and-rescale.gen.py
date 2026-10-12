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


# ---- generator: a shift the observations cannot see, a rescaling they can (Return of Zero, M38) ----
import os, math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "softmax-shift-and-rescale.svg")

def softmax(z):
    m = max(z); e = [math.exp(v - m) for v in z]; s = sum(e); return [v / s for v in e]
def sigma(x):
    return 1 / (1 + math.exp(-x))

Z = [2.0, 1.0, 0.0]
cases = [
    ("the scores as given", "z = (2, 1, 0)", Z, None),
    ("add the same constant to every score", "z + 5 = (7, 6, 5)", [v + 5 for v in Z], ("invisible: the distribution", "is unchanged")),
    ("rescale the differences, temperature 2", "z / 2 = (1, 0.5, 0)", [v / 2 for v in Z], ("visible: the distribution", "changes")),
]
P0 = softmax(Z)
TITLE = "A shift the observations cannot see, a rescaling they can"
DESC = ("Three rows apply different operations to the same three scores, 2, 1 and 0, for candidates A, B and C. Each row "
        "shows the scores as bars, the softmax distribution they give, and the Bradley-Terry preference of A over B. As given: "
        "probabilities %.3f, %.3f, %.3f and preference %.3f. After adding the same constant, five, to every score: the "
        "probabilities and the preference are identical. After halving the scores: probabilities %.3f, %.3f, %.3f and preference "
        "%.3f, a changed distribution. A footer gives the reference-policy form: a common addition to the reward cancels in "
        "normalisation, while replacing the reference policy does not." % (
            *P0, sigma(1), *softmax([1, .5, 0]), sigma(.5)))
f = Fig(1100, 920, TITLE, DESC)
f.header("Diagram", "A shift the observations cannot see, a rescaling they can", "softmax and the Bradley–Terry comparison depend on differences of scores, not on their origin")

f.text(330, 150, "scores", size=16, fill=MUTED, italic=True)
f.text(580, 150, "softmax distribution", size=16, fill=MUTED, italic=True)
f.text(830, 150, "preference of A over B", size=16, fill=MUTED, italic=True)
for k, (op, expr, z, verdict) in enumerate(cases):
    y = 168 + k * 206
    p = softmax(z)
    changed = verdict is not None and verdict[0].startswith("visible")
    f.rect(50, y, 1000, 196, fill=PANEL, stroke=RULE, sw=1.4, rx=6)
    f.text(72, y + 34, op, size=16.5, italic=True)
    f.text(72, y + 66, expr, size=17, mono=True)
    if verdict:
        f.lines(72, y + 108, verdict, step=22, size=16, fill=(RED if changed else INDIGO), bold=True)
    # score bars
    base = y + 140; sc = 10
    for i, (name, v) in enumerate(zip("ABC", z)):
        x = 330 + i * 54
        h = max(v * sc, 1.5)
        f.rect(x, base - h, 36, h, fill=RULE, stroke=MUTED, sw=1.2)
        f.text(x + 18, base + 42, f"{v:g}", size=15, anchor="middle", mono=True, fill=MUTED)
        f.text(x + 18, base + 20, name, size=16, anchor="middle")
    f.line(318, base, 330 + 3 * 54 - 10, base, stroke=MUTED, sw=1.2)
    f.line(488, y + 90, 545, y + 90, stroke=INK, sw=2, marker="ah")
    f.text(517, y + 80, "softmax", size=14.5, anchor="middle", fill=MUTED)
    # probability bars
    bx0 = 565; bw = 44; gap = 14; ps = 118
    for i, (name, pv) in enumerate(zip("ABC", p)):
        x = bx0 + i * (bw + gap)
        h = pv * ps
        if changed:
            h0 = P0[i] * ps
            f.rect(x, base - h0, bw, h0, fill="none", stroke=MUTED, sw=1.4, dash="5 4")
        f.rect(x, base - h, bw, h, fill=(RED if changed else INDIGO), stroke=INK, sw=1.2, opacity=None) if False else f.rect(x, base - h, bw, h, fill=(RED if changed else INDIGO), stroke=INK, sw=1.2)
        f.text(x + bw / 2, base + 42, f"{pv:.3f}", size=14.5, anchor="middle", mono=True, fill=(RED if changed else INDIGO))
        f.text(x + bw / 2, base + 20, name, size=16, anchor="middle")
    f.line(555, base, bx0 + 3 * bw + 2 * gap + 10, base, stroke=MUTED, sw=1.2)
    # Bradley-Terry pair (candidates A, B)
    ra, rb = z[0], z[1]
    f.text(790, y + 66, "P(A ≻ B) = σ(r_A − r_B)", size=17, mono=True)
    f.text(790, y + 100, f"r_A − r_B = {ra - rb:g}", size=17, mono=True)
    f.text(790, y + 134, f"P = σ({ra - rb:g}) = {sigma(ra - rb):.3f}", size=19, mono=True, fill=(RED if changed else INDIGO), bold=True)
    if changed:
        f.text(1030, y + 30, "dashed: the row-one distribution", size=14, fill=MUTED, anchor="end", italic=True)

fy = 812
f.line(60, fy - 14, 1040, fy - 14, stroke=RULE, sw=1.2)
f.text(550, fy + 12, "a common constant drops out in normalisation; a change to the measure of difference does not", size=17, anchor="middle", italic=True)
f.text(550, fy + 44, "reference policy:  π*(y|x) ∝ π_ref(y|x) · exp(r(x,y)/β)", size=17, anchor="middle", mono=True)
f.text(550, fy + 72, "adding a constant to r cancels through normalisation; replacing π_ref changes the weight each possibility departs from", size=15.5, fill=MUTED, anchor="middle")
f.save(OUT)
print("wrote", OUT)
