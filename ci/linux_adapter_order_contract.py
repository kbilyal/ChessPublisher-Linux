#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
entry=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
hubfix=entry.find('apply_hub_tab_visibility()');layout=entry.find('apply_tournament_setup_layout()');shared=entry.find('apply_shared_source()');runtime=entry.find('apply_runtime_instance()');platform=entry.find('apply_pairings_result_desk()')
if min(hubfix,layout,shared,runtime,platform)<0 or not platform<hubfix<layout<shared<runtime:raise RuntimeError('Linux platform order must be Result Desk -> Hub visibility -> Tournament Setup layout -> shared source -> runtime instance selection')
for forbidden in ('apply_cloud_directional_sync()','apply_web_results_download()','apply_cloud_unified_sync()','apply_rating_lists_ui()'):
    if forbidden in entry:raise RuntimeError(f'Linux-specific shared/business policy remains active: {forbidden}')
adapter=(ROOT/'linux'/'shared_source_integration.py').read_text(encoding='utf-8')
order=['/linux/LinuxWebViewShim.js','/source/webview/WebViewAdapter.js','/source/hub/client/hub-snapshot.js','/source/hub/client/hub-api-client.js','/source/webview/HubAdapter.js','/source/cloud/client/cloud-workspace-api.js','/source/webview/CloudWorkspaceAdapter.js','/source/webview/CloudWorkspaceRedesign.js']
pos=[adapter.find(x) for x in order]
if min(pos)<0 or pos!=sorted(pos):raise RuntimeError(f'beta.85 shared stack order mismatch: {pos}')
if 'data-chesspublisher-linux-delivery' not in adapter or 'DELIVERY_REVISION' not in adapter:raise RuntimeError('Linux delivery identity marker is missing')
hub=(ROOT/'linux'/'hub_tab_visibility_integration.py').read_text(encoding='utf-8')
for marker in ('grid-template-columns:repeat(9,minmax(0,1fr))!important','#appWindow #tabHub','visibility:visible!important','opacity:1!important'):
    if marker not in hub:raise RuntimeError(f'Online Hub visibility marker missing: {marker}')
layout_adapter=(ROOT/'linux'/'tournament_setup_layout_integration.py').read_text(encoding='utf-8')
for marker in ('cpLinuxTournamentSetupLayoutStyle','#cpBeta70LongEventBox','grid-column:1 / -1!important','justify-self:stretch!important'):
    if marker not in layout_adapter:raise RuntimeError(f'Tournament Setup layout marker missing: {marker}')
build=(ROOT/'linux'/'build_info.py').read_text(encoding='utf-8')
if 'DELIVERY_REVISION = "beta85-tournament-layout-runtime3"' not in build:raise RuntimeError('Tournament Setup point-fix delivery revision is missing')

sys.path.insert(0,str(ROOT/'linux'))
import runtime_instance_integration as instance
original_probe=instance._probe
try:
    def check(states,expected,scan_ports=6):
        instance._probe=lambda port: states.get(port,'occupied')
        actual=instance.select_default_port(18765,scan_ports)
        if actual!=expected:raise RuntimeError(f'Runtime selection mismatch: {actual} != {expected}')
    check({18765:'current'},(18765,'current'))
    check({18765:'stale',18766:'free'},(18766,'stale-bypassed'))
    check({18765:'stale',18766:'free',18767:'current'},(18767,'current'))
    check({18765:'occupied',18766:'free'},(18766,'free'))
    # Scan boundaries must be deterministic: a matching instance outside the configured
    # range must not be reused, and scan_ports<=0 still probes exactly the base port.
    check({18765:'occupied',18766:'free',18767:'current'},(18766,'free'),2)
    check({18765:'free'},(18765,'free'),0)
    # Fail closed when the complete scan range is owned by stale/foreign processes.
    for states in (
        {18765:'occupied',18766:'occupied',18767:'occupied'},
        {18765:'stale',18766:'occupied',18767:'stale'},
    ):
        instance._probe=lambda port,states=states: states.get(port,'occupied')
        try:
            instance.select_default_port(18765,3)
        except RuntimeError as exc:
            if 'No free Chess-Publisher LocalEngine port found' not in str(exc):raise
        else:
            raise RuntimeError('Exhausted runtime port range must fail closed')
finally:
    instance._probe=original_probe
if not instance._explicit_port(['--port','19999']) or not instance._explicit_port(['--port=19999']) or instance._explicit_port(['--quiet']):raise RuntimeError('Explicit --port detection regression')
print('BETA85_LINUX_ADAPTER_LOAD_ORDER=PASS')
print('BETA85_LINUX_ONLINE_HUB_TAB_LAYOUT_GUARD=PASS')
print('BETA85_TOURNAMENT_SETUP_LAYOUT_GUARD=PASS')
print('BETA85_STALE_RUNTIME_INSTANCE_SELECTION=PASS')
print('BETA85_RUNTIME_INSTANCE_FAIL_CLOSED=PASS')
