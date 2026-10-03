export interface Project {
  title: string;
  slug: string;
  line1: string;
  line2: string;
  tags: string[];
}

export interface Content {
  handle: string;
  name: string;
  role: string;
  pillars: string;
  tagline: string[];
  github: string;
  linkedin: string;
  portfolio: string;
  location?: string;
  brand?: { latin: string; arabic?: string };
  about: string[];
  journey: { lang: string; area: string }[];
  skills: { label: string; mono: string }[];
  projects: Project[];
  footer: { line1: string; line2: string; arabic?: string };
  options: { useArabic: boolean; useCJK: boolean };
}

export interface StyleModule {
  id: string;
  name: string;
  keywords: string[];
  palette: { light: string[]; dark: string[] };
  motion: "none" | "calm" | "lively";
  image?: { file: string; credit?: string; note?: string };
  options?: Array<"useArabic" | "useCJK">;
  render(content: Content, ctx: RenderCtx): Promise<RenderResult> | RenderResult;
}

export interface RenderCtx {
  loadImage(path: string): Promise<HTMLImageElement>;
  cropToDataUrl(
    img: HTMLImageElement,
    box: [number, number, number, number],
    size: [number, number],
    quality?: number
  ): string;
}

export interface RenderResult {
  files: Record<string, string>; // filename -> svg content
  readme: string;
  meta: { bytes: number };
}
