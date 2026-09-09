#!/usr/bin/env python3
"""Static safety contract for beta.85 shared Web-results/SYNC architecture.

The dev23 Linux result-only implementation remains regression-tested as rollback
code, but beta.85 active behavior comes from the exact shared source.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'linux'/'web_results_download.js').read_text(encoding='utf-8')
PY=(ROOT/'linux'/'web_results_download_integration.py').read_text(encoding='utf-8')
ENTRY=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
SHARED=(ROOT/'linux'/'shared_source_integration.py').read_text(encoding='utf-8')
MANIFEST=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))

# Preserve rollback result-only safety; no pairing/player mutation may creep in.
required=(
    'Download Results','cpDownloadWebResultsBtn','/arbiter-results','/arbiter-results/ack',
    'listPendingWebResults','acknowledgeWebResults','submissionIds:ids',
    'getSelectedPairingRoundNumber','isSelectedRoundEditable','buildReconcilePlan',
    'pairingIdentity','board.result=item.remoteResult','Keep Desktop','Use Web',
    'cpKeepDesktopResultBtn','cpUseWebResultBtn',"remoteResult==='-'",'RESULT-ONLY SAFETY',
    'exact board number + White/Black key matching','synchronizeResultsToCanonicalBase',
    'cpUnifiedSync','cpCloudCheckStatus','lastWebResultsDownloadRevision',
    'lastWebResultsSyncAt','lastWebResultsAcknowledgedCount',
)
for marker in required:
    if marker not in JS: raise SystemExit(f'MISSING_JS: {marker}')
for forbidden in (
    'generatePairingWithGacrux(','pullCloudToDesktop(','data.tournaments[','getCurrentSnapshot(',
    'localBoards[item.localIndex]=','whiteKey=item.','blackKey=item.','OK = Web','Cancel = Desktop',
):
    if forbidden in JS: raise SystemExit(f'FORBIDDEN_JS: {forbidden}')
for marker in ('inject_web_results_download','cpWebResultsDownloadScript','_SCRIPT_FILE'):
    if marker not in PY: raise SystemExit(f'MISSING_PY: {marker}')

# Active beta.85 entry must NOT fork the shared Web-results/unified-SYNC policy.
for forbidden in ('from web_results_download_integration import apply as apply_web_results_download','apply_web_results_download()'):
    if forbidden in ENTRY: raise SystemExit(f'LINUX_WEB_RESULTS_FORK_ACTIVE: {forbidden}')
if 'apply_shared_source()' not in ENTRY: raise SystemExit('MISSING_SHARED_SOURCE_ENTRY')
for marker in ('/source/webview/CloudWorkspaceAdapter.js','/source/webview/CloudWorkspaceRedesign.js'):
    if marker not in SHARED: raise SystemExit(f'MISSING_SHARED_STACK: {marker}')
if MANIFEST.get('cloudFingerprintContentSchema')!=7: raise SystemExit('WRONG_CLOUD_SCHEMA')
shared=MANIFEST.get('runtimeSharedFiles') or {}
if (shared.get('webview/CloudWorkspaceAdapter.js') or {}).get('sha256')!='6ce71bd7b4eb4b2401e9ee657f60b308ed6222a162efa0ded925f9b510e9569e': raise SystemExit('WRONG_SCHEMA7_ADAPTER')
if (shared.get('webview/CloudWorkspaceRedesign.js') or {}).get('sha256')!='52f39e7c8ab992611f0f9b0eed02836cc19a002016d87b226b94da388f78177a': raise SystemExit('WRONG_BETA85_SYNC_REDESIGN')
print('BETA85_WEB_RESULTS_SHARED_SOURCE_STATIC_CONTRACT=PASS')
