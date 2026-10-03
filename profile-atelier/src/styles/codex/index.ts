import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Book Antiqua','DejaVu Serif',serif";
const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"];

interface ThemeColors {
  bg1: string;
  bg2: string;
  fg: string;
  ink: string;
  mute: string;
  blue: string;
  blue2: string;
  verm: string;
  gold: string;
  line: string;
  card: string;
  cream: string;
  teal: string;
  orange: string;
  grain: string;
  petals: string[];
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  light: {
    bg1: "#f7edcc",
    bg2: "#e9d6a2",
    fg: "#2a2118",
    ink: "#2a1d12",
    mute: "#6b5a43",
    blue: "#1d3f94",
    blue2: "#2f5fc4",
    verm: "#c4321f",
    gold: "#b3841c",
    line: "#c7ad70",
    card: "#fbf3d8",
    cream: "#fbf1d0",
    teal: "#2b8484",
    orange: "#e8892a",
    grain: "0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .1  0 0 0 .20 0",
    petals: ["#2b57c4", "#6c8fe0", "#d9a52a", "#e8892a"],
  },
  dark: {
    bg1: "#0f1c47",
    bg2: "#070d26",
    fg: "#f4e9c9",
    ink: "#080c1e",
    mute: "#b9ac8a",
    blue: "#1a3270",
    blue2: "#4a74e0",
    verm: "#e5583e",
    gold: "#e8c45a",
    line: "#4a5a98",
    card: "#12224f",
    cream: "#f4e9c9",
    teal: "#4cb0aa",
    orange: "#ff9a45",
    grain: "0 0 0 0 .95  0 0 0 0 .85  0 0 0 0 .6  0 0 0 .09 0",
    petals: ["#7fa2ff", "#bcd0ff", "#f1cd6a", "#ff9a45"],
  },
};

const STYLE = `<style>
.spin{transform-box:fill-box;transform-origin:center;animation:spin 80s linear infinite}
.spin.r{animation-direction:reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.tw{transform-box:fill-box;transform-origin:center;animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.3;transform:scale(.6)}50%{opacity:1;transform:scale(1.15)}}
.flick{animation:fl 2.8s ease-in-out infinite}
@keyframes fl{0%,100%{opacity:.65}30%{opacity:1}55%{opacity:.5}80%{opacity:.95}}
.glow{animation:glow 6s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.45}50%{opacity:1}}
.sweep{animation:sw 7s ease-in-out infinite}
@keyframes sw{0%,30%{transform:translateX(-140px)}70%,100%{transform:translateX(420px)}}
.leafsway{transform-box:fill-box;transform-origin:0 0;animation:ls 7s ease-in-out infinite alternate}
@keyframes ls{from{transform:rotate(-6deg)}to{transform:rotate(6deg)}}
.swing{transform-origin:top center;animation:sg 6s ease-in-out infinite alternate}
@keyframes sg{from{transform:rotate(-4deg)}to{transform:rotate(4deg)}}
.tail{transform-origin:82px 96px;animation:tl 4s ease-in-out infinite alternate}
@keyframes tl{from{transform:rotate(-8deg)}to{transform:rotate(12deg)}}
.fall{animation:fall linear infinite}
@keyframes fall{from{transform:translateY(-30px)}to{transform:translateY(540px)}}
.sway{transform-box:fill-box;transform-origin:center;animation:sway ease-in-out infinite alternate}
@keyframes sway{from{transform:translateX(-18px) rotate(-25deg)}to{transform:translateX(18px) rotate(25deg)}}
.ff{animation:ff ease-in-out infinite alternate}
@keyframes ff{0%{opacity:.15;transform:translate(0,0)}50%{opacity:.8;transform:translate(6px,-10px)}100%{opacity:.2;transform:translate(-6px,-18px)}}
@media (prefers-reduced-motion:reduce){.spin,.tw,.flick,.glow,.sweep,.leafsway,.swing,.tail,.fall,.sway,.ff{animation:none}}
</style>`;

function star4(x: number, y: number, s: number, col: string, op = 1, cls = "", delay = 0): string {
  const d = `M${f1(x)} ${f1(y - s)}Q${f1(x)} ${f1(y)} ${f1(x + s)} ${f1(y)}Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y + s)}Q${f1(x)} ${f1(y)} ${f1(x - s)} ${f1(y)}Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y - s)}Z`;
  const st = cls ? ` style="animation-delay:${(-delay).toFixed(1)}s;animation-duration:${(3 + (delay % 3)).toFixed(1)}s"` : "";
  return `<path class="${cls}" d="${d}" fill="${col}" opacity="${op}"${st}/>`;
}

function quatrefoil(x: number, y: number, s: number, c: ThemeColors): string {
  let o = "";
  const offsets: [number, number][] = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  offsets.forEach(([dx, dy]) => {
    o += `<circle cx="${f1(x + dx * s)}" cy="${f1(y + dy * s)}" r="${f1(s * 0.62)}" fill="url(#gold)" stroke="${c.ink}" stroke-width=".6"/>`;
  });
  return o + `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(s * 0.55)}" fill="${c.verm}" stroke="${c.ink}" stroke-width=".6"/>`;
}

function spiral(cx: number, cy: number, r: number, turns = 2, rot = 0): string {
  const pts: [number, number][] = [];
  const n = Math.floor(turns * 20);
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const th = t * turns * 2 * Math.PI + rot;
    const rr = r * (0.12 + 0.88 * (1 - t));
    pts.push([cx + rr * Math.cos(th), cy + rr * Math.sin(th)]);
  }
  return "M" + pts.map(([x, y]) => `${f1(x)} ${f1(y)}`).join("L");
}

const LEAF = "M0 0C6 -3 11 -11 5 -17C2 -13 0 -13 -2 -17C-8 -11 -6 -3 0 0Z";

function vine(c: ThemeColors, x0: number, x1: number, y: number, seed = 1, amp = 4): string {
  const o: string[] = [];
  const stem: [number, number][] = [];
  for (let x = Math.floor(x0); x <= Math.floor(x1); x += 5) {
    stem.push([x, y + amp * Math.sin(x / 28)]);
  }
  o.push(`<path d="M${stem.map(([a, b]) => `${f1(a)} ${f1(b)}`).join("L")}" fill="none" stroke="${c.gold}" stroke-width="1.4"/>`);

  let k = 0;
  for (let x = Math.floor(x0) + 20; x < Math.floor(x1) - 10; x += 38) {
    const yy = y + amp * Math.sin(x / 28);
    const up = k % 2 === 0;
    const sgn = up ? -1 : 1;
    o.push(`<path d="${spiral(x + 6, yy + sgn * 9, 8, 2, (seed * 1.5) % 6)}" fill="none" stroke="${c.gold}" stroke-width="1.1"/>`);
    o.push(`<circle cx="${x + 6}" cy="${f1(yy + sgn * 9)}" r="2.4" fill="${c.verm}"/>`);
    const col = k % 3 ? c.blue2 : c.teal;
    o.push(`<g class="leafsway"><path transform="translate(${x - 10} ${f1(yy)}) rotate(${up ? -35 : 145}) scale(.9)" d="${LEAF}" fill="${col}" stroke="${c.ink}" stroke-width=".5"/></g>`);
    o.push(`<circle cx="${x + 20}" cy="${f1(yy + (up ? -5 : 5))}" r="1.8" fill="url(#gold)"/>`);
    k++;
  }
  return o.join("");
}

function defs(c: ThemeColors): string {
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a6212"/><stop offset=".3" stop-color="#f3dc84"/><stop offset=".55" stop-color="#c79a2e"/><stop offset=".8" stop-color="#f7e9a8"/><stop offset="1" stop-color="#9a7218"/></linearGradient>
<linearGradient id="shim" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".42"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".4" stop-color="#ffb347" stop-opacity=".4"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="stain"><stop offset="0" stop-color="${c.gold}" stop-opacity=".16"/><stop offset="1" stop-color="${c.gold}" stop-opacity="0"/></radialGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="4"/><feColorMatrix values="${c.grain}"/></filter>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string, frame = true): string {
  const side = frame ? `<path d="M.5 0V${h}M${w - 0.5} 0V${h}" stroke="${c.line}"/>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${SERIF}">
${STYLE}${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>
<ellipse cx="${w * 0.2}" cy="${h * 0.3}" rx="${w * 0.3}" ry="${h * 0.5}" fill="url(#stain)"/><ellipse cx="${w * 0.85}" cy="${h * 0.8}" rx="${w * 0.25}" ry="${h * 0.5}" fill="url(#stain)"/>
<rect width="${w}" height="${h}" filter="url(#grain)"/>${body}${side}</svg>`;
}

function petals(c: ThemeColors, n: number, xr: [number, number]): string {
  const o: string[] = [];
  const [xMin, xMax] = xr;
  for (let i = 0; i < n; i++) {
    const x = xMin + ((i * 73) % (xMax - xMin));
    const s = 0.7 + ((i * 17) % 50) / 100;
    const col = c.petals[i % c.petals.length];
    const d = 16 + (i * 3) % 12;
    const sd = 3.5 + (i * 2) % 3;
    o.push(`<g transform="translate(${f1(x)} 0)"><g class="fall" style="animation-duration:${d}s;animation-delay:-${i * 2}s">
<g class="sway" style="animation-duration:${sd}s;animation-delay:-${i * 1.5}s">
<path transform="rotate(${(i * 45) % 180}) scale(${s.toFixed(2)})" d="M0 -8C6 -6 7 4 0 9C-7 4 -6 -6 0 -8Z" fill="${col}" opacity=".9"/></g></g></g>`);
  }
  return o.join("");
}

function sparks(n: number, centers: [number, number][]): string {
  const o: string[] = [];
  for (let i = 0; i < n; i++) {
    const [cx, cy] = centers[i % centers.length];
    const x = cx + ((i * 11) % 24) - 12;
    const y = cy + ((i * 17) % 20) - 10;
    const d = 6 + (i % 6);
    o.push(`<g class="ff" style="animation-duration:${d}s;animation-delay:-${i * 1.3}s"><circle cx="${f1(x)}" cy="${f1(y)}" r="4.5" fill="#ffd57a" opacity=".25"/><circle cx="${f1(x)}" cy="${f1(y)}" r="1.7" fill="#fff0b8"/></g>`);
  }
  return o.join("");
}

function heading(c: ThemeColors, y: number, numeral: string, label: string, x = 60): string {
  return `<text x="${x}" y="${y + 5}" font-size="20" fill="${c.verm}">¶</text>
<text x="${x + 22}" y="${y + 4}" font-size="10.5" font-family="${MONO}" letter-spacing="2" fill="${c.verm}">CAPUT ${numeral}</text>
<text x="${x + 102}" y="${y + 5}" font-size="15" font-weight="700" letter-spacing="3" fill="${c.fg}">${escapeXml(label)}</text>
<path d="M${x} ${y + 16}H${x + 300}" stroke="url(#gold)" stroke-width="1.6"/>${quatrefoil(x + 306, y + 16, 3.2, c)}`;
}

function dropcap(c: ThemeColors, x: number, y: number, s: number, letter: string, fs: number): string {
  return `<rect x="${x}" y="${y}" width="${s}" height="${s}" fill="url(#gold)" stroke="${c.ink}" stroke-width="1.2"/>
<rect x="${x + s * 0.09}" y="${y + s * 0.09}" width="${s * 0.82}" height="${s * 0.82}" fill="${c.blue}" stroke="${c.ink}" stroke-width=".8"/>
<path d="M${x + s * 0.09} ${y + s * 0.09}l${s * 0.18} ${s * 0.18}M${x + s * 0.91} ${y + s * 0.09}l-${s * 0.18} ${s * 0.18}M${x + s * 0.09} ${y + s * 0.91}l${s * 0.18} -${s * 0.18}M${x + s * 0.91} ${y + s * 0.91}l-${s * 0.18} -${s * 0.18}" stroke="${c.gold}" stroke-opacity=".8"/>
<text x="${x + s / 2}" y="${y + s * 0.74}" font-size="${fs}" font-weight="700" text-anchor="middle" fill="${c.cream}" stroke="${c.ink}" stroke-width=".6">${escapeXml(letter)}</text>`;
}

const S = 0.4312;
function mp(x: number, y: number): [number, number] {
  return [560 + x * S - 8.7, 40 + (y - 22) * S];
}

function hero(c: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const arch = "M560 150A150 110 0 0 1 860 150V460H560Z";
  let b = "";
  // Frame + corner ornaments
  b += `<rect x="10" y="10" width="880" height="480" fill="none" stroke="url(#gold)" stroke-width="3"/>
<rect x="17" y="17" width="866" height="466" fill="none" stroke="${c.blue2}" stroke-width="1"/>`;

  [[10, 10], [890, 10], [10, 490], [890, 490]].forEach(([x, y]) => {
    b += quatrefoil(x, y, 7, c);
  });
  [[450, 10], [450, 490]].forEach(([x, y]) => {
    b += quatrefoil(x, y, 4.5, c);
  });

  // Top bar + avatar
  b += `<defs><clipPath id="av"><circle cx="64" cy="52" r="14"/></clipPath></defs>
<image x="50" y="38" width="28" height="28" clip-path="url(#av)" href="${avatarImg}" xlink:href="${avatarImg}"/>
<circle cx="64" cy="52" r="14" fill="none" stroke="url(#gold)" stroke-width="2"/>
<text x="88" y="56" font-size="12" font-family="${MONO}" fill="${c.mute}">${escapeXml(content.handle)} <tspan fill="${c.verm}">/</tspan> README</text>`;

  const init = content.name.charAt(0) || "S";
  const rest = content.name.slice(1);

  b += `<text x="58" y="112" font-size="14" letter-spacing="3" fill="${c.verm}">¶ <tspan fill="${c.mute}">HI, I'M</tspan></text>
${dropcap(c, 58, 124, 72, init, 58)}
<text x="140" y="168" font-size="38" fill="${c.fg}">${escapeXml(rest)}</text>
<text x="60" y="232" font-size="15" font-weight="700" letter-spacing="4" fill="${c.gold}">${escapeXml(content.role.toUpperCase())}</text>
<text x="60" y="268" font-size="14" letter-spacing="1.5" fill="${c.fg}" xml:space="preserve">${escapeXml(content.pillars)}</text>
<path d="M60 286H280" stroke="url(#gold)" stroke-width="1.6"/>${quatrefoil(286, 286, 3.2, c)}`;

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${318 + i * 22}" font-size="14" font-style="italic" fill="${c.mute}">${escapeXml(t)}</text>`;
  });

  // Miniature arch with illumination & shimmer
  b += `<defs><clipPath id="arch"><path d="${arch}"/></clipPath></defs>
<g clip-path="url(#arch)"><image x="560" y="40" width="300" height="420" preserveAspectRatio="xMidYMid slice" href="${heroImg}" xlink:href="${heroImg}"/>`;

  const [mx, my] = mp(198, 160);
  const [lx, ly] = mp(250, 640);
  const [bx, by] = mp(195, 905);
  const [tx, ty] = mp(650, 310);
  const [ex, ey] = mp(425, 258);

  b += `<circle class="glow" cx="${f1(mx)}" cy="${f1(my)}" r="54" fill="url(#warm)"/>
<circle class="flick" cx="${f1(lx)}" cy="${f1(ly)}" r="34" fill="url(#warm)"/>
<circle class="flick" cx="${f1(bx)}" cy="${f1(by)}" r="30" fill="url(#warm)" style="animation-delay:-1.2s"/>
<circle class="flick" cx="${f1(tx)}" cy="${f1(ty)}" r="30" fill="url(#warm)" style="animation-delay:-2s"/>
${star4(ex, ey, 6, "#fff3b0", 1, "tw", 1)}
<g class="sweep"><rect x="470" y="10" width="70" height="520" fill="url(#shim)" transform="rotate(16 560 250)"/></g></g>
<path d="${arch}" fill="none" stroke="${c.ink}" stroke-width="9"/><path d="${arch}" fill="none" stroke="url(#gold)" stroke-width="6"/>
<path d="${arch}" fill="none" stroke="${c.blue2}" stroke-width="1.2"/>`;

  b += quatrefoil(710, 36, 5, c) + vine(c, 40, 860, 474, 3, 3);
  b += sparks(10, [[lx, ly], [bx, by], [tx, ty], [mx + 20, my + 30]]) + petals(c, 12, [300, 880]);

  return wrap(900, 500, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const b = `<rect x=".75" y=".75" width="${w - 1.5}" height="38.5" rx="3" fill="${c.card}" stroke="url(#gold)" stroke-width="2"/>
<rect x="4" y="4" width="${w - 8}" height="32" rx="1.5" fill="none" stroke="${c.blue2}" stroke-opacity=".7"/>
${quatrefoil(22, 20, 3.4, c)}
<text x="38" y="24.5" font-size="12" letter-spacing="2" fill="${c.fg}">${escapeXml(label.toUpperCase())}</text>`;

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${SERIF}"><defs><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8a6212"/><stop offset=".3" stop-color="#f3dc84"/><stop offset=".55" stop-color="#c79a2e"/><stop offset=".8" stop-color="#f7e9a8"/><stop offset="1" stop-color="#9a7218"/></linearGradient></defs>${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = heading(c, 42, "I", "ABOUT");
  b += dropcap(c, 60, 78, 36, "I", 30);

  const words = content.about.join(" ").split(" ");
  const lines: string[] = [];
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

  lines.slice(0, 6).forEach((line, i) => {
    const x = i < 2 ? 106 : 60;
    const y = i === 0 ? 92 : i === 1 ? 112 : 136 + (i - 2) * 20;
    b += `<text x="${x}" y="${y}" font-size="14" fill="${c.fg}">${escapeXml(line)}</text>`;
  });

  b += `<path d="M450 76V236" stroke="url(#gold)" stroke-width="1.3"/>${quatrefoil(450, 76, 3, c)}${quatrefoil(450, 236, 3, c)}`;
  b += heading(c, 42, "II", "MY JOURNEY", 480);

  content.journey.slice(0, 5).forEach((j, i) => {
    const y = 98 + i * 30;
    b += `${quatrefoil(490, y - 4, 2.6, c)}
<text x="506" y="${y}" font-size="14" fill="${c.fg}">${escapeXml(j.lang)}</text>
<path d="M600 ${y}H690" stroke="${c.gold}" stroke-width="1.6" stroke-dasharray="1 5" stroke-linecap="round"/>
<text x="700" y="${y}" font-size="14" font-style="italic" fill="${c.mute}">${escapeXml(j.area)}</text>`;
  });

  b += vine(c, 40, 860, 276, 5, 3);
  return wrap(900, 296, c, b);
}

function octagon(cx: number, cy: number, R: number, rot = 22.5): string {
  const pts: [number, number][] = [];
  for (let i = 0; i < 8; i++) {
    const rad = (Math.PI / 180) * (rot + 45 * i);
    pts.push([cx + R * Math.cos(rad), cy + R * Math.sin(rad)]);
  }
  return "M" + pts.map(([x, y]) => `${f1(x)} ${f1(y)}`).join("L") + "Z";
}

function skills(c: ThemeColors, content: Content): string {
  let b = heading(c, 40, "III", "TECHNOLOGIES &amp; SKILLS");
  const bx = 40, by = 64, bw = 820, bh = 232;

  b += `<defs><pattern id="lat" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0H34M0 0V34" stroke="${c.gold}" stroke-opacity=".22"/></pattern></defs>
<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" fill="${c.blue}" stroke="url(#gold)" stroke-width="3"/>
<rect x="${bx}" y="${by}" width="${bw}" height="${bh}" fill="url(#lat)"/>
<rect x="${bx + 6}" y="${by + 6}" width="${bw - 12}" height="${bh - 12}" fill="none" stroke="${c.gold}" stroke-opacity=".5"/>`;

  content.skills.slice(0, 12).forEach((s, i) => {
    const cx = bx + 68.3 + (i % 6) * 136.7;
    const cy = by + 56 + Math.floor(i / 6) * 104;
    b += `<path d="${octagon(cx, cy, 42)}" fill="url(#gold)" stroke="${c.ink}" stroke-width="1.6"/>
<path d="${octagon(cx, cy, 34)}" fill="none" stroke="${c.ink}" stroke-opacity=".55"/>
<g class="spin${i % 2 !== 0 ? " r" : ""}"><path d="${spiral(cx, cy, 25, 2.2, i)}" fill="none" stroke="${c.ink}" stroke-opacity=".28" stroke-width="1.3"/></g>
<text x="${f1(cx)}" y="${cy + 6}" font-size="17" font-weight="700" text-anchor="middle" fill="${c.ink}">${escapeXml(s.mono)}</text>
<text x="${f1(cx)}" y="${cy + 60}" font-size="11.5" font-style="italic" text-anchor="middle" fill="${c.cream}">${escapeXml(s.label)}</text>
${star4(cx + 30, cy - 30, 4, "#fff3b0", 0.9, "tw", i * 0.9)}`;
  });

  b += vine(c, 40, 860, 318, 6, 3);
  return wrap(900, 338, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 60, c, heading(c, 32, "IV", "SELECTED PROJECTS"));
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
  const w = 208, h = 206;
  let b = `<rect x="1.5" y="1.5" width="${w - 3}" height="${h - 3}" fill="${c.card}" stroke="url(#gold)" stroke-width="3"/>
<rect x="6" y="6" width="${w - 12}" height="${h - 12}" fill="none" stroke="${c.blue2}" stroke-opacity=".8"/>
<image x="12" y="12" width="184" height="86" preserveAspectRatio="xMidYMid slice" href="${cardImg}" xlink:href="${cardImg}"/>
<rect x="12" y="12" width="184" height="86" fill="none" stroke="${c.ink}" stroke-width="1.4"/>
<rect x="12" y="12" width="26" height="18" fill="${c.verm}"/><text x="25" y="25" font-size="10.5" font-weight="700" text-anchor="middle" fill="${c.cream}">${ROMAN[idx] || idx + 1}</text>
<g clip-path="url(#sc${idx})"><g class="sweep" style="animation-duration:${10 + idx}s"><rect x="-40" y="0" width="30" height="110" fill="url(#shim)" transform="rotate(16 0 50)"/></g></g>
<defs><clipPath id="sc${idx}"><rect x="12" y="12" width="184" height="86"/></clipPath></defs>
<text x="16" y="123" font-size="15" font-weight="700" fill="${c.fg}">${escapeXml(title)}</text>
<text x="16" y="142" font-size="11.5" font-style="italic" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="157" font-size="11.5" font-style="italic" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let x = 16;
  tags.slice(0, 3).forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${f1(x)}" y="170" width="${f1(cw)}" height="17" rx="2" fill="none" stroke="${c.gold}"/>
<text x="${f1(x + cw / 2)}" y="181.5" font-size="8.5" font-family="${MONO}" text-anchor="middle" fill="${c.gold}">${escapeXml(t)}</text>`;
    x += cw + 5;
  });

  [[1.5, 1.5], [w - 1.5, 1.5], [1.5, h - 1.5], [w - 1.5, h - 1.5]].forEach(([qx, qy]) => {
    b += quatrefoil(qx, qy, 3, c);
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${SERIF}">${STYLE}${defs(c)}${b}</svg>`;
}

function cat(c: ThemeColors, x: number, y: number): string {
  const col = c.bg1 === "#f7edcc" ? "#0b0a10" : "#05060d";
  return `<g transform="translate(${x} ${y})"><g class="tail"><path d="M82 96C108 94 112 66 98 56" fill="none" stroke="${col}" stroke-width="7" stroke-linecap="round"/></g>
<path d="M30 100C22 80 26 62 36 52C34 44 36 38 40 34L36 12L48 22C52 21 56 21 60 22L72 10L72 34C76 40 78 46 76 52C90 62 94 84 88 100Z" fill="${col}"/>
<ellipse cx="46" cy="34" rx="3.6" ry="2.4" fill="#f2c64a"/>${star4(46, 34, 5, "#fff3b0", 0.9, "tw", 2)}</g>`;
}

function lantern(c: ThemeColors, x: number, y0: number, ln: number, delay = 0): string {
  const y = y0 + ln;
  return `<g class="swing" style="animation-delay:-${delay}s"><path d="M${x} ${y0}V${y - 14}" stroke="${c.gold}" stroke-width="1.2"/>
<circle class="flick" cx="${x}" cy="${y + 4}" r="34" fill="url(#warm)" style="animation-delay:-${delay}s"/>
<rect x="${x - 7}" y="${y - 14}" width="14" height="4" fill="${c.ink}"/><path d="M${x - 10} ${y - 10}H${x + 10}L${x + 12} ${y + 14}H${x - 12}Z" fill="${c.orange}" stroke="${c.ink}" stroke-width="1.2"/>
<path d="M${x - 10} ${y + 2}H${x + 10}" stroke="${c.ink}" stroke-opacity=".5"/><rect x="${x - 9}" y="${y + 14}" width="18" height="4" fill="${c.ink}"/></g>`;
}

function footer(c: ThemeColors, content: Content): string {
  let b = `<text x="60" y="78" font-size="11" font-family="${MONO}" letter-spacing="4" fill="${c.verm}">EXPLICIT LIBER</text>
<text x="60" y="118" font-size="20" font-weight="700" letter-spacing="3" fill="${c.fg}" xml:space="preserve">${escapeXml(content.footer.line1.toUpperCase())}</text>
<path d="M60 134H470" stroke="url(#gold)" stroke-width="1.6"/>${quatrefoil(476, 134, 3.2, c)}
<text x="60" y="160" font-size="13" font-style="italic" fill="${c.mute}">${escapeXml(content.footer.line2)}</text>`;

  // Moon
  b += `<circle class="glow" cx="640" cy="64" r="58" fill="url(#warm)"/><circle cx="640" cy="64" r="36" fill="${c.orange}" stroke="${c.ink}" stroke-width="1.6"/>
<g class="spin"><path d="${spiral(640, 64, 26, 2.6)}" fill="none" stroke="#fff3c4" stroke-width="2.4" stroke-linecap="round"/></g>`;

  // Pagoda roof
  const roof = "M560 138C560 124 574 112 590 104C582 122 600 134 632 138L870 138V156H632C600 154 570 148 560 138Z";
  let eaves = "";
  for (let x = 640; x < 870; x += 14) {
    eaves += `<path d="M${x} 140V154" stroke="${c.ink}" stroke-opacity=".5"/>`;
  }
  b += `<path d="${roof}" fill="${c.blue}" stroke="${c.ink}" stroke-width="1.6"/>${eaves}<path d="M632 138H870" stroke="url(#gold)" stroke-width="2.4"/>`;
  b += cat(c, 758, 38);

  const lanterns: [number, number][] = [[650, 28], [700, 52], [760, 34], [810, 60], [850, 36]];
  lanterns.forEach(([x, ln], i) => {
    b += lantern(c, x, 156, ln, i * 0.7);
  });

  b += vine(c, 40, 540, 214, 7, 3) + sparks(10, [[650, 190], [760, 200], [850, 195], [700, 215]]) + petals(c, 6, [40, 560]);
  return wrap(900, 240, c, b);
}

export const codexStyle: StyleModule = {
  id: "codex",
  name: "Codex",
  keywords: ["illuminated-manuscript", "gold-leaf", "medieval", "vellum"],
  palette: {
    light: ["#f7edcc", "#2a2118", "#b3841c", "#1d3f94", "#c4321f"],
    dark: ["#0f1c47", "#f4e9c9", "#e8c45a", "#4a74e0", "#e5583e"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/codex/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 22, 736, 996], [620, 820], 0.92);
    const avatarCrop = ctx.cropToDataUrl(img, [390, 200, 490, 300], [64, 64], 0.92);

    const cropBoxes: [number, number, number, number][] = [
      [98, 115, 298, 209],
      [500, 440, 700, 534],
      [350, 200, 550, 294],
      [200, 360, 400, 454],
      [50, 670, 250, 764],
      [130, 840, 330, 934],
      [420, 560, 620, 654],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 188], 0.9)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop, avatarCrop);
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
            `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `${p.title}: ${p.line1}`, "24%")}</a>`
        )
        .join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name} — ${content.role}. Illuminated Codex miniature with gold frame.`, "100%"),
      `<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Explicit liber. Build, Explore, Understand", "100%"),
    ].filter(Boolean);

    const readme = `<div align="center">\n\n${readmeParts.join("\n\n")}\n\n</div>\n`;

    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += new Blob([str]).size));

    return { files, readme, meta: { bytes } };
  },
};

