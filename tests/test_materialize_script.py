#!/usr/bin/env python3
"""Contract for beta.85 exact-source, fail-closed Linux materialization."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=(ROOT/'scripts'/'bootstrap_dev21_from_upstream.py').read_text(encoding='utf-8')
required=(
'UPSTREAM_COMMIT = "5e0b37708cbef2828ec60d7e6faa247d4ecc904d"',
'SHARED_ARCHIVE_NAME = "Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz"',
'SHARED_ARCHIVE_SHA256 = "2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69"',
'runtimeSharedFiles','verify_source_root','resolve_source_root','activate_source','"--source-archive"','"--source-root"','"--allow-source-unavailable"',
'copy_tree(repo_root/"linux",output/"linux")','copy_tree(repo_root/"ci",output/"ci")','MATERIALIZED_STATE.json','olderBeta81SharedSourceAllowed','Older beta.81/beta.34 shared source is forbidden for the beta.85 target.')
for marker in required:
    if marker not in SCRIPT: raise SystemExit('MISSING: '+marker)
for forbidden in ('Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz','b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b','Chess-Publisher-v1.06.00-beta.34-protected-source.tar.gz'):
    if forbidden in SCRIPT: raise SystemExit('FORBIDDEN: '+forbidden)
print('BETA85_LINUX_MATERIALIZER_FAIL_CLOSED_CONTRACT=PASS')
