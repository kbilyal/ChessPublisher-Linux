# AI HANDOFF — READ THIS FIRST

You are continuing Chess-Publisher Linux from the dedicated authoritative repository:
`kbilyal/ChessPublisher-Linux`, branch `main`.

## Current development state
- Version: `v1.06.00-beta.34-linuxdev22`
- Known development head when this handoff was updated: `e55db834915a8850640bf82a9b20c3c8e3a51103`
- dev21 immutable baseline: `kbilyal/ChessPublisher@5e0b37708cbef2828ec60d7e6faa247d4ecc904d`
- dev21 Linux Ubuntu Acceptance #242: SUCCESS
- dev22 Rating Lists CI #1, #2 and #3: SUCCESS
- dev22 full protected Linux acceptance: NOT YET RUN/FINISHED

Always inspect the actual current Git HEAD before writing; it may be newer than the SHA above.

## Start every new chat/agent here
1. Read `CURRENT_STATE.json`.
2. Read `CHANGELOG-LINUX.md`.
3. Read `docs/PROTECTED_COMPONENTS.md`.
4. Read `docs/RATING_LIST_INTEGRATION_PLAN.md`.
5. Inspect current `main` HEAD and recent commits.
6. Materialize a complete runtime only through `scripts/bootstrap_dev21_from_upstream.py --output <dir>` when needed.

The materializer is deliberately non-destructive: it reconstructs the exact tested dev21 runtime in a separate directory, verifies protected source hashes, then overlays the current dedicated-repository `linux/` and `tests/` deltas. Never replace the repo's current Linux files with old dev21 files.

## Mandatory Git rule
Every completed Linux fix must be committed and pushed here before it is reported as complete.
No force push. Re-read branch HEAD before updating the ref. Never overwrite concurrent commits.

## Release rule
Never call a build final/stable merely because it launches. Do not call dev22 a test candidate until the full protected Ubuntu/Chromium/FIDE/Chess-Results/TRF/Gacrux gate is green.

## Protected components
Do not modify unless explicitly authorized:
- Gacrux 1.9.57
- Swiss Dutch pairing
- TRF16/TRF26 core
- BBP checker
- Tie-Break core/checker
- Chess-Results protocol/core

## dev22 Rating Lists architecture already implemented
- Standard / Rapid / Blitz providers.
- Installation-local generation-based SQLite reference database.
- Exact FIDE-ID lookup.
- Case/accent/punctuation tolerant normalized name search.
- Explicit full update only; no full network download on startup.
- Three-list atomic activation and previous-generation rollback safety.
- Persistent status/metadata/checksums/update report.
- Linux UI cards and explicit `Review Player Updates` action.
- Full rating-list update does NOT mutate `tournament.players`.
- On Linux, full update/search are server-authoritative; the automatic update does not sequentially rebuild the huge browser-side FIDE map.
- Manual/offline lists remain fallback.

## Next task
Materialize the full current runtime, run the complete protected acceptance suite, fix only dev22 integration defects if any, update CURRENT_STATE/CHANGELOG, and only after a fully green run build the dev22 `.deb` TEST CANDIDATE with exact SHA256.
