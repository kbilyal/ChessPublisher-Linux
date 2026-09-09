# AI HANDOFF — READ THIS FIRST

Continue Chess-Publisher as ONE Windows/Linux product. Linux code changes remain in `kbilyal/ChessPublisher-Linux`, branch `main`, until repository consolidation is explicitly approved.

## Current directive — supersedes old standalone Linux release path
Windows and Linux must now move in version lockstep from one logical shared tournament/business source baseline. Do not continue a separate `linuxdev24/linuxdev25` product line. Do not start beta.82 feature work until Linux parity against Windows `v1.06.00-beta.81` is measured and restored.

## Current observed baselines
### Windows reference
- Version: `v1.06.00-beta.81`.
- Repo: `kbilyal/Chess-Publisher-Windows-FIDE-Beta`.
- HEAD observed at parity audit: `93f5474bd161057af0dec130d51663d10be004f7`.
- beta.81 Type-B checkpoint: `fc0672079e4e6d14106cb7844d855c9abcbb73c6`.
- VCL evidence: PASS 159 / PARTIAL 14 / FAIL 0 / CONDITIONAL 21 / NEEDS TEST 0 / NEEDS TEC 1 / N/A 30.
- Q18 remains external TEC; never mark it PASS locally.

### Linux rollback baseline
- Legacy version label: `v1.06.00-beta.34-linuxdev23`.
- Accepted runtime commit: `39d698a1f6dd3015313d0113540212afb596bc2b`.
- Hosted full acceptance #24: PASS.
- Existing protected source snapshot: `cp-v1.06.00-beta.34-linux-source-20260907`.
- Current Linux source lineage is therefore NOT beta.81 parity yet.

## Read first
1. `CURRENT_STATE.json`
2. `CROSS-PLATFORM-PARITY.md`
3. `TEC-VCL-STATUS.md`
4. `CHECKPOINTS/beta81-parity-baseline.md`
5. `docs/PROTECTED_COMPONENTS.md`
6. actual current `main` HEAD and recent commits

## Shared protected/business logic
Do not create Linux-specific versions of:
- Gacrux 1.9.57 / Swiss Dutch pairing logic
- TRF16/TRF26 core and TRF pairing path
- BBP
- Tie-Break core/checker
- Chess-Results protocol/core
- player/pairing identity semantics
- rating-list semantics
- TEC/FIDE warning logic
- tournament file format
- Cloud tournament identity / unified SYNC contract

Platform-specific code is limited to launcher/runtime, browser/WebView shell, filesystem/dialogs, printing/PDF integration, hardware bridge and installers/packages.

## Linux features already accepted
- Ubuntu runtime/hosted acceptance.
- integrated Standard/Rapid/Blitz local rating-list database and safe atomic update.
- Web result-only reconciliation with exact board/player identity and explicit conflict choice.
- unified Cloud SYNC with stable identity, BASE/LOCAL/REMOTE classification and fail-closed conflicts.
- Refresh is metadata/status only; autosave is local only.
- Gacrux/TRF/BBP/Tie-Break/Chess-Results hosted regression passed for the dev23 rollback baseline.

## Known parity gaps / evidence gaps
See `CROSS-PLATFORM-PARITY.md`. The critical architectural gap is that Linux still materializes beta.34 protected/shared source while Windows has beta.35-beta.81 shared compliance work. Do NOT copy Windows PASS labels into Linux. Establish shared beta.81 source first.

Two immediately visible UX/feature gaps:
- Windows Pairings normal action is `↕ SYNC` (validated Web result intake followed by unified SYNC); Linux dev23 still exposes `Download Results` separately.
- Windows beta.81 Type-B Rating Lists (Q120/Q122) are not present/proven in current Linux rating-list store/UI.

## TEC/VCL references
Use `VCL4THP.13.xlsx` and `TEC Manual 30HdT.docx` as primary working TEC/VCL references. The FIDE Handbook takes precedence if it conflicts with the TEC Manual.

## Git rule
Before every write, re-read `main` HEAD. Every completed logical block: TEST -> REGRESSION -> COMMIT -> PUSH -> verify remote HEAD -> record SHA. Never force push.

## Next logical block
Recover/materialize exact Windows beta.81 shared source (or exact canonical additive source modules) as the Linux shared input, preserving the accepted Linux platform adapters. Then run protected hashes and targeted regression before any functional parity modification or beta.81 Linux candidate label.
