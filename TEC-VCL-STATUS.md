# Chess-Publisher TEC / VCL Cross-Platform Status

Closure baseline: 2026-09-09
Shared version: `v1.06.00-beta.81`
Status: **CROSS-PLATFORM IMPLEMENTATION/REGRESSION PARITY PASS**

## Reference baseline
- VCL: `VCL4THP.13.xlsx`
- TEC Manual: `TEC Manual 30HdT.docx`, FIDE Technical Commission Policies and Procedures Manual, version 2.0, 12 August 2026
- FIDE Handbook remains authoritative if it conflicts with the TEC Manual.

## Windows beta.81 VCL evidence baseline
- PASS: 159
- PARTIAL: 14
- FAIL: 0
- CONDITIONAL: 21
- NEEDS TEST: 0
- NEEDS TEC: 1
- N/A: 30

These statuses are implementation/testing evidence, not FIDE certification.

## Linux shared TEC parity evidence
Linux now runs the exact beta.81 shared source rather than a beta.34 reconstruction.

- applicable shared TEC regression: **42 PASS / 0 FAIL**
- shared static audit: **PASS**
- protected/shared source after adaptation: **574/574 byte-identical**
- Windows ↔ Linux matrix: **20/20 PASS**

Platform-specific Linux runtime tests separately cover Chromium, filesystem, Ubuntu packages, hardware bridge abstraction and LocalEngine.

## Type-B Rating Lists
Beta.81 dedicated Type-B suite: **29/29 PASS**.

Verified on the shared source used by Linux:
- Q120 Type-B list management: PASS
- Q122 import of official FIDE Standard/Rapid/Blitz lists as Type-B: PASS
- Standard: PASS
- Rapid: PASS
- Blitz: PASS
- `originalSourceKnown=false`: PASS
- import: PASS
- catalogue: PASS
- delete: PASS
- lookup: PASS
- no silent promotion to Type-A provenance: PASS

## External TEC dependency
Q18 remains `NEEDS TEC`; it is not converted to PASS by local code or testing. Q19-Q39 remain conditional on the Q18 decision.

## Warning semantics
Warning Levels 1-5 remain shared business logic. Exact-source TEC regression and cross-platform warning-equivalence evidence pass; Linux may differ only in platform presentation, not severity, mutation boundary or fail-closed behavior.

## Next-version policy
beta.81 is the cross-platform parity anchor. Linux beta.82 is not started. Exact Windows beta.83 source must become the next shared baseline, followed by protected hashes, TEC/VCL, Type-B, Cloud/SYNC and parity regression before beta.83 can be called cross-platform complete.
