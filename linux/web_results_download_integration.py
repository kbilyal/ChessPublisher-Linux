#!/usr/bin/env python3
"""Linux Pairings web-result download adapter.

Protected ChessPublisher.html and pairing/TRF/engine cores remain byte-identical.
This adapter injects a read-only Cloud results downloader into Pairings. It
reconciles only the selected round's board.result values and never replaces
boards, players, pairing identity, or tournament settings.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any

import chess_publisher_linux as cp

_APPLIED = False
_SCRIPT_FILE = Path(__file__).with_name("web_results_download.js")
_STYLE = r'''
<style id="cpWebResultsDownloadStyle">
#pairings #cpDownloadWebResultsBtn{
  white-space:nowrap!important;
}
#pairings #cpDownloadWebResultsBtn:disabled{
  opacity:.62!important;
  cursor:wait!important;
}
</style>
'''.encode("utf-8")


def inject_web_results_download(data: bytes) -> bytes:
    if b'id="cpWebResultsDownloadScript"' in data:
        return data
    js = _SCRIPT_FILE.read_bytes()
    script = b'\n<script id="cpWebResultsDownloadScript">\n' + js + b'\n</script>\n'
    head = data.lower().rfind(b"</head>")
    if head >= 0:
        data = data[:head] + _STYLE + data[head:]
    else:
        data = _STYLE + data
    body = data.lower().rfind(b"</body>")
    if body >= 0:
        return data[:body] + script + data[body:]
    return data + script


def apply() -> None:
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True
    original_serve = cp.Handler._serve_app

    def serve_app(self: cp.Handler) -> Any:
        original_text = self._text

        def web_results_text(status: int, data: bytes, content_type: str) -> Any:
            if content_type.lower().startswith("text/html"):
                data = inject_web_results_download(data)
            return original_text(status, data, content_type)

        self._text = web_results_text  # type: ignore[method-assign]
        try:
            return original_serve(self)
        finally:
            self._text = original_text  # type: ignore[method-assign]

    cp.Handler._serve_app = serve_app  # type: ignore[assignment]
