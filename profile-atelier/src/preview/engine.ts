import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkRehype from "remark-rehype";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeHighlight from "rehype-highlight";
import rehypeStringify from "rehype-stringify";

import { RenderOptions, RenderResult, AssetWarning, DebugReport } from "./types";
import { substituteVariables } from "./variables";
import { resolveAsset, isExternalOrSpecialUrl } from "./assetResolver";
import { sanitizeHtml } from "./sanitizer";

interface VisitorContext {
  assets: Record<string, string>;
  theme: "dark" | "light";
  warnings: AssetWarning[];
  elementCount: number;
  imageCount: number;
  tableCount: number;
}

function walkHast(node: any, ctx: VisitorContext) {
  if (!node || typeof node !== "object") return;

  if (node.type === "element") {
    ctx.elementCount++;
    const tag = node.tagName?.toLowerCase();
    const props = node.properties || (node.properties = {});

    // Special handling for <picture> tags to honor the preview's theme toggle
    if (tag === "picture" && Array.isArray(node.children)) {
      let darkSourceNode: any = null;
      let lightSourceNode: any = null;
      let darkSourceUrl: string | null = null;
      let lightSourceUrl: string | null = null;
      let imgNode: any = null;

      for (const child of node.children) {
        if (child.type === "element") {
          const cTag = child.tagName?.toLowerCase();
          if (cTag === "source") {
            const cProps = child.properties || {};
            const media = (cProps.media || "").toLowerCase();
            const srcset = cProps.srcset || cProps.srcSet || "";
            if (media.includes("dark") || media.includes("prefers-color-scheme: dark")) {
              darkSourceNode = child;
              darkSourceUrl = srcset;
            } else if (media.includes("light") || media.includes("prefers-color-scheme: light")) {
              lightSourceNode = child;
              lightSourceUrl = srcset;
            }
          } else if (cTag === "img") {
            imgNode = child;
          }
        }
      }

      if (imgNode) {
        imgNode.properties = imgNode.properties || {};

        // Resolve dark source
        let resolvedDarkUrl: string | null = null;
        if (darkSourceUrl) {
          const { resolvedUrl, warning } = resolveAsset(darkSourceUrl, ctx.assets, "dark");
          resolvedDarkUrl = resolvedUrl;
          if (warning && ctx.theme === "dark") ctx.warnings.push(warning);
        }

        // Resolve light source
        let resolvedLightUrl: string | null = null;
        if (lightSourceUrl) {
          const { resolvedUrl, warning } = resolveAsset(lightSourceUrl, ctx.assets, "light");
          resolvedLightUrl = resolvedUrl;
          if (warning && ctx.theme === "light") ctx.warnings.push(warning);
        }

        // Determine active theme's URL
        let activeUrl = ctx.theme === "dark" ? resolvedDarkUrl : resolvedLightUrl;
        if (!activeUrl && typeof imgNode.properties.src === "string") {
          const { resolvedUrl, warning } = resolveAsset(imgNode.properties.src, ctx.assets, ctx.theme);
          activeUrl = resolvedUrl;
          if (warning) ctx.warnings.push(warning);
        }

        if (activeUrl) {
          imgNode.properties.src = activeUrl;
          imgNode._resolvedByPicture = true;
        }

        // Configure <source> media queries and resolved srcset
        if (darkSourceNode) {
          darkSourceNode.properties = darkSourceNode.properties || {};
          darkSourceNode.properties.media = ctx.theme === "dark" ? "all" : "not all";
          if (resolvedDarkUrl) {
            darkSourceNode.properties.srcset = resolvedDarkUrl;
            delete darkSourceNode.properties.srcSet;
          }
          darkSourceNode._resolvedByPicture = true;
        }

        if (lightSourceNode) {
          lightSourceNode.properties = lightSourceNode.properties || {};
          lightSourceNode.properties.media = ctx.theme === "light" ? "all" : "not all";
          if (resolvedLightUrl) {
            lightSourceNode.properties.srcset = resolvedLightUrl;
            delete lightSourceNode.properties.srcSet;
          }
          lightSourceNode._resolvedByPicture = true;
        }
      }
    }

    if (tag === "img") {
      ctx.imageCount++;
      if (!node._resolvedByPicture && typeof props.src === "string") {
        const { resolvedUrl, warning } = resolveAsset(props.src, ctx.assets, ctx.theme);
        props.src = resolvedUrl;
        if (warning) {
          ctx.warnings.push(warning);
        }
      }
    } else if (tag === "source") {
      if (!node._resolvedByPicture) {
        const currentSrcset = props.srcset || props.srcSet;
        if (typeof currentSrcset === "string") {
          const { resolvedUrl, warning } = resolveAsset(currentSrcset, ctx.assets, ctx.theme);
          props.srcset = resolvedUrl;
          delete props.srcSet;
          if (warning) {
            ctx.warnings.push(warning);
          }
        }
      }
    } else if (tag === "table") {
      ctx.tableCount++;
    } else if (tag === "a") {
      if (typeof props.href === "string" && isExternalOrSpecialUrl(props.href)) {
        if (!props.target) {
          props.target = "_blank";
        }
        if (!props.rel) {
          props.rel = "noreferrer noopener";
        }
      }
    }
  }

  if (Array.isArray(node.children)) {
    for (const child of node.children) {
      walkHast(child, ctx);
    }
  }
}

function rehypeAstProcessor(ctx: VisitorContext) {
  return (tree: any) => {
    walkHast(tree, ctx);
  };
}

export async function renderGithubReadme(
  markdown: string,
  options: RenderOptions = {}
): Promise<RenderResult> {
  const startTime = typeof performance !== "undefined" ? performance.now() : Date.now();

  const theme = options.theme || "dark";
  const assets = options.assets || {};
  const variables = options.variables || {};

  // Step 1: Substitute variables
  const substituted = substituteVariables(markdown || "", variables);

  // Step 2: Context collection for debug metrics & asset resolving
  const visitorContext: VisitorContext = {
    assets,
    theme,
    warnings: [],
    elementCount: 0,
    imageCount: 0,
    tableCount: 0,
  };

  // Step 3: Parse markdown with unified pipeline
  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeSlug)
    .use(rehypeHighlight)
    .use(rehypeAstProcessor, visitorContext)
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(substituted);

  const rawHtml = String(file);

  // Step 4: Sanitize HTML
  const sanitizedHtml = sanitizeHtml(rawHtml);

  // Step 5: Calculate debug report
  const endTime = typeof performance !== "undefined" ? performance.now() : Date.now();
  const renderTimeMs = Math.round(endTime - startTime);

  const debugReport: DebugReport = {
    renderTimeMs,
    elementCount: visitorContext.elementCount,
    imageCount: visitorContext.imageCount,
    tableCount: visitorContext.tableCount,
    warnings: visitorContext.warnings,
  };

  return {
    html: sanitizedHtml,
    debugReport,
  };
}
