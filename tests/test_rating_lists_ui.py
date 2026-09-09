#!/usr/bin/env python3
"""Static contract for beta.85 shared rating-list UI + Linux native data backend."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
BACKEND=(ROOT/'linux'/'rating_lists_integration.py').read_text(encoding='utf-8')
ENTRY=(ROOT/'linux'/'chess_publisher_linux_entry.py').read_text(encoding='utf-8')
SHARED=(ROOT/'linux'/'shared_source_integration.py').read_text(encoding='utf-8')
MANIFEST=json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))

for marker in (
    'Integrated FIDE rating lists + LEGACY fallback',
    'activate_from_files',
    'tournamentPlayersChanged',
    'rolledBack',
    'generation',
    'LIST_TYPES',
):
    if marker not in BACKEND: raise SystemExit(f'MISSING_BACKEND: {marker}')
for forbidden in ('generatePairings','tournament.players =','tournament.players='):
    if forbidden in BACKEND: raise SystemExit(f'FORBIDDEN_BACKEND: {forbidden}')

if 'from rating_lists_integration import apply as apply_rating_lists' not in ENTRY or 'apply_rating_lists()' not in ENTRY:
    raise SystemExit('MISSING_NATIVE_RATING_BACKEND')
# beta.85 parity: shared source owns rating-list UI/business semantics; the old
# Linux-specific UI adapter may remain for rollback history but must not be active.
for forbidden in ('from rating_lists_ui_integration import apply as apply_rating_lists_ui','apply_rating_lists_ui()'):
    if forbidden in ENTRY: raise SystemExit(f'LINUX_UI_FORK_ACTIVE: {forbidden}')
if 'apply_shared_source()' not in ENTRY: raise SystemExit('MISSING_SHARED_SOURCE_ENTRY')
if '/source/webview/CloudWorkspaceRedesign.js' not in SHARED: raise SystemExit('MISSING_SHARED_STACK')

type_b=MANIFEST.get('authoritativeTypeB') or {}
if type_b.get('path')!='ChessPublisher-Beta81-TypeB-RatingLists.js': raise SystemExit('TYPE_B_PATH_CHANGED')
if type_b.get('sha256')!='3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96': raise SystemExit('TYPE_B_HASH_CHANGED')
if MANIFEST.get('baseRelease')!='v1.06.00-beta.85': raise SystemExit('WRONG_SHARED_BASE')
print('BETA85_SHARED_RATING_LISTS_UI_CONTRACT=PASS')
