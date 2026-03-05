#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Merge volumes/chapters into a single Markdown, with realism-first cleanup.

Design goals:
- Deterministic order (by chapter number parsed from filenames like "第三十八章：...md")
- Keep only narrative (truncate before meta sections like "叙事分析")
- Normalize headings: H1 book title, H2 volumes, H3 chapters
- Normalize scene breaks: "***" -> "---" and bold first line after break (if suitable)
- Apply small, safe de-mystification string replacements (idempotent)
- UTF-8 WITHOUT BOM output

This script intentionally does NOT try to do heavy semantic rewrites.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(r"D:\_Progs\01Center\ASTO\小说故事\《逻辑裂缝3.0》")
OUT = ROOT / "《逻辑裂缝3.0》_全书定稿_现实主义清洗.md"

VOLUMES = [
    "卷一：疼痛的接口",
    "卷二：逻辑的灰度",
    "卷三：系统的反噬",
    "卷四：带着错误运行",
]

CN_DIGIT = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn_to_int(s: str) -> int:
    s = s.strip()
    if not s:
        raise ValueError("empty chinese numeral")
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十", 1)
        tens = CN_DIGIT[a] if a else 1
        ones = CN_DIGIT[b] if b else 0
        return tens * 10 + ones
    # handle 1-9
    if s in CN_DIGIT:
        return CN_DIGIT[s]
    raise ValueError(f"unsupported chinese numeral: {s}")


def parse_chapter_no_from_filename(name: str) -> int:
    # e.g. "第三十八章：手动拥堵.md" -> 38
    m = re.match(r"^第(?P<num>[^章]+)章", name)
    if not m:
        raise ValueError(f"cannot parse chapter prefix from: {name}")
    return cn_to_int(m.group("num"))


TRUNCATE_MARKERS = [
    "叙事分析",
    "接下来的计划",
]

SAFE_REPLACEMENTS: list[tuple[str, str]] = [
    # name consistency
    ("小陈", "小马"),
    ("Ghost", "老余"),
    ("Jack", "Jax"),
    # de-tech a few high-signal terms (avoid sci-fi tone)
    ("分布式反击", "手动拥堵"),
    ("两小时的宕机", "两小时的卡顿"),
    ("宕机", "卡顿"),
    ("反向链接", "倒查"),
    ("宇宙缝隙", "世界死角"),
]


@dataclass
class Chapter:
    volume: str
    no: int
    path: Path


def read_text(path: Path) -> str:
    # tolerate BOM
    data = path.read_bytes()
    # decode as UTF-8 with optional BOM
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig")
    return data.decode("utf-8")


def truncate_meta(text: str) -> str:
    # remove anything after the first marker line (inclusive)
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        for mk in TRUNCATE_MARKERS:
            if mk in ln:
                return "\n".join(lines[:i]).rstrip() + "\n"
    return text


def normalize_scene_breaks(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    bold_next = False

    def should_bold(line: str) -> bool:
        s = line.strip()
        if not s:
            return False
        if s.startswith("#"):
            return False
        if s.startswith("**") and s.endswith("**"):
            return False
        if s.startswith("---"):
            return False
        return True

    for ln in lines:
        if ln.strip() == "***":
            out.append("---")
            bold_next = True
            continue
        if bold_next and should_bold(ln):
            out.append(f"**{ln.strip()}**")
            bold_next = False
            continue
        out.append(ln)
        if ln.strip():
            # only keep bold_next true across blank lines
            pass
    return "\n".join(out)


def normalize_chapter_heading(text: str) -> tuple[str, str]:
    """Return (chapter_title, body_without_h1)."""
    lines = text.splitlines()
    # find first markdown heading line
    title = None
    start_idx = 0
    for i, ln in enumerate(lines):
        m = re.match(r"^#\s+(.*)$", ln.strip())
        if m:
            title = m.group(1).strip()
            start_idx = i + 1
            break
    if not title:
        # fallback: filename will be used by caller
        title = ""
        start_idx = 0
    body = "\n".join(lines[start_idx:]).lstrip("\n")
    return title, body


def apply_safe_replacements(text: str) -> str:
    for a, b in SAFE_REPLACEMENTS:
        text = text.replace(a, b)
    return text


def collect_chapters() -> list[Chapter]:
    chapters: list[Chapter] = []
    for vol in VOLUMES:
        d = ROOT / vol
        if not d.exists():
            raise SystemExit(f"Missing volume dir: {d}")
        for p in d.glob("*.md"):
            try:
                no = parse_chapter_no_from_filename(p.name)
            except Exception:
                continue
            chapters.append(Chapter(volume=vol, no=no, path=p))
    # sort by volume order then number
    vol_index = {v: i for i, v in enumerate(VOLUMES)}
    chapters.sort(key=lambda c: (vol_index.get(c.volume, 99), c.no))
    return chapters


def main() -> None:
    chapters = collect_chapters()

    parts: list[str] = []
    parts.append("# 《逻辑裂缝3.0》\n")

    current_vol = None
    for ch in chapters:
        if ch.volume != current_vol:
            current_vol = ch.volume
            parts.append(f"## {current_vol}\n")

        raw = read_text(ch.path)
        raw = raw.replace("\r\n", "\n").replace("\r", "\n")
        raw = truncate_meta(raw)
        raw = apply_safe_replacements(raw)

        title, body = normalize_chapter_heading(raw)
        if not title:
            # fallback to filename without extension
            title = ch.path.stem

        body = normalize_scene_breaks(body)
        body = body.strip("\n")

        parts.append(f"### {title}\n")
        if body:
            parts.append(body + "\n")
        else:
            parts.append("\n")

    # optional: append afterword (kept as a separate file so edits won't be overwritten)
    afterword_path = ROOT / "后记：免费疗愈室.md"
    if afterword_path.exists():
        raw = read_text(afterword_path)
        raw = raw.replace("\r\n", "\n").replace("\r", "\n")
        raw = apply_safe_replacements(raw)
        title, body = normalize_chapter_heading(raw)
        if not title:
            title = afterword_path.stem
        body = normalize_scene_breaks(body)
        body = body.strip("\n")

        parts.append(f"## {title}\n")
        if body:
            parts.append(body + "\n")
        else:
            parts.append("\n")

    out_text = "\n".join(parts).rstrip() + "\n"
    OUT.write_text(out_text, encoding="utf-8", newline="\n")
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    main()
