#!/usr/bin/env python3
"""
Profile README generator: "Lapis & Gold" (indigo, kintsugi gold filigree, ivory vellum).
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
     ["React", "TS", "Fastify", "PostgreSQL"], (0, 40, 300, 183)),
    ("LeetResume", "leetresume", "AI-powered resume builder and optimizer.",
     ["Next.js", "Prisma", "Postgres"], (60, 120, 270, 220)),
    ("Libora", "libora", "Flutter PDF reader with modern experience.",
     ["Flutter", "Dart", "Riverpod"], (110, 430, 330, 535)),
    ("Webserv", "webserv", "C++98 HTTP server from scratch.",
     ["C++98", "Networking"], (340, 70, 526, 158)),
    ("solaJobs v2", "solajobs-v2", "Arabic-first job board platform.",
     ["Arabic-first", "Jobs"], (330, 420, 526, 513)),
    ("Alert Generator", "prometheus-alert-generator", "AI generator for Prometheus alert rules.",
     ["AI", "Prometheus"], (0, 640, 300, 783)),
    ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose dashboard.",
     ["Docker", "Compose"], (300, 650, 526, 770)),
]
FOOTER_1 = "Build  ·  Explore  ·  Understand"
FOOTER_2 = "Software Engineering · Systems · AI · Mathematics"
ART_CREDIT = "Artwork: source unknown (update this line when you know the artist)"
SIGNATURE = "NashirTech \u00b7 \u0646\u0627\u0634\u0631 \u062a\u0643"
SOURCE = "art/source.jpg"
HERO_CROP = (0, 0, 526, 789)
AVATAR_CROP = (95, 120, 215, 240)
MEDALLION_CROP = (60, 100, 260, 300)
# ================================================================================

SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {
    "dark": dict(bg="#0B0F2E", bg2="#1B2466", panel="#141B4F", panel2="#1F2A70", ink="#F3EBDD",
                 soft="#C9CDEB", accent="#E8C46A", gold="#E3BE63", blue="#7FA7D6", pink="#E08AA8",
                 shadow="#05071A", band="#070A1F", glow="#8E9BDB", star="#FFF3C4"),
    "light": dict(bg="#F5EDDF", bg2="#E2E2F1", panel="#FCF8EE", panel2="#E9E6F4", ink="#161C5A",
                  soft="#4A5088", accent="#7A5A12", gold="#BE9435", blue="#5E88C4", pink="#C8607F",
                  shadow="#C9CDEB", band="#161C5A", glow="#8E9BDB", star="#BE9435"),
}
ROUNDEL = [("#8E9BDB", "#101648"), ("#6BB5C9", "#101648"), ("#E08AA8", "#2A0F2E"), ("#1F2F8A", "#F3EBDD")]

CSS = """
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.kb{transform-box:fill-box;transform-origin:50% 40%;animation-name:kb;animation-duration:28s}
.glint{transform-box:fill-box;transform-origin:center;animation-name:glint;animation-duration:3.6s}
.sweep{animation-name:sweep;animation-duration:10s;animation-timing-function:ease-in-out;animation-direction:normal}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:70s;animation-timing-function:linear;animation-direction:normal}
.flow{animation-name:flow;animation-duration:3.5s;animation-timing-function:linear;animation-direction:normal}
.pulse{transform-box:fill-box;transform-origin:center;animation-name:pulse;animation-duration:6s}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
@keyframes glint{0%{opacity:.2;transform:scale(.5)}60%{opacity:1;transform:scale(1.1)}100%{opacity:.3;transform:scale(.6)}}
@keyframes sweep{0%{transform:translateX(-160px)}55%,100%{transform:translateX(520px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flow{to{stroke-dashoffset:-48}}
@keyframes pulse{from{opacity:.75;transform:scale(1)}to{opacity:1;transform:scale(1.04)}}
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


def vwave(x, y0, y1, amp, wl, step=6):
    pts, y = [], y0
    while y <= y1:
        pts.append(f"{x + amp * math.sin((y - y0) / wl * 2 * math.pi):.1f},{y:.1f}")
        y += step
    return "M" + " L".join(pts)


def rosette(cx, cy, r, T, petals=6, fill=None):
    fill = fill or T["gold"]
    ps = "".join(
        f'<circle cx="{cx + r * .56 * math.cos(a):.1f}" cy="{cy + r * .56 * math.sin(a):.1f}" r="{r * .44:.1f}"/>'
        for a in [i * 2 * math.pi / petals for i in range(petals)])
    return (f'<g fill="{fill}">{ps}</g><circle cx="{cx}" cy="{cy}" r="{r * .3:.1f}" fill="{T["panel"]}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .14:.1f}" fill="{fill}"/>')


def diamond(cx, cy, r, fill):
    return f'<path d="M{cx},{cy - r} L{cx + r},{cy} L{cx},{cy + r} L{cx - r},{cy} Z" fill="{fill}"/>'


def star(x, y, s, T, cls="glint a", style=""):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})"><path class="{cls}" style="{style}" fill="{T["star"]}" '
            f'd="M0,-12 L2.4,-2.4 L12,0 L2.4,2.4 L0,12 L-2.4,2.4 L-12,0 L-2.4,-2.4Z"/></g>')


def veins(T, x0, y0, x1, y1, seed, n=16, op=.35):
    """Kintsugi crack network: random-walk gold lines with branches."""
    r = random.Random(seed)
    out = []

    def walk(x, y, a, steps, depth):
        pts = [(x, y)]
        for _ in range(steps):
            a += r.uniform(-.7, .7)
            x += math.cos(a) * r.uniform(12, 26)
            y += math.sin(a) * r.uniform(12, 26)
            if not (x0 <= x <= x1 and y0 <= y <= y1):
                break
            pts.append((x, y))
            if depth < 2 and r.random() < .22:
                walk(x, y, a + r.choice((-1, 1)) * r.uniform(.6, 1.2), steps // 2, depth + 1)
        if len(pts) > 1:
            out.append("M" + " L".join(f"{px:.0f},{py:.0f}" for px, py in pts))

    for _ in range(n):
        walk(r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(0, 6.28), r.randint(5, 9), 0)
    return (f'<path d="{" ".join(out)}" fill="none" stroke="{T["gold"]}" stroke-width=".9" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>')


def vine(T, x0, x1, y, amp, wl, seed, flower_every=3):
    r = random.Random(seed)
    parts = [f'<path d="{wave(x0, x1, y, amp, wl)}" fill="none" stroke="{T["gold"]}" stroke-width="1.8" stroke-linecap="round"/>']
    k = 0
    x = x0 + wl / 4
    while x < x1:
        yy = y + amp * math.sin((x - x0) / wl * 2 * math.pi)
        side = -1 if k % 2 else 1
        if k % flower_every == 2:
            parts.append(rosette(round(x, 1), round(yy + side * 9, 1), 6.5, T))
        else:
            ang = -30 if side < 0 else 30
            parts.append(f'<path transform="translate({x:.1f},{yy:.1f}) rotate({ang + r.randint(-10, 10)})" '
                         f'd="M0,0 Q8,{side * -9} 18,{side * -3} Q9,{side * 3} 0,0 Z" fill="{T["gold"]}" opacity=".85"/>')
        x += wl / 2
        k += 1
    return "".join(parts)


def base(T, W, H, sid="s", glow=False):
    defs = (f'<linearGradient id="{sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/>'
            f'<stop offset="1" stop-color="{T["bg2"]}"/></linearGradient>')
    return defs, f'<rect width="{W}" height="{H}" fill="url(#{sid}g)"/>'


def panel(T, x, y, w, h):
    corners = "".join(rosette(cx, cy, 6, T) for cx, cy in
                      ((x, y), (x + w, y), (x, y + h), (x + w, y + h)))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{T["panel"]}" stroke="{T["gold"]}" stroke-width="2"/>'
            f'<rect x="{x + 7}" y="{y + 7}" width="{w - 14}" height="{h - 14}" rx="2" fill="none" stroke="{T["gold"]}" stroke-width=".9" opacity=".7"/>'
            + corners)


def heading(x, y, text, T, size=26):
    return (rosette(x + 11, y - 9, 9, T) +
            f'<text x="{x + 30}" y="{y}" font-family="{SERIF}" font-size="{size}" letter-spacing=".6" fill="{T["ink"]}">{esc(text)}</text>'
            f'<path d="M{x + 30},{y + 12} H{x + 150}" stroke="{T["gold"]}" stroke-width="1.6"/>' + diamond(x + 156, y + 12, 4, T["gold"]))


def arch(x, y, w, h, pad=0):
    r = w / 2 + pad
    return (f"M{x - pad},{y + w / 2} A{r},{r} 0 0 1 {x + w + pad},{y + w / 2} V{y + h + pad} H{x - pad} Z")


# ----------------------------------- panels -----------------------------------
def hero(T, imgs):
    W, H = 900, 580
    defs, bg = base(T, W, H, "h")
    fx, fy, fw = 520, 36, 330
    fh = round(fw * 789 / 526)
    defs += f'<clipPath id="hclip"><path d="{arch(fx, fy, fw, fh)}"/></clipPath><clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>'
    defs += (f'<radialGradient id="hglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{T["glow"]}" stop-opacity=".45"/>'
             f'<stop offset="1" stop-color="{T["glow"]}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="hsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="#fff" stop-opacity=".38"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    s = [bg, veins(T, 0, 0, 500, H, 7, 14, .3), veins(T, 560, 0, W, H, 9, 8, .25)]
    s.append(f'<ellipse cx="{fx + fw / 2}" cy="{fy + fh / 2}" rx="280" ry="320" fill="url(#hglow)"/>')
    s.append(f'<image href="{imgs["avatar"]}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>')
    s.append(f'<circle cx="64" cy="34" r="14" fill="none" stroke="{T["gold"]}" stroke-width="2"/>')
    s.append(f'<text x="86" y="39" font-family="{MONO}" font-size="12.5" fill="{T["soft"]}">{esc(HANDLE)} / README</text>')
    s.append(f'<path d="M50,62 H460" stroke="{T["gold"]}" stroke-width="1.2"/>' + diamond(255, 62, 4.5, T["gold"]))
    s.append(f'<text x="52" y="124" font-family="{SERIF}" font-size="19" font-style="italic" fill="{T["soft"]}">Hi, I\'m</text>')
    for txt, y in ((NAME_1, 196), (NAME_2, 266)):
        s.append(f'<text x="55" y="{y + 3}" font-family="{SERIF}" font-size="64" fill="none" stroke="{T["gold"]}" stroke-width="1.2">{esc(txt)}</text>')
        s.append(f'<text x="52" y="{y}" font-family="{SERIF}" font-size="64" fill="{T["ink"]}">{esc(txt)}</text>')
    s.append(f'<text x="53" y="326" font-family="{SANS}" font-size="13.5" font-weight="700" letter-spacing="6" fill="{T["accent"]}">{esc(ROLE)}</text>')
    sep = "\u00a0\u00a0|\u00a0\u00a0"
    s.append(f'<text x="53" y="358" font-family="{SERIF}" font-size="17.5" font-style="italic" fill="{T["ink"]}">{esc(sep.join(PILLARS))}</text>')
    for i, line in enumerate(TAGLINE):
        s.append(f'<text x="53" y="{404 + i * 23}" font-family="{SERIF}" font-size="15.5" fill="{T["soft"]}">{esc(line)}</text>')
    s.append(vine(T, 50, 470, 506, 8, 110, 4))
    # arch frame
    s.append(f'<path d="{arch(fx, fy, fw, fh, 9)}" fill="none" stroke="{T["gold"]}" stroke-width="2.4"/>')
    s.append(f'<g clip-path="url(#hclip)"><image class="kb a" href="{imgs["hero"]}" x="{fx}" y="{fy}" width="{fw}" height="{fh}" preserveAspectRatio="xMidYMid slice"/>'
             f'<rect class="sweep a" x="{fx}" y="{fy}" width="90" height="{fh}" fill="url(#hsw)" transform="skewX(-12)"/></g>')
    s.append(f'<path d="{arch(fx, fy, fw, fh)}" fill="none" stroke="{T["ink"]}" stroke-width="1.5"/>')
    s.append(star(fx + 20, fy + fh * .62, .8, T, style="animation-delay:-1s"))
    s.append(star(fx + fw - 24, fy + fh * .3, 1, T, style="animation-delay:-2.4s"))
    s.append(star(fx + 118, fy + 70, .7, T, style="animation-delay:-3s"))
    s.append(rosette(fx + fw / 2, fy - 18, 9, T))
    return svg(W, H, "".join(s), f"{FULL_NAME}: {ROLE.title()}",
               "Profile header with name, role, and an illustration of a blue dragon beside a crowned woman in a gold-embroidered gown.", defs)


def button(T, label):
    body = (f'<path d="M12,3 H138 L147,19 L138,35 H12 L3,19 Z" fill="{T["panel2"]}" stroke="{T["gold"]}" stroke-width="2"/>'
            f'<path d="M15,7 H135 L142,19 L135,31 H15 L8,19 Z" fill="none" stroke="{T["gold"]}" stroke-width=".8" opacity=".7"/>'
            + rosette(26, 19, 6, T) +
            f'<text x="86" y="24.5" text-anchor="middle" font-family="{SERIF}" font-size="15" letter-spacing=".8" fill="{T["ink"]}">{esc(label)}</text>')
    return svg(150, 40, body, label, f"Button linking to {label}", animated=False)


def about(T):
    W, H = 900, 340
    defs, bg = base(T, W, H, "a")
    s = [bg, panel(T, 16, 16, 868, 306), heading(50, 70, "About", T), heading(526, 70, "My journey", T)]
    lines = textwrap.wrap(ABOUT, 52)
    for i, line in enumerate(lines):
        s.append(f'<text x="52" y="{110 + i * 24}" font-family="{SERIF}" font-size="14.5" fill="{T["ink"]}">{esc(line)}</text>')
    y = 110 + 24 * len(lines) + 22
    for line in textwrap.wrap(FACTS, 58):
        s.append(f'<text x="52" y="{y}" font-family="{SANS}" font-size="12" fill="{T["soft"]}">{esc(line)}</text>')
        y += 18
    s.append(f'<text x="52" y="{y + 8}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{T["accent"]}">{esc(FOCUS)}</text>')
    s.append(f'<path d="{vwave(498, 50, 296, 3, 70)}" fill="none" stroke="{T["gold"]}" stroke-width="1.6"/>' + rosette(498, 173, 7, T))
    for i, (lang, area) in enumerate(JOURNEY):
        yy = 124 + i * 44
        x1 = 530 + len(lang) * 10.6 + 12
        x2 = 850 - len(area) * 7.6 - 32
        s.append(f'<text x="530" y="{yy}" font-family="{SERIF}" font-size="18" fill="{T["ink"]}">{esc(lang)}</text>')
        s.append(f'<line class="flow a" x1="{x1:.0f}" y1="{yy - 5}" x2="{x2:.0f}" y2="{yy - 5}" stroke="{T["gold"]}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="2 10"/>')
        s.append(diamond(round(x2 + 8), yy - 5, 3.5, T["gold"]))
        s.append(f'<text x="850" y="{yy}" text-anchor="end" font-family="{SANS}" font-size="13.5" font-weight="700" fill="{T["accent"]}">{esc(area)}</text>')
    return svg(W, H, "".join(s), "About and journey",
               "About text on the left; on the right the journey: " + ", ".join(f"{a} to {b}" for a, b in JOURNEY) + ".", defs)


def skills(T):
    W, H = 900, 340
    defs, bg = base(T, W, H, "k")
    s = [bg, panel(T, 16, 16, 868, 306), heading(50, 70, "Technologies & Skills", T)]
    cell = 800 / 6
    for i, (lab, mono) in enumerate(SKILLS):
        cx = 50 + cell * (i % 6 + .5)
        cy = 142 + (i // 6) * 104
        fill, txt = ROUNDEL[i % 4]
        s.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="33" fill="{fill}" stroke="{T["gold"]}" stroke-width="3"/>')
        s.append(f'<circle class="spin a" cx="{cx:.1f}" cy="{cy}" r="27" fill="none" stroke="{T["gold"]}" stroke-width="1.3" stroke-dasharray="3 5" style="animation-delay:-{i * 7}s"/>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 6}" text-anchor="middle" font-family="{SERIF}" font-size="17" font-weight="700" fill="{txt}">{esc(mono)}</text>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 55}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{T["ink"]}">{esc(lab)}</text>')
    return svg(W, H, "".join(s), "Technologies and skills",
               "Twelve gold-ringed medallions: " + ", ".join(l for l, _ in SKILLS) + ".", defs)


def projects_title(T):
    W, H = 900, 84
    defs, bg = base(T, W, H, "p")
    s = [bg, heading(50, 52, "Selected projects", T, 28), vine(T, 360, 850, 44, 6, 90, 2)]
    return svg(W, H, "".join(s), "Selected projects", "Section heading.", defs, animated=False)


def chips(tags):
    rows, x, y = [], 14, 0
    for t in tags:
        w = 9.5 * .58 * len(t) + 14
        if x + w > 186:
            x, y = 14, y + 22
        rows.append((t, x, y, w))
        x += w + 5
    return rows, (y // 22) + 1


ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def card(T, idx, title, desc, tags, img, nrows):
    W, ty = 208, 190
    H = ty + nrows * 22 + 18
    cw, ch = 196, H - 10
    ox, oy = 6, 5
    c = 12
    body = f"M{ox + c},{oy} H{ox + cw - c} L{ox + cw},{oy + c} V{oy + ch - c} L{ox + cw - c},{oy + ch} H{ox + c} L{ox},{oy + ch - c} V{oy + c} Z"
    s = [f'<path d="{body}" fill="{T["panel"]}" stroke="{T["gold"]}" stroke-width="2"/>',
         f'<rect x="{ox + 6}" y="{oy + 6}" width="{cw - 12}" height="{ch - 12}" rx="5" fill="none" stroke="{T["gold"]}" stroke-width=".8" opacity=".6"/>',
         f'<image href="{img}" x="16" y="16" width="176" height="84" preserveAspectRatio="xMidYMid slice"/>',
         f'<rect x="16" y="16" width="176" height="84" fill="none" stroke="{T["gold"]}" stroke-width="1.6"/>',
         f'<path d="M16,16 h20 l-20,20 Z" fill="{T["gold"]}"/>',
         f'<path d="M192,100 h-20 l20,-20 Z" fill="{T["gold"]}"/>',
         f'<circle cx="104" cy="100" r="13" fill="{T["panel2"]}" stroke="{T["gold"]}" stroke-width="2"/>',
         f'<text x="104" y="104.5" text-anchor="middle" font-family="{SERIF}" font-size="{12 if idx < 4 else 11}" font-weight="700" fill="{T["ink"]}">{ROMAN[idx - 1]}</text>',
         f'<text x="16" y="136" font-family="{SERIF}" font-size="{min(16, 168 / (len(title) * 0.7)):.1f}" font-weight="700" fill="{T["ink"]}">{esc(title)}</text>']
    for i, line in enumerate(textwrap.wrap(desc, 34)[:2]):
        s.append(f'<text x="16" y="{152 + i * 14}" font-family="{SANS}" font-size="10.5" fill="{T["soft"]}">{esc(line)}</text>')
    rows, _ = chips(tags)
    for t, x, y, w in rows:
        s.append(f'<rect x="{x + 2:.1f}" y="{ty + y - 12}" width="{w:.1f}" height="17" rx="3" fill="{T["panel2"]}" stroke="{T["gold"]}" stroke-width="1"/>'
                 f'<text x="{x + 2 + w / 2:.1f}" y="{ty + y}" text-anchor="middle" font-family="{SANS}" font-size="9.5" font-weight="700" fill="{T["ink"]}">{esc(t)}</text>')
    return svg(W, H, "".join(s), f"Project {title}", f"{title}: {desc} Tags: {', '.join(tags)}.", animated=False)


def footer(T, imgs):
    W, H = 900, 290
    defs, bg = base(T, W, H, "f")
    defs += '<clipPath id="fmed"><circle cx="450" cy="178" r="50"/></clipPath>'
    s = [bg, veins(T, 0, 0, W, H - 34, 21, 14, .3)]
    s.append(f'<text x="450" y="54" text-anchor="middle" font-family="{SERIF}" font-size="30" letter-spacing="1" fill="{T["ink"]}">{esc(FOOTER_1)}</text>')
    s.append(f'<text x="450" y="82" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="1" fill="{T["soft"]}">{esc(FOOTER_2)}</text>')
    s.append(vine(T, 40, 372, 178, 9, 100, 5))
    s.append(vine(T, 528, 860, 178, 9, 100, 6))
    s.append(f'<g clip-path="url(#fmed)"><image href="{imgs["medal"]}" x="400" y="128" width="100" height="100" preserveAspectRatio="xMidYMid slice"/></g>')
    s.append(f'<circle cx="450" cy="178" r="50" fill="none" stroke="{T["gold"]}" stroke-width="3.5"/>')
    s.append(f'<circle class="spin a" cx="450" cy="178" r="59" fill="none" stroke="{T["gold"]}" stroke-width="1.4" stroke-dasharray="3 6"/>')
    s.append(f'<circle cx="450" cy="178" r="66" fill="none" stroke="{T["gold"]}" stroke-width=".9" opacity=".7"/>')
    s.append(star(450, 106, 1, T))
    s.append(f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="{T["band"]}"/>')
    s.append(f'<path d="M0,{H - 34} H{W}" stroke="{T["gold"]}" stroke-width="2"/>')
    s.append(f'<text x="50" y="{H - 13}" font-family="{SANS}" font-size="11" fill="#F3EBDD">{esc(ART_CREDIT)}</text>')
    s.append(f'<text x="850" y="{H - 13}" text-anchor="end" font-family="{SANS}" font-size="11.5" font-weight="700" fill="#E8C46A">{esc(SIGNATURE)}</text>')
    return svg(W, H, "".join(s), "Footer", f"{FOOTER_1}. {FOOTER_2}.", defs)


# ----------------------------------- README -----------------------------------
def pic(name, alt, href=None, width="100%"):
    p = (f'<picture>\n<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'<img alt="{html.escape(alt)}" src="assets/{name}-light.svg" width="{width}">\n</picture>')
    return f'<a href="{href}">\n{p}\n</a>' if href else p


def main():
    os.makedirs(ASSETS, exist_ok=True)
    imgs = {"hero": b64_crop(HERO_CROP, (526, 789), 80), "avatar": b64_crop(AVATAR_CROP, (96, 96)),
            "medal": b64_crop(MEDALLION_CROP, (200, 200))}
    thumbs = [b64_crop(p[4], (400, 190)) for p in PROJECTS]
    nrows = max(chips(p[3])[1] for p in PROJECTS)
    for th, T in THEMES.items():
        save("hero", th, hero(T, imgs))
        save("btn-github", th, button(T, "GitHub"))
        save("btn-linkedin", th, button(T, "LinkedIn"))
        save("btn-portfolio", th, button(T, "Portfolio"))
        save("about", th, about(T))
        save("skills", th, skills(T))
        save("projects-title", th, projects_title(T))
        save("footer", th, footer(T, imgs))
        for i, (title, slug, desc, tags, _) in enumerate(PROJECTS):
            save(f"card-{slug}", th, card(T, i + 1, title, desc, tags, thumbs[i], nrows))
    cards = [pic(f"card-{p[1]}", f"{p[0]}: {p[2]}", f"{GITHUB}/{p[1]}", "24%") for p in PROJECTS]
    md = ['<div align="center">', "",
          pic("hero", f"{FULL_NAME}, {ROLE.title()}. A blue dragon beside a woman in a gold-embroidered gown."), "",
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
