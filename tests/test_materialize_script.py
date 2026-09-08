#!/usr/bin/env python3
"""Contract for non-destructive Linux runtime materialization."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / 'scripts' / 'bootstrap_dev21_from_upstream.py').read_text(encoding='utf-8')

for marker in (
    'UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"',
    '"--output"',
    'output / "source"',
    'copy_tree(repo_root / "linux", output / "linux")',
    'copy_tree(repo_root / "tests", output / "tests")',
    'MATERIALIZED_STATE.json',
    'Protected source hash mismatch',
    'Refusing to materialize over the repository source tree',
):
    if marker not in SCRIPT:
        raise SystemExit('MISSING: '+marker)

# The recovery tool must not erase the current checkout's Linux source.
if 'copy_tree(upstream / "linux-port" / "linux", repo_root / "linux")' in SCRIPT:
    raise SystemExit('FORBIDDEN: destructive dev21 overwrite of repo linux/')

print('LINUX_MATERIALIZER_CONTRACT=PASS')
