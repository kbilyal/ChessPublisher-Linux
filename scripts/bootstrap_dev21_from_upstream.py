#!/usr/bin/env python3
"""Materialize the Linux runtime around the exact beta.81 shared source.

The immutable upstream Linux platform baseline is used only for platform/runtime
files. Shared Chess-Publisher tournament/business source is accepted only from
the exact beta.81 source archive/root pinned by source_manifest.json.
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
MAX_UPSTREAM_ARCHIVE_BYTES = 120 * 1024 * 1024
MAX_SHARED_ARCHIVE_BYTES = 4 * 1024 * 1024
MAX_SHARED_EXTRACTED_BYTES = 16 * 1024 * 1024
SHARED_ARCHIVE_NAME = "Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz"
SHARED_ARCHIVE_SHA256 = "b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_upstream() -> bytes:
    req = urllib.request.Request(ARCHIVE_URL, headers={"User-Agent": "ChessPublisher-Linux-materializer/4"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(MAX_UPSTREAM_ARCHIVE_BYTES + 1)
    if len(data) > MAX_UPSTREAM_ARCHIVE_BYTES:
        raise RuntimeError("Upstream archive exceeded safety limit")
    return data


def safe_extract_upstream(data: bytes, target: Path) -> Path:
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


def source_specs(manifest: dict) -> dict:
    specs = manifest.get("runtimeSharedFiles") or manifest.get("files")
    if not isinstance(specs, dict) or not specs:
        raise RuntimeError("Shared source manifest has no runtimeSharedFiles/files set")
    return specs


def verify_source_root(source_root: Path, manifest: dict) -> list[dict]:
    root = source_root.resolve()
    checked = []
    for rel, spec in source_specs(manifest).items():
        src = (root / rel).resolve()
        if root not in src.parents and src != root:
            raise RuntimeError(f"Unsafe shared source path: {rel}")
        if not src.is_file():
            raise RuntimeError(f"Exact beta.81 shared source is incomplete: missing {rel}")
        actual_size = src.stat().st_size
        expected_size = int(spec.get("size") or 0)
        if actual_size != expected_size:
            raise RuntimeError(f"Shared source size mismatch for {rel}: {actual_size} != {expected_size}")
        actual = sha256(src)
        expected = str(spec.get("sha256") or "").lower()
        if actual != expected:
            raise RuntimeError(f"Shared source hash mismatch for {rel}: {actual} != {expected}")
        checked.append({"path": rel, "size": actual_size, "sha256": actual})
    version = (root / "VERSION.txt").read_text(encoding="utf-8").strip()
    expected_version = str(manifest.get("baseRelease") or "").removeprefix("v")
    if version != expected_version:
        raise RuntimeError(f"Shared source VERSION.txt mismatch: {version} != {expected_version}")
    return checked


def activate_source(source_root: Path, output: Path, manifest: dict) -> list[dict]:
    checked = verify_source_root(source_root, manifest)
    target = output / "source"
    copy_tree(source_root, target, replace=True)
    verify_source_root(target, manifest)
    return checked


def safe_extract_shared(archive: Path, target: Path) -> Path:
    if archive.stat().st_size <= 0 or archive.stat().st_size > MAX_SHARED_ARCHIVE_BYTES:
        raise RuntimeError(f"Shared source archive size is invalid: {archive.stat().st_size}")
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, mode="r:gz") as tf:
        members = []
        total = 0
        for member in tf.getmembers():
            p = Path(member.name)
            if p.is_absolute() or ".." in p.parts or member.issym() or member.islnk() or member.isdev() or member.isfifo():
                raise RuntimeError(f"Unsafe beta.81 source archive entry: {member.name}")
            if member.isfile():
                total += int(member.size or 0)
                if total > MAX_SHARED_EXTRACTED_BYTES:
                    raise RuntimeError("Shared source archive exceeds extraction limit")
            elif not member.isdir():
                raise RuntimeError(f"Unsupported beta.81 source archive entry: {member.name}")
            members.append(member)
        tf.extractall(target, members=members, filter="data")
    return target


def extract_shared_archive(archive: Path, output: Path, manifest: dict) -> list[dict]:
    actual_archive = sha256(archive)
    if actual_archive != SHARED_ARCHIVE_SHA256:
        raise RuntimeError(f"Shared source archive hash mismatch: {actual_archive} != {SHARED_ARCHIVE_SHA256}")
    with tempfile.TemporaryDirectory(prefix="cp-beta81-shared-") as td:
        staged = safe_extract_shared(archive, Path(td) / "source")
        return activate_source(staged, output, manifest)


def locate_exact_source(repo_root: Path, explicit_archive: Path | None, explicit_root: Path | None):
    if explicit_root:
        return ("root", explicit_root.expanduser().resolve())
    candidates = []
    if explicit_archive:
        candidates.append(explicit_archive)
    env_archive = os.environ.get("CP_SHARED_SOURCE_ARCHIVE", "").strip() or os.environ.get("CP_PROTECTED_SOURCE_ARCHIVE", "").strip()
    if env_archive:
        candidates.append(Path(env_archive))
    candidates.extend([
        repo_root / SHARED_ARCHIVE_NAME,
        repo_root.parent / SHARED_ARCHIVE_NAME,
        Path.home() / "Downloads" / SHARED_ARCHIVE_NAME,
        Path.home() / "Изтегляния" / SHARED_ARCHIVE_NAME,
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
    parser.add_argument("--source-archive", type=Path, help="exact beta.81 shared source archive")
    parser.add_argument("--source-root", type=Path, help="directory containing exact beta.81 shared source")
    parser.add_argument("--allow-source-unavailable", action="store_true",
                        help="materialize platform runtime only; never substitute an older shared source")
    args = parser.parse_args()

    output = args.output.expanduser().resolve()
    if output == repo_root.resolve() or (repo_root.resolve() in output.parents and output.name == "linux"):
        raise RuntimeError("Refusing to materialize over the repository source tree")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    manifest = json.loads((repo_root / "source_manifest.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="cp-linux-upstream-") as td:
        upstream = safe_extract_upstream(download_upstream(), Path(td))
        copy_tree(upstream / "linux-port" / "linux", output / "linux", replace=True)
        copy_tree(upstream / "linux-port" / "packaging", output / "packaging", replace=True)
        copy_tree(upstream / "linux-port" / "ci", output / "ci", replace=True)
        copy_tree(upstream / "linux-port" / "tests", output / "tests", replace=True)
        fide_seed = upstream / "fide"
        if fide_seed.is_dir():
            copy_tree(fide_seed, output / "fide-cache", replace=True)

    source_kind, source_location = locate_exact_source(repo_root, args.source_archive, args.source_root)
    shared_verified = False
    shared_origin = "unavailable"
    checked = []
    if source_kind == "archive":
        checked = extract_shared_archive(source_location, output, manifest)
        shared_verified = True
        shared_origin = f"archive:{source_location.name}"
    elif source_kind == "root":
        checked = activate_source(source_location, output, manifest)
        shared_verified = True
        shared_origin = f"root:{source_location}"
    elif not args.allow_source_unavailable:
        raise RuntimeError("Exact beta.81 shared source is unavailable. Supply --source-archive/--source-root or "
                           "CP_SHARED_SOURCE_ARCHIVE. Older beta.34 shared source is forbidden.")

    # Reapply Linux-only adapters/runtime after the immutable upstream platform seed.
    copy_tree(repo_root / "linux", output / "linux")
    copy_tree(repo_root / "tests", output / "tests")
    if (repo_root / "ci").is_dir():
        copy_tree(repo_root / "ci", output / "ci")
    copy_tree(repo_root / "scripts", output / "scripts")
    if (repo_root / "packaging").is_dir():
        copy_tree(repo_root / "packaging", output / "packaging")
    shutil.copy2(repo_root / "source_manifest.json", output / "source_manifest.json")
    for version_name in ("VERSION", "VERSION.txt"):
        if (repo_root / version_name).is_file():
            shutil.copy2(repo_root / version_name, output / version_name)

    target_version = (repo_root / "VERSION.txt").read_text(encoding="utf-8").strip()
    state = {
        "upstreamRepository": UPSTREAM_REPO,
        "upstreamCommit": UPSTREAM_COMMIT,
        "dedicatedRepository": "kbilyal/ChessPublisher-Linux",
        "version": target_version,
        "sharedSourceSnapshot": manifest.get("snapshotId"),
        "sharedSourceVerified": shared_verified,
        "protectedSourceVerified": shared_verified,
        "sharedSourceOrigin": shared_origin,
        "protectedSourceOrigin": shared_origin,
        "sharedArchiveSha256": SHARED_ARCHIVE_SHA256,
        "protectedArchiveSha256": SHARED_ARCHIVE_SHA256,
        "sharedFilesChecked": len(checked),
        "oldUpstreamRootSourceAllowed": False,
        "olderBeta34SharedSourceAllowed": False,
        "overlay": ["linux platform adapters", "tests", "scripts", "packaging"],
    }
    (output / "MATERIALIZED_STATE.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    print(f"Materialized beta.81 Linux runtime at {output}")
    print(f"Platform baseline: {UPSTREAM_REPO}@{UPSTREAM_COMMIT}")
    print(f"Shared source verified: {shared_verified} ({shared_origin})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
