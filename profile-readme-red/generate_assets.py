#!/usr/bin/env python3
"""Generates phoenix-themed (crimson / gold / ivory) dark+light SVG panels + README.md.
Needs: pip install pillow   (crops art/phoenix.jpg and embeds the crops into the SVGs)"""
import os, re, io, base64
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
ART = Image.open(os.path.join(HERE, "art", "phoenix.jpg"))
FONT = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
SERIF = "'Cormorant Garamond','Playfair Display',Georgia,'Times New Roman',serif"
JP = "'Noto Sans JP','Yu Gothic','Hiragino Sans',sans-serif"

# palette pulled from the phoenix piece: lacquer red, leaf gold, ivory feathers, coral, jade
THEMES = {
 "dark":  dict(bg1="#6a0d10", bg2="#2a0507", fg="#f7eddb", mute="#dcc196", acc="#e8c56e", acc2="#f6e0a0",
               line="#a98230", card="#3b0709", coral="#e8935a", jade="#4d9a8e", ring="#f6e0a0"),
 "light": dict(bg1="#fffaf0", bg2="#f3e5c9", fg="#3a0a0c", mute="#7d4b3b", acc="#a8191c", acc2="#b8893a",
               line="#d2b06a", card="#fff6e2", coral="#d9763f", jade="#2f7f74", ring="#b8893a"),
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
# (title, repo-slug, line1, line2, tags, crop-box in phoenix.jpg)
PROJECTS = [
 ("LazyEquation", "lazyequation", "Interactive math & physics", "visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"], (20, 300, 320, 381)),
 ("LeetResume", "leetresume", "AI-powered resume", "builder and optimizer.", ["Next.js", "Prisma", "Postgres"], (330, 90, 630, 171)),
 ("Libora", "libora", "Flutter PDF reader with", "modern experience.", ["Flutter", "Dart", "Riverpod"], (350, 310, 650, 391)),
 ("Webserv", "webserv", "C++98 HTTP server", "from scratch.", ["C++98", "Networking"], (435, 380, 735, 461)),
 ("solaJobs v2", "solajobs-v2", "Arabic-first job board", "platform.", ["Arabic-first", "Jobs"], (0, 730, 300, 811)),
 ("Alert Generator", "prometheus-alert-generator", "AI generator for", "Prometheus alert rules.", ["AI", "Prometheus"], (250, 590, 550, 671)),
 ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose", "dashboard.", ["Docker", "Compose"], (0, 480, 300, 561)),
]
# ---------------------------------------------

def crop64(box, size, q=80):
    im = ART.crop(box).resize(size, Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def mix(a, b, t):
    pa = [int(a[i:i+2], 16) for i in (1, 3, 5)]; pb = [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x + (y - x) * t) for x, y in zip(pa, pb))

def defs(c):
    edge = mix(c["bg1"], c["bg2"], .5)
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{c['line']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['acc2']}"/><stop offset="1" stop-color="{c['line']}" stop-opacity="0"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['acc2']}"/><stop offset="1" stop-color="{c['line']}"/></linearGradient>
<linearGradient id="side" x1="0" x2="1"><stop offset="0" stop-color="{edge}"/><stop offset=".55" stop-color="{edge}" stop-opacity=".75"/><stop offset="1" stop-color="{edge}" stop-opacity="0"/></linearGradient>
</defs>'''

def wrap(w, h, c, body, frame=True):
    fr = f'<path d="M1 0V{h}M{w-1} 0V{h}" stroke="{c["line"]}" stroke-width="2"/>' if frame else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">'
            f'{defs(c)}<rect width="{w}" height="{h}" fill="url(#bg)"/>{body}{fr}</svg>')

def star(x, y, s, col, op=1):
    return f'<path d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z" fill="{col}" opacity="{op}"/>'

def bloom(x, y, r, c, petals=8, col=None):
    """Little gilded peony: layered petals + pearl centre."""
    col = col or c["acc"]; o = []
    for layer, (k, op) in enumerate([(1, .55), (.68, .8), (.4, 1)]):
        for i in range(petals):
            a = i * 360 / petals + layer * 22
            o.append(f'<ellipse cx="{x}" cy="{y - r*k*.55:.1f}" rx="{r*k*.34:.1f}" ry="{r*k*.55:.1f}" '
                     f'transform="rotate({a} {x} {y})" fill="{col}" fill-opacity="{op*.5:.2f}" stroke="{c["acc2"]}" stroke-width=".8"/>')
    o.append(f'<circle cx="{x}" cy="{y}" r="{r*.14:.1f}" fill="{c["fg"]}"/>')
    return "".join(o)

def title(c, y, label):
    return (bloom(62, y, 12, c, 6) +
            f'<text x="86" y="{y+7}" font-size="22" font-weight="700" font-family="{SERIF}" fill="{c["fg"]}">{label}</text>')

def divider(c, y, w=900):
    return (f'<rect x="40" y="{y}" width="{w-80}" height="1.2" fill="url(#fade)"/>'
            f'<path d="M{w/2} {y-6}l6 6.6-6 6.6-6-6.6z" fill="url(#gold)"/>'
            f'<circle cx="{w/2-22}" cy="{y+.6}" r="2.2" fill="{c["acc2"]}"/><circle cx="{w/2+22}" cy="{y+.6}" r="2.2" fill="{c["acc2"]}"/>')

# ---------- panels ----------
def header(c):
    img = crop64((0, 140, 735, 715), (500, 392), 82)
    b = (f'<image x="400" y="0" width="500" height="360" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/>'
         f'<rect x="400" y="0" width="200" height="360" fill="url(#side)"/>')
    b += star(120, 40, 7, c["acc"]) + star(300, 70, 5, c["acc2"], .8) + star(600, 330, 6, c["acc2"], .9)
    b += (f'<text x="60" y="95" font-size="20" fill="{c["mute"]}">Hi, I\'m</text>'
          f'<text x="58" y="148" font-size="42" font-weight="700" font-family="{SERIF}" fill="{c["fg"]}">{NAME}</text>'
          f'<text x="60" y="198" font-size="24" fill="{c["acc"]}">Software Engineer</text>'
          f'<rect x="298" y="179" width="12" height="22" fill="{c["acc"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
          f'<text x="60" y="246" font-size="15" fill="{c["fg"]}" xml:space="preserve">AI   |   Math   |   Newest Technologies</text>')
    for i, t in enumerate(["Building systems, web applications,", "developer tools and intelligent software", "for a better tomorrow."]):
        b += f'<text x="60" y="{288+i*20}" font-size="13" fill="{c["mute"]}">{t}</text>'
    b += f'<rect x="858" y="40" width="28" height="108" rx="4" fill="{c["bg2"]}" fill-opacity=".72" stroke="{c["acc"]}"/>'
    for i, ch in enumerate("夢を築く"):
        b += f'<text x="872" y="{63+i*25}" font-size="16" text-anchor="middle" font-family="{JP}" fill="{c["acc2"]}">{ch}</text>'
    b += divider(c, 346)
    return wrap(900, 360, c, b)

def button(c, label):
    w = 150
    b = (f'<rect x="1" y="1" width="{w-2}" height="38" rx="19" fill="{c["card"]}" stroke="{c["acc"]}" stroke-width="1.5"/>'
         + bloom(26, 20, 9, c, 6) +
         f'<text x="44" y="25" font-size="13" fill="{c["fg"]}">{label}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" font-family="{FONT}">{b}</svg>'

def about(c):
    b = title(c, 42, "About")
    L = ["I'm Solayman El Mouden, a software engineer", "focused on systems, web technologies,",
         "artificial intelligence and mathematics.", "", "I enjoy understanding how things work",
         "underneath the abstraction and turning that", "knowledge into useful software."]
    for i, t in enumerate(L):
        b += f'<text x="60" y="{90+i*21}" font-size="13" fill="{c["fg"]}" xml:space="preserve">{t}</text>'
    b += f'<rect x="440" y="75" width="1" height="165" fill="{c["line"]}"/>'
    b += f'<text x="475" y="94" font-size="19" font-weight="700" font-family="{SERIF}" fill="{c["fg"]}">My journey</text>'
    for i, (a, t) in enumerate(JOURNEY):
        y = 130 + i * 30
        b += (f'<path d="M485 {y-11}l6 6-6 6-6-6z" fill="none" stroke="{c["acc"]}" stroke-width="1.4"/>'
              f'<text x="504" y="{y}" font-size="13" fill="{c["fg"]}">{a}</text>'
              f'<text x="640" y="{y}" font-size="13" fill="{c["acc"]}">→</text>'
              f'<text x="680" y="{y}" font-size="13" fill="{c["mute"]}">{t}</text>')
    b += bloom(840, 135, 26, c, 8, c["coral"]) + star(872, 90, 7, c["acc2"], .8) + star(815, 185, 5, c["acc"], .7)
    b += divider(c, 272)
    return wrap(900, 285, c, b)

def skills(c):
    b = title(c, 38, "Technologies &amp; Skills")
    w, g = 125, 14
    for i, (name, mono) in enumerate(SKILLS):
        x = 40 + (i % 6) * (w + g); y = 70 + (i // 6) * 78
        b += (f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="10" fill="{c["card"]}" fill-opacity=".85" stroke="{c["line"]}" stroke-width="1.4"/>'
              f'<text x="{x+w/2}" y="{y+29}" font-size="18" font-weight="700" text-anchor="middle" fill="{c["acc"]}">{mono}</text>'
              f'<text x="{x+w/2}" y="{y+50}" font-size="11" text-anchor="middle" fill="{c["fg"]}">{name}</text>')
    b += divider(c, 238)
    return wrap(900, 250, c, b)

def projects_title(c):
    return wrap(900, 62, c, title(c, 36, "Selected Projects"))

def card(c, name, d1, d2, tags, box):
    w, h = 208, 172
    img = crop64(box, (400, 108), 80)
    b = (f'<defs><clipPath id="cl"><rect x="8" y="8" width="{w-16}" height="52" rx="6"/></clipPath></defs>'
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{c["card"]}" stroke="{c["acc"]}" stroke-opacity=".8" stroke-width="1.5"/>'
         f'<image x="8" y="8" width="{w-16}" height="52" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)" href="{img}" xlink:href="{img}"/>'
         f'<rect x="8" y="8" width="{w-16}" height="52" rx="6" fill="none" stroke="{c["acc2"]}" stroke-opacity=".7"/>'
         f'<text x="16" y="86" font-size="14" font-weight="700" fill="{c["fg"]}">{name}</text>'
         f'<text x="16" y="106" font-size="10.5" fill="{c["mute"]}">{d1}</text>'
         f'<text x="16" y="120" font-size="10.5" fill="{c["mute"]}">{d2}</text>')
    x = 16
    for t in tags:
        cw = len(t) * 5.1 + 10
        b += (f'<rect x="{x}" y="138" width="{cw:.1f}" height="17" rx="8.5" fill="none" stroke="{c["line"]}"/>'
              f'<text x="{x+cw/2:.1f}" y="150" font-size="8.5" text-anchor="middle" fill="{c["acc"]}">{t}</text>')
        x += cw + 5
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">{defs(c)}{b}</svg>')

def footer(c):
    img = crop64((0, 640, 735, 745), (900, 129), 78)
    b = (f'<image x="0" y="0" width="900" height="129" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/>'
         f'<rect width="900" height="120" fill="{c["bg2"]}" fill-opacity=".62"/>'
         f'<text x="450" y="52" font-size="19" font-weight="700" font-family="{SERIF}" text-anchor="middle" fill="{c["acc2"] if c is THEMES["dark"] else c["fg"]}" xml:space="preserve">Build  ·  Explore  ·  Understand</text>'
         f'<text x="450" y="80" font-size="11" text-anchor="middle" fill="{c["fg"]}" xml:space="preserve">Software Engineering  ·  Systems  ·  AI  ·  Mathematics</text>')
    b += star(120, 60, 7, c["acc2"]) + star(780, 60, 7, c["acc2"])
    return wrap(900, 120, c, b)

def save(name, theme, svg):
    svg = re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", svg)
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f: f.write(svg)

for th, c in THEMES.items():
    save("header", th, header(c)); save("about", th, about(c)); save("skills", th, skills(c))
    save("projects-title", th, projects_title(c)); save("footer", th, footer(c))
    for lbl in ("GitHub", "LinkedIn", "Portfolio"): save(f"btn-{lbl.lower()}", th, button(c, lbl))
    for n, slug, d1, d2, tags, box in PROJECTS: save(f"card-{slug}", th, card(c, n, d1, d2, tags, box))

def pic(name, alt, width=None, href=None):
    w = f' width="{width}"' if width else ""
    p = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'  <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'  <img alt="{alt}" src="assets/{name}-dark.svg"{w}>\n</picture>')
    return f'<a href="{href}">{p}</a>' if href else p

def cards(items):
    return "\n".join(pic(f"card-{s}", n, "24%", f"{GITHUB}/{s}") for n, s, *_ in items)

parts = [pic("header", f"{NAME} — Software Engineer", "100%"),
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
