import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";

interface ThemeColors {
  bg: string;
  panel: string;
  ink: string;
  mut: string;
  trunk: string;
  trunk2: string;
  swirl: string;
  swirl2: string;
  gold: string;
  goldtx: string;
  coral: string;
  cream: string;
  magic: string;
  rib: string;
  ribtx: string;
  chip: string;
  sky: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#0b1030", panel: "#141d4d", ink: "#eef0fa", mut: "#aab5df",
    trunk: "#24347e", trunk2: "#3d4fa8", swirl: "#34507f", swirl2: "#86a8c4",
    gold: "#f0c25a", goldtx: "#f0c25a", coral: "#ee7f5f", cream: "#f4e6bb",
    magic: "#8fd3ff", rib: "#24347e", ribtx: "#f9efcf", chip: "#1c2a66", sky: "#1a2a63"
  },
  light: {
    bg: "#efe5ca", panel: "#f8f1de", ink: "#1b2457", mut: "#4c5686",
    trunk: "#2b3f8c", trunk2: "#4a5fb0", swirl: "#8fb0c4", swirl2: "#4f7896",
    gold: "#b3822a", goldtx: "#7d5a12", coral: "#d9583a", cream: "#fff6d8",
    magic: "#2b6fb0", rib: "#2b3f8c", ribtx: "#fff6d8", chip: "#e8dcb8", sky: "#c6d3d8"
  }
};

const CSS = `.a{transform-box:fill-box;transform-origin:center}
.spin{animation:spin 80s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.spinr{animation:spin 110s linear infinite reverse}
.swim{animation:swim 18s ease-in-out infinite alternate}
@keyframes swim{from{transform:translateX(0)}to{transform:translateX(34px)}}
.flag{transform-origin:left center;animation:flag 3.2s ease-in-out infinite alternate}
@keyframes flag{from{transform:skewY(-6deg) scaleX(1)}to{transform:skewY(6deg) scaleX(.9)}}
.rise{animation:rise 9s ease-in infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.95}100%{transform:translateY(-70px);opacity:0}}
.pulse{animation:pulse 6s ease-in-out infinite alternate}
@keyframes pulse{from{opacity:.55}to{opacity:1}}
.kb{animation:kb 24s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
.dash{animation:dash 7s linear infinite}
@keyframes dash{to{stroke-dashoffset:-60}}
.shim{animation:shim 9s ease-in-out infinite}
@keyframes shim{0%,55%{transform:translateX(-120px)}100%{transform:translateX(420px)}}
.tw{animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion: reduce){.spin,.spinr,.swim,.flag,.rise,.pulse,.kb,.dash,.shim,.tw{animation:none}}`;

const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];

function root(w: number, h: number, T: ThemeColors, title: string, body: string, extraDefs = ""): string {
  const d = `<defs>`
    + `<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${T.magic}" stop-opacity=".42"/><stop offset="1" stop-color="${T.magic}" stop-opacity="0"/></radialGradient>`
    + `<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${T.gold}" stop-opacity="0"/><stop offset=".5" stop-color="${T.gold}" stop-opacity=".38"/><stop offset="1" stop-color="${T.gold}" stop-opacity="0"/></linearGradient>`
    + `<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="5"/><feColorMatrix values="0 0 0 0 .4  0 0 0 0 .4  0 0 0 0 .5  0 0 0 .5 -.16"/></filter>`
    + `${extraDefs}</defs>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${escapeXml(title)}"><title>${escapeXml(title)}</title><style>${CSS}</style>${d}${body}<rect class="grain" width="${w}" height="${h}" fill="#000" opacity=".5" filter="url(#noise)"/></svg>`;
}

function scallop(r: number, bumps = 18, amp = 0.05, ph = 0.0): string {
  const pts: string[] = [];
  const n = bumps * 6;
  for (let k = 0; k < n; k++) {
    const a = (2 * Math.PI * k) / n;
    const rr = r * (1 + amp * Math.sin(bumps * a + ph));
    pts.push(`${f1(rr * Math.cos(a))},${f1(rr * Math.sin(a))}`);
  }
  return "M" + pts.join(" L") + "Z";
}

function swirl(r: number, T: ThemeColors, seed: number, rings = 5, base = true, bumps = 16): string {
  const rng = createRng(seed);
  const ph = rng() * 6;
  const out: string[] = [];
  if (base) {
    out.push(`<path d="${scallop(r, bumps, 0.05, ph)}" fill="${T.swirl}" stroke="${T.swirl2}" stroke-width="1.2"/>`);
  }
  for (let k = 1; k < rings; k++) {
    const rr = r * (1 - (k / rings) * 0.92);
    out.push(`<path d="${scallop(rr, bumps, 0.05, ph + k)}" fill="none" stroke="${T.swirl2}" stroke-width="1.1" opacity=".9"/>`);
  }
  return out.join("");
}

function bushRow(T: ThemeColors, x0: number, x1: number, y: number, seed: number, r = 34, step = 46, op = 1): string {
  const rng = createRng(seed);
  const out: string[] = [];
  let x = x0;
  while (x < x1) {
    out.push(`<g transform="translate(${f1(x)},${f1(y + (rng() - 0.5) * 16)})">${swirl(r * (0.8 + rng() * 0.4), T, Math.floor(rng() * 1000), 4)}</g>`);
    x += step * (0.8 + rng() * 0.3);
  }
  return `<g opacity="${op}">${out.join("")}</g>`;
}

function trunk(x: number, y: number, w: number, h: number, T: ThemeColors, seed: number): string {
  const rng = createRng(seed);
  const g: string[] = [`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${T.trunk}"/>`];
  const numLines = Math.max(3, Math.floor(w / 7));
  const segs: string[] = [];
  for (let i = 0; i < numLines; i++) {
    segs.push(`M${f1(x + w * (0.1 + rng() * 0.8))},${y}v${h}`);
  }
  g.push(`<path d="${segs.join("")}" stroke="${T.trunk2}" stroke-width="1.2" opacity=".7" fill="none"/>`);
  const numKnots = Math.max(1, Math.floor(h / 220));
  for (let i = 0; i < numKnots; i++) {
    const kx = x + w * (0.3 + rng() * 0.4);
    const ky = y + h * (0.1 + rng() * 0.8);
    g.push(`<ellipse cx="${f1(kx)}" cy="${f1(ky)}" rx="${f1(w * 0.12)}" ry="${f1(w * 0.2)}" fill="none" stroke="${T.trunk2}" stroke-width="1.4"/>`);
  }
  return g.join("");
}

function castle(T: ThemeColors, x: number, y: number, s = 1.0, dark = false): string {
  const win = dark ? T.gold : T.trunk;
  const wins = [
    [-22, -26], [-8, -30], [8, -24], [-30, -10], [20, -8]
  ].map(([wx, wy], i) => `<rect class="tw" style="animation-delay:-${i * 1.1}s" x="${wx}" y="${wy}" width="4" height="7" rx="1.5" fill="${win}"/>`).join("");

  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">`
    + `<path d="M-62,6C-50,-6 -30,-2 -10,4C10,10 30,0 62,6L52,40H-52Z" fill="${T.cream}" opacity=".55"/>`
    + `<rect x="-34" y="-34" width="52" height="38" fill="${T.cream}" stroke="${T.trunk}" stroke-width="1"/>`
    + `<path d="M-40,-34L-8,-62L24,-34Z" fill="${T.coral}" stroke="${T.trunk}" stroke-width="1"/>`
    + `<rect x="-52" y="-52" width="16" height="56" fill="${T.cream}" stroke="${T.trunk}" stroke-width="1"/>`
    + `<path d="M-56,-52L-44,-84L-32,-52Z" fill="${T.coral}" stroke="${T.trunk}" stroke-width="1"/>`
    + `<rect x="18" y="-44" width="14" height="48" fill="${T.cream}" stroke="${T.trunk}" stroke-width="1"/>`
    + `<path d="M15,-44L25,-72L35,-44Z" fill="${T.coral}" stroke="${T.trunk}" stroke-width="1"/>`
    + `<path d="M-44,-84V-96" stroke="${T.trunk}" stroke-width="1.2"/>`
    + `<path class="flag" d="M-44,-96L-30,-92L-44,-88Z" fill="${T.coral}"/>${wins}</g>`;
}

function rider(T: ThemeColors, x: number, y: number, s = 1.0, cloak = "coral", hat = true, delay = 0): string {
  const body = cloak === "coral" ? T.coral : (cloak === "cream" ? T.cream : T.gold);
  const hatSvg = hat ? `<path d="M-3,-45L3,-64L8,-45Z" fill="${T.coral}"/>` : "";
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})"><g class="a swim" style="animation-delay:${delay}s">`
    + `<path d="M-24,-2C-24,-14 -4,-16 14,-12C20,-18 24,-26 32,-26L36,-20C32,-18 30,-12 24,-4C20,6 12,8 -24,-2Z" fill="${T.trunk}" stroke="${T.gold}" stroke-width=".8"/>`
    + `<path d="M-18,4V22M-6,6V22M10,4V22M18,2V22" stroke="${T.trunk}" stroke-width="3" stroke-linecap="round"/>`
    + `<path d="M-24,-4C-34,-2 -36,8 -34,14" stroke="${T.trunk}" stroke-width="2.4" fill="none"/>`
    + `<path d="M-6,-12C-14,-30 -4,-40 6,-34C12,-30 12,-16 10,-10Z" fill="${body}" stroke="${T.gold}" stroke-width=".8"/>`
    + `<circle cx="2" cy="-42" r="5" fill="${T.cream}" stroke="${T.trunk}" stroke-width=".8"/>`
    + hatSvg
    + `<path d="M12,-30L40,-58" stroke="${T.gold}" stroke-width="1.4"/><path d="M40,-58l8,3l-6,4Z" fill="${T.cream}"/></g></g>`;
}

function corner(T: ThemeColors, x: number, y: number, sx: number, sy: number): string {
  return `<g transform="translate(${x},{y}) scale(${sx},${sy})" fill="none" stroke="${T.gold}" stroke-width="1.2">`
    + `<path d="M6,6C26,6 30,18 20,24C12,28 8,20 14,16"/><path d="M6,6C6,26 18,30 24,20C28,12 20,8 16,14"/>`
    + `<circle cx="6" cy="6" r="2.2" fill="${T.gold}"/></g>`;
}

function window(T: ThemeColors, x: number, y: number, w: number, h: number, n = 14): string {
  const g = T.gold;
  const d = `M${x + n},${y}H${x + w - n}L${x + w},${y + n}V${y + h - n}L${x + w - n},${y + h}H${x + n}L${x},${y + h - n}V${y + n}Z`;
  const i = 6;
  const d2 = `M${x + n + i},${y + i}H${x + w - n - i}L${x + w - i},${y + n + i}V${y + h - n - i}L${x + w - n - i},${y + h - i}H${x + n + i}L${x + i},${y + h - n - i}V${y + n + i}Z`;
  return `<path d="${d}" fill="${T.panel}" stroke="${g}" stroke-width="1.8"/>`
    + `<path d="${d2}" fill="none" stroke="${g}" stroke-width=".8" opacity=".6"/>`
    + corner(T, x + 10, y + 10, 1, 1) + corner(T, x + w - 10, y + 10, -1, 1)
    + corner(T, x + 10, y + h - 10, 1, -1) + corner(T, x + w - 10, y + h - 10, -1, -1);
}

function star4(T: ThemeColors, x: number, y: number, s = 6, col?: string): string {
  const c = col || T.gold;
  return `<path transform="translate(${f1(x)},${f1(y)}) scale(${s / 6})" d="M0,-8L2,-2L8,0L2,2L0,8L-2,2L-8,0L-2,-2Z" fill="${c}"/>`;
}

function label(T: ThemeColors, x: number, y: number, num: string, text: string): string {
  return `${star4(T, x + 6, y - 5, 7)}`
    + `<text x="${x + 20}" y="${y}" font-family="${MONO}" font-size="12.5" letter-spacing="3" fill="${T.goldtx}" font-weight="700">${num}  \u00b7  ${escapeXml(text)}</text>`;
}

function fireflies(T: ThemeColors, pts: [number, number][], seed = 1): string {
  const rng = createRng(seed);
  return pts.map(([x, y]) =>
    `<circle class="a rise" cx="${x}" cy="${y}" r="${f1(1.4 + rng() * 1.2)}" fill="${T.gold}" style="animation-delay:-${f1(rng() * 9)}s;animation-duration:${f1(7 + rng() * 5)}s"/>`
  ).join("");
}

function divider(T: ThemeColors, x0: number, x1: number, y: number, delay = 0): string {
  const pts: string[] = [];
  for (let x = Math.floor(x0); x <= Math.floor(x1); x += 10) {
    pts.push(`${x},${f1(y + 2.4 * Math.sin(x / 34))}`);
  }
  const nodes: string[] = [];
  for (let x = Math.floor(x0) + 90; x < Math.floor(x1); x += 180) {
    nodes.push(star4(T, x, y + 2.4 * Math.sin(x / 34), 5));
  }
  const p = "M" + pts.join(" L");
  return `<path d="${p}" fill="none" stroke="${T.gold}" stroke-width="1" opacity=".75"/>`
    + `<path d="${p}" fill="none" stroke="${T.cream}" stroke-width="2" stroke-linecap="round" stroke-dasharray="1 14" class="dash" style="animation-delay:${delay}s" opacity=".85"/>${nodes.join("")}`;
}

function magicCircle(T: ThemeColors, cx: number, cy: number, r: number, seed = 3): string {
  const rng = createRng(seed);
  const runes: string[] = [];
  const n = 28;
  for (let i = 0; i < n; i++) {
    const a = (2 * Math.PI * i) / n;
    const rr = r * 0.9;
    const px = cx + rr * Math.cos(a);
    const py = cy + rr * Math.sin(a);
    const deg = (a * 180) / Math.PI + 90;
    const segs = Array.from({ length: 3 }, () => `M${f1((rng() - 0.5) * 6)},${f1((rng() - 0.5) * 8)}l${f1((rng() - 0.5) * 6)},${f1((rng() - 0.5) * 8)}`).join("");
    runes.push(`<path transform="translate(${f1(px)},${f1(py)}) rotate(${f1(deg)})" d="${segs}" stroke="${T.magic}" stroke-width="1.3" fill="none" stroke-linecap="round"/>`);
  }
  const starPts: [number, number][] = [];
  for (let i = 0; i < 8; i++) {
    const a = (2 * Math.PI * i * 3) / 8 - Math.PI / 2;
    starPts.push([cx + r * 0.78 * Math.cos(a), cy + r * 0.78 * Math.sin(a)]);
  }
  const star = `<path d="M` + starPts.map(([x, y]) => `${f1(x)},${f1(y)}`).join(" L") + `Z" fill="none" stroke="${T.gold}" stroke-width="1" opacity=".8"/>`;

  return `<g class="a spin" opacity=".9"><circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${T.gold}" stroke-width="1.6"/>`
    + `<circle cx="${cx}" cy="${cy}" r="${f1(r * 0.96)}" fill="none" stroke="${T.magic}" stroke-width=".8" stroke-dasharray="2 5"/>`
    + `<circle cx="${cx}" cy="${cy}" r="${f1(r * 0.82)}" fill="none" stroke="${T.gold}" stroke-width=".8"/>`
    + `${runes.join("")}${star}</g>`
    + `<g class="a spinr" opacity=".7"><circle cx="${cx}" cy="${cy}" r="${f1(r * 0.64)}" fill="none" stroke="${T.magic}" stroke-width="1" stroke-dasharray="10 6"/>`
    + `<circle cx="${cx}" cy="${cy}" r="${f1(r * 0.58)}" fill="none" stroke="${T.gold}" stroke-width=".7"/></g>`;
}

function hero(T: ThemeColors, isDark: boolean, content: Content, heroImg: string, avatarImg: string): string {
  const cx = 710, ax = 565, ay = 70, aw = 290, ah = 390;
  const arch = (x: number, y: number, w: number, h: number) => `M${x},${y + h}V${y + w / 2}A${w / 2},${w / 2} 0 0 1 ${x + w},${y + w / 2}V${y + h}Z`;
  const b: string[] = [
    `<rect width="900" height="520" fill="${T.bg}"/>`,
    `<clipPath id="pc"><rect width="900" height="520"/></clipPath><g clip-path="url(#pc)">`
  ];
  if (isDark) {
    const rng = createRng(4);
    for (let i = 0; i < 34; i++) {
      b.push(`<circle class="tw" style="animation-delay:-${f1(rng() * 4)}s" cx="${f1(20 + rng() * 860)}" cy="${f1(10 + rng() * 290)}" r="${f1(0.8 + rng() * 1.0)}" fill="${T.cream}"/>`);
    }
  }
  b.push(`<circle class="a pulse" cx="${cx}" cy="265" r="270" fill="url(#gl)"/>`);
  b.push(trunk(0, 0, 30, 520, T, 1) + trunk(42, 0, 16, 520, T, 2) + trunk(866, 0, 34, 520, T, 3));
  b.push(magicCircle(T, cx, 265, 205));
  b.push(bushRow(T, 20, 900, 516, 8, 36, 44));
  b.push(rider(T, 80, 494, 0.85, "coral", true, 0) + rider(T, 190, 498, 0.8, "cream", true, -5) + rider(T, 300, 494, 0.85, "gold", true, -9));
  b.push(fireflies(T, [[90, 440], [260, 430], [480, 450], [520, 380], [880, 420], [600, 470]], 2));
  b.push(`</g>`);

  b.push(`<clipPath id="hc"><path d="${arch(ax + 8, ay + 8, aw - 16, ah - 16)}"/></clipPath>`
    + `<linearGradient id="vg" x1="0" y1="0" x2="0" y2="1"><stop offset=".6" stop-color="${T.bg}" stop-opacity="0"/><stop offset="1" stop-color="${T.bg}" stop-opacity=".6"/></linearGradient>`
    + `<path d="${arch(ax, ay, aw, ah)}" fill="${T.panel}" stroke="${T.gold}" stroke-width="2"/>`
    + `<path d="${arch(ax - 6, ay - 6, aw + 12, ah + 12)}" fill="none" stroke="${T.gold}" stroke-width=".8" opacity=".7"/>`
    + `<g clip-path="url(#hc)"><image class="a kb" x="${ax + 8}" y="${ay + 8}" width="${aw - 16}" height="${ah - 16}" preserveAspectRatio="xMidYMid slice" href="${heroImg}"/>`
    + `<rect x="${ax + 8}" y="${ay + 8}" width="${aw - 16}" height="${ah - 16}" fill="url(#vg)"/>`
    + `<g transform="skewX(-20)"><rect class="a shim" x="570" y="70" width="40" height="390" fill="url(#shg)"/></g></g>`
    + star4(T, cx, ay - 12, 11));

  const names = content.name.split(" ");
  const name1 = names[0] || "Solayman";
  const name2 = names.slice(1).join(" ") || "El Mouden";

  b.push(`<clipPath id="av"><circle cx="76" cy="52" r="14"/></clipPath>`
    + `<image x="62" y="38" width="28" height="28" clip-path="url(#av)" href="${avatarImg}"/>`
    + `<circle cx="76" cy="52" r="14" fill="none" stroke="${T.gold}" stroke-width="1.2"/>`
    + `<text x="100" y="56" font-family="${MONO}" font-size="12.5" fill="${T.mut}">${escapeXml(content.handle)} / README</text>`
    + `<path d="M62,78H500" stroke="${T.gold}" stroke-width=".8" stroke-dasharray="2 5" opacity=".7"/>`
    + `<text x="62" y="136" font-family="${SERIF}" font-style="italic" font-size="22" fill="${T.mut}">Hi, I'm</text>`
    + `<text x="60" y="204" font-family="${SERIF}" font-weight="700" font-size="66" fill="${T.ink}">${escapeXml(name1)}</text>`
    + `<text x="60" y="272" font-family="${SERIF}" font-weight="700" font-size="66" fill="${T.ink}">${escapeXml(name2)}</text>`
    + `<text x="62" y="312" font-family="${MONO}" font-weight="700" font-size="14" letter-spacing="5" fill="${T.goldtx}">${escapeXml(content.role.toUpperCase())}</text>`
    + `<text x="62" y="338" font-family="${MONO}" font-size="13" fill="${T.ink}">${escapeXml(content.pillars)}</text>`);

  content.tagline.forEach((ln, i) => {
    b.push(`<text x="62" y="${378 + i * 22}" font-family="${SERIF}" font-size="15" fill="${T.mut}">${escapeXml(ln)}</text>`);
  });

  return root(900, 520, T, `${content.name} - ${content.role}`, b.join(""));
}

function button(T: ThemeColors, text: string): string {
  const g = T.gold;
  const d = "M12,1H138L149,12V28L138,39H12L1,28V12Z";
  const b = `<path d="${d}" fill="${T.panel}" stroke="${g}" stroke-width="1.4"/>`
    + star4(T, 22, 20, 8)
    + `<text x="38" y="25" font-family="${MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="${T.ink}">${escapeXml(text)}</text>`;
  return root(150, 40, T, text, b);
}

function about(T: ThemeColors, content: Content): string {
  const b: string[] = [
    `<rect width="900" height="330" fill="${T.bg}"/>`,
    window(T, 20, 14, 860, 302),
    label(T, 56, 58, "I", "ABOUT"),
    label(T, 536, 58, "II", "MY JOURNEY")
  ];
  content.about.forEach((ln, i) => {
    b.push(`<text x="58" y="${106 + i * 28}" font-family="${SERIF}" font-size="15" fill="${T.ink}">${escapeXml(ln)}</text>`);
  });
  content.journey.forEach(({ lang, area }, i) => {
    const y = 108 + i * 38;
    b.push(star4(T, 540, y - 5, 6)
      + `<text x="554" y="${y}" font-family="${MONO}" font-size="14" font-weight="700" fill="${T.ink}">${escapeXml(lang)}</text>`
      + `<path d="M656,${y - 5}H708" stroke="${T.gold}" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="1 7" class="dash" style="animation-delay:-${i}s"/>`
      + `<text x="720" y="${y}" font-family="${SERIF}" font-size="15" fill="${T.ink}">${escapeXml(area)}</text>`);
  });
  b.push(divider(T, 56, 844, 288));
  b.push(fireflies(T, [[480, 280], [500, 250], [60, 270]], 5));
  return root(900, 330, T, "About and Journey", b.join(""));
}

function orb(T: ThemeColors, i: number, mono: string): string {
  const spin = i % 2 === 0 ? "spin" : "spinr";
  return `<circle r="42" fill="url(#gl)"/><g class="a ${spin}">${swirl(36, T, 70 + i, 5, true, 14)}</g>`
    + `<circle r="19" fill="${T.trunk}" stroke="${T.gold}" stroke-width="1.2"/>`
    + `<text y="5" text-anchor="middle" font-family="${MONO}" font-size="15" font-weight="700" fill="${T.ribtx}">${escapeXml(mono)}</text>`;
}

function skills(T: ThemeColors, content: Content): string {
  const b: string[] = [
    `<rect width="900" height="360" fill="${T.bg}"/>`,
    window(T, 20, 14, 860, 330),
    label(T, 56, 58, "III", "TECHNOLOGIES &amp; SKILLS"),
    divider(T, 56, 844, 80, -2)
  ];
  content.skills.slice(0, 12).forEach(({ label: name, mono }, i) => {
    const cx = 121.5 + (i % 6) * 131;
    const cy = 148 + Math.floor(i / 6) * 114;
    b.push(`<g transform="translate(${f1(cx)},${cy})">${orb(T, i, mono)}</g>`);
    b.push(`<text x="${f1(cx)}" y="${cy + 62}" text-anchor="middle" font-family="${SERIF}" font-size="12.5" fill="${T.ink}">${escapeXml(name)}</text>`);
  });
  return root(900, 360, T, "Technologies and skills", b.join(""));
}

function projectsTitle(T: ThemeColors): string {
  const g = T.gold;
  const rib = "M300,18H600L612,34L600,50H300L288,34Z";
  const b = [
    `<rect width="900" height="90" fill="${T.bg}"/>`,
    divider(T, 40, 280, 34), divider(T, 620, 860, 34, -3),
    `<path d="${rib}" fill="${T.rib}" stroke="${g}" stroke-width="1.6"/>`,
    `<text x="450" y="39" text-anchor="middle" font-family="${MONO}" font-size="13" font-weight="700" letter-spacing="3.5" fill="${T.ribtx}">IV  \u00b7  SELECTED PROJECTS</text>`,
    `<path d="M300,60V84M600,60V84" stroke="${g}" stroke-width="1.4"/>`,
    `<path class="flag" d="M300,60L324,66L300,72Z" fill="${T.coral}"/><path class="flag" d="M600,60L624,66L600,72Z" fill="${T.coral}" style="animation-delay:-1.5s"/>`
  ];
  return root(900, 90, T, "Selected projects", b.join(""));
}

function chips(T: ThemeColors, tags: string[]): string {
  const out: string[] = [];
  let x = 8, y = 178;
  for (const t of tags) {
    const w = t.length * 6.4 + 14;
    if (x + w > 200) {
      x = 8;
      y += 22;
    }
    out.push(`<rect x="${f1(x)}" y="${y}" width="${f1(w)}" height="18" rx="9" fill="${T.chip}" stroke="${T.gold}" stroke-width=".6" stroke-opacity=".7"/>`
      + `<text x="${f1(x + w / 2)}" y="${y + 12.5}" text-anchor="middle" font-family="${MONO}" font-size="10.5" fill="${T.ink}">${escapeXml(t)}</text>`);
    x += w + 5;
  }
  return out.join("");
}

function card(T: ThemeColors, i: number, title: string, desc1: string, desc2: string, tags: string[], cardImg: string): string {
  const n = 12;
  const d = `M${n},1H${208 - n}L207,${n}V${229 - n}L${208 - n},230H${n}L1,${229 - n}V${n}Z`;
  const romanNum = ROMAN[i] || String(i + 1);
  const b: string[] = [
    `<path d="${d}" fill="${T.panel}" stroke="${T.gold}" stroke-width="1.3"/>`,
    `<clipPath id="tc${i}"><rect x="8" y="8" width="192" height="92" rx="4"/></clipPath>`,
    `<g clip-path="url(#tc${i})"><image class="a kb" x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" href="${cardImg}" style="animation-delay:-${i * 3}s"/>`
    + `<g transform="skewX(-20)"><rect class="a shim" x="20" y="8" width="26" height="92" fill="url(#shg)" style="animation-delay:-${i * 1.3}s"/></g></g>`,
    `<rect x="8" y="8" width="192" height="92" rx="4" fill="none" stroke="${T.gold}" stroke-width=".8" opacity=".85"/>`,
    `<path d="M14,8H70V34L42,27L14,34Z" fill="${T.rib}" stroke="${T.gold}" stroke-width="1"/>`,
    `<text x="42" y="22" text-anchor="middle" font-family="${MONO}" font-size="10.5" font-weight="700" fill="${T.ribtx}">${romanNum}</text>`,
    `<text x="10" y="126" font-family="${SERIF}" font-weight="700" font-size="16" fill="${T.ink}">${escapeXml(title)}</text>`,
    `<text x="10" y="145" font-family="${SERIF}" font-size="11.5" fill="${T.mut}">${escapeXml(desc1)}</text>`,
    `<text x="10" y="160" font-family="${SERIF}" font-size="11.5" fill="${T.mut}">${escapeXml(desc2)}</text>`,
    chips(T, tags)
  ];
  return root(208, 230, T, `Quest ${romanNum}: ${title} project card`, b.join(""));
}

function footer(T: ThemeColors, isDark: boolean, content: Content): string {
  const brand = content.brand?.latin || "NashirTech";
  const b: string[] = [
    `<rect width="900" height="270" fill="${T.bg}"/>`,
    `<clipPath id="pc"><rect width="900" height="270"/></clipPath><g clip-path="url(#pc)">`
  ];
  if (isDark) {
    const rng = createRng(9);
    for (let i = 0; i < 26; i++) {
      b.push(`<circle class="tw" style="animation-delay:-${f1(rng() * 4)}s" cx="${f1(20 + rng() * 860)}" cy="${f1(8 + rng() * 142)}" r="${f1(0.8 + rng() * 0.9)}" fill="${T.cream}"/>`);
    }
  }
  b.push(`<circle cx="780" cy="64" r="26" fill="${isDark ? T.cream : T.gold}" opacity="${isDark ? ".9" : ".55"}"/>`);
  b.push(`<circle class="a pulse" cx="780" cy="64" r="80" fill="url(#gl)"/>`);
  b.push(trunk(0, 0, 28, 270, T, 11) + trunk(36, 0, 14, 270, T, 12) + trunk(872, 0, 28, 270, T, 13));
  b.push(bushRow(T, 60, 860, 262, 21, 34, 44));
  b.push(castle(T, 150, 214, 0.95, isDark));
  b.push(rider(T, 400, 238, 0.7, "coral", true, 0) + rider(T, 500, 240, 0.65, "cream", true, -6) + rider(T, 600, 238, 0.7, "gold", true, -10));
  b.push(fireflies(T, [[250, 200], [330, 170], [700, 190], [820, 210], [460, 200]], 7));
  b.push(`</g>`);
  b.push(`<text x="450" y="80" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="30" fill="${T.ink}">${escapeXml(content.footer.line1)}</text>`
    + `<text x="450" y="110" text-anchor="middle" font-family="${MONO}" font-size="12.5" letter-spacing="1" fill="${T.mut}">${escapeXml(content.footer.line2)}</text>`
    + divider(T, 230, 670, 134, -1)
    + `<text x="450" y="160" text-anchor="middle" font-family="${SERIF}" font-size="13" fill="${T.goldtx}">${escapeXml(brand)}</text>`);
  return root(900, 270, T, "Footer", b.join(""));
}

export const isekaiStyle: StyleModule = {
  id: "isekai",
  name: "Isekai Tale Parchment",
  keywords: ["isekai", "fantasy", "parchment", "castle", "knight", "magic"],
  palette: {
    dark: ["#0b1030", "#141d4d", "#f0c25a", "#8fd3ff", "#ee7f5f"],
    light: ["#efe5ca", "#f8f1de", "#b3822a", "#2b6fb0", "#d9583a"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/isekai/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [170, 10, 560, 542], [516, 704], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [300, 230, 440, 370], [64, 64], 0.9);

    const cropBoxes: [number, number, number, number][] = [
      [320, 200, 380, 520],
      [450, 180, 270, 410],
      [280, 420, 180, 320],
      [450, 370, 240, 380],
      [200, 200, 260, 400],
      [240, 60, 320, 460],
      [560, 300, 220, 360],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 190], 0.85)
    );

    const files: Record<string, string> = {};

    for (const theme of ["dark", "light"] as const) {
      const T = THEMES[theme];
      const isDark = theme === "dark";
      files[`hero-${theme}.svg`] = hero(T, isDark, content, heroCrop, avatarCrop);
      files[`btn-github-${theme}.svg`] = button(T, "GITHUB");
      files[`btn-linkedin-${theme}.svg`] = button(T, "LINKEDIN");
      files[`btn-portfolio-${theme}.svg`] = button(T, "PORTFOLIO");
      files[`about-${theme}.svg`] = about(T, content);
      files[`skills-${theme}.svg`] = skills(T, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(T);
      files[`footer-${theme}.svg`] = footer(T, isDark, content);

      content.projects.forEach((proj, i) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(T, i, proj.title, proj.line1, proj.line2, proj.tags, cardCrops[i]);
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items.map((p, i) => `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `Quest ${ROMAN[i] || i + 1}, ${p.title}: ${p.line1} ${p.line2}`, "24%")}</a>`).join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name}, ${content.role}. A castle seen through a magic portal in a storybook forest.`, "100%"),
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
export default isekaiStyle;
