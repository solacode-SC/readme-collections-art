import React, { useState, useEffect } from "react";
import { Content, RenderResult } from "../types";
import { STYLES, getStyleById } from "../styles/registry";
import { DEFAULT_CONTENT } from "../lib/defaultContent";
import { ImageLoader } from "../lib/image";
import { ThemeMode, MotionMode, DeviceMode, saveContent } from "../state/store";
import { StyleGallery } from "../components/StyleGallery";
import { PreviewStage } from "../components/PreviewStage";
import { ContentEditor } from "../components/ContentEditor";
import { WeightGauge } from "../components/WeightGauge";
import { CatMascot } from "../components/CatMascot";
import { createStyleZip, createAllStylesZip, downloadBlob } from "../lib/zip";
import { buildAgentPrompt } from "../lib/promptBuilder";

type MobileTab = "templates" | "preview" | "editor";

export const App: React.FC = () => {
  const [content, setContent] = useState<Content>(() => {
    try {
      const raw = localStorage.getItem("profile_atelier_content_v1");
      if (raw) return JSON.parse(raw);
    } catch (e) {
      console.error(e);
    }
    return DEFAULT_CONTENT;
  });

  const [selectedStyleId, setSelectedStyleId] = useState<string>("swirl");
  const [theme, setTheme] = useState<ThemeMode>("dark");
  const [motion, setMotion] = useState<MotionMode>("play");
  const [device, setDevice] = useState<DeviceMode>("desktop");
  const [mobileTab, setMobileTab] = useState<MobileTab>("preview");
  const [showLeftSidebar, setShowLeftSidebar] = useState<boolean>(true);
  const [showRightSidebar, setShowRightSidebar] = useState<boolean>(true);

  const [renderResult, setRenderResult] = useState<RenderResult | null>(null);
  const [isExporting, setIsExporting] = useState<boolean>(false);
  const [exportProgress, setExportProgress] = useState<string | null>(null);

  const activeStyle = getStyleById(selectedStyleId);

  // Debounced render
  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(async () => {
      try {
        const res = await activeStyle.render(content, ImageLoader);
        if (!cancelled) {
          setRenderResult(res);
        }
      } catch (err) {
        console.error("Rendering error:", err);
      }
    }, 180);

    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [content, selectedStyleId]);

  // Persist content
  const handleContentChange = (updated: Content) => {
    setContent(updated);
    saveContent(updated);
  };

  const handleReset = () => {
    if (confirm("Reset all content to defaults?")) {
      setContent(DEFAULT_CONTENT);
      saveContent(DEFAULT_CONTENT);
    }
  };

  const handleDownloadSingle = async () => {
    if (!renderResult) return;
    setIsExporting(true);
    try {
      const blob = await createStyleZip(activeStyle, content, renderResult);
      downloadBlob(blob, `${content.handle}-${activeStyle.id}.zip`);
    } catch (err) {
      alert("Export failed: " + err);
    } finally {
      setIsExporting(false);
    }
  };

  const handleDownloadAll = async () => {
    setIsExporting(true);
    try {
      const blob = await createAllStylesZip(STYLES, content, (pct, name) => {
        setExportProgress(`${pct}% — ${name}`);
      });
      downloadBlob(blob, `${content.handle}-all-styles.zip`);
    } catch (err) {
      alert("Batch export failed: " + err);
    } finally {
      setIsExporting(false);
      setExportProgress(null);
    }
  };

  const handleCopyPrompt = () => {
    const text = buildAgentPrompt(content);
    navigator.clipboard.writeText(text);
    alert("AI prompt copied to clipboard!");
  };

  const handleSelectStyle = (id: string) => {
    setSelectedStyleId(id);
    // On mobile, switch to preview when a style is selected
    if (window.innerWidth <= 768) {
      setMobileTab("preview");
    }
  };

  return (
    <>
      {/* ---- Header ---- */}
      <header className="app-header">
        <div className="app-header__brand">
          <div className="app-header__brand-icon">A</div>
          <span>Profile Atelier</span>
          <span className="caption desktop-only" style={{ marginLeft: 4 }}>
            — README Studio
          </span>
        </div>

        <div className="app-header__toggles desktop-only">
          <button
            className={`btn btn--ghost btn--sm ${!showLeftSidebar ? "btn--panel-inactive" : ""}`}
            onClick={() => setShowLeftSidebar((v) => !v)}
            title={showLeftSidebar ? "Hide Styles Sidebar (Left)" : "Show Styles Sidebar (Left)"}
          >
            <span>{showLeftSidebar ? "◧ Hide Styles" : "◨ Show Styles"}</span>
          </button>
          <button
            className={`btn btn--ghost btn--sm ${!showRightSidebar ? "btn--panel-inactive" : ""}`}
            onClick={() => setShowRightSidebar((v) => !v)}
            title={showRightSidebar ? "Hide Content Editor (Right)" : "Show Content Editor (Right)"}
          >
            <span>{showRightSidebar ? "◨ Hide Editor" : "◧ Show Editor"}</span>
          </button>
        </div>

        <div className="app-header__actions">
          <button
            className="btn btn--primary btn--sm"
            onClick={handleDownloadSingle}
            disabled={isExporting || !renderResult}
          >
            <span>↓</span>
            <span className="desktop-only">Download ZIP</span>
          </button>
          <button
            className="btn btn--secondary btn--sm"
            onClick={handleDownloadAll}
            disabled={isExporting}
          >
            <span className="desktop-only">All Styles</span>
            <span className="mobile-only">All</span>
          </button>
          <button
            className="btn btn--ghost btn--sm"
            onClick={handleCopyPrompt}
            title="Copy AI prompt"
          >
            ✦
          </button>
        </div>
      </header>

      {/* ---- Mobile Tabs ---- */}
      <nav className="mobile-tabs">
        <div className="mobile-tabs__list">
          {(["templates", "preview", "editor"] as MobileTab[]).map((tab) => (
            <button
              key={tab}
              className={`mobile-tabs__tab ${mobileTab === tab ? "mobile-tabs__tab--active" : ""}`}
              onClick={() => setMobileTab(tab)}
            >
              {tab === "templates" ? `Styles (${STYLES.length})` : tab === "preview" ? "Preview" : "Content"}
            </button>
          ))}
        </div>
      </nav>

      {/* ---- Body ---- */}
      <div className="app-body">
        {/* Sidebar — Style Gallery */}
        <aside className={`sidebar ${mobileTab === "templates" ? "sidebar--mobile-visible" : ""} ${!showLeftSidebar ? "sidebar--collapsed" : ""}`}>
          <StyleGallery
            styles={STYLES}
            selectedId={selectedStyleId}
            onSelect={handleSelectStyle}
            onClose={() => setShowLeftSidebar(false)}
          />
        </aside>

        {/* Preview Panel */}
        <main className={`preview-panel ${mobileTab === "preview" ? "preview-panel--mobile-visible" : ""}`}>
          {/* Toolbar */}
          <div className="preview-panel__toolbar">
            <div className="preview-panel__toolbar-group">
              {!showLeftSidebar && (
                <button
                  className="btn btn--secondary btn--sm desktop-only"
                  onClick={() => setShowLeftSidebar(true)}
                  title="Show Styles Sidebar"
                  style={{ marginRight: 6 }}
                >
                  ◀ Styles
                </button>
              )}

              <div className="segmented">
                <button
                  className={`segmented__btn ${device === "desktop" ? "segmented__btn--active" : ""}`}
                  onClick={() => setDevice("desktop")}
                >
                  Desktop
                </button>
                <button
                  className={`segmented__btn ${device === "phone" ? "segmented__btn--active" : ""}`}
                  onClick={() => setDevice("phone")}
                >
                  Phone
                </button>
              </div>

              <div style={{ width: 1, height: 20, background: "var(--border)", margin: "0 4px" }} />

              <div className="segmented">
                <button
                  className={`segmented__btn ${theme === "dark" ? "segmented__btn--active" : ""}`}
                  onClick={() => setTheme("dark")}
                >
                  Dark
                </button>
                <button
                  className={`segmented__btn ${theme === "light" ? "segmented__btn--active" : ""}`}
                  onClick={() => setTheme("light")}
                >
                  Light
                </button>
              </div>
            </div>

            <div className="preview-panel__toolbar-group">
              <div className="segmented">
                <button
                  className={`segmented__btn ${motion === "play" ? "segmented__btn--active" : ""}`}
                  onClick={() => setMotion("play")}
                  title="Play animations"
                >
                  ▶
                </button>
                <button
                  className="segmented__btn"
                  onClick={() => { setMotion("reduced"); setTimeout(() => setMotion("play"), 50); }}
                  title="Replay once"
                >
                  ↻
                </button>
                <button
                  className={`segmented__btn ${motion === "reduced" ? "segmented__btn--active" : ""}`}
                  onClick={() => setMotion("reduced")}
                  title="Reduced motion"
                >
                  ⏸
                </button>
              </div>

              <span className="caption desktop-only" style={{ marginLeft: 8 }}>
                {activeStyle.name}
              </span>

              {!showRightSidebar && (
                <button
                  className="btn btn--secondary btn--sm desktop-only"
                  onClick={() => setShowRightSidebar(true)}
                  title="Show Content Editor"
                  style={{ marginLeft: 8 }}
                >
                  Content ▶
                </button>
              )}
            </div>
          </div>

          {/* Preview Content */}
          <div className="preview-panel__content">
            <PreviewStage
              content={content}
              theme={theme}
              motion={motion}
              device={device}
              result={renderResult}
            />
          </div>
        </main>

        {/* Editor Panel */}
        <aside className={`editor-panel ${mobileTab === "editor" ? "editor-panel--mobile-visible" : ""} ${!showRightSidebar ? "editor-panel--collapsed" : ""}`}>
          <div className="editor-panel__header">
            <span className="section-label">Content</span>
            <div style={{ display: "flex", gap: "4px", alignItems: "center" }}>
              <button
                className="btn btn--ghost btn--sm"
                onClick={handleReset}
              >
                Reset
              </button>
              <button
                className="btn btn--ghost btn--sm desktop-only"
                onClick={() => setShowRightSidebar(false)}
                title="Hide content editor"
              >
                ✕
              </button>
            </div>
          </div>
          <div className="editor-panel__body">
            <ContentEditor
              content={content}
              onChange={handleContentChange}
              onReset={handleReset}
            />
          </div>
        </aside>
      </div>

      {/* ---- Footer ---- */}
      <footer className="app-footer">
        <div className="app-footer__group">
          <CatMascot bytes={renderResult?.meta.bytes || 0} />
          <WeightGauge bytes={renderResult?.meta.bytes || 0} />
        </div>

        <div className="app-footer__group">
          {exportProgress && (
            <span className="caption">{exportProgress}</span>
          )}

          <div className="palette desktop-only">
            {(theme === "dark" ? activeStyle.palette.dark : activeStyle.palette.light).map((hex, i) => (
              <div key={i} className="palette__dot" style={{ backgroundColor: hex }} title={hex} />
            ))}
          </div>

          <span className="caption desktop-only">
            {STYLES.length} styles · {activeStyle.keywords.join(", ")}
          </span>
        </div>
      </footer>
    </>
  );
};

