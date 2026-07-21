"""
Package the Pro Tools Bundle — all 35 tools in a downloadable ZIP.

Usage: python scripts/package-pro-bundle.py
Output: pro-bundle-v1.0.zip  (in the root directory)
"""

import os
import zipfile
import json
import shutil
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
OUTPUT_ZIP = os.path.join(ROOT, "pro-bundle-v1.0.zip")
APPS_DIR = os.path.join(ROOT, "apps")
EXCLUDE = {"node_modules", "__pycache__", ".git", ".github"}

def build_manifest():
    """Build a manifest.json for the pro bundle."""
    tools = sorted(os.listdir(APPS_DIR))
    manifest = {
        "bundle_name": "Free Web Tools — Pro Bundle",
        "version": "1.0.0",
        "release_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "total_tools": len(tools),
        "license": "Commercial License — All Rights Reserved",
        "author": "aymanviola1-creator",
        "website": "https://aymanviola1-creator.github.io/free-web-tools/",
        "features": [
            "Offline usage — no internet required",
            "No ads, no trackers, no analytics",
            "Dark & light theme toggle",
            "localStorage settings persistence",
            "One-click export & download options",
            "Print-friendly layouts",
            "Commercial use allowed",
            "Free updates forever",
        ],
        "tools": [],
    }
    for tool in tools:
        tool_path = os.path.join(APPS_DIR, tool, "index.html")
        if os.path.exists(tool_path):
            manifest["tools"].append({
                "name": tool.replace("-", " ").title(),
                "directory": tool,
                "entry": f"apps/{tool}/index.html",
            })
    return manifest

def package_bundle():
    print("=" * 60)
    print("  PACKAGING PRO TOOLS BUNDLE")
    print("=" * 60)

    if not os.path.exists(APPS_DIR):
        print(f"❌ Apps directory not found: {APPS_DIR}")
        return False

    # Build manifest
    manifest = build_manifest()
    print(f"\n📦 Tools in bundle: {manifest['total_tools']}")

    # Create ZIP
    with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add manifest
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))
        print("  ✅ Added: manifest.json")

        # Add each tool
        for tool in sorted(os.listdir(APPS_DIR)):
            tool_dir = os.path.join(APPS_DIR, tool)
            if not os.path.isdir(tool_dir):
                continue
            html_file = os.path.join(tool_dir, "index.html")
            if os.path.exists(html_file):
                arc_name = f"apps/{tool}/index.html"
                zf.write(html_file, arc_name)
                print(f"  ✅ Added: {arc_name}")

        # Add the main landing page (without ad code)
        index_path = os.path.join(ROOT, "index.html")
        if os.path.exists(index_path):
            zf.write(index_path, "index.html")
            print("  ✅ Added: index.html")

        # Add icon
        icon_path = os.path.join(ROOT, "icon.svg")
        if os.path.exists(icon_path):
            zf.write(icon_path, "icon.svg")
            print("  ✅ Added: icon.svg")

        # Add README
        readme = """# Free Web Tools — Pro Bundle

## What's Included
All 35 premium web tools in a single offline package.

## How to Use
1. Unzip the folder
2. Open `index.html` in your browser
3. All tools work offline — no internet required

## Features
- 35 tools: HTML/CSS/JS minifiers, SQL formatter, YAML/JSON converters, UUID generator, regex tester, QR code tools, markdown editor, and 25+ more
- Dark & light theme toggle
- No ads, no trackers, no analytics
- Commercial use allowed
- Free updates forever

## License
Commercial License — All Rights Reserved
Copyright 2026 aymanviola1-creator
"""
        zf.writestr("README.txt", readme)
        print("  ✅ Added: README.txt")

    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"\n✅ Bundle created: {OUTPUT_ZIP}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   Tools: {manifest['total_tools']}")
    return True

if __name__ == "__main__":
    package_bundle()
