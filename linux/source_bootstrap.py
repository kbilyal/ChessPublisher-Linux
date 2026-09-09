#!/usr/bin/env python3
"""Bootstrap the exact authoritative beta.85 shared source for Linux."""
from __future__ import annotations
import hashlib, os, shutil, tarfile, tempfile
from pathlib import Path
from typing import Any
from source_guard import SourceIdentityError, verify_source, load_manifest

ARCHIVE_NAME = "Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz"
ARCHIVE_SHA256 = "2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69"
MAX_ARCHIVE_BYTES = 64 * 1024 * 1024
MAX_EXTRACTED_BYTES = 512 * 1024 * 1024

def _sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def _archive_candidates(package_root: Path) -> list[Path]:
    home=Path.home();raw=[package_root/ARCHIVE_NAME,package_root.parent/ARCHIVE_NAME,home/'Downloads'/ARCHIVE_NAME,home/'Изтегляния'/ARCHIVE_NAME]
    env=os.environ.get('CP_SHARED_SOURCE_ARCHIVE','').strip() or os.environ.get('CP_PROTECTED_SOURCE_ARCHIVE','').strip()
    if env: raw.insert(0,Path(env))
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

def _resolve_source_root(staged: Path, manifest: Path) -> Path:
    candidates=[staged]
    for vf in staged.rglob('VERSION.txt'):
        try: rel=vf.relative_to(staged)
        except ValueError: continue
        if len(rel.parts)<=3: candidates.append(vf.parent)
    good=[];seen=set()
    for c in candidates:
        c=c.resolve()
        if c in seen: continue
        seen.add(c)
        try: verify_source(c,manifest)
        except SourceIdentityError: continue
        good.append(c)
    if len(good)!=1:
        raise SourceIdentityError(f'Could not resolve exactly one beta.85 shared source root (matches={len(good)}).')
    return good[0]

def _copy_manifest_files(source_root: Path, target: Path, manifest_path: Path) -> None:
    manifest=load_manifest(manifest_path);specs=manifest.get('runtimeSharedFiles') or manifest.get('files') or {}
    if target.exists(): shutil.rmtree(target)
    target.mkdir(parents=True)
    for rel in specs:
        src=(source_root/rel).resolve();dst=(target/rel).resolve()
        if source_root.resolve() not in src.parents and src!=source_root.resolve(): raise SourceIdentityError(f'Unsafe shared source path: {rel}')
        if target.resolve() not in dst.parents: raise SourceIdentityError(f'Unsafe target shared source path: {rel}')
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    verify_source(target,manifest_path)

def ensure_source(package_root: Path) -> dict[str,Any]:
    root=package_root.expanduser().resolve();source=root/'source';manifest=root/'source_manifest.json'
    try:
        result=verify_source(source,manifest);result['bootstrapped']=False;return result
    except SourceIdentityError:
        if source.exists() and any(source.rglob('*')): raise
    archive=next((p for p in _archive_candidates(root) if p.is_file()),None)
    if archive is None:
        locations='\n  - '.join(str(p) for p in _archive_candidates(root))
        raise SourceIdentityError(f'Required exact beta.85 shared source is not present.\nPlace {ARCHIVE_NAME} in one of these locations:\n  - {locations}')
    size=archive.stat().st_size
    if size<=0 or size>MAX_ARCHIVE_BYTES: raise SourceIdentityError(f'Shared source archive size is invalid: {size} bytes')
    digest=_sha256(archive)
    if digest!=ARCHIVE_SHA256: raise SourceIdentityError(f'Shared source archive SHA256 mismatch. Expected {ARCHIVE_SHA256}, got {digest}.')
    root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cp-beta85-source-',dir=str(root)) as td_raw:
        staged=Path(td_raw)/'extract';staged.mkdir()
        try:
            with tarfile.open(archive,'r:gz') as tf:
                members=_safe_members(tf);tf.extractall(staged,members=members,filter='data')
        except (OSError,tarfile.TarError) as exc:
            raise SourceIdentityError(f'Could not extract exact beta.85 source: {exc}') from exc
        source_root=_resolve_source_root(staged,manifest)
        prepared=Path(td_raw)/'shared';_copy_manifest_files(source_root,prepared,manifest)
        if source.exists(): shutil.rmtree(source)
        os.replace(prepared,source)
        verified=verify_source(source,manifest);verified['bootstrapped']=True;verified['archive']=str(archive);return verified

if __name__=='__main__':
    package_root=Path(__file__).resolve().parent.parent
    result=ensure_source(package_root);state='RESTORED' if result.get('bootstrapped') else 'READY'
    print(f"SHARED_SOURCE_{state}={result.get('snapshotId')}")
