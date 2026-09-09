import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
function assert(ok,msg){if(!ok)throw new Error(msg)}

const localBoards=[
  {board:1,whiteKey:'A',blackKey:'B',result:'-'},
  {board:2,whiteKey:'C',blackKey:'D',result:'1 - 0'},
  {board:3,whiteKey:'E',blackKey:'F',result:'½ - ½'},
];
const pending=[
  {id:'r1',round:1,board:1,whiteKey:'A',blackKey:'B',result:'1 - 0',arbiterName:'Arbiter A'},
  {id:'r2',round:1,board:2,whiteKey:'C',blackKey:'D',result:'0 - 1',arbiterName:'Arbiter B'},
  {id:'r3',round:1,board:3,whiteKey:'E',blackKey:'F',result:'½ - ½',arbiterName:'Arbiter C'},
  {id:'r4-other-round',round:2,board:1,whiteKey:'A',blackKey:'B',result:'0 - 1',arbiterName:'Arbiter D'},
];
const calls=[];
const steps=[];
const alerts=[];
let choices=0;
let saves=0;
const button={disabled:false};
const tournament={name:'Test',cloud:{cloudTournamentId:'cloud-123',internalId:'internal-123',baseRevision:9}};

global.window={
  document:{
    documentElement:{dataset:{chesspublisherVersion:'1.06.00-beta.34-linuxdev23'}},
    getElementById(id){return id==='cpDownloadWebResultsBtn'?button:null},
    querySelector(){return null},
  },
  getLanguage(){return 'en'},
  getCurrentTournament(){return tournament},
  getSelectedPairingRoundNumber(){return 1},
  isSelectedRoundEditable(){return true},
  getLivePairingBoards(){return localBoards},
  cpOnlineOrganizerSecretKey(){return 'organizer'},
  async cpNativeHubSecretGet(){return 'secret-token'},
  ChessPublisherCloudWorkspaceApi:{
    DEFAULT_BASE_URL:'https://api.test',
    createClient(){return {
      async getTournament(){return {tournament:{id:'cloud-123',revision:9,localKey:'internal-123'}}},
      async listTournaments(){throw new Error('direct cloud id should avoid listing')},
    }},
  },
  async fetch(url,init){
    calls.push({url,method:init?.method||'GET',body:init?.body||''});
    if(url.endsWith('/arbiter-results')){
      steps.push('pending-get');
      return new Response(JSON.stringify({ok:true,results:pending}),{status:200,headers:{'Content-Type':'application/json'}});
    }
    if(url.endsWith('/arbiter-results/ack')){
      steps.push('ack');
      assert(steps.includes('sync'),'ACK must happen only after unified SYNC');
      const body=JSON.parse(init.body);
      assert(new Set(body.submissionIds).size===3,'exactly three reviewed submissions must be acknowledged');
      assert(body.submissionIds.includes('r1')&&body.submissionIds.includes('r2')&&body.submissionIds.includes('r3'),'fill/conflict/identical ids acknowledged');
      assert(!body.submissionIds.includes('r4-other-round'),'other round must not be acknowledged');
      return new Response(JSON.stringify({ok:true,acknowledged:3}),{status:200,headers:{'Content-Type':'application/json'}});
    }
    throw new Error(`unexpected URL ${url}`);
  },
  async cpChooseWebResultConflict(item){
    choices++;
    assert(item.localResult==='1 - 0'&&item.remoteResult==='0 - 1','conflict exposes both results');
    return 'desktop';
  },
  async cpUnifiedSync(){
    steps.push('sync');
    tournament.cloud.baseRevision=10;
    return {status:'IN_SYNC',revision:10};
  },
  async cpCloudCheckStatus(){return {status:'IN_SYNC',revision:10}},
  async cpUnifiedSyncRefreshFromResults(){steps.push('refresh')},
  async appAlert(message){alerts.push(message)},
  saveData(){saves++},
  setStatus(){},
  recalculateRoundHistoryState(){},
  renderLivePairings(){},
  updateGacruxPanel(){},
  refreshPairingStandingsPanel(){},
  refreshFinalStandings(){},
  scheduleTieBreakCheckerAutoCheck(){},
  cpRefreshRoundControlLog(){},
};

global.document=global.window.document;
const api=require('../linux/web_results_download.js');
const result=await api.downloadResults();
assert(result.ok===true,'download flow succeeds');
assert(result.pending===3,'only selected-round pending submissions processed');
assert(result.applied===1,'blank Desktop result filled from Web');
assert(result.keptDesktop===1,'conflicting Desktop result kept by explicit choice');
assert(result.acknowledged===3,'all reviewed selected-round submissions acknowledged');
assert(result.syncStatus==='IN_SYNC','Download Results ends In Sync');
assert(result.revision===10,'Download Results records post-sync revision/base');
assert(localBoards[0].result==='1 - 0','Web result applied to blank Desktop board');
assert(localBoards[1].result==='1 - 0','Desktop conflict choice preserved');
assert(localBoards[2].result==='½ - ½','identical result unchanged');
assert(choices===1,'exactly one conflict choice');
assert(steps.indexOf('sync')<steps.indexOf('ack'),'SYNC precedes ACK');
assert(tournament.cloud.lastWebResultsSyncAt,'sync timestamp recorded');
assert(saves>=2,'local result and sync metadata are persisted');
assert(alerts.at(-1).includes('Acknowledged as reviewed: 3'),'summary reports acknowledgement');
assert(button.disabled===false,'button re-enabled after completion');
console.log('WEB_RESULTS_PENDING_FLOW_CONTRACT=PASS');
