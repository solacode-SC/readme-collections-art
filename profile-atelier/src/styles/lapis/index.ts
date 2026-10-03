import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  panel2: string;
  ink: string;
  soft: string;
  accent: string;
  gold: string;
  blue: string;
  pink: string;
  shadow: string;
  band: string;
  glow: string;
  star: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0B0F2E",
    bg2: "#1B2466",
    panel: "#141B4F",
    panel2: "#1F2A70",
    ink: "#F3EBDD",
    soft: "#C9CDEB",
    accent: "#E8C46A",
    gold: "#E3BE63",
    blue: "#7FA7D6",
    pink: "#E08AA8",
    shadow: "#05071A",
    band: "#070A1F",
    glow: "#8E9BDB",
    star: "#FFF3C4",
  },
  light: {
    bg: "#F5EDDF",
    bg2: "#E2E2F1",
    panel: "#FCF8EE",
    panel2: "#E9E6F4",
    ink: "#161C5A",
    soft: "#4A5088",
    accent: "#7A5A12",
    gold: "#BE9435",
    blue: "#5E88C4",
    pink: "#C8607F",
    shadow: "#C9CDEB",
    band: "#161C5A",
    glow: "#8E9BDB",
    star: "#BE9435",
  },
};

const ROUNDEL: [string, string][] = [
  ["#8E9BDB", "#101648"],
  ["#6BB5C9", "#101648"],
  ["#E08AA8", "#2A0F2E"],
  ["#1F2F8A", "#F3EBDD"],
];

const CSS = `
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.kb{transform-box:fill-box;transform-origin:50% 40%;animation-name:kb;animation-duration:28s}
.glint{transform-box:fill-box;transform-origin:center;animation-name:glint;animation-duration:3.6s}
.sweep{animation-name:sweep;animation-duration:10s;animation-timing-function:ease-in-out;animation-direction:normal}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:70s;animation-timing-function:linear;animation-direction:normal}
.flow{animation-name:flow;animation-duration:3.5s;animation-timing-function:linear;animation-direction:normal}
.pulse{transform-box:fill-box;transform-origin:center;animation-name:pulse;animation-duration:6s}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
@keyframes glint{0%{opacity:.2;transform:scale(.5)}60%{opacity:1;transform:scale(1.1)}100%{opacity:.3;transform:scale(.6)}}
@keyframes sweep{0%{transform:translateX(-160px)}55%,100%{transform:translateX(520px)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flow{to{stroke-dashoffset:-48}}
@keyframes pulse{from{opacity:.75;transform:scale(1)}to{opacity:1;transform:scale(1.04)}}
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

function vwave(x: number, y0: number, y1: number, amp: number, wl: number, step = 6): string {
  const pts: string[] = [];
  let y = y0;
  while (y <= y1) {
    pts.push(`${f1(x + amp * Math.sin(((y - y0) / wl) * 2 * Math.PI))},${f1(y)}`);
    y += step;
  }
  return "M" + pts.join(" L");
}

function rosette(cx: number, cy: number, r: number, c: ThemeColors, petals = 6, fill?: string): string {
  const fCol = fill || c.gold;
  let ps = "";
  for (let i = 0; i < petals; i++) {
    const a = (i * 2 * Math.PI) / petals;
    ps += `<circle cx="${f1(cx + r * 0.56 * Math.cos(a))}" cy="${f1(cy + r * 0.56 * Math.sin(a))}" r="${f1(r * 0.44)}"/>`;
  }
  return `<g fill="${fCol}">${ps}</g><circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * 0.3)}" fill="${c.panel}"/><circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r * 0.14)}" fill="${fCol}"/>`;
}

function diamond(cx: number, cy: number, r: number, fill: string): string {
  return `<path d="M${f1(cx)},${f1(cy - r)} L${f1(cx + r)},${f1(cy)} L${f1(cx)},${f1(cy + r)} L${f1(cx - r)},${f1(cy)} Z" fill="${fill}"/>`;
}

function star(x: number, y: number, s: number, c: ThemeColors, cls = "glint a", style = ""): string {
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(s)})"><path class="${cls}" style="${style}" fill="${c.star}" d="M0,-12 L2.4,-2.4 L12,0 L2.4,2.4 L0,12 L-2.4,2.4 L-12,0 L-2.4,-2.4Z"/></g>`;
}

function veins(c: ThemeColors, x0: number, y0: number, x1: number, y1: number, seed: number, n = 16, op = 0.35): string {
  const rng = createRng(seed);
  const out: string[] = [];

  function walk(x: number, y: number, a: number, steps: number, depth: number) {
    const pts = [`${f1(x)},${f1(y)}`];
    for (let i = 0; i < steps; i++) {
      a += rng() * 1.4 - 0.7;
      x += Math.cos(a) * (12 + rng() * 14);
      y += Math.sin(a) * (12 + rng() * 14);
      if (x < x0 || x > x1 || y < y0 || y > y1) break;
      pts.push(`${f1(x)},${f1(y)}`);
      if (depth < 2 && rng() < 0.22) {
        walk(x, y, a + (rng() < 0.5 ? -1 : 1) * (0.6 + rng() * 0.6), Math.floor(steps / 2), depth + 1);
      }
    }
    if (pts.length > 1) {
      out.push("M" + pts.join(" L"));
    }
  }

  for (let i = 0; i < n; i++) {
    walk(x0 + rng() * (x1 - x0), y0 + rng() * (y1 - y0), rng() * 6.28, Math.floor(5 + rng() * 5), 0);
  }

  return `<path d="${out.join(" ")}" fill="none" stroke="${c.gold}" stroke-width=".9" stroke-linecap="round" stroke-linejoin="round" opacity="${op}"/>`;
}

function vine(c: ThemeColors, x0: number, x1: number, y: number, amp: number, wl: number, seed: number, flowerEvery = 3): string {
  const rng = createRng(seed);
  const parts = [`<path d="${wave(x0, x1, y, amp, wl)}" fill="none" stroke="${c.gold}" stroke-width="1.8" stroke-linecap="round"/>`];
  let k = 0;
  let x = x0 + wl / 4;
  while (x < x1) {
    const yy = y + amp * Math.sin(((x - x0) / wl) * 2 * Math.PI);
    const side = k % 2 ? 1 : -1;
    if (k % flowerEvery === 2) {
      parts.push(rosette(Math.round(x), Math.round(yy + side * 9), 6.5, c));
    } else {
      const ang = (side < 0 ? -30 : 30) + (rng() * 20 - 10);
      parts.push(
        `<path transform="translate(${f1(x)},${f1(yy)}) rotate(${f1(ang)})" d="M0,0 Q8,${side * -9} 18,${side * -3} Q9,${side * 3} 0,0 Z" fill="${c.gold}" opacity=".85"/>`
      );
    }
    x += wl / 2;
    k++;
  }
  return parts.join("");
}

function base(c: ThemeColors, W: number, H: number, sid = "s"): { defs: string; bg: string } {
  const defs = `<linearGradient id="${sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  return { defs, bg: `<rect width="${W}" height="${H}" fill="url(#${sid}g)"/>` };
}

function panel(c: ThemeColors, x: number, y: number, w: number, h: number): string {
  const corners = [
    [x, y],
    [x + w, y],
    [x, y + h],
    [x + w, y + h],
  ]
    .map(([cx, cy]) => rosette(cx, cy, 6, c))
    .join("");
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="5" fill="${c.panel}" stroke="${c.gold}" stroke-width="2"/>
<rect x="${x + 7}" y="${y + 7}" width="${w - 14}" height="${h - 14}" rx="2" fill="none" stroke="${c.gold}" stroke-width=".9" opacity=".7"/>
${corners}`;
}

function heading(x: number, y: number, text: string, c: ThemeColors, size = 26): string {
  return `${rosette(x + 11, y - 9, 9, c)}
<text x="${x + 30}" y="${y}" font-family="${SERIF}" font-size="${size}" letter-spacing=".6" fill="${c.ink}">${escapeXml(text)}</text>
<path d="M${x + 30},${y + 12} H${x + 150}" stroke="${c.gold}" stroke-width="1.6"/>${diamond(x + 156, y + 12, 4, c.gold)}`;
}

function arch(x: number, y: number, w: number, h: number, pad = 0): string {
  const r = w / 2 + pad;
  return `M${f1(x - pad)},${f1(y + w / 2)} A${f1(r)},${f1(r)} 0 0 1 ${f1(x + w + pad)},${f1(y + w / 2)} V${f1(y + h + pad)} H${f1(x - pad)} Z`;
}

function hero(c: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const W = 900, H = 580;
  const { defs: bDefs, bg } = base(c, W, H, "h");
  const fx = 520, fy = 36, fw = 330;
  const fh = Math.round((fw * 789) / 526);

  const defs = bDefs + `
<clipPath id="hclip"><path d="${arch(fx, fy, fw, fh)}"/></clipPath>
<clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath>
<radialGradient id="hglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${c.glow}" stop-opacity=".45"/><stop offset="1" stop-color="${c.glow}" stop-opacity="0"/></radialGradient>
<linearGradient id="hsw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".38"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>`;

  const s: string[] = [
    bg,
    veins(c, 0, 0, 500, H, 7, 14, 0.3),
    veins(c, 560, 0, W, H, 9, 8, 0.25),
    `<ellipse cx="${fx + fw / 2}" cy="${fy + fh / 2}" rx="280" ry="320" fill="url(#hglow)"/>`,
    `<image href="${avatarImg}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>`,
    `<circle cx="64" cy="34" r="14" fill="none" stroke="${c.gold}" stroke-width="2"/>`,
    `<text x="86" y="39" font-family="${MONO}" font-size="12.5" fill="${c.soft}">${escapeXml(content.handle)} / README</text>`,
    `<path d="M50,62 H460" stroke="${c.gold}" stroke-width="1.2"/>${diamond(255, 62, 4.5, c.gold)}`,
    `<text x="52" y="124" font-family="${SERIF}" font-size="19" font-style="italic" fill="${c.soft}">Hi, I'm</text>`,
  ];

  const nameParts = content.name.split(" ");
  const name1 = nameParts[0] || content.name;
  const name2 = nameParts.slice(1).join(" ");

  for (const [txt, y] of [[name1, 196], [name2, 266]] as [string, number][]) {
    s.push(`<text x="55" y="${y + 3}" font-family="${SERIF}" font-size="64" fill="none" stroke="${c.gold}" stroke-width="1.2">${escapeXml(txt)}</text>`);
    s.push(`<text x="52" y="${y}" font-family="${SERIF}" font-size="64" fill="${c.ink}">${escapeXml(txt)}</text>`);
  }

  s.push(`<text x="53" y="326" font-family="${SANS}" font-size="13.5" font-weight="700" letter-spacing="6" fill="${c.accent}">${escapeXml(content.role.toUpperCase())}</text>`);
  s.push(`<text x="53" y="358" font-family="${SERIF}" font-size="17.5" font-style="italic" fill="${c.ink}">${escapeXml(content.pillars)}</text>`);
  content.tagline.forEach((line, i) => {
    s.push(`<text x="53" y="${404 + i * 23}" font-family="${SERIF}" font-size="15.5" fill="${c.soft}">${escapeXml(line)}</text>`);
  });

  s.push(vine(c, 50, 470, 506, 8, 110, 4));
  s.push(`<path d="${arch(fx, fy, fw, fh, 9)}" fill="none" stroke="${c.gold}" stroke-width="2.4"/>`);
  s.push(
    `<g clip-path="url(#hclip)"><image class="kb a" href="${heroImg}" x="${fx}" y="${fy}" width="${fw}" height="${fh}" preserveAspectRatio="xMidYMid slice"/><rect class="sweep a" x="${fx}" y="${fy}" width="90" height="${fh}" fill="url(#hsw)" transform="skewX(-12)"/></g>`
  );
  s.push(`<path d="${arch(fx, fy, fw, fh)}" fill="none" stroke="${c.ink}" stroke-width="1.5"/>`);
  s.push(star(fx + 20, fy + fh * 0.62, 0.8, c, "glint a", "animation-delay:-1s"));
  s.push(star(fx + fw - 24, fy + fh * 0.3, 1, c, "glint a", "animation-delay:-2.4s"));
  s.push(star(fx + 118, fy + 70, 0.7, c, "glint a", "animation-delay:-3s"));
  s.push(rosette(fx + fw / 2, fy - 18, 9, c));

  return svgDoc(W, H, s.join(""), `${content.name}: ${content.role}`, "Profile header with lapis blue arch window and gold ornaments.", defs);
}

function button(c: ThemeColors, label: string): string {
  const body = `<path d="M12,3 H138 L147,19 L138,35 H12 L3,19 Z" fill="${c.panel2}" stroke="${c.gold}" stroke-width="2"/>
<path d="M15,7 H135 L142,19 L135,31 H15 L8,19 Z" fill="none" stroke="${c.gold}" stroke-width=".8" opacity=".7"/>
${rosette(26, 19, 6, c)}
<text x="86" y="24.5" text-anchor="middle" font-family="${SERIF}" font-size="15" letter-spacing=".8" fill="${c.ink}">${escapeXml(label)}</text>`;
  return svgDoc(150, 40, body, label, `Button linking to ${label}`, "", false);
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "a");
  const s: string[] = [
    bg,
    panel(c, 16, 16, 868, 306),
    heading(50, 70, "About", c),
    heading(526, 70, "My journey", c),
  ];

  content.about.forEach((line, i) => {
    s.push(`<text x="52" y="${110 + i * 24}" font-family="${SERIF}" font-size="14.5" fill="${c.ink}">${escapeXml(line)}</text>`);
  });

  const factY = 110 + 24 * content.about.length + 22;
  s.push(`<text x="52" y="${factY}" font-family="${SANS}" font-size="12" fill="${c.soft}">Software engineering · Mathematics &amp; Physics · Based in Morocco</text>`);
  s.push(`<text x="52" y="${factY + 18}" font-family="${SANS}" font-size="12.5" font-weight="700" fill="${c.accent}">Focus: Systems, Web, Intelligence &amp; Mathematics</text>`);

  s.push(`<path d="${vwave(498, 50, 296, 3, 70)}" fill="none" stroke="${c.gold}" stroke-width="1.6"/>${rosette(498, 173, 7, c)}`);

  content.journey.forEach((item, i) => {
    const yy = 124 + i * 44;
    const x1 = 530 + item.lang.length * 10.6 + 12;
    const x2 = 850 - item.area.length * 7.6 - 32;
    s.push(`<text x="530" y="${yy}" font-family="${SERIF}" font-size="18" fill="${c.ink}">${escapeXml(item.lang)}</text>`);
    s.push(`<line class="flow a" x1="${f1(x1)}" y1="${yy - 5}" x2="${f1(x2)}" y2="${yy - 5}" stroke="${c.gold}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="2 10"/>`);
    s.push(diamond(Math.round(x2 + 8), yy - 5, 3.5, c.gold));
    s.push(`<text x="850" y="${yy}" text-anchor="end" font-family="${SANS}" font-size="13.5" font-weight="700" fill="${c.accent}">${escapeXml(item.area)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "About and journey", "About and journey section", defs);
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 340;
  const { defs, bg } = base(c, W, H, "k");
  const s: string[] = [bg, panel(c, 16, 16, 868, 306), heading(50, 70, "Technologies & Skills", c)];

  const cell = 800 / 6;
  content.skills.slice(0, 12).forEach((item, i) => {
    const cx = 50 + cell * ((i % 6) + 0.5);
    const cy = 142 + Math.floor(i / 6) * 104;
    const [fill, txt] = ROUNDEL[i % 4];
    s.push(`<circle cx="${f1(cx)}" cy="${cy}" r="33" fill="${fill}" stroke="${c.gold}" stroke-width="3"/>`);
    s.push(`<circle class="spin a" cx="${f1(cx)}" cy="${cy}" r="27" fill="none" stroke="${c.gold}" stroke-width="1.3" stroke-dasharray="3 5" style="animation-delay:-${i * 7}s"/>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 6}" text-anchor="middle" font-family="${SERIF}" font-size="17" font-weight="700" fill="${txt}">${escapeXml(item.mono)}</text>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 55}" text-anchor="middle" font-family="${SANS}" font-size="12" font-weight="700" fill="${c.ink}">${escapeXml(item.label)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "Technologies and skills", "Twelve gold-ringed medallions", defs);
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 84;
  const { defs, bg } = base(c, W, H, "p");
  const s = [bg, heading(50, 52, "Selected projects", c, 28), vine(c, 360, 850, 44, 6, 90, 2)];
  return svgDoc(W, H, s.join(""), "Selected projects", "Section heading", defs, false);
}

function card(c: ThemeColors, idx: number, title: string, desc: string, tags: string[], img: string): string {
  const W = 208, H = 280;
  const defs = `<clipPath id="lclip${idx}"><path d="${arch(16, 16, 176, 140)}"/></clipPath>`;

  const g = [
    `<rect x="6" y="6" width="196" height="268" rx="8" fill="${c.panel}" stroke="${c.gold}" stroke-width="1.8"/>`,
    `<g clip-path="url(#lclip${idx})"><image href="${img}" x="16" y="16" width="176" height="140" preserveAspectRatio="xMidYMid slice"/></g>`,
    `<path d="${arch(16, 16, 176, 140)}" fill="none" stroke="${c.gold}" stroke-width="1.4"/>`,
    rosette(104, 156, 7, c),
    `<text x="104" y="184" text-anchor="middle" font-family="${SERIF}" font-weight="700" font-size="17" fill="${c.ink}">${escapeXml(title)}</text>`,
    `<text x="104" y="202" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(0, 32))}</text>`,
  ];

  if (desc.length > 32) {
    g.push(`<text x="104" y="216" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(32, 64))}</text>`);
  }

  g.push(`<text x="104" y="242" text-anchor="middle" font-family="${SANS}" font-size="10" font-weight="700" fill="${c.accent}">${escapeXml(tags.slice(0, 3).join(" · "))}</text>`);

  return svgDoc(W, H, g.join(""), `Project ${title}`, `${title}: ${desc}`, defs);
}

function footer(c: ThemeColors, content: Content, footerImg: string): string {
  const W = 900, H = 280;
  const { defs, bg } = base(c, W, H, "f");
  const s = [
    bg,
    `<rect x="16" y="16" width="868" height="216" rx="6" fill="${c.panel}" stroke="${c.gold}" stroke-width="2"/>`,
    vine(c, 40, 860, 48, 6, 90, 5),
    `<text x="450" y="112" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="34" fill="${c.ink}">${escapeXml(content.footer.line1)}</text>`,
    `<text x="450" y="152" text-anchor="middle" font-family="${SANS}" font-size="13" letter-spacing="1.5" fill="${c.soft}">${escapeXml(content.footer.line2)}</text>`,
    vine(c, 40, 860, 192, 6, 90, 8),
    `<rect x="0" y="${H - 32}" width="${W}" height="32" fill="${c.band}"/>`,
    `<text x="30" y="${H - 12}" font-family="${SANS}" font-size="10.5" fill="#F3EBDD">Artwork: celestial lapis &amp; gold</text>`,
    `<text x="870" y="${H - 12}" text-anchor="end" font-family="${SANS}" font-size="11.5" font-weight="700" fill="${c.gold}">NashirTech · ناشر تك</text>`,
  ];

  return svgDoc(W, H, s.join(""), "Footer", `${content.footer.line1}. ${content.footer.line2}`, defs);
}

export const lapisStyle: StyleModule = {
  id: "lapis",
  name: "Celestial Lapis",
  keywords: ["indigo", "gold", "kintsugi", "celestial", "medieval"],
  palette: {
    dark: ["#0B0F2E", "#1B2466", "#E8C46A", "#F3EBDD", "#8E9BDB"],
    light: ["#F5EDDF", "#E2E2F1", "#7A5A12", "#161C5A", "#BE9435"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/lapis/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 526, 789], [330, 495], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [170, 330, 310, 470], [64, 64], 0.9);

    const cropBoxes: [number, number, number, number][] = [
      [0, 40, 240, 280],
      [160, 170, 400, 410],
      [286, 239, 526, 479],
      [0, 260, 240, 500],
      [160, 450, 400, 690],
      [286, 479, 526, 719],
      [0, 549, 240, 789],
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
      pic("hero", `${content.name}, ${content.role}. Lapis arch window with golden illuminated ornaments.`, "100%"),
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
