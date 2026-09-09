#!/usr/bin/env python3
"""Static contract: Linux wraps exact beta.85 shared logic and does not fork it."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
assert manifest['baseRelease']=='v1.06.00-beta.85'
assert manifest['archive']['sha256']=='2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69'
assert manifest['authoritativeWindowsCommit']=='1354a8061fbbc520ecd1ea09b93350e388428dfd'
assert manifest['cloudFingerprintContentSchema']==7
shared=manifest['runtimeSharedFiles']
assert shared['webview/CloudWorkspaceAdapter.js']['sha256']=='6ce71bd7b4eb4b2401e9ee657f60b308ed6222a162efa0ded925f9b510e9569e'
assert shared['webview/CloudWorkspaceRedesign.js']['sha256']=='52f39e7c8ab992611f0f9b0eed02836cc19a002016d87b226b94da388f78177a'
assert shared['ChessPublisher.html']['sha256']=='2a0437da7d6ae20f04cf4499ba36b6c7c81698c1517b390b1fed6f3775f5a175'
entry=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
assert 'apply_shared_source()' in entry
for forbidden_call in ('apply_cloud_directional_sync()','apply_web_results_download()','apply_cloud_unified_sync()','apply_rating_lists_ui()'):
    assert forbidden_call not in entry, forbidden_call
adapter=(ROOT/'linux'/'shared_source_integration.py').read_text(encoding='utf-8')
ordered=['/linux/LinuxWebViewShim.js','/source/webview/WebViewAdapter.js','/source/hub/client/hub-snapshot.js','/source/hub/client/hub-api-client.js','/source/webview/HubAdapter.js','/source/cloud/client/cloud-workspace-api.js','/source/webview/CloudWorkspaceAdapter.js','/source/webview/CloudWorkspaceRedesign.js']
pos=[adapter.index(x) for x in ordered]
assert pos==sorted(pos),pos
assert "chesspublisherLinuxBuild='1.06.00-beta.85'" in adapter
for forbidden in ('GacruxRuntime','generate_pairings','exportTRF','tieBreak','pairingIdentity','cloud.internalId'):
    assert forbidden not in adapter, forbidden
print('BETA85_SHARED_SOURCE_ADAPTER_CONTRACT=PASS')
