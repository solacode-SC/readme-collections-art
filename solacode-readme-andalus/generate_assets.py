#!/usr/bin/env python3
"""
Profile README generator: "Andalus" (Alhambra / Moroccan zellige: horseshoe arches,
eight-point star friezes, muqarnas, pointed merlons).
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
# (title, slug, description, tags, square crop box in art/source.jpg)
PROJECTS = [
    ("LazyEquation", "lazyequation", "Interactive math & physics visualization platform.",
     ["React", "TS", "Fastify", "PostgreSQL"], (170, 140, 370, 340)),
    ("LeetResume", "leetresume", "AI-powered resume builder and optimizer.",
     ["Next.js", "Prisma", "Postgres"], (130, 410, 290, 570)),
    ("Libora", "libora", "Flutter PDF reader with modern experience.",
     ["Flutter", "Dart", "Riverpod"], (400, 380, 640, 620)),
    ("Webserv", "webserv", "C++98 HTTP server from scratch.",
     ["C++98", "Networking"], (0, 780, 240, 1020)),
    ("solaJobs v2", "solajobs-v2", "Arabic-first job board platform.",
     ["Arabic-first", "Jobs"], (440, 810, 640, 1010)),
    ("Alert Generator", "prometheus-alert-generator", "AI generator for Prometheus alert rules.",
     ["AI", "Prometheus"], (536, 897, 736, 1097)),
    ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose dashboard.",
     ["Docker", "Compose"], (480, 20, 730, 270)),
]
FOOTER_1 = "Build  ·  Explore  ·  Understand"
FOOTER_2 = "Software Engineering · Systems · AI · Mathematics"
# Arabic accents (have a native speaker double-check before publishing)
AR = dict(role="مهندس برمجيات", about="نبذة عني", journey="رحلتي",
          skills="التقنيات والمهارات", projects="مشاريع مختارة", footer="ابنِ · اكتشف · افهم")
AR_NUMS = "\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668"   # Arabic-Indic digits 1-8
ART_CREDIT = "Artwork: Teal Newcomb (Metal Kirin)"
ART_CAPTION = "Artwork: Teal Newcomb"
SIGNATURE = "NashirTech \u00b7 \u0646\u0627\u0634\u0631 \u062a\u0643"
SOURCE = "art/source.jpg"
HERO_CROP = (0, 115, 736, 1097)     # starts below the artist watermark, ends at the image bottom
# ================================================================================

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
ARAB = "'Amiri','Scheherazade New','Noto Naskh Arabic','Geeza Pro','Segoe UI',Tahoma,serif"

TILES = ["#2A8C82", "#C4573C", "#8FB39A", "#A99CD0"]   # teal, terracotta, sage, lavender (from the art)
THEMES = {
    "dark": dict(bg="#0D1B19", bg2="#183530", panel="#132826", panel2="#1C3A35", ink="#F3EAD3",
                 soft="#C2D2C4", accent="#E8B27A", gold="#CDA652", line="#CDA652", band="#081211",
                 btn="#B04A32", btntxt="#FFF6E0", seal="#C4573C", glow="#A99CD0", star="#F6E3A8"),
    "light": dict(bg="#F5ECD6", bg2="#E6E4CF", panel="#FBF6E6", panel2="#EBE5D0", ink="#17332F",
                  soft="#496660", accent="#A2412A", gold="#B38B34", line="#B38B34", band="#17332F",
                  btn="#B04A32", btntxt="#FFF6E0", seal="#B04A32", glow="#A99CD0", star="#B38B34"),
}

CSS = """
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.kb{transform-box:fill-box;transform-origin:50% 45%;animation-name:kb;animation-duration:32s}
.glint{transform-box:fill-box;transform-origin:center;animation-name:glint;animation-duration:4s}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:90s;animation-timing-function:linear;animation-direction:normal}
.flow{animation-name:flow;animation-duration:6s;animation-timing-function:linear;animation-direction:normal}
.breathe{animation-name:breathe;animation-duration:7s}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.06)}}
@keyframes glint{0%{opacity:.3;transform:scale(.6)}60%{opacity:1;transform:scale(1.1)}100%{opacity:.4;transform:scale(.7)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flow{to{stroke-dashoffset:-48}}
@keyframes breathe{from{opacity:.55}to{opacity:1}}
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


# ------------------------------- geometry helpers -------------------------------
def star8_pts(cx, cy, ro, ratio=.62):
    pts = []
    for i in range(16):
        a = -math.pi / 2 + i * math.pi / 8
        r = ro if i % 2 == 0 else ro * ratio
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def star8(cx, cy, ro, fill, stroke=None, sw=1, op=1):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return f'<polygon points="{star8_pts(cx, cy, ro)}" fill="{fill}"{st} opacity="{op}"/>'


def diamond(cx, cy, r, fill):
    return f'<path d="M{cx:.1f},{cy - r:.1f} L{cx + r:.1f},{cy:.1f} L{cx:.1f},{cy + r:.1f} L{cx - r:.1f},{cy:.1f} Z" fill="{fill}"/>'


def horseshoe(x, y, W, H, pad=0):
    R0 = W / 1.92
    cx, cy = x + W / 2, y + R0
    R = R0 + pad
    d, ys = .96 * R, cy + .28 * R
    return f"M{cx - d:.1f},{ys:.1f} A{R:.1f},{R:.1f} 0 1 1 {cx + d:.1f},{ys:.1f} V{y + H + pad:.1f} H{cx - d:.1f} Z"


def merlons(x, y, w, n, h=14):
    u = w / n
    d = f"M{x},{y + h}"
    for i in range(n):
        d += f" L{x + u * i + u / 2:.1f},{y} L{x + u * (i + 1):.1f},{y + h}"
    return d


def frieze(T, x0, x1, y, h, phase=0, breathe=False):
    step = h * 1.3
    n = int((x1 - x0) / step)
    off = (x1 - x0 - n * step) / 2 + step / 2
    out = [f'<path d="M{x0},{y + h / 2} H{x1}" stroke="{T["gold"]}" stroke-width="1" opacity=".6"/>']
    for i in range(n):
        cx = x0 + off + i * step
        cls = ' class="breathe a"' if breathe and i % 3 == 0 else ""
        style = f' style="animation-delay:-{i % 7}s"' if cls else ""
        out.append(f'<g{cls}{style}>{star8(cx, y + h / 2, h / 2, TILES[(i + phase) % 4], T["ink"], .8)}</g>')
        if i < n - 1:
            out.append(diamond(cx + step / 2, y + h / 2, h * .16, T["gold"]))
    return "".join(out)


def muqarnas(T, x0, x1, y, tiers=3):
    out = []
    w, h = 44, 34
    for t in range(tiers):
        cnt = int((x1 - x0) / w) + 2
        for i in range(cnt):
            x = x0 + i * w - (w / 2 if t % 2 else 0) - (t * 2)
            yy = y + t * 20
            d = (f"M{x:.1f},{yy} C{x:.1f},{yy + h * .7:.1f} {x + w / 2 - 7:.1f},{yy + h * .88:.1f} {x + w / 2:.1f},{yy + h:.1f} "
                 f"C{x + w / 2 + 7:.1f},{yy + h * .88:.1f} {x + w:.1f},{yy + h * .7:.1f} {x + w:.1f},{yy} Z")
            out.append(f'<path d="{d}" fill="{TILES[(i + t) % 4]}" stroke="{T["ink"]}" stroke-width="1" opacity="{.95 - t * .1:.2f}"/>')
    return "".join(out)


def tile_pattern(T, pid):
    return (f'<pattern id="{pid}" width="56" height="56" patternUnits="userSpaceOnUse">'
            f'<rect x="9" y="9" width="38" height="38" fill="none" stroke="{T["line"]}" stroke-width=".8"/>'
            f'<path d="M28,2 L54,28 L28,54 L2,28 Z" fill="none" stroke="{T["line"]}" stroke-width=".8"/>'
            f'<circle cx="28" cy="28" r="3" fill="none" stroke="{T["line"]}" stroke-width=".8"/></pattern>')


def base(T, W, H, sid="s"):
    defs = (f'<linearGradient id="{sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/>'
            f'<stop offset="1" stop-color="{T["bg2"]}"/></linearGradient>' + tile_pattern(T, sid + "t"))
    return defs, (f'<rect width="{W}" height="{H}" fill="url(#{sid}g)"/>'
                  f'<rect width="{W}" height="{H}" fill="url(#{sid}t)" opacity=".13"/>')


def star_twinkle(x, y, s, T, delay=0):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})"><path class="glint a" style="animation-delay:-{delay}s" fill="{T["star"]}" '
            f'd="M0,-12 L2.4,-2.4 L12,0 L2.4,2.4 L0,12 L-2.4,2.4 L-12,0 L-2.4,-2.4Z"/></g>')


def panel(T, x, y, w, h, n):
    d = merlons(x, y, w, n) + f" V{y + h} H{x} Z"
    return (f'<path d="{d}" fill="{T["panel"]}" stroke="{T["gold"]}" stroke-width="2" stroke-linejoin="round"/>'
            f'<rect x="{x + 8}" y="{y + 20}" width="{w - 16}" height="{h - 28}" fill="none" stroke="{T["gold"]}" stroke-width=".8" opacity=".6"/>'
            + frieze(T, x + 18, x + w - 18, y + 26, 18, 0))


def heading(x, y, text, ar, ar_right, T, size=28):
    arsize = 21
    arw = len(ar) * arsize * .45
    return (star8(x + 11, y - 9, 11, TILES[1], T["ink"], 1) +
            f'<text x="{x + 32}" y="{y}" font-family="{SERIF}" font-size="{size}" letter-spacing=".8" fill="{T["ink"]}">{esc(text)}</text>'
            f'<text x="{ar_right - arw / 2:.0f}" y="{y - 1}" text-anchor="middle" font-family="{ARAB}" font-size="{arsize}" fill="{T["accent"]}">{ar}</text>')


# ----------------------------------- panels -----------------------------------
def hero(T, imgs):
    W, H = 900, 610
    defs, bg = base(T, W, H, "h")
    ax, ay, aw, ah = 530, 52, 320, 480
    defs += f'<clipPath id="hclip"><path d="{horseshoe(ax, ay, aw, ah)}"/></clipPath><clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>'
    defs += (f'<radialGradient id="hglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{T["glow"]}" stop-opacity=".5"/>'
             f'<stop offset="1" stop-color="{T["glow"]}" stop-opacity="0"/></radialGradient>')
    s = [bg, f'<ellipse cx="{ax + aw / 2}" cy="{ay + ah / 2}" rx="280" ry="310" fill="url(#hglow)"/>']
    s.append(f'<image href="{imgs[1]}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>')
    s.append(f'<circle cx="64" cy="34" r="14" fill="none" stroke="{T["gold"]}" stroke-width="1.8"/>')
    s.append(f'<text x="86" y="39" font-family="{MONO}" font-size="12.5" fill="{T["soft"]}">{esc(HANDLE)} / README</text>')
    s.append(f'<path d="M50,62 H470" stroke="{T["gold"]}" stroke-width="1.2"/>' + star8(260, 62, 8, TILES[1], T["ink"], .8))
    s.append(f'<text x="52" y="128" font-family="{SERIF}" font-size="19" font-style="italic" fill="{T["soft"]}">Hi, I\'m</text>')
    for txt, y in ((NAME_1, 198), (NAME_2, 266)):
        s.append(f'<text x="54" y="{y + 3}" font-family="{SERIF}" font-size="62" letter-spacing="1" fill="{TILES[0]}" opacity=".55">{esc(txt)}</text>')
        s.append(f'<text x="52" y="{y}" font-family="{SERIF}" font-size="62" letter-spacing="1" fill="{T["ink"]}">{esc(txt)}</text>')
    s.append(f'<text x="53" y="324" font-family="{SANS}" font-size="13.5" font-weight="700" letter-spacing="5" fill="{T["accent"]}">{esc(ROLE)}</text>')
    s.append(f'<text x="425" y="325" text-anchor="middle" font-family="{ARAB}" font-size="19" fill="{T["accent"]}">{AR["role"]}</text>')
    sep = "\u00a0\u00a0|\u00a0\u00a0"
    s.append(f'<text x="53" y="358" font-family="{SERIF}" font-size="17.5" font-style="italic" fill="{T["ink"]}">{esc(sep.join(PILLARS))}</text>')
    for i, line in enumerate(TAGLINE):
        s.append(f'<text x="53" y="{408 + i * 23}" font-family="{SERIF}" font-size="15.5" fill="{T["soft"]}">{esc(line)}</text>')
    # horseshoe arch with zellige border
    s.append(f'<path d="{horseshoe(ax, ay, aw, ah, 15)}" fill="none" stroke="{TILES[0]}" stroke-width="9"/>')
    s.append(f'<path d="{horseshoe(ax, ay, aw, ah, 15)}" fill="none" stroke="{TILES[1]}" stroke-width="9" stroke-dasharray="9 27"/>')
    s.append(f'<path d="{horseshoe(ax, ay, aw, ah, 15)}" fill="none" stroke="{TILES[3]}" stroke-width="9" stroke-dasharray="9 27" stroke-dashoffset="-18"/>')
    s.append(f'<path d="{horseshoe(ax, ay, aw, ah, 21)}" fill="none" stroke="{T["gold"]}" stroke-width="2"/>')
    s.append(f'<path d="{horseshoe(ax, ay, aw, ah, 9)}" fill="none" stroke="{T["gold"]}" stroke-width="1.4"/>')
    s.append(f'<g clip-path="url(#hclip)"><image class="kb a" href="{imgs["hero"]}" x="{ax}" y="{ay}" width="{aw}" height="{ah}" preserveAspectRatio="xMidYMid slice"/></g>')
    s.append(f'<path d="{horseshoe(ax, ay, aw, ah)}" fill="none" stroke="{T["ink"]}" stroke-width="1.5"/>')
    s.append(star8(ax + aw / 2, ay - 42, 13, TILES[1], T["ink"], 1.2))
    s.append(star_twinkle(ax + aw / 2, ay - 42, .8, T))
    s.append(f'<text x="{ax + aw / 2}" y="{ay + ah + 36}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{T["soft"]}">{esc(ART_CAPTION)}</text>')
    s.append(frieze(T, 0, W, H - 34, 22, 1, breathe=True))
    return svg(W, H, "".join(s), f"{FULL_NAME}: {ROLE.title()}",
               "Profile header with name and role beside a horseshoe-arch window showing two pale lavender dragons among flowers.", defs)


def button(T, label):
    body = (f'<path d="M14,3 H136 L147,20 L136,37 H14 L3,20 Z" fill="{T["btn"]}" stroke="{T["gold"]}" stroke-width="1.6"/>'
            + star8(28, 20, 8, T["btntxt"]) +
            f'<text x="89" y="25.5" text-anchor="middle" font-family="{SERIF}" font-size="15" letter-spacing=".8" fill="{T["btntxt"]}">{esc(label)}</text>')
    return svg(150, 40, body, label, f"Button linking to {label}", animated=False)


def about(T):
    W, H = 900, 410
    defs, bg = base(T, W, H, "a")
    s = [bg, panel(T, 18, 14, 864, 376, 24)]
    s.append(heading(52, 104, "About", AR["about"], 440, T))
    s.append(heading(520, 104, "My journey", AR["journey"], 850, T))
    lines = textwrap.wrap(ABOUT, 52)
    for i, line in enumerate(lines):
        s.append(f'<text x="54" y="{146 + i * 24}" font-family="{SERIF}" font-size="14.5" fill="{T["ink"]}">{esc(line)}</text>')
    y = 146 + 24 * len(lines) + 24
    for line in textwrap.wrap(FACTS, 58):
        s.append(f'<text x="54" y="{y}" font-family="{SANS}" font-size="12" fill="{T["soft"]}">{esc(line)}</text>')
        y += 18
    s.append(f'<text x="54" y="{y + 8}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{T["accent"]}">{esc(FOCUS)}</text>')
    s.append(f'<path d="M488,84 V350" stroke="{T["gold"]}" stroke-width="1.2"/>')
    for k, yy in enumerate((130, 217, 304)):
        s.append(star8(488, yy, 7, TILES[(k + 1) % 4], T["ink"], .8))
    for i, (lang, area) in enumerate(JOURNEY):
        yy = 160 + i * 44
        x1 = 520 + len(lang) * 10.4 + 14
        x2 = 850 - len(area) * 7.6 - 30
        s.append(f'<text x="520" y="{yy}" font-family="{SERIF}" font-size="18" fill="{T["ink"]}">{esc(lang)}</text>')
        s.append(f'<line class="flow a" x1="{x1:.0f}" y1="{yy - 5}" x2="{x2:.0f}" y2="{yy - 5}" stroke="{TILES[i % 4]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="3 9"/>')
        s.append(diamond(round(x2 + 10), yy - 5, 4, T["gold"]))
        s.append(f'<text x="850" y="{yy}" text-anchor="end" font-family="{SANS}" font-size="13.5" font-weight="700" fill="{T["accent"]}">{esc(area)}</text>')
    return svg(W, H, "".join(s), "About and journey",
               "About text on the left; on the right the journey: " + ", ".join(f"{a} to {b}" for a, b in JOURNEY) + ".", defs)


def skills(T):
    W, H = 900, 440
    defs, bg = base(T, W, H, "k")
    s = [bg, panel(T, 18, 14, 864, 406, 24), heading(52, 104, "Technologies & Skills", AR["skills"], 850, T)]
    cell = 800 / 6
    for i, (lab, mono) in enumerate(SKILLS):
        cx = 50 + cell * (i % 6 + .5)
        cy = 196 + (i // 6) * 118
        col = TILES[i % 4]
        s.append(f'<g class="spin a" style="animation-delay:-{i * 9}s"><polygon points="{star8_pts(cx, cy, 46, .8)}" fill="none" stroke="{T["gold"]}" stroke-width="1.2" stroke-dasharray="4 5"/></g>')
        s.append(star8(cx, cy, 38, col, T["ink"], 1.6))
        s.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="18" fill="{T["panel"]}" stroke="{T["ink"]}" stroke-width="1.4"/>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 5}" text-anchor="middle" font-family="{SERIF}" font-size="14" font-weight="700" fill="{T["ink"]}">{esc(mono)}</text>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 62}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{T["ink"]}">{esc(lab)}</text>')
    return svg(W, H, "".join(s), "Technologies and skills",
               "Twelve eight-point star tiles: " + ", ".join(l for l, _ in SKILLS) + ".", defs)


def projects_title(T):
    W, H = 900, 96
    defs, bg = base(T, W, H, "p")
    s = [bg, heading(52, 58, "Selected projects", AR["projects"], 850, T, 30),
         frieze(T, 420, 700, 40, 16, 2)]
    return svg(W, H, "".join(s), "Selected projects", "Section heading.", defs, animated=False)


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
    W, H = 208, 284
    defs = f'<clipPath id="c{idx}"><path d="{horseshoe(38, 34, 132, 122)}"/></clipPath>'
    body = merlons(6, 6, 196, 7, 12) + f" V{H - 8} H6 Z"
    g = [f'<path d="{body}" fill="{T["panel"]}" stroke="{T["gold"]}" stroke-width="2" stroke-linejoin="round"/>',
         f'<path d="{horseshoe(38, 34, 132, 122, 6)}" fill="none" stroke="{TILES[(idx - 1) % 4]}" stroke-width="5"/>',
         f'<g clip-path="url(#c{idx})"><image href="{img}" x="38" y="34" width="132" height="122" preserveAspectRatio="xMidYMid slice"/></g>',
         f'<path d="{horseshoe(38, 34, 132, 122)}" fill="none" stroke="{T["ink"]}" stroke-width="1.4"/>',
         star8(104, 158, 17, T["seal"], T["ink"], 1.4),
         f'<text x="104" y="164" text-anchor="middle" font-family="{ARAB}" font-size="17" font-weight="700" fill="#FFF6E0">{AR_NUMS[idx - 1]}</text>',
         f'<text x="104" y="198" text-anchor="middle" font-family="{SERIF}" font-size="{min(16, 176 / (len(title) * .66)):.1f}" font-weight="700" fill="{T["ink"]}">{esc(title)}</text>']
    for i, line in enumerate(textwrap.wrap(desc, 34)[:2]):
        g.append(f'<text x="104" y="{217 + i * 14}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{T["soft"]}">{esc(line)}</text>')
    for i, line in enumerate(tag_lines(tags)):
        g.append(f'<text x="104" y="{250 + i * 15}" text-anchor="middle" font-family="{SANS}" font-size="10.5" font-weight="700" fill="{T["accent"]}">{esc(line)}</text>')
    return svg(W, H, "".join(g), f"Project {title}", f"{title}: {desc} Tags: {', '.join(tags)}.", defs, animated=False)


def footer(T):
    W, H = 900, 350
    defs, bg = base(T, W, H, "f")
    s = [bg, muqarnas(T, -20, W + 20, 0, 3)]
    s.append(f'<text x="450" y="164" text-anchor="middle" font-family="{SERIF}" font-size="31" letter-spacing="1" fill="{T["ink"]}">{esc(FOOTER_1)}</text>')
    s.append(f'<text x="450" y="198" text-anchor="middle" font-family="{ARAB}" font-size="23" fill="{T["accent"]}">{AR["footer"]}</text>')
    s.append(f'<text x="450" y="226" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="1" fill="{T["soft"]}">{esc(FOOTER_2)}</text>')
    s.append(frieze(T, 0, W, H - 82, 24, 0, breathe=True))
    s.append(star_twinkle(450, 116, 1, T))
    s.append(f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="{T["band"]}"/>')
    s.append(f'<path d="M0,{H - 34} H{W}" stroke="{T["gold"]}" stroke-width="2"/>')
    s.append(f'<text x="30" y="{H - 13}" font-family="{SANS}" font-size="10.5" fill="#F3EAD3">{esc(ART_CREDIT)}</text>')
    s.append(f'<text x="870" y="{H - 13}" text-anchor="end" font-family="{SANS}" font-size="11.5" font-weight="700" fill="#E8B27A">{esc(SIGNATURE)}</text>')
    return svg(W, H, "".join(s), "Footer", f"{FOOTER_1}. {FOOTER_2}.", defs)


# ----------------------------------- README -----------------------------------
def pic(name, alt, href=None, width="100%"):
    p = (f'<picture>\n<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'<img alt="{html.escape(alt)}" src="assets/{name}-light.svg" width="{width}">\n</picture>')
    return f'<a href="{href}">\n{p}\n</a>' if href else p


def main():
    os.makedirs(ASSETS, exist_ok=True)
    thumbs = [b64_crop(p[4], (220, 220)) for p in PROJECTS]
    imgs = {"hero": b64_crop(HERO_CROP, (640, 854), 82), 1: thumbs[1]}
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
          pic("hero", f"{FULL_NAME}, {ROLE.title()}. Two pale dragons among flowers inside a horseshoe arch."), "",
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
