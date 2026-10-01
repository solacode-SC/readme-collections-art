#!/usr/bin/env python3
"""Swirl / flow-field edition. Pure Python, no dependencies.
Generates dark+light SVG assets (assets/) and README.md.
Art system (reinterpreted from the reference, nothing is copied):
  - sky      -> evenly-spaced streamlines of a multi-vortex field
  - roses    -> archimedean spirals
  - fields   -> layered sine contour bands
"""
import math, os, random, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif"
JP = "'Noto Sans JP','Yu Gothic','Hiragino Sans',sans-serif"

THEMES = {
 "dark":  dict(bg1="#041114", bg2="#0a2126", fg="#ecf4ef", mute="#8db2ac", acc="#f0d672", acc2="#7fc9bf",
               line="#1d4a50", card="#08191d", pal=["#2f8f98", "#4fb09b", "#8fc99c", "#5aaebb"], warm="#f0d672", roof="#dc7a52"),
 "light": dict(bg1="#fbf7ea", bg2="#efe8d2", fg="#12343a", mute="#58797c", acc="#96640a", acc2="#1d6670",
               line="#c3d2c6", card="#fffdf4", pal=["#1d6670", "#2f8a7e", "#5f9a74", "#3f8e9c"], warm="#c9971c", roof="#b6532f"),
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
# (title, repo-slug, line1, line2, tags, motif)
PROJECTS = [
 ("LazyEquation", "lazyequation", "Interactive math & physics", "visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"], "waves"),
 ("LeetResume", "leetresume", "AI-powered resume", "builder and optimizer.", ["Next.js", "Prisma", "Postgres"], "flow"),
 ("Libora", "libora", "Flutter PDF reader with", "modern experience.", ["Flutter", "Dart", "Riverpod"], "spiral"),
 ("Webserv", "webserv", "C++98 HTTP server", "from scratch.", ["C++98", "Networking"], "network"),
 ("solaJobs v2", "solajobs-v2", "Arabic-first job board", "platform.", ["Arabic-first", "Jobs"], "roses"),
 ("Alert Generator", "prometheus-alert-generator", "AI generator for", "Prometheus alert rules.", ["AI", "Prometheus"], "pulse"),
 ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose", "dashboard.", ["Docker", "Compose"], "grid"),
]
# ---------------------------------------------

STYLE = '''<style>
.spin{transform-box:fill-box;transform-origin:center;animation:spin 70s linear infinite}
.spin.r{animation-direction:reverse;animation-duration:95s}
@keyframes spin{to{transform:rotate(360deg)}}
.dots{stroke-dasharray:.1 34;stroke-linecap:round;animation:run 18s linear infinite}
@keyframes run{to{stroke-dashoffset:-341}}
.pulse{animation:pulse 10s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
@media (prefers-reduced-motion:reduce){.spin,.dots,.pulse{animation:none}}
</style>'''

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")
def pts_path(pts): return "M" + "L".join(f"{f1(x)} {f1(y)}" for x, y in pts)

# ---------- math art primitives ----------
VORT = [(700, 170, 1.0, .20, 44), (570, 285, -.6, .12, 24), (850, 62, -.55, .14, 22), (545, 60, .5, .12, 24), (860, 290, .55, .12, 22)]
def vel(x, y):
    vx = vy = 0.0
    for cx, cy, g, k, a in VORT:
        dx, dy = x - cx, y - cy; d2 = dx * dx + dy * dy + a * a
        w = a * 2 / d2
        vx += (-g * dy - k * dx) * w; vy += (g * dx - k * dy) * w
    n = math.hypot(vx, vy) or 1
    return vx / n, vy / n

def streamlines(x0=430, x1=900, y0=0, y1=345, dsep=8.5, h=4.0, seed=4):
    rnd = random.Random(seed); cell = dsep; grid = {}
    def near(x, y, r):
        i, j = int(x // cell), int(y // cell); r2 = r * r
        for a in (i - 1, i, i + 1):
            for b in (j - 1, j, j + 1):
                for px, py in grid.get((a, b), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < r2: return True
        return False
    def step(x, y, s):
        vx, vy = vel(x, y); mx, my = x + s * vx * h / 2, y + s * vy * h / 2
        vx, vy = vel(mx, my); return x + s * vx * h, y + s * vy * h
    def trace(x, y, s):
        out = []
        for n in range(260):
            x, y = step(x, y, s)
            if not (x0 <= x <= x1 and y0 <= y <= y1): break
            if near(x, y, dsep * .55): break
            if any(math.hypot(x - cx, y - cy) < 3 for cx, cy, *_ in VORT): break
            if n > 12 and out and math.hypot(x - out[0][0], y - out[0][1]) < h: break
            out.append((x, y))
        return out
    lines = []
    for _ in range(9000):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if near(x, y, dsep): continue
        fw, bw = trace(x, y, 1), trace(x, y, -1)
        line = bw[::-1] + [(x, y)] + fw
        if len(line) < 10: continue
        for p in line: grid.setdefault((int(p[0] // cell), int(p[1] // cell)), []).append(p)
        lines.append(line)
    return lines
STREAM = streamlines()

def line_color(c, line):
    mx = sum(p[0] for p in line) / len(line); my = sum(p[1] for p in line) / len(line)
    best = min(range(len(VORT)), key=lambda i: math.hypot(mx - VORT[i][0], my - VORT[i][1]) - VORT[i][4])
    d = math.hypot(mx - VORT[best][0], my - VORT[best][1])
    return c["pal"][(int(d / 30) + best) % 4]

def spiral(cx, cy, r, turns=3, rot=0, start=.15):
    pts = []; n = int(turns * 28)
    for i in range(n + 1):
        t = i / n; th = t * turns * 2 * math.pi + rot; rr = r * (start + (1 - start) * t)
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    return pts

def waves(x0, x1, y0, rows, c, amp=12, gap=3.8, seed=1, cols=None):
    rnd = random.Random(seed); o = []; cols = cols or [c["warm"], c["pal"][2], c["warm"], c["pal"][1]]
    ph = rnd.uniform(0, 6)
    for i in range(rows):
        pts = []
        for x in range(int(x0), int(x1) + 1, 6):
            y = y0 + i * gap + amp * math.sin(x / 95 + i * .16 + ph) + amp * .35 * math.sin(x / 38 + i * .3)
            pts.append((x, y))
        o.append(f'<path d="{pts_path(pts)}" fill="none" stroke="{cols[i % len(cols)]}" stroke-width="1.1" opacity="{.5 + .4 * (i % 2)}"/>')
    return "".join(o)

def plus(x, y, s, col, op=.8):
    return f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" stroke="{col}" stroke-width="1" opacity="{op}"/>'

def defs(c):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<linearGradient id="side" x1="0" x2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset=".35" stop-color="{c['bg1']}" stop-opacity=".96"/><stop offset="1" stop-color="{c['bg1']}" stop-opacity="0"/></linearGradient>
</defs>'''

def wrap(w, h, c, body, cls_font=MONO):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{cls_font}">'
            f'{STYLE}{defs(c)}<rect width="{w}" height="{h}" fill="url(#bg)"/>{body}'
            f'<path d="M.5 0V{h}M{w-.5} 0V{h}" stroke="{c["line"]}"/></svg>')

def divider(c, y, w=900):
    pts = [(x, y + 3 * math.sin(x / 38)) for x in range(40, w - 39, 6)]
    d = pts_path(pts)
    return (f'<path d="{d}" fill="none" stroke="{c["line"]}" stroke-width="1"/>'
            f'<path class="dots" d="{d}" fill="none" stroke="{c["acc"]}" stroke-width="2.4"/>')

def heading(c, y, idx, label):
    sp = pts_path(spiral(60, y, 9, 2.4))
    return (f'<path d="{sp}" fill="none" stroke="{c["acc"]}" stroke-width="1.5"/>'
            f'<text x="82" y="{y+4}" font-size="12" letter-spacing="2.2" fill="{c["mute"]}">{idx} /</text>'
            f'<text x="126" y="{y+4}" font-size="12" font-weight="700" letter-spacing="2.2" fill="{c["fg"]}">{label}</text>')

def corners(c, x, y, w, h, s=7, op=.9):
    return (f'<path d="M{x} {y+s}V{y}H{x+s}M{x+w-s} {y}H{x+w}V{y+s}M{x+w} {y+h-s}V{y+h}H{x+w-s}M{x+s} {y+h}H{x}V{y+h-s}" '
            f'fill="none" stroke="{c["acc"]}" stroke-width="1.3" opacity="{op}"/>')

# ---------- panels ----------
def hero(c):
    b = "".join(f'<path d="{pts_path(l)}" fill="none" stroke="{line_color(c, l)}" stroke-width="1.15" opacity=".88"/>' for l in STREAM)
    # particles drifting along a handful of streamlines
    for l in STREAM[::9]:
        b += f'<path class="dots" d="{pts_path(l)}" fill="none" stroke="{c["acc"]}" stroke-width="2.4" opacity=".9"/>'
    b += f'<rect x="400" y="0" width="300" height="400" fill="url(#side)"/>'
    # contour fields + spiral roses
    b += waves(0, 900, 372, 12, c, amp=11, gap=3.6)
    for i, (x, y, r) in enumerate([(560, 366, 15), (640, 380, 11), (725, 360, 17), (815, 378, 12), (868, 358, 10)]):
        b += (f'<circle cx="{x}" cy="{y}" r="{r+3}" fill="{c["bg1"]}"/>'
              f'<path class="spin{" r" if i % 2 else ""}" d="{pts_path(spiral(x, y, r, 3, i))}" fill="none" stroke="{c["warm"]}" stroke-width="1.4"/>')
    # top bar
    b += (f'<path d="{pts_path(spiral(60, 34, 8, 2.4))}" fill="none" stroke="{c["acc"]}" stroke-width="1.4"/>'
          f'<text x="80" y="38" font-size="12" fill="{c["mute"]}">solacode-SC <tspan fill="{c["line"]}">/</tspan> README</text>'
          f'<path d="M40 56H860" stroke="{c["line"]}"/>' + plus(40, 56, 4, c["acc"]) + plus(860, 56, 4, c["acc"]))
    b += plus(436, 100, 4, c["mute"], .5) + plus(884, 332, 4, c["mute"], .5)
    b += f'<text x="868" y="332" font-size="9" text-anchor="end" fill="{c["mute"]}" opacity=".8">r = a·e^(bθ)</text>'
    # copy
    b += (f'<text x="60" y="108" font-size="13" letter-spacing="3" fill="{c["mute"]}">HI, I\'M</text>'
          f'<text x="58" y="160" font-size="42" font-family="{SERIF}" letter-spacing="-.5" fill="{c["fg"]}">{NAME}</text>'
          f'<text x="60" y="204" font-size="16" font-weight="700" letter-spacing="3" fill="{c["acc"]}">SOFTWARE ENGINEER</text>'
          f'<text x="60" y="246" font-size="13" letter-spacing="1" fill="{c["fg"]}" xml:space="preserve">AI  ·  Math  ·  Newest Technologies</text>')
    for i, t in enumerate(["Building systems, web applications,", "developer tools and intelligent software", "for a better tomorrow."]):
        b += f'<text x="60" y="{290+i*20}" font-size="12.5" fill="{c["mute"]}">{t}</text>'
    b += f'<rect x="60" y="262" width="36" height="2" fill="{c["acc"]}"/>'
    # vertical mark
    for i, ch in enumerate("夢を築く"):
        b += f'<text x="878" y="{92+i*22}" font-size="14" text-anchor="middle" font-family="{JP}" fill="{c["acc2"]}" opacity=".9">{ch}</text>'
    return wrap(900, 410, c, b)

def button(c, label):
    w = 150
    b = (f'<rect x=".75" y=".75" width="{w-1.5}" height="38.5" rx="4" fill="{c["card"]}" stroke="{c["acc2"]}" stroke-opacity=".8"/>'
         f'<path d="{pts_path(spiral(24, 20, 8, 2.2))}" fill="none" stroke="{c["acc"]}" stroke-width="1.4"/>'
         f'<text x="42" y="24.5" font-size="12" letter-spacing="1.2" fill="{c["fg"]}">{label.upper()}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" font-family="{MONO}">{b}</svg>'

def about(c):
    b = heading(c, 42, "01", "ABOUT")
    L = ["I'm Solayman El Mouden, a software engineer", "focused on systems, web technologies,",
         "artificial intelligence and mathematics.", "", "I enjoy understanding how things work",
         "underneath the abstraction and turning that", "knowledge into useful software."]
    for i, t in enumerate(L):
        b += f'<text x="60" y="{92+i*21}" font-size="13" fill="{c["fg"]}" xml:space="preserve">{t}</text>'
    b += f'<path d="M450 74V246" stroke="{c["line"]}"/>' + plus(450, 74, 4, c["acc"]) + plus(450, 246, 4, c["acc"])
    b += heading(c, 42, "02", "MY JOURNEY").replace('x="60"', 'x="480"').replace('x="82"', 'x="502"').replace('x="126"', 'x="546"')
    for i, (a, t) in enumerate(JOURNEY):
        y = 96 + i * 30
        b += (f'<path d="{pts_path(spiral(488, y-4, 6, 2))}" fill="none" stroke="{c["acc"]}" stroke-width="1.3"/>'
              f'<text x="508" y="{y}" font-size="13" fill="{c["fg"]}">{a}</text>'
              f'<path d="M640 {y-4}H664M659 {y-8}L664 {y-4}L659 {y}" fill="none" stroke="{c["acc2"]}"/>'
              f'<text x="682" y="{y}" font-size="13" fill="{c["mute"]}">{t}</text>')
    b += divider(c, 274)
    return wrap(900, 290, c, b)

def skills(c):
    b = heading(c, 40, "03", "TECHNOLOGIES &amp; SKILLS")
    w, g = 125, 14
    for i, (name, mono) in enumerate(SKILLS):
        x = 40 + (i % 6) * (w + g); y = 68 + (i // 6) * 66
        b += (f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="53" rx="5" fill="{c["card"]}" stroke="{c["line"]}"/>'
              + corners(c, x + 3, y + 3, w - 6, 47, 5, .7) +
              f'<text x="{x+w/2}" y="{y+25}" font-size="16" font-weight="700" text-anchor="middle" fill="{c["acc"]}">{mono}</text>'
              f'<text x="{x+w/2}" y="{y+43}" font-size="10.5" text-anchor="middle" fill="{c["fg"]}">{name}</text>')
    b += divider(c, 214)
    return wrap(900, 226, c, b)

def projects_title(c):
    return wrap(900, 60, c, heading(c, 34, "04", "SELECTED PROJECTS"))

def motif(c, kind, idx):
    W, H = 192, 56; rnd = random.Random(idx * 7 + 3); p = c["pal"]; o = []
    if kind == "waves":
        for k, (f, a, col) in enumerate([(.05, 14, p[0]), (.09, 9, p[1]), (.14, 6, c["warm"])]):
            pts = [(x, 28 + a * math.sin(x * f + k) + 4 * math.sin(x * f * 2.7)) for x in range(0, W + 1, 3)]
            o.append(f'<path d="{pts_path(pts)}" fill="none" stroke="{col}" stroke-width="1.3"/>')
    elif kind == "flow":
        for k in range(9):
            pts = [(x, 6 + k * 5.5 + (k - 4) * 3 * math.sin(x / 38 + k * .2) * (x / W)) for x in range(0, W + 1, 3)]
            o.append(f'<path d="{pts_path(pts)}" fill="none" stroke="{p[k % 4]}" stroke-width="1.2"/>')
    elif kind == "spiral":
        o.append(f'<path d="{pts_path(spiral(70, 28, 40, 5))}" fill="none" stroke="{p[0]}" stroke-width="1.2"/>')
        o.append(f'<path d="{pts_path(spiral(138, 30, 26, 4, 1.2))}" fill="none" stroke="{c["warm"]}" stroke-width="1.2"/>')
    elif kind == "network":
        nodes = [(rnd.uniform(14, W - 14), rnd.uniform(10, H - 10)) for _ in range(9)]
        for i, a in enumerate(nodes):
            for bb in sorted(nodes, key=lambda n: math.hypot(n[0] - a[0], n[1] - a[1]))[1:3]:
                o.append(f'<path d="M{f1(a[0])} {f1(a[1])}L{f1(bb[0])} {f1(bb[1])}" stroke="{p[1]}" stroke-width=".9" opacity=".8"/>')
        o += [f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{2.6 if i else 4}" fill="{c["warm"] if i == 0 else p[2]}"/>' for i, (x, y) in enumerate(nodes)]
    elif kind == "roses":
        for i, (x, y, r) in enumerate([(30, 30, 16), (72, 18, 10), (100, 38, 15), (140, 20, 11), (168, 40, 12)]):
            o.append(f'<path d="{pts_path(spiral(x, y, r, 3, i))}" fill="none" stroke="{c["warm"]}" stroke-width="1.3"/>')
        o.append(f'<path d="M0 50Q40 44 90 50T192 48" fill="none" stroke="{p[2]}" stroke-width="1.1"/>')
    elif kind == "pulse":
        pts = []; x = 0
        while x < W:
            spike = rnd.random() < .22
            pts += [(x, 30), (x + 4, 30 - (22 if spike else 4)), (x + 8, 30 + (14 if spike else 4)), (x + 12, 30)]; x += 14
        o.append(f'<path d="{pts_path(pts)}" fill="none" stroke="{p[1]}" stroke-width="1.2"/>')
        o.append(f'<path d="M0 30H{W}" stroke="{c["warm"]}" stroke-width=".8" stroke-dasharray="2 4"/>')
    else:  # grid
        for i in range(8):
            for j in range(3):
                on = (i * 3 + j) in (4, 11, 17)
                o.append(f'<rect x="{10+i*23}" y="{8+j*16}" width="18" height="11" rx="2" fill="{c["warm"] if on else "none"}" fill-opacity=".85" stroke="{p[0]}" stroke-width=".9"/>')
    return "".join(o)

def card(c, idx, name, d1, d2, tags, kind):
    w, h = 208, 176
    b = (f'<defs><clipPath id="cl"><rect x="8" y="8" width="192" height="56" rx="3"/></clipPath></defs>'
         f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="6" fill="{c["card"]}" stroke="{c["line"]}"/>'
         + corners(c, 4, 4, w - 8, h - 8, 8) +
         f'<rect x="8" y="8" width="192" height="56" rx="3" fill="{c["bg1"]}"/>'
         f'<g transform="translate(8 8)" clip-path="url(#cl)">{motif(c, kind, idx)}</g>'
         f'<text x="14" y="20" font-size="8.5" fill="{c["mute"]}">N°{idx+1:02d}</text>'
         f'<text x="16" y="92" font-size="13.5" font-weight="700" fill="{c["fg"]}">{name}</text>'
         f'<text x="16" y="111" font-size="10.5" fill="{c["mute"]}">{d1}</text>'
         f'<text x="16" y="125" font-size="10.5" fill="{c["mute"]}">{d2}</text>')
    x = 16
    for t in tags:
        cw = len(t) * 5.1 + 10
        b += (f'<rect x="{f1(x)}" y="142" width="{f1(cw)}" height="17" rx="3" fill="none" stroke="{c["line"]}"/>'
              f'<text x="{f1(x+cw/2)}" y="153.5" font-size="8.5" text-anchor="middle" fill="{c["acc2"]}">{t}</text>')
        x += cw + 5
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{MONO}">{defs(c)}{b}</svg>'

def footer(c):
    b = waves(0, 900, 78, 13, c, amp=10, gap=3.5, seed=5)
    for i, (x, y, r) in enumerate([(90, 70, 14), (210, 82, 10), (690, 72, 12), (800, 84, 16), (860, 68, 9)]):
        b += (f'<circle cx="{x}" cy="{y}" r="{r+3}" fill="{c["bg1"]}"/>'
              f'<path class="spin{" r" if i % 2 else ""}" d="{pts_path(spiral(x, y, r, 3, i))}" fill="none" stroke="{c["warm"]}" stroke-width="1.4"/>')
    b += f'<rect x="270" y="0" width="360" height="74" fill="{c["bg1"]}" opacity=".9"/>'
    b += (f'<text x="450" y="34" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle" fill="{c["acc"]}" xml:space="preserve">BUILD  ·  EXPLORE  ·  UNDERSTAND</text>'
          f'<text x="450" y="56" font-size="10.5" letter-spacing="1" text-anchor="middle" fill="{c["mute"]}" xml:space="preserve">Software Engineering · Systems · AI · Mathematics</text>')
    return wrap(900, 130, c, b)

def save(name, theme, svg):
    svg = re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", svg)
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f: f.write(svg)

for th, c in THEMES.items():
    save("hero", th, hero(c)); save("about", th, about(c)); save("skills", th, skills(c))
    save("projects-title", th, projects_title(c)); save("footer", th, footer(c))
    for lbl in ("GitHub", "LinkedIn", "Portfolio"): save(f"btn-{lbl.lower()}", th, button(c, lbl))
    for i, (n, slug, d1, d2, tags, kind) in enumerate(PROJECTS): save(f"card-{slug}", th, card(c, i, n, d1, d2, tags, kind))

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
print("done", len(STREAM), "streamlines")
