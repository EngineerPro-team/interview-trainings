#!/usr/bin/env python3
"""Assemble src/dsa-homework/data/*.json into problems.js."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HW = os.path.join(ROOT, "src", "dsa-homework")
DATA = os.path.join(HW, "data")
CATALOG = os.path.join(HW, "catalog.json")
OUT = os.path.join(HW, "problems.js")


def main() -> int:
    with open(CATALOG, encoding="utf-8") as f:
        catalog = json.load(f)

    parts = {}
    if os.path.isdir(DATA):
        for name in sorted(os.listdir(DATA)):
            if not name.endswith(".json") or name.startswith("_"):
                continue
            with open(os.path.join(DATA, name), encoding="utf-8") as f:
                payload = json.load(f)
            topics = payload if isinstance(payload, list) else payload.get("topics", [payload])
            for topic in topics:
                tid = topic["id"]
                parts[tid] = topic

    missing = []
    courses_out = []
    n_problems = 0
    n_complete = 0
    for course in catalog["courses"]:
        topics_out = []
        for meta in course["topics"]:
            tid = meta["id"]
            topic = parts.get(tid)
            if not topic:
                missing.append(tid)
                topic = {
                    "id": tid,
                    "title": meta["title"],
                    "lead": meta.get("lead", ""),
                    "problems": [],
                }
            else:
                topic = {
                    "id": tid,
                    "title": topic.get("title") or meta["title"],
                    "lead": topic.get("lead") or meta.get("lead", ""),
                    "problems": topic.get("problems", []),
                }
            for p in topic["problems"]:
                n_problems += 1
                codes = p.get("codes") or {}
                if all(codes.get(k) for k in ("cpp", "java", "python")):
                    n_complete += 1
            topics_out.append(topic)
        courses_out.append({
            "id": course["id"],
            "title": course["title"],
            "topics": topics_out,
        })

    blob = {
        "notice": catalog["notice"],
        "courses": courses_out,
    }
    js = "window.DSA_HW = " + json.dumps(blob, ensure_ascii=False, indent=2) + ";\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"[dsa-homework] wrote {os.path.relpath(OUT, ROOT)}  problems={n_problems} complete={n_complete}")
    if missing:
        print("[dsa-homework] missing topic files:", ", ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
