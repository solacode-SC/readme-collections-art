import { describe, it, expect } from "vitest";
import { renderGithubReadme } from "../src/preview/engine";
import { substituteVariables } from "../src/preview/variables";
import { resolveAsset } from "../src/preview/assetResolver";
import { sanitizeHtml } from "../src/preview/sanitizer";
import { swirlStyle } from "../src/styles/swirl";
import { andalusStyle } from "../src/styles/andalus";
import { codexStyle } from "../src/styles/codex";
import { DEFAULT_CONTENT } from "../src/lib/defaultContent";

describe("Variables Interpolation", () => {
  it("replaces single and double curly brackets and dollar syntax", () => {
    const template = "Hello {{name}}! Welcome to ${role}.";
    const res = substituteVariables(template, { name: "Solayman", role: "Atelier" });
    expect(res).toBe("Hello Solayman! Welcome to Atelier.");
  });

  it("resolves nested and array paths", () => {
    const template = "Primary: {{projects[0].title}}, Secondary: {{projects.1.title}}";
    const res = substituteVariables(template, {
      projects: [{ title: "First" }, { title: "Second" }],
    });
    expect(res).toBe("Primary: First, Secondary: Second");
  });

  it("leaves unmatched keys unchanged", () => {
    const template = "Hello {{unknown}}!";
    const res = substituteVariables(template, {});
    expect(res).toBe("Hello {{unknown}}!");
  });
});

describe("Asset Resolution", () => {
  const mockAssets = {
    "hero-dark.svg": "blob:http://localhost/hero-dark-blob",
    "assets/hero-light.svg": "blob:http://localhost/hero-light-blob",
  };

  it("resolves exact and basename matches", () => {
    const r1 = resolveAsset("assets/hero-dark.svg", mockAssets);
    expect(r1.resolvedUrl).toBe("blob:http://localhost/hero-dark-blob");
    expect(r1.warning).toBeUndefined();

    const r2 = resolveAsset("assets/hero-light.svg", mockAssets);
    expect(r2.resolvedUrl).toBe("blob:http://localhost/hero-light-blob");
    expect(r2.warning).toBeUndefined();
  });

  it("resolves theme-variant fallbacks", () => {
    const resDark = resolveAsset("assets/hero.svg", mockAssets, "dark");
    expect(resDark.resolvedUrl).toBe("blob:http://localhost/hero-dark-blob");

    const resLight = resolveAsset("assets/hero.svg", mockAssets, "light");
    expect(resLight.resolvedUrl).toBe("blob:http://localhost/hero-light-blob");
  });

  it("preserves external URLs untouched", () => {
    const url = "https://img.shields.io/badge/test-pass-green";
    const res = resolveAsset(url, mockAssets);
    expect(res.resolvedUrl).toBe(url);
    expect(res.warning).toBeUndefined();
  });

  it("returns warnings for missing assets", () => {
    const res = resolveAsset("assets/missing-asset.svg", mockAssets);
    expect(res.resolvedUrl).toBe("assets/missing-asset.svg");
    expect(res.warning).toBeDefined();
    expect(res.warning?.path).toBe("assets/missing-asset.svg");
    expect(res.warning?.normalized).toBe("assets/missing-asset.svg");
  });
});

describe("Sanitizer Security", () => {
  it("strips malicious script tags and inline handlers", () => {
    const dirty = `<p>Safe</p><script>alert('xss')</script><img src="x" onerror="alert(1)">`;
    const clean = sanitizeHtml(dirty);
    expect(clean).toContain("<p>Safe</p>");
    expect(clean).not.toContain("<script>");
    expect(clean).not.toContain("onerror");
  });

  it("allows safe github elements like picture, source, details, and align", () => {
    const html = `<div align="center"><picture><source srcset="blob:http://localhost/dark.svg" media="(prefers-color-scheme: dark)"><img src="blob:http://localhost/light.svg" alt="logo"></picture><details><summary>More</summary>Content</details></div>`;
    const clean = sanitizeHtml(html);
    expect(clean).toContain("<picture>");
    expect(clean).toContain("<source");
    expect(clean).toContain("<details>");
    expect(clean).toContain("<summary>");
    expect(clean).toContain('align="center"');
    expect(clean).toContain('src="blob:http://localhost/light.svg"');
  });

  it("preserves data URIs on both img and source", () => {
    const html = `<picture><source srcset="data:image/svg+xml;base64,PHN2Zz4="><img src="data:image/svg+xml;base64,PHN2Zz4=" alt="img"></picture>`;
    const clean = sanitizeHtml(html);
    expect(clean).toContain('srcset="data:image/svg+xml;base64,PHN2Zz4="');
    expect(clean).toContain('src="data:image/svg+xml;base64,PHN2Zz4="');
  });
});

describe("README Rendering Engine", () => {
  it("renders basic markdown headings and formatting", async () => {
    const markdown = "# Test Heading\n\nThis is **bold** and *italic*.";
    const result = await renderGithubReadme(markdown);

    expect(result.html).toContain("<h1");
    expect(result.html).toContain("<strong>bold</strong>");
    expect(result.html).toContain("<em>italic</em>");
    expect(result.debugReport.elementCount).toBeGreaterThan(0);
  });

  it("renders GFM tables and records tableCount", async () => {
    const markdown = `
| Name | Role |
| :--- | :--- |
| Sola | Dev |
    `.trim();

    const result = await renderGithubReadme(markdown);
    expect(result.html).toContain("<table");
    expect(result.html).toContain("Name</th>");
    expect(result.debugReport.tableCount).toBe(1);
  });

  it("switches picture source and updates source media for dark and light theme", async () => {
    const markdown = `
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <img src="assets/hero-light.svg" alt="Hero">
</picture>
    `.trim();

    const assets = {
      "hero-dark.svg": "blob:dark-url",
      "hero-light.svg": "blob:light-url",
    };

    const darkResult = await renderGithubReadme(markdown, { theme: "dark", assets });
    expect(darkResult.html).toContain('src="blob:dark-url"');
    expect(darkResult.html).toContain('media="all"');
    expect(darkResult.html).toContain('srcset="blob:dark-url"');

    const lightResult = await renderGithubReadme(markdown, { theme: "light", assets });
    expect(lightResult.html).toContain('src="blob:light-url"');
    expect(lightResult.html).toContain('media="not all"');
  });

  it("handles dual source pictures (dark and light sources)", async () => {
    const markdown = `
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero-light.svg" alt="Hero">
</picture>
    `.trim();

    const assets = {
      "hero-dark.svg": "blob:dark-url",
      "hero-light.svg": "blob:light-url",
    };

    const darkResult = await renderGithubReadme(markdown, { theme: "dark", assets });
    expect(darkResult.html).toContain('src="blob:dark-url"');

    const lightResult = await renderGithubReadme(markdown, { theme: "light", assets });
    expect(lightResult.html).toContain('src="blob:light-url"');
  });

  it("tracks missing assets warnings in debug mode", async () => {
    const markdown = `![Missing](assets/nonexistent.png)`;
    const result = await renderGithubReadme(markdown, { debugMode: true });

    expect(result.debugReport.warnings.length).toBe(1);
    expect(result.debugReport.warnings[0].path).toBe("assets/nonexistent.png");
  });

  it("authentically renders Swirl template README without recoding template", async () => {
    const mockCtx = {
      loadImage: async () => ({}) as any,
      cropToDataUrl: () => "data:image/svg+xml;base64,mock",
    };
    const res = await swirlStyle.render(DEFAULT_CONTENT, mockCtx);
    const mockBlobAssets: Record<string, string> = {};
    for (const [key] of Object.entries(res.files)) {
      mockBlobAssets[key] = `blob:http://localhost/${key}`;
    }

    const darkResult = await renderGithubReadme(res.readme, {
      theme: "dark",
      assets: mockBlobAssets,
    });
    expect(darkResult.html).toContain('align="center"');
    expect(darkResult.html).toContain('src="blob:http://localhost/hero-dark.svg"');
    expect(darkResult.html).toContain('src="blob:http://localhost/about-dark.svg"');
    expect(darkResult.html).toContain('width="24%"');
    expect(darkResult.debugReport.warnings).toHaveLength(0);

    const lightResult = await renderGithubReadme(res.readme, {
      theme: "light",
      assets: mockBlobAssets,
    });
    expect(lightResult.html).toContain('src="blob:http://localhost/hero-light.svg"');
    expect(lightResult.html).toContain('src="blob:http://localhost/about-light.svg"');
    expect(lightResult.debugReport.warnings).toHaveLength(0);
  });

  it("authentically renders Andalus template README without recoding template", async () => {
    const mockCtx = {
      loadImage: async () => ({}) as any,
      cropToDataUrl: () => "data:image/svg+xml;base64,mock",
    };
    const res = await andalusStyle.render(DEFAULT_CONTENT, mockCtx);
    const mockBlobAssets: Record<string, string> = {};
    for (const [key] of Object.entries(res.files)) {
      mockBlobAssets[key] = `blob:http://localhost/${key}`;
    }

    const darkResult = await renderGithubReadme(res.readme, {
      theme: "dark",
      assets: mockBlobAssets,
    });
    expect(darkResult.html).toContain('src="blob:http://localhost/hero-dark.svg"');
    expect(darkResult.html).toContain('src="blob:http://localhost/skills-dark.svg"');
    expect(darkResult.debugReport.warnings).toHaveLength(0);
  });

  it("authentically renders Codex template README without recoding template", async () => {
    const mockCtx = {
      loadImage: async () => ({}) as any,
      cropToDataUrl: () => "data:image/svg+xml;base64,mock",
    };
    const res = await codexStyle.render(DEFAULT_CONTENT, mockCtx);
    const mockBlobAssets: Record<string, string> = {};
    for (const [key] of Object.entries(res.files)) {
      mockBlobAssets[key] = `blob:http://localhost/${key}`;
    }

    const darkResult = await renderGithubReadme(res.readme, {
      theme: "dark",
      assets: mockBlobAssets,
    });
    expect(darkResult.html).toContain('src="blob:http://localhost/hero-dark.svg"');
    expect(darkResult.debugReport.warnings).toHaveLength(0);
  });
});
