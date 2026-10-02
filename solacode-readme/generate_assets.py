#!/usr/bin/env python3
"""
Profile README generator: "Sunset Citadel" (ligne claire, pink clouds, red dragon).
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
ROLE = "SOFTWARE ENGINEER"
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
# (title, slug, description, tags, crop box in art/source.jpg)
PROJECTS = [
    ("LazyEquation", "lazyequation", "Interactive math & physics visualization platform.",
     ["React", "TS", "Fastify", "PostgreSQL"], (100, 370, 400, 513)),
    ("LeetResume", "leetresume", "AI-powered resume builder and optimizer.",
     ["Next.js", "Prisma", "Postgres"], (170, 20, 470, 163)),
    ("Libora", "libora", "Flutter PDF reader with modern experience.",
     ["Flutter", "Dart", "Riverpod"], (170, 430, 410, 544)),
    ("Webserv", "webserv", "C++98 HTTP server from scratch.",
     ["C++98", "Networking"], (0, 560, 300, 703)),
    ("solaJobs v2", "solajobs-v2", "Arabic-first job board platform.",
     ["Arabic-first", "Jobs"], (0, 260, 300, 403)),
    ("Alert Generator", "prometheus-alert-generator", "AI generator for Prometheus alert rules.",
     ["AI", "Prometheus"], (330, 400, 598, 527)),
    ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose dashboard.",
     ["Docker", "Compose"], (300, 540, 598, 682)),
]
FOOTER_1 = "Build  ·  Explore  ·  Understand"
FOOTER_2 = "Software Engineering · Systems · AI · Mathematics"
ART_CREDIT = "Artwork: \u201cKlauth, Unrivaled Ancient\u201d by Diego Andrade"
SIGNATURE = "NashirTech \u00b7 \u0646\u0627\u0634\u0631 \u062a\u0643"
SOURCE = "art/source.jpg"
HERO_CROP = (0, 0, 598, 700)        # dragon + spire, signature excluded
AVATAR_CROP = (150, 370, 290, 510)
# ================================================================================

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {
    "dark": dict(bg="#1E1028", sky2="#4A1F45", panel="#2B1738", panel2="#3B2150", ink="#FCE9C9",
                 soft="#DCC3D2", accent="#F7C95A", sun="#F7C95A", coral="#F0735F", pink="#F4A3BC",
                 crimson="#CF2F3C", lav="#AFA6EC", olive="#9DB05A", shadow="#0E0614",
                 fshadow="#F0735F", rim="#F7C95A", line="#FCE9C9", wave="#F7C95A", dot="#FCE9C9",
                 city="#3A2147", roofA="#8A9A4B", roofB="#E4414B", band="#12091A", star="#FFF3C4", cloudfill="#F4A3BC"),
    "light": dict(bg="#FFF1D0", sky2="#FFD3A0", panel="#FFF9E8", panel2="#FBE3B5", ink="#34142A",
                  soft="#6A3A55", accent="#B8232F", sun="#F2B13C", coral="#E2603F", pink="#EE8EAA",
                  crimson="#C32835", lav="#8E85D6", olive="#6B7A2C", shadow="#F2A0B8",
                  fshadow="#F2A0B8", rim="#34142A", line="#34142A", wave="#C32835", dot="#34142A",
                  city="#F5D9A0", roofA="#6B7A2C", roofB="#C32835", band="#34142A", star="#C32835", cloudfill="#F4A3BC"),
}
BADGE_INK = "#2A1230"
BADGE_FILLS = ["#F4A3BC", "#F7C95A", "#AFA6EC", "#B7C77A"]

CSS = """
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.drift{animation-name:drift;animation-duration:24s}
.bob{transform-box:fill-box;transform-origin:center;animation-name:bob;animation-duration:6s}
.kb{transform-box:fill-box;transform-origin:50% 38%;animation-name:kb;animation-duration:26s}
.glint{transform-box:fill-box;transform-origin:center;animation-name:glint;animation-duration:3.6s}
.pulse{transform-box:fill-box;transform-origin:center;animation-name:pulse;animation-duration:6s}
.flow{animation-name:flow;animation-duration:3s;animation-timing-function:linear;animation-direction:normal}
@keyframes drift{from{transform:translateX(-14px)}to{transform:translateX(26px)}}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-4px)}}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
@keyframes glint{0%{opacity:.25;transform:scale(.5)}60%{opacity:1;transform:scale(1.1)}100%{opacity:.35;transform:scale(.6)}}
@keyframes pulse{from{opacity:.8;transform:scale(1)}to{opacity:1;transform:scale(1.05)}}
@keyframes flow{to{stroke-dashoffset:-48}}
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


def wave(x0, x1, y, amp, wl, ph=0.0, step=8):
    pts, x = [], x0
    while x <= x1:
        pts.append(f"{x:.1f},{y + amp * math.sin((x - x0) / wl * 2 * math.pi + ph):.1f}")
        x += step
    return "M" + " L".join(pts)


def vwave(x, y0, y1, amp, wl, step=8):
    pts, y = [], y0
    while y <= y1:
        pts.append(f"{x + amp * math.sin((y - y0) / wl * 2 * math.pi):.1f},{y:.1f}")
        y += step
    return "M" + " L".join(pts)


def cloud(cx, cy, w, fill, rim, rimw=4, seed=0, cls="", style=""):
    """Scalloped cloud: rim circles first, fill circles on top (union look)."""
    r = random.Random(seed)
    n = max(4, int(w / 32))
    cs = []
    for i in range(n):
        t = (i + .5) / n
        rad = w * (0.10 + 0.07 * math.sin(math.pi * t)) * (0.85 + 0.3 * r.random())
        cs.append((cx - w / 2 + t * w, cy - math.sin(math.pi * t) * w * 0.05 - rad * .3, rad))
    if w > 100:
        for i in range(max(2, n // 2)):
            t = (i + .8) / (n // 2 + .6)
            rad = w * 0.11 * (0.85 + 0.3 * r.random())
            cs.append((cx - w / 2 + t * w * .9 + w * .05, cy - w * 0.13, rad))
    rims = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad + rimw:.1f}"/>' for x, y, rad in cs)
    fills = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}"/>' for x, y, rad in cs)
    inner = f'<g fill="{rim}">{rims}</g><g fill="{fill}">{fills}</g>'
    if cls:
        return f'<g><g class="{cls}" style="{style}">{inner}</g></g>'
    return f'<g>{inner}</g>'


def star(x, y, s=1.0, fill="#FFF3C4", cls="glint a", style=""):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})"><path class="{cls}" style="{style}" fill="{fill}" '
            f'd="M0,-12 L2.4,-2.4 L12,0 L2.4,2.4 L0,12 L-2.4,2.4 L-12,0 L-2.4,-2.4Z"/></g>')


def sun_glyph(cx, cy, r, T):
    rays = "".join(
        f'<line x1="{cx + (r + 3) * math.cos(a):.1f}" y1="{cy + (r + 3) * math.sin(a):.1f}" '
        f'x2="{cx + (r + 7) * math.cos(a):.1f}" y2="{cy + (r + 7) * math.sin(a):.1f}"/>'
        for a in [i * math.pi / 4 for i in range(8)])
    return (f'<g stroke="{T["ink"]}" stroke-width="1.6" stroke-linecap="round">{rays}</g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{T["sun"]}" stroke="{T["ink"]}" stroke-width="1.8"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .5:.1f}" fill="none" stroke="{T["ink"]}" stroke-width="1"/>')


def heading(x, y, text, T, size=24):
    return (sun_glyph(x + 10, y - 8, 7, T) +
            f'<text x="{x + 32}" y="{y}" font-family="{SERIF}" font-size="{size}" font-weight="700" '
            f'font-style="italic" fill="{T["ink"]}">{esc(text)}</text>')


def base(T, W, H, sky=True, sid="s"):
    defs = (f'<linearGradient id="{sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/>'
            f'<stop offset="1" stop-color="{T["sky2"]}"/></linearGradient>'
            f'<pattern id="{sid}d" width="9" height="9" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1" fill="{T["dot"]}"/></pattern>')
    body = (f'<rect width="{W}" height="{H}" fill="url(#{sid}g)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#{sid}d)" opacity=".07"/>')
    return defs, body


def contours(T, W, H, n, y0, gap, op=.3):
    out = []
    for i in range(n):
        out.append(f'<path d="{wave(0, W, y0 + i * gap, 5 + (i % 3) * 3, 140 + (i * 13) % 70, i * 0.9)}" '
                   f'fill="none" stroke="{T["wave"]}" stroke-width="1.1" opacity="{op}"/>')
    return "".join(out)


def panel(T, x, y, w, h, rx=22):
    return (f'<rect x="{x + 7}" y="{y + 7}" width="{w}" height="{h}" rx="{rx}" fill="{T["shadow"]}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{T["panel"]}" '
            f'stroke="{T["ink"]}" stroke-width="2.4"/>')


# ----------------------------------- panels -----------------------------------
def hero(T, th, imgs):
    W, H = 900, 520
    defs, body = base(T, W, H, sid="h")
    fx, fy, fw = 510, 40, 370
    fh = round(fw * 700 / 598)
    defs += f'<clipPath id="hclip"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="5"/></clipPath>'
    defs += f'<clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>'
    defs += (f'<radialGradient id="hglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{T["sun"]}" stop-opacity=".35"/>'
             f'<stop offset="1" stop-color="{T["sun"]}" stop-opacity="0"/></radialGradient>')
    s = [body, contours(T, W, H, 15, 30, 31, .22)]
    s.append(f'<ellipse cx="{fx + fw / 2}" cy="{fy + fh / 2}" rx="300" ry="290" fill="url(#hglow)"/>')
    # top bar
    s.append(f'<image href="{imgs["avatar"]}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>')
    s.append(f'<circle cx="64" cy="34" r="14" fill="none" stroke="{T["sun"]}" stroke-width="2"/>')
    s.append(f'<text x="86" y="39" font-family="{MONO}" font-size="12.5" fill="{T["soft"]}">{esc(HANDLE)} / README</text>')
    s.append(f'<path d="{wave(50, 470, 64, 2.5, 60)}" fill="none" stroke="{T["accent"]}" stroke-width="1.6" opacity=".8"/>')
    # text
    s.append(f'<text x="52" y="116" font-family="{SERIF}" font-size="20" font-style="italic" fill="{T["soft"]}">Hi, I\'m</text>')
    for txt, y in ((NAME_1, 186), (NAME_2, 252)):
        s.append(f'<text x="55" y="{y + 3}" font-family="{SERIF}" font-size="64" font-weight="700" font-style="italic" fill="{T["fshadow"]}">{esc(txt)}</text>')
        s.append(f'<text x="52" y="{y}" font-family="{SERIF}" font-size="64" font-weight="700" font-style="italic" fill="{T["ink"]}">{esc(txt)}</text>')
    s.append(f'<text x="53" y="310" font-family="{SANS}" font-size="14" font-weight="700" letter-spacing="5" fill="{T["accent"]}">{esc(ROLE)}</text>')
    sep = "\u00a0\u00a0|\u00a0\u00a0"
    s.append(f'<text x="53" y="341" font-family="{SERIF}" font-size="17" font-style="italic" fill="{T["ink"]}">{esc(sep.join(PILLARS))}</text>')
    for i, line in enumerate(TAGLINE):
        s.append(f'<text x="53" y="{384 + i * 22}" font-family="{SERIF}" font-size="15.5" fill="{T["soft"]}">{esc(line)}</text>')
    # framed art
    s.append(f'<rect x="{fx + 10}" y="{fy + 10}" width="{fw}" height="{fh}" rx="5" fill="{T["fshadow"]}"/>')
    s.append(f'<g clip-path="url(#hclip)"><image class="kb a" href="{imgs["hero"]}" x="{fx}" y="{fy}" width="{fw}" height="{fh}" preserveAspectRatio="xMidYMid slice"/></g>')
    s.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="5" fill="none" stroke="{T["ink"]}" stroke-width="3"/>')
    s.append(star(fx + 283 * fw / 598, fy + 457 * fw / 598, 1.1))
    # cloud horizon, partly over the frame
    cf = T["cloudfill"]
    s.append(cloud(230, 570, 420, cf, T["rim"], seed=3, cls="drift a", style="animation-duration:30s;animation-delay:-9s"))
    s.append(cloud(640, 562, 300, T["sun"], T["rim"], seed=5, cls="drift a", style="animation-duration:23s;animation-delay:-4s"))
    s.append(cloud(830, 556, 280, cf, T["rim"], seed=8, cls="drift a", style="animation-duration:27s;animation-delay:-15s"))
    return svg(W, H, "".join(s), f"{FULL_NAME}: {ROLE.title()}",
               "Profile header: name, role and a framed illustration of a red dragon above a sunset citadel.", defs)


def button(T, label):
    body = (f'<rect x="6" y="6" width="141" height="31" rx="15.5" fill="{T["sun"]}"/>'
            f'<rect x="3" y="3" width="141" height="31" rx="15.5" fill="{T["crimson"]}" stroke="{T["ink"]}" stroke-width="2"/>'
            f'<circle cx="30" cy="18.5" r="5.5" fill="{T["sun"]}" stroke="#2A1230" stroke-width="1.4"/>'
            f'<text x="86" y="24" text-anchor="middle" font-family="{SERIF}" font-size="15" font-weight="700" font-style="italic" fill="#FFF3DC">{esc(label)}</text>')
    return svg(150, 40, body, label, f"Button linking to {label}", animated=False)


def about(T):
    W, H = 900, 332
    defs, bg = base(T, W, H, sid="a")
    s = [bg, panel(T, 14, 14, 868, 302)]
    s.append(heading(50, 66, "About", T))
    s.append(heading(526, 66, "My journey", T))
    for i, line in enumerate(textwrap.wrap(ABOUT, 52)):
        s.append(f'<text x="52" y="{104 + i * 24}" font-family="{SERIF}" font-size="14.5" fill="{T["ink"]}">{esc(line)}</text>')
    y = 104 + 24 * len(textwrap.wrap(ABOUT, 52)) + 22
    for line in textwrap.wrap(FACTS, 58):
        s.append(f'<text x="52" y="{y}" font-family="{SANS}" font-size="12" fill="{T["soft"]}">{esc(line)}</text>')
        y += 18
    s.append(f'<text x="52" y="{y + 8}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{T["accent"]}">{esc(FOCUS)}</text>')
    s.append(f'<path d="{vwave(496, 44, 290, 3, 60)}" fill="none" stroke="{T["coral"]}" stroke-width="1.8" opacity=".8"/>')
    for i, (lang, area) in enumerate(JOURNEY):
        yy = 118 + i * 44
        x1 = 530 + len(lang) * 10.8 + 12
        x2 = 850 - len(area) * 7.6 - 18
        s.append(f'<text x="530" y="{yy}" font-family="{SERIF}" font-size="18" font-weight="700" fill="{T["ink"]}">{esc(lang)}</text>')
        s.append(f'<line class="flow a" x1="{x1:.0f}" y1="{yy - 5}" x2="{x2:.0f}" y2="{yy - 5}" stroke="{T["coral"]}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 10"/>')
        s.append(f'<text x="850" y="{yy}" text-anchor="end" font-family="{SANS}" font-size="13.5" font-weight="700" fill="{T["accent"]}">{esc(area)}</text>')
    return svg(W, H, "".join(s), "About and journey",
               "About text on the left; on the right the journey from languages to areas: " +
               ", ".join(f"{a} to {b}" for a, b in JOURNEY) + ".", defs)


def skills(T):
    W, H = 900, 332
    defs, bg = base(T, W, H, sid="k")
    s = [bg, panel(T, 14, 14, 868, 302), heading(50, 66, "Technologies & Skills", T)]
    cell = 800 / 6
    for i, (lab, mono) in enumerate(SKILLS):
        cx = 50 + cell * (i % 6 + .5)
        cy = 130 + (i // 6) * 100
        s.append(cloud(cx, cy, 104, BADGE_FILLS[i % 4], T["rim"], rimw=3, seed=20 + i, cls="bob a",
                       style=f"animation-delay:-{(i * 1.3) % 6:.1f}s;animation-duration:{5 + (i % 3)}s"))
        s.append(f'<text x="{cx:.1f}" y="{cy - 5}" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="700" fill="{BADGE_INK}">{esc(mono)}</text>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 46}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{T["ink"]}">{esc(lab)}</text>')
    return svg(W, H, "".join(s), "Technologies and skills",
               "Twelve cloud badges: " + ", ".join(l for l, _ in SKILLS) + ".", defs)


def projects_title(T):
    W, H = 900, 84
    defs, bg = base(T, W, H, sid="p")
    s = [bg, heading(50, 52, "Selected projects", T, 28)]
    s.append(f'<path class="flow a" d="{wave(330, 850, 44, 5, 90)}" fill="none" stroke="{T["coral"]}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 10"/>')
    s.append(star(866, 44, .7, T["star"]))
    return svg(W, H, "".join(s), "Selected projects", "Section heading.", defs)


def chips(tags):
    rows, x, y = [], 14, 0
    for t in tags:
        w = 9.5 * .58 * len(t) + 14
        if x + w > 186:
            x, y = 14, y + 22
        rows.append((t, x, y, w))
        x += w + 5
    return rows, (y // 22) + 1


def card(T, idx, title, desc, tags, img, nrows):
    W = 208
    ty = 176
    H = ty + nrows * 22 + 16
    ch = H - 14
    r, y0 = 34, 14
    thumb = (f'M14,{y0 + r} A{r},{r} 0 0 1 {14 + r},{y0} H{186 - r} A{r},{r} 0 0 1 186,{y0 + r} V{y0 + 82} H14 Z')
    defs = f'<clipPath id="c{idx}"><path d="{thumb}"/></clipPath>'
    s = [panel(T, 4, 4, 192, ch, 14)]
    s.append(f'<g clip-path="url(#c{idx})"><image href="{img}" x="14" y="{y0}" width="172" height="82" preserveAspectRatio="xMidYMid slice"/></g>')
    s.append(f'<path d="{thumb}" fill="none" stroke="{T["ink"]}" stroke-width="1.8"/>')
    s.append(f'<circle cx="170" cy="96" r="13" fill="{T["crimson"]}" stroke="{T["ink"]}" stroke-width="2"/>'
             f'<text x="170" y="100.5" text-anchor="middle" font-family="{SERIF}" font-size="12" font-weight="700" fill="#FFF3DC">{idx:02d}</text>')
    s.append(f'<text x="14" y="124" font-family="{SERIF}" font-size="{min(16, 160 / (len(title) * 0.72)):.1f}" font-weight="700" font-style="italic" fill="{T["ink"]}">{esc(title)}</text>')
    for i, line in enumerate(textwrap.wrap(desc, 34)[:2]):
        s.append(f'<text x="14" y="{141 + i * 14}" font-family="{SANS}" font-size="10.5" fill="{T["soft"]}">{esc(line)}</text>')
    rows, _ = chips(tags)
    for t, x, y, w in rows:
        s.append(f'<rect x="{x:.1f}" y="{ty + y - 12}" width="{w:.1f}" height="17" rx="8.5" fill="{T["panel2"]}" stroke="{T["accent"]}" stroke-width="1"/>'
                 f'<text x="{x + w / 2:.1f}" y="{ty + y}" text-anchor="middle" font-family="{SANS}" font-size="9.5" font-weight="700" fill="{T["ink"]}">{esc(t)}</text>')
    return svg(W, H, "".join(s), f"Project {title}", f"{title}: {desc} Tags: {', '.join(tags)}.", defs, animated=False)


def city(T, x0, x1, base_y, seed, skip=(400, 500)):
    r = random.Random(seed)
    out, x = [], x0
    while x < x1:
        w, h = r.randint(26, 50), r.randint(22, 58)
        if not (x + w > skip[0] and x < skip[1]):
            roof = T["roofB"] if r.random() < .28 else T["roofA"]
            rh = r.randint(14, 24)
            out.append(f'<rect x="{x}" y="{base_y - h}" width="{w}" height="{h}" fill="{T["city"]}" stroke="{T["ink"]}" stroke-width="1.6"/>')
            out.append(f'<path d="M{x - 3},{base_y - h} L{x + w / 2:.0f},{base_y - h - rh} L{x + w + 3},{base_y - h} Z" fill="{roof}" stroke="{T["ink"]}" stroke-width="1.6" stroke-linejoin="round"/>')
            for wx in range(x + 7, x + w - 6, 12):
                out.append(f'<rect x="{wx}" y="{base_y - h + 10}" width="4" height="7" fill="{T["ink"]}" opacity=".55"/>')
        x += w + r.randint(-4, 3)
    return "".join(out)


def footer(T):
    W, H = 900, 270
    defs, bg = base(T, W, H, sid="f")
    by = 236
    s = [bg, contours(T, W, H, 6, 20, 26, .2)]
    s.append(f'<text x="450" y="50" text-anchor="middle" font-family="{SERIF}" font-size="30" font-weight="700" font-style="italic" fill="{T["ink"]}">{esc(FOOTER_1)}</text>')
    s.append(f'<text x="450" y="78" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="1" fill="{T["soft"]}">{esc(FOOTER_2)}</text>')
    # sun + sea
    s.append(f'<g class="pulse a"><circle cx="450" cy="178" r="64" fill="{T["sun"]}" stroke="{T["ink"]}" stroke-width="2.2"/>'
             f'<circle cx="450" cy="178" r="46" fill="none" stroke="{T["ink"]}" stroke-width="1" opacity=".5"/></g>')
    s.append(f'<rect x="0" y="{by - 44}" width="{W}" height="44" fill="{T["lav"]}" opacity=".55"/>')
    s.append(city(T, 20, 880, by, 11))
    # central tower
    s.append(f'<rect x="432" y="{by - 80}" width="36" height="80" fill="{T["city"]}" stroke="{T["ink"]}" stroke-width="2"/>'
             f'<path d="M428,{by - 80} L450,{by - 120} L472,{by - 80} Z" fill="{T["roofA"]}" stroke="{T["ink"]}" stroke-width="2" stroke-linejoin="round"/>'
             f'<line x1="450" y1="{by - 120}" x2="450" y2="{by - 134}" stroke="{T["ink"]}" stroke-width="2"/>')
    for wy in (by - 62, by - 44, by - 26):
        s.append(f'<rect x="446" y="{wy}" width="8" height="12" rx="4" fill="{T["ink"]}" opacity=".6"/>')
    s.append(star(450, by - 138, 1.2, T["star"]))
    s.append(cloud(120, by + 26, 240, T["cloudfill"], T["rim"], seed=31, cls="drift a", style="animation-duration:28s;animation-delay:-8s"))
    s.append(cloud(790, by + 28, 260, T["cloudfill"], T["rim"], seed=33, cls="drift a", style="animation-duration:25s;animation-delay:-14s"))
    # credit band
    s.append(f'<rect x="0" y="{H - 32}" width="{W}" height="32" fill="{T["band"]}"/>')
    s.append(f'<text x="50" y="{H - 12}" font-family="{SANS}" font-size="11" fill="#FCE9C9">{esc(ART_CREDIT)}</text>')
    s.append(f'<text x="850" y="{H - 12}" text-anchor="end" font-family="{SANS}" font-size="11.5" font-weight="700" fill="#F7C95A">{esc(SIGNATURE)}</text>')
    return svg(W, H, "".join(s), "Footer", f"{FOOTER_1}. {FOOTER_2}. {ART_CREDIT}.", defs)


# ----------------------------------- README -----------------------------------
def pic(name, alt, href=None, width="100%"):
    p = (f'<picture>\n<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'<img alt="{html.escape(alt)}" src="assets/{name}-light.svg" width="{width}">\n</picture>')
    return f'<a href="{href}">\n{p}\n</a>' if href else p


def main():
    os.makedirs(ASSETS, exist_ok=True)
    imgs = {"hero": b64_crop(HERO_CROP, (598, 700), 80), "avatar": b64_crop(AVATAR_CROP, (96, 96), 80)}
    thumbs = [b64_crop(p[4], (400, 190), 80) for p in PROJECTS]
    nrows = max(chips(p[3])[1] for p in PROJECTS)
    for th, T in THEMES.items():
        save("hero", th, hero(T, th, imgs))
        save("btn-github", th, button(T, "GitHub"))
        save("btn-linkedin", th, button(T, "LinkedIn"))
        save("btn-portfolio", th, button(T, "Portfolio"))
        save("about", th, about(T))
        save("skills", th, skills(T))
        save("projects-title", th, projects_title(T))
        save("footer", th, footer(T))
        for i, (title, slug, desc, tags, _) in enumerate(PROJECTS):
            save(f"card-{slug}", th, card(T, i + 1, title, desc, tags, thumbs[i], nrows))
    cards = [pic(f"card-{p[1]}", f"{p[0]}: {p[2]}", f"{GITHUB}/{p[1]}", "24%") for p in PROJECTS]
    md = ['<div align="center">', "",
          pic("hero", f"{FULL_NAME}, {ROLE.title()}. A red dragon flies over a citadel at sunset."), "",
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
