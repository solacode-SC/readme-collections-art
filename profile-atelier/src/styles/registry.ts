import { StyleModule } from "../types";
import { AUTHENTIC_STYLES, getAuthenticStyleById } from "./authenticTemplates";

// Procedural fallback modules
import { constellationStyle } from "./constellation";
import { terminalStyle } from "./terminal";
import { qamariyaStyle } from "./qamariya";
import { blueprintStyle } from "./blueprint";
import { helixStyle } from "./helix";

// Other styles kept for compatibility
const ADDITIONAL_STYLES: StyleModule[] = [
  constellationStyle,
  terminalStyle,
  qamariyaStyle,
  blueprintStyle,
  helixStyle,
];

// Combine: authentic templates first, then any extra procedural styles
export const STYLES: StyleModule[] = [
  ...AUTHENTIC_STYLES,
  ...ADDITIONAL_STYLES.filter((s) => !AUTHENTIC_STYLES.some((a) => a.id === s.id)),
];

const ALIASES: Record<string, string> = {
  phoenix: "citadel",
  "solacode-readme": "citadel",
  "solacode-lotus-readme": "lotus",
  "solacode-readme-frost": "frost",
  "solacode-isekai-readme": "isekai",
  "solacode-ghost-readme": "ghost",
  "solacode-readme-lapis": "lapis",
  "solacode-readme-canopy": "canopy",
  "solacode-readme-andalus": "andalus",
  "solayman-tree-readme": "tree",
  "solayman-floral-readme-v2": "floral",
  "solayman-vangogh-readme": "vangogh",
  "profile-readme-swirl": "swirl",
  "profile-readme-moongate": "moongate",
  "profile-readme-inkscroll": "inkscroll",
  "profile-readme-garden": "garden",
  "profile-readme-codex": "codex",
  "profile-readme-andalusn": "andalusn",
  "profile-readme-red": "red",
  "profile-readme": "classic",
  jjjjj: "lilypond",
};

export function getStyleById(id: string): StyleModule {
  const targetId = ALIASES[id] || id;
  const authentic = getAuthenticStyleById(targetId);
  if (authentic) return authentic;

  const found = STYLES.find((s) => s.id === targetId || s.id === id);
  return found || STYLES[0];
}
