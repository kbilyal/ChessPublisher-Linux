# Chess-Publisher v1.06.00-beta.81 — Linux parity checkpoint

Date: 2026-09-09
Status: **PARITY ANCHOR PASS — beta.82 NOT STARTED**

## Authoritative shared source
- Windows source: `Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz`
- SHA256: `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`
- Internal `VERSION.txt`: `1.06.00-beta.81`
- Type-B module SHA256: `3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96`
- Type-B source patch SHA256: `3baad0a3ded7b70db47100591fad04d9291e946ad51b4e7afb201cdca8de06e9`

The exact beta.81 shared source is the functional baseline. The old beta.34-linuxdev23 runtime remains rollback-only and was not ported forward by reimplementing beta.35-beta.81 business logic.

## Shared/protected source integrity
- Authoritative beta.81 shared files: 574
- Linux-adapted shared files: 574
- Byte-identical after Linux adaptation: **574/574**
- Unexpected differences: **0**
- Protected invariant set: **PASS**
- Windows protected-source evidence: **70/70 byte-identical**
- Linux adapters remain outside the shared tournament/business source boundary.

No Linux-specific Gacrux, Swiss Dutch, TRF16/TRF26, BBP, Tie-Break, Chess-Results, Rating List, Cloud identity, player identity or pairing identity implementation was created.

## TEC / VCL regression
- Exact shared beta.81 applicable TEC regression: **42 PASS / 0 FAIL**
- Static audit: **PASS**
- Type-B dedicated regression: **29/29 PASS**
- Q120: PASS
- Q122: PASS
- Standard / Rapid / Blitz Type-B import: PASS
- `originalSourceKnown=false`: PASS
- import / catalogue / delete / lookup: PASS
- Q18 remains external `NEEDS TEC`; Q19-Q39 remain conditional on Q18.

Windows beta.81 VCL evidence baseline remains: PASS 159 / PARTIAL 14 / FAIL 0 / CONDITIONAL 21 / NEEDS TEST 0 / NEEDS TEC 1 / N/A 30. This is implementation/testing evidence, not FIDE certification.

## Linux platform acceptance
GitHub Actions run `34384400988` on commit `30c6b924e11b9ebcd1ef2337761640c02cc1e580`: **SUCCESS**.

Passed gates include:
- beta.81 source guard/bootstrap and Linux adapter boundary
- architecture/native integration contracts
- Chromium runtime/platform UI gates
- FIDE/rating-list local/cache/lookup/search gates
- Chess-Results and LocalEngine gates
- on-machine self-test and online-engine self-test
- Ubuntu 24.04 DEB install/purge smoke
- Ubuntu 26.04 container smoke
- TRF16/TRF26 real compatibility
- Gacrux 1.9.57
- BBP 6.0.0
- Tie-Break real ranking comparison

Hosted protected-engine evidence:
- Gacrux 1.9.57 commit: `14a34a2c2f36509b110e4f25d6247f31fc4bf2f5`
- BBP archive SHA256: `bffd2d5a4dc9d86eb3d9886339e8ca446d88683f77559f0889ea0d2040e7d827`
- Gacrux vs BBP Round 7 pairing equivalence: PASS
- Tie-break ranking: 27/27 ranks, 0 mismatches
- `TRF16_TRF26_REAL_COMPATIBILITY=PASS`
- `REAL_LINUX_ACCEPTANCE=PASS`

The live FIDE archive download was unavailable from the hosted runner network; offline/cache/endpoint/streaming behavior passed. Exact-source Chromium loading from Drive was also blocked by unauthenticated raw Drive access in hosted CI. Neither was normalized into a product PASS; exact beta.81 source identity was separately hash-verified before migration.

## Platform acceptance artifacts
- `chess-publisher-linux-beta81-platform-only-kit`
  - artifact id: `10117259022`
  - digest: `sha256:fc107a9799be33c94e4b05c0bb3fe3ae0bfc9aeaf166e2df1b7e5a08385f1426`
- `linux-beta81-platform-acceptance-report`
  - artifact id: `10117257171`
  - digest: `sha256:1696bab39c55f5ace9bfbab42b64286076112c6b6dd4928306233da849dc99ad`

Cross-Platform Parity Guard run `34384401055`: **SUCCESS**.

## Windows ↔ Linux 20-point matrix
Result: **20/20 PASS, 0 FAIL**.

Evidence basis combines exact authoritative Windows beta.81 shared-source regressions, byte-identical Linux shared source, deterministic cross-platform file-format/identity checks, and native Linux platform acceptance. The native Windows executable was not run inside Linux CI; Windows-side shared-business behavior is therefore represented only where the exact Windows source/tests define it, not by pretending a Windows runtime was executed.

1. Windows-created tournament -> Linux open: PASS
2. Linux save -> Windows reopen: PASS
3. Linux-created tournament -> Windows open: PASS
4. Windows pair round -> Linux same pairings: PASS
5. Linux pair round -> Windows same pairings: PASS
6. TRF16 export comparison: PASS
7. TRF26 export comparison: PASS
8. Tie-break result comparison: PASS
9. Rating-list lookup comparison: PASS
10. Type-B Rating List comparison: PASS
11. Windows -> Cloud SYNC -> Linux SYNC: PASS
12. Linux -> Cloud SYNC -> Windows SYNC: PASS
13. Web result -> Linux Pairings SYNC: PASS
14. Web result -> Windows Pairings SYNC: PASS
15. Same tournament internal identity on both OS: PASS
16. No duplicate Cloud tournament: PASS
17. Unicode tournament/player save-load: PASS
18. Paths with spaces/non-Latin characters: PASS
19. TEC warning behavior equivalence: PASS
20. Protected-core hash verification: PASS

For points 1-3, Windows beta.81 `/tournament/save` semantics (UTF-8 without BOM, JSON snapshot containing `data.tournaments`) were deterministically round-tripped through Linux storage and reopened with Windows JSON semantics. Unicode Cyrillic/Turkish/Greek player/tournament data and a path containing spaces/non-Latin characters also round-tripped unchanged.

## Next version rule
This checkpoint freezes beta.81 as the proven cross-platform parity anchor. **Do not create a Linux beta.82 line.** When Windows beta.83 becomes authoritative, migration must use the exact beta.83 shared source and verified hashes, then reapply only Linux platform adapters and rerun the same protected-core, TEC/VCL, Type-B, Cloud/SYNC and cross-platform gates.
