import React, { useState } from "react";
import { Content, RenderResult } from "../types";
import { ThemeMode, MotionMode, DeviceMode } from "../state/store";
import { GithubFrame } from "./GithubFrame";
import { PhoneFrame } from "./PhoneFrame";
import { GithubReadmePreview } from "../preview/GithubReadmePreview";

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
  const [debugMode, setDebugMode] = useState<boolean>(false);
  const [copied, setCopied] = useState(false);

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

  const readmePreviewElement = (
    <GithubReadmePreview
      readme={result.readme}
      files={result.files}
      theme={theme}
      variables={content as unknown as Record<string, any>}
      motion={motion}
      debugMode={debugMode}
    />
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
          gap: "8px",
          flexWrap: "wrap",
        }}
      >
        <div style={{ display: "flex", gap: "8px", alignItems: "center" }}>
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

          {viewTab === "visual" && (
            <div className="segmented">
              <button
                className={`segmented__btn ${!debugMode ? "segmented__btn--active" : ""}`}
                onClick={() => setDebugMode(false)}
                title="Standard GitHub rendering mode"
              >
                GitHub Mode
              </button>
              <button
                className={`segmented__btn ${debugMode ? "segmented__btn--active" : ""}`}
                onClick={() => setDebugMode(true)}
                title="Developer debug rendering mode"
              >
                Debug Rendering
              </button>
            </div>
          )}
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
        <PhoneFrame theme={theme}>{readmePreviewElement}</PhoneFrame>
      ) : (
        <GithubFrame handle={content.handle} theme={theme}>
          {readmePreviewElement}
        </GithubFrame>
      )}
    </div>
  );
};
