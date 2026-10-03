export function escapeXml(str: string | undefined | null): string {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

export function f1(v: number): string {
  return v.toFixed(1).replace(/\.0$/, "").replace(/(\.\d)0$/, "$1");
}

export function clamp(v: number, min: number, max: number): number {
  return Math.min(Math.max(v, min), max);
}

// Seeded pseudo-random number generator (Mulberry32)
export function createRng(seed: number) {
  let s = seed >>> 0;
  return function () {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function ptsPath(pts: [number, number][]): string {
  return "M" + pts.map(([x, y]) => `${f1(x)} ${f1(y)}`).join("L");
}

// Helper to generate <picture> element for README.md
export function pic(name: string, alt: string, width?: string, extraStyle?: string): string {
  const wAttr = width ? ` width="${width}"` : "";
  const sAttr = extraStyle ? ` style="${extraStyle}"` : "";
  return `<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/${name}-dark.svg">
  <img src="assets/${name}-light.svg" alt="${escapeXml(alt)}"${wAttr}${sAttr}>
</picture>`;
}
