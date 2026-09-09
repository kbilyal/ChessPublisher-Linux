# AI HANDOFF — READ THIS FIRST

Continue Chess-Publisher Linux only from `kbilyal/ChessPublisher-Linux`, branch `main`.

## Current development state
- Version: `v1.06.00-beta.34-linuxdev23`.
- Status: **DEVELOPMENT / TEST**, not final/stable.
- The last fully accepted runtime/package baseline remains dev22 until dev23 full protected acceptance and real Ubuntu runtime confirmation pass.
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

## dev23 tests
Targeted pre-commit checks added/passing before branch write:
- 21-point `cloud_sync_dev23_regression.mjs` contract.
- unified SYNC contract.
- Web results reconcile contract.
- pending Web results flow contract.
- result-only static safety contract.
- JavaScript syntax checks.

After the commit, inspect both GitHub workflows:
- `Linux Web Results Download`.
- `Linux Full Protected Acceptance`.
Do not call dev23 accepted until the relevant GitHub runs pass.

## Last accepted dev22 baseline
- Runtime commit: `eeb30c4cb08ec4dd760b1af800c5d3c56700c557`.
- Linux Full Protected Acceptance #17 / run `34359612332`: SUCCESS.
- Runtime-only artifact: `chess-publisher-linux-dev22-runtime-only-kit`, artifact ID `10107299648`, digest `sha256:5752152277a5f91cad6887e8894037c39846d7521a0c0f337e0a62b308a568ac`.
- Last exact package: `Chess-Publisher-v1.06.00-beta.34-linuxdev22-Ubuntu-amd64.deb`, SHA256 `c1ecf6cf9936735a526a4e9c9eb28363d52a867a415b0142188538fa85f5e01a`.

## Protected-source/materialization rule
The upstream Git root does not contain the exact protected source used by the accepted Linux package. Never substitute the old root `ChessPublisher.html`.
- Immutable source baseline: `kbilyal/ChessPublisher@5e0b37708cbef2828ec60d7e6faa247d4ecc904d`.
- Protected snapshot: `cp-v1.06.00-beta.34-linux-source-20260907`.
- Protected recovery archive SHA256: `19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff`.
- Hosted CI may materialize runtime-only with `protectedSourceVerified=false`; exact package candidates require verified protected source.

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
Run and inspect dev23 hosted workflows. If full protected acceptance passes, build an exact protected-source dev23 test candidate, then install/start/test it on Ubuntu before any final/stable promotion.
