#!/usr/bin/env python3
"""Check whether source PDFs are new or changed since they were organized."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="也列出已整理的來源")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source_dir = root / "data" / "sources"
    manifest_path = source_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    counts = {"organized": 0, "changed": 0, "new": 0}
    for source in sorted(source_dir.glob("*.pdf")):
        name = source.name
        current = sha256(source)
        record = manifest.get(name)
        if record is None:
            status = "尚未整理"
            counts["new"] += 1
        elif current != record["sha256"]:
            status = "內容已變更，需重新整理"
            counts["changed"] += 1
        else:
            status = "已整理"
            counts["organized"] += 1

        if args.all or status != "已整理":
            outputs = "、".join(record["organized_in"]) if record else "（尚無對應文件）"
            print(f"{status}: {name} -> {outputs}")

    print(
        f"\n總計：已整理 {counts['organized']}、"
        f"內容已變更 {counts['changed']}、尚未整理 {counts['new']}"
    )
    return 0 if not (counts["changed"] or counts["new"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
