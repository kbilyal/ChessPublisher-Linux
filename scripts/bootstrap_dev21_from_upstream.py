#!/usr/bin/env python3
"""Materialize current Linux runtime from immutable dev21 + dedicated deltas.

The upstream git tree does NOT contain the protected source snapshot used by the
Linux package. Never substitute the old root ChessPublisher.html. Exact source
may be supplied explicitly; hosted CI may materialize runtime-only with a clear
fail-closed state and run the same source-independent gates used by dev21.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import tarfile
import tempfile
import urllib.request
from pathlib import Path

UPSTREAM_REPO = "kbilyal/ChessPublisher"
UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"
ARCHIVE_URL = f"https://github.com/{UPSTREAM_REPO}/archive/{UPSTREAM_COMMIT}.tar.gz"
MAX_ARCHIVE_BYTES = 120 * 1024 * 1024
PROTECTED_ARCHIVE_NAME = "Chess-Publisher-v1.06.00-beta.34-protected-source.tar.gz"
PROTECTED_ARCHIVE_SHA256 = "19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff"

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
    req = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "ChessPublisher-Linux-materializer/3"})
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
        tf.extractall(target, members=members, filter="data")
    roots = [p for p in target.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise RuntimeError("Unexpected upstream archive layout")
    return roots[0]


def copy_tree(src: Path, dst: Path, *, replace: bool = False) -> None:
    if replace and dst.exists():
        shutil.rmtree(dst)
    if not src.is_dir():
        return
    shutil.copytree(src, dst, dirs_exist_ok=not replace,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))


def verify_source_root(source_root: Path, output: Path, manifest: dict) -> None:
    target = output / "source"
    if target.exists():
        shutil.rmtree(target)
    for rel in PROTECTED_PATHS:
        src = source_root / rel
        if not src.is_file():
            raise RuntimeError(f"Exact protected source is incomplete: missing {rel}")
        expected = manifest["files"][rel]["sha256"]
        actual = sha256(src)
        if actual != expected:
            raise RuntimeError(f"Protected source hash mismatch for {rel}: {actual} != {expected}")
        dst = target / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def extract_protected_archive(archive: Path, output: Path, manifest: dict) -> None:
    actual_archive = sha256(archive)
    if actual_archive != PROTECTED_ARCHIVE_SHA256:
        raise RuntimeError(
            f"Protected source archive hash mismatch: {actual_archive} != {PROTECTED_ARCHIVE_SHA256}"
        )
    with tempfile.TemporaryDirectory(prefix="cp-protected-source-") as td:
        root = Path(td)
        with tarfile.open(archive, mode="r:gz") as tf:
            members = []
            for member in tf.getmembers():
                p = Path(member.name)
                if p.is_absolute() or ".." in p.parts or member.issym() or member.islnk():
                    raise RuntimeError("Unsafe path in protected source archive")
                members.append(member)
            tf.extractall(root, members=members, filter="data")
        source_root = root / "source"
        if not source_root.is_dir():
            raise RuntimeError("Protected source archive has no source/ directory")
        verify_source_root(source_root, output, manifest)


def locate_exact_source(repo_root: Path, explicit_archive: Path | None, explicit_root: Path | None):
    if explicit_root:
        return ("root", explicit_root.expanduser().resolve())
    candidates = []
    if explicit_archive:
        candidates.append(explicit_archive)
    env_archive = os.environ.get("CP_PROTECTED_SOURCE_ARCHIVE", "").strip()
    if env_archive:
        candidates.append(Path(env_archive))
    candidates.extend([
        repo_root / PROTECTED_ARCHIVE_NAME,
        repo_root.parent / PROTECTED_ARCHIVE_NAME,
        Path.home() / "Downloads" / PROTECTED_ARCHIVE_NAME,
        Path.home() / "Изтегляния" / PROTECTED_ARCHIVE_NAME,
    ])
    for item in candidates:
        path = item.expanduser().resolve()
        if path.is_file():
            return ("archive", path)
    return (None, None)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=repo_root / ".runtime" / "materialized")
    parser.add_argument("--source-archive", type=Path, help="exact protected recovery archive")
    parser.add_argument("--source-root", type=Path, help="directory containing exact protected paths")
    parser.add_argument(
        "--allow-source-unavailable", action="store_true",
        help="materialize runtime only; never substitute upstream root protected files",
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
        copy_tree(upstream / "linux-port" / "linux", output / "linux", replace=True)
        copy_tree(upstream / "linux-port" / "packaging", output / "packaging", replace=True)
        copy_tree(upstream / "linux-port" / "ci", output / "ci", replace=True)
        copy_tree(upstream / "linux-port" / "tests", output / "tests", replace=True)
        fide_seed = upstream / "fide"
        if fide_seed.is_dir():
            copy_tree(fide_seed, output / "fide-cache", replace=True)

    # Never copy protected paths from the upstream git root: its HTML is the old
    # public repository copy and does not match the pinned protected snapshot.
    source_kind, source_location = locate_exact_source(repo_root, args.source_archive, args.source_root)
    protected_verified = False
    protected_origin = "unavailable"
    if source_kind == "archive":
        extract_protected_archive(source_location, output, manifest)
        protected_verified = True
        protected_origin = f"archive:{source_location.name}"
    elif source_kind == "root":
        verify_source_root(source_location, output, manifest)
        protected_verified = True
        protected_origin = f"root:{source_location}"
    elif not args.allow_source_unavailable:
        raise RuntimeError(
            "Exact protected source is unavailable. Supply --source-archive/--source-root or "
            "CP_PROTECTED_SOURCE_ARCHIVE. The old upstream root source is forbidden."
        )

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
        "protectedSourceVerified": protected_verified,
        "protectedSourceOrigin": protected_origin,
        "protectedArchiveSha256": PROTECTED_ARCHIVE_SHA256,
        "oldUpstreamRootSourceAllowed": False,
        "overlay": ["linux/", "tests/", "scripts/", "packaging/ when present"],
    }
    (output / "MATERIALIZED_STATE.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"Materialized {state['version']} runtime at {output}")
    print(f"Baseline: {UPSTREAM_REPO}@{UPSTREAM_COMMIT}")
    print(f"Protected source verified: {protected_verified} ({protected_origin})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
