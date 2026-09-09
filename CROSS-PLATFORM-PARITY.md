# Chess-Publisher Cross-Platform Parity

Audit date: 2026-09-09

## Product rule
Chess-Publisher is one product with one shared tournament/business core and two desktop platforms: Windows and Linux. New functional releases must use the same `v1.06.00-beta.N` feature baseline on both platforms. Linux-specific numbering is legacy history only and must not continue after parity is restored.

## Authoritative baselines
- Windows reference: `v1.06.00-beta.81`.
- Windows checkpoint repository: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`.
- Windows current HEAD observed for the audit: `93f5474bd161057af0dec130d51663d10be004f7`.
- Windows beta.81 implementation/checkpoint commit: `fc0672079e4e6d14106cb7844d855c9abcbb73c6`.
- Linux current HEAD before this audit checkpoint: `d86d9f92661dbfd64080c42b6e47b8856fe51159`.
- Linux accepted runtime implementation: `39d698a1f6dd3015313d0113540212afb596bc2b`.
- Linux legacy runtime label: `v1.06.00-beta.34-linuxdev23`.
- Linux protected source snapshot is still based on `v1.06.00-beta.34` (`cp-v1.06.00-beta.34-linux-source-20260907`).

## A-H parity report

### A. Real Linux version now
`v1.06.00-beta.34-linuxdev23`, hosted acceptance passed, but it is NOT a beta.81 parity candidate.

### B. Source lineage
The Linux protected browser/shared source is beta.34-era. Linux overlays later native/runtime work for Fluidity, integrated FIDE lists, Download Results and unified Cloud SYNC. This means the current Linux package is not built from the same logical shared source checkpoint as Windows beta.81.

### C. Windows beta.81 functions not yet proven equivalent on Linux
The current beta.34 protected-source lineage does not by itself contain the Windows compliance work added after beta.34. These workstreams require port-by-shared-source or exact Linux evidence before parity can be claimed:

1. beta.35-beta.38: TRF-import/manual-pairing integrity checks, sensitive configuration revalidation, absolute criteria/prohibited pairing handling, historical PAB verification.
2. beta.39-beta.42: FIDE Baku acceleration workflow, Round Robin TPN/public-draw handling, withdrawal <50% standings rule, mandatory Round Robin tie-breaks.
3. beta.43-beta.46: mid-event tie-break Level-4 safety, Adjourned/ITDX handling, unusual OTB results, mandatory Swiss tie-break catalogue.
4. beta.47-beta.50: complete English manual/direct help, HPB/full-point-bye rules, repeated HPB Level-3 warning, TPN exchange/regeneration/late-entry rules.
5. beta.51-beta.70: tournament/official rating separation and provenance, date-effective/freshness checks, Effective Rapid/Blitz, Rating List Sequence, rating-report corrections/TRF completeness, RR manual opponent coverage, complete PIBE warning/TRF coverage, formal Type-A lists, sequence consistency, publication-order guard, previous-round correction window, exact tied-place/lot/manual ordering, long-event rating history.
6. beta.73: Q214-Q216 historical-rating tie-break policies (`FIDE_FIRST`, `ROUND_EFFECTIVE`, `USER_SELECTED`).
7. beta.74: Pairings/Starting List export controls and static Result Entry panel require UI parity verification. Linux already has independent Web-result reconciliation safety.
8. beta.79: Pairings toolbar should expose the Windows `↕ SYNC` composition (Web results validation + unified Cloud SYNC), not a separate normal `Download Results` UX.
9. beta.81: Type-B Rating Lists are not present in current Linux rating-list store/UI. Required: import, catalogue, delete, lookup, Standard/Rapid/Blitz import, stable descriptors and `originalSourceKnown=false` semantics.
10. beta.80 is evidence-only where the underlying behavior exists; Linux must prove the same warning/sequence behavior rather than copying a PASS label.

### D. Already equivalent or strongly aligned
- Gacrux 1.9.57 remains unchanged and accepted by Linux hosted gates.
- Swiss Dutch pairing core, TRF16/TRF26, BBP, Tie-Break and Chess-Results protected cores passed the accepted Linux hosted gate.
- Tournament file compatibility remains a protected design requirement.
- Linux has integrated local Standard/Rapid/Blitz FIDE data with atomic activation, exact FIDE-ID lookup and normalized search.
- Linux has result-only Web reconciliation with exact board + White/Black identity and explicit conflict choice.
- Linux has unified Cloud SYNC with stable Cloud identity, BASE/LOCAL/REMOTE classification, merge/conflict handling, Refresh-only metadata behavior and local-only autosave.

### E. Platform-specific areas
Only adapters may differ: launcher/runtime, browser/WebView shell, filesystem integration, native dialogs, printing/PDF integration, hardware bridge and installers/packages. DGT/native Windows helpers may remain Windows-supported with a documented Linux bridge/pending-native status; they must not fork tournament logic.

### F. Protected-core status
No code was changed by this audit checkpoint. Existing accepted Linux protected-source manifest remains unchanged. The beta.34 protected snapshot is therefore still the before-parity hash baseline. Any future core hash change requires STOP + investigation before acceptance.

### G. Linux TEC/VCL parity status
Windows beta.81 evidence baseline: PASS 159 / PARTIAL 14 / FAIL 0 / CONDITIONAL 21 / NEEDS TEST 0 / NEEDS TEC 1 / N/A 30.

Linux must NOT inherit those statuses automatically. Q18 remains an external TEC dependency and must not be marked PASS locally. At this audit checkpoint Linux is **PARITY NOT YET PROVEN** because the shared source lineage is beta.34 and the post-beta.34 compliance workstreams above do not yet have equivalent Linux evidence. For each Windows PASS row affected by those workstreams, Linux status is provisionally `NEEDS TEST / ALIGNMENT` until shared-source integration and regression evidence exist.

### H. Minimal safe alignment plan
1. Preserve the accepted Linux dev23 runtime as rollback baseline.
2. Establish beta.81 shared-source recovery/materialization instead of reimplementing the post-beta.34 business logic in Linux-only code.
3. Keep Linux adapters additive around that shared source.
4. Re-apply/verify Linux native rating-list store and unified SYNC against beta.81 contracts.
5. Add beta.81 Type-B functionality using the same semantic model as Windows, not a parallel identity/provenance model.
6. Change Pairings normal action to the same `↕ SYNC` composition as Windows after deterministic result/sync tests pass.
7. Run the 20-point cross-platform matrix, protected hashes and TEC/VCL row-by-row parity audit.
8. Only then label Linux `v1.06.00-beta.81` parity candidate and proceed to beta.82 shared development.

## Cross-platform acceptance matrix
1. Windows-created tournament -> Linux open.
2. Linux save -> Windows reopen.
3. Linux-created tournament -> Windows open.
4. Windows pair round -> Linux same pairings.
5. Linux pair round -> Windows same pairings.
6. TRF16 export comparison.
7. TRF26 export comparison.
8. Tie-break result comparison.
9. Rating-list lookup comparison.
10. Type-B Rating List comparison.
11. Windows -> Cloud SYNC -> Linux SYNC.
12. Linux -> Cloud SYNC -> Windows SYNC.
13. Web result -> Linux Pairings SYNC.
14. Web result -> Windows Pairings SYNC.
15. Same tournament internal identity on both OS.
16. No duplicate Cloud tournament.
17. Unicode tournament/player save-load.
18. Paths with spaces/non-Latin characters.
19. TEC warning behavior equivalence.
20. Protected-core hash verification.

## Release rule
Do not build or call a new Linux beta.81 candidate until the shared-source gap is closed. Do not start beta.82 feature work until beta.81 parity is measured and the remaining differences are explicitly documented.
