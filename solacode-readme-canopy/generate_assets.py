#!/usr/bin/env python3
"""
Profile README generator: "Canopy Spiral" (borderless, organic, strange and calm).
Run:  python3 generate_assets.py        (needs: pip install pillow)
Edit only the "EDIT CONTENT HERE" block to change text, links, projects.
"""
import base64, html, io, math, os, random, re, textwrap
from PIL import Image

# =============================== EDIT CONTENT HERE ===============================
NAME_1, NAME_2 = "Solayman", "El Mouden"
FULL_NAME = "Solayman El Mouden"
HANDLE = "solacode-SC"
GITHUB = "https://github.com/solacode-SC"
PORTFOLIO = "https://solaymantech.me"
LINKEDIN = "https://www.linkedin.com/in/YOUR-LINKEDIN"   # <-- REPLACE WITH YOUR REAL URL
ROLE = "Software Engineer"
PILLARS = ["AI", "Math", "Newest Technologies"]
TAGLINE = ["Building systems, web applications,",
           "developer tools and intelligent software",
           "for a better tomorrow."]
ABOUT = ("I'm Solayman El Mouden, a software engineer focused on systems, web "
         "technologies, artificial intelligence and mathematics. I enjoy understanding "
         "how things work underneath the abstraction and turning that knowledge into "
         "useful software.")
FACTS = ("Software engineering student at 1337 School (UM6P, 42 Network); earlier CPGE "
         "(Mathematics and Physics track). Based in Morocco.")
FOCUS = "Focus: AI Fullstack, Backend / DevOps"
JOURNEY = [("C / C++", "Systems"), ("Python", "Backend & AI"), ("TypeScript", "Web & Tools"),
           ("Docker", "Infrastructure"), ("Linux", "DevOps")]
SKILLS = [("C/C++", "C++"), ("Python", "Py"), ("JavaScript", "JS"), ("TypeScript", "TS"),
          ("React", "Rx"), ("Next.js", "N"), ("Django", "dj"), ("FastAPI", "FA"),
          ("PostgreSQL", "Pg"), ("Docker", "Dk"), ("Linux", "Lx"), ("Git", "Git")]
# (title, slug, description, tags, square crop box in art/source.jpg)
PROJECTS = [
    ("LazyEquation", "lazyequation", "Interactive math & physics visualization platform.",
     ["React", "TS", "Fastify", "PostgreSQL"], (340, 150, 580, 390)),
    ("LeetResume", "leetresume", "AI-powered resume builder and optimizer.",
     ["Next.js", "Prisma", "Postgres"], (520, 280, 736, 496)),
    ("Libora", "libora", "Flutter PDF reader with modern experience.",
     ["Flutter", "Dart", "Riverpod"], (0, 430, 240, 670)),
    ("Webserv", "webserv", "C++98 HTTP server from scratch.",
     ["C++98", "Networking"], (400, 880, 640, 1120)),
    ("solaJobs v2", "solajobs-v2", "Arabic-first job board platform.",
     ["Arabic-first", "Jobs"], (60, 950, 300, 1190)),
    ("Alert Generator", "prometheus-alert-generator", "AI generator for Prometheus alert rules.",
     ["AI", "Prometheus"], (420, 560, 660, 800)),
    ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose dashboard.",
     ["Docker", "Compose"], (230, 1068, 470, 1308)),
]
FOOTER_1 = "Build  ·  Explore  ·  Understand"
FOOTER_2 = "Software Engineering · Systems · AI · Mathematics"
ART_CREDIT = "Artwork: source unknown (update this line when you know the artist)"
SIGNATURE = "NashirTech \u00b7 \u0646\u0627\u0634\u0631 \u062a\u0643"
SOURCE = "art/source.jpg"
HERO_CROP = (0, 120, 736, 1174)
# ================================================================================

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {
    "dark": dict(bg="#0C1810", bg2="#18351F", panel="#183323", ink="#EAF1D2", soft="#B9CBA6",
                 accent="#C9E66B", line="#8DB33A", twig="#6F9A78", twigop=".55", disc="#EAF1D2",
                 disctxt="#12261A", btn="#B7D957", btntxt="#10200F", band="#08110B",
                 dots=["#8DB33A", "#A9D04B", "#5E9B6B", "#C9E66B", "#6FA89A"], blob_op=".55"),
    "light": dict(bg="#F4F6E0", bg2="#DCE8BE", panel="#FBFCEB", ink="#1B2D19", soft="#47603F",
                  accent="#3C6A1B", line="#6E9A2C", twig="#3B2D20", twigop=".45", disc="#FBFCEB",
                  disctxt="#1B2D19", btn="#3C6A1B", btntxt="#F6F8E6", band="#1B2D19",
                  dots=["#6E9A2C", "#8DB33A", "#4E8A5E", "#A9C84A", "#5E9AA0"], blob_op=".7"),
}

CSS = """
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.kb{transform-box:fill-box;transform-origin:50% 40%;animation-name:kb;animation-duration:40s}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:160s;animation-timing-function:linear;animation-direction:normal}
.sway{transform-box:fill-box;transform-origin:center;animation-name:sway;animation-duration:18s}
.bob{animation-name:bob;animation-duration:9s}
.flow{animation-name:flow;animation-duration:9s;animation-timing-function:linear;animation-direction:normal}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.05)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes sway{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-8px)}}
@keyframes flow{to{stroke-dashoffset:-64}}
@media (prefers-reduced-motion: reduce){.a{animation:none}}
"""

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
esc = lambda s: html.escape(s, quote=False)


def b64_crop(box, size, q=80):
    im = Image.open(os.path.join(ROOT, SOURCE)).convert("RGB").crop(box).resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def svg(W, H, body, title, desc, defs="", animated=True):
    style = f"<style>{CSS}</style>" if animated else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><desc>{esc(desc)}</desc><defs>{defs}</defs>{style}{body}</svg>')


def save(name, theme, content):
    content = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", content)
    with open(os.path.join(ASSETS, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(content)


def wave(x0, x1, y, amp, wl, ph=0.0, step=6):
    pts, x = [], x0
    while x <= x1:
        pts.append(f"{x:.1f},{y + amp * math.sin((x - x0) / wl * 2 * math.pi + ph):.1f}")
        x += step
    return "M" + " L".join(pts)


def blob_path(cx, cy, rx, ry, seed, n=9, jit=.1):
    """Smooth closed organic shape (Catmull-Rom converted to cubic beziers)."""
    r = random.Random(seed)
    pts = []
    for i in range(n):
        a = i * 2 * math.pi / n
        k = 1 + r.uniform(-jit, jit)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + " Z"


def spiral_d(R, turns, step=.25):
    pts, th, tmax = [], 0.0, turns * 2 * math.pi
    while th <= tmax:
        r = R * th / tmax
        pts.append(f"{r * math.cos(th):.1f},{r * math.sin(th):.1f}")
        th += step
    return "M" + " L".join(pts)


def spiral(cx, cy, R, turns, color, w=2, op=1.0, rot=0, spin=False, delay=0):
    guard = f'<circle r="{R}" fill="none" stroke="none"/>'
    path = (f'<path d="{spiral_d(R, turns)}" fill="none" stroke="{color}" stroke-width="{w}" '
            f'stroke-linecap="round" opacity="{op}"/>')
    inner = guard + path
    if spin:
        inner = f'<g class="spin a" style="animation-delay:-{delay}s">{inner}</g>'
    return f'<g transform="translate({cx},{cy}) rotate({rot})">{inner}</g>'


def phyllotaxis(cx, cy, n, spread, T, spin_delay=None):
    out = [f'<circle r="{spread * math.sqrt(n) + 4:.0f}" fill="none" stroke="none"/>']
    for i in range(1, n + 1):
        th = i * 2.399963
        rr = spread * math.sqrt(i)
        out.append(f'<circle cx="{rr * math.cos(th):.1f}" cy="{rr * math.sin(th):.1f}" r="{1.2 + 2.0 * i / n:.1f}" fill="{T["dots"][i % 5]}"/>')
    g = "".join(out)
    if spin_delay is not None:
        g = f'<g class="spin a" style="animation-delay:-{spin_delay}s;animation-duration:90s">{g}</g>'
    return f'<g transform="translate({cx:.1f},{cy:.1f})">{g}</g>'


def twig(T, x, y, ang, L, seed, depth=5, w=3.2):
    r = random.Random(seed)
    segs = []

    def grow(x, y, a, L, d, w):
        a2 = a + r.uniform(-.35, .35)
        x2, y2 = x + L * math.cos(a2), y + L * math.sin(a2)
        mx, my = (x + x2) / 2 + r.uniform(-L, L) * .15, (y + y2) / 2 + r.uniform(-L, L) * .15
        segs.append(f'<path d="M{x:.0f},{y:.0f} Q{mx:.0f},{my:.0f} {x2:.0f},{y2:.0f}" stroke-width="{max(w, .8):.1f}"/>')
        if d > 0:
            grow(x2, y2, a2 + r.uniform(.25, .6), L * .76, d - 1, w * .66)
            if r.random() < .8:
                grow(x2, y2, a2 - r.uniform(.3, .7), L * .7, d - 1, w * .6)

    grow(x, y, ang, L, depth, w)
    return (f'<g fill="none" stroke="{T["twig"]}" stroke-linecap="round" opacity="{T["twigop"]}">{"".join(segs)}</g>')


def base(T, W, H, sid="s"):
    defs = (f'<linearGradient id="{sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/>'
            f'<stop offset="1" stop-color="{T["bg2"]}"/></linearGradient>')
    return defs, f'<rect width="{W}" height="{H}" fill="url(#{sid}g)"/>'


def heading(x, y, text, T, size=28):
    return (spiral(x + 12, y - 9, 11, 2.2, T["accent"], 2.2) +
            f'<text x="{x + 34}" y="{y}" font-family="{SERIF}" font-size="{size}" font-style="italic" letter-spacing=".8" fill="{T["ink"]}">{esc(text)}</text>')


def scatter_spirals(T, W, H, seed, n, rmin, rmax, op=(.15, .35), avoid=None, spin_n=3):
    r = random.Random(seed)
    out = []
    for i in range(n):
        for _ in range(20):
            x, y, R = r.uniform(0, W), r.uniform(0, H), r.uniform(rmin, rmax)
            if not avoid or not (avoid[0] < x < avoid[2] and avoid[1] < y < avoid[3]):
                break
        out.append(spiral(round(x), round(y), round(R), r.choice((2.5, 3, 3.5)), T["line"], r.choice((1.4, 2, 2.6)),
                          round(r.uniform(*op), 2), r.randint(0, 359), spin=(i < spin_n), delay=r.randint(0, 80)))
    return "".join(out)


# ----------------------------------- panels -----------------------------------
def hero(T, imgs):
    W, H = 900, 580
    defs, bg = base(T, W, H, "h")
    bx, by, brx, bry = 670, 292, 182, 262
    blob = blob_path(bx, by, brx, bry, 12, 9, .07)
    defs += f'<clipPath id="hclip"><path d="{blob}"/></clipPath><clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>'
    defs += '<clipPath id="hf1"><circle cx="455" cy="500" r="32"/></clipPath><clipPath id="hf2"><circle cx="868" cy="62" r="26"/></clipPath>'
    s = [bg, scatter_spirals(T, 500, H, 3, 7, 40, 120, (.1, .22), avoid=(40, 90, 480, 470), spin_n=2)]
    s.append(twig(T, 0, 590, -1.2, 78, 5, 5, 4.2))
    s.append(twig(T, 520, -10, 1.5, 60, 8, 4, 3))
    # top bar
    s.append(f'<image href="{imgs[0]}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>')
    s.append(f'<circle cx="64" cy="34" r="14" fill="none" stroke="{T["accent"]}" stroke-width="1.6"/>')
    s.append(f'<text x="86" y="39" font-family="{MONO}" font-size="12.5" fill="{T["soft"]}">{esc(HANDLE)} / README</text>')
    s.append(f'<path d="{wave(50, 400, 64, 3, 70)}" fill="none" stroke="{T["line"]}" stroke-width="1.4" opacity=".8"/>')
    # text, drifting a little off-grid on purpose
    s.append(f'<text x="52" y="132" font-family="{SERIF}" font-size="20" font-style="italic" fill="{T["soft"]}">hi, i\'m</text>')
    s.append(spiral(122, 126, 9, 2, T["accent"], 2))
    s.append(f'<text x="50" y="202" font-family="{SERIF}" font-size="60" font-style="italic" fill="{T["ink"]}">{esc(NAME_1)}</text>')
    s.append(f'<text x="96" y="268" font-family="{SERIF}" font-size="60" font-style="italic" fill="{T["ink"]}">{esc(NAME_2)}</text>')
    s.append(f'<text x="98" y="322" font-family="{SANS}" font-size="14" font-weight="700" letter-spacing="4" fill="{T["accent"]}">{esc(ROLE)}</text>')
    sep = "\u00a0\u00a0|\u00a0\u00a0"
    s.append(f'<text x="98" y="354" font-family="{SERIF}" font-size="17.5" font-style="italic" fill="{T["ink"]}">{esc(sep.join(PILLARS))}</text>')
    for i, line in enumerate(TAGLINE):
        s.append(f'<text x="{60 + i * 10}" y="{408 + i * 23}" font-family="{SERIF}" font-size="15.5" fill="{T["soft"]}">{esc(line)}</text>')
    # organic art window with echoing outlines
    s.append(f'<path class="sway a" d="{blob_path(bx, by, brx + 14, bry + 14, 12, 9, .07)}" fill="none" stroke="{T["accent"]}" stroke-width="1.2" opacity=".7"/>')
    s.append(f'<path class="sway a" style="animation-direction:alternate-reverse;animation-duration:24s" d="{blob_path(bx, by, brx + 28, bry + 26, 12, 9, .07)}" fill="none" stroke="{T["line"]}" stroke-width=".9" opacity=".5"/>')
    s.append(f'<g clip-path="url(#hclip)"><image class="kb a" href="{imgs["hero"]}" x="{bx - 185}" y="{by - 267}" width="370" height="534" preserveAspectRatio="xMidYMid slice"/></g>')
    # floating pebbles of the same canopy
    s.append(f'<g class="bob a"><g clip-path="url(#hf1)"><image href="{imgs[2]}" x="423" y="468" width="64" height="64"/></g>'
             f'<circle cx="455" cy="500" r="32" fill="none" stroke="{T["accent"]}" stroke-width="1.4"/></g>')
    s.append(f'<g class="bob a" style="animation-delay:-4s"><g clip-path="url(#hf2)"><image href="{imgs[4]}" x="842" y="36" width="52" height="52"/></g>'
             f'<circle cx="868" cy="62" r="26" fill="none" stroke="{T["accent"]}" stroke-width="1.4"/></g>')
    return svg(W, H, "".join(s), f"{FULL_NAME}: {ROLE}",
               "Profile header with name, role and an organic window showing a tree canopy whose leaves swirl into spirals.", defs)


def button(T, label):
    body = (f'<path d="M5,20 C30,2 120,2 145,20 C120,38 30,38 5,20 Z" fill="{T["btn"]}"/>'
            + spiral(32, 20, 7, 2, T["btntxt"], 1.8) +
            f'<text x="88" y="25" text-anchor="middle" font-family="{SERIF}" font-size="15" font-style="italic" letter-spacing=".6" fill="{T["btntxt"]}">{esc(label)}</text>')
    return svg(150, 40, body, label, f"Button linking to {label}", animated=False)


def about(T):
    W, H = 900, 392
    defs, bg = base(T, W, H, "a")
    s = [bg, f'<path d="{blob_path(450, 196, 430, 172, 4, 10, .06)}" fill="{T["panel"]}" opacity="{T["blob_op"]}"/>']
    s.append(spiral(770, 210, 150, 3.5, T["line"], 2, .22, 0, spin=True))
    s.append(twig(T, 900, 400, -2.6, 70, 11, 4, 3))
    s.append(heading(60, 78, "about", T))
    s.append(heading(520, 78, "my journey", T))
    lines = textwrap.wrap(ABOUT, 50)
    g = []
    for i, line in enumerate(lines):
        g.append(f'<text x="60" y="{122 + i * 24}" font-family="{SERIF}" font-size="14.5" fill="{T["ink"]}">{esc(line)}</text>')
    y = 122 + 24 * len(lines) + 24
    for line in textwrap.wrap(FACTS, 58):
        g.append(f'<text x="60" y="{y}" font-family="{SANS}" font-size="12" fill="{T["soft"]}">{esc(line)}</text>')
        y += 18
    g.append(f'<text x="60" y="{y + 8}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{T["accent"]}">{esc(FOCUS)}</text>')
    s.append(f'<g transform="rotate(-.8 60 122)">{"".join(g)}</g>')
    for i, (lang, area) in enumerate(JOURNEY):
        yy = 134 + i * 44
        lx = 520 + round(9 * math.sin(i * 1.4))
        x1 = lx + len(lang) * 10.4 + 14
        x2 = 850 - len(area) * 7.6 - 30
        s.append(f'<text x="{lx}" y="{yy}" font-family="{SERIF}" font-size="18" font-style="italic" fill="{T["ink"]}">{esc(lang)}</text>')
        s.append(f'<path class="flow a" d="{wave(round(x1), round(x2), yy - 5, 3, 50, i)}" fill="none" stroke="{T["line"]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="0 8"/>')
        s.append(f'<text x="850" y="{yy}" text-anchor="end" font-family="{SANS}" font-size="13.5" font-weight="700" fill="{T["accent"]}">{esc(area)}</text>')
    return svg(W, H, "".join(s), "About and journey",
               "About text on the left; on the right the journey: " + ", ".join(f"{a} to {b}" for a, b in JOURNEY) + ".", defs)


def skills(T):
    W, H = 900, 360
    defs, bg = base(T, W, H, "k")
    s = [bg, f'<path d="{blob_path(450, 190, 430, 160, 9, 10, .06)}" fill="{T["panel"]}" opacity="{T["blob_op"]}"/>',
         scatter_spirals(T, W, H, 6, 5, 50, 110, (.08, .16), spin_n=1), heading(60, 78, "technologies & skills", T)]
    cell = 800 / 6
    for i, (lab, mono) in enumerate(SKILLS):
        row, col = divmod(i, 6)
        cx = 50 + cell * (col + .5) + row * 22
        cy = 160 + row * 116 + round(9 * math.sin(col * 1.7 + row))
        s.append(phyllotaxis(cx, cy, 60, 4.6, T, spin_delay=i * 11))
        s.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="17" fill="{T["disc"]}"/>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 4.5}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{T["disctxt"]}">{esc(mono)}</text>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 58}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{T["ink"]}">{esc(lab)}</text>')
    return svg(W, H, "".join(s), "Technologies and skills",
               "Twelve seed-like spirals: " + ", ".join(l for l, _ in SKILLS) + ".", defs)


def projects_title(T):
    W, H = 900, 92
    defs, bg = base(T, W, H, "p")
    s = [bg, heading(60, 56, "selected projects", T, 30),
         f'<path d="{wave(360, 800, 48, 7, 120)}" fill="none" stroke="{T["line"]}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0 8" class="flow a"/>',
         spiral(830, 48, 16, 2.6, T["accent"], 2.2)]
    return svg(W, H, "".join(s), "Selected projects", "Section heading.", defs)


def tag_lines(tags):
    lines, cur = [], ""
    for t in tags:
        nxt = t if not cur else cur + " \u00b7 " + t
        if len(nxt) > 30 and cur:
            lines.append(cur)
            cur = t
        else:
            cur = nxt
    lines.append(cur)
    return lines


def card(T, idx, title, desc, tags, img):
    W, H = 208, 262
    dy = 14 if idx % 2 == 0 else 0
    cx, cy, r = 104, 74, 56
    defs = f'<clipPath id="c{idx}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    g = [spiral(cx, cy, 86, 3, T["line"], 1.6, .35, idx * 40),
         f'<g clip-path="url(#c{idx})"><image href="{img}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}"/></g>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{T["accent"]}" stroke-width="2"/>',
         f'<circle cx="{cx + 6}" cy="{cy - 4}" r="{r + 8}" fill="none" stroke="{T["line"]}" stroke-width="1" opacity=".7"/>',
         f'<text x="{cx + 52}" y="{cy - 46}" font-family="{SERIF}" font-size="15" font-style="italic" fill="{T["accent"]}">{idx:02d}</text>',
         f'<text x="{cx}" y="156" text-anchor="middle" font-family="{SERIF}" font-size="{min(17, 190 / (len(title) * .62)):.1f}" font-style="italic" fill="{T["ink"]}">{esc(title)}</text>']
    for i, line in enumerate(textwrap.wrap(desc, 34)[:2]):
        g.append(f'<text x="{cx}" y="{176 + i * 14}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{T["soft"]}">{esc(line)}</text>')
    for i, line in enumerate(tag_lines(tags)):
        g.append(f'<text x="{cx}" y="{214 + i * 15}" text-anchor="middle" font-family="{SANS}" font-size="10.5" font-weight="700" fill="{T["accent"]}">{esc(line)}</text>')
    return svg(W, H, f'<g transform="translate(0,{dy})">{"".join(g)}</g>', f"Project {title}",
               f"{title}: {desc} Tags: {', '.join(tags)}.", defs, animated=False)


def footer(T):
    W, H = 900, 310
    defs, bg = base(T, W, H, "f")
    s = [bg, scatter_spirals(T, W, H - 40, 17, 26, 16, 52, (.25, .55), spin_n=4)]
    s.append(twig(T, 0, H - 34, -1.0, 90, 3, 5, 4.6))
    s.append(twig(T, W, H - 34, -2.1, 86, 6, 5, 4.4))
    s.append(f'<path d="{blob_path(450, 92, 330, 62, 2, 9, .05)}" fill="{T["bg"]}" opacity=".88"/>')
    s.append(f'<text x="450" y="94" text-anchor="middle" font-family="{SERIF}" font-size="31" font-style="italic" letter-spacing="1" fill="{T["ink"]}">{esc(FOOTER_1)}</text>')
    s.append(f'<text x="450" y="124" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="1" fill="{T["soft"]}">{esc(FOOTER_2)}</text>')
    s.append(f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="{T["band"]}"/>')
    s.append(f'<text x="50" y="{H - 13}" font-family="{SANS}" font-size="11" fill="#EAF1D2">{esc(ART_CREDIT)}</text>')
    s.append(f'<text x="850" y="{H - 13}" text-anchor="end" font-family="{SANS}" font-size="11.5" font-weight="700" fill="#C9E66B">{esc(SIGNATURE)}</text>')
    return svg(W, H, "".join(s), "Footer", f"{FOOTER_1}. {FOOTER_2}.", defs)


# ----------------------------------- README -----------------------------------
def pic(name, alt, href=None, width="100%"):
    p = (f'<picture>\n<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'<img alt="{html.escape(alt)}" src="assets/{name}-light.svg" width="{width}">\n</picture>')
    return f'<a href="{href}">\n{p}\n</a>' if href else p


def main():
    os.makedirs(ASSETS, exist_ok=True)
    thumbs = [b64_crop(p[4], (200, 200)) for p in PROJECTS]
    imgs = {"hero": b64_crop(HERO_CROP, (556, 794), 80), 0: thumbs[0], 2: thumbs[2], 4: thumbs[4]}
    for th, T in THEMES.items():
        save("hero", th, hero(T, imgs))
        save("btn-github", th, button(T, "GitHub"))
        save("btn-linkedin", th, button(T, "LinkedIn"))
        save("btn-portfolio", th, button(T, "Portfolio"))
        save("about", th, about(T))
        save("skills", th, skills(T))
        save("projects-title", th, projects_title(T))
        save("footer", th, footer(T))
        for i, (title, slug, desc, tags, _) in enumerate(PROJECTS):
            save(f"card-{slug}", th, card(T, i + 1, title, desc, tags, thumbs[i]))
    cards = [pic(f"card-{p[1]}", f"{p[0]}: {p[2]}", f"{GITHUB}/{p[1]}", "24%") for p in PROJECTS]
    md = ['<div align="center">', "",
          pic("hero", f"{FULL_NAME}, {ROLE}. A tree canopy whose leaves swirl into spirals."), "",
          pic("btn-github", "GitHub profile", GITHUB, "150") + "&nbsp;" +
          pic("btn-linkedin", "LinkedIn profile", LINKEDIN, "150") + "&nbsp;" +
          pic("btn-portfolio", "Portfolio website", PORTFOLIO, "150"), "",
          pic("about", "About me and my journey from languages to areas"), "",
          pic("skills", "Technologies and skills"), "",
          pic("projects-title", "Selected projects"), "",
          "\n".join(cards[:4]), "", "\n".join(cards[4:]), "",
          pic("footer", FOOTER_1 + ". " + FOOTER_2), "", "</div>", ""]
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print("done")


if __name__ == "__main__":
    main()
