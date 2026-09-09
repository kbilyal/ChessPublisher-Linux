# Continuity implementation plan

1. Keep the immutable dev21 Linux runtime as the functional baseline.
2. Never copy the old root upstream `ChessPublisher.html` into protected source.
3. Store/recover the verified beta.34 protected-source archive by its SHA256 `19d6f55b...`.
4. Extract into a staging directory only.
5. Verify all seven files against `source_manifest.json`.
6. Atomically activate staged `source/` only after complete verification.
7. Overlay current dev22 `linux/` and `tests/` changes without modifying protected files.
8. Run full Ubuntu/Chromium/FIDE/Chess-Results/TRF/Gacrux acceptance before packaging.
