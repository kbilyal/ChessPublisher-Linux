# Exact protected-source recovery

The dedicated Linux repository must materialize the exact protected beta.34 source before any full acceptance or package build.

Authoritative protected `ChessPublisher.html`:

- size: `1,526,307` bytes
- SHA256: `f51355b1a449870be6ed69d1bb941c19a9d8d2bdf3c8f91da845b4bc1275f310`

The older root `ChessPublisher.html` present in the immutable dev21 Git commit is **not** the protected source and must never be accepted as a fallback. Current full acceptance intentionally fails closed when that mismatch is detected.

The verified recovery archive identity is:

- file: `Chess-Publisher-v1.06.00-beta.34-protected-source.tar.gz`
- SHA256: `19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff`

Recovery must verify the archive and then all seven protected source identities from `source_manifest.json` before activation. A failed verification must never overwrite an existing valid source tree.
