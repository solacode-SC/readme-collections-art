#!/usr/bin/env python3
"""Arabic project-README generator (lotus-pond edition).  Needs: pip install pillow fonttools brotli
Produces dark/light SVG panels with EMBEDDED Arabic fonts (Aref Ruqaa, Reem Kufi, Amiri, subset to the
glyphs used) so the Arabic looks the same on every device, plus a real-Markdown RTL README.md."""
import base64, io, math, os, random, re
from PIL import Image
from fontTools import subset
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets"); os.makedirs(OUT, exist_ok=True)
ART = Image.open(os.path.join(HERE, "art", "source.jpg"))

# ---------- edit your project info here ----------
NAME_AR, NAME_EN = "فهم", "Fahm"                       # <- project name
REPO = "https://github.com/solacode-SC/REPO_NAME"       # <- your repo URL
LABEL = "مشروع تعليمي"
TAGLINE = "اشرح العالم… بلغتك"
SUB = ["مفاهيم العالم، مشروحة بالعربية", "ببساطة، وعمق، وجمال."]
EN_LINE = "Explaining world concepts in Arabic"
CHIPS = ["عربي أولاً", "مفاهيم مبسّطة", "مفتوح للمساهمة"]
SECTIONS = {"about": ("عن المشروع", "ما فكرة المشروع؟"), "fields": ("المجالات", "ما الذي نشرحه؟"),
            "how": ("كيف يعمل", "ثلاث خطوات بسيطة"), "sample": ("مثال على مفهوم", "هكذا يبدو الشرح"),
            "start": ("البدء السريع", "شغّل المشروع بنفسك"), "contribute": ("المساهمة", "شاركنا في نشر المعرفة")}
FIELDS = [("علوم", "الكون والحياة والمادة", "atom"), ("تقنية", "الحوسبة والذكاء والإنترنت", "chip"),
          ("اقتصاد", "المال والسوق والقرار", "coin"), ("تاريخ", "كيف صرنا إلى ما نحن عليه", "hour"),
          ("فلسفة", "الأسئلة الكبرى والتفكير", "bulb"), ("مجتمع", "الناس والثقافة والقانون", "people")]
STEPS = ["اختر مفهومًا", "اقرأ الشرح المبسّط", "اربطه بمثال من حياتك"]
CONCEPT = dict(term="الجاذبية", en="Gravity", tags=["علوم", "فيزياء"],
               defl=["القوة التي تجذب الأجسام ذات الكتلة بعضها نحو بعض؛", "فهي ما يُبقينا على الأرض، ويُبقي القمر في مداره."],
               ex_label="مثال", ex="لماذا يسقط التفاح إلى الأسفل ولا يطير إلى السماء؟",
               rel_label="مفاهيم مرتبطة", rel=["الكتلة", "الوزن", "المدار"])
QUOTE, QUOTE_SUB = "افهم العالم… بلغتك", "المعرفة حقٌّ للجميع"
# --------------------------------------------------

THEMES = {
 "light": dict(bg1="#fbf8ea", bg2="#e9f0e2", ink="#123e7c", ink2="#1c5fa8", text="#1d2f4a", mute="#5b6f8a", sage="#8fb8a8", sage2="#b5d1b0",
               gold="#c9981a", card="#ffffff", cardop=".82", line="#b9cfcf", petal="#ffffff", petalstroke="#9fb6c8", padop=".75", band="#123e7c"),
 "dark":  dict(bg1="#0a2142", bg2="#12427f", ink="#fbf8ea", ink2="#9cc7ee", text="#e8f0f7", mute="#a9c0d8", sage="#6fa595", sage2="#8fb8a8",
               gold="#f0cb5a", card="#0c2d5c", cardop=".72", line="#33669b", petal="#fbf8ea", petalstroke="#cfe0ee", padop=".5", band="#0a2142"),
}

# ---------- fonts (subset to used glyphs, embed as data URIs) ----------
FONTS = {"FahmRuqaa": ("ruqaa", "'FahmRuqaa','Aref Ruqaa'"), "FahmKufi": ("kufi", "'FahmKufi','Reem Kufi'"), "FahmNaskh": ("naskh", "'FahmNaskh','Amiri'")}
def all_text():
    s = " ٠١٢٣٤٥٦٧٨٩.,؛،؟:-—…·"
    for v in (NAME_AR, LABEL, TAGLINE, QUOTE, QUOTE_SUB, "".join(SUB), "".join(CHIPS), "".join(STEPS), "".join(CONCEPT["tags"]), "".join(CONCEPT["defl"]), CONCEPT["term"], CONCEPT["ex"], CONCEPT["ex_label"], CONCEPT["rel_label"], "".join(CONCEPT["rel"])):
        s += v
    for a, b in SECTIONS.values(): s += a + b
    for a, b, _ in FIELDS: s += a + b
    return "".join(sorted(set(s)))
def build_fonts():
    css = {}
    text = all_text()
    for fam, (key, _) in FONTS.items():
        opts = subset.Options(); opts.layout_features = ["*"]; opts.flavor = "woff2"; opts.notdef_outline = True
        f = TTFont(os.path.join(HERE, "art", "fonts", f"{key}.woff2"))
        sub = subset.Subsetter(opts); sub.populate(text=text); sub.subset(f)
        buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
        css[fam] = f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode(buf.getvalue()).decode()}) format('woff2')}}"
    return css
FONTCSS = build_fonts()
RUQAA, KUFI, NASKH = (FONTS[k][1] + ",serif" for k in ("FahmRuqaa", "FahmKufi", "FahmNaskh"))

STYLE = '''<style>
.rip{transform-box:fill-box;transform-origin:center;animation:rip 9s ease-out infinite;opacity:0}
@keyframes rip{0%{transform:scale(.15);opacity:0}15%{opacity:.75}100%{transform:scale(1.6);opacity:0}}
.drift{animation:drift 40s ease-in-out infinite alternate}
@keyframes drift{from{transform:translate(-18px,-6px) rotate(-4deg)}to{transform:translate(18px,8px) rotate(5deg)}}
.bob{transform-box:fill-box;transform-origin:center;animation:bob 8s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(-2px) rotate(-1.2deg)}to{transform:translateY(3px) rotate(1.2deg)}}
.pfall{animation:pfall linear infinite}
@keyframes pfall{from{transform:translate(0,-30px)}to{transform:translate(-120px,600px)}}
.psway{transform-box:fill-box;transform-origin:center;animation:psway ease-in-out infinite alternate}
@keyframes psway{from{transform:translateX(-16px) rotate(-30deg)}to{transform:translateX(16px) rotate(30deg)}}
.glow{animation:glow 9s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.15}50%{opacity:.55}}
.dots{stroke-dasharray:.1 14;stroke-linecap:round;animation:run 14s linear infinite}
@keyframes run{to{stroke-dashoffset:-141.0}}
.breath{transform-box:fill-box;transform-origin:center;animation:br 26s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1)}to{transform:scale(1.06)}}
@media (prefers-reduced-motion:reduce){.rip,.drift,.bob,.pfall,.psway,.glow,.dots,.breath{animation:none}.rip{opacity:.3}.glow{opacity:.3}}
</style>'''

def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")
def crop64(box, size, q=82):
    im = ART.crop(box).resize(size, Image.LANCZOS); buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def wrap(w, h, c, body, rx=22):
    fonts = "".join(css for fam, css in FONTCSS.items() if fam in body)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<style>{fonts}</style>{STYLE}<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>'
            f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{c["line"]}" stop-opacity="0"/><stop offset=".5" stop-color="{c["line"]}"/><stop offset="1" stop-color="{c["line"]}" stop-opacity="0"/></linearGradient>'
            f'<radialGradient id="gl"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient><clipPath id="card"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath></defs>'
            f'<g clip-path="url(#card)"><rect width="{w}" height="{h}" fill="url(#bg)"/>{body}</g>'
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="{rx}" fill="none" stroke="{c["line"]}" stroke-width="1.5"/></svg>')

def txt(x, y, s, size, fam, fill, anchor="end", weight="400", extra=""):
    if re.search("[\u0600-\u06FF]", s): s = "\u2067" + s + "\u2069"
    return f'<text x="{x}" y="{y}" font-size="{size}" font-family="{fam}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'

def lotus(x, y, s, c, op=1):
    o = []
    for ang, k in ((-62, .8), (62, .8), (-34, .95), (34, .95), (0, 1.1)):
        o.append(f'<ellipse cx="0" cy="{-14*s*k:.1f}" rx="{6*s:.1f}" ry="{15*s*k:.1f}" transform="rotate({ang})" fill="{c["petal"]}" stroke="{c["petalstroke"]}" stroke-width=".8"/>')
    o.append(f'<circle r="{3*s:.1f}" cy="{-2*s:.1f}" fill="{c["gold"]}"/>')
    return f'<g class="bob" transform="translate({x} {y})" opacity="{op}">{"".join(o)}</g>'

def pad(x, y, r, rot, c, op):
    a1, a2 = math.radians(20), math.radians(48)
    p1 = (r * math.cos(a1), r * math.sin(a1)); p2 = (r * math.cos(a2), r * math.sin(a2))
    veins = "".join(f'<path d="M0 0L{r*.92*math.cos(math.radians(a)):.1f} {r*.92*math.sin(math.radians(a)):.1f}" stroke="{c["sage"]}" stroke-width=".8" opacity=".7"/>' for a in range(70, 350, 36))
    return (f'<g transform="translate({x} {y}) rotate({rot})"><g class="drift" style="animation-duration:{30+(x%17)}s;animation-delay:-{x%11}s" opacity="{op}">'
            f'<path d="M0 0L{p1[0]:.1f} {p1[1]:.1f}A{r} {r} 0 1 0 {p2[0]:.1f} {p2[1]:.1f}Z" fill="{c["sage2"]}" stroke="{c["sage"]}" stroke-width="1.4"/>{veins}</g></g>')

def petals(c, n, seed, x0=300, x1=900):
    r = random.Random(seed); o = []
    for _ in range(n):
        x = r.uniform(x0, x1); d = r.uniform(40, 62); s = r.uniform(.7, 1.1); sd = r.uniform(6, 10)
        o.append(f'<g transform="translate({f1(x)} 0)"><g class="pfall" style="animation-duration:{d:.1f}s;animation-delay:-{r.uniform(0,d):.1f}s"><g class="psway" style="animation-duration:{sd:.1f}s">'
                 f'<path transform="rotate({r.uniform(0,180):.0f}) scale({s:.2f})" d="M0 -8C6 -7 7 4 0 9C-7 4 -6 -7 0 -8Z" fill="{c["petal"]}" stroke="{c["petalstroke"]}" stroke-width=".6" opacity=".9"/></g></g></g>')
    return "".join(o)

def chip(xr, y, s, c, fs=14):
    w = len(s) * fs * .52 + 30
    return (f'<rect x="{f1(xr-w)}" y="{y-20}" width="{f1(w)}" height="30" rx="15" fill="{c["card"]}" fill-opacity="{c["cardop"]}" stroke="{c["ink2"]}" stroke-opacity=".6"/>'
            + txt(f1(xr - w / 2), y, s, fs, NASKH, c["ink"], "middle"), w)

def water_line(c, x0, x1, y):
    d = f"M{x0} {y}" + "".join(f"L{x} {f1(y+3*math.sin(x/22))}" for x in range(x0, x1 + 1, 6))
    return f'<path d="{d}" fill="none" stroke="url(#fade)" stroke-width="1.4"/><path class="dots" d="{d}" fill="none" stroke="{c["gold"]}" stroke-width="2.2"/>'

# ---------- panels ----------
def hero(c, th):
    W, H = 900, 540; cx, cy, R = 250, 270, 214
    img = crop64((100, 180, 700, 780), (620, 620), 82)
    b = "".join(pad(x, y, r, rot, c, c["padop"]) for x, y, r, rot in ((540, 90, 70, 30), (700, 470, 90, 200), (610, 300, 46, 110), (850, 130, 60, 300), (470, 480, 40, 60)))
    b += (f'<circle cx="{cx}" cy="{cy}" r="{R+14}" fill="none" stroke="{c["gold"]}" stroke-opacity=".6" stroke-dasharray="1 6" stroke-linecap="round"/>'
          f'<defs><clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath></defs>'
          f'<g clip-path="url(#pc)"><g class="breath"><image x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" href="{img}" xlink:href="{img}"/></g>')
    lx, ly = cx - R + 445 * (2 * R / 600), cy - R + 300 * (2 * R / 600)
    for k in range(3):
        b += f'<circle class="rip" style="animation-delay:-{k*3}s" cx="{f1(lx)}" cy="{f1(ly)}" r="62" fill="none" stroke="#fff" stroke-width="1.6"/>'
    b += f'<circle class="glow" cx="{f1(lx)}" cy="{f1(ly)}" r="80" fill="url(#gl)" opacity=".3"/></g><circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c["gold"]}" stroke-width="2.5"/>'
    b += txt(860, 80, LABEL, 17, KUFI, c["gold"], "end", extra='letter-spacing="1"') + f'<path d="M740 96H860" stroke="{c["gold"]}" stroke-width="1.6"/>'
    b += txt(860, 232, NAME_AR, 128, RUQAA, c["ink"], "end", "700")
    b += txt(860, 296, TAGLINE, 30, KUFI, c["ink2"], "end")
    for i, t in enumerate(SUB): b += txt(860, 346 + i * 30, t, 20, NASKH, c["text"], "end")
    xr = 860
    for t in CHIPS:
        s, w = chip(xr, 424, t, c); b += s; xr -= w + 12
    b += txt(860, 490, EN_LINE, 14, "Georgia,serif", c["mute"], "end", extra='font-style="italic" letter-spacing="1"')
    b += petals(c, 8, 4) + water_line(c, 520, 870, 516)
    return wrap(W, H, c, b, 28)

def banner(c, th, key, idx):
    t, sub = SECTIONS[key]; W, H = 900, 96
    b = lotus(84, 56, 1.3, c) + water_line(c, 130, 560, 60)
    b += f'<circle cx="842" cy="48" r="24" fill="none" stroke="{c["gold"]}" stroke-width="1.6"/><circle cx="842" cy="48" r="19" fill="{c["gold"]}" fill-opacity=".18"/>'
    b += txt(842, 59, "٠١٢٣٤٥٦٧٨٩"[idx], 28, RUQAA, c["ink"], "middle", "700")
    b += txt(800, 50, t, 34, KUFI, c["ink"], "end") + txt(800, 78, sub, 17, NASKH, c["mute"], "end")
    return wrap(W, H, c, b, 18)

def icon(kind, x, y, c):
    s = f'fill="none" stroke="{c["ink"]}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'
    g = {"atom": "".join(f'<ellipse rx="19" ry="7.5" transform="rotate({a})"/>' for a in (0, 60, 120)) + f'<circle r="3" fill="{c["gold"]}" stroke="none"/>',
         "chip": '<rect x="-12" y="-12" width="24" height="24" rx="4"/><rect x="-5" y="-5" width="10" height="10"/>' + "".join(f'<path d="M{a} -12V-18M{a} 12V18M-12 {a}H-18M12 {a}H18"/>' for a in (-6, 6)),
         "coin": f'<circle r="16"/><circle r="10"/><path d="M0 -5V5" stroke="{c["gold"]}"/>',
         "hour": '<path d="M-11 -16H11M-11 16H11M-9 -16C-9 -2 9 -2 9 16M9 -16C9 -2 -9 -2 -9 16"/>',
         "bulb": '<path d="M-9 8C-18 -4 -8 -18 0 -18C8 -18 18 -4 9 8V12H-9Z"/><path d="M-6 17H6"/>',
         "people": '<circle cx="-8" cy="-6" r="6"/><circle cx="9" cy="-4" r="5"/><path d="M-19 14C-19 4 -3 4 -3 14M2 14C2 6 16 6 16 14"/>'}[kind]
    return f'<g transform="translate({x} {y})" {s}>{g}</g>'

def fields(c, th):
    W, H = 900, 270; b = ""
    tw, thh, gx, gy = 268, 106, 16, 16
    for i, (t, d, ic) in enumerate(FIELDS):
        col, row = i % 3, i // 3; xr = 860 - col * (tw + gx); y = 22 + row * (thh + gy)
        b += (f'<rect x="{xr-tw}" y="{y}" width="{tw}" height="{thh}" rx="16" fill="{c["card"]}" fill-opacity="{c["cardop"]}" stroke="{c["line"]}"/>'
              f'<circle cx="{xr-46}" cy="{y+thh/2}" r="30" fill="{c["gold"]}" fill-opacity=".14" stroke="{c["gold"]}" stroke-opacity=".7"/>' + icon(ic, xr - 46, y + thh / 2, c) +
              txt(xr - 92, y + 48, t, 26, KUFI, c["ink"]) + txt(xr - 92, y + 76, d, 14, NASKH, c["mute"]))
    return wrap(W, H, c, b, 18)

def steps(c, th):
    W, H = 900, 200; b = water_line(c, 120, 780, 70)
    for i, t in enumerate(STEPS):
        x = 770 - i * 320
        b += (f'<circle cx="{x}" cy="70" r="30" fill="{c["card"]}" fill-opacity="{c["cardop"]}" stroke="{c["gold"]}" stroke-width="2"/>'
              + txt(x, 84, "٠١٢٣٤٥٦٧٨٩"[i + 1], 40, RUQAA, c["ink"], "middle", "700") + lotus(x, 28, .7, c, .9) +
              txt(x, 150, t, 21, KUFI, c["ink"], "middle"))
    return wrap(W, H, c, b, 18)

def sample(c, th):
    W, H = 900, 340; lot = crop64((380, 380, 620, 600), (300, 275), 82)
    b = (f'<defs><clipPath id="lc"><rect x="30" y="30" width="250" height="280" rx="22"/></clipPath></defs>'
         f'<g clip-path="url(#lc)"><image x="30" y="30" width="250" height="280" preserveAspectRatio="xMidYMid slice" href="{lot}" xlink:href="{lot}"/>'
         f'<circle class="rip" cx="170" cy="150" r="60" fill="none" stroke="#fff" stroke-width="1.5"/><circle class="rip" style="animation-delay:-4.5s" cx="170" cy="150" r="60" fill="none" stroke="#fff" stroke-width="1.5"/></g>'
         f'<rect x="30" y="30" width="250" height="280" rx="22" fill="none" stroke="{c["gold"]}" stroke-width="2"/>')
    d = CONCEPT; xr = 860
    b += txt(xr, 96, d["term"], 66, RUQAA, c["ink"], "end", "700") + txt(xr - 4, 126, d["en"], 17, "Georgia,serif", c["mute"], "end", extra='font-style="italic" letter-spacing="2"')
    xx = xr
    for t in d["tags"]:
        s, w = chip(xx - 170, 90, t, c, 13); b += s; xx -= w + 10
    for i, t in enumerate(d["defl"]): b += txt(xr, 172 + i * 30, t, 20, NASKH, c["text"])
    b += f'<path d="M320 214H860" stroke="{c["line"]}"/>' + txt(xr, 246, d["ex_label"], 15, KUFI, c["gold"]) + txt(xr - 62, 246, d["ex"], 18, NASKH, c["text"])
    b += txt(xr, 292, d["rel_label"], 15, KUFI, c["gold"]); xx = xr - 118
    for t in d["rel"]:
        s, w = chip(xx, 296, t, c, 14); b += s; xx -= w + 10
    return wrap(W, H, c, b, 22)

def footer(c, th):
    W, H = 900, 200; img = crop64((0, 40, 736, 204), (900, 200), 80)
    b = (f'<image x="0" y="0" width="900" height="200" preserveAspectRatio="xMidYMid slice" href="{img}" xlink:href="{img}"/>'
         f'<rect width="900" height="200" fill="{c["band"]}" fill-opacity=".62"/>'
         + txt(450, 96, QUOTE, 50, RUQAA, "#fbf8ea", "middle", "700") + txt(450, 138, QUOTE_SUB, 20, NASKH, "#dcebf3", "middle")
         + lotus(450, 176, 1.1, THEMES["dark"], .95) + petals(c, 6, 9, 0, 900))
    return wrap(W, H, c, b, 22)

def save(name, theme, svg):
    svg = re.sub(r"&(?!amp;|lt;|gt;|quot;|#)", "&amp;", svg)
    open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8").write(svg)

for th, c in THEMES.items():
    save("hero", th, hero(c, th)); save("fields", th, fields(c, th)); save("steps", th, steps(c, th))
    save("sample", th, sample(c, th)); save("footer", th, footer(c, th))
    for i, k in enumerate(SECTIONS): save(f"banner-{k}", th, banner(c, th, k, i + 1))

def pic(name, alt, width="100%"):
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="assets/{name}-light.svg">\n  <img alt="{alt}" src="assets/{name}-light.svg" width="{width}">\n</picture>')

MD = f'''<!-- Hero art: lotus-pond painting (artist/source unknown). Replace art/source.jpg with an image you have the right to use. -->
<div align="center">

{pic("hero", f"{NAME_AR} — {TAGLINE}")}

</div>

<div dir="rtl" align="right">

{pic("banner-about", SECTIONS["about"][0])}

**{NAME_AR}** مشروع يشرح مفاهيم العالم باللغة العربية بأسلوب واضح ودقيق وجميل. نؤمن أن المعرفة تُفهم بعمق أكبر، وتنتشر أوسع، حين تُقدَّم بلغة القارئ نفسه.

نجمع في مكان واحد شروحًا مبسّطة للمفاهيم، مع المصطلح الإنجليزي المقابل، وأمثلة من الحياة اليومية، وروابط بين المفاهيم المتقاربة.

- شرح مبسّط لكل مفهوم دون إخلال بالدقة.
- المصطلح الإنجليزي المقابل بجانب كل مفهوم.
- أمثلة من الحياة اليومية تقرّب الفكرة.
- ربط المفاهيم المتقاربة ببعضها.
- تصميم هادئ يسهّل القراءة.

{pic("banner-fields", SECTIONS["fields"][0])}

{pic("fields", "المجالات: علوم، تقنية، اقتصاد، تاريخ، فلسفة، مجتمع")}

{pic("banner-how", SECTIONS["how"][0])}

{pic("steps", "اختر مفهومًا، اقرأ الشرح المبسّط، اربطه بمثال من حياتك")}

{pic("banner-sample", SECTIONS["sample"][0])}

{pic("sample", "مثال: مفهوم الجاذبية (Gravity)")}

{pic("banner-start", SECTIONS["start"][0])}

```bash
git clone {REPO}.git
cd REPO_NAME
# أضف هنا خطوات تشغيل مشروعك (تثبيت الحزم ثم التشغيل)
```

{pic("banner-contribute", SECTIONS["contribute"][0])}

1. افتح **Issue** لاقتراح مفهوم جديد أو لتصحيح شرح موجود.
2. اتبع قالب الشرح: المفهوم، المصطلح بالإنجليزية، التعريف، مثال، مفاهيم مرتبطة.
3. أرسل **Pull Request** بتغييراتك، وسنراجعها معًا.

> **الترخيص:** حدّد ترخيص المشروع هنا (مثال: MIT).

</div>

<div align="center">

{pic("footer", QUOTE)}

</div>
'''
open(os.path.join(HERE, "README.md"), "w", encoding="utf-8").write(MD)
print("done")
