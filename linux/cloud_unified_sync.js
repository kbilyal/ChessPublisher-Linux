(()=>{
'use strict';
if(window.__cpUnifiedCloudSyncLoaded)return;
window.__cpUnifiedCloudSyncLoaded=true;
const stats={syncs:0,pushes:0,pulls:0,conflicts:0,refreshes:0,resultRefreshes:0};
window.__cpUnifiedCloudSyncStats=stats;
let busy=false;
const legacyCloudRefreshList=typeof window.cpCloudRefreshList==='function'?window.cpCloudRefreshList.bind(window):null;
function text(v){return v==null?'':String(v).trim();}
function statusText(s){return text(s?.status||s).toUpperCase();}
function currentTournament(){try{return typeof getCurrentTournament==='function'?getCurrentTournament():null;}catch(_){return null;}}
function syncButton(){return document.getElementById('cpUnifiedSyncBtn');}
async function checkStatus(){
if(typeof window.cpCloudCheckStatus!=='function')throw new Error('Cloud sync status engine is unavailable.');
return window.cpCloudCheckStatus({quiet:true});
}
async function push(){
if(typeof window.cpCloudPushToCloud!=='function')throw new Error('Cloud push engine is unavailable.');
stats.pushes++;
return window.cpCloudPushToCloud();
}
async function pull(){
if(typeof window.cpCloudPullToDesktop!=='function')throw new Error('Cloud pull engine is unavailable.');
stats.pulls++;
return window.cpCloudPullToDesktop();
}
async function unifiedSync(){
if(busy)return {status:'BUSY'};
busy=true;stats.syncs++;
const button=syncButton();
if(button)button.disabled=true;
try{
let checked=await checkStatus();
let status=statusText(checked);
if(status==='IN_SYNC')return checked;
if(status==='LOCAL_CHANGES'){
return await push();
}
if(status==='REMOTE_CHANGES'){
return await pull();
}
if(status==='CONFLICT'){
stats.conflicts++;
// The existing directional engine owns BASE/LOCAL/REMOTE and performs
// the safe three-way merge. Pull here does NOT blindly overwrite.
const merged=await pull();
// Non-overlapping changes can be merged automatically. Finish the one-click
// SYNC by pushing the merged Desktop state back to the same Cloud object.
if(statusText(merged)==='LOCAL_CHANGES'&&merged?.merged&&!merged?.conflict){
return await push();
}
// Same-field divergence must remain explicit. The directional conflict UI
// presents Keep Desktop / Keep Cloud per field; nothing is silently chosen.
if(merged?.conflict){
if(typeof window.cpCloudResolveConflict==='function'){
await window.cpCloudResolveConflict();
}
return {status:'CONFLICT',conflict:true,awaitingResolution:true,details:merged};
}
return merged;
}
if(status==='OFFLINE')throw new Error(checked?.error?.message||'Cloud is offline or Organizer Token is not connected.');
throw new Error(`Unsupported Cloud sync state: ${status||'unknown'}`);
}finally{
busy=false;
if(button)button.disabled=false;
setTimeout(installUi,0);
}
}
async function refreshOnly({quiet=true}={}){
stats.refreshes++;
let listResult=null;
if(legacyCloudRefreshList){
try{listResult=await legacyCloudRefreshList({quiet:true});}
catch(error){
if(!quiet)throw error;
console.warn('My Online Tournaments metadata refresh failed:',error);
}
}
const checked=await checkStatus();
if(!quiet&&statusText(checked)==='OFFLINE'){
throw new Error(checked?.error?.message||'Cloud is offline or Organizer Token is not connected.');
}
if(checked&&typeof checked==='object')return {...checked,listResult};
return checked;
}
async function refreshAfterResults(){
stats.resultRefreshes++;
// Download Results performs a real unified SYNC before ACK. This hook is only
// a metadata/status refresh and must never invent LOCAL_CHANGES or mutate BASE.
return refreshOnly({quiet:true});
}
function hideLegacyActions(){
document.querySelectorAll('button,a').forEach(el=>{
const label=text(el.textContent).toLowerCase();
if(label==='upload current'||label==='pull current'||label==='upload as new'||label.includes('upload as new')){
el.style.display='none';
el.setAttribute('aria-hidden','true');
el.tabIndex=-1;
}
});
}
function removePublicList(){
const workspace=document.getElementById('cloudWorkspace')||document;
workspace.querySelectorAll('*').forEach(el=>{
if(el.children.length!==0||text(el.textContent).toUpperCase()!=='PUBLIC LIST')return;
let block=el;
let cursor=el.parentElement;
while(cursor&&cursor!==workspace&&cursor!==document.body){
const content=text(cursor.textContent).toUpperCase();
if(content.includes('MY ONLINE TOURNAMENTS')||content.includes('ONLINE & CLOUD'))break;
block=cursor;
if(cursor.matches?.('section,fieldset,.card,.panel,.box,.cloud-secondary-box,.cloud-list-box'))break;
cursor=cursor.parentElement;
}
block.style.display='none';
block.setAttribute('aria-hidden','true');
block.dataset.cpPublicListRemoved='1';
});
}
function installUi(){
hideLegacyActions();
removePublicList();
const panel=document.getElementById('cpDirectionalCloudPanel');
if(!panel)return false;
const actions=panel.querySelector('.cp-directional-main-actions');
if(actions){
actions.style.gridTemplateColumns='1fr';
if(!document.getElementById('cpUnifiedSyncBtn')){
actions.innerHTML='<button id="cpUnifiedSyncBtn" class="primary" type="button">⟳ SYNC</button>';
document.getElementById('cpUnifiedSyncBtn').onclick=()=>unifiedSync().catch(error=>{
console.error(error);
if(typeof window.appAlert==='function')window.appAlert(`SYNC failed.\n\n${error?.message||error}`,'SYNC');
else window.alert?.(`SYNC failed.\n\n${error?.message||error}`);
});
}
}
// Refresh is status/list metadata only. It must not push, pull, change current
// tournament, or resolve conflicts.
const refresh=document.getElementById('cpDirectionalCheckBtn');
if(refresh){
refresh.textContent='Refresh';
refresh.title='Refresh Cloud status and list metadata only. No tournament data is pushed or pulled.';
refresh.onclick=()=>refreshOnly({quiet:false}).catch(error=>{
console.error(error);
if(typeof window.appAlert==='function')window.appAlert(`Refresh failed.\n\n${error?.message||error}`,'Refresh');
});
}
const note=panel.querySelector('.cp-directional-local-note');
if(note)note.innerHTML='<b>SYNC chooses the safe direction automatically.</b> Desktop-only changes are pushed, Cloud-only changes are pulled, non-overlapping changes are merged, and same-field conflicts require an explicit choice. Autosave remains local only.';
return true;
}
window.cpUnifiedSync=unifiedSync;
window.cpCloudSyncCurrent=unifiedSync;
window.cpCloudRefreshList=refreshOnly;
window.cpUnifiedSyncRefreshFromResults=refreshAfterResults;
window.__cpUnifiedSyncTestHooks={statusText,unifiedSync,refreshOnly,refreshAfterResults,hideLegacyActions,removePublicList};
if(window.__CP_UNIFIED_SYNC_TEST__)return;
const observer=new MutationObserver(()=>installUi());
const start=()=>{
installUi();
observer.observe(document.documentElement,{childList:true,subtree:true});
let attempts=0;
const timer=setInterval(()=>{attempts++;if(installUi()||attempts>120)clearInterval(timer);},100);
};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
