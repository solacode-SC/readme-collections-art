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
# 2. LAPIS (Lapis & Gold)
# ==============================================================================
lapis_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Iowan Old Style',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  panel2: string;
  ink: string;
  soft: string;
  accent: string;
  gold: string;
  blue: string;
  pink: string;
  shadow: string;
  band: string;
  glow: string;
  star: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0B0F2E",
    bg2: "#1B2466",
    panel: "#141B4F",
    panel2: "#1F2A70",
    ink: "#F3EBDD",
    soft: "#C9CDEB",
    accent: "#E8C46A",
    gold: "#E3BE63",
    blue: "#7FA7D6",
    pink: "#E08AA8",
    shadow: "#05071A",
    band: "#070A1F",
    glow: "#8E9BDB",
    star: "#FFF3C4",
  },
  light: {
    bg: "#F5EDDF",
    bg2: "#E2E2F1",
    panel: "#FCF8EE",
    panel2: "#E9E6F4",
    ink: "#161C5A",
    soft: "#4A5088",
    accent: "#7A5A12",
    gold: "#BE9435",
    blue: "#5E88C4",
    pink: "#C8607F",
    shadow: "#C9CDEB",
    band: "#161C5A",
    glow: "#8E9BDB",
    star: "#BE9435",
  },
};

const STYLE = `<style>
.shimmer { animation: shm 6s ease-in-out infinite alternate; }
@keyframes shm { 0% { opacity: 0.6; } 100% { opacity: 1; } }
.gold-vein { stroke-dasharray: 4 12; animation: vFlow 24s linear infinite; }
@keyframes vFlow { to { stroke-dashoffset: -160; } }
@media (prefers-reduced-motion: reduce) { .shimmer, .gold-vein { animation: none !important; } }
</style>`;

function rosette(cx: number, cy: number, r: number, fill: string, stroke: string): string {
  let petals = '';
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI) / 4;
    const px = cx + r * 0.6 * Math.cos(a);
    const py = cy + r * 0.6 * Math.sin(a);
    petals += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1(r * 0.45)}" fill="${fill}" stroke="${stroke}" stroke-width="1.2"/>`;
  }
  return `<g>${petals}<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * 0.5)}" fill="${fill}" stroke="${stroke}" stroke-width="1.4"/></g>`;
}

function octagon(x: number, y: number, w: number, h: number, chamfer = 24): string {
  return `M${f1(x + chamfer)} ${f1(y)} L${f1(x + w - chamfer)} ${f1(y)} L${f1(x + w)} ${f1(y + chamfer)} L${f1(x + w)} ${f1(y + h - chamfer)} L${f1(x + w - chamfer)} ${f1(y + h)} L${f1(x + chamfer)} ${f1(y + h)} L${f1(x)} ${f1(y + h - chamfer)} L${f1(x)} ${f1(y + chamfer)} Z`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "lh");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="lArch"><path d="${octagon(imgX + 20, 30, imgW - 40, H - 60, 36)}"/></clipPath>
</defs>
${STYLE}
${bg}
<g clip-path="url(#lArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<path d="${octagon(imgX + 20, 30, imgW - 40, H - 60, 36)}" fill="none" stroke="${c.gold}" stroke-width="2.2" stroke-opacity="0.8"/>
<g transform="translate(54, 150)">
  ${rosette(30, 0, 18, c.panel, c.gold)}
  <text x=\"64\" y=\"8\" font-family=\"${SERIF}\" font-size=\"20\" fill=\"${c.accent}\" letter-spacing=\"2\">EDITION</text>
  <text x=\"0\" y=\"68\" font-family=\"${SERIF}\" font-size=\"50\" font-weight=\"700\" fill=\"${c.ink}\">${escapeXml(content.name)}</text>
  <text x=\"2\" y=\"112\" font-family=\"${SANS}\" font-size=\"18\" font-weight=\"600\" fill=\"${c.accent}\" letter-spacing=\"1.5\">${escapeXml(content.role.toUpperCase())}</text>
  <line x1=\"0\" y1=\"145\" x2=\"340\" y2=\"145\" stroke=\"${c.gold}\" stroke-width=\"1.5\" stroke-opacity=\"0.6\" class=\"gold-vein\"/>
  <text x=\"2\" y=\"185\" font-family=\"${SERIF}\" font-size=\"15\" fill=\"${c.soft}\">${escapeXml(content.tagline[0] || "")}</text>
  <text x=\"2\" y=\"211\" font-family=\"${SERIF}\" font-size=\"15\" fill=\"${c.soft}\">${escapeXml(content.tagline[1] || "")}</text>
  <text x=\"2\" y=\"237\" font-family=\"${SERIF}\" font-size=\"15\" fill=\"${c.soft}\">${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x=\"0\" y=\"${H - 24}\" width=\"${W}\" height=\"24\" fill=\"${c.band}\"/>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="10" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5"/>
${rosette(24, 20, 9, c.bg, c.gold)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "la");
  const lines = content.about.map((t, i) => `<text x=\"54\" y=\"${120 + i * 26}\" font-family=\"${SERIF}\" font-size=\"15\" fill=\"${c.ink}\">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform=\"translate(510, ${y})\">
<circle cx=\"12\" cy=\"-5\" r=\"5\" fill=\"${c.gold}\"/>
<text x=\"30\" y=\"0\" font-family=\"${SERIF}\" font-size=\"16\" font-weight=\"700\" fill=\"${c.ink}\">${escapeXml(item.lang)}</text>
<text x=\"160\" y=\"0\" font-family=\"${SANS}\" font-size=\"14\" fill=\"${c.soft}\">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5" stroke-opacity="0.5"/>
${rosette(58, 60, 14, c.bg, c.gold)}
<text x="88" y="66" font-family="${SERIF}" font-size=\"28\" font-weight=\"700\" fill=\"${c.ink}\">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size=\"24\" font-weight=\"700\" fill=\"${c.ink}\">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "lsk");
  const cardW = 125, cardH = 70;
  const cols = 6;
  const startX = 54, startY = 100;
  const gapX = 14, gapY = 16;

  const cards = content.skills.map((s, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    return `<g transform=\"translate(${x}, ${y})\">
<rect width=\"${cardW}\" height=\"${cardH}\" rx=\"10\" fill=\"${c.panel2}\" stroke=\"${c.gold}\" stroke-width=\"1.2\" stroke-opacity=\"0.6\"/>
<text x=\"${cardW / 2}\" y=\"32\" text-anchor=\"middle\" font-family=\"${SANS}\" font-size=\"16\" font-weight=\"700\" fill=\"${c.gold}\">${escapeXml(s.mono)}</text>
<text x=\"${cardW / 2}\" y=\"54\" text-anchor=\"middle\" font-family=\"${SERIF}\" font-size=\"12\" fill=\"${c.ink}\">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="20" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5" stroke-opacity="0.5"/>
${rosette(58, 60, 14, c.bg, c.gold)}
<text x="88" y="66" font-family="${SERIF}" font-size=\"28\" font-weight=\"700\" fill=\"${c.ink}\">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "lpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${rosette(58, 50, 14, c.bg, c.gold)}
<text x="88" y="56" font-family="${SERIF}" font-size=\"28\" font-weight=\"700\" fill=\"${c.ink}\">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id=\"lcp${idx}\"><path d=\"${octagon(20, 20, 168, 140, 20)}\"/></clipPath>
</defs>
<rect width=\"${W}\" height=\"${H}\" rx=\"16\" fill=\"${c.panel}\" stroke=\"${c.gold}\" stroke-width=\"1.4\"/>
<g clip-path=\"url(#lcp${idx})\">
  ${crop ? `<image href=\"${crop}\" x=\"20\" y=\"20\" width=\"168\" height=\"140\" preserveAspectRatio=\"xMidYMid slice\"/>` : `<rect x=\"20\" y=\"20\" width=\"168\" height=\"140\" fill=\"${c.panel2}\"/>`}
</g>
<path d=\"${octagon(20, 20, 168, 140, 20)}\" fill=\"none\" stroke=\"${c.gold}\" stroke-width=\"1.4\" stroke-opacity=\"0.7\"/>
${rosette(104, 172, 8, c.bg, c.gold)}
<text x=\"104\" y=\"205\" text-anchor=\"middle\" font-family=\"${SERIF}\" font-size=\"18\" font-weight=\"700\" fill=\"${c.ink}\">${escapeXml(title)}</text>
<text x=\"104\" y=\"228\" text-anchor=\"middle\" font-family=\"${SANS}\" font-size=\"11\" fill=\"${c.soft}\">${escapeXml(line1)}</text>
<text x=\"104\" y=\"244\" text-anchor=\"middle\" font-family=\"${SANS}\" font-size=\"11\" fill=\"${c.soft}\">${escapeXml(line2)}</text>
<g transform=\"translate(16, 274)\">
  ${tags.map((t, i) => `<text x=\"${i * 48 + 12}\" y=\"12\" font-family=\"${SANS}\" font-size=\"10\" font-weight=\"600\" fill=\"${c.gold}\">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "lft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform=\"translate(450, 75)\" text-anchor=\"middle\">
  ${rosette(0, -18, 14, c.bg, c.gold)}
  <text x=\"0\" y=\"28\" font-family=\"${SERIF}\" font-size=\"30\" font-weight=\"700\" fill=\"${c.ink}\" letter-spacing=\"1\">${escapeXml(content.footer.line1)}</text>
  <text x=\"0\" y=\"60\" font-family=\"${SANS}\" font-size=\"14\" fill=\"${c.soft}\" letter-spacing=\"1.5\">${escapeXml(content.footer.line2)}</text>
</g>
<rect x=\"0\" y=\"${H - 18}\" width=\"${W}\" height=\"18\" fill=\"${c.band}\"/>
</svg>`;
}

export const lapisStyle: StyleModule = {
  id: "lapis",
  name: "Lapis & Gold",
  keywords: ["lapis", "kintsugi", "gold", "filigree", "indigo"],
  palette: {
    light: ["#F5EDDF", "#161C5A", "#BE9435", "#7A5A12", "#5E88C4"],
    dark: ["#0B0F2E", "#F3EBDD", "#E8C46A", "#E3BE63", "#7FA7D6"],
  },
  motion: "calm",
  image: { file: "source.jpg", credit: "Dragon and gold robe in lapis lazuli" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/lapis/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 526, 789], [526, 789], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [140, 230, 340, 430],
      [40, 170, 300, 430],
      [300, 380, 520, 600],
      [250, 600, 470, 820],
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
write_style("lapis", lapis_code)
