import React, { useState, useMemo } from "react";
import { StyleModule } from "../types";

interface StyleGalleryProps {
  styles: StyleModule[];
  selectedId: string;
  onSelect: (id: string) => void;
  onClose?: () => void;
}

export const StyleGallery: React.FC<StyleGalleryProps> = ({
  styles,
  selectedId,
  onSelect,
  onClose,
}) => {
  const [search, setSearch] = useState("");

  const filtered = useMemo(() => {
    if (!search.trim()) return styles;
    const q = search.trim().toLowerCase();
    return styles.filter(
      (s) =>
        s.name.toLowerCase().includes(q) ||
        s.id.toLowerCase().includes(q) ||
        s.keywords.some((k) => k.toLowerCase().includes(q))
    );
  }, [styles, search]);

  return (
    <>
      {/* Search */}
      <div className="sidebar__header">
        <input
          className="sidebar__search"
          type="text"
          placeholder="Search templates..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        {onClose && (
          <button
            className="btn btn--ghost btn--sm desktop-only"
            style={{ marginLeft: 6, minWidth: 28, padding: "0 6px", height: 28 }}
            onClick={onClose}
            title="Hide styles sidebar"
          >
            ✕
          </button>
        )}
      </div>

      {/* Style list */}
      <div className="sidebar__list">
        {filtered.map((s) => {
          const isActive = s.id === selectedId;
          return (
            <div
              key={s.id}
              className={`style-card ${isActive ? "style-card--active" : ""}`}
              onClick={() => onSelect(s.id)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onSelect(s.id);
                }
              }}
            >
              {/* Color swatch */}
              <div
                className="style-card__swatch"
                style={{ background: s.palette.dark[0] }}
              >
                <div className="style-card__swatch-dots">
                  {s.palette.dark.slice(1, 5).map((hex, i) => (
                    <div
                      key={i}
                      className="style-card__swatch-dot"
                      style={{ backgroundColor: hex }}
                    />
                  ))}
                </div>
              </div>

              {/* Info */}
              <div className="style-card__info">
                <span className="style-card__name">{s.name}</span>
              </div>
            </div>
          );
        })}

        {filtered.length === 0 && (
          <div style={{ padding: "20px 8px", textAlign: "center" }}>
            <span className="caption">No templates match your search</span>
          </div>
        )}
      </div>
    </>
  );
};

