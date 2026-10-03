import { Content, RenderResult } from "../types";

export interface ValidationIssue {
  type: "error" | "warning";
  field?: string;
  message: string;
}

export function validateContent(content: Content): ValidationIssue[] {
  const issues: ValidationIssue[] = [];

  // Check handle format: /^[A-Za-z0-9-]{1,39}$/
  if (!/^[A-Za-z0-9-]{1,39}$/.test(content.handle)) {
    issues.push({
      type: "error",
      field: "handle",
      message: "GitHub handle must contain 1-39 alphanumeric characters or hyphens only.",
    });
  }

  // LinkedIn placeholder check
  if (content.linkedin.includes("YOUR-LINKEDIN")) {
    issues.push({
      type: "warning",
      field: "linkedin",
      message: "LinkedIn placeholder URL detected ('YOUR-LINKEDIN'). Replace with your actual profile link.",
    });
  }

  // About check
  if (!content.about || content.about.length === 0 || !content.about[0]?.trim()) {
    issues.push({
      type: "warning",
      field: "about",
      message: "About section is empty.",
    });
  }

  // Projects check
  if (content.projects.length === 0) {
    issues.push({
      type: "error",
      field: "projects",
      message: "At least one project is required.",
    });
  }

  return issues;
}

export function validateRenderResult(result: RenderResult): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  const parser = new DOMParser();

  let totalSize = 0;
  for (const [name, svgText] of Object.entries(result.files)) {
    const size = new Blob([svgText]).size;
    totalSize += size;

    if (size > 1024 * 1024) {
      issues.push({
        type: "error",
        message: `Asset ${name} exceeds 1 MB cap (${(size / 1024).toFixed(1)} KB).`,
      });
    }

    const doc = parser.parseFromString(svgText, "image/svg+xml");
    const parserError = doc.querySelector("parsererror");
    if (parserError) {
      issues.push({
        type: "error",
        message: `SVG parsing error in ${name}: ${parserError.textContent?.slice(0, 80)}`,
      });
    }
  }

  if (totalSize > 5 * 1024 * 1024) {
    issues.push({
      type: "error",
      message: `Total asset package size (${(totalSize / 1024 / 1024).toFixed(2)} MB) exceeds 5 MB hard cap.`,
    });
  } else if (totalSize > 2.5 * 1024 * 1024) {
    issues.push({
      type: "warning",
      message: `Total asset size (${(totalSize / 1024 / 1024).toFixed(2)} MB) exceeds 2.5 MB recommendation.`,
    });
  }

  return issues;
}
