import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const ARAB = "'Amiri','Scheherazade New','Noto Naskh Arabic','Geeza Pro','Segoe UI',Tahoma,serif";

const TILES = ["#2A8C82", "#C4573C", "#8FB39A", "#A99CD0"];

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  panel2: string;
  ink: string;
  soft: string;
  accent: string;
  gold: string;
  line: string;
  band: string;
  btn: string;
  btntxt: string;
  seal: string;
  glow: string;
  star: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0D1B19",
    bg2: "#183530",
    panel: "#132826",
    panel2: "#1C3A35",
    ink: "#F3EAD3",
    soft: "#C2D2C4",
    accent: "#E8B27A",
    gold: "#CDA652",
    line: "#CDA652",
    band: "#081211",
    btn: "#B04A32",
    btntxt: "#FFF6E0",
    seal: "#C4573C",
    glow: "#A99CD0",
    star: "#F6E3A8",
  },
  light: {
    bg: "#F5ECD6",
    bg2: "#E6E4CF",
    panel: "#FBF6E6",
    panel2: "#EBE5D0",
    ink: "#17332F",
    soft: "#496660",
    accent: "#A2412A",
    gold: "#B38B34",
    line: "#B38B34",
    band: "#17332F",
    btn: "#B04A32",
    btntxt: "#FFF6E0",
    seal: "#B04A32",
    glow: "#A99CD0",
    star: "#B38B34",
  },
};

const CSS = `<style>
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.kb{transform-box:fill-box;transform-origin:50% 45%;animation-name:kb;animation-duration:32s}
.glint{transform-box:fill-box;transform-origin:center;animation-name:glint;animation-duration:4s}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:90s;animation-timing-function:linear;animation-direction:normal}
.flow{animation-name:flow;animation-duration:6s;animation-timing-function:linear;animation-direction:normal}
.breathe{animation-name:breathe;animation-duration:7s}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.06)}}
@keyframes glint{0%{opacity:.3;transform:scale(.6)}60%{opacity:1;transform:scale(1.1)}100%{opacity:.4;transform:scale(.7)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flow{to{stroke-dashoffset:-48}}
@keyframes breathe{from{opacity:.55}to{opacity:1}}
@media (prefers-reduced-motion: reduce){.a{animation:none}}
</style>`;

const AR_NUMS = ["١", "٢", "٣", "٤", "٥", "٦", "٧", "٨"];

function star8Pts(cx: number, cy: number, ro: number, ratio = 0.62): string {
  const pts: string[] = [];
  for (let i = 0; i < 16; i++) {
    const a = -Math.PI / 2 + (i * Math.PI) / 8;
    const r = i % 2 === 0 ? ro : ro * ratio;
    pts.push(`${f1(cx + r * Math.cos(a))},${f1(cy + r * Math.sin(a))}`);
  }
  return pts.join(" ");
}

function star8(cx: number, cy: number, ro: number, fill: string, stroke?: string, sw = 1, op = 1): string {
  const st = stroke ? ` stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"` : "";
  return `<polygon points="${star8Pts(cx, cy, ro)}" fill="${fill}"${st} opacity="${op}"/>`;
}

function diamond(cx: number, cy: number, r: number, fill: string): string {
  return `<path d="M${f1(cx)},${f1(cy - r)} L${f1(cx + r)},${f1(cy)} L${f1(cx)},${f1(cy + r)} L${f1(cx - r)},${f1(cy)} Z" fill="${fill}"/>`;
}

function horseshoe(x: number, y: number, W: number, H: number, pad = 0): string {
  const R0 = W / 1.92;
  const cx = x + W / 2;
  const cy = y + R0;
  const R = R0 + pad;
  const d = 0.96 * R;
  const ys = cy + 0.28 * R;
  return `M${f1(cx - d)},${f1(ys)} A${f1(R)},${f1(R)} 0 1 1 ${f1(cx + d)},${f1(ys)} V${f1(y + H + pad)} H${f1(cx - d)} Z`;
}

function merlons(x: number, y: number, w: number, n: number, h = 14): string {
  const u = w / n;
  let d = `M${x},${y + h}`;
  for (let i = 0; i < n; i++) {
    d += ` L${f1(x + u * i + u / 2)},${y} L${f1(x + u * (i + 1))},${y + h}`;
  }
  return d;
}

function frieze(T: ThemeColors, x0: number, x1: number, y: number, h: number, phase = 0, breathe = false): string {
  const step = h * 1.3;
  const n = Math.floor((x1 - x0) / step);
  const off = (x1 - x0 - n * step) / 2 + step / 2;
  const out = [`<path d="M${x0},${y + h / 2} H${x1}" stroke="${T.gold}" stroke-width="1" opacity=".6"/>`];
  for (let i = 0; i < n; i++) {
    const cx = x0 + off + i * step;
    const cls = breathe && i % 3 === 0 ? ' class="breathe a"' : "";
    const style = cls ? ` style="animation-delay:-${i % 7}s"` : "";
    out.push(`<g${cls}${style}>${star8(cx, y + h / 2, h / 2, TILES[(i + phase) % 4], T.ink, 0.8)}</g>`);
    if (i < n - 1) {
      out.push(diamond(cx + step / 2, y + h / 2, h * 0.16, T.gold));
    }
  }
  return out.join("");
}

function muqarnas(T: ThemeColors, x0: number, x1: number, y: number, tiers = 3): string {
  const out: string[] = [];
  const w = 44, h = 34;
  for (let t = 0; t < tiers; t++) {
    const cnt = Math.floor((x1 - x0) / w) + 2;
    for (let i = 0; i < cnt; i++) {
      const x = x0 + i * w - (t % 2 ? w / 2 : 0) - (t * 2);
      const yy = y + t * 20;
      const d = `M${f1(x)},${yy} C${f1(x)},${f1(yy + h * 0.7)} ${f1(x + w / 2 - 7)},${f1(yy + h * 0.88)} ${f1(x + w / 2)},${f1(yy + h)} C${f1(x + w / 2 + 7)},${f1(yy + h * 0.88)} ${f1(x + w)},${f1(yy + h * 0.7)} ${f1(x + w)},${yy} Z`;
      out.push(`<path d="${d}" fill="${TILES[(i + t) % 4]}" stroke="${T.ink}" stroke-width="1" opacity="${(0.95 - t * 0.1).toFixed(2)}"/>`);
    }
  }
  return out.join("");
}

function tilePattern(T: ThemeColors, pid: string): string {
  return `<pattern id="${pid}" width="56" height="56" patternUnits="userSpaceOnUse"><rect x="9" y="9" width="38" height="38" fill="none" stroke="${T.line}" stroke-width=".8"/><path d="M28,2 L54,28 L28,54 L2,28 Z" fill="none" stroke="${T.line}" stroke-width=".8"/><circle cx="28" cy="28" r="3" fill="none" stroke="${T.line}" stroke-width=".8"/></pattern>`;
}

function base(T: ThemeColors, W: number, H: number, sid: string): [string, string] {
  const defs = `<linearGradient id="${sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${T.bg}"/><stop offset="1" stop-color="${T.bg2}"/></linearGradient>${tilePattern(T, sid + "t")}`;
  const bg = `<rect width="${W}" height="${H}" fill="url(#${sid}g)"/><rect width="${W}" height="${H}" fill="url(#${sid}t)" opacity=".13"/>`;
  return [defs, bg];
}

function starTwinkle(x: number, y: number, s: number, T: ThemeColors, delay = 0): string {
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><path class="glint a" style="animation-delay:-${delay}s" fill="${T.star}" d="M0,-12 L2.4,-2.4 L12,0 L2.4,2.4 L0,12 L-2.4,2.4 L-12,0 L-2.4,-2.4Z"/></g>`;
}

function panel(T: ThemeColors, x: number, y: number, w: number, h: number, n: number): string {
  const d = merlons(x, y, w, n) + ` V${y + h} H${x} Z`;
  return `<path d="${d}" fill="${T.panel}" stroke="${T.gold}" stroke-width="2" stroke-linejoin="round"/><rect x="${x + 8}" y="${y + 20}" width="${w - 16}" height="${h - 28}" fill="none" stroke="${T.gold}" stroke-width=".8" opacity=".6"/>${frieze(T, x + 18, x + w - 18, y + 26, 18, 0)}`;
}

function heading(x: number, y: number, text: string, ar: string, arRight: number, T: ThemeColors, size = 28): string {
  const arsize = 21;
  const arw = ar.length * arsize * 0.45;
  return `${star8(x + 11, y - 9, 11, TILES[1], T.ink, 1)}<text x="${x + 32}" y="${y}" font-family="${SERIF}" font-size="${size}" letter-spacing=".8" fill="${T.ink}">${escapeXml(text)}</text><text x="${f1(arRight - arw / 2)}" y="${y - 1}" text-anchor="middle" font-family="${ARAB}" font-size="${arsize}" fill="${T.accent}">${escapeXml(ar)}</text>`;
}

function svgWrap(W: number, H: number, body: string, title: string, desc: string, defs = "", animated = true): string {
  const style = animated ? CSS : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${escapeXml(title)}"><title>${escapeXml(title)}</title><desc>${escapeXml(desc)}</desc><defs>${defs}</defs>${style}${body}</svg>`;
}

function hero(T: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const W = 900, H = 610;
  const [baseDefs, bg] = base(T, W, H, "h");
  const ax = 530, ay = 52, aw = 320, ah = 480;
  const defs = `${baseDefs}<clipPath id="hclip"><path d="${horseshoe(ax, ay, aw, ah)}"/></clipPath><clipPath id="hav"><circle cx="64" cy="34" r="14"/></clipPath><radialGradient id="hglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${T.glow}" stop-opacity=".5"/><stop offset="1" stop-color="${T.glow}" stop-opacity="0"/></radialGradient>`;
  
  const s: string[] = [bg, `<ellipse cx="${ax + aw / 2}" cy="${ay + ah / 2}" rx="280" ry="310" fill="url(#hglow)"/>`];
  s.push(`<image href="${avatarImg}" x="50" y="20" width="28" height="28" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/>`);
  s.push(`<circle cx="64" cy="34" r="14" fill="none" stroke="${T.gold}" stroke-width="1.8"/>`);
  s.push(`<text x="86" y="39" font-family="${MONO}" font-size="12.5" fill="${T.soft}">${escapeXml(content.handle)} / README</text>`);
  s.push(`<path d="M50,62 H470" stroke="${T.gold}" stroke-width="1.2"/>${star8(260, 62, 8, TILES[1], T.ink, 0.8)}`);
  s.push(`<text x="52" y="128" font-family="${SERIF}" font-size="19" font-style="italic" fill="${T.soft}">Hi, I'm</text>`);

  const nameParts = content.name.split(" ");
  const name1 = nameParts[0] || content.name;
  const name2 = nameParts.slice(1).join(" ");

  if (name2) {
    s.push(`<text x="54" y="201" font-family="${SERIF}" font-size="62" letter-spacing="1" fill="${TILES[0]}" opacity=".55">${escapeXml(name1)}</text>`);
    s.push(`<text x="52" y="198" font-family="${SERIF}" font-size="62" letter-spacing="1" fill="${T.ink}">${escapeXml(name1)}</text>`);
    s.push(`<text x="54" y="269" font-family="${SERIF}" font-size="62" letter-spacing="1" fill="${TILES[0]}" opacity=".55">${escapeXml(name2)}</text>`);
    s.push(`<text x="52" y="266" font-family="${SERIF}" font-size="62" letter-spacing="1" fill="${T.ink}">${escapeXml(name2)}</text>`);
  } else {
    s.push(`<text x="54" y="201" font-family="${SERIF}" font-size="54" letter-spacing="1" fill="${TILES[0]}" opacity=".55">${escapeXml(name1)}</text>`);
    s.push(`<text x="52" y="198" font-family="${SERIF}" font-size="54" letter-spacing="1" fill="${T.ink}">${escapeXml(name1)}</text>`);
  }

  s.push(`<text x="53" y="324" font-family="${SANS}" font-size="13.5" font-weight="700" letter-spacing="5" fill="${T.accent}">${escapeXml(content.role.toUpperCase())}</text>`);
  if (content.options.useArabic) {
    s.push(`<text x="425" y="325" text-anchor="middle" font-family="${ARAB}" font-size="19" fill="${T.accent}">مهندس برمجيات</text>`);
  }
  s.push(`<text x="53" y="358" font-family="${SERIF}" font-size="17.5" font-style="italic" fill="${T.ink}">${escapeXml(content.pillars)}</text>`);

  content.tagline.forEach((line, i) => {
    s.push(`<text x="53" y="${408 + i * 23}" font-family="${SERIF}" font-size="15.5" fill="${T.soft}">${escapeXml(line)}</text>`);
  });

  // Horseshoe arch with authentic zellige borders
  s.push(`<path d="${horseshoe(ax, ay, aw, ah, 15)}" fill="none" stroke="${TILES[0]}" stroke-width="9"/>`);
  s.push(`<path d="${horseshoe(ax, ay, aw, ah, 15)}" fill="none" stroke="${TILES[1]}" stroke-width="9" stroke-dasharray="9 27"/>`);
  s.push(`<path d="${horseshoe(ax, ay, aw, ah, 15)}" fill="none" stroke="${TILES[3]}" stroke-width="9" stroke-dasharray="9 27" stroke-dashoffset="-18"/>`);
  s.push(`<path d="${horseshoe(ax, ay, aw, ah, 21)}" fill="none" stroke="${T.gold}" stroke-width="2"/>`);
  s.push(`<path d="${horseshoe(ax, ay, aw, ah, 9)}" fill="none" stroke="${T.gold}" stroke-width="1.4"/>`);
  s.push(`<g clip-path="url(#hclip)"><image class="kb a" href="${heroImg}" x="${ax}" y="${ay}" width="${aw}" height="${ah}" preserveAspectRatio="xMidYMid slice"/></g>`);
  s.push(`<path d="${horseshoe(ax, ay, aw, ah)}" fill="none" stroke="${T.ink}" stroke-width="1.5"/>`);
  s.push(star8(ax + aw / 2, ay - 42, 13, TILES[1], T.ink, 1.2));
  s.push(starTwinkle(ax + aw / 2, ay - 42, 0.8, T));
  s.push(`<text x="${ax + aw / 2}" y="${ay + ah + 36}" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${T.soft}">Artwork: Teal Newcomb</text>`);
  s.push(frieze(T, 0, W, H - 34, 22, 1, true));

  return svgWrap(W, H, s.join(""), `${content.name}: ${content.role}`, "Profile header with horseshoe arch window.", defs, true);
}

function button(T: ThemeColors, label: string): string {
  const body = `<path d="M14,3 H136 L147,20 L136,37 H14 L3,20 Z" fill="${T.btn}" stroke="${T.gold}" stroke-width="1.6"/>${star8(28, 20, 8, T.btntxt)}<text x="89" y="25.5" text-anchor="middle" font-family="${SERIF}" font-size="15" letter-spacing=".8" fill="${T.btntxt}">${escapeXml(label)}</text>`;
  return svgWrap(150, 40, body, label, `Button linking to ${label}`, "", false);
}

function about(T: ThemeColors, content: Content): string {
  const W = 900, H = 410;
  const [baseDefs, bg] = base(T, W, H, "a");
  const s: string[] = [bg, panel(T, 18, 14, 864, 376, 24)];
  s.push(heading(52, 104, "About", content.options.useArabic ? "نبذة عني" : "PROFILE", 440, T));
  s.push(heading(520, 104, "My journey", content.options.useArabic ? "رحلتي" : "JOURNEY", 850, T));

  const words = content.about.join(" ").split(" ");
  const lines: string[] = [];
  let cur = "";
  words.forEach((w) => {
    if ((cur + " " + w).trim().length > 50) {
      lines.push(cur.trim());
      cur = w;
    } else {
      cur = (cur + " " + w).trim();
    }
  });
  if (cur) lines.push(cur);

  lines.slice(0, 6).forEach((line, i) => {
    s.push(`<text x="54" y="${146 + i * 24}" font-family="${SERIF}" font-size="14.5" fill="${T.ink}">${escapeXml(line)}</text>`);
  });

  const factsY = 146 + 24 * Math.min(lines.length, 6) + 20;
  s.push(`<text x="54" y="${factsY}" font-family="${SANS}" font-size="12" fill="${T.soft}">Focus: AI Fullstack, Backend &amp; DevOps</text>`);
  s.push(`<path d="M488,84 V350" stroke="${T.gold}" stroke-width="1.2"/>`);
  
  [130, 217, 304].forEach((yy, k) => {
    s.push(star8(488, yy, 7, TILES[(k + 1) % 4], T.ink, 0.8));
  });

  content.journey.slice(0, 5).forEach((j, i) => {
    const yy = 160 + i * 44;
    const x1 = 520 + j.lang.length * 10.4 + 14;
    const x2 = 850 - j.area.length * 7.6 - 30;
    s.push(`<text x="520" y="${yy}" font-family="${SERIF}" font-size="18" fill="${T.ink}">${escapeXml(j.lang)}</text>`);
    s.push(`<line class="flow a" x1="${f1(x1)}" y1="${yy - 5}" x2="${f1(x2)}" y2="${yy - 5}" stroke="${TILES[i % 4]}" stroke-width="3" stroke-linecap="round" stroke-dasharray="3 9"/>`);
    s.push(diamond(Math.round(x2 + 10), yy - 5, 4, T.gold));
    s.push(`<text x="850" y="${yy}" text-anchor="end" font-family="${SANS}" font-size="13.5" font-weight="700" fill="${T.accent}">${escapeXml(j.area)}</text>`);
  });

  return svgWrap(W, H, s.join(""), "About and journey", "About text and journey.", baseDefs, true);
}

function skills(T: ThemeColors, content: Content): string {
  const W = 900, H = 440;
  const [baseDefs, bg] = base(T, W, H, "k");
  const s: string[] = [bg, panel(T, 18, 14, 864, 406, 24), heading(52, 104, "Technologies & Skills", content.options.useArabic ? "التقنيات والمهارات" : "SKILLS", 850, T)];
  const cell = 800 / 6;

  content.skills.slice(0, 12).forEach((sk, i) => {
    const cx = 50 + cell * ((i % 6) + 0.5);
    const cy = 196 + Math.floor(i / 6) * 118;
    const col = TILES[i % 4];
    s.push(`<g class="spin a" style="animation-delay:-${i * 9}s"><polygon points="${star8Pts(cx, cy, 46, 0.8)}" fill="none" stroke="${T.gold}" stroke-width="1.2" stroke-dasharray="4 5"/></g>`);
    s.push(star8(cx, cy, 38, col, T.ink, 1.6));
    s.push(`<circle cx="${f1(cx)}" cy="${cy}" r="18" fill="${T.panel}" stroke="${T.ink}" stroke-width="1.4"/>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 5}" text-anchor="middle" font-family="${SERIF}" font-size="14" font-weight="700" fill="${T.ink}">${escapeXml(sk.mono)}</text>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 62}" text-anchor="middle" font-family="${SANS}" font-size="12" font-weight="700" fill="${T.ink}">${escapeXml(sk.label)}</text>`);
  });

  return svgWrap(W, H, s.join(""), "Technologies and skills", "Twelve eight-point star tiles.", baseDefs, true);
}

function projectsTitle(T: ThemeColors, content: Content): string {
  const W = 900, H = 96;
  const [baseDefs, bg] = base(T, W, H, "p");
  const s = [bg, heading(52, 58, "Selected projects", content.options.useArabic ? "مشاريع مختارة" : "PROJECTS", 850, T, 30), frieze(T, 420, 700, 40, 16, 2)];
  return svgWrap(W, H, s.join(""), "Selected projects", "Section heading.", baseDefs, false);
}

function tagLines(tags: string[]): string[] {
  const lines: string[] = [];
  let cur = "";
  for (const t of tags) {
    const nxt = !cur ? t : cur + " · " + t;
    if (nxt.length > 30 && cur) {
      lines.push(cur);
      cur = t;
    } else {
      cur = nxt;
    }
  }
  if (cur) lines.push(cur);
  return lines;
}

function card(T: ThemeColors, idx: number, title: string, desc: string, tags: string[], img: string): string {
  const W = 208, H = 284;
  const defs = `<clipPath id="c${idx}"><path d="${horseshoe(38, 34, 132, 122)}"/></clipPath>`;
  const body = merlons(6, 6, 196, 7, 12) + ` V${H - 8} H6 Z`;
  const g: string[] = [
    `<path d="${body}" fill="${T.panel}" stroke="${T.gold}" stroke-width="2" stroke-linejoin="round"/>`,
    `<path d="${horseshoe(38, 34, 132, 122, 6)}" fill="none" stroke="${TILES[(idx - 1) % 4]}" stroke-width="5"/>`,
    `<g clip-path="url(#c${idx})"><image href="${img}" x="38" y="34" width="132" height="122" preserveAspectRatio="xMidYMid slice"/></g>`,
    `<path d="${horseshoe(38, 34, 132, 122)}" fill="none" stroke="${T.ink}" stroke-width="1.4"/>`,
    star8(104, 158, 17, T.seal, T.ink, 1.4),
    `<text x="104" y="164" text-anchor="middle" font-family="${ARAB}" font-size="17" font-weight="700" fill="#FFF6E0">${AR_NUMS[idx - 1] || idx}</text>`,
    `<text x="104" y="198" text-anchor="middle" font-family="${SERIF}" font-size="${Math.min(16, 176 / (title.length * 0.66)).toFixed(1)}" font-weight="700" fill="${T.ink}">${escapeXml(title)}</text>`,
  ];

  const descWords = desc.split(" ");
  const dLines: string[] = [];
  let dCur = "";
  descWords.forEach((w) => {
    if ((dCur + " " + w).trim().length > 28) {
      dLines.push(dCur.trim());
      dCur = w;
    } else {
      dCur = (dCur + " " + w).trim();
    }
  });
  if (dCur) dLines.push(dCur);

  dLines.slice(0, 2).forEach((line, i) => {
    g.push(`<text x="104" y="${217 + i * 14}" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${T.soft}">${escapeXml(line)}</text>`);
  });

  tagLines(tags).slice(0, 2).forEach((line, i) => {
    g.push(`<text x="104" y="${250 + i * 15}" text-anchor="middle" font-family="${SANS}" font-size="10.5" font-weight="700" fill="${T.accent}">${escapeXml(line)}</text>`);
  });

  return svgWrap(W, H, g.join(""), `Project ${title}`, `${title}: ${desc}`, defs, false);
}

function footer(T: ThemeColors, content: Content): string {
  const W = 900, H = 350;
  const [baseDefs, bg] = base(T, W, H, "f");
  const s: string[] = [bg, muqarnas(T, -20, W + 20, 0, 3)];
  s.push(`<text x="450" y="164" text-anchor="middle" font-family="${SERIF}" font-size="31" letter-spacing="1" fill="${T.ink}">${escapeXml(content.footer.line1)}</text>`);
  if (content.options.useArabic) {
    s.push(`<text x="450" y="198" text-anchor="middle" font-family="${ARAB}" font-size="23" fill="${T.accent}">ابنِ · اكتشف · افهم</text>`);
  }
  s.push(`<text x="450" y="226" text-anchor="middle" font-family="${SANS}" font-size="13" letter-spacing="1" fill="${T.soft}">${escapeXml(content.footer.line2)}</text>`);
  s.push(frieze(T, 0, W, H - 82, 24, 0, true));
  s.push(starTwinkle(450, 116, 1, T));
  s.push(`<rect x="0" y="${H - 34}" width="${W}" height="34" fill="${T.band}"/>`);
  s.push(`<path d="M0,${H - 34} H${W}" stroke="${T.gold}" stroke-width="2"/>`);
  s.push(`<text x="30" y="${H - 13}" font-family="${SANS}" font-size="10.5" fill="#F3EAD3">Artwork: Teal Newcomb (Metal Kirin)</text>`);
  s.push(`<text x="870" y="${H - 13}" text-anchor="end" font-family="${SANS}" font-size="11.5" font-weight="700" fill="#E8B27A">NashirTech · ناشر تك</text>`);

  return svgWrap(W, H, s.join(""), "Footer", `${content.footer.line1}. ${content.footer.line2}`, baseDefs, true);
}

export const andalusStyle: StyleModule = {
  id: "andalus",
  name: "Andalus",
  keywords: ["moroccan", "zellige", "horseshoe-arch", "alhambra"],
  palette: {
    light: ["#F5ECD6", "#17332F", "#A2412A", "#B38B34", "#2A8C82"],
    dark: ["#0D1B19", "#F3EAD3", "#E8B27A", "#CDA652", "#2A8C82"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/andalus/source.jpg");
    // High-quality crops from source.jpg
    const heroCrop = ctx.cropToDataUrl(img, [0, 115, 736, 1097], [640, 854], 0.92);
    const avatarCrop = ctx.cropToDataUrl(img, [130, 410, 290, 570], [64, 64], 0.92);

    const cropBoxes: [number, number, number, number][] = [
      [170, 140, 370, 340],
      [130, 410, 290, 570],
      [400, 380, 640, 620],
      [0, 780, 240, 1020],
      [440, 810, 640, 1010],
      [536, 897, 736, 1097],
      [480, 20, 730, 270],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [220, 220], 0.9)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop, avatarCrop);
      files[`about-${theme}.svg`] = about(c, content);
      files[`skills-${theme}.svg`] = skills(c, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(c, content);
      files[`footer-${theme}.svg`] = footer(c, content);
      files[`btn-github-${theme}.svg`] = button(c, "GitHub");
      files[`btn-linkedin-${theme}.svg`] = button(c, "LinkedIn");
      files[`btn-portfolio-${theme}.svg`] = button(c, "Portfolio");

      content.projects.forEach((proj, idx) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(
          c,
          idx + 1,
          proj.title,
          proj.line1 + " " + proj.line2,
          proj.tags,
          cardCrops[idx]
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
      pic("hero", `${content.name}, ${content.role}. Horseshoe arch window with pale lavender dragons.`, "100%"),
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

