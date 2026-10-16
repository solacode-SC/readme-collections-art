import os, re

folders = sorted([d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and d != 'profile-atelier'])
for f in folders:
    rm_path = os.path.join(f, 'README.md')
    if os.path.exists(rm_path):
        txt = open(rm_path, encoding='utf-8', errors='ignore').read()
        alts = re.findall(r'alt=["\']([^"\']+)["\']', txt)
        print(f"=== {f} ===")
        print("  Top alts:", alts[:3])
        # Also check assets prefix in README
        refs = re.findall(r'(?:src|srcset)=["\']([^"\']+)["\']', txt)
        asset_refs = [r for r in refs if 'assets/' in r]
        print(f"  Asset count referenced: {len(asset_refs)}, unique: {len(set(asset_refs))}")
        print("  Sample asset refs:", asset_refs[:3])
