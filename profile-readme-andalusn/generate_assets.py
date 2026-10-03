#!/usr/bin/env python3
"""Al-Andalus edition (Alhambra / Granada / Cordoba language).  Needs: pip install pillow
Image  -> stained-glass 'qamariya' window inside a horseshoe arch + micro crops in multifoil card niches.
Andalus-> horseshoe arches, alfiz frame, zellige 8-point-star tilework, khatam medallions, arcade footer
          with pierced lamps, Arabic-Indic numerals, Arabic tagline (optional, USE_ARABIC flag).
Motion -> calm only: slow rosette, light shimmer through the glass, breathing glow, drifting petals,
          lamp glow, water ripples, star twinkle."""
import io, base64, math, os, random, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
ART = Image.open(os.path.join(HERE, "art", "source.jpg"))     # 714 x 1308 (side bars removed)
SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Book Antiqua','DejaVu Serif',serif"
MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace"
ARAB = "'Amiri','Noto Naskh Arabic','Scheherazade New','Traditional Arabic','Geeza Pro','Segoe UI',Tahoma,serif"

THEMES = {
 "light": dict(bg1="#f9eed9", bg2="#ecd8b6", fg="#3a1218", mute="#7a5a52", gold="#a87f1f", gold2="#d9b45a", turq="#176f78", red="#b3162a",
               emer="#2a7a58", line="#cdb27a", card="#fbf3e2", plaster="#f7e9d0", wine="#4a1424", tile="#1b7d86", paper="#fbf2df",
               petals=["#f1a3b2", "#e8798f", "#fbd3cc"], grain="0 0 0 0 .4  0 0 0 0 .25  0 0 0 0 .1  0 0 0 .16 0"),
 "dark":  dict(bg1="#1c0b14", bg2="#0d0609", fg="#f7ead2", mute="#cdb0a2", gold="#dcb85e", gold2="#f3dc92", turq="#38b6bb", red="#e23c52",
               emer="#41a67e", line="#5a3b3a", card="#26101a", plaster="#2b1019", wine="#12060b", tile="#145a62", paper="#f7ead2",
               petals=["#f1a3b2", "#e8798f", "#fbd3cc"], grain="0 0 0 0 .95  0 0 0 0 .8  0 0 0 0 .6  0 0 0 .08 0"),
}

# ---------- your content: edit here ----------
USE_ARABIC = True      # False -> Latin numerals/text only (if readers may lack Arabic fonts)
GITHUB = "https://github.com/solacode-SC"
LINKEDIN = "https://www.linkedin.com/in/YOUR-LINKEDIN"   # <- change me
PORTFOLIO = "https://solaymantech.me"
NAME = "Solayman El Mouden"
JOURNEY = [("C / C++", "Systems"), ("Python", "Backend & AI"), ("TypeScript", "Web & Tools"),
           ("Docker", "Infrastructure"), ("Linux", "DevOps")]
SKILLS = [("C/C++", "C++"), ("Python", "Py"), ("JavaScript", "JS"), ("TypeScript", "TS"), ("React", "Rx"),
          ("Next.js", "N"), ("Django", "dj"), ("FastAPI", "FA"), ("PostgreSQL", "Pg"), ("Docker", "Dk"),
          ("Linux", "Lx"), ("Git", "Git")]
AR_TAGLINE = "أبني · أستكشف · أفهم"      # "I build · I explore · I understand"
BRAND = ("NashirTech", "ناشر تك")
# (title, slug, line1, line2, tags, micro-crop box in source.jpg [~200x95])
PROJECTS = [
 ("LazyEquation", "lazyequation", "Interactive math & physics", "visualization platform.", ["React", "TS", "Fastify", "PostgreSQL"], (380, 20, 580, 115)),
 ("LeetResume", "leetresume", "AI-powered resume", "builder and optimizer.", ["Next.js", "Prisma", "Postgres"], (50, 245, 250, 340)),
 ("Libora", "libora", "Flutter PDF reader with", "modern experience.", ["Flutter", "Dart", "Riverpod"], (220, 540, 420, 635)),
 ("Webserv", "webserv", "C++98 HTTP server", "from scratch.", ["C++98", "Networking"], (330, 720, 530, 815)),
 ("solaJobs v2", "solajobs-v2", "Arabic-first job board", "platform.", ["Arabic-first", "Jobs"], (430, 300, 630, 395)),
 ("Alert Generator", "prometheus-alert-generator", "AI generator for", "Prometheus alert rules.", ["AI", "Prometheus"], (90, 1090, 290, 1185)),
 ("Compose Dashboard", "docker-compose-dashboard", "Docker Compose", "dashboard.", ["Docker", "Compose"], (240, 770, 440, 865)),
]
# ---------------------------------------------

def num(i): return "٠١٢٣٤٥٦٧٨٩"[i] if USE_ARABIC else str(i)
def numstr(n): return "".join(num(int(d)) for d in str(n))

def crop64(box, size, q=82):
    im = ART.crop(box).resize(size, Image.LANCZOS); buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
def full64(size, q=80):
    im = ART.resize(size, Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

STYLE = '''<style>
.rosette{transform-box:fill-box;transform-origin:center;animation:spin 220s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.tw{animation:tw 7s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.35}50%{opacity:1}}
.glow{animation:glow 10s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.05}50%{opacity:.4}}
.sweep{animation:sweep 14s ease-in-out infinite}
@keyframes sweep{0%,50%{transform:translateX(-380px)}100%{transform:translateX(460px)}}
.lamp{animation:lamp 6s ease-in-out infinite}
@keyframes lamp{0%,100%{opacity:.55}50%{opacity:1}}
.rip{transform-box:fill-box;transform-origin:center;animation:rip 10s ease-out infinite;opacity:0}
@keyframes rip{0%{transform:scale(.2);opacity:0}15%{opacity:.7}100%{transform:scale(1.5);opacity:0}}
.pfall{animation:pfall linear infinite}
@keyframes pfall{from{transform:translateY(-30px)}to{transform:translateY(580px)}}
.psway{transform-box:fill-box;transform-origin:center;animation:psway ease-in-out infinite alternate}
@keyframes psway{from{transform:translateX(-26px) rotate(-30deg)}to{transform:translateX(26px) rotate(30deg)}}
.breath{transform-box:fill-box;transform-origin:center;animation:br 24s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1)}to{transform:scale(1.05)}}
@media (prefers-reduced-motion:reduce){.rosette,.tw,.glow,.sweep,.lamp,.rip,.pfall,.psway,.breath{animation:none}}
</style>'''

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")

# ---------- Andalusian geometry ----------
def khatam(cx, cy, R, rot=0):
    """8-point star = two overlapping squares (returns two polygon point strings)."""
    out = []
    for off in (0, 45):
        pts = [(cx + R * math.cos(math.radians(rot + off + 90 * k + 45)), cy + R * math.sin(math.radians(rot + off + 90 * k + 45))) for k in range(4)]
        out.append(" ".join(f"{f1(x)},{f1(y)}" for x, y in pts))
    return out
def star(cx, cy, R, fill, stroke="none", sw=1, rot=0, extra=""):
    a, b = khatam(cx, cy, R, rot)
    return f'<g fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}><polygon points="{a}"/><polygon points="{b}"/></g>'

def horseshoe(cx, ytop, r, ybase, ratio=.88):
    a = r * ratio; cy = ytop + r; d = math.sqrt(r * r - a * a); yl = cy + d
    return f"M{f1(cx-a)} {f1(ybase)}V{f1(yl)}A{f1(r)} {f1(r)} 0 1 1 {f1(cx+a)} {f1(yl)}V{f1(ybase)}Z"

def multifoil(x0, ys, w, ybase, lobes=3):
    r = w / (2 * lobes)
    arcs = "".join(f"A{f1(r)} {f1(r)} 0 0 1 {f1(x0+2*r*(i+1))} {f1(ys)}" for i in range(lobes))
    return f"M{f1(x0)} {f1(ybase)}V{f1(ys)}{arcs}V{f1(ybase)}Z"

def defs(c):
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['gold']}"/><stop offset=".5" stop-color="{c['gold2']}"/><stop offset="1" stop-color="{c['gold']}"/></linearGradient>
<linearGradient id="shim" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".4"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".45" stop-color="#ffb347" stop-opacity=".35"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="lightg"><stop offset="0" stop-color="#ff9aa8" stop-opacity=".9"/><stop offset="1" stop-color="#ff9aa8" stop-opacity="0"/></radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="6"/><feColorMatrix values="{c['grain']}"/></filter>
<pattern id="zel" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="{c['tile']}"/>
<g stroke="{c['gold2']}" stroke-width=".9" stroke-linejoin="round"><polygon points="{khatam(20,20,13)[0]}" fill="{c['red']}"/><polygon points="{khatam(20,20,13)[1]}" fill="{c['red']}"/></g>
<circle cx="20" cy="20" r="4" fill="{c['gold2']}"/>
<g fill="{c['gold']}" stroke="{c['gold2']}" stroke-width=".6"><path d="M0 -5L5 0L0 5L-5 0Z" transform="translate(0 0)"/><path d="M0 -5L5 0L0 5L-5 0Z" transform="translate(40 0)"/><path d="M0 -5L5 0L0 5L-5 0Z" transform="translate(0 40)"/><path d="M0 -5L5 0L0 5L-5 0Z" transform="translate(40 40)"/></g></pattern>
<pattern id="zel2" width="28" height="28" patternUnits="userSpaceOnUse"><g fill="none" stroke="{c['gold']}" stroke-opacity=".5" stroke-width=".8"><polygon points="{khatam(14,14,9)[0]}"/><polygon points="{khatam(14,14,9)[1]}"/><circle cx="14" cy="14" r="2.4"/></g></pattern>
</defs>'''

def wrap(w, h, c, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SERIF}">'
            f'{STYLE}{defs(c)}<rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" filter="url(#grain)"/>{body}'
            f'<path d="M.5 0V{h}M{w-.5} 0V{h}" stroke="{c["line"]}"/></svg>')

def petals(c, n, xr, seed=3, dur=(36, 58)):
    r = random.Random(seed); o = []
    for _ in range(n):
        x = r.uniform(*xr); s = r.uniform(.7, 1.15); col = r.choice(c["petals"]); d = r.uniform(*dur); sd = r.uniform(5, 9)
        o.append(f'<g transform="translate({f1(x)} 0)"><g class="pfall" style="animation-duration:{d:.1f}s;animation-delay:{-r.uniform(0,d):.1f}s">'
                 f'<g class="psway" style="animation-duration:{sd:.1f}s;animation-delay:{-r.uniform(0,sd):.1f}s">'
                 f'<path transform="rotate({r.uniform(0,180):.0f}) scale({s:.2f})" d="M0 -7C6 -7 7 3 0 8C-7 3 -6 -7 0 -7Z" fill="{col}" opacity=".85"/></g></g></g>')
    return "".join(o)

def divider(c, y, seed=1):
    r = random.Random(seed); o = [f'<path d="M40 {y}H860" stroke="url(#gold)" stroke-width="1.2"/>']
    for i, x in enumerate(range(52, 860, 36)):
        big = i % 4 == 0
        o.append(star(x, y, 7 if big else 4.5, c["red"] if big else c["turq"], c["gold"], .8))
        if big: o.append(f'<circle class="tw" cx="{x}" cy="{y}" r="1.8" fill="{c["gold2"]}" style="animation-delay:-{r.uniform(0,7):.1f}s"/>')
    return "".join(o)

def heading(c, y, idx, label, x=60):
    return (star(x + 14, y, 15, c["red"], c["gold"], 1) +
            f'<text x="{x+14}" y="{y+6}" font-size="15" font-weight="700" text-anchor="middle" fill="{c["paper"]}" font-family="{ARAB}">{num(idx)}</text>'
            f'<text x="{x+40}" y="{y+5}" font-size="15" font-weight="700" letter-spacing="3" fill="{c["fg"]}">{label}</text>'
            f'<path d="M{x+40} {y+16}H{x+300}" stroke="url(#gold)" stroke-width="1.4"/>' + star(x + 306, y + 16, 4, c["turq"], c["gold"], .6))

# ---------- panels ----------
def hero(c):
    img = full64((500, 916), 80)
    av = crop64((50, 245, 250, 445), (64, 64))
    b = f'<g class="rosette" opacity=".13">{"".join(star(700, 285, 330 - k * 55, "none", c["gold"], .9, k * 11) for k in range(6))}</g>'
    # top bar
    b += (f'<defs><clipPath id="av"><circle cx="64" cy="48" r="14"/></clipPath></defs>'
          f'<image x="50" y="34" width="28" height="28" clip-path="url(#av)" href="{av}" xlink:href="{av}"/>'
          f'<circle cx="64" cy="48" r="14" fill="none" stroke="url(#gold)" stroke-width="2"/>'
          f'<text x="88" y="52" font-size="12" font-family="{MONO}" fill="{c["mute"]}">solacode-SC <tspan fill="{c["red"]}">/</tspan> README</text>')
    # copy
    b += (f'<text x="60" y="128" font-size="13" letter-spacing="4" fill="{c["mute"]}">HI, I\'M</text>'
          f'<path d="M60 140H100" stroke="url(#gold)" stroke-width="2"/>'
          f'<text x="58" y="190" font-size="38" fill="{c["fg"]}">{NAME}</text>'
          f'<text x="60" y="234" font-size="15" font-weight="700" letter-spacing="5" fill="{c["turq"]}">SOFTWARE ENGINEER</text>'
          f'<text x="60" y="274" font-size="14" letter-spacing="1.5" fill="{c["fg"]}" xml:space="preserve">AI  ·  Math  ·  Newest Technologies</text>')
    b += star(60, 296, 5, c["red"], c["gold"], .6) + f'<path d="M72 296H260" stroke="url(#gold)" stroke-width="1.2"/>'
    for i, t in enumerate(["Building systems, web applications,", "developer tools and intelligent software", "for a better tomorrow."]):
        b += f'<text x="60" y="{332+i*23}" font-size="14" font-style="italic" fill="{c["mute"]}">{t}</text>'
    if USE_ARABIC:
        b += (f'<text x="60" y="440" font-size="13" letter-spacing="2" fill="{c["gold"]}">{BRAND[0].upper()}</text>'
              f'<text x="176" y="441" font-size="19" fill="{c["gold"]}" font-family="{ARAB}">{BRAND[1]}</text>')
    # alfiz frame + arch window
    cx, r, ytop, ybase = 700, 124, 74, 476
    arch = horseshoe(cx, ytop, r, ybase)
    b += (f'<rect x="540" y="36" width="320" height="476" fill="url(#zel)" stroke="{c["gold"]}" stroke-width="3"/>'
          f'<rect x="556" y="52" width="288" height="444" fill="{c["plaster"]}" stroke="{c["gold"]}" stroke-width="2"/>'
          f'<rect x="556" y="52" width="288" height="444" fill="url(#zel2)"/>'
          f'<path d="{arch}" fill="{c["wine"]}" stroke="{c["gold"]}" stroke-width="9"/>'
          f'<defs><clipPath id="arch"><path d="{arch}"/></clipPath></defs>'
          f'<g clip-path="url(#arch)"><g class="breath"><image x="{cx-r}" y="{ytop-6}" width="{2*r}" height="{ybase-ytop+12}" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/></g>'
          f'<circle class="glow" cx="{cx}" cy="250" r="150" fill="url(#lightg)"/>'
          f'<g class="sweep"><rect x="470" y="20" width="70" height="520" fill="url(#shim)" transform="rotate(16 560 250)"/></g></g>'
          f'<path d="{arch}" fill="none" stroke="url(#gold)" stroke-width="5"/><path d="{arch}" fill="none" stroke="{c["red"]}" stroke-width="1" stroke-dasharray="1 6" stroke-linecap="round" transform="translate(0 0)"/>'
          f'<rect x="{cx-r}" y="{ybase}" width="{2*r}" height="20" fill="{c["tile"]}" stroke="{c["gold"]}" stroke-width="1.6"/>')
    for k in range(8): b += star(cx - r + 16 + k * 31, ybase + 10, 6.5, c["red"] if k % 2 else c["gold2"], c["gold"], .5)
    for (sx, sy) in ((572, 68), (828, 68)): b += star(sx, sy, 8, c["gold2"], c["gold"], .8) + f'<circle class="tw" cx="{sx}" cy="{sy}" r="2" fill="{c["red"]}"/>'
    b += petals(c, 9, (300, 880), 6) + divider(c, 526, 3)
    return wrap(900, 540, c, b)

def button(c, label):
    w = 150
    b = (f'<path d="M12 1H{w-12}L{w-1} 20L{w-12} 39H12L1 20Z" fill="{c["card"]}" stroke="url(#gold)" stroke-width="2"/>'
         + star(24, 20, 8, c["red"], c["gold"], .8) +
         f'<text x="40" y="24.5" font-size="12" letter-spacing="2" fill="{c["fg"]}">{label.upper()}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 40" width="{w}" height="40" font-family="{SERIF}">{defs(c)}{b}</svg>'

def about(c):
    b = heading(c, 42, 1, "ABOUT")
    L = ["I'm Solayman El Mouden, a software engineer", "focused on systems, web technologies,",
         "artificial intelligence and mathematics.", "", "I enjoy understanding how things work",
         "underneath the abstraction and turning that", "knowledge into useful software."]
    for i, t in enumerate(L): b += f'<text x="60" y="{94+i*23}" font-size="14" fill="{c["fg"]}" xml:space="preserve">{t}</text>'
    b += f'<path d="M452 76V246" stroke="url(#gold)" stroke-width="1.3"/>' + star(452, 76, 5, c["red"], c["gold"], .6) + star(452, 246, 5, c["red"], c["gold"], .6)
    b += heading(c, 42, 2, "MY JOURNEY", 480)
    for i, (a, t) in enumerate(JOURNEY):
        y = 100 + i * 30
        wave = "M" + "L".join(f"{x} {f1(y-4+2.5*math.sin(x/9))}" for x in range(606, 694, 3))
        b += (star(492, y - 4, 6, [c["red"], c["turq"], c["emer"], c["gold"], c["red"]][i], c["gold"], .6) +
              f'<text x="510" y="{y}" font-size="14" fill="{c["fg"]}">{a}</text>'
              f'<path d="{wave}" fill="none" stroke="{c["gold"]}" stroke-width="1.2" opacity=".8"/>'
              f'<text x="704" y="{y}" font-size="14" font-style="italic" fill="{c["mute"]}">{t}</text>')
    b += divider(c, 278, 5)
    return wrap(900, 298, c, b)

def skills(c):
    b = heading(c, 40, 3, "TECHNOLOGIES &amp; SKILLS")
    cols = [c["red"], c["turq"], c["emer"], c["gold"]]
    for i, (name, mono) in enumerate(SKILLS):
        cx = 40 + 68.3 + (i % 6) * 136.7; cy = 102 + (i // 6) * 106
        b += (star(cx, cy, 40, cols[(i + i // 6) % 4], c["gold2"], 1.6) +
              f'<circle cx="{f1(cx)}" cy="{cy}" r="21" fill="{c["plaster"]}" stroke="{c["gold"]}" stroke-width="1.4"/>'
              f'<circle class="tw" cx="{f1(cx)}" cy="{cy}" r="25" fill="none" stroke="{c["gold2"]}" stroke-width=".8" stroke-dasharray="1.5 4" style="animation-delay:-{i*.7:.1f}s"/>'
              f'<text x="{f1(cx)}" y="{cy+6}" font-size="15" font-weight="700" text-anchor="middle" fill="{c["fg"]}">{mono}</text>'
              f'<text x="{f1(cx)}" y="{cy+58}" font-size="12" font-style="italic" text-anchor="middle" fill="{c["fg"]}">{name}</text>')
    b += divider(c, 312, 6)
    return wrap(900, 332, c, b)

def projects_title(c): return wrap(900, 60, c, heading(c, 32, 4, "SELECTED PROJECTS"))

def card(c, idx, name, d1, d2, tags, box):
    w, h = 208, 206
    img = crop64(box, (400, 190), 82)
    niche = multifoil(12, 44, 184, 108)
    b = (f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="6" fill="{c["card"]}" stroke="url(#gold)" stroke-width="2.4"/>'
         f'<rect x="6" y="6" width="{w-12}" height="{h-12}" rx="3" fill="none" stroke="{c["red"]}" stroke-opacity=".5"/>'
         f'<defs><clipPath id="nc"><path d="{niche}"/></clipPath></defs>'
         f'<g clip-path="url(#nc)"><image x="12" y="14" width="184" height="94" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/>'
         f'<g class="sweep" style="animation-duration:{15+idx}s"><rect x="-60" y="0" width="30" height="120" fill="url(#shim)" transform="rotate(16 0 50)"/></g></g>'
         f'<path d="{niche}" fill="none" stroke="url(#gold)" stroke-width="2.4"/>'
         + star(180, 28, 12, c["red"], c["gold"], .9) +
         f'<text x="180" y="33" font-size="12" font-weight="700" text-anchor="middle" fill="{c["paper"]}" font-family="{ARAB}">{num(idx+1)}</text>'
         f'<text x="16" y="130" font-size="15" font-weight="700" fill="{c["fg"]}">{name}</text>'
         f'<text x="16" y="148" font-size="11.5" font-style="italic" fill="{c["mute"]}">{d1}</text>'
         f'<text x="16" y="162" font-size="11.5" font-style="italic" fill="{c["mute"]}">{d2}</text>')
    x = 16
    for t in tags:
        cw = len(t) * 5.1 + 10
        b += (f'<rect x="{f1(x)}" y="174" width="{f1(cw)}" height="17" rx="8.5" fill="none" stroke="{c["turq"]}"/>'
              f'<text x="{f1(x+cw/2)}" y="185.5" font-size="8.5" font-family="{MONO}" text-anchor="middle" fill="{c["turq"]}">{t}</text>')
        x += cw + 5
    return f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{SERIF}">{STYLE}{defs(c)}{b}</svg>'

def footer(c):
    b = ""
    if USE_ARABIC:
        b += f'<text x="450" y="58" font-size="28" text-anchor="middle" fill="{c["gold"]}" font-family="{ARAB}">{AR_TAGLINE}</text>'
    b += (f'<text x="450" y="{92 if USE_ARABIC else 62}" font-size="15" font-weight="700" letter-spacing="5" text-anchor="middle" fill="{c["fg"]}" xml:space="preserve">BUILD  ·  EXPLORE  ·  UNDERSTAND</text>'
          f'<text x="450" y="{114 if USE_ARABIC else 86}" font-size="12" font-style="italic" text-anchor="middle" fill="{c["mute"]}" xml:space="preserve">Software Engineering · Systems · AI · Mathematics</text>')
    y0, yb = 136, 262
    b += f'<rect x="0" y="{y0}" width="900" height="{yb-y0+8}" fill="{c["plaster"]}"/><path d="M0 {y0}H900" stroke="url(#gold)" stroke-width="2.4"/>'
    for i in range(7):
        cx = 64 + i * 128; arch = horseshoe(cx, y0 + 12, 44, yb)
        b += (f'<path d="{arch}" fill="{c["wine"]}" stroke="url(#gold)" stroke-width="3.4"/>'
              f'<g class="lamp" style="animation-delay:-{i*.9:.1f}s"><circle cx="{cx}" cy="{y0+62}" r="30" fill="url(#warm)"/></g>'
              f'<path d="M{cx} {y0+14}V{y0+48}" stroke="{c["gold"]}"/>' + star(cx, y0 + 58, 9, c["gold2"], c["gold"], .8) +
              f'<circle cx="{cx}" cy="{y0+58}" r="2.6" fill="#fff3c0"/>')
        if i < 6: b += f'<rect x="{cx+46}" y="{y0+8}" width="36" height="{yb-y0}" fill="url(#zel2)"/>'
    b += (f'<rect x="0" y="{yb}" width="900" height="14" fill="{c["tile"]}"/><path d="M0 {yb}H900" stroke="url(#gold)" stroke-width="1.6"/>'
          f'<g fill="none" stroke="#fff" stroke-opacity=".7"><ellipse class="rip" cx="220" cy="{yb+7}" rx="40" ry="3"/><ellipse class="rip" style="animation-delay:-5s" cx="640" cy="{yb+7}" rx="40" ry="3"/></g>')
    b += petals(c, 5, (40, 860), 21, (40, 60))
    return wrap(900, 280, c, b)

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

parts = [pic("hero", f"{NAME} — Software Engineer. AI, Math, Newest Technologies.", "100%"),
         "<br>\n" + "&nbsp;\n".join(pic(f"btn-{l.lower()}", l, href=u) for l, u in (("GitHub", GITHUB), ("LinkedIn", LINKEDIN), ("Portfolio", PORTFOLIO))),
         pic("about", "About and journey", "100%"), pic("skills", "Technologies and skills", "100%"),
         pic("projects-title", "Selected projects", "100%"), cards(PROJECTS[:4]), cards(PROJECTS[4:]),
         pic("footer", "Build, Explore, Understand", "100%"),
         f'<sub><a href="{PORTFOLIO}">solaymantech.me</a> &nbsp;·&nbsp; <a href="{LINKEDIN}">LinkedIn</a></sub>']
with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as f:
    f.write('<div align="center">\n\n' + "\n\n".join(parts) + "\n\n</div>\n")
print("done")
