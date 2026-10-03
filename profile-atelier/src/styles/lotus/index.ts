import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "Georgia,'Iowan Old Style','Palatino Linotype','DejaVu Serif',serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";

interface ThemeColors {
  bg: string;
  panel: string;
  ink: string;
  mut: string;
  teal: string;
  teal2: string;
  aqua: string;
  leaf1: string;
  leaf2: string;
  gold: string;
  goldtx: string;
  koi: string;
  koi2: string;
  paper: string;
  seal: string;
  sealtxt: string;
  chip: string;
  strip: string;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#06151b", panel: "#0d2a34", ink: "#e8f2ef", mut: "#9dbdbb",
    teal: "#1d7f8f", teal2: "#2fa3a8", aqua: "#69cbc6", leaf1: "#155f73",
    leaf2: "#0c3f55", gold: "#e2bb63", goldtx: "#e2bb63", koi: "#ea5a2c",
    koi2: "#b83a18", paper: "#efdcb8", seal: "#d6402a", sealtxt: "#fbeed6",
    chip: "#12404d", strip: "#e9d6b0"
  },
  light: {
    bg: "#f1e3c6", panel: "#fbf4e1", ink: "#13303a", mut: "#4b646a",
    teal: "#14707f", teal2: "#1e8d95", aqua: "#2f9aa0", leaf1: "#1c7c8a",
    leaf2: "#0f5566", gold: "#a2711f", goldtx: "#7d5510", koi: "#d2461c",
    koi2: "#a8300f", paper: "#fffaf0", seal: "#c23520", sealtxt: "#fff4e0",
    chip: "#e6d7b4", strip: "#2a1f10"
  }
};

const CSS = `.a{transform-box:fill-box;transform-origin:center}
.sway{animation:sway 9s ease-in-out infinite alternate}
@keyframes sway{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}
.swim{animation:swim 15s ease-in-out infinite alternate}
@keyframes swim{from{transform:translate(0,0)}to{transform:translate(40px,-5px)}}
.rip{opacity:.3;animation:rip 8s ease-out infinite}
@keyframes rip{0%{transform:scale(.2);opacity:.7}100%{transform:scale(1.5);opacity:0}}
.kb{animation:kb 24s ease-in-out infinite alternate}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.07)}}
.dash{animation:dash 7s linear infinite}
@keyframes dash{to{stroke-dashoffset:-60}}
.shim{animation:shim 9s ease-in-out infinite}
@keyframes shim{0%,55%{transform:translateX(-120px)}100%{transform:translateX(420px)}}
.tw{animation:tw 4s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
@media (prefers-reduced-motion: reduce){.sway,.swim,.rip,.kb,.dash,.shim,.tw{animation:none}}`;

function root(w: number, h: number, T: ThemeColors, title: string, body: string, extraDefs = ""): string {
  const d = `<defs>`
    + `<radialGradient id="lg" cx=".4" cy=".38" r=".8"><stop offset="0" stop-color="${T.teal2}"/><stop offset=".55" stop-color="${T.leaf1}"/><stop offset="1" stop-color="${T.leaf2}"/></radialGradient>`
    + `<linearGradient id="pt" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="${T.paper}"/><stop offset=".6" stop-color="${T.paper}"/><stop offset="1" stop-color="${T.aqua}"/></linearGradient>`
    + `<linearGradient id="shg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="${T.gold}" stop-opacity="0"/><stop offset=".5" stop-color="${T.gold}" stop-opacity=".38"/><stop offset="1" stop-color="${T.gold}" stop-opacity="0"/></linearGradient>`
    + `<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .4  0 0 0 0 .3  0 0 0 .55 -.18"/></filter>`
    + `${extraDefs}</defs>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${escapeXml(title)}"><title>${escapeXml(title)}</title><style>${CSS}</style>${d}${body}<rect class="grain" width="${w}" height="${h}" fill="#000" opacity=".5" filter="url(#noise)"/></svg>`;
}

function leaf(r: number, T: ThemeColors, seed: number, n = 14, wav = 0.05): string {
  const rng = createRng(seed);
  const ph = rng() * 6.28;
  const pts: string[] = [];
  for (let k = 0; k < 48; k++) {
    const a = (2 * Math.PI * k) / 48;
    const rr = r * (1 + wav * Math.sin(3 * a + ph) + wav * 0.6 * Math.sin(7 * a + ph * 2));
    pts.push(`${f1(rr * Math.cos(a))},${f1(rr * Math.sin(a))}`);
  }
  const d = "M" + pts.join(" L") + "Z";
  const veins: string[] = [];
  for (let i = 0; i < n; i++) {
    const a = (2 * Math.PI * i) / n + (rng() - 0.5) * 0.1;
    const ex = r * 0.94 * Math.cos(a);
    const ey = r * 0.94 * Math.sin(a);
    const cx = r * 0.5 * Math.cos(a + 0.12);
    const cy = r * 0.5 * Math.sin(a + 0.12);
    veins.push(`M0,0Q${f1(cx)},${f1(cy)} ${f1(ex)},${f1(ey)}`);
    if (r > 20) {
      const mx = r * 0.6 * Math.cos(a + 0.08);
      const my = r * 0.6 * Math.sin(a + 0.08);
      for (const s of [-0.3, 0.3]) {
        veins.push(`M${f1(mx)},${f1(my)}L${f1(r * 0.9 * Math.cos(a + s * 0.5))},${f1(r * 0.9 * Math.sin(a + s * 0.5))}`);
      }
    }
  }
  const g = T.gold;
  return `<path d="${d}" fill="url(#lg)" stroke="${g}" stroke-width="1" stroke-opacity=".8"/>`
    + `<path d="${veins.join(" ")}" fill="none" stroke="${g}" stroke-width=".8" stroke-opacity=".85" stroke-linecap="round"/>`
    + `<circle r="${f1(r * 0.55)}" fill="none" stroke="${g}" stroke-width=".6" stroke-dasharray="1 4" opacity=".5"/>`
    + `<circle r="${f1(Math.max(r * 0.05, 1.5))}" fill="${g}"/>`;
}

function place(x: number, y: number, inner: string, delay = 0, cls = "sway", scale = 1, op?: number): string {
  const o = op !== undefined ? ` opacity="${op}"` : "";
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${scale})"${o}><g class="a ${cls}" style="animation-delay:${delay}s">${inner}</g></g>`;
}

function koi(T: ThemeColors, x: number, y: number, s = 1.0, flip = false, delay = 0, patch = true): string {
  const sx = flip ? -s : s;
  const p = patch ? `<path d="M26,-9C40,-13 60,-9 66,-5C56,-2 40,-4 26,-9Z" fill="${T.paper}" opacity=".85"/>` : "";
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${f1(sx)},${f1(s)})"><g class="a swim" style="animation-delay:${delay}s">`
    + `<path d="M0,0C8,-9 30,-13 55,-9C75,-6 90,-2 104,0L126,-13C121,-5 119,-1 119,2C119,5 121,9 126,16L104,4C90,7 75,10 55,9C30,12 8,8 0,0Z" fill="${T.koi}" stroke="${T.gold}" stroke-width=".9" stroke-linejoin="round"/>${p}`
    + `<path d="M32,5C35,15 44,21 54,23C49,14 44,9 40,6Z" fill="${T.koi2}" stroke="${T.gold}" stroke-width=".6"/>`
    + `<path d="M42,-10C52,-18 68,-18 80,-8Z" fill="${T.koi2}" stroke="${T.gold}" stroke-width=".6"/>`
    + `<path d="M70,-6q6,6 0,13M80,-5q6,5 0,11M90,-3q5,4 0,8" fill="none" stroke="${T.gold}" stroke-width=".6" opacity=".75"/>`
    + `<circle cx="9" cy="-2" r="1.6" fill="${T.bg}"/></g></g>`;
}

function lotus(T: ThemeColors, x: number, y: number, s = 1.0): string {
  const pet = "M0,0C-12,-14 -11,-30 0,-38C11,-30 12,-14 0,0Z";
  const st = T.teal;
  const out: string[] = [];
  for (const a of [-64, -40, -16, 16, 40, 64]) {
    out.push(`<path d="${pet}" transform="rotate(${a})" fill="url(#pt)" stroke="${st}" stroke-width=".8" opacity=".9"/>`);
  }
  for (const a of [-50, -26, 0, 26, 50]) {
    out.push(`<path d="${pet}" transform="rotate(${a}) scale(.88)" fill="url(#pt)" stroke="${st}" stroke-width=".8"/>`);
  }
  out.push(`<circle cy="-4" r="3" fill="${T.gold}"/>`);
  return `<g transform="translate(${f1(x)},${f1(y)}) scale(${s})">${out.join("")}</g>`;
}

function seal(T: ThemeColors, x: number, y: number, txt: string, size = 24, rot = -3, fs?: number): string {
  const fsz = fs || size * 0.5;
  return `<g transform="translate(${f1(x)},${f1(y)}) rotate(${rot})"><rect width="${size}" height="${f1(size * 0.8)}" rx="3" fill="${T.seal}"/>`
    + `<rect x="2" y="2" width="${size - 4}" height="${f1(size * 0.8 - 4)}" rx="2" fill="none" stroke="${T.sealtxt}" stroke-width=".7" opacity=".6"/>`
    + `<text x="${f1(size / 2)}" y="${f1((size * 0.8) / 2 + fsz * 0.35)}" text-anchor="middle" font-family="${MONO}" font-size="${f1(fsz)}" font-weight="700" fill="${T.sealtxt}">${escapeXml(txt)}</text></g>`;
}

function strip(x: number, y: number, w: number, h: number, T: ThemeColors, rng: () => number, op: number): string {
  const segs: string[] = [];
  for (let yy = y + 6; yy < y + h - 4; yy += 9) {
    segs.push(`M${x + 4},${yy}H${x + w - 4}`);
  }
  const choices = [1, 2, 3, 5, 7];
  const pat = Array.from({ length: 6 }, () => choices[Math.floor(rng() * choices.length)]).join(" ");
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${T.strip}" opacity="${op}"/>`
    + `<path d="${segs.join(" ")}" stroke="${T.ink}" stroke-width="1.6" stroke-dasharray="${pat}" opacity="${f1(op * 1.6)}" fill="none"/>`;
}

function divider(T: ThemeColors, x0: number, x1: number, y: number, delay = 0): string {
  const pts: string[] = [];
  for (let x = Math.floor(x0); x <= Math.floor(x1); x += 10) {
    pts.push(`${x},${f1(y + 2.2 * Math.sin(x / 38))}`);
  }
  const nodes: string[] = [];
  for (let x = Math.floor(x0) + 70; x < Math.floor(x1); x += 160) {
    nodes.push(`<circle cx="${x}" cy="${f1(y + 2.2 * Math.sin(x / 38))}" r="2.2" fill="${T.gold}"/>`);
  }
  const p = "M" + pts.join(" L");
  return `<path d="${p}" fill="none" stroke="${T.gold}" stroke-width="1" opacity=".7"/>`
    + `<path d="${p}" fill="none" stroke="${T.paper}" stroke-width="2" stroke-linecap="round" stroke-dasharray="1 14" class="dash" style="animation-delay:${delay}s" opacity=".8"/>${nodes.join("")}`;
}

function label(T: ThemeColors, x: number, y: number, num: string, text: string): string {
  return `${seal(T, x, y - 17, num, 24, -3, 11)}`
    + `<text x="${x + 34}" y="${y}" font-family="${MONO}" font-size="12.5" letter-spacing="3" fill="${T.goldtx}" font-weight="700">${escapeXml(text)}</text>`;
}

function ripples(T: ThemeColors, cx: number, cy: number, rx: number, delay = 0): string {
  return [0, 1, 2].map((i) =>
    `<ellipse class="a rip" cx="${cx}" cy="${cy}" rx="${rx}" ry="${f1(rx * 0.28)}" fill="none" stroke="${T.teal2}" stroke-width="1.2" style="animation-delay:${delay - i * 2.6}s"/>`
  ).join("");
}

function hero(T: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const rng = createRng(11);
  const b: string[] = [
    `<rect width="900" height="500" fill="${T.bg}"/>`,
    `<clipPath id="pc"><rect width="900" height="500"/></clipPath>`,
    `<g clip-path="url(#pc)">`
  ];
  for (const [x, w, op] of [[472, 30, 0.10], [512, 48, 0.13], [640, 60, 0.12], [840, 60, 0.14]] as [number, number, number][]) {
    b.push(strip(x, 0, w, 500, T, rng, op));
  }
  b.push(place(850, 40, leaf(120, T, 3, 20), 0, "sway", 1, 0.7));
  b.push(place(520, 540, leaf(130, T, 5, 20), -4, "sway", 1, 0.7));
  b.push(ripples(T, 140, 470, 120, 0));
  b.push(`</g>`);

  b.push(`<clipPath id="hc"><rect x="564" y="68" width="284" height="364" rx="4"/></clipPath>`
    + `<linearGradient id="vg" x1="0" y1="0" x2="0" y2="1"><stop offset=".6" stop-color="${T.bg}" stop-opacity="0"/><stop offset="1" stop-color="${T.bg}" stop-opacity=".55"/></linearGradient>`
    + `<rect x="556" y="60" width="300" height="380" rx="7" fill="${T.panel}" stroke="${T.gold}" stroke-width="1.6"/>`
    + `<g clip-path="url(#hc)"><image class="a kb" x="564" y="68" width="284" height="364" preserveAspectRatio="xMidYMid slice" href="${heroImg}"/>`
    + `<rect x="564" y="68" width="284" height="364" fill="url(#vg)"/>`
    + `<g transform="skewX(-20)"><rect class="a shim" x="560" y="68" width="40" height="364" fill="url(#shg)"/></g></g>`
    + `<rect x="564" y="68" width="284" height="364" rx="4" fill="none" stroke="${T.gold}" stroke-width=".8" opacity=".8"/>`
    + seal(T, 826, 46, "SC", 34, 5, 14));

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
    b.push(`<text x="62" y="${380 + i * 22}" font-family="${SERIF}" font-size="15" fill="${T.mut}">${escapeXml(ln)}</text>`);
  });

  b.push(koi(T, 70, 466, 0.9, false, 0) + koi(T, 330, 482, 0.6, true, -6, false));
  return root(900, 500, T, `${content.name} - ${content.role}`, b.join(""));
}

function button(T: ThemeColors, text: string): string {
  const g = T.gold;
  const b = `<rect x="1" y="1" width="148" height="38" rx="19" fill="${T.panel}" stroke="${g}" stroke-width="1.4"/>`
    + place(22, 20, leaf(10, T, 7, 8), 0)
    + `<text x="42" y="25" font-family="${MONO}" font-size="12" font-weight="700" letter-spacing="2" fill="${T.ink}">${escapeXml(text)}</text>`;
  return root(150, 40, T, text, b);
}

function about(T: ThemeColors, content: Content): string {
  const rng = createRng(21);
  const b: string[] = [
    `<rect width="900" height="310" fill="${T.bg}"/>`,
    `<clipPath id="pc"><rect width="900" height="310"/></clipPath><g clip-path="url(#pc)">`,
    strip(0, 0, 36, 310, T, rng, 0.10), strip(864, 0, 36, 310, T, rng, 0.10),
    place(905, 365, leaf(100, T, 9, 18), -2, "sway", 1, 0.55),
    `</g>`,
    label(T, 56, 52, "01", "ABOUT"), label(T, 540, 52, "02", "MY JOURNEY")
  ];
  content.about.forEach((ln, i) => {
    b.push(`<text x="58" y="${104 + i * 28}" font-family="${SERIF}" font-size="15" fill="${T.ink}">${escapeXml(ln)}</text>`);
  });
  content.journey.forEach(({ lang, area }, i) => {
    const y = 106 + i * 38;
    b.push(place(534, y - 5, leaf(7, T, 20 + i, 8), -i, "sway", 1)
      + `<text x="550" y="${y}" font-family="${MONO}" font-size="14" font-weight="700" fill="${T.ink}">${escapeXml(lang)}</text>`
      + `<path d="M652,${y - 5}H704" stroke="${T.gold}" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="1 7" class="dash" style="animation-delay:-${i}s"/>`
      + `<text x="716" y="${y}" font-family="${SERIF}" font-size="15" fill="${T.ink}">${escapeXml(area)}</text>`);
  });
  b.push(divider(T, 56, 844, 292));
  b.push(koi(T, 60, 276, 0.55, false, -3));
  return root(900, 310, T, "About and Journey", b.join(""));
}

function skills(T: ThemeColors, content: Content): string {
  const b: string[] = [
    `<rect width="900" height="340" fill="${T.bg}"/>`,
    label(T, 56, 52, "03", "TECHNOLOGIES &amp; SKILLS"),
    divider(T, 56, 844, 76, -2)
  ];
  content.skills.slice(0, 12).forEach(({ label: name, mono }, i) => {
    const cx = 121.5 + (i % 6) * 131;
    const cy = 134 + Math.floor(i / 6) * 112;
    const inner = leaf(38, T, 40 + i, 12)
      + `<circle r="17" fill="${T.leaf2}" stroke="${T.gold}" stroke-width="1"/>`
      + `<text y="5" text-anchor="middle" font-family="${MONO}" font-size="15" font-weight="700" fill="${T.sealtxt}">${escapeXml(mono)}</text>`;
    b.push(place(cx, cy, inner, -i * 0.7));
    b.push(`<text x="${f1(cx)}" y="${cy + 60}" text-anchor="middle" font-family="${SERIF}" font-size="12.5" fill="${T.ink}">${escapeXml(name)}</text>`);
  });
  return root(900, 340, T, "Technologies and Skills", b.join(""));
}

function projectsTitle(T: ThemeColors): string {
  const b = `<rect width="900" height="80" fill="${T.bg}"/>`
    + label(T, 56, 44, "04", "SELECTED PROJECTS")
    + koi(T, 690, 40, 0.7, false, -2)
    + divider(T, 56, 844, 66, -3);
  return root(900, 80, T, "Selected projects", b);
}

function chips(T: ThemeColors, tags: string[]): string {
  const out: string[] = [];
  let x = 8, y = 170;
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
  const b: string[] = [
    `<rect x="1" y="1" width="206" height="220" rx="9" fill="${T.panel}" stroke="${T.gold}" stroke-width="1.2"/>`,
    `<clipPath id="tc${i}"><rect x="8" y="8" width="192" height="92" rx="5"/></clipPath>`,
    `<g clip-path="url(#tc${i})"><image class="a kb" x="8" y="8" width="192" height="92" preserveAspectRatio="xMidYMid slice" href="${cardImg}" style="animation-delay:-${i * 3}s"/>`
    + `<g transform="skewX(-20)"><rect class="a shim" x="20" y="8" width="26" height="92" fill="url(#shg)" style="animation-delay:-${i * 1.3}s"/></g></g>`,
    `<rect x="8" y="8" width="192" height="92" rx="5" fill="none" stroke="${T.gold}" stroke-width=".7" opacity=".8"/>`,
    seal(T, 14, 14, String(i + 1).padStart(2, "0"), 28, -3, 11),
    `<text x="10" y="124" font-family="${SERIF}" font-weight="700" font-size="16" fill="${T.ink}">${escapeXml(title)}</text>`,
    `<text x="10" y="142" font-family="${SERIF}" font-size="11.5" fill="${T.mut}">${escapeXml(desc1)}</text>`,
    `<text x="10" y="157" font-family="${SERIF}" font-size="11.5" fill="${T.mut}">${escapeXml(desc2)}</text>`,
    chips(T, tags)
  ];
  return root(208, 222, T, `${title} project card`, b.join(""));
}

function footer(T: ThemeColors, content: Content): string {
  const brand = content.brand?.latin || "NashirTech";
  const b: string[] = [
    `<rect width="900" height="250" fill="${T.bg}"/>`,
    `<clipPath id="pc"><rect width="900" height="250"/></clipPath><g clip-path="url(#pc)">`,
    ripples(T, 450, 228, 210, 0),
    place(40, 270, leaf(140, T, 61, 20), 0, "sway", 1, 0.8),
    place(870, 280, leaf(150, T, 62, 22), -3, "sway", 1, 0.8),
    `<path d="M165,250V215M735,250V210" stroke="${T.teal}" stroke-width="2"/>`,
    lotus(T, 165, 215, 1.1), lotus(T, 735, 210, 1.2),
    koi(T, 330, 205, 1.0, false, 0), koi(T, 640, 232, 0.75, true, -5),
    `</g>`,
    `<text x="450" y="80" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="30" fill="${T.ink}">${escapeXml(content.footer.line1)}</text>`,
    `<text x="450" y="110" text-anchor="middle" font-family="${MONO}" font-size="12.5" letter-spacing="1" fill="${T.mut}">${escapeXml(content.footer.line2)}</text>`,
    divider(T, 230, 670, 136, -1),
    `<text x="450" y="162" text-anchor="middle" font-family="${SERIF}" font-size="13" fill="${T.goldtx}">${escapeXml(brand)}</text>`
  ];
  return root(900, 250, T, "Footer", b.join(""));
}

export const lotusStyle: StyleModule = {
  id: "lotus",
  name: "Kintsugi Lotus Pond",
  keywords: ["lotus", "koi", "kintsugi", "pond", "zen", "gold"],
  palette: {
    dark: ["#06151b", "#0d2a34", "#e8f2ef", "#e2bb63", "#ea5a2c"],
    light: ["#f1e3c6", "#fbf4e1", "#13303a", "#a2711f", "#d2461c"],
  },
  motion: "calm",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/lotus/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [30, 530, 630, 1290], [600, 760], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [270, 260, 430, 420], [64, 64], 0.9);

    const cropBoxes: [number, number, number, number][] = [
      [200, 650, 400, 840],
      [350, 340, 270, 470],
      [580, 100, 150, 240],
      [270, 930, 240, 360],
      [480, 80, 280, 410],
      [480, 830, 340, 470],
      [530, 1150, 250, 380],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [400, 190], 0.85)
    );

    const files: Record<string, string> = {};

    for (const theme of ["dark", "light"] as const) {
      const T = THEMES[theme];
      files[`hero-${theme}.svg`] = hero(T, content, heroCrop, avatarCrop);
      files[`btn-github-${theme}.svg`] = button(T, "GITHUB");
      files[`btn-linkedin-${theme}.svg`] = button(T, "LINKEDIN");
      files[`btn-portfolio-${theme}.svg`] = button(T, "PORTFOLIO");
      files[`about-${theme}.svg`] = about(T, content);
      files[`skills-${theme}.svg`] = skills(T, content);
      files[`projects-title-${theme}.svg`] = projectsTitle(T);
      files[`footer-${theme}.svg`] = footer(T, content);

      content.projects.forEach((proj, i) => {
        files[`card-${proj.slug}-${theme}.svg`] = card(T, i, proj.title, proj.line1, proj.line2, proj.tags, cardCrops[i]);
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items.map((p) => `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `${p.title}: ${p.line1} ${p.line2}`, "24%")}</a>`).join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("hero", `${content.name}, ${content.role}. Lotus pond and koi artwork.`, "100%"),
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
export default lotusStyle;
