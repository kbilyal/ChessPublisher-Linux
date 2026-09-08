#!/usr/bin/env python3
"""Linux UI + LocalEngine surface for integrated FIDE rating lists.

This adapter keeps the protected ChessPublisher.html byte-for-byte unchanged.
The local SQLite generation is authoritative on Linux, so a full rating-list
update does not repopulate the browser's giant in-memory FIDE map. Search and
registered-player review use the LocalEngine endpoints directly.
"""
from __future__ import annotations

import urllib.parse
from typing import Any

import chess_publisher_linux as cp

_APPLIED = False

_STYLE = r'''
<style id="cpIntegratedRatingListsStyle">
#cpIntegratedRatingLists{
  margin:7px 0 4px;padding:8px;border:1px solid #a9a9a9;border-radius:5px;
  background:#f8f8f8;font:12px/1.35 "Segoe UI",Tahoma,Arial,sans-serif
}
#cpIntegratedRatingLists .cp-rl-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:7px}
#cpIntegratedRatingLists .cp-rl-title{font-weight:700;font-size:13px}
#cpIntegratedRatingLists .cp-rl-safe{color:#365a2c;background:#edf7e9;border:1px solid #bed7b5;border-radius:4px;padding:3px 6px;white-space:nowrap}
#cpIntegratedRatingLists .cp-rl-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-bottom:7px}
#cpIntegratedRatingLists .cp-rl-card{border:1px solid #c6c6c6;background:#fff;border-radius:4px;padding:6px 7px;min-width:0}
#cpIntegratedRatingLists .cp-rl-card strong{display:block;margin-bottom:3px}
#cpIntegratedRatingLists .cp-rl-meta{color:#555;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#cpIntegratedRatingLists .cp-rl-status{font-weight:600}
#cpIntegratedRatingLists .cp-rl-actions{display:flex;gap:5px;align-items:center;flex-wrap:wrap}
#cpIntegratedRatingLists .cp-rl-note{margin-top:6px;color:#555;font-size:11px}
#cpIntegratedRatingLists .cp-rl-count{padding:3px 6px;border:1px solid #c8c8c8;border-radius:4px;background:#fff}
@media(max-width:900px){
  #cpIntegratedRatingLists .cp-rl-grid{grid-template-columns:1fr!important}
  #cpIntegratedRatingLists .cp-rl-safe{white-space:normal}
}
@media print{#cpIntegratedRatingLists{display:none!important}}
</style>
'''.encode('utf-8')

_SCRIPT = r'''
<script id="cpIntegratedRatingListsScript">
(function(){
  'use strict';
  if(window.__cpIntegratedRatingListsLoaded)return;
  window.__cpIntegratedRatingListsLoaded=true;

  const LISTS=[['std','Standard'],['rapid','Rapid'],['blitz','Blitz']];
  const stats={statusLoads:0,updates:0,rollbacksReported:0,serverSearches:0,searchFallbacks:0};
  window.__cpIntegratedRatingListsStats=stats;

  async function localFetch(path,options={}){
    if(typeof fetchLocalEngine==='function') return fetchLocalEngine(path,options,0);
    return fetch(path,options);
  }

  function text(value,fallback='—'){
    const s=String(value??'').trim();
    return s||fallback;
  }

  function number(value){
    const n=Number(value||0);
    return Number.isFinite(n)?n:0;
  }

  function niceDate(value){
    const raw=String(value||'').trim();
    if(!raw)return '—';
    const d=new Date(raw);
    return Number.isNaN(d.getTime())?raw:d.toLocaleString();
  }

  function setCard(type,item,status){
    const records=document.getElementById('cpRlRecords-'+type);
    const period=document.getElementById('cpRlPeriod-'+type);
    const updated=document.getElementById('cpRlUpdated-'+type);
    const state=document.getElementById('cpRlState-'+type);
    if(records)records.textContent=number(item?.records).toLocaleString();
    if(period)period.textContent=text(item?.period||item?.periodKey);
    if(updated)updated.textContent=niceDate(item?.updatedAt||status?.updatedAt);
    if(state){
      const ready=!!item?.records;
      state.textContent=ready?'Ready':'Not installed';
      state.title=text(item?.source,'Integrated local FIDE list');
    }
  }

  async function refreshPanel(){
    const panel=document.getElementById('cpIntegratedRatingLists');
    if(!panel)return null;
    try{
      const response=await localFetch('/fide/rating-lists/status',{cache:'no-store'});
      const status=await response.json().catch(()=>({}));
      if(!response.ok)throw new Error(status.error||'Rating-list status is unavailable.');
      stats.statusLoads++;
      for(const [type] of LISTS)setCard(type,status.lists?.[type]||{},status);
      const count=document.getElementById('cpRlPlayers');
      const generation=document.getElementById('cpRlGeneration');
      const reportBtn=document.getElementById('cpRlReportBtn');
      if(count)count.textContent=number(status.players).toLocaleString();
      if(generation)generation.textContent=text(status.generation,'none');
      if(reportBtn)reportBtn.disabled=!status.reportAvailable;
      panel.dataset.ready=status.ready?'1':'0';
      return status;
    }catch(err){
      panel.dataset.ready='0';
      for(const [type] of LISTS)setCard(type,{},{});
      const generation=document.getElementById('cpRlGeneration');
      if(generation)generation.textContent='offline / unavailable';
      return null;
    }
  }
  window.cpRefreshIntegratedRatingLists=refreshPanel;

  async function viewReport(){
    try{
      const response=await localFetch('/fide/rating-lists/report',{cache:'no-store'});
      const body=await response.text();
      if(!response.ok)throw new Error(body||'No rating-list update report is available yet.');
      if(typeof appAlert==='function')appAlert(body);
      else window.alert(body);
    }catch(err){
      const message=err?.message||String(err);
      if(typeof appAlert==='function')appAlert('Rating Lists\n\n'+message);
      else window.alert(message);
    }
  }
  window.cpViewIntegratedRatingListsReport=viewReport;

  async function updateRatingLists(){
    if(typeof fideBackgroundUpdateRunning!=='undefined'&&fideBackgroundUpdateRunning)return false;
    const buttons=[document.getElementById('btnAutoUpdateFide'),document.getElementById('cpRlUpdateBtn')].filter(Boolean);
    try{
      if(typeof fideBackgroundUpdateRunning!=='undefined')fideBackgroundUpdateRunning=true;
      buttons.forEach(b=>b.disabled=true);
      if(typeof updateFideAutoStatus==='function')updateFideAutoStatus('updating integrated rating lists…');

      // LINUX_DEV22_SERVER_ATOMIC_UPDATE:
      // The browser FIDE map is deliberately NOT modified here. The server builds
      // and validates a complete Standard/Rapid/Blitz SQLite generation and flips
      // one atomic pointer only after all three lists pass. Therefore a failed
      // network/parser/index update cannot leave a partial browser or server set.
      const response=await localFetch('/fide-update',{method:'POST',cache:'no-store'});
      const report=await response.json().catch(()=>({}));
      if(!response.ok||!report.ok){
        if(report.rolledBack)stats.rollbacksReported++;
        throw new Error(report.error||'Integrated rating-list update failed. The previous complete generation was kept.');
      }
      stats.updates++;
      await refreshPanel();
      if(typeof updateFideAutoStatus==='function')updateFideAutoStatus('integrated rating lists ready');
      if(typeof setStatus==='function')setStatus(`Rating Lists updated safely • ${number(report.players).toLocaleString()} players`);
      const suffix=Array.isArray(report.errors)&&report.errors.length
        ? '\n\nStandard/Rapid/Blitz are ready. Optional LEGACY directory warning: '+report.errors.join('; ')
        : '';
      const message='Integrated Rating Lists updated successfully.\n\n'+
        'Standard, Rapid and Blitz were activated as one atomic generation.\n'+
        'Tournament players were NOT modified.'+suffix;
      if(typeof appAlert==='function')appAlert(message); else window.alert(message);
      return true;
    }catch(err){
      await refreshPanel();
      if(typeof updateFideAutoStatus==='function')updateFideAutoStatus('update failed — previous generation kept');
      const message=err?.message||String(err);
      const body='Rating Lists update failed.\n\n'+message+'\n\nThe previous complete local rating-list generation remains active.';
      if(typeof appAlert==='function')appAlert(body); else window.alert(body);
      return false;
    }finally{
      if(typeof fideBackgroundUpdateRunning!=='undefined')fideBackgroundUpdateRunning=false;
      buttons.forEach(b=>b.disabled=false);
    }
  }
  window.cpUpdateIntegratedRatingLists=updateRatingLists;

  function installUpdateOverride(){
    // Keep manual/offline list import unchanged. Only replace the full automatic
    // update path on the Linux LocalEngine page.
    if(typeof window.downloadAndUpdateFideDatabases==='function'){
      window.downloadAndUpdateFideDatabases=updateRatingLists;
    }
    const button=document.getElementById('btnAutoUpdateFide');
    if(button){
      button.textContent='Update Rating Lists';
      button.onclick=updateRatingLists;
    }
  }

  function installSearchOverride(){
    if(window.__cpIntegratedRatingSearchInstalled)return;
    const original=window.queueFideSearch;
    if(typeof original!=='function')return;

    window.queueFideSearch=function(){
      clearTimeout(fideSearchTimer);
      fideSearchTimer=setTimeout(async()=>{
        const raw=String(typeof val==='function'?val('fideSearch'):(document.getElementById('fideSearch')?.value||'')).trim();
        latestSearchRequest++;
        const requestId=latestSearchRequest;
        if(raw.length<2){renderFideResults([]);return;}

        try{
          const response=await localFetch('/fide/players-search',{
            method:'POST',headers:{'Content-Type':'application/json'},
            body:JSON.stringify({query:raw,limit:60}),cache:'no-store'
          });
          const payload=await response.json().catch(()=>({}));
          if(!response.ok)throw new Error(payload.error||'Integrated rating-list search is unavailable.');
          if(requestId!==latestSearchRequest)return;
          stats.serverSearches++;
          const players=Array.isArray(payload.players)?payload.players:[];
          for(const player of players){
            try{if(typeof cacheFideDirectoryMetadata==='function')cacheFideDirectoryMetadata(player);}catch(_){ }
          }
          renderFideResults(players);
        }catch(err){
          if(requestId!==latestSearchRequest)return;
          stats.searchFallbacks++;
          // Fail soft to the existing in-memory/manual-list search without
          // changing it. The official local generation is never deleted.
          const q=raw.toLowerCase();
          const terms=q.split(/[\s,]+/).filter(Boolean);
          const out=[];
          try{
            for(const p of fideMainDb.values()){
              const key=String(p.searchKey||'').toLowerCase();
              if(terms.every(t=>key.includes(t))){out.push(p);if(out.length>=60)break;}
            }
          }catch(_){ }
          if(typeof renderFideSearchWithLegacy==='function')renderFideSearchWithLegacy(raw,requestId,out);
          else renderFideResults(out);
        }
      },55);
    };
    window.__cpIntegratedRatingSearchInstalled=true;
  }

  function insertPanel(){
    if(document.getElementById('cpIntegratedRatingLists'))return;
    const mainButton=document.getElementById('btnAutoUpdateFide');
    const cluster=mainButton?.closest?.('.button-cluster');
    if(!cluster)return;

    for(const title of document.querySelectorAll('.button-cluster-title')){
      if(String(title.textContent||'').trim()==='FIDE Database')title.textContent='Integrated Rating Lists';
      if(String(title.textContent||'').trim()==='Local Lists')title.textContent='Manual / Offline Lists';
    }
    const review=document.getElementById('btnUpdateRegisteredFromFide');
    if(review)review.textContent='Review Player Updates';

    const panel=document.createElement('div');
    panel.id='cpIntegratedRatingLists';
    panel.innerHTML=`
      <div class="cp-rl-head">
        <div class="cp-rl-title">Integrated Rating Lists</div>
        <div class="cp-rl-safe">Tournament data is not changed automatically</div>
      </div>
      <div class="cp-rl-grid">
        ${LISTS.map(([type,label])=>`
          <div class="cp-rl-card">
            <strong>${label}</strong>
            <div>Records: <b id="cpRlRecords-${type}">0</b></div>
            <div class="cp-rl-meta">List: <span id="cpRlPeriod-${type}">—</span></div>
            <div class="cp-rl-meta">Updated: <span id="cpRlUpdated-${type}">—</span></div>
            <div class="cp-rl-meta">Status: <span class="cp-rl-status" id="cpRlState-${type}">Not installed</span></div>
          </div>`).join('')}
      </div>
      <div class="cp-rl-actions">
        <button class="primary" id="cpRlUpdateBtn" type="button">Update Rating Lists</button>
        <button id="cpRlReportBtn" type="button" disabled>View Last Update Report</button>
        <button id="cpRlReviewBtn" type="button">Review Player Updates</button>
        <span class="cp-rl-count">Local directory: <b id="cpRlPlayers">0</b></span>
      </div>
      <div class="cp-rl-note">
        Updating rating lists does not automatically modify tournament players.
        Active generation: <span id="cpRlGeneration">none</span>.
        Search uses the local integrated database first; manual/offline lists remain available as fallback.
      </div>`;
    cluster.insertAdjacentElement('afterend',panel);
    document.getElementById('cpRlUpdateBtn')?.addEventListener('click',updateRatingLists);
    document.getElementById('cpRlReportBtn')?.addEventListener('click',viewReport);
    document.getElementById('cpRlReviewBtn')?.addEventListener('click',()=>{
      if(typeof openRegisteredPlayersFideUpdateDialog==='function')openRegisteredPlayersFideUpdateDialog();
    });
  }

  function install(){
    insertPanel();
    installUpdateOverride();
    installSearchOverride();
    refreshPanel();
    setTimeout(()=>{insertPanel();installUpdateOverride();installSearchOverride();refreshPanel();},0);
    setTimeout(()=>{insertPanel();installUpdateOverride();refreshPanel();},300);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();
</script>
'''.encode('utf-8')


def inject_rating_lists_ui(data: bytes) -> bytes:
    if b'id="cpIntegratedRatingListsScript"' in data:
        return data
    head = data.lower().rfind(b'</head>')
    if head >= 0:
        data = data[:head] + _STYLE + data[head:]
    else:
        data = _STYLE + data
    body = data.lower().rfind(b'</body>')
    if body >= 0:
        data = data[:body] + _SCRIPT + data[body:]
    else:
        data += _SCRIPT
    return data


def apply() -> None:
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True

    original_get = cp.Handler.do_GET

    def do_get(self: cp.Handler) -> None:
        path = urllib.parse.urlsplit(self.path).path
        if path == '/fide/rating-lists/status':
            store = getattr(getattr(self.engine, 'fide', None), 'integrated_rating_lists', None)
            if store is None:
                return self._json(503, {'ok': False, 'ready': False, 'error': 'Integrated rating-list store is not attached.'})
            status = store.status().as_dict()
            status.update({
                'platform': 'linux',
                'reportAvailable': store.report_file.is_file(),
                'tournamentPlayersChanged': False,
            })
            return self._json(200, status)
        if path == '/fide/rating-lists/report':
            store = getattr(getattr(self.engine, 'fide', None), 'integrated_rating_lists', None)
            if store is None or not store.report_file.is_file():
                return self._json(404, {'ok': False, 'error': 'No integrated rating-list update report is available yet.'})
            return self._text(200, store.report_file.read_bytes(), 'text/plain; charset=utf-8')
        return original_get(self)

    cp.Handler.do_GET = do_get  # type: ignore[assignment]

    original_serve = cp.Handler._serve_app

    def serve_app(self: cp.Handler) -> Any:
        original_text = self._text

        def rating_text(status: int, data: bytes, content_type: str) -> Any:
            if content_type.lower().startswith('text/html'):
                data = inject_rating_lists_ui(data)
            return original_text(status, data, content_type)

        self._text = rating_text  # type: ignore[method-assign]
        try:
            return original_serve(self)
        finally:
            self._text = original_text  # type: ignore[method-assign]

    cp.Handler._serve_app = serve_app  # type: ignore[assignment]
