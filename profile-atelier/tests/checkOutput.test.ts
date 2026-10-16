import { describe, it } from "vitest";
import { STYLES } from "../src/styles/registry";
import { DEFAULT_CONTENT } from "../src/lib/defaultContent";
import { renderGithubReadme } from "../src/preview/engine";

describe("Check preview output for all styles", () => {
  const mockCtx = {
    loadImage: async () => ({}) as any,
    cropToDataUrl: () => "data:image/jpeg;base64,mock",
  };

  for (const style of STYLES) {
    it(`checks ${style.id}`, async () => {
      let res;
      try {
        res = await style.render(DEFAULT_CONTENT, mockCtx);
      } catch (err: any) {
        console.error(`FAILED render for ${style.id}:`, err.message);
        throw err;
      }

      const assetUrls: Record<string, string> = {};
      for (const [k, v] of Object.entries(res.files)) {
        assetUrls[k] = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(v)}`;
      }

      const darkResult = await renderGithubReadme(res.readme, {
        theme: "dark",
        assets: assetUrls,
        debugMode: true,
      });

      const lightResult = await renderGithubReadme(res.readme, {
        theme: "light",
        assets: assetUrls,
        debugMode: true,
      });

      if (darkResult.debugReport.warnings.length > 0) {
        console.warn(`[${style.id} DARK WARNINGS]:`, darkResult.debugReport.warnings);
      }
      if (lightResult.debugReport.warnings.length > 0) {
        console.warn(`[${style.id} LIGHT WARNINGS]:`, lightResult.debugReport.warnings);
      }
    });
  }
});
