#!/usr/bin/env python3
"""Contract for beta.81 exact-source, fail-closed Linux materialization."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=(ROOT/'scripts'/'bootstrap_dev21_from_upstream.py').read_text(encoding='utf-8')
required=(
'UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"',
'SHARED_ARCHIVE_NAME = "Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz"',
'SHARED_ARCHIVE_SHA256 = "b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b"',
'runtimeSharedFiles','verify_source_root','extract_shared_archive','"--source-archive"','"--source-root"','"--allow-source-unavailable"',
'copy_tree(repo_root / "linux", output / "linux")','copy_tree(repo_root / "ci", output / "ci")','MATERIALIZED_STATE.json','olderBeta34SharedSourceAllowed','Older beta.34 shared source is forbidden.')
for marker in required:
    if marker not in SCRIPT: raise SystemExit('MISSING: '+marker)
for forbidden in ('Chess-Publisher-v1.06.00-beta.34-protected-source.tar.gz','19d6f55bd6954db4cd6327ad61892b538e5b7a7129ac1fce2adf5e3ec2176eff','copy_tree(upstream / "linux-port" / "linux", repo_root / "linux")','shutil.copy2(upstream / rel'):
    if forbidden in SCRIPT: raise SystemExit('FORBIDDEN: '+forbidden)
print('BETA81_LINUX_MATERIALIZER_FAIL_CLOSED_CONTRACT=PASS')
