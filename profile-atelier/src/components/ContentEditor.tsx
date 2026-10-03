import React from "react";
import { Content, Project } from "../types";

interface ContentEditorProps {
  content: Content;
  onChange: (updated: Content) => void;
  onReset: () => void;
}

export const ContentEditor: React.FC<ContentEditorProps> = ({ content, onChange }) => {
  const update = (partial: Partial<Content>) => {
    onChange({ ...content, ...partial });
  };

  const updateProject = (index: number, partial: Partial<Project>) => {
    const list = [...content.projects];
    list[index] = { ...list[index], ...partial };
    update({ projects: list });
  };

  const addProject = () => {
    const newProj: Project = {
      title: "New Project",
      slug: "new-project",
      line1: "Project description line 1",
      line2: "Project description line 2",
      tags: ["React", "TypeScript"],
    };
    update({ projects: [...content.projects, newProj] });
  };

  const removeProject = (index: number) => {
    update({ projects: content.projects.filter((_, i) => i !== index) });
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
      {/* ---- Identity ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Identity</span>
        <div className="form-field">
          <label className="form-label">Name</label>
          <input
            className="input"
            maxLength={28}
            value={content.name}
            onChange={(e) => update({ name: e.target.value })}
            placeholder="Your full name"
          />
        </div>
        <div className="form-field">
          <label className="form-label">Handle</label>
          <input
            className="input"
            maxLength={39}
            value={content.handle}
            onChange={(e) => update({ handle: e.target.value })}
            placeholder="GitHub username"
          />
        </div>
        <div className="form-field">
          <label className="form-label">Role</label>
          <input
            className="input"
            maxLength={28}
            value={content.role}
            onChange={(e) => update({ role: e.target.value })}
            placeholder="Software Engineer"
          />
        </div>
        <div className="form-field">
          <label className="form-label">Pillars</label>
          <input
            className="input"
            value={content.pillars}
            onChange={(e) => update({ pillars: e.target.value })}
            placeholder="AI | Math | Web"
          />
        </div>
      </div>

      <hr className="divider" />

      {/* ---- Links ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Links</span>
        <div className="form-field">
          <label className="form-label">GitHub URL</label>
          <input
            className="input"
            value={content.github}
            onChange={(e) => update({ github: e.target.value })}
          />
        </div>
        <div className="form-field">
          <label className="form-label">
            LinkedIn URL
            {content.linkedin.includes("YOUR-LINKEDIN") && (
              <span className="form-label__badge">Placeholder</span>
            )}
          </label>
          <input
            className="input"
            value={content.linkedin}
            onChange={(e) => update({ linkedin: e.target.value })}
          />
        </div>
        <div className="form-field">
          <label className="form-label">Portfolio URL</label>
          <input
            className="input"
            value={content.portfolio}
            onChange={(e) => update({ portfolio: e.target.value })}
          />
        </div>
      </div>

      <hr className="divider" />

      {/* ---- Tagline ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Tagline</span>
        {content.tagline.map((line, idx) => (
          <div className="form-field" key={idx}>
            <input
              className="input"
              value={line}
              onChange={(e) => {
                const list = [...content.tagline];
                list[idx] = e.target.value;
                update({ tagline: list });
              }}
              placeholder={`Tagline line ${idx + 1}`}
            />
          </div>
        ))}
      </div>

      <hr className="divider" />

      {/* ---- About ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>About</span>
        {content.about.map((p, idx) => (
          <div className="form-field" key={idx}>
            <textarea
              className="input"
              rows={3}
              value={p}
              onChange={(e) => {
                const list = [...content.about];
                list[idx] = e.target.value;
                update({ about: list });
              }}
              placeholder={`Paragraph ${idx + 1}`}
            />
          </div>
        ))}
      </div>

      <hr className="divider" />

      {/* ---- Journey ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Journey</span>
        {content.journey.map((j, idx) => (
          <div className="form-field" key={idx} style={{ display: "flex", gap: 6, flexDirection: "row" }}>
            <input
              className="input"
              value={j.lang}
              onChange={(e) => {
                const list = [...content.journey];
                list[idx] = { ...list[idx], lang: e.target.value };
                update({ journey: list });
              }}
              placeholder="Language"
              style={{ flex: 1 }}
            />
            <input
              className="input"
              value={j.area}
              onChange={(e) => {
                const list = [...content.journey];
                list[idx] = { ...list[idx], area: e.target.value };
                update({ journey: list });
              }}
              placeholder="Area"
              style={{ flex: 1 }}
            />
          </div>
        ))}
      </div>

      <hr className="divider" />

      {/* ---- Skills ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Skills</span>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
          {content.skills.map((s, idx) => (
            <div key={idx} style={{ display: "flex", gap: 4 }}>
              <input
                className="input"
                value={s.label}
                onChange={(e) => {
                  const list = [...content.skills];
                  list[idx] = { ...list[idx], label: e.target.value };
                  update({ skills: list });
                }}
                placeholder="Label"
                style={{ flex: 2 }}
              />
              <input
                className="input"
                value={s.mono}
                onChange={(e) => {
                  const list = [...content.skills];
                  list[idx] = { ...list[idx], mono: e.target.value };
                  update({ skills: list });
                }}
                placeholder="Abbr"
                style={{ flex: 1, fontFamily: "var(--font-mono)", fontSize: 12 }}
              />
            </div>
          ))}
        </div>
      </div>

      <hr className="divider" />

      {/* ---- Projects ---- */}
      <div className="form-section">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <span className="section-label">Projects ({content.projects.length})</span>
          <button className="btn btn--secondary btn--sm" onClick={addProject}>
            + Add
          </button>
        </div>

        {content.projects.map((proj, idx) => (
          <div className="project-card" key={idx}>
            <div className="project-card__header">
              <span className="project-card__title">#{idx + 1} {proj.title}</span>
              <button
                className="project-card__remove"
                onClick={() => removeProject(idx)}
                title="Remove project"
              >
                ✕
              </button>
            </div>
            <input
              className="input"
              placeholder="Title"
              maxLength={18}
              value={proj.title}
              onChange={(e) => {
                const title = e.target.value;
                const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
                updateProject(idx, { title, slug });
              }}
            />
            <input
              className="input"
              placeholder="Description line 1"
              maxLength={30}
              value={proj.line1}
              onChange={(e) => updateProject(idx, { line1: e.target.value })}
            />
            <input
              className="input"
              placeholder="Description line 2"
              maxLength={30}
              value={proj.line2}
              onChange={(e) => updateProject(idx, { line2: e.target.value })}
            />
            <input
              className="input"
              placeholder="Tags (comma-separated)"
              value={proj.tags.join(", ")}
              onChange={(e) =>
                updateProject(idx, {
                  tags: e.target.value.split(",").map((t) => t.trim()).filter(Boolean),
                })
              }
            />
          </div>
        ))}
      </div>

      <hr className="divider" />

      {/* ---- Footer content ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Footer</span>
        <div className="form-field">
          <label className="form-label">Line 1</label>
          <input
            className="input"
            value={content.footer.line1}
            onChange={(e) => update({ footer: { ...content.footer, line1: e.target.value } })}
          />
        </div>
        <div className="form-field">
          <label className="form-label">Line 2</label>
          <input
            className="input"
            value={content.footer.line2}
            onChange={(e) => update({ footer: { ...content.footer, line2: e.target.value } })}
          />
        </div>
      </div>

      <hr className="divider" />

      {/* ---- Options ---- */}
      <div className="form-section">
        <span className="section-label" style={{ marginBottom: 8 }}>Options</span>
        <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, cursor: "pointer" }}>
          <input
            type="checkbox"
            checked={content.options.useArabic}
            onChange={(e) => update({ options: { ...content.options, useArabic: e.target.checked } })}
          />
          Use Arabic text
        </label>
        <label style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, cursor: "pointer", marginTop: 6 }}>
          <input
            type="checkbox"
            checked={content.options.useCJK}
            onChange={(e) => update({ options: { ...content.options, useCJK: e.target.checked } })}
          />
          Use CJK characters
        </label>
      </div>
    </div>
  );
};

