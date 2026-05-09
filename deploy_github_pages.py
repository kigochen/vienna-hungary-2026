#!/usr/bin/env python3
"""
Vienna Trip - GitHub Pages Deployment Script
"""

import os
import shutil
import sys
from pathlib import Path

WORKSPACE = Path("/home/node/.openclaw/workspace")
SRC_DIR = WORKSPACE / "vienna-trip" / "src"
DST_DIR = WORKSPACE / "vienna-trip-gh-pages"

SRC_FILES = {
    "index.html": "index.html",
    "places.json": "places.json",
}

README_CONTENT = """# 維也納 + 匈牙利之旅 2026

旅遊景點收藏網站 | 8/30-9/12

## 🔗 Live Site
https://[username].github.io/vienna-trip/

## 📂 部署方式
1. Fork 或複製這個 repo
2. 開啟 GitHub Pages（Settings → Pages → Source: main branch）
3. 即可透過 https://[username].github.io/vienna-trip/ 存取

## 📁 檔案結構
- `index.html` - 主網站（Dark Mode, Leaflet 地圖）
- `places.json` - 景點資料（62 景點，14天行程）

## ✏️ 如何更新景點
編輯 `places.json` 即可自動更新網站上的所有景點卡片、地圖標記、行程時間線。
"""

def deploy():
    DST_DIR.mkdir(parents=True, exist_ok=True)
    errors = []

    for src_rel, dst_rel in SRC_FILES.items():
        src = SRC_DIR / src_rel
        dst = DST_DIR / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Copied {src_rel}")
        else:
            print(f"  ⚠️  Missing {src_rel} (skipping)")
            errors.append(f"Missing: {src_rel}")

    # Copy README
    readme = DST_DIR / "README.md"
    readme.write_text(README_CONTENT.strip())
    print(f"  ✅ Written README.md")

    print(f"\n{'='*50}")
    print(f"Deploy complete: {len(SRC_FILES) + 1} files copied")
    print(f"Output dir: {DST_DIR}")
    if errors:
        print(f"Warnings: {len(errors)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(deploy())