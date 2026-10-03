import React from "react";

interface WeightGaugeProps {
  bytes: number; // in bytes
}

export const WeightGauge: React.FC<WeightGaugeProps> = ({ bytes }) => {
  const maxBytes = 2.5 * 1024 * 1024; // 2.5 MB target budget
  const percent = Math.min(Math.round((bytes / maxBytes) * 100), 100);
  const kb = Math.round(bytes / 1024);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "5px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span className="micro-label">WEIGHT GAUGE</span>
        <span style={{ fontSize: "11px", fontFamily: "var(--font-mono)", color: "var(--ink-700)" }}>
          {percent}% ({kb} KB)
        </span>
      </div>
      <div
        style={{
          width: "120px",
          height: "10px",
          borderRadius: "999px",
          backgroundColor: "var(--paper-200)",
          border: "1px solid var(--stone-300)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${percent}%`,
            backgroundColor: "var(--ink-700)",
            transition: "width 0.2s ease-out",
          }}
        />
      </div>
    </div>
  );
};
