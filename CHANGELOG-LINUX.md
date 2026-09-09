# Linux changelog

## v1.06.00-beta.85 — EXACT-SOURCE ONLINE HUB FIX TEST CANDIDATE PASS
- Advanced the active Linux product/version target from the beta.81 parity anchor to the authoritative Windows `v1.06.00-beta.85` line.
- Exact authoritative source archive verified: `Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz`, `27933592` bytes, SHA256 `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`.
- Runtime shared source guard verified **40/40** manifest-listed files. `ChessPublisher.html` is `1592803` bytes with SHA256 `2a0437da7d6ae20f04cf4499ba36b6c7c81698c1517b390b1fed6f3775f5a175`.
- Cloud fingerprint content schema remains **7**. Shared Hub/Cloud/SYNC, Web Results, player/pairing identity and tournament business logic remain authoritative shared beta.85 code.
- Fixed a Linux-only navigation regression that hid the dynamically created `Online & Cloud (Beta)` tab. Root cause: Linux fluid navigation was fixed to an eight-column grid with clipped overflow while beta.85 `HubAdapter.js` adds `#tabHub` as the ninth primary tab.
- Added `linux/hub_tab_visibility_integration.py`: primary navigation now uses nine columns and explicitly keeps `#tabHub` visible. The adapter changes presentation/delivery only and loads before final `apply_shared_source()`.
- Added real Chromium regression `ci/hub_tab_browser_contract.py`, which dynamically adds the ninth Hub tab and verifies it remains single-row, visible, inside the navigation viewport and clickable.
- Added adapter-order/layout guard so the Hub visibility fix cannot become a Linux business fork or load after shared source.
- No Gacrux 1.9.57, Swiss Dutch pairing, TRF16/TRF26, TRF pairing path, BBP, Tie-Break, Chess-Results protocol/core, player/pairing identity or tournament-file core was changed.

### Online Hub fix commits
- `50af24a898195df53c5f0948b057e900a5eede1f` — Linux Online Hub visibility adapter.
- `84673811c664463b187cbf44699a4e45f9e6d3f6` — wire Hub visibility adapter before final shared-source delivery.
- `aa9300461989d22a9722f292b11db728862a004b` — real Chromium dynamic ninth-tab regression.
- `123dcf71a84756f1c66468244980e6dc6d8d7e96` — adapter-order/layout guard.
- `8f6586868c92536e4141765fce3099b2f0ed7350` — accepted hosted code checkpoint.

### Accepted hosted gates after Hub fix
- Linux beta.85 Platform Acceptance #49 (`34410974326`): **SUCCESS**.
- Cross-Platform Parity #48 (`34410974401`): **SUCCESS**.
- Real Chromium: `LINUX_ONLINE_HUB_TAB_BROWSER=PASS` — dynamic ninth tab visible, single-row and clickable.
- Ubuntu 24.04 normal apt install/self-test: **PASS**.
- Ubuntu 26.04 container smoke: **PASS**.
- Gacrux 1.9.57 / BBP 6.0.0 online-engine checks: **PASS**.
- TRF16/TRF26: **PASS**.
- Tie-Break: **27/27 ranks, 0 mismatches**.
- Chess-Results and LocalEngine: **PASS**.
- Platform-only artifact: `chess-publisher-linux-beta85-platform-only-kit`, ID `10127279784`, digest `sha256:c423b779751cd4988b763cd2e529c4059b498948f3ff2f7c43d19aa06c1b3a5b`.
- Acceptance report: ID `10127278461`, digest `sha256:3b8579c3ce317a9494ac5a4de7ca036751f0eb3a81a26355f88c95380a1af537`.

### Exact-source Ubuntu test candidate
- File: `Chess-Publisher-v1.06.00-beta.85-Ubuntu-amd64-ONLINE-HUB-FIX-EXACT-SOURCE-TEST-CANDIDATE.deb`.
- Size: `55860084` bytes.
- SHA256: `6391da6f16603b6809fe9752d51f6dfa6b8e94b9dc8ba5f66b6783636aaa0b99`.
- Package version: `1.06.00~beta85`.
- Exact shared-source payload: **VERIFIED**.
- Local installed self-test: **6 PASS / 0 FAIL**.
- Bundle: `Chess-Publisher-v1.06.00-beta.85-Ubuntu-amd64-ONLINE-HUB-FIX-EXACT-SOURCE-TEST-CANDIDATE.zip`, SHA256 `a339004e980abf79f5cee8135411489e76f92dd24b8dcf58a2cb40c4bb0a1ce5`.
- Previous beta.85 exact-source candidate SHA256 `aeca57bafa97d6c1fc2b14985041a8d6a215ed50436693e932ab43148d148c74` is **SUPERSEDED** because its Linux eight-column layout hid `Online & Cloud (Beta)`.

### Remaining gate
`releaseCandidate=false` remains mandatory. Install/reinstall the Online Hub fixed exact-source `.deb` on a real Ubuntu machine and confirm application startup, visible/clickable `Online & Cloud (Beta)`, normal existing-tournament loading, Pairings, Standings and Chess-Results. Do not promote Final/Stable before that user runtime confirmation.

## v1.06.00-beta.81 — PREVIOUS EXACT SHARED-SOURCE PARITY ANCHOR
- Exact Windows/Linux shared source parity proven: 574/574 authoritative shared files byte-identical.
- Linux commit `30c6b924e11b9ebcd1ef2337761640c02cc1e580`; Platform Acceptance `34384400988` PASS; Windows/Linux matrix 20/20 PASS.
- First managed Linux beta.81 `.deb` SHA256: `be2015aec5b1f64490cd1496ffe2323bbadf898285007f8afdca00c48c29addc`.
- Retained as the previous exact-source rollback/parity anchor.

## v1.06.00-beta.34-linuxdev23 — LEGACY ROLLBACK
- Accepted runtime commit: `39d698a1f6dd3015313d0113540212afb596bc2b`.
- Hosted Full Protected Acceptance #24 (`34373652571`): SUCCESS.
- This line is rollback history only and must not be used as forward source lineage.
