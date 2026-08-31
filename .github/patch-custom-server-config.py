#!/usr/bin/env python3
"""Patch RustDesk custom server config:
ID/rendezvous server, public key, and API server (so the built client
connects to the self-hosted server out of the box).
Runs from any cwd; locates the repo by its own path.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONFIG_REPLACEMENTS = [
    ("rs-ny.rustdesk.com", "aly.low.bot.cd"),
    (
        "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=",
        "TT4A28var5o9r5IHQ5wxLzX0bUEHsEYEaVnJzJ3wuIE=",
    ),
]

API_REPLACEMENTS = [
    (
        '"https://admin.rustdesk.com".to_owned()',
        '"http://47.108.238.50:21114".to_owned()',
    ),
]


def patch(rel_path, pairs):
    path = ROOT / rel_path
    text = path.read_text(encoding="utf-8")
    ok = True
    for src, dst in pairs:
        if src in text:
            text = text.replace(src, dst)
            print(f"[patched] {rel_path}: {src!r} -> {dst!r}")
        else:
            print(f"[warn   ] {rel_path}: pattern NOT found: {src!r}")
            ok = False
    path.write_text(text, encoding="utf-8")
    return ok


status = True
status &= patch("libs/hbb_common/src/config.rs", CONFIG_REPLACEMENTS)
status &= patch("src/common.rs", API_REPLACEMENTS)
sys.exit(0 if status else 1)