#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
entry=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
hubfix=entry.find('apply_hub_tab_visibility()');shared=entry.find('apply_shared_source()');platform=entry.find('apply_pairings_result_desk()')
if min(hubfix,shared,platform)<0 or not platform<hubfix<shared:raise RuntimeError('Linux Hub visibility fix must remain platform-only and load before the final shared-source delivery adapter')
for forbidden in ('apply_cloud_directional_sync()','apply_web_results_download()','apply_cloud_unified_sync()','apply_rating_lists_ui()'):
    if forbidden in entry:raise RuntimeError(f'Linux-specific shared/business policy remains active: {forbidden}')
adapter=(ROOT/'linux'/'shared_source_integration.py').read_text(encoding='utf-8')
order=['/linux/LinuxWebViewShim.js','/source/webview/WebViewAdapter.js','/source/hub/client/hub-snapshot.js','/source/hub/client/hub-api-client.js','/source/webview/HubAdapter.js','/source/cloud/client/cloud-workspace-api.js','/source/webview/CloudWorkspaceAdapter.js','/source/webview/CloudWorkspaceRedesign.js']
pos=[adapter.find(x) for x in order]
if min(pos)<0 or pos!=sorted(pos):raise RuntimeError(f'beta.85 shared stack order mismatch: {pos}')
hub=(ROOT/'linux'/'hub_tab_visibility_integration.py').read_text(encoding='utf-8')
for marker in ('grid-template-columns:repeat(9,minmax(0,1fr))!important','#appWindow #tabHub','visibility:visible!important','opacity:1!important'):
    if marker not in hub:raise RuntimeError(f'Online Hub visibility marker missing: {marker}')
print('BETA85_LINUX_ADAPTER_LOAD_ORDER=PASS')
print('BETA85_LINUX_ONLINE_HUB_TAB_LAYOUT_GUARD=PASS')
