#!/usr/bin/env python3
"""Select the current Chess-Publisher Linux runtime instance safely.

A same-version point fix may be installed while an older LocalEngine process is
still listening on the default port. The upstream launcher reused any process
that identified itself only as Chess-Publisher, which could reopen stale UI
assets after a successful reinstall. This platform-only adapter probes a
current delivery marker and reuses only an identical delivery. Otherwise it
selects the next free/current port without killing an existing process.
"""
from __future__ import annotations
import json
import socket
import sys
import urllib.request
from typing import Literal

from build_info import DELIVERY_REVISION

_APPLIED = False
_SCAN_PORTS = 24
_MARKER = f"data-chesspublisher-linux-delivery=\"{DELIVERY_REVISION}\"".encode("utf-8")


def _explicit_port(argv: list[str] | None = None) -> bool:
    args = list(sys.argv[1:] if argv is None else argv)
    return any(arg == "--port" or arg.startswith("--port=") for arg in args)


def _socket_open(port: int, timeout: float = 0.12) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=timeout):
            return True
    except OSError:
        return False


def _probe(port: int) -> Literal["free", "current", "stale", "occupied"]:
    if not _socket_open(port):
        return "free"
    base = f"http://127.0.0.1:{int(port)}/"
    try:
        with urllib.request.urlopen(base + "health", timeout=0.45) as resp:
            health = json.loads(resp.read(4096).decode("utf-8", "replace"))
    except Exception:
        return "occupied"
    if health.get("service") != "Chess-Publisher Linux LocalEngine":
        return "occupied"
    try:
        with urllib.request.urlopen(base, timeout=0.75) as resp:
            html = resp.read(2 * 1024 * 1024)
    except Exception:
        return "stale"
    return "current" if _MARKER in html else "stale"


def select_default_port(base_port: int, scan_ports: int = _SCAN_PORTS) -> tuple[int, str]:
    """Return (port, state). Prefer a matching live runtime, else first free port."""
    first_free: int | None = None
    stale_seen = False
    for port in range(int(base_port), int(base_port) + max(1, int(scan_ports))):
        state = _probe(port)
        if state == "current":
            return port, "current"
        if state == "stale":
            stale_seen = True
        elif state == "free" and first_free is None:
            first_free = port
    if first_free is not None:
        return first_free, "stale-bypassed" if stale_seen else "free"
    raise RuntimeError(f"No free Chess-Publisher LocalEngine port found in {base_port}-{base_port + max(1, int(scan_ports)) - 1}.")


def apply() -> None:
    import chess_publisher_linux as cp
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True
    if _explicit_port():
        return
    port, state = select_default_port(cp.DEFAULT_PORT)
    cp.DEFAULT_PORT = port
    cp.CP_RUNTIME_INSTANCE_SELECTION = {"deliveryRevision": DELIVERY_REVISION, "port": port, "state": state}
