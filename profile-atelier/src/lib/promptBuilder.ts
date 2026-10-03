import { Content } from "../types";

export function buildAgentPrompt(content: Content, brief: string = ""): string {
  return `================================================================================
NEW GITHUB PROFILE README STYLE GENERATOR PROMPT
================================================================================

1. OWNER DATA
name ........... ${content.name}
handle ......... ${content.handle} (GitHub: ${content.github})
portfolio ...... ${content.portfolio}
linkedin ....... ${content.linkedin}
role ........... ${content.role}
pillars ........ ${content.pillars}
tagline ........ ${content.tagline.join(" ")}
about ..........
  ${content.about.join("\n  ")}
journey:
${content.journey.map((j) => `  ${j.lang} -> ${j.area}`).join(" | ")}
skills:
  ${content.skills.map((s) => `${s.label} (${s.mono})`).join(", ")}
projects:
${content.projects.map((p, i) => `  ${i + 1}. ${p.title} (${p.slug}): ${p.line1} ${p.line2} [${p.tags.join(", ")}]`).join("\n")}
footer ......... "${content.footer.line1}" / "${content.footer.line2}"

2. STYLE BRIEF
${brief || "<Describe your artistic direction, colors, mood, animation, and image usage here>"}

3. TECHNICAL REQUIREMENTS
- Produces valid SVGs for dark and light themes:
  hero-dark.svg, hero-light.svg
  btn-github-dark.svg, btn-github-light.svg
  btn-linkedin-dark.svg, btn-linkedin-light.svg
  btn-portfolio-dark.svg, btn-portfolio-light.svg
  about-dark.svg, about-light.svg
  skills-dark.svg, skills-light.svg
  projects-title-dark.svg, projects-title-light.svg
  card-<slug>-dark.svg, card-<slug>-light.svg (for each project)
  footer-dark.svg, footer-light.svg
- README.md uses <picture> tags for light/dark switching.
- Projects are arranged in rows with width="24%".
- Every text string inserted in SVGs MUST be XML-escaped (& < > " ').
- CSS-only animations inside SVG with @media (prefers-reduced-motion: reduce) { animation: none }.
- Zero remote scripts or fonts; self-contained vector and cropped embedded base64.
================================================================================`;
}
