#!/usr/bin/env python3
"""Guard a demo HTML page: no external resources, complete document, size cap."""
from __future__ import annotations

import re
import sys

EXTERNAL_ATTR = re.compile(
    r"""(?ix)
    <(?:script|img|link|iframe|source|video|audio|embed|object|form)\b
    [^>]*?
    \b(?:src|srcset|href|data|action)\s*=\s*
    (?:
        ["']\s*(?:https?:)?//   # quoted http(s) or protocol-relative
      | (?!["'])(?:https?:)?// # unquoted
    )
    """
)

CSS_EXTERNAL = re.compile(
    r"""(?ix)
    (?:
        url\(\s*["']?(?:https?:)?//
      | @import\s+(?:url\()?["']?(?:https?:)?//
    )
    """
)

NETWORK_JS = re.compile(
    r"""(?ix)
    \bfetch\s*\(
  | XMLHttpRequest
  | navigator\.sendBeacon
  | WebSocket\s*\(
  | \bimport\s*\(
    """
)


def check_html(html: str, max_lines: int = 320) -> list[str]:
    reasons: list[str] = []
    if "</html>" not in html.lower():
        reasons.append("page must contain a closing </html>")
    lines = html.count("\n") + 1
    if lines > max_lines:
        reasons.append(f"page is too long ({lines} lines; keep under ~300)")
    if EXTERNAL_ATTR.search(html):
        reasons.append(
            "external src/href/srcset/data/action "
            "(script/img/link/iframe/source/video/audio/embed/object/form) is not allowed"
        )
    if CSS_EXTERNAL.search(html):
        reasons.append("external CSS url()/ @import is not allowed")
    if NETWORK_JS.search(html):
        reasons.append("network calls (fetch/XHR/WebSocket/import) are not allowed")
    return reasons


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: guard_html.py <file.html>", file=sys.stderr)
        return 2
    html = open(argv[0], encoding="utf-8", errors="replace").read()
    reasons = check_html(html)
    if reasons:
        print("; ".join(reasons))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
