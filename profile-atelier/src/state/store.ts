import { Content, StyleModule } from "../types";
import { DEFAULT_CONTENT } from "../lib/defaultContent";
import { getStyleById, STYLES } from "../styles/registry";

export type ThemeMode = "dark" | "light";
export type MotionMode = "play" | "step" | "reduced";
export type DeviceMode = "desktop" | "phone";

interface AppState {
  content: Content;
  selectedStyleId: string;
  theme: ThemeMode;
  motion: MotionMode;
  device: DeviceMode;
  filterKeyword: string | null;
}

const STORAGE_KEY = "profile_atelier_content_v1";

function loadSavedContent(): Content {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      return JSON.parse(raw);
    }
  } catch (e) {
    console.error("Failed to load content from localStorage", e);
  }
  return DEFAULT_CONTENT;
}

export function saveContent(content: Content): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(content));
  } catch (e) {
    console.error("Failed to save content to localStorage", e);
  }
}

export const initialAppState: AppState = {
  content: loadSavedContent(),
  selectedStyleId: STYLES[0].id,
  theme: "dark",
  motion: "play",
  device: "desktop",
  filterKeyword: null,
};
