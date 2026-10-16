export type Theme = "dark" | "light";

export interface AssetWarning {
  path: string;
  normalized: string;
}

export interface DebugReport {
  renderTimeMs: number;
  elementCount: number;
  imageCount: number;
  tableCount: number;
  warnings: AssetWarning[];
}

export interface RenderOptions {
  theme?: Theme;
  variables?: Record<string, any>;
  assets?: Record<string, string>;
  debugMode?: boolean;
  reducedMotion?: boolean;
}

export interface RenderResult {
  html: string;
  debugReport: DebugReport;
}

