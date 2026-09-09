# Chess-Publisher Cross-Platform Parity

Audit update: 2026-09-10
Status: **v1.06.00-beta.85 HOSTED PLATFORM ALIGNMENT PASS / EXACT-SOURCE BYTE PARITY PENDING**

## Product rule
Chess-Publisher is one product with one shared tournament/business core and Windows/Linux platform adapters. Functional release numbering is shared; independent `linuxdev` numbering is rollback history only.

## Active beta.85 target
- Windows version: `v1.06.00-beta.85`
- authoritative Windows source commit: `1354a8061fbbc520ecd1ea09b93350e388428dfd`
- authoritative archive: `Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz`
- archive SHA256: `2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69`
- Cloud fingerprint schema: 7
- Cloud API/protocol: unchanged
- beta.85 SYNC: independent two-sided edits may deterministic three-way merge; true same-field conflicts remain fail-closed.

Linux active version/build metadata and shared-source contract are aligned to beta.85. `source_manifest.json` pins the exact archive and the authoritative hashes for the cumulative shared changes, including:
- `ChessPublisher.html` → `2a0437da7d6ae20f04cf4499ba36b6c7c81698c1517b390b1fed6f3775f5a175`
- `webview/CloudWorkspaceAdapter.js` → `6ce71bd7b4eb4b2401e9ee657f60b308ed6222a162efa0ded925f9b510e9569e`
- `webview/CloudWorkspaceRedesign.js` → `52f39e7c8ab992611f0f9b0eed02836cc19a002016d87b226b94da388f78177a`
- `VERSION.txt` → `b9c3202d834191d9b45d5a9a7ac7bcd93d78d2b059825452194efcc9e4acfd3f`

## Hosted Linux beta.85 acceptance
Accepted hosted HEAD before this documentation checkpoint: `a19155fa2002d8175f3db4ba046cdba903d172bf`.

- Platform Acceptance #42 / `34406223149`: PASS
- Cross-Platform Parity #38 / `34406223165`: PASS
- Rating Lists #16 / `34406223143`: PASS
- Web Results #10 / `34406223189`: PASS

Platform Acceptance #42 covers real Chromium, FIDE/integrated rating data, Chess-Results/LocalEngine, Ubuntu 24.04 install/self-test, Ubuntu 26.04 container smoke, TRF16/TRF26, Gacrux 1.9.57, BBP and Tie-Break. No protected core was changed by the Linux alignment.

## Exact-source evidence boundary
The beta.85 archive is present in the connected Google Drive beta85 release folder and its metadata size matches `27933592` bytes, but raw provider download/materialization returns HTTP 403. Consequently this checkpoint does **not** claim:
- byte-identical beta.85 shared-source runtime on Linux;
- an exact beta.85 Linux `.deb`;
- beta.85 release-candidate/final/stable status.

The Linux materializer remains fail-closed: beta.81, beta.34, or upstream root source cannot silently substitute for beta.85.

## Last fully proven exact-source parity anchor — beta.81
`v1.06.00-beta.81` remains the rollback/proof anchor until the beta.85 archive can be read and verified:
- exact beta.81 shared source: verified
- Linux commit: `30c6b924e11b9ebcd1ef2337761640c02cc1e580`
- Platform Acceptance: `34384400988` PASS
- Windows ↔ Linux acceptance matrix: 20/20 PASS
- authoritative shared files: 574/574 byte-identical
- exact Type-B suite: 29/29 PASS
- beta.81 `.deb` SHA256: `be2015aec5b1f64490cd1496ffe2323bbadf898285007f8afdca00c48c29addc`

Q18 remains external `NEEDS TEC` and is never promoted by local testing.

## Next proof gate
Acquire readable exact beta.85 archive bytes → verify archive SHA256 → materialize exact shared source → verify per-file manifest hashes → rerun exact-source Cloud/SYNC/TEC/protected regressions → build/test beta.85 `.deb` → real Ubuntu install/start confirmation. Only then consider release-candidate promotion.
