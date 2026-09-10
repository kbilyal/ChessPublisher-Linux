#!/usr/bin/env python3
"""Linux presentation-only repair for the beta.85 Tournament Setup grid.

The authoritative beta.70 compliance module dynamically inserts
#cpBeta70LongEventBox immediately after the Rating Type control. That element is
one direct child inside a four-column form grid, so without an explicit span it
consumes one grid cell and shifts every following label/control pair. This
adapter changes only Linux delivery CSS: the existing long-event help panel gets
its own full-width grid row. Shared rating policy and tournament data remain
untouched.
"""
from __future__ import annotations
from typing import Any

import chess_publisher_linux as cp

_APPLIED = False

_STYLE = r'''
<style id="cpLinuxTournamentSetupLayoutStyle">
/* Keep the dynamically injected beta.70 long-event control from shifting the
   remaining four-column Tournament Setup fields. */
#appWindow #main .tournament-general-grid > #cpBeta70LongEventBox{
  grid-column:1 / -1!important;
  min-width:0!important;
  width:auto!important;
  box-sizing:border-box!important;
  justify-self:stretch!important;
  margin:6px 0!important;
}
</style>
'''.encode('utf-8')


def inject_tournament_setup_layout(data: bytes) -> bytes:
    if b'id="cpLinuxTournamentSetupLayoutStyle"' in data:
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

        def layout_text(status: int, data: bytes, content_type: str) -> Any:
            if content_type.lower().startswith('text/html'):
                data = inject_tournament_setup_layout(data)
            return original_text(status, data, content_type)

        self._text = layout_text  # type: ignore[method-assign]
        try:
            return original_serve(self)
        finally:
            self._text = original_text  # type: ignore[method-assign]

    cp.Handler._serve_app = serve_app  # type: ignore[assignment]
