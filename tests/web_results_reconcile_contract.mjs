import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const api=require('../linux/web_results_download.js');
function assert(ok,msg){if(!ok)throw new Error(msg)}
assert(api.canonicalResult('1:0')==='1 - 0','1:0 canonical');
assert(api.canonicalResult('1/2-1/2')==='½ - ½','draw canonical');
assert(api.canonicalResult(' 0f - 1f ')==='0F - 1F','forfeit canonical');
assert(api.pairingIdentity({board:7,whiteKey:'A',blackKey:'B'})==='board:7|w:A|b:B','identity includes board and colors');
const local=[
 {board:1,whiteKey:'A',blackKey:'B',result:'-'},
 {board:2,whiteKey:'C',blackKey:'D',result:'1 - 0'},
 {board:3,whiteKey:'E',blackKey:'F',result:'½ - ½'},
 {board:4,whiteKey:'G',blackKey:'H',result:'0 - 1'},
 {board:6,whiteKey:'K',blackKey:'L',result:'-'},
];
const remote=[
 {id:'r1',board:1,whiteKey:'A',blackKey:'B',result:'1-0'},
 {id:'r2',board:2,whiteKey:'C',blackKey:'D',result:'0-1'},
 {id:'r3',board:3,whiteKey:'E',blackKey:'F',result:'1/2-1/2'},
 {id:'r4',board:4,whiteKey:'H',blackKey:'G',result:'1-0'},
 {id:'r5',board:5,whiteKey:'I',blackKey:'J',result:'-'},
 {id:'r6',board:7,whiteKey:'K',blackKey:'L',result:'1-0'},
];
const plan=api.buildReconcilePlan(local,remote);
assert(plan.fills.length===1,'one blank desktop fill');
assert(plan.conflicts.length===1,'one true result conflict');
assert(plan.identical===1,'one identical result');
assert(plan.identicalEntries.length===1&&plan.identicalEntries[0].submissionId==='r3','identical submission remains acknowledgeable');
assert(plan.unmatched.length===2,'reversed colors and changed board number must not be guessed');
assert(plan.remoteBlank===1,'blank web result ignored');
assert(plan.fills[0].localIndex===0&&plan.fills[0].remoteResult==='1 - 0'&&plan.fills[0].submissionId==='r1','fill data');
assert(plan.conflicts[0].localIndex===1&&plan.conflicts[0].localResult==='1 - 0'&&plan.conflicts[0].remoteResult==='0 - 1'&&plan.conflicts[0].submissionId==='r2','conflict data');
console.log('WEB_RESULTS_RECONCILE_CONTRACT=PASS');
