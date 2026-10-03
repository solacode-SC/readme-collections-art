import { Content, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Fraunces','Cormorant Garamond',Georgia,serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  ink: string;
  soft: string;
  gold: string;
  teal: string;
  aqua: string;
  line: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0a1f1c",
    bg2: "#051311",
    panel: "#112e2a",
    ink: "#e7f4f0",
    soft: "#8eada6",
    gold: "#e0ab53",
    teal: "#2f7b6d",
    aqua: "#4cb39e",
    line: "#1f4a43",
  },
  light: {
    bg: "#f2f8f6",
    bg2: "#e1ede9",
    panel: "#fafffd",
    ink: "#12302b",
    soft: "#46635d",
    gold: "#a6731e",
    teal: "#25665a",
    aqua: "#3b8f7e",
    line: "#b5d1cb",
  },
};

const STYLE = `<style>
.frog-breathe { transform-box: fill-box; transform-origin: center; animation: frgBr 5s ease-in-out infinite alternate; }
@keyframes frgBr { from { transform: scale(1); } to { transform: scale(1.03); } }
@media (prefers-reduced-motion: reduce) { .frog-breathe { animation: none !important; } }
</style>`;

function frogGlyph(cx: number, cy: number, r: number, color: string): string {
  return `<g class="frog-breathe">
<ellipse cx="${f1(cx)}" cy="${f1(cy)}" rx="${f1(r)}" ry="${f1(r * 0.75)}" fill="${color}"/>
<circle cx="${f1(cx - r * 0.45)}" cy="${f1(cy - r * 0.6)}" r="${f1(r * 0.35)}" fill="${color}"/>
<circle cx="${f1(cx + r * 0.45)}" cy="${f1(cy - r * 0.6)}" r="${f1(r * 0.35)}" fill="${color}"/>
<circle cx="${f1(cx - r * 0.45)}" cy="${f1(cy - r * 0.6)}" r="${f1(r * 0.15)}" fill="#0a1f1c"/>
<circle cx="${f1(cx + r * 0.45)}" cy="${f1(cy - r * 0.6)}" r="${f1(r * 0.15)}" fill="#0a1f1c"/>
</g>`;
}

function lilyPad(cx: number, cy: number, r: number, color: string): string {
  return `<path d="M${f1(cx)} ${f1(cy)} L${f1(cx + r * 0.8)} ${f1(cy - r * 0.6)} A${f1(r)} ${f1(r)} 0 1 1 ${f1(cx + r * 0.8)} ${f1(cy + r * 0.6)} Z" fill="${color}" opacity="0.6"/>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content): string {
  const W = 900, H = 540;
  const { defs, bg } = base(c, W, H, "lph");

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
${lilyPad(720, 260, 140, c.teal)}
${lilyPad(560, 360, 90, c.teal)}
${frogGlyph(720, 230, 38, c.aqua)}
<g transform="translate(54, 140)">
  ${frogGlyph(24, 0, 16, c.aqua)}
  <text x="54" y="6" font-family="${SERIF}" font-size="20" fill="${c.gold}" letter-spacing="2">LILY POND</text>
  <text x="0" y="68" font-family="${SERIF}" font-size="52" font-weight="700" fill="${c.ink}">${escapeXml(content.name)}</text>
  <text x="2" y="112" font-family="${SANS}" font-size="18" font-weight="600" fill="${c.aqua}" letter-spacing="1.5">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="145" x2="340" y2="145" stroke="${c.line}" stroke-width="1.6"/>
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
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="12" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
${frogGlyph(24, 20, 7, c.aqua)}
<text x="86" y="25" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="600" fill="${c.ink}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "lpa");
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
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="18" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
${frogGlyph(54, 56, 12, c.aqua)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">About</text>
<text x="510" y="66" font-family="${SERIF}" font-size="24" font-weight="700" fill="${c.ink}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "lpsk");
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
<text x="${cardW / 2}" y="32" text-anchor="middle" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.aqua}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SERIF}" font-size="12" fill="${c.ink}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="18" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
${frogGlyph(54, 56, 12, c.aqua)}
<text x="88" y="66" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 90;
  const { defs, bg } = base(c, W, H, "lppt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${bg}
${frogGlyph(54, 46, 12, c.aqua)}
<text x="88" y="56" font-family="${SERIF}" font-size="28" font-weight="700" fill="${c.ink}">Selected Projects</text>
</svg>`;
}

function card(c: ThemeColors, titleStr: string, line1: string, line2: string, tags: string[]): string {
  const W = 208, H = 316;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<rect width="${W}" height="${H}" rx="18" fill="${c.panel}" stroke="${c.line}" stroke-width="1.4"/>
<g transform="translate(104, 80)">
  ${lilyPad(0, 0, 50, c.teal)}
  ${frogGlyph(0, -10, 20, c.aqua)}
</g>
<text x="104" y="205" text-anchor="middle" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(titleStr)}</text>
<text x="104" y="228" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line1)}</text>
<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.soft}">${escapeXml(line2)}</text>
<g transform="translate(16, 274)">
  ${tags.map((t, i) => `<text x="${i * 48 + 12}" y="12" font-family="${SANS}" font-size="10" font-weight="600" fill="${c.gold}">${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 220;
  const { defs, bg } = base(c, W, H, "lpft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  ${frogGlyph(0, -18, 14, c.aqua)}
  <text x="0" y="28" font-family="${SERIF}" font-size="30" font-weight="700" fill="${c.ink}" letter-spacing="1">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="14" fill="${c.soft}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.bg2}"/>
</svg>`;
}

export const lilypondStyle: StyleModule = {
  id: "lilypond",
  name: "Lily Pond",
  keywords: ["frog", "waterlily", "teal", "pond", "editorial"],
  palette: {
    light: ["#f2f8f6", "#12302b", "#a6731e", "#25665a", "#3b8f7e"],
    dark: ["#0a1f1c", "#e7f4f0", "#e0ab53", "#2f7b6d", "#4cb39e"],
  },
  motion: "calm",
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

      content.projects.forEach((proj) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
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
