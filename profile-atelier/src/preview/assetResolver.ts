import { AssetWarning, Theme } from "./types";

/**
 * Normalizes an asset path into canonical keys for lookup.
 */
export function normalizeAssetPath(rawPath: string): {
  cleanPath: string;
  basename: string;
  hash: string;
} {
  if (!rawPath) return { cleanPath: "", basename: "", hash: "" };

  const [withoutHash, hash = ""] = rawPath.split("#");
  const [clean] = withoutHash.split("?");

  const normalized = clean.replace(/\\/g, "/").replace(/^\.?\//, "");
  const parts = normalized.split("/");
  const basename = parts[parts.length - 1] || "";

  return { cleanPath: normalized, basename, hash };
}

/**
 * Checks if a URL is an external link, data URI, or anchor.
 */
export function isExternalOrSpecialUrl(url: string): boolean {
  if (!url) return false;
  return (
    url.startsWith("http://") ||
    url.startsWith("https://") ||
    url.startsWith("data:") ||
    url.startsWith("blob:") ||
    url.startsWith("mailto:") ||
    url.startsWith("#")
  );
}

/**
 * Resolves an asset URL against the provided asset map.
 * Also tracks warnings if an internal asset cannot be found.
 */
export function resolveAsset(
  rawUrl: string,
  assets: Record<string, string> = {},
  theme?: Theme
): { resolvedUrl: string; warning?: AssetWarning } {
  if (!rawUrl) {
    return { resolvedUrl: "" };
  }

  // Handle external or data/blob URLs
  if (isExternalOrSpecialUrl(rawUrl)) {
    return { resolvedUrl: rawUrl };
  }

  const { cleanPath, basename } = normalizeAssetPath(rawUrl);

  // 1. Direct match (exact raw URL)
  if (assets[rawUrl]) {
    return { resolvedUrl: assets[rawUrl] };
  }

  // 2. Clean path match (e.g. "assets/hero-dark.svg")
  if (assets[cleanPath]) {
    return { resolvedUrl: assets[cleanPath] };
  }

  // 3. Basename match (e.g. "hero-dark.svg")
  if (assets[basename]) {
    return { resolvedUrl: assets[basename] };
  }

  // 4. Without "assets/" prefix match
  const strippedAssetsPrefix = cleanPath.replace(/^assets\//, "");
  if (assets[strippedAssetsPrefix]) {
    return { resolvedUrl: assets[strippedAssetsPrefix] };
  }

  // 5. With "assets/" prefix match
  const withAssetsPrefix = `assets/${basename}`;
  if (assets[withAssetsPrefix]) {
    return { resolvedUrl: assets[withAssetsPrefix] };
  }

  // 6. Theme variant match if theme is provided
  if (theme) {
    // e.g. hero-light.svg -> hero-dark.svg
    const themeVariantBasename =
      theme === "dark"
        ? basename.replace("-light.", "-dark.")
        : basename.replace("-dark.", "-light.");
    if (assets[themeVariantBasename]) {
      return { resolvedUrl: assets[themeVariantBasename] };
    }
    if (assets[`assets/${themeVariantBasename}`]) {
      return { resolvedUrl: assets[`assets/${themeVariantBasename}`] };
    }

    // e.g. hero.svg -> hero-dark.svg
    const dotIdx = basename.lastIndexOf(".");
    if (dotIdx > 0) {
      const namePart = basename.substring(0, dotIdx);
      const extPart = basename.substring(dotIdx);
      if (!namePart.endsWith("-dark") && !namePart.endsWith("-light")) {
        const themeCandidate = `${namePart}-${theme}${extPart}`;
        if (assets[themeCandidate]) {
          return { resolvedUrl: assets[themeCandidate] };
        }
        if (assets[`assets/${themeCandidate}`]) {
          return { resolvedUrl: assets[`assets/${themeCandidate}`] };
        }
      }
    }
  }

  // 7. Strip theme suffix match (e.g. hero-dark.svg -> hero.svg)
  const withoutThemeSuffix = basename.replace(/-(dark|light)\./, ".");
  if (assets[withoutThemeSuffix]) {
    return { resolvedUrl: assets[withoutThemeSuffix] };
  }
  if (assets[`assets/${withoutThemeSuffix}`]) {
    return { resolvedUrl: assets[`assets/${withoutThemeSuffix}`] };
  }

  // Not found in asset map: emit warning
  return {
    resolvedUrl: rawUrl,
    warning: {
      path: rawUrl,
      normalized: cleanPath,
    },
  };
}
