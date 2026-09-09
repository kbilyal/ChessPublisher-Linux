# AI HANDOFF — READ THIS FIRST

Continue Chess-Publisher as ONE Windows/Linux product. Linux code changes remain in `kbilyal/ChessPublisher-Linux`, branch `main`, until repository consolidation is explicitly approved.

## Current directive
The active cross-platform target is **v1.06.00-beta.85**. Do not return to a separate `linuxdev` forward line and do not reconstruct Windows beta.82-beta.85 behavior manually. Shared tournament/business behavior must come from the exact authoritative Windows beta.85 source identity; Linux code is platform/native adaptation only.

## Current Windows reference
- Version: `v1.06.00-beta.85`.
- Repo: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`.
- Authoritative source commit: `1354a8061fbbc520ecd1ea09b93350e388428dfd`.
- Source archive: `Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz`.
- Source SHA256: `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`.
- Source size: `27933592` bytes.
- Cloud fingerprint content schema: **7**, unchanged.
- Cloud API/protocol: unchanged.
- beta.85 SYNC: `BOTH_CHANGED` attempts deterministic three-way merge; independent Desktop/Web changes merge-push, true same-field conflicts remain fail-closed.
- Windows targeted evidence: beta.85 next-round SYNC 8/8 PASS; beta.84 schema-7 unified SYNC 18/18 PASS.
- Windows cumulative regression: 73 PASS / 3 approved historical / 1 designated skip / 0 unexpected.
- Q18 remains external TEC; never self-mark it PASS.

## Linux beta.85 hosted alignment
Active Linux version files and build identity are beta.85. Shared WebView/Hub/Cloud logic is loaded through `linux/shared_source_integration.py`; the entrypoint does **not** activate Linux-specific Cloud directional/unified-sync, Web-results, or rating-list UI business forks.

Accepted hosted checkpoint before this documentation commit:
- implementation: `249469275061581edd822870d0797ebf6c7a9617`
- accepted hosted HEAD: `a19155fa2002d8175f3db4ba046cdba903d172bf`
- Linux beta.85 Platform Acceptance #42, run `34406223149`: PASS
- Cross-Platform Parity #38, run `34406223165`: PASS
- Linux Rating Lists #16, run `34406223143`: PASS
- Linux Web Results #10, run `34406223189`: PASS

Platform Acceptance #42 passed beta.85 source/alignment guards, fail-closed materialization, adapter order, compile, native integration contracts, real Chromium, FIDE/rating data, Chess-Results/LocalEngine, Ubuntu 24.04, Ubuntu 26.04, TRF16/TRF26, Gacrux 1.9.57, BBP and Tie-Break.

Artifacts:
- `chess-publisher-linux-beta85-platform-only-kit`, ID `10125532864`, digest `sha256:ef9ee9136b79bf86f15f52265b20f987a4ab6e1734bb24314f4513b08103fe35`
- `linux-beta85-platform-acceptance-report`, ID `10125531728`, digest `sha256:a691165aabfe9f41ce4cc89d60b74c6f8485bd2a8af8e4261962e5b8d0b145bb`

## Important evidence boundary
**beta.85 is NOT a Linux release candidate yet.** The exact beta.85 authoritative source archive is visible in the connected Google Drive release folder with the expected size, but raw download/materialization through the connected provider returns HTTP 403 because Google has flagged the binary/archive. Therefore:
- do not claim exact beta.85 shared-source byte parity on Linux;
- do not claim an exact beta.85 `.deb` exists;
- do not set `releaseCandidate=true`;
- do not call beta.85 Final/Stable.

The last fully proven exact-shared-source Windows/Linux parity anchor remains **v1.06.00-beta.81**:
- Linux commit `30c6b924e11b9ebcd1ef2337761640c02cc1e580`
- Platform Acceptance `34384400988`: PASS
- Windows/Linux matrix: 20/20 PASS
- first managed Linux beta.81 `.deb` SHA256 `be2015aec5b1f64490cd1496ffe2323bbadf898285007f8afdca00c48c29addc`

Legacy `v1.06.00-beta.34-linuxdev23` / `39d698a1f6dd3015313d0113540212afb596bc2b` remains rollback-only and must never become forward source lineage.

## Shared protected/business logic
Do not create Linux-specific versions of Gacrux 1.9.57 / Swiss Dutch pairing, TRF16/TRF26 or TRF pairing path, BBP, Tie-Break, Chess-Results protocol/core, player/pairing identity, rating-list semantics, TEC/FIDE warning logic, tournament file format, Cloud tournament identity or unified SYNC behavior.

Platform-specific code is limited to launcher/runtime, browser/WebView shell, filesystem/dialogs, printing/PDF integration, hardware bridge and installers/packages.

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
Obtain readable bytes of the exact beta.85 authoritative source archive. Verify the archive SHA256 before extraction, materialize only manifest-listed shared files, run source guard + exact-source regressions + package acceptance, build a beta.85 Ubuntu `.deb`, and require real Ubuntu install/start confirmation before any release-candidate promotion.
