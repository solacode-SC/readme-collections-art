import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  ink: string;
  soft: string;
  accent: string;
  line: string;
  twig: string;
  twigop: string;
  disc: string;
  disctxt: string;
  btn: string;
  btntxt: string;
  band: string;
  dots: string[];
  blob_op: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0C1810",
    bg2: "#18351F",
    panel: "#183323",
    ink: "#EAF1D2",
    soft: "#B9CBA6",
    accent: "#C9E66B",
    line: "#8DB33A",
    twig: "#6F9A78",
    twigop: ".55",
    disc: "#EAF1D2",
    disctxt: "#12261A",
    btn: "#B7D957",
    btntxt: "#10200F",
    band: "#08110B",
    dots: ["#8DB33A", "#A9D04B", "#5E9B6B", "#C9E66B", "#6FA89A"],
    blob_op: ".55",
  },
  light: {
    bg: "#F4F6E0",
    bg2: "#DCE8BE",
    panel: "#FBFCEB",
    ink: "#1B2D19",
    soft: "#47603F",
    accent: "#3C6A1B",
    line: "#6E9A2C",
    twig: "#3B2D20",
    twigop: ".45",
    disc: "#FBFCEB",
    disctxt: "#1B2D19",
    btn: "#3C6A1B",
    btntxt: "#F6F8E6",
    band: "#1B2D19",
    dots: ["#6E9A2C", "#8DB33A", "#4E8A5E", "#A9C84A", "#5E9AA0"],
    blob_op: ".7",
  },
};

const CSS = `
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.kb{transform-box:fill-box;transform-origin:50% 40%;animation-name:kb;animation-duration:40s}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:160s;animation-timing-function:linear;animation-direction:normal}
.sway{transform-box:fill-box;transform-origin:center;animation-name:sway;animation-duration:18s}
.bob{animation-name:bob;animation-duration:9s}
.flow{animation-name:flow;animation-duration:9s;animation-timing-function:linear;animation-direction:normal}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.05)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes sway{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-8px)}}
@keyframes flow{to{stroke-dashoffset:-64}}
@media (prefers-reduced-motion: reduce){.a{animation:none}}
`;

function svgDoc(W: number, H: number, body: string, title: string, desc: string, defs = "", animated = true): string {
  const style = animated ? `<style>${CSS}</style>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${escapeXml(title)}">
<title>${escapeXml(title)}</title><desc>${escapeXml(desc)}</desc><defs>${defs}</defs>${style}${body}</svg>`;
}

function wave(x0: number, x1: number, y: number, amp: number, wl: number, ph = 0.0, step = 6): string {
  const pts: string[] = [];
  let x = x0;
  while (x <= x1) {
    pts.push(`${f1(x)},${f1(y + amp * Math.sin(((x - x0) / wl) * 2 * Math.PI + ph))}`);
    x += step;
  }
  return "M" + pts.join(" L");
}

function blobPath(cx: number, cy: number, rx: number, ry: number, seed: number, n = 9, jit = 0.1): string {
  const rng = createRng(seed);
  const pts: [number, number][] = [];
  for (let i = 0; i < n; i++) {
    const a = (i * 2 * Math.PI) / n;
    const k = 1 + (rng() * 2 * jit - jit);
    pts.push([cx + rx * k * Math.cos(a), cy + ry * k * Math.sin(a)]);
  }
  let d = `M${f1(pts[0][0])},${f1(pts[0][1])}`;
  for (let i = 0; i < n; i++) {
    const p0 = pts[(i - 1 + n) % n];
    const p1 = pts[i];
    const p2 = pts[(i + 1) % n];
    const p3 = pts[(i + 2) % n];
    const c1: [number, number] = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2: [number, number] = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${f1(c1[0])},${f1(c1[1])} ${f1(c2[0])},${f1(c2[1])} ${f1(p2[0])},${f1(p2[1])}`;
  }
  return d + " Z";
}

function spiralD(R: number, turns: number, step = 0.25): string {
  const pts: string[] = [];
  let th = 0.0;
  const tmax = turns * 2 * Math.PI;
  while (th <= tmax) {
    const r = (R * th) / tmax;
    pts.push(`${f1(r * Math.cos(th))},${f1(r * Math.sin(th))}`);
    th += step;
  }
  return "M" + pts.join(" L");
}

function spiral(cx: number, cy: number, R: number, turns: number, color: string, w = 2, op = 1.0, rot = 0, spin = false, delay = 0): string {
  const guard = `<circle r="${R}" fill="none" stroke="none"/>`;
  const path = `<path d="${spiralD(R, turns)}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" opacity="${op}"/>`;
  let inner = guard + path;
  if (spin) {
    inner = `<g class="spin a" style="animation-delay:-${delay}s">${inner}</g>`;
  }
  return `<g transform="translate(${cx},${cy}) rotate(${rot})">${inner}</g>`;
}

function phyllotaxis(cx: number, cy: number, n: number, spread: number, c: ThemeColors, spinDelay?: number): string {
  const out = [`<circle r="${f1(spread * Math.sqrt(n) + 4)}" fill="none" stroke="none"/>`];
  for (let i = 1; i <= n; i++) {
    const th = i * 2.399963;
    const rr = spread * Math.sqrt(i);
    out.push(`<circle cx="${f1(rr * Math.cos(th))}" cy="${f1(rr * Math.sin(th))}" r="${f1(1.2 + (2.0 * i) / n)}" fill="${c.dots[i % 5]}"/>`);
  }
  let g = out.join("");
  if (spinDelay !== undefined) {
    g = `<g class="spin a" style="animation-delay:-${spinDelay}s;animation-duration:90s">${g}</g>`;
  }
  return `<g transform="translate(${f1(cx)},${f1(cy)})">${g}</g>`;
}

function twig(c: ThemeColors, x: number, y: number, ang: number, L: number, seed: number, depth = 5, w = 3.2): string {
  const rng = createRng(seed);
  const segs: string[] = [];

  function grow(gx: number, gy: number, a: number, len: number, d: number, width: number) {
    const a2 = a + (rng() * 0.7 - 0.35);
    const x2 = gx + len * Math.cos(a2);
    const y2 = gy + len * Math.sin(a2);
    const mx = (gx + x2) / 2 + (rng() * 2 * len - len) * 0.15;
    const my = (gy + y2) / 2 + (rng() * 2 * len - len) * 0.15;
    segs.push(`<path d="M${f1(gx)},${f1(gy)} Q${f1(mx)},${f1(my)} ${f1(x2)},${f1(y2)}" stroke-width="${f1(Math.max(width, 0.8))}"/>`);
    if (d > 0) {
      grow(x2, y2, a2 + (0.25 + rng() * 0.35), len * 0.76, d - 1, width * 0.66);
      if (rng() < 0.8) {
        grow(x2, y2, a2 - (0.3 + rng() * 0.4), len * 0.7, d - 1, width * 0.6);
      }
    }
  }

  grow(x, y, ang, L, depth, w);
  return `<g fill="none" stroke="${c.twig}" stroke-linecap="round" opacity="${c.twigop}">${segs.join("")}</g>`;
}

function base(c: ThemeColors, W: number, H: number, sid = "s"): { defs: string; bg: string } {
  const defs = `<linearGradient id="${sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  return { defs, bg: `<rect width="${W}" height="${H}" fill="url(#${sid}g)"/>` };
}

function heading(x: number, y: number, text: string, c: ThemeColors, size = 28): string {
  return `${spiral(x + 12, y - 9, 11, 2.2, c.accent, 2.2)}
<text x="${x + 34}" y="${y}" font-family="${SERIF}" font-size="${size}" font-style="italic" letter-spacing=".8" fill="${c.ink}">${escapeXml(text)}</text>`;
}

function scatterSpirals(c: ThemeColors, W: number, H: number, seed: number, n: number, rmin: number, rmax: number, op: [number, number], avoid?: [number, number, number, number], spinN = 3): string {
  const rng = createRng(seed);
  const out: string[] = [];
  for (let i = 0; i < n; i++) {
    let sx = rng() * W;
    let sy = rng() * H;
    let sR = rmin + rng() * (rmax - rmin);
    if (avoid && sx > avoid[0] && sx < avoid[2] && sy > avoid[1] && sy < avoid[3]) {
      sx = (sx + 300) % W;
    }
    const turns = [2.5, 3, 3.5][Math.floor(rng() * 3)];
    const sw = [1.4, 2, 2.6][Math.floor(rng() * 3)];
    const sop = op[0] + rng() * (op[1] - op[0]);
    out.push(spiral(Math.round(sx), Math.round(sy), Math.round(sR), turns, c.line, sw, Number(f1(sop)), Math.floor(rng() * 360), i < spinN, Math.floor(rng() * 80)));
  }
  return out.join("");
}

function hero(c: ThemeColors, content: Content, heroImg: string, avatarImg: string, peb1: string, peb2: string): string {
  const W = 900, H = 580;
  const { defs: bDefs, bg } = base(c, W, H, "h");
  const bx = 670, by = 292, brx = 182, bry = 262;
  const blob = blobPath(bx, by, brx, bry, 12, 9, 0.07);

  const defs = bDefs + `
<clipPath id="hclip"><path d="${blob}"/></clipPath>
<clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>
<clipPath id="hf1"><circle cx="455" cy="500" r="32"/></clipPath>
<clipPath id="hf2"><circle cx="868" cy="62" r="26"/></clipPath>`;

  const s: string[] = [
    bg,
    scatterSpirals(c, 500, H, 3, 7, 40, 120, [0.1, 0.22], [40, 90, 480, 470], 2),
    twig(c, 0, 590, -1.2, 78, 5, 5, 4.2),
    twig(c, 520, -10, 1.5, 60, 8, 4, 3),
    `<image href="${avatarImg}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>`,
    `<circle cx="64" cy="34" r="14" fill="none" stroke="${c.accent}" stroke-width="1.6"/>`,
    `<text x="86" y="39" font-family="${MONO}" font-size="12.5" fill="${c.soft}">${escapeXml(content.handle)} / README</text>`,
    `<path d="${wave(50, 400, 64, 3, 70)}" fill="none" stroke="${c.line}" stroke-width="1.4" opacity=".8"/>`,
    `<text x="52" y="132" font-family="${SERIF}" font-size="20" font-style="italic" fill="${c.soft}">hi, i'm</text>`,
    spiral(122, 126, 9, 2, c.accent, 2),
  ];

  const nameParts = content.name.split(" ");
  const name1 = nameParts[0] || content.name;
  const name2 = nameParts.slice(1).join(" ");

  s.push(`<text x="50" y="202" font-family="${SERIF}" font-size="60" font-style="italic" fill="${c.ink}">${escapeXml(name1)}</text>`);
  s.push(`<text x="96" y="268" font-family="${SERIF}" font-size="60" font-style="italic" fill="${c.ink}">${escapeXml(name2)}</text>`);
  s.push(`<text x="98" y="322" font-family="${SANS}" font-size="14" font-weight="700" letter-spacing="4" fill="${c.accent}">${escapeXml(content.role.toUpperCase())}</text>`);
  s.push(`<text x="98" y="354" font-family="${SERIF}" font-size="17.5" font-style="italic" fill="${c.ink}">${escapeXml(content.pillars)}</text>`);

  content.tagline.forEach((line, i) => {
    s.push(`<text x="${60 + i * 10}" y="${408 + i * 23}" font-family="${SERIF}" font-size="15.5" fill="${c.soft}">${escapeXml(line)}</text>`);
  });

  s.push(`<path class="sway a" d="${blobPath(bx, by, brx + 14, bry + 14, 12, 9, 0.07)}" fill="none" stroke="${c.accent}" stroke-width="1.2" opacity=".7"/>`);
  s.push(`<path class="sway a" style="animation-direction:alternate-reverse;animation-duration:24s" d="${blobPath(bx, by, brx + 28, bry + 26, 12, 9, 0.07)}" fill="none" stroke="${c.line}" stroke-width=".9" opacity=".5"/>`);
  s.push(`<g clip-path="url(#hclip)"><image class="kb a" href="${heroImg}" x="${bx - 185}" y="${by - 267}" width="370" height="534" preserveAspectRatio="xMidYMid slice"/></g>`);

  s.push(
    `<g class="bob a"><g clip-path="url(#hf1)"><image href="${peb1}" x="423" y="468" width="64" height="64"/></g><circle cx="455" cy="500" r="32" fill="none" stroke="${c.accent}" stroke-width="1.4"/></g>`
  );
  s.push(
    `<g class="bob a" style="animation-delay:-4s"><g clip-path="url(#hf2)"><image href="${peb2}" x="842" y="36" width="52" height="52"/></g><circle cx="868" cy="62" r="26" fill="none" stroke="${c.accent}" stroke-width="1.4"/></g>`
  );

  return svgDoc(W, H, s.join(""), `${content.name}: ${content.role}`, "Profile header with organic window showing tree canopy.", defs);
}

function button(c: ThemeColors, label: string): string {
  const body = `<path d="M5,20 C30,2 120,2 145,20 C120,38 30,38 5,20 Z" fill="${c.btn}"/>
${spiral(32, 20, 7, 2, c.btntxt, 1.8)}
<text x="88" y="25" text-anchor="middle" font-family="${SERIF}" font-size="15" font-style="italic" letter-spacing=".6" fill="${c.btntxt}">${escapeXml(label)}</text>`;
  return svgDoc(150, 40, body, label, `Button linking to ${label}`, "", false);
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 392;
  const { defs, bg } = base(c, W, H, "a");
  const s: string[] = [
    bg,
    `<path d="${blobPath(450, 196, 430, 172, 4, 10, 0.06)}" fill="${c.panel}" opacity="${c.blob_op}"/>`,
    spiral(770, 210, 150, 3.5, c.line, 2, 0.22, 0, true),
    twig(c, 900, 400, -2.6, 70, 11, 4, 3),
    heading(60, 78, "about", c),
    heading(520, 78, "my journey", c),
  ];

  const g: string[] = [];
  content.about.forEach((line, i) => {
    g.push(`<text x="60" y="${122 + i * 24}" font-family="${SERIF}" font-size="14.5" fill="${c.ink}">${escapeXml(line)}</text>`);
  });

  const factY = 122 + 24 * content.about.length + 24;
  g.push(`<text x="60" y="${factY}" font-family="${SANS}" font-size="12" fill="${c.soft}">Software engineering · Mathematics &amp; Physics · Based in Morocco</text>`);
  g.push(`<text x="60" y="${factY + 18}" font-family="${SANS}" font-size="12.5" font-weight="700" fill="${c.accent}">Focus: Systems, Web, Intelligence &amp; Mathematics</text>`);
  s.push(`<g transform="rotate(-.8 60 122)">${g.join("")}</g>`);

  content.journey.forEach((item, i) => {
    const yy = 134 + i * 44;
    const lx = 520 + Math.round(9 * Math.sin(i * 1.4));
    const x1 = lx + item.lang.length * 10.4 + 14;
    const x2 = 850 - item.area.length * 7.6 - 30;
    s.push(`<text x="${lx}" y="${yy}" font-family="${SERIF}" font-size="18" font-style="italic" fill="${c.ink}">${escapeXml(item.lang)}</text>`);
    s.push(`<path class="flow a" d="${wave(Math.round(x1), Math.round(x2), yy - 5, 3, 50, i)}" fill="none" stroke="${c.line}" stroke-width="3" stroke-linecap="round" stroke-dasharray="0 8"/>`);
    s.push(`<text x="850" y="${yy}" text-anchor="end" font-family="${SANS}" font-size="13.5" font-weight="700" fill="${c.accent}">${escapeXml(item.area)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "About and journey", "About and journey section", defs);
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 360;
  const { defs, bg } = base(c, W, H, "k");
  const s: string[] = [
    bg,
    `<path d="${blobPath(450, 190, 430, 160, 9, 10, 0.06)}" fill="${c.panel}" opacity="${c.blob_op}"/>`,
    scatterSpirals(c, W, H, 6, 5, 50, 110, [0.08, 0.16], undefined, 1),
    heading(60, 78, "technologies & skills", c),
  ];

  const cell = 800 / 6;
  content.skills.slice(0, 12).forEach((item, i) => {
    const row = Math.floor(i / 6);
    const col = i % 6;
    const cx = 50 + cell * (col + 0.5) + row * 22;
    const cy = 160 + row * 116 + Math.round(9 * Math.sin(col * 1.7 + row));
    s.push(phyllotaxis(cx, cy, 60, 4.6, c, i * 11));
    s.push(`<circle cx="${f1(cx)}" cy="${cy}" r="17" fill="${c.disc}"/>`);
    s.push(`<text x="${f1(cx)}" y="${f1(cy + 4.5)}" text-anchor="middle" font-family="${MONO}" font-size="12.5" font-weight="700" fill="${c.disctxt}">${escapeXml(item.mono)}</text>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 58}" text-anchor="middle" font-family="${SANS}" font-size="12" font-weight="700" fill="${c.ink}">${escapeXml(item.label)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "Technologies and skills", "Twelve seed-like spirals", defs);
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 92;
  const { defs, bg } = base(c, W, H, "p");
  const s = [
    bg,
    heading(60, 56, "selected projects", c, 30),
    `<path d="${wave(360, 800, 48, 7, 120)}" fill="none" stroke="${c.line}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0 8" class="flow a"/>`,
    spiral(830, 48, 16, 2.6, c.accent, 2.2),
  ];
  return svgDoc(W, H, s.join(""), "Selected projects", "Section heading", defs);
}

function card(c: ThemeColors, idx: number, title: string, desc: string, tags: string[], img: string): string {
  const W = 208, H = 280;
  const defs = `<clipPath id="cblob${idx}"><path d="${blobPath(104, 82, 86, 68, idx * 7, 8, 0.08)}"/></clipPath>`;

  const g = [
    `<rect x="6" y="6" width="196" height="268" rx="14" fill="${c.panel}" stroke="${c.line}" stroke-width="1.6" opacity="${c.blob_op}"/>`,
    `<g clip-path="url(#cblob${idx})"><image href="${img}" x="18" y="14" width="172" height="136" preserveAspectRatio="xMidYMid slice"/></g>`,
    `<path d="${blobPath(104, 82, 86, 68, idx * 7, 8, 0.08)}" fill="none" stroke="${c.accent}" stroke-width="1.4"/>`,
    spiral(104, 156, 10, 2, c.accent, 1.8),
    `<text x="104" y="186" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-weight="700" font-size="18" fill="${c.ink}">${escapeXml(title)}</text>`,
    `<text x="104" y="206" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(0, 32))}</text>`,
  ];

  if (desc.length > 32) {
    g.push(`<text x="104" y="220" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(32, 64))}</text>`);
  }

  g.push(`<text x="104" y="244" text-anchor="middle" font-family="${SANS}" font-size="10" font-weight="700" fill="${c.accent}">${escapeXml(tags.slice(0, 3).join(" · "))}</text>`);

  return svgDoc(W, H, g.join(""), `Project ${title}`, `${title}: ${desc}`, defs);
}

function footer(c: ThemeColors, content: Content, heroImg: string): string {
  const W = 900, H = 280;
  const { defs, bg } = base(c, W, H, "f");
  const s = [
    bg,
    `<path d="${blobPath(450, 130, 420, 110, 8, 10, 0.05)}" fill="${c.panel}" opacity="${c.blob_op}"/>`,
    spiral(450, 110, 80, 3, c.line, 1.4, 0.3, 0, true),
    `<text x="450" y="104" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="34" fill="${c.ink}">${escapeXml(content.footer.line1)}</text>`,
    `<text x="450" y="146" text-anchor="middle" font-family="${SANS}" font-size="13" letter-spacing="1.5" fill="${c.soft}">${escapeXml(content.footer.line2)}</text>`,
    twig(c, 40, 230, 0.4, 60, 4, 3, 2.2),
    twig(c, 860, 230, 2.7, 60, 9, 3, 2.2),
    `<rect x="0" y="${H - 32}" width="${W}" height="32" fill="${c.band}"/>`,
    `<text x="30" y="${H - 12}" font-family="${SANS}" font-size="10.5" fill="#EAF1D2">Artwork: forest canopy spiral</text>`,
    `<text x="870" y="${H - 12}" text-anchor="end" font-family="${SANS}" font-size="11.5" font-weight="700" fill="${c.accent}">NashirTech · ناشر تك</text>`,
  ];

  return svgDoc(W, H, s.join(""), "Footer", `${content.footer.line1}. ${content.footer.line2}`, defs);
}

export const canopyStyle: StyleModule = {
  id: "canopy",
  name: "Canopy Spiral",
  keywords: ["forest", "emerald", "organic", "spiral", "nature"],
  palette: {
    dark: ["#0C1810", "#18351F", "#C9E66B", "#EAF1D2", "#8DB33A"],
    light: ["#F4F6E0", "#DCE8BE", "#3C6A1B", "#1B2D19", "#6E9A2C"],
  },
  motion: "lively",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/canopy/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 120, 736, 1174], [370, 534], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [150, 100, 290, 240], [64, 64], 0.9);
    const peb1 = ctx.cropToDataUrl(img, [180, 140, 340, 300], [64, 64], 0.85);
    const peb2 = ctx.cropToDataUrl(img, [400, 380, 560, 540], [52, 52], 0.85);

    const cropBoxes: [number, number, number, number][] = [
      [0, 120, 260, 380],
      [180, 320, 440, 580],
      [400, 500, 660, 760],
      [476, 120, 736, 380],
      [0, 600, 260, 860],
      [200, 780, 460, 1040],
      [476, 800, 736, 1060],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [220, 220], 0.85)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop, avatarCrop, peb1, peb2);
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
      pic("hero", `${content.name}, ${content.role}. Organic window with spiraling tree canopy leaves.`, "100%"),
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
