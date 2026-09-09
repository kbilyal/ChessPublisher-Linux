# Checkpoint — exact beta.81 shared source verified

Date: 2026-09-09
Status: **SOURCE VERIFIED / MIGRATION INPUT ACCEPTED — NOT YET LINUX PARITY COMPLETE**

## Authoritative migration input
- `Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz`
- SHA256: `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`
- Internal `VERSION.txt`: `1.06.00-beta.81`
- Source was extracted into a completely fresh migration workspace.

## Type-B authoritative inputs
- `ChessPublisher-Beta81-TypeB-RatingLists.js`
  - SHA256: `3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96`
- `beta81-type-b-rating-lists.patch`
  - SHA256: `3baad0a3ded7b70db47100591fad04d9291e946ad51b4e7afb201cdca8de06e9`

All supplied SHA256 values match exactly. The source blocker is closed.

## Exact source lineage check
The supplied beta.80 fallback source was also verified (`b027ce2442459cc7dedaa8fd99c0b4a38cc30d822629318dd4f4341b37784101`) and compared to beta.81. Beta.81 differs in exactly 15 files: beta.81 evidence/report files, Type-B module/test/patch, release markers, and three small source/test changes. No manual beta.35-beta.81 reconstruction is required or permitted.

## Linux beta.34 source-path comparison
Against the previous Linux beta.34 protected-source manifest:
- byte-identical: `cloud/client/cloud-workspace-api.js`, `hub/client/hub-snapshot.js`, `webview/CloudWorkspaceAdapter.js`, `webview/HubAdapter.js`, `webview/WebViewAdapter.js`;
- authoritative shared-source evolution: `ChessPublisher.html`, `hub/client/hub-api-client.js`.

These two differences are accepted only because they come from the hash-verified exact beta.81 authoritative source; they are not Linux-local rewrites.

## beta.81 protected-core evidence
The source contains `BETA81-PROTECTED-CORE-HASH-CHECK.log` with the Windows beta.81 protected gate reporting all listed protected components `OK`, and the beta.81 checkpoint records protected core `70/70 byte-identical` versus its parent protected baseline.

## Rollback
The accepted `v1.06.00-beta.34-linuxdev23` runtime remains untouched as rollback baseline.

## Next block
Rebase only Linux-specific adapters/runtime around the exact beta.81 shared source. Do not fork pairing, TRF, tie-break, rating-list semantics, Chess-Results, Cloud identity, player identity, or pairing identity.
