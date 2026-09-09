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
    if manifest.get('baseRelease')!='v1.06.00-beta.85':raise RuntimeError('beta.85 source is not authoritative')
    redesign=manifest['runtimeSharedFiles']['webview/CloudWorkspaceRedesign.js']
    if redesign['sha256']!='52f39e7c8ab992611f0f9b0eed02836cc19a002016d87b226b94da388f78177a':raise RuntimeError('beta.85 redesign identity changed')
    with tempfile.TemporaryDirectory(prefix='cp-source-guard-') as td:
        td=Path(td);src=td/'source';src.mkdir();data=b'exact-shared-source';(src/'app.html').write_bytes(data);(src/'VERSION.txt').write_text('1.06.00-beta.85\n')
        mf=td/'manifest.json';mf.write_text(json.dumps({'baseRelease':'v1.06.00-beta.85','runtimeSharedFiles':{'app.html':{'sha256':digest(data)},'VERSION.txt':{'size':16,'sha256':digest(b'1.06.00-beta.85\n')}}}),encoding='utf-8')
        if not verify_source(src,mf)['ok']:raise RuntimeError('exact source was rejected')
        (src/'app.html').write_bytes(data+b'!')
        try:verify_source(src,mf)
        except SourceIdentityError:pass
        else:raise RuntimeError('modified source was accepted')
    print('BETA85_SOURCE_GUARD_CONTRACT=PASS');return 0
if __name__=='__main__':raise SystemExit(main())
