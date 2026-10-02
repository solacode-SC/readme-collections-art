#!/usr/bin/env python3
"""
Isekai Storybook - animated light/dark GitHub profile README generator.
Owner: Solayman El Mouden (solacode-SC).  Run:  python3 generate_assets.py
Needs: Python 3 + Pillow.  Deterministic (seeded).
"""
import os, re, math, random, base64, io
from PIL import Image

# =============================================================================
# EDIT CONTENT HERE
# =============================================================================
NAME_1, NAME_2 = "Solayman", "El Mouden"
HANDLE = "solacode-SC"
GITHUB = "https://github.com/solacode-SC"
PORTFOLIO = "https://solaymantech.me"
LINKEDIN = "https://www.linkedin.com/in/YOUR-LINKEDIN"   # <-- REPLACE ME
ROLE = "SOFTWARE ENGINEER"
PILLARS = "AI  |  Math  |  Newest Technologies"
TAGLINE = ["Building systems, web applications,",
           "developer tools and intelligent",
           "software for a better tomorrow."]
ABOUT = ["I'm Solayman El Mouden, a software engineer",
         "focused on systems, web technologies,",
         "artificial intelligence and mathematics.",
         "I enjoy understanding how things work underneath",
         "the abstraction and turning that knowledge into",
         "useful software."]
JOURNEY = [("C / C++", "Systems"), ("Python", "Backend & AI"),
           ("TypeScript", "Web & Tools"), ("Docker", "Infrastructure"),
           ("Linux", "DevOps")]
SKILLS = [("C/C++", "C++"), ("Python", "Py"), ("JavaScript", "JS"),
          ("TypeScript", "TS"), ("React", "Rx"), ("Next.js", "N"),
          ("Django", "dj"), ("FastAPI", "FA"), ("PostgreSQL", "Pg"),
          ("Docker", "Dk"), ("Linux", "Lx"), ("Git", "Git")]
# (title, slug, [desc line 1, desc line 2], tags, crop (cx, cy, width) on art/source.jpg)
PROJECTS = [
    ("LazyEquation", "lazyequation", ["Interactive math & physics", "visualization platform."],
     ["React", "TS", "Fastify", "PostgreSQL"], (220, 480, 240)),
    ("LeetResume", "leetresume", ["AI-powered resume builder", "and optimizer."],
     ["Next.js", "Prisma", "Postgres"], (590, 720, 200)),
    ("Libora", "libora", ["Flutter PDF reader with", "modern experience."],
     ["Flutter", "Dart", "Riverpod"], (370, 320, 200)),
    ("Webserv", "webserv", ["C++98 HTTP server", "from scratch."],
     ["C++98", "Networking"], (360, 500, 240)),
    ("solaJobs v2", "solajobs-v2", ["Arabic-first job board", "platform."],
     ["Arabic-first", "Jobs"], (390, 720, 330)),
    ("Alert Generator", "prometheus-alert-generator", ["AI generator for Prometheus", "alert rules."],
     ["AI", "Prometheus"], (410, 660, 170)),
    ("Compose Dashboard", "docker-compose-dashboard", ["Docker Compose", "dashboard."],
     ["Docker", "Compose"], (560, 300, 220)),
]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]
FOOT_1 = "Build  \u00b7  Explore  \u00b7  Understand"
FOOT_2 = "Software Engineering \u00b7 Systems \u00b7 AI \u00b7 Mathematics"
BRAND = "NashirTech  \u00b7  \u0646\u0627\u0634\u0631 \u062a\u0643"
HERO_CROP = (170, 10, 560, 542)    # castle clearing between the trees
AVATAR_CROP = (300, 230, 440, 370)  # castle spires
# =============================================================================

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)
SRC = Image.open(os.path.join(ROOT, "art", "source.jpg")).convert("RGB")

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {   # dark = moonlit forest, light = storybook daylight
    "dark": dict(bg="#0b1030", panel="#141d4d", ink="#eef0fa", mut="#aab5df",
                 trunk="#24347e", trunk2="#3d4fa8", swirl="#34507f", swirl2="#86a8c4",
                 gold="#f0c25a", goldtx="#f0c25a", coral="#ee7f5f", cream="#f4e6bb",
                 magic="#8fd3ff", rib="#24347e", ribtx="#f9efcf", chip="#1c2a66", sky="#1a2a63"),
    "light": dict(bg="#efe5ca", panel="#f8f1de", ink="#1b2457", mut="#4c5686",
                  trunk="#2b3f8c", trunk2="#4a5fb0", swirl="#8fb0c4", swirl2="#4f7896",
                  gold="#b3822a", goldtx="#7d5a12", coral="#d9583a", cream="#fff6d8",
                  magic="#2b6fb0", rib="#2b3f8c", ribtx="#fff6d8", chip="#e8dcb8", sky="#c6d3d8"),
}

CSS = """.a{transform-box:fill-box;transform-origin:center}
.spin{animation:spin 80s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.spinr{animation:spin 110s linear infinite reverse}
.swim{animation:swim 18s ease-in-out infinite alternate}
@keyframes swim{from{transform:translateX(0)}to{transform:translateX(34px)}}
.flag{transform-origin:left center;animation:flag 3.2s ease-in-out infinite alternate}
@keyframes flag{from{transform:skewY(-6deg) scaleX(1)}to{transform:skewY(6deg) scaleX(.9)}}
.rise{animation:rise 9s ease-in infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.95}100%{transform:translateY(-70px);opacity:0}}
.pulse{animation:pulse 6s ease-in-out infinite alternate}
@keyframes pulse{from{opacity:.55}to{opacity:1}}
.kb{animation:kb 24s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
.dash{animation:dash 7s linear infinite}
@keyframes dash{to{stroke-dashoffset:-60}}
.shim{animation:shim 9s ease-in-out infinite}
@keyframes shim{0%,55%{transform:translateX(-120px)}100%{transform:translateX(420px)}}
.tw{animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion: reduce){.spin,.spinr,.swim,.flag,.rise,.pulse,.kb,.dash,.shim,.tw{animation:none}}"""


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def uri(cx_cy_w=None, box=None, size=(400, 190), q=80):
    if box is None:
        cx, cy, w = cx_cy_w
        h = w * size[1] / size[0]
        box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    box = tuple(int(round(b)) for b in box)
    im = SRC.crop(box).resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def save(name, theme, svg):
    svg = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", "&amp;", svg)
    with open(os.path.join(ASSETS, f"{name}-{theme}.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)


def root(w, h, T, title, body, extra_defs=""):
    d = (f'<defs><radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{T["magic"]}" stop-opacity=".42"/>'
         f'<stop offset="1" stop-color="{T["magic"]}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T["gold"]}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{T["gold"]}" stop-opacity=".38"/><stop offset="1" stop-color="{T["gold"]}" stop-opacity="0"/></linearGradient>'
         f'<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5"/>'
         f'<feColorMatrix values="0 0 0 0 .4  0 0 0 0 .4  0 0 0 0 .5  0 0 0 .5 -.16"/></filter>{extra_defs}</defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<title>{title}</title><style>{CSS}</style>{d}{body}'
            f'<rect class="grain" width="{w}" height="{h}" fill="#000" opacity=".5" filter="url(#noise)"/></svg>')


# ------------------------------------------------------------------ ornaments
def scallop(r, rng, bumps=18, amp=.05, ph=0.0):
    pts = []
    n = bumps * 6
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * (1 + amp * math.sin(bumps * a + ph))
        pts.append(f"{f(rr*math.cos(a))},{f(rr*math.sin(a))}")
    return "M" + " L".join(pts) + "Z"


def swirl(r, T, seed, rings=5, base=True, bumps=16):
    """Concentric scalloped rings, the storybook 'cloud bush'."""
    rng = random.Random(seed)
    ph = rng.random() * 6
    out = []
    if base:
        out.append(f'<path d="{scallop(r, rng, bumps, .05, ph)}" fill="{T["swirl"]}" stroke="{T["swirl2"]}" stroke-width="1.2"/>')
    for k in range(1, rings):
        rr = r * (1 - k / rings * .92)
        out.append(f'<path d="{scallop(rr, rng, bumps, .05, ph + k)}" fill="none" stroke="{T["swirl2"]}" stroke-width="1.1" opacity=".9"/>')
    return "".join(out)


def bush_row(T, x0, x1, y, seed, r=34, step=46, op=1):
    rng = random.Random(seed)
    out = []
    x = x0
    while x < x1:
        out.append(f'<g transform="translate({f(x)},{f(y + rng.uniform(-8, 8))})">{swirl(r * rng.uniform(.8, 1.2), T, rng.randint(0, 999), 4)}</g>')
        x += step * rng.uniform(.8, 1.1)
    return f'<g opacity="{op}">{"".join(out)}</g>'


def trunk(x, y, w, h, T, seed):
    rng = random.Random(seed)
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T["trunk"]}"/>']
    d = "".join(f"M{f(x + w*rng.uniform(.1, .9))},{y}v{h}" for _ in range(max(3, int(w / 7))))
    g.append(f'<path d="{d}" stroke="{T["trunk2"]}" stroke-width="1.2" opacity=".7" fill="none"/>')
    for _ in range(max(1, int(h / 220))):
        kx, ky = x + w * rng.uniform(.3, .7), y + h * rng.uniform(.1, .9)
        g.append(f'<ellipse cx="{f(kx)}" cy="{f(ky)}" rx="{f(w*.12)}" ry="{f(w*.2)}" fill="none" stroke="{T["trunk2"]}" stroke-width="1.4"/>')
    return "".join(g)


def castle(T, x, y, s=1.0, dark=False):
    cream, coral, g = T["cream"], T["coral"], T["gold"]
    win = g if dark else T["trunk"]
    wins = "".join(f'<rect class="tw" style="animation-delay:-{i*1.1}s" x="{wx}" y="{wy}" width="4" height="7" rx="1.5" fill="{win}"/>'
                   for i, (wx, wy) in enumerate([(-22, -26), (-8, -30), (8, -24), (-30, -10), (20, -8)]))
    return (f'<g transform="translate({f(x)},{f(y)}) scale({s})">'
            f'<path d="M-62,6C-50,-6 -30,-2 -10,4C10,10 30,0 62,6L52,40H-52Z" fill="{T["cream"]}" opacity=".55"/>'
            f'<rect x="-34" y="-34" width="52" height="38" fill="{cream}" stroke="{T["trunk"]}" stroke-width="1"/>'
            f'<path d="M-40,-34L-8,-62L24,-34Z" fill="{coral}" stroke="{T["trunk"]}" stroke-width="1"/>'
            f'<rect x="-52" y="-52" width="16" height="56" fill="{cream}" stroke="{T["trunk"]}" stroke-width="1"/>'
            f'<path d="M-56,-52L-44,-84L-32,-52Z" fill="{coral}" stroke="{T["trunk"]}" stroke-width="1"/>'
            f'<rect x="18" y="-44" width="14" height="48" fill="{cream}" stroke="{T["trunk"]}" stroke-width="1"/>'
            f'<path d="M15,-44L25,-72L35,-44Z" fill="{coral}" stroke="{T["trunk"]}" stroke-width="1"/>'
            f'<path d="M-44,-84V-96" stroke="{T["trunk"]}" stroke-width="1.2"/>'
            f'<path class="flag" d="M-44,-96L-30,-92L-44,-88Z" fill="{coral}"/>{wins}</g>')


def rider(T, x, y, s=1.0, cloak="coral", hat=True, delay=0):
    body = T[cloak] if cloak in T else cloak
    t, g = T["trunk"], T["gold"]
    return (f'<g transform="translate({f(x)},{f(y)}) scale({s})"><g class="a swim" style="animation-delay:{delay}s">'
            f'<path d="M-24,-2C-24,-14 -4,-16 14,-12C20,-18 24,-26 32,-26L36,-20C32,-18 30,-12 24,-4C20,6 12,8 -24,-2Z" fill="{t}" stroke="{g}" stroke-width=".8"/>'
            f'<path d="M-18,4V22M-6,6V22M10,4V22M18,2V22" stroke="{t}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M-24,-4C-34,-2 -36,8 -34,14" stroke="{t}" stroke-width="2.4" fill="none"/>'
            f'<path d="M-6,-12C-14,-30 -4,-40 6,-34C12,-30 12,-16 10,-10Z" fill="{body}" stroke="{g}" stroke-width=".8"/>'
            f'<circle cx="2" cy="-42" r="5" fill="{T["cream"]}" stroke="{t}" stroke-width=".8"/>'
            + (f'<path d="M-3,-45L3,-64L8,-45Z" fill="{T["coral"]}"/>' if hat else "")
            + f'<path d="M12,-30L40,-58" stroke="{g}" stroke-width="1.4"/><path d="M40,-58l8,3l-6,4Z" fill="{T["cream"]}"/></g></g>')


def corner(T, x, y, sx, sy):
    g = T["gold"]
    return (f'<g transform="translate({x},{y}) scale({sx},{sy})" fill="none" stroke="{g}" stroke-width="1.2">'
            f'<path d="M6,6C26,6 30,18 20,24C12,28 8,20 14,16"/><path d="M6,6C6,26 18,30 24,20C28,12 20,8 16,14"/>'
            f'<circle cx="6" cy="6" r="2.2" fill="{g}"/></g>')


def window(T, x, y, w, h, n=14):
    g = T["gold"]
    d = f"M{x+n},{y}H{x+w-n}L{x+w},{y+n}V{y+h-n}L{x+w-n},{y+h}H{x+n}L{x},{y+h-n}V{y+n}Z"
    i = 6
    d2 = f"M{x+n+i},{y+i}H{x+w-n-i}L{x+w-i},{y+n+i}V{y+h-n-i}L{x+w-n-i},{y+h-i}H{x+n+i}L{x+i},{y+h-n-i}V{y+n+i}Z"
    return (f'<path d="{d}" fill="{T["panel"]}" stroke="{g}" stroke-width="1.8"/>'
            f'<path d="{d2}" fill="none" stroke="{g}" stroke-width=".8" opacity=".6"/>'
            + corner(T, x + 10, y + 10, 1, 1) + corner(T, x + w - 10, y + 10, -1, 1)
            + corner(T, x + 10, y + h - 10, 1, -1) + corner(T, x + w - 10, y + h - 10, -1, -1))


def star4(T, x, y, s=6, col=None):
    col = col or T["gold"]
    return (f'<path transform="translate({f(x)},{f(y)}) scale({s/6})" d="M0,-8L2,-2L8,0L2,2L0,8L-2,2L-8,0L-2,-2Z" fill="{col}"/>')


def label(T, x, y, num, text):
    return (f'{star4(T, x + 6, y - 5, 7)}'
            f'<text x="{x+20}" y="{y}" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{T["goldtx"]}" font-weight="700">{num}  \u00b7  {text}</text>')


def fireflies(T, pts, seed=1):
    rng = random.Random(seed)
    return "".join(f'<circle class="a rise" cx="{x}" cy="{y}" r="{f(rng.uniform(1.4, 2.6))}" fill="{T["gold"]}" '
                   f'style="animation-delay:-{f(rng.uniform(0, 9))}s;animation-duration:{f(rng.uniform(7, 12))}s"/>' for x, y in pts)


def divider(T, x0, x1, y, delay=0):
    pts = " L".join(f"{x},{f(y + 2.4*math.sin(x/34))}" for x in range(int(x0), int(x1) + 1, 10))
    g = T["gold"]
    nodes = "".join(star4(T, x, y + 2.4 * math.sin(x / 34), 5) for x in range(int(x0) + 90, int(x1), 180))
    return (f'<path d="M{pts}" fill="none" stroke="{g}" stroke-width="1" opacity=".75"/>'
            f'<path d="M{pts}" fill="none" stroke="{T["cream"]}" stroke-width="2" stroke-linecap="round" '
            f'stroke-dasharray="1 14" class="dash" style="animation-delay:{delay}s" opacity=".85"/>{nodes}')


def magic_circle(T, cx, cy, r, seed=3):
    rng = random.Random(seed)
    g, m = T["gold"], T["magic"]
    runes = []
    n = 28
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * .9
        px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
        deg = math.degrees(a) + 90
        segs = "".join(f"M{f(rng.uniform(-3,3))},{f(rng.uniform(-4,4))}l{f(rng.uniform(-3,3))},{f(rng.uniform(-4,4))}" for _ in range(3))
        runes.append(f'<path transform="translate({f(px)},{f(py)}) rotate({f(deg)})" d="{segs}" stroke="{m}" stroke-width="1.3" fill="none" stroke-linecap="round"/>')
    star = []
    for k in (3,):
        pts = [(cx + r * .78 * math.cos(2 * math.pi * i * k / 8 - math.pi / 2), cy + r * .78 * math.sin(2 * math.pi * i * k / 8 - math.pi / 2)) for i in range(8)]
        star.append('<path d="M' + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + 'Z" fill="none" stroke="' + g + '" stroke-width="1" opacity=".8"/>')
    return (f'<g class="a spin" opacity=".9"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{g}" stroke-width="1.6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{f(r*.96)}" fill="none" stroke="{m}" stroke-width=".8" stroke-dasharray="2 5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{f(r*.82)}" fill="none" stroke="{g}" stroke-width=".8"/>'
            f'{"".join(runes)}{"".join(star)}</g>'
            f'<g class="a spinr" opacity=".7"><circle cx="{cx}" cy="{cy}" r="{f(r*.64)}" fill="none" stroke="{m}" stroke-width="1" stroke-dasharray="10 6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{f(r*.58)}" fill="none" stroke="{g}" stroke-width=".7"/></g>')


# --------------------------------------------------------------------- panels
def hero(T, th):
    dark = th == "dark"
    img = uri(box=HERO_CROP, size=(516, 704), q=80)
    av = uri(box=AVATAR_CROP, size=(64, 64), q=80)
    cx, ax, ay, aw, ah = 710, 565, 70, 290, 390
    arch = lambda x, y, w, h: f"M{x},{y+h}V{y+w/2}A{w/2},{w/2} 0 0 1 {x+w},{y+w/2}V{y+h}Z"
    b = [f'<rect width="900" height="520" fill="{T["bg"]}"/>', '<clipPath id="pc"><rect width="900" height="520"/></clipPath><g clip-path="url(#pc)">']
    if dark:
        rng = random.Random(4)
        b += [f'<circle class="tw" style="animation-delay:-{f(rng.uniform(0,4))}s" cx="{rng.randint(20,880)}" cy="{rng.randint(10,300)}" r="{f(rng.uniform(.8,1.8))}" fill="{T["cream"]}"/>' for _ in range(34)]
    b.append(f'<circle class="a pulse" cx="{cx}" cy="265" r="270" fill="url(#gl)"/>')
    b.append(trunk(0, 0, 30, 520, T, 1) + trunk(42, 0, 16, 520, T, 2) + trunk(866, 0, 34, 520, T, 3))
    b.append(magic_circle(T, cx, 265, 205))
    b.append(bush_row(T, 20, 900, 516, 8, 36, 44))
    b.append(rider(T, 80, 494, .85, "coral", True, 0) + rider(T, 190, 498, .8, "cream", True, -5)
             + rider(T, 300, 494, .85, "gold", True, -9))
    b.append(fireflies(T, [(90, 440), (260, 430), (480, 450), (520, 380), (880, 420), (600, 470)], 2))
    b.append('</g>')
    # portal
    b.append(f'<clipPath id="hc"><path d="{arch(ax+8, ay+8, aw-16, ah-16)}"/></clipPath>'
             f'<linearGradient id="vg" x1="0" y1="0" x2="0" y2="1"><stop offset=".65" stop-color="{T["bg"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{T["bg"]}" stop-opacity=".5"/></linearGradient>')
    b.append(f'<path d="{arch(ax, ay, aw, ah)}" fill="{T["panel"]}" stroke="{T["gold"]}" stroke-width="2.2"/>')
    b.append(f'<path d="{arch(ax-6, ay-6, aw+12, ah+12)}" fill="none" stroke="{T["gold"]}" stroke-width=".8" opacity=".7"/>')
    b.append(f'<g clip-path="url(#hc)"><image class="a kb" x="{ax+8}" y="{ay+8}" width="{aw-16}" height="{ah-16}" preserveAspectRatio="xMidYMid slice" xlink:href="{img}"/>'
             f'<rect x="{ax+8}" y="{ay+8}" width="{aw-16}" height="{ah-16}" fill="url(#vg)"/>'
             f'<g transform="skewX(-20)"><rect class="a shim" x="570" y="70" width="40" height="390" fill="url(#shg)"/></g></g>')
    b.append(star4(T, cx, ay - 12, 11))
    # text
    b.append('<clipPath id="av"><circle cx="76" cy="52" r="14"/></clipPath>'
             f'<image x="62" y="38" width="28" height="28" clip-path="url(#av)" xlink:href="{av}"/>'
             f'<circle cx="76" cy="52" r="14" fill="none" stroke="{T["gold"]}" stroke-width="1.2"/>'
             f'<text x="100" y="56" font-family="{MONO}" font-size="12.5" fill="{T["mut"]}">{HANDLE} / README</text>'
             f'<path d="M62,78H500" stroke="{T["gold"]}" stroke-width=".8" stroke-dasharray="2 5" opacity=".7"/>')
    b.append(f'<text x="62" y="136" font-family="{SERIF}" font-style="italic" font-size="22" fill="{T["mut"]}">Hi, I\'m</text>'
             f'<text x="60" y="204" font-family="{SERIF}" font-weight="700" font-size="66" fill="{T["ink"]}">{NAME_1}</text>'
             f'<text x="60" y="272" font-family="{SERIF}" font-weight="700" font-size="66" fill="{T["ink"]}">{NAME_2}</text>'
             f'<text x="62" y="312" font-family="{MONO}" font-weight="700" font-size="14" letter-spacing="5" fill="{T["goldtx"]}">{ROLE}</text>'
             f'<text x="62" y="338" font-family="{MONO}" font-size="13" fill="{T["ink"]}">{PILLARS}</text>')
    for i, ln in enumerate(TAGLINE):
        b.append(f'<text x="62" y="{378 + i*22}" font-family="{SERIF}" font-size="15" fill="{T["mut"]}">{ln}</text>')
    return root(900, 520, T, f"{NAME_1} {NAME_2} - {ROLE.title()}", "".join(b))


def button(T, th, text):
    g = T["gold"]
    d = "M12,1H138L149,12V28L138,39H12L1,28V12Z"
    b = (f'<path d="{d}" fill="{T["panel"]}" stroke="{g}" stroke-width="1.4"/>' + star4(T, 22, 20, 8)
         + f'<text x="38" y="25" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{T["ink"]}">{text}</text>')
    return root(150, 40, T, text.title(), b)


def about(T, th):
    b = [f'<rect width="900" height="330" fill="{T["bg"]}"/>', window(T, 20, 14, 860, 302),
         label(T, 56, 58, "I", "ABOUT"), label(T, 536, 58, "II", "MY JOURNEY")]
    for i, ln in enumerate(ABOUT):
        b.append(f'<text x="58" y="{106 + i*28}" font-family="{SERIF}" font-size="15" fill="{T["ink"]}">{ln}</text>')
    for i, (lang, area) in enumerate(JOURNEY):
        y = 108 + i * 38
        b.append(star4(T, 540, y - 5, 6)
                 + f'<text x="554" y="{y}" font-family="{MONO}" font-size="14" font-weight="700" fill="{T["ink"]}">{lang}</text>'
                 + f'<path d="M656,{y-5}H708" stroke="{T["gold"]}" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="1 7" class="dash" style="animation-delay:-{i}s"/>'
                 + f'<text x="720" y="{y}" font-family="{SERIF}" font-size="15" fill="{T["ink"]}">{area}</text>')
    b.append(divider(T, 56, 844, 288))
    b.append(fireflies(T, [(480, 280), (500, 250), (60, 270)], 5))
    return root(900, 330, T, "About Solayman El Mouden and his journey", "".join(b))


def orb(T, i, mono):
    spin = "spin" if i % 2 == 0 else "spinr"
    return (f'<circle r="42" fill="url(#gl)"/><g class="a {spin}">{swirl(36, T, 70 + i, 5, True, 14)}</g>'
            f'<circle r="19" fill="{T["trunk"]}" stroke="{T["gold"]}" stroke-width="1.2"/>'
            f'<text y="5" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{T["ribtx"]}">{mono}</text>')


def skills(T, th):
    b = [f'<rect width="900" height="360" fill="{T["bg"]}"/>', window(T, 20, 14, 860, 330), label(T, 56, 58, "III", "TECHNOLOGIES &amp; SKILLS"),
         divider(T, 56, 844, 80, -2)]
    for i, (name, mono) in enumerate(SKILLS):
        cx = 121.5 + (i % 6) * 131
        cy = 148 + (i // 6) * 114
        b.append(f'<g transform="translate({f(cx)},{cy})">{orb(T, i, mono)}</g>')
        b.append(f'<text x="{f(cx)}" y="{cy + 62}" text-anchor="middle" font-family="{SERIF}" font-size="12.5" fill="{T["ink"]}">{name}</text>')
    return root(900, 360, T, "Technologies and skills: " + ", ".join(s[0] for s in SKILLS), "".join(b))


def projects_title(T, th):
    g = T["gold"]
    rib = "M300,18H600L612,34L600,50H300L288,34Z"
    b = [f'<rect width="900" height="90" fill="{T["bg"]}"/>', divider(T, 40, 280, 34), divider(T, 620, 860, 34, -3),
         f'<path d="{rib}" fill="{T["rib"]}" stroke="{g}" stroke-width="1.6"/>',
         f'<text x="450" y="39" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="{T["ribtx"]}">IV  \u00b7  SELECTED PROJECTS</text>',
         f'<path d="M300,60V84M600,60V84" stroke="{g}" stroke-width="1.4"/>',
         f'<path class="flag" d="M300,60L324,66L300,72Z" fill="{T["coral"]}"/><path class="flag" d="M600,60L624,66L600,72Z" fill="{T["coral"]}" style="animation-delay:-1.5s"/>']
    return root(900, 90, T, "Selected projects", "".join(b))


def chips(T, tags):
    out, x, y = [], 8, 178
    for t in tags:
        w = len(t) * 6.4 + 14
        if x + w > 200:
            x, y = 8, y + 22
        out.append(f'<rect x="{f(x)}" y="{y}" width="{f(w)}" height="18" rx="9" fill="{T["chip"]}" stroke="{T["gold"]}" stroke-width=".6" stroke-opacity=".7"/>'
                   f'<text x="{f(x+w/2)}" y="{y+12.5}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{T["ink"]}">{t}</text>')
        x += w + 5
    return "".join(out)


def card(T, th, i, p):
    title, slug, desc, tags, crop = p
    img = uri(crop, size=(400, 190), q=80)
    n = 12
    d = f"M{n},1H{208-n}L207,{n}V{229-n}L{208-n},230H{n}L1,{229-n}V{n}Z"
    b = [f'<path d="{d}" fill="{T["panel"]}" stroke="{T["gold"]}" stroke-width="1.3"/>',
         '<clipPath id="tc"><rect x="8" y="8" width="192" height="92" rx="4"/></clipPath>',
         f'<g clip-path="url(#tc)"><image class="a kb" x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" xlink:href="{img}" style="animation-delay:-{i*3}s"/>'
         f'<g transform="skewX(-20)"><rect class="a shim" x="20" y="8" width="26" height="92" fill="url(#shg)" style="animation-delay:-{i*1.3}s"/></g></g>',
         f'<rect x="8" y="8" width="192" height="92" rx="4" fill="none" stroke="{T["gold"]}" stroke-width=".8" opacity=".85"/>',
         f'<path d="M14,8H70V34L42,27L14,34Z" fill="{T["rib"]}" stroke="{T["gold"]}" stroke-width="1"/>'
         f'<text x="42" y="22" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{T["ribtx"]}">{ROMAN[i]}</text>',
         f'<text x="10" y="126" font-family="{SERIF}" font-weight="700" font-size="16" fill="{T["ink"]}">{title}</text>',
         f'<text x="10" y="145" font-family="{SERIF}" font-size="11.5" fill="{T["mut"]}">{desc[0]}</text>',
         f'<text x="10" y="160" font-family="{SERIF}" font-size="11.5" fill="{T["mut"]}">{desc[1]}</text>',
         chips(T, tags)]
    return root(208, 230, T, f"Quest {ROMAN[i]}: {title} project card", "".join(b))


def footer(T, th):
    dark = th == "dark"
    b = [f'<rect width="900" height="270" fill="{T["bg"]}"/>', '<clipPath id="pc"><rect width="900" height="270"/></clipPath><g clip-path="url(#pc)">']
    if dark:
        rng = random.Random(9)
        b += [f'<circle class="tw" style="animation-delay:-{f(rng.uniform(0,4))}s" cx="{rng.randint(20,880)}" cy="{rng.randint(8,150)}" r="{f(rng.uniform(.8,1.7))}" fill="{T["cream"]}"/>' for _ in range(26)]
    b.append(f'<circle cx="780" cy="64" r="26" fill="{T["cream"] if dark else T["gold"]}" opacity="{".9" if dark else ".55"}"/>')
    b.append(f'<circle class="a pulse" cx="780" cy="64" r="80" fill="url(#gl)"/>')
    b.append(trunk(0, 0, 28, 270, T, 11) + trunk(36, 0, 14, 270, T, 12) + trunk(872, 0, 28, 270, T, 13))
    b.append(bush_row(T, 60, 860, 262, 21, 34, 44))
    b.append(castle(T, 150, 214, .95, dark))
    b.append(rider(T, 400, 238, .7, "coral", True, 0) + rider(T, 500, 240, .65, "cream", True, -6) + rider(T, 600, 238, .7, "gold", True, -10))
    b.append(fireflies(T, [(250, 200), (330, 170), (700, 190), (820, 210), (460, 200)], 7))
    b.append('</g>')
    b.append(f'<text x="450" y="80" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="30" fill="{T["ink"]}">{FOOT_1}</text>'
             f'<text x="450" y="110" text-anchor="middle" font-family="{MONO}" font-size="12.5" letter-spacing="1" fill="{T["mut"]}">{FOOT_2}</text>'
             + divider(T, 230, 670, 134, -1)
             + f'<text x="450" y="160" text-anchor="middle" font-family="{SERIF}" font-size="13" fill="{T["goldtx"]}">{BRAND}</text>')
    return root(900, 270, T, "Footer: Build, Explore, Understand", "".join(b))


# ----------------------------------------------------------------- README
def pic(name, alt, width="100%", href=None):
    h = (f'<picture>\n    <source media="(prefers-color-scheme: dark)"  srcset="assets/{name}-dark.svg">\n'
         f'    <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'    <img alt="{alt}" src="assets/{name}-light.svg" width="{width}">\n  </picture>')
    return f'<a href="{href}">\n  {h}\n</a>' if href else f'  {h}'


def write_readme():
    cards = [pic(f"card-{p[1]}", f"Quest {ROMAN[i]}, {p[0]}: {' '.join(p[2])} Tags: {', '.join(p[3])}.", "24%",
                 f"https://github.com/solacode-SC/{p[1]}") for i, p in enumerate(PROJECTS)]
    L = ['<div align="center">', "", pic("hero", f"{NAME_1} {NAME_2}, software engineer. AI, Math, Newest Technologies. A castle seen through a magic portal in a storybook forest."), "",
         " &nbsp; ".join([pic("btn-github", "GitHub profile", "150", GITHUB), pic("btn-linkedin", "LinkedIn profile", "150", LINKEDIN),
                          pic("btn-portfolio", "Portfolio website", "150", PORTFOLIO)]), "",
         pic("about", "About Solayman El Mouden and his journey: C/C++ systems, Python backend and AI, TypeScript web and tools, Docker infrastructure, Linux DevOps."), "",
         pic("skills", "Technologies and skills: " + ", ".join(s[0] for s in SKILLS) + "."), "",
         pic("projects-title", "Selected projects"), "",
         "\n".join(cards[:4]), "", "\n".join(cards[4:]), "",
         pic("footer", "Build, Explore, Understand. Software Engineering, Systems, AI, Mathematics."), "", "</div>", ""]
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main():
    for th, T in THEMES.items():
        save("hero", th, hero(T, th))
        for n, t in (("github", "GITHUB"), ("linkedin", "LINKEDIN"), ("portfolio", "PORTFOLIO")):
            save(f"btn-{n}", th, button(T, th, t))
        save("about", th, about(T, th))
        save("skills", th, skills(T, th))
        save("projects-title", th, projects_title(T, th))
        for i, p in enumerate(PROJECTS):
            save(f"card-{p[1]}", th, card(T, th, i, p))
        save("footer", th, footer(T, th))
    write_readme()
    print("done")


if __name__ == "__main__":
    main()
