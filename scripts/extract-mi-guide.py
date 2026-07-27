#!/usr/bin/env python3
"""將 MI DOCX 依功能標題整理成可搜尋的 Markdown 完整版。"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/sources/csp/MI操作手冊20251112.docx"
OUTPUT = ROOT / "docs/csp/operations/MI完整手冊.md"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

CHAPTERS = {
    "系統登入與基本設定": "登入與基本設定",
    "二、 訂單客服管理": "訂單客服管理",
    "三、訊息管理": "訊息管理",
    "四、音檔管理": "音檔管理",
    "五、內部工作管理": "內部工作管理",
    "六、名單管理": "名單管理",
    "●儀錶板篇": "補充：儀表板",
    "●商品篇": "補充：商品與接單",
    "其他/補充教材": "補充教材",
}


def paragraphs() -> list[str]:
    with ZipFile(SOURCE) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    result = []
    for paragraph in root.findall(".//w:p", NS):
        text = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
        text = text.replace(r"\n", "\n").strip()
        if text:
            result.append(text)
    return result


def main() -> None:
    lines = [
        "# MI 操作指南完整整理版",
        "",
        "來源：`data/sources/csp/MI操作手冊20251112.docx`",
        "",
        "本文件依原始手冊段落與功能標題整理，保留完整操作條件、限制、例外、話術、聯絡方式與補充教材。快速查詢請先看 [MI 維運操作入口](MI維運操作入口.md)。",
        "",
    ]
    chapter_started = False
    for text in paragraphs():
        if text in CHAPTERS:
            lines.extend([f"## {CHAPTERS[text]}", ""])
            chapter_started = True
            continue
        if text.startswith("【") and text.endswith("】"):
            lines.extend([f"### {text}", ""])
            continue
        if not chapter_started:
            lines.extend([text, ""])
            continue
        if text.startswith(("1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "10. ", "11. ", "12. ")):
            lines.extend([f"- {text}", ""])
        else:
            lines.extend([text, ""])
    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"完成：{len(paragraphs())} 段 -> {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
