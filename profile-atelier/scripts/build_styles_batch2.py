import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "styles"))

def write_style(style_id, code):
    out_dir = os.path.join(BASE_DIR, style_id)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "index.ts")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(code.strip() + "\n")
    print(f"Generated {style_id}/index.ts ({len(code)} bytes)")

# ==============================================================================
# 7. ISEKAI (Isekai Storybook)
# ==============================================================================
isekai_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  panel: string;
  ink: string;
  mut: string;
  trunk: string;
  trunk2: string;
  swirl: string;
  swirl2: string;
  gold: string;
  coral: string;
  cream: string;
  magic: string;
  chip: string;
  sky: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0b1030",
    panel: "#141d4d",
    ink: "#eef0fa",
    mut: "#aab5df",
    trunk: "#24347e",
    trunk2: "#3d4fa8",
    swirl: "#34507f",
    swirl2: "#86a8c4",
    gold: "#f0c25a",
    coral: "#ee7f5f",
    cream: "#f4e6bb",
    magic: "#8fd3ff",
    chip: "#1c2a66",
    sky: "#1a2a63",
  },
  light: {
    bg: "#efe5ca",
    panel: "#f8f1de",
    ink: "#1b2457",
    mut: "#4c5686",
    trunk: "#2b3f8c",
    trunk2: "#4a5fb0",
    swirl: "#8fb0c4",
    swirl2: "#4f7896",
    gold: "#9e741a",
    coral: "#b54a2e",
    cream: "#2c3b6b",
    magic: "#2c6d99",
    chip: "#ded0aa",
    sky: "#e0d3af",
  },
};

const STYLE = `<style>
.magic-rotate { transform-box: fill-box; transform-origin: center; animation: mRotate 30s linear infinite; }
@keyframes mRotate { to { transform: rotate(360deg); } }
.firefly-rise { animation: ffRise 14s ease-in-out infinite alternate; }
@keyframes ffRise { from { transform: translateY(0); } to { transform: translateY(-30px); } }
@media (prefers-reduced-motion: reduce) { .magic-rotate, .firefly-rise { animation: none !important; } }
</style>`;

function magicCircle(cx: number, cy: number, r: number, color: string): string {
  let stars = '';
  for (let i = 0; i < 4; i++) {
    const a = (i * Math.PI) / 2;
    const px = cx + r * 0.7 * Math.cos(a);
    const py = cy + r * 0.7 * Math.sin(a);
    stars += `<circle cx="${f1(px)}" cy="${f1(py)}" r="2" fill="${color}"/>`;
  }
  return `<g class="magic-rotate">
<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="none" stroke="${color}" stroke-width="1.2" stroke-dasharray="3 3"/>
<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * 0.75)}" fill="none" stroke="${color}" stroke-width="0.8"/>
${stars}
</g>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.sky}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "ish");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="isArch"><rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#isArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24" fill="none" stroke="${c.magic}" stroke-width="2.2" stroke-opacity="0.8"/>
<g transform="translate(54, 150)">
  ${magicCircle(24, 0, 16, c.magic)}
  <text x="54" y="6" font-family="${SERIF}" font-size="20" fill="${c.gold}" letter-spacing="2">STORYBOOK</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.coral}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.gold}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="185" font-family="${SERIF}" font-size="15" fill="${c.mut}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="211" font-family="${SERIF}" font-size="15" fill="${c.mut}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="237" font-family="${SERIF}" font-size="15" fill="${c.mut}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.panel}"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.panel}" stroke="${c.magic}" stroke-width="1.5"/>
${magicCircle(24, 20, 8, c.gold)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "isa");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.ink}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.gold}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.mut}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.magic}" stroke-width="1.4" stroke-opacity="0.5"/>
${magicCircle(54, 56, 12, c.magic)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "issk");
  const cardW = 125, cardH = 70;
  const cols = 6;
  const startX = 54, startY = 100;
  const gapX = 14, gapY = 16;

  const cards = content.skills.map((s, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    return `<g transform="translate(${x}, ${y})">
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.chip}" stroke="${c.magic}" stroke-width="1.2" stroke-opacity="0.5"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.gold}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.magic}" stroke-width="1.4" stroke-opacity="0.5"/>
${magicCircle(54, 56, 12, c.magic)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "ispt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${magicCircle(54, 46, 12, c.magic)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="iscp${idx}"><rect x="20" y="20" width="168" height="140" rx="14"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="${c.panel}" stroke="${c.magic}" stroke-width="1.4"/>
<g clip-path="url(#iscp${idx})">
  ${crop ? `<image href="${crop}" x="20" y="20" width="168" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="20" y="20" width="168" height="140" fill="${c.chip}"/>`}
</g>
<rect x="20" y="20" width="168" height="140" rx="14" fill="none" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.7"/>
${magicCircle(104, 172, 8, c.gold)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.mut}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.mut}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.coral}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "isft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${magicCircle(0, -18, 14, c.magic)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.mut}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.panel}"/>
</svg>`;
}

export const isekaiStyle: StyleModule = {
  id: "isekai",
  name: "Isekai Storybook",
  keywords: ["isekai", "storybook", "castle", "fairy-tale", "fireflies"],
  palette: {
    light: ["#efe5ca", "#1b2457", "#9e741a", "#b54a2e", "#2c6d99"],
    dark: ["#0b1030", "#eef0fa", "#f0c25a", "#ee7f5f", "#8fd3ff"],
  },
  motion: "lively",
  image: { file: "source.jpg", credit: "Castle seen through moonlit foliage" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/isekai/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [170, 10, 560, 542], [516, 704], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [200, 200, 440, 420],
      [100, 100, 320, 320],
      [340, 300, 560, 500],
      [150, 400, 380, 600],
      [0, 660, 240, 900],
      [0, 0, 260, 260],
      [480, 300, 736, 556],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [220, 220], 0.85)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop);
      files[`header-${theme}.svg`] = files[`hero-${theme}.svg`];
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content);

      content.projects.forEach((proj, idx) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
          idx,
          proj.title,
          proj.line1,
          proj.line2,
          proj.tags,
          cardCrops[idx]
        );
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items
        .map(
          (p) =>
            `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, p.title, "24%")}</a>`
        )
        .join("\\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name} — ${content.role}`, "100%"),
      `<br>\\n<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Build, Explore, Understand", "100%"),
      `<sub><a href="${content.portfolio}">portfolio</a> &nbsp;·&nbsp; <a href="${content.linkedin}">LinkedIn</a></sub>`,
    ].filter(Boolean);

    const readme = `<div align="center">\\n\\n${readmeParts.join("\\n\\n")}\\n\\n</div>\\n`;
    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += str.length));

    return { files, readme, meta: { bytes } };
  },
};
"""
write_style("isekai", isekai_code)

# ==============================================================================
# 8. VANGOGH (Van Gogh Starry Night)
# ==============================================================================
vangogh_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg1: string;
  bg2: string;
  bg3: string;
  text1: string;
  text2: string;
  text3: string;
  teal1: string;
  teal2: string;
  teal3: string;
  gold1: string;
  gold2: string;
  gold3: string;
  accent: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg1: "#0A1A1F",
    bg2: "#0F2832",
    bg3: "#112E38",
    text1: "#F0F5F0",
    text2: "#D0DFE2",
    text3: "#9BB8BC",
    teal1: "#3B7A8C",
    teal2: "#5BA3A0",
    teal3: "#6FB5A2",
    gold1: "#C4A843",
    gold2: "#D4B64A",
    gold3: "#8FA055",
    accent: "#8BBFC4",
  },
  light: {
    bg1: "#FAFDF7",
    bg2: "#F0F5EE",
    bg3: "#E8EFE5",
    text1: "#1A2F35",
    text2: "#2D4A52",
    text3: "#5A7A7F",
    teal1: "#2D6B77",
    teal2: "#3B7A8C",
    teal3: "#5BA3A0",
    gold1: "#8A7030",
    gold2: "#A08838",
    gold3: "#6B7A3A",
    accent: "#3B7A8C",
  },
};

const STYLE = `<style>
.vg-spiral { transform-box: fill-box; transform-origin: center; animation: vgSpin 60s linear infinite; }
.vg-spiral-r { transform-box: fill-box; transform-origin: center; animation: vgSpinR 75s linear infinite; }
@keyframes vgSpin { to { transform: rotate(360deg); } }
@keyframes vgSpinR { to { transform: rotate(-360deg); } }
@media (prefers-reduced-motion: reduce) { .vg-spiral, .vg-spiral-r { animation: none !important; } }
</style>`;

function spiralPath(cx: number, cy: number, r0: number, r1: number, turns: number): string {
  const steps = 80;
  const pts: string[] = [];
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const r = r0 + t * (r1 - r0);
    const theta = t * turns * 2 * Math.PI;
    const x = cx + r * Math.cos(theta);
    const y = cy + r * Math.sin(theta);
    pts.push(`${f1(x)},${f1(y)}`);
  }
  return 'M' + pts.join(' L');
}

function starrySwirl(cx: number, cy: number, r: number, c: ThemeColors, rev = false): string {
  const cls = rev ? "vg-spiral-r" : "vg-spiral";
  return `<g class="${cls}">
<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * 0.2)}" fill="${c.gold2}" opacity="0.8"/>
<path d="${spiralPath(cx, cy, r * 0.1, r, 2.5)}" fill="none" stroke="${c.gold1}" stroke-width="2.4" stroke-linecap="round"/>
<path d="${spiralPath(cx, cy, r * 0.2, r * 0.85, 2)}" fill="none" stroke="${c.teal2}" stroke-width="1.6" stroke-linecap="round" opacity="0.75"/>
<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="none" stroke="${c.teal1}" stroke-width="1" stroke-opacity="0.3"/>
</g>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="0.6" stop-color="${c.bg2}"/><stop offset="1" stop-color="${c.bg3}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content): string {
  const W = 900, H = 540;
  const { defs: bDefs, bg } = base(c, W, H, "vgh");

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${bDefs}</defs>
${STYLE}
${bg}
${starrySwirl(720, 180, 140, c)}
${starrySwirl(520, 110, 80, c, true)}
${starrySwirl(820, 380, 95, c)}
<g transform="translate(54, 130)">
  ${starrySwirl(30, 0, 20, c)}
  <text x="64" y="8" font-family="${SERIF}" font-size="20" fill="${c.gold1}" letter-spacing="2">STARRY NIGHT</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="52" font-weight="700" fill="${c.text1}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.teal3}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.gold1}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="185" font-family="${SERIF}" font-size="15" fill="${c.text2}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="211" font-family="${SERIF}" font-size="15" fill="${c.text2}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="237" font-family="${SERIF}" font-size="15" fill="${c.text2}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.bg1}"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.bg2}" stroke="${c.gold1}" stroke-width="1.5"/>
${starrySwirl(24, 20, 8, c)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.text1}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "vga");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.text1}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.gold1}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.text1}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.text2}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.bg2}" stroke="${c.teal1}" stroke-width="1.4" stroke-opacity="0.5"/>
${starrySwirl(58, 60, 14, c)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.text1}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.text1}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "vgsk");
  const cardW = 125, cardH = 70;
  const cols = 6;
  const startX = 54, startY = 100;
  const gapX = 14, gapY = 16;

  const cards = content.skills.map((s, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    return `<g transform="translate(${x}, ${y})">
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.bg3}" stroke="${c.gold1}" stroke-width="1.2" stroke-opacity="0.5"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.gold1}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.text1}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.bg2}" stroke="${c.teal1}" stroke-width="1.4" stroke-opacity="0.5"/>
${starrySwirl(58, 60, 14, c)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.text1}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "vgpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${starrySwirl(58, 50, 14, c)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.text1}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[]): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<linearGradient id="vgc${idx}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg3}"/></linearGradient>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="url(#vgc${idx})" stroke="${c.teal1}" stroke-width="1.4"/>
<g transform="translate(104, 80)">
  ${starrySwirl(0, 0, 50, c)}
</g>
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.text1}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.text2}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.text2}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.gold1}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "vgft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
${starrySwirl(200, 110, 80, c)}
${starrySwirl(700, 110, 80, c, true)}
<g transform="translate(450, 75)" text-anchor="middle">
  ${starrySwirl(0, -18, 14, c)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.text1}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.text2}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.bg1}"/>
</svg>`;
}

export const vangoghStyle: StyleModule = {
  id: "vangogh",
  name: "Van Gogh",
  keywords: ["van-gogh", "post-impressionism", "spirals", "starry-night", "teal"],
  palette: {
    light: ["#FAFDF7", "#1A2F35", "#8A7030", "#2D6B77", "#5BA3A0"],
    dark: ["#0A1A1F", "#F0F5F0", "#C4A843", "#3B7A8C", "#5BA3A0"],
  },
  motion: "lively",
  render(content: Content): RenderResult {
    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content);
      files[`header-${theme}.svg`] = files[`hero-${theme}.svg`];
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content);

      content.projects.forEach((proj, idx) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
          idx,
          proj.title,
          proj.line1,
          proj.line2,
          proj.tags
        );
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items
        .map(
          (p) =>
            `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, p.title, "24%")}</a>`
        )
        .join("\\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name} — ${content.role}`, "100%"),
      `<br>\\n<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Build, Explore, Understand", "100%"),
      `<sub><a href="${content.portfolio}">portfolio</a> &nbsp;·&nbsp; <a href="${content.linkedin}">LinkedIn</a></sub>`,
    ].filter(Boolean);

    const readme = `<div align="center">\\n\\n${readmeParts.join("\\n\\n")}\\n\\n</div>\\n`;
    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += str.length));

    return { files, readme, meta: { bytes } };
  },
};
"""
write_style("vangogh", vangogh_code)

# ==============================================================================
# 9. FLORAL (Floral Gold)
# ==============================================================================
floral_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  ink: string;
  soft: string;
  gold: string;
  gold2: string;
  line: string;
  blue: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#07101e",
    bg2: "#030811",
    panel: "#0c1b33",
    ink: "#f3edd8",
    soft: "#b8c5d9",
    gold: "#e3b341",
    gold2: "#f5d376",
    line: "#c29329",
    blue: "#23497d",
  },
  light: {
    bg: "#fbf7ee",
    bg2: "#f3ebd6",
    panel: "#fffbf2",
    ink: "#111d33",
    soft: "#4a5a73",
    gold: "#a87a1d",
    gold2: "#c7962c",
    line: "#d4a946",
    blue: "#1e4070",
  },
};

const STYLE = `<style>
.botanical-shimmer { animation: bShimmer 8s ease-in-out infinite alternate; }
@keyframes bShimmer { from { opacity: 0.7; } to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .botanical-shimmer { animation: none !important; } }
</style>`;

function floralBorder(w: number, h: number, gold: string): string {
  return `<rect x="12" y="12" width="${w - 24}" height="${h - 24}" rx="14" fill="none" stroke="${gold}" stroke-width="1.6"/>
<rect x="18" y="18" width="${w - 36}" height="${h - 36}" rx="10" fill="none" stroke="${gold}" stroke-width="0.8" stroke-dasharray="4 2"/>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "flh");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="flArch"><rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="20"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#flArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="20" fill="none" stroke="${c.gold}" stroke-width="2.2"/>
${floralBorder(W, H, c.gold)}
<g transform="translate(54, 150)">
  <circle cx="20" cy="0" r="10" fill="${c.gold}"/>
  <text x="44" y="6" font-family="${SERIF}" font-size="20" fill="${c.gold2}" letter-spacing="2">BOTANICAL ATELIER</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.gold}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.gold}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="185" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="211" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="237" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[2] || "")}</text>
</g>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="8" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5"/>
<circle cx="20" cy="20" r="5" fill="${c.gold}"/>
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "fla");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.ink}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.gold}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.soft}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="16" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4"/>
<circle cx="54" cy="56" r="10" fill="${c.gold}"/>
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "flsk");
  const cardW = 125, cardH = 70;
  const cols = 6;
  const startX = 54, startY = 100;
  const gapX = 14, gapY = 16;

  const cards = content.skills.map((s, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    return `<g transform="translate(${x}, ${y})">
<rect width="${cardW}" height="${cardH}" rx="10" fill="${c.bg2}" stroke="${c.gold}" stroke-width="1.2" stroke-opacity="0.6"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.gold}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="16" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4"/>
<circle cx="54" cy="56" r="10" fill="${c.gold}"/>
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "flpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<circle cx="54" cy="46" r="10" fill="${c.gold}"/>
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="flcp${idx}"><rect x="18" y="18" width="172" height="144" rx="12"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="14" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5"/>
<g clip-path="url(#flcp${idx})">
  ${crop ? `<image href="${crop}" x="18" y="18" width="172" height="144" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="18" y="18" width="172" height="144" fill="${c.bg2}"/>`}
</g>
<rect x="18" y="18" width="172" height="144" rx="12" fill="none" stroke="${c.gold}" stroke-width="1.2"/>
<circle cx="104" cy="176" r="6" fill="${c.gold}"/>
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.gold}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "flft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  <circle cx="0" cy="-18" r="12" fill="${c.gold}"/>
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
</svg>`;
}

export const floralStyle: StyleModule = {
  id: "floral",
  name: "Floral Gold",
  keywords: ["botanical", "antique", "gold", "royal-blue", "peony"],
  palette: {
    light: ["#fbf7ee", "#111d33", "#a87a1d", "#1e4070", "#4672b8"],
    dark: ["#07101e", "#f3edd8", "#e3b341", "#23497d", "#5b8edb"],
  },
  motion: "calm",
  image: { file: "source.png", credit: "Antique gold botanical engraving" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/floral/source.png");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 736, 900], [500, 640], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [100, 200, 340, 440],
      [240, 100, 480, 340],
      [300, 350, 540, 590],
      [150, 450, 390, 690],
      [0, 660, 240, 900],
      [0, 0, 260, 260],
      [480, 300, 736, 556],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [220, 220], 0.85)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop);
      files[`header-${theme}.svg`] = files[`hero-${theme}.svg`];
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content);

      content.projects.forEach((proj, idx) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
          idx,
          proj.title,
          proj.line1,
          proj.line2,
          proj.tags,
          cardCrops[idx]
        );
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items
        .map(
          (p) =>
            `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, p.title, "24%")}</a>`
        )
        .join("\\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name} — ${content.role}`, "100%"),
      `<br>\\n<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Build, Explore, Understand", "100%"),
      `<sub><a href="${content.portfolio}">portfolio</a> &nbsp;·&nbsp; <a href="${content.linkedin}">LinkedIn</a></sub>`,
    ].filter(Boolean);

    const readme = `<div align="center">\\n\\n${readmeParts.join("\\n\\n")}\\n\\n</div>\\n`;
    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += str.length));

    return { files, readme, meta: { bytes } };
  },
};
"""
write_style("floral", floral_code)

# ==============================================================================
# 10. TREE (Ancient Tree)
# ==============================================================================
tree_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  ink: string;
  soft: string;
  cyan: string;
  gold: string;
  mint: string;
  line: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0a131c",
    bg2: "#060d14",
    panel: "#132338",
    ink: "#e7eff7",
    soft: "#8ea4ba",
    cyan: "#56cfe1",
    gold: "#e0a96d",
    mint: "#72efdd",
    line: "#1e3757",
  },
  light: {
    bg: "#f4f8fb",
    bg2: "#e4edf5",
    panel: "#ffffff",
    ink: "#11202e",
    soft: "#465d73",
    cyan: "#1b7d91",
    gold: "#946128",
    mint: "#1f8f7c",
    line: "#b8d0e5",
  },
};

const STYLE = `<style>
.contour-pulse { animation: cntPulse 9s ease-in-out infinite alternate; }
@keyframes cntPulse { from { opacity: 0.6; } to { opacity: 0.95; } }
@media (prefers-reduced-motion: reduce) { .contour-pulse { animation: none !important; } }
</style>`;

function growthRings(cx: number, cy: number, r: number, color: string): string {
  let rings = '';
  for (let i = 1; i <= 6; i++) {
    rings += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * (i / 6))}" fill="none" stroke="${color}" stroke-width="1.2" opacity="${f1(0.3 + i * 0.1)}"/>`;
  }
  return `<g class="contour-pulse">${rings}<circle cx="${f1(cx)}" cy="${f1(cy)}" r="3" fill="${color}"/></g>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "trh");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="trArch"><rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#trArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24" fill="none" stroke="${c.cyan}" stroke-width="2"/>
<g transform="translate(54, 150)">
  ${growthRings(24, 0, 18, c.cyan)}
  <text x="54" y="6" font-family="${SERIF}" font-size="20" fill="${c.gold}" letter-spacing="2">ANCIENT TREE</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.mint}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.cyan}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="185" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="211" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="237" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.bg2}"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.panel}" stroke="${c.cyan}" stroke-width="1.4"/>
${growthRings(24, 20, 8, c.cyan)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "tra");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.ink}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.gold}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.soft}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
${growthRings(54, 56, 12, c.cyan)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "trsk");
  const cardW = 125, cardH = 70;
  const cols = 6;
  const startX = 54, startY = 100;
  const gapX = 14, gapY = 16;

  const cards = content.skills.map((s, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    return `<g transform="translate(${x}, ${y})">
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.bg}" stroke="${c.line}" stroke-width="1.2"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.cyan}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
${growthRings(54, 56, 12, c.cyan)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "trpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${growthRings(54, 46, 12, c.cyan)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="trcp${idx}"><rect x="20" y="20" width="168" height="140" rx="14"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
<g clip-path="url(#trcp${idx})">
  ${crop ? `<image href="${crop}" x="20" y="20" width="168" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="20" y="20" width="168" height="140" fill="${c.bg2}"/>`}
</g>
<rect x="20" y="20" width="168" height="140" rx="14" fill="none" stroke="${c.cyan}" stroke-width="1.4" stroke-opacity="0.7"/>
${growthRings(104, 172, 8, c.cyan)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.mint}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "trft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${growthRings(0, -18, 14, c.cyan)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.bg2}"/>
</svg>`;
}

export const treeStyle: StyleModule = {
  id: "tree",
  name: "Ancient Tree",
  keywords: ["tree", "rings", "topographic", "roots", "forest"],
  palette: {
    light: ["#f4f8fb", "#11202e", "#1b7d91", "#946128", "#1f8f7c"],
    dark: ["#0a131c", "#e7eff7", "#56cfe1", "#e0a96d", "#72efdd"],
  },
  motion: "calm",
  image: { file: "source.jpg", credit: "Ancient Tree of Life" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/tree/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 736, 1000], [520, 700], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [150, 200, 390, 440],
      [100, 100, 340, 340],
      [300, 350, 540, 590],
      [200, 450, 440, 690],
      [0, 660, 240, 900],
      [0, 0, 260, 260],
      [480, 300, 736, 556],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [220, 220], 0.85)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop);
      files[`header-${theme}.svg`] = files[`hero-${theme}.svg`];
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content);

      content.projects.forEach((proj, idx) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
          idx,
          proj.title,
          proj.line1,
          proj.line2,
          proj.tags,
          cardCrops[idx]
        );
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items
        .map(
          (p) =>
            `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, p.title, "24%")}</a>`
        )
        .join("\\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name} — ${content.role}`, "100%"),
      `<br>\\n<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Build, Explore, Understand", "100%"),
      `<sub><a href="${content.portfolio}">portfolio</a> &nbsp;·&nbsp; <a href="${content.linkedin}">LinkedIn</a></sub>`,
    ].filter(Boolean);

    const readme = `<div align="center">\\n\\n${readmeParts.join("\\n\\n")}\\n\\n</div>\\n`;
    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += str.length));

    return { files, readme, meta: { bytes } };
  },
};
"""
write_style("tree", tree_code)
