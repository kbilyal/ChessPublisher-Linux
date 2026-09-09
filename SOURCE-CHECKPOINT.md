# Shared Source Checkpoint — target v1.06.00-beta.81

Status: **PARITY SOURCE RECOVERY IN PROGRESS — NOT A RELEASE CANDIDATE**
Date: 2026-09-09

## Target
One logical Chess-Publisher shared source baseline for Windows and Linux at `v1.06.00-beta.81`.

## Windows evidence
- Windows checkpoint repository: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`.
- beta.81 implementation checkpoint: `fc0672079e4e6d14106cb7844d855c9abcbb73c6`.
- version HEAD observed: `93f5474bd161057af0dec130d51663d10be004f7`.
- beta.81 source archive expected SHA256: `b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b`.
- beta.81 Type-B module expected SHA256: `3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96`.
- beta.81 source patch expected SHA256: `3baad0a3ded7b70db47100591fad04d9291e946ad51b4e7afb201cdca8de06e9`.

## Recoverable predecessor
The beta.80 Drive checkpoint contains `Chess-Publisher-Windows-FIDE-Beta80-SOURCE.tar.gz`; its Drive file is present, but automated retrieval is currently blocked by Google Drive's abusive-file malware/spam flag. Do not bypass source verification with a different file.

## Current Linux source
- snapshot: `cp-v1.06.00-beta.34-linux-source-20260907`.
- base release: `v1.06.00-beta.34`.
- protected archive SHA256: `19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff`.

This beta.34 source remains a rollback/test baseline only. It is not allowed to become a beta.81 release candidate.

## Fail-closed rule
`VERSION.txt` records the shared target (`1.06.00-beta.81`), while legacy `VERSION` remains the last accepted Linux runtime label until source parity is achieved. `tests/cross_platform_parity_guard.py` must prevent release-candidate promotion while `source_manifest.json` is behind the shared target.

## Next source action
Recover the exact beta.81 source archive or the exact beta.80 archive plus beta.81 canonical source patch/module. Verify hashes before use. Only after exact recovery should Linux materialization switch from the beta.34 protected source to the beta.81 shared source.
