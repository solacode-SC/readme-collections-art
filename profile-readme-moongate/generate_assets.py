#!/usr/bin/env python3
"""Moon-gate / night-garden magic edition.  Needs: pip install pillow
Image  -> hero 'portal' (circular crop) + micro arch thumbnails for project cards.
Magic  -> rotating rune rings & octagram, pulsing lantern light, twinkling constellations,
          rising fireflies, drifting blossom petals, frosted-canopy footer (procedural)."""
import io, base64, math, os, random, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
ART = Image.open(os.path.join(HERE, "art", "source.jpg"))
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"

THEMES = {
 "dark":  dict(bg1="#070d3a", bg2="#0c1a66", fg="#eef0ff", mute="#9fb0ee", acc="#f5c15a", acc2="#ff7a52",
               line="#2a3da6", card="#0b1560", star="#ffffff", petals=["#ffffff", "#e9c6e0", "#bcc8ff"],
               canopy=["#e8eaff", "#c9d2ff", "#9fb0f0", "#f3d3ea", "#ffffff"], coral="#ff7a52", ground="#0a1352"),
 "light": dict(bg1="#f4f5ff", bg2="#dfe5ff", fg="#0f1a66", mute="#4b5ca9", acc="#d6502b", acc2="#1f3fd1",
               line="#b4c1f2", card="#ffffff", star="#1f3fd1", petals=["#eaa8c9", "#9fb0f0", "#f4b49a"],
               canopy=["#ffffff", "#d3dcff", "#aebdf5", "#f1c9e2", "#8ea4ec"], coral="#e8603a", ground="#cfd8fb"),
}

# ---------- your content: edit here ----------
NAME = "Solayman El Mouden"
GITHUB = "https://github.com/solacode-SC"
LINKEDIN = "https://www.linkedin.com/in/YOUR-LINKEDIN"   # <- change me
PORTFOLIO = "https://solaymantech.me"
JOURNEY = [("C / C++", "Systems"), ("Python", "Backend & AI"), ("TypeScript", "Web & Tools"),
           ("Docker", "Infrastructure"), ("Linux", "DevOps")]
SKILLS = [("C/C++", "C++"), ("Python", "Py"), ("JavaScript", "JS"), ("TypeScript", "TS"), ("React", "Rx"),
          ("Next.js", "N"), ("Django", "dj"), ("FastAPI", "FA"), ("PostgreSQL", "Pg"), ("Docker", "Dk"),
          ("Linux", "Lx"), ("Git", "Git")]
# (title, slug, line1, line2, tags, micro-crop box in source.jpg  [~200x94])
PROJECTS = [
 ("LazyEquation", "lazyequation", "Interactive math & physics", "visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"], (400, 60, 600, 154)),
 ("LeetResume", "leetresume", "AI-powered resume", "builder and optimizer.", ["Next.js", "Prisma", "Postgres"], (100, 300, 300, 394)),
 ("Libora", "libora", "Flutter PDF reader with", "modern experience.", ["Flutter", "Dart", "Riverpod"], (100, 800, 300, 894)),
 ("Webserv", "webserv", "C++98 HTTP server", "from scratch.", ["C++98", "Networking"], (230, 770, 430, 864)),
 ("solaJobs v2", "solajobs-v2", "Arabic-first job board", "platform.", ["Arabic-first", "Jobs"], (380, 290, 580, 384)),
 ("Alert Generator", "prometheus-alert-generator", "AI generator for", "Prometheus alert rules.", ["AI", "Prometheus"], (440, 690, 640, 784)),
 ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose", "dashboard.", ["Docker", "Compose"], (150, 480, 350, 574)),
]
# ---------------------------------------------

def crop64(box, size, q=82):
    im = ART.crop(box).resize(size, Image.LANCZOS); buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

STYLE = '''<style>
.spin{transform-box:fill-box;transform-origin:center;animation:spin 90s linear infinite}
.spin.r{animation-direction:reverse;animation-duration:140s}
.spin.f{animation-duration:46s}
@keyframes spin{to{transform:rotate(360deg)}}
.tw{transform-box:fill-box;transform-origin:center;animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25;transform:scale(.6)}50%{opacity:1;transform:scale(1.15)}}
.glow{animation:glow 5s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.45}50%{opacity:1}}
.flick{animation:fl 2.8s ease-in-out infinite}
@keyframes fl{0%,100%{opacity:.7}30%{opacity:1}55%{opacity:.55}80%{opacity:.95}}
.ff{animation:ff linear infinite;opacity:0}
@keyframes ff{0%{opacity:0;transform:translate(0,0)}15%{opacity:1}85%{opacity:.9}100%{opacity:0;transform:translate(16px,-80px)}}
.fall{animation:fall linear infinite}
@keyframes fall{from{transform:translateY(-30px)}to{transform:translateY(520px)}}
.sway{transform-box:fill-box;transform-origin:center;animation:sway ease-in-out infinite alternate}
@keyframes sway{from{transform:translateX(-22px) rotate(-40deg)}to{transform:translateX(22px) rotate(40deg)}}
.breathe{transform-box:fill-box;transform-origin:center;animation:br 30s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1)}to{transform:scale(1.08)}}
.dots{stroke-dasharray:.1 16;stroke-linecap:round;animation:run 12s linear infinite}
@keyframes run{to{stroke-dashoffset:-161}}
.cursor{animation:cur 1.1s steps(1) infinite}
@keyframes cur{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.spin,.tw,.glow,.flick,.ff,.fall,.sway,.breathe,.dots,.cursor{animation:none}.ff{opacity:.6}}
</style>'''

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")
def star4(x, y, s, col, op=1, cls="", delay=0):
    d = f"M{f1(x)} {f1(y-s)}Q{f1(x)} {f1(y)} {f1(x+s)} {f1(y)}Q{f1(x)} {f1(y)} {f1(x)} {f1(y+s)}Q{f1(x)} {f1(y)} {f1(x-s)} {f1(y)}Q{f1(x)} {f1(y)} {f1(x)} {f1(y-s)}Z"
    st = f' style="animation-delay:{-delay:.1f}s;animation-duration:{3+delay%3:.1f}s"' if cls else ""
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}"{st}/>'

PETAL = "M0 -8C6 -6 7 4 0 9C-7 4 -6 -6 0 -8Z"
def petals(c, n, xr, seed=3):
    r = random.Random(seed); o = []
    for _ in range(n):
        x = r.uniform(*xr); s = r.uniform(.6, 1.2); col = r.choice(c["petals"])
        d = r.uniform(16, 28); sd = r.uniform(3.5, 6.5)
        o.append(f'<g transform="translate({f1(x)} 0)"><g class="fall" style="animation-duration:{d:.1f}s;animation-delay:{-r.uniform(0,d):.1f}s">'
                 f'<g class="sway" style="animation-duration:{sd:.1f}s;animation-delay:{-r.uniform(0,sd):.1f}s">'
                 f'<path transform="rotate({r.uniform(0,180):.0f}) scale({s:.2f})" d="{PETAL}" fill="{col}" opacity=".92"/></g></g></g>')
    return "".join(o)

def fireflies(c, n, box, seed=5):
    r = random.Random(seed); x0, y0, x1, y1 = box; o = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1); d = r.uniform(7, 14)
        o.append(f'<g class="ff" style="animation-duration:{d:.1f}s;animation-delay:{-r.uniform(0,d):.1f}s">'
                 f'<circle cx="{f1(x)}" cy="{f1(y)}" r="5" fill="#ffd57a" opacity=".25"/><circle cx="{f1(x)}" cy="{f1(y)}" r="1.9" fill="#fff0b8"/></g>')
    return "".join(o)

def rune_ring(c, r, n=24, col=None):
    col = col or c["acc"]; o = [f'<circle r="{r}" fill="none" stroke="{col}" stroke-width=".9" opacity=".7"/>']
    for i in range(n):
        a = 2 * math.pi * i / n; x, y = r * math.cos(a), r * math.sin(a); k = i % 4; deg = math.degrees(a)
        if k == 0: o.append(f'<circle cx="{f1(x)}" cy="{f1(y)}" r="2.3" fill="none" stroke="{col}"/>')
        elif k == 1: o.append(f'<path transform="translate({f1(x)} {f1(y)}) rotate({f1(deg)})" d="M-3 0L0 -3.4L3 0L0 3.4Z" fill="{col}"/>')
        elif k == 2: o.append(f'<path transform="translate({f1(x)} {f1(y)}) rotate({f1(deg+90)})" d="M0 -4L3.4 3L-3.4 3Z" fill="none" stroke="{col}"/>')
        else: o.append(f'<path transform="translate({f1(x)} {f1(y)}) rotate({f1(deg)})" d="M-4 0H4M0 -2.5V2.5" stroke="{col}"/>')
    return "".join(o)

def octagram(R, col):
    p = [(R * math.cos(2 * math.pi * i / 8 - math.pi / 2), R * math.sin(2 * math.pi * i / 8 - math.pi / 2)) for i in range(8)]
    order = [0, 3, 6, 1, 4, 7, 2, 5]
    return f'<path d="M{"L".join(f"{f1(p[i][0])} {f1(p[i][1])}" for i in order)}Z" fill="none" stroke="{col}" stroke-width=".9" opacity=".6"/>'

def defs(c):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".4" stop-color="#ffb347" stop-opacity=".4"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="aura"><stop offset=".55" stop-color="{c['acc2']}" stop-opacity="0"/><stop offset=".8" stop-color="{c['acc2']}" stop-opacity=".22"/><stop offset="1" stop-color="{c['acc2']}" stop-opacity="0"/></radialGradient>
<linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="{c['fg']}"/><stop offset="1" stop-color="{c['acc'] if c is THEMES['dark'] else c['acc2']}"/></linearGradient>
</defs>'''

def wrap(w, h, c, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{MONO}">'
            f'{STYLE}{defs(c)}<rect width="{w}" height="{h}" fill="url(#bg)"/>{body}'
            f'<path d="M.5 0V{h}M{w-.5} 0V{h}" stroke="{c["line"]}"/></svg>')

def sky(c, w, h, n, seed, avoid=None):
    r = random.Random(seed); o = []
    for i in range(n):
        x, y = r.uniform(10, w - 10), r.uniform(8, h - 8)
        if avoid and avoid(x, y): continue
        o.append(star4(x, y, r.uniform(1.8, 4.2), c["star"], r.uniform(.5, .95), "tw", r.uniform(0, 6)))
    return "".join(o)

def divider(c, y, w=900, seed=1):
    r = random.Random(seed); pts = []
    for x in range(70, w - 60, 95): pts.append((x + r.uniform(-12, 12), y + r.uniform(-9, 9)))
    d = "M" + "L".join(f"{f1(a)} {f1(b)}" for a, b in pts)
    o = [f'<path d="{d}" fill="none" stroke="{c["line"]}" stroke-width="1.2"/><path class="dots" d="{d}" fill="none" stroke="{c["acc"]}" stroke-width="2.2"/>']
    for i, (a, b) in enumerate(pts): o.append(star4(a, b, 4.5 if i % 3 == 0 else 3, c["acc"] if i % 3 == 0 else c["star"], .95, "tw", i * 1.3))
    return "".join(o)

def heading(c, y, idx, label, x=60):
    return (star4(x, y, 8, c["acc"], 1, "tw", 1) +
            f'<text x="{x+22}" y="{y+4}" font-size="12" letter-spacing="2" fill="{c["mute"]}">{idx} /</text>'
            f'<text x="{x+62}" y="{y+4}" font-size="12" font-weight="700" letter-spacing="2" fill="{c["fg"]}">{label}</text>')

# ---------- panels ----------
def hero(c):
    cx, cy, R = 680, 235, 170
    img = crop64((60, 600, 500, 1040), (620, 620), 82)
    lx, ly = cx - R + (303 - 60) * (2 * R / 440), cy - R + (818 - 600) * (2 * R / 440)
    avoid = lambda x, y: x < 440 and 90 < y < 330
    b = sky(c, 900, 470, 70, 2, avoid)
    # constellation (top-left / top-right)
    cons = [(300, 40), (352, 66), (410, 48), (452, 92), (402, 118)]
    b += f'<path d="M{"L".join(f"{x} {y}" for x,y in cons)}" fill="none" stroke="{c["mute"]}" stroke-opacity=".5" stroke-dasharray="3 5"/>'
    b += "".join(star4(x, y, 4.5, c["acc"], 1, "tw", i * 1.1) for i, (x, y) in enumerate(cons))
    b += f'<circle cx="{cx}" cy="{cy}" r="{R+60}" fill="url(#aura)" class="glow"/>'
    b += (f'<g transform="translate({cx} {cy})"><g class="spin r">{octagram(R+26, c["acc"])}</g>'
          f'<g class="spin">{rune_ring(c, R+36, 28)}</g><g class="spin f">{rune_ring(c, R+14, 20, c["acc2"])}</g>'
          f'<g class="spin f"><circle cx="{R+36}" cy="0" r="3.4" fill="#ffd57a"/><circle cx="-{R+36}" cy="0" r="3.4" fill="#ffd57a"/></g></g>')
    b += (f'<defs><clipPath id="moon"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>'
          f'<g clip-path="url(#moon)"><g class="breathe"><image x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" href="{img}" xlink:href="{img}"/></g>'
          f'<circle class="flick" cx="{f1(lx)}" cy="{f1(ly)}" r="62" fill="url(#warm)"/></g>'
          f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c["acc"]}" stroke-width="2"/>'
          f'<circle cx="{cx}" cy="{cy}" r="{R+6}" fill="none" stroke="{c["acc"]}" stroke-opacity=".4" stroke-dasharray="1 5"/>')
    # top bar + copy
    b += (star4(66, 34, 8, c["acc"], 1, "tw", .5) +
          f'<text x="84" y="38" font-size="12" fill="{c["mute"]}">solacode-SC <tspan fill="{c["line"]}">/</tspan> README</text>'
          f'<path d="M40 56H420" stroke="{c["line"]}"/>'
          f'<text x="60" y="122" font-size="13" letter-spacing="3" fill="{c["mute"]}">HI, I\'M</text>'
          f'<text x="58" y="172" font-size="40" font-family="{SERIF}" font-style="italic" fill="url(#nm)">{NAME}</text>'
          f'<text x="60" y="216" font-size="16" font-weight="700" letter-spacing="3" fill="{c["acc"]}">SOFTWARE ENGINEER</text>'
          f'<rect class="cursor" x="308" y="202" width="9" height="16" fill="{c["acc"]}"/>'
          f'<text x="60" y="258" font-size="13" letter-spacing="1" fill="{c["fg"]}" xml:space="preserve">AI  ·  Math  ·  Newest Technologies</text>'
          f'<rect x="60" y="274" width="36" height="2" fill="{c["acc"]}"/>')
    for i, t in enumerate(["Building systems, web applications,", "developer tools and intelligent software", "for a better tomorrow."]):
        b += f'<text x="60" y="{306+i*20}" font-size="12.5" fill="{c["mute"]}">{t}</text>'
    b += divider(c, 448, seed=4) + fireflies(c, 14, (480, 120, 880, 420)) + petals(c, 12, (300, 890), 8)
    return wrap(900, 470, c, b)

def button(c, label):
    w = 150
    b = (f'<rect x=".75" y=".75" width="{w-1.5}" height="38.5" rx="19" fill="{c["card"]}" stroke="{c["acc"]}" stroke-opacity=".85"/>'
         + star4(26, 20, 7, c["acc"], 1, "tw", 1) +
         f'<text x="44" y="24.5" font-size="12" letter-spacing="1.2" fill="{c["fg"]}">{label.upper()}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" font-family="{MONO}">{STYLE}{b}</svg>'

def about(c):
    b = sky(c, 900, 290, 26, 3) + heading(c, 42, "01", "ABOUT")
    L = ["I'm Solayman El Mouden, a software engineer", "focused on systems, web technologies,",
         "artificial intelligence and mathematics.", "", "I enjoy understanding how things work",
         "underneath the abstraction and turning that", "knowledge into useful software."]
    for i, t in enumerate(L):
        b += f'<text x="60" y="{92+i*21}" font-size="13" fill="{c["fg"]}" xml:space="preserve">{t}</text>'
    b += heading(c, 42, "02", "MY JOURNEY", 480)
    ys = [96 + i * 30 for i in range(len(JOURNEY))]
    b += f'<path d="M490 {ys[0]-4}V{ys[-1]-4}" stroke="{c["acc"]}" stroke-opacity=".6" stroke-dasharray="3 4"/>'
    for i, ((a, t), y) in enumerate(zip(JOURNEY, ys)):
        b += (star4(490, y - 4, 6, c["acc"], 1, "tw", i * 1.2) +
              f'<text x="512" y="{y}" font-size="13" fill="{c["fg"]}">{a}</text>'
              f'<path d="M640 {y-4}H664M659 {y-8}L664 {y-4}L659 {y}" fill="none" stroke="{c["acc2"]}"/>'
              f'<text x="682" y="{y}" font-size="13" fill="{c["mute"]}">{t}</text>')
    b += divider(c, 274, seed=5)
    return wrap(900, 290, c, b)

def skills(c):
    b = sky(c, 900, 270, 24, 4) + heading(c, 38, "03", "TECHNOLOGIES &amp; SKILLS")
    for i, (name, mono) in enumerate(SKILLS):
        cx = 40 + 68.3 + (i % 6) * 136.7; cy = 92 + (i // 6) * 100
        b += (f'<circle cx="{f1(cx)}" cy="{cy}" r="29" fill="{c["card"]}" fill-opacity=".85" stroke="{c["line"]}" stroke-width="1.4"/>'
              f'<g transform="translate({f1(cx)} {cy})"><g class="spin{" r" if i % 2 else ""}"><circle r="35" fill="none" stroke="{c["acc"]}" stroke-width="1.2" stroke-dasharray="1 6.2" stroke-linecap="round"/>'
              + star4(35, 0, 3.5, c["acc"]) + star4(-35, 0, 3.5, c["acc"]) + '</g></g>' +
              f'<text x="{f1(cx)}" y="{cy+5}" font-size="14" font-weight="700" text-anchor="middle" fill="{c["acc"]}">{mono}</text>'
              f'<text x="{f1(cx)}" y="{cy+54}" font-size="10.5" text-anchor="middle" fill="{c["fg"]}">{name}</text>')
    b += divider(c, 250, seed=6)
    return wrap(900, 268, c, b)

def projects_title(c):
    return wrap(900, 60, c, sky(c, 900, 60, 14, 5) + heading(c, 34, "04", "SELECTED PROJECTS"))

def card(c, idx, name, d1, d2, tags, box):
    w, h = 208, 198
    img = crop64(box, (400, 188), 82)
    arch = "M8 100V56A96 48 0 0 1 200 56V100Z"
    b = (f'<defs><clipPath id="cl"><path d="{arch}"/></clipPath></defs>'
         f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="14" fill="{c["card"]}" fill-opacity=".9" stroke="{c["line"]}" stroke-width="1.5"/>'
         f'<image x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)" href="{img}" xlink:href="{img}"/>'
         f'<path d="{arch}" fill="none" stroke="{c["acc"]}" stroke-width="1.4"/>'
         f'<path class="dots" d="{arch}" fill="none" stroke="{c["acc"]}" stroke-width="2.4"/>'
         + star4(104, 8, 5, c["acc"], 1, "tw", idx) + star4(182, 26, 3, c["star"], .9, "tw", idx + 2) +
         f'<text x="16" y="124" font-size="13.5" font-weight="700" fill="{c["fg"]}">{name}</text>'
         f'<text x="16" y="143" font-size="10.5" fill="{c["mute"]}">{d1}</text>'
         f'<text x="16" y="157" font-size="10.5" fill="{c["mute"]}">{d2}</text>')
    x = 16
    for t in tags:
        cw = len(t) * 5.1 + 10
        b += (f'<rect x="{f1(x)}" y="171" width="{f1(cw)}" height="17" rx="8.5" fill="none" stroke="{c["line"]}"/>'
              f'<text x="{f1(x+cw/2)}" y="182.5" font-size="8.5" text-anchor="middle" fill="{c["acc"]}">{t}</text>')
        x += cw + 5
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{MONO}">{STYLE}{defs(c)}{b}</svg>'

def lantern(c, x, y, top=0):
    return (f'<path d="M{x} {top}V{y-18}" stroke="{c["mute"]}" stroke-opacity=".7"/>'
            f'<circle class="flick" cx="{x}" cy="{y}" r="70" fill="url(#warm)"/>'
            f'<g transform="translate({x} {y})"><g class="spin f">{rune_ring(c, 34, 12)}</g></g>'
            f'<rect x="{x-8}" y="{y-18}" width="16" height="4" rx="2" fill="{c["mute"]}"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="10" ry="13" fill="#ffb347"/><ellipse class="flick" cx="{x}" cy="{y}" rx="5" ry="8" fill="#fff0b8"/>'
            f'<rect x="{x-8}" y="{y+13}" width="16" height="4" rx="2" fill="{c["mute"]}"/>')

def footer(c):
    r = random.Random(12); b = sky(c, 900, 140, 36, 6)
    b += lantern(c, 120, 118) + lantern(c, 780, 118)
    # frosted canopy hills
    hill = lambda x: 176 + 22 * math.sin(x / 85) + 10 * math.sin(x / 33 + 1)
    for _ in range(900):
        x = r.uniform(0, 900); y = r.uniform(hill(x), 262)
        col = c["coral"] if r.random() < .05 else r.choice(c["canopy"])
        b += f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r.uniform(2.2, 6):.1f}" fill="{col}" opacity="{r.uniform(.6, .95):.2f}"/>'
    b += (f'<text x="450" y="52" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle" fill="{c["acc"]}" xml:space="preserve">BUILD  ·  EXPLORE  ·  UNDERSTAND</text>'
          f'<text x="450" y="76" font-size="10.5" letter-spacing="1" text-anchor="middle" fill="{c["mute"]}" xml:space="preserve">Software Engineering · Systems · AI · Mathematics</text>')
    b += fireflies(c, 12, (40, 90, 860, 230), 9) + petals(c, 7, (60, 840), 13)
    return wrap(900, 262, c, b)

def save(name, theme, svg):
    svg = re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", svg)
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f: f.write(svg)

for th, c in THEMES.items():
    save("hero", th, hero(c)); save("about", th, about(c)); save("skills", th, skills(c))
    save("projects-title", th, projects_title(c)); save("footer", th, footer(c))
    for lbl in ("GitHub", "LinkedIn", "Portfolio"): save(f"btn-{lbl.lower()}", th, button(c, lbl))
    for i, (n, slug, d1, d2, tags, box) in enumerate(PROJECTS): save(f"card-{slug}", th, card(c, i, n, d1, d2, tags, box))

def pic(name, alt, width=None, href=None):
    w = f' width="{width}"' if width else ""
    p = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'  <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'  <img alt="{alt}" src="assets/{name}-dark.svg"{w}>\n</picture>')
    return f'<a href="{href}">{p}</a>' if href else p

def cards(items):
    return "\n".join(pic(f"card-{s}", n, "24%", f"{GITHUB}/{s}") for n, s, *_ in items)

parts = [pic("hero", f"{NAME} — Software Engineer. AI, Math, Newest Technologies.", "100%"),
         "<br>\n" + "&nbsp;\n".join(pic(f"btn-{l.lower()}", l, href=u) for l, u in
                                    (("GitHub", GITHUB), ("LinkedIn", LINKEDIN), ("Portfolio", PORTFOLIO))),
         pic("about", "About and journey", "100%"), pic("skills", "Technologies and skills", "100%"),
         pic("projects-title", "Selected projects", "100%"),
         cards(PROJECTS[:4]), cards(PROJECTS[4:]),
         pic("footer", "Build, Explore, Understand", "100%"),
         f'<sub><a href="{PORTFOLIO}">solaymantech.me</a> &nbsp;·&nbsp; <a href="{LINKEDIN}">LinkedIn</a></sub>']
with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
    f.write('<div align="center">\n\n' + "\n\n".join(parts) + "\n\n</div>\n")
print("done")
