#!/usr/bin/env python3
"""Static contract for Linux dev22 integrated rating-list UI adapter."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / 'linux' / 'rating_lists_ui_integration.py'
ENTRY = ROOT / 'linux' / 'chess_publisher_linux_entry.py'


def require(text: str, marker: str) -> None:
    if marker not in text:
        raise SystemExit(f'MISSING: {marker}')


def forbid(text: str, marker: str) -> None:
    if marker in text:
        raise SystemExit(f'FORBIDDEN: {marker}')


def main() -> int:
    ui = UI.read_text(encoding='utf-8')
    entry = ENTRY.read_text(encoding='utf-8')

    for marker in (
        '/fide/rating-lists/status',
        '/fide/rating-lists/report',
        'reportAvailable',
        'tournamentPlayersChanged',
        'LINUX_DEV22_SERVER_ATOMIC_UPDATE',
        "window.downloadAndUpdateFideDatabases=updateRatingLists",
        '/fide/players-search',
        'Integrated Rating Lists',
        'Update Rating Lists',
        'View Last Update Report',
        'Review Player Updates',
        'Tournament data is not changed automatically',
        'Updating rating lists does not automatically modify tournament players',
        'Manual / Offline Lists',
        'Local directory:',
        'serverSearches',
        'searchFallbacks',
    ):
        require(ui, marker)

    # Full automatic Linux updates are server-authoritative. They must not
    # sequentially rebuild the browser FIDE map, which would reintroduce a
    # partial Standard/Rapid/Blitz state on frontend failure.
    forbid(ui, 'replaceFideRatingTypeFromText')
    forbid(ui, 'fideMainDb.clear()')
    forbid(ui, 'saveAll()')
    forbid(ui, 'generatePairings')

    require(entry, 'from rating_lists_ui_integration import apply as apply_rating_lists_ui')
    require(entry, 'apply_rating_lists_ui()')

    print('LINUX_RATING_LISTS_UI_CONTRACT=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
