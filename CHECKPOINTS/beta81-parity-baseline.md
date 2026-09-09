# Checkpoint — beta.81 Windows/Linux parity baseline

Date: 2026-09-09
Status: **AUDIT CHECKPOINT / PARITY WORK IN PROGRESS — NOT A RELEASE CANDIDATE**

## Parent Linux state
- Linux repo: `kbilyal/ChessPublisher-Linux`
- Parent HEAD: `d86d9f92661dbfd64080c42b6e47b8856fe51159`
- Accepted Linux runtime implementation: `39d698a1f6dd3015313d0113540212afb596bc2b`
- Legacy Linux runtime label: `v1.06.00-beta.34-linuxdev23`
- Protected source snapshot: `cp-v1.06.00-beta.34-linux-source-20260907`

## Windows reference
- Target functional baseline: `v1.06.00-beta.81`
- Repo: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`
- HEAD observed: `93f5474bd161057af0dec130d51663d10be004f7`
- beta.81 Type-B checkpoint: `fc0672079e4e6d14106cb7844d855c9abcbb73c6`

## Audit conclusion
Linux and Windows are not yet source-parity. Linux has strong platform work (Ubuntu runtime, integrated official rating lists, Web Results safety, unified Cloud SYNC) but its protected/shared source is beta.34-era. Windows beta.81 contains shared TEC/VCL business logic added beta.35-beta.81 that must not be recreated as a separate Linux tournament core.

## Decision
Freeze new beta.82 feature development. First recover/materialize the exact beta.81 shared source and run Linux adapters against it. Keep current dev23 as rollback baseline.

## Protected core
No production source was changed by this checkpoint. Existing Linux protected hashes remain the before-alignment baseline. If any protected hash changes during shared-source alignment, stop and establish whether the change is an intentional Windows beta.81 shared-core delta or an accidental Linux fork.

## TEC/VCL
Windows beta.81 evidence: 159 PASS / 14 PARTIAL / 0 FAIL / 21 CONDITIONAL / 0 NEEDS TEST / 1 NEEDS TEC / 30 N/A.
Linux does not inherit these statuses. Q18 remains external TEC. Q120/Q122 require Linux Type-B implementation/evidence.

## Next logical block
Establish an exact beta.81 shared-source input for Linux materialization, preserving Linux-only adapter boundaries. Do not port protected/business logic feature-by-feature unless the shared source artifact cannot be recovered and the exact Windows additive modules are used as the canonical source.
