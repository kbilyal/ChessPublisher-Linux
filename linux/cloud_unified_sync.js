(()=>{
  'use strict';
  if(window.__cpUnifiedCloudSyncLoaded)return;
  window.__cpUnifiedCloudSyncLoaded=true;

  const stats={syncs:0,pushes:0,pulls:0,conflicts:0,resultRefreshes:0};
  window.__cpUnifiedCloudSyncStats=stats;
  let busy=false;

  function text(v){return v==null?'':String(v).trim();}
  function currentTournament(){try{return typeof getCurrentTournament==='function'?getCurrentTournament():null;}catch(_){return null;}}
  function statusText(s){return text(s?.status||s).toUpperCase();}

  async function unifiedSync(){
    if(busy)return {status:'BUSY'};
    busy=true;stats.syncs++;
    const button=document.getElementById('cpUnifiedSyncBtn');
    if(button)button.disabled=true;
    try{
      if(typeof window.cpCloudCheckStatus!=='function')throw new Error('Cloud sync status engine is unavailable.');
      const checked=await window.cpCloudCheckStatus({quiet:true});
      const status=statusText(checked);
      if(status==='IN_SYNC')return checked;
      if(status==='LOCAL_CHANGES'){
        if(typeof window.cpCloudPushToCloud!=='function')throw new Error('Cloud push engine is unavailable.');
        stats.pushes++;
        return await window.cpCloudPushToCloud();
      }
      if(status==='REMOTE_CHANGES'){
        if(typeof window.cpCloudPullToDesktop!=='function')throw new Error('Cloud pull engine is unavailable.');
        stats.pulls++;
        return await window.cpCloudPullToDesktop();
      }
      if(status==='CONFLICT'){
        stats.conflicts++;
        if(typeof window.cpCloudPullToDesktop!=='function')throw new Error('Cloud merge engine is unavailable.');
        const pulled=await window.cpCloudPullToDesktop();
        if(pulled?.conflict&&typeof window.cpCloudResolveConflict==='function'){
          await window.cpCloudResolveConflict();
        }
        return pulled;
      }
      if(status==='OFFLINE')throw new Error(checked?.error?.message||'Cloud is offline or Organizer Token is not connected.');
      throw new Error(`Unsupported Cloud sync state: ${status||'unknown'}`);
    }finally{
      busy=false;
      if(button)button.disabled=false;
      setTimeout(installUi,0);
    }
  }

  async function refreshAfterResults(){
    stats.resultRefreshes++;
    const tournament=currentTournament();
    if(tournament){
      tournament.cloud=tournament.cloud&&typeof tournament.cloud==='object'?tournament.cloud:{};
      tournament.cloud.syncStatus='LOCAL_CHANGES';
      tournament.cloud.lastSyncStateRefreshAt=new Date().toISOString();
    }
    if(typeof window.cpCloudCheckStatus==='function'){
      try{return await window.cpCloudCheckStatus({quiet:true});}catch(error){console.warn('SYNC status refresh after Download Results failed:',error);}
    }
    return null;
  }

  function hideLegacyUi(){
    document.querySelectorAll('button,a').forEach(el=>{
      const label=text(el.textContent).toLowerCase();
      if(label==='upload current'||label==='pull current'||label==='upload as new'||label.includes('upload as new')){
        el.style.display='none';el.setAttribute('aria-hidden','true');el.tabIndex=-1;
      }
    });
    document.querySelectorAll('*').forEach(el=>{
      if(el.children.length===0&&text(el.textContent).toUpperCase()==='PUBLIC LIST'){
        el.style.display='none';el.setAttribute('aria-hidden','true');
      }
    });
  }

  function installUi(){
    hideLegacyUi();
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
    const note=panel.querySelector('.cp-directional-local-note');
    if(note)note.innerHTML='<b>SYNC is automatic-direction.</b> Desktop-only changes are pushed, Cloud-only changes are pulled, and conflicts require an explicit choice. Autosave remains local only.';
    return true;
  }

  window.cpUnifiedSync=unifiedSync;
  window.cpCloudSyncCurrent=unifiedSync;
  window.cpUnifiedSyncRefreshFromResults=refreshAfterResults;

  const observer=new MutationObserver(()=>installUi());
  const start=()=>{
    installUi();
    observer.observe(document.documentElement,{childList:true,subtree:true});
    let attempts=0;const timer=setInterval(()=>{attempts++;if(installUi()||attempts>120)clearInterval(timer);},100);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
