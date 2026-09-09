# Chess-Publisher v1.06.00-beta.81 — Linux package candidate

Date: 2026-09-09
Status: **EXACT-SOURCE PACKAGE CANDIDATE PASS**

## Candidate
- File: `Chess-Publisher-v1.06.00-beta.81-Ubuntu-amd64.deb`
- SHA256: `be2015aec5b1f64490cd1496ffe2323bbadf898285007f8afdca00c48c29addc`
- Size: `32238004` bytes
- Package version: `1.06.00~beta81`
- App build: `1.06.00-beta.81`
- Linux engine: `0.7.0-linux`

## Source identity
The candidate was built from the exact authoritative shared source:
- `Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz`
- SHA256 `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`
- snapshot `cp-v1.06.00-beta.81-shared-source-20260909`

Candidate source payload comparison against the authoritative extraction:
- authoritative source files: 574
- packaged source files: 574
- differences: 0
- result: **574/574 byte-identical**

## Candidate smoke
The built DEB was extracted into a fresh package root and tested from that exact payload.

- source guard: PASS
- runtime integrity: PASS
- LocalEngine filesystem: PASS
- HTTP delivery: PASS
- platform services: PASS
- self-test: **6 PASS / 0 FAIL**
- startup probe: PASS
- `/health`: `appBuild=1.06.00-beta.81`, `engineVersion=0.7.0-linux`
- `/source/VERSION.txt`: `1.06.00-beta.81`
- exact candidate start smoke: **PASS**

The same packaging/runtime code previously passed native Ubuntu 24.04 DEB install/purge and Ubuntu 26.04 container acceptance in GitHub Actions run `34384400988`. The exact-source candidate additionally passed the source-payload and startup checks above.

## Parity anchor
This candidate is built only after:
- exact beta.81 shared-source verification
- 574/574 shared-source integrity
- 42/0 shared TEC regression
- Type-B 29/29
- Windows ↔ Linux matrix 20/20
- Linux platform acceptance PASS
- TRF16/TRF26, Gacrux 1.9.57, BBP 6.0.0 and Tie-Break acceptance PASS

## Version sequencing
This closes Linux beta.81 as the proven parity/package anchor. **Do not create Linux beta.82.** The next functional source migration is exact Windows beta.83 when its source archive and hashes become authoritative.
