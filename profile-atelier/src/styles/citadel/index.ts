import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";

interface ThemeColors {
  bg: string;
  sky2: string;
  panel: string;
  panel2: string;
  ink: string;
  soft: string;
  accent: string;
  sun: string;
  coral: string;
  pink: string;
  crimson: string;
  lav: string;
  olive: string;
  shadow: string;
  fshadow: string;
  rim: string;
  line: string;
  wave: string;
  dot: string;
  city: string;
  roofA: string;
  roofB: string;
  band: string;
  star: string;
  cloudfill: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#1E1028",
    sky2: "#4A1F45",
    panel: "#2B1738",
    panel2: "#3B2150",
    ink: "#FCE9C9",
    soft: "#DCC3D2",
    accent: "#F7C95A",
    sun: "#F7C95A",
    coral: "#F0735F",
    pink: "#F4A3BC",
    crimson: "#CF2F3C",
    lav: "#AFA6EC",
    olive: "#9DB05A",
    shadow: "#0E0614",
    fshadow: "#F0735F",
    rim: "#F7C95A",
    line: "#FCE9C9",
    wave: "#F7C95A",
    dot: "#FCE9C9",
    city: "#3A2147",
    roofA: "#8A9A4B",
    roofB: "#E4414B",
    band: "#12091A",
    star: "#FFF3C4",
    cloudfill: "#F4A3BC",
  },
  light: {
    bg: "#FFF1D0",
    sky2: "#FFD3A0",
    panel: "#FFF9E8",
    panel2: "#FBE3B5",
    ink: "#34142A",
    soft: "#6A3A55",
    accent: "#B8232F",
    sun: "#F2B13C",
    coral: "#E2603F",
    pink: "#EE8EAA",
    crimson: "#C32835",
    lav: "#8E85D6",
    olive: "#6B7A2C",
    shadow: "#F2A0B8",
    fshadow: "#F2A0B8",
    rim: "#34142A",
    line: "#34142A",
    wave: "#C32835",
    dot: "#34142A",
    city: "#F5D9A0",
    roofA: "#6B7A2C",
    roofB: "#C32835",
    band: "#34142A",
    star: "#C32835",
    cloudfill: "#F4A3BC",
  },
};

const BADGE_INK = "#2A1230";
const BADGE_FILLS = ["#F4A3BC", "#F7C95A", "#AFA6EC", "#B7C77A"];

const CSS = `
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.drift{animation-name:drift;animation-duration:24s}
.bob{transform-box:fill-box;transform-origin:center;animation-name:bob;animation-duration:6s}
.kb{transform-box:fill-box;transform-origin:50% 38%;animation-name:kb;animation-duration:26s}
.glint{transform-box:fill-box;transform-origin:center;animation-name:glint;animation-duration:3.6s}
.pulse{transform-box:fill-box;transform-origin:center;animation-name:pulse;animation-duration:6s}
.flow{animation-name:flow;animation-duration:3s;animation-timing-function:linear;animation-direction:normal}
@keyframes drift{from{transform:translateX(-14px)}to{transform:translateX(26px)}}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-4px)}}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
@keyframes glint{0%{opacity:.25;transform:scale(.5)}60%{opacity:1;transform:scale(1.1)}100%{opacity:.35;transform:scale(.6)}}
@keyframes pulse{from{opacity:.8;transform:scale(1)}to{opacity:1;transform:scale(1.05)}}
@keyframes flow{to{stroke-dashoffset:-48}}
@media (prefers-reduced-motion: reduce){.a{animation:none}}
`;

function svgDoc(W: number, H: number, body: string, title: string, desc: string, defs = "", animated = true): string {
  const style = animated ? `<style>${CSS}</style>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${escapeXml(title)}">
<title>${escapeXml(title)}</title><desc>${escapeXml(desc)}</desc><defs>${defs}</defs>${style}${body}</svg>`;
}

function wave(x0: number, x1: number, y: number, amp: number, wl: number, ph = 0.0, step = 8): string {
  const pts: string[] = [];
  let x = x0;
  while (x <= x1) {
    pts.push(`${f1(x)},${f1(y + amp * Math.sin(((x - x0) / wl) * 2 * Math.PI + ph))}`);
    x += step;
  }
  return "M" + pts.join(" L");
}

function vwave(x: number, y0: number, y1: number, amp: number, wl: number, step = 8): string {
  const pts: string[] = [];
  let y = y0;
  while (y <= y1) {
    pts.push(`${f1(x + amp * Math.sin(((y - y0) / wl) * 2 * Math.PI))},${f1(y)}`);
    y += step;
  }
  return "M" + pts.join(" L");
}

function cloud(cx: number, cy: number, w: number, fill: string, rim: string, rimw = 4, seed = 0, cls = "", style = ""): string {
  const rng = createRng(seed);
  const n = Math.max(4, Math.floor(w / 32));
  const cs: [number, number, number][] = [];
  for (let i = 0; i < n; i++) {
    const t = (i + 0.5) / n;
    const rad = w * (0.10 + 0.07 * Math.sin(Math.PI * t)) * (0.85 + 0.3 * rng());
    cs.push([cx - w / 2 + t * w, cy - Math.sin(Math.PI * t) * w * 0.05 - rad * 0.3, rad]);
  }
  if (w > 100) {
    for (let i = 0; i < Math.max(2, Math.floor(n / 2)); i++) {
      const t = (i + 0.8) / (Math.floor(n / 2) + 0.6);
      const rad = w * 0.11 * (0.85 + 0.3 * rng());
      cs.push([cx - w / 2 + t * w * 0.9 + w * 0.05, cy - w * 0.13, rad]);
    }
  }

  const rims = cs.map(([x, y, rad]) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rad + rimw)}"/>`).join("");
  const fills = cs.map(([x, y, rad]) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(rad)}"/>`).join("");
  const inner = `<g fill="${rim}">${rims}</g><g fill="${fill}">${fills}</g>`;
  if (cls) {
    return `<g><g class="${cls}" style="${style}">${inner}</g></g>`;
  }
  return `<g>${inner}</g>`;
}

function star(x: number, y: number, s = 1.0, fill = "#FFF3C4", cls = "glint a", style = ""): string {
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})"><path class="${cls}" style="${style}" fill="${fill}" d="M0,-12 L2.4,-2.4 L12,0 L2.4,2.4 L0,12 L-2.4,2.4 L-12,0 L-2.4,-2.4Z"/></g>`;
}

function sunGlyph(cx: number, cy: number, r: number, c: ThemeColors): string {
  let rays = "";
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI) / 4;
    rays += `<line x1="${f1(cx + (r + 3) * Math.cos(a))}" y1="${f1(cy + (r + 3) * Math.sin(a))}" x2="${f1(cx + (r + 7) * Math.cos(a))}" y2="${f1(cy + (r + 7) * Math.sin(a))}"/>`;
  }
  return `<g stroke="${c.ink}" stroke-width="1.6" stroke-linecap="round">${rays}</g>
<circle cx="${cx}" cy="${cy}" r="${r}" fill="${c.sun}" stroke="${c.ink}" stroke-width="1.8"/>
<circle cx="${cx}" cy="${cy}" r="${f1(r * 0.5)}" fill="none" stroke="${c.ink}" stroke-width="1"/>`;
}

function heading(x: number, y: number, text: string, c: ThemeColors, size = 24): string {
  return `${sunGlyph(x + 10, y - 8, 7, c)}
<text x="${x + 32}" y="${y}" font-family="${SERIF}" font-size="${size}" font-weight="700" font-style="italic" fill="${c.ink}">${escapeXml(text)}</text>`;
}

function base(c: ThemeColors, W: number, H: number, sid = "s"): { defs: string; body: string } {
  const defs = `<linearGradient id="${sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.sky2}"/></linearGradient>
<pattern id="${sid}d" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="${c.dot}"/></pattern>`;
  const body = `<rect width="${W}" height="${H}" fill="url(#${sid}g)"/>
<rect width="${W}" height="${H}" fill="url(#${sid}d)" opacity=".07"/>`;
  return { defs, body };
}

function contours(c: ThemeColors, W: number, H: number, n: number, y0: number, gap: number, op = 0.3): string {
  const out: string[] = [];
  for (let i = 0; i < n; i++) {
    out.push(
      `<path d="${wave(0, W, y0 + i * gap, 5 + (i % 3) * 3, 140 + ((i * 13) % 70), i * 0.9)}" fill="none" stroke="${c.wave}" stroke-width="1.1" opacity="${op}"/>`
    );
  }
  return out.join("");
}

function panel(c: ThemeColors, x: number, y: number, w: number, h: number, rx = 22): string {
  return `<rect x="${x + 7}" y="${y + 7}" width="${w}" height="${h}" rx="${rx}" fill="${c.shadow}"/>
<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${c.panel}" stroke="${c.ink}" stroke-width="2.4"/>`;
}

function hero(c: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const W = 900, H = 520;
  const { defs: bDefs, body } = base(c, W, H, "h");
  const fx = 510, fy = 40, fw = 370;
  const fh = Math.round((fw * 700) / 598);

  const defs = bDefs + `
<clipPath id="hclip"><rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" rx="5"/></clipPath>
<clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>
<radialGradient id="hglow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="${c.sun}" stop-opacity=".35"/><stop offset="1" stop-color="${c.sun}" stop-opacity="0"/></radialGradient>`;

  const s: string[] = [
    body,
    contours(c, W, H, 15, 30, 31, 0.22),
    `<ellipse cx="${fx + fw / 2}" cy="${fy + fh / 2}" rx="300" ry="290" fill="url(#hglow)"/>`,
    `<image href="${avatarImg}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>`,
    `<circle cx="64" cy="34" r="14" fill="none" stroke="${c.sun}" stroke-width="2"/>`,
    `<text x="86" y="39" font-family="${MONO}" font-size="12.5" fill="${c.soft}">${escapeXml(content.handle)} / README</text>`,
    `<path d="${wave(50, 470, 64, 2.5, 60)}" fill="none" stroke="${c.accent}" stroke-width="1.6" opacity=".8"/>`,
    `<text x="52" y="116" font-family="${SERIF}" font-size="20" font-style="italic" fill="${c.soft}">Hi, I'm</text>`,
  ];

  const nameParts = content.name.split(" ");
  const name1 = nameParts[0] || content.name;
  const name2 = nameParts.slice(1).join(" ");

  for (const [txt, y] of [[name1, 186], [name2, 252]] as [string, number][]) {
    s.push(`<text x="55" y="${y + 3}" font-family="${SERIF}" font-size="64" font-weight="700" font-style="italic" fill="${c.fshadow}">${escapeXml(txt)}</text>`);
    s.push(`<text x="52" y="${y}" font-family="${SERIF}" font-size="64" font-weight="700" font-style="italic" fill="${c.ink}">${escapeXml(txt)}</text>`);
  }

  s.push(`<text x="53" y="310" font-family="${SANS}" font-size="14" font-weight="700" letter-spacing="5" fill="${c.accent}">${escapeXml(content.role.toUpperCase())}</text>`);
  s.push(`<text x="53" y="341" font-family="${SERIF}" font-size="17" font-style="italic" fill="${c.ink}">${escapeXml(content.pillars)}</text>`);

  content.tagline.forEach((line, i) => {
    s.push(`<text x="53" y="${384 + i * 22}" font-family="${SERIF}" font-size="15.5" fill="${c.soft}">${escapeXml(line)}</text>`);
  });

  s.push(`<rect x="${fx + 10}" y="${fy + 10}" width="${fw}" height="${fh}" rx="5" fill="${c.fshadow}"/>`);
  s.push(`<g clip-path="url(#hclip)"><image class="kb a" href="${heroImg}" x="${fx}" y="${fy}" width="${fw}" height="${fh}" preserveAspectRatio="xMidYMid slice"/></g>`);
  s.push(`<rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" rx="5" fill="none" stroke="${c.ink}" stroke-width="3"/>`);
  s.push(star(fx + (283 * fw) / 598, fy + (457 * fw) / 598, 1.1, c.star));

  s.push(cloud(230, 570, 420, c.cloudfill, c.rim, 4, 3, "drift a", "animation-duration:30s;animation-delay:-9s"));
  s.push(cloud(640, 562, 300, c.sun, c.rim, 4, 5, "drift a", "animation-duration:23s;animation-delay:-4s"));
  s.push(cloud(830, 556, 280, c.cloudfill, c.rim, 4, 8, "drift a", "animation-duration:27s;animation-delay:-15s"));

  return svgDoc(W, H, s.join(""), `${content.name}: ${content.role}`, "Profile header with framed dragon illustration above sunset citadel.", defs);
}

function button(c: ThemeColors, label: string): string {
  const body = `<rect x="6" y="6" width="141" height="31" rx="15.5" fill="${c.sun}"/>
<rect x="3" y="3" width="141" height="31" rx="15.5" fill="${c.crimson}" stroke="${c.ink}" stroke-width="2"/>
<circle cx="30" cy="18.5" r="5.5" fill="${c.sun}" stroke="#2A1230" stroke-width="1.4"/>
<text x="86" y="24" text-anchor="middle" font-family="${SERIF}" font-size="15" font-weight="700" font-style="italic" fill="#FFF3DC">${escapeXml(label)}</text>`;
  return svgDoc(150, 40, body, label, `Button linking to ${label}`, "", false);
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 332;
  const { defs, body } = base(c, W, H, "a");
  const s: string[] = [
    body,
    panel(c, 14, 14, 868, 302),
    heading(50, 66, "About", c),
    heading(526, 66, "My journey", c),
  ];

  content.about.forEach((line, i) => {
    s.push(`<text x="52" y="${104 + i * 24}" font-family="${SERIF}" font-size="14.5" fill="${c.ink}">${escapeXml(line)}</text>`);
  });

  const factY = 104 + 24 * content.about.length + 22;
  s.push(`<text x="52" y="${factY}" font-family="${SANS}" font-size="12" fill="${c.soft}">Software engineering · Mathematics &amp; Physics · Based in Morocco</text>`);
  s.push(`<text x="52" y="${factY + 18}" font-family="${SANS}" font-size="12.5" font-weight="700" fill="${c.accent}">Focus: Systems, Web, Intelligence &amp; Mathematics</text>`);

  s.push(`<path d="${vwave(496, 44, 290, 3, 60)}" fill="none" stroke="${c.coral}" stroke-width="1.8" opacity=".8"/>`);

  content.journey.forEach((item, i) => {
    const yy = 118 + i * 44;
    const x1 = 530 + item.lang.length * 10.8 + 12;
    const x2 = 850 - item.area.length * 7.6 - 18;
    s.push(`<text x="530" y="${yy}" font-family="${SERIF}" font-size="18" font-weight="700" fill="${c.ink}">${escapeXml(item.lang)}</text>`);
    s.push(`<line class="flow a" x1="${f1(x1)}" y1="${yy - 5}" x2="${f1(x2)}" y2="${yy - 5}" stroke="${c.coral}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 10"/>`);
    s.push(`<text x="850" y="${yy}" text-anchor="end" font-family="${SANS}" font-size="13.5" font-weight="700" fill="${c.accent}">${escapeXml(item.area)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "About and journey", "About and journey section", defs);
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 332;
  const { defs, body } = base(c, W, H, "k");
  const s: string[] = [body, panel(c, 14, 14, 868, 302), heading(50, 66, "Technologies & Skills", c)];

  const cell = 800 / 6;
  content.skills.slice(0, 12).forEach((item, i) => {
    const cx = 50 + cell * ((i % 6) + 0.5);
    const cy = 130 + Math.floor(i / 6) * 100;
    s.push(
      cloud(cx, cy, 104, BADGE_FILLS[i % 4], c.rim, 3, 20 + i, "bob a", `animation-delay:-${f1((i * 1.3) % 6)}s;animation-duration:${5 + (i % 3)}s`)
    );
    s.push(`<text x="${f1(cx)}" y="${cy - 5}" text-anchor="middle" font-family="${MONO}" font-size="17" font-weight="700" fill="${BADGE_INK}">${escapeXml(item.mono)}</text>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 46}" text-anchor="middle" font-family="${SANS}" font-size="12" font-weight="700" fill="${c.ink}">${escapeXml(item.label)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "Technologies and skills", "Twelve cloud badges", defs);
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 84;
  const { defs, body } = base(c, W, H, "p");
  const s = [
    body,
    heading(50, 52, "Selected projects", c, 28),
    `<path class="flow a" d="${wave(330, 850, 44, 5, 90)}" fill="none" stroke="${c.coral}" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 10"/>`,
    star(866, 44, 0.7, c.star),
  ];
  return svgDoc(W, H, s.join(""), "Selected projects", "Section heading", defs);
}

function card(c: ThemeColors, idx: number, title: string, desc: string, tags: string[], img: string): string {
  const W = 208, H = 264;
  const defs = `<clipPath id="cimg${idx}"><rect x="14" y="24" width="180" height="130" rx="4"/></clipPath>`;

  const g = [
    `<rect x="11" y="11" width="186" height="242" rx="4" fill="${c.shadow}"/>`,
    `<rect x="6" y="6" width="186" height="242" rx="4" fill="${c.panel}" stroke="${c.ink}" stroke-width="2.2"/>`,
    `<g clip-path="url(#cimg${idx})"><image href="${img}" x="14" y="24" width="180" height="130" preserveAspectRatio="xMidYMid slice"/></g>`,
    `<rect x="14" y="24" width="180" height="130" rx="4" fill="none" stroke="${c.ink}" stroke-width="1.6"/>`,
    `<text x="104" y="180" text-anchor="middle" font-family="${SERIF}" font-weight="700" font-size="17" fill="${c.ink}">${escapeXml(title)}</text>`,
    `<text x="104" y="200" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(0, 32))}</text>`,
  ];

  if (desc.length > 32) {
    g.push(`<text x="104" y="214" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(32, 64))}</text>`);
  }

  g.push(`<text x="104" y="238" text-anchor="middle" font-family="${SANS}" font-size="10" font-weight="700" fill="${c.coral}">${escapeXml(tags.slice(0, 3).join(" · "))}</text>`);

  return svgDoc(W, H, g.join(""), `Project ${title}`, `${title}: ${desc}`, defs);
}

function footer(c: ThemeColors, content: Content, heroImg: string): string {
  const W = 900, H = 280;
  const { defs, body } = base(c, W, H, "f");
  const s = [
    body,
    panel(c, 16, 16, 868, 216),
    sunGlyph(450, 60, 16, c),
    `<text x="450" y="118" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="34" fill="${c.ink}">${escapeXml(content.footer.line1)}</text>`,
    `<text x="450" y="156" text-anchor="middle" font-family="${SANS}" font-size="13" letter-spacing="1.5" fill="${c.soft}">${escapeXml(content.footer.line2)}</text>`,
    `<rect x="0" y="${H - 32}" width="${W}" height="32" fill="${c.band}"/>`,
    `<text x="30" y="${H - 12}" font-family="${SANS}" font-size="10.5" fill="#FCE9C9">Artwork: terracotta desert citadel</text>`,
    `<text x="870" y="${H - 12}" text-anchor="end" font-family="${SANS}" font-size="11.5" font-weight="700" fill="${c.accent}">NashirTech · ناشر تك</text>`,
  ];

  return svgDoc(W, H, s.join(""), "Footer", `${content.footer.line1}. ${content.footer.line2}`, defs);
}

export const citadelStyle: StyleModule = {
  id: "citadel",
  name: "Desert Citadel",
  keywords: ["citadel", "terracotta", "desert", "dragon", "warm"],
  palette: {
    dark: ["#1E1028", "#4A1F45", "#F7C95A", "#FCE9C9", "#F0735F"],
    light: ["#FFF1D0", "#FFD3A0", "#B8232F", "#34142A", "#E2603F"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/citadel/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 598, 700], [370, 433], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [150, 370, 290, 510], [64, 64], 0.9);

    const cropBoxes: [number, number, number, number][] = [
      [0, 30, 240, 270],
      [160, 120, 400, 360],
      [358, 200, 598, 440],
      [0, 260, 240, 500],
      [180, 380, 420, 620],
      [358, 440, 598, 680],
      [50, 460, 290, 700],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [220, 220], 0.85)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop, avatarCrop);
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c);
      files[`footer-${theme}.svg`] = footer(c, content, heroCrop);

      content.projects.forEach((proj, i) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
          i + 1,
          proj.title,
          proj.line1 + " " + proj.line2,
          proj.tags,
          cardCrops[i]
        );
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items
        .map(
          (p) =>
            `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `${p.title}: ${p.line1} ${p.line2}`, "24%")}</a>`
        )
        .join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name}, ${content.role}. Sunset terracotta citadel under starry cloudscape.`, "100%"),
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
  },
};
