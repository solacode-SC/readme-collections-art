#!/usr/bin/env python3
"""Illuminated-codex edition (Book-of-Hours / 15th-century manuscript language).  Needs: pip install pillow
Image  -> framed 'miniature' in the hero + micro crops for project cards and avatar.
Codex  -> vellum + grain, gold-leaf frames with shimmer, illuminated drop caps, vine borders,
          ultramarine octagon lattice (from the image's window panels), Roman folio numbers,
          dot-leader table of contents, 'Explicit' colophon footer with roof, cat and lanterns."""
import io, base64, math, os, random, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
ART = Image.open(os.path.join(HERE, "art", "source.jpg"))
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Book Antiqua','DejaVu Serif',serif"

THEMES = {
 "light": dict(bg1="#f7edcc", bg2="#e9d6a2", fg="#2a2118", ink="#2a1d12", mute="#6b5a43", blue="#1d3f94", blue2="#2f5fc4",
               verm="#c4321f", gold="#b3841c", line="#c7ad70", card="#fbf3d8", cream="#fbf1d0", teal="#2b8484", orange="#e8892a",
               grain="0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .1  0 0 0 .20 0", petals=["#2b57c4", "#6c8fe0", "#d9a52a", "#e8892a"]),
 "dark":  dict(bg1="#0f1c47", bg2="#070d26", fg="#f4e9c9", ink="#080c1e", mute="#b9ac8a", blue="#1a3270", blue2="#4a74e0",
               verm="#e5583e", gold="#e8c45a", line="#4a5a98", card="#12224f", cream="#f4e9c9", teal="#4cb0aa", orange="#ff9a45",
               grain="0 0 0 0 .95  0 0 0 0 .85  0 0 0 0 .6  0 0 0 .09 0", petals=["#7fa2ff", "#bcd0ff", "#f1cd6a", "#ff9a45"]),
}

# ---------- your content: edit here ----------
NAME_INITIAL, NAME_REST = "S", "olayman El Mouden"
GITHUB = "https://github.com/solacode-SC"
LINKEDIN = "https://www.linkedin.com/in/YOUR-LINKEDIN"   # <- change me
PORTFOLIO = "https://solaymantech.me"
JOURNEY = [("C / C++", "Systems"), ("Python", "Backend & AI"), ("TypeScript", "Web & Tools"),
           ("Docker", "Infrastructure"), ("Linux", "DevOps")]
SKILLS = [("C/C++", "C++"), ("Python", "Py"), ("JavaScript", "JS"), ("TypeScript", "TS"), ("React", "Rx"),
          ("Next.js", "N"), ("Django", "dj"), ("FastAPI", "FA"), ("PostgreSQL", "Pg"), ("Docker", "Dk"),
          ("Linux", "Lx"), ("Git", "Git")]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII"]
# (title, slug, line1, line2, tags, micro-crop box in source.jpg [~200x94])
PROJECTS = [
 ("LazyEquation", "lazyequation", "Interactive math & physics", "visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"], (98, 115, 298, 209)),
 ("LeetResume", "leetresume", "AI-powered resume", "builder and optimizer.", ["Next.js", "Prisma", "Postgres"], (500, 440, 700, 534)),
 ("Libora", "libora", "Flutter PDF reader with", "modern experience.", ["Flutter", "Dart", "Riverpod"], (350, 200, 550, 294)),
 ("Webserv", "webserv", "C++98 HTTP server", "from scratch.", ["C++98", "Networking"], (200, 360, 400, 454)),
 ("solaJobs v2", "solajobs-v2", "Arabic-first job board", "platform.", ["Arabic-first", "Jobs"], (50, 670, 250, 764)),
 ("Alert Generator", "prometheus-alert-generator", "AI generator for", "Prometheus alert rules.", ["AI", "Prometheus"], (130, 840, 330, 934)),
 ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose", "dashboard.", ["Docker", "Compose"], (420, 560, 620, 654)),
]
# ---------------------------------------------

def crop64(box, size, q=82):
    im = ART.crop(box).resize(size, Image.LANCZOS); buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

STYLE = '''<style>
.spin{transform-box:fill-box;transform-origin:center;animation:spin 80s linear infinite}
.spin.r{animation-direction:reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.tw{transform-box:fill-box;transform-origin:center;animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.3;transform:scale(.6)}50%{opacity:1;transform:scale(1.15)}}
.flick{animation:fl 2.8s ease-in-out infinite}
@keyframes fl{0%,100%{opacity:.65}30%{opacity:1}55%{opacity:.5}80%{opacity:.95}}
.glow{animation:glow 6s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:.95}}
.ff{animation:ff linear infinite;opacity:0}
@keyframes ff{0%{opacity:0;transform:translate(0,0)}15%{opacity:1}85%{opacity:.9}100%{opacity:0;transform:translate(14px,-70px)}}
.fall{animation:fall linear infinite}
@keyframes fall{from{transform:translateY(-30px)}to{transform:translateY(540px)}}
.sway{transform-box:fill-box;transform-origin:center;animation:sway ease-in-out infinite alternate}
@keyframes sway{from{transform:translateX(-22px) rotate(-40deg)}to{transform:translateX(22px) rotate(40deg)}}
.leafsway{transform-box:fill-box;transform-origin:50% 100%;animation:ls 6s ease-in-out infinite alternate}
@keyframes ls{from{transform:rotate(-8deg)}to{transform:rotate(8deg)}}
.sweep{animation:sweep 9s ease-in-out infinite}
@keyframes sweep{0%,55%{transform:translateX(-380px)}100%{transform:translateX(480px)}}
.tail{transform-box:fill-box;transform-origin:0% 100%;animation:tail 4.5s ease-in-out infinite alternate}
@keyframes tail{from{transform:rotate(-9deg)}to{transform:rotate(12deg)}}
.swing{transform-box:fill-box;transform-origin:50% 0%;animation:swing 5s ease-in-out infinite alternate}
@keyframes swing{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}
.cursor{animation:cur 1.1s steps(1) infinite}
@keyframes cur{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.spin,.tw,.flick,.glow,.ff,.fall,.sway,.leafsway,.sweep,.tail,.swing,.cursor{animation:none}.ff{opacity:.6}}
</style>'''

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")
def star4(x, y, s, col, op=1, cls="", delay=0):
    d = f"M{f1(x)} {f1(y-s)}Q{f1(x)} {f1(y)} {f1(x+s)} {f1(y)}Q{f1(x)} {f1(y)} {f1(x)} {f1(y+s)}Q{f1(x)} {f1(y)} {f1(x-s)} {f1(y)}Q{f1(x)} {f1(y)} {f1(x)} {f1(y-s)}Z"
    st = f' style="animation-delay:{-delay:.1f}s;animation-duration:{3+delay%3:.1f}s"' if cls else ""
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}"{st}/>'

def quatrefoil(x, y, s, c):
    o = "".join(f'<circle cx="{f1(x+dx*s)}" cy="{f1(y+dy*s)}" r="{f1(s*.62)}" fill="url(#gold)" stroke="{c["ink"]}" stroke-width=".6"/>' for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return o + f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{f1(s*.55)}" fill="{c["verm"]}" stroke="{c["ink"]}" stroke-width=".6"/>'

def spiral(cx, cy, r, turns=2, rot=0):
    pts = []; n = int(turns * 20)
    for i in range(n + 1):
        t = i / n; th = t * turns * 2 * math.pi + rot; rr = r * (.12 + .88 * (1 - t))
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    return "M" + "L".join(f"{f1(x)} {f1(y)}" for x, y in pts)

LEAF = "M0 0C6 -3 11 -11 5 -17C2 -13 0 -13 -2 -17C-8 -11 -6 -3 0 0Z"
def vine(c, x0, x1, y, seed=1, amp=4):
    r = random.Random(seed); o = []
    stem = [(x, y + amp * math.sin(x / 28)) for x in range(int(x0), int(x1) + 1, 5)]
    o.append(f'<path d="M{"L".join(f"{f1(a)} {f1(b)}" for a,b in stem)}" fill="none" stroke="{c["gold"]}" stroke-width="1.4"/>')
    k = 0
    for x in range(int(x0) + 20, int(x1) - 10, 38):
        yy = y + amp * math.sin(x / 28); up = k % 2 == 0; sgn = -1 if up else 1
        o.append(f'<path d="{spiral(x + 6, yy + sgn * 9, 8, 2, r.uniform(0, 6))}" fill="none" stroke="{c["gold"]}" stroke-width="1.1"/>')
        o.append(f'<circle cx="{x+6}" cy="{f1(yy+sgn*9)}" r="2.4" fill="{c["verm"]}"/>')
        col = c["blue2"] if k % 3 else c["teal"]
        o.append(f'<g class="leafsway" style="animation-delay:{-r.uniform(0,6):.1f}s"><path transform="translate({x-10} {f1(yy)}) rotate({-35 if up else 145}) scale(.9)" d="{LEAF}" fill="{col}" stroke="{c["ink"]}" stroke-width=".5"/></g>')
        o.append(f'<circle cx="{x+20}" cy="{f1(yy+(-5 if up else 5))}" r="1.8" fill="url(#gold)"/>')
        k += 1
    return "".join(o)

def defs(c, w, h):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a6212"/><stop offset=".3" stop-color="#f3dc84"/><stop offset=".55" stop-color="#c79a2e"/><stop offset=".8" stop-color="#f7e9a8"/><stop offset="1" stop-color="#9a7218"/></linearGradient>
<linearGradient id="shim" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".4" stop-color="#ffb347" stop-opacity=".4"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="stain"><stop offset="0" stop-color="{c['gold']}" stop-opacity=".16"/><stop offset="1" stop-color="{c['gold']}" stop-opacity="0"/></radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix values="{c['grain']}"/></filter>
</defs>'''

def wrap(w, h, c, body, frame=True):
    side = f'<path d="M.5 0V{h}M{w-.5} 0V{h}" stroke="{c["line"]}"/>' if frame else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SERIF}">'
            f'{STYLE}{defs(c, w, h)}<rect width="{w}" height="{h}" fill="url(#bg)"/>'
            f'<ellipse cx="{w*.2}" cy="{h*.3}" rx="{w*.3}" ry="{h*.5}" fill="url(#stain)"/><ellipse cx="{w*.85}" cy="{h*.8}" rx="{w*.25}" ry="{h*.5}" fill="url(#stain)"/>'
            f'<rect width="{w}" height="{h}" filter="url(#grain)"/>{body}{side}</svg>')

def petals(c, n, xr, seed=3):
    r = random.Random(seed); o = []
    for _ in range(n):
        x = r.uniform(*xr); s = r.uniform(.6, 1.15); col = r.choice(c["petals"]); d = r.uniform(16, 28); sd = r.uniform(3.5, 6.5)
        o.append(f'<g transform="translate({f1(x)} 0)"><g class="fall" style="animation-duration:{d:.1f}s;animation-delay:{-r.uniform(0,d):.1f}s">'
                 f'<g class="sway" style="animation-duration:{sd:.1f}s;animation-delay:{-r.uniform(0,sd):.1f}s">'
                 f'<path transform="rotate({r.uniform(0,180):.0f}) scale({s:.2f})" d="M0 -8C6 -6 7 4 0 9C-7 4 -6 -6 0 -8Z" fill="{col}" opacity=".9"/></g></g></g>')
    return "".join(o)

def sparks(n, centers, seed=5, spread=14):
    r = random.Random(seed); o = []
    for i in range(n):
        cx, cy = centers[i % len(centers)]; x, y = cx + r.uniform(-spread, spread), cy + r.uniform(-4, spread); d = r.uniform(6, 12)
        o.append(f'<g class="ff" style="animation-duration:{d:.1f}s;animation-delay:{-r.uniform(0,d):.1f}s">'
                 f'<circle cx="{f1(x)}" cy="{f1(y)}" r="4.5" fill="#ffd57a" opacity=".25"/><circle cx="{f1(x)}" cy="{f1(y)}" r="1.7" fill="#fff0b8"/></g>')
    return "".join(o)

def divider(c, y, seed=1): return vine(c, 40, 860, y, seed, 3)

def heading(c, y, numeral, label, x=60):
    return (f'<text x="{x}" y="{y+5}" font-size="20" fill="{c["verm"]}">¶</text>'
            f'<text x="{x+22}" y="{y+4}" font-size="10.5" font-family="{MONO}" letter-spacing="2" fill="{c["verm"]}">CAPUT {numeral}</text>'
            f'<text x="{x+102}" y="{y+5}" font-size="15" font-weight="700" letter-spacing="3" fill="{c["fg"]}">{label}</text>'
            f'<path d="M{x} {y+16}H{x+300}" stroke="url(#gold)" stroke-width="1.6"/>' + quatrefoil(x + 306, y + 16, 3.2, c))

def dropcap(c, x, y, s, letter, fs):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="url(#gold)" stroke="{c["ink"]}" stroke-width="1.2"/>'
            f'<rect x="{x+s*.09}" y="{y+s*.09}" width="{s*.82}" height="{s*.82}" fill="{c["blue"]}" stroke="{c["ink"]}" stroke-width=".8"/>'
            f'<path d="M{x+s*.09} {y+s*.09}l{s*.18} {s*.18}M{x+s*.91} {y+s*.09}l-{s*.18} {s*.18}M{x+s*.09} {y+s*.91}l{s*.18} -{s*.18}M{x+s*.91} {y+s*.91}l-{s*.18} -{s*.18}" stroke="{c["gold"]}" stroke-opacity=".8"/>'
            f'<text x="{x+s/2}" y="{y+s*.74}" font-size="{fs}" font-weight="700" text-anchor="middle" fill="{c["cream"]}" stroke="{c["ink"]}" stroke-width=".6">{letter}</text>')

# ---------- panels ----------
S = .4312  # hero miniature scale for the image (see mapping below)
def mp(x, y): return 560 + x * S - 8.7, 40 + (y - 22) * S

def hero(c):
    img = crop64((0, 22, 736, 996), (620, 820), 82)
    av = crop64((390, 200, 490, 300), (64, 64), 82)
    arch = "M560 150A150 110 0 0 1 860 150V460H560Z"
    b = ""
    # frame + corner ornaments
    b += (f'<rect x="10" y="10" width="880" height="480" fill="none" stroke="url(#gold)" stroke-width="3"/>'
          f'<rect x="17" y="17" width="866" height="466" fill="none" stroke="{c["blue2"]}" stroke-width="1"/>')
    for (x, y) in ((10, 10), (890, 10), (10, 490), (890, 490)): b += quatrefoil(x, y, 7, c)
    for (x, y) in ((450, 10), (450, 490)): b += quatrefoil(x, y, 4.5, c)
    # top bar + avatar
    b += (f'<defs><clipPath id="av"><circle cx="64" cy="52" r="14"/></clipPath></defs>'
          f'<image x="50" y="38" width="28" height="28" clip-path="url(#av)" href="{av}" xlink:href="{av}"/>'
          f'<circle cx="64" cy="52" r="14" fill="none" stroke="url(#gold)" stroke-width="2"/>'
          f'<text x="88" y="56" font-size="12" font-family="{MONO}" fill="{c["mute"]}">solacode-SC <tspan fill="{c["verm"]}">/</tspan> README</text>')
    # copy
    b += (f'<text x="58" y="112" font-size="14" letter-spacing="3" fill="{c["verm"]}">¶ <tspan fill="{c["mute"]}">HI, I\'M</tspan></text>'
          + dropcap(c, 58, 124, 72, NAME_INITIAL, 58) +
          f'<text x="140" y="168" font-size="38" fill="{c["fg"]}">{NAME_REST}</text>'
          f'<text x="60" y="232" font-size="15" font-weight="700" letter-spacing="4" fill="{c["blue2"] if c is THEMES["light"] else c["gold"]}">SOFTWARE ENGINEER</text>'
          f'<rect class="cursor" x="326" y="219" width="8" height="15" fill="{c["verm"]}"/>'
          f'<text x="60" y="268" font-size="14" letter-spacing="1.5" fill="{c["fg"]}" xml:space="preserve">AI  ·  Math  ·  Newest Technologies</text>'
          f'<path d="M60 286H280" stroke="url(#gold)" stroke-width="1.6"/>' + quatrefoil(286, 286, 3.2, c))
    for i, t in enumerate(["Building systems, web applications,", "developer tools and intelligent software", "for a better tomorrow."]):
        b += f'<text x="60" y="{318+i*22}" font-size="14" font-style="italic" fill="{c["mute"]}">{t}</text>'
    # miniature
    b += (f'<defs><clipPath id="arch"><path d="{arch}"/></clipPath></defs>'
          f'<g clip-path="url(#arch)"><image x="560" y="40" width="300" height="420" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/>')
    (mx, my), (lx, ly), (bx, by), (tx, ty), (ex, ey) = mp(198, 160), mp(250, 640), mp(195, 905), mp(650, 310), mp(425, 258)
    b += (f'<circle class="glow" cx="{f1(mx)}" cy="{f1(my)}" r="54" fill="url(#warm)"/>'
          f'<circle class="flick" cx="{f1(lx)}" cy="{f1(ly)}" r="34" fill="url(#warm)"/>'
          f'<circle class="flick" cx="{f1(bx)}" cy="{f1(by)}" r="30" fill="url(#warm)" style="animation-delay:-1.2s"/>'
          f'<circle class="flick" cx="{f1(tx)}" cy="{f1(ty)}" r="30" fill="url(#warm)" style="animation-delay:-2s"/>'
          + star4(ex, ey, 6, "#fff3b0", 1, "tw", 1) +
          f'<g class="sweep"><rect x="470" y="10" width="70" height="520" fill="url(#shim)" transform="rotate(16 560 250)"/></g></g>'
          f'<path d="{arch}" fill="none" stroke="{c["ink"]}" stroke-width="9"/><path d="{arch}" fill="none" stroke="url(#gold)" stroke-width="6"/>'
          f'<path d="{arch}" fill="none" stroke="{c["blue2"]}" stroke-width="1.2"/>')
    b += quatrefoil(710, 36, 5, c) + vine(c, 40, 860, 474, 3, 3)
    b += sparks(10, [(lx, ly), (bx, by), (tx, ty), (mx + 20, my + 30)], 8) + petals(c, 12, (300, 880), 6)
    return wrap(900, 500, c, b)

def button(c, label):
    w = 150
    b = (f'<rect x=".75" y=".75" width="{w-1.5}" height="38.5" rx="3" fill="{c["card"]}" stroke="url(#gold)" stroke-width="2"/>'
         f'<rect x="4" y="4" width="{w-8}" height="32" rx="1.5" fill="none" stroke="{c["blue2"]}" stroke-opacity=".7"/>'
         + quatrefoil(22, 20, 3.4, c) +
         f'<text x="38" y="24.5" font-size="12" letter-spacing="2" fill="{c["fg"]}">{label.upper()}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" font-family="{SERIF}"><defs><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a6212"/><stop offset=".3" stop-color="#f3dc84"/><stop offset=".55" stop-color="#c79a2e"/><stop offset=".8" stop-color="#f7e9a8"/><stop offset="1" stop-color="#9a7218"/></linearGradient></defs>{b}</svg>'

def about(c):
    b = heading(c, 42, "I", "ABOUT")
    b += dropcap(c, 60, 78, 36, "I", 30)
    L1 = [(106, 92, "'m Solayman El Mouden, a software engineer"), (106, 112, "focused on systems, web technologies,"),
          (60, 136, "artificial intelligence and mathematics."),
          (60, 176, "I enjoy understanding how things work underneath"), (60, 196, "the abstraction and turning that knowledge into"),
          (60, 216, "useful software.")]
    for x, y, t in L1: b += f'<text x="{x}" y="{y}" font-size="14" fill="{c["fg"]}">{t}</text>'
    b += f'<path d="M450 76V236" stroke="url(#gold)" stroke-width="1.3"/>' + quatrefoil(450, 76, 3, c) + quatrefoil(450, 236, 3, c)
    b += heading(c, 42, "II", "MY JOURNEY", 480)
    for i, (a, t) in enumerate(JOURNEY):
        y = 98 + i * 30
        b += (quatrefoil(490, y - 4, 2.6, c) +
              f'<text x="506" y="{y}" font-size="14" fill="{c["fg"]}">{a}</text>'
              f'<path d="M600 {y}H690" stroke="{c["gold"]}" stroke-width="1.6" stroke-dasharray="1 5" stroke-linecap="round"/>'
              f'<text x="700" y="{y}" font-size="14" font-style="italic" fill="{c["mute"]}">{t}</text>')
    b += divider(c, 276, 5)
    return wrap(900, 296, c, b)

def octagon(cx, cy, R, rot=22.5):
    return "M" + "L".join(f"{f1(cx+R*math.cos(math.radians(rot+45*i)))} {f1(cy+R*math.sin(math.radians(rot+45*i)))}" for i in range(8)) + "Z"

def skills(c):
    b = heading(c, 40, "III", "TECHNOLOGIES &amp; SKILLS")
    bx, by, bw, bh = 40, 64, 820, 232
    b += (f'<defs><pattern id="lat" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0H34M0 0V34" stroke="{c["gold"]}" stroke-opacity=".22"/></pattern></defs>'
          f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{c["blue"]}" stroke="url(#gold)" stroke-width="3"/>'
          f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#lat)"/>'
          f'<rect x="{bx+6}" y="{by+6}" width="{bw-12}" height="{bh-12}" fill="none" stroke="{c["gold"]}" stroke-opacity=".5"/>')
    for i, (name, mono) in enumerate(SKILLS):
        cx = bx + 68.3 + (i % 6) * 136.7; cy = by + 56 + (i // 6) * 104
        b += (f'<path d="{octagon(cx, cy, 42)}" fill="url(#gold)" stroke="{c["ink"]}" stroke-width="1.6"/>'
              f'<path d="{octagon(cx, cy, 34)}" fill="none" stroke="{c["ink"]}" stroke-opacity=".55"/>'
              f'<g class="spin{" r" if i % 2 else ""}"><path d="{spiral(cx, cy, 25, 2.2, i)}" fill="none" stroke="{c["ink"]}" stroke-opacity=".28" stroke-width="1.3"/></g>'
              f'<text x="{f1(cx)}" y="{cy+6}" font-size="17" font-weight="700" text-anchor="middle" fill="{c["blue"] if c is THEMES["light"] else c["ink"]}">{mono}</text>'
              f'<text x="{f1(cx)}" y="{cy+60}" font-size="11.5" font-style="italic" text-anchor="middle" fill="{c["cream"]}">{name}</text>'
              + star4(cx + 30, cy - 30, 4, "#fff3b0", .9, "tw", i * .9))
    b += divider(c, 318, 6)
    return wrap(900, 338, c, b)

def projects_title(c): return wrap(900, 60, c, heading(c, 32, "IV", "SELECTED PROJECTS"))

def card(c, idx, name, d1, d2, tags, box):
    w, h = 208, 206
    img = crop64(box, (400, 188), 82)
    b = (f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" fill="{c["card"]}" stroke="url(#gold)" stroke-width="3"/>'
         f'<rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="{c["blue2"]}" stroke-opacity=".8"/>'
         f'<image x="12" y="12" width="184" height="86" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/>'
         f'<rect x="12" y="12" width="184" height="86" fill="none" stroke="{c["ink"]}" stroke-width="1.4"/>'
         f'<rect x="12" y="12" width="26" height="18" fill="{c["verm"]}"/><text x="25" y="25" font-size="10.5" font-weight="700" text-anchor="middle" fill="{c["cream"]}">{ROMAN[idx]}</text>'
         f'<g clip-path="url(#sc{idx})"><g class="sweep" style="animation-duration:{10+idx}s"><rect x="-40" y="0" width="30" height="110" fill="url(#shim)" transform="rotate(16 0 50)"/></g></g>'
         f'<defs><clipPath id="sc{idx}"><rect x="12" y="12" width="184" height="86"/></clipPath></defs>'
         f'<text x="16" y="123" font-size="15" font-weight="700" fill="{c["fg"]}">{name}</text>'
         f'<text x="16" y="142" font-size="11.5" font-style="italic" fill="{c["mute"]}">{d1}</text>'
         f'<text x="16" y="157" font-size="11.5" font-style="italic" fill="{c["mute"]}">{d2}</text>')
    x = 16
    for t in tags:
        cw = len(t) * 5.1 + 10
        b += (f'<rect x="{f1(x)}" y="170" width="{f1(cw)}" height="17" rx="2" fill="none" stroke="{c["gold"]}"/>'
              f'<text x="{f1(x+cw/2)}" y="181.5" font-size="8.5" font-family="{MONO}" text-anchor="middle" fill="{c["blue2"] if c is THEMES["light"] else c["gold"]}">{t}</text>')
        x += cw + 5
    for (qx, qy) in ((1.5, 1.5), (w - 1.5, 1.5), (1.5, h - 1.5), (w - 1.5, h - 1.5)): b += quatrefoil(qx, qy, 3, c)
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SERIF}">{STYLE}{defs(c, w, h)}{b}</svg>'

def cat(c, x, y, k=1.0):
    col = "#0b0a10" if c is THEMES["light"] else "#05060d"
    return (f'<g transform="translate({x} {y}) scale({k})"><g class="tail"><path d="M82 96C108 94 112 66 98 56" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/></g>'
            f'<path d="M30 100C22 80 26 62 36 52C34 44 36 38 40 34L36 12L48 22C52 21 56 21 60 22L72 10L72 34C76 40 78 46 76 52C90 62 94 84 88 100Z" fill="{col}"/>'
            f'<ellipse cx="46" cy="34" rx="3.6" ry="2.4" fill="#f2c64a"/>' + star4(46, 34, 5, "#fff3b0", .9, "tw", 2) + '</g>')

def lantern(c, x, y0, ln, k=1.0, delay=0):
    y = y0 + ln
    return (f'<g class="swing" style="animation-delay:-{delay}s"><path d="M{x} {y0}V{y-14}" stroke="{c["gold"]}" stroke-width="1.2"/>'
            f'<circle class="flick" cx="{x}" cy="{y+4}" r="34" fill="url(#warm)" style="animation-delay:-{delay}s"/>'
            f'<rect x="{x-7}" y="{y-14}" width="14" height="4" fill="{c["ink"]}"/><path d="M{x-10} {y-10}H{x+10}L{x+12} {y+14}H{x-12}Z" fill="{c["orange"]}" stroke="{c["ink"]}" stroke-width="1.2"/>'
            f'<path d="M{x-10} {y+2}H{x+10}" stroke="{c["ink"]}" stroke-opacity=".5"/><rect x="{x-9}" y="{y+14}" width="18" height="4" fill="{c["ink"]}"/></g>')

def footer(c):
    b = f'<text x="60" y="78" font-size="11" font-family="{MONO}" letter-spacing="4" fill="{c["verm"]}">EXPLICIT LIBER</text>'
    b += (f'<text x="60" y="118" font-size="20" font-weight="700" letter-spacing="3" fill="{c["fg"]}" xml:space="preserve">BUILD  ·  EXPLORE  ·  UNDERSTAND</text>'
          f'<path d="M60 134H470" stroke="url(#gold)" stroke-width="1.6"/>' + quatrefoil(476, 134, 3.2, c) +
          f'<text x="60" y="160" font-size="13" font-style="italic" fill="{c["mute"]}">Software Engineering · Systems · AI · Mathematics</text>')
    # moon
    b += (f'<circle class="glow" cx="640" cy="64" r="58" fill="url(#warm)"/><circle cx="640" cy="64" r="36" fill="{c["orange"]}" stroke="{c["ink"]}" stroke-width="1.6"/>'
          f'<g class="spin"><path d="{spiral(640, 64, 26, 2.6)}" fill="none" stroke="#fff3c4" stroke-width="2.4" stroke-linecap="round"/></g>')
    # roof with upturned eave
    roof = "M560 138C560 124 574 112 590 104C582 122 600 134 632 138L870 138V156H632C600 154 570 148 560 138Z"
    b += (f'<path d="{roof}" fill="{c["blue2"] if c is THEMES["dark"] else c["blue"]}" stroke="{c["ink"]}" stroke-width="1.6"/>'
          + "".join(f'<path d="M{x} 140V154" stroke="{c["ink"]}" stroke-opacity=".5"/>' for x in range(640, 870, 14)) +
          f'<path d="M632 138H870" stroke="url(#gold)" stroke-width="2.4"/>')
    b += cat(c, 758, 38, .98)
    for i, (x, ln) in enumerate([(650, 28), (700, 52), (760, 34), (810, 60), (850, 36)]): b += lantern(c, x, 156, ln, 1, i * .7)
    b += vine(c, 40, 540, 214, 7, 3) + sparks(10, [(650, 190), (760, 200), (850, 195), (700, 215)], 3) + petals(c, 6, (40, 560), 11)
    return wrap(900, 240, c, b)

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
         f'  <img alt="{alt}" src="assets/{name}-light.svg"{w}>\n</picture>')
    return f'<a href="{href}">{p}</a>' if href else p

def cards(items): return "\n".join(pic(f"card-{s}", n, "24%", f"{GITHUB}/{s}") for n, s, *_ in items)

parts = [pic("hero", "Solayman El Mouden — Software Engineer. AI, Math, Newest Technologies.", "100%"),
         "<br>\n" + "&nbsp;\n".join(pic(f"btn-{l.lower()}", l, href=u) for l, u in (("GitHub", GITHUB), ("LinkedIn", LINKEDIN), ("Portfolio", PORTFOLIO))),
         pic("about", "About and journey", "100%"), pic("skills", "Technologies and skills", "100%"),
         pic("projects-title", "Selected projects", "100%"), cards(PROJECTS[:4]), cards(PROJECTS[4:]),
         pic("footer", "Explicit liber. Build, Explore, Understand", "100%"),
         f'<sub><a href="{PORTFOLIO}">solaymantech.me</a> &nbsp;·&nbsp; <a href="{LINKEDIN}">LinkedIn</a></sub>']
with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
    f.write('<div align="center">\n\n' + "\n\n".join(parts) + "\n\n</div>\n")
print("done")
