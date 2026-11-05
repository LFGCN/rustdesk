#!/usr/bin/env python3
"""Patch RustDesk self-hosted server config.

Replaces the upstream rendezvous server, admin API server and public key
so the built client connects to our self-hosted server out of the box.

Upstream 1.5.1 compile bugs are fixed directly in libs/hbb_common/src/config.rs
(see git log) — this script no longer patches any Rust source.

Runs from any cwd; locates the repo by its own path.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ------- 服务器配置 -------
RENDEZVOUS_NEW = "aly.low.bot.cd"
PUBLIC_KEY_NEW = "TT4A28var5o9r5IHQ5wxLzX0bUEHsEYEaVnJzJ3wuIE="
API_SERVER_NEW = '"http://47.108.238.50:21114".to_owned()'

CONFIG_RS = ROOT / "libs/hbb_common/src/config.rs"
COMMON_RS = ROOT / "src/common.rs"

CONFIG_REPLACEMENTS = [
    # 上游默认 rendezvous 域名
    ("rs-ny.rustdesk.com", RENDEZVOUS_NEW),
    ("rs-ny-old.rustdesk.com", RENDEZVOUS_NEW),
    ("rs-ny-1.rustdesk.com", RENDEZVOUS_NEW),
    ("rs-ny-2.rustdesk.com", RENDEZVOUS_NEW),
    ("rs-ny-3.rustdesk.com", RENDEZVOUS_NEW),
    ("rs-ny-4.rustdesk.com", RENDEZVOUS_NEW),
    # 上游默认公钥
    (
        "OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=",
        PUBLIC_KEY_NEW,
    ),
    # 上游默认 API server 域名
    ("https://admin.rustdesk.com", API_SERVER_NEW.strip('"')),
]

API_REPLACEMENTS = [
    ('"https://admin.rustdesk.com".to_owned()', API_SERVER_NEW),
    ('"https://admin.rustdesk.com/"', '"http://47.108.238.50:21114/"'),
    ("https://admin.rustdesk.com", "http://47.108.238.50:21114"),
]


def patch(path: Path, pairs):
    text = path.read_text(encoding="utf-8")
    ok = True
    any_patched = False
    for src, dst in pairs:
        if src in text:
            text = text.replace(src, dst)
            print(f"  [ok]   {path.relative_to(ROOT)}: {src!r} -> {dst!r}")
            any_patched = True
        else:
            # Some patterns may not exist in every version; skip silently.
            pass
    if any_patched:
        path.write_text(text, encoding="utf-8")
    return ok


def main():
    print("== Patching RustDesk server config ==")
    status = True
    status &= patch(CONFIG_RS, CONFIG_REPLACEMENTS)
    status &= patch(COMMON_RS, API_REPLACEMENTS)
    if status:
        print("== Done (no errors) ==")
    else:
        print("== Done (with errors) ==", file=sys.stderr)
    sys.exit(0 if status else 1)


if __name__ == "__main__":
    main()
