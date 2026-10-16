import React from "react";
import { ThemeMode } from "../state/store";
import { BookOpen, Pencil } from "lucide-react";

interface GithubFrameProps {
  handle: string;
  theme: ThemeMode;
  children: React.ReactNode;
}

export const GithubFrame: React.FC<GithubFrameProps> = ({ handle, theme, children }) => {
  const isDark = theme === "dark";
  const bg = isDark ? "#0d1117" : "#ffffff";
  const fg = isDark ? "#f0f6fc" : "#1f2328";
  const border = isDark ? "#30363d" : "#d0d7de";
  const boxBg = isDark ? "#161b22" : "#f6f8fa";
  const muted = isDark ? "#848d97" : "#656d76";

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "880px",
        margin: "0 auto",
        backgroundColor: bg,
        color: fg,
        border: `1px solid ${border}`,
        borderRadius: "6px",
        overflow: "hidden",
        boxShadow: isDark
          ? "0 4px 20px rgba(0,0,0,0.45)"
          : "0 4px 20px rgba(0,0,0,0.06)",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif',
      }}
    >
      {/* GitHub Profile README Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "10px 16px",
          backgroundColor: boxBg,
          borderBottom: `1px solid ${border}`,
          userSelect: "none",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px" }}>
          <BookOpen size={15} color={muted} />
          <span style={{ fontWeight: 600, color: fg }}>{handle}</span>
          <span style={{ color: muted }}>/</span>
          <span style={{ color: fg }}>README.md</span>
        </div>
        <div
          title="Edit README"
          style={{
            display: "flex",
            alignItems: "center",
            cursor: "pointer",
            padding: "4px",
            borderRadius: "4px",
            color: muted,
          }}
        >
          <Pencil size={13} />
        </div>
      </div>

      {/* GitHub README Markdown Body */}
      <div style={{ padding: "28px 32px", overflowX: "auto" }}>
        {children}
      </div>
    </div>
  );
};
