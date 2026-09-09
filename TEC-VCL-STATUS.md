# Chess-Publisher TEC / VCL Cross-Platform Status

Audit baseline: 2026-09-09

## Reference documents
- VCL: `VCL4THP.13.xlsx`.
- TEC Manual: `TEC Manual 30HdT.docx`, FIDE Technical Commission Policies and Procedures Manual, version 2.0, 12 August 2026.
- The TEC Manual complements the FIDE Handbook; the Handbook remains authoritative if they conflict.

## Windows beta.81 evidence baseline
- PASS: 159
- PARTIAL: 14
- FAIL: 0
- CONDITIONAL: 21
- NEEDS TEST: 0
- NEEDS TEC: 1
- N/A: 30

This is implementation/testing evidence, not FIDE certification.

## External TEC dependency
Q18 remains `NEEDS TEC`. Do not change it to PASS through local implementation evidence. Q19-Q39 remain conditional on the Q18 decision.

## Type-B requirements
The TEC Manual distinguishes Type-A lists (original source known to the THP) from Type-B lists (original source not known to the THP). If a THP supports Type-B lists, import of any official FIDE rating list must be allowed.

Windows beta.81 evidence closes:
- Q120: Type-B list management -> PASS.
- Q122: all official FIDE Standard/Rapid/Blitz lists can deliberately be imported as Type-B -> PASS.
- Type-B descriptors retain `originalSourceKnown=false` and stay separate from Type-A provenance.

Current Linux beta.34-linuxdev23 has an integrated Standard/Rapid/Blitz store but no proven Type-B catalogue/import/delete/lookup layer. Therefore Q120/Q122 are `Windows PASS / Linux NEEDS ALIGNMENT+TEST` at this checkpoint.

## Warning requirements
TEC Manual warning levels remain shared business logic:
- Level 1: allowed non-standard action; no explicit warning required.
- Level 2: informational warning / acknowledgement.
- Level 3: explicit proceed/cancel confirmation.
- Level 4: two-step confirmation with consequences made explicit.
- Level 5: rejected in FIDE mode or requires leaving FIDE mode.

Linux must use the same warning semantics as Windows. Platform UI may differ, but severity, mutation boundary and fail-closed behavior must not differ.

## Linux parity classification rule
For every VCL row currently PASS on Windows beta.81, use one of:
- `Windows PASS / Linux PASS` — equivalent behavior plus Linux evidence exists.
- `Windows PASS / Linux NEEDS TEST` — behavior is likely/shared but Linux-specific evidence is missing.
- `Windows PASS / Linux NEEDS ALIGNMENT` — current Linux source lineage does not contain/prove the implementation.
- `platform specific` — requirement genuinely depends on OS integration.
- `external TEC dependency` — cannot be closed by product code/testing.

No Linux row may be promoted only because Windows passed it.

## Current Linux global status
`PARITY NOT YET PROVEN`.

Reason: Linux still materializes a beta.34 shared/protected source snapshot while Windows beta.81 includes many shared compliance layers introduced beta.35-beta.81. The correct fix is shared-source alignment, not independent Linux reimplementation of pairing/TRF/tie-break/tournament semantics.

## Gate to beta.81 Linux candidate
Required before calling Linux beta.81 a candidate:
1. beta.81 shared source/materialization established.
2. Protected-core hashes checked before/after.
3. Platform-independent Windows PASS rows re-run/proven on Linux.
4. Type-B Q120/Q122 PASS on Linux.
5. Q18 remains external TEC.
6. 20-point cross-platform matrix completed.
7. Ubuntu 24.04 + 26.04 runtime gates PASS.
8. Windows regression rerun if shared source changes.
