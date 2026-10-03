import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, ptsPath, pic } from "../../lib/svg";

const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";

interface ThemeColors {
  bg1: string;
  bg2: string;
  fg: string;
  mute: string;
  acc: string;
  acc2: string;
  line: string;
  card: string;
  star: string;
  petals: string[];
  canopy: string[];
  coral: string;
  ground: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg1: "#070d3a",
    bg2: "#0c1a66",
    fg: "#eef0ff",
    mute: "#9fb0ee",
    acc: "#f5c15a",
    acc2: "#ff7a52",
    line: "#2a3da6",
    card: "#0b1560",
    star: "#ffffff",
    petals: ["#ffffff", "#e9c6e0", "#bcc8ff"],
    canopy: ["#e8eaff", "#c9d2ff", "#9fb0f0", "#f3d3ea", "#ffffff"],
    coral: "#ff7a52",
    ground: "#0a1352",
  },
  light: {
    bg1: "#f4f5ff",
    bg2: "#dfe5ff",
    fg: "#0f1a66",
    mute: "#4b5ca9",
    acc: "#d6502b",
    acc2: "#1f3fd1",
    line: "#b4c1f2",
    card: "#ffffff",
    star: "#1f3fd1",
    petals: ["#eaa8c9", "#9fb0f0", "#f4b49a"],
    canopy: ["#ffffff", "#d3dcff", "#aebdf5", "#f1c9e2", "#8ea4ec"],
    coral: "#e8603a",
    ground: "#cfd8fb",
  },
};

const STYLE = `<style>
.spin{transform-box:fill-box;transform-origin:center;animation:spin 90s linear infinite}
.spin.r{animation-direction:reverse;animation-duration:140s}
.spin.f{animation-duration:46s}
@keyframes spin{to{transform:rotate(360deg)}}
.tw{transform-box:fill-box;transform-origin:center;animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25;transform:scale(.6)}50%{opacity:1;transform:scale(1.15)}}
.glow{animation:glow 5s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.45}50%{opacity:1}}
.flick{animation:fl 2.8s ease-in-out infinite}
@keyframes fl{0%,100%{opacity:.7}30%{opacity:1}55%{opacity:.55}80%{opacity:.95}}
.ff{animation:ff linear infinite;opacity:0}
@keyframes ff{0%{opacity:0;transform:translate(0,0)}15%{opacity:1}85%{opacity:.9}100%{opacity:0;transform:translate(16px,-80px)}}
.fall{animation:fall linear infinite}
@keyframes fall{from{transform:translateY(-30px)}to{transform:translateY(520px)}}
.sway{transform-box:fill-box;transform-origin:center;animation:sway ease-in-out infinite alternate}
@keyframes sway{from{transform:translateX(-22px) rotate(-40deg)}to{transform:translateX(22px) rotate(40deg)}}
.breathe{transform-box:fill-box;transform-origin:center;animation:br 30s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1)}to{transform:scale(1.08)}}
.dots{stroke-dasharray:.1 16;stroke-linecap:round;animation:run 12s linear infinite}
@keyframes run{to{stroke-dashoffset:-161}}
.cursor{animation:cur 1.1s steps(1) infinite}
@keyframes cur{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.spin,.tw,.glow,.flick,.ff,.fall,.sway,.breathe,.dots,.cursor{animation:none}.ff{opacity:.6}}
</style>`;

function star4(x: number, y: number, s: number, col: string, op = 1, cls = "", delay = 0): string {
  const d = `M${f1(x)} ${f1(y - s)}Q${f1(x)} ${f1(y)} ${f1(x + s)} ${f1(y)}Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y + s)}Q${f1(x)} ${f1(y)} ${f1(x - s)} ${f1(y)}Q${f1(x)} ${f1(y)} ${f1(x)} ${f1(y - s)}Z`;
  const st = cls ? ` style="animation-delay:${(-delay).toFixed(1)}s;animation-duration:${(3 + (delay % 3)).toFixed(1)}s"` : "";
  return `<path class="${cls}" d="${d}" fill="${col}" opacity="${op}"${st}/>`;
}

const PETAL = "M0 -8C6 -6 7 4 0 9C-7 4 -6 -6 0 -8Z";
function petals(c: ThemeColors, n: number, xr: [number, number]): string {
  const o: string[] = [];
  for (let i = 0; i < n; i++) {
    const x = xr[0] + ((i * 47) % (xr[1] - xr[0]));
    const s = 0.7 + (i % 5) * 0.1;
    const col = c.petals[i % c.petals.length];
    const d = 18 + (i % 8);
    const sd = 4 + (i % 3);
    o.push(`<g transform="translate(${f1(x)} 0)"><g class="fall" style="animation-duration:${d}s;animation-delay:-${i * 1.5}s">
<g class="sway" style="animation-duration:${sd}s;animation-delay:-${i}s">
<path transform="rotate(${i * 25}) scale(${s})" d="${PETAL}" fill="${col}" opacity=".92"/></g></g></g>`);
  }
  return o.join("");
}

function fireflies(n: number, box: [number, number, number, number]): string {
  const [x0, y0, x1, y1] = box;
  const o: string[] = [];
  for (let i = 0; i < n; i++) {
    const x = x0 + ((i * 73) % (x1 - x0));
    const y = y0 + ((i * 51) % (y1 - y0));
    const d = 8 + (i % 6);
    o.push(`<g class="ff" style="animation-duration:${d}s;animation-delay:-${i * 1.2}s">
<circle cx="${f1(x)}" cy="${f1(y)}" r="5" fill="#ffd57a" opacity=".25"/><circle cx="${f1(x)}" cy="${f1(y)}" r="1.9" fill="#fff0b8"/></g>`);
  }
  return o.join("");
}

function runeRing(c: ThemeColors, r: number, n = 24, col?: string): string {
  const ringCol = col || c.acc;
  const o: string[] = [`<circle r="${r}" fill="none" stroke="${ringCol}" stroke-width=".9" opacity=".7"/>`];
  for (let i = 0; i < n; i++) {
    const a = (2 * Math.PI * i) / n;
    const x = r * Math.cos(a);
    const y = r * Math.sin(a);
    const k = i % 4;
    const deg = (a * 180) / Math.PI;
    if (k === 0) o.push(`<circle cx="${f1(x)}" cy="${f1(y)}" r="2.3" fill="none" stroke="${ringCol}"/>`);
    else if (k === 1) o.push(`<path transform="translate(${f1(x)} ${f1(y)}) rotate(${f1(deg)})" d="M-3 0L0 -3.4L3 0L0 3.4Z" fill="${ringCol}"/>`);
    else if (k === 2) o.push(`<path transform="translate(${f1(x)} ${f1(y)}) rotate(${f1(deg + 90)})" d="M0 -4L3.4 3L-3.4 3Z" fill="none" stroke="${ringCol}"/>`);
    else o.push(`<path transform="translate(${f1(x)} ${f1(y)}) rotate(${f1(deg)})" d="M-4 0H4M0 -2.5V2.5" stroke="${ringCol}"/>`);
  }
  return o.join("");
}

function octagram(R: number, col: string): string {
  const p: [number, number][] = [];
  for (let i = 0; i < 8; i++) {
    p.push([R * Math.cos((2 * Math.PI * i) / 8 - Math.PI / 2), R * Math.sin((2 * Math.PI * i) / 8 - Math.PI / 2)]);
  }
  const order = [0, 3, 6, 1, 4, 7, 2, 5];
  return `<path d="M${order.map((idx) => `${f1(p[idx][0])} ${f1(p[idx][1])}`).join("L")}Z" fill="none" stroke="${col}" stroke-width=".9" opacity=".6"/>`;
}

function defs(c: ThemeColors): string {
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".95"/><stop offset=".4" stop-color="#ffb347" stop-opacity=".4"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
<radialGradient id="aura"><stop offset=".55" stop-color="${c.acc2}" stop-opacity="0"/><stop offset=".8" stop-color="${c.acc2}" stop-opacity=".22"/><stop offset="1" stop-color="${c.acc2}" stop-opacity="0"/></radialGradient>
<linearGradient id="nm" x1="0" x2="1"><stop offset="0" stop-color="${c.fg}"/><stop offset="1" stop-color="${c.acc}"/></linearGradient>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string): string {
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">
${STYLE}${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>${body}
<path d="M.5 0V${h}M${w - 0.5} 0V${h}" stroke="${c.line}"/></svg>`;
}

function sky(c: ThemeColors, w: number, h: number, n: number): string {
  const o: string[] = [];
  for (let i = 0; i < n; i++) {
    const x = 15 + ((i * 89) % (w - 30));
    const y = 10 + ((i * 47) % (h - 20));
    if (x < 440 && y > 90 && y < 330) continue;
    o.push(star4(x, y, 2 + (i % 3), c.star, 0.7, "tw", i * 0.4));
  }
  return o.join("");
}

function divider(c: ThemeColors, y: number, w = 900): string {
  const pts: [number, number][] = [];
  for (let x = 70; x <= w - 60; x += 95) {
    pts.push([x, y + ((x / 95) % 2 === 0 ? -5 : 5)]);
  }
  const d = ptsPath(pts);
  const o = [`<path d="${d}" fill="none" stroke="${c.line}" stroke-width="1.2"/><path class="dots" d="${d}" fill="none" stroke="${c.acc}" stroke-width="2.2"/>`];
  pts.forEach(([a, b], i) => {
    o.push(star4(a, b, i % 3 === 0 ? 4.5 : 3, i % 3 === 0 ? c.acc : c.star, 0.95, "tw", i * 1.3));
  });
  return o.join("");
}

function heading(c: ThemeColors, y: number, idx: string, label: string, x = 60): string {
  return (
    star4(x, y, 8, c.acc, 1, "tw", 1) +
    `<text x="${x + 22}" y="${y + 4}" font-size="12" letter-spacing="2" fill="${c.mute}">${idx} /</text>
<text x="${x + 62}" y="${y + 4}" font-size="12" font-weight="700" letter-spacing="2" fill="${c.fg}">${escapeXml(label)}</text>`
  );
}

function lantern(c: ThemeColors, x: number, y: number, top = 0): string {
  return `<path d="M${x} ${top}V${y - 18}" stroke="${c.mute}" stroke-opacity=".7"/>
<circle class="flick" cx="${x}" cy="${y}" r="70" fill="url(#warm)"/>
<g transform="translate(${x} ${y})"><g class="spin f">${runeRing(c, 34, 12)}</g></g>
<rect x="${x - 8}" y="${y - 18}" width="16" height="4" rx="2" fill="${c.mute}"/>
<ellipse cx="${x}" cy="${y}" rx="10" ry="13" fill="#ffb347"/><ellipse class="flick" cx="${x}" cy="${y}" rx="5" ry="8" fill="#fff0b8"/>
<rect x="${x - 8}" y="${y + 13}" width="16" height="4" rx="2" fill="${c.mute}"/>`;
}

function hero(c: ThemeColors, content: Content, heroImg: string): string {
  const cx = 680, cy = 235, R = 170;
  const lx = cx - 20, ly = cy - 40;
  let b = sky(c, 900, 470, 70);

  const cons: [number, number][] = [[300, 40], [352, 66], [410, 48], [452, 92], [402, 118]];
  b += `<path d="M${cons.map(([x, y]) => `${x} ${y}`).join("L")}" fill="none" stroke="${c.mute}" stroke-opacity=".5" stroke-dasharray="3 5"/>`;
  b += cons.map(([x, y], i) => star4(x, y, 4.5, c.acc, 1, "tw", i * 1.1)).join("");

  b += `<circle cx="${cx}" cy="${cy}" r="${R + 60}" fill="url(#aura)" class="glow"/>`;
  b += `<g transform="translate(${cx} ${cy})"><g class="spin r">${octagram(R + 26, c.acc)}</g>
<g class="spin">${runeRing(c, R + 36, 28)}</g><g class="spin f">${runeRing(c, R + 14, 20, c.acc2)}</g>
<g class="spin f"><circle cx="${R + 36}" cy="0" r="3.4" fill="#ffd57a"/><circle cx="-${R + 36}" cy="0" r="3.4" fill="#ffd57a"/></g></g>`;

  b += `<defs><clipPath id="moon"><circle cx="${cx}" cy="${cy}" r="${R}"/></clipPath></defs>
<g clip-path="url(#moon)"><g class="breathe">
<image x="${cx - R}" y="${cy - R}" width="${2 * R}" height="${2 * R}" href="${heroImg}" xlink:href="${heroImg}"/>
</g><circle class="flick" cx="${f1(lx)}" cy="${f1(ly)}" r="62" fill="url(#warm)"/></g>
<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="${c.acc}" stroke-width="2"/>
<circle cx="${cx}" cy="${cy}" r="${R + 6}" fill="none" stroke="${c.acc}" stroke-opacity=".4" stroke-dasharray="1 5"/>`;

  b += star4(66, 34, 8, c.acc, 1, "tw", 0.5);
  b += `<text x="84" y="38" font-size="12" fill="${c.mute}">${escapeXml(content.handle)} <tspan fill="${c.line}">/</tspan> README</text>
<path d="M40 56H420" stroke="${c.line}"/>
<text x="60" y="122" font-size="13" letter-spacing="3" fill="${c.mute}">HI, I&apos;M</text>
<text x="58" y="172" font-size="40" font-family="${SERIF}" font-style="italic" fill="url(#nm)">${escapeXml(content.name)}</text>
<text x="60" y="216" font-size="16" font-weight="700" letter-spacing="3" fill="${c.acc}">${escapeXml(content.role.toUpperCase())}</text>
<rect class="cursor" x="308" y="202" width="9" height="16" fill="${c.acc}"/>
<text x="60" y="258" font-size="13" letter-spacing="1" fill="${c.fg}" xml:space="preserve">${escapeXml(content.pillars)}</text>
<rect x="60" y="274" width="36" height="2" fill="${c.acc}"/>`;

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${306 + i * 20}" font-size="12.5" fill="${c.mute}">${escapeXml(t)}</text>`;
  });

  b += divider(c, 448) + fireflies(14, [480, 120, 880, 420]) + petals(c, 12, [300, 890]);
  return wrap(900, 470, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const b = `<rect x=".75" y=".75" width="${w - 1.5}" height="38.5" rx="19" fill="${c.card}" stroke="${c.acc}" stroke-opacity=".85"/>
${star4(26, 20, 7, c.acc, 1, "tw", 1)}
<text x="44" y="24.5" font-size="12" letter-spacing="1.2" fill="${c.fg}">${escapeXml(label.toUpperCase())}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${MONO}">${STYLE}${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = sky(c, 900, 290, 26) + heading(c, 42, "01", "ABOUT");
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

  b += heading(c, 42, "02", "MY JOURNEY", 480);
  const ys = content.journey.slice(0, 5).map((_, i) => 96 + i * 30);
  if (ys.length) {
    b += `<path d="M490 ${ys[0] - 4}V${ys[ys.length - 1] - 4}" stroke="${c.acc}" stroke-opacity=".6" stroke-dasharray="3 4"/>`;
  }
  content.journey.slice(0, 5).forEach((j, i) => {
    const y = ys[i];
    b += `${star4(490, y - 4, 6, c.acc, 1, "tw", i * 1.2)}
<text x="512" y="${y}" font-size="13" fill="${c.fg}">${escapeXml(j.lang)}</text>
<path d="M640 ${y - 4}H664M659 ${y - 8}L664 ${y - 4}L659 ${y}" fill="none" stroke="${c.acc2}"/>
<text x="682" y="${y}" font-size="13" fill="${c.mute}">${escapeXml(j.area)}</text>`;
  });

  b += divider(c, 274);
  return wrap(900, 290, c, b);
}

function skills(c: ThemeColors, content: Content): string {
  let b = sky(c, 900, 270, 24) + heading(c, 38, "03", "TECHNOLOGIES &amp; SKILLS");
  content.skills.slice(0, 12).forEach((s, i) => {
    const cx = 40 + 68.3 + (i % 6) * 136.7;
    const cy = 92 + Math.floor(i / 6) * 100;
    b += `<circle cx="${f1(cx)}" cy="${cy}" r="29" fill="${c.card}" fill-opacity=".85" stroke="${c.line}" stroke-width="1.4"/>
<g transform="translate(${f1(cx)} ${cy})"><g class="spin${i % 2 !== 0 ? " r" : ""}"><circle r="35" fill="none" stroke="${c.acc}" stroke-width="1.2" stroke-dasharray="1 6.2" stroke-linecap="round"/>
${star4(35, 0, 3.5, c.acc)}${star4(-35, 0, 3.5, c.acc)}</g></g>
<text x="${f1(cx)}" y="${cy + 5}" font-size="14" font-weight="700" text-anchor="middle" fill="${c.acc}">${escapeXml(s.mono)}</text>
<text x="${f1(cx)}" y="${cy + 54}" font-size="10.5" text-anchor="middle" fill="${c.fg}">${escapeXml(s.label)}</text>`;
  });
  b += divider(c, 250);
  return wrap(900, 268, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 60, c, sky(c, 900, 60, 14) + heading(c, 34, "04", "SELECTED PROJECTS"));
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
  const w = 208, h = 198;
  const arch = "M8 100V56A96 48 0 0 1 200 56V100Z";
  let b = `<defs><clipPath id="cl"><path d="${arch}"/></clipPath></defs>
<rect x=".75" y=".75" width="${w - 1.5}" height="${h - 1.5}" rx="14" fill="${c.card}" fill-opacity=".9" stroke="${c.line}" stroke-width="1.5"/>
<image x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)" href="${cardImg}" xlink:href="${cardImg}"/>
<path d="${arch}" fill="none" stroke="${c.acc}" stroke-width="1.4"/>
<path class="dots" d="${arch}" fill="none" stroke="${c.acc}" stroke-width="2.4"/>
${star4(104, 8, 5, c.acc, 1, "tw", idx)}${star4(182, 26, 3, c.star, 0.9, "tw", idx + 2)}
<text x="16" y="124" font-size="13.5" font-weight="700" fill="${c.fg}">${escapeXml(title)}</text>
<text x="16" y="143" font-size="10.5" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="157" font-size="10.5" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let x = 16;
  tags.slice(0, 4).forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${f1(x)}" y="171" width="${f1(cw)}" height="17" rx="8.5" fill="none" stroke="${c.line}"/>
<text x="${f1(x + cw / 2)}" y="182.5" font-size="8.5" text-anchor="middle" fill="${c.acc}">${escapeXml(t)}</text>`;
    x += cw + 5;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${MONO}">${STYLE}${defs(c)}${b}</svg>`;
}

function footer(c: ThemeColors, content: Content): string {
  let b = sky(c, 900, 140, 36);
  b += lantern(c, 120, 118) + lantern(c, 780, 118);

  // Frosted canopy hills
  for (let i = 0; i < 400; i++) {
    const x = (i * 19) % 900;
    const hillY = 176 + 22 * Math.sin(x / 85) + 10 * Math.sin(x / 33 + 1);
    const y = hillY + ((i * 7) % Math.max(1, 262 - hillY));
    const col = (i % 20 === 0) ? c.coral : c.canopy[i % c.canopy.length];
    b += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${(2.5 + (i % 4) * 0.8).toFixed(1)}" fill="${col}" opacity="${(0.6 + (i % 4) * 0.1).toFixed(2)}"/>`;
  }

  b += `<text x="450" y="52" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle" fill="${c.acc}" xml:space="preserve">${escapeXml(content.footer.line1.toUpperCase())}</text>
<text x="450" y="76" font-size="10.5" letter-spacing="1" text-anchor="middle" fill="${c.mute}" xml:space="preserve">${escapeXml(content.footer.line2)}</text>`;

  b += fireflies(12, [40, 90, 860, 230]) + petals(c, 7, [60, 840]);
  return wrap(900, 262, c, b);
}

export const moongateStyle: StyleModule = {
  id: "moongate",
  name: "Moon Gate",
  keywords: ["night", "magic", "rune rings"],
  palette: {
    light: ["#f4f5ff", "#0f1a66", "#d6502b", "#1f3fd1", "#b4c1f2"],
    dark: ["#070d3a", "#eef0ff", "#f5c15a", "#ff7a52", "#2a3da6"],
  },
  motion: "lively",
  image: { file: "source.jpg", note: "Night Garden portal & lanterns" },
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/moongate/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [60, 600, 500, 1040], [620, 620], 0.82);

    const cropBoxes: [number, number, number, number][] = [
      [400, 60, 600, 154],
      [100, 300, 300, 394],
      [100, 800, 300, 894],
      [230, 770, 430, 864],
      [380, 290, 580, 384],
      [440, 690, 640, 784],
      [150, 480, 350, 574],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 188], 0.8)
    );

    const files: Record<string, string> = {};
    for (const theme of ["dark", "light"] as const) {
      const c = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(c, content, heroCrop);
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
