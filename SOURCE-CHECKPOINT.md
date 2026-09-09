# Shared Source Checkpoint — v1.06.00-beta.81 parity anchor

Status: **EXACT SHARED SOURCE VERIFIED — WINDOWS/LINUX PARITY PASS**
Date: 2026-09-09

## Authoritative source
Chess-Publisher uses one shared tournament/business source for Windows and Linux.

- Source archive: `Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz`
- SHA256: `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`
- Internal `VERSION.txt`: `1.06.00-beta.81`
- Type-B module SHA256: `3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96`
- Type-B patch SHA256: `3baad0a3ded7b70db47100591fad04d9291e946ad51b4e7afb201cdca8de06e9`
- Linux shared snapshot: `cp-v1.06.00-beta.81-shared-source-20260909`

The source blocker is closed. beta.35-beta.81 was not reconstructed or reimplemented for Linux; the exact beta.81 source became the Linux functional baseline.

## Integrity after Linux adaptation
- authoritative shared files: 574
- Linux shared files: 574
- byte-identical: 574/574
- unexpected differences: 0
- protected invariant set: PASS
- Windows protected-source evidence: 70/70 byte-identical

Linux differences are restricted to launcher/browser shell, filesystem/dialogs, printing/PDF, hardware bridge abstraction and packaging.

## Rollback baseline
`v1.06.00-beta.34-linuxdev23` remains rollback-only. It is not a forward source lineage and must not be used to recreate later shared features.

## Acceptance
- Cross-Platform Parity Guard `34384401055`: PASS
- Linux beta.81 Platform Acceptance `34384400988`: PASS
- 20-point Windows ↔ Linux matrix: 20/20 PASS
- exact shared TEC regression: 42 PASS / 0 FAIL
- Type-B: 29/29 PASS

Q18 remains an external TEC dependency.

## Next shared version
beta.81 is the parity anchor. Do not create a Linux beta.82 line. When Windows beta.83 is authoritative, require exact beta.83 source + hashes, then reapply only Linux platform adapters and rerun all parity/protected gates.
