# Checkpoint — beta.81 TEC/VCL shared-source regression on Linux migration

Date: 2026-09-09
Status: **PASS FOR APPLICABLE SHARED TEC/VCL SOURCE TESTS — TYPE-B VERIFIED IN NEXT GATE**

The exact hash-verified beta.81 shared source was tested directly. No beta.35–beta.81 functionality was reconstructed or ported manually.

## Live shared-source regression
- applicable beta.35–beta.80 shared TEC/function regression files: **42 PASS / 0 FAIL**
- full-program static audit: **PASS**
- beta.81 Type-B test is reserved for the dedicated next gate
- `BETA68-GACRUX-RUNTIME-HARDENING-REGRESSION.js` is classified as a Windows packaging/runtime-fixture test because the source-only archive intentionally does not contain the sealed Windows Gacrux runtime archive/tree. Linux Gacrux is validated by the separate Linux protected engine gate; this test is not treated as a shared TEC failure.

The live report SHA256 is:
`1f6ec4eda0d0d6a6d197dafb4b43732a06a64e67d648f6f584f371c16122b760`.

## Covered exact-source workstreams
The live set includes the exact beta.81 source tests for pairing-integrity and configuration revalidation, adjourned/unusual results, mandatory Swiss tie-breaks, manual/help, HPB and TPN rules, rating provenance/effective/freshness/sequences, TRF26 completeness, PIBE warnings, Type-A list semantics, ordering/correction/tied-place/long-event rating history, Q214-Q216 rating policies, final TEC UI gaps, Web-result validation, Cloud identity/list behavior, unified SYNC, Pairings SYNC UI and beta.80 warning/evidence closures.

## VCL baseline
Windows beta.81 evidence baseline remains:
- PASS 159
- PARTIAL 14
- FAIL 0
- CONDITIONAL 21
- NEEDS TEST 0
- NEEDS TEC 1
- N/A 30

Linux now uses the same exact shared implementation for these platform-independent functions. Q18 remains the external TEC dependency and is not promoted locally. Platform-specific rows continue to require Linux platform evidence.

## Next gate
Run dedicated beta.81 Type-B Q120/Q122 verification on the exact shared module, including Standard/Rapid/Blitz, `originalSourceKnown=false`, import, catalogue, delete and lookup.
