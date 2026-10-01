#!/usr/bin/env python3
"""Generates dark/light SVG panels + README.md for the solacode-SC profile."""
import os, random
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
FONT = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
JP = "'Noto Sans JP','Yu Gothic','Hiragino Sans',sans-serif"

THEMES = {
 "dark": dict(bg1="#060b2e", bg2="#03061a", fg="#dfe7ff", mute="#8fa3e8", acc="#5b8cff", acc2="#9ab6ff",
              line="#2b3c9e", card="#0a1347", deep="#1b2fb0", mid="#3d63e8", lite="#9fb8ff",
              dot="#8fb0ff", ring="#bcd0ff"),
 "light": dict(bg1="#fbfbfe", bg2="#eff3fb", fg="#16205a", mute="#4b5fa8", acc="#2f54d6", acc2="#1f3bb3",
               line="#9fb2ee", card="#eaeffc", deep="#1b2fb0", mid="#3d63e8", lite="#b9c9f7",
               dot="#2a3f9c", ring="#e6edff"),
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
PROJECTS = [("LazyEquation", "Interactive math & physics", "visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"]),
            ("LeetResume", "AI-powered resume", "builder and optimizer.", ["Next.js", "Prisma", "Postgres"]),
            ("Libora", "Flutter PDF reader with", "modern experience.", ["Flutter", "Dart", "Riverpod"]),
            ("Webserv", "C++98 HTTP server", "from scratch.", ["C++98", "Networking"])]
REPO = lambda n: f"{GITHUB}/{n.lower()}"
S1337 = [("minishell", "Shell & processes", ">_"), ("philosophers", "Threads & sync", "φ"), ("ft_irc", "IRC server", "#"),
         ("Inception", "Docker & services", "[]"), ("cub3d", "3D raycasting", "3D"), ("webserv", "HTTP server", "<>")]
# ---------------------------------------------

def defs(c):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{c['line']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['line']}"/><stop offset="1" stop-color="{c['line']}" stop-opacity="0"/></linearGradient>
<radialGradient id="g0" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="{c['lite']}"/><stop offset=".5" stop-color="{c['mid']}"/><stop offset="1" stop-color="{c['deep']}"/></radialGradient>
<radialGradient id="g1" cx=".6" cy=".7" r=".9"><stop offset="0" stop-color="{c['mid']}"/><stop offset="1" stop-color="{c['deep']}"/></radialGradient>
</defs>'''

def wrap(w, h, c, body, frame=True):
    fr = f'<path d="M.75 0V{h}M{w-.75} 0V{h}" stroke="{c["line"]}" stroke-width="1.5"/>' if frame else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">'
            f'{defs(c)}<rect width="{w}" height="{h}" fill="url(#bg)"/>{body}{fr}</svg>')

def star(x, y, s, col, op=1):
    return f'<path d="M{x} {y-s}Q{x} {y} {x+s} {y}Q{x} {y} {x} {y+s}Q{x} {y} {x-s} {y}Q{x} {y} {x} {y-s}Z" fill="{col}" opacity="{op}"/>'

def art(c, ox, oy, s=1.0, seed=3):
    """Procedural take on the dotted-ring / indigo-wash artwork."""
    r = random.Random(seed); o = []
    blobs = [(0, 0, 105), (-92, -68, 58), (88, -84, 48), (-66, 92, 64), (96, 72, 52), (8, -122, 34), (-120, 20, 30)]
    for i, (x, y, R) in enumerate(blobs):
        X, Y, R = ox + x * s, oy + y * s, R * s
        filled = i % 2 == 0
        if filled:
            o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{R:.1f}" fill="url(#g{(i//2)%2})"/>')
        n = max(2, int(R / (8 * max(s, .5))))
        col = c["ring"] if filled else c["dot"]
        for j in range(1, n + 1):
            rr = R * j / n
            o.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{rr:.1f}" fill="none" stroke="{col}" stroke-width="{max(1.2,2*s):.1f}" '
                     f'stroke-dasharray="0.1 {max(3,4.2*s):.1f}" stroke-linecap="round" opacity="{.95 if filled else .8}"/>')
    for (x, y, a, k) in [(-40, -125, -30, 1), (70, -40, 40, .8), (-100, 60, 200, .9), (40, 130, 120, .7)]:
        o.append(f'<path transform="translate({ox+x*s:.1f} {oy+y*s:.1f}) rotate({a}) scale({k*s:.2f})" '
                 f'd="M0 0C22-34 66-22 54 12C46 34 18 38 8 22C18 20 30 12 25 0C20-12 4-8 0 0Z" '
                 f'fill="{c["mid"]}" stroke="{c["dot"]}" stroke-width="1.5"/>')
    for _ in range(26):
        ang = r.random() * 6.283; d = (150 + r.random() * 60) * s
        o.append(f'<circle cx="{ox+d*__import__("math").cos(ang):.1f}" cy="{oy+d*__import__("math").sin(ang):.1f}" r="{r.random()*1.6+.6:.1f}" fill="{c["dot"]}" opacity=".6"/>')
    return "".join(o)

def title(c, y, label):
    return (f'<circle cx="62" cy="{y}" r="11" fill="none" stroke="{c["acc"]}" stroke-width="2"/>'
            f'<circle cx="62" cy="{y}" r="3.5" fill="{c["acc"]}"/>'
            f'<text x="84" y="{y+6}" font-size="17" font-weight="600" fill="{c["fg"]}">{label}</text>')

def divider(c, y, w=900):
    return (f'<rect x="40" y="{y}" width="{w-80}" height="1" fill="url(#fade)"/>'
            f'<path d="M{w/2} {y-4}l4 4-4 4-4-4z" fill="{c["acc"]}"/>')

# ---------- panels ----------
def header(c):
    b = art(c, 700, 185, 1.0)
    b += star(120, 40, 7, c["acc"]) + star(560, 60, 6, c["acc2"], .8) + star(840, 30, 8, c["acc"])
    b += (f'<text x="60" y="95" font-size="20" fill="{c["mute"]}">Hi, I\'m</text>'
          f'<text x="58" y="148" font-size="40" font-weight="700" fill="{c["fg"]}">{NAME}</text>'
          f'<text x="60" y="198" font-size="24" fill="{c["acc"]}">Software Engineer</text>'
          f'<rect x="298" y="179" width="12" height="22" fill="{c["acc"]}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
          f'<text x="60" y="246" font-size="15" fill="{c["fg"]}" xml:space="preserve">AI   |   Math   |   Newest Technologies</text>')
    for i, t in enumerate(["Building systems, web applications,", "developer tools and intelligent software", "for a better tomorrow."]):
        b += f'<text x="60" y="{288+i*20}" font-size="13" fill="{c["mute"]}">{t}</text>'
    b += (f'<rect x="858" y="52" width="26" height="104" rx="4" fill="{c["card"]}" stroke="{c["line"]}"/>')
    for i, ch in enumerate("夢を築く"):
        b += f'<text x="871" y="{74+i*24}" font-size="15" text-anchor="middle" font-family="{JP}" fill="{c["acc2"]}">{ch}</text>'
    b += divider(c, 345)
    return wrap(900, 360, c, b)

def button(c, label):
    w = 150
    b = (f'<rect x="1" y="1" width="{w-2}" height="38" rx="8" fill="{c["card"]}" stroke="{c["line"]}" stroke-width="1.5"/>'
         + star(24, 20, 6, c["acc"]) +
         f'<text x="40" y="25" font-size="13" fill="{c["fg"]}">{label}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" font-family="{FONT}">{b}</svg>')

def about(c):
    b = title(c, 42, "About")
    L = ["I'm Solayman El Mouden, a software engineer", "focused on systems, web technologies,",
         "artificial intelligence and mathematics.", "", "I enjoy understanding how things work",
         "underneath the abstraction and turning that", "knowledge into useful software."]
    for i, t in enumerate(L):
        b += f'<text x="60" y="{90+i*21}" font-size="13" fill="{c["fg"]}" xml:space="preserve">{t}</text>'
    b += f'<rect x="440" y="75" width="1" height="165" fill="{c["line"]}"/>'
    b += f'<text x="475" y="92" font-size="14" font-weight="600" fill="{c["fg"]}">My journey</text>'
    for i, (a, t) in enumerate(JOURNEY):
        y = 130 + i * 30
        b += (f'<rect x="478" y="{y-12}" width="14" height="14" rx="3" fill="none" stroke="{c["acc"]}"/>'
              f'<text x="504" y="{y}" font-size="13" fill="{c["fg"]}">{a}</text>'
              f'<text x="640" y="{y}" font-size="13" fill="{c["acc"]}">→</text>'
              f'<text x="680" y="{y}" font-size="13" fill="{c["mute"]}">{t}</text>')
    b += star(850, 120, 9, c["acc"], .7) + star(870, 150, 5, c["acc2"], .6)
    b += divider(c, 272)
    return wrap(900, 285, c, b)

def skills(c):
    b = title(c, 38, "Technologies &amp; Skills")
    w, g = 125, 14
    for i, (name, mono) in enumerate(SKILLS):
        x = 40 + (i % 6) * (w + g); y = 70 + (i // 6) * 78
        b += (f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="8" fill="{c["card"]}" stroke="{c["line"]}" stroke-width="1.3"/>'
              f'<text x="{x+w/2}" y="{y+29}" font-size="18" font-weight="700" text-anchor="middle" fill="{c["acc"]}">{mono}</text>'
              f'<text x="{x+w/2}" y="{y+50}" font-size="11" text-anchor="middle" fill="{c["fg"]}">{name}</text>')
    b += divider(c, 238)
    return wrap(900, 250, c, b)

def projects_title(c):
    return wrap(900, 62, c, title(c, 36, "Selected Projects"))

def card(c, idx, name, d1, d2, tags):
    w, h = 208, 172
    b = (f'<defs><clipPath id="cl"><rect x="8" y="8" width="{w-16}" height="52" rx="5"/></clipPath></defs>'
         f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="{c["card"]}" stroke="{c["line"]}" stroke-width="1.5"/>'
         f'<rect x="8" y="8" width="{w-16}" height="52" rx="5" fill="{c["bg2"]}"/>'
         f'<g clip-path="url(#cl)">{art(c, 104, 34, .26, seed=idx+11)}</g>'
         f'<text x="16" y="86" font-size="14" font-weight="700" fill="{c["fg"]}">{name}</text>'
         f'<text x="16" y="106" font-size="10.5" fill="{c["mute"]}">{d1}</text>'
         f'<text x="16" y="120" font-size="10.5" fill="{c["mute"]}">{d2}</text>')
    x = 16
    for t in tags:
        cw = len(t) * 5.1 + 10
        b += (f'<rect x="{x}" y="138" width="{cw:.1f}" height="17" rx="4" fill="none" stroke="{c["line"]}"/>'
              f'<text x="{x+cw/2:.1f}" y="150" font-size="8.5" text-anchor="middle" fill="{c["acc"]}">{t}</text>')
        x += cw + 5
    # the card needs its own defs for gradients
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">{defs(c)}{b}</svg>')

def s1337(c):
    b = title(c, 38, "1337 / UM6P Projects")
    b += f'<rect x="100" y="94" width="700" height="1.5" fill="{c["line"]}"/>'
    for i, (n, sub, g) in enumerate(S1337):
        x = 100 + i * 140
        b += (f'<circle cx="{x}" cy="95" r="19" fill="{c["bg2"]}" stroke="{c["acc"]}" stroke-width="1.8"/>'
              f'<text x="{x}" y="100" font-size="12" font-weight="700" text-anchor="middle" fill="{c["acc"]}">{g.replace("<","&lt;").replace(">","&gt;")}</text>'
              f'<text x="{x}" y="138" font-size="13" text-anchor="middle" fill="{c["fg"]}">{n}</text>'
              f'<text x="{x}" y="156" font-size="10" text-anchor="middle" fill="{c["mute"]}">{sub}</text>')
        if i < 5:
            b += f'<circle cx="{x+70}" cy="95" r="3" fill="{c["acc"]}"/>'
    b += divider(c, 182)
    return wrap(900, 195, c, b)

def footer(c):
    b = art(c, 0, 150, .38, seed=5) + art(c, 900, 150, .38, seed=9)
    b += (f'<text x="450" y="52" font-size="16" text-anchor="middle" fill="{c["acc2"]}" xml:space="preserve">Build  ·  Explore  ·  Understand</text>'
          f'<text x="450" y="80" font-size="11" text-anchor="middle" fill="{c["mute"]}" xml:space="preserve">Software Engineering  ·  Systems  ·  AI  ·  Mathematics</text>')
    return wrap(900, 120, c, b)

import re
def fix_amp(svg):
    return re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", svg)

def save(name, theme, svg):
    svg = fix_amp(svg)
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f: f.write(svg)

for th, c in THEMES.items():
    save("header", th, header(c)); save("about", th, about(c)); save("skills", th, skills(c))
    save("projects-title", th, projects_title(c)); save("1337", th, s1337(c)); save("footer", th, footer(c))
    for lbl in ("GitHub", "LinkedIn", "Portfolio"): save(f"btn-{lbl.lower()}", th, button(c, lbl))
    for i, (n, d1, d2, t) in enumerate(PROJECTS): save(f"card-{n.lower()}", th, card(c, i, n, d1, d2, t))

def pic(name, alt, width=None, href=None):
    w = f' width="{width}"' if width else ""
    p = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
         f'  <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n'
         f'  <img alt="{alt}" src="assets/{name}-dark.svg"{w}>\n</picture>')
    return f'<a href="{href}">{p}</a>' if href else p

parts = [pic("header", f"{NAME} — Software Engineer", "100%"),
         "<br>\n" + "&nbsp;\n".join(pic(f"btn-{l.lower()}", l, href=u) for l, u in
                                    (("GitHub", GITHUB), ("LinkedIn", LINKEDIN), ("Portfolio", PORTFOLIO))),
         pic("about", "About and journey", "100%"), pic("skills", "Technologies and skills", "100%"),
         pic("projects-title", "Selected projects", "100%"),
         "\n".join(pic(f"card-{n.lower()}", n, "24%", REPO(n)) for n, *_ in PROJECTS),
         pic("1337", "1337 / UM6P projects", "100%"), pic("footer", "Build, Explore, Understand", "100%"),
         f'<sub><a href="{PORTFOLIO}">solaymantech.me</a> &nbsp;·&nbsp; <a href="{LINKEDIN}">LinkedIn</a></sub>']
with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
    f.write('<div align="center">\n\n' + "\n\n".join(parts) + "\n\n</div>\n")
print("done")
