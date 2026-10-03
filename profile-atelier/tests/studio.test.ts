import { describe, it, expect } from "vitest";
import { escapeXml } from "../src/lib/svg";
import { swirlStyle } from "../src/styles/swirl";
import { DEFAULT_CONTENT } from "../src/lib/defaultContent";
import { validateContent } from "../src/lib/validate";

describe("XML Escaping & Security", () => {
  it("escapes all special characters including & < > \" '", () => {
    const input = `AT&T <script>alert("xss")</script> 'hello'`;
    const escaped = escapeXml(input);
    expect(escaped).toBe("AT&amp;T &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt; &apos;hello&apos;");
    expect(escaped).not.toContain("<script>");
  });

  it("handles null or undefined safely", () => {
    expect(escapeXml(null)).toBe("");
    expect(escapeXml(undefined)).toBe("");
  });
});

describe("Content Validation", () => {
  it("validates github handle format correctly", () => {
    const valid = validateContent(DEFAULT_CONTENT);
    expect(valid.filter((v) => v.type === "error")).toHaveLength(0);

    const invalid = validateContent({
      ...DEFAULT_CONTENT,
      handle: "Invalid Handle With Spaces!",
    });
    expect(invalid.some((v) => v.field === "handle" && v.type === "error")).toBe(true);
  });

  it("warns about placeholder LinkedIn URL", () => {
    const issues = validateContent(DEFAULT_CONTENT);
    const linkedInIssue = issues.find((v) => v.field === "linkedin");
    expect(linkedInIssue).toBeDefined();
    expect(linkedInIssue?.type).toBe("warning");
  });
});

describe("Swirl Procedural Engine", () => {
  it("renders with default content without throwing", () => {
    const mockCtx = {
      loadImage: async () => ({}) as any,
      cropToDataUrl: () => "data:image/jpeg;base64,mock",
    };
    const res = swirlStyle.render(DEFAULT_CONTENT, mockCtx);
    expect(res).toBeDefined();
    if ("then" in res) {
      // Async handling
    } else {
      expect(res.readme).toContain("solacode-SC");
      expect(res.readme).toContain("<picture>");
      expect(res.files["hero-dark.svg"]).toBeDefined();
      expect(res.files["hero-light.svg"]).toBeDefined();
      expect(res.meta.bytes).toBeGreaterThan(1000);
    }
  });

  it("safely handles XSS attempts in name and project titles", () => {
    const attackContent = {
      ...DEFAULT_CONTENT,
      name: "Solayman & <Co>",
      projects: [
        {
          title: "Attack & Test <script>",
          slug: "attack-test",
          line1: "line 1 & 2",
          line2: "line 2 <tag>",
          tags: ["XSS & 1", "<tag>"],
        },
      ],
    };
    const mockCtx = {
      loadImage: async () => ({}) as any,
      cropToDataUrl: () => "data:image/jpeg;base64,mock",
    };
    const res = swirlStyle.render(attackContent, mockCtx);
    if (!("then" in res)) {
      expect(res.files["hero-dark.svg"]).not.toContain("<Co>");
      expect(res.files["hero-dark.svg"]).toContain("&lt;Co&gt;");
      expect(res.files["card-attack-test-dark.svg"]).not.toContain("<script>");
      expect(res.files["card-attack-test-dark.svg"]).toContain("&lt;script&gt;");
    }
  });
});

describe("Style Modules High Fidelity Rendering", () => {
  const mockCtx = {
    loadImage: async () => ({}) as any,
    cropToDataUrl: () => "data:image/jpeg;base64,mockImage",
  };

  it("renders Andalus with authentic horseshoe arch and zellige features", async () => {
    const { andalusStyle } = await import("../src/styles/andalus");
    const res = await andalusStyle.render(DEFAULT_CONTENT, mockCtx);
    expect(res.files["hero-dark.svg"]).toBeDefined();
    expect(res.files["hero-dark.svg"]).toContain("clip-path");
    expect(res.files["hero-dark.svg"]).toContain("polygon"); // star8
    expect(res.files["card-lazyequation-dark.svg"]).toBeDefined();
    expect(res.files["footer-dark.svg"]).toBeDefined();
    expect(res.readme).toContain("solacode-SC");
  });

  it("renders Codex with illuminated miniature arch and gold foil details", async () => {
    const { codexStyle } = await import("../src/styles/codex");
    const res = await codexStyle.render(DEFAULT_CONTENT, mockCtx);
    expect(res.files["hero-dark.svg"]).toBeDefined();
    expect(res.files["hero-dark.svg"]).toContain("arch");
    expect(res.files["footer-dark.svg"]).toContain("EXPLICIT LIBER");
    expect(res.files["skills-dark.svg"]).toBeDefined();
  });

  it("renders Inkscroll with hanging scroll and seals", async () => {
    const { inkscrollStyle } = await import("../src/styles/inkscroll");
    const res = await inkscrollStyle.render(DEFAULT_CONTENT, mockCtx);
    expect(res.files["hero-dark.svg"]).toBeDefined();
    expect(res.files["hero-dark.svg"]).toContain("sway");
    expect(res.files["footer-dark.svg"]).toContain("wave");
  });
});
