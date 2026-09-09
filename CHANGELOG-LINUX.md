# Linux changelog

## v1.06.00-beta.34-linuxdev23 — HOSTED ACCEPTANCE PASSED / TEST DEVELOPMENT
- Replaced the normal directional `Upload Current` / `Pull Current` workflow with one explicit `SYNC` control.
- Kept the existing canonical Cloud identity model; no second ID model was introduced.
  - `cloud.internalId` / Cloud `localKey` remain the stable logical identity.
  - `cloud.cloudTournamentId` remains the linked Cloud object identity.
  - Rename, revision, filename and import origin do not change identity.
- `SYNC` delegates BASE/LOCAL/REMOTE classification and field-level merge to the existing directional engine.
  - Desktop-only change -> push.
  - Cloud-only change -> pull.
  - No change -> In Sync.
  - Non-overlapping two-sided changes -> safe merge and push in one SYNC operation.
  - Same-field divergence -> explicit conflict resolution; no silent overwrite.
- Removed normal `Upload as New` access for an already linked current tournament and hides obsolete `Upload Current` / `Pull Current` controls.
- Removed the `Public List` block from the Linux normal Cloud UI.
- `Refresh` now reuses the existing My Online Tournaments list refresh and status check only. It never performs hidden push/pull or resolves conflicts.
- Autosave remains local-only.
- `Download Results` remains a separate results-only action.
  - Exact board number + White/Black key identity only.
  - Web blank result never deletes a Desktop result.
  - Pairing mismatch is skipped; no guessing or color swapping.
  - Only `board.result` may change.
  - Result conflicts use explicit `Keep Desktop` / `Use Web` buttons instead of OK/Cancel semantics.
  - Accepted result decisions are saved locally and passed through the same unified Cloud SYNC before pending Web submissions can be acknowledged.
  - If SYNC does not reach `In Sync`, the local decision stays saved but the Web submission remains pending for safe retry.
- Added `cloud_sync_dev23_regression.mjs` covering the 21 requested identity/sync/result/Refresh/Autosave contracts.
- No protected source/core was modified.

### Accepted hosted gates
- Implementation commit: `39d698a1f6dd3015313d0113540212afb596bc2b`.
- Linux Web Results Download #7 (`34373652482`): **SUCCESS**.
- Linux Rating Lists #10 (`34373652481`): **SUCCESS**.
- Linux Full Protected Acceptance #24 (`34373652571`): **SUCCESS**.
- Full gate passed real Chromium UI, FIDE/Rating Lists, Chess-Results/LocalEngine, Ubuntu 24.04, Ubuntu 26.04, TRF16, TRF26, Gacrux 1.9.57, BBP and Tie-Break.
- Runtime-only artifact: `chess-publisher-linux-dev23-runtime-only-kit`, ID `10113058905`, digest `sha256:9cd3f054e1a259902ed54c3a6fb6dd32fa37c8d724b322b13050033f880896e0`.
- Acceptance report: `linux-dev23-full-acceptance-report`, ID `10113056566`, digest `sha256:372f08eba086b4c702a6b03d7182e18e8d33da9e5f3b4090a7159d89a41f75fd`.
- Status remains **TEST DEVELOPMENT**, not final/stable: exact protected-source dev23 packaging and real Ubuntu user runtime confirmation are still required.

## v1.06.00-beta.34-linuxdev22 — TEST CANDIDATE
- Dedicated `kbilyal/ChessPublisher-Linux` repository established as Linux source of truth.
- Added integrated FIDE Standard/Rapid/Blitz local reference database with generation-based SQLite, atomic activation and rollback safety.
- Added Pairings `Download Results` for pending Arbiter Access Web results with result-only matching/mutation safety.
- Reworked protected-source materialization to fail closed and retain exact SHA256-pinned source identity.
- Linux Full Protected Acceptance #17 (`34359612332`) SUCCESS at runtime commit `eeb30c4cb08ec4dd760b1af800c5d3c56700c557`.
- Exact dev22 protected-source package self-test PASS; dev22 remained a test candidate, not final/stable.

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
