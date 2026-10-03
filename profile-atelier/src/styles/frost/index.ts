import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic, createRng } from "../../lib/svg";

const SERIF = "'Cormorant Garamond',Georgia,'Times New Roman',serif";
const SANS = "'Trebuchet MS','Segoe UI',Verdana,'DejaVu Sans',sans-serif";
const MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Consolas,Menlo,monospace";
const ARABIC = "'Aref Ruqaa','Amiri','Scheherazade New','Noto Naskh Arabic','Geeza Pro','Segoe UI',Tahoma,serif";
const KUFI = "'Reem Kufi','Noto Kufi Arabic','Segoe UI',Tahoma,sans-serif";

interface ThemeColors {
  bg: string;
  bg2: string;
  panel: string;
  panel_op: string;
  border: string;
  border_op: string;
  ink: string;
  soft: string;
  accent: string;
  hi: string;
  snow: string;
  snow_op: number;
  frost: string;
  btn: string;
  btntxt: string;
  disc: string;
  band: string;
  stars: boolean;
}

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: {
    bg: "#050917",
    bg2: "#0B2358",
    panel: "#FFFFFF",
    panel_op: ".055",
    border: "#8FB6FF",
    border_op: ".38",
    ink: "#F3F1EA",
    soft: "#B9C9E8",
    accent: "#9CC0FF",
    hi: "#F5E9B8",
    snow: "#FFFFFF",
    snow_op: 0.85,
    frost: "#DCE8FF",
    btn: "#2557C0",
    btntxt: "#FFFFFF",
    disc: "#0A1A45",
    band: "#03060F",
    stars: true,
  },
  light: {
    bg: "#E8F0FC",
    bg2: "#F6F2E7",
    panel: "#FFFFFF",
    panel_op: ".72",
    border: "#1C4DB0",
    border_op: ".35",
    ink: "#0A1B45",
    soft: "#3E5384",
    accent: "#1C4DB0",
    hi: "#7A5D12",
    snow: "#6F9BE0",
    snow_op: 0.8,
    frost: "#4F7FD0",
    btn: "#2557C0",
    btntxt: "#FFFFFF",
    disc: "#FFFFFF",
    band: "#0A1B45",
    stars: false,
  },
};

const NIGHT = {
  ink: "#F3F1EA",
  soft: "#C4D3F0",
  accent: "#9CC0FF",
  hi: "#F5E9B8",
};

const CSS = `
.a{animation-timing-function:ease-in-out;animation-iteration-count:infinite;animation-direction:alternate}
.r{animation-fill-mode:both}
.fallH,.fallM,.fallF{animation-timing-function:linear;animation-iteration-count:infinite}
.fallH{animation-name:fallH}.fallM{animation-name:fallM}.fallF{animation-name:fallF}
.sway{animation-name:sway}
.twinkle{animation-name:twinkle;animation-duration:3s}
.pulse{transform-box:fill-box;transform-origin:center;animation-name:pulse;animation-duration:5s}
.shimmer{animation-name:shimmer;animation-duration:4.5s}
.ripple{transform-box:fill-box;transform-origin:center;animation-name:ripple;animation-duration:6s;animation-timing-function:ease-out;animation-iteration-count:infinite}
.shine{animation-name:shine;animation-duration:8s;animation-timing-function:ease-in-out;animation-iteration-count:infinite}
.rise{animation-name:rise;animation-duration:1.1s;animation-timing-function:cubic-bezier(.2,.7,.2,1)}
.spin{transform-box:fill-box;transform-origin:center;animation-name:spin;animation-duration:80s;animation-timing-function:linear;animation-iteration-count:infinite}
.flow{animation-name:flow;animation-duration:7s;animation-timing-function:linear;animation-iteration-count:infinite}
.draw{animation-name:draw;animation-duration:3.2s;animation-timing-function:ease-out}
.branch{transform-box:fill-box;transform-origin:center;animation-name:branch;animation-duration:9s}
.kb{transform-box:fill-box;transform-origin:60% 40%;animation-name:kb;animation-duration:30s}
@keyframes fallH{from{transform:translateY(-30px)}to{transform:translateY(680px)}}
@keyframes fallM{from{transform:translateY(-20px)}to{transform:translateY(470px)}}
@keyframes fallF{from{transform:translateY(-20px)}to{transform:translateY(400px)}}
@keyframes sway{from{transform:translateX(-14px)}to{transform:translateX(14px)}}
@keyframes twinkle{from{opacity:.15}to{opacity:1}}
@keyframes pulse{from{opacity:.55;transform:scale(.9)}to{opacity:1;transform:scale(1.18)}}
@keyframes shimmer{from{opacity:.05;transform:translateX(-10px)}to{opacity:.7;transform:translateX(10px)}}
@keyframes ripple{0%{opacity:.75;transform:scale(.25)}100%{opacity:0;transform:scale(1.9)}}
@keyframes shine{0%{transform:translateX(-300px)}55%,100%{transform:translateX(620px)}}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes flow{to{stroke-dashoffset:-60}}
@keyframes draw{from{stroke-dasharray:0 900}to{stroke-dasharray:900 0}}
@keyframes branch{from{transform:rotate(-2.2deg)}to{transform:rotate(2.2deg)}}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.06)}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}.fk,.ripple{display:none}}
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

function snow(c: ThemeColors, w: number, n: number, seed: number, kf = "fallH", rmax = 3.2, op?: number, clip?: string): string {
  const rng = createRng(seed);
  const out: string[] = [];
  const baseOp = op ?? c.snow_op;
  for (let i = 0; i < n; i++) {
    const x = rng() * w;
    const rad = 1.0 + rng() * (rmax - 1.0);
    const dur = (10 + rng() * 10) * (1.3 - rad / 6);
    const dl = rng() * 20;
    const sw = 4 + rng() * 4;
    const o = baseOp * (0.5 + rng() * 0.5);
    out.push(
      `<g class="fk" transform="translate(${f1(x)},0)"><g class="${kf} r" style="animation-duration:${f1(dur)}s;animation-delay:-${f1(dl)}s"><g class="sway a" style="animation-duration:${f1(sw)}s;animation-delay:-${f1(dl / 3)}s"><circle r="${f1(rad)}" fill="${c.snow}" opacity="${f1(o)}"/></g></g></g>`
    );
  }
  const g = out.join("");
  return clip ? `<g clip-path="url(#${clip})">${g}</g>` : g;
}

function flakePath(r: number): string {
  const d: string[] = [];
  for (let k = 0; k < 6; k++) {
    const a = (k * Math.PI) / 3;
    const ca = Math.cos(a);
    const sa = Math.sin(a);
    d.push(`M0,0 L${f1(r * ca)},${f1(r * sa)}`);
    for (const [f, ln] of [[0.5, 0.3], [0.78, 0.22]]) {
      const bx = r * f * ca;
      const by = r * f * sa;
      for (const s of [-1, 1]) {
        const b = a + (s * Math.PI) / 3;
        d.push(`M${f1(bx)},${f1(by)} L${f1(bx + r * ln * Math.cos(b))},${f1(by + r * ln * Math.sin(b))}`);
      }
    }
  }
  return d.join(" ");
}

function frostBranch(c: ThemeColors, ox: number, oy: number, ang: number, L: number, seed: number, depth = 4, w = 2.4, sway = true): string {
  const rng = createRng(seed);
  const segs: string[] = [];
  const dots: string[] = [];

  function grow(x: number, y: number, a: number, len: number, d: number, width: number) {
    const a2 = a + (rng() * 0.6 - 0.3);
    const x2 = x + len * Math.cos(a2);
    const y2 = y + len * Math.sin(a2);
    segs.push(`<path d="M${f1(x)},${f1(y)} L${f1(x2)},${f1(y2)}" stroke-width="${f1(Math.max(width, 0.7))}"/>`);
    if (d === 0 || rng() < 0.15) {
      dots.push(`<circle cx="${f1(x2)}" cy="${f1(y2)}" r="${f1(1.6 + rng() * 1.6)}"/>`);
    }
    if (d > 0) {
      grow(x2, y2, a2 + (0.3 + rng() * 0.4), len * 0.74, d - 1, width * 0.66);
      if (rng() < 0.85) {
        grow(x2, y2, a2 - (0.3 + rng() * 0.4), len * 0.7, d - 1, width * 0.62);
      }
    }
  }

  grow(0, 0, ang, L, depth, w);
  const guard = `<circle r="${f1(L * 2.4)}" fill="none" stroke="none"/>`;
  let inner = `${guard}<g fill="none" stroke="${c.frost}" stroke-linecap="round" opacity="0.7">${segs.join("")}</g><g fill="${c.frost}" opacity="0.85">${dots.join("")}</g>`;
  if (sway) {
    inner = `<g class="branch a" style="animation-delay:-${seed % 7}s">${inner}</g>`;
  }
  return `<g transform="translate(${f1(ox)},${f1(oy)})">${inner}</g>`;
}

function snowflake(cx: number, cy: number, r: number, color: string, spinDelay?: number, w = 1.6): string {
  const path = `<path d="${flakePath(r)}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round"/>`;
  let tips = "";
  for (let k = 0; k < 6; k++) {
    tips += `<circle cx="${f1(r * Math.cos((k * Math.PI) / 3))}" cy="${f1(r * Math.sin((k * Math.PI) / 3))}" r="2.4" fill="${color}"/>`;
  }
  let inner = `<circle r="${f1(r + 3)}" fill="none" stroke="none"/>${path}${tips}`;
  if (spinDelay !== undefined) {
    inner = `<g class="spin" style="animation-delay:-${f1(spinDelay)}s;animation-direction:${Math.floor(spinDelay) % 2 ? "reverse" : "normal"}">${inner}</g>`;
  }
  return `<g transform="translate(${f1(cx)},${f1(cy)})">${inner}</g>`;
}

function moonIcon(c: ThemeColors, cx: number, cy: number, r = 10): string {
  return `<circle cx="${f1(cx)}" cy="${f1(cy)}" r="${f1(r)}" fill="${c.hi}"/>
<circle cx="${f1(cx - r * 0.3)}" cy="${f1(cy - r * 0.2)}" r="${f1(r * 0.22)}" fill="${c.bg}" opacity="0.25"/>
<circle cx="${f1(cx + r * 0.3)}" cy="${f1(cy + r * 0.35)}" r="${f1(r * 0.15)}" fill="${c.bg}" opacity="0.25"/>`;
}

function base(c: ThemeColors, W: number, H: number, sid = "s"): { defs: string; bg: string } {
  const defs = `<linearGradient id="${sid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset="1" stop-color="${c.bg2}"/></linearGradient>`;
  return { defs, bg: `<rect width="${W}" height="${H}" fill="url(#${sid}g)"/>` };
}

function panel(c: ThemeColors, x: number, y: number, w: number, h: number, pid: string): { defs: string; body: string } {
  const defs = `<clipPath id="${pid}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="26"/></clipPath>`;
  const body = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="26" fill="${c.panel}" fill-opacity="${c.panel_op}" stroke="${c.border}" stroke-opacity="${c.border_op}" stroke-width="1.4"/>
<path d="M${x + 30},${y + 1} H${x + w - 30}" stroke="${c.ink}" stroke-opacity="0.35" stroke-width="1.2"/>`;
  return { defs, body };
}

function heading(x: number, y: number, text: string, ar: string, arRight: number, c: ThemeColors, size = 36): string {
  const arPart = ar && arRight > 0 ? `<text x="${arRight}" y="${y - 1}" text-anchor="end" font-family="${KUFI}" font-size="25" fill="${c.accent}">${escapeXml(ar)}</text>` : "";
  return `${moonIcon(c, x + 12, y - 12, 11)}
<text x="${x + 34}" y="${y}" font-family="${SERIF}" font-weight="700" font-size="${size}" fill="${c.ink}">${escapeXml(text)}</text>
${arPart}`;
}

function hero(c: ThemeColors, content: Content, heroImg: string, avatarImg: string): string {
  const W = 900, H = 640;
  const s_ = H / 1033;
  const aw = 736 * s_;
  const ax = W - aw;
  const { defs: bDefs, bg } = base(c, W, H, "h");
  const mx = ax + aw * 0.55;

  let defs = bDefs + `
<linearGradient id="hfL" gradientUnits="userSpaceOnUse" x1="${f1(ax)}" y1="0" x2="${f1(mx)}" y2="0"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="hfB" gradientUnits="userSpaceOnUse" x1="0" y1="${f1(H * 0.78)}" x2="0" y2="${H}"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="hmL"><rect width="${W}" height="${H}" fill="url(#hfL)"/></mask>
<mask id="hmB"><rect width="${W}" height="${H}" fill="url(#hfB)"/></mask>
<radialGradient id="hmoon"><stop offset="0" stop-color="${c.hi}" stop-opacity=".95"/><stop offset=".35" stop-color="${c.hi}" stop-opacity=".35"/><stop offset="1" stop-color="${c.hi}" stop-opacity="0"/></radialGradient>
<linearGradient id="hshine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="${c.stars ? c.hi : "#FFFFFF"}" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="hav"><circle cx="64" cy="38" r="15"/></clipPath>
<clipPath id="hname"><text x="50" y="214" font-family="${SERIF}" font-size="88">${escapeXml(content.name.split(" ")[0] || content.name)}</text>
<text x="50" y="296" font-family="${SERIF}" font-size="88">${escapeXml(content.name.split(" ").slice(1).join(" ") || "")}</text></clipPath>`;

  const s: string[] = [bg];
  if (c.stars) {
    const rr = createRng(5);
    for (let i = 0; i < 22; i++) {
      s.push(
        `<circle class="twinkle a" style="animation-delay:-${f1(rr() * 3)}s;animation-duration:${f1(2 + rr() * 3)}s" cx="${f1(20 + rr() * 410)}" cy="${f1(10 + rr() * 590)}" r="${f1(0.7 + rr() * 0.9)}" fill="#fff"/>`
      );
    }
  }

  const mw = ax + 239 * s_;
  const my = 324 * s_;
  let shimmers = "";
  for (let i = 0; i < 8; i++) {
    shimmers += `<path class="shimmer a" style="animation-delay:-${f1(i * 0.7)}s;animation-duration:${f1(3.5 + i * 0.4)}s" d="M${f1(ax + 40 + i * 52)},${400 + (i % 4) * 26} q22,-5 46,0" stroke="#fff" stroke-width="1.6" fill="none" stroke-linecap="round"/>`;
  }

  s.push(
    `<g mask="url(#hmL)"><g mask="url(#hmB)"><g><image class="kb a" href="${heroImg}" x="${f1(ax)}" y="0" width="${f1(aw)}" height="${H}"/><circle class="pulse a" cx="${f1(mw)}" cy="${f1(my)}" r="40" fill="url(#hmoon)"/>${shimmers}</g></g></g>`
  );
  s.push(snow(c, W, 38, 11, "fallH"));

  const nameParts = content.name.split(" ");
  const name1 = nameParts[0] || content.name;
  const name2 = nameParts.slice(1).join(" ");
  const arName = content.options?.useArabic !== false ? (content.brand?.arabic || "سليمان المودن") : "";

  // top bar
  s.push(
    `<g class="rise r" style="animation-delay:.05s"><image href="${avatarImg}" x="49" y="23" width="30" height="30" clip-path="url(#hav)" preserveAspectRatio="xMidYMid slice"/><circle cx="64" cy="38" r="15" fill="none" stroke="${c.accent}" stroke-width="1.6"/><text x="88" y="43" font-family="${MONO}" font-size="12.5" fill="${c.soft}">${escapeXml(content.handle)} / README</text></g>`
  );
  s.push(`<g class="rise r" style="animation-delay:.2s"><text x="52" y="132" font-family="${SERIF}" font-style="italic" font-size="30" fill="${c.soft}">Hi, I'm</text></g>`);
  s.push(
    `<g class="rise r" style="animation-delay:.35s"><text x="50" y="214" font-family="${SERIF}" font-size="88" fill="${c.ink}">${escapeXml(name1)}</text><text x="50" y="296" font-family="${SERIF}" font-size="88" fill="${c.ink}">${escapeXml(name2)}</text></g>`
  );
  s.push(`<g clip-path="url(#hname)"><g class="shine"><rect x="-80" y="130" width="170" height="190" fill="url(#hshine)" transform="skewX(-18)" opacity=".85"/></g></g>`);
  if (arName) {
    s.push(`<g class="rise r" style="animation-delay:.6s"><text x="54" y="358" font-family="${ARABIC}" font-size="46" fill="${c.hi}">${escapeXml(arName)}</text></g>`);
  }
  s.push(
    `<g class="rise r" style="animation-delay:.8s"><text x="54" y="408" font-family="${SERIF}" font-weight="700" font-size="19" letter-spacing="7" fill="${c.accent}">${escapeXml(content.role.toUpperCase())}</text><path d="M54,424 H300" stroke="${c.accent}" stroke-opacity=".5" stroke-width="1"/></g>`
  );
  s.push(
    `<g class="rise r" style="animation-delay:1s"><text x="54" y="458" font-family="${SERIF}" font-style="italic" font-size="30" fill="${c.ink}">${escapeXml(content.pillars)}</text></g>`
  );
  content.tagline.forEach((line, i) => {
    s.push(`<g class="rise r" style="animation-delay:${f1(1.15 + i * 0.15)}s"><text x="54" y="${506 + i * 28}" font-family="${SERIF}" font-size="21" fill="${c.soft}">${escapeXml(line)}</text></g>`);
  });

  return svgDoc(W, H, s.join(""), `${content.name}: ${content.role}`, "Profile header over a snowy night scene: castle by a moonlit lake.", defs);
}

function button(c: ThemeColors, label: string): string {
  const body = `<rect x="3" y="3" width="144" height="34" rx="17" fill="${c.btn}" stroke="${c.accent}" stroke-width="1.4"/>
${snowflake(28, 20, 9, c.btntxt, undefined, 1.4)}
<text x="91" y="26" text-anchor="middle" font-family="${SERIF}" font-weight="700" font-size="19" letter-spacing=".6" fill="${c.btntxt}">${escapeXml(label)}</text>`;
  return svgDoc(150, 40, body, label, `Button linking to ${label}`, "", false);
}

function about(c: ThemeColors, content: Content): string {
  const W = 900, H = 450;
  const { defs: bDefs, bg } = base(c, W, H, "a");
  const { defs: pDefs, body: pBody } = panel(c, 16, 14, 868, 422, "apc");
  const defs = bDefs + pDefs;
  const s: string[] = [
    bg,
    pBody,
    snow(c, W, 14, 21, "fallM", 2.4, 0.6, "apc"),
    frostBranch(c, 884, 14, 2.45, 24, 3, 3, 2.0),
    frostBranch(c, 16, 436, -0.7, 22, 9, 3, 1.8),
  ];

  s.push(heading(54, 90, "About", "نبذة عني", 468, c));
  s.push(heading(520, 90, "My journey", "رحلتي", 846, c));

  content.about.forEach((line, i) => {
    s.push(`<text x="56" y="${140 + i * 28}" font-family="${SERIF}" font-size="20" fill="${c.ink}">${escapeXml(line)}</text>`);
  });

  const factY = 140 + 28 * content.about.length + 22;
  s.push(`<text x="56" y="${factY}" font-family="${SANS}" font-size="12" fill="${c.soft}">Software engineering · Mathematics &amp; Physics · Based in Morocco</text>`);
  s.push(`<text x="56" y="${factY + 22}" font-family="${SANS}" font-size="12.5" font-weight="700" fill="${c.accent}">Focus: Systems, Web, Intelligence &amp; Mathematics</text>`);

  s.push(`<path d="M494,70 L492,390" stroke="${c.accent}" stroke-opacity=".55" stroke-width="1.2"/>`);
  for (const yy of [140, 230, 320]) {
    s.push(snowflake(493, yy, 7, c.accent, undefined, 1.2));
  }

  content.journey.forEach((item, i) => {
    const yy = 150 + i * 54;
    const x1 = 520 + item.lang.length * 11.5 + 14;
    const x2 = 846 - item.area.length * 7.6 - 32;
    s.push(`<text x="520" y="${yy}" font-family="${SERIF}" font-weight="700" font-size="25" fill="${c.ink}">${escapeXml(item.lang)}</text>`);
    s.push(`<line class="flow" x1="${f1(x1)}" y1="${yy - 6}" x2="${f1(x2)}" y2="${yy - 6}" stroke="${c.accent}" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="1 9"/>`);
    s.push(`<circle cx="${Math.round(x2 + 12)}" cy="${yy - 6}" r="3" fill="${c.hi}"/>`);
    s.push(`<text x="846" y="${yy}" text-anchor="end" font-family="${SANS}" font-size="13.5" font-weight="700" fill="${c.accent}">${escapeXml(item.area)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "About and journey", "About text and journey paths", defs);
}

function skills(c: ThemeColors, content: Content): string {
  const W = 900, H = 478;
  const { defs: bDefs, bg } = base(c, W, H, "k");
  const { defs: pDefs, body: pBody } = panel(c, 16, 14, 868, 450, "kpc");
  const defs = bDefs + pDefs;
  const s: string[] = [
    bg,
    pBody,
    snow(c, W, 16, 33, "fallM", 2.4, 0.55, "kpc"),
    frostBranch(c, 16, 14, 0.7, 24, 5, 3, 2.0),
    frostBranch(c, 884, 464, -2.4, 24, 12, 3, 2.0),
    heading(54, 90, "Technologies & Skills", "التقنيات والمهارات", 846, c),
  ];

  const cell = 800 / 6;
  const cols = [c.accent, c.frost, c.hi];
  content.skills.slice(0, 12).forEach((item, i) => {
    const cx = 50 + cell * ((i % 6) + 0.5);
    const cy = 196 + Math.floor(i / 6) * 140;
    const col = cols[i % 3];
    s.push(snowflake(cx, cy, 46, col, i * 7 + 1));
    s.push(`<circle cx="${f1(cx)}" cy="${cy}" r="23" fill="${c.disc}" stroke="${col}" stroke-width="1.6"/>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 6}" text-anchor="middle" font-family="${SERIF}" font-weight="700" font-size="20" fill="${c.ink}">${escapeXml(item.mono)}</text>`);
    s.push(`<text x="${f1(cx)}" y="${cy + 70}" text-anchor="middle" font-family="${SANS}" font-size="12" font-weight="700" fill="${c.ink}">${escapeXml(item.label)}</text>`);
  });

  return svgDoc(W, H, s.join(""), "Technologies and skills", "Twelve snowflake medallions", defs);
}

function projectsTitle(c: ThemeColors): string {
  const W = 900, H = 110;
  const { defs, bg } = base(c, W, H, "p");
  const s = [
    bg,
    heading(54, 70, "Selected projects", "", 0, c, 40),
    `<text x="846" y="68" text-anchor="end" font-family="${KUFI}" font-size="27" fill="${c.accent}">مشاريع مختارة</text>`,
    `<path class="draw r" d="${wave(380, 640, 82, 4, 80)}" fill="none" stroke="${c.accent}" stroke-opacity=".7" stroke-width="1.6" stroke-linecap="round"/>`,
    snowflake(660, 82, 8, c.hi, 3, 1.3),
  ];
  return svgDoc(W, H, s.join(""), "Selected projects", "Section heading", defs);
}

function lancet(x0: number, x1: number, ys: number, y1: number): string {
  const W = x1 - x0;
  const cx = (x0 + x1) / 2;
  const y0 = ys - 0.866 * W;
  return `M${x0},${y1} V${ys} A${W},${W} 0 0 1 ${cx},${f1(y0)} A${W},${W} 0 0 1 ${x1},${ys} V${y1} Z`;
}

const AR_NUMS = ["١", "٢", "٣", "٤", "٥", "٦", "٧", "٨"];

function card(c: ThemeColors, idx: number, title: string, desc: string, tags: string[], img: string): string {
  const W = 208, H = 316;
  const defs = `<clipPath id="cc${idx}"><rect x="6" y="6" width="196" height="304" rx="24"/></clipPath>
<clipPath id="cw${idx}"><path d="${lancet(36, 172, 146, 196)}"/></clipPath>`;

  const g = [
    `<rect x="6" y="6" width="196" height="304" rx="24" fill="${c.panel}" fill-opacity="${c.panel_op}" stroke="${c.border}" stroke-opacity="${c.border_op}" stroke-width="1.4"/>`,
    snow(c, W, 6, idx * 13, "fallM", 2.0, 0.6, `cc${idx}`),
    `<path d="${lancet(30, 178, 146, 202)}" fill="none" stroke="${c.accent}" stroke-opacity=".6" stroke-width="1.2"/>`,
    `<g clip-path="url(#cw${idx})"><image href="${img}" x="36" y="24" width="136" height="172" preserveAspectRatio="xMidYMid slice"/></g>`,
    `<path d="${lancet(36, 172, 146, 196)}" fill="none" stroke="${c.ink}" stroke-opacity=".8" stroke-width="1.4"/>`,
    `<circle cx="104" cy="198" r="16" fill="${c.disc}" stroke="${c.accent}" stroke-width="1.6"/>`,
    `<text x="104" y="205" text-anchor="middle" font-family="${ARABIC}" font-size="21" fill="${c.hi}">${AR_NUMS[idx - 1] || idx}</text>`,
    `<text x="104" y="242" text-anchor="middle" font-family="${SERIF}" font-weight="700" font-size="${f1(Math.min(24, 180 / (title.length * 0.5)))}" fill="${c.ink}">${escapeXml(title)}</text>`,
  ];

  g.push(`<text x="104" y="260" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(0, 36))}</text>`);
  if (desc.length > 36) {
    g.push(`<text x="104" y="274" text-anchor="middle" font-family="${SANS}" font-size="10.5" fill="${c.soft}">${escapeXml(desc.slice(36, 72))}</text>`);
  }
  g.push(`<text x="104" y="296" text-anchor="middle" font-family="${SANS}" font-size="10.5" font-weight="700" fill="${c.accent}">${escapeXml(tags.slice(0, 3).join(" · "))}</text>`);

  return svgDoc(W, H, g.join(""), `Project ${title}`, `${title}: ${desc}`, defs);
}

function footer(c: ThemeColors, content: Content, footerImg: string): string {
  const W = 900, H = 430;
  const T2 = { ...c, ...NIGHT, snow: "#FFFFFF", snow_op: 0.85, frost: "#DCE8FF" };
  const defs = `<linearGradient id="ftop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c.bg}"/><stop offset=".5" stop-color="${c.bg}" stop-opacity="0"/></linearGradient>
<linearGradient id="fdim" x1="0" y1="0" x2="0" y2="1"><stop offset=".25" stop-color="#050917" stop-opacity="0"/><stop offset=".55" stop-color="#050917" stop-opacity=".8"/><stop offset="1" stop-color="#050917" stop-opacity=".85"/></linearGradient>`;

  const ih = 396;
  const s: string[] = [
    `<rect width="${W}" height="${H}" fill="${c.bg}"/>`,
    `<image href="${footerImg}" x="0" y="${H - 34 - ih}" width="${W}" height="${ih}" preserveAspectRatio="xMidYMid slice"/>`,
    `<rect width="${W}" height="${H - 34}" fill="url(#fdim)"/>`,
    `<rect width="${W}" height="${H - 34}" fill="url(#ftop)"/>`,
  ];

  for (let i = 0; i < 4; i++) {
    s.push(`<ellipse class="ripple" style="animation-delay:-${f1(i * 1.5)}s" cx="450" cy="360" rx="330" ry="28" fill="none" stroke="#DCE8FF" stroke-width="1.4"/>`);
  }
  s.push(snow(T2, W, 26, 41, "fallF"));
  s.push(`<text x="450" y="178" text-anchor="middle" font-family="${SERIF}" font-style="italic" font-size="50" fill="${NIGHT.ink}">${escapeXml(content.footer.line1)}</text>`);

  const arWords = ["ابنِ", "اكتشف", "افهم"];
  [570, 450, 330].forEach((x, i) => {
    s.push(`<text x="${x}" y="244" text-anchor="middle" font-family="${ARABIC}" font-size="44" fill="${NIGHT.hi}">${arWords[i]}</text>`);
  });
  s.push(snowflake(390, 232, 9, NIGHT.accent, 3, 1.3));
  s.push(snowflake(510, 232, 9, NIGHT.accent, 6, 1.3));

  s.push(`<text x="450" y="296" text-anchor="middle" font-family="${SANS}" font-size="13" letter-spacing="1.2" fill="${NIGHT.soft}">${escapeXml(content.footer.line2)}</text>`);
  s.push(`<rect x="0" y="${H - 34}" width="${W}" height="34" fill="${c.band}"/>`);
  s.push(`<path d="M0,${H - 34} H${W}" stroke="#9CC0FF" stroke-opacity=".6" stroke-width="1.4"/>`);
  s.push(`<text x="30" y="${H - 13}" font-family="${SANS}" font-size="10.5" fill="#F3F1EA">Artwork: source unknown</text>`);
  s.push(`<text x="870" y="${H - 13}" text-anchor="end" font-family="${SANS}" font-size="11.5" font-weight="700" fill="#F5E9B8">NashirTech · ناشر تك</text>`);

  return svgDoc(W, H, s.join(""), "Footer", `${content.footer.line1}. ${content.footer.line2}`, defs);
}

export const frostStyle: StyleModule = {
  id: "frost",
  name: "Frost & Ink",
  keywords: ["indigo", "snow", "woodblock", "calligraphy", "arctic"],
  palette: {
    dark: ["#050917", "#0B2358", "#8FB6FF", "#F3F1EA", "#F5E9B8"],
    light: ["#E8F0FC", "#F6F2E7", "#1C4DB0", "#0A1B45", "#7A5D12"],
  },
  motion: "lively",
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    const img = await ctx.loadImage("/art/frost/source.jpg");
    const heroCrop = ctx.cropToDataUrl(img, [0, 0, 736, 1033], [520, 730], 0.85);
    const avatarCrop = ctx.cropToDataUrl(img, [100, 170, 260, 330], [96, 96], 0.9);
    const footerCrop = ctx.cropToDataUrl(img, [0, 709, 736, 1033], [900, 396], 0.8);

    const cropBoxes: [number, number, number, number][] = [
      [40, 170, 300, 430],
      [140, 230, 340, 430],
      [300, 380, 520, 600],
      [250, 600, 470, 820],
      [0, 660, 240, 900],
      [0, 0, 260, 260],
      [480, 300, 736, 556],
    ];

    const cardCrops = content.projects.map((_, i) =>
      ctx.cropToDataUrl(img, cropBoxes[i % cropBoxes.length], [240, 240], 0.85)
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
      files[`footer-${theme}.svg`] = footer(c, content, footerCrop);

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
      pic("hero", `${content.name}, ${content.role}. A white-and-blue castle by a moonlit lake under falling snow.`, "100%"),
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
