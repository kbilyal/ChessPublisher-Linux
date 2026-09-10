# beta.85 post-LocalEngine exact-source acceptance checkpoint — 2026-09-10

Status: **TEST CANDIDATE / WINDOWS-LINUX PARITY — NOT FINAL/STABLE**

## Baseline
- Linux `main` HEAD audited before this checkpoint: `c9762644b39175bb1ce92d22b5bf30ba94db8518`
- Target/shared version: `v1.06.00-beta.85`
- Authoritative Windows source commit: `1354a8061fbbc520ecd1ea09b93350e388428dfd`
- Authoritative archive SHA256: `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`
- Shared source guard: `40/40 PASS`
- Cloud fingerprint content schema: `7`

## Findings
No new shared/protected business-logic defect was found on `c976...`.

One release-artifact gap was found: the previously recorded exact-source Online-Hub-fixed package (`6391da6f...`) was built before the later stale-LocalEngine same-version reinstall fix (`2cb772f...` + test hardening `c976264...`). It therefore must not be treated as the package for the current HEAD.

## Exact-source regression rerun
- beta.82 all SYNC/Web Results: `7/7 PASS`
- beta.83 Cloud-only workspace: `7/7 PASS`
- beta.84 schema-7 unified SYNC: `18/18 PASS`
- beta.84 forced checkpoint persistence: `9/9 PASS`
- beta.85 next-round three-way merge: `8/8 PASS`
- cumulative rerun: `73/73` expected current tests PASS; `3` approved historical exceptions; `1` designated browser-runner skip; `0` unexpected

## Current-HEAD Linux/runtime acceptance
Hosted CI on `c976...`:
- Linux beta.85 Platform Acceptance run `34417308670`: PASS
- Cross-Platform Parity Guard run `34417308719`: PASS
- Ubuntu 24.04 install/self-test: PASS
- Ubuntu 26.04 container smoke: PASS
- real Chromium platform/Online & Cloud tab gates: PASS
- Chess-Results / LocalEngine: PASS
- TRF16/TRF26: PASS
- Gacrux 1.9.57 / BBP 6.0.0 / Tie-Break 27/27: PASS

Additional package-level runtime-instance checks on the rebuilt exact-source payload:
- clean/free default port: PASS
- identical current runtime reuse: PASS
- stale same-version runtime bypass: PASS
- unrelated occupied-port bypass: PASS
- matching current runtime preference: PASS
- exhausted scan range fails closed: PASS
- explicit `--port` handling: PASS
- package self-test: `6 PASS / 0 FAIL`
- Linux runtime files in package vs `c976...` platform kit: `57/57` byte-identical

## Protected core
Protected files changed by this work: **NONE**.
Authoritative beta.85 protected comparison remains `70/70 byte-identical; 0 unexpected`.

## New exact-source test candidate
- File: `Chess-Publisher-v1.06.00-beta.85-Ubuntu-amd64-POST-LOCALENGINE-FIX-EXACT-SOURCE-TEST-CANDIDATE.deb`
- Bytes: `55860056`
- SHA256: `a2f4be23d60269a771cf9675660d79e33c0c93b16e717e7ebcb178c02877a348`
- Package version: `1.06.00~beta85`
- Matching evidence ZIP SHA256: `111c540d872511120c113c851e12f75ebc48bff00898ecc117685cf6728e75ed`

## Remaining real-machine gate
Before any Final/Stable or RC promotion, install/start this post-LocalEngine-fix exact-source `.deb` on a real Ubuntu machine and confirm startup, Online & Cloud visibility/clickability, tournament open, Pairings, Standings and Chess-Results.
