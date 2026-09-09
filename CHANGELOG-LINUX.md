# Linux changelog

## v1.06.00-beta.85 — HOSTED PLATFORM ALIGNMENT PASS / EXACT-SOURCE PACKAGE PENDING
- Advanced the active Linux product/version target from the beta.81 parity anchor to the current authoritative Windows `v1.06.00-beta.85` line.
- Pinned Windows beta.85 source commit `1354a8061fbbc520ecd1ea09b93350e388428dfd`, authoritative archive SHA256 `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`, and Cloud fingerprint schema 7.
- Replaced the beta81-named delivery adapter with generic `shared_source_integration.py`; it is platform transport only and loads the shared WebView/Hub/Cloud stack in Windows-compatible order.
- Active Linux entrypoint no longer enables Linux-specific Cloud directional/unified SYNC, Web-results, or rating-list UI business forks. Native Linux rating-data backend remains platform infrastructure.
- Updated fail-closed source guard/bootstrap/materializer for exact beta.85 identity. Older beta.81/beta.34/upstream-root shared source cannot silently substitute.
- The beta.85 materializer copies only manifest-listed shared files from the authoritative Windows source; Windows binaries/launchers are not copied into Linux runtime.
- Updated legacy Web-results and Rating Lists regression contracts so rollback safety remains tested while active beta.85 business/UI semantics are required to come from shared source.
- No Gacrux 1.9.57, Swiss Dutch pairing, TRF16/TRF26, TRF pairing path, BBP, Tie-Break, Chess-Results protocol/core, player/pairing identity or tournament-file core was changed.

### Accepted hosted gates
- Implementation commit: `249469275061581edd822870d0797ebf6c7a9617`.
- Accepted hosted test commit: `a19155fa2002d8175f3db4ba046cdba903d172bf`.
- Linux beta.85 Platform Acceptance #42 (`34406223149`): **SUCCESS**.
- Cross-Platform Parity #38 (`34406223165`): **SUCCESS**.
- Linux Rating Lists #16 (`34406223143`): **SUCCESS**.
- Linux Web Results #10 (`34406223189`): **SUCCESS**.
- Platform gate passed real Chromium, FIDE/Rating Lists, Chess-Results/LocalEngine, Ubuntu 24.04, Ubuntu 26.04, TRF16/TRF26, Gacrux 1.9.57, BBP and Tie-Break.
- Platform-only artifact: `chess-publisher-linux-beta85-platform-only-kit`, ID `10125532864`, digest `sha256:ef9ee9136b79bf86f15f52265b20f987a4ab6e1734bb24314f4513b08103fe35`.
- Acceptance report: ID `10125531728`, digest `sha256:a691165aabfe9f41ce4cc89d60b74c6f8485bd2a8af8e4261962e5b8d0b145bb`.

### Remaining gate
The exact beta.85 source archive is present in Google Drive but connected raw materialization returns provider HTTP 403. Therefore this is **not** an exact-source Linux beta.85 package/release checkpoint yet. No beta.85 `.deb` is claimed and `releaseCandidate=false` remains mandatory.

## v1.06.00-beta.81 — EXACT SHARED-SOURCE PARITY ANCHOR
- Exact Windows/Linux shared source parity proven: 574/574 authoritative shared files byte-identical.
- Linux commit `30c6b924e11b9ebcd1ef2337761640c02cc1e580`; Platform Acceptance `34384400988` PASS; Windows/Linux matrix 20/20 PASS.
- First managed Linux beta.81 `.deb` SHA256: `be2015aec5b1f64490cd1496ffe2323bbadf898285007f8afdca00c48c29addc`.
- Remains the last fully proven exact-source rollback/parity anchor until beta.85 exact-source proof is completed.

## v1.06.00-beta.34-linuxdev23 — LEGACY ROLLBACK
- Accepted runtime commit: `39d698a1f6dd3015313d0113540212afb596bc2b`.
- Hosted Full Protected Acceptance #24 (`34373652571`): SUCCESS.
- This line is rollback history only and must not be used as forward source lineage.
