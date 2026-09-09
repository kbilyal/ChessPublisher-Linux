#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'linux'))
from source_guard import verify_source,SourceIdentityError,load_manifest

def digest(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def main()->int:
    manifest=load_manifest(ROOT/'source_manifest.json')
    if manifest.get('baseRelease')!='v1.06.00-beta.81':raise RuntimeError('beta.81 source is not authoritative')
    expected=manifest['runtimeSharedFiles']['ChessPublisher.html']
    if expected['size']!=1591436 or expected['sha256']!='7bdea647f95c3e387326e1290791d60696c140a273d55be8ad43c331362bf2c8':
        raise RuntimeError('Pinned beta.81 shared source identity changed unexpectedly.')
    with tempfile.TemporaryDirectory(prefix='cp-source-guard-') as td:
        td=Path(td);src=td/'source';src.mkdir();data=b'exact-shared-source';(src/'app.html').write_bytes(data);(src/'VERSION.txt').write_text('1.06.00-beta.81\n')
        mf=td/'manifest.json';mf.write_text(json.dumps({'baseRelease':'v1.06.00-beta.81','runtimeSharedFiles':{'app.html':{'size':len(data),'sha256':digest(data)},'VERSION.txt':{'size':16,'sha256':digest(b'1.06.00-beta.81\n')}}}),encoding='utf-8')
        if not verify_source(src,mf)['ok']:raise RuntimeError('exact source was rejected')
        (src/'app.html').write_bytes(data+b'!')
        try:verify_source(src,mf)
        except SourceIdentityError:pass
        else:raise RuntimeError('modified source was accepted')
    print('BETA81_SOURCE_GUARD_CONTRACT=PASS');return 0
if __name__=='__main__':raise SystemExit(main())
