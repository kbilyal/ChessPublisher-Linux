#!/usr/bin/env python3
"""Inject Linux-only unified Cloud synchronization UI/policy.

This adapter does not modify protected ChessPublisher.html or Cloud/Hub adapters.
It is loaded after the existing directional sync and results-only adapters.
"""
from __future__ import annotations
from typing import Any

import chess_publisher_linux as cp

_APPLIED = False
_SCRIPT = b'<script src="/linux/cloud_unified_sync.js"></script>\n'


def inject_unified_cloud_sync(data: bytes) -> bytes:
    if _SCRIPT in data:
        return data
    marker = b'</body>'
    pos = data.lower().rfind(marker)
    if pos >= 0:
        return data[:pos] + _SCRIPT + data[pos:]
    return data + _SCRIPT


def apply() -> None:
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True
    original_serve = cp.Handler._serve_app

    def serve_app(self: cp.Handler) -> Any:
        original_text = self._text

        def unified_text(status: int, data: bytes, content_type: str) -> Any:
            if content_type.lower().startswith('text/html'):
                data = inject_unified_cloud_sync(data)
            return original_text(status, data, content_type)

        self._text = unified_text  # type: ignore[method-assign]
        try:
            return original_serve(self)
        finally:
            self._text = original_text  # type: ignore[method-assign]

    cp.Handler._serve_app = serve_app  # type: ignore[assignment]
