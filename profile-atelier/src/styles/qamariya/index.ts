import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";
const ARAB = "'Amiri','Scheherazade New','Noto Naskh Arabic',serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  ink: string;
  soft: string;
  gold: string;
  gold2: string;
  terra: string;
  teal: string;
  line: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0b1617",
    bg2: "#122527",
    panel: "#152c2e",
    ink: "#f3ecdc",
    soft: "#adc2be",
    gold: "#d89e4b",
    gold2: "#f0bf6c",
    terra: "#c4583c",
    teal: "#388d84",
    line: "#b07f35",
  },
  light: {
    bg: "#f8f2e2",
    bg2: "#ede3cd",
    panel: "#fdfaf0",
    ink: "#182c2e",
    soft: "#4e6361",
    gold: "#b87d2b",
    gold2: "#d49a3e",
    terra: "#a9442a",
    teal: "#286e66",
    line: "#c49646",
  },
};

function horseshoeArch(x: number, y: number, w: number, h: number): string {
  const r = w / 2;
  const neckY = y + r * 1.15;
  return `M${f1(x + r * 0.1)} ${f1(neckY)} C${f1(x - r * 0.15)} ${f1(y + r * 0.4)}, ${f1(x + r * 0.3)} ${f1(y)}, ${f1(x + r)} ${f1(y)} C${f1(x + w - r * 0.3)} ${f1(y)}, ${f1(x + w + r * 0.15)} ${f1(y + r * 0.4)}, ${f1(x + w - r * 0.1)} ${f1(neckY)} L${f1(x + w)} ${f1(y + h)} L${f1(x)} ${f1(y + h)} Z`;
}

function star8(cx: number, cy: number, r: number, color: string): string {
  const pts: string[] = [];
  for (let i = 0; i < 16; i++) {
    const a = (i * Math.PI) / 8;
    const rad = i % 2 === 0 ? r : r * 0.54;
    pts.push(`${f1(cx + rad * Math.cos(a))},${f1(cy + rad * Math.sin(a))}`);
  }
  return `<polygon points="${pts.join(' ')}" fill="${color}"/>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content, heroCrop?: string): string {
  const W = 900, H = 640;
  const { defs: bDefs, bg } = base(c, W, H, "qmh");
  const imgW = 460;
  const imgX = W - imgW;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
${bDefs}
<clipPath id="qmArch"><path d="${horseshoeArch(imgX + 20, 30, imgW - 40, H - 60)}"/></clipPath>
</defs>
${bg}
<g clip-path="url(#qmArch)">
  ${heroCrop ? `<image href="${heroCrop}" x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="${imgX + 20}" y="30" width="${imgW - 40}" height="${H - 60}" fill="${c.panel}"/>`}
</g>
<path d="${horseshoeArch(imgX + 20, 30, imgW - 40, H - 60)}" fill="none" stroke="${c.gold}" stroke-width="2.2"/>
<g transform="translate(54, 150)">
  ${star8(24, 0, 14, c.gold)}
  <text x="54" y="6" font-family="${SERIF}" font-size="20" fill="${c.gold2}" letter-spacing="2">QAMARIYA</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="50" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.teal}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  ${content.brand?.arabic ? `<text x="2" y="148" font-family="${ARAB}" font-size="22" fill="${c.gold}">${escapeXml(content.brand.arabic)}</text>` : ''}
  <line x1="0" y1="170" x2="340" y2="170" stroke="${c.gold}" stroke-width="1.6" stroke-opacity="0.6"/>
  <text x="2" y="205" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="231" font-family="${SERIF}" font-size="15" fill="${c.soft}">${escapeXml(content.tagline[1] || "")}</text>
</g>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="8" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.5"/>
${star8(22, 20, 7, c.gold)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "qma");
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
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="18" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.6"/>
${star8(54, 56, 12, c.gold)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "qmsk");
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
<rect width="${cardW}" height="${cardH}" rx="10" fill="${c.bg2}" stroke="${c.gold}" stroke-width="1.2" stroke-opacity="0.5"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.gold}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="18" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.6"/>
${star8(54, 56, 12, c.gold)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "qmpt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${star8(54, 46, 12, c.gold)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, idx: number, title: string, line1: string, line2: string, tags: string[], crop?: string): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>
<clipPath id="qmcp${idx}"><path d="${horseshoeArch(20, 20, 168, 140)}"/></clipPath>
</defs>
<rect width="${W}" height="${H}" rx="16" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.4"/>
<g clip-path="url(#qmcp${idx})">
  ${crop ? `<image href="${crop}" x="20" y="20" width="168" height="140" preserveAspectRatio="xMidYMid slice"/>` : `<rect x="20" y="20" width="168" height="140" fill="${c.bg2}"/>`}
</g>
<path d="${horseshoeArch(20, 20, 168, 140)}" fill="none" stroke="${c.gold}" stroke-width="1.4" stroke-opacity="0.8"/>
${star8(104, 172, 8, c.gold)}
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
  const { defs, bg } = base(c, W, H, "qmft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${star8(0, -18, 14, c.gold)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
  ${content.footer.arabic ? `<text x="0" y="90" font-family="${ARAB}" font-size="20" fill="${c.gold}">${escapeXml(content.footer.arabic)}</text>` : ''}
</g>
</svg>`;
}

export const qamariyaStyle: StyleModule = {
  id: "qamariya",
  name: "Al-Andalus Qamariya",
  keywords: ["andalus", "qamariya", "stained-glass", "granada", "arabic"],
  palette: {
    light: ["#f8f2e2", "#182c2e", "#b87d2b", "#a9442a", "#286e66"],
    dark: ["#0b1617", "#f3ecdc", "#d89e4b", "#c4583c", "#388d84"],
  },
  motion: "lively",
  image: { file: "source.jpg", credit: "Alhambra stained-glass qamariya" },
  options: ["useArabic"],
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/qamariya/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 736, 1000], [520, 700], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [380, 20, 580, 115],
      [140, 230, 340, 430],
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
        .join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name} — ${content.role}`, "100%"),
      `<br>\n<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Build, Explore, Understand", "100%"),
      `<sub><a href="${content.portfolio}">portfolio</a> &nbsp;·&nbsp; <a href="${content.linkedin}">LinkedIn</a></sub>`,
    ].filter(Boolean);

    const readme = `<div align="center">\n\n${readmeParts.join("\n\n")}\n\n</div>\n`;
    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += str.length));

    return { files, readme, meta: { bytes } };
  },
};
