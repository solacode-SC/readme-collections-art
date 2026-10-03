import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, pic } from "../../lib/svg";

const FONT = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const SERIF = "'Cormorant Garamond','Playfair Display',Georgia,'Times New Roman',serif";
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
  coral: string;
  jade: string;
  ring: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg1: "#6a0d10",
    bg2: "#2a0507",
    fg: "#f7eddb",
    mute: "#dcc196",
    acc: "#e8c56e",
    acc2: "#f6e0a0",
    line: "#a98230",
    card: "#3b0709",
    coral: "#e8935a",
    jade: "#4d9a8e",
    ring: "#f6e0a0",
  },
  light: {
    bg1: "#fffaf0",
    bg2: "#f3e5c9",
    fg: "#3a0a0c",
    mute: "#7d4b3b",
    acc: "#a8191c",
    acc2: "#b8893a",
    line: "#d2b06a",
    card: "#fff6e2",
    coral: "#d9763f",
    jade: "#2f7f74",
    ring: "#b8893a",
  },
};

function mix(a: string, b: string, t: number): string {
  const pa = [parseInt(a.slice(1, 3), 16), parseInt(a.slice(3, 5), 16), parseInt(a.slice(5, 7), 16)];
  const pb = [parseInt(b.slice(1, 3), 16), parseInt(b.slice(3, 5), 16), parseInt(b.slice(5, 7), 16)];
  return "#" + pa.map((v, i) => Math.round(v + (pb[i] - v) * t).toString(16).padStart(2, "0")).join("");
}

function defs(c: ThemeColors): string {
  const edge = mix(c.bg1, c.bg2, 0.5);
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="${c.line}" stop-opacity="0"/><stop offset=".5" stop-color="${c.acc2}"/><stop offset="1" stop-color="${c.line}" stop-opacity="0"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.acc2}"/><stop offset="1" stop-color="${c.line}"/></linearGradient>
<linearGradient id="side" x1="0" x2="1"><stop offset="0" stop-color="${edge}"/><stop offset=".55" stop-color="${edge}" stop-opacity=".75"/><stop offset="1" stop-color="${edge}" stop-opacity="0"/></linearGradient>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string, frame = true): string {
  const fr = frame ? `<path d="M1 0V${h}M${w - 1} 0V${h}" stroke="${c.line}" stroke-width="2"/>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${FONT}">
${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>${body}${fr}</svg>`;
}

function star(x: number, y: number, s: number, col: string, op = 1): string {
  return `<path d="M${x} ${y - s}Q${x} ${y} ${x + s} ${y}Q${x} ${y} ${x} ${y + s}Q${x} ${y} ${x - s} ${y}Q${x} ${y} ${x} ${y - s}Z" fill="${col}" opacity="${op}"/>`;
}

function bloom(x: number, y: number, r: number, c: ThemeColors, petals = 8, col?: string): string {
  const baseCol = col || c.acc;
  const o: string[] = [];
  const layers: [number, number][] = [[1, 0.55], [0.68, 0.8], [0.4, 1]];
  layers.forEach(([k, op], layer) => {
    for (let i = 0; i < petals; i++) {
      const a = (i * 360) / petals + layer * 22;
      o.push(
        `<ellipse cx="${x}" cy="${(y - r * k * 0.55).toFixed(1)}" rx="${(r * k * 0.34).toFixed(1)}" ry="${(r * k * 0.55).toFixed(1)}" transform="rotate(${a} ${x} ${y})" fill="${baseCol}" fill-opacity="${(op * 0.5).toFixed(2)}" stroke="${c.acc2}" stroke-width=".8"/>`
      );
    }
  });
  o.push(`<circle cx="${x}" cy="${y}" r="${(r * 0.14).toFixed(1)}" fill="${c.fg}"/>`);
  return o.join("");
}

function title(c: ThemeColors, y: number, label: string): string {
  return (
    bloom(62, y, 12, c, 6) +
    `<text x="86" y="${y + 7}" font-size="22" font-weight="700" font-family="${SERIF}" fill="${c.fg}">${escapeXml(label)}</text>`
  );
}

function divider(c: ThemeColors, y: number, w = 900): string {
  return `<rect x="40" y="${y}" width="${w - 80}" height="1.2" fill="url(#fade)"/>
<path d="M${w / 2} ${y - 6}l6 6.6-6 6.6-6-6.6z" fill="url(#gold)"/>
<circle cx="${w / 2 - 22}" cy="${y + 0.6}" r="2.2" fill="${c.acc2}"/><circle cx="${w / 2 + 22}" cy="${y + 0.6}" r="2.2" fill="${c.acc2}"/>`;
}

function hero(c: ThemeColors, content: Content, heroImg: string): string {
  let b = `<image x="400" y="0" width="500" height="360" preserveAspectRatio="xMidYMid slice" href="${heroImg}" xlink:href="${heroImg}"/>
<rect x="400" y="0" width="200" height="360" fill="url(#side)"/>`;
  b += star(120, 40, 7, c.acc) + star(300, 70, 5, c.acc2, 0.8) + star(600, 330, 6, c.acc2, 0.9);
  b += `<text x="60" y="95" font-size="20" fill="${c.mute}">Hi, I&apos;M</text>
<text x="58" y="148" font-size="42" font-weight="700" font-family="${SERIF}" fill="${c.fg}">${escapeXml(content.name)}</text>
<text x="60" y="198" font-size="24" fill="${c.acc}">${escapeXml(content.role)}</text>
<rect x="298" y="179" width="12" height="22" fill="${c.acc}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
<text x="60" y="246" font-size="15" fill="${c.fg}" xml:space="preserve">${escapeXml(content.pillars)}</text>`;

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${288 + i * 20}" font-size="13" fill="${c.mute}">${escapeXml(t)}</text>`;
  });

  b += `<rect x="858" y="40" width="28" height="108" rx="4" fill="${c.bg2}" fill-opacity=".72" stroke="${c.acc}"/>`;
  const kanji = content.options.useCJK ? "夢を築く" : "DREAM";
  Array.from(kanji).forEach((ch, i) => {
    b += `<text x="872" y="${63 + i * 25}" font-size="16" text-anchor="middle" font-family="${JP}" fill="${c.acc2}">${escapeXml(ch)}</text>`;
  });

  b += divider(c, 346);
  return wrap(900, 360, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const b = `<rect x="1" y="1" width="${w - 2}" height="38" rx="19" fill="${c.card}" stroke="${c.acc}" stroke-width="1.5"/>
${bloom(26, 20, 9, c, 6)}
<text x="44" y="25" font-size="13" fill="${c.fg}">${escapeXml(label)}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${FONT}">${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = title(c, 42, "About");
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
    b += `<text x="60" y="${90 + i * 21}" font-size="13" fill="${c.fg}" xml:space="preserve">${escapeXml(t)}</text>`;
  });

  b += `<rect x="440" y="75" width="1" height="165" fill="${c.line}"/>
<text x="475" y="94" font-size="19" font-weight="700" font-family="${SERIF}" fill="${c.fg}">My journey</text>`;

  content.journey.slice(0, 5).forEach((j, i) => {
    const y = 130 + i * 30;
    b += `<path d="M485 ${y - 11}l6 6-6 6-6-6z" fill="none" stroke="${c.acc}" stroke-width="1.4"/>
<text x="504" y="${y}" font-size="13" fill="${c.fg}">${escapeXml(j.lang)}</text>
<text x="640" y="${y}" font-size="13" fill="${c.acc}">→</text>
<text x="680" y="${y}" font-size="13" fill="${c.mute}">${escapeXml(j.area)}</text>`;
  });

  b += bloom(840, 135, 26, c, 8, c.coral) + star(872, 90, 7, c.acc2, 0.8) + star(815, 185, 5, c.acc, 0.7);
  b += divider(c, 272);
  return wrap(900, 285, c, b);
}

function skills(c: ThemeColors, content: Content): string {
  let b = title(c, 38, "Technologies &amp; Skills");
  const w = 125, g = 14;
  content.skills.slice(0, 12).forEach((s, i) => {
    const x = 40 + (i % 6) * (w + g);
    const y = 70 + Math.floor(i / 6) * 78;
    b += `<rect x="${x}" y="${y}" width="${w}" height="64" rx="10" fill="${c.card}" fill-opacity=".85" stroke="${c.line}" stroke-width="1.4"/>
<text x="${x + w / 2}" y="${y + 29}" font-size="18" font-weight="700" text-anchor="middle" fill="${c.acc}">${escapeXml(s.mono)}</text>
<text x="${x + w / 2}" y="${y + 50}" font-size="11" text-anchor="middle" fill="${c.fg}">${escapeXml(s.label)}</text>`;
  });
  b += divider(c, 238);
  return wrap(900, 250, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 62, c, title(c, 36, "Selected Projects"));
}

function card(
  c: ThemeColors,
  title: string,
  d1: string,
  d2: string,
  tags: string[],
  cardImg: string
): string {
  const w = 208, h = 172;
  let b = `<defs><clipPath id="cl"><rect x="8" y="8" width="${w - 16}" height="52" rx="6"/></clipPath></defs>
<rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="12" fill="${c.card}" stroke="${c.acc}" stroke-opacity=".8" stroke-width="1.5"/>
<image x="8" y="8" width="${w - 16}" height="52" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)" href="${cardImg}" xlink:href="${cardImg}"/>
<rect x="8" y="8" width="${w - 16}" height="52" rx="6" fill="none" stroke="${c.acc2}" stroke-opacity=".7"/>
<text x="16" y="86" font-size="14" font-weight="700" fill="${c.fg}">${escapeXml(title)}</text>
<text x="16" y="106" font-size="10.5" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="120" font-size="10.5" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let x = 16;
  tags.slice(0, 4).forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${x}" y="138" width="${cw.toFixed(1)}" height="17" rx="8.5" fill="none" stroke="${c.line}"/>
<text x="${(x + cw / 2).toFixed(1)}" y="150" font-size="8.5" text-anchor="middle" fill="${c.acc}">${escapeXml(t)}</text>`;
    x += cw + 5;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${FONT}">${defs(c)}${b}</svg>`;
}

function footer(c: ThemeColors, content: Content, footerImg: string): string {
  let b = `<image x="0" y="0" width="900" height="129" preserveAspectRatio="xMidYMid slice" href="${footerImg}" xlink:href="${footerImg}"/>
<rect width="900" height="120" fill="${c.bg2}" fill-opacity=".62"/>
<text x="450" y="52" font-size="19" font-weight="700" font-family="${SERIF}" text-anchor="middle" fill="${c.acc2}" xml:space="preserve">${escapeXml(content.footer.line1)}</text>
<text x="450" y="80" font-size="11" text-anchor="middle" fill="${c.fg}" xml:space="preserve">${escapeXml(content.footer.line2)}</text>`;
  b += star(120, 60, 7, c.acc2) + star(780, 60, 7, c.acc2);
  return wrap(900, 120, c, b);
}

export const phoenixStyle: StyleModule = {
  id: "phoenix",
  name: "Phoenix",
  keywords: ["crimson", "gold", "regal"],
  palette: {
    light: ["#fffaf0", "#3a0a0c", "#a8191c", "#b8893a", "#d9763f"],
    dark: ["#6a0d10", "#f7eddb", "#e8c56e", "#f6e0a0", "#e8935a"],
  },
  motion: "calm",
  image: { file: "source.jpg", note: "Crimson phoenix painting" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/phoenix/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 140, 735, 715], [500, 392], 0.82);
    const footerCrop = ctx.cropToDataUrl(img, [0, 640, 735, 745], [900, 129], 0.78);

    const cropBoxes: [number, number, number, number][] = [
      [20, 300, 320, 381],
      [330, 90, 630, 171],
      [350, 310, 650, 391],
      [435, 380, 735, 461],
      [0, 730, 300, 811],
      [250, 590, 550, 671],
      [0, 480, 300, 561],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 108], 0.8)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop);
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content, footerCrop);
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");

      content.projects.forEach((proj, idx) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
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
