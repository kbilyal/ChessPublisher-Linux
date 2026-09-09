# AI HANDOFF — READ THIS FIRST

Continue Chess-Publisher Linux only from `kbilyal/ChessPublisher-Linux`, branch `main`.

## Current development state
- Version: `v1.06.00-beta.34-linuxdev23`.
- Status: **HOSTED ACCEPTANCE PASSED / TEST DEVELOPMENT**, not final/stable.
- Accepted dev23 runtime commit: `39d698a1f6dd3015313d0113540212afb596bc2b`.
- Linux Full Protected Acceptance #24, run `34373652571`: **SUCCESS**.
- Accepted runtime-only artifact: `chess-publisher-linux-dev23-runtime-only-kit`, artifact ID `10113058905`, digest `sha256:9cd3f054e1a259902ed54c3a6fb6dd32fa37c8d724b322b13050033f880896e0`.
- Targeted Linux Web Results Download #7, run `34373652482`: **SUCCESS**.
- Targeted Linux Rating Lists #10, run `34373652481`: **SUCCESS**.
- The last exact protected-source `.deb` is still dev22. Do not call dev23 final/stable until an exact dev23 package is built and the real app is installed/started/tested on Ubuntu.
- Always inspect the actual current `main` HEAD before writing. Repository state overrides old chat context.

## Start every new agent/chat here
1. Read `CURRENT_STATE.json`.
2. Read `AI_HANDOFF.md`.
3. Read `CHANGELOG-LINUX.md`.
4. Read `docs/PROTECTED_COMPONENTS.md`.
5. Inspect current `main` HEAD and recent commits.
6. Materialize only through `scripts/bootstrap_dev21_from_upstream.py`.

## dev23 Cloud synchronization
- Normal Linux Cloud control is one `SYNC` button.
- Do not restore separate normal `Upload Current`, `Pull Current` or `Upload as New` workflows.
- Do not introduce a second tournament identity model.
- Canonical identity remains the existing directional model: `cloud.internalId` / Cloud `localKey` plus `cloud.cloudTournamentId` after linking.
- Identity must never depend on name, filename, `Imported`, revision or where the tournament was created.
- The existing directional engine owns BASE/LOCAL/REMOTE using `baseRevision`, historical Cloud revision and content fingerprints.
- `SYNC` behavior:
  - LOCAL only -> push;
  - REMOTE only -> pull;
  - same -> In Sync;
  - non-overlapping two-sided changes -> field merge then push in the same SYNC;
  - same-field divergence -> explicit Keep Desktop / Keep Cloud conflict resolution; never silently choose.
- `Refresh` is not SYNC. It refreshes My Online Tournaments/list metadata and Cloud status only; it must not push, pull, change current tournament or resolve conflicts.
- Autosave remains local-only.
- `Public List` is not part of the normal Linux Cloud UI.

## dev23 Download Results
- `Download Results` remains in Pairings and is results-only.
- Selected editable round only.
- Exact board number + `whiteKey` + `blackKey`; do not infer, swap colors or remap pairings.
- Blank Desktop + Web result -> Web may fill.
- Same -> no board change.
- Different populated results -> explicit `Keep Desktop` / `Use Web` buttons.
- Blank Web never erases Desktop.
- Mutation boundary is **only** `board.result`.
- Critical ordering: save accepted local result decisions -> unified SYNC on the same canonical Cloud identity -> verify `In Sync` -> ACK pending Web submissions.
- If SYNC fails/conflicts/offline, local changes may remain saved but Web submissions must remain pending for retry.

## dev23 accepted hosted gates
Linux Full Protected Acceptance #24 passed all required hosted stages:
- materialization / source-policy contracts;
- deterministic Linux integration contracts including the 21 requested sync/result cases;
- real Chromium UI;
- FIDE and integrated Rating Lists;
- Chess-Results and LocalEngine;
- Ubuntu 24.04 install/self-test;
- Ubuntu 26.04 install/self-test;
- TRF16 / TRF26;
- Gacrux 1.9.57 / BBP / Tie-Break.

Acceptance report artifact: `linux-dev23-full-acceptance-report`, ID `10113056566`, digest `sha256:372f08eba086b4c702a6b03d7182e18e8d33da9e5f3b4090a7159d89a41f75fd`.

## Protected-source/materialization rule
The upstream Git root does not contain the exact protected source used by the accepted Linux package. Never substitute the old root `ChessPublisher.html`.
- Immutable source baseline: `kbilyal/ChessPublisher@5e0b37708cbef2828ec60d7e6faa247d4ecc904d`.
- Protected snapshot: `cp-v1.06.00-beta.34-linux-source-20260907`.
- Protected recovery archive SHA256: `19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff`.
- Hosted CI may materialize runtime-only with `protectedSourceVerified=false`; exact package candidates require verified protected source.

## Last exact package baseline
- Version: `v1.06.00-beta.34-linuxdev22`.
- File: `Chess-Publisher-v1.06.00-beta.34-linuxdev22-Ubuntu-amd64.deb`.
- SHA256: `c1ecf6cf9936735a526a4e9c9eb28363d52a867a415b0142188538fa85f5e01a`.
- This remains the last exact protected-source package until dev23 is packaged.

## Protected components — do not modify without explicit approval
- Gacrux 1.9.57.
- Swiss Dutch pairing.
- TRF16/TRF26 core and TRF pairing path.
- BBP checker.
- Tie-Break core/checker.
- Chess-Results protocol/core.
- Player/pairing identity semantics.
- Tournament file format.

## Git rule
Every completed Linux fix must be committed and pushed to `ChessPublisher-Linux/main`. No force push. Re-read HEAD before branch update and never overwrite a concurrent commit.

## Next gate
Build an exact protected-source dev23 Ubuntu test candidate from accepted runtime commit `39d698a1f6dd3015313d0113540212afb596bc2b`. Then install/start/test the real app on Ubuntu before any final/stable promotion.
