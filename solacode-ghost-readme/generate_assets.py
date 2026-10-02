#!/usr/bin/env python3
"""
Spectral Archive - animated light/dark GitHub profile README generator.
Owner: Solayman El Mouden (solacode-SC).  Run:  python3 generate_assets.py
Needs: Python 3 + Pillow.  Deterministic (seeded).
"""
import os, re, math, random, base64, io
from PIL import Image, ImageOps

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
     ["React", "TS", "Fastify", "PostgreSQL"], (400, 80, 260)),
    ("LeetResume", "leetresume", ["AI-powered resume builder", "and optimizer."],
     ["Next.js", "Prisma", "Postgres"], (620, 800, 200)),
    ("Libora", "libora", ["Flutter PDF reader with", "modern experience."],
     ["Flutter", "Dart", "Riverpod"], (150, 350, 260)),
    ("Webserv", "webserv", ["C++98 HTTP server", "from scratch."],
     ["C++98", "Networking"], (430, 500, 240)),
    ("solaJobs v2", "solajobs-v2", ["Arabic-first job board", "platform."],
     ["Arabic-first", "Jobs"], (160, 880, 320)),
    ("Alert Generator", "prometheus-alert-generator", ["AI generator for Prometheus", "alert rules."],
     ["AI", "Prometheus"], (590, 580, 160)),
    ("Compose Dashboard", "docker-compose-dashboard", ["Docker Compose", "dashboard."],
     ["Docker", "Compose"], (200, 500, 300)),
]
FOOT_1 = "Build  \u00b7  Explore  \u00b7  Understand"
FOOT_2 = "Software Engineering \u00b7 Systems \u00b7 AI \u00b7 Mathematics"
BRAND = "NashirTech  \u00b7  \u0646\u0627\u0634\u0631 \u062a\u0643"
HERO_BOX = (0, 40, 736, 1004)       # engraving crop for the hero window
AVATAR_CROP = (230, 20, 530, 320)   # spiral staircase
# =============================================================================

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)
SRC = Image.open(os.path.join(ROOT, "art", "source.jpg")).convert("L")

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {   # dark = midnight reading room, light = aged paper
    "dark": dict(bg="#05090c", panel="#0b1519", panel2="#101e24", ink="#e6f1ee", mut="#9db5b0",
                 ecto="#8ff0d0", ectotx="#8ff0d0", ecto2="#3f9d8d", violet="#a79bff", gold="#ffd27a",
                 line="#2a4048", hatch="#8ff0d0", duo=("#03070a", "#2d5a55", "#a8d6cb"),
                 spines=["#16282e", "#1b3037", "#241f3d", "#173a34", "#2a2230", "#1c2c3a"],
                 gh_top=".55", gh_bot=".1", gh_fill="#8ff0d0", gh_line="#8ff0d0", eye="#05090c"),
    "light": dict(bg="#efece1", panel="#f8f6ee", panel2="#e7e3d4", ink="#1a2326", mut="#4b5a5c",
                  ecto="#2a8f7e", ectotx="#1d6f63", ecto2="#3c7f74", violet="#6d5fd0", gold="#c98a1a",
                  line="#c9c3ae", hatch="#1a2326", duo=("#141c1f", "#8a9a96", "#f4f1e6"),
                  spines=["#d9cfb4", "#cdd8cf", "#d8cbd2", "#cfd4c0", "#d4d0e0", "#e0d3bd"],
                  gh_top=".9", gh_bot=".45", gh_fill="#ffffff", gh_line="#1a2326", eye="#1a2326"),
}

CSS = """.a{transform-box:fill-box;transform-origin:center}
.bob{animation:bob 6s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(-5px) rotate(-2deg)}to{transform:translateY(6px) rotate(2deg)}}
.blink{animation:blink 7s ease-in-out infinite}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
.flick{animation:flick 2.4s ease-in-out infinite alternate}
@keyframes flick{from{transform:scale(1,1);opacity:.85}to{transform:scale(.85,1.15);opacity:1}}
.rise{animation:rise 10s ease-in infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.8}100%{transform:translateY(-80px);opacity:0}}
.pulse{animation:pulse 6s ease-in-out infinite alternate}
@keyframes pulse{from{opacity:.5}to{opacity:1}}
.kb{animation:kb 24s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
.dash{animation:dash 8s linear infinite}
@keyframes dash{to{stroke-dashoffset:-72}}
.shim{animation:shim 10s ease-in-out infinite}
@keyframes shim{0%,55%{transform:translateX(-120px)}100%{transform:translateX(420px)}}
.tw{animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion: reduce){.bob,.blink,.flick,.rise,.pulse,.kb,.dash,.shim,.tw{animation:none}}"""


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def uri(T, cx_cy_w=None, box=None, size=(400, 190), q=80):
    if box is None:
        cx, cy, w = cx_cy_w
        h = w * size[1] / size[0]
        box = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    box = tuple(int(round(b)) for b in box)
    im = SRC.crop(box).resize(size, Image.LANCZOS)
    lo, mid, hi = T["duo"]
    im = ImageOps.colorize(im, black=lo, white=hi, mid=mid)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def save(name, theme, svg):
    svg = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", "&amp;", svg)
    with open(os.path.join(ASSETS, f"{name}-{theme}.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)


def root(w, h, T, title, body):
    d = (f'<defs><radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{T["ecto"]}" stop-opacity=".32"/>'
         f'<stop offset="1" stop-color="{T["ecto"]}" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="cg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{T["gold"]}" stop-opacity=".55"/>'
         f'<stop offset="1" stop-color="{T["gold"]}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="gb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["gh_fill"]}" stop-opacity="{T["gh_top"]}"/>'
         f'<stop offset="1" stop-color="{T["gh_fill"]}" stop-opacity="{T["gh_bot"]}"/></linearGradient>'
         f'<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{T["ecto"]}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{T["ecto"]}" stop-opacity=".3"/><stop offset="1" stop-color="{T["ecto"]}" stop-opacity="0"/></linearGradient>'
         f'<pattern id="ht" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0V5" stroke="{T["hatch"]}" stroke-width=".8" opacity=".07"/></pattern>'
         f'<pattern id="twp" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><path d="M0,0H9" stroke="{T["ecto2"]}" stroke-width="1.8" opacity=".85"/></pattern>'
         f'<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7"/>'
         f'<feColorMatrix values="0 0 0 0 .5  0 0 0 0 .55  0 0 0 0 .5  0 0 0 .5 -.17"/></filter></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<title>{title}</title><style>{CSS}</style>{d}<rect width="{w}" height="{h}" fill="{T["bg"]}"/>'
            f'<rect width="{w}" height="{h}" fill="url(#ht)"/>{body}'
            f'<rect class="grain" width="{w}" height="{h}" fill="#000" opacity=".5" filter="url(#noise)"/></svg>')


# ------------------------------------------------------------------ ornaments
def ghost(T, x, y, s=1.0, delay=0, book=False, candle=False, flip=False, op=1):
    sx = -s if flip else s
    gl, gline, eye = T["gh_line"], T["gh_line"], T["eye"]
    body = ("M0,-40C-20,-40 -30,-25 -30,-5L-30,40C-26,34 -22,44 -16,38C-10,32 -6,44 0,38C6,32 10,44 16,38C22,34 26,44 30,40"
            "L30,-5C30,-25 20,-40 0,-40Z")
    parts = [f'<circle r="62" cy="0" fill="url(#gl)"/>',
             f'<path d="{body}" fill="url(#gb)" stroke="{gline}" stroke-width="1.3" stroke-linejoin="round"/>',
             f'<path d="M-30,6C-42,10 -44,22 -36,26M30,6C42,10 44,22 36,26" fill="none" stroke="{gline}" stroke-width="1.3" stroke-linecap="round"/>',
             f'<ellipse class="a blink" cx="-10" cy="-12" rx="4" ry="6" fill="{eye}"/><ellipse class="a blink" cx="10" cy="-12" rx="4" ry="6" fill="{eye}"/>',
             f'<ellipse cx="0" cy="3" rx="3" ry="5" fill="{eye}"/>']
    if book:
        parts.append(f'<rect x="-14" y="8" width="28" height="19" rx="2" fill="{T["violet"]}" stroke="{gline}" stroke-width="1"/>'
                     f'<path d="M0,8V27" stroke="{gline}" stroke-width=".8"/>')
    if candle:
        parts.append(f'<circle cx="38" cy="8" r="24" fill="url(#cg)"/><rect x="35" y="14" width="6" height="14" rx="1" fill="{T["panel2"]}" stroke="{gline}" stroke-width=".8"/>'
                     f'<path class="a flick" d="M38,13C34,8 38,4 38,0C42,4 42,9 38,13Z" fill="{T["gold"]}"/>')
    return (f'<g transform="translate({f(x)},{f(y)}) scale({f(sx)},{f(s)})" opacity="{op}">'
            f'<g class="a bob" style="animation-delay:{delay}s">{"".join(parts)}</g></g>')


def meander(T, x0, x1, y, delay=0, op=.9):
    d = "".join(f"M{x},{y+10}V{y}H{x+12}V{y+8}H{x+4}V{y+4}H{x+8}" for x in range(int(x0), int(x1) - 12, 16))
    return (f'<path d="{d}" fill="none" stroke="{T["ecto2"]}" stroke-width="1.2" opacity="{op}" stroke-linejoin="miter"/>'
            f'<path d="M{x0},{y+11}H{x1}" stroke="{T["ecto"]}" stroke-width="1.6" stroke-dasharray="2 10" stroke-linecap="round" '
            f'class="dash" style="animation-delay:{delay}s" opacity=".85"/>')


def column(T, x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{T["panel2"]}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#twp)" opacity=".55"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{T["line"]}" stroke-width="1"/>'
            f'<rect x="{x-4}" y="{y}" width="{w+8}" height="9" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="1"/>'
            f'<rect x="{x-4}" y="{y+h-9}" width="{w+8}" height="9" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="1"/>')


def frame(T, x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="1.6"/>'
            f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="2" fill="none" stroke="{T["ecto"]}" stroke-width=".7" opacity=".55"/>'
            + "".join(f'<path d="M{cx},{cy}h{12*sx}M{cx},{cy}v{12*sy}" stroke="{T["ecto"]}" stroke-width="2"/>'
                      for cx, cy, sx, sy in ((x + 4, y + 4, 1, 1), (x + w - 4, y + 4, -1, 1), (x + 4, y + h - 4, 1, -1), (x + w - 4, y + h - 4, -1, -1))))


def bookicon(T, x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect width="12" height="15" rx="1.5" fill="none" stroke="{T["ectotx"]}" stroke-width="1.5"/>'
            f'<path d="M3,3H9M3,6H9" stroke="{T["ectotx"]}" stroke-width="1"/></g>')


def label(T, x, y, num, text):
    return (bookicon(T, x, y - 13)
            + f'<text x="{x+22}" y="{y}" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{T["ectotx"]}" font-weight="700">SHELF {num}  /  {text}</text>')


def motes(T, pts, seed=1):
    rng = random.Random(seed)
    return "".join(f'<circle class="a rise" cx="{x}" cy="{y}" r="{f(rng.uniform(1.2, 2.4))}" fill="{T["ecto"]}" '
                   f'style="animation-delay:-{f(rng.uniform(0, 10))}s;animation-duration:{f(rng.uniform(8, 13))}s"/>' for x, y in pts)


def stars(T, n, seed, x0, x1, y0, y1):
    rng = random.Random(seed)
    return "".join(f'<circle class="tw" style="animation-delay:-{f(rng.uniform(0,4))}s" cx="{rng.randint(x0,x1)}" cy="{rng.randint(y0,y1)}" '
                   f'r="{f(rng.uniform(.8,1.7))}" fill="{T["ink"]}"/>' for _ in range(n))


# --------------------------------------------------------------------- panels
def hero(T, th):
    dark = th == "dark"
    img = uri(T, box=HERO_BOX, size=(520, 680), q=80)
    av = uri(T, box=AVATAR_CROP, size=(64, 64), q=80)
    fx, fy, fw, fh = 562, 80, 300, 388
    b = ['<clipPath id="pc"><rect width="900" height="540"/></clipPath><g clip-path="url(#pc)">']
    if dark:
        b.append(stars(T, 30, 3, 10, 520, 10, 300))
    b.append(f'<circle class="a pulse" cx="712" cy="274" r="270" fill="url(#gl)"/>')
    b.append(column(T, 540, 66, 16, 412) + column(T, 868, 66, 16, 412))
    b.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="2"/>'
             f'<rect x="{fx-5}" y="{fy-5}" width="{fw+10}" height="{fh+10}" fill="none" stroke="{T["ecto"]}" stroke-width=".8" opacity=".6"/>'
             f'<clipPath id="hc"><rect x="{fx+8}" y="{fy+8}" width="{fw-16}" height="{fh-16}"/></clipPath>'
             f'<g clip-path="url(#hc)"><image class="a kb" x="{fx+8}" y="{fy+8}" width="{fw-16}" height="{fh-16}" preserveAspectRatio="xMidYMid slice" xlink:href="{img}"/>'
             f'<g transform="skewX(-20)"><rect class="a shim" x="570" y="80" width="40" height="388" fill="url(#shg)"/></g></g>')
    b.append(meander(T, 0, 900, 514))
    b.append(motes(T, [(120, 440), (300, 470), (520, 420), (640, 500), (840, 380), (60, 300)], 2))
    b.append('</g>')
    b.append('<clipPath id="av"><circle cx="76" cy="52" r="14"/></clipPath>'
             f'<image x="62" y="38" width="28" height="28" clip-path="url(#av)" xlink:href="{av}"/>'
             f'<circle cx="76" cy="52" r="14" fill="none" stroke="{T["ecto"]}" stroke-width="1.2"/>'
             f'<text x="100" y="56" font-family="{MONO}" font-size="12.5" fill="{T["mut"]}">{HANDLE} / README</text>'
             f'<path d="M62,78H500" stroke="{T["ecto2"]}" stroke-width=".8" stroke-dasharray="2 5" opacity=".8"/>')
    b.append(f'<text x="62" y="136" font-family="{SERIF}" font-style="italic" font-size="22" fill="{T["mut"]}">Hi, I\'m</text>'
             f'<text x="60" y="204" font-family="{SERIF}" font-weight="700" font-size="66" fill="{T["ink"]}">{NAME_1}</text>'
             f'<text x="60" y="272" font-family="{SERIF}" font-weight="700" font-size="66" fill="{T["ink"]}">{NAME_2}</text>'
             f'<text x="62" y="312" font-family="{MONO}" font-weight="700" font-size="14" letter-spacing="5" fill="{T["ectotx"]}">{ROLE}</text>'
             f'<text x="62" y="338" font-family="{MONO}" font-size="13" fill="{T["ink"]}">{PILLARS}</text>')
    for i, ln in enumerate(TAGLINE):
        b.append(f'<text x="62" y="{378 + i*22}" font-family="{SERIF}" font-size="15" fill="{T["mut"]}">{ln}</text>')
    b.append(ghost(T, 498, 352, 1.15, 0, book=True) + ghost(T, 430, 478, .8, -3, candle=True) + ghost(T, 880, 470, 1.0, -2, flip=True, op=.95))
    return root(900, 540, T, f"{NAME_1} {NAME_2} - {ROLE.title()}", "".join(b))


def button(T, th, text):
    b = (f'<rect x="1" y="1" width="148" height="38" rx="3" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="1.5"/>'
         f'<rect x="5" y="5" width="140" height="30" rx="2" fill="none" stroke="{T["ecto"]}" stroke-width=".6" opacity=".6"/>'
         + bookicon(T, 16, 12.5)
         + f'<text x="38" y="25" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="{T["ink"]}">{text}</text>')
    return root(150, 40, T, text.title(), b)


def about(T, th):
    b = [frame(T, 20, 14, 860, 302), label(T, 56, 58, "01", "ABOUT"), label(T, 536, 58, "02", "MY JOURNEY")]
    for i, ln in enumerate(ABOUT):
        y = 106 + i * 28
        b.append(f'<path d="M56,{y+8}H500" stroke="{T["line"]}" stroke-width=".9"/>'
                 f'<text x="58" y="{y}" font-family="{SERIF}" font-size="15" fill="{T["ink"]}">{ln}</text>')
    for i, (lang, area) in enumerate(JOURNEY):
        y = 108 + i * 38
        b.append(f'<rect x="538" y="{y-10}" width="7" height="11" rx="1" fill="none" stroke="{T["ectotx"]}" stroke-width="1.3"/>'
                 f'<text x="554" y="{y}" font-family="{MONO}" font-size="14" font-weight="700" fill="{T["ink"]}">{lang}</text>'
                 f'<path d="M656,{y-5}H708" stroke="{T["ecto"]}" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="1 7" class="dash" style="animation-delay:-{i}s"/>'
                 f'<text x="720" y="{y}" font-family="{SERIF}" font-size="15" fill="{T["ink"]}">{area}</text>')
    b.append(meander(T, 56, 500, 280, -2, .7))
    b.append(ghost(T, 840, 282, .55, -2, book=True))
    return root(900, 330, T, "About Solayman El Mouden and his journey", "".join(b))


def skills(T, th):
    heights = [104, 92, 110, 98, 86, 108, 96, 110, 88, 100, 106, 94]
    b = [frame(T, 20, 14, 860, 372), label(T, 56, 58, "03", "TECHNOLOGIES &amp; SKILLS"), meander(T, 56, 844, 70, -3, .7)]
    for row in range(2):
        base = 196 + row * 142
        b.append(f'<rect x="40" y="{base}" width="820" height="9" fill="{T["panel2"]}" stroke="{T["ecto2"]}" stroke-width="1"/>')
    for i, (name, mono) in enumerate(SKILLS):
        row, col = divmod(i, 6)
        base = 196 + row * 142
        cx = 121.5 + col * 131
        h, w = heights[i], 64
        col_fill = T["spines"][i % 6]
        sp = (f'<g class="a bob" style="animation-delay:-2s">' if i == 7 else '<g>')
        sp += (f'<rect x="{f(cx-w/2)}" y="{base-h}" width="{w}" height="{h}" rx="2" fill="{col_fill}" stroke="{T["ecto2"]}" stroke-width="1.2"/>'
               f'<path d="M{f(cx-w/2)},{base-h+9}h{w}M{f(cx-w/2)},{base-12}h{w}" stroke="{T["ecto2"]}" stroke-width="2"/>'
               f'<text x="{f(cx)}" y="{base-h+36}" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{T["ink"]}">{mono}</text>'
               f'<path transform="translate({f(cx)},{base-h+52})" d="M0,-5L4,0L0,5L-4,0Z" fill="{T["ecto"]}"/></g>')
        b.append(sp)
        b.append(f'<text x="{f(cx)}" y="{base+26}" text-anchor="middle" font-family="{SERIF}" font-size="12.5" fill="{T["ink"]}">{name}</text>')
    b.append(ghost(T, 846, 150, .6, -1))
    return root(900, 400, T, "Technologies and skills: " + ", ".join(s[0] for s in SKILLS), "".join(b))


def projects_title(T, th):
    b = [meander(T, 40, 270, 32), meander(T, 630, 860, 32, -3),
         f'<rect x="286" y="14" width="328" height="42" rx="3" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="1.6"/>'
         f'<rect x="291" y="19" width="318" height="32" rx="2" fill="none" stroke="{T["ecto"]}" stroke-width=".6" opacity=".6"/>',
         f'<text x="450" y="40" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="3" fill="{T["ectotx"]}">SHELF 04  /  SELECTED PROJECTS</text>',
         f'<circle cx="450" cy="66" r="3" fill="{T["ecto"]}"/>']
    return root(900, 80, T, "Selected projects", "".join(b))


def chips(T, tags):
    out, x, y = [], 8, 176
    for t in tags:
        w = len(t) * 6.4 + 14
        if x + w > 200:
            x, y = 8, y + 22
        out.append(f'<rect x="{f(x)}" y="{y}" width="{f(w)}" height="18" rx="3" fill="{T["panel2"]}" stroke="{T["ecto2"]}" stroke-width=".8"/>'
                   f'<text x="{f(x+w/2)}" y="{y+12.5}" text-anchor="middle" font-family="{MONO}" font-size="10.5" fill="{T["ink"]}">{t}</text>')
        x += w + 5
    return "".join(out)


def card(T, th, i, p):
    title, slug, desc, tags, crop = p
    img = uri(T, crop, size=(400, 190), q=80)
    b = [f'<rect x="1" y="1" width="206" height="236" rx="4" fill="{T["panel"]}" stroke="{T["ecto2"]}" stroke-width="1.4"/>',
         '<clipPath id="tc"><rect x="8" y="8" width="192" height="92"/></clipPath>',
         f'<g clip-path="url(#tc)"><image class="a kb" x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" xlink:href="{img}" style="animation-delay:-{i*3}s"/>'
         f'<g transform="skewX(-20)"><rect class="a shim" x="20" y="8" width="26" height="92" fill="url(#shg)" style="animation-delay:-{i*1.3}s"/></g></g>',
         f'<rect x="8" y="8" width="192" height="92" fill="none" stroke="{T["ecto"]}" stroke-width=".9"/>',
         f'<rect x="8" y="8" width="58" height="19" fill="{T["bg"]}" stroke="{T["ecto"]}" stroke-width=".9"/>'
         f'<text x="37" y="21" text-anchor="middle" font-family="{MONO}" font-size="10.5" font-weight="700" fill="{T["ectotx"]}">No. {i+1:02d}</text>',
         f'<path d="M10,131H198M10,150H198M10,165H198" stroke="{T["line"]}" stroke-width=".8" opacity=".8"/>',
         f'<text x="10" y="126" font-family="{SERIF}" font-weight="700" font-size="16" fill="{T["ink"]}">{title}</text>',
         f'<text x="10" y="145" font-family="{SERIF}" font-size="11.5" fill="{T["mut"]}">{desc[0]}</text>',
         f'<text x="10" y="160" font-family="{SERIF}" font-size="11.5" fill="{T["mut"]}">{desc[1]}</text>',
         chips(T, tags), f'<circle cx="104" cy="229" r="3.5" fill="{T["bg"]}" stroke="{T["ecto2"]}" stroke-width="1"/>']
    return root(208, 238, T, f"No. {i+1:02d}, {title} project card", "".join(b))


def footer(T, th):
    dark = th == "dark"
    b = ['<clipPath id="pc"><rect width="900" height="270"/></clipPath><g clip-path="url(#pc)">']
    if dark:
        b.append(stars(T, 24, 8, 10, 890, 8, 150))
    # arcade of arches
    sky = T["bg"] if dark else T["panel2"]
    for k in range(7):
        cx = 64 + k * 128
        b.append(f'<path d="M{cx-44},270V212A44,44 0 0 1 {cx+44},212V270Z" fill="{sky}" stroke="{T["ecto2"]}" stroke-width="1.4"/>')
        if dark:
            rng = random.Random(30 + k)
            for _ in range(4):
                b.append(f'<circle class="tw" style="animation-delay:-{f(rng.uniform(0,4))}s" cx="{cx+rng.randint(-34,34)}" cy="{rng.randint(222,262)}" r="1.2" fill="{T["ink"]}"/>')
    for k in range(8):
        b.append(column(T, k * 128 - 14, 178, 28, 92))
    b.append(ghost(T, 192, 226, .75, 0) + ghost(T, 448, 232, .65, -3, book=True) + ghost(T, 704, 226, .75, -5, candle=True, flip=True))
    b.append(motes(T, [(250, 170), (620, 160), (820, 180), (80, 190)], 4))
    b.append('</g>')
    b.append(f'<text x="450" y="70" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="30" fill="{T["ink"]}">{FOOT_1}</text>'
             f'<text x="450" y="100" text-anchor="middle" font-family="{MONO}" font-size="12.5" letter-spacing="1" fill="{T["mut"]}">{FOOT_2}</text>'
             + meander(T, 240, 660, 118, -1, .8)
             + f'<text x="450" y="152" text-anchor="middle" font-family="{SERIF}" font-size="13" fill="{T["ectotx"]}">{BRAND}</text>')
    return root(900, 270, T, "Footer: Build, Explore, Understand", "".join(b))


# ----------------------------------------------------------------- README
def pic(name, alt, width="100%", href=None):
    h = (f'<picture>\n    <source media="(prefers-color-scheme: dark)"  srcset="assets/{name}-dark.svg">\n'
         f'    <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'    <img alt="{alt}" src="assets/{name}-light.svg" width="{width}">\n  </picture>')
    return f'<a href="{href}">\n  {h}\n</a>' if href else f'  {h}'


def write_readme():
    cards = [pic(f"card-{p[1]}", f"No. {i+1:02d}, {p[0]}: {' '.join(p[2])} Tags: {', '.join(p[3])}.", "24%",
                 f"https://github.com/solacode-SC/{p[1]}") for i, p in enumerate(PROJECTS)]
    L = ['<div align="center">', "", pic("hero", f"{NAME_1} {NAME_2}, software engineer. AI, Math, Newest Technologies. Friendly ghosts in an impossible starlit library."), "",
         " &nbsp; ".join([pic("btn-github", "GitHub profile", "150", GITHUB), pic("btn-linkedin", "LinkedIn profile", "150", LINKEDIN),
                          pic("btn-portfolio", "Portfolio website", "150", PORTFOLIO)]), "",
         pic("about", "About Solayman El Mouden and his journey: C/C++ systems, Python backend and AI, TypeScript web and tools, Docker infrastructure, Linux DevOps."), "",
         pic("skills", "Technologies and skills shelved as books: " + ", ".join(s[0] for s in SKILLS) + "."), "",
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
