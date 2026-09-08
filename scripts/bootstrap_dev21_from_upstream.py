#!/usr/bin/env python3
"""Materialize the current Linux runtime from the immutable dev21 baseline.

The dedicated repository stores Linux deltas and handoff metadata.  This tool
reconstructs the exact pre-split dev21 runtime into a separate output folder,
verifies protected source hashes, then overlays the current repository's Linux
files/tests/scripts.  It never overwrites the repository checkout itself.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Iterable

UPSTREAM_REPO = "kbilyal/ChessPublisher"
UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"
ARCHIVE_URL = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
MAX_ARCHIVE_BYTES = 120 * 1024 * 1024

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
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download() -> bytes:
    req = urllib.request.Request(
        ARCHIVE_URL,
        headers={"User-Agent": "ChessPublisher-Linux-materializer/2"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(MAX_ARCHIVE_BYTES + 1)
    if len(data) > MAX_ARCHIVE_BYTES:
        raise RuntimeError("Upstream archive exceeded safety limit")
    return data


def safe_extract(data: bytes, target: Path) -> Path:
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        members = []
        for member in tf.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or member.issym() or member.islnk():
                raise RuntimeError("Unsafe path in upstream archive")
            members.append(member)
        tf.extractall(target, members=members)
    roots = [p for p in target.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise RuntimeError("Unexpected upstream archive layout")
    return roots[0]


def copy_tree(src: Path, dst: Path, *, replace: bool = False) -> None:
    if replace and dst.exists():
        shutil.rmtree(dst)
    if not src.is_dir():
        return
    shutil.copytree(
        src,
        dst,
        dirs_exist_ok=not replace,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )


def copy_files(paths: Iterable[str], upstream: Path, output: Path, manifest: dict) -> None:
    source_root = output / "source"
    for rel in paths:
        src = upstream / rel
        dst = source_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        expected = manifest["files"][rel]["sha256"]
        actual = sha256(dst)
        if actual != expected:
            raise RuntimeError(
                f"Protected source hash mismatch for {rel}: {actual} != {expected}"
            )


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=repo_root / ".runtime" / "materialized",
        help="separate runtime directory to create",
    )
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    if output == repo_root.resolve() or (repo_root.resolve() in output.parents and output.name == "linux"):
        raise RuntimeError("Refusing to materialize over the repository source tree")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((repo_root / "source_manifest.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="cp-linux-upstream-") as td:
        upstream = safe_extract(download(), Path(td))

        # Exact tested dev21 baseline.
        copy_tree(upstream / "linux-port" / "linux", output / "linux", replace=True)
        copy_tree(upstream / "linux-port" / "packaging", output / "packaging", replace=True)
        copy_tree(upstream / "linux-port" / "ci", output / "ci", replace=True)
        copy_tree(upstream / "linux-port" / "tests", output / "tests", replace=True)
        copy_files(PROTECTED_PATHS, upstream, output, manifest)

        # Optional offline seeds from the same immutable upstream snapshot.
        fide_seed = upstream / "fide"
        if fide_seed.is_dir():
            copy_tree(fide_seed, output / "fide-cache", replace=True)

    # Overlay current dedicated-repository deltas. This is what makes a new
    # agent materialize the current dev22+ state instead of reverting to dev21.
    copy_tree(repo_root / "linux", output / "linux")
    copy_tree(repo_root / "tests", output / "tests")
    copy_tree(repo_root / "scripts", output / "scripts")
    if (repo_root / "packaging").is_dir():
        copy_tree(repo_root / "packaging", output / "packaging")

    shutil.copy2(repo_root / "source_manifest.json", output / "source_manifest.json")
    if (repo_root / "VERSION").is_file():
        shutil.copy2(repo_root / "VERSION", output / "VERSION")

    state = {
        "upstreamRepository": UPSTREAM_REPO,
        "upstreamCommit": UPSTREAM_COMMIT,
        "dedicatedRepository": "kbilyal/ChessPublisher-Linux",
        "version": (repo_root / "VERSION").read_text(encoding="utf-8").strip(),
        "protectedSourceVerified": True,
        "overlay": ["linux/", "tests/", "scripts/", "packaging/ when present"],
    }
    (output / "MATERIALIZED_STATE.json").write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Materialized {state['version']} runtime at {output}")
    print(f"Baseline: {UPSTREAM_REPO}@{UPSTREAM_COMMIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
