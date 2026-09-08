# Linux changelog

## v1.06.00-beta.34-linuxdev21
- Fluidity v2 integrated.
- Pairings Result Desk fixed; board table scrolls independently.
- Chess-Results main tab kept visible.
- Clean tab navigation skips redundant full persistence.
- Stale view-only rendering guarded.
- Linux Ubuntu Acceptance #242 SUCCESS.
- Ubuntu 24.04/26.04 install gates PASS.
- TRF16/TRF26 PASS.
- Chess-Results secure Worker contract PASS.
- Gacrux 1.9.57 / BBP / Tie-Break PASS.

## v1.06.00-beta.34-linuxdev22 — in progress
- Dedicated `kbilyal/ChessPublisher-Linux` repository established as Linux source of truth.
- Added integrated FIDE Standard/Rapid/Blitz local reference database.
- Added generation-based SQLite index with exact FIDE-ID lookup.
- Added Unicode NFKD case/accent/punctuation-normalized name search.
- Added atomic three-list activation; any failed download/parse/index keeps the previous complete generation.
- Added persistent update metadata/checksums and human-readable last successful update report.
- Rating-list update explicitly does **not** mutate tournament players.
- Added Linux UI adapter: Standard/Rapid/Blitz cards, `Update Rating Lists`, `View Last Update Report`, `Review Player Updates`.
- Linux search now uses the integrated LocalEngine database first instead of scanning/rebuilding the giant browser FIDE map.
- Manual/offline rating-list import remains available as fallback.
- Added `/fide/rating-lists/status` and `/fide/rating-lists/report` LocalEngine endpoints.
- Made dev21 runtime materialization non-destructive: immutable baseline is created in a separate runtime folder, protected source is verified, then current repo deltas are overlaid.
- Linux Rating Lists CI #1 PASS: parser/store/search/atomic rollback.
- Linux Rating Lists CI #2 PASS: UI/status/report/server-search contracts.
- Linux Rating Lists CI #3 PASS: continuity/materializer contract.
- Full protected Linux acceptance is still pending; dev22 is not yet a release/test candidate.
