import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";

interface ThemeColors {
  bg: string;
  panel: string;
  panel2: string;
  ink: string;
  mut: string;
  ecto: string;
  ectotx: string;
  ecto2: string;
  violet: string;
  gold: string;
  line: string;
  hatch: string;
  spines: string[];
  gh_top: string;
  gh_bot: string;
  gh_fill: string;
  gh_line: string;
  eye: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#05090c", panel: "#0b1519", panel2: "#101e24", ink: "#e6f1ee", mut: "#9db5b0",
    ecto: "#8ff0d0", ectotx: "#8ff0d0", ecto2: "#3f9d8d", violet: "#a79bff", gold: "#ffd27a",
    line: "#2a4048", hatch: "#8ff0d0",
    spines: ["#16282e", "#1b3037", "#241f3d", "#173a34", "#2a2230", "#1c2c3a"],
    gh_top: ".55", gh_bot: ".1", gh_fill: "#8ff0d0", gh_line: "#8ff0d0", eye: "#05090c"
  },
  light: {
    bg: "#efece1", panel: "#f8f6ee", panel2: "#e7e3d4", ink: "#1a2326", mut: "#4b5a5c",
    ecto: "#2a8f7e", ectotx: "#1d6f63", ecto2: "#3c7f74", violet: "#6d5fd0", gold: "#c98a1a",
    line: "#c9c3ae", hatch: "#1a2326",
    spines: ["#d9cfb4", "#cdd8cf", "#d8cbd2", "#cfd4c0", "#d4d0e0", "#e0d3bd"],
    gh_top: ".9", gh_bot: ".45", gh_fill: "#ffffff", gh_line: "#1a2326", eye: "#1a2326"
  }
};

const CSS = `.a{transform-box:fill-box;transform-origin:center}
.bob{animation:bob 6s ease-in-out infinite alternate}
@keyframes bob{from{transform:translateY(-5px) rotate(-2deg)}to{transform:translateY(6px) rotate(2deg)}}
.blink{animation:blink 7s ease-in-out infinite}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
.flick{animation:flick 2.4s ease-in-out infinite alternate}
@keyframes flick{from{transform:scale(1,1);opacity:.85}to{transform:scale(.85,1.15);opacity:1}}
.rise{animation:rise 10s ease-in infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}20%{opacity:.8}100%{transform:translateY(-80px);opacity:0}}
.pulse{animation:pulse 6s ease-in-out infinite alternate}
@keyframes pulse{from{opacity:.5}to{opacity:1}}
.kb{animation:kb 24s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
.dash{animation:dash 8s linear infinite}
@keyframes dash{to{stroke-dashoffset:-72}}
.shim{animation:shim 10s ease-in-out infinite}
@keyframes shim{0%,55%{transform:translateX(-120px)}100%{transform:translateX(420px)}}
.tw{animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion: reduce){.bob,.blink,.flick,.rise,.pulse,.kb,.dash,.shim,.tw{animation:none}}`;

function root(w: number, h: number, T: ThemeColors, title: string, body: string): string {
  const d = `<defs>`
    + `<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${T.ecto}" stop-opacity=".32"/><stop offset="1" stop-color="${T.ecto}" stop-opacity="0"/></radialGradient>`
    + `<radialGradient id="cg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="${T.gold}" stop-opacity=".55"/><stop offset="1" stop-color="${T.gold}" stop-opacity="0"/></radialGradient>`
    + `<linearGradient id="gb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${T.gh_fill}" stop-opacity="${T.gh_top}"/><stop offset="1" stop-color="${T.gh_fill}" stop-opacity="${T.gh_bot}"/></linearGradient>`
    + `<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${T.ecto}" stop-opacity="0"/><stop offset=".5" stop-color="${T.ecto}" stop-opacity=".3"/><stop offset="1" stop-color="${T.ecto}" stop-opacity="0"/></linearGradient>`
    + `<pattern id="ht" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0V5" stroke="${T.hatch}" stroke-width=".8" opacity=".07"/></pattern>`
    + `<pattern id="twp" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><path d="M0,0H9" stroke="${T.ecto2}" stroke-width="1.8" opacity=".85"/></pattern>`
    + `<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .55  0 0 0 0 .5  0 0 0 .5 -.17"/></filter>`
    + `</defs>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${escapeXml(title)}"><title>${escapeXml(title)}</title><style>${CSS}</style>${d}<rect width="${w}" height="${h}" fill="${T.bg}"/><rect width="${w}" height="${h}" fill="url(#ht)"/>${body}<rect class="grain" width="${w}" height="${h}" fill="#000" opacity=".5" filter="url(#noise)"/></svg>`;
}

function ghost(T: ThemeColors, x: number, y: number, s = 1.0, delay = 0, book = false, candle = false, flip = false, op = 1): string {
  const sx = flip ? -s : s;
  const body = "M0,-40C-20,-40 -30,-25 -30,-5L-30,40C-26,34 -22,44 -16,38C-10,32 -6,44 0,38C6,32 10,44 16,38C22,34 26,44 30,40L30,-5C30,-25 20,-40 0,-40Z";
  const parts = [
    `<circle r="62" cy="0" fill="url(#gl)"/>`,
    `<path d="${body}" fill="url(#gb)" stroke="${T.gh_line}" stroke-width="1.3" stroke-linejoin="round"/>`,
    `<path d="M-30,6C-42,10 -44,22 -36,26M30,6C42,10 44,22 36,26" fill="none" stroke="${T.gh_line}" stroke-width="1.3" stroke-linecap="round"/>`,
    `<ellipse class="a blink" cx="-10" cy="-12" rx="4" ry="6" fill="${T.eye}"/><ellipse class="a blink" cx="10" cy="-12" rx="4" ry="6" fill="${T.eye}"/>`,
    `<ellipse cx="0" cy="3" rx="3" ry="5" fill="${T.eye}"/>`
  ];
  if (book) {
    parts.push(`<rect x="-14" y="8" width="28" height="19" rx="2" fill="${T.violet}" stroke="${T.gh_line}" stroke-width="1"/><path d="M0,8V27" stroke="${T.gh_line}" stroke-width=".8"/>`);
  }
  if (candle) {
    parts.push(`<circle cx="38" cy="8" r="24" fill="url(#cg)"/><rect x="35" y="14" width="6" height="14" rx="1" fill="${T.panel2}" stroke="${T.gh_line}" stroke-width=".8"/><path class="a flick" d="M38,13C34,8 38,4 38,0C42,4 42,9 38,13Z" fill="${T.gold}"/>`);
  }
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(sx)},${f1(s)})" opacity="${op}"><g class="a bob" style="animation-delay:${delay}s">${parts.join("")}</g></g>`;
}

function meander(T: ThemeColors, x0: number, x1: number, y: number, delay = 0, op = 0.9): string {
  const segs: string[] = [];
  for (let x = Math.floor(x0); x < Math.floor(x1) - 12; x += 16) {
    segs.push(`M${x},${y + 10}V${y}H${x + 12}V${y + 8}H${x + 4}V${y + 4}H${x + 8}`);
  }
  return `<path d="${segs.join("")}" fill="none" stroke="${T.ecto2}" stroke-width="1.2" opacity="${op}" stroke-linejoin="miter"/>`
    + `<path d="M${x0},${y + 11}H${x1}" stroke="${T.ecto}" stroke-width="1.6" stroke-dasharray="2 10" stroke-linecap="round" class="dash" style="animation-delay:${delay}s" opacity=".85"/>`;
}

function column(T: ThemeColors, x: number, y: number, w: number, h: number): string {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${T.panel2}"/>`
    + `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#twp)" opacity=".55"/>`
    + `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="none" stroke="${T.line}" stroke-width="1"/>`
    + `<rect x="${x - 4}" y="${y}" width="${w + 8}" height="9" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="1"/>`
    + `<rect x="${x - 4}" y="${y + h - 9}" width="${w + 8}" height="9" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="1"/>`;
}

function frame(T: ThemeColors, x: number, y: number, w: number, h: number): string {
  const corners = [
    [x + 4, y + 4, 1, 1], [x + w - 4, y + 4, -1, 1],
    [x + 4, y + h - 4, 1, -1], [x + w - 4, y + h - 4, -1, -1]
  ].map(([cx, cy, sx, sy]) => `<path d="M${cx},${cy}h${12 * sx}M${cx},${cy}v${12 * sy}" stroke="${T.ecto}" stroke-width="2"/>`).join("");
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="3" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="1.6"/>`
    + `<rect x="${x + 6}" y="${y + 6}" width="${w - 12}" height="${h - 12}" rx="2" fill="none" stroke="${T.ecto}" stroke-width=".7" opacity=".55"/>`
    + corners;
}

function bookicon(T: ThemeColors, x: number, y: number, s = 1.0): string {
  return `<g transform="translate(${x},${y}) scale(${s})"><rect width="12" height="15" rx="1.5" fill="none" stroke="${T.ectotx}" stroke-width="1.5"/><path d="M3,3H9M3,6H9" stroke="${T.ectotx}" stroke-width="1"/></g>`;
}

function label(T: ThemeColors, x: number, y: number, num: string, text: string): string {
  return bookicon(T, x, y - 13)
    + `<text x="${x + 22}" y="${y}" font-family="${MONO}" font-size="12.5" letter-spacing="3" fill="${T.ectotx}" font-weight="700">SHELF ${num}  /  ${escapeXml(text)}</text>`;
}

function motes(T: ThemeColors, pts: [number, number][], seed = 1): string {
  const rng = createRng(seed);
  return pts.map(([x, y]) =>
    `<circle class="a rise" cx="${x}" cy="${y}" r="${f1(1.2 + rng() * 1.2)}" fill="${T.ecto}" style="animation-delay:-${f1(rng() * 10)}s;animation-duration:${f1(8 + rng() * 5)}s"/>`
  ).join("");
}

function stars(T: ThemeColors, n: number, seed: number, x0: number, x1: number, y0: number, y1: number): string {
  const rng = createRng(seed);
  const out: string[] = [];
  for (let i = 0; i < n; i++) {
    const x = x0 + rng() * (x1 - x0);
    const y = y0 + rng() * (y1 - y0);
    out.push(`<circle class="tw" style="animation-delay:-${f1(rng() * 4)}s" cx="${f1(x)}" cy="${f1(y)}" r="${f1(0.8 + rng() * 0.9)}" fill="${T.ink}"/>`);
  }
  return out.join("");
}

function hero(T: ThemeColors, isDark: boolean, content: Content, heroImg: string, avatarImg: string): string {
  const fx = 562, fy = 80, fw = 300, fh = 388;
  const b: string[] = [
    `<clipPath id="pc"><rect width="900" height="540"/></clipPath><g clip-path="url(#pc)">`
  ];
  if (isDark) {
    b.push(stars(T, 30, 3, 10, 520, 10, 300));
  }
  b.push(`<circle class="a pulse" cx="712" cy="274" r="270" fill="url(#gl)"/>`);
  b.push(column(T, 540, 66, 16, 412) + column(T, 868, 66, 16, 412));
  b.push(`<rect x="${fx}" y="${fy}" width="${fw}" height="${fh}" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="2"/>`
    + `<rect x="${fx - 5}" y="${fy - 5}" width="${fw + 10}" height="${fh + 10}" fill="none" stroke="${T.ecto}" stroke-width=".8" opacity=".6"/>`
    + `<clipPath id="hc"><rect x="${fx + 8}" y="${fy + 8}" width="${fw - 16}" height="${fh - 16}"/></clipPath>`
    + `<g clip-path="url(#hc)"><image class="a kb" x="${fx + 8}" y="${fy + 8}" width="${fw - 16}" height="${fh - 16}" preserveAspectRatio="xMidYMid slice" href="${heroImg}"/>`
    + `<g transform="skewX(-20)"><rect class="a shim" x="570" y="80" width="40" height="388" fill="url(#shg)"/></g></g>`);
  b.push(meander(T, 0, 900, 514));
  b.push(motes(T, [[120, 440], [300, 470], [520, 420], [640, 500], [840, 380], [60, 300]], 2));
  b.push(`</g>`);

  const names = content.name.split(" ");
  const name1 = names[0] || "Solayman";
  const name2 = names.slice(1).join(" ") || "El Mouden";

  b.push(`<clipPath id="av"><circle cx="76" cy="52" r="14"/></clipPath>`
    + `<image x="62" y="38" width="28" height="28" clip-path="url(#av)" href="${avatarImg}"/>`
    + `<circle cx="76" cy="52" r="14" fill="none" stroke="${T.ecto}" stroke-width="1.2"/>`
    + `<text x="100" y="56" font-family="${MONO}" font-size="12.5" fill="${T.mut}">${escapeXml(content.handle)} / README</text>`
    + `<path d="M62,78H500" stroke="${T.ecto2}" stroke-width=".8" stroke-dasharray="2 5" opacity=".8"/>`
    + `<text x="62" y="136" font-family="${SERIF}" font-style="italic" font-size="22" fill="${T.mut}">Hi, I'm</text>`
    + `<text x="60" y="204" font-family="${SERIF}" font-weight="700" font-size="66" fill="${T.ink}">${escapeXml(name1)}</text>`
    + `<text x="60" y="272" font-family="${SERIF}" font-weight="700" font-size="66" fill="${T.ink}">${escapeXml(name2)}</text>`
    + `<text x="62" y="312" font-family="${MONO}" font-weight="700" font-size="14" letter-spacing="5" fill="${T.ectotx}">${escapeXml(content.role.toUpperCase())}</text>`
    + `<text x="62" y="338" font-family="${MONO}" font-size="13" fill="${T.ink}">${escapeXml(content.pillars)}</text>`);

  content.tagline.forEach((ln, i) => {
    b.push(`<text x="62" y="${378 + i * 22}" font-family="${SERIF}" font-size="15" fill="${T.mut}">${escapeXml(ln)}</text>`);
  });

  b.push(ghost(T, 498, 352, 1.15, 0, true, false) + ghost(T, 430, 478, 0.8, -3, false, true) + ghost(T, 880, 470, 1.0, -2, false, false, true, 0.95));
  return root(900, 540, T, `${content.name} - ${content.role}`, b.join(""));
}

function button(T: ThemeColors, text: string): string {
  const b = `<rect x="1" y="1" width="148" height="38" rx="3" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="1.5"/>`
    + `<rect x="5" y="5" width="140" height="30" rx="2" fill="none" stroke="${T.ecto}" stroke-width=".6" opacity=".6"/>`
    + bookicon(T, 16, 12.5)
    + `<text x="38" y="25" font-family="${MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="${T.ink}">${escapeXml(text)}</text>`;
  return root(150, 40, T, text, b);
}

function about(T: ThemeColors, content: Content): string {
  const b: string[] = [
    frame(T, 20, 14, 860, 302),
    label(T, 56, 58, "01", "ABOUT"),
    label(T, 536, 58, "02", "MY JOURNEY")
  ];
  content.about.forEach((ln, i) => {
    const y = 106 + i * 28;
    b.push(`<path d="M56,${y + 8}H500" stroke="${T.line}" stroke-width=".9"/>`
      + `<text x="58" y="${y}" font-family="${SERIF}" font-size="15" fill="${T.ink}">${escapeXml(ln)}</text>`);
  });
  content.journey.forEach(({ lang, area }, i) => {
    const y = 108 + i * 38;
    b.push(`<rect x="538" y="${y - 10}" width="7" height="11" rx="1" fill="none" stroke="${T.ectotx}" stroke-width="1.3"/>`
      + `<text x="554" y="${y}" font-family="${MONO}" font-size="14" font-weight="700" fill="${T.ink}">${escapeXml(lang)}</text>`
      + `<path d="M656,${y - 5}H708" stroke="${T.ecto}" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="1 7" class="dash" style="animation-delay:-${i}s"/>`
      + `<text x="720" y="${y}" font-family="${SERIF}" font-size="15" fill="${T.ink}">${escapeXml(area)}</text>`);
  });
  b.push(meander(T, 56, 500, 280, -2, 0.7));
  b.push(ghost(T, 840, 282, 0.55, -2, true));
  return root(900, 330, T, "About and Journey", b.join(""));
}

function skills(T: ThemeColors, content: Content): string {
  const heights = [104, 92, 110, 98, 86, 108, 96, 110, 88, 100, 106, 94];
  const b: string[] = [
    frame(T, 20, 14, 860, 372),
    label(T, 56, 58, "03", "TECHNOLOGIES &amp; SKILLS"),
    meander(T, 56, 844, 70, -3, 0.7)
  ];
  for (let row = 0; row < 2; row++) {
    const base = 196 + row * 142;
    b.push(`<rect x="40" y="${base}" width="820" height="9" fill="${T.panel2}" stroke="${T.ecto2}" stroke-width="1"/>`);
  }
  content.skills.slice(0, 12).forEach(({ label: name, mono }, i) => {
    const row = Math.floor(i / 6);
    const col = i % 6;
    const base = 196 + row * 142;
    const cx = 121.5 + col * 131;
    const h = heights[i % heights.length];
    const w = 64;
    const colFill = T.spines[i % 6];
    let sp = i === 7 ? `<g class="a bob" style="animation-delay:-2s">` : `<g>`;
    sp += `<rect x="${f1(cx - w / 2)}" y="${base - h}" width="${w}" height="${h}" rx="2" fill="${colFill}" stroke="${T.ecto2}" stroke-width="1.2"/>`
      + `<path d="M${f1(cx - w / 2)},${base - h + 9}h${w}M${f1(cx - w / 2)},${base - 12}h${w}" stroke="${T.ecto2}" stroke-width="2"/>`
      + `<text x="${f1(cx)}" y="${base - h + 36}" text-anchor="middle" font-family="${MONO}" font-size="15" font-weight="700" fill="${T.ink}">${escapeXml(mono)}</text>`
      + `<path transform="translate(${f1(cx)},${base - h + 52})" d="M0,-5L4,0L0,5L-4,0Z" fill="${T.ecto}"/></g>`;
    b.push(sp);
    b.push(`<text x="${f1(cx)}" y="${base + 26}" text-anchor="middle" font-family="${SERIF}" font-size="12.5" fill="${T.ink}">${escapeXml(name)}</text>`);
  });
  b.push(ghost(T, 846, 150, 0.6, -1));
  return root(900, 400, T, "Technologies and skills", b.join(""));
}

function projectsTitle(T: ThemeColors): string {
  const b = [
    meander(T, 40, 270, 32), meander(T, 630, 860, 32, -3),
    `<rect x="286" y="14" width="328" height="42" rx="3" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="1.6"/>`
    + `<rect x="291" y="19" width="318" height="32" rx="2" fill="none" stroke="${T.ecto}" stroke-width=".6" opacity=".6"/>`
    + `<text x="450" y="40" text-anchor="middle" font-family="${MONO}" font-size="12.5" font-weight="700" letter-spacing="3" fill="${T.ectotx}">SHELF 04  /  SELECTED PROJECTS</text>`
    + `<circle cx="450" cy="66" r="3" fill="${T.ecto}"/>`
  ];
  return root(900, 80, T, "Selected projects", b.join(""));
}

function chips(T: ThemeColors, tags: string[]): string {
  const out: string[] = [];
  let x = 8, y = 176;
  for (const t of tags) {
    const w = t.length * 6.4 + 14;
    if (x + w > 200) {
      x = 8;
      y += 22;
    }
    out.push(`<rect x="${f1(x)}" y="${y}" width="${f1(w)}" height="18" rx="3" fill="${T.panel2}" stroke="${T.ecto2}" stroke-width=".8"/>`
      + `<text x="${f1(x + w / 2)}" y="${y + 12.5}" text-anchor="middle" font-family="${MONO}" font-size="10.5" fill="${T.ink}">${escapeXml(t)}</text>`);
    x += w + 5;
  }
  return out.join("");
}

function card(T: ThemeColors, i: number, title: string, desc1: string, desc2: string, tags: string[], cardImg: string): string {
  const b: string[] = [
    `<rect x="1" y="1" width="206" height="236" rx="4" fill="${T.panel}" stroke="${T.ecto2}" stroke-width="1.4"/>`,
    `<clipPath id="tc${i}"><rect x="8" y="8" width="192" height="92"/></clipPath>`,
    `<g clip-path="url(#tc${i})"><image class="a kb" x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" href="${cardImg}" style="animation-delay:-${i * 3}s"/>`
    + `<g transform="skewX(-20)"><rect class="a shim" x="20" y="8" width="26" height="92" fill="url(#shg)" style="animation-delay:-${i * 1.3}s"/></g></g>`,
    `<rect x="8" y="8" width="192" height="92" fill="none" stroke="${T.ecto}" stroke-width=".9"/>`,
    `<rect x="8" y="8" width="58" height="19" fill="${T.bg}" stroke="${T.ecto}" stroke-width=".9"/>`
    + `<text x="37" y="21" text-anchor="middle" font-family="${MONO}" font-size="10.5" font-weight="700" fill="${T.ectotx}">No. ${String(i + 1).padStart(2, "0")}</text>`,
    `<path d="M10,131H198M10,150H198M10,165H198" stroke="${T.line}" stroke-width=".8" opacity=".8"/>`,
    `<text x="10" y="126" font-family="${SERIF}" font-weight="700" font-size="16" fill="${T.ink}">${escapeXml(title)}</text>`,
    `<text x="10" y="145" font-family="${SERIF}" font-size="11.5" fill="${T.mut}">${escapeXml(desc1)}</text>`,
    `<text x="10" y="160" font-family="${SERIF}" font-size="11.5" fill="${T.mut}">${escapeXml(desc2)}</text>`,
    chips(T, tags),
    `<circle cx="104" cy="229" r="3.5" fill="${T.bg}" stroke="${T.ecto2}" stroke-width="1"/>`
  ];
  return root(208, 238, T, `No. ${String(i + 1).padStart(2, "0")}, ${title} project card`, b.join(""));
}

function footer(T: ThemeColors, isDark: boolean, content: Content): string {
  const brand = content.brand?.latin || "NashirTech";
  const b: string[] = [
    `<clipPath id="pc"><rect width="900" height="270"/></clipPath><g clip-path="url(#pc)">`
  ];
  if (isDark) {
    b.push(stars(T, 24, 8, 10, 890, 8, 150));
  }
  const sky = isDark ? T.bg : T.panel2;
  for (let k = 0; k < 7; k++) {
    const cx = 64 + k * 128;
    b.push(`<path d="M${cx - 44},270V212A44,44 0 0 1 ${cx + 44},212V270Z" fill="${sky}" stroke="${T.ecto2}" stroke-width="1.4"/>`);
    if (isDark) {
      const rng = createRng(30 + k);
      for (let s = 0; s < 4; s++) {
        b.push(`<circle class="tw" style="animation-delay:-${f1(rng() * 4)}s" cx="${cx + (rng() - 0.5) * 68}" cy="${222 + rng() * 40}" r="1.2" fill="${T.ink}"/>`);
      }
    }
  }
  for (let k = 0; k < 8; k++) {
    b.push(column(T, k * 128 - 14, 178, 28, 92));
  }
  b.push(ghost(T, 192, 226, 0.75, 0) + ghost(T, 448, 232, 0.65, -3, true) + ghost(T, 704, 226, 0.75, -5, false, true, true));
  b.push(motes(T, [[250, 170], [620, 160], [820, 180], [80, 190]], 4));
  b.push(`</g>`);
  b.push(`<text x="450" y="70" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="30" fill="${T.ink}">${escapeXml(content.footer.line1)}</text>`
    + `<text x="450" y="100" text-anchor="middle" font-family="${MONO}" font-size="12.5" letter-spacing="1" fill="${T.mut}">${escapeXml(content.footer.line2)}</text>`
    + meander(T, 240, 660, 118, -1, 0.8)
    + `<text x="450" y="152" text-anchor="middle" font-family="${SERIF}" font-size="13" fill="${T.ectotx}">${escapeXml(brand)}</text>`);
  return root(900, 270, T, "Footer", b.join(""));
}

export const ghostStyle: StyleModule = {
  id: "ghost",
  name: "Ghost Scholar Library",
  keywords: ["ghost", "library", "books", "scholar", "meander", "vintage"],
  palette: {
    dark: ["#05090c", "#0b1519", "#8ff0d0", "#ffd27a", "#a79bff"],
    light: ["#efece1", "#f8f6ee", "#2a8f7e", "#c98a1a", "#6d5fd0"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/ghost/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [270, 0, 790, 680], [520, 680], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [470, 180, 610, 320], [64, 64], 0.9);

    const cropBoxes: [number, number, number, number][] = [
      [470, 360, 400, 550],
      [620, 220, 280, 410],
      [680, 60, 180, 270],
      [460, 600, 250, 380],
      [320, 480, 300, 490],
      [340, 180, 320, 510],
      [680, 380, 240, 370],
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
      items.map((p, i) => `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `No. ${String(i + 1).padStart(2, "0")}, ${p.title}: ${p.line1} ${p.line2}`, "24%")}</a>`).join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name}, ${content.role}. Friendly ghosts in an impossible starlit library.`, "100%"),
      `<a href="${content.github}">${pic("btn-github", "GitHub profile", "150")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn profile", "150")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio website", "150")}</a>`,
      pic("about", "About me and my journey", "100%"),
      pic("skills", "Technologies and skills shelved as books", "100%"),
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
export default ghostStyle;
