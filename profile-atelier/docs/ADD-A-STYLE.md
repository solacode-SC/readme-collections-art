# How to Add a New README Style in 6 Steps

Follow these steps to contribute or add a custom style to Profile Atelier:

### Step 1: Create Style Directory
Create a folder named with your style slug under `src/styles/<style-id>/`.

### Step 2: Provide Source Image
If your style uses background or hero artwork:
- Save your image to `public/art/<style-id>/source.jpg`.
- If pure procedural math (like `swirl`), you can skip this.

### Step 3: Implement the Style Module
Create `src/styles/<style-id>/index.ts` implementing `StyleModule`:

```ts
import { StyleModule, Content, RenderCtx, RenderResult } from "../../types";

export const myStyle: StyleModule = {
  id: "my-style",
  name: "My Style",
  keywords: ["keyword1", "keyword2", "keyword3"],
  palette: {
    light: ["#FFFFFF", "#000000", ...],
    dark: ["#000000", "#FFFFFF", ...]
  },
  motion: "calm", // "none" | "calm" | "lively"
  async render(content: Content, ctx: RenderCtx): Promise<RenderResult> {
    // Generate SVGs for dark & light
    // Return files dictionary, README.md markdown string, and total size
  }
};
```

### Step 4: Ensure Standard Panels
Every style must generate SVG files matching these naming conventions for both `-dark.svg` and `-light.svg`:
- `hero`
- `btn-github`, `btn-linkedin`, `btn-portfolio`
- `about`
- `skills`
- `projects-title`
- `card-<slug>` for each project
- `footer`

### Step 5: Register in Styles Registry
Open `src/styles/registry.ts`, import your module and append it to the `STYLES` array.

### Step 6: Test & Verify
Run tests and build to ensure all SVG files are valid XML and under size budgets:
```bash
npm test
npm run build
```
