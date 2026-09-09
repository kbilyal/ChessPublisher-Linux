# Pairings — Download Results

`Download Results` is a Linux dev22 Pairings action for organizer-controlled retrieval of results entered through Web Arbiter Access.

## Source of truth
Web Arbiter Access submissions are **not** read from the normal Cloud snapshot. They are pending organizer submissions from:

- `GET /api/v1/cloud/tournaments/{id}/arbiter-results`
- reviewed submissions are cleared with `POST /api/v1/cloud/tournaments/{id}/arbiter-results/ack`

The authenticated Desktop Organizer Token is used. The tournament is matched by `cloudTournamentId` or exact `internalId`/Cloud `localKey`; tournament names are never used as identity.

## Reconciliation rules
Only the currently selected **editable** round is processed.

For every pending Web submission, Desktop requires an exact match of:

1. board number;
2. White player key;
3. Black player key.

Then:

- Desktop result empty + Web result present → Web result is applied automatically.
- Desktop and Web result identical → no Desktop change; submission is acknowledged as reviewed.
- Desktop and Web both present but different → organizer is shown both values and chooses **Web** or **Desktop** for that board.
- Web submission with different board/pairing identity → left pending and not guessed.
- Unsupported Web result → left pending.
- A blank Web value never erases a Desktop result.

After result changes, the tournament is saved once and derived standings/tie-break views are refreshed. Reviewed submissions are acknowledged only after local processing. If acknowledgement fails, local result changes are kept and the queue remains retryable.

## Safety boundary
The integration changes only `board.result` after the exact identity checks above. It does not replace boards, regenerate pairings, alter players, starting numbers, colors, tournament settings, TRF history, Gacrux, BBP, Tie-Break core or Chess-Results core.
