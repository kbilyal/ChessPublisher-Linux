#!/usr/bin/env python3
"""Fail-closed exact shared-source identity guard for Chess-Publisher Linux."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from typing import Any

class SourceIdentityError(RuntimeError):
    pass

def _sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def load_manifest(path: Path) -> dict[str,Any]:
    try:
        value=json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise SourceIdentityError(f'Could not read source manifest: {exc}') from exc
    if not isinstance(value,dict):
        raise SourceIdentityError('Source manifest is invalid.')
    files=value.get('runtimeSharedFiles') or value.get('files')
    if not isinstance(files,dict) or not files:
        raise SourceIdentityError('Source manifest has no shared runtime file set.')
    return value

def verify_source(source_root: Path, manifest_path: Path) -> dict[str,Any]:
    source_root=source_root.resolve();manifest=load_manifest(manifest_path)
    specs=manifest.get('runtimeSharedFiles') or manifest.get('files') or {}
    checked=[]
    for rel,spec in specs.items():
        p=(source_root/rel).resolve()
        if source_root not in p.parents and p!=source_root:
            raise SourceIdentityError(f'Unsafe source path in manifest: {rel}')
        if not p.is_file():
            raise SourceIdentityError(f'Required shared source file is missing: {rel}')
        expected_size=int(spec.get('size') or 0);actual_size=p.stat().st_size
        if actual_size!=expected_size:
            raise SourceIdentityError(f'Shared source size mismatch for {rel}: expected {expected_size}, got {actual_size}.')
        got=_sha256(p);expected=str(spec.get('sha256') or '').lower()
        if got!=expected:
            raise SourceIdentityError(f'Shared source SHA256 mismatch for {rel}: expected {expected}, got {got}.')
        checked.append({'path':rel,'size':actual_size,'sha256':got})
    version_file=source_root/'VERSION.txt'
    version=version_file.read_text(encoding='utf-8').strip() if version_file.is_file() else ''
    base=str(manifest.get('baseRelease') or '').removeprefix('v')
    if base and version!=base:
        raise SourceIdentityError(f'Shared source VERSION.txt mismatch: expected {base}, got {version or "missing"}.')
    return {'ok':True,'snapshotId':manifest.get('snapshotId'),'baseRelease':manifest.get('baseRelease'),'version':version,'files':checked}

def require_package_source(package_root: Path) -> dict[str,Any]:
    root=package_root.resolve()
    return verify_source(root/'source',root/'source_manifest.json')
