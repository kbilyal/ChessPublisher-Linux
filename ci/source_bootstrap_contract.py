#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bootstrap=(ROOT/'linux'/'source_bootstrap.py').read_text(encoding='utf-8')
runner=(ROOT/'linux'/'run-chess-publisher.sh').read_text(encoding='utf-8')
required=['ARCHIVE_NAME = "Chess-Publisher-Windows-v1.06.00-beta.85-AUTHORITATIVE-SOURCE.tar.gz"','ARCHIVE_SHA256 = "2795a0612f56f381b65db0c30c3171ccc5f4e16e9bc0778fa5bc7e61fe430e69"','verify_source(source,manifest)','verify_source(target,manifest_path)','_resolve_source_root','_copy_manifest_files',"if source.exists() and any(source.rglob('*')): raise","tf.extractall(staged,members=members,filter='data')"]
missing=[x for x in required if x not in bootstrap]
if missing:raise RuntimeError(f'beta.85 source bootstrap markers missing: {missing}')
for forbidden in ('Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz','beta.34 fallback'):
    if forbidden in bootstrap:raise RuntimeError(f'old source fallback remains: {forbidden}')
bootstrap_call='python3 "$HERE/source_bootstrap.py"';entry_call='exec python3 "$HERE/chess_publisher_linux_entry.py"'
if bootstrap_call not in runner or entry_call not in runner or runner.index(bootstrap_call)>runner.index(entry_call):raise RuntimeError('runner must bootstrap verified source before entrypoint')
print('BETA85_FRESH_CHECKOUT_SOURCE_BOOTSTRAP=PASS')
