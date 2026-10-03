import React from "react";

interface CatMascotProps {
  bytes: number;
}

export const CatMascot: React.FC<CatMascotProps> = ({ bytes }) => {
  const maxBytes = 2.5 * 1024 * 1024;
  const ratio = bytes / maxBytes;

  let stateText = "ふつう"; // normal
  let bodyRadius = 14;

  if (ratio < 0.5) {
    stateText = "軽い"; // light
    bodyRadius = 11;
  } else if (ratio > 0.8) {
    stateText = "重い"; // heavy
    bodyRadius = 18;
  }

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
      <svg width="42" height="38" viewBox="0 0 42 38" fill="none">
        {/* Cat Ears */}
        <polygon points="12,14 16,6 20,13" fill="var(--ink-900)" />
        <polygon points="22,13 26,6 30,14" fill="var(--ink-900)" />
        {/* Cat Head */}
        <circle cx="21" cy="17" r="10" fill="var(--ink-900)" />
        {/* Cat Body */}
        <ellipse cx="21" cy="27" rx={bodyRadius} ry="9" fill="var(--ink-900)" />
        {/* Cat Eyes */}
        <circle cx="18" cy="16" r="1.5" fill="var(--paper-100)" />
        <circle cx="24" cy="16" r="1.5" fill="var(--paper-100)" />
        {/* Cat Tail */}
        <path
          d="M32 29 Q 38 25 36 20"
          stroke="var(--ink-900)"
          strokeWidth="2.5"
          strokeLinecap="round"
          fill="none"
        />
      </svg>
      <div style={{ display: "flex", flexDirection: "column" }}>
        <span className="micro-label">CAT STATE</span>
        <span style={{ fontSize: "12px", color: "var(--ink-900)", fontWeight: 500 }}>
          {stateText}
        </span>
      </div>
    </div>
  );
};
