"""Regenerates every SVG in ./assets from the supplied painting (crops stored in src/crops.json)."""
import json, math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

CROPS = json.load(open('src/crops.json'))
FR = lambda w, s='normal': f'node_modules/@fontsource/fraunces/files/fraunces-latin-{w}-{s}.woff'
CG = lambda w: f'node_modules/@fontsource/cormorant-garamond/files/cormorant-garamond-latin-{w}-italic.woff'
NAME_F, NAME_I, BODY, ACC_I, ACC_I2 = FR(600), FR(600, 'italic'), FR(400), CG(500), CG(600)

TH = {
 'dark':  dict(bg='#0a1f26', text='#f3f1cf', muted='#a3bcb0', acc='#cfd94f', acc2='#5fb4a2', line='#2f6a62', fire='#ffd95a', tint=.2,  tilebg='#0e2a31', halo='#06191e'),
 'light': dict(bg='#f5f4e1', text='#12322c', muted='#4c6b60', acc='#2f6f4f', acc2='#2d7f8f', line='#9bb8a2', fire='#d9a21b', tint=0,   tilebg='#fbfaec', halo='#0a2a30'),
}
PADCOL = dict(lang=('#6a934f', '#a9d4a4'), fw=('#b1ba42', '#e0e283'), db=('#408968', '#7cc0ae'), tool=('#e0a232', '#f1cf7a'))
_f = {}
def tpath(font, text, size, x, y, track=0.0):
    t = _f.setdefault(font, TTFont(font)); gs, cm, upm = t.getGlyphSet(), t.getBestCmap(), t['head'].unitsPerEm
    s = size / upm; pen = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip(".")); cur = 0.0
    for ch in text:
        g = cm.get(ord(ch))
        if not g: continue
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x + cur, y))); cur += gs[g].width * s + track
    return pen.getCommands(), cur
def T(font, text, size, x, y, fill, track=0.0, anchor='start', op=1):
    d, w = tpath(font, text, size, 0, 0, track)
    dx = x - (w / 2 if anchor == 'middle' else w if anchor == 'end' else 0)
    d, w = tpath(font, text, size, dx, y, track)
    return f'<path d="{d}" fill="{fill}" opacity="{op}"/>', w
def wrap(font, text, size, maxw):
    lines, cur = [], ''
    for wd in text.split():
        t = (cur + ' ' + wd).strip()
        if tpath(font, t, size, 0, 0)[1] > maxw and cur: lines.append(cur); cur = wd
        else: cur = t
    return lines + [cur]
def pl(pts): return 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
def pad(cx, cy, R, notch=-125, nw=8, sc=.028, k=9):
    a0, a1 = math.radians(notch + nw/2), math.radians(notch + 360 - nw/2)
    pts = [(cx + R*(1+sc*math.sin(k*a))*math.cos(a), cy + R*(1+sc*math.sin(k*a))*math.sin(a)) for a in (a0 + (a1-a0)*i/160 for i in range(161))]
    return f'M{cx:.1f},{cy:.1f} L' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'
def img(name, x, y, w, h, extra=''):
    b = CROPS[name]['b64']
    return f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" href="data:image/jpeg;base64,{b}" xlink:href="data:image/jpeg;base64,{b}" preserveAspectRatio="none" {extra}/>'
def svg(W, H, body, label, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            f'<defs>{defs}</defs>{body}</svg>')
def spiral(cx, cy, rmax, turns, c, op, sw=1.6, dash='6 5', dur=90, arms=1):
    s = ''
    for a in range(arms):
        pts = [(cx + rmax*t*math.cos(t*turns*2*math.pi + a*2*math.pi/arms), cy + rmax*t*math.sin(t*turns*2*math.pi + a*2*math.pi/arms)) for t in (i/220 for i in range(221))]
        s += f'<path d="{pl(pts)}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-dasharray="{dash}" stroke-linecap="round" opacity="{op}"/>'
    return f'<g>{s}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>'
def twinkle(rnd, n, x0, x1, y0, y1, c):
    o = ''
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(1.4, 3.1); d = rnd.uniform(7, 13)
        o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{c}"><animate attributeName="opacity" values=".15;.95;.15" dur="{d:.1f}s" begin="-{rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></g>'.replace('</g>', '</circle>')
    return o
def waves(W, y0, n, c, op, amp=7, per=160, gap=11):
    o = ''
    for i in range(n):
        pts = [(x, y0 + i*gap + amp*math.sin((x / per) * 2*math.pi + i*.7)) for x in range(-per, W + per + 1, 20)]
        o += f'<path d="{pl(pts)}" fill="none" stroke="{c}" stroke-width="1.2" opacity="{op*(1-i/(n+1)):.2f}"/>'
    return f'<g>{o}<animateTransform attributeName="transform" type="translate" from="0 0" to="-{per} 0" dur="24s" repeatCount="indefinite"/></g>'
def padicon(cx, cy, r, fill, hi, vein):
    v = ''.join(f'<line x1="{cx}" y1="{cy}" x2="{cx + .86*r*math.cos(math.radians(a)):.1f}" y2="{cy + .86*r*math.sin(math.radians(a)):.1f}" stroke="{vein}" stroke-width="1" opacity=".55"/>' for a in range(-30, 300, 36))
    return f'<path d="{pad(cx, cy, r, sc=.04, k=7)}" fill="{fill}"/><circle cx="{cx}" cy="{cy}" r="{r*.42:.1f}" fill="{hi}" opacity=".5"/>{v}'

# ---------------------------------------------------------------- HERO
def hero(m):
    c = TH[m]; W, H = 1200, 640; cx, cy, R = 880, 335, 255
    rnd = random.Random(11); body = f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>'
    body += waves(W, 560, 5, c['acc2'], .42)
    body += spiral(470, 96, 62, 4, c['acc'], .55, dur=70) + spiral(10, 650, 125, 5, c['acc2'], .3, dur=110)
    for i, d in enumerate((0, 4, 8)):
        body += f'<circle cx="{cx}" cy="{cy}" r="{R+10}" fill="none" stroke="{c["acc2"]}" stroke-width="1.4"><animate attributeName="r" values="{R+10};{R+80}" dur="12s" begin="{d}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".55;0" dur="12s" begin="{d}s" repeatCount="indefinite"/></circle>'
    clip = f'<clipPath id="pad"><path d="{pad(cx, cy, R)}"/></clipPath><clipPath id="med"><circle cx="1085" cy="100" r="96"/></clipPath>'
    s = 2*R*1.04
    body += img('frog', cx - s/2, cy - s/2, s, s, 'clip-path="url(#pad)"')
    if c['tint']: body += f'<path d="{pad(cx, cy, R)}" fill="#06242c" opacity="{c["tint"]}"/>'
    body += f'<path d="{pad(cx, cy, R)}" fill="none" stroke="{c["acc"]}" stroke-width="2.2"/><path d="{pad(cx, cy, R+12)}" fill="none" stroke="{c["acc2"]}" stroke-width="1.2" stroke-dasharray="2 7" opacity=".8"/>'
    body += f'<circle cx="1085" cy="100" r="104" fill="{c["bg"]}"/>' + img('spiral', 1085 - 142, 100 - 77, 285, 285, 'clip-path="url(#med)"')
    body += f'<circle cx="1085" cy="100" r="96" fill="none" stroke="{c["acc"]}" stroke-width="2"/>'
    body += twinkle(rnd, 30, 560, 1190, 30, 610, c['fire'])
    for bx, by, dur in ((690, 88, 21), (735, 122, 26)):
        body += f'<g transform="translate({bx} {by})"><path d="M0,0 q8,-9 16,0 q8,-9 16,0" fill="none" stroke="{c["text"]}" stroke-width="2" stroke-linecap="round"/><animateTransform attributeName="transform" type="translate" values="{bx} {by};{bx+34} {by-9};{bx} {by}" dur="{dur}s" repeatCount="indefinite"/></g>'
    for px, py, r, i in ((300, 600, 22, 0), (420, 618, 15, 1), (180, 612, 12, 2)):
        body += f'<g>{padicon(px, py, r, "#6a934f", "#b1ba42", c["bg"])}<animateTransform attributeName="transform" type="translate" values="0 0;{8+i*3} {-2};0 0" dur="{13+i*3}s" repeatCount="indefinite"/></g>'
    x = 64
    t, _ = T(ACC_I, 'Hi, I’m', 36, x, 150, c['acc']); body += t
    t, _ = T(NAME_F, 'Solayman', 98, x - 4, 256, c['text']); body += t
    t, _ = T(NAME_F, 'El Mouden', 98, x - 4, 354, c['text']); body += t
    t, _ = T(ACC_I2, 'Software Engineer', 34, x, 408, c['acc']); body += t
    t, _ = T(BODY, 'AI  |  Math  |  Newest Technologies', 18, x, 446, c['acc2'], track=1.6); body += t
    for i, ln in enumerate(wrap(ACC_I, 'Building systems, web applications, developer tools and intelligent software for a better tomorrow.', 25, 440)):
        t, _ = T(ACC_I, ln, 25, x, 496 + i*30, c['muted']); body += t
    return svg(W, H, body, 'Solayman El Mouden, Software Engineer. AI, Math, Newest Technologies. Lily-pond painting with a frog on a pad, ripples and fireflies.', clip)

# ---------------------------------------------------------------- DIVIDER / HEADINGS
def divider(m):
    c = TH[m]; W, H = 1200, 60
    pts = [(x, 30 + 4*math.sin(x/70)) for x in range(0, W + 1, 12)]; path = pl(pts)
    b = f'<path d="{path}" fill="none" stroke="{c["line"]}" stroke-width="1.4"/>'
    for x, r in ((190, 11), (600, 16), (1010, 11)):
        y = 30 + 4*math.sin(x/70); b += f'<ellipse cx="{x}" cy="{y+4:.1f}" rx="{r*2.2:.0f}" ry="{r*.5:.1f}" fill="none" stroke="{c["acc2"]}" stroke-width="1" opacity=".5"><animate attributeName="rx" values="{r*1.6:.0f};{r*3.2:.0f}" dur="10s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0" dur="10s" repeatCount="indefinite"/></ellipse>'
        b += f'<g transform="translate(0 0)">{padicon(x, y - 2, r, "#6a934f", "#b1ba42", c["bg"])}</g>'
    b += f'<circle r="2.6" fill="{c["fire"]}"><animateMotion dur="16s" repeatCount="indefinite" path="{path}"/></circle>'
    return svg(W, H, b, 'Decorative water line with lily pads')

def heading(m, title, sub, crop, k):
    c = TH[m]; W, H = 1200, 104; cx, cy, r = 56, 52, 38
    t, tw = T(NAME_F, title, 48, 116, 62, c['text']); s, sw_ = T(ACC_I, sub, 23, 116, 92, c['muted'])
    x0 = 116 + max(tw, sw_) + 36
    pts = [(x, 50 + 5*math.sin((x - x0)/60)) for x in range(int(x0), 1161, 12)]
    box = CROPS[crop]; D = 2*r*1.25
    b = (f'<clipPath id="c{k}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>' + img(crop, cx - D/2, cy - D/2*box['h']/box['w'], D, D*box['h']/box['w'], f'clip-path="url(#c{k})"')
         + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["acc"]}" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="{r+8}" fill="none" stroke="{c["acc2"]}" stroke-width="1" stroke-dasharray="2 6" opacity=".8"/>'
         + t + s + f'<path d="{pl(pts)}" fill="none" stroke="{c["line"]}" stroke-width="1.4"/>' + padicon(1172, 50, 13, '#b1ba42', '#e0e283', c['bg'])
         + f'<circle r="2.6" fill="{c["fire"]}"><animateMotion dur="14s" repeatCount="indefinite" path="{pl(pts)}"/></circle>')
    return svg(W, H, b, title)

# ---------------------------------------------------------------- APPROACH + SKILLS
def tile_frame(c, x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{c["tilebg"]}" stroke="{c["acc"]}" stroke-opacity=".38"/>'
            f'<path d="M{x+w-34},{y+h} a34,34 0 0 1 34,-34" fill="none" stroke="{c["acc2"]}" stroke-opacity=".5"/><path d="M{x+w-22},{y+h} a22,22 0 0 1 22,-22" fill="none" stroke="{c["acc2"]}" stroke-opacity=".35"/>')
def approach(m):
    c = TH[m]; W, H = 1200, 176; items = [('Systems', 'C / C++', 'lang'), ('Intelligence', 'Python / AI', 'fw'), ('Web', 'TypeScript / React', 'db'), ('Infrastructure', 'Docker / Linux', 'tool'), ('Exploration', 'Mathematics /', 'lang')]
    tw = (W - 4*20)/5; b = ''
    for i, (a, v, k) in enumerate(items):
        x = i*(tw + 20); b += tile_frame(c, x, 0, tw, H - 4) + padicon(x + 34, 38, 15, PADCOL[k][0], PADCOL[k][1], c['tilebg'])
        b += T(NAME_F, a, 25, x + 22, 98, c['text'])[0] + T(ACC_I2, v, 22, x + 22, 128, c['acc'])[0]
        if i == 4: b += T(ACC_I2, 'New Technologies', 22, x + 22, 154, c['acc'])[0]
        b += f'<path d="M{x+60},38 h30 m-6,-5 l6,5 l-6,5" fill="none" stroke="{c["acc2"]}" stroke-width="1.4" stroke-linecap="round"/>'
    return svg(W, H, b, 'My approach: Systems with C and C++, Intelligence with Python and AI, Web with TypeScript and React, Infrastructure with Docker and Linux, Exploration with mathematics and new technologies.')
def skillgrid(m):
    c = TH[m]; techs = [('C / C++', 'language', 'lang'), ('Python', 'language', 'lang'), ('JavaScript', 'language', 'lang'), ('TypeScript', 'language', 'lang'), ('React', 'library', 'fw'), ('Next.js', 'framework', 'fw'),
                        ('Django', 'framework', 'fw'), ('FastAPI', 'framework', 'fw'), ('PostgreSQL', 'database', 'db'), ('Docker', 'containers', 'tool'), ('Linux', 'operating system', 'tool'), ('Git', 'version control', 'tool')]
    cols, gap = 6, 20; tw = (1200 - gap*(cols-1))/cols; th = 108; H = th*2 + gap; b = ''
    for i, (n, cat, k) in enumerate(techs):
        x, y = (i % cols)*(tw + gap), (i//cols)*(th + gap)
        b += tile_frame(c, x, y, tw, th) + padicon(x + 32, y + 32, 14, PADCOL[k][0], PADCOL[k][1], c['tilebg'])
        b += T(NAME_F, n, 24, x + 20, y + 78, c['text'])[0] + T(ACC_I, cat, 19, x + 20, y + 98, c['muted'])[0]
    return svg(1200, H, b, 'Technologies: C and C++, Python, JavaScript, TypeScript, React, Next.js, Django, FastAPI, PostgreSQL, Docker, Linux, Git.')

# ---------------------------------------------------------------- CARDS
def overlay(kind, cx, cy, r, c):
    ink, halo = '#fffbd6', c['halo']; paths = []; dots = ''; anim = ''
    if kind == 'lazyequation':
        for a in range(2):
            paths.append(pl([(cx + r*1.05*t*math.cos(t*3*2*math.pi + a*math.pi), cy + r*1.05*t*math.sin(t*3*2*math.pi + a*math.pi)) for t in (i/120 for i in range(121))]))
        orbit = f'M{cx - r*1.25},{cy} a{r*1.25},{r*.42} 0 1 0 {r*2.5},0 a{r*1.25},{r*.42} 0 1 0 {-r*2.5},0'
        paths.append(orbit); dots = f'<circle r="4.5" fill="{c["fire"]}"><animateMotion dur="14s" repeatCount="indefinite" path="{orbit}"/></circle>'
    elif kind == 'leetresume':
        for ex, ey in ((-.9, -.1), (-.5, -.65), (.1, -.9), (.75, -.5), (.95, .25), (.45, .8)):
            paths.append(f'M{cx},{cy + r*.95:.0f} C{cx + ex*r*.1:.0f},{cy + r*.3:.0f} {cx + ex*r*.9:.0f},{cy + ey*r*.3:.0f} {cx + ex*r:.0f},{cy + ey*r:.0f}')
            dots += f'<circle cx="{cx + ex*r:.0f}" cy="{cy + ey*r:.0f}" r="3.6" fill="{ink}"/>'
    elif kind == 'libora':
        for i, (dx, rot) in enumerate(((-18, -9), (14, 6))):
            paths.append(f'M{cx+dx-34},{cy-52} h68 v104 h-68 Z'); 
            for j in range(4): paths.append(f'M{cx+dx-22},{cy-34+j*16} h{44 - (j % 2)*12}')
        anim = ''
        paths.append(f'M{cx-r},{cy+r*.55} C{cx-r*.4},{cy+r*.2} {cx+r*.3},{cy+r*.9} {cx+r},{cy+r*.4}')
    elif kind == 'webserv':
        nodes = [(cx + r*.95*math.cos(math.radians(a)), cy + r*.95*math.sin(math.radians(a))) for a in range(-90, 270, 60)]
        for i, (x, y) in enumerate(nodes):
            paths.append(f'M{cx},{cy} L{x:.0f},{y:.0f}'); dots += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.4" fill="{ink}"/>'
            paths.append(f'M{x:.0f},{y:.0f} L{nodes[(i+1) % 6][0]:.0f},{nodes[(i+1) % 6][1]:.0f}')
        dots += f'<circle cx="{cx}" cy="{cy}" r="6" fill="{c["fire"]}"/><circle r="3.6" fill="{c["fire"]}"><animateMotion dur="8s" repeatCount="indefinite" path="M{cx},{cy} L{nodes[0][0]:.0f},{nodes[0][1]:.0f} L{nodes[3][0]:.0f},{nodes[3][1]:.0f} L{cx},{cy}"/></circle>'
    else:
        for rr in (.35, .65, .95): paths.append(f'M{cx - r*rr},{cy} a{r*rr},{r*rr} 0 1 0 {2*r*rr},0 a{r*rr},{r*rr} 0 1 0 {-2*r*rr},0')
        for a in range(0, 360, 45): paths.append(f'M{cx + r*.35*math.cos(math.radians(a)):.0f},{cy + r*.35*math.sin(math.radians(a)):.0f} L{cx + r*1.08*math.cos(math.radians(a)):.0f},{cy + r*1.08*math.sin(math.radians(a)):.0f}')
        for a, rr in ((30, .65), (140, .95), (250, .35), (320, .95)): dots += f'<circle cx="{cx + r*rr*math.cos(math.radians(a)):.0f}" cy="{cy + r*rr*math.sin(math.radians(a)):.0f}" r="4.2" fill="{c["fire"]}"/>'
    o = ''.join(f'<path d="{d}" fill="none" stroke="{halo}" stroke-opacity=".45" stroke-width="4" stroke-linecap="round"/>' for d in paths) + ''.join(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>' for d in paths)
    g = f'<g>{o}{dots}'
    if kind in ('lazyequation', 'solajobs'): g += f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{360 if kind == "solajobs" else -360}" dur="{120 if kind == "solajobs" else 90}s" repeatCount="indefinite"/>' if kind == 'solajobs' else ''
    return g + '</g>'
CARDS = [
 ('lazyequation', '01', 'LazyEquation', 'Interactive mathematics and physics visualization platform.', ['React', 'TS', 'Fastify', 'PostgreSQL'], 'spiral'),
 ('leetresume', '02', 'LeetResume', 'AI-powered resume builder and optimizer.', ['Next.js', 'Prisma', 'PostgreSQL'], 'yellow'),
 ('libora', '03', 'Libora', 'Flutter PDF reader with a modern reading experience.', ['Flutter', 'Dart', 'Riverpod'], 'drops'),
 ('webserv', '04', 'Webserv', 'C++98 HTTP server built from scratch.', ['C++98', 'Networking'], 'field'),
 ('solajobs', '05', 'solaJobs v2', 'Job platform project.', [], 'blue'),
]
REPO = {'lazyequation': 'lazyequation', 'leetresume': 'leetresume', 'libora': 'libora', 'webserv': 'webserv', 'solajobs': 'solajobs-v2'}
def card(m, i):
    c = TH[m]; kind, num, name, desc, tags, crop = CARDS[i]; W, H = (580 if i < 4 else 1180), 262; cx, cy, r = 114, 131, 82
    box = CROPS[crop]; D = 2*r*1.2; hh = D*box['h']/box['w']
    b = (f'<clipPath id="k"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
         + f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{c["tilebg"]}" stroke="{c["acc"]}" stroke-opacity=".4"/>'
         + img(crop, cx - D/2, cy - hh/2, D, hh, 'clip-path="url(#k)"') + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["acc"]}" stroke-width="2"/>'
         + f'<circle cx="{cx}" cy="{cy}" r="{r+9}" fill="none" stroke="{c["acc2"]}" stroke-width="1" stroke-dasharray="2 6" opacity=".8"/>'
         + f'<g clip-path="url(#k)">{overlay(kind, cx, cy, r*.78, c)}</g>')
    x = 226; b += T(ACC_I2, num, 56, x, 76, c['acc'])[0] + T(NAME_F, name, 33, x, 118, c['text'])[0]
    for j, ln in enumerate(wrap(ACC_I, desc, 22, W - x - 40 if i < 4 else 520)): b += T(ACC_I, ln, 22, x, 152 + j*25, c['muted'])[0]
    tx = x
    for t in tags:
        d, w = tpath(BODY, t, 13, 0, 0, .4); b += f'<rect x="{tx}" y="194" width="{w+22:.0f}" height="26" rx="13" fill="none" stroke="{c["acc2"]}" stroke-opacity=".8"/>' + T(BODY, t, 13, tx + 11, 212, c['text'], .4)[0]; tx += w + 32
    b += T(BODY, f'github.com/solacode-SC/{REPO[kind]}', 13, x, 248, c["acc2"], .3)[0]
    b += f'<path d="M{W-52},{H-14} a40,40 0 0 1 40,-40" fill="none" stroke="{c["acc2"]}" stroke-opacity=".55"/><path d="M{W-34},{H-14} a22,22 0 0 1 22,-22" fill="none" stroke="{c["acc2"]}" stroke-opacity=".4"/>'
    return svg(W, H, b, f'Project {num}: {name}. {desc} ' + ', '.join(tags))

# ---------------------------------------------------------------- FOOTER
def footer(m):
    c = TH[m]; W, H = 1200, 320; box = CROPS['pond']; h = W*box['h']/box['w']; rnd = random.Random(5)
    defs = (f'<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".62"/><stop offset=".7" stop-color="#fff" stop-opacity=".4"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="fm"><rect width="{W}" height="{H}" fill="url(#fg)"/></mask>'
            f'<radialGradient id="sc"><stop offset="0" stop-color="{c["bg"]}" stop-opacity=".95"/><stop offset=".7" stop-color="{c["bg"]}" stop-opacity=".6"/><stop offset="1" stop-color="{c["bg"]}" stop-opacity="0"/></radialGradient>')
    b = f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/><g mask="url(#fm)">' + img('pond', 0, H - h + 20, W, h) + f'</g>'
    if c['tint']: b += f'<rect width="{W}" height="{H}" fill="#06242c" opacity=".25" mask="url(#fm)"/>'
    b += f'<ellipse cx="600" cy="150" rx="520" ry="105" fill="url(#sc)"/>' + twinkle(rnd, 14, 60, 1140, 215, 305, c['fire'])
    for d in (0, 5): b += f'<ellipse cx="600" cy="262" rx="40" ry="8" fill="none" stroke="{c["acc"]}" stroke-width="1.2"><animate attributeName="rx" values="40;360" dur="10s" begin="{d}s" repeatCount="indefinite"/><animate attributeName="ry" values="8;44" dur="10s" begin="{d}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0" dur="10s" begin="{d}s" repeatCount="indefinite"/></ellipse>'
    b += T(NAME_I, 'Build · Explore · Understand', 52, 600, 138, c['text'], anchor='middle')[0] + T(ACC_I, 'Software Engineering · Systems · AI · Mathematics', 25, 600, 182, c['acc'], anchor='middle')[0]
    return svg(W, H, b, 'Build, Explore, Understand. Software Engineering, Systems, AI, Mathematics.', defs)

for m in TH:
    w = lambda n, s: open(f'assets/{n}-{m}.svg', 'w').write(s)
    w('header', hero(m)); w('divider', divider(m)); w('approach', approach(m)); w('skills-grid', skillgrid(m)); w('footer', footer(m))
    w('about', heading(m, 'About', 'how I think, how I build', 'spiral', 1)); w('skills', heading(m, 'Technologies', 'the toolkit', 'yellow', 2)); w('projects-title', heading(m, 'Selected Projects', 'five systems', 'field', 3))
    for i, cd in enumerate(CARDS): w('card-' + ('solajobs-v2' if cd[0] == 'solajobs' else cd[0]), card(m, i))
