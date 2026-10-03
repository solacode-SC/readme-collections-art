import { Content, RenderResult, StyleModule } from "../../types";
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
