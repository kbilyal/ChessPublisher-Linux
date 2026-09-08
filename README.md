# ChessPublisher-Linux

Dedicated Linux development repository for Chess-Publisher.

## Current authoritative state

- Version: `v1.06.00-beta.34-linuxdev21`
- Source commit before split: `5e0b37708cbef2828ec60d7e6faa247d4ecc904d`
- Source branch before split: `kbilyal/ChessPublisher:linux-ubuntu-port`
- Linux Ubuntu Acceptance #242: **SUCCESS**
- Ubuntu 24.04 install: PASS
- Ubuntu 26.04 clean container install: PASS
- TRF16/TRF26: PASS
- Gacrux 1.9.57 / BBP / Tie-Break: PASS
- Chess-Results secure Worker contract: PASS
- Desktop ↔ Web Cloud directional sync: PASS
- Fluidity v2: PASS in real Chromium

## Rule for all future work

This repository is the single source of truth for Linux development.

Every completed Linux fix/version MUST be committed and pushed here before it is reported as complete.

Never depend on chat memory alone. A new chat or AI agent must be able to resume solely from:
1. `CURRENT_STATE.json`
2. `AI_HANDOFF.md`
3. `CHANGELOG-LINUX.md`
4. `docs/PROTECTED_COMPONENTS.md`
5. the current Git HEAD

## Protected core

Do not modify unless explicitly authorized:
- Gacrux 1.9.57
- Swiss Dutch pairing logic
- TRF16/TRF26 core
- BBP checker
- Tie-Break core/checker
- Chess-Results protocol/core

See `docs/PROTECTED_COMPONENTS.md`.

## Next development target

Integrated Rating Lists:
- FIDE Standard
- FIDE Rapid
- FIDE Blitz
- local/offline reference database
- normalized search by name / exact FIDE ID
- explicit `Update Rating Lists`
- atomic update with rollback safety
- update report
- no automatic mutation of players in already-started tournaments
