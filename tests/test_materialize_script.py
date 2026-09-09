#!/usr/bin/env python3
"""Contract for non-destructive, fail-closed Linux runtime materialization."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / 'scripts' / 'bootstrap_dev21_from_upstream.py').read_text(encoding='utf-8')

for marker in (
    'UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"',
    'PROTECTED_ARCHIVE_SHA256 = "19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff"',
    '"--output"',
    '"--source-archive"',
    '"--source-root"',
    '"--allow-source-unavailable"',
    'verify_source_root',
    'extract_protected_archive',
    'copy_tree(repo_root / "linux", output / "linux")',
    'copy_tree(repo_root / "tests", output / "tests")',
    'MATERIALIZED_STATE.json',
    'Protected source hash mismatch',
    'Refusing to materialize over the repository source tree',
    'oldUpstreamRootSourceAllowed',
    'The old upstream root source is forbidden',
):
    if marker not in SCRIPT:
        raise SystemExit('MISSING: '+marker)

# Recovery must never overwrite the current checkout or silently reuse the old
# root HTML that is present in the upstream git tree.
for forbidden in (
    'copy_tree(upstream / "linux-port" / "linux", repo_root / "linux")',
    'copy_files(PROTECTED_PATHS, upstream, output, manifest)',
    'shutil.copy2(upstream / rel',
):
    if forbidden in SCRIPT:
        raise SystemExit('FORBIDDEN: '+forbidden)

print('LINUX_MATERIALIZER_FAIL_CLOSED_CONTRACT=PASS')
