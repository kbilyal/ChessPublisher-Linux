(function(root,factory){
const api=factory(root);
if(typeof module==='object'&&module.exports)module.exports=api;
if(root&&root.document)api.install();
})(typeof window!=='undefined'?window:null,function(root){
'use strict';
const ALLOWED_RESULTS=new Set(['-','1 - 0','½ - ½','0 - 1','1F - 0F','0F - 1F','0F - 0F','PAB','½ BYE','0 BYE']);
const stats={downloads:0,applied:0,conflicts:0,keptDesktop:0,unmatched:0,unsupported:0,acknowledged:0,ackFailures:0,syncs:0,syncFailures:0};
let busy=false;
function text(value){return value==null?'':String(value).trim();}
function canonicalResult(value){
const raw=text(value);
if(!raw||raw==='-')return '-';
const compact=raw.toUpperCase().replace(/\s+/g,'').replace(/:/g,'-');
if(compact==='1-0')return '1 - 0';
if(compact==='0-1')return '0 - 1';
if(compact==='1F-0F')return '1F - 0F';
if(compact==='0F-1F')return '0F - 1F';
if(compact==='0F-0F')return '0F - 0F';
if(compact==='½-½'||compact==='1/2-1/2'||compact==='0.5-0.5'||compact==='=')return '½ - ½';
if(compact==='PAB')return 'PAB';
if(compact==='½BYE'||compact==='1/2BYE'||compact==='0.5BYE')return '½ BYE';
if(compact==='0BYE')return '0 BYE';
return raw;
}
function boardNumber(board,index=-1){
const n=Number(board?.board);
return Number.isInteger(n)&&n>0?n:(index>=0?index+1:0);
}
function pairingIdentity(board,index=-1){
const white=text(board?.whiteKey);
const black=text(board?.blackKey);
const number=boardNumber(board,index);
if(!number||!white||!black)return '';
return `board:${number}|w:${white}|b:${black}`;
}
function buildReconcilePlan(localBoards,remoteBoards){
const local=Array.isArray(localBoards)?localBoards:[];
const remote=Array.isArray(remoteBoards)?remoteBoards:[];
const byIdentity=new Map();
local.forEach((board,index)=>{
const key=pairingIdentity(board,index);
if(!key)return;
if(!byIdentity.has(key))byIdentity.set(key,[]);
byIdentity.get(key).push(index);
});
const plan={fills:[],conflicts:[],identical:0,identicalEntries:[],remoteBlank:0,unmatched:[],unsupported:[]};
remote.forEach((remoteBoard,remoteIndex)=>{
const remoteResult=canonicalResult(remoteBoard?.result);
if(remoteResult==='-'){plan.remoteBlank++;return;}
if(!ALLOWED_RESULTS.has(remoteResult)){
plan.unsupported.push({remoteIndex,board:remoteBoard,result:remoteResult});
return;
}
const key=pairingIdentity(remoteBoard,remoteIndex);
const matches=key?byIdentity.get(key)||[]:[];
if(matches.length!==1){
plan.unmatched.push({remoteIndex,board:remoteBoard,reason:matches.length>1?'ambiguous_pairing':'pairing_not_found'});
return;
}
const localIndex=matches[0];
const localBoard=local[localIndex];
const localResult=canonicalResult(localBoard?.result);
const entry={localIndex,remoteIndex,localBoard,remoteBoard,localResult,remoteResult,submissionId:text(remoteBoard?.id)};
if(localResult===remoteResult){plan.identical++;plan.identicalEntries.push(entry);return;}
if(localResult==='-'){plan.fills.push(entry);return;}
plan.conflicts.push(entry);
});
return plan;
}
function languageBg(){
try{return typeof root.getLanguage==='function'&&root.getLanguage()==='bg';}catch(_){return false;}
}
async function alertUser(message,title='Download Results'){
if(typeof root.appAlert==='function')return root.appAlert(message,title);
if(root.alert)return root.alert(message);
}
function boardDescription(board,index,round){
const boardNo=boardNumber(board,index);
let white=text(board?.whiteKey)||'—';
let black=text(board?.blackKey)||'—';
try{
const w=typeof root.resolveRegisteredPlayer==='function'?root.resolveRegisteredPlayer(board?.whiteKey):null;
const b=typeof root.resolveRegisteredPlayer==='function'?root.resolveRegisteredPlayer(board?.blackKey):null;
if(w?.name)white=w.name;
if(b?.name)black=b.name;
}catch(_){}
return {boardNo,white,black,label:`Round ${round} · Board ${boardNo}`};
}
function conflictChoiceModal(item,round){
if(typeof root.cpChooseWebResultConflict==='function'){
return Promise.resolve(root.cpChooseWebResultConflict(item,round)).then(choice=>choice==='web'?'web':'desktop');
}
const doc=root.document;
if(!doc?.body)return Promise.resolve('desktop');
const old=doc.getElementById('cpWebResultConflictModal');
old?.remove?.();
const d=boardDescription(item.localBoard,item.localIndex,round);
const bg=languageBg();
const arbiter=text(item.remoteBoard?.arbiterName)||'Web Arbiter';
const updated=text(item.remoteBoard?.updatedAt);
const sourceLine=updated?`${arbiter} · ${updated}`:arbiter;
return new Promise(resolve=>{
const overlay=doc.createElement('div');
overlay.id='cpWebResultConflictModal';
overlay.style.cssText='position:fixed;inset:0;z-index:32000;background:rgba(0,0,0,.28);display:flex;align-items:center;justify-content:center;padding:20px';
const box=doc.createElement('div');
box.style.cssText='width:min(620px,96vw);background:#fff;border:1px solid #77818b;box-shadow:0 18px 55px rgba(0,0,0,.35);padding:18px;border-radius:7px';
box.innerHTML=`<div style="font-size:17px;font-weight:800;margin-bottom:10px">${bg?'Различен резултат':'Result conflict'} — ${d.label}</div>
<div style="font-size:14px;margin-bottom:10px"><b>${d.white}</b> — <b>${d.black}</b></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
<div style="border:1px solid #cfd6dd;padding:10px"><div style="font-size:11px;font-weight:800">Desktop</div><div style="font-size:20px;font-weight:800">${item.localResult}</div></div>
<div style="border:1px solid #cfd6dd;padding:10px"><div style="font-size:11px;font-weight:800">Web</div><div style="font-size:20px;font-weight:800">${item.remoteResult}</div></div>
</div>
<div style="font-size:11px;color:#5d6771;margin-bottom:14px">${sourceLine}</div>
<div style="display:flex;justify-content:flex-end;gap:10px">
<button id="cpKeepDesktopResultBtn" type="button">${bg?'Запази Desktop':'Keep Desktop'}</button>
<button id="cpUseWebResultBtn" class="primary" type="button">${bg?'Използвай Web':'Use Web'}</button>
</div>`;
overlay.appendChild(box);
doc.body.appendChild(overlay);
let done=false;
const finish=choice=>{
if(done)return;
done=true;
overlay.remove();
resolve(choice);
};
box.querySelector('#cpKeepDesktopResultBtn').onclick=()=>finish('desktop');
box.querySelector('#cpUseWebResultBtn').onclick=()=>finish('web');
});
}
async function organizerToken(){
if(typeof root.cpNativeHubSecretGet!=='function'||typeof root.cpOnlineOrganizerSecretKey!=='function')return '';
return text(await root.cpNativeHubSecretGet(root.cpOnlineOrganizerSecretKey()));
}
function cloudLibrary(){
const lib=root.ChessPublisherCloudWorkspaceApi;
if(!lib||typeof lib.createClient!=='function')throw new Error('Cloud Workspace API is unavailable.');
return lib;
}
function cloudClient(){
const lib=cloudLibrary();
return lib.createClient({clientVersion:String(root.document?.documentElement?.dataset?.chesspublisherVersion||'1.06.00-beta.34').trim()});
}
async function organizerApiRequest(token,path,options={}){
const lib=cloudLibrary();
const base=text(lib.DEFAULT_BASE_URL).replace(/\/+$/,'');
if(!base)throw new Error('Cloud API base URL is unavailable.');
const headers=new Headers(options.headers||{});
headers.set('Accept','application/json');
headers.set('Authorization',`Bearer ${token}`);
let body=options.body;
if(body!==undefined&&body!==null&&typeof body!=='string'){
headers.set('Content-Type','application/json');
body=JSON.stringify(body);
}
const controller=typeof AbortController!=='undefined'?new AbortController():null;
const timer=controller?setTimeout(()=>controller.abort(),45000):null;
try{
const response=await root.fetch(`${base}${path}`,{...options,headers,body,cache:'no-store',...(controller?{signal:controller.signal}:{})});
const raw=await response.text();
let payload={};
if(raw){try{payload=JSON.parse(raw);}catch{payload={raw};}}
if(!response.ok){
const error=new Error(text(payload?.message||payload?.error)||`Cloud request failed (${response.status}).`);
error.status=response.status;error.code=text(payload?.error||payload?.code)||'cloud_api_error';error.payload=payload;
throw error;
}
return payload;
}catch(error){
if(error?.name==='AbortError')throw new Error('Cloud results request timed out.');
throw error;
}finally{if(timer!==null)clearTimeout(timer);}
}
async function findRemoteReadOnly(client,token,tournament){
const direct=text(tournament?.cloud?.cloudTournamentId);
if(direct)return {id:direct};
const internalId=text(tournament?.cloud?.internalId);
if(!internalId)throw new Error('This tournament is not linked to Cloud yet. SYNC it first.');
const listed=await client.listTournaments(token);
const rows=Array.isArray(listed?.tournaments)?listed.tournaments:[];
const matches=rows.filter(row=>text(row?.localKey)===internalId);
if(matches.length>1)throw new Error('Multiple Cloud tournaments share this internalId. Results were not downloaded.');
if(matches.length!==1)throw new Error('No matching Cloud tournament was found. SYNC this tournament first.');
return matches[0];
}
async function verifyRemoteIdentity(client,token,remote,tournament){
const id=text(remote?.id||remote);
if(!id)throw new Error('Cloud tournament ID is missing.');
const metaResponse=await client.getTournament(token,id);
const meta=metaResponse?.tournament||remote||{};
const localInternal=text(tournament?.cloud?.internalId);
const remoteInternal=text(meta?.localKey);
if(localInternal&&remoteInternal&&localInternal!==remoteInternal){
throw new Error('Cloud tournament identity does not match this Desktop tournament. Results were not changed.');
}
return {id,revision:Math.max(0,Number(meta?.revision)||0),meta};
}
async function listPendingWebResults(token,cloudId,round){
const payload=await organizerApiRequest(token,`/api/v1/cloud/tournaments/${encodeURIComponent(cloudId)}/arbiter-results`,{method:'GET'});
const all=Array.isArray(payload?.results)?payload.results:[];
return all.filter(item=>Number(item?.round)===round);
}
async function acknowledgeWebResults(token,cloudId,submissionIds){
const ids=[...new Set((submissionIds||[]).map(text).filter(Boolean))];
if(!ids.length)return 0;
const payload=await organizerApiRequest(token,`/api/v1/cloud/tournaments/${encodeURIComponent(cloudId)}/arbiter-results/ack`,{
method:'POST',body:{submissionIds:ids}
});
const count=Math.max(0,Number(payload?.acknowledged)||0);
stats.acknowledged+=count;
return count;
}
function refreshDerivedViews(){
for(const name of ['recalculateRoundHistoryState','renderLivePairings','updateGacruxPanel','refreshPairingStandingsPanel','refreshFinalStandings']){
try{
if(typeof root[name]==='function'){
if(name==='renderLivePairings')root[name](true); else root[name]();
}
}catch(error){console.warn(`Download Results: ${name} refresh failed`,error);}
}
try{root.scheduleTieBreakCheckerAutoCheck?.(250);}catch(_){}
try{root.cpRefreshRoundControlLog?.();}catch(_){}
}
function statusText(value){return text(value?.status||value).toUpperCase();}
async function synchronizeResultsToCanonicalBase(){
const sync=typeof root.cpUnifiedSync==='function'
? root.cpUnifiedSync
: (typeof root.cpCloudSyncCurrent==='function'?root.cpCloudSyncCurrent:null);
if(!sync)throw new Error('Unified Cloud SYNC is unavailable. Results remain local and pending Web submissions were not acknowledged.');
stats.syncs++;
let result;
try{result=await sync();}catch(error){stats.syncFailures++;throw error;}
if(result?.conflict||['CONFLICT','OFFLINE','REMOTE_CHANGES','LOCAL_CHANGES','BUSY'].includes(statusText(result))){
stats.syncFailures++;
throw new Error('Results were saved locally, but SYNC did not reach In Sync. Pending Web submissions were not acknowledged.');
}
if(typeof root.cpCloudCheckStatus==='function'){
const verified=await root.cpCloudCheckStatus({quiet:true});
if(statusText(verified)!=='IN_SYNC'){
stats.syncFailures++;
throw new Error(`Results were saved locally, but Cloud status is ${statusText(verified)||'unknown'} after SYNC. Pending Web submissions were not acknowledged.`);
}
result={...result,status:'IN_SYNC',revision:Number(verified?.revision||verified?.cloud?.revision||result?.revision)||result?.revision};
}
try{await root.cpUnifiedSyncRefreshFromResults?.();}catch(error){console.warn('Download Results: sync status refresh failed',error);}
return result||{status:'IN_SYNC'};
}
function summaryText(round,pendingCount,applied,plan,keptDesktop,acknowledged,ackWarning=''){
const bg=languageBg();
const mismatch=plan.unmatched.length;
const unsupported=plan.unsupported.length;
const warning=ackWarning?`\n\n${bg?'Внимание':'Warning'}: ${ackWarning}`:'';
return (bg
? `Web резултатите за Round ${round} са проверени.\n\nPending Web резултати: ${pendingCount}\nПриложени от Web: ${applied}\nОставени Desktop резултати при конфликт: ${keptDesktop}\nВече еднакви: ${plan.identical}\nОтбелязани като прегледани: ${acknowledged}\nОставени pending заради различен жребий: ${mismatch}\nНеподдържани Web резултати: ${unsupported}`
: `Web results for Round ${round} were checked.\n\nPending Web results: ${pendingCount}\nApplied from Web: ${applied}\nDesktop results kept after conflicts: ${keptDesktop}\nAlready identical: ${plan.identical}\nAcknowledged as reviewed: ${acknowledged}\nLeft pending because pairings differ: ${mismatch}\nUnsupported Web results: ${unsupported}`)+warning;
}
async function downloadResults(){
if(busy)return false;
busy=true;
let localCommitted=false;
const button=root.document?.getElementById('cpDownloadWebResultsBtn');
if(button)button.disabled=true;
try{
const tournament=typeof root.getCurrentTournament==='function'?root.getCurrentTournament():null;
if(!tournament)throw new Error('No tournament is open.');
const round=Math.max(0,Number(typeof root.getSelectedPairingRoundNumber==='function'?root.getSelectedPairingRoundNumber():0)||0);
if(!round)throw new Error('No pairing round is selected.');
if(typeof root.isSelectedRoundEditable==='function'&&!root.isSelectedRoundEditable()){
throw new Error(`Round ${round} is read-only history. Select the current editable round before downloading web results.`);
}
const localBoards=typeof root.getLivePairingBoards==='function'?root.getLivePairingBoards():[];
if(!Array.isArray(localBoards)||!localBoards.length)throw new Error(`Round ${round} has no Desktop pairings.`);
const token=await organizerToken();
if(!token)throw new Error('Organizer Token is not connected.');
const client=cloudClient();
const remote=await findRemoteReadOnly(client,token,tournament);
const cloud=await verifyRemoteIdentity(client,token,remote,tournament);
const pending=await listPendingWebResults(token,cloud.id,round);
stats.downloads++;
if(!pending.length){
try{root.setStatus?.(`Download Results • Round ${round} • no pending Web results`);}catch(_){}
await alertUser(languageBg()?`Няма pending Web резултати за Round ${round}.`:`There are no pending Web results for Round ${round}.`);
return {ok:true,round,revision:cloud.revision,applied:0,pending:0};
}
const plan=buildReconcilePlan(localBoards,pending);
stats.conflicts+=plan.conflicts.length;
stats.unmatched+=plan.unmatched.length;
stats.unsupported+=plan.unsupported.length;
const accepted=[...plan.fills];
const reviewedIds=plan.fills.map(item=>item.submissionId).concat(plan.identicalEntries.map(item=>item.submissionId));
let keptDesktop=0;
for(const item of plan.conflicts){
const choice=await conflictChoiceModal(item,round);
if(choice==='web')accepted.push(item);
else keptDesktop++;
if(item.submissionId)reviewedIds.push(item.submissionId);
}
stats.keptDesktop+=keptDesktop;
let applied=0;
for(const item of accepted){
const board=localBoards[item.localIndex];
if(!board)continue;
// RESULT-ONLY SAFETY: never replace a board, colors, players or pairing identity.
// Only board.result changes after exact board number + White/Black key matching.
board.result=item.remoteResult;
applied++;
}
if(applied){
if(!tournament.cloud||typeof tournament.cloud!=='object')tournament.cloud={};
tournament.cloud.lastWebResultsDownloadAt=new Date().toISOString();
tournament.cloud.lastWebResultsDownloadRevision=cloud.revision;
tournament.cloud.lastWebResultsDownloadRound=round;
try{root.stateDirty=true;}catch(_){}
if(typeof root.saveData==='function')await Promise.resolve(root.saveData());
localCommitted=true;
refreshDerivedViews();
try{root.setStatus?.(`Download Results • Round ${round} • ${applied} Web result(s) applied locally`);}catch(_){}
try{setTimeout(()=>root.checkTournamentCompletionPrompt?.(),40);}catch(_){}
}
// CANONICAL BASE SAFETY:
// Download Results and normal SYNC must share the same stable identity and BASE.
// Sync the locally accepted decisions to the already-linked Cloud object BEFORE ACK.
const syncResult=await synchronizeResultsToCanonicalBase();
if(!tournament.cloud||typeof tournament.cloud!=='object')tournament.cloud={};
tournament.cloud.lastWebResultsSyncAt=new Date().toISOString();
tournament.cloud.lastWebResultsDownloadRevision=Math.max(0,Number(syncResult?.revision||tournament.cloud?.baseRevision||cloud.revision)||0);
if(typeof root.saveData==='function')await Promise.resolve(root.saveData());
localCommitted=true;
let acknowledged=0;
let ackWarning='';
const ids=[...new Set(reviewedIds.map(text).filter(Boolean))];
if(ids.length){
try{
acknowledged=await acknowledgeWebResults(token,cloud.id,ids);
tournament.cloud.lastWebResultsAcknowledgedAt=new Date().toISOString();
tournament.cloud.lastWebResultsAcknowledgedCount=acknowledged;
if(typeof root.saveData==='function')await Promise.resolve(root.saveData());
}catch(error){
stats.ackFailures++;
ackWarning=languageBg()
? `Резултатите са записани и синхронизирани, но Web опашката не можа да бъде потвърдена: ${error?.message||error}`
: `Results were saved and synchronized, but the Web queue could not be acknowledged: ${error?.message||error}`;
}
}
if(!applied){
try{root.setStatus?.(`Download Results • Round ${round} • reviewed ${ids.length}, no Desktop result changes`);}catch(_){}
}else{
try{root.setStatus?.(`Download Results • Round ${round} • ${applied} result(s) applied · In Sync`);}catch(_){}
}
stats.applied+=applied;
await alertUser(summaryText(round,pending.length,applied,plan,keptDesktop,acknowledged,ackWarning));
return {ok:true,round,revision:tournament.cloud.lastWebResultsDownloadRevision,pending:pending.length,applied,keptDesktop,acknowledged,plan,ackWarning,syncStatus:'IN_SYNC'};
}catch(error){
const message=error?.message||String(error);
const prefix=localCommitted
? (languageBg()?'Резултатите са запазени локално, но не са премахнати от Web pending опашката.\n\n':'Results were saved locally, but pending Web submissions were not acknowledged.\n\n')
: (languageBg()?'Download Results не промени турнира.\n\n':'Download Results did not change the tournament.\n\n');
await alertUser(prefix+message);
return {ok:false,error:message,localCommitted};
}finally{
busy=false;
if(button)button.disabled=false;
}
}
function installButton(){
if(!root.document||root.document.getElementById('cpDownloadWebResultsBtn'))return;
const toolbar=root.document.querySelector('#pairings .live-pairing-toolbar');
if(!toolbar)return;
const button=root.document.createElement('button');
button.id='cpDownloadWebResultsBtn';
button.type='button';
button.textContent='Download Results';
button.title='Download pending Web / Arbiter Access results for the selected round. Conflicts use Keep Desktop / Use Web; successful decisions are synchronized before acknowledgement.';
button.addEventListener('click',downloadResults);
const anchor=root.document.getElementById('pairingsChessResultsPublishBtn');
if(anchor?.parentElement===toolbar)anchor.insertAdjacentElement('afterend',button);
else toolbar.appendChild(button);
}
function install(){
if(root.__cpWebResultsDownloadLoaded)return;
root.__cpWebResultsDownloadLoaded=true;
root.cpDownloadWebResults=downloadResults;
root.__cpWebResultsDownloadStats=stats;
root.__cpWebResultsDownloadTestHooks={canonicalResult,boardNumber,pairingIdentity,buildReconcilePlan,conflictChoiceModal,synchronizeResultsToCanonicalBase};
installButton();
setTimeout(installButton,0);
setTimeout(installButton,300);
}
return {canonicalResult,boardNumber,pairingIdentity,buildReconcilePlan,conflictChoiceModal,synchronizeResultsToCanonicalBase,install,downloadResults,stats};
});
