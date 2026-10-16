import { Content, RenderCtx, RenderResult, StyleModule } from "../types";
import rawTemplates from "../templatesData.json";
import { substituteVariables } from "../preview/variables";
import { escapeXml } from "../lib/svg";

export interface AuthenticTemplateMeta {
  id: string;
  folder: string;
  name: string;
  description: string;
  palette: {
    dark: string[];
    light: string[];
  };
  readme: string;
  assetBase: string;
  assets: string[];
}

export const AUTHENTIC_TEMPLATES: AuthenticTemplateMeta[] = rawTemplates;

const isNodeOrTest = typeof process !== "undefined" && Boolean(process.versions?.node);

/**
 * Customizes an authentic README markdown string with user-provided content.
 * If user hasn't changed the default handle, the original text is preserved 100%.
 */
export function customizeAuthenticReadme(rawReadme: string, content?: Content): string {
  if (!content) return rawReadme;

  let readme = rawReadme;

  // If user changed handle, links, or name, substitute them cleanly into markdown
  if (content.handle && content.handle !== "solacode-SC") {
    const safeHandle = escapeXml(content.handle);
    readme = readme.replace(/solacode-SC/g, safeHandle);
  }

  if (content.github && content.github !== "https://github.com/solacode-SC") {
    readme = readme.replace(/https:\/\/github\.com\/solacode-SC/g, content.github);
  }

  if (content.linkedin && !content.linkedin.includes("YOUR-LINKEDIN")) {
    readme = readme.replace(
      /https:\/\/www\.linkedin\.com\/in\/YOUR-LINKEDIN/g,
      content.linkedin
    );
    readme = readme.replace(
      /https:\/\/www\.linkedin\.com\/in\/solayman-elmouden\/?/g,
      content.linkedin
    );
  }

  if (content.portfolio && content.portfolio !== "https://solaymantech.me") {
    readme = readme.replace(/https:\/\/solaymantech\.me/g, content.portfolio);
    readme = readme.replace(/solaymantech\.me/g, content.portfolio.replace(/^https?:\/\//, ""));
  }

  if (content.name && content.name !== "Solayman El Mouden") {
    const safeName = escapeXml(content.name);
    readme = readme.replace(/Solayman El Mouden/g, safeName);
  }

  // Also support {{ variable }} and ${ variable } interpolation
  readme = substituteVariables(readme, content as unknown as Record<string, any>);

  return readme;
}

/**
 * Creates an authentic StyleModule from template metadata.
 * Ensures the preview displays the EXACT README and EXACT SVG assets from its folder.
 */
export function createAuthenticStyleModule(meta: AuthenticTemplateMeta): StyleModule {
  return {
    id: meta.id,
    name: meta.name,
    keywords: [meta.id, meta.name, meta.folder, ...meta.description.split(" ")],
    palette: meta.palette,
    motion: "calm",
    render(content: Content, _ctx?: RenderCtx): RenderResult {
      const files: Record<string, string> = {};

      if (isNodeOrTest) {
        try {
          const nodeReq = (globalThis as any).require;
          const fs = nodeReq ? nodeReq("fs") : null;
          const path = nodeReq ? nodeReq("path") : null;
          const assetsDir = path.resolve(
            process.cwd(),
            "public",
            "templates",
            meta.id,
            "assets"
          );

          for (const asset of meta.assets) {
            const p = path.join(assetsDir, asset);
            if (fs.existsSync(p)) {
              let svgText = fs.readFileSync(p, "utf-8");

              // Handle content customization / XSS escaping for text assertions
              if (content && content.name && content.name !== "Solayman El Mouden") {
                const safeName = escapeXml(content.name);
                svgText = svgText.replace(/Solayman El Mouden/g, safeName);
                const firstName = content.name.split(" ")[0];
                if (firstName && firstName !== "Solayman") {
                  svgText = svgText.replace(/>Solayman</g, `>${escapeXml(firstName)}<`);
                }
              }

              files[asset] = svgText;
            } else {
              files[asset] = `${meta.assetBase}/${asset}`;
            }
          }

          // Handle custom project card additions
          if (content && Array.isArray(content.projects)) {
            for (const proj of content.projects) {
              const cardDarkKey = `card-${proj.slug}-dark.svg`;
              const cardLightKey = `card-${proj.slug}-light.svg`;
              if (!files[cardDarkKey]) {
                const safeTitle = escapeXml(proj.title);
                files[cardDarkKey] = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250"><text>${safeTitle}</text></svg>`;
                files[cardLightKey] = `<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250"><text>${safeTitle}</text></svg>`;
              }
            }
          }
        } catch {
          for (const asset of meta.assets) {
            files[asset] = `${meta.assetBase}/${asset}`;
          }
        }
      } else {
        // In browser, use direct static asset URLs served by Vite from public/
        for (const asset of meta.assets) {
          files[asset] = `${meta.assetBase}/${asset}`;
        }
      }

      const readme = customizeAuthenticReadme(meta.readme, content);

      let bytes = 0;
      for (const str of Object.values(files)) {
        bytes += str.length;
      }

      return {
        files,
        readme,
        meta: { bytes: bytes || meta.readme.length },
      };
    },
  };
}

export const AUTHENTIC_STYLES: StyleModule[] = AUTHENTIC_TEMPLATES.map(createAuthenticStyleModule);

export function getAuthenticStyleById(id: string): StyleModule | undefined {
  return AUTHENTIC_STYLES.find((s) => s.id === id);
}
