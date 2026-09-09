#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bootstrap=(ROOT/'linux'/'source_bootstrap.py').read_text(encoding='utf-8')
runner=(ROOT/'linux'/'run-chess-publisher.sh').read_text(encoding='utf-8')
required=['ARCHIVE_NAME = "Chess-Publisher-Windows-FIDE-Beta81-SOURCE.tar.gz"','ARCHIVE_SHA256 = "b7b728d3dc545f8cc07abed1580f4b57b151047971ab36438b58be4c1d80fc6b"','verify_source(source,manifest)','verify_source(staged,manifest)',"if source.exists() and any(source.rglob('*')): raise","tf.extractall(staged,members=members,filter='data')"]
missing=[x for x in required if x not in bootstrap]
if missing:raise RuntimeError(f'beta.81 source bootstrap markers missing: {missing}')
if 'beta.34' in bootstrap.lower():raise RuntimeError('beta.34 fallback remains in beta.81 bootstrap')
bootstrap_call='python3 "$HERE/source_bootstrap.py"';entry_call='exec python3 "$HERE/chess_publisher_linux_entry.py"'
if bootstrap_call not in runner or entry_call not in runner or runner.index(bootstrap_call)>runner.index(entry_call):raise RuntimeError('runner must bootstrap verified source before entrypoint')
print('BETA81_FRESH_CHECKOUT_SOURCE_BOOTSTRAP=PASS')
