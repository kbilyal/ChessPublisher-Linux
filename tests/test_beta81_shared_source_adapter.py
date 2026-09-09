#!/usr/bin/env python3
"""Static contract: Linux wraps beta.81 shared logic and does not fork it."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
assert manifest['baseRelease']=='v1.06.00-beta.81'
assert manifest['archive']['sha256']=='b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b'
assert manifest['authoritativeTypeB']['sha256']=='3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96'
entry=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
assert 'apply_beta81_shared_source()' in entry
for forbidden_call in ('apply_cloud_directional_sync()','apply_web_results_download()','apply_cloud_unified_sync()','apply_rating_lists_ui()'):
    assert forbidden_call not in entry, forbidden_call
adapter=(ROOT/'linux'/'beta81_shared_source_integration.py').read_text(encoding='utf-8')
ordered=['/linux/LinuxWebViewShim.js','/source/webview/WebViewAdapter.js','/source/hub/client/hub-snapshot.js','/source/hub/client/hub-api-client.js','/source/webview/HubAdapter.js','/source/cloud/client/cloud-workspace-api.js','/source/webview/CloudWorkspaceAdapter.js','/source/webview/CloudWorkspaceRedesign.js']
pos=[adapter.index(x) for x in ordered]
assert pos==sorted(pos),pos
assert 'ChessPublisher-' in adapter and 'USER-MANUAL-EN.html' in adapter
for forbidden in ('GacruxRuntime','generate_pairings','exportTRF','tieBreak','pairingIdentity','cloud.internalId'):
    assert forbidden not in adapter, forbidden
print('BETA81_SHARED_SOURCE_ADAPTER_CONTRACT=PASS')
