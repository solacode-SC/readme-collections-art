import { Content, RenderResult, StyleModule } from "../../types";
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
