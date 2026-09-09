#!/usr/bin/env python3
"""Linux delivery adapter for the exact current shared browser source.

No tournament/business logic lives here. It only exposes source-root assets and
loads the same WebView/Hub/Cloud stack, in the same order, as the Windows shell.
"""
from __future__ import annotations
import mimetypes, re, urllib.parse
from pathlib import Path
from typing import Any
import chess_publisher_linux as cp

_APPLIED=False
_STACK = b'''\n<!-- CP beta.85 shared WebView stack; Linux transport only -->
<script src="/linux/LinuxWebViewShim.js"></script>
<script src="/source/webview/WebViewAdapter.js"></script>
<script src="/source/hub/client/hub-snapshot.js"></script>
<script src="/source/hub/client/hub-api-client.js"></script>
<script src="/source/webview/HubAdapter.js"></script>
<script src="/source/cloud/client/cloud-workspace-api.js"></script>
<script src="/source/webview/CloudWorkspaceAdapter.js"></script>
<script src="/source/webview/CloudWorkspaceRedesign.js"></script>
<script>document.documentElement.dataset.chesspublisherLinuxBuild='1.06.00-beta.85';</script>
'''
_BUILD_MARKER_RE=re.compile(rb"<script>\s*document\.documentElement\.dataset\.chesspublisherLinuxBuild='[^']*';\s*</script>")
_OLD_TAGS=(
 b'<script src="/linux/LinuxWebViewShim.js"></script>',
 b'<script src="/source/webview/WebViewAdapter.js"></script>',
 b'<script src="/source/hub/client/hub-snapshot.js"></script>',
 b'<script src="/source/hub/client/hub-api-client.js"></script>',
 b'<script src="/source/webview/HubAdapter.js"></script>',
 b'<script src="/source/cloud/client/cloud-workspace-api.js"></script>',
 b'<script src="/source/webview/CloudWorkspaceAdapter.js"></script>',
 b'<script src="/source/webview/CloudWorkspaceRedesign.js"></script>',
)

def _transform_html(data: bytes) -> bytes:
    if b'CP beta.85 shared WebView stack' in data: return data
    for tag in _OLD_TAGS: data=data.replace(tag,b'')
    data=_BUILD_MARKER_RE.sub(b'',data)
    pos=data.lower().rfind(b'</body>')
    return data[:pos]+_STACK+data[pos:] if pos>=0 else data+_STACK

def _serve_root_asset(self: cp.Handler,path: str) -> bool:
    if '/' in path.lstrip('/'):
        return False
    name=urllib.parse.unquote(path.lstrip('/'))
    if not (name.startswith('ChessPublisher-') and name.endswith('.js')) and name not in {'USER-MANUAL-EN.html'}:
        return False
    root=self.engine.source_root.resolve();candidate=(root/name).resolve()
    if root not in candidate.parents or not candidate.is_file():
        return False
    mime=mimetypes.guess_type(candidate.name)[0] or 'application/octet-stream'
    self._text(200,candidate.read_bytes(),mime+('; charset=utf-8' if mime.startswith(('text/','application/javascript')) else ''))
    return True

def apply() -> None:
    global _APPLIED
    if _APPLIED:return
    _APPLIED=True
    original_serve=cp.Handler._serve_app
    def serve_app(self: cp.Handler)->Any:
        original_text=self._text
        def shared_text(status:int,data:bytes,content_type:str)->Any:
            if content_type.lower().startswith('text/html'): data=_transform_html(data)
            return original_text(status,data,content_type)
        self._text=shared_text  # type: ignore[method-assign]
        try:return original_serve(self)
        finally:self._text=original_text  # type: ignore[method-assign]
    cp.Handler._serve_app=serve_app  # type: ignore[assignment]
    original_get=cp.Handler.do_GET
    def do_get(self: cp.Handler)->None:
        path=urllib.parse.urlsplit(self.path).path
        if _serve_root_asset(self,path):return
        return original_get(self)
    cp.Handler.do_GET=do_get  # type: ignore[assignment]
