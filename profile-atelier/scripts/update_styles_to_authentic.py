import os

STYLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "styles"))

mapping = {
    "swirl": "swirl",
    "lotus": "lotus",
    "frost": "frost",
    "tree": "tree",
    "citadel": "citadel",
    "phoenix": "citadel",
    "isekai": "isekai",
    "ghost": "ghost",
    "lapis": "lapis",
    "canopy": "canopy",
    "andalus": "andalus",
    "floral": "floral",
    "vangogh": "vangogh",
    "moongate": "moongate",
    "inkscroll": "inkscroll",
    "garden": "garden",
    "codex": "codex",
    "lilypond": "lilypond",
}

for style_name, template_id in mapping.items():
    idx_path = os.path.join(STYLES_DIR, style_name, "index.ts")
    export_name = f"{style_name}Style"
    code = f'''import {{ StyleModule }} from "../../types";
import {{ getAuthenticStyleById }} from "../authenticTemplates";

export const {export_name}: StyleModule = getAuthenticStyleById("{template_id}")!;
export default {export_name};
'''
    os.makedirs(os.path.dirname(idx_path), exist_ok=True)
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Updated {style_name}/index.ts -> authentic template '{template_id}'")

print("All style modules successfully updated to authentic folder templates.")
