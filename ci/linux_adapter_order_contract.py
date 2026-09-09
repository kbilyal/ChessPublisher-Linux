#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
entry=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
shared=entry.find('apply_beta81_shared_source()');platform=entry.find('apply_pairings_result_desk()')
if min(shared,platform)<0 or not platform<shared:raise RuntimeError('beta.81 shared-source delivery adapter must be last')
for forbidden in ('apply_cloud_directional_sync()','apply_web_results_download()','apply_cloud_unified_sync()','apply_rating_lists_ui()'):
    if forbidden in entry:raise RuntimeError(f'Linux-specific shared/business policy remains active: {forbidden}')
adapter=(ROOT/'linux'/'beta81_shared_source_integration.py').read_text(encoding='utf-8')
order=['/linux/LinuxWebViewShim.js','/source/webview/WebViewAdapter.js','/source/hub/client/hub-snapshot.js','/source/hub/client/hub-api-client.js','/source/webview/HubAdapter.js','/source/cloud/client/cloud-workspace-api.js','/source/webview/CloudWorkspaceAdapter.js','/source/webview/CloudWorkspaceRedesign.js']
pos=[adapter.find(x) for x in order]
if min(pos)<0 or pos!=sorted(pos):raise RuntimeError(f'beta.81 shared stack order mismatch: {pos}')
print('BETA81_LINUX_ADAPTER_LOAD_ORDER=PASS')
