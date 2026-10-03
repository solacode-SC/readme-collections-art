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
# 15. BLUEPRINT (Flow Blueprint Technical)
# ==============================================================================
blueprint_code = """import { Content, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',Consolas,monospace";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  grid: string;
  fg: string;
  mute: string;
  acc: string;
  acc2: string;
  line: string;
  card: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#081726",
    bg2: "#050f1a",
    grid: "#122b45",
    fg: "#d9ecff",
    mute: "#6b93ba",
    acc: "#4cc9f0",
    acc2: "#70e000",
    line: "#1e4d79",
    card: "#0c2035",
  },
  light: {
    bg: "#f0f7ff",
    bg2: "#e0efff",
    grid: "#c2deff",
    fg: "#0f2b47",
    mute: "#486e94",
    acc: "#1d70b8",
    acc2: "#2d8a00",
    line: "#9ec5f0",
    card: "#ffffff",
  },
};

const STYLE = `<style>
.bp-flow { stroke-dasharray: 4 8; animation: bpFlow 20s linear infinite; }
@keyframes bpFlow { to { stroke-dashoffset: -120; } }
@media (prefers-reduced-motion: reduce) { .bp-flow { animation: none !important; } }
</style>`;

function blueprintGrid(w: number, h: number, gridCol: string): string {
  let lines = '';
  for (let x = 40; x < w; x += 40) {
    lines += `<line x1="${x}" y1="0" x2="${x}" y2="${h}" stroke="${gridCol}" stroke-width="0.8" opacity="0.6"/>`;
  }
  for (let y = 40; y < h; y += 40) {
    lines += `<line x1="0" y1="${y}" x2="${w}" y2="${y}" stroke="${gridCol}" stroke-width="0.8" opacity="0.6"/>`;
  }
  return `<g>${lines}</g>`;
}

function compassRose(cx: number, cy: number, r: number, color: string): string {
  return `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="none" stroke="${color}" stroke-width="1.2"/>
<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * 0.4)}" fill="none" stroke="${color}" stroke-width="0.8"/>
<line x1="${f1(cx - r * 1.3)}" y1="${f1(cy)}" x2="${f1(cx + r * 1.3)}" y2="${f1(cy)}" stroke="${color}" stroke-width="1"/>
<line x1="${f1(cx)}" y1="${f1(cy - r * 1.3)}" x2="${f1(cx)}" y2="${f1(cy + r * 1.3)}" stroke="${color}" stroke-width="1"/>`;
}

function base(c: ThemeColors, w: number, h: number, id: string): { defs: string; bg: string } {
  const defs = `<linearGradient id="${id}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  const bg = `<rect width="${w}" height="${h}" fill="url(#${id}g)"/>${blueprintGrid(w, h, c.grid)}`;
  return { defs, bg };
}

function hero(c: ThemeColors, content: Content): string {
  const W = 900, H = 540;
  const { defs, bg } = base(c, W, H, "bph");

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<defs>${defs}</defs>
${STYLE}
${bg}
<rect x="14" y="14" width="${W - 28}" height="${H - 28}" fill="none" stroke="${c.line}" stroke-width="1.5"/>
<g transform="translate(700, 200)">
  ${compassRose(0, 0, 75, c.acc)}
</g>
<g transform="translate(54, 140)">
  <text x="0" y="0" font-size="13" fill="${c.mute}" letter-spacing="2">SPECIFICATION: IDENTITY</text>
  <text x="0" y="54" font-family="${SANS}" font-size="50" font-weight="700" fill="${c.fg}">${escapeXml(content.name)}</text>
  <text x="2" y="96" font-size="16" fill="${c.acc}">SYS_ROLE = "${escapeXml(content.role)}"</text>
  <line x1="0" y1="130" x2="380" y2="130" stroke="${c.acc}" stroke-width="1.4" class="bp-flow"/>
  <text x="2" y="170" font-size="13" fill="${c.mute}">TARGET_01 = ${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="196" font-size="13" fill="${c.mute}">TARGET_02 = ${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="222" font-size="13" fill="${c.mute}">TARGET_03 = ${escapeXml(content.tagline[2] || "")}</text>
</g>
<rect x="0" y="${H - 24}" width="${W}" height="24" fill="${c.bg2}"/>
<text x="24" y="${H - 8}" font-size="11" fill="${c.mute}">DWG NO: SC-${content.handle.toUpperCase()}-2026 // REV 04</text>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="4" fill="${c.card}" stroke="${c.line}" stroke-width="1.2"/>
<line x1="8" y1="8" x2="16" y2="8" stroke="${c.acc}" stroke-width="1.5"/>
<line x1="8" y1="8" x2="8" y2="16" stroke="${c.acc}" stroke-width="1.5"/>
<text x="80" y="25" text-anchor="middle" font-size="12" font-weight="600" fill="${c.fg}">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 420;
  const { defs, bg } = base(c, W, H, "bpa");
  const lines = content.about.map((t, i) => `<text x="54" y="${120 + i * 26}" font-family="${SANS}" font-size="15" fill="${c.fg}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 120 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.acc}"/>
<text x="30" y="0" font-size="15" font-weight="700" fill="${c.fg}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="13" fill="${c.mute}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="6" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<text x="54" y="66" font-size="20" font-weight="700" fill="${c.acc}">// SECTION 01: ABOUT</text>
<text x="510" y="66" font-size="20" font-weight="700" fill="${c.acc}">// SECTION 02: JOURNEY</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "bpsk");
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
<rect width="${cardW}" height="${cardH}" rx="4" fill="${c.bg2}" stroke="${c.line}" stroke-width="1"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-size="15" font-weight="700" fill="${c.acc}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.fg}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<defs>${defs}</defs>
${bg}
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="6" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<text x="54" y="66" font-size="20" font-weight="700" fill="${c.acc}">// SECTION 03: MODULE INVENTORY</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 80;
  const { defs, bg } = base(c, W, H, "bppt");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<defs>${defs}</defs>
${bg}
<text x="40" y="48" font-size="18" font-weight="700" fill="${c.acc}">// SECTION 04: FEATURED ARTIFACTS</text>
<line x1="380" y1="44" x2="840" y2="44" stroke="${c.line}" stroke-width="1.2" stroke-dasharray="6 4"/>
</svg>`;
}

function card(c: ThemeColors, titleStr: string, line1: string, line2: string, tags: string[]): string {
  const W = 208, H = 260;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="6" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<rect x="0" y="0" width="${W}" height="24" fill="${c.bg2}"/>
<text x="12" y="16" font-size="10" fill="${c.mute}">MOD.EXEC</text>
<g transform="translate(14, 46)">
  <text x="0" y="18" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.acc}">${escapeXml(titleStr)}</text>
  <text x="0" y="44" font-family="${SANS}" font-size="11" fill="${c.mute}">${escapeXml(line1)}</text>
  <text x="0" y="60" font-family="${SANS}" font-size="11" fill="${c.mute}">${escapeXml(line2)}</text>
  <g transform="translate(0, 100)">
    ${tags.map((t, i) => `<text x="${i * 44}" y="14" font-size="9" fill="${c.acc2}">${escapeXml(t)}</text>`).join('')}
  </g>
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 180;
  const { defs, bg } = base(c, W, H, "bpft");
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<defs>${defs}</defs>
${STYLE}
${bg}
<g transform="translate(450, 75)" text-anchor="middle">
  <text x="0" y="24" font-family="${SANS}" font-size="26" font-weight="700" fill="${c.fg}">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="52" font-size="13" fill="${c.mute}">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.bg2}"/>
</svg>`;
}

export const blueprintStyle: StyleModule = {
  id: "blueprint",
  name: "Flow Blueprint",
  keywords: ["blueprint", "technical", "cad", "vector", "schematic"],
  palette: {
    light: ["#f0f7ff", "#0f2b47", "#1d70b8", "#14548a", "#2d8a00"],
    dark: ["#081726", "#d9ecff", "#4cc9f0", "#3a86c8", "#70e000"],
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
write_style("blueprint", blueprint_code)

# ==============================================================================
# 16. HELIX (Vector Helix Harmonic Spirals)
# ==============================================================================
helix_code = """import { Content, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',Consolas,monospace";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,sans-serif";

interface ThemeColors {
  bg: string;
  a: string;
  a2: string;
  b: string;
  grid: string;
  txt: string;
  card: string;
  line: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#07090d",
    a: "#ff5a52",
    a2: "#ffb0a4",
    b: "#3a5670",
    grid: "#1b2a38",
    txt: "#9aa7b4",
    card: "#0d131a",
    line: "#24374a",
  },
  light: {
    bg: "#f7f2ee",
    a: "#c7352d",
    a2: "#e8847a",
    b: "#4a6580",
    grid: "#d9d0ca",
    txt: "#5b6670",
    card: "#ffffff",
    line: "#cfc3bb",
  },
};

const STYLE = `<style>
.spin-helix { transform-box: fill-box; transform-origin: center; animation: spHel 70s linear infinite; }
.spin-helix-r { transform-box: fill-box; transform-origin: center; animation: spHelR 85s linear infinite; }
@keyframes spHel { to { transform: rotate(360deg); } }
@keyframes spHelR { to { transform: rotate(-360deg); } }
@media (prefers-reduced-motion: reduce) { .spin-helix, .spin-helix-r { animation: none !important; } }
</style>`;

function spiralPath(cx: number, cy: number, r0: number, r1: number, turns: number, k = 0): string {
  const steps = 140;
  const pts: string[] = [];
  for (let i = 0; i < steps; i++) {
    const t = i / (steps - 1);
    const r = r0 * Math.pow(r1 / r0, t);
    const th = t * turns * 2 * Math.PI + k;
    pts.push(`${f1(cx + r * Math.cos(th))},${f1(cy + r * Math.sin(th))}`);
  }
  return 'M' + pts.join(' L');
}

function spiralDisc(cx: number, cy: number, R: number, c: string, c2: string, rev = false): string {
  let s = '';
  for (let k = 0; k < 5; k++) {
    const pCol = k % 2 === 0 ? c : c2;
    const sWidth = k % 2 === 0 ? 2.2 : 1.2;
    s += `<path d="${spiralPath(cx, cy, R * 0.04, R, 3.2, (k * 2 * Math.PI) / 5)}" fill="none" stroke="${pCol}" stroke-width="${sWidth}" stroke-linecap="round"/>`;
  }
  s += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(R)}" fill="none" stroke="${c}" stroke-width="1" opacity="0.5"/>`;
  const cls = rev ? "spin-helix-r" : "spin-helix";
  return `<g class="${cls}">${s}</g>`;
}

function concentricRings(cx: number, cy: number, r: number, n: number, col: string): string {
  let rings = '';
  for (let i = 0; i < n; i++) {
    rings += `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1((r * (i + 1)) / n)}" fill="none" stroke="${col}" stroke-width="1.4" opacity="0.85"/>`;
  }
  return rings;
}

function flowLines(w: number, h: number, col: string, n: number): string {
  let out = '';
  for (let i = 0; i < n; i++) {
    const y0 = (h * (i + 0.5)) / n;
    const pts: string[] = [];
    for (let s = 0; s <= w + 60; s += 60) {
      const y = y0 + 36 * Math.sin(s / 190 + i * 0.35) + 20 * Math.sin(s / 90 - i * 0.2);
      pts.push(`${s},${f1(y)}`);
    }
    out += `<path d="M-20,${f1(y0)} L${pts.join(' L')}" fill="none" stroke="${col}" stroke-width="1.1" opacity="0.45"/>`;
  }
  return out;
}

function hero(c: ThemeColors, content: Content): string {
  const W = 900, H = 520;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
${STYLE}
<rect width="${W}" height="${H}" fill="${c.bg}"/>
<g>${flowLines(W, H, c.b, 16)}</g>
${spiralDisc(740, 260, 150, c.a, c.a2)}
${spiralDisc(560, 160, 90, c.a, c.a2, true)}
${concentricRings(740, 260, 50, 4, c.a)}
<g transform="translate(54, 140)">
  <circle cx="20" cy="0" r="8" fill="${c.a}"/>
  <text x="36" y="5" font-size="13" fill="${c.txt}" letter-spacing="2">HARMONIC FIELD</text>
  <text x="0" y="56" font-family="${SANS}" font-size="50" font-weight="700" fill="${c.a}">${escapeXml(content.name)}</text>
  <text x="2" y="98" font-size="18" fill="${c.b}">${escapeXml(content.role.toUpperCase())}</text>
  <line x1="0" y1="130" x2="340" y2="130" stroke="${c.line}" stroke-width="1.5"/>
  <text x="2" y="168" font-family="${SANS}" font-size="15" fill="${c.txt}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="2" y="194" font-family="${SANS}" font-size="15" fill="${c.txt}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="2" y="220" font-family="${SANS}" font-size="15" fill="${c.txt}">${escapeXml(content.tagline[2] || "")}</text>
</g>
<text x="24" y="${H - 18}" font-size="11" fill="${c.txt}">z → z² + c</text>
<text x="${W - 24}" y="${H - 18}" text-anchor="end" font-size="11" fill="${c.txt}">r = a·e^(bθ)</text>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="8" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<circle cx="22" cy="20" r="5" fill="${c.a}"/>
<text x="84" y="25" text-anchor="middle" font-size="12" font-weight="600" fill="${c.txt}" letter-spacing="0.5">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 400;
  const lines = content.about.map((t, i) => `<text x="54" y="${110 + i * 26}" font-family="${SANS}" font-size="15" fill="${c.txt}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    const y = 110 + i * 44;
    return `<g transform="translate(510, ${y})">
<circle cx="12" cy="-5" r="5" fill="${c.a}"/>
<text x="30" y="0" font-size="15" font-weight="700" fill="${c.a}">${escapeXml(item.lang)}</text>
<text x="160" y="0" font-family="${SANS}" font-size="14" fill="${c.txt}">${escapeXml(item.area)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" fill="${c.bg}"/>
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="14" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<text x="54" y="66" font-size="22" font-weight="700" fill="${c.a}">About</text>
<text x="510" y="66" font-size="22" font-weight="700" fill="${c.a}">Journey</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
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
<rect width="${cardW}" height="${cardH}" rx="10" fill="${c.bg}" stroke="${c.line}" stroke-width="1.2"/>
<text x="${cardW / 2}" y="32" text-anchor="middle" font-size="15" font-weight="700" fill="${c.a}">${escapeXml(s.mono)}</text>
<text x="${cardW / 2}" y="54" text-anchor="middle" font-family="${SANS}" font-size="11" fill="${c.txt}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" fill="${c.bg}"/>
<rect x="24" y="20" width="${W - 48}" height="${H - 40}" rx="14" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<text x="54" y="66" font-size="22" font-weight="700" fill="${c.a}">Technologies &amp; Skills</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 80;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" fill="${c.bg}"/>
<text x="40" y="50" font-size="22" font-weight="700" fill="${c.a}">Selected Projects</text>
<line x1="320" y1="44" x2="840" y2="44" stroke="${c.line}" stroke-width="1.4"/>
</svg>`;
}

function card(c: ThemeColors, titleStr: string, line1: string, line2: string, tags: string[]): string {
  const W = 208, H = 260;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="12" fill="${c.card}" stroke="${c.line}" stroke-width="1.4"/>
<g transform="translate(104, 70)">
  ${spiralDisc(0, 0, 45, c.a, c.a2)}
</g>
<g transform="translate(16, 150)">
  <text x="0" y="16" font-family="${SANS}" font-size="16" font-weight="700" fill="${c.a}">${escapeXml(titleStr)}</text>
  <text x="0" y="38" font-family="${SANS}" font-size="11" fill="${c.txt}">${escapeXml(line1)}</text>
  <text x="0" y="54" font-family="${SANS}" font-size="11" fill="${c.txt}">${escapeXml(line2)}</text>
  <g transform="translate(0, 80)">
    ${tags.map((t, i) => `<text x="${i * 42}" y="12" font-size="9" fill="${c.b}">${escapeXml(t)}</text>`).join('')}
  </g>
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 200;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<defs></defs>
${STYLE}
<rect width="${W}" height="${H}" fill="${c.bg}"/>
${spiralDisc(140, 100, 60, c.a, c.a2)}
${spiralDisc(760, 100, 60, c.a, c.a2, true)}
<g transform="translate(450, 75)" text-anchor="middle">
  <text x="0" y="24" font-family="${SANS}" font-size="28" font-weight="700" fill="${c.a}">${escapeXml(content.footer.line1)}</text>
  <text x="0" y="52" font-size="13" fill="${c.txt}">${escapeXml(content.footer.line2)}</text>
</g>
<rect x="0" y="${H - 18}" width="${W}" height="18" fill="${c.card}"/>
</svg>`;
}

export const helixStyle: StyleModule = {
  id: "helix",
  name: "Vector Helix",
  keywords: ["generative", "helix", "math", "coral", "slate"],
  palette: {
    light: ["#f7f2ee", "#c7352d", "#e8847a", "#4a6580", "#5b6670"],
    dark: ["#07090d", "#ff5a52", "#ffb0a4", "#3a5670", "#9aa7b4"],
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
write_style("blueprint", blueprint_code)
write_style("helix", helix_code)
