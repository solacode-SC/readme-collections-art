import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','Book Antiqua','DejaVu Serif',serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const CJK = "'KaiTi','STKaiti','Kaiti SC','AR PL UKai CN','Noto Serif SC','Songti SC','SimSun',serif";

interface ThemeColors {
  bg1: string;
  bg2: string;
  fg: string;
  ink: string;
  mute: string;
  indigo: string;
  verm: string;
  line: string;
  card: string;
  mount: string;
  mount2: string;
  green: string;
  paper: string;
  fibre: string;
  bloom: string[];
  petal: string[];
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  light: {
    bg1: "#f3e9cd",
    bg2: "#e4d4a9",
    fg: "#26211b",
    ink: "#23201c",
    mute: "#6a5f4d",
    indigo: "#29486f",
    verm: "#bf2a22",
    line: "#b9a77a",
    card: "#f8f0d6",
    mount: "#b3c3ca",
    mount2: "#8ea5b2",
    green: "#3a6b4a",
    paper: "#f6edd2",
    fibre: "0 0 0 0 .45  0 0 0 0 .33  0 0 0 0 .15  0 0 0 .5 0",
    bloom: ["#bf2a22", "#f8f1df", "#e9a8a0"],
    petal: ["#f4d6d0", "#e9a8a0", "#bf2a22"],
  },
  dark: {
    bg1: "#181d28",
    bg2: "#0d1017",
    fg: "#efe5cb",
    ink: "#d9cfb6",
    mute: "#a99f88",
    indigo: "#93b3d9",
    verm: "#d6402f",
    line: "#3b4662",
    card: "#1b2130",
    mount: "#2a3c55",
    mount2: "#42597a",
    green: "#6aa77e",
    paper: "#efe5cb",
    fibre: "0 0 0 0 .9  0 0 0 0 .85  0 0 0 0 .7  0 0 0 .22 0",
    bloom: ["#d6402f", "#efe3cf", "#d99a96"],
    petal: ["#efe3cf", "#d99a96", "#d6402f"],
  },
};

const STYLE = `<style>
.sway{transform-origin:710px 8px;animation:sway 11s ease-in-out infinite alternate}
@keyframes sway{from{transform:rotate(-.45deg)}to{transform:rotate(.45deg)}}
.drift{animation:drift 60s ease-in-out infinite alternate}
@keyframes drift{from{transform:translateX(-26px)}to{transform:translateX(26px)}}
.pfall{animation:pfall linear infinite}
@keyframes pfall{from{transform:translateY(-30px)}to{transform:translateY(560px)}}
.psway{transform-box:fill-box;transform-origin:center;animation:psway ease-in-out infinite alternate}
@keyframes psway{from{transform:translateX(-26px) rotate(-30deg)}to{transform:translateX(26px) rotate(30deg)}}
.rip{transform-box:fill-box;transform-origin:center;animation:rip 9s ease-out infinite;opacity:0}
@keyframes rip{0%{transform:scale(.2);opacity:0}15%{opacity:.7}100%{transform:scale(1.6);opacity:0}}
.sun{animation:sun 12s ease-in-out infinite}
@keyframes sun{0%,100%{opacity:.05}50%{opacity:.34}}
.mist{animation:mist 40s ease-in-out infinite alternate}
@keyframes mist{from{transform:translateX(-40px)}to{transform:translateX(40px)}}
.wave{animation:wave 26s linear infinite}
@keyframes wave{to{transform:translateX(-48px)}}
.breath{transform-box:fill-box;transform-origin:center;animation:br 14s ease-in-out infinite alternate}
@keyframes br{from{transform:scale(1)}to{transform:scale(1.03)}}
@media (prefers-reduced-motion:reduce){.sway,.drift,.pfall,.psway,.rip,.sun,.mist,.wave,.breath{animation:none}}
</style>`;

function defs(c: ThemeColors): string {
  return `<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c.bg1}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".65" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="${c.line}" stop-opacity=".28"/></radialGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#ff6a4a" stop-opacity=".9"/><stop offset="1" stop-color="#ff6a4a" stop-opacity="0"/></radialGradient>
<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012 .4" numOctaves="3" seed="5"/><feColorMatrix values="${c.fibre}"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 .3  0 0 0 0 .22  0 0 0 0 .1  0 0 0 .13 0"/></filter>
<filter id="rough" x="-6%" y="-6%" width="112%" height="112%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="3" seed="7" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="3.4" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="wob" x="-4%" y="-20%" width="108%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="2" seed="3" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="1.6" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="paint" x="-4%" y="-4%" width="108%" height="108%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="3" seed="2" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="d"/><feColorMatrix in="d" type="saturate" values=".9"/></filter>
<pattern id="sei" width="24" height="12" patternUnits="userSpaceOnUse"><g fill="none" stroke="${c.mount2}" stroke-width=".8"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="4"/><circle cx="0" cy="6" r="10"/><circle cx="0" cy="6" r="7"/><circle cx="0" cy="6" r="4"/><circle cx="24" cy="6" r="10"/><circle cx="24" cy="6" r="7"/><circle cx="24" cy="6" r="4"/></g></pattern>
</defs>`;
}

function wrap(w: number, h: number, c: ThemeColors, body: string, edge = true): string {
  const side = edge ? `<path d="M.5 0V${h}M${w - 0.5} 0V${h}" stroke="${c.line}"/>` : "";
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${SERIF}">
${STYLE}${defs(c)}<rect width="${w}" height="${h}" fill="url(#bg)"/>
<rect width="${w}" height="${h}" filter="url(#paper)"/><rect width="${w}" height="${h}" filter="url(#grain)"/>
<rect width="${w}" height="${h}" fill="url(#vig)"/>${body}${side}</svg>`;
}

function taper(pts: [number, number][], w0: number, w1: number): string {
  const n = pts.length;
  const L: [number, number][] = [];
  const R: [number, number][] = [];
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1);
    const w = w0 * (1 - t) + w1 * t;
    const [x, y] = pts[i];
    const [xa, ya] = pts[Math.max(i - 1, 0)];
    const [xb, yb] = pts[Math.min(i + 1, n - 1)];
    const dx = xb - xa;
    const dy = yb - ya;
    const l = Math.hypot(dx, dy) || 1;
    const nx = -dy / l;
    const ny = dx / l;
    L.push([x + (nx * w) / 2, y + (ny * w) / 2]);
    R.push([x - (nx * w) / 2, y - (ny * w) / 2]);
  }
  const all = [...L, ...R.reverse()];
  return "M" + all.map(([a, b]) => `${f1(a)} ${f1(b)}`).join("L") + "Z";
}

function curve(x0: number, y0: number, x1: number, y1: number, bend: number, n = 14): [number, number][] {
  const pts: [number, number][] = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const x = x0 + (x1 - x0) * t;
    const y = y0 + (y1 - y0) * t + bend * Math.sin(t * Math.PI);
    pts.push([x, y]);
  }
  return pts;
}

function brush(c: ThemeColors, x0: number, y0: number, x1: number, y1: number, w0 = 3, w1 = 0.5, bend = 0, col?: string, op = 0.9): string {
  return `<path d="${taper(curve(x0, y0, x1, y1, bend, 16), w0, w1)}" fill="${col || c.ink}" opacity="${op}" filter="url(#wob)"/>`;
}

function blossom(c: ThemeColors, x: number, y: number, R: number, col?: string): string {
  const petalCol = col || c.bloom[0];
  const stroke = petalCol !== c.bloom[0] ? c.verm : c.ink;
  const o: string[] = [];
  for (let i = 0; i < 5; i++) {
    const a = (i * 72 * Math.PI) / 180;
    o.push(`<circle cx="${f1(x + R * 0.55 * Math.cos(a))}" cy="${f1(y + R * 0.55 * Math.sin(a))}" r="${f1(R * 0.5)}" fill="${petalCol}" stroke="${stroke}" stroke-opacity=".55" stroke-width=".6"/>`);
  }
  o.push(`<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(R * 0.2)}" fill="#e0b13a"/>`);
  return o.join("");
}

function branch(c: ThemeColors, x0: number, y0: number, x1: number, y1: number, seed = 1, nBlooms = 7, w0 = 5, bend = -14, sparse = false): string {
  const o: string[] = [];
  const main = curve(x0, y0, x1, y1, bend, 22);
  o.push(`<path d="${taper(main, w0, 0.9)}" fill="${c.ink}" opacity=".92" filter="url(#wob)"/>`);
  const tips: [number, number][] = [main[main.length - 1]];

  const count = sparse ? 3 : 5;
  for (let k = 0; k < count; k++) {
    const i = Math.floor(main.length * (0.15 + k * 0.17));
    const [bx, by] = main[i];
    const ang = (((k % 2 === 0 ? -62 : 58) * Math.PI) / 180) + Math.atan2(y1 - y0, x1 - x0);
    const ln = 28 + (k * 4);
    const ex = bx + ln * Math.cos(ang);
    const ey = by + ln * Math.sin(ang);
    const tw = curve(bx, by, ex, ey, 2, 8);
    o.push(`<path d="${taper(tw, 2.4, 0.5)}" fill="${c.ink}" opacity=".9" filter="url(#wob)"/>`);
    tips.push([ex, ey]);
  }

  tips.slice(0, nBlooms).forEach(([tx, ty], k) => {
    o.push(blossom(c, tx, ty, 5.2, c.bloom[k % c.bloom.length]));
  });

  for (let k = 0; k < Math.floor(nBlooms / 2); k++) {
    const i = Math.min(main.length - 2, Math.max(2, 3 + k * 4));
    const [bx, by] = main[i];
    o.push(`<circle cx="${f1(bx - 3)}" cy="${f1(by - 4)}" r="2" fill="${c.verm}"/>`);
  }
  return o.join("");
}

function divider(c: ThemeColors, y: number): string {
  return branch(c, 40, y + 6, 860, y - 4, 1, 6, 2.4, -8, true);
}

function handText(txt: string, x: number, y: number, size: number, fill: string, weight = "400", ls = 0): string {
  return `<text x="${x}" y="${y}" font-size="${size}" font-weight="${weight}" fill="${fill}" letter-spacing="${ls}">${escapeXml(txt)}</text>`;
}

function seal(c: ThemeColors, x: number, y: number, s: number, glyph: string, rot = 0): string {
  return `<g transform="rotate(${f1(rot)} ${f1(x + s / 2)} ${f1(y + s / 2)})" filter="url(#rough)"><rect x="${x}" y="${y}" width="${s}" height="${s}" fill="${c.verm}"/>
<rect x="${x + s * 0.07}" y="${y + s * 0.07}" width="${s * 0.86}" height="${s * 0.86}" fill="none" stroke="${c.paper}" stroke-opacity=".75" stroke-width="${Math.max(1, s * 0.035).toFixed(1)}"/>
<text x="${x + s / 2}" y="${y + s * 0.72}" font-size="${f1(s * 0.6)}" font-family="${CJK}" font-weight="700" text-anchor="middle" fill="${c.paper}">${escapeXml(glyph)}</text></g>`;
}

const NUM_HEAD = ["壹", "貳", "參", "肆"];
const NUM_CARD = ["一", "二", "三", "四", "五", "六", "七", "八"];

function heading(c: ThemeColors, y: number, idx: number, label: string, x = 60): string {
  return (
    seal(c, x, y - 14, 24, NUM_HEAD[idx] || "壹", 0) +
    handText(label, x + 36, y + 5, 15, c.fg, "700", 3) +
    brush(c, x, y + 18, x + 300, y + 20, 2.6, 0.4, 1.5, c.indigo, 0.75)
  );
}

function petals(c: ThemeColors, n: number, xr: [number, number]): string {
  const o: string[] = [];
  const [xMin, xMax] = xr;
  for (let i = 0; i < n; i++) {
    const x = xMin + ((i * 89) % (xMax - xMin));
    const s = 0.7 + ((i * 13) % 40) / 100;
    const col = c.petal[i % c.petal.length];
    const d = 36 + (i * 4) % 18;
    const sd = 5 + (i * 2) % 4;
    o.push(`<g transform="translate(${f1(x)} 0)"><g class="pfall" style="animation-duration:${d}s;animation-delay:-${i * 3}s">
<g class="psway" style="animation-duration:${sd}s;animation-delay:-${i * 2}s">
<path transform="rotate(${(i * 50) % 180}) scale(${s.toFixed(2)})" d="M0 -7C6 -7 7 3 0 8C-7 3 -6 -7 0 -7Z" fill="${col}" opacity=".85"/></g></g></g>`);
  }
  return o.join("");
}

function cloud(c: ThemeColors, x: number, y: number, k: number, col: string, op = 0.2): string {
  const cs: [number, number, number][] = [[0, 0, 16], [20, -8, 20], [44, -2, 17], [62, 6, 12], [-16, 8, 11]];
  const o = cs.map(([a, b, r]) => `<circle cx="${f1(x + a * k)}" cy="${f1(y + b * k)}" r="${f1(r * k)}"/>`).join("");
  return `<g class="mist" fill="${col}" opacity="${op}">${o}</g>`;
}

function hero(c: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const W = 900, H = 540;
  let b = branch(c, -10, 520, 340, 430, 4, 8, 6, -20);
  b += cloud(c, 380, 66, 0.8, c.indigo, 0.16) + cloud(c, 420, 470, 0.7, c.indigo, 0.13);

  // Top bar + avatar
  b += `<defs><clipPath id="av"><circle cx="64" cy="48" r="14"/></clipPath></defs>
<image x="50" y="34" width="28" height="28" clip-path="url(#av)" href="${avatarImg}" xlink:href="${avatarImg}"/>
<circle cx="64" cy="48" r="14" fill="none" stroke="${c.ink}" stroke-width="1.4" filter="url(#wob)"/>
<text x="88" y="52" font-size="12" font-family="${MONO}" fill="${c.mute}">${escapeXml(content.handle)} <tspan fill="${c.verm}">/</tspan> README</text>`;

  // Copy
  b += brush(c, 60, 124, 84, 124, 2.4, 0.5, 0, c.verm);
  b += `<text x="94" y="129" font-size="13" letter-spacing="4" fill="${c.mute}">HI, I'M</text>`;
  b += handText(content.name, 58, 186, 36, c.ink, "700");
  b += handText(content.role.toUpperCase(), 60, 232, 15, c.indigo, "700", 5);
  b += `<text x="60" y="272" font-size="14" letter-spacing="1.5" fill="${c.fg}" xml:space="preserve">${escapeXml(content.pillars)}</text>`;
  b += brush(c, 60, 292, 250, 294, 3, 0.4, 2, c.ink, 0.8);

  content.tagline.forEach((t, i) => {
    b += `<text x="60" y="${328 + i * 23}" font-size="14" font-style="italic" fill="${c.mute}">${escapeXml(t)}</text>`;
  });

  // Vertical calligraphy + seal
  if (content.options.useCJK) {
    const kanji = ["築", "夢"];
    kanji.forEach((ch, i) => {
      b += `<text x="516" y="${176 + i * 58}" font-size="46" font-family="${CJK}" font-weight="700" text-anchor="middle" fill="${c.ink}" opacity=".9" filter="url(#wob)">${ch}</text>`;
    });
  }
  b += seal(c, 494, 300, 44, content.options.useCJK ? "碼" : "SC", 2);

  // Hanging scroll
  const px = 586, py = 92, pw = 248, ph = 372;
  const sx = pw / 736;
  const sunX = px + 365 * sx;
  const sunY = py + 355 * sx;
  const lakeX = px + 372 * sx;
  const lakeY = py + 610 * sx;

  let sc = `<g class="sway">
<path d="M710 8L572 40M710 8L848 40" stroke="${c.ink}" stroke-width="1.2"/><circle cx="710" cy="8" r="3.2" fill="none" stroke="${c.ink}" stroke-width="1.4"/>
<rect x="562" y="36" width="296" height="10" rx="5" fill="${c.ink}"/><circle cx="560" cy="41" r="6" fill="${c.verm}"/><circle cx="860" cy="41" r="6" fill="${c.verm}"/>
<rect x="570" y="46" width="280" height="452" fill="${c.mount}" stroke="${c.ink}" stroke-width="1"/><rect x="570" y="46" width="280" height="452" fill="url(#sei)"/>
<rect x="576" y="52" width="268" height="440" fill="none" stroke="${c.paper}" stroke-opacity=".7"/>
<rect x="${px - 8}" y="${py - 8}" width="${pw + 16}" height="${ph + 16}" fill="${c.paper}" stroke="${c.ink}" stroke-opacity=".55"/>
<defs><clipPath id="pw"><rect x="${px}" y="${py}" width="${pw}" height="${ph}"/></clipPath></defs>
<g clip-path="url(#pw)"><image x="${px}" y="${py}" width="${pw}" height="${ph}" href="${heroImg}" xlink:href="${heroImg}" filter="url(#paint)"/>
<circle class="sun" cx="${f1(sunX)}" cy="${f1(sunY)}" r="52" fill="url(#sunglow)"/>
<g fill="none" stroke="#fff" stroke-width="1.2"><ellipse class="rip" cx="${f1(lakeX)}" cy="${f1(lakeY)}" rx="46" ry="10"/></g>
<rect x="${px}" y="${py}" width="${pw}" height="${ph}" fill="#c9b27a" opacity=".12" style="mix-blend-mode:multiply"/></g>
<rect x="${px}" y="${py}" width="${pw}" height="${ph}" fill="none" stroke="${c.ink}" stroke-width="1.2" filter="url(#wob)"/>`;

  if (content.options.useCJK) {
    sc += `<text x="${px + 14}" y="${py + ph + 30}" font-size="13" font-family="${CJK}" letter-spacing="6" fill="${c.ink}" opacity=".85">靜水流深</text>`;
  }
  sc += seal(c, px + pw - 30, py + ph + 14, 24, content.options.useCJK ? "碼" : "SC", 1);
  sc += `<rect x="562" y="498" width="296" height="12" rx="6" fill="${c.ink}"/><circle cx="560" cy="504" r="6" fill="${c.verm}"/><circle cx="860" cy="504" r="6" fill="${c.verm}"/></g>`;

  b += sc + petals(c, 9, [300, 860]) + divider(c, 526);
  return wrap(W, H, c, b);
}

function button(c: ThemeColors, label: string): string {
  const w = 150;
  const glyphMap: Record<string, string> = { GitHub: "碼", LinkedIn: "鏈", Portfolio: "作" };
  const glyph = glyphMap[label] || "碼";
  const b = `<rect x="2" y="2" width="${w - 4}" height="36" fill="${c.card}" stroke="${c.ink}" stroke-width="1.4" filter="url(#wob)"/>
<rect x="8" y="9" width="22" height="22" fill="${c.verm}" filter="url(#rough)"/><text x="19" y="25.5" font-size="14" font-family="${CJK}" font-weight="700" text-anchor="middle" fill="${c.paper}">${glyph}</text>
<text x="40" y="24.5" font-size="12" letter-spacing="2" fill="${c.fg}">${escapeXml(label.toUpperCase())}</text>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 40" width="${w}" height="40" font-family="${SERIF}">${defs(c)}${b}</svg>`;
}

function about(c: ThemeColors, content: Content): string {
  let b = heading(c, 42, 0, "ABOUT");
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
    b += `<text x="60" y="${92 + i * 23}" font-size="14" fill="${c.fg}" xml:space="preserve">${escapeXml(line)}</text>`;
  });

  b += brush(c, 452, 74, 452, 246, 1.8, 0.6, 4, c.ink, 0.55);
  b += heading(c, 42, 1, "MY JOURNEY", 480);

  content.journey.slice(0, 5).forEach((j, i) => {
    const y = 98 + i * 30;
    b += `<circle cx="490" cy="${y - 4}" r="3.6" fill="${c.verm}" filter="url(#wob)"/>
<text x="506" y="${y}" font-size="14" fill="${c.fg}">${escapeXml(j.lang)}</text>
${brush(c, 612, y - 4, 690, y - 5, 1.8, 0.4, 1, c.ink, 0.6)}
<text x="702" y="${y}" font-size="14" font-style="italic" fill="${c.mute}">${escapeXml(j.area)}</text>`;
  });

  b += divider(c, 276) + petals(c, 3, [500, 860]);
  return wrap(900, 296, c, b);
}

function skills(c: ThemeColors, content: Content): string {
  let b = heading(c, 40, 2, "TECHNOLOGIES &amp; SKILLS");
  content.skills.slice(0, 12).forEach((s, i) => {
    const cx = 40 + 68.3 + (i % 6) * 136.7;
    const cy = 94 + Math.floor(i / 6) * 100;
    const sz = 62;
    b += `<g transform="rotate(${((i * 3) % 5) - 2} ${f1(cx)} ${cy})" filter="url(#rough)">
<rect x="${f1(cx - sz / 2)}" y="${cy - sz / 2}" width="${sz}" height="${sz}" fill="${c.verm}"/>
<rect x="${f1(cx - sz / 2 + 5)}" y="${cy - sz / 2 + 5}" width="${sz - 10}" height="${sz - 10}" fill="none" stroke="${c.paper}" stroke-opacity=".7" stroke-width="1.6"/>
<text x="${f1(cx)}" y="${cy + 8}" font-size="22" font-weight="700" text-anchor="middle" fill="${c.paper}">${escapeXml(s.mono)}</text></g>
<text x="${f1(cx)}" y="${cy + 50}" font-size="12" font-style="italic" text-anchor="middle" fill="${c.fg}">${escapeXml(s.label)}</text>`;
  });

  b += divider(c, 272) + petals(c, 3, [60, 840]);
  return wrap(900, 292, c, b);
}

function projectsTitle(c: ThemeColors): string {
  return wrap(900, 60, c, heading(c, 32, 3, "SELECTED PROJECTS"));
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
  let b = `<rect x="3" y="3" width="${w - 6}" height="${h - 6}" fill="${c.card}" stroke="${c.ink}" stroke-width="1.6" filter="url(#wob)"/>
<rect x="8" y="8" width="${w - 16}" height="${h - 16}" fill="none" stroke="${c.ink}" stroke-opacity=".35" filter="url(#wob)"/>
<image x="14" y="14" width="180" height="82" preserveAspectRatio="xMidYMid slice" href="${cardImg}" xlink:href="${cardImg}" filter="url(#paint)"/>
<rect x="14" y="14" width="180" height="82" fill="#c9b27a" opacity=".12" style="mix-blend-mode:multiply"/>
${seal(c, 168, 8, 24, NUM_CARD[idx] || String(idx + 1), -1)}
${handText(title, 16, 122, 15, c.ink, "700")}
<text x="16" y="141" font-size="11.5" font-style="italic" fill="${c.mute}">${escapeXml(d1)}</text>
<text x="16" y="156" font-size="11.5" font-style="italic" fill="${c.mute}">${escapeXml(d2)}</text>`;

  let x = 16;
  tags.slice(0, 3).forEach((t) => {
    const cw = t.length * 5.1 + 10;
    b += `<rect x="${f1(x)}" y="169" width="${f1(cw)}" height="17" fill="none" stroke="${c.indigo}" stroke-opacity=".8" filter="url(#wob)"/>
<text x="${f1(x + cw / 2)}" y="180.5" font-size="8.5" font-family="${MONO}" text-anchor="middle" fill="${c.indigo}">${escapeXml(t)}</text>`;
    x += cw + 5;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="${SERIF}">${STYLE}${defs(c)}${b}</svg>`;
}

function seigaiha(c: ThemeColors, y0: number, rows: number, cols = 21): string {
  const o: string[] = [];
  const fills = [c.indigo, c.paper, c.indigo, c.paper];
  for (let rr = 0; rr < rows; rr++) {
    for (let cc = -1; cc < cols; cc++) {
      const cx = cc * 48 + (rr % 2 ? 24 : 0);
      const cy = y0 + rr * 13;
      [24, 18, 12, 6].forEach((rad, fi) => {
        o.push(`<circle cx="${cx}" cy="${cy}" r="${rad}" fill="${fills[fi]}" stroke="${c.ink}" stroke-opacity=".35" stroke-width=".6"/>`);
      });
    }
  }
  return `<g class="wave" opacity=".92">${o.join("")}</g>`;
}

function footer(c: ThemeColors, content: Content): string {
  let b = branch(c, 910, 6, 600, 58, 8, 8, 5, 10);
  b += handText(content.footer.line1.toUpperCase(), 60, 74, 20, c.ink, "700", 3);
  b += brush(c, 60, 90, 440, 92, 2.6, 0.4, 2, c.verm, 0.8);
  b += `<text x="60" y="116" font-size="13" font-style="italic" fill="${c.mute}">${escapeXml(content.footer.line2)}</text>`;
  b += seal(c, 780, 78, 40, content.options.useCJK ? "碼" : "SC", 2);
  b += seigaiha(c, 150, 9) + petals(c, 5, [40, 860]);
  return wrap(900, 256, c, b);
}

export const inkscrollStyle: StyleModule = {
  id: "inkscroll",
  name: "Inkscroll",
  keywords: ["chinese-ink", "calligraphy", "hanging-scroll", "xuan-paper"],
  palette: {
    light: ["#f3e9cd", "#26211b", "#bf2a22", "#29486f", "#8ea5b2"],
    dark: ["#181d28", "#efe5cb", "#d6402f", "#93b3d9", "#42597a"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/inkscroll/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 736, 1097], [496, 744], 0.92);
    const avatarCrop = ctx.cropToDataUrl(img, [230, 450, 330, 550], [64, 64], 0.92);

    const cropBoxes: [number, number, number, number][] = [
      [270, 385, 470, 479],
      [120, 865, 320, 957],
      [140, 440, 340, 532],
      [270, 790, 470, 882],
      [100, 140, 300, 232],
      [250, 270, 450, 362],
      [536, 370, 736, 462],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 184], 0.9)
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
      pic("hero", `${content.name} — ${content.role}. Hand-painted hanging scroll.`, "100%"),
      `<a href="${content.github}">${pic("btn-github", "GitHub")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio")}</a>`,
      pic("about", "About and journey", "100%"),
      pic("skills", "Technologies and skills", "100%"),
      pic("projects-title", "Selected projects", "100%"),
      cardPics(row1),
      row2.length ? cardPics(row2) : "",
      pic("footer", "Build, Explore, Understand", "100%"),
    ].filter(Boolean);

    const readme = `<div align="center">\n\n${readmeParts.join("\n\n")}\n\n</div>\n`;

    let bytes = 0;
    Object.values(files).forEach((str) => (bytes += new Blob([str]).size));

    return { files, readme, meta: { bytes } };
  },
};
