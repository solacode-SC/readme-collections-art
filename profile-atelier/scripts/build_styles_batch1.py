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
# 3. CANOPY (Canopy Spiral)
# ==============================================================================
canopy_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  ink: string;
  soft: string;
  accent: string;
  line: string;
  twig: string;
  disc: string;
  disctxt: string;
  btn: string;
  btntxt: string;
  band: string;
  dots: string[];
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0C1810",
    bg2: "#18351F",
    panel: "#183323",
    ink: "#EAF1D2",
    soft: "#B9CBA6",
    accent: "#C9E66B",
    line: "#8DB33A",
    twig: "#6F9A78",
    disc: "#EAF1D2",
    disctxt: "#12261A",
    btn: "#B7D957",
    btntxt: "#10200F",
    band: "#08110B",
    dots: ["#8DB33A", "#A9D04B", "#5E9B6B", "#C9E66B", "#6FA89A"],
  },
  light: {
    bg: "#F4F6E0",
    bg2: "#DCE8BE",
    panel: "#FBFCEB",
    ink: "#1B2D19",
    soft: "#47603F",
    accent: "#3C6A1B",
    line: "#6E9A2C",
    twig: "#3B2D20",
    disc: "#FBFCEB",
    disctxt: "#1B2D19",
    btn: "#4C8022",
    btntxt: "#FBFCEB",
    band: "#1B2D19",
    dots: ["#6E9A2C", "#4C8022", "#3C6A1B", "#7F9C3E", "#2D5A27"],
  },
};

const STYLE = `<style>
.spin-slow { transform-box: fill-box; transform-origin: center; animation: spSlow 45s linear infinite; }
@keyframes spSlow { to { transform: rotate(360deg); } }
.twig-sway { transform-box: fill-box; transform-origin: bottom center; animation: twgSway 6s ease-in-out infinite alternate; }
@keyframes twgSway { from { transform: rotate(-3deg); } to { transform: rotate(3deg); } }
@media (prefers-reduced-motion: reduce) { .spin-slow, .twig-sway { animation: none !important; } }
</style>`;

function phyllotaxis(cx: number, cy: number, count: number, c: ThemeColors): string {
  let florets = '';
  const cAngle = 137.5 * (Math.PI / 180);
  for (let i = 0; i < count; i++) {
    const r = 4.2 * Math.sqrt(i);
    const theta = i * cAngle;
    const x = cx + r * Math.cos(theta);
    const y = cy + r * Math.sin(theta);
    const col = c.dots[i % c.dots.length];
    florets += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(1.2 + (i / count) * 1.8)}" fill="${col}" opacity="0.85"/>`;
  }
  return `<g class="spin-slow">${florets}</g>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "ch");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="cArch"><circle cx="${f1(imgX + (imgW - 40) / 2 + 20)}" cy="${H / 2}" r="${f1((H - 80) / 2)}"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#cArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="40" width="${imgW - 40}" height="${H - 80}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="40" width="${imgW - 40}" height="${H - 80}" fill="${c.panel}"/>`}
</g>
<circle cx="${f1(imgX + (imgW - 40) / 2 + 20)}" cy="${H / 2}" r="${f1((H - 80) / 2)}" fill="none" stroke="${c.line}" stroke-width="2.5" stroke-opacity="0.8"/>
${phyllotaxis(imgX + (imgW - 40) / 2 + 20, H / 2, 85, c)}
<g transform="translate(54, 150)">
  ${phyllotaxis(24, 0, 35, c)}
  <text x="64" y="8" font-family="${SERIF}" font-size="20" fill="${c.accent}" letter-spacing="2">CANOPY</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.accent}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.line}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="185" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="211" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="237" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.band}"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="20" fill="${c.btn}" stroke="${c.line}" stroke-width="1.4"/>
<circle cx="24" cy="20" r="7" fill="${c.btntxt}"/>
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.btntxt}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "ca");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.ink}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.accent}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.soft}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4" stroke-opacity="0.5"/>
${phyllotaxis(60, 60, 25, c)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "csk");
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
<rect width="${cardW}" height="${cardH}" rx="14" fill="${c.bg}" stroke="${c.line}" stroke-width="1.2" stroke-opacity="0.6"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.accent}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4" stroke-opacity="0.5"/>
${phyllotaxis(60, 60, 25, c)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "cpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${phyllotaxis(60, 50, 25, c)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="ccp${idx}"><circle cx="104" cy="90" r="70"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
<g clip-path="url(#ccp${idx})">
  ${crop ? `<image href="${crop}" x="34" y="20" width="140" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="34" y="20" width="140" height="140" fill="${c.bg2}"/>`}
</g>
<circle cx="104" cy="90" r="70" fill="none" stroke="${c.line}" stroke-width="1.5" stroke-opacity="0.8"/>
${phyllotaxis(104, 172, 20, c)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.accent}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "cft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${phyllotaxis(0, -18, 30, c)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.band}"/>
</svg>`;
}

export const canopyStyle: StyleModule = {
  id: "canopy",
  name: "Canopy Spiral",
  keywords: ["nature", "organic", "spiral", "phyllotaxis", "foliage"],
  palette: {
    light: ["#F4F6E0", "#1B2D19", "#3C6A1B", "#6E9A2C", "#3B2D20"],
    dark: ["#0C1810", "#EAF1D2", "#C9E66B", "#8DB33A", "#6F9A78"],
  },
  motion: "lively",
  image: { file: "source.jpg", credit: "Canopy spiral leaf whorls" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/canopy/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 120, 736, 1174], [556, 794], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [200, 300, 480, 580],
      [80, 180, 320, 420],
      [360, 440, 600, 680],
      [150, 600, 400, 850],
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
write_style("canopy", canopy_code)

# ==============================================================================
# 4. CITADEL (Sunset Citadel)
# ==============================================================================
citadel_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  sky2: string;
  panel: string;
  panel2: string;
  ink: string;
  soft: string;
  accent: string;
  sun: string;
  coral: string;
  pink: string;
  crimson: string;
  line: string;
  city: string;
  band: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#1E1028",
    sky2: "#4A1F45",
    panel: "#2B1738",
    panel2: "#3B2150",
    ink: "#FCE9C9",
    soft: "#DCC3D2",
    accent: "#F7C95A",
    sun: "#F7C95A",
    coral: "#F0735F",
    pink: "#F4A3BC",
    crimson: "#CF2F3C",
    line: "#FCE9C9",
    city: "#3A2147",
    band: "#12091A",
  },
  light: {
    bg: "#FFF1D0",
    sky2: "#FFD3A0",
    panel: "#FFF9E8",
    panel2: "#FBE3B5",
    ink: "#2E1538",
    soft: "#7D536B",
    accent: "#CF2F3C",
    sun: "#CF2F3C",
    coral: "#E05A47",
    pink: "#C25D77",
    crimson: "#8E1D2A",
    line: "#2E1538",
    city: "#F0D2AC",
    band: "#2E1538",
  },
};

const STYLE = `<style>
.cloud-drift { animation: cDrift 28s ease-in-out infinite alternate; }
@keyframes cDrift { from { transform: translateX(-15px); } to { transform: translateX(15px); } }
.sun-pulse { animation: sPulse 8s ease-in-out infinite; }
@keyframes sPulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.04); } }
@media (prefers-reduced-motion: reduce) { .cloud-drift, .sun-pulse { animation: none !important; } }
</style>`;

function sunGlyph(cx: number, cy: number, r: number, color: string): string {
  let rays = '';
  for (let i = 0; i < 12; i++) {
    const a = (i * Math.PI) / 6;
    const x1 = cx + (r + 3) * Math.cos(a);
    const y1 = cy + (r + 3) * Math.sin(a);
    const x2 = cx + (r + 9) * Math.cos(a);
    const y2 = cy + (r + 9) * Math.sin(a);
    rays += `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${color}" stroke-width="1.8" stroke-linecap="round"/>`;
  }
  return `<g class="sun-pulse"><circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="${color}"/>${rays}</g>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.sky2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "cth");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="ctArch"><rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#ctArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24" fill="none" stroke="${c.accent}" stroke-width="2.2" stroke-opacity="0.8"/>
<g transform="translate(54, 150)">
  ${sunGlyph(30, 0, 16, c.accent)}
  <text x="64" y="8" font-family="${SERIF}" font-size="20" fill="${c.coral}" letter-spacing="2">SUNSET CITADEL</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.accent}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.coral}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="185" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="211" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="237" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.band}"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.panel}" stroke="${c.accent}" stroke-width="1.5"/>
<circle cx="24" cy="20" r="6" fill="${c.coral}"/>
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "cta");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.ink}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.coral}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.soft}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.accent}" stroke-width="1.4" stroke-opacity="0.5"/>
${sunGlyph(58, 60, 12, c.accent)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "ctsk");
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
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.panel2}" stroke="${c.coral}" stroke-width="1.2" stroke-opacity="0.6"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.accent}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.accent}" stroke-width="1.4" stroke-opacity="0.5"/>
${sunGlyph(58, 60, 12, c.accent)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "ctpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${sunGlyph(58, 50, 12, c.accent)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="ctcp${idx}"><rect x="20" y="20" width="168" height="140" rx="14"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="${c.panel}" stroke="${c.coral}" stroke-width="1.4"/>
<g clip-path="url(#ctcp${idx})">
  ${crop ? `<image href="${crop}" x="20" y="20" width="168" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="20" y="20" width="168" height="140" fill="${c.panel2}"/>`}
</g>
<rect x="20" y="20" width="168" height="140" rx="14" fill="none" stroke="${c.accent}" stroke-width="1.4" stroke-opacity="0.7"/>
${sunGlyph(104, 172, 8, c.accent)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.coral}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "ctft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${sunGlyph(0, -18, 14, c.accent)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.band}"/>
</svg>`;
}

export const citadelStyle: StyleModule = {
  id: "citadel",
  name: "Sunset Citadel",
  keywords: ["ligne-claire", "sunset", "clouds", "dragon", "citadel"],
  palette: {
    light: ["#FFF1D0", "#2E1538", "#CF2F3C", "#E05A47", "#5B682E"],
    dark: ["#1E1028", "#FCE9C9", "#F7C95A", "#F0735F", "#CF2F3C"],
  },
  motion: "lively",
  image: { file: "source.jpg", credit: "Red dragon soaring over a citadel at sunset" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/citadel/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 598, 700], [598, 700], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [220, 200, 440, 420],
      [80, 140, 300, 360],
      [320, 380, 540, 600],
      [180, 480, 400, 700],
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
write_style("citadel", citadel_code)

# ==============================================================================
# 5. LOTUS (Kintsugi Lotus Pond)
# ==============================================================================
lotus_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  panel: string;
  ink: string;
  mut: string;
  teal: string;
  teal2: string;
  aqua: string;
  gold: string;
  koi: string;
  koi2: string;
  seal: string;
  sealtxt: string;
  chip: string;
  strip: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#06151b",
    panel: "#0d2a34",
    ink: "#e8f2ef",
    mut: "#9dbdbb",
    teal: "#1d7f8f",
    teal2: "#2fa3a8",
    aqua: "#69cbc6",
    gold: "#e2bb63",
    koi: "#ea5a2c",
    koi2: "#b83a18",
    seal: "#d6402a",
    sealtxt: "#fbeed6",
    chip: "#12404d",
    strip: "#e9d6b0",
  },
  light: {
    bg: "#f1e3c6",
    panel: "#fbf4e1",
    ink: "#13303a",
    mut: "#4b646a",
    teal: "#14707f",
    teal2: "#1e8d95",
    aqua: "#2f9aa0",
    gold: "#a27129",
    koi: "#c9431c",
    koi2: "#91280d",
    seal: "#b6321e",
    sealtxt: "#fbeed6",
    chip: "#e5d3af",
    strip: "#3a2a16",
  },
};

const STYLE = `<style>
.ripple-slow { animation: rpSlow 10s ease-out infinite; }
@keyframes rpSlow { 0% { r: 5px; opacity: 0.9; } 100% { r: 45px; opacity: 0; } }
.koi-swim { transform-box: fill-box; transform-origin: center; animation: kSwim 14s ease-in-out infinite alternate; }
@keyframes kSwim { from { transform: translate(-8px, -4px) rotate(-4deg); } to { transform: translate(8px, 4px) rotate(4deg); } }
@media (prefers-reduced-motion: reduce) { .ripple-slow, .koi-swim { animation: none !important; } }
</style>`;

function sealStamp(cx: number, cy: number, r: number, fill: string, textCol: string): string {
  return `<rect x="${f1(cx - r)}" y="${f1(cy - r)}" width="${f1(r * 2)}" height="${f1(r * 2)}" rx="4" fill="${fill}"/>
<text x="${f1(cx)}" y="${f1(cy + 5)}" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="700" fill="${textCol}">印</text>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.panel}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "lth");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="ltArch"><rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#ltArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24" fill="none" stroke="${c.gold}" stroke-width="2.2" stroke-opacity="0.8"/>
<g transform="translate(54, 150)">
  ${sealStamp(24, 0, 14, c.seal, c.sealtxt)}
  <text x="54" y="6" font-family="${SERIF}" font-size="20" fill="${c.gold}" letter-spacing="2">KINTSUGI</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.aqua}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
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
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5"/>
<circle cx="24" cy="20" r="6" fill="${c.koi}"/>
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "lta");
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
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.5"/>
${sealStamp(54, 56, 12, c.seal, c.sealtxt)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "ltsk");
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
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.chip}" stroke="${c.gold}" stroke-width="1.2" stroke-opacity="0.5"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.gold}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.5"/>
${sealStamp(54, 56, 12, c.seal, c.sealtxt)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "ltpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${sealStamp(54, 46, 12, c.seal, c.sealtxt)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="ltcp${idx}"><rect x="20" y="20" width="168" height="140" rx="14"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4"/>
<g clip-path="url(#ltcp${idx})">
  ${crop ? `<image href="${crop}" x="20" y="20" width="168" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="20" y="20" width="168" height="140" fill="${c.chip}"/>`}
</g>
<rect x="20" y="20" width="168" height="140" rx="14" fill="none" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.7"/>
${sealStamp(104, 172, 8, c.seal, c.sealtxt)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.mut}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.mut}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.gold}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "ltft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${sealStamp(0, -18, 14, c.seal, c.sealtxt)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.mut}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.panel}"/>
</svg>`;
}

export const lotusStyle: StyleModule = {
  id: "lotus",
  name: "Kintsugi Lotus Pond",
  keywords: ["lotus", "koi", "water", "gold", "calm"],
  palette: {
    light: ["#f1e3c6", "#13303a", "#a27129", "#14707f", "#b83a18"],
    dark: ["#06151b", "#e8f2ef", "#e2bb63", "#1d7f8f", "#ea5a2c"],
  },
  motion: "calm",
  image: { file: "source.jpg", credit: "Lotus pond and swimming koi with gold veins" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/lotus/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [30, 530, 630, 1290], [600, 760], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [200, 650, 400, 850],
      [100, 400, 300, 600],
      [350, 500, 550, 700],
      [150, 800, 350, 1000],
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
write_style("lotus", lotus_code)

# ==============================================================================
# 6. GHOST (Spectral Archive)
# ==============================================================================
ghost_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  panel: string;
  panel2: string;
  ink: string;
  mut: string;
  ecto: string;
  ecto2: string;
  violet: string;
  gold: string;
  line: string;
  spines: string[];
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#05090c",
    panel: "#0b1519",
    panel2: "#101e24",
    ink: "#e6f1ee",
    mut: "#9db5b0",
    ecto: "#8ff0d0",
    ecto2: "#3f9d8d",
    violet: "#a79bff",
    gold: "#ffd27a",
    line: "#2a4048",
    spines: ["#16282e", "#1b3037", "#241f3d", "#173a34", "#2a2230", "#1c2c3a"],
  },
  light: {
    bg: "#efece1",
    panel: "#f8f6ee",
    panel2: "#e5e0cf",
    ink: "#152024",
    mut: "#556460",
    ecto: "#207a68",
    ecto2: "#2d917d",
    violet: "#5a5099",
    gold: "#9a6e1a",
    line: "#c2baa3",
    spines: ["#d8d2be", "#cdc5ae", "#ded7c5", "#c8c1aa", "#d2cbb5", "#dfd9c7"],
  },
};

const STYLE = `<style>
.ghost-float { animation: ghFloat 7s ease-in-out infinite alternate; }
@keyframes ghFloat { from { transform: translateY(-6px); } to { transform: translateY(6px); } }
.motes-rise { animation: mRise 18s linear infinite; }
@keyframes mRise { from { transform: translateY(0); } to { transform: translateY(-300px); } }
@media (prefers-reduced-motion: reduce) { .ghost-float, .motes-rise { animation: none !important; } }
</style>`;

function ghostIcon(cx: number, cy: number, r: number, color: string): string {
  return `<g class="ghost-float">
<path d="M${f1(cx - r)} ${f1(cy + r)} C${f1(cx - r)} ${f1(cy - r * 0.8)}, ${f1(cx + r)} ${f1(cy - r * 0.8)}, ${f1(cx + r)} ${f1(cy + r)} Q${f1(cx + r * 0.5)} ${f1(cy + r * 0.7)}, ${f1(cx)} ${f1(cy + r)} Q${f1(cx - r * 0.5)} ${f1(cy + r * 0.7)}, ${f1(cx - r)} ${f1(cy + r)} Z" fill="${color}" opacity="0.85"/>
<circle cx="${f1(cx - r * 0.35)}" cy="${f1(cy - r * 0.2)}" r="2" fill="#05090c"/>
<circle cx="${f1(cx + r * 0.35)}" cy="${f1(cy - r * 0.2)}" r="2" fill="#05090c"/>
</g>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.panel}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "ghh");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="ghArch"><rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#ghArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" rx="24" fill="none" stroke="${c.ecto}" stroke-width="2.2" stroke-opacity="0.8"/>
<g transform="translate(54, 150)">
  ${ghostIcon(24, 0, 14, c.ecto)}
  <text x="54" y="6" font-family="${SERIF}" font-size="20" fill="${c.ecto}" letter-spacing="2">SPECTRAL ARCHIVE</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.ecto}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.line}" stroke-width="1.6" stroke-opacity="0.6"/>
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
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.panel}" stroke="${c.ecto}" stroke-width="1.5"/>
${ghostIcon(24, 20, 7, c.ecto)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "gha");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SERIF}" font-size="15" fill="${c.ink}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.ecto}"/>
<text x="30" y="0" font-family="${SERIF}" font-size="16" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.mut}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4" stroke-opacity="0.5"/>
${ghostIcon(54, 56, 12, c.ecto)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "ghsk");
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
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.panel2}" stroke="${c.line}" stroke-width="1.2" stroke-opacity="0.5"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.ecto}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4" stroke-opacity="0.5"/>
${ghostIcon(54, 56, 12, c.ecto)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "ghpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${ghostIcon(54, 46, 12, c.ecto)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="ghcp${idx}"><rect x="20" y="20" width="168" height="140" rx="14"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
<g clip-path="url(#ghcp${idx})">
  ${crop ? `<image href="${crop}" x="20" y="20" width="168" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="20" y="20" width="168" height="140" fill="${c.panel2}"/>`}
</g>
<rect x="20" y="20" width="168" height="140" rx="14" fill="none" stroke="${c.ecto}" stroke-width="1.4" stroke-opacity="0.7"/>
${ghostIcon(104, 172, 8, c.ecto)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.mut}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.mut}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.ecto}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "ghft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${ghostIcon(0, -18, 14, c.ecto)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.mut}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.panel}"/>
</svg>`;
}

export const ghostStyle: StyleModule = {
  id: "ghost",
  name: "Spectral Archive",
  keywords: ["spectral", "archive", "library", "lantern", "gothic"],
  palette: {
    light: ["#efece1", "#152024", "#207a68", "#9a6e1a", "#5a5099"],
    dark: ["#05090c", "#e6f1ee", "#8ff0d0", "#ffd27a", "#a79bff"],
  },
  motion: "lively",
  image: { file: "source.jpg", credit: "Moonlit archive with gentle library ghosts" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/ghost/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 40, 736, 1004], [600, 760], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [230, 20, 530, 320],
      [100, 300, 400, 600],
      [350, 400, 650, 700],
      [200, 600, 500, 900],
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
write_style("ghost", ghost_code)
