#!/usr/bin/env python3
"""
Profile README generator: "Frost & Ink" (three-ink woodblock night: indigo, ice, black).
Embeds subsetted OFL fonts (Cormorant Garamond, Aref Ruqaa, Reem Kufi) straight into each SVG,
so the Arabic calligraphy renders identically everywhere, even inside GitHub's <img> sandbox.

Run:  pip install pillow fonttools brotli  &&  python3 generate_assets.py
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
     ["React", "TS", "Fastify", "PostgreSQL"], (40, 170, 300, 430)),
    ("LeetResume", "leetresume", "AI-powered resume builder and optimizer.",
     ["Next.js", "Prisma", "Postgres"], (140, 230, 340, 430)),
    ("Libora", "libora", "Flutter PDF reader with modern experience.",
     ["Flutter", "Dart", "Riverpod"], (300, 380, 520, 600)),
    ("Webserv", "webserv", "C++98 HTTP server from scratch.",
     ["C++98", "Networking"], (250, 600, 470, 820)),
    ("solaJobs v2", "solajobs-v2", "Arabic-first job board platform.",
     ["Arabic-first", "Jobs"], (0, 660, 240, 900)),
    ("Alert Generator", "prometheus-alert-generator", "AI generator for Prometheus alert rules.",
     ["AI", "Prometheus"], (0, 0, 260, 260)),
    ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose dashboard.",
     ["Docker", "Compose"], (480, 300, 736, 556)),
]
FOOTER_1 = "Build  ·  Explore  ·  Understand"
FOOTER_2 = "Software Engineering · Systems · AI · Mathematics"
# Arabic copy. Have a native speaker confirm before publishing (especially AR_NAME).
AR_NAME = "سليمان المودن"
AR = dict(about="نبذة عني", journey="رحلتي", skills="التقنيات والمهارات", projects="مشاريع مختارة")
AR_FOOTER = ["ابنِ", "اكتشف", "افهم"]          # build, explore, understand (shown right-to-left)
AR_NUMS = "\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668"
ART_CREDIT = "Artwork: source unknown (update this line when you know the artist)"
SIGNATURE = "NashirTech \u00b7 \u0646\u0627\u0634\u0631 \u062a\u0643"
SOURCE = "art/source.jpg"
AVATAR_CROP = (100, 170, 260, 330)
FOOTER_CROP = (0, 709, 736, 1033)
# ================================================================================

FONT_FILES = {   # @font-face family -> woff2 in fonts/
    "FrostSerif": "cormorant-garamond-latin-600-normal.woff2",
    "FrostSerifI": "cormorant-garamond-latin-600-italic.woff2",
    "FrostSerifB": "cormorant-garamond-latin-700-normal.woff2",
    "FrostAr": "aref-ruqaa-arabic-700-normal.woff2",
    "FrostKufi": "reem-kufi-arabic-600-normal.woff2",
}
SERIF = "FrostSerif,'Cormorant Garamond',Georgia,'Times New Roman',serif"
SERIF_I = "FrostSerifI,'Cormorant Garamond',Georgia,'Times New Roman',serif"
SERIF_B = "FrostSerifB,'Cormorant Garamond',Georgia,'Times New Roman',serif"
ARABIC = "FrostAr,'Amiri','Noto Naskh Arabic','Geeza Pro','Segoe UI',Tahoma,serif"
KUFI = "FrostKufi,'Reem Kufi','Noto Kufi Arabic','Segoe UI',Tahoma,sans-serif"
SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"

THEMES = {
    "dark": dict(bg="#050917", bg2="#0B2358", panel="#FFFFFF", panel_op=".055", border="#8FB6FF", border_op=".38",
                 ink="#F3F1EA", soft="#B9C9E8", accent="#9CC0FF", hi="#F5E9B8", snow="#FFFFFF", snow_op=.85,
                 frost="#DCE8FF", btn="#2557C0", btntxt="#FFFFFF", disc="#0A1A45", band="#03060F", stars=True),
    "light": dict(bg="#E8F0FC", bg2="#F6F2E7", panel="#FFFFFF", panel_op=".72", border="#1C4DB0", border_op=".35",
                  ink="#0A1B45", soft="#3E5384", accent="#1C4DB0", hi="#7A5D12", snow="#6F9BE0", snow_op=.8,
                  frost="#4F7FD0", btn="#2557C0", btntxt="#FFFFFF", disc="#FFFFFF", band="#0A1B45", stars=False),
}
NIGHT = dict(ink="#F3F1EA", soft="#C4D3F0", accent="#9CC0FF", hi="#F5E9B8")   # footer is always night

CSS = """
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.r{animation-fill-mode:both}
.fallH,.fallM,.fallF{animation-timing-function:linear;animation-iteration-count:infinite}
.fallH{animation-name:fallH}.fallM{animation-name:fallM}.fallF{animation-name:fallF}
.sway{animation-name:sway}
.twinkle{animation-name:twinkle;animation-duration:3s}
.pulse{transform-box:fill-box;transform-origin:center;animation-name:pulse;animation-duration:5s}
.shimmer{animation-name:shimmer;animation-duration:4.5s}
.ripple{transform-box:fill-box;transform-origin:center;animation-name:ripple;animation-duration:6s;animation-timing-function:ease-out;animation-iteration-count:infinite}
.shine{animation-name:shine;animation-duration:8s;animation-timing-function:ease-in-out;animation-iteration-count:infinite}
.rise{animation-name:rise;animation-duration:1.1s;animation-timing-function:cubic-bezier(.2,.7,.2,1)}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:80s;animation-timing-function:linear;animation-iteration-count:infinite}
.flow{animation-name:flow;animation-duration:7s;animation-timing-function:linear;animation-iteration-count:infinite}
.draw{animation-name:draw;animation-duration:3.2s;animation-timing-function:ease-out}
.branch{transform-box:fill-box;transform-origin:center;animation-name:branch;animation-duration:9s}
.kb{transform-box:fill-box;transform-origin:60% 40%;animation-name:kb;animation-duration:30s}
@keyframes fallH{from{transform:translateY(-30px)}to{transform:translateY(680px)}}
@keyframes fallM{from{transform:translateY(-20px)}to{transform:translateY(470px)}}
@keyframes fallF{from{transform:translateY(-20px)}to{transform:translateY(400px)}}
@keyframes sway{from{transform:translateX(-14px)}to{transform:translateX(14px)}}
@keyframes twinkle{from{opacity:.15}to{opacity:1}}
@keyframes pulse{from{opacity:.55;transform:scale(.9)}to{opacity:1;transform:scale(1.18)}}
@keyframes shimmer{from{opacity:.05;transform:translateX(-10px)}to{opacity:.7;transform:translateX(10px)}}
@keyframes ripple{0%{opacity:.75;transform:scale(.25)}100%{opacity:0;transform:scale(1.9)}}
@keyframes shine{0%{transform:translateX(-300px)}55%,100%{transform:translateX(620px)}}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flow{to{stroke-dashoffset:-60}}
@keyframes draw{from{stroke-dasharray:0 900}to{stroke-dasharray:900 0}}
@keyframes branch{from{transform:rotate(-2.2deg)}to{transform:rotate(2.2deg)}}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.06)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}.fk,.ripple{display:none}}
"""

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
esc = lambda s: html.escape(s, quote=False)

# ------------------------------------ fonts ------------------------------------
_font_cache = {}


def font_b64(family, chars):
    """Subset a bundled woff2 to the glyphs actually used, return a data URI (or None)."""
    key = (family, "".join(sorted(chars)))
    if key in _font_cache:
        return _font_cache[key]
    try:
        from fontTools import subset
        from fontTools.ttLib import TTFont
        path = os.path.join(ROOT, "fonts", FONT_FILES[family])
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.notdef_outline = True
        opts.hinting = False
        opts.name_IDs = [1, 2]
        font = subset.load_font(path, opts)
        cmap = TTFont(path).getBestCmap()
        want = {c for c in chars if ord(c) in cmap}
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(want | {" "})))
        sub.subset(font)
        buf = io.BytesIO()
        subset.save_font(font, buf, opts)
        uri = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:                      # fonts are optional: fall back to system stacks
        print("font embed skipped for", family, "->", e)
        uri = None
    _font_cache[key] = uri
    return uri


def fontface_css(body):
    texts = re.findall(r"<text[^>]*>(.*?)</text>", body, re.S)
    chars = set(html.unescape(re.sub(r"<[^>]+>", "", " ".join(texts))))
    css = []
    for fam in FONT_FILES:
        if fam in body:
            uri = font_b64(fam, chars)
            if uri:
                css.append(f"@font-face{{font-family:'{fam}';src:url({uri}) format('woff2');font-weight:normal;font-style:normal}}")
    return "".join(css)


def b64_crop(box, size, q=80):
    im = Image.open(os.path.join(ROOT, SOURCE)).convert("RGB").crop(box).resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def svg(W, H, body, title, desc, defs="", animated=True):
    css = fontface_css(body) + (CSS if animated else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title><desc>{esc(desc)}</desc><defs>{defs}</defs><style>{css}</style>{body}</svg>')


def save(name, theme, content):
    content = re.sub(r"&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", content)
    with open(os.path.join(ASSETS, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(content)


# ------------------------------- drawing helpers -------------------------------
def wave(x0, x1, y, amp, wl, ph=0.0, step=6):
    pts, x = [], x0
    while x <= x1:
        pts.append(f"{x:.1f},{y + amp * math.sin((x - x0) / wl * 2 * math.pi + ph):.1f}")
        x += step
    return "M" + " L".join(pts)


def snow(T, W, n, seed, kf="fallH", rmax=3.2, op=None, clip=None):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x = r.uniform(0, W)
        rad = r.uniform(1.0, rmax)
        dur = r.uniform(10, 20) * (1.3 - rad / 6)
        dl = r.uniform(0, 20)
        sw = r.uniform(4, 8)
        o = (op or T["snow_op"]) * r.uniform(.5, 1)
        out.append(f'<g class="fk" transform="translate({x:.0f},0)"><g class="{kf} r" style="animation-duration:{dur:.1f}s;animation-delay:-{dl:.1f}s">'
                   f'<g class="sway a" style="animation-duration:{sw:.1f}s;animation-delay:-{dl / 3:.1f}s">'
                   f'<circle r="{rad:.1f}" fill="{T["snow"]}" opacity="{o:.2f}"/></g></g></g>')
    g = "".join(out)
    return f'<g clip-path="url(#{clip})">{g}</g>' if clip else g


def flake_path(r):
    d = []
    for k in range(6):
        a = k * math.pi / 3
        ca, sa = math.cos(a), math.sin(a)
        d.append(f"M0,0 L{r * ca:.1f},{r * sa:.1f}")
        for f, ln in ((.5, .3), (.78, .22)):
            bx, by = r * f * ca, r * f * sa
            for s in (-1, 1):
                b = a + s * math.pi / 3
                d.append(f"M{bx:.1f},{by:.1f} L{bx + r * ln * math.cos(b):.1f},{by + r * ln * math.sin(b):.1f}")
    return " ".join(d)


def frost_branch(T, ox, oy, ang, L, seed, depth=4, w=2.4, sway=True):
    """Frosted twig with blossom dots at the tips, like the trees in the art."""
    r = random.Random(seed)
    segs, dots = [], []

    def grow(x, y, a, L, d, w):
        a2 = a + r.uniform(-.3, .3)
        x2, y2 = x + L * math.cos(a2), y + L * math.sin(a2)
        segs.append(f'<path d="M{x:.0f},{y:.0f} L{x2:.0f},{y2:.0f}" stroke-width="{max(w, .7):.1f}"/>')
        if d == 0 or r.random() < .15:
            dots.append(f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="{r.uniform(1.6, 3.2):.1f}"/>')
        if d > 0:
            grow(x2, y2, a2 + r.uniform(.3, .7), L * .74, d - 1, w * .66)
            if r.random() < .85:
                grow(x2, y2, a2 - r.uniform(.3, .7), L * .7, d - 1, w * .62)

    grow(0, 0, ang, L, depth, w)
    guard = f'<circle r="{L * 2.4:.0f}" fill="none" stroke="none"/>'
    inner = (f'{guard}<g fill="none" stroke="{T["frost"]}" stroke-linecap="round" opacity=".7">{"".join(segs)}</g>'
             f'<g fill="{T["frost"]}" opacity=".85">{"".join(dots)}</g>')
    if sway:
        inner = f'<g class="branch a" style="animation-delay:-{seed % 7}s">{inner}</g>'
    return f'<g transform="translate({ox},{oy})">{inner}</g>'


def snowflake(T, cx, cy, r, color, spin_delay=None, w=1.6):
    path = f'<path d="{flake_path(r)}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
    tips = "".join(f'<circle cx="{r * math.cos(k * math.pi / 3):.1f}" cy="{r * math.sin(k * math.pi / 3):.1f}" r="2.4" fill="{color}"/>' for k in range(6))
    inner = f'<circle r="{r + 3:.0f}" fill="none" stroke="none"/>{path}{tips}'
    if spin_delay is not None:
        inner = f'<g class="spin" style="animation-delay:-{spin_delay}s;animation-direction:{"reverse" if int(spin_delay) % 2 else "normal"}">{inner}</g>'
    return f'<g transform="translate({cx:.1f},{cy:.1f})">{inner}</g>'


def moon_icon(T, cx, cy, r=10):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{T["hi"]}"/>'
            f'<circle cx="{cx - r * .3}" cy="{cy - r * .2}" r="{r * .22}" fill="{T["bg"]}" opacity=".25"/>'
            f'<circle cx="{cx + r * .3}" cy="{cy + r * .35}" r="{r * .15}" fill="{T["bg"]}" opacity=".25"/>')


def base(T, W, H, sid="s"):
    defs = (f'<linearGradient id="{sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/>'
            f'<stop offset="1" stop-color="{T["bg2"]}"/></linearGradient>')
    return defs, f'<rect width="{W}" height="{H}" fill="url(#{sid}g)"/>'


def panel(T, x, y, w, h, pid):
    defs = f'<clipPath id="{pid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26"/></clipPath>'
    body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="{T["panel"]}" fill-opacity="{T["panel_op"]}" '
            f'stroke="{T["border"]}" stroke-opacity="{T["border_op"]}" stroke-width="1.4"/>'
            f'<path d="M{x + 30},{y + 1} H{x + w - 30}" stroke="{T["ink"]}" stroke-opacity=".35" stroke-width="1.2"/>')
    return defs, body


def heading(x, y, text, ar, ar_right, T, size=36):
    return (moon_icon(T, x + 12, y - 12, 11) +
            f'<text x="{x + 34}" y="{y}" font-family="{SERIF_B}" font-size="{size}" fill="{T["ink"]}">{esc(text)}</text>'
            f'<text x="{ar_right}" y="{y - 1}" text-anchor="end" font-family="{KUFI}" font-size="25" fill="{T["accent"]}">{ar}</text>')


# ----------------------------------- panels -----------------------------------
def hero(T, imgs):
    W, H = 900, 640
    s_ = H / 1033
    aw = 736 * s_
    ax = W - aw
    defs, bg = base(T, W, H, "h")
    mx = ax + aw * .55
    defs += (f'<linearGradient id="hfL" gradientUnits="userSpaceOnUse" x1="{ax:.0f}" y1="0" x2="{mx:.0f}" y2="0">'
             f'<stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>'
             f'<linearGradient id="hfB" gradientUnits="userSpaceOnUse" x1="0" y1="{H * .78:.0f}" x2="0" y2="{H}">'
             f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
             f'<mask id="hmL"><rect width="{W}" height="{H}" fill="url(#hfL)"/></mask>'
             f'<mask id="hmB"><rect width="{W}" height="{H}" fill="url(#hfB)"/></mask>'
             f'<radialGradient id="hmoon"><stop offset="0" stop-color="{T["hi"]}" stop-opacity=".95"/>'
             f'<stop offset=".35" stop-color="{T["hi"]}" stop-opacity=".35"/><stop offset="1" stop-color="{T["hi"]}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="hshine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
             f'<stop offset=".5" stop-color="{T["hi"] if T["stars"] else "#FFFFFF"}" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="hav"><circle cx="64" cy="38" r="15"/></clipPath>'
             f'<clipPath id="hname"><text x="50" y="214" font-family="{SERIF}" font-size="88">{esc(NAME_1)}</text>'
             f'<text x="50" y="296" font-family="{SERIF}" font-size="88">{esc(NAME_2)}</text></clipPath>')
    s = [bg]
    if T["stars"]:
        rr = random.Random(5)
        for i in range(22):
            s.append(f'<circle class="twinkle a" style="animation-delay:-{rr.uniform(0, 3):.1f}s;animation-duration:{rr.uniform(2, 5):.1f}s" '
                     f'cx="{rr.uniform(20, 430):.0f}" cy="{rr.uniform(10, 600):.0f}" r="{rr.uniform(.7, 1.6):.1f}" fill="#fff"/>')
    # art, dissolving into the page
    mw = round(moon_x := ax + 239 * s_)
    my = round(324 * s_)
    s.append(f'<g mask="url(#hmL)"><g mask="url(#hmB)"><g><image class="kb a" href="{imgs["hero"]}" x="{ax:.1f}" y="0" width="{aw:.1f}" height="{H}"/>'
             f'<circle class="pulse a" cx="{mw}" cy="{my}" r="40" fill="url(#hmoon)"/>'
             + "".join(f'<path class="shimmer a" style="animation-delay:-{i * .7:.1f}s;animation-duration:{3.5 + i * .4:.1f}s" '
                       f'd="M{ax + 40 + i * 52:.0f},{400 + (i % 4) * 26} q22,-5 46,0" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round"/>' for i in range(8)) +
             f'</g></g></g>')
    s.append(snow(T, W, 38, 11, "fallH"))
    # top bar
    s.append(f'<g class="rise r" style="animation-delay:.05s"><image href="{imgs["avatar"]}" x="49" y="23" width="30" height="30" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>'
             f'<circle cx="64" cy="38" r="15" fill="none" stroke="{T["accent"]}" stroke-width="1.6"/>'
             f'<text x="88" y="43" font-family="{MONO}" font-size="12.5" fill="{T["soft"]}">{esc(HANDLE)} / README</text></g>')
    s.append(f'<g class="rise r" style="animation-delay:.2s"><text x="52" y="132" font-family="{SERIF_I}" font-size="30" fill="{T["soft"]}">Hi, I\'m</text></g>')
    s.append(f'<g class="rise r" style="animation-delay:.35s"><text x="50" y="214" font-family="{SERIF}" font-size="88" fill="{T["ink"]}">{esc(NAME_1)}</text>'
             f'<text x="50" y="296" font-family="{SERIF}" font-size="88" fill="{T["ink"]}">{esc(NAME_2)}</text></g>')
    s.append(f'<g clip-path="url(#hname)"><g class="shine"><rect x="-80" y="130" width="170" height="190" fill="url(#hshine)" transform="skewX(-18)" opacity=".85"/></g></g>')
    s.append(f'<g class="rise r" style="animation-delay:.6s"><text x="54" y="358" font-family="{ARABIC}" font-size="46" fill="{T["hi"]}">{AR_NAME}</text></g>')
    s.append(f'<g class="rise r" style="animation-delay:.8s"><text x="54" y="408" font-family="{SERIF_B}" font-size="19" letter-spacing="7" fill="{T["accent"]}">{esc(ROLE)}</text>'
             f'<path d="M54,424 H300" stroke="{T["accent"]}" stroke-opacity=".5" stroke-width="1"/></g>')
    sep = "\u00a0\u00a0|\u00a0\u00a0"
    s.append(f'<g class="rise r" style="animation-delay:1s"><text x="54" y="458" font-family="{SERIF_I}" font-size="30" fill="{T["ink"]}">{esc(sep.join(PILLARS))}</text></g>')
    for i, line in enumerate(TAGLINE):
        s.append(f'<g class="rise r" style="animation-delay:{1.15 + i * .15:.2f}s"><text x="54" y="{506 + i * 28}" font-family="{SERIF}" font-size="21" fill="{T["soft"]}">{esc(line)}</text></g>')
    return svg(W, H, "".join(s), f"{FULL_NAME}: {ROLE.title()}",
               "Profile header over a snowy night scene: a white-and-blue castle by a moonlit lake. Name in Latin and Arabic script.", defs)


def button(T, label):
    body = (f'<rect x="3" y="3" width="144" height="34" rx="17" fill="{T["btn"]}" stroke="{T["accent"]}" stroke-width="1.4"/>'
            + snowflake(T, 28, 20, 9, T["btntxt"], w=1.4) +
            f'<text x="91" y="26" text-anchor="middle" font-family="{SERIF_B}" font-size="19" letter-spacing=".6" fill="{T["btntxt"]}">{esc(label)}</text>')
    return svg(150, 40, body, label, f"Button linking to {label}", animated=False)


def about(T):
    W, H = 900, 450
    defs, bg = base(T, W, H, "a")
    pd, pb = panel(T, 16, 14, 868, 422, "apc")
    defs += pd
    s = [bg, pb, snow(T, W, 14, 21, "fallM", 2.4, .6, "apc"), frost_branch(T, 884, 14, 2.45, 24, 3, 3, 2.0),
         frost_branch(T, 16, 436, -.7, 22, 9, 3, 1.8)]
    s.append(heading(54, 90, "About", AR["about"], 468, T))
    s.append(heading(520, 90, "My journey", AR["journey"], 846, T))
    lines = textwrap.wrap(ABOUT, 47)
    for i, line in enumerate(lines):
        s.append(f'<text x="56" y="{140 + i * 28}" font-family="{SERIF}" font-size="20" fill="{T["ink"]}">{esc(line)}</text>')
    y = 140 + 28 * len(lines) + 22
    for line in textwrap.wrap(FACTS, 58):
        s.append(f'<text x="56" y="{y}" font-family="{SANS}" font-size="12" fill="{T["soft"]}">{esc(line)}</text>')
        y += 18
    s.append(f'<text x="56" y="{y + 10}" font-family="{SANS}" font-size="12.5" font-weight="700" fill="{T["accent"]}">{esc(FOCUS)}</text>')
    s.append(f'<path d="M494,70 L492,390" stroke="{T["accent"]}" stroke-opacity=".55" stroke-width="1.2"/>')
    for yy in (140, 230, 320):
        s.append(snowflake(T, 493, yy, 7, T["accent"], w=1.2))
    for i, (lang, area) in enumerate(JOURNEY):
        yy = 150 + i * 54
        x1 = 520 + len(lang) * 11.5 + 14
        x2 = 846 - len(area) * 7.6 - 32
        s.append(f'<text x="520" y="{yy}" font-family="{SERIF_B}" font-size="25" fill="{T["ink"]}">{esc(lang)}</text>')
        s.append(f'<line class="flow" x1="{x1:.0f}" y1="{yy - 6}" x2="{x2:.0f}" y2="{yy - 6}" stroke="{T["accent"]}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="1 9"/>')
        s.append(f'<circle cx="{round(x2 + 12)}" cy="{yy - 6}" r="3" fill="{T["hi"]}"/>')
        s.append(f'<text x="846" y="{yy}" text-anchor="end" font-family="{SANS}" font-size="13.5" font-weight="700" fill="{T["accent"]}">{esc(area)}</text>')
    return svg(W, H, "".join(s), "About and journey",
               "About text on the left; on the right the journey: " + ", ".join(f"{a} to {b}" for a, b in JOURNEY) + ".", defs)


def skills(T):
    W, H = 900, 478
    defs, bg = base(T, W, H, "k")
    pd, pb = panel(T, 16, 14, 868, 450, "kpc")
    defs += pd
    s = [bg, pb, snow(T, W, 16, 33, "fallM", 2.4, .55, "kpc"), frost_branch(T, 16, 14, .7, 24, 5, 3, 2.0),
         frost_branch(T, 884, 464, -2.4, 24, 12, 3, 2.0), heading(54, 90, "Technologies & Skills", AR["skills"], 846, T)]
    cell = 800 / 6
    cols = [T["accent"], T["frost"], T["hi"]]
    for i, (lab, mono) in enumerate(SKILLS):
        cx = 50 + cell * (i % 6 + .5)
        cy = 196 + (i // 6) * 140
        s.append(snowflake(T, cx, cy, 46, cols[i % 3], spin_delay=i * 7 + 1))
        s.append(f'<circle cx="{cx:.1f}" cy="{cy}" r="23" fill="{T["disc"]}" stroke="{cols[i % 3]}" stroke-width="1.6"/>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 6}" text-anchor="middle" font-family="{SERIF_B}" font-size="20" fill="{T["ink"]}">{esc(mono)}</text>')
        s.append(f'<text x="{cx:.1f}" y="{cy + 70}" text-anchor="middle" font-family="{SANS}" font-size="12" font-weight="700" fill="{T["ink"]}">{esc(lab)}</text>')
    return svg(W, H, "".join(s), "Technologies and skills",
               "Twelve snowflake medallions: " + ", ".join(l for l, _ in SKILLS) + ".", defs)


def projects_title(T):
    W, H = 900, 110
    defs, bg = base(T, W, H, "p")
    s = [bg, heading(54, 70, "Selected projects", "", 0, T, 40)]
    s.append(f'<text x="846" y="68" text-anchor="end" font-family="{KUFI}" font-size="27" fill="{T["accent"]}">{AR["projects"]}</text>')
    s.append(f'<path class="draw r" d="{wave(380, 640, 82, 4, 80)}" fill="none" stroke="{T["accent"]}" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>')
    s.append(snowflake(T, 660, 82, 8, T["hi"], spin_delay=3, w=1.3))
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


def lancet(x0, x1, ys, y1):
    W = x1 - x0
    cx = (x0 + x1) / 2
    y0 = ys - .866 * W
    return f"M{x0},{y1} V{ys} A{W},{W} 0 0 1 {cx},{y0:.1f} A{W},{W} 0 0 1 {x1},{ys} V{y1} Z"


def card(T, idx, title, desc, tags, img):
    W, H = 208, 316
    defs = (f'<clipPath id="cc{idx}"><rect x="6" y="6" width="196" height="304" rx="24"/></clipPath>'
            f'<clipPath id="cw{idx}"><path d="{lancet(36, 172, 146, 196)}"/></clipPath>')
    g = [f'<rect x="6" y="6" width="196" height="304" rx="24" fill="{T["panel"]}" fill-opacity="{T["panel_op"]}" stroke="{T["border"]}" stroke-opacity="{T["border_op"]}" stroke-width="1.4"/>',
         snow(T, W, 6, idx * 13, "fallM", 2.0, .6, f"cc{idx}"),
         f'<path d="{lancet(30, 178, 146, 202)}" fill="none" stroke="{T["accent"]}" stroke-opacity=".6" stroke-width="1.2"/>',
         f'<g clip-path="url(#cw{idx})"><image href="{img}" x="36" y="24" width="136" height="172" preserveAspectRatio="xMidYMid slice"/></g>',
         f'<path d="{lancet(36, 172, 146, 196)}" fill="none" stroke="{T["ink"]}" stroke-opacity=".8" stroke-width="1.4"/>',
         f'<circle cx="104" cy="198" r="16" fill="{T["disc"]}" stroke="{T["accent"]}" stroke-width="1.6"/>',
         f'<text x="104" y="205" text-anchor="middle" font-family="{ARABIC}" font-size="21" fill="{T["hi"]}">{AR_NUMS[idx - 1]}</text>',
         f'<text x="104" y="242" text-anchor="middle" font-family="{SERIF_B}" font-size="{min(24, 180 / (len(title) * .5)):.1f}" fill="{T["ink"]}">{esc(title)}</text>']
    for i, line in enumerate(textwrap.wrap(desc, 34)[:2]):
        g.append(f'<text x="104" y="{260 + i * 14}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{T["soft"]}">{esc(line)}</text>')
    for i, line in enumerate(tag_lines(tags)):
        g.append(f'<text x="104" y="{291 + i * 14}" text-anchor="middle" font-family="{SANS}" font-size="10.5" font-weight="700" fill="{T["accent"]}">{esc(line)}</text>')
    return svg(W, H, "".join(g), f"Project {title}", f"{title}: {desc} Tags: {', '.join(tags)}.", defs)


def footer(T, imgs):
    N = NIGHT
    W, H = 900, 430
    T2 = dict(T, **N, snow="#FFFFFF", snow_op=.85, frost="#DCE8FF")
    defs = (f'<linearGradient id="ftop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg"]}"/><stop offset=".5" stop-color="{T["bg"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fdim" x1="0" y1="0" x2="0" y2="1"><stop offset=".25" stop-color="#050917" stop-opacity="0"/>'
            f'<stop offset=".55" stop-color="#050917" stop-opacity=".8"/><stop offset="1" stop-color="#050917" stop-opacity=".85"/></linearGradient>'
            f'<radialGradient id="fmoon"><stop offset="0" stop-color="#F5E9B8" stop-opacity=".9"/><stop offset="1" stop-color="#F5E9B8" stop-opacity="0"/></radialGradient>')
    ih = 900 / 736 * (FOOTER_CROP[3] - FOOTER_CROP[1])
    s = [f'<rect width="{W}" height="{H}" fill="{T["bg"]}"/>',
         f'<image href="{imgs["footer"]}" x="0" y="{H - 34 - ih:.0f}" width="{W}" height="{ih:.0f}" preserveAspectRatio="xMidYMid slice"/>',
         f'<rect width="{W}" height="{H - 34}" fill="url(#fdim)"/>',
         f'<rect width="{W}" height="{H - 34}" fill="url(#ftop)"/>']
    for i in range(4):
        s.append(f'<ellipse class="ripple" style="animation-delay:-{i * 1.5}s" cx="450" cy="360" rx="330" ry="28" fill="none" stroke="#DCE8FF" stroke-width="1.4"/>')
    s.append(snow(T2, W, 26, 41, "fallF"))
    s.append(f'<text x="450" y="178" text-anchor="middle" font-family="{SERIF_I}" font-size="50" fill="{N["ink"]}">{esc(FOOTER_1)}</text>')
    for word, x in zip(AR_FOOTER, (570, 450, 330)):
        s.append(f'<text x="{x}" y="244" text-anchor="middle" font-family="{ARABIC}" font-size="44" fill="{N["hi"]}">{word}</text>')
    for x in (390, 510):
        s.append(snowflake(T2, x, 232, 9, N["accent"], spin_delay=x % 11, w=1.3))
    s.append(f'<text x="450" y="296" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="1.2" fill="{N["soft"]}">{esc(FOOTER_2)}</text>')
    s.append(f'<rect x="0" y="{H - 34}" width="{W}" height="34" fill="{T["band"]}"/>')
    s.append(f'<path d="M0,{H - 34} H{W}" stroke="#9CC0FF" stroke-opacity=".6" stroke-width="1.4"/>')
    s.append(f'<text x="30" y="{H - 13}" font-family="{SANS}" font-size="10.5" fill="#F3F1EA">{esc(ART_CREDIT)}</text>')
    s.append(f'<text x="870" y="{H - 13}" text-anchor="end" font-family="{SANS}" font-size="11.5" font-weight="700" fill="#F5E9B8">{esc(SIGNATURE)}</text>')
    return svg(W, H, "".join(s), "Footer", f"{FOOTER_2}. Snowfall over a moonlit lake.", defs)


# ----------------------------------- README -----------------------------------
def pic(name, alt, href=None, width="100%"):
    p = (f'<picture>\n<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'<img alt="{html.escape(alt)}" src="assets/{name}-light.svg" width="{width}">\n</picture>')
    return f'<a href="{href}">\n{p}\n</a>' if href else p


def main():
    os.makedirs(ASSETS, exist_ok=True)
    thumbs = [b64_crop(p[4], (240, 240)) for p in PROJECTS]
    imgs = {"hero": b64_crop((0, 0, 736, 1033), (520, 730), 80), "avatar": b64_crop(AVATAR_CROP, (96, 96)),
            "footer": b64_crop(FOOTER_CROP, (900, round(900 / 736 * (FOOTER_CROP[3] - FOOTER_CROP[1]))), 78)}
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
            save(f"card-{slug}", th, card(T, i + 1, title, desc, tags, thumbs[i]))
    cards = [pic(f"card-{p[1]}", f"{p[0]}: {p[2]}", f"{GITHUB}/{p[1]}", "24%") for p in PROJECTS]
    md = ['<div align="center">', "",
          pic("hero", f"{FULL_NAME}, {ROLE.title()}. A white-and-blue castle by a moonlit lake under falling snow."), "",
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
