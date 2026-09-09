# AI HANDOFF — READ THIS FIRST

You are continuing Chess-Publisher Linux from the dedicated authoritative repository:
`kbilyal/ChessPublisher-Linux`, branch `main`.

## Current development state
- Version: `v1.06.00-beta.34-linuxdev22`
- Status: **TEST CANDIDATE** — not final/stable yet.
- Always inspect the actual current Git HEAD before writing; documentation commits may be newer than the accepted runtime commit.
- Accepted dev22 runtime commit: `eeb30c4cb08ec4dd760b1af800c5d3c56700c557`.
- dev22 Linux Full Protected Acceptance #17, run `34359612332`: **SUCCESS**.
- Continuity Recovery Probe #2, run `34359640237`: **SUCCESS**.
- dev21 immutable baseline: `kbilyal/ChessPublisher@5e0b37708cbef2828ec60d7e6faa247d4ecc904d`.
- dev21 Linux Ubuntu Acceptance #242: SUCCESS.

## Start every new chat/agent here
1. Read `CURRENT_STATE.json`.
2. Read `CHANGELOG-LINUX.md`.
3. Read `docs/PROTECTED_COMPONENTS.md`.
4. Read `docs/RATING_LIST_INTEGRATION_PLAN.md`.
5. Inspect current `main` HEAD and recent commits.
6. Materialize through `scripts/bootstrap_dev21_from_upstream.py` only.

## Materialization / protected-source rule
The upstream git root does **not** contain the exact protected source used by the accepted Linux package. Never substitute its old `ChessPublisher.html`.

The materializer is non-destructive and fail-closed:
- reconstructs the immutable dev21 runtime in a separate output directory;
- overlays current dedicated-repo Linux/tests/scripts deltas;
- accepts exact protected source through `--source-archive`, `--source-root`, or `CP_PROTECTED_SOURCE_ARCHIVE`;
- hosted CI may use `--allow-source-unavailable`, which must record `protectedSourceVerified=false` and must not stage a fake protected source;
- exact package candidates require the separately verified protected source.

Protected recovery archive identity:
- name: `Chess-Publisher-v1.06.00-beta.34-protected-source.tar.gz`
- SHA256: `19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff`
- source snapshot: `cp-v1.06.00-beta.34-linux-source-20260907`

## Mandatory Git rule
Every completed Linux fix must be committed and pushed here before it is reported as complete.
No force push. Re-read branch HEAD before updating. Never overwrite concurrent commits.

## Release rule
The current dev22 package is a **TEST CANDIDATE**. Do not promote it to final/stable until the user installs it on Ubuntu, starts the real app, and confirms runtime behavior. A successful launch alone is not permission to modify protected core.

## Protected components
Do not modify unless explicitly authorized:
- Gacrux 1.9.57
- Swiss Dutch pairing
- TRF16/TRF26 core
- BBP checker
- Tie-Break core/checker
- Chess-Results protocol/core

## dev22 Rating Lists
Already implemented and accepted:
- Standard / Rapid / Blitz providers.
- Installation-local generation-based SQLite reference database.
- Exact FIDE-ID lookup.
- Case/accent/punctuation tolerant normalized name search.
- Explicit full update only; no full network download on startup.
- Three-list atomic activation and previous-generation rollback safety.
- Persistent status/metadata/checksums/update report.
- Linux UI cards and explicit `Review Player Updates` action.
- Full rating-list update does NOT mutate `tournament.players`.
- Linux full update/search are server-authoritative.
- Manual/offline lists remain fallback.

## Pairings Download Results
Already implemented and accepted:
- Button: `Download Results` in Pairings toolbar.
- Source: pending Arbiter Access Web result queue (`/arbiter-results`), not the ordinary Cloud snapshot.
- Selected editable round only.
- Exact `whiteKey + blackKey` board identity.
- Blank Desktop + Web result => apply Web automatically.
- Same => no change.
- Different populated results => ask which stays, Web or Desktop.
- Blank Web never erases Desktop.
- Pairing mismatch => skip; never infer or swap colors.
- Mutation boundary: `board.result` only.
- Pending Web submissions are acknowledged only after local save succeeds; ack failure leaves them available for retry.
- Targeted Linux Web Results Download CI #5, run `34334839940`: SUCCESS.

## Accepted dev22 runtime gate
Linux Full Protected Acceptance #17, run `34359612332`, runtime commit `eeb30c4cb08ec4dd760b1af800c5d3c56700c557`: SUCCESS.
The run passed:
- fail-closed materialization;
- dev22 deterministic contracts;
- adapter/source-policy contracts;
- Chromium UI;
- FIDE + integrated Rating Lists;
- Chess-Results + LocalEngine;
- Ubuntu 24.04 + Ubuntu 26.04 install/self-test;
- TRF16/TRF26;
- Gacrux 1.9.57 / BBP / Tie-Break.

Accepted runtime-only artifact:
- name `chess-publisher-linux-dev22-runtime-only-kit`
- artifact ID `10107299648`
- digest `sha256:5752152277a5f91cad6887e8894037c39846d7521a0c0f337e0a62b308a568ac`

## Exact dev22 package candidate
Built from the accepted runtime-only artifact + exact protected source.
- file: `Chess-Publisher-v1.06.00-beta.34-linuxdev22-Ubuntu-amd64.deb`
- package version: `1.06.00~beta34+linuxdev22`
- architecture: `amd64`
- bytes: `31814980`
- SHA256: `c1ecf6cf9936735a526a4e9c9eb28363d52a867a415b0142188538fa85f5e01a`
- app build: `1.06.00-beta.34-linux-dev.22`
- engine: `0.7.0-linux-dev`
- runtime files: 51
- FIDE seed files: 3
- bytecode included: false
- exact protected source verification: PASS
- extracted-package self-test: **PASS — 6 passed, 0 failed**

## Next task
Have the user install/start the exact dev22 `.deb` test candidate on Ubuntu and test the real UI, especially Pairings `Download Results`, Result Desk, Chess-Results visibility, Cloud/Arbiter result flow, and normal tournament persistence. If that runtime gate passes, record the confirmation and decide on promotion without rebuilding or touching protected core.
