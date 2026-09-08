# Rating List Integration Plan

## Architecture
Rating lists are installation-local reference data, separate from tournament snapshots.

### Providers
- `fide-standard`
- `fide-rapid`
- `fide-blitz`
- future federation/national providers

### Metadata
Each provider stores:
- provider id
- source URL
- list date
- downloadedAt
- player count
- source checksum
- index schema version
- status

### Update flow
1. Update only when explicitly requested.
2. Download to temporary files.
3. Verify basic file validity and size limits.
4. Parse completely.
5. Build a new index in a temporary location.
6. Run integrity checks.
7. Atomically swap the complete new DB/index into active location.
8. Keep the previous working DB until success.
9. Write a human-readable update report.

### Search
- FIDE ID: exact lookup first.
- Name: Unicode normalized, case-insensitive, accent-insensitive and punctuation-tolerant.
- Return Standard/Rapid/Blitz together when available.

### Tournament safety
Importing a player copies rating-list fields into tournament `players[]`.
Later rating-list updates do not mutate tournament players.
An explicit reviewable `Update tournament players from rating list` operation may be added later.
