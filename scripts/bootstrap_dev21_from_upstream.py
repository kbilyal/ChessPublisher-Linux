#!/usr/bin/env python3
"""Reconstruct the exact Linux dev21 baseline from the pre-split repository.

This is a continuity/recovery tool.  It downloads one immutable upstream commit,
extracts only the Linux runtime/packaging and protected source files, and then
verifies protected source SHA256 values from source_manifest.json.
"""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

UPSTREAM_REPO = "kbilyal/ChessPublisher"
UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"
ARCHIVE_URL = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
MAX_ARCHIVE_BYTES = 80 * 1024 * 1024

PROTECTED_PATHS = (
    "ChessPublisher.html",
    "cloud/client/cloud-workspace-api.js",
    "hub/client/hub-api-client.js",
    "hub/client/hub-snapshot.js",
    "webview/CloudWorkspaceAdapter.js",
    "webview/HubAdapter.js",
    "webview/WebViewAdapter.js",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> bytes:
    req = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "ChessPublisher-Linux-bootstrap/1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(MAX_ARCHIVE_BYTES + 1)
    if len(data) > MAX_ARCHIVE_BYTES:
        raise RuntimeError("Upstream archive exceeded safety limit")
    return data


def safe_extract(data: bytes, target: Path) -> Path:
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        members = []
        for member in tf.getmembers():
            p = Path(member.name)
            if p.is_absolute() or ".." in p.parts or member.issym() or member.islnk():
                raise RuntimeError("Unsafe path in upstream archive")
            members.append(member)
        tf.extractall(target, members=members)
    roots = [p for p in target.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise RuntimeError("Unexpected upstream archive layout")
    return roots[0]


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = json.loads((repo_root / "source_manifest.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="cp-linux-upstream-") as td:
        upstream = safe_extract(download(), Path(td))
        copy_tree(upstream / "linux-port" / "linux", repo_root / "linux")
        copy_tree(upstream / "linux-port" / "packaging", repo_root / "packaging")

        protected_root = repo_root / "protected-source"
        protected_root.mkdir(parents=True, exist_ok=True)
        for rel in PROTECTED_PATHS:
            src = upstream / rel
            dst = protected_root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            expected = manifest["files"][rel]["sha256"]
            actual = sha256(dst)
            if actual != expected:
                raise RuntimeError(f"Protected source hash mismatch for {rel}: {actual} != {expected}")

    print(f"Recovered Linux dev21 from {UPSTREAM_REPO}@{UPSTREAM_COMMIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
