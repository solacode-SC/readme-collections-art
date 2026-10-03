# Profile Atelier (README Style Studio)

> **Design tool & live engine for GitHub profile READMEs.**  
> Built with Japanese-Bauhaus editorial aesthetics, vector animations, live customizer, and client-side zero-server ZIP export.

---

## ✦ Key Features

1. **7 Distinct Styles Supported**:
   - **Swirl**: Pure mathematical flow-field streamlines and Archimedean spirals.
   - **Moon Gate**: Magical night portal, rotating rune rings, octagrams, and drifting blossom petals.
   - **Garden**: Autumn storybook illustration with gently swaying twigs and falling leaves.
   - **Phoenix**: Regal crimson and gold lacquer with layered gilded peonies.
   - **Andalus**: Alhambra Moroccan zellige, 8-point geometric star friezes, and bilingual Arabic support.
   - **Codex**: 15th-century illuminated manuscript with gilded drop caps, vellum frames, and Roman numerals.
   - **Ink Scroll**: Calm Chinese hanging scroll with hand-lettered seals and xuan paper aesthetic.

2. **Live Interactive Editor**:
   - Edit personal identity, links, about paragraphs, journey milestones, skills monograms, and projects.
   - Live debounced re-renders with defense against text overflow and XML security escaping (`& < > " '`).
   - Warning flags for placeholder LinkedIn profile links.

3. **Multi-device & Theme Simulation**:
   - Exact simulation of GitHub profile README light and dark themes.
   - Desktop and Mobile (390px ink bezel phone frame) toggle.
   - Motion controls: 走る (Play), 跳ぶ (Step / Replay), 落ちる (Reduced motion emulation).

4. **100% Client-side Offline Exports**:
   - Single-style ready-to-push ZIP (`<handle>-<style>.zip`) containing SVG assets, `README.md`, `content.json`, and guides.
   - Full collection ZIP package (`<handle>-all-styles.zip`) with complete multi-style folder tree.
   - "Copy Agent Prompt" generator to allow any AI to create new styles using your latest profile data.

---

## ✦ Quick Start

```bash
# Clone the repository and enter the directory
cd profile-atelier

# Install dependencies
npm install

# Start development server
npm run dev

# Run unit tests
npm test

# Build production bundle
npm run build
```

---

## ✦ Adding a New Style (in 6 Steps)

1. Create a new folder under `src/styles/<style-id>/`.
2. Add your source image (if needed) under `public/art/<style-id>/source.jpg`.
3. Implement `src/styles/<style-id>/index.ts` conforming to the `StyleModule` interface.
4. Export SVG generators for panels: `hero`, `about`, `skills`, `projects-title`, `btn-*`, `card-*`, and `footer`.
5. Register the style module in `src/styles/registry.ts`.
6. Run `npm test` and verify that all generated SVGs pass XML parsing and size constraints.
