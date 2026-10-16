import React, { useEffect, useMemo, useState, useRef } from "react";
import { renderGithubReadme } from "./engine";
import { DebugReport } from "./types";
import { MotionMode } from "../state/store";
import "./githubReadme.css";

interface GithubReadmePreviewProps {
  readme: string;
  files?: Record<string, string>;
  theme: "dark" | "light";
  variables?: Record<string, any>;
  debugMode?: boolean;
  motion?: MotionMode;
}

export const GithubReadmePreview: React.FC<GithubReadmePreviewProps> = ({
  readme,
  files = {},
  theme,
  variables = {},
  debugMode = false,
  motion = "play",
}) => {
  const [renderedHtml, setRenderedHtml] = useState<string>("");
  const [debugReport, setDebugReport] = useState<DebugReport | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Convert files (SVG strings or URLs) into reliable data URIs
  const assetUrls = useMemo(() => {
    const urls: Record<string, string> = {};

    for (const [name, content] of Object.entries(files)) {
      if (typeof content === "string") {
        if (content.startsWith("<svg") || content.includes("<svg")) {
          let svg = content;
          if (motion === "reduced") {
            svg = svg.replace(
              "</style>",
              `* { animation: none !important; transition: none !important; }\n</style>`
            );
          }
          urls[name] = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
        } else {
          // Already a URL or base64
          urls[name] = content;
        }
      }
    }

    return urls;
  }, [files, motion]);

  // Render markdown with engine
  useEffect(() => {
    let cancelled = false;

    renderGithubReadme(readme, {
      theme,
      variables,
      assets: assetUrls,
      debugMode,
      reducedMotion: motion === "reduced",
    })
      .then((result) => {
        if (!cancelled) {
          setRenderedHtml(result.html);
          setDebugReport(result.debugReport);
        }
      })
      .catch((err) => {
        console.error("Preview render failed:", err);
      });

    return () => {
      cancelled = true;
    };
  }, [readme, assetUrls, theme, variables, debugMode, motion]);

  return (
    <div style={{ width: "100%", display: "flex", flexDirection: "column" }}>
      {/* Developer Debug Overlay */}
      {debugMode && debugReport && (
        <div style={{ marginBottom: "16px" }}>
          <div className="readme-debug-stats">
            <span>⏱️ Render: {debugReport.renderTimeMs}ms</span>
            <span>🧩 Elements: {debugReport.elementCount}</span>
            <span>🖼️ Images: {debugReport.imageCount}</span>
            <span>📊 Tables: {debugReport.tableCount}</span>
            <span style={{ color: debugReport.warnings.length > 0 ? "#eb5757" : "#4dab5c" }}>
              ⚠️ Missing Assets: {debugReport.warnings.length}
            </span>
          </div>

          {debugReport.warnings.length > 0 && (
            <div className="readme-debug-warning-banner">
              <h4>⚠️ Asset Loading Warnings</h4>
              <ul style={{ margin: 0, paddingLeft: "20px" }}>
                {debugReport.warnings.map((w, i) => (
                  <li key={i}>
                    <strong>Asset not found:</strong> <code>{w.path}</code> (looked for normalized:{" "}
                    <code>{w.normalized}</code>)
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* GitHub Markdown Body Container */}
      <div
        ref={containerRef}
        data-theme={theme}
        className={`github-readme-preview markdown-body theme-${theme} ${
          debugMode ? "github-readme-preview--debug" : ""
        }`}
        dangerouslySetInnerHTML={{ __html: renderedHtml }}
      />
    </div>
  );
};
