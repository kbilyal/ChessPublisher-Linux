# AI HANDOFF — READ THIS FIRST

Continue Chess-Publisher as ONE Windows/Linux product. Linux code changes remain in `kbilyal/ChessPublisher-Linux`, branch `main`, until repository consolidation is explicitly approved.

## Current directive
The active cross-platform target is **v1.06.00-beta.85**. Do not create a separate `linuxdev` forward line and do not reconstruct Windows beta.82-beta.85 business behavior manually. Shared tournament/business behavior must come from the exact authoritative Windows beta.85 source identity; Linux code is platform/native adaptation only.

## Exact authoritative beta.85 source — VERIFIED
- Windows repo: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`.
- Authoritative commit: `1354a8061fbbc520ecd1ea09b93350e388428dfd`.
- Archive: `Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz`.
- Size: `27933592` bytes.
- SHA256: `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`.
- Source snapshot: `cp-v1.06.00-beta.85-shared-source-20260909`.
- Runtime shared source guard: **40/40 PASS**.
- `ChessPublisher.html`: `1592803` bytes, SHA256 `2a0437da7d6ae20f04cf4499ba36b6c7c81698c1517b390b1fed6f3775f5a175`.
- Cloud fingerprint content schema: **7**, unchanged.
- The archive bytes were recovered from ChatGPT Library after Google Drive raw download was blocked. The archive size/SHA and all manifest runtime hashes were verified before package build.

## Online & Cloud tab regression — FIXED
User found that the Linux package did not show the Online Hub tab. Root cause was Linux presentation only:
- authoritative beta.85 `HubAdapter.js` dynamically creates `#tabHub` / `Online & Cloud (Beta)`;
- inherited Linux fluid navigation was fixed to `repeat(8, ...)` with `overflow:hidden`;
- the dynamic ninth tab wrapped into a clipped second row.

Fix scope is deliberately Linux-only presentation/delivery:
- `linux/hub_tab_visibility_integration.py` changes the primary navigation grid to 9 columns and explicitly keeps `#tabHub` visible;
- shared `HubAdapter.js`, Cloud schema 7, unified SYNC, Web Results, player/pairing identity, tournament data and protected core are unchanged;
- fix loads before final `apply_shared_source()` so shared beta.85 remains authoritative.

Fix commits:
- `50af24a898195df53c5f0948b057e900a5eede1f` — Linux Hub-tab visibility adapter
- `84673811c664463b187cbf44699a4e45f9e6d3f6` — wire adapter before shared source
- `aa9300461989d22a9722f292b11db728862a004b` — real Chromium dynamic ninth-tab regression
- `123dcf71a84756f1c66468244980e6dc6d8d7e96` — adapter-order/layout guard
- `8f6586868c92536e4141765fce3099b2f0ed7350` — hosted acceptance checkpoint

## Accepted hosted gates after Hub fix
- Cross-Platform Parity #48, run `34410974401`: **PASS**.
- Linux beta.85 Platform Acceptance #49, run `34410974326`: **PASS**.
- Real Chromium: `LINUX_ONLINE_HUB_TAB_BROWSER=PASS` — dynamic ninth tab visible, single-row and clickable.
- Ubuntu 24.04 normal apt install/self-test: PASS.
- Ubuntu 26.04 container smoke: PASS.
- Online engines: Gacrux 1.9.57 PASS; BBP 6.0.0 PASS.
- TRF16/TRF26: PASS.
- Tie-Break: 27/27 ranks, 0 mismatches.
- Chess-Results / LocalEngine: PASS.

Artifacts from Platform Acceptance #49:
- `chess-publisher-linux-beta85-platform-only-kit`, ID `10127279784`, digest `sha256:c423b779751cd4988b763cd2e529c4059b498948f3ff2f7c43d19aa06c1b3a5b`.
- `linux-beta85-platform-acceptance-report`, ID `10127278461`, digest `sha256:3b8579c3ce317a9494ac5a4de7ca036751f0eb3a81a26355f88c95380a1af537`.

## Exact-source Ubuntu test candidate
Use only the Online Hub fixed package:
- `Chess-Publisher-v1.06.00-beta.85-Ubuntu-amd64-ONLINE-HUB-FIX-EXACT-SOURCE-TEST-CANDIDATE.deb`
- size `55860084` bytes
- SHA256 `6391da6f16603b6809fe9752d51f6dfa6b8e94b9dc8ba5f66b6783636aaa0b99`
- package version `1.06.00~beta85`
- exact source payload: verified
- local installed self-test: **6 PASS / 0 FAIL**

Matching bundle:
- `Chess-Publisher-v1.06.00-beta.85-Ubuntu-amd64-ONLINE-HUB-FIX-EXACT-SOURCE-TEST-CANDIDATE.zip`
- SHA256 `a339004e980abf79f5cee8135411489e76f92dd24b8dcf58a2cb40c4bb0a1ce5`

The older exact-source candidate SHA256 `aeca57bafa97d6c1fc2b14985041a8d6a215ed50436693e932ab43148d148c74` is **SUPERSEDED** because it hides the Online & Cloud tab.

## Release boundary
**beta.85 is still NOT Final/Stable and `releaseCandidate=false`.** The remaining gate is a real user Ubuntu install/start test of the fixed exact-source `.deb`:
1. app starts normally;
2. `Online & Cloud (Beta)` is visible on the top navigation row;
3. the tab is clickable and opens the Online/Cloud workspace;
4. an existing tournament opens normally;
5. Pairings, Standings and Chess-Results remain functional.

Only after that real-machine confirmation may beta.85 be considered for release-candidate promotion.

## Shared protected/business logic
Do not create Linux-specific versions of Gacrux 1.9.57 / Swiss Dutch pairing, TRF16/TRF26 or TRF pairing path, BBP, Tie-Break, Chess-Results protocol/core, player/pairing identity, rating-list semantics, TEC/FIDE warning logic, tournament file format, Cloud tournament identity or unified SYNC behavior.

Platform-specific code is limited to launcher/runtime, browser/WebView shell and presentation, filesystem/dialogs, printing/PDF integration, hardware bridge and installers/packages.

Q18 remains external TEC; never self-mark it PASS.

## Read first
1. `CURRENT_STATE.json`
2. `SOURCE-CHECKPOINT.md`
3. `CROSS-PLATFORM-PARITY.md`
4. `TEC-VCL-STATUS.md`
5. `docs/PROTECTED_COMPONENTS.md`
6. actual current `main` HEAD and recent commits

## Git rule
Before every write, re-read `main` HEAD. Every completed logical block: TEST -> REGRESSION -> COMMIT -> PUSH -> verify remote HEAD -> record SHA. Never force push.

## Next logical block
Install/reinstall the fixed exact-source beta.85 `.deb` on a real Ubuntu machine. Confirm the Online & Cloud tab and normal tournament workflow. Do not promote Final/Stable before that user gate.
