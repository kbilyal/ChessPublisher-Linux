# Checkpoint — beta.81 Type-B Rating Lists on Linux shared source

Date: 2026-09-09
Status: **PASS — Q120 / Q122 shared-source verification**

The exact authoritative beta.81 module was re-hashed and executed directly from the shared source used for Linux migration.

## Exact module
- `ChessPublisher-Beta81-TypeB-RatingLists.js`
- SHA256: `3d41cee5bafe393b5632f12be8874bdf4e207fab52af36e5391118679478fb96`
- result: exact expected hash

## Dedicated live regression
`BETA81-TYPE-B-RATING-LISTS-REGRESSION.js`:
- PASS: 29
- FAIL: 0
- TOTAL: 29

Live log SHA256:
`e7e9bc34def5271e9e57beb75f3ce8eee19c58990410bf96fc56a52c0938062f`

## Required parity points
PASS:
- Q120 Type-B managed-list support
- Q122 deliberate import of official FIDE rating lists as Type-B
- Standard
- Rapid
- Blitz
- `originalSourceKnown=false`
- import
- managed catalogue
- delete
- FIDE-ID/player rating lookup
- duplicate Type-B list ID rejected
- unsupported rating type rejected
- invalid list content rejected
- Type-B is not silently promoted to Type-A
- Type-A beta.65 API is not modified
- pairing/TRF core is not touched
- Integrated Rating Lists panel receives the Type-B UI hook

The Linux migration does not implement a separate Type-B data model. It serves and uses the exact beta.81 shared module.

## Next gate
Run the defined 20-point Windows ↔ Linux parity matrix. Do not call beta.81 parity complete before the matrix and full Linux platform acceptance pass.
