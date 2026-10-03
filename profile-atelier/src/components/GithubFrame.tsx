import React from "react";
import { ThemeMode } from "../state/store";

interface GithubFrameProps {
  handle: string;
  theme: ThemeMode;
  children: React.ReactNode;
}

export const GithubFrame: React.FC<GithubFrameProps> = ({ handle, theme, children }) => {
  const isDark = theme === "dark";
  const bg = isDark ? "#0D1117" : "#FFFFFF";
  const fg = isDark ? "#E6EDF3" : "#1F2328";
  const border = isDark ? "#30363D" : "#D0D7DE";
  const boxBg = isDark ? "#161B22" : "#F6F8FA";

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "880px",
        margin: "0 auto",
        backgroundColor: bg,
        color: fg,
        border: `1px solid ${border}`,
        borderRadius: "8px",
        overflow: "hidden",
        boxShadow: "0 4px 14px rgba(0,0,0,0.06)",
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
      }}
    >
      {/* GitHub Repo Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "10px 16px",
          backgroundColor: boxBg,
          borderBottom: `1px solid ${border}`,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "13px" }}>
          <span style={{ fontWeight: 600 }}>{handle}</span>
          <span style={{ opacity: 0.5 }}>/</span>
          <span>README.md</span>
        </div>
        <span
          style={{
            fontSize: "11px",
            padding: "2px 8px",
            borderRadius: "999px",
            border: `1px solid ${border}`,
            color: fg,
            opacity: 0.8,
          }}
        >
          Public
        </span>
      </div>

      {/* GitHub README Markdown Body */}
      <div style={{ padding: "32px", overflowX: "auto" }}>
        {children}
      </div>
    </div>
  );
};
