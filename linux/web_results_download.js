(function(root,factory){
  const api=factory(root);
  if(typeof module==='object'&&module.exports)module.exports=api;
  if(root&&root.document)api.install();
})(typeof window!=='undefined'?window:null,function(root){
  'use strict';

  const ALLOWED_RESULTS=new Set(['-','1 - 0','½ - ½','0 - 1','1F - 0F','0F - 1F','0F - 0F','PAB','½ BYE','0 BYE']);
  const stats={downloads:0,applied:0,conflicts:0,keptDesktop:0,unmatched:0,unsupported:0};
  let busy=false;

  function text(value){return value==null?'':String(value).trim();}
  function canonicalResult(value){
    let raw=text(value);
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

  function pairingIdentity(board){
    const white=text(board?.whiteKey);
    const black=text(board?.blackKey);
    if(!white&&!black)return '';
    return `w:${white}|b:${black}`;
  }

  function buildReconcilePlan(localBoards,remoteBoards){
    const local=Array.isArray(localBoards)?localBoards:[];
    const remote=Array.isArray(remoteBoards)?remoteBoards:[];
    const byIdentity=new Map();
    local.forEach((board,index)=>{
      const key=pairingIdentity(board);
      if(!key)return;
      if(!byIdentity.has(key))byIdentity.set(key,[]);
      byIdentity.get(key).push(index);
    });

    const plan={fills:[],conflicts:[],identical:0,remoteBlank:0,unmatched:[],unsupported:[]};
    remote.forEach((remoteBoard,remoteIndex)=>{
      const remoteResult=canonicalResult(remoteBoard?.result);
      if(remoteResult==='-'){plan.remoteBlank++;return;}
      if(!ALLOWED_RESULTS.has(remoteResult)){
        plan.unsupported.push({remoteIndex,board:remoteBoard,result:remoteResult});
        return;
      }
      const key=pairingIdentity(remoteBoard);
      const matches=key?byIdentity.get(key)||[]:[];
      if(matches.length!==1){
        plan.unmatched.push({remoteIndex,board:remoteBoard,reason:matches.length>1?'ambiguous_pairing':'pairing_not_found'});
        return;
      }
      const localIndex=matches[0];
      const localBoard=local[localIndex];
      const localResult=canonicalResult(localBoard?.result);
      const entry={localIndex,remoteIndex,localBoard,remoteBoard,localResult,remoteResult};
      if(localResult===remoteResult){plan.identical++;return;}
      if(localResult==='-'){plan.fills.push(entry);return;}
      plan.conflicts.push(entry);
    });
    return plan;
  }

  function extractTournament(snapshot,fallbackName=''){
    const tournaments=snapshot?.data?.tournaments;
    if(!tournaments||typeof tournaments!=='object')throw new Error('Cloud snapshot does not contain tournament data.');
    const keys=Object.keys(tournaments);
    const requested=text(snapshot?.data?.currentTournament||snapshot?.currentTournament||fallbackName);
    const name=requested&&tournaments[requested]?requested:(keys[0]||requested);
    if(!name||!tournaments[name])throw new Error('Cloud snapshot does not contain its tournament.');
    return {name,tournament:tournaments[name]};
  }

  function languageBg(){
    try{return typeof root.getLanguage==='function'&&root.getLanguage()==='bg';}catch(_){return false;}
  }

  async function alertUser(message,title='Download Results'){
    if(typeof root.appAlert==='function')return root.appAlert(message,title);
    if(root.alert)root.alert(message);
  }

  async function confirmUser(message,title='Result conflict'){
    if(typeof root.appConfirm==='function')return !!(await root.appConfirm(message,title,'question'));
    return !!root.confirm?.(message);
  }

  async function organizerToken(){
    if(typeof root.cpNativeHubSecretGet!=='function'||typeof root.cpOnlineOrganizerSecretKey!=='function')return '';
    return text(await root.cpNativeHubSecretGet(root.cpOnlineOrganizerSecretKey()));
  }

  function cloudClient(){
    const lib=root.ChessPublisherCloudWorkspaceApi;
    const create=lib?.createClient;
    if(typeof create!=='function')throw new Error('Cloud Workspace API is unavailable.');
    return create({clientVersion:String(root.document?.documentElement?.dataset?.chesspublisherVersion||'1.06.00-beta.34').trim()});
  }

  async function findRemoteReadOnly(client,token,tournament){
    const direct=text(tournament?.cloud?.cloudTournamentId);
    if(direct)return {id:direct};
    const internalId=text(tournament?.cloud?.internalId);
    if(!internalId)throw new Error('This tournament is not linked to Cloud yet. Push it to Cloud first.');
    const listed=await client.listTournaments(token);
    const rows=Array.isArray(listed?.tournaments)?listed.tournaments:[];
    const matches=rows.filter(row=>text(row?.localKey)===internalId);
    if(matches.length>1)throw new Error('Multiple Cloud tournaments share this internalId. Results were not downloaded.');
    if(matches.length!==1)throw new Error('No matching Cloud tournament was found. Push this tournament to Cloud first.');
    return matches[0];
  }

  async function getRemoteCurrent(client,token,remote,fallbackName,tournament){
    const id=text(remote?.id||remote);
    if(!id)throw new Error('Cloud tournament ID is missing.');
    const metaResponse=await client.getTournament(token,id);
    const meta=metaResponse?.tournament||remote||{};
    const revision=Math.max(0,Number(meta?.revision)||0);
    if(revision<=0)throw new Error('The Cloud tournament has no saved web snapshot yet.');
    const response=await client.getCurrentSnapshot(token,id);
    const parsed=extractTournament(response?.snapshot,text(meta?.name||fallbackName));
    const localInternal=text(tournament?.cloud?.internalId);
    const remoteInternal=text(parsed.tournament?.cloud?.internalId||meta?.localKey);
    if(localInternal&&remoteInternal&&localInternal!==remoteInternal){
      throw new Error('Cloud tournament identity does not match this Desktop tournament. Results were not changed.');
    }
    const snapshotCloudId=text(parsed.tournament?.cloud?.cloudTournamentId);
    if(snapshotCloudId&&snapshotCloudId!==id){
      throw new Error('Cloud snapshot ID does not match the linked tournament. Results were not changed.');
    }
    return {id,revision,meta,response,tournament:parsed.tournament,name:parsed.name};
  }

  function boardDescription(board,index,round){
    const boardNo=Number(board?.board)||index+1;
    let white=text(board?.whiteKey)||'—';
    let black=text(board?.blackKey)||'—';
    try{
      const w=typeof root.resolveRegisteredPlayer==='function'?root.resolveRegisteredPlayer(board?.whiteKey):null;
      const b=typeof root.resolveRegisteredPlayer==='function'?root.resolveRegisteredPlayer(board?.blackKey):null;
      if(w?.name)white=w.name;
      if(b?.name)black=b.name;
    }catch(_){ }
    return {boardNo,white,black,label:`Round ${round} · Board ${boardNo}`};
  }

  function refreshDerivedViews(){
    for(const name of ['recalculateRoundHistoryState','renderLivePairings','updateGacruxPanel','refreshPairingStandingsPanel','refreshFinalStandings']){
      try{
        if(typeof root[name]==='function'){
          if(name==='renderLivePairings')root[name](true); else root[name]();
        }
      }catch(err){console.warn(`Download Results: ${name} refresh failed`,err);}
    }
    try{root.scheduleTieBreakCheckerAutoCheck?.(250);}catch(_){ }
    try{root.cpRefreshRoundControlLog?.();}catch(_){ }
  }

  function summaryText(round,applied,plan,keptDesktop){
    const bg=languageBg();
    const mismatch=plan.unmatched.length;
    const unsupported=plan.unsupported.length;
    return bg
      ? `Web резултатите за Round ${round} са проверени.\n\nПриложени: ${applied}\nОставени Desktop резултати при конфликт: ${keptDesktop}\nВече еднакви: ${plan.identical}\nПропуснати заради различен жребий: ${mismatch}\nНеподдържани Web резултати: ${unsupported}`
      : `Web results for Round ${round} were checked.\n\nApplied: ${applied}\nDesktop results kept after conflicts: ${keptDesktop}\nAlready identical: ${plan.identical}\nSkipped because pairings differ: ${mismatch}\nUnsupported Web results: ${unsupported}`;
  }

  async function downloadResults(){
    if(busy)return false;
    busy=true;
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
      const cloud=await getRemoteCurrent(client,token,remote,text(tournament.name),tournament);
      const remoteBoards=cloud.tournament?.pairings?.liveBoards?.[String(round)];
      if(!Array.isArray(remoteBoards)||!remoteBoards.length){
        throw new Error(`The web snapshot has no pairings for Round ${round}.`);
      }

      const plan=buildReconcilePlan(localBoards,remoteBoards);
      stats.downloads++;
      stats.conflicts+=plan.conflicts.length;
      stats.unmatched+=plan.unmatched.length;
      stats.unsupported+=plan.unsupported.length;

      const accepted=[...plan.fills];
      let keptDesktop=0;
      for(const item of plan.conflicts){
        const d=boardDescription(item.localBoard,item.localIndex,round);
        const bg=languageBg();
        const message=bg
          ? `${d.label}\n${d.white} — ${d.black}\n\nDesktop: ${item.localResult}\nWeb: ${item.remoteResult}\n\nДа остане ли WEB резултатът?\nOK = Web · Cancel = Desktop`
          : `${d.label}\n${d.white} — ${d.black}\n\nDesktop: ${item.localResult}\nWeb: ${item.remoteResult}\n\nKeep the WEB result?\nOK = Web · Cancel = Desktop`;
        if(await confirmUser(message,bg?'Различен резултат':'Result conflict'))accepted.push(item);
        else keptDesktop++;
      }
      stats.keptDesktop+=keptDesktop;

      let applied=0;
      for(const item of accepted){
        const board=localBoards[item.localIndex];
        if(!board)continue;
        // RESULT-ONLY SAFETY: never replace the board or pairing identity.
        // Only the result field of an exact White/Black identity match changes.
        board.result=item.remoteResult;
        applied++;
      }

      if(applied){
        if(!tournament.cloud||typeof tournament.cloud!=='object')tournament.cloud={};
        tournament.cloud.lastWebResultsDownloadAt=new Date().toISOString();
        tournament.cloud.lastWebResultsDownloadRevision=cloud.revision;
        tournament.cloud.lastWebResultsDownloadRound=round;
        try{root.stateDirty=true;}catch(_){ }
        if(typeof root.saveData==='function')root.saveData();
        refreshDerivedViews();
        try{root.setStatus?.(`Download Results • Round ${round} • ${applied} web result(s) applied`);}catch(_){ }
        try{setTimeout(()=>root.checkTournamentCompletionPrompt?.(),40);}catch(_){ }
      }else{
        try{root.setStatus?.(`Download Results • Round ${round} • no result changes`);}catch(_){ }
      }
      stats.applied+=applied;
      await alertUser(summaryText(round,applied,plan,keptDesktop));
      return {ok:true,round,revision:cloud.revision,applied,keptDesktop,plan};
    }catch(err){
      const message=err?.message||String(err);
      await alertUser((languageBg()?'Download Results не промени турнира.\n\n':'Download Results did not change the tournament.\n\n')+message);
      return {ok:false,error:message};
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
    button.title='Download web-entered results for the selected round. Conflicting Desktop/Web results require a choice.';
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
    root.__cpWebResultsDownloadTestHooks={canonicalResult,pairingIdentity,buildReconcilePlan};
    installButton();
    setTimeout(installButton,0);
    setTimeout(installButton,300);
  }

  return {canonicalResult,pairingIdentity,buildReconcilePlan,extractTournament,install,downloadResults,stats};
});
