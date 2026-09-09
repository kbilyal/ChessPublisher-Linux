# Chess-Publisher Cross-Platform Parity

Audit/closure date: 2026-09-09
Status: **v1.06.00-beta.81 PARITY PASS**

## Product rule
Chess-Publisher is one product with one shared tournament/business core and Windows/Linux platform adapters. Functional release numbering is shared; independent `linuxdev` numbering is legacy rollback history only.

## Authoritative baseline
- Windows/Linux shared version: `v1.06.00-beta.81`
- exact source SHA256: `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`
- exact Type-B module SHA256: `3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96`
- Linux beta.34-linuxdev23: rollback-only

## Shared-source parity
The exact beta.81 Windows source is the Linux functional baseline. After Linux adapter rebasing:
- 574/574 authoritative shared files are byte-identical.
- unexpected shared-source differences: 0.
- protected invariant verification: PASS.
- no Linux-specific pairing/TRF/tie-break/Chess-Results/rating-list/Cloud/player/pairing identity core was created.

## TEC / Type-B
- applicable exact shared TEC regression: 42 PASS / 0 FAIL
- static audit: PASS
- Type-B beta.81 suite: 29/29 PASS
- Q120/Q122: PASS
- Standard/Rapid/Blitz Type-B: PASS
- `originalSourceKnown=false`: PASS
- Q18: external `NEEDS TEC`; Q19-Q39 remain conditional on Q18

## Native Linux platform acceptance
Run `34384400988` at `30c6b924e11b9ebcd1ef2337761640c02cc1e580`: PASS.

Covered: source/adapter guards, Chromium, FIDE/local rating data, Chess-Results, LocalEngine, Ubuntu 24.04 install/self-test, Ubuntu 26.04 container smoke, TRF16/TRF26, Gacrux 1.9.57, BBP 6.0.0 and Tie-Break.

The hosted live FIDE download and raw Drive exact-source UI probe were externally blocked; these were not converted into false product PASS claims. Offline/cache/endpoint/streaming tests passed, and the exact source was independently hash-verified before migration.

## Windows ↔ Linux acceptance matrix
Evidence combines the authoritative Windows beta.81 source/regressions, byte-identical Linux shared source, deterministic cross-platform storage tests and native Linux platform gates. A native Windows executable was not executed inside Linux CI.

| # | Check | Result |
|---:|---|---|
| 1 | Windows-created tournament -> Linux open | PASS |
| 2 | Linux save -> Windows reopen | PASS |
| 3 | Linux-created tournament -> Windows open | PASS |
| 4 | Windows pair round -> Linux same pairings | PASS |
| 5 | Linux pair round -> Windows same pairings | PASS |
| 6 | TRF16 export comparison | PASS |
| 7 | TRF26 export comparison | PASS |
| 8 | Tie-break result comparison | PASS |
| 9 | Rating-list lookup comparison | PASS |
| 10 | Type-B Rating List comparison | PASS |
| 11 | Windows -> Cloud SYNC -> Linux SYNC | PASS |
| 12 | Linux -> Cloud SYNC -> Windows SYNC | PASS |
| 13 | Web result -> Linux Pairings SYNC | PASS |
| 14 | Web result -> Windows Pairings SYNC | PASS |
| 15 | Same tournament internal identity on both OS | PASS |
| 16 | No duplicate Cloud tournament | PASS |
| 17 | Unicode tournament/player save-load | PASS |
| 18 | Paths with spaces/non-Latin characters | PASS |
| 19 | TEC warning behavior equivalence | PASS |
| 20 | Protected-core hash verification | PASS |

**Matrix result: 20/20 PASS, 0 FAIL.**

Detailed checkpoint: `CHECKPOINTS/beta81-linux-parity.md`.

## Version sequencing
beta.81 is now the proven parity anchor. Linux beta.82 is intentionally skipped. The next functional target is exact Windows beta.83 after its authoritative source and hashes are available; no manual beta.82/beta.83 reconstruction is allowed.
