import fs from 'node:fs';
import vm from 'node:vm';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);

function assert(ok,msg){if(!ok)throw new Error(msg)}
const cloudSrc=fs.readFileSync(new URL('../linux/cloud_unified_sync.js',import.meta.url),'utf8');
const webSrc=fs.readFileSync(new URL('../linux/web_results_download.js',import.meta.url),'utf8');
const web=require('../linux/web_results_download.js');

function makeCloud(status, pullResult={status:'IN_SYNC'}, pushResult={status:'IN_SYNC'}){
  const calls=[];
  const document={
    getElementById(){return null},
    querySelectorAll(){return []},
    body:{},
  };
  const window={
    __CP_UNIFIED_SYNC_TEST__:true,
    document,
    async cpCloudRefreshList(){calls.push('list');return {ok:true}},
    async cpCloudCheckStatus(){calls.push('check');return {status}},
    async cpCloudPushToCloud(){calls.push('push');return pushResult},
    async cpCloudPullToDesktop(){calls.push('pull');return pullResult},
    async cpCloudResolveConflict(){calls.push('resolve')},
  };
  const context={window,document,console,setTimeout(){},getCurrentTournament(){return null}};
  vm.runInNewContext(cloudSrc,context,{filename:'cloud_unified_sync.js'});
  return {window,calls};
}

// 1-3 stable identity contract: unified layer never invents identity from mutable display fields.
assert(!cloudSrc.includes('createTournament('),'1 stable identity creation remains in canonical directional layer');
assert(!cloudSrc.includes('tournament.name==='),'2 rename must not drive identity matching');
assert(!/revision\s*===\s*.*identity/i.test(cloudSrc),'3 revision must not be identity');

// 4-6 creation/repeat behavior: one delegated push, no duplicate creation in unified layer, In Sync is no-op.
{
  const {window,calls}=makeCloud('LOCAL_CHANGES');
  await window.cpUnifiedSync();
  assert(calls.filter(x=>x==='push').length===1,'4 Desktop-created SYNC delegates one identity-safe push');
}
assert(!cloudSrc.includes('localKey=')&&!cloudSrc.includes('internalId='),'5 Web-created identity is not rewritten by unified UI');
{
  const {window,calls}=makeCloud('IN_SYNC');
  await window.cpUnifiedSync();
  assert(!calls.includes('push')&&!calls.includes('pull'),'6 repeated In Sync SYNC creates no duplicate or transfer');
}

// 7 local-only -> push.
{
  const {window,calls}=makeCloud('LOCAL_CHANGES');
  await window.cpUnifiedSync();
  assert(calls.join(',')==='check,push','7 local-only change -> push');
}

// 8 remote-only -> pull.
{
  const {window,calls}=makeCloud('REMOTE_CHANGES');
  await window.cpUnifiedSync();
  assert(calls.join(',')==='check,pull','8 remote-only change -> pull');
}

// 9 non-overlap conflict -> safe merge via directional pull, then push.
{
  const {window,calls}=makeCloud('CONFLICT',{status:'LOCAL_CHANGES',merged:true});
  const result=await window.cpUnifiedSync();
  assert(calls.join(',')==='check,pull,push'&&result.status==='IN_SYNC','9 non-overlapping changes -> merge then push');
}

// 10 same-field conflict -> explicit resolver, no silent push.
{
  const {window,calls}=makeCloud('CONFLICT',{status:'CONFLICT',conflict:true,conflicts:[{path:'pairings.liveBoards.1.0.result'}]});
  const result=await window.cpUnifiedSync();
  assert(calls.join(',')==='check,pull,resolve'&&result.awaitingResolution===true,'10 same-field divergence -> explicit conflict');
}

// 11 result-only mutation.
assert(webSrc.includes('board.result=item.remoteResult'),'11 Download Results updates board.result');
for(const forbidden of ['localBoards[item.localIndex]=','whiteKey=item.','blackKey=item.'])assert(!webSrc.includes(forbidden),'11 no pairing/player replacement');

// 12 blank Web never deletes Desktop.
{
  const plan=web.buildReconcilePlan([{board:1,whiteKey:'A',blackKey:'B',result:'1 - 0'}],[{id:'x',board:1,whiteKey:'A',blackKey:'B',result:'-'}]);
  assert(plan.remoteBlank===1&&plan.fills.length===0&&plan.conflicts.length===0,'12 blank Web result ignored');
}

// 13 conflict requires clear buttons, not OK/Cancel.
assert(webSrc.includes('Keep Desktop')&&webSrc.includes('Use Web'),'13 explicit conflict buttons present');
assert(!webSrc.includes('OK = Web')&&!webSrc.includes('Cancel = Desktop'),'13 OK/Cancel removed');

// 14-15 accepted result syncs canonical BASE before ACK and finishes In Sync.
assert(webSrc.indexOf('synchronizeResultsToCanonicalBase()')<webSrc.indexOf('acknowledgeWebResults(token,cloud.id,ids)'),'14 sync/base update precedes ACK');
assert(webSrc.includes("syncStatus:'IN_SYNC'"),'15 successful Download Results reports In Sync');

// 16 Public List is removed.
assert(cloudSrc.includes("text(el.textContent).toUpperCase()!=='PUBLIC LIST'")&&cloudSrc.includes("dataset.cpPublicListRemoved='1'"),'16 Public List removal contract');

// 17-19 obsolete actions hidden.
for(const label of ['upload current','pull current','upload as new'])assert(cloudSrc.includes(label),`missing obsolete action guard ${label}`);

// 20 Refresh is status-only: no push/pull.
{
  const {window,calls}=makeCloud('IN_SYNC');
  await window.cpCloudRefreshList();
  assert(calls.join(',')==='list,check'&&!calls.includes('push')&&!calls.includes('pull'),'20 Refresh updates list/status metadata only; no hidden sync');
}

// 21 Autosave never invokes cloud transfer in unified layer.
assert(!/autosave[\s\S]{0,120}(push\(|pull\()/i.test(cloudSrc),'21 Autosave performs no Cloud push/pull');

console.log('CLOUD_SYNC_DEV23_REGRESSION=PASS');
