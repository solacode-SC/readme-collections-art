import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "'Cormorant Garamond','Playfair Display',Georgia,'Times New Roman',serif";
const MONO = "'JetBrains Mono','SF Mono',Consolas,Menlo,monospace";

interface ThemeColors {
  bg0: string;
  bg1: string;
  bg2: string;
  gold0: string;
  gold1: string;
  fade0: string;
  fade1: string;
  imageFade: string;
  text_primary: string;
  text_muted: string;
  text_gold: string;
  border: string;
  card_bg: string;
  chip_bg: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg0: "#06132D", bg1: "#0B2047", bg2: "#103171",
    gold0: "#F1CD72", gold1: "#D8A63A",
    fade0: "#557CC1", fade1: "#F1CD72",
    imageFade: "#06132D",
    text_primary: "#F7EBCB",
    text_muted: "#C7D4EC",
    text_gold: "#F1CD72",
    border: "#D8A63A",
    card_bg: "#0B2047",
    chip_bg: "rgba(11,32,71,0.7)"
  },
  light: {
    bg0: "#F7F1DF", bg1: "#E9DFC5", bg2: "#97a2b4",
    gold0: "#D7A83D", gold1: "#B88320",
    fade0: "#9DB4D8", fade1: "#D7A83D",
    imageFade: "#F7F1DF",
    text_primary: "#1A2542",
    text_muted: "#4A5873",
    text_gold: "#996E14",
    border: "#B88320",
    card_bg: "#E9DFC5",
    chip_bg: "rgba(233,223,197,0.7)"
  }
};

function starPulser(x: number, y: number, delay = "0s", s = 1.0, dur = "3.2s"): string {
  const d = `M${f1(x)} ${f1(y - 7 * s)} Q${f1(x)} ${f1(y)} ${f1(x + 7 * s)} ${f1(y)} Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y + 7 * s)} Q${f1(x)} ${f1(y)} ${f1(x - 7 * s)} ${f1(y)} Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y - 7 * s)}Z`;
  return `<g fill="url(#gold)" opacity=".8"><path d="${d}"><animate attributeName="opacity" values=".25;.95;.25" dur="${dur}" begin="${delay}" repeatCount="indefinite"/></path></g>`;
}

function bloom(cx: number, cy: number, r = 24, rot = 0): string {
  const petals: string[] = [];
  for (let a = 0; a < 360; a += 45) {
    petals.push(`<ellipse cx="${cx}" cy="${cy}" rx="${f1(r * 0.4)}" ry="${f1(r * 0.95)}" fill="none" stroke="url(#gold)" stroke-width="0.8" opacity=".65" transform="rotate(${a + rot} ${cx} ${cy})"/>`);
  }
  return `<g>${petals.join("")}<circle cx="${cx}" cy="${cy}" r="${f1(r * 0.2)}" fill="url(#gold)" opacity=".9"/></g>`;
}

function root(w: number, h: number, T: ThemeColors, body: string): string {
  const defs = `<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${T.bg0}"/>
      <stop offset=".55" stop-color="${T.bg1}"/>
      <stop offset="1" stop-color="${T.bg2}"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${T.gold0}"/>
      <stop offset="1" stop-color="${T.gold1}"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="${T.fade0}" stop-opacity="0"/>
      <stop offset=".5" stop-color="${T.fade1}" stop-opacity=".9"/>
      <stop offset="1" stop-color="${T.fade0}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="imageFade" x1="0" x2="1">
      <stop offset="0" stop-color="${T.imageFade}" stop-opacity=".98"/>
      <stop offset=".45" stop-color="${T.imageFade}" stop-opacity=".45"/>
      <stop offset=".75" stop-color="${T.imageFade}" stop-opacity=".08"/>
      <stop offset="1" stop-color="${T.imageFade}" stop-opacity="0"/>
    </linearGradient>
    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>`;

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">
  ${defs}
  <rect width="${w}" height="${h}" fill="url(#bg)"/>
  ${body}
  <rect x="1" y="1" width="${w - 2}" height="${h - 2}" rx="8" fill="none" stroke="${T.border}" stroke-width="1.5"/>
</svg>`;
}

function hero(T: ThemeColors, content: Content, artImg: string): string {
  const W = 1100, H = 360;
  const stars = [
    starPulser(110, 45, "0s", 1.0), starPulser(320, 73, "1.1s", 0.7),
    starPulser(1010, 58, "0.5s", 1.0), starPulser(960, 290, "1.8s", 0.8),
    starPulser(520, 310, "2.2s", 0.6)
  ].join("");

  const blooms = bloom(70, 70, 22, 15) + bloom(1030, 290, 26, 30);

  const body = `
  <image x="420" y="0" width="680" height="360" preserveAspectRatio="xMidYMid slice" href="${artImg}"/>
  <rect x="420" y="0" width="330" height="360" fill="url(#imageFade)"/>
  ${stars}
  ${blooms}

  <!-- Text -->
  <text x="62" y="78" font-size="19" fill="${T.text_muted}">Hi, I'm</text>
  <text x="60" y="135" font-size="42" font-weight="700" font-family="${SERIF}" fill="${T.text_primary}">${escapeXml(content.name)}</text>
  <text x="62" y="180" font-size="23" fill="${T.text_gold}">${escapeXml(content.role)}</text>
  <text x="62" y="220" font-size="14" fill="${T.text_primary}">${escapeXml(content.pillars)}</text>
  <text x="62" y="264" font-size="13" fill="${T.text_muted}">${escapeXml(content.tagline[0] || "")}</text>
  <text x="62" y="286" font-size="13" fill="${T.text_muted}">${escapeXml(content.tagline[1] || "")}</text>
  `;
  return root(W, H, T, body);
}

function button(T: ThemeColors, text: string): string {
  const W = 166, H = 42;
  const body = `
  <rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="6" fill="url(#bg)" stroke="url(#gold)" stroke-width="1.2"/>
  ${starPulser(20, 21, "0s", 0.55)}
  <text x="${W / 2 + 5}" y="25" text-anchor="middle" font-size="12" font-weight="700" fill="${T.text_primary}" letter-spacing="1.5">${escapeXml(text)}</text>
  `;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" font-family="${MONO}">
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${T.bg0}"/><stop offset="1" stop-color="${T.bg1}"/></linearGradient>
      <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${T.gold0}"/><stop offset="1" stop-color="${T.gold1}"/></linearGradient>
    </defs>
    ${body}
  </svg>`;
}

function about(T: ThemeColors, content: Content): string {
  const W = 1100, H = 290;
  const stars = starPulser(80, 42, "0.3s", 0.8) + starPulser(1020, 240, "1.5s", 0.7);
  const bioLines = content.about.map((ln, i) =>
    `<text x="60" y="${92 + i * 26}" font-size="14.5" fill="${T.text_muted}">${escapeXml(ln)}</text>`
  ).join("");

  const journeyItems = content.journey.slice(0, 5).map(({ lang, area }, i) => {
    const y = 92 + i * 36;
    return `${starPulser(620, y - 4, `${i * 0.4}s`, 0.5)}`
      + `<text x="640" y="${y}" font-size="14" font-weight="700" fill="${T.text_gold}">${escapeXml(lang)}</text>`
      + `<path d="M740,${y - 4}H790" stroke="url(#gold)" stroke-width="1" stroke-dasharray="2 5" opacity=".7"/>`
      + `<text x="806" y="${y}" font-size="14" font-family="${SERIF}" fill="${T.text_primary}">${escapeXml(area)}</text>`;
  }).join("");

  const body = `
  ${stars}
  <text x="60" y="48" font-size="20" font-family="${SERIF}" font-weight="700" fill="${T.text_gold}" letter-spacing="2">ABOUT ME</text>
  <text x="620" y="48" font-size="20" font-family="${SERIF}" font-weight="700" fill="${T.text_gold}" letter-spacing="2">MY JOURNEY</text>
  <path d="M60,62H480M620,62H1040" stroke="url(#fade)" stroke-width="1.2"/>
  ${bioLines}
  ${journeyItems}
  `;
  return root(W, H, T, body);
}

function skills(T: ThemeColors, content: Content): string {
  const W = 1100, H = 250;
  const stars = starPulser(80, 40, "0s", 0.8) + starPulser(1020, 210, "1.2s", 0.7);

  const pills = content.skills.slice(0, 12).map(({ label: name, mono }, i) => {
    const row = Math.floor(i / 6);
    const col = i % 6;
    const x = 60 + col * 165;
    const y = 80 + row * 70;
    return `<rect x="${x}" y="${y}" width="150" height="48" rx="6" fill="${T.chip_bg}" stroke="url(#gold)" stroke-width="0.8"/>`
      + `${starPulser(x + 16, y + 24, `${i * 0.3}s`, 0.45)}`
      + `<text x="${x + 32}" y="${y + 28}" font-size="13" font-weight="700" fill="${T.text_primary}">${escapeXml(name)}</text>`
      + `<text x="${x + 138}" y="${y + 28}" text-anchor="end" font-size="11" fill="${T.text_gold}">${escapeXml(mono)}</text>`;
  }).join("");

  const body = `
  ${stars}
  <text x="60" y="46" font-size="20" font-family="${SERIF}" font-weight="700" fill="${T.text_gold}" letter-spacing="2">TECHNOLOGIES &amp; SKILLS</text>
  <path d="M60,58H1040" stroke="url(#fade)" stroke-width="1.2"/>
  ${pills}
  `;
  return root(W, H, T, body);
}

function projectsTitle(T: ThemeColors): string {
  const W = 1100, H = 65;
  const stars = starPulser(40, 32, "0s", 0.8) + starPulser(1060, 32, "1.5s", 0.8);
  const body = `
  ${stars}
  <text x="${W / 2}" y="38" text-anchor="middle" font-size="20" font-family="${SERIF}" font-weight="700" fill="${T.text_gold}" letter-spacing="3">SELECTED PROJECTS</text>
  <path d="M120,48H400M700,48H980" stroke="url(#fade)" stroke-width="1.2"/>
  `;
  return root(W, H, T, body);
}

function card(T: ThemeColors, i: number, title: string, desc: string, tags: string[], cardImg: string): string {
  const W = 260, H = 190;
  const chips = tags.slice(0, 3).map((t, idx) => {
    const x = 12 + idx * 78;
    return `<rect x="${x}" y="156" width="72" height="18" rx="4" fill="${T.chip_bg}" stroke="url(#gold)" stroke-width="0.6"/>`
      + `<text x="${x + 36}" y="169" text-anchor="middle" font-size="9.5" fill="${T.text_primary}">${escapeXml(t)}</text>`;
  }).join("");

  const body = `
  <clipPath id="cimg${i}"><rect x="8" y="8" width="244" height="78" rx="4"/></clipPath>
  <image x="8" y="8" width="244" height="78" preserveAspectRatio="xMidYMid slice" href="${cardImg}" clip-path="url(#cimg${i})"/>
  <rect x="8" y="8" width="244" height="78" rx="4" fill="none" stroke="url(#gold)" stroke-width="0.8"/>
  <text x="12" y="110" font-size="14" font-weight="700" fill="${T.text_primary}">${escapeXml(title)}</text>
  <text x="12" y="128" font-size="10.5" fill="${T.text_muted}">${escapeXml(desc.slice(0, 36))}</text>
  <text x="12" y="142" font-size="10.5" fill="${T.text_muted}">${escapeXml(desc.slice(36, 72))}</text>
  ${chips}
  `;
  return root(W, H, T, body);
}

function footer(T: ThemeColors, content: Content): string {
  const W = 1100, H = 150;
  const stars = starPulser(150, 75, "0s", 1.0) + starPulser(950, 75, "1.6s", 1.0);
  const bloomSvg = bloom(W / 2, 38, 22, 0);
  const brand = content.brand?.latin || "NashirTech";

  const body = `
  ${stars}
  ${bloomSvg}
  <text x="${W / 2}" y="85" text-anchor="middle" font-size="20" font-family="${SERIF}" font-weight="700" fill="${T.text_gold}" letter-spacing="3">${escapeXml(content.footer.line1)}</text>
  <text x="${W / 2}" y="110" text-anchor="middle" font-size="12" fill="${T.text_muted}" letter-spacing="1.5">${escapeXml(content.footer.line2)}</text>
  <text x="${W / 2}" y="132" text-anchor="middle" font-size="11" fill="${T.text_primary}">${escapeXml(brand)}</text>
  `;
  return root(W, H, T, body);
}

export const floralStyle: StyleModule = {
  id: "floral",
  name: "Gilded Floral Botanical",
  keywords: ["floral", "botanical", "gilded", "stars", "gold", "royal"],
  palette: {
    dark: ["#06132D", "#0B2047", "#103171", "#F1CD72", "#D8A63A"],
    light: ["#F7F1DF", "#E9DFC5", "#97a2b4", "#D7A83D", "#B88320"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/floral/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 680, 360], [680, 360], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [20, 20, 260, 100],
      [80, 100, 320, 180],
      [140, 180, 380, 260],
      [200, 260, 440, 340],
      [50, 150, 290, 230],
      [120, 220, 360, 300],
      [220, 80, 460, 160],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [244, 78], 0.85)
    );

    const files: Record<string, string> = {};

    for (const theme of ["dark", "light"] as const) {
      const T = THEMES[theme];
      const heroSvg = hero(T, content, heroCrop);
      files[`hero-${theme}.svg`] = heroSvg;
      files[`header-${theme}.svg`] = heroSvg;
      files[`btn-github-${theme}.svg`] = button(T, "GITHUB");
      files[`btn-linkedin-${theme}.svg`] = button(T, "LINKEDIN");
      files[`btn-portfolio-${theme}.svg`] = button(T, "PORTFOLIO");
      files[`about-${theme}.svg`] = about(T, content);
      files[`skills-${theme}.svg`] = skills(T, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(T);
      files[`footer-${theme}.svg`] = footer(T, content);

      content.projects.forEach((proj, i) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(T, i, proj.title, `${proj.line1} ${proj.line2}`, proj.tags, cardCrops[i]);
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items.map((p) => `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `${p.title}: ${p.line1} ${p.line2}`, "24%")}</a>`).join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("header", `${content.name}, ${content.role}. Gilded floral botanical identity.`, "100%"),
      `<a href="${content.github}">${pic("btn-github", "GitHub profile", "150")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn profile", "150")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio website", "150")}</a>`,
      pic("about", "About me and my journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", `${content.footer.line1}. ${content.footer.line2}`, "100%"),
    ].filter(Boolean);

    const readme = `<div align="center">\n\n${readmeParts.join("\n\n")}\n\n</div>\n`;
    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += new Blob([str]).size));
    return { files, readme, meta: { bytes } };
  }
};
export default floralStyle;
