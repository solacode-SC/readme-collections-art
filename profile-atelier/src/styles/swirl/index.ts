import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, ptsPath, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
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
  pal: string[];
  warm: string;
  roof: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg1: "#041114",
    bg2: "#0a2126",
    fg: "#ecf4ef",
    mute: "#8db2ac",
    acc: "#f0d672",
    acc2: "#7fc9bf",
    line: "#1d4a50",
    card: "#08191d",
    pal: ["#2f8f98", "#4fb09b", "#8fc99c", "#5aaebb"],
    warm: "#f0d672",
    roof: "#dc7a52",
  },
  light: {
    bg1: "#fbf7ea",
    bg2: "#efe8d2",
    fg: "#12343a",
    mute: "#58797c",
    acc: "#96640a",
    acc2: "#1d6670",
    line: "#c3d2c6",
    card: "#fffdf4",
    pal: ["#1d6670", "#2f8a7e", "#5f9a74", "#3f8e9c"],
    warm: "#c9971c",
    roof: "#b6532f",
  },
};

const STYLE = `<style>
.spin{transform-box:fill-box;transform-origin:center;animation:spin 70s linear infinite}
.spin.r{animation-direction:reverse;animation-duration:95s}
@keyframes spin{to{transform:rotate(360deg)}}
.dots{stroke-dasharray:.1 34;stroke-linecap:round;animation:run 18s linear infinite}
@keyframes run{to{stroke-dashoffset:-341}}
.pulse{animation:pulse 10s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
@media (prefers-reduced-motion:reduce){.spin,.dots,.pulse{animation:none}}
</style>`;

const VORT: [number, number, number, number, number][] = [
  [700, 170, 1.0, 0.2, 44],
  [570, 285, -0.6, 0.12, 24],
  [850, 62, -0.55, 0.14, 22],
  [545, 60, 0.5, 0.12, 24],
  [860, 290, 0.55, 0.12, 22],
];

function vel(x: number, y: number): [number, number] {
  let vx = 0;
  let vy = 0;
  for (const [cx, cy, g, k, a] of VORT) {
    const dx = x - cx;
    const dy = y - cy;
    const d2 = dx * dx + dy * dy + a * a;
    const w = (a * 2) / d2;
    vx += (-g * dy - k * dx) * w;
    vy += (g * dx - k * dy) * w;
  }
  const n = Math.hypot(vx, vy) || 1;
  return [vx / n, vy / n];
}

function computeStreamlines(): [number, number][][] {
  const x0 = 430, x1 = 900, y0 = 0, y1 = 345, dsep = 8.5, h = 4.0;
  const cell = dsep;
  const grid = new Map<string, [number, number][]>();

  function near(x: number, y: number, r: number): boolean {
    const i = Math.floor(x / cell);
    const j = Math.floor(y / cell);
    const r2 = r * r;
    for (let a = i - 1; a <= i + 1; a++) {
      for (let b = j - 1; b <= j + 1; b++) {
        const pts = grid.get(`${a},${b}`);
        if (pts) {
          for (const [px, py] of pts) {
            if ((px - x) ** 2 + (py - y) ** 2 < r2) return true;
          }
        }
      }
    }
    return false;
  }

  function step(x: number, y: number, s: number): [number, number] {
    const [vx1, vy1] = vel(x, y);
    const mx = x + (s * vx1 * h) / 2;
    const my = y + (s * vy1 * h) / 2;
    const [vx2, vy2] = vel(mx, my);
    return [x + s * vx2 * h, y + s * vy2 * h];
  }

  function trace(startX: number, startY: number, s: number): [number, number][] {
    const out: [number, number][] = [];
    let x = startX, y = startY;
    for (let n = 0; n < 260; n++) {
      [x, y] = step(x, y, s);
      if (!(x0 <= x && x <= x1 && y0 <= y && y <= y1)) break;
      if (near(x, y, dsep * 0.55)) break;
      if (VORT.some(([cx, cy]) => Math.hypot(x - cx, y - cy) < 3)) break;
      if (n > 12 && out.length && Math.hypot(x - out[0][0], y - out[0][1]) < h) break;
      out.push([x, y]);
    }
    return out;
  }

  let sfc = 4;
  function rnd() {
    sfc = (sfc * 1664525 + 1013904223) >>> 0;
    return sfc / 4294967296;
  }

  const lines: [number, number][][] = [];
  for (let it = 0; it < 6000; it++) {
    const x = x0 + rnd() * (x1 - x0);
    const y = y0 + rnd() * (y1 - y0);
    if (near(x, y, dsep)) continue;
    const fw = trace(x, y, 1);
    const bw = trace(x, y, -1);
    const line: [number, number][] = [...bw.reverse(), [x, y], ...fw];
    if (line.length < 10) continue;
    for (const p of line) {
      const key = `${Math.floor(p[0] / cell)},${Math.floor(p[1] / cell)}`;
      if (!grid.has(key)) grid.set(key, []);
      grid.get(key)!.push(p);
    }
    lines.push(line);
  }
  return lines;
}

const PRECOMPUTED_STREAMLINES = computeStreamlines();

function lineColor(c: ThemeColors, line: [number, number][]): string {
  const mx = line.reduce((acc, p) => acc + p[0], 0) / line.length;
  const my = line.reduce((acc, p) => acc + p[1], 0) / line.length;
  let best = 0;
  let minVal = Infinity;
  for (let i = 0; i < VORT.length; i++) {
    const val = Math.hypot(mx - VORT[i][0], my - VORT[i][1]) - VORT[i][4];
    if (val < minVal) {
      minVal = val;
      best = i;
    }
  }
  const d = Math.hypot(mx - VORT[best][0], my - VORT[best][1]);
  return c.pal[(Math.floor(d / 30) + best) % 4];
}

function spiral(cx: number, cy: number, r: number, turns = 3, rot = 0, start = 0.15): [number, number][] {
  const pts: [number, number][] = [];
  const n = Math.floor(turns * 28);
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const th = t * turns * 2 * Math.PI + rot;
    const rr = r * (start + (1 - start) * t);
    pts.push([cx + rr * Math.cos(th), cy + rr * Math.sin(th)]);
  }
  return pts;
}

function waves(
  x0: number,
  x1: number,
  y0: number,
  rows: number,
  c: ThemeColors,
  amp = 12,
  gap = 3.8,
  seed = 1,
  cols?: string[]
): string {
  const colorList = cols || [c.warm, c.pal[2], c.warm, c.pal[1]];
  const ph = seed * 1.7;
  const o: string[] = [];
  for (let i = 0; i < rows; i++) {
    const pts: [number, number][] = [];
    for (let x = Math.floor(x0); x <= Math.floor(x1); x += 6) {
      const y = y0 + i * gap + amp * Math.sin(x / 95 + i * 0.16 + ph) + amp * 0.35 * Math.sin(x / 38 + i * 0.3);
      pts.push([x, y]);
    }
    o.push(
      `<path d="${ptsPath(pts)}" fill="none" stroke="${colorList[i % colorList.length]}" stroke-width="1.1" opacity="${0.5 + 0.4 * (i % 2)}"/>`
    );
  }
  return o.join("");
}

function plus(x: number, y: number, s: number, col: string, op = 0.8): string {
  return `<path d="M${x - s} ${y}H${x + s}M${x} ${y - s}V${y + s}" stroke="${col}" stroke-width="1" opacity="${op}"/>`;
}

function defs(c: ThemeColors): string {
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<linearGradient id="side" x1="0" x2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset=".35" stop-color="${c.bg1}" stop-opacity=".96"/><stop offset="1" stop-color="${c.bg1}" stop-opacity="0"/></linearGradient>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string, clsFont = MONO): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${clsFont}">
${STYLE}${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>${body}
<path d="M.5 0V${h}M${w - 0.5} 0V${h}" stroke="${c.line}"/></svg>`;
}

function divider(c: ThemeColors, y: number, w = 900): string {
  const pts: [number, number][] = [];
  for (let x = 40; x <= w - 39; x += 6) {
    pts.push([x, y + 3 * Math.sin(x / 38)]);
  }
  const d = ptsPath(pts);
  return `<path d="${d}" fill="none" stroke="${c.line}" stroke-width="1"/>
<path class="dots" d="${d}" fill="none" stroke="${c.acc}" stroke-width="2.4"/>`;
}

function heading(c: ThemeColors, y: number, idx: string, label: string): string {
  const sp = ptsPath(spiral(60, y, 9, 2.4));
  return `<path d="${sp}" fill="none" stroke="${c.acc}" stroke-width="1.5"/>
<text x="82" y="${y + 4}" font-size="12" letter-spacing="2.2" fill="${c.mute}">${idx} /</text>
<text x="126" y="${y + 4}" font-size="12" font-weight="700" letter-spacing="2.2" fill="${c.fg}">${escapeXml(label)}</text>`;
}

function corners(c: ThemeColors, x: number, y: number, w: number, h: number, s = 7, op = 0.9): string {
  return `<path d="M${x} ${y + s}V${y}H${x + s}M${x + w - s} ${y}H${x + w}V${y + s}M${x + w} ${y + h - s}V${y + h}H${x + w - s}M${x + s} ${y + h}H${x}V${y + h - s}" fill="none" stroke="${c.acc}" stroke-width="1.3" opacity="${op}"/>`;
}

function hero(c: ThemeColors, content: Content): string {
  let b = PRECOMPUTED_STREAMLINES.map(
    (l) => `<path d="${ptsPath(l)}" fill="none" stroke="${lineColor(c, l)}" stroke-width="1.15" opacity=".88"/>`
  ).join("");

  for (let i = 0; i < PRECOMPUTED_STREAMLINES.length; i += 9) {
    b += `<path class="dots" d="${ptsPath(PRECOMPUTED_STREAMLINES[i])}" fill="none" stroke="${c.acc}" stroke-width="2.4" opacity=".9"/>`;
  }
  b += `<rect x="400" y="0" width="300" height="400" fill="url(#side)"/>`;
  b += waves(0, 900, 372, 12, c, 11, 3.6);

  const spiralRoses: [number, number, number][] = [
    [560, 366, 15],
    [640, 380, 11],
    [725, 360, 17],
    [815, 378, 12],
    [868, 358, 10],
  ];
  spiralRoses.forEach(([x, y, r], i) => {
    b += `<circle cx="${x}" cy="${y}" r="${r + 3}" fill="${c.bg1}"/>
<path class="spin${i % 2 !== 0 ? " r" : ""}" d="${ptsPath(spiral(x, y, r, 3, i))}" fill="none" stroke="${c.warm}" stroke-width="1.4"/>`;
  });

  b += `<path d="${ptsPath(spiral(60, 34, 8, 2.4))}" fill="none" stroke="${c.acc}" stroke-width="1.4"/>
<text x="80" y="38" font-size="12" fill="${c.mute}">${escapeXml(content.handle)} <tspan fill="${c.line}">/</tspan> README</text>
<path d="M40 56H860" stroke="${c.line}"/>${plus(40, 56, 4, c.acc)}${plus(860, 56, 4, c.acc)}`;
  b += plus(436, 100, 4, c.mute, 0.5) + plus(884, 332, 4, c.mute, 0.5);
  b += `<text x="868" y="332" font-size="9" text-anchor="end" fill="${c.mute}" opacity=".8">r = a·e^(bθ)</text>`;

  b += `<text x="60" y="108" font-size="13" letter-spacing="3" fill="${c.mute}">HI, I&apos;M</text>
<text x="58" y="160" font-size="42" font-family="${SERIF}" letter-spacing="-.5" fill="${c.fg}">${escapeXml(content.name)}</text>
<text x="60" y="204" font-size="16" font-weight="700" letter-spacing="3" fill="${c.acc}">${escapeXml(content.role.toUpperCase())}</text>
<text x="60" y="246" font-size="13" letter-spacing="1" fill="${c.fg}" xml:space="preserve">${escapeXml(content.pillars)}</text>`;

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${290 + i * 20}" font-size="12.5" fill="${c.mute}">${escapeXml(t)}</text>`;
  });
  b += `<rect x="60" y="262" width="36" height="2" fill="${c.acc}"/>`;

  const kanji = content.options.useCJK ? "夢を築く" : "DREAM";
  Array.from(kanji).forEach((ch, i) => {
    b += `<text x="878" y="${92 + i * 22}" font-size="14" text-anchor="middle" font-family="${JP}" fill="${c.acc2}" opacity=".9">${escapeXml(ch)}</text>`;
  });

  return wrap(900, 410, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const b = `<rect x=".75" y=".75" width="${w - 1.5}" height="38.5" rx="4" fill="${c.card}" stroke="${c.acc2}" stroke-opacity=".8"/>
<path d="${ptsPath(spiral(24, 20, 8, 2.2))}" fill="none" stroke="${c.acc}" stroke-width="1.4"/>
<text x="42" y="24.5" font-size="12" letter-spacing="1.2" fill="${c.fg}">${escapeXml(label.toUpperCase())}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${MONO}">${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = heading(c, 42, "01", "ABOUT");
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
    b += `<text x="60" y="${92 + i * 21}" font-size="13" fill="${c.fg}" xml:space="preserve">${escapeXml(t)}</text>`;
  });

  b += `<path d="M450 74V246" stroke="${c.line}"/>${plus(450, 74, 4, c.acc)}${plus(450, 246, 4, c.acc)}`;
  b += heading(c, 42, "02", "MY JOURNEY")
    .replace('x="60"', 'x="480"')
    .replace('x="82"', 'x="502"')
    .replace('x="126"', 'x="546"');

  content.journey.slice(0, 5).forEach((j, i) => {
    const y = 96 + i * 30;
    b += `<path d="${ptsPath(spiral(488, y - 4, 6, 2))}" fill="none" stroke="${c.acc}" stroke-width="1.3"/>
<text x="508" y="${y}" font-size="13" fill="${c.fg}">${escapeXml(j.lang)}</text>
<path d="M640 ${y - 4}H664M659 ${y - 8}L664 ${y - 4}L659 ${y}" fill="none" stroke="${c.acc2}"/>
<text x="682" y="${y}" font-size="13" fill="${c.mute}">${escapeXml(j.area)}</text>`;
  });

  b += divider(c, 274);
  return wrap(900, 290, c, b);
}

function skills(c: ThemeColors, content: Content): string {
  let b = heading(c, 40, "03", "TECHNOLOGIES &amp; SKILLS");
  const w = 125, g = 14;
  content.skills.slice(0, 12).forEach((s, i) => {
    const x = 40 + (i % 6) * (w + g);
    const y = 68 + Math.floor(i / 6) * 66;
    b += `<rect x="${x + 0.5}" y="${y + 0.5}" width="${w - 1}" height="53" rx="5" fill="${c.card}" stroke="${c.line}"/>
${corners(c, x + 3, y + 3, w - 6, 47, 5, 0.7)}
<text x="${x + w / 2}" y="${y + 25}" font-size="16" font-weight="700" text-anchor="middle" fill="${c.acc}">${escapeXml(s.mono)}</text>
<text x="${x + w / 2}" y="${y + 43}" font-size="10.5" text-anchor="middle" fill="${c.fg}">${escapeXml(s.label)}</text>`;
  });
  b += divider(c, 214);
  return wrap(900, 226, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 60, c, heading(c, 34, "04", "SELECTED PROJECTS"));
}

function motif(c: ThemeColors, kind: string, idx: number): string {
  const W = 192, H = 56;
  const p = c.pal;
  const o: string[] = [];

  if (kind === "waves" || idx === 0) {
    const specs: [number, number, string][] = [
      [0.05, 14, p[0]],
      [0.09, 9, p[1]],
      [0.14, 6, c.warm],
    ];
    specs.forEach(([f, a, col], k) => {
      const pts: [number, number][] = [];
      for (let x = 0; x <= W; x += 3) {
        pts.push([x, 28 + a * Math.sin(x * f + k) + 4 * Math.sin(x * f * 2.7)]);
      }
      o.push(`<path d="${ptsPath(pts)}" fill="none" stroke="${col}" stroke-width="1.3"/>`);
    });
  } else if (kind === "flow" || idx === 1) {
    for (let k = 0; k < 9; k++) {
      const pts: [number, number][] = [];
      for (let x = 0; x <= W; x += 3) {
        pts.push([x, 6 + k * 5.5 + (k - 4) * 3 * Math.sin(x / 38 + k * 0.2) * (x / W)]);
      }
      o.push(`<path d="${ptsPath(pts)}" fill="none" stroke="${p[k % 4]}" stroke-width="1.2"/>`);
    }
  } else if (kind === "spiral" || idx === 2) {
    o.push(`<path d="${ptsPath(spiral(70, 28, 40, 5))}" fill="none" stroke="${p[0]}" stroke-width="1.2"/>`);
    o.push(`<path d="${ptsPath(spiral(138, 30, 26, 4, 1.2))}" fill="none" stroke="${c.warm}" stroke-width="1.2"/>`);
  } else if (kind === "network" || idx === 3) {
    const nodes: [number, number][] = [
      [24, 20], [60, 42], [80, 15], [110, 35], [140, 18], [170, 38], [95, 48], [45, 12], [155, 46]
    ];
    nodes.forEach(([ax, ay]) => {
      nodes.slice(0, 3).forEach(([bx, by]) => {
        if (ax !== bx) {
          o.push(`<path d="M${f1(ax)} ${f1(ay)}L${f1(bx)} ${f1(by)}" stroke="${p[1]}" stroke-width=".9" opacity=".8"/>`);
        }
      });
    });
    nodes.forEach(([x, y], i) => {
      o.push(`<circle cx="${f1(x)}" cy="${f1(y)}" r="${i === 0 ? 4 : 2.6}" fill="${i === 0 ? c.warm : p[2]}"/>`);
    });
  } else if (kind === "roses" || idx === 4) {
    const list: [number, number, number][] = [
      [30, 30, 16], [72, 18, 10], [100, 38, 15], [140, 20, 11], [168, 40, 12]
    ];
    list.forEach(([x, y, r], i) => {
      o.push(`<path d="${ptsPath(spiral(x, y, r, 3, i))}" fill="none" stroke="${c.warm}" stroke-width="1.3"/>`);
    });
    o.push(`<path d="M0 50Q40 44 90 50T192 48" fill="none" stroke="${p[2]}" stroke-width="1.1"/>`);
  } else if (kind === "pulse" || idx === 5) {
    const pts: [number, number][] = [];
    let x = 0;
    while (x < W) {
      const spike = (x / 14) % 3 === 0;
      pts.push([x, 30], [x + 4, 30 - (spike ? 22 : 4)], [x + 8, 30 + (spike ? 14 : 4)], [x + 12, 30]);
      x += 14;
    }
    o.push(`<path d="${ptsPath(pts)}" fill="none" stroke="${p[1]}" stroke-width="1.2"/>`);
    o.push(`<path d="M0 30H${W}" stroke="${c.warm}" stroke-width=".8" stroke-dasharray="2 4"/>`);
  } else {
    for (let i = 0; i < 8; i++) {
      for (let j = 0; j < 3; j++) {
        const on = (i * 3 + j) === 4 || (i * 3 + j) === 11 || (i * 3 + j) === 17;
        o.push(`<rect x="${10 + i * 23}" y="${8 + j * 16}" width="18" height="11" rx="2" fill="${on ? c.warm : "none"}" fill-opacity=".85" stroke="${p[0]}" stroke-width=".9"/>`);
      }
    }
  }
  return o.join("");
}

function card(
  c: ThemeColors,
  idx: number,
  title: string,
  d1: string,
  d2: string,
  tags: string[],
  kind: string
): string {
  const w = 208, h = 176;
  let b = `<defs><clipPath id="cl"><rect x="8" y="8" width="192" height="56" rx="3"/></clipPath></defs>
<rect x=".75" y=".75" width="${w - 1.5}" height="${h - 1.5}" rx="6" fill="${c.card}" stroke="${c.line}"/>
${corners(c, 4, 4, w - 8, h - 8, 8)}
<rect x="8" y="8" width="192" height="56" rx="3" fill="${c.bg1}"/>
<g transform="translate(8 8)" clip-path="url(#cl)">${motif(c, kind, idx)}</g>
<text x="14" y="20" font-size="8.5" fill="${c.mute}">N°${String(idx + 1).padStart(2, "0")}</text>
<text x="16" y="92" font-size="13.5" font-weight="700" fill="${c.fg}">${escapeXml(title)}</text>
<text x="16" y="111" font-size="10.5" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="125" font-size="10.5" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let tagX = 16;
  tags.slice(0, 4).forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${f1(tagX)}" y="142" width="${f1(cw)}" height="17" rx="3" fill="none" stroke="${c.line}"/>
<text x="${f1(tagX + cw / 2)}" y="153.5" font-size="8.5" text-anchor="middle" fill="${c.acc2}">${escapeXml(t)}</text>`;
    tagX += cw + 5;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">${defs(c)}${b}</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  let b = waves(0, 900, 78, 13, c, 10, 3.5, 5);
  const spiralList: [number, number, number][] = [
    [90, 70, 14], [210, 82, 10], [690, 72, 12], [800, 84, 16], [860, 68, 9]
  ];
  spiralList.forEach(([x, y, r], i) => {
    b += `<circle cx="${x}" cy="${y}" r="${r + 3}" fill="${c.bg1}"/>
<path class="spin${i % 2 !== 0 ? " r" : ""}" d="${ptsPath(spiral(x, y, r, 3, i))}" fill="none" stroke="${c.warm}" stroke-width="1.4"/>`;
  });
  b += `<rect x="270" y="0" width="360" height="74" fill="${c.bg1}" opacity=".9"/>
<text x="450" y="34" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle" fill="${c.acc}" xml:space="preserve">${escapeXml(content.footer.line1.toUpperCase())}</text>
<text x="450" y="56" font-size="10.5" letter-spacing="1" text-anchor="middle" fill="${c.mute}" xml:space="preserve">${escapeXml(content.footer.line2)}</text>`;

  return wrap(900, 130, c, b);
}

export const swirlStyle: StyleModule = {
  id: "swirl",
  name: "Swirl",
  keywords: ["flow-field", "teal", "calm"],
  palette: {
    light: ["#fbf7ea", "#12343a", "#96640a", "#1d6670", "#dc7a52"],
    dark: ["#041114", "#ecf4ef", "#f0d672", "#2f8f98", "#dc7a52"],
  },
  motion: "calm",
  render(content: Content): RenderResult {
    const files: Record<string, string> = {};
    const motifs = ["waves", "flow", "spiral", "network", "roses", "pulse", "grid"];

    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content);
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
          motifs[idx % motifs.length]
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
