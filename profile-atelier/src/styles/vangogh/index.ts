import { Content, RenderCtx, RenderResult, StyleModule } from "../../types";
import { escapeXml, f1, pic } from "../../lib/svg";

interface ThemeColors {
  bg1: string;
  bg2: string;
  bg3: string;
  text1: string;
  text2: string;
  text3: string;
  teal1: string;
  teal2: string;
  teal3: string;
  teal4: string;
  gold1: string;
  gold2: string;
  gold3: string;
  accent: string;
  card_bg1: string;
  card_bg2: string;
}

const DARK: ThemeColors = {
  bg1: "#0A1A1F", bg2: "#0F2832", bg3: "#112E38",
  text1: "#F0F5F0", text2: "#D0DFE2", text3: "#9BB8BC",
  teal1: "#3B7A8C", teal2: "#5BA3A0", teal3: "#6FB5A2", teal4: "#2D6B77",
  gold1: "#C4A843", gold2: "#D4B64A", gold3: "#8FA055",
  accent: "#8BBFC4",
  card_bg1: "#0C1E25", card_bg2: "#112A33",
};

const LIGHT: ThemeColors = {
  bg1: "#FAFDF7", bg2: "#F0F5EE", bg3: "#E8EFE5",
  text1: "#1A2F35", text2: "#2D4A52", text3: "#5A7A7F",
  teal1: "#2D6B77", teal2: "#3B7A8C", teal3: "#5BA3A0", teal4: "#1F5560",
  gold1: "#8A7030", gold2: "#A08838", gold3: "#6B7A3A",
  accent: "#3B7A8C",
  card_bg1: "#F5F8F2", card_bg2: "#EDF2E9",
};

const THEMES: Record<"dark" | "light", ThemeColors> = {
  dark: DARK,
  light: LIGHT,
};

function pointsToSmoothPath(points: [number, number][]): string {
  if (points.length < 2) return "";
  let d = `M ${f1(points[0][0])} ${f1(points[0][1])}`;
  for (let i = 1; i < points.length; i++) {
    let cp1x: number, cp1y: number, cp2x: number, cp2y: number;
    if (i === 1) {
      cp1x = points[0][0] + (points[1][0] - points[0][0]) / 3;
      cp1y = points[0][1] + (points[1][1] - points[0][1]) / 3;
      const idx2 = Math.min(2, points.length - 1);
      cp2x = points[1][0] - (points[idx2][0] - points[0][0]) / 3;
      cp2y = points[1][1] - (points[idx2][1] - points[0][1]) / 3;
    } else {
      const prev = points[i - 2];
      const curr = points[i - 1];
      const nextP = points[i];
      cp1x = curr[0] + (nextP[0] - prev[0]) / 6;
      cp1y = curr[1] + (nextP[1] - prev[1]) / 6;
      if (i < points.length - 1) {
        const nextNext = points[i + 1];
        cp2x = nextP[0] - (nextNext[0] - curr[0]) / 6;
        cp2y = nextP[1] - (nextNext[1] - curr[1]) / 6;
      } else {
        cp2x = nextP[0] - (nextP[0] - curr[0]) / 3;
        cp2y = nextP[1] - (nextP[1] - curr[1]) / 3;
      }
    }
    d += ` C ${f1(cp1x)} ${f1(cp1y)}, ${f1(cp2x)} ${f1(cp2y)}, ${f1(points[i][0])} ${f1(points[i][1])}`;
  }
  return d;
}

function spiralPath(cx: number, cy: number, startR: number, endR: number, turns: number, startAngle = 0, stepsPerTurn = 30): string {
  const totalSteps = Math.max(Math.floor(turns * stepsPerTurn), 8);
  const points: [number, number][] = [];
  for (let i = 0; i <= totalSteps; i++) {
    const t = i / totalSteps;
    const angle = startAngle + t * turns * 2 * Math.PI;
    const r = startR + t * (endR - startR);
    points.push([cx + r * Math.cos(angle), cy + r * Math.sin(angle)]);
  }
  return pointsToSmoothPath(points);
}

function wavePath(x1: number, y1: number, x2: number, y2: number, amplitude = 20, waves = 3): string {
  const dx = x2 - x1;
  const dy = y2 - y1;
  const length = Math.sqrt(dx * dx + dy * dy);
  const nx = -dy / length;
  const ny = dx / length;
  const points: [number, number][] = [];
  const steps = waves * 20;
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const wave = Math.sin(t * waves * 2 * Math.PI) * amplitude;
    const x = x1 + t * dx + wave * nx;
    const y = y1 + t * dy + wave * ny;
    points.push([x, y]);
  }
  return pointsToSmoothPath(points);
}

function flowingCurve(x1: number, y1: number, x2: number, y2: number, bend = 40): string {
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const length = Math.sqrt(dx * dx + dy * dy);
  const nx = -dy / length;
  const ny = dx / length;
  const cpx = mx + nx * bend;
  const cpy = my + ny * bend;
  return `M ${f1(x1)} ${f1(y1)} Q ${f1(cpx)} ${f1(cpy)} ${f1(x2)} ${f1(y2)}`;
}

function gridPattern(pid = "grid", size = 40, color = "#3B7A8C", opacity = 0.03): string {
  return `<pattern id="${pid}" width="${size}" height="${size}" patternUnits="userSpaceOnUse"><path d="M ${size} 0 L 0 0 0 ${size}" fill="none" stroke="${color}" stroke-width="0.5" opacity="${opacity}"/></pattern>`;
}

const HEADER_ANIMATIONS = `
  <style>
    @keyframes spiralPulse {
      0%, 100% { opacity: 0.35; }
      50% { opacity: 0.55; }
    }
    @keyframes nodePulse {
      0%, 100% { opacity: 0.3; r: 2; }
      50% { opacity: 0.7; r: 3; }
    }
    @keyframes flowDrift {
      0% { stroke-dashoffset: 0; }
      100% { stroke-dashoffset: -200; }
    }
    .spiral-animated { animation: spiralPulse 12s ease-in-out infinite; }
    .node-animated { animation: nodePulse 8s ease-in-out infinite; }
    .flow-animated {
      stroke-dasharray: 8 12;
      animation: flowDrift 16s linear infinite;
    }
    @media (prefers-reduced-motion: reduce) {
      .spiral-animated, .node-animated, .flow-animated { animation: none; }
    }
  </style>
`;

function generateHeader(mode: "dark" | "light", content: Content): string {
  const p = THEMES[mode];
  const W = 1100, H = 380;

  const spiralDefs: [number, number, number, number, number, number][] = [
    [820, 120, 8, 120, 2.8, 0],
    [950, 200, 5, 90, 2.2, 1.2],
    [750, 280, 10, 100, 2.5, 2.5],
    [900, 80, 6, 70, 1.8, 0.8],
    [680, 160, 12, 80, 2.0, 3.8],
    [1000, 300, 4, 60, 1.5, 1.5],
    [600, 60, 8, 110, 2.3, 4.5],
    [850, 340, 6, 50, 1.6, 2.0],
  ];

  const spirals = spiralDefs.map(([cx, cy, sr, er, t, sa], i) => {
    const opacity = mode === "dark" ? 0.25 - i * 0.02 : 0.18 - i * 0.015;
    const d = spiralPath(cx, cy, sr, er, t, sa);
    const animClass = i % 3 === 0 ? ' class="spiral-animated"' : "";
    return `<path d="${d}" fill="none" stroke="${p.teal2}" stroke-width="${f1(1.5 - i * 0.1)}" opacity="${f1(Math.max(opacity, 0.06))}"${animClass}/>`;
  });

  const waves: string[] = [];
  for (let i = 0; i < 5; i++) {
    const yBase = 300 + i * 18;
    const amp = 15 - i * 2;
    const d = wavePath(0, yBase, W, yBase - 10 + i * 5, amp, 4 + i);
    const goldOpacity = mode === "dark" ? 0.15 - i * 0.025 : 0.12 - i * 0.02;
    const flowClass = i % 2 === 0 ? ' class="flow-animated"' : "";
    waves.push(`<path d="${d}" fill="none" stroke="${p.gold1}" stroke-width="1.0" opacity="${f1(Math.max(goldOpacity, 0.04))}"${flowClass}/>`);
  }

  const nodePositions: [number, number][] = [
    [820, 120], [950, 200], [750, 280], [680, 160], [900, 80], [1000, 300], [600, 60], [850, 340],
    [770, 190], [880, 250], [920, 140], [980, 100]
  ];
  const nodes = nodePositions.map(([x, y], i) => {
    const anim = i % 2 === 0 ? ' class="node-animated"' : "";
    const op = mode === "dark" ? 0.4 : 0.3;
    return `<circle cx="${x}" cy="${y}" r="2.5" fill="${p.gold1}" opacity="${op}"${anim}/>`;
  });

  const cloudSpirals: string[] = [];
  for (const [cx, cy] of [[750, 50], [1050, 150], [650, 300]]) {
    for (let j = 0; j < 3; j++) {
      const d = spiralPath(cx + j * 15, cy + j * 8, 2, 15 + j * 5, 1.2, j * 2.1);
      cloudSpirals.push(`<path d="${d}" fill="none" stroke="${p.text1}" stroke-width="0.6" opacity="0.08"/>`);
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${p.bg1}"/>
      <stop offset="0.6" stop-color="${p.bg2}"/>
      <stop offset="1" stop-color="${p.bg3}"/>
    </linearGradient>
    ${gridPattern("hgrid", 50, p.teal1, mode === "dark" ? 0.025 : 0.04)}
    ${HEADER_ANIMATIONS}
  </defs>

  <rect width="${W}" height="${H}" fill="url(#hbg)"/>
  <rect width="${W}" height="${H}" fill="url(#hgrid)"/>

  <!-- Flowing spiral patterns -->
${spirals.join("\n")}

  <!-- Golden field waves -->
${waves.join("\n")}

  <!-- Cloud spiral clusters -->
${cloudSpirals.join("\n")}

  <!-- Decorative nodes -->
${nodes.join("\n")}

  <!-- Text Content -->
  <text x="80" y="110" fill="${p.accent}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="14" font-weight="300" letter-spacing="2">Hi, I'm</text>
  <text x="80" y="158" fill="${p.text1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="32" font-weight="700" letter-spacing="6">${escapeXml(content.name.toUpperCase())}</text>
  <text x="82" y="195" fill="${p.gold1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="16" font-weight="500" letter-spacing="3">${escapeXml(content.role)}</text>
  <text x="82" y="228" fill="${p.teal2}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="13" font-weight="400" letter-spacing="1.5">${escapeXml(content.pillars)}</text>
  <line x1="80" y1="245" x2="420" y2="245" stroke="${p.gold1}" stroke-width="0.5" opacity="0.3"/>
  <text x="82" y="272" fill="${p.text3}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300" letter-spacing="0.5">${escapeXml(content.tagline[0] || "")}</text>
  <text x="82" y="292" fill="${p.text3}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300" letter-spacing="0.5">${escapeXml(content.tagline[1] || "")}</text>
</svg>`;
}

function generateButton(label: string, mode: "dark" | "light"): string {
  const p = THEMES[mode];
  const W = 160, H = 36;
  const iconMap: Record<string, string> = {
    GitHub: `<path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" fill="${p.text1}" transform="translate(10,8) scale(0.85)"/>`,
    LinkedIn: `<path d="M19 3H5a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2zM9 17H6.5v-7H9v7zM7.7 8.7c-.8 0-1.3-.5-1.3-1.2s.5-1.2 1.4-1.2 1.3.5 1.3 1.2-.5 1.2-1.4 1.2zM18 17h-2.5v-3.8c0-1-.7-1.2-1-1.2s-1.2.1-1.2 1.2V17h-2.5v-7h2.5v1c.3-.6 1.1-1 2.2-1 1.1 0 2.5.8 2.5 3.5V17z" fill="${p.text1}" transform="translate(8,5) scale(0.85)"/>`,
    Portfolio: `<circle cx="20" cy="17" r="7" fill="none" stroke="${p.text1}" stroke-width="1.5"/><path d="M16 13l3 3 5-5" fill="none" stroke="${p.text1}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>`,
  };

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <rect width="${W}" height="${H}" rx="8" fill="none" stroke="${p.teal1}" stroke-width="1" opacity="0.5"/>
  ${iconMap[label] || ""}
  <text x="38" y="22" fill="${p.text1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="500" letter-spacing="1">${escapeXml(label)}</text>
</svg>`;
}

function generateAbout(mode: "dark" | "light", content: Content): string {
  const p = THEMES[mode];
  const W = 1100, H = 300;

  const radial: string[] = [];
  for (let i = 0; i < 8; i++) {
    const angle = (i * Math.PI) / 4;
    const x2 = 80 + 25 * Math.cos(angle);
    const y2 = 42 + 25 * Math.sin(angle);
    radial.push(`<line x1="80" y1="42" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${p.teal2}" stroke-width="0.5" opacity="0.15"/>`);
  }
  radial.push(`<circle cx="80" cy="42" r="25" fill="none" stroke="${p.teal2}" stroke-width="0.5" opacity="0.1"/>`);
  radial.push(`<circle cx="80" cy="42" r="15" fill="none" stroke="${p.teal2}" stroke-width="0.4" opacity="0.08"/>`);

  const approaches = content.journey.slice(0, 5).map(({ lang, area }) => ({ label: area, tech: lang }));
  const cards: string[] = [];
  const cardW = 180, cardH = 52;
  const totalW = approaches.length * cardW + (approaches.length - 1) * 12;
  const startX = (W - totalW) / 2;
  const cardY = 210;

  approaches.forEach(({ label, tech }, i) => {
    const x = startX + i * (cardW + 12);
    cards.push(`<rect x="${f1(x)}" y="${cardY}" width="${cardW}" height="${cardH}" rx="6" fill="none" stroke="${p.teal1}" stroke-width="0.8" opacity="0.3"/>`);
    const miniSpiral = spiralPath(x + 16, cardY + 26, 2, 8, 1.0, i * 1.3);
    cards.push(`<path d="${miniSpiral}" fill="none" stroke="${p.teal2}" stroke-width="0.5" opacity="0.2"/>`);
    cards.push(`<text x="${f1(x + 32)}" y="${cardY + 22}" fill="${p.gold1}" font-family="'Segoe UI',sans-serif" font-size="11" font-weight="600">${escapeXml(label)}</text>`);
    cards.push(`<text x="${f1(x + 32)}" y="${cardY + 40}" fill="${p.text3}" font-family="'JetBrains Mono',monospace" font-size="9.5">→ ${escapeXml(tech)}</text>`);
  });

  const connectors: string[] = [];
  for (let i = 0; i < approaches.length - 1; i++) {
    const x1 = startX + i * (cardW + 12) + cardW;
    const x2 = startX + (i + 1) * (cardW + 12);
    const d = flowingCurve(x1, cardY + 26, x2, cardY + 26, -8);
    connectors.push(`<path d="${d}" fill="none" stroke="${p.teal2}" stroke-width="0.6" opacity="0.15"/>`);
  }

  const bgSpirals = [
    [950, 80, 5, 50, 1.5], [150, 250, 3, 35, 1.2], [1050, 250, 4, 40, 1.3]
  ].map(([cx, cy, r1, r2, t]) => {
    const d = spiralPath(cx, cy, r1, r2, t, cx / 100);
    return `<path d="${d}" fill="none" stroke="${p.teal2}" stroke-width="0.6" opacity="0.07"/>`;
  });

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <defs>
    <linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${p.bg2}"/>
      <stop offset="1" stop-color="${p.bg1}"/>
    </linearGradient>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#abg)"/>

  <!-- Background spirals -->
${bgSpirals.join("\n")}

  <!-- Radial diagram -->
${radial.join("\n")}

  <!-- Section title -->
  <text x="115" y="50" fill="${p.gold1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="20" font-weight="600" letter-spacing="3">About</text>
  <line x1="115" y1="60" x2="250" y2="60" stroke="${p.gold1}" stroke-width="0.5" opacity="0.3"/>

  <!-- Bio text -->
  <text x="115" y="95" fill="${p.text2}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="13" font-weight="400">${escapeXml(content.about[0] || "")}</text>
  <text x="115" y="115" fill="${p.text2}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="13" font-weight="400">${escapeXml(content.about[1] || "")}</text>
  <text x="115" y="148" fill="${p.text3}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300">${escapeXml(content.about[2] || "")}</text>
  <text x="115" y="168" fill="${p.text3}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="300">${escapeXml(content.about[3] || "")}</text>

  <!-- My Approach heading -->
  <text x="${f1(W / 2)}" y="200" fill="${p.accent}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="14" font-weight="500" letter-spacing="2" text-anchor="middle">My Approach</text>

  <!-- Approach cards -->
${cards.join("\n")}

  <!-- Connectors -->
${connectors.join("\n")}
</svg>`;
}

function generateSkills(mode: "dark" | "light", content: Content): string {
  const p = THEMES[mode];
  const W = 1100, H = 270;

  const techs = content.skills.slice(0, 12).map(({ label }) => label);
  const rows = [
    techs.slice(0, 4),
    techs.slice(4, 8),
    techs.slice(8, 12),
  ];

  const cardW = 130, cardH = 52;
  const gapX = 16, gapY = 14;
  const totalW = 4 * cardW + 3 * gapX;
  const startX = (W - totalW) / 2;
  const startY = 75;

  const cards: string[] = [];
  const allPositions: [number, number][] = [];
  rows.forEach((row, rowI) => {
    row.forEach((tech, colI) => {
      const x = startX + colI * (cardW + gapX);
      const y = startY + rowI * (cardH + gapY);
      allPositions.push([x + cardW / 2, y + cardH / 2]);
      cards.push(`<rect x="${f1(x)}" y="${f1(y)}" width="${cardW}" height="${cardH}" rx="6" fill="${p.card_bg1}" stroke="${p.teal1}" stroke-width="0.7" opacity="0.85"/>`);
      cards.push(`<circle cx="${f1(x + 14)}" cy="${f1(y + cardH / 2)}" r="2" fill="${p.gold1}" opacity="0.5"/>`);
      cards.push(`<text x="${f1(x + 24)}" y="${f1(y + cardH / 2 + 4)}" fill="${p.text2}" font-family="'JetBrains Mono','SF Mono',monospace" font-size="11.5" font-weight="500">${escapeXml(tech)}</text>`);
    });
  });

  const flowLines: string[] = [];
  for (let i = 0; i < allPositions.length - 1; i++) {
    if ((i + 1) % 4 !== 0) {
      const [x1, y1] = allPositions[i];
      const [x2, y2] = allPositions[i + 1];
      flowLines.push(`<line x1="${f1(x1 + cardW / 2 - 5)}" y1="${f1(y1)}" x2="${f1(x2 - cardW / 2 + 5)}" y2="${f1(y2)}" stroke="${p.teal2}" stroke-width="0.4" opacity="0.1"/>`);
    }
  }

  const bgSpirals = [
    [100, 130, 40], [1000, 200, 35], [550, 30, 25]
  ].map(([cx, cy, r]) => {
    const d = spiralPath(cx, cy, 3, r, 1.3, cx / 80);
    return `<path d="${d}" fill="none" stroke="${p.teal2}" stroke-width="0.5" opacity="0.06"/>`;
  });

  const titleSpiral = spiralPath(100, 35, 3, 15, 1.0, 0);

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <defs>
    <linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${p.bg1}"/>
      <stop offset="1" stop-color="${p.bg2}"/>
    </linearGradient>
    ${gridPattern("sgrid", 45, p.teal1, mode === "dark" ? 0.02 : 0.035)}
  </defs>
  <rect width="${W}" height="${H}" fill="url(#sbg)"/>
  <rect width="${W}" height="${H}" fill="url(#sgrid)"/>

  <!-- Background spirals -->
${bgSpirals.join("\n")}

  <!-- Title -->
  <path d="${titleSpiral}" fill="none" stroke="${p.teal2}" stroke-width="0.6" opacity="0.2"/>
  <text x="125" y="42" fill="${p.gold1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="18" font-weight="600" letter-spacing="2">Technologies &amp; Skills</text>
  <line x1="125" y1="52" x2="400" y2="52" stroke="${p.gold1}" stroke-width="0.4" opacity="0.25"/>

  <!-- Tech cards -->
${cards.join("\n")}

  <!-- Flow lines -->
${flowLines.join("\n")}
</svg>`;
}

function generateProjectsTitle(mode: "dark" | "light"): string {
  const p = THEMES[mode];
  const W = 1100, H = 60;
  const spiralD = spiralPath(35, 30, 3, 18, 1.2, 0.5);
  const waveD = wavePath(70, 45, W - 70, 45, 4, 8);

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <rect width="${W}" height="${H}" fill="${p.bg1}"/>
  <path d="${spiralD}" fill="none" stroke="${p.teal2}" stroke-width="0.7" opacity="0.2"/>
  <text x="60" y="35" fill="${p.gold1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="18" font-weight="600" letter-spacing="2">Selected Projects</text>
  <path d="${waveD}" fill="none" stroke="${p.gold1}" stroke-width="0.5" opacity="0.2"/>
  <line x1="0" y1="58" x2="${W}" y2="58" stroke="${p.teal1}" stroke-width="0.3" opacity="0.1"/>
</svg>`;
}

function generateProjectCard(num: number, name: string, desc: string, tags: string[], patternType: string, mode: "dark" | "light"): string {
  const p = THEMES[mode];
  const W = 320, H = 210;
  const patternPaths: string[] = [];

  if (patternType === "orbital") {
    for (let i = 0; i < 4; i++) {
      const cx = W / 2, cy = 42;
      const rx = 30 + i * 20;
      const ry = 12 + i * 8;
      const angle = i * 25;
      patternPaths.push(`<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${p.teal2}" stroke-width="0.7" opacity="${f1(0.2 - i * 0.04)}" transform="rotate(${angle} ${cx} ${cy})"/>`);
    }
    patternPaths.push(`<circle cx="${W / 2}" cy="42" r="3" fill="${p.gold1}" opacity="0.4"/>`);
    for (const angle of [0, 90, 180, 270]) {
      const x = W / 2 + 40 * Math.cos((angle * Math.PI) / 180);
      const y = 42 + 15 * Math.sin((angle * Math.PI) / 180);
      patternPaths.push(`<circle cx="${f1(x)}" cy="${f1(y)}" r="1.5" fill="${p.teal3}" opacity="0.3"/>`);
    }
  } else if (patternType === "network") {
    const nodes: [number, number][] = [
      [W / 2, 20], [W / 2 - 60, 45], [W / 2 + 60, 45], [W / 2 - 90, 70], [W / 2 - 30, 70], [W / 2 + 30, 70], [W / 2 + 90, 70]
    ];
    nodes.forEach(([x, y]) => {
      patternPaths.push(`<circle cx="${x}" cy="${y}" r="3" fill="${p.teal2}" opacity="0.25"/>`);
    });
    const edges: [number, number][] = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]];
    edges.forEach(([a, b]) => {
      const d = flowingCurve(nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], -8);
      patternPaths.push(`<path d="${d}" fill="none" stroke="${p.teal2}" stroke-width="0.8" opacity="0.2"/>`);
    });
  } else if (patternType === "pages") {
    for (let i = 0; i < 3; i++) {
      const x = W / 2 - 50 + i * 30;
      const y = 15 + i * 5;
      patternPaths.push(`<rect x="${x}" y="${y}" width="40" height="55" rx="3" fill="none" stroke="${p.teal2}" stroke-width="0.7" opacity="${f1(0.2 - i * 0.05)}"/>`);
    }
    const d = wavePath(W / 2 - 60, 40, W / 2 + 70, 40, 15, 2);
    patternPaths.push(`<path d="${d}" fill="none" stroke="${p.gold1}" stroke-width="0.6" opacity="0.2"/>`);
  } else if (patternType === "routing") {
    const nodes: [number, number][] = [
      [50, 40], [W / 2 - 40, 25], [W / 2 + 40, 25], [W - 50, 40], [W / 2, 55], [80, 65], [W - 80, 65]
    ];
    nodes.forEach(([x, y]) => {
      patternPaths.push(`<circle cx="${x}" cy="${y}" r="3" fill="${p.teal2}" opacity="0.2"/>`);
      patternPaths.push(`<circle cx="${x}" cy="${y}" r="6" fill="none" stroke="${p.teal2}" stroke-width="0.4" opacity="0.12"/>`);
    });
    const connections: [number, number][] = [[0, 1], [1, 2], [2, 3], [1, 4], [2, 4], [4, 5], [4, 6]];
    connections.forEach(([a, b]) => {
      patternPaths.push(`<line x1="${nodes[a][0]}" y1="${nodes[a][1]}" x2="${nodes[b][0]}" y2="${nodes[b][1]}" stroke="${p.teal2}" stroke-width="0.6" opacity="0.15"/>`);
    });
  } else {
    // radial
    const cx = W / 2, cy = 42;
    for (const r of [15, 30, 45]) {
      patternPaths.push(`<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${p.teal2}" stroke-width="0.5" opacity="${f1(0.18 - r * 0.003)}"/>`);
    }
    for (let i = 0; i < 8; i++) {
      const angle = (i * Math.PI) / 4;
      const x2 = cx + 50 * Math.cos(angle);
      const y2 = cy + 50 * Math.sin(angle);
      patternPaths.push(`<line x1="${cx}" y1="${cy}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${p.teal2}" stroke-width="0.4" opacity="0.1"/>`);
    }
    patternPaths.push(`<circle cx="${cx}" cy="${cy}" r="3" fill="${p.gold1}" opacity="0.35"/>`);
  }

  const tagText = tags.join(" · ");
  const line1 = desc.slice(0, 50);
  const line2 = desc.length > 50 ? desc.slice(50) : "";

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <defs>
    <linearGradient id="cbg${num}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${p.card_bg1}"/>
      <stop offset="0.7" stop-color="${p.card_bg2}"/>
      <stop offset="1" stop-color="${p.bg2}"/>
    </linearGradient>
    <clipPath id="cclip${num}"><rect x="1" y="1" width="${W - 2}" height="80" rx="10"/></clipPath>
  </defs>

  <!-- Card background -->
  <rect width="${W}" height="${H}" rx="10" fill="url(#cbg${num})" stroke="${p.teal1}" stroke-width="0.8" opacity="0.9"/>

  <!-- Pattern area (clipped) -->
  <g clip-path="url(#cclip${num})">
${patternPaths.join("\n")}
  </g>

  <!-- Divider -->
  <line x1="20" y1="85" x2="${W - 20}" y2="85" stroke="${p.teal1}" stroke-width="0.4" opacity="0.2"/>

  <!-- Project number -->
  <text x="20" y="108" fill="${p.teal2}" font-family="'JetBrains Mono',monospace" font-size="9" font-weight="400" opacity="0.5">PROJECT ${String(num).padStart(2, "0")}</text>

  <!-- Project name -->
  <text x="20" y="130" fill="${p.text1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="15" font-weight="700">${escapeXml(name)}</text>

  <!-- Description -->
  <text x="20" y="152" fill="${p.text3}" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="300">${escapeXml(line1)}</text>
  <text x="20" y="166" fill="${p.text3}" font-family="'Segoe UI',sans-serif" font-size="10" font-weight="300">${escapeXml(line2)}</text>

  <!-- Tags -->
  <text x="20" y="${H - 16}" fill="${p.gold1}" font-family="'JetBrains Mono',monospace" font-size="9" font-weight="500" opacity="0.7">${escapeXml(tagText)}</text>
</svg>`;
}

function generateFooter(mode: "dark" | "light", content: Content): string {
  const p = THEMES[mode];
  const W = 1100, H = 160;

  const positions: [number, number, number, number, number, number, number][] = [
    [150, 30, 5, 60, 1.8, 0, 0.2],
    [400, 40, 3, 45, 1.5, 1.2, 0.12],
    [650, 25, 4, 55, 1.6, 2.5, 0.15],
    [900, 35, 6, 50, 1.4, 0.8, 0.1],
    [250, 80, 3, 30, 1.0, 3.2, 0.06],
    [750, 90, 4, 35, 1.2, 1.8, 0.05],
    [1050, 50, 3, 40, 1.3, 4.0, 0.08],
    [50, 60, 5, 35, 1.1, 2.2, 0.07],
  ];
  const fadingSpirals = positions.map(([cx, cy, r1, r2, t, sa, op]) => {
    const d = spiralPath(cx, cy, r1, r2, t, sa);
    return `<path d="${d}" fill="none" stroke="${p.teal2}" stroke-width="0.6" opacity="${op}"/>`;
  });

  const waveD = wavePath(0, 130, W, 130, 5, 12);
  const brand = content.brand?.latin || "solaymantech.me";

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
  <defs>
    <linearGradient id="fbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${p.bg2}"/>
      <stop offset="1" stop-color="${p.bg1}"/>
    </linearGradient>
  </defs>
  <rect width="${W}" height="${H}" fill="url(#fbg)"/>

  <!-- Fading spirals -->
${fadingSpirals.join("\n")}

  <!-- Fading wave -->
  <path d="${waveD}" fill="none" stroke="${p.gold1}" stroke-width="0.4" opacity="0.1"/>

  <!-- Footer text -->
  <text x="${f1(W / 2)}" y="50" fill="${p.gold1}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="18" font-weight="600" letter-spacing="4" text-anchor="middle">${escapeXml(content.footer.line1)}</text>
  <text x="${f1(W / 2)}" y="78" fill="${p.teal2}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="12" font-weight="400" letter-spacing="2" text-anchor="middle">${escapeXml(content.footer.line2)}</text>
  <text x="${f1(W / 2)}" y="105" fill="${p.accent}" font-family="'Segoe UI','SF Pro Display','Helvetica Neue',sans-serif" font-size="11" font-weight="300" letter-spacing="1" text-anchor="middle">${escapeXml(brand)}</text>

  <!-- Bottom fade line -->
  <line x1="300" y1="120" x2="${W - 300}" y2="120" stroke="${p.gold1}" stroke-width="0.3" opacity="0.15"/>
</svg>`;
}

export const vangoghStyle: StyleModule = {
  id: "vangogh",
  name: "Van Gogh Starry Flow",
  keywords: ["vangogh", "spirals", "starry", "waves", "flow", "algorithmic"],
  palette: {
    dark: ["#0A1A1F", "#0F2832", "#3B7A8C", "#C4A843", "#8BBFC4"],
    light: ["#FAFDF7", "#F0F5EE", "#2D6B77", "#8A7030", "#3B7A8C"],
  },
  motion: "lively",
  render(content: Content, _ctx: RenderCtx): RenderResult {
    const files: Record<string, string> = {};
    const patternTypes = ["orbital", "network", "pages", "routing", "radial"];

    for (const theme of ["dark", "light"] as const) {
      const headerSvg = generateHeader(theme, content);
      files[`hero-${theme}.svg`] = headerSvg;
      files[`header-${theme}.svg`] = headerSvg;
      files[`btn-github-${theme}.svg`] = generateButton("GitHub", theme);
      files[`btn-linkedin-${theme}.svg`] = generateButton("LinkedIn", theme);
      files[`btn-portfolio-${theme}.svg`] = generateButton("Portfolio", theme);
      files[`about-${theme}.svg`] = generateAbout(theme, content);
      files[`skills-${theme}.svg`] = generateSkills(theme, content);
      files[`projects-title-${theme}.svg`] = generateProjectsTitle(theme);
      files[`footer-${theme}.svg`] = generateFooter(theme, content);

      content.projects.forEach((proj, i) => {
        const pType = patternTypes[i % patternTypes.length];
        files[`card-${proj.slug}-${theme}.svg`] = generateProjectCard(i + 1, proj.title, `${proj.line1} ${proj.line2}`, proj.tags, pType, theme);
      });
    }

    const cardPics = (items: typeof content.projects) =>
      items.map((p) => `<a href="${content.github}/${p.slug}">${pic(`card-${p.slug}`, `${p.title}: ${p.line1} ${p.line2}`, "24%")}</a>`).join("\n");

    const row1 = content.projects.slice(0, 4);
    const row2 = content.projects.slice(4);

    const readmeParts = [
      pic("header", `${content.name}, ${content.role}. Van Gogh flowing spirals aesthetic.`, "100%"),
      `<a href="${content.github}">${pic("btn-github", "GitHub profile", "150")}</a>&nbsp;\n<a href="${content.linkedin}">${pic("btn-linkedin", "LinkedIn profile", "150")}</a>&nbsp;\n<a href="${content.portfolio}">${pic("btn-portfolio", "Portfolio website", "150")}</a>`,
      pic("about", "About me and my approach", "100%"),
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
export default vangoghStyle;
