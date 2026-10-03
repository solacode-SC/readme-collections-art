import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";

interface ThemeColors {
  bg1: string;
  bg2: string;
  fg: string;
  mute: string;
  acc: string;
  acc2: string;
  line: string;
  card: string;
  ink: string;
  leaves: string[];
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg1: "#17120d",
    bg2: "#0d0a07",
    fg: "#f4ebd6",
    mute: "#c2b08f",
    acc: "#f28f3b",
    acc2: "#e8c46a",
    line: "#3d2f21",
    card: "#1e1710",
    ink: "#120e0b",
    leaves: ["#e0782f", "#c8262e", "#8f9d3d", "#d9a441"],
  },
  light: {
    bg1: "#f6eedc",
    bg2: "#eadfc5",
    fg: "#241a14",
    mute: "#6f5b48",
    acc: "#c4561a",
    acc2: "#8a6a1a",
    line: "#cdbb9a",
    card: "#fbf5e6",
    ink: "#120e0b",
    leaves: ["#d4691f", "#b3262c", "#7f8d33", "#c9942f"],
  },
};

const STYLE = `<style>
.fall{animation:fall linear infinite}
@keyframes fall{from{transform:translateY(-40px)}to{transform:translateY(520px)}}
.sway{transform-box:fill-box;transform-origin:center;animation:sway ease-in-out infinite alternate}
@keyframes sway{from{transform:translateX(-20px) rotate(-38deg)}to{transform:translateX(20px) rotate(38deg)}}
.leafsway{transform-box:fill-box;transform-origin:50% 100%;animation:ls 6s ease-in-out infinite alternate}
@keyframes ls{from{transform:rotate(-7deg)}to{transform:rotate(7deg)}}
.glow{animation:glow 6s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.2}50%{opacity:.85}}
.lid{opacity:0;animation:blink 7.5s linear infinite}
@keyframes blink{0%,93%,100%{opacity:0}94.5%,97%{opacity:1}}
.breathe{transform-box:fill-box;transform-origin:center;animation:br 26s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1)}to{transform:scale(1.06)}}
.flick{animation:fl 2.6s ease-in-out infinite}
@keyframes fl{0%,100%{opacity:.75}30%{opacity:1}55%{opacity:.6}80%{opacity:.95}}
.cursor{animation:cur 1.1s steps(1) infinite}
@keyframes cur{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.fall,.sway,.leafsway,.glow,.lid,.breathe,.flick,.cursor{animation:none}}
</style>`;

const LEAF = "M0 -11C9 -8 11 5 0 13C-11 5 -9 -8 0 -11Z";
function leaf(x: number, y: number, s: number, col: string, rot = 0, rib = "#000"): string {
  return `<g transform="translate(${f1(x)} ${f1(y)}) rotate(${f1(rot)}) scale(${f1(s)})"><path d="${LEAF}" fill="${col}"/>
<path d="M0 -8V11" stroke="${rib}" stroke-opacity=".3" stroke-width="1"/></g>`;
}

function falling(c: ThemeColors, n: number, xr: [number, number]): string {
  const o: string[] = [];
  for (let i = 0; i < n; i++) {
    const x = xr[0] + ((i * 53) % (xr[1] - xr[0]));
    const s = 0.75 + (i % 4) * 0.12;
    const col = c.leaves[i % c.leaves.length];
    const d = 16 + (i % 9);
    const sd = 4 + (i % 3);
    o.push(`<g transform="translate(${f1(x)} 0)"><g class="fall" style="animation-duration:${d}s;animation-delay:-${i * 1.6}s">
<g class="sway" style="animation-duration:${sd}s;animation-delay:-${i}s">${leaf(0, 0, s, col, (i * 35) % 180)}</g></g></g>`);
  }
  return o.join("");
}

function twig(
  x: number,
  y: number,
  ang: number,
  ln: number,
  depth: number,
  out: string[],
  seed = 0
): void {
  if (depth === 0 || ln < 5) return;
  const x2 = x + ln * Math.cos(ang);
  const y2 = y + ln * Math.sin(ang);
  out.push(`M${f1(x)} ${f1(y)}L${f1(x2)} ${f1(y2)}`);
  twig(x2, y2, ang - 0.42, ln * 0.7, depth - 1, out, seed + 1);
  twig(x2, y2, ang + 0.38, ln * 0.65, depth - 1, out, seed + 2);
}

function twigs(c: ThemeColors, specs: [number, number, number, number, number][]): string {
  const o: string[] = [];
  specs.forEach(([x, y, ang, ln, d], i) => {
    twig(x, y, (ang * Math.PI) / 180, ln, d, o, i);
  });
  return `<path d="${o.join("")}" fill="none" stroke="${c.mute}" stroke-opacity=".38" stroke-width="1.2" stroke-linecap="round"/>`;
}

function defs(c: ThemeColors): string {
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#ffb347" stop-opacity=".85"/><stop offset=".5" stop-color="#f28f3b" stop-opacity=".3"/><stop offset="1" stop-color="#f28f3b" stop-opacity="0"/></radialGradient>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">
${STYLE}${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>${body}
<path d="M.5 0V${h}M${w - 0.5} 0V${h}" stroke="${c.line}"/></svg>`;
}

function divider(c: ThemeColors, y: number, w = 900): string {
  const pts: [number, number][] = [];
  for (let x = 40; x <= w - 39; x += 6) {
    pts.push([x, y + 2.5 * Math.sin(x / 45)]);
  }
  const d = "M" + pts.map(([a, b]) => `${f1(a)} ${f1(b)}`).join("L");
  const o = [`<path d="${d}" fill="none" stroke="${c.line}" stroke-width="1.4"/>`];
  let idx = 0;
  for (let x = 80; x <= w - 60; x += 78) {
    const yy = y + 2.5 * Math.sin(x / 45);
    const up = idx % 2 === 0;
    o.push(
      `<g class="leafsway" style="animation-delay:-${idx * 0.8}s">${leaf(
        x,
        yy + (up ? -9 : 9),
        0.55,
        c.leaves[idx % 4],
        up ? -25 : 155,
        c.ink
      )}</g>`
    );
    idx++;
  }
  return o.join("");
}

function heading(c: ThemeColors, y: number, idx: string, label: string, x = 60): string {
  return (
    leaf(x, y, 0.85, c.acc, 35, c.ink) +
    `<text x="${x + 22}" y="${y + 4}" font-size="12" letter-spacing="2" fill="${c.mute}">${idx} /</text>
<text x="${x + 62}" y="${y + 4}" font-size="12" font-weight="700" letter-spacing="2" fill="${c.fg}">${escapeXml(label)}</text>`
  );
}

function lantern(c: ThemeColors, x: number, y: number): string {
  return `<circle class="flick" cx="${x}" cy="${y}" r="95" fill="url(#warm)"/>
<path d="M${x - 9} ${y - 24}a9 9 0 0 1 18 0" fill="none" stroke="${c.mute}" stroke-width="1.8"/>
<rect x="${x - 11}" y="${y - 20}" width="22" height="5" rx="2" fill="${c.mute}"/>
<rect x="${x - 10}" y="${y - 15}" width="20" height="26" rx="4" fill="#e0782f" fill-opacity=".9"/>
<ellipse class="flick" cx="${x}" cy="${y - 1}" rx="5" ry="8" fill="#ffe29a"/>
<rect x="${x - 12}" y="${y + 10}" width="24" height="5" rx="2" fill="${c.mute}"/>`;
}

function hero(c: ThemeColors, content: Content, heroImg: string, avImg: string): string {
  const px = 486, py = 48, pw = 384, ph = 365;
  let b = twigs(c, [
    [0, 0, 38, 70, 5],
    [410, 0, 100, 55, 4],
    [-4, 410, -30, 60, 4],
  ]);

  b += `<defs><clipPath id="pc"><rect x="${px}" y="${py}" width="${pw}" height="${ph}" rx="14"/></clipPath></defs>
<g clip-path="url(#pc)"><g class="breathe"><image x="${px}" y="${py}" width="${pw}" height="${ph}" preserveAspectRatio="xMidYMid slice" href="${heroImg}" xlink:href="${heroImg}"/></g>`;

  const EYES: [number, number][] = [[577, 147], [616, 128]];
  EYES.forEach(([ex, ey]) => {
    b += `<ellipse class="lid" cx="${ex}" cy="${ey}" rx="13" ry="16" fill="#14100f"/>
<circle class="glow" cx="${ex}" cy="${ey}" r="34" fill="url(#halo)"/>`;
  });

  b += `</g><rect x="${px}" y="${py}" width="${pw}" height="${ph}" rx="14" fill="none" stroke="${c.acc}" stroke-width="1.6"/>
<rect x="${px - 7}" y="${py - 7}" width="${pw + 14}" height="${ph + 14}" rx="19" fill="none" stroke="${c.line}" stroke-dasharray="2 5"/>`;

  b += `<defs><clipPath id="av"><circle cx="72" cy="34" r="13"/></clipPath></defs>
<image x="59" y="21" width="26" height="26" clip-path="url(#av)" href="${avImg}" xlink:href="${avImg}"/>
<circle cx="72" cy="34" r="13" fill="none" stroke="${c.acc}" stroke-width="1.4"/>
<text x="94" y="38" font-size="12" fill="${c.mute}">${escapeXml(content.handle)} <tspan fill="${c.line}">/</tspan> README</text>`;

  b += `<text x="60" y="118" font-size="13" letter-spacing="3" fill="${c.mute}">HI, I&apos;M</text>
<text x="58" y="168" font-size="38" font-family="${SERIF}" font-style="italic" fill="${c.fg}">${escapeXml(content.name)}</text>
<text x="60" y="212" font-size="16" font-weight="700" letter-spacing="3" fill="${c.acc}">${escapeXml(content.role.toUpperCase())}</text>
<rect class="cursor" x="308" y="198" width="9" height="16" fill="${c.acc}"/>
<text x="60" y="254" font-size="13" letter-spacing="1" fill="${c.fg}" xml:space="preserve">${escapeXml(content.pillars)}</text>
<rect x="60" y="270" width="36" height="2" fill="${c.acc}"/>`;

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${302 + i * 20}" font-size="12.5" fill="${c.mute}">${escapeXml(t)}</text>`;
  });

  b += divider(c, 430) + falling(c, 15, [330, 880]);
  return wrap(900, 445, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const b = `<rect x=".75" y=".75" width="${w - 1.5}" height="38.5" rx="19" fill="${c.card}" stroke="${c.acc}" stroke-opacity=".85"/>
${leaf(26, 20, 0.8, c.acc, 40, c.ink)}
<text x="44" y="24.5" font-size="12" letter-spacing="1.2" fill="${c.fg}">${escapeXml(label.toUpperCase())}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${MONO}">${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = heading(c, 42, "01", "ABOUT");
  const lines: string[] = [];
  content.about.forEach((p, idx) => {
    if (idx > 0) lines.push("");
    const words = p.split(" ");
    let cur = "";
    words.forEach((w) => {
      if ((cur + " " + w).trim().length > 44) {
        lines.push(cur.trim());
        cur = w;
      } else {
        cur = (cur + " " + w).trim();
      }
    });
    if (cur) lines.push(cur);
  });

  lines.slice(0, 8).forEach((t, i) => {
    b += `<text x="60" y="${92 + i * 21}" font-size="13" fill="${c.fg}" xml:space="preserve">${escapeXml(t)}</text>`;
  });

  b += `<path d="M450 74V246" stroke="${c.line}" stroke-dasharray="2 5"/>`;
  b += heading(c, 42, "02", "MY JOURNEY", 480);
  content.journey.slice(0, 5).forEach((j, i) => {
    const y = 96 + i * 30;
    b += `${leaf(488, y - 4, 0.62, c.leaves[i % 4], 30 + i * 25, c.ink)}
<text x="508" y="${y}" font-size="13" fill="${c.fg}">${escapeXml(j.lang)}</text>
<path d="M640 ${y - 4}H664M659 ${y - 8}L664 ${y - 4}L659 ${y}" fill="none" stroke="${c.acc}"/>
<text x="682" y="${y}" font-size="13" fill="${c.mute}">${escapeXml(j.area)}</text>`;
  });

  b += divider(c, 274);
  return wrap(900, 290, c, b);
}

function skills(c: ThemeColors, content: Content): string {
  let b = heading(c, 40, "03", "TECHNOLOGIES &amp; SKILLS");
  const w = 125, g = 14;
  content.skills.slice(0, 12).forEach((s, i) => {
    const x = 40 + (i % 6) * (w + g);
    const y = 68 + Math.floor(i / 6) * 66;
    b += `<rect x="${x + 0.5}" y="${y + 0.5}" width="${w - 1}" height="53" rx="10" fill="${c.card}" stroke="${c.line}"/>
${leaf(x + w - 14, y + 14, 0.5, c.leaves[i % 4], 40 + i * 30, c.ink)}
<text x="${x + w / 2}" y="${y + 25}" font-size="16" font-weight="700" text-anchor="middle" fill="${c.acc}">${escapeXml(s.mono)}</text>
<text x="${x + w / 2}" y="${y + 43}" font-size="10.5" text-anchor="middle" fill="${c.fg}">${escapeXml(s.label)}</text>`;
  });
  b += divider(c, 214);
  return wrap(900, 226, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 60, c, heading(c, 34, "04", "SELECTED PROJECTS"));
}

function card(
  c: ThemeColors,
  idx: number,
  title: string,
  d1: string,
  d2: string,
  tags: string[],
  cardImg: string
): string {
  const w = 208, h = 184;
  let b = `<defs><clipPath id="cl"><rect x="8" y="8" width="192" height="72" rx="8"/></clipPath></defs>
<rect x=".75" y=".75" width="${w - 1.5}" height="${h - 1.5}" rx="12" fill="${c.card}" stroke="${c.line}" stroke-width="1.5"/>
<image x="8" y="8" width="192" height="72" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)" href="${cardImg}" xlink:href="${cardImg}"/>
<rect x="8" y="8" width="192" height="72" rx="8" fill="none" stroke="${c.acc}" stroke-opacity=".7"/>
${leaf(186, 20, 0.55, c.leaves[idx % 4], 30 + idx * 40, c.ink)}
<text x="16" y="103" font-size="13.5" font-weight="700" fill="${c.fg}">${escapeXml(title)}</text>
<text x="16" y="122" font-size="10.5" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="136" font-size="10.5" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let x = 16;
  tags.slice(0, 4).forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${f1(x)}" y="152" width="${f1(cw)}" height="17" rx="8.5" fill="none" stroke="${c.line}"/>
<text x="${f1(x + cw / 2)}" y="163.5" font-size="8.5" text-anchor="middle" fill="${c.acc}">${escapeXml(t)}</text>`;
    x += cw + 5;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">${STYLE}${defs(c)}${b}</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  let b = "";
  for (let i = 0; i < 34; i++) {
    const x = 20 + i * 26;
    const y = 196 + ((i * 7) % 12);
    b += `<g class="leafsway" style="animation-delay:-${(i * 0.4).toFixed(1)}s;animation-duration:${(5 + (i % 3)).toFixed(1)}s">${leaf(
      x,
      y,
      0.9 + (i % 3) * 0.2,
      c.leaves[i % 4],
      ((i * 45) % 120) - 60,
      c.ink
    )}</g>`;
  }
  b = twigs(c, [[60, 0, 80, 60, 5], [840, 0, 100, 55, 5]]) + b;
  b += lantern(c, 450, 150);
  b += `<text x="450" y="46" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle" fill="${c.acc}" xml:space="preserve">${escapeXml(content.footer.line1.toUpperCase())}</text>
<text x="450" y="68" font-size="10.5" letter-spacing="1" text-anchor="middle" fill="${c.mute}" xml:space="preserve">${escapeXml(content.footer.line2)}</text>
<text x="450" y="226" font-size="9" text-anchor="middle" fill="${c.mute}" opacity=".9">Artwork by Crimson-Chains</text>`;
  b += falling(c, 6, [80, 820]);
  return wrap(900, 236, c, b);
}

export const gardenStyle: StyleModule = {
  id: "garden",
  name: "Garden",
  keywords: ["autumn", "storybook", "falling leaves"],
  palette: {
    light: ["#f6eedc", "#241a14", "#c4561a", "#8a6a1a", "#d4691f"],
    dark: ["#17120d", "#f4ebd6", "#f28f3b", "#e8c46a", "#e0782f"],
  },
  motion: "lively",
  image: { file: "source.jpg", credit: "Artwork by Crimson-Chains" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/garden/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 60, 736, 759], [700, 665], 0.8);
    const avCrop = ctx.cropToDataUrl(img, [255, 615, 345, 705], [64, 64], 0.82);

    const cropBoxes: [number, number, number, number][] = [
      [350, 440, 550, 515],
      [95, 430, 295, 505],
      [200, 610, 400, 685],
      [430, 790, 630, 865],
      [300, 780, 500, 855],
      [92, 190, 352, 288],
      [430, 590, 630, 665],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 150], 0.8)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop, avCrop);
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content);
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");

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
    Object.values(files).forEach((str) => (bytes += new Blob([str]).size));

    return { files, readme, meta: { bytes } };
  },
};
