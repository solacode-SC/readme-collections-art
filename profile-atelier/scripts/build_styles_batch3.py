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
# 11. CONSTELLATION (Indigo Wash & Dotted Orbits)
# ==============================================================================
constellation_code = """import { Content, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const FONT = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const JP = "'Noto Sans JP','Yu Gothic','Hiragino Sans',sans-serif";

interface ThemeColors {
  bg1: string;
  bg2: string;
  fg: string;
  mute: string;
  acc: string;
  acc2: string;
  line: string;
  card: string;
  deep: string;
  mid: string;
  lite: string;
  dot: string;
  ring: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg1: "#060b2e",
    bg2: "#03061a",
    fg: "#dfe7ff",
    mute: "#8fa3e8",
    acc: "#5b8cff",
    acc2: "#9ab6ff",
    line: "#2b3c9e",
    card: "#0a1347",
    deep: "#1b2fb0",
    mid: "#3d63e8",
    lite: "#9fb8ff",
    dot: "#8fb0ff",
    ring: "#bcd0ff",
  },
  light: {
    bg1: "#fbfbfe",
    bg2: "#eff3fb",
    fg: "#16205a",
    mute: "#4b5fa8",
    acc: "#2f54d6",
    acc2: "#1f3bb3",
    line: "#9fb2ee",
    card: "#eaeffc",
    deep: "#1b2fb0",
    mid: "#3d63e8",
    lite: "#b9c9f7",
    dot: "#2a3f9c",
    ring: "#e6edff",
  },
};

function defs(c: ThemeColors): string {
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${c.line}" stop-opacity="0"/><stop offset="0.5" stop-color="${c.line}"/><stop offset="1" stop-color="${c.line}" stop-opacity="0"/></linearGradient>
<radialGradient id="g0" cx="0.35" cy="0.3" r="0.9"><stop offset="0" stop-color="${c.lite}"/><stop offset="0.5" stop-color="${c.mid}"/><stop offset="1" stop-color="${c.deep}"/></radialGradient>
<radialGradient id="g1" cx="0.6" cy="0.7" r="0.9"><stop offset="0" stop-color="${c.mid}"/><stop offset="1" stop-color="${c.deep}"/></radialGradient>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string, frame = true): string {
  const fr = frame ? `<path d="M0.75 0V${h}M${w - 0.75} 0V${h}" stroke="${c.line}" stroke-width="1.5"/>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${FONT}">${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>${body}${fr}</svg>`;
}

function star(x: number, y: number, s: number, col: string, op = 1): string {
  return `<path d="M${f1(x)} ${f1(y - s)}Q${f1(x)} ${f1(y)} ${f1(x + s)} ${f1(y)}Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y + s)}Q${f1(x)} ${f1(y)} ${f1(x - s)} ${f1(y)}Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y - s)}Z" fill="${col}" opacity="${f1(op)}"/>`;
}

function art(c: ThemeColors, ox: number, oy: number, s = 1.0): string {
  const blobs: [number, number, number][] = [
    [0, 0, 105], [-92, -68, 58], [88, -84, 48], [-66, 92, 64],
    [96, 72, 52], [8, -122, 34], [-120, 20, 30]
  ];
  let o = '';
  blobs.forEach(([x, y, R], i) => {
    const X = ox + x * s;
    const Y = oy + y * s;
    const r = R * s;
    const filled = i % 2 === 0;
    if (filled) {
      o += `<circle cx="${f1(X)}" cy="${f1(Y)}" r="${f1(r)}" fill="url(#g${(Math.floor(i / 2)) % 2})"/>`;
    }
    const n = Math.max(2, Math.floor(r / (8 * Math.max(s, 0.5))));
    const col = filled ? c.ring : c.dot;
    for (let j = 1; j <= n; j++) {
      const rr = (r * j) / n;
      o += `<circle cx="${f1(X)}" cy="${f1(Y)}" r="${f1(rr)}" fill="none" stroke="${col}" stroke-width="${f1(Math.max(1.2, 2 * s))}" stroke-dasharray="0.1 ${f1(Math.max(3, 4.2 * s))}" stroke-linecap="round" opacity="${filled ? 0.95 : 0.8}"/>`;
    }
  });
  return o;
}

function title(c: ThemeColors, y: number, label: string): string {
  return `<circle cx="62" cy="${y}" r="11" fill="none" stroke="${c.acc}" stroke-width="2"/>
<circle cx="62" cy="${y}" r="3.5" fill="${c.acc}"/>
<text x="84" y="${y + 6}" font-size="17" font-weight="600" fill="${c.fg}">${label}</text>`;
}

function divider(c: ThemeColors, y: number, w = 900): string {
  return `<rect x="40" y="${y}" width="${w - 80}" height="1" fill="url(#fade)"/>
<path d="M${w / 2} ${y - 4}l4 4-4 4-4-4z" fill="${c.acc}"/>`;
}

function header(c: ThemeColors, content: Content): string {
  let b = art(c, 700, 185, 1.0);
  b += star(120, 40, 7, c.acc) + star(560, 60, 6, c.acc2, 0.8) + star(840, 30, 8, c.acc);
  b += `<text x="60" y="95" font-size="20" fill="${c.mute}">Hi, I'm</text>
<text x="58" y="148" font-size="40" font-weight="700" fill="${c.fg}">${escapeXml(content.name)}</text>
<text x="60" y="198" font-size="24" fill="${c.acc}">${escapeXml(content.role)}</text>
<text x="60" y="246" font-size="15" fill="${c.fg}">${escapeXml(content.pillars || "AI   |   Math   |   Newest Technologies")}</text>`;

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${288 + i * 20}" font-size="13" fill="${c.mute}">${escapeXml(t)}</text>`;
  });

  b += `<rect x="858" y="52" width="26" height="104" rx="4" fill="${c.card}" stroke="${c.line}"/>`;
  "夢を築く".split("").forEach((ch, i) => {
    b += `<text x="871" y="${74 + i * 24}" font-size="15" text-anchor="middle" font-family="${JP}" fill="${c.acc2}">${ch}</text>`;
  });
  b += divider(c, 345);
  return wrap(900, 360, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const b = `<rect x="1" y="1" width="${w - 2}" height="38" rx="8" fill="${c.card}" stroke="${c.line}" stroke-width="1.5"/>
${star(24, 20, 6, c.acc)}
<text x="40" y="25" font-size="13" fill="${c.fg}">${escapeXml(label)}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${FONT}">${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = title(c, 42, "About");
  content.about.forEach((t, i) => {
    b += `<text x="60" y="${90 + i * 21}" font-size="13" fill="${c.fg}">${escapeXml(t)}</text>`;
  });
  b += `<rect x="440" y="75" width="1" height="165" fill="${c.line}"/>
<text x="475" y="92" font-size="14" font-weight="600" fill="${c.fg}">My journey</text>`;
  content.journey.forEach((item, i) => {
    const y = 130 + i * 30;
    b += `<rect x="478" y="${y - 12}" width="14" height="14" rx="3" fill="none" stroke="${c.acc}"/>
<text x="504" y="${y}" font-size="13" fill="${c.fg}">${escapeXml(item.lang)}</text>
<text x="640" y="${y}" font-size="13" fill="${c.acc}">→</text>
<text x="680" y="${y}" font-size="13" fill="${c.mute}">${escapeXml(item.area)}</text>`;
  });
  b += star(850, 120, 9, c.acc, 0.7) + star(870, 150, 5, c.acc2, 0.6);
  b += divider(c, 272);
  return wrap(900, 285, c, b);
}

function skills(c: ThemeColors, content: Content): string {
  let b = title(c, 38, "Technologies &amp; Skills");
  const w = 125, g = 14;
  content.skills.forEach((s, i) => {
    const x = 40 + (i % 6) * (w + g);
    const y = 70 + Math.floor(i / 6) * 78;
    b += `<rect x="${x}" y="${y}" width="${w}" height="64" rx="8" fill="${c.card}" stroke="${c.line}" stroke-width="1.3"/>
<text x="${x + w / 2}" y="${y + 29}" font-size="18" font-weight="700" text-anchor="middle" fill="${c.acc}">${escapeXml(s.mono)}</text>
<text x="${x + w / 2}" y="${y + 50}" font-size="11" text-anchor="middle" fill="${c.fg}">${escapeXml(s.label)}</text>`;
  });
  b += divider(c, 238);
  return wrap(900, 250, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 62, c, title(c, 36, "Selected Projects"));
}

function card(c: ThemeColors, titleStr: string, d1: string, d2: string, tags: string[]): string {
  const w = 208, h = 172;
  let b = `<defs><clipPath id="cl"><rect x="8" y="8" width="${w - 16}" height="52" rx="5"/></clipPath></defs>
<rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="10" fill="${c.card}" stroke="${c.line}" stroke-width="1.5"/>
<rect x="8" y="8" width="${w - 16}" height="52" rx="5" fill="${c.bg2}"/>
<g clip-path="url(#cl)">${art(c, 104, 34, 0.26)}</g>
<text x="16" y="86" font-size="14" font-weight="700" fill="${c.fg}">${escapeXml(titleStr)}</text>
<text x="16" y="106" font-size="10.5" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="120" font-size="10.5" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let x = 16;
  tags.forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${f1(x)}" y="138" width="${f1(cw)}" height="17" rx="4" fill="none" stroke="${c.line}"/>
<text x="${f1(x + cw / 2)}" y="150" font-size="8.5" text-anchor="middle" fill="${c.acc}">${escapeXml(t)}</text>`;
    x += cw + 5;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${FONT}">${defs(c)}${b}</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  let b = art(c, 0, 150, 0.38) + art(c, 900, 150, 0.38);
  b += `<text x="450" y="52" font-size="16" text-anchor="middle" fill="${c.acc2}">${escapeXml(content.footer.line1)}</text>
<text x="450" y="80" font-size="11" text-anchor="middle" fill="${c.mute}">${escapeXml(content.footer.line2)}</text>`;
  return wrap(900, 120, c, b);
}

export const constellationStyle: StyleModule = {
  id: "constellation",
  name: "Constellation",
  keywords: ["space", "indigo", "orbits", "astronomy", "minimal"],
  palette: {
    light: ["#fbfbfe", "#16205a", "#2f54d6", "#4b5fa8", "#1f3bb3"],
    dark: ["#060b2e", "#dfe7ff", "#5b8cff", "#8fa3e8", "#9ab6ff"],
  },
  motion: "calm",
  render(content: Content): RenderResult {
    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = header(c, content);
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
write_style("constellation", constellation_code)

# ==============================================================================
# 12. TERMINAL (Terminal 1337 Cyber Matrix)
# ==============================================================================
terminal_code = """import { Content, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',Consolas,'Courier New',monospace";

interface ThemeColors {
  bg: string;
  bg2: string;
  fg: string;
  mute: string;
  acc: string;
  acc2: string;
  line: string;
  card: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#030712",
    bg2: "#0f172a",
    fg: "#4ade80",
    mute: "#15803d",
    acc: "#22c55e",
    acc2: "#86efac",
    line: "#166534",
    card: "#05130b",
  },
  light: {
    bg: "#f0fdf4",
    bg2: "#dcfce7",
    fg: "#14532d",
    mute: "#15803d",
    acc: "#16a34a",
    acc2: "#166534",
    line: "#86efac",
    card: "#ffffff",
  },
};

const STYLE = `<style>
.term-cursor { animation: curBlink 1.1s steps(1) infinite; }
@keyframes curBlink { 50% { opacity: 0; } }
@media (prefers-reduced-motion: reduce) { .term-cursor { animation: none !important; } }
</style>`;

function terminalHeader(c: ThemeColors, w: number): string {
  return `<rect x="0" y="0" width="${w}" height="30" fill="${c.bg2}"/>
<circle cx="20" cy="15" r="5" fill="#ef4444"/>
<circle cx="36" cy="15" r="5" fill="#eab308"/>
<circle cx="52" cy="15" r="5" fill="#22c55e"/>
<line x1="0" y1="30" x2="${w}" y2="30" stroke="${c.line}" stroke-width="1"/>`;
}

function hero(c: ThemeColors, content: Content): string {
  const W = 900, H = 400;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
${STYLE}
<rect width="${W}" height="${H}" rx="12" fill="${c.bg}" stroke="${c.line}" stroke-width="1.5"/>
${terminalHeader(c, W)}
<g transform="translate(36, 68)">
  <text x="0" y="0" font-size="14" fill="${c.mute}">user@system:~$ whoami</text>
  <text x="0" y="42" font-size="34" font-weight="700" fill="${c.fg}">&gt; ${escapeXml(content.name)}</text>
  <text x="0" y="80" font-size="18" fill="${c.acc}">[ ${escapeXml(content.role)} ]</text>
  <text x="0" y="120" font-size="13" fill="${c.mute}">user@system:~$ cat /etc/pillars.conf</text>
  <text x="0" y="148" font-size="14" fill="${c.fg}">AI | Math | Systems Engineering</text>
  <text x="0" y="188" font-size="13" fill="${c.mute}">user@system:~$ cat /proc/mission</text>
  <text x="0" y="214" font-size="13" fill="${c.acc2}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="0" y="234" font-size="13" fill="${c.acc2}">${escapeXml(content.tagline[1] || "")}</text>
  <text x="0" y="268" font-size="14" fill="${c.fg}">user@system:~$ <rect x="156" y="254" width="10" height="18" fill="${c.fg}" class="term-cursor"/></text>
</g>
</svg>`;
}

function button(c: ThemeColors, label: string): string {
  const w = 150, h = 40;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">
<rect x="2" y="2" width="${w - 4}" height="${h - 4}" rx="6" fill="${c.card}" stroke="${c.line}" stroke-width="1.2"/>
<text x="14" y="25" font-size="12" font-weight="600" fill="${c.acc}">&gt;</text>
<text x="32" y="25" font-size="12" font-weight="600" fill="${c.fg}">${escapeXml(label)}</text>
</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 380;
  const lines = content.about.map((t, i) => `<text x="36" y="${80 + i * 24}" font-size="13" fill="${c.fg}">${escapeXml(t)}</text>`).join('');
  const journey = content.journey.map((item, i) => {
    return `<text x="480" y="${80 + i * 28}" font-size="13" fill="${c.acc}">[OK] ${escapeXml(item.lang)} <tspan fill="${c.mute}">--&gt; ${escapeXml(item.area)}</tspan></text>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="12" fill="${c.bg}" stroke="${c.line}" stroke-width="1.5"/>
${terminalHeader(c, W)}
<text x="36" y="54" font-size="13" fill="${c.mute}">// ABOUT &amp; PIPELINE JOURNEY</text>
<text x="480" y="54" font-size="13" fill="${c.mute}">// SERVICES LOG</text>
${lines}
${journey}
</svg>`;
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 320;
  const cardW = 125, cardH = 60;
  const cols = 6;
  const startX = 36, startY = 68;
  const gapX = 16, gapY = 16;

  const cards = content.skills.map((s, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = startX + col * (cardW + gapX);
    const y = startY + row * (cardH + gapY);
    return `<g transform="translate(${x}, ${y})">
<rect width="${cardW}" height="${cardH}" rx="6" fill="${c.card}" stroke="${c.line}" stroke-width="1"/>
<text x="12" y="26" font-size="14" font-weight="700" fill="${c.acc}">&gt; ${escapeXml(s.mono)}</text>
<text x="12" y="46" font-size="11" fill="${c.fg}">${escapeXml(s.label)}</text>
</g>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="12" fill="${c.bg}" stroke="${c.line}" stroke-width="1.5"/>
${terminalHeader(c, W)}
<text x="36" y="52" font-size="13" fill="${c.mute}">$ tech --list --installed</text>
${cards}
</svg>`;
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 64;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="8" fill="${c.bg}" stroke="${c.line}" stroke-width="1.2"/>
<text x="24" y="38" font-size="15" fill="${c.fg}">$ ls -la ~/projects/featured</text>
<text x="${W - 24}" y="38" text-anchor="end" font-size="12" fill="${c.mute}">total ${f1(8)}</text>
</svg>`;
}

function card(c: ThemeColors, titleStr: string, line1: string, line2: string, tags: string[]): string {
  const W = 208, H = 220;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="8" fill="${c.bg}" stroke="${c.line}" stroke-width="1.2"/>
<rect x="0" y="0" width="${W}" height="24" fill="${c.bg2}"/>
<circle cx="12" cy="12" r="3.5" fill="${c.acc}"/>
<text x="24" y="16" font-size="11" font-weight="600" fill="${c.fg}">app.exec</text>
<g transform="translate(14, 46)">
  <text x="0" y="16" font-size="15" font-weight="700" fill="${c.acc}">&gt; ${escapeXml(titleStr)}</text>
  <text x="0" y="42" font-size="10.5" fill="${c.mute}">${escapeXml(line1)}</text>
  <text x="0" y="58" font-size="10.5" fill="${c.mute}">${escapeXml(line2)}</text>
  <text x="0" y="90" font-size="10" fill="${c.acc}">tags:</text>
  ${tags.map((t, i) => `<text x="${i * 44}" y="108" font-size="9" fill="${c.fg}">#${escapeXml(t)}</text>`).join('')}
</g>
</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  const W = 900, H = 140;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
<rect width="${W}" height="${H}" rx="10" fill="${c.bg}" stroke="${c.line}" stroke-width="1.5"/>
${terminalHeader(c, W)}
<g transform="translate(450, 75)" text-anchor="middle">
  <text x="0" y="0" font-size="16" font-weight="700" fill="${c.fg}">[ PROCESS TERMINATED: 0 ]</text>
  <text x="0" y="24" font-size="12" fill="${c.mute}">${escapeXml(content.footer.line1)} // ${escapeXml(content.footer.line2)}</text>
</g>
</svg>`;
}

export const terminalStyle: StyleModule = {
  id: "terminal",
  name: "Terminal 1337",
  keywords: ["terminal", "cyber", "hacker", "retro", "1337"],
  palette: {
    light: ["#f0fdf4", "#14532d", "#16a34a", "#15803d", "#166534"],
    dark: ["#030712", "#4ade80", "#22c55e", "#15803d", "#86efac"],
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
write_style("terminal", terminal_code)

# ==============================================================================
# 13. QAMARIYA (Al-Andalus Stained Glass)
# ==============================================================================
qamariya_code = """import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
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
write_style("qamariya", qamariya_code)

# ==============================================================================
# 14. LILYPOND (Lily Pond & Frog)
# ==============================================================================
lilypond_code = """import { Content, RenderResult, StyleModule } from "../../types";
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
write_style("lilypond", lilypond_code)
