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
# 1. FROST
# ==============================================================================
frost_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style','DejaVu Serif',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif";
const ARAB = "'Amiri','Scheherazade New','Noto Naskh Arabic','Geeza Pro',serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  panelOp: string;
  border: string;
  ink: string;
  soft: string;
  accent: string;
  hi: string;
  snow: string;
  frost: string;
  btn: string;
  btntxt: string;
  disc: string;
  band: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#050917",
    bg2: "#0B2358",
    panel: "#FFFFFF",
    panelOp: "0.055",
    border: "#8FB6FF",
    ink: "#F3F1EA",
    soft: "#B9C9E8",
    accent: "#9CC0FF",
    hi: "#F5E9B8",
    snow: "#FFFFFF",
    frost: "#DCE8FF",
    btn: "#2557C0",
    btntxt: "#FFFFFF",
    disc: "#0A1A45",
    band: "#03060F",
  },
  light: {
    bg: "#E8F0FC",
    bg2: "#F6F2E7",
    panel: "#FFFFFF",
    panelOp: "0.72",
    border: "#1C4DB0",
    ink: "#0A1B45",
    soft: "#3E5384",
    accent: "#1C4DB0",
    hi: "#7A5D12",
    snow: "#6F9BE0",
    frost: "#4F78B0",
    btn: "#1C4DB0",
    btntxt: "#FFFFFF",
    disc: "#E8F0FC",
    band: "#1C4DB0",
  },
};

const STYLE = `<style>
.fallM { animation: fallM 16s linear infinite; }
@keyframes fallM { from { transform: translateY(-40px); } to { transform: translateY(500px); } }
.moon-glow { animation: mGlow 5s ease-in-out infinite alternate; }
@keyframes mGlow { from { opacity: 0.8; } to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) { .fallM, .moon-glow { animation: none !important; } }
</style>`;

function wave(x0: number, x1: number, y: number, amp: number, wl: number, ph = 0.0, step = 8): string {
  const pts: string[] = [];
  let x = x0;
  while (x <= x1) {
    pts.push(`${f1(x)},${f1(y + amp * Math.sin(((x - x0) / wl) * 2 * Math.PI + ph))}`);
    x += step;
  }
  return 'M' + pts.join(' L');
}

function snowflake(cx: number, cy: number, r: number, color: string): string {
  let arms = '';
  for (let i = 0; i < 6; i++) {
    const a = (i * Math.PI) / 3;
    const x = cx + r * Math.cos(a);
    const y = cy + r * Math.sin(a);
    arms += `<line x1="${f1(cx)}" y1="${f1(cy)}" x2="${f1(x)}" y2="${f1(y)}" stroke="${color}" stroke-width="1.4" stroke-linecap="round"/>`;
  }
  return `<g>${arms}<circle cx="${f1(cx)}" cy="${f1(cy)}" r="2" fill="${color}"/></g>`;
}

function moonIcon(c: ThemeColors, cx: number, cy: number, r = 10): string {
  return `<g class="moon-glow"><circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="${c.hi}"/>
<circle cx="${f1(cx - r * 0.3)}" cy="${f1(cy - r * 0.2)}" r="${f1(r * 0.22)}" fill="${c.bg}" opacity="0.2"/>
<circle cx="${f1(cx + r * 0.3)}" cy="${f1(cy + r * 0.35)}" r="${f1(r * 0.15)}" fill="${c.bg}" opacity="0.2"/></g>`;
}

function snowParticles(c: ThemeColors, w: number, h: number, count = 20): string {
  let dots = '';
  for (let i = 0; i < count; i++) {
    const x = (i * 47) % w;
    const y = (i * 29) % h;
    const r = 1 + (i % 3) * 0.6;
    const delay = -(i * 1.3);
    dots += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="${c.snow}" opacity="0.7" style="animation-delay: ${f1(delay)}s;"/>`;
  }
  return `<g class="fallM">${dots}</g>`;
}

function lancet(x: number, y: number, w: number, h: number): string {
  const r = w / 2;
  const topH = r * 1.3;
  return `M${f1(x)} ${f1(y + topH)} C${f1(x)} ${f1(y + r * 0.4)}, ${f1(x + r * 0.4)} ${f1(y)}, ${f1(x + r)} ${f1(y)} C${f1(x + w - r * 0.4)} ${f1(y)}, ${f1(x + w)} ${f1(y + r * 0.4)}, ${f1(x + w)} ${f1(y + topH)} L${f1(x + w)} ${f1(y + h)} L${f1(x)} ${f1(y + h)} Z`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function panel(c: ThemeColors, x: number, y: number, w: number, h: number, pid: string): { defs: string; body: string } {
  const defs = `<clipPath id="${pid}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="24"/></clipPath>`;
  const body = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="24" fill="${c.panel}" fill-opacity="${c.panelOp}" stroke="${c.border}" stroke-width="1.4" stroke-opacity="0.4"/>`;
  return { defs, body };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "h");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<linearGradient id="hFade" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="${c.bg}"/>
  <stop offset="0.2" stop-color="${c.bg}" stop-opacity="0.9"/>
  <stop offset="1" stop-color="${c.bg}" stop-opacity="0"/>
</linearGradient>
<clipPath id="hArch"><path d="${lancet(imgX + 20, 30, imgW - 40, H - 60)}"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#hArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.bg2}"/>`}
  <rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="url(#hFade)"/>
</g>
<path d="${lancet(imgX + 20, 30, imgW - 40, H - 60)}" fill="none" stroke="${c.border}" stroke-width="2" stroke-opacity="0.6"/>
${snowParticles(c, W, H, 24)}
<g transform="translate(54, 140)">
  ${moonIcon(c, 24, 0, 16)}
  <text x="54" y="8" font-family="${SERIF}" font-size="20" fill="${c.soft}" letter-spacing="2">STUDIO OF</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="52" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.accent}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  ${content.brand?.arabic ? `<text x="2" y="150" font-family="${ARAB}" font-size="24" fill="${c.hi}">${escapeXml(content.brand.arabic)}</text>` : ''}
  <path d="${wave(0, 360, 175, 4, 90)}" fill="none" stroke="${c.border}" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="2" y="210" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="236" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="262" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.band}"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="20" fill="${c.btn}" stroke="${c.border}" stroke-width="1.4"/>
${snowflake(22, 20, 8, c.btntxt)}
<text x="84" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.btntxt}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs: bDefs, bg } = base(c, W, H, "ab");
  const { defs: pDefs, body: pBody } = panel(c, 24, 20, W - 48, H - 40, "abp");

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
<defs>${bDefs}${pDefs}</defs>
${STYLE}
${bg}
${pBody}
${moonIcon(c, 58, 60, 12)}
<text x="84" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs: bDefs, bg } = base(c, W, H, "sk");
  const { defs: pDefs, body: pBody } = panel(c, 24, 20, W - 48, H - 40, "skp");

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
<rect width="${cardW}" height="${cardH}" rx="12" fill="${c.panel}" fill-opacity="0.7" stroke="${c.border}" stroke-width="1.2" stroke-opacity="0.4"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.accent}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${bDefs}${pDefs}</defs>
${bg}
${pBody}
${moonIcon(c, 58, 60, 12)}
<text x="84" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "pt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${moonIcon(c, 58, 50, 12)}
<text x="84" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
<path d="${wave(380, 840, 50, 3, 70)}" fill="none" stroke="${c.border}" stroke-width="1.4" stroke-opacity="0.4"/>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<linearGradient id="cg${idx}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<clipPath id="cp${idx}"><path d="${lancet(24, 20, 160, 140)}"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="20" fill="url(#cg${idx})" stroke="${c.border}" stroke-width="1.4" stroke-opacity="0.5"/>
<g clip-path="url(#cp${idx})">
  ${crop ? `<image href="${crop}" x="24" y="20" width="160" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="24" y="20" width="160" height="140" fill="${c.bg2}"/>`}
</g>
<path d="${lancet(24, 20, 160, 140)}" fill="none" stroke="${c.border}" stroke-width="1.5" stroke-opacity="0.7"/>
${snowflake(104, 172, 8, c.accent)}
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(title)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.accent}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 240;
  const { defs, bg } = base(c, W, H, "ft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
${snowParticles(c, W, H, 16)}
<g transform="translate(450, 80)" text-anchor="middle">
  ${moonIcon(c, 0, -20, 14)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
  ${content.footer.arabic ? `<text x="0" y="92" font-family="${ARAB}" font-size="20" fill="${c.hi}">${escapeXml(content.footer.arabic)}</text>` : ''}
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.band}"/>
</svg>`;
}

export const frostStyle: StyleModule = {
  id: "frost",
  name: "Frost & Ink",
  keywords: ["woodblock", "ice", "indigo", "arabic", "minimal"],
  palette: {
    light: ["#E8F0FC", "#0A1B45", "#1C4DB0", "#4F78B0", "#7A5D12"],
    dark: ["#050917", "#F3F1EA", "#9CC0FF", "#8FB6FF", "#F5E9B8"],
  },
  motion: "calm",
  image: { file: "source.jpg", credit: "Woodblock print night lake" },
  options: ["useArabic"],
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/frost/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 736, 1033], [520, 730], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [40, 170, 300, 430],
      [140, 230, 340, 430],
      [300, 380, 520, 600],
      [250, 600, 470, 820],
      [0, 660, 240, 900],
      [0, 0, 260, 260],
      [480, 300, 736, 556],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [240, 240], 0.85)
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
write_style("frost", frost_code)
