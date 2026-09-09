#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'CURRENT_STATE.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
assert (ROOT/'VERSION.txt').read_text().strip()=='1.06.00-beta.85'
assert (ROOT/'VERSION').read_text().strip()=='v1.06.00-beta.85'
assert state['targetSharedVersion']=='v1.06.00-beta.85'
assert state['windowsReference']['version']=='v1.06.00-beta.85'
assert state['windowsReference']['commit']=='1354a8061fbbc520ecd1ea09b93350e388428dfd'
assert state['windowsReference']['sourceSha256']=='2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69'
assert state['windowsReference']['cloudFingerprintContentSchema']==7
assert state['windowsReference']['vcl']['externalTecRow']=='Q18'
assert state['releaseCandidate'] is False
assert manifest['baseRelease']=='v1.06.00-beta.85'
assert manifest['archive']['sha256']==state['windowsReference']['sourceSha256']
assert manifest['runtimeSharedFiles']['ChessPublisher.html']['sha256']=='2a0437da7d6ae20f04cf4499ba36b6c7c81698c1517b390b1fed6f3775f5a175'
assert manifest['runtimeSharedFiles']['webview/CloudWorkspaceAdapter.js']['sha256']=='6ce71bd7b4eb4b2401e9ee657f60b308ed6222a162efa0ded925f9b510e9569e'
assert manifest['runtimeSharedFiles']['webview/CloudWorkspaceRedesign.js']['sha256']=='52f39e7c8ab992611f0f9b0eed02836cc19a002016d87b226b94da388f78177a'
print('BETA85_WINDOWS_LINUX_ALIGNMENT_CONTRACT=PASS')
