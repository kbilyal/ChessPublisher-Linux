import fs from 'node:fs';
import assert from 'node:assert/strict';

const src=fs.readFileSync(new URL('../linux/cloud_unified_sync.js',import.meta.url),'utf8');

for(const marker of [
  'cpUnifiedSyncBtn',
  '⟳ SYNC',
  "status==='LOCAL_CHANGES'",
  'cpCloudPushToCloud',
  "status==='REMOTE_CHANGES'",
  'cpCloudPullToDesktop',
  "status==='CONFLICT'",
  'cpCloudResolveConflict',
  'cpUnifiedSyncRefreshFromResults',
  "tournament.cloud.syncStatus='LOCAL_CHANGES'",
  'cpDownloadWebResultsBtn',
  'PUBLIC LIST',
  "label==='upload current'",
  "label==='pull current'",
  "label==='upload as new'"
]) assert.ok(src.includes(marker),`missing ${marker}`);

assert.equal((src.match(/id=\\?"cpUnifiedSyncBtn/g)||[]).length>=1,true,'single SYNC control missing');
assert.ok(!src.includes('tournament.name==='),'SYNC identity must not match by tournament name');
assert.ok(!src.includes('Imported'),'SYNC identity must not depend on Imported state');
assert.ok(!src.includes('createTournament('),'unified UI must delegate identity-safe creation to the existing Cloud identity layer');

console.log('LINUX_UNIFIED_CLOUD_SYNC_CONTRACT=PASS');
