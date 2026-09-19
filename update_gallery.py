#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
520aj 同步脚本 —— 引用主站(aj5.netlify.app)地址，同步到本地目录

原理：
- 从主站拉取 manifest.json（图片地址全部是 https://aj5.netlify.app/images/...，即引用主站地址）
- 拉取主站 index.html 的导航区(AUTO_NAV)，保持 520aj 分类与主站一致
- 生成本地 manifest.json 快照 + 更新 index.html 导航
- 线上 520aj 仍优先实时 fetch 主站(引用主站地址)，主站不可用时回退本地快照

运行：python3 update_gallery.py
"""
import json, re, urllib.request
from pathlib import Path

MAIN_SITE = "https://aj5.netlify.app"
MAIN_MANIFEST_URL = MAIN_SITE + "/manifest.json"
MAIN_INDEX_URL = MAIN_SITE + "/"
LOCAL_MAIN = Path("../2026-05-08-task-4")  # 同机主站副本(联网失败回退)
LOCAL_MANIFEST = Path("manifest.json")
INDEX_FILE = Path("index.html")


def _http_get(url):
    req = urllib.request.Request(
        url, headers={'Cache-Control': 'no-cache', 'User-Agent': '520aj-sync/1.0'}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8')


def fetch_main_manifest():
    try:
        return json.loads(_http_get(MAIN_MANIFEST_URL))
    except Exception as e:
        print(f"[WARN] 联网拉取主站 manifest 失败({e})，改用同机主站副本")
        return json.loads((LOCAL_MAIN / "manifest.json").read_text(encoding='utf-8'))


def fetch_main_index():
    try:
        return _http_get(MAIN_INDEX_URL)
    except Exception as e:
        print(f"[WARN] 联网拉取主站首页失败({e})，改用同机主站副本")
        return (LOCAL_MAIN / "index.html").read_text(encoding='utf-8')


def extract_nav(html):
    s = html.find("<!-- AUTO_NAV_START -->")
    e = html.find("<!-- AUTO_NAV_END -->")
    if s == -1 or e == -1:
        raise RuntimeError("主站 index.html 未找到 AUTO_NAV 标记")
    return html[s:e]  # 含首尾标记


def save_local_manifest(data):
    # 保持引用主站地址：base_url 与 shoes[].image 均不变
    LOCAL_MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"[OK] 本地 manifest.json 已写入({len(data['shoes'])} 件，图片均引用 {data.get('base_url', '主站')})")


def update_nav(nav_html):
    content = INDEX_FILE.read_text(encoding='utf-8')
    s = content.find("<!-- AUTO_NAV_START -->")
    e = content.find("<!-- AUTO_NAV_END -->")
    if s == -1 or e == -1:
        raise RuntimeError("520aj index.html 未找到 AUTO_NAV 标记")
    new = content[:s] + nav_html + content[e:]  # 保留 END 标记
    INDEX_FILE.write_text(new, encoding='utf-8')
    print("[OK] 导航已同步为主站最新分类")


def fix_fallback():
    """主站不可用时回退本地 manifest.json(同域)，修复原 shoes=[] 空备份 + initializeGallery 未定义"""
    content = INDEX_FILE.read_text(encoding='utf-8')
    if 'async function loadLocalManifest' not in content:
        marker = "async function loadShoesFromMainSite() {"
        helper = (
            "async function loadLocalManifest() {\n"
            "  try {\n"
            "    const r = await fetch('manifest.json?t=' + Date.now());\n"
            "    const m = await r.json();\n"
            "    return m.shoes || [];\n"
            "  } catch (_) { return []; }\n"
            "}\n\n"
        )
        content = content.replace(marker, helper + marker, 1)
    content = re.sub(
        r"shoes = \[\];\s*initializeGallery\(\);",
        "shoes = await loadLocalManifest();\n    if (shoes.length) renderGallery(\"all\");",
        content,
    )
    INDEX_FILE.write_text(content, encoding='utf-8')
    print("[OK] 已修复离线回退(主站不可用时读取本地 manifest.json)")


if __name__ == "__main__":
    print("=" * 50)
    print("520aj 同步：引用主站地址(aj5.netlify.app)")
    print("=" * 50)
    manifest = fetch_main_manifest()
    save_local_manifest(manifest)
    nav = extract_nav(fetch_main_index())
    update_nav(nav)
    fix_fallback()
    print("\n完成！提交到 GitHub 部署即可。")
