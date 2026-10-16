#!/usr/bin/env python3
import os
import shutil
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PUBLIC_TEMPLATES_DIR = os.path.join(APP_DIR, "public", "templates")
os.makedirs(PUBLIC_TEMPLATES_DIR, exist_ok=True)

# List of templates to map from original folders
# (id, folder_name, display_name, description, dark_palette, light_palette)
CONFIG = [
    (
        "swirl",
        "profile-readme-swirl",
        "Golden Swirl",
        "Fibonacci golden ratio spirals with dynamic generative flow lines",
        ["#041114", "#0a2126", "#ecf4ef", "#f0d672", "#2f8f98"],
        ["#fbf7ea", "#efe8d2", "#12343a", "#96640a", "#1d6670"]
    ),
    (
        "lotus",
        "solacode-lotus-readme",
        "Lotus Pond",
        "Kintsugi Lotus Pond with animated swimming koi and golden leaf patterns",
        ["#06151b", "#0d2a34", "#e8f2ef", "#e2bb63", "#ea5a2c"],
        ["#f1e3c6", "#fbf4e1", "#13303a", "#a2711f", "#d2461c"]
    ),
    (
        "frost",
        "solacode-readme-frost",
        "Frost Castle",
        "Moonlit winter citadel by a frozen lake with falling snow & custom typography",
        ["#050917", "#0b2358", "#f3f1ea", "#8fb6ff", "#2557c0"],
        ["#e8f0fc", "#f6f2e7", "#0a1b45", "#1c4db0", "#7a5d12"]
    ),
    (
        "tree",
        "solayman-tree-readme",
        "Topographic Tree",
        "Organic topographic contour rings and architectural growth methodology",
        ["#09111c", "#0e1a2b", "#f2f7fc", "#56cfe1", "#e0a96d"],
        ["#f5f8fc", "#ebf2fa", "#0b1523", "#1a6f87", "#9e6831"]
    ),
    (
        "citadel",
        "solacode-readme",
        "Sunset Citadel",
        "Crimson dragon soaring above a desert fortress citadel at golden sunset",
        ["#140c0a", "#241410", "#faeee8", "#e85d38", "#f2b544"],
        ["#faf4ee", "#f4e4d6", "#2a150e", "#b84222", "#b88224"]
    ),
    (
        "isekai",
        "solacode-isekai-readme",
        "Isekai Portal",
        "Magic forest portal overlooking an enchanted castle in a fantasy realm",
        ["#0a1418", "#112228", "#ebf5f7", "#69cbc6", "#e2bb63"],
        ["#f2f8f6", "#e5f1ee", "#14282e", "#2c948e", "#a87a22"]
    ),
    (
        "ghost",
        "solacode-ghost-readme",
        "Ghost Library",
        "Friendly spirits floating through an impossible starlit cosmic library",
        ["#080e1a", "#101a2e", "#e8efff", "#7fa8ff", "#f3c76a"],
        ["#f0f4fc", "#e4ecfa", "#101c34", "#3b6ed6", "#a6781c"]
    ),
    (
        "lapis",
        "solacode-readme-lapis",
        "Lapis Dragon",
        "Majestic sapphire dragon beside an embroidered royal gown and stars",
        ["#06111e", "#0c1d32", "#eaf1fa", "#4c8ee8", "#d8a946"],
        ["#edf4fc", "#e0ebf8", "#0e2038", "#2466be", "#a4791e"]
    ),
    (
        "canopy",
        "solacode-readme-canopy",
        "Spiral Canopy",
        "Lush forest canopy swirling into mathematical Fibonacci spirals",
        ["#061510", "#0c261e", "#eaf5ee", "#4ec989", "#d4a849"],
        ["#eef8f2", "#e0f0e6", "#0e2c22", "#289e62", "#9e7722"]
    ),
    (
        "andalus",
        "solacode-readme-andalus",
        "Andalusian Dragons",
        "Twin pale dragons intertwining inside a Moorish horseshoe arch",
        ["#100c0a", "#1e1612", "#faeee3", "#e07a5f", "#d4a359"],
        ["#f9f3ec", "#f0e5d8", "#2c1e18", "#b65037", "#a27429"]
    ),
    (
        "floral",
        "solayman-floral-readme-v2",
        "Floral Botanic",
        "Botanical flora artwork with rich garden illustration and banners",
        ["#081711", "#10271e", "#edf7f1", "#4eb87a", "#deb248"],
        ["#f0f8f3", "#e3f2e8", "#123024", "#2c9458", "#a68020"]
    ),
    (
        "moongate",
        "profile-readme-moongate",
        "Cherry Moongate",
        "Zen moongate pavilion framing blossoms under the moonlight",
        ["#080a14", "#111524", "#f0f2fa", "#e87a90", "#6b82e8"],
        ["#f6f7fc", "#eceef8", "#12162a", "#c64e66", "#445cb8"]
    ),
    (
        "inkscroll",
        "profile-readme-inkscroll",
        "Zen Ink Scroll",
        "Traditional hanging silk scroll with crimson artist seals",
        ["#101010", "#1c1c1c", "#f5f5f3", "#c83838", "#a0a09e"],
        ["#fafaf8", "#f0f0ec", "#181816", "#a82020", "#585854"]
    ),
    (
        "garden",
        "profile-readme-garden",
        "Zen Garden",
        "Japanese rock and botanical garden with serene water lilies",
        ["#061410", "#0d221c", "#edf5f1", "#52b788", "#d69e2e"],
        ["#eef6f2", "#e0ede6", "#0c241e", "#318c62", "#9e6f10"]
    ),
    (
        "codex",
        "profile-readme-codex",
        "Illuminated Codex",
        "Medieval illuminated manuscript with gilded gold borders",
        ["#140f0c", "#221914", "#f8f2ec", "#c99e32", "#9c3826"],
        ["#faf5f0", "#f2eae0", "#241912", "#987216", "#822616"]
    ),
    (
        "andalusn",
        "profile-readme-andalusn",
        "Andalusian Geometric",
        "Intricate Moorish geometric arabesque patterns and calligraphy",
        ["#0c1015", "#141c24", "#edf2f8", "#4a90e2", "#c59b27"],
        ["#f2f5f9", "#e5ecf4", "#121a24", "#2c6eb8", "#987412"]
    ),
    (
        "red",
        "profile-readme-red",
        "Crimson Citadel",
        "Fiery crimson phoenix banner with bold technical layout",
        ["#160808", "#240f0f", "#fceeee", "#e63946", "#f4a261"],
        ["#fdf4f4", "#fae6e6", "#280e0e", "#b82430", "#c66e2c"]
    ),
    (
        "classic",
        "profile-readme",
        "Midnight Classic",
        "Clean elegant modern developer profile with dark aesthetics",
        ["#0d1117", "#161b22", "#f0f6fc", "#4493f8", "#238636"],
        ["#ffffff", "#f6f8fa", "#1f2328", "#0969da", "#1a7f37"]
    ),
    (
        "lilypond",
        "jjjjj",
        "Lily Pond Painting",
        "Impressionist lily pond artwork with lotus pads and frogs",
        ["#071412", "#0f2420", "#ecf5f3", "#38b000", "#70e000"],
        ["#f0f8f6", "#e2f2ee", "#0e2420", "#247800", "#4aa000"]
    ),
    (
        "vangogh",
        "solayman-vangogh-readme",
        "Van Gogh Spirals",
        "Starry night swirling skies and golden flow fields",
        ["#0a1a1f", "#0f2832", "#f0f5f0", "#5ba3a0", "#c4a843"],
        ["#f5faf4", "#e8f2e6", "#14282e", "#3a7a76", "#9a8026"]
    )
]

def main():
    templates_meta = []
    
    for item in CONFIG:
        tid, folder_name, display_name, desc, dark_pal, light_pal = item
        src_folder = os.path.join(ROOT_DIR, folder_name)
        if not os.path.exists(src_folder):
            print(f"Warning: Folder {src_folder} does not exist, skipping.")
            continue
            
        dest_folder = os.path.join(PUBLIC_TEMPLATES_DIR, tid)
        os.makedirs(dest_folder, exist_ok=True)
        dest_assets = os.path.join(dest_folder, "assets")
        os.makedirs(dest_assets, exist_ok=True)
        
        # 1. Copy assets
        src_assets = os.path.join(src_folder, "assets")
        asset_files = []
        if os.path.exists(src_assets):
            for fname in os.listdir(src_assets):
                if fname.endswith(".svg") or fname.endswith(".png") or fname.endswith(".jpg"):
                    s_file = os.path.join(src_assets, fname)
                    d_file = os.path.join(dest_assets, fname)
                    shutil.copy2(s_file, d_file)
                    asset_files.append(fname)
                    
        # 2. Read or generate README.md
        src_readme_path = os.path.join(src_folder, "README.md")
        readme_content = ""
        if os.path.exists(src_readme_path):
            with open(src_readme_path, "r", encoding="utf-8", errors="ignore") as f:
                readme_content = f.read().strip()
                
        # If readme is empty (e.g. vangogh), generate authentic matching readme
        if not readme_content and tid == "vangogh":
            readme_content = """<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
  <img alt="Solayman El Mouden — Software Engineer. Van Gogh flowing spirals aesthetic." src="assets/header-dark.svg" width="100%">
</picture>

<br>
<a href="https://github.com/solacode-SC"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/btn-github-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/btn-github-light.svg">
  <img alt="GitHub" src="assets/btn-github-dark.svg" width="150">
</picture></a>&nbsp;
<a href="https://www.linkedin.com/in/YOUR-LINKEDIN"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/btn-linkedin-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/btn-linkedin-light.svg">
  <img alt="LinkedIn" src="assets/btn-linkedin-dark.svg" width="150">
</picture></a>&nbsp;
<a href="https://solaymantech.me"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/btn-portfolio-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/btn-portfolio-light.svg">
  <img alt="Portfolio" src="assets/btn-portfolio-dark.svg" width="150">
</picture></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/about-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/about-light.svg">
  <img alt="About me and my approach" src="assets/about-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/skills-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/skills-light.svg">
  <img alt="Technologies and skills" src="assets/skills-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/projects-title-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/projects-title-light.svg">
  <img alt="Selected projects" src="assets/projects-title-dark.svg" width="100%">
</picture>

<a href="https://github.com/solacode-SC/lazyequation"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-lazyequation-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-lazyequation-light.svg">
  <img alt="LazyEquation" src="assets/card-lazyequation-dark.svg" width="24%">
</picture></a>
<a href="https://github.com/solacode-SC/leetresume"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-leetresume-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-leetresume-light.svg">
  <img alt="LeetResume" src="assets/card-leetresume-dark.svg" width="24%">
</picture></a>
<a href="https://github.com/solacode-SC/libora"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-libora-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-libora-light.svg">
  <img alt="Libora" src="assets/card-libora-dark.svg" width="24%">
</picture></a>
<a href="https://github.com/solacode-SC/webserv"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-webserv-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-webserv-light.svg">
  <img alt="Webserv" src="assets/card-webserv-dark.svg" width="24%">
</picture></a>

<a href="https://github.com/solacode-SC/solajobs-v2"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-solajobs-v2-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/card-solajobs-v2-light.svg">
  <img alt="solaJobs v2" src="assets/card-solajobs-v2-dark.svg" width="24%">
</picture></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg">
  <img alt="Build, Explore, Understand" src="assets/footer-dark.svg" width="100%">
</picture>

<sub><a href="https://solaymantech.me">solaymantech.me</a> &nbsp;·&nbsp; <a href="https://www.linkedin.com/in/YOUR-LINKEDIN">LinkedIn</a></sub>

</div>"""
            with open(src_readme_path, "w", encoding="utf-8") as f:
                f.write(readme_content + "\n")
                
        # Write destination README
        dest_readme = os.path.join(dest_folder, "README.md")
        with open(dest_readme, "w", encoding="utf-8") as f:
            f.write(readme_content + "\n")
            
        templates_meta.append({
            "id": tid,
            "folder": folder_name,
            "name": display_name,
            "description": desc,
            "palette": {
                "dark": dark_pal,
                "light": light_pal
            },
            "readme": readme_content,
            "assetBase": f"/templates/{tid}/assets",
            "assets": sorted(asset_files)
        })
        print(f"Synced {tid} ({folder_name}): {len(asset_files)} assets, README {len(readme_content)} chars")

    # Save metadata JSON for client
    meta_json_path = os.path.join(APP_DIR, "src", "templatesData.json")
    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(templates_meta, f, indent=2)
    print(f"\nWrote {meta_json_path} with {len(templates_meta)} authentic templates.")

if __name__ == "__main__":
    main()
