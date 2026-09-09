# Download Results regression expectations

Mandatory checks before dev22 candidate:

- reads pending Arbiter Access queue, not the normal Cloud snapshot;
- Organizer Token authentication only;
- selected editable round only;
- exact board number + White key + Black key match;
- blank Desktop result accepts Web automatically;
- identical result is a no-op and can be acknowledged;
- differing nonblank results require organizer choice Web/Desktop;
- choosing Desktop never rewrites the Desktop result;
- pairing mismatch stays pending and is never guessed;
- blank/unsupported Web value never clears Desktop;
- local save occurs before Web acknowledgement;
- acknowledgement failure leaves queue retryable;
- no pairing regeneration, player mutation, starting-number change or protected-core mutation.
