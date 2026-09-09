#!/usr/bin/env python3
"""Linux delivery-only fix for the dynamic Online & Cloud tab.

The authoritative beta.85 shared source creates #tabHub dynamically from
HubAdapter.js. The inherited Linux fluid workspace was fixed to an eight-column
grid, so the ninth tab wrapped into a hidden second row. This adapter changes
only Linux presentation CSS; no shared Hub/Cloud/SYNC or tournament logic is
modified.
"""
from __future__ import annotations
from typing import Any

import chess_publisher_linux as cp

_APPLIED = False

_STYLE = r'''
<style id="cpLinuxOnlineHubTabVisibilityStyle">
/* beta.85 has nine primary tabs after HubAdapter creates Online & Cloud. */
#appWindow .tabs{
  grid-template-columns:repeat(9,minmax(0,1fr))!important;
}
#appWindow #tabHub{
  display:flex!important;
  visibility:visible!important;
  opacity:1!important;
  min-width:0!important;
}
</style>
'''.encode('utf-8')


def inject_online_hub_tab_visibility(data: bytes) -> bytes:
    if b'id="cpLinuxOnlineHubTabVisibilityStyle"' in data:
        return data
    head = data.lower().rfind(b'</head>')
    if head >= 0:
        return data[:head] + _STYLE + data[head:]
    return _STYLE + data


def apply() -> None:
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True
    original_serve = cp.Handler._serve_app

    def serve_app(self: cp.Handler) -> Any:
        original_text = self._text

        def hub_tab_text(status: int, data: bytes, content_type: str) -> Any:
            if content_type.lower().startswith('text/html'):
                data = inject_online_hub_tab_visibility(data)
            return original_text(status, data, content_type)

        self._text = hub_tab_text  # type: ignore[method-assign]
        try:
            return original_serve(self)
        finally:
            self._text = original_text  # type: ignore[method-assign]

    cp.Handler._serve_app = serve_app  # type: ignore[assignment]
