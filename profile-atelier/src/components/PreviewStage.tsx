import React, { useMemo, useState } from "react";
import { Content, RenderResult } from "../types";
import { ThemeMode, MotionMode, DeviceMode } from "../state/store";
import { GithubFrame } from "./GithubFrame";
import { PhoneFrame } from "./PhoneFrame";

interface PreviewStageProps {
  content: Content;
  theme: ThemeMode;
  motion: MotionMode;
  device: DeviceMode;
  result: RenderResult | null;
  onLinkedInWarning?: () => void;
}

export const PreviewStage: React.FC<PreviewStageProps> = ({
  content,
  theme,
  motion,
  device,
  result,
}) => {
  const [viewTab, setViewTab] = useState<"visual" | "markdown">("visual");
  const [copied, setCopied] = useState(false);

  // Create Blob URLs with motion handling
  const blobUrls = useMemo(() => {
    if (!result) return {};
    const map: Record<string, string> = {};

    for (const [name, svgText] of Object.entries(result.files)) {
      let finalSvg = svgText;
      if (motion === "reduced") {
        finalSvg = finalSvg.replace(
          "</style>",
          `* { animation: none !important; transition: none !important; }\n</style>`
        );
      }
      const blob = new Blob([finalSvg], { type: "image/svg+xml;charset=utf-8" });
      map[name] = URL.createObjectURL(blob);
    }
    return map;
  }, [result, motion]);

  const handleCopyMarkdown = () => {
    if (!result?.readme) return;
    navigator.clipboard.writeText(result.readme);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!result) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "400px",
          color: "var(--text-secondary)",
          fontSize: "14px",
        }}
      >
        <span>Rendering high-quality preview...</span>
      </div>
    );
  }

  const getUrl = (prefix: string) => blobUrls[`${prefix}-${theme}.svg`];

  const contentElements = (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "10px",
        width: "100%",
      }}
    >
      {/* Hero */}
      {getUrl("hero") && (
        <div style={{ width: "100%" }}>
          <img
            src={getUrl("hero")}
            alt={`${content.name} hero`}
            style={{
              width: "100%",
              height: "auto",
              display: "block",
              shapeRendering: "geometricPrecision",
              textRendering: "geometricPrecision",
            }}
          />
        </div>
      )}

      {/* Buttons */}
      <div
        style={{
          display: "flex",
          gap: "8px",
          flexWrap: "wrap",
          justifyContent: "center",
          margin: "4px 0",
        }}
      >
        {getUrl("btn-github") && (
          <a href={content.github} target="_blank" rel="noreferrer" style={{ display: "inline-block" }}>
            <img
              src={getUrl("btn-github")}
              alt="GitHub"
              style={{ height: "38px", width: "auto", display: "block" }}
            />
          </a>
        )}
        {getUrl("btn-linkedin") && (
          <a
            href={content.linkedin}
            target="_blank"
            rel="noreferrer"
            style={{ display: "inline-block" }}
            onClick={(e) => {
              if (content.linkedin.includes("YOUR-LINKEDIN")) {
                e.preventDefault();
                alert("Please update your LinkedIn URL in the Content editor!");
              }
            }}
          >
            <img
              src={getUrl("btn-linkedin")}
              alt="LinkedIn"
              style={{ height: "38px", width: "auto", display: "block" }}
            />
          </a>
        )}
        {getUrl("btn-portfolio") && (
          <a href={content.portfolio} target="_blank" rel="noreferrer" style={{ display: "inline-block" }}>
            <img
              src={getUrl("btn-portfolio")}
              alt="Portfolio"
              style={{ height: "38px", width: "auto", display: "block" }}
            />
          </a>
        )}
      </div>

      {/* About */}
      {getUrl("about") && (
        <div style={{ width: "100%" }}>
          <img
            src={getUrl("about")}
            alt="About"
            style={{
              width: "100%",
              height: "auto",
              display: "block",
              shapeRendering: "geometricPrecision",
              textRendering: "geometricPrecision",
            }}
          />
        </div>
      )}

      {/* Skills */}
      {getUrl("skills") && (
        <div style={{ width: "100%" }}>
          <img
            src={getUrl("skills")}
            alt="Skills"
            style={{
              width: "100%",
              height: "auto",
              display: "block",
              shapeRendering: "geometricPrecision",
              textRendering: "geometricPrecision",
            }}
          />
        </div>
      )}

      {/* Projects Title */}
      {getUrl("projects-title") && (
        <div style={{ width: "100%" }}>
          <img
            src={getUrl("projects-title")}
            alt="Selected Projects"
            style={{
              width: "100%",
              height: "auto",
              display: "block",
              shapeRendering: "geometricPrecision",
              textRendering: "geometricPrecision",
            }}
          />
        </div>
      )}

      {/* Projects Cards Grid — matching GitHub centered inline layout */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: device === "phone" ? "8px" : "1.3%",
          width: "100%",
          margin: "4px 0",
        }}
      >
        {content.projects.map((proj) => {
          const cardUrl = getUrl(`card-${proj.slug}`);
          if (!cardUrl) return null;
          return (
            <a
              key={proj.slug}
              href={`${content.github}/${proj.slug}`}
              target="_blank"
              rel="noreferrer"
              style={{
                width: device === "phone" ? "48%" : "23.8%",
                display: "block",
                marginBottom: "6px",
                textDecoration: "none",
              }}
            >
              <img
                src={cardUrl}
                alt={proj.title}
                style={{
                  width: "100%",
                  height: "auto",
                  display: "block",
                  borderRadius: "4px",
                  shapeRendering: "geometricPrecision",
                  textRendering: "geometricPrecision",
                }}
              />
            </a>
          );
        })}
      </div>

      {/* Footer */}
      {getUrl("footer") && (
        <div style={{ width: "100%" }}>
          <img
            src={getUrl("footer")}
            alt="Footer"
            style={{
              width: "100%",
              height: "auto",
              display: "block",
              shapeRendering: "geometricPrecision",
              textRendering: "geometricPrecision",
            }}
          />
        </div>
      )}

      {/* Subtitle footer links */}
      <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "6px", textAlign: "center" }}>
        <sub>
          <a href={content.portfolio} target="_blank" rel="noreferrer" style={{ color: "inherit", textDecoration: "none" }}>
            {content.portfolio.replace(/^https?:\/\//, "")}
          </a>{" "}
          &nbsp;·&nbsp;{" "}
          <a href={content.linkedin} target="_blank" rel="noreferrer" style={{ color: "inherit", textDecoration: "none" }}>
            LinkedIn
          </a>
        </sub>
      </div>
    </div>
  );

  return (
    <div style={{ width: "100%", display: "flex", flexDirection: "column", alignItems: "center" }}>
      {/* Mode switch bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          width: "100%",
          maxWidth: "880px",
          marginBottom: "12px",
        }}
      >
        <div className="segmented">
          <button
            className={`segmented__btn ${viewTab === "visual" ? "segmented__btn--active" : ""}`}
            onClick={() => setViewTab("visual")}
          >
            Live GitHub View
          </button>
          <button
            className={`segmented__btn ${viewTab === "markdown" ? "segmented__btn--active" : ""}`}
            onClick={() => setViewTab("markdown")}
          >
            README.md Code
          </button>
        </div>

        {viewTab === "markdown" && (
          <button className="btn btn--secondary btn--sm" onClick={handleCopyMarkdown}>
            {copied ? "Copied!" : "Copy Markdown"}
          </button>
        )}
      </div>

      {viewTab === "markdown" ? (
        <div
          style={{
            width: "100%",
            maxWidth: "880px",
            backgroundColor: theme === "dark" ? "#0D1117" : "#F6F8FA",
            color: theme === "dark" ? "#E6EDF3" : "#24292F",
            border: `1px solid ${theme === "dark" ? "#30363D" : "#D0D7DE"}`,
            borderRadius: "6px",
            padding: "16px",
            overflowX: "auto",
            fontFamily: "var(--font-mono)",
            fontSize: "12px",
            lineHeight: 1.5,
            whiteSpace: "pre-wrap",
          }}
        >
          {result.readme}
        </div>
      ) : device === "phone" ? (
        <PhoneFrame theme={theme}>{contentElements}</PhoneFrame>
      ) : (
        <GithubFrame handle={content.handle} theme={theme}>
          {contentElements}
        </GithubFrame>
      )}
    </div>
  );
};

