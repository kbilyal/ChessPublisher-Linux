#!/usr/bin/env python3
"""Static safety contract for Pairings Download Results integration."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
JS=(ROOT/'linux'/'web_results_download.js').read_text(encoding='utf-8')
PY=(ROOT/'linux'/'web_results_download_integration.py').read_text(encoding='utf-8')

required=(
    'Download Results',
    'cpDownloadWebResultsBtn',
    '/arbiter-results',
    '/arbiter-results/ack',
    'listPendingWebResults',
    'acknowledgeWebResults',
    'submissionIds:ids',
    'getSelectedPairingRoundNumber',
    'isSelectedRoundEditable',
    'buildReconcilePlan',
    'pairingIdentity',
    'board.result=item.remoteResult',
    'Keep Desktop',
    'Use Web',
    'cpKeepDesktopResultBtn',
    'cpUseWebResultBtn',
    "remoteResult==='-'",
    'RESULT-ONLY SAFETY',
    'exact board number + White/Black key matching',
    'synchronizeResultsToCanonicalBase',
    'cpUnifiedSync',
    'cpCloudCheckStatus',
    'lastWebResultsDownloadRevision',
    'lastWebResultsSyncAt',
    'lastWebResultsAcknowledgedCount',
)
for marker in required:
    if marker not in JS:
        raise SystemExit(f'MISSING_JS: {marker}')

for forbidden in (
    'generatePairingWithGacrux(',
    'pullCloudToDesktop(',
    'data.tournaments[',
    'getCurrentSnapshot(',
    'localBoards[item.localIndex]=',
    'whiteKey=item.',
    'blackKey=item.',
    'OK = Web',
    'Cancel = Desktop',
):
    if forbidden in JS:
        raise SystemExit(f'FORBIDDEN_JS: {forbidden}')

for marker in ('inject_web_results_download','cpWebResultsDownloadScript','_SCRIPT_FILE'):
    if marker not in PY:
        raise SystemExit(f'MISSING_PY: {marker}')

entry=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
if 'from web_results_download_integration import apply as apply_web_results_download' not in entry:
    raise SystemExit('MISSING_ENTRY_IMPORT')
if 'apply_web_results_download()' not in entry:
    raise SystemExit('MISSING_ENTRY_APPLY')

print('WEB_RESULTS_DOWNLOAD_STATIC_CONTRACT=PASS')
