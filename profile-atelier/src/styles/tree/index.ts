import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

interface ThemeColors {
  bgGrad0: string;
  bgGrad1: string;
  bgGrad2: string;
  contour0: string;
  contour1: string;
  contour2: string;
  cyan: string;
  teal: string;
  gold: string;
  textPrimary: string;
  textMuted: string;
  panel: string;
  panelBorder: string;
  badgeBg: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bgGrad0: "#09111c", bgGrad1: "#0e1a2b", bgGrad2: "#09111c",
    contour0: "#56cfe1", contour1: "#72efdd", contour2: "#e0a96d",
    cyan: "#56cfe1", teal: "#72efdd", gold: "#e0a96d",
    textPrimary: "#f2f7fc", textMuted: "#a2bad2",
    panel: "#0e1a2b", panelBorder: "rgba(86,207,225,0.25)",
    badgeBg: "#132338"
  },
  light: {
    bgGrad0: "#f5f8fc", bgGrad1: "#ebf2fa", bgGrad2: "#f5f8fc",
    contour0: "#1a6f87", contour1: "#1d877a", contour2: "#9e6831",
    cyan: "#1a6f87", teal: "#1d877a", gold: "#9e6831",
    textPrimary: "#0b1523", textMuted: "#3e556e",
    panel: "#ebf2fa", panelBorder: "rgba(26,111,135,0.25)",
    badgeBg: "#dfe8f2"
  }
};

const CSS = `
  .font-sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", Roboto, Helvetica, Arial, sans-serif; }
  .font-serif { font-family: "Cinzel", "Playfair Display", Georgia, "Times New Roman", serif; }
  .font-mono { font-family: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace; }
  
  .contour-drift-0 { stroke-dasharray: 6 8; animation: drift0 28s linear infinite; }
  .contour-drift-1 { stroke-dasharray: 10 10; animation: drift1 34s linear infinite; }
  .pulse-glow { animation: pulseGlow 4s ease-in-out infinite alternate; }
  .badge-spin { animation: badgeSpin 40s linear infinite; }

  @keyframes drift0 {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: -280; }
  }
  @keyframes drift1 {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: 320; }
  }
  @keyframes pulseGlow {
      0% { opacity: 0.35; }
      100% { opacity: 0.85; }
  }
  @keyframes badgeSpin {
      from { transform: rotate(0deg); }
      to { transform: rotate(360deg); }
  }
  @media (prefers-reduced-motion: reduce) {
      .contour-drift-0, .contour-drift-1, .pulse-glow, .badge-spin {
          animation: none !important;
      }
  }
`;

function root(w: number, h: number, T: ThemeColors, body: string): string {
  const defs = `<defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="${T.bgGrad0}"/>
      <stop offset="55%" stop-color="${T.bgGrad1}"/>
      <stop offset="100%" stop-color="${T.bgGrad2}"/>
    </linearGradient>
    <linearGradient id="artFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000" stop-opacity="0"/>
      <stop offset="28%" stop-color="#fff" stop-opacity="1"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="1"/>
    </linearGradient>
    <mask id="treeMask">
      <rect x="660" y="30" width="510" height="520" rx="28" fill="url(#artFade)"/>
    </mask>
    <clipPath id="heroFrame">
      <rect x="660" y="30" width="510" height="520" rx="28"/>
    </clipPath>
    <clipPath id="knotBadge">
      <circle cx="680" cy="450" r="54"/>
    </clipPath>
  </defs><style>${CSS}</style>`;

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
  ${defs}
  <rect width="${w}" height="${h}" fill="url(#bgGrad)"/>
  ${body}
</svg>`;
}

function generateWhorlContours(cx: number, cy: number, T: ThemeColors): string {
  const loops: string[] = [];
  for (let r = 40; r <= 240; r += 24) {
    const pts: string[] = [];
    for (let a = 0; a <= 360; a += 30) {
      const rad = (a * Math.PI) / 180;
      const wobble = 1 + 0.08 * Math.sin(rad * 3) + 0.05 * Math.cos(rad * 5);
      const px = cx + r * wobble * Math.cos(rad);
      const py = cy + r * wobble * 0.75 * Math.sin(rad);
      pts.push(`${f1(px)},${f1(py)}`);
    }
    const color = r % 48 === 0 ? T.gold : T.cyan;
    const cls = r % 48 === 0 ? "contour-drift-1" : "contour-drift-0";
    loops.push(`<path d="M ${pts.join(" L ")} Z" fill="none" stroke="${color}" stroke-width="1.1" opacity=".4" class="${cls}"/>`);
  }
  return loops.join("\n");
}

function header(T: ThemeColors, content: Content, artImg: string): string {
  const W = 1200, H = 580;
  const whorl = generateWhorlContours(915, 290, T);

  const body = `
  <!-- TOPOGRAPHIC BACKGROUND CONTOURS -->
  <g opacity=".6">
    ${whorl}
  </g>

  <!-- HERO IMAGE WITH BOTANICAL ORGANIC BLEND -->
  <g clip-path="url(#heroFrame)" mask="url(#treeMask)">
    <image x="660" y="30" width="510" height="520" preserveAspectRatio="xMidYMid slice" href="${artImg}"/>
  </g>
  <rect x="660" y="30" width="510" height="520" rx="28" fill="none" stroke="${T.cyan}" stroke-width="1.6" opacity=".5"/>

  <!-- WHORL BADGE -->
  <g>
    <circle cx="680" cy="450" r="54" fill="${T.badgeBg}" stroke="${T.gold}" stroke-width="1.5"/>
    <g class="badge-spin" style="transform-origin: 680px 450px;">
      <circle cx="680" cy="450" r="44" fill="none" stroke="${T.cyan}" stroke-width="1" stroke-dasharray="4 6"/>
    </g>
    <text x="680" y="445" text-anchor="middle" fill="${T.gold}" font-size="11" font-weight="700" letter-spacing="1.5" class="font-mono">ORGANIC</text>
    <text x="680" y="462" text-anchor="middle" fill="${T.teal}" font-size="9" font-weight="600" letter-spacing="1" class="font-mono">GROWTH</text>
  </g>

  <!-- TEXT CONTENT -->
  <g transform="translate(70, 70)">
    <rect x="0" y="0" width="230" height="28" rx="14" fill="${T.panel}" stroke="${T.panelBorder}" stroke-width="1"/>
    <circle cx="16" cy="14" r="4" fill="${T.teal}" class="pulse-glow"/>
    <text x="32" y="18" fill="${T.textMuted}" font-size="10.5" font-weight="600" letter-spacing="1.1" class="font-mono">${escapeXml(content.pillars.slice(0, 32).toUpperCase())}</text>

    <text x="0" y="90" fill="${T.cyan}" font-size="14" font-weight="600" letter-spacing="2" class="font-mono">HI, I'M</text>
    <text x="0" y="152" fill="${T.textPrimary}" font-size="44" font-weight="700" letter-spacing="-0.5" class="font-serif">${escapeXml(content.name)}</text>
    <text x="0" y="196" fill="${T.cyan}" font-size="20" font-weight="600" letter-spacing="0.5" class="font-sans">${escapeXml(content.role)}</text>

    <line x1="0" y1="225" x2="480" y2="225" stroke="${T.cyan}" stroke-width="1.2" opacity=".35"/>

    <text x="0" y="260" fill="${T.textMuted}" font-size="15" font-style="italic" class="font-serif">"${escapeXml(content.tagline[0] || "")}"</text>
    <text x="0" y="285" fill="${T.textMuted}" font-size="14" class="font-sans">${escapeXml(content.tagline[1] || "")}</text>
  </g>
  `;
  return root(W, H, T, body);
}

function divider(T: ThemeColors): string {
  const W = 1200, H = 54;
  const d1 = "M 50 27 Q 300 10 600 27 T 1150 27";
  const d2 = "M 50 27 Q 300 44 600 27 T 1150 27";
  const body = `
  <path d="${d1}" fill="none" stroke="${T.cyan}" stroke-width="1.2" opacity=".6" class="contour-drift-0"/>
  <path d="${d2}" fill="none" stroke="${T.gold}" stroke-width="1" opacity=".5" class="contour-drift-1"/>
  <circle cx="600" cy="27" r="4" fill="${T.teal}" class="pulse-glow"/>
  `;
  return root(W, H, T, body);
}

function about(T: ThemeColors, content: Content): string {
  const W = 1200, H = 310;
  const pillars = content.journey.slice(0, 4).map(({ lang, area }) => ({ title: area.toUpperCase(), subtitle: lang, tech: lang }));

  const cards = pillars.map((p, i) => {
    const x = 70 + i * 270;
    const y = 110;
    return `<rect x="${x}" y="${y}" width="250" height="150" rx="14" fill="${T.panel}" stroke="${T.panelBorder}" stroke-width="1.2"/>
    <circle cx="${x + 24}" cy="${y + 28}" r="5" fill="${T.gold}"/>
    <text x="${x + 40}" y="${y + 32}" fill="${T.cyan}" font-size="11" font-weight="700" letter-spacing="1" class="font-mono">${escapeXml(p.tech)}</text>
    <text x="${x + 20}" y="${y + 72}" fill="${T.textPrimary}" font-size="14" font-weight="700" class="font-sans">${escapeXml(p.title)}</text>
    <text x="${x + 20}" y="${y + 98}" fill="${T.textMuted}" font-size="11.5" class="font-sans">${escapeXml(p.subtitle)}</text>
    <line x1="${x + 20}" y1="${y + 120}" x2="${x + 230}" y2="${y + 120}" stroke="${T.cyan}" stroke-width="0.8" opacity=".25"/>`;
  }).join("\n");

  const body = `
  <g transform="translate(70, 40)">
    <text x="0" y="24" fill="${T.gold}" font-size="13" font-weight="700" letter-spacing="2" class="font-mono">METHODOLOGY</text>
    <text x="0" y="52" fill="${T.textPrimary}" font-size="24" font-weight="700" class="font-serif">Architectural Pillars &amp; Foundations</text>
  </g>
  ${cards}
  `;
  return root(W, H, T, body);
}

function skills(T: ThemeColors, content: Content): string {
  const W = 1200, H = 330;
  const items = content.skills.slice(0, 12);

  const pills = items.map(({ label: name, mono }, i) => {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const x = 70 + col * 270;
    const y = 100 + row * 64;
    return `<rect x="${x}" y="${y}" width="250" height="50" rx="10" fill="${T.panel}" stroke="${T.panelBorder}" stroke-width="1"/>
    <circle cx="${x + 20}" cy="${y + 25}" r="3" fill="${T.teal}" class="pulse-glow"/>
    <text x="${x + 36}" y="${y + 29}" fill="${T.textPrimary}" font-size="13.5" font-weight="600" class="font-sans">${escapeXml(name)}</text>
    <rect x="${x + 196}" y="${y + 14}" width="42" height="22" rx="6" fill="${T.badgeBg}"/>
    <text x="${x + 217}" y="${y + 29}" text-anchor="middle" fill="${T.gold}" font-size="11" font-weight="700" class="font-mono">${escapeXml(mono)}</text>`;
  }).join("\n");

  const body = `
  <g transform="translate(70, 40)">
    <text x="0" y="24" fill="${T.gold}" font-size="13" font-weight="700" letter-spacing="2" class="font-mono">SKILLS MATRIX</text>
    <text x="0" y="52" fill="${T.textPrimary}" font-size="24" font-weight="700" class="font-serif">Annular Growth Rings &amp; Stack</text>
  </g>
  ${pills}
  `;
  return root(W, H, T, body);
}

function card(T: ThemeColors, i: number, title: string, desc: string, tags: string[], cardImg: string): string {
  const W = 280, H = 220;
  const chipSvgs = tags.slice(0, 3).map((t, idx) => {
    const x = 14 + idx * 82;
    return `<rect x="${x}" y="184" width="76" height="20" rx="5" fill="${T.badgeBg}" stroke="${T.panelBorder}" stroke-width="0.8"/>`
      + `<text x="${x + 38}" y="198" text-anchor="middle" fill="${T.cyan}" font-size="10" font-weight="600" class="font-mono">${escapeXml(t)}</text>`;
  }).join("");

  const body = `
  <rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="14" fill="${T.panel}" stroke="${T.panelBorder}" stroke-width="1.2"/>
  <clipPath id="tc${i}"><rect x="10" y="10" width="${W - 20}" height="90" rx="8"/></clipPath>
  <image x="10" y="10" width="${W - 20}" height="90" preserveAspectRatio="xMidYMid slice" href="${cardImg}" clip-path="url(#tc${i})"/>
  <rect x="10" y="10" width="${W - 20}" height="90" rx="8" fill="none" stroke="${T.cyan}" stroke-width="1" opacity=".4"/>
  <text x="14" y="126" fill="${T.gold}" font-size="10.5" font-weight="700" class="font-mono">0${i + 1} · PROJECT</text>
  <text x="14" y="148" fill="${T.textPrimary}" font-size="15" font-weight="700" class="font-sans">${escapeXml(title)}</text>
  <text x="14" y="168" fill="${T.textMuted}" font-size="11" class="font-sans">${escapeXml(desc.slice(0, 40))}</text>
  ${chipSvgs}
  `;
  return root(W, H, T, body);
}

function projectsGrid(T: ThemeColors, content: Content, cardImg: string): string {
  const W = 1200, H = 480;
  const cards = content.projects.slice(0, 4).map((p, i) => {
    const x = 70 + i * 270;
    const y = 100;
    const chipSvgs = p.tags.slice(0, 2).map((t, idx) => {
      const cx = x + 16 + idx * 72;
      return `<rect x="${cx}" y="${y + 265}" width="66" height="20" rx="5" fill="${T.badgeBg}"/>`
        + `<text x="${cx + 33}" y="${y + 279}" text-anchor="middle" fill="${T.cyan}" font-size="9.5" font-weight="600" class="font-mono">${escapeXml(t)}</text>`;
    }).join("");

    return `
    <rect x="${x}" y="${y}" width="250" height="320" rx="14" fill="${T.panel}" stroke="${T.panelBorder}" stroke-width="1.2"/>
    <clipPath id="pgc${i}"><rect x="${x + 10}" y="${y + 10}" width="230" height="130" rx="8"/></clipPath>
    <image x="${x + 10}" y="${y + 10}" width="230" height="130" preserveAspectRatio="xMidYMid slice" href="${cardImg}" clip-path="url(#pgc${i})"/>
    <rect x="${x + 10}" y="${y + 10}" width="230" height="130" rx="8" fill="none" stroke="${T.cyan}" stroke-width="0.8" opacity=".4"/>
    <text x="${x + 16}" y="${y + 172}" fill="${T.gold}" font-size="10.5" font-weight="700" class="font-mono">0${i + 1} · SELECTED CODEBASE</text>
    <text x="${x + 16}" y="${y + 198}" fill="${T.textPrimary}" font-size="16" font-weight="700" class="font-sans">${escapeXml(p.title)}</text>
    <text x="${x + 16}" y="${y + 224}" fill="${T.textMuted}" font-size="11.5" class="font-sans">${escapeXml(p.line1)}</text>
    <text x="${x + 16}" y="${y + 242}" fill="${T.textMuted}" font-size="11.5" class="font-sans">${escapeXml(p.line2)}</text>
    ${chipSvgs}
    `;
  }).join("\n");

  const body = `
  <g transform="translate(70, 40)">
    <text x="0" y="24" fill="${T.gold}" font-size="13" font-weight="700" letter-spacing="2" class="font-mono">CURATED WORKS</text>
    <text x="0" y="52" fill="${T.textPrimary}" font-size="24" font-weight="700" class="font-serif">Selected Projects &amp; Architectures</text>
  </g>
  ${cards}
  `;
  return root(W, H, T, body);
}

function footer(T: ThemeColors, content: Content): string {
  const W = 1200, H = 230;
  const brand = content.brand?.latin || "solaymantech.me";
  const body = `
  <path d="M 100 60 Q 600 20 1100 60" fill="none" stroke="${T.cyan}" stroke-width="1" opacity=".3" class="contour-drift-0"/>
  <path d="M 100 80 Q 600 40 1100 80" fill="none" stroke="${T.gold}" stroke-width="0.8" opacity=".3" class="contour-drift-1"/>

  <g transform="translate(600, 110)">
    <text x="0" y="0" text-anchor="middle" fill="${T.textPrimary}" font-size="26" font-weight="700" letter-spacing="3" class="font-serif">${escapeXml(content.footer.line1)}</text>
    <text x="0" y="32" text-anchor="middle" fill="${T.cyan}" font-size="13" font-weight="600" letter-spacing="1.5" class="font-mono">${escapeXml(content.footer.line2)}</text>
    <text x="0" y="60" text-anchor="middle" fill="${T.gold}" font-size="12" class="font-mono">${escapeXml(brand)}</text>
  </g>
  `;
  return root(W, H, T, body);
}

function button(T: ThemeColors, text: string): string {
  const W = 160, H = 38;
  const body = `
  <rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="8" fill="${T.panel}" stroke="${T.panelBorder}" stroke-width="1.2"/>
  <circle cx="18" cy="${H / 2}" r="3" fill="${T.teal}" class="pulse-glow"/>
  <text x="${W / 2 + 6}" y="${H / 2 + 4}" text-anchor="middle" fill="${T.textPrimary}" font-size="12" font-weight="600" class="font-sans">${escapeXml(text)}</text>
  `;
  return root(W, H, T, body);
}

export const treeStyle: StyleModule = {
  id: "tree",
  name: "Topographic Tree Contours",
  keywords: ["tree", "topographic", "contours", "rings", "nature", "algorithmic"],
  palette: {
    dark: ["#09111c", "#0e1a2b", "#56cfe1", "#72efdd", "#e0a96d"],
    light: ["#f5f8fc", "#ebf2fa", "#1a6f87", "#1d877a", "#9e6831"],
  },
  motion: "lively",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/tree/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 510, 520], [510, 520], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [20, 20, 250, 150],
      [80, 100, 310, 230],
      [140, 180, 370, 310],
      [200, 260, 430, 390],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [230, 130], 0.85)
    );

    const files: Record<string, string> = {};

    for (const theme of ["dark", "light"] as const) {
      const T = THEMES[theme];
      const headerSvg = header(T, content, heroCrop);
      files[`hero-${theme}.svg`] = headerSvg;
      files[`header-${theme}.svg`] = headerSvg;
      files[`divider-${theme}.svg`] = divider(T);
      files[`btn-github-${theme}.svg`] = button(T, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(T, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(T, "Portfolio");
      files[`about-${theme}.svg`] = about(T, content);
      files[`skills-${theme}.svg`] = skills(T, content);
      files[`projects-grid-${theme}.svg`] = projectsGrid(T, content, heroCrop);
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
      pic("header", `${content.name} — ${content.role}`, "100%"),
      `<a href="${content.github}">${pic("btn-github", "GitHub profile", "150")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn profile", "150")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio website", "150")}</a>`,
      pic("divider", "Contour Divider", "100%"),
      pic("about", "Architectural Pillars and Foundations", "100%"),
      pic("skills", "Annular Growth Rings and Technical Stack", "100%"),
      pic("divider", "Contour Divider", "100%"),
      pic("projects-grid", "Selected Projects and Architectures", "100%"),
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
export default treeStyle;
