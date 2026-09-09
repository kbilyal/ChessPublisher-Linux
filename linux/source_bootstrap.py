#!/usr/bin/env python3
"""Bootstrap the exact authoritative beta.81 shared source for Linux."""
from __future__ import annotations
import hashlib, os, shutil, tarfile, tempfile
from pathlib import Path
from typing import Any
from source_guard import SourceIdentityError, verify_source

ARCHIVE_NAME = "Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz"
ARCHIVE_SHA256 = "b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b"
MAX_ARCHIVE_BYTES = 4 * 1024 * 1024
MAX_EXTRACTED_BYTES = 16 * 1024 * 1024

def _sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def _archive_candidates(package_root: Path) -> list[Path]:
    home=Path.home();raw=[package_root/ARCHIVE_NAME,package_root.parent/ARCHIVE_NAME,home/'Downloads'/ARCHIVE_NAME,home/'Изтегляния'/ARCHIVE_NAME]
    out=[];seen=set()
    for item in raw:
        r=item.expanduser().resolve()
        if r not in seen: seen.add(r);out.append(r)
    return out

def _safe_members(tf: tarfile.TarFile) -> list[tarfile.TarInfo]:
    members=tf.getmembers()
    if not members: raise SourceIdentityError('Shared source archive is empty.')
    total=0
    for member in members:
        p=Path(member.name)
        if p.is_absolute() or '..' in p.parts or member.issym() or member.islnk() or member.isdev() or member.isfifo():
            raise SourceIdentityError(f'Unsafe shared source archive entry: {member.name}')
        if member.isfile():
            total+=int(member.size or 0)
            if total>MAX_EXTRACTED_BYTES: raise SourceIdentityError('Shared source archive exceeds extraction limit.')
        elif not member.isdir(): raise SourceIdentityError(f'Unsupported shared source archive entry: {member.name}')
    return members

def ensure_source(package_root: Path) -> dict[str,Any]:
    root=package_root.expanduser().resolve();source=root/'source';manifest=root/'source_manifest.json'
    try:
        result=verify_source(source,manifest);result['bootstrapped']=False;return result
    except SourceIdentityError:
        if source.exists() and any(source.rglob('*')): raise
    archive=next((p for p in _archive_candidates(root) if p.is_file()),None)
    if archive is None:
        locations='\n  - '.join(str(p) for p in _archive_candidates(root))
        raise SourceIdentityError(f'Required exact beta.81 shared source is not present.\nPlace {ARCHIVE_NAME} in one of these locations:\n  - {locations}')
    size=archive.stat().st_size
    if size<=0 or size>MAX_ARCHIVE_BYTES: raise SourceIdentityError(f'Shared source archive size is invalid: {size} bytes')
    digest=_sha256(archive)
    if digest!=ARCHIVE_SHA256: raise SourceIdentityError(f'Shared source archive SHA256 mismatch. Expected {ARCHIVE_SHA256}, got {digest}.')
    root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cp-beta81-source-',dir=str(root)) as td_raw:
        staged=Path(td_raw)/'source';staged.mkdir()
        try:
            with tarfile.open(archive,'r:gz') as tf:
                members=_safe_members(tf);tf.extractall(staged,members=members,filter='data')
        except (OSError,tarfile.TarError) as exc:
            raise SourceIdentityError(f'Could not extract exact beta.81 source: {exc}') from exc
        verified=verify_source(staged,manifest)
        if source.exists(): shutil.rmtree(source)
        os.replace(staged,source)
        verified=verify_source(source,manifest);verified['bootstrapped']=True;verified['archive']=str(archive);return verified

if __name__=='__main__':
    package_root=Path(__file__).resolve().parent.parent
    result=ensure_source(package_root);state='RESTORED' if result.get('bootstrapped') else 'READY'
    print(f"SHARED_SOURCE_{state}={result.get('snapshotId')}")
