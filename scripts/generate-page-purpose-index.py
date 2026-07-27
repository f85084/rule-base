#!/usr/bin/env python3
"""從 project-docs 的 CSP L2 頁面文件建立簡單的網站頁面用途索引。"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENU = ROOT / "data/sources/csp/website-menus.json"
OUT = ROOT / "docs/csp/requirements/page-purpose-index.md"
PROJECT_DOCS = Path("/home/art/openab-repos/project-docs/projects/CSP/data/business-flows/L2")
L2_INDEX = PROJECT_DOCS / "INDEX.md"


def normalize_route(route):
    route = route.strip().strip("`").lower().rstrip("/") or "/"
    return route if route.startswith("/") else f"/{route}"


def load_l2_index():
    found = {}
    if not L2_INDEX.exists():
        return found
    for line in L2_INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "路由路徑" in line:
            continue
        cols = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cols) < 3:
            continue
        route = normalize_route(cols[1])
        if not route.startswith("/"):
            continue
        file_match = re.search(r"\]\(([^)]+)\)", cols[2])
        if file_match:
            found[route] = file_match.group(1)
    return found


def purpose_from_file(path):
    if not path.exists():
        return "尚未找到 L2 頁面全貌文件。"
    lines = path.read_text(encoding="utf-8").splitlines()

    # 優先讀取 L2 明確整理的頁面概覽／意圖，避免只讀到前端路徑。
    for heading in ("## 頁面概覽", "## 頁面意圖描述"):
        try:
            start = lines.index(heading) + 1
        except ValueError:
            continue
        current = []
        for line in lines[start:]:
            if line.startswith("#") or line.startswith("|"):
                break
            text = line.strip().lstrip("> ")
            if text:
                current.append(text)
            elif current:
                break
        if current:
            return " ".join(current).replace("|", "\\|")[:360]

    started = False
    paragraphs = []
    current = []
    for line in lines:
        if line.startswith("# 頁面："):
            started = True
            continue
        if not started:
            continue
        if line.startswith("#") or line.startswith("##") or line.startswith("|"):
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
            if line.startswith("#"):
                break
            continue
        text = line.strip().lstrip("> ")
        if text:
            current.append(text)
        elif current:
            paragraphs.append(" ".join(current).strip())
            current = []
        if sum(len(x) for x in paragraphs) > 360:
            break
    if current:
        paragraphs.append(" ".join(current).strip())
    purpose = next((x for x in paragraphs if len(x) > 20), "尚未從 L2 文件擷取到用途摘要。")
    return purpose.replace("|", "\\|")[:360]


def main():
    menu = json.loads(MENU.read_text(encoding="utf-8"))
    l2 = load_l2_index()
    lines = [
        "# CSP 網站頁面用途索引", "",
        "用途說明來源：`/home/art/openab-repos/project-docs/projects/CSP/data/business-flows/L2/`。",
        "本文件先提供簡要頁面用途，作為需求單分類的人工校對依據；詳細流程仍以 project-docs 的 L2 文件為準。", "",
        "| 頁面 | URL | 頁面用途摘要 | project-docs L2 |",
        "|---|---|---|---|",
    ]
    for group in menu["groups"]:
        for page in group["pages"]:
            route = page["url"]
            filename = l2.get(normalize_route(route))
            source = f"`{filename}`" if filename else "—"
            purpose = purpose_from_file(PROJECT_DOCS / filename) if filename else "尚未找到對應 L2 文件，先依網站選單名稱與需求單內容判斷。"
            lines.append(f"| {page['name']} | `{route}` | {purpose} | {source} |")
    lines += ["", "## 使用方式", "", "1. 先用頁面用途判斷需求單是否真的屬於該頁。", "2. 若需求描述與頁面用途不符，不要只因關鍵字命中就歸類，改列入人工確認或補充分類規則。", "3. 需要更完整流程時，沿著表格中的 L2 文件回到 project-docs 查閱。"]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"完成：{sum(len(g['pages']) for g in menu['groups'])} 個網站頁面")


if __name__ == "__main__":
    main()
