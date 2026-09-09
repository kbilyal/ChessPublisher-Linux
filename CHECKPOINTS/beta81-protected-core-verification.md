# Checkpoint — beta.81 protected/shared core verification after Linux adaptation

Date: 2026-09-09
Status: **PASS — no shared-source mutation by Linux adaptation**

## Authoritative input
`Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz`
SHA256 `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`.

## Before/after Linux adaptation
A recursive byte-for-byte comparison was made between the freshly extracted authoritative beta.81 source and the shared source used by the adapted Linux runtime.

- authoritative source files: 574
- Linux shared-source files: 574
- differing files: 0
- result: **574/574 byte-identical**

The Linux delivery/runtime changes are outside the shared source tree. Served HTML is adapted in memory only for platform transport and the exact source on disk is not rewritten.

## Protected invariant paths
The paths that were invariant against the previous Linux source baseline also remain exact:
- `cloud/client/cloud-workspace-api.js` — `733b9f921af5f4986c0ef89df62c650d1e621011b40aeeb02f5ba4ba900a1ab5`
- `hub/client/hub-snapshot.js` — `d980c520d74a71e66b3a3aa2a54e5ed626ea3618c53159145f9e48b445effac9`
- `webview/CloudWorkspaceAdapter.js` — `a25dba042e46d0f120f9cf721b68fdb70178ab323da902bbcc34c42e6947a602`
- `webview/HubAdapter.js` — `e5d61eb452f8b98e70e874cb5a90da2ab6dfe4669c9da363a5047332c9ae62c0`
- `webview/WebViewAdapter.js` — `d23af37ce1624fac96b46f62c85d7801ed733a66f7e03bab40f453ce4db67861`

## Expected shared-source evolution
`ChessPublisher.html` and `hub/client/hub-api-client.js` differ from the old beta.34 Linux snapshot only because the exact beta.81 shared source is authoritative. They were not recreated or edited by Linux migration code.

## Windows beta.81 protected evidence
The exact source carries the beta.81 protected-core gate reporting `70/70 byte-identical` against its accepted parent protected baseline.

## Local verification report
`protected-core-beta81-linux-adaptation.json` SHA256:
`d15060301f098eef92f13440c169f1966589f6fa63dab8c32472af7ddb721f69`.

No unexpected protected/core hash change was found, so migration may continue to TEC/VCL regression.
