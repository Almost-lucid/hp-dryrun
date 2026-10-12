#!/usr/bin/env python3
"""Quick local tests for tools/guard_html.py outside-source checks."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from guard_html import check_html

OK = """<!doctype html><html><head><title>Ok</title>
<meta name="description" content="x">
<style>body{background:#fff}</style></head>
<body><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="">
<script>const x=1;</script></body></html>
"""

CASES = [
    ("missing close", OK.replace("</html>", ""), "closing </html>"),
    ("quoted script src", '<!doctype html><html><body><script src="https://x.com/a.js"></script></body></html>', "external"),
    ("unquoted script src", "<!doctype html><html><body><script src=https://x.com/a.js></script></body></html>", "external"),
    ("protocol-relative img", '<!doctype html><html><body><img src="//cdn.example/a.png"></body></html>', "external"),
    ("srcset", '<!doctype html><html><body><img srcset="https://x.com/a.png 1x"></body></html>', "external"),
    ("link href", '<!doctype html><html><head><link rel="stylesheet" href="https://x.com/a.css"></head><body></body></html>', "external"),
    ("object data", '<!doctype html><html><body><object data="https://x.com/a.svg"></object></body></html>', "external"),
    ("embed src", '<!doctype html><html><body><embed src="https://x.com/a.swf"></body></html>', "external"),
    ("video src", '<!doctype html><html><body><video src="https://x.com/a.mp4"></video></body></html>', "external"),
    ("audio src", '<!doctype html><html><body><audio src="https://x.com/a.mp3"></audio></body></html>', "external"),
    ("source src", '<!doctype html><html><body><video><source src="https://x.com/a.mp4"></video></body></html>', "external"),
    ("iframe src", '<!doctype html><html><body><iframe src="https://x.com"></iframe></body></html>', "external"),
    ("form action", '<!doctype html><html><body><form action="https://x.com"></form></body></html>', "external"),
    ("css url", "<!doctype html><html><head><style>body{background:url(https://x.com/a.png)}</style></head><body></body></html>", "CSS"),
    ("css url protocol-relative", "<!doctype html><html><head><style>body{background:url(//x.com/a.png)}</style></head><body></body></html>", "CSS"),
    ("css @import", "<!doctype html><html><head><style>@import url('https://x.com/a.css');</style></head><body></body></html>", "CSS"),
    ("fetch", "<!doctype html><html><body><script>fetch('https://x.com')</script></body></html>", "network"),
    ("xhr", "<!doctype html><html><body><script>new XMLHttpRequest()</script></body></html>", "network"),
    ("websocket", "<!doctype html><html><body><script>new WebSocket('wss://x')</script></body></html>", "network"),
    ("ok page", OK, None),
]

failed = 0
for name, html, expect in CASES:
    reasons = check_html(html)
    joined = "; ".join(reasons)
    if expect is None:
        if reasons:
            print(f"FAIL {name}: expected OK, got {joined!r}")
            failed += 1
        else:
            print(f"PASS {name}")
    else:
        if not reasons or expect.lower() not in joined.lower():
            print(f"FAIL {name}: expected reason containing {expect!r}, got {joined!r}")
            failed += 1
        else:
            print(f"PASS {name}")

raise SystemExit(failed)
