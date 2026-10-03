import { StyleModule } from "../types";
import { swirlStyle } from "./swirl";
import { moongateStyle } from "./moongate";
import { gardenStyle } from "./garden";
import { phoenixStyle } from "./phoenix";
import { andalusStyle } from "./andalus";
import { codexStyle } from "./codex";
import { inkscrollStyle } from "./inkscroll";
import { frostStyle } from "./frost";
import { lapisStyle } from "./lapis";
import { canopyStyle } from "./canopy";
import { citadelStyle } from "./citadel";
import { lotusStyle } from "./lotus";
import { ghostStyle } from "./ghost";
import { isekaiStyle } from "./isekai";
import { vangoghStyle } from "./vangogh";
import { floralStyle } from "./floral";
import { treeStyle } from "./tree";
import { constellationStyle } from "./constellation";
import { terminalStyle } from "./terminal";
import { qamariyaStyle } from "./qamariya";
import { lilypondStyle } from "./lilypond";
import { blueprintStyle } from "./blueprint";
import { helixStyle } from "./helix";

export const STYLES: StyleModule[] = [
  swirlStyle,
  moongateStyle,
  gardenStyle,
  phoenixStyle,
  andalusStyle,
  codexStyle,
  inkscrollStyle,
  frostStyle,
  lapisStyle,
  canopyStyle,
  citadelStyle,
  lotusStyle,
  ghostStyle,
  isekaiStyle,
  vangoghStyle,
  floralStyle,
  treeStyle,
  constellationStyle,
  terminalStyle,
  qamariyaStyle,
  lilypondStyle,
  blueprintStyle,
  helixStyle,
];

export function getStyleById(id: string): StyleModule {
  return STYLES.find((s) => s.id === id) || STYLES[0];
}

