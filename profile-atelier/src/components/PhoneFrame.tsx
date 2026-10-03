import React from "react";
import { ThemeMode } from "../state/store";

interface PhoneFrameProps {
  theme: ThemeMode;
  children: React.ReactNode;
}

export const PhoneFrame: React.FC<PhoneFrameProps> = ({ theme, children }) => {
  const isDark = theme === "dark";
  const bg = isDark ? "#0D1117" : "#FFFFFF";

  return (
    <div
      style={{
        width: "390px",
        height: "760px",
        margin: "0 auto",
        borderRadius: "44px",
        backgroundColor: "var(--ink-900)",
        padding: "10px",
        boxShadow: "0 20px 40px rgba(0,0,0,0.2)",
        position: "relative",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Inner Screen */}
      <div
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: bg,
          borderRadius: "34px",
          overflowY: "auto",
          overflowX: "hidden",
          padding: "16px 12px",
          position: "relative",
        }}
      >
        {/* Dynamic Island / Camera Notch */}
        <div
          style={{
            width: "90px",
            height: "22px",
            backgroundColor: "var(--ink-900)",
            borderRadius: "999px",
            margin: "0 auto 16px auto",
          }}
        />
        {children}
      </div>
    </div>
  );
};
