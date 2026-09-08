# AI HANDOFF — READ THIS FIRST

You are continuing Chess-Publisher Linux.

## Authoritative baseline
Version: v1.06.00-beta.34-linuxdev21
Commit before repository split: 5e0b37708cbef2828ec60d7e6faa247d4ecc904d
Acceptance: Linux Ubuntu Acceptance #242 = SUCCESS

## Do not guess from old chats
Treat this repository as source of truth.

Before changing code:
1. Read CURRENT_STATE.json.
2. Read docs/PROTECTED_COMPONENTS.md.
3. Read CHANGELOG-LINUX.md.
4. Inspect current Git HEAD.
5. Run relevant regression contracts before and after changes.

## Mandatory Git rule
Every completed fix must be committed and pushed.
Never say a fix is complete while it exists only locally.
No force push.
Never overwrite concurrent commits.
Always re-read branch HEAD before a write.

## Release rule
Never call a build final/stable merely because it launches.
Use TEST CANDIDATE until the complete required regression gate is green.

## Protected components
Do not change Gacrux 1.9.57, Swiss Dutch pairing, TRF16/TRF26 core,
BBP checker, Tie-Break core/checker, or Chess-Results protocol/core
unless the user explicitly requests it.

## Current next task: Rating Lists
Build a separate local reference-data subsystem.
The rating-list database is NOT tournament state.

Required first phase:
- Standard / Rapid / Blitz providers
- explicit update operation
- download to temporary location
- validate payload
- parse/index
- atomic replacement only after full success
- preserve previous good database on any failure
- exact lookup by FIDE ID
- normalized name search (case/accent/punctuation tolerant)
- metadata: list date, downloadedAt, count, checksum, status
- human-readable update report

Important:
A rating-list update must NEVER silently change players already stored in a tournament.
Any tournament-player refresh must be a separate explicit reviewed action.
