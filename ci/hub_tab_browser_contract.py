#!/usr/bin/env python3
"""Real-Chromium regression for the dynamic beta.85 Online & Cloud tab."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'linux'))
from window_integration import inject_window_mode
from hub_tab_visibility_integration import inject_online_hub_tab_visibility
from chromium_runtime_smoke import _browser, _run_browser


def main() -> int:
    fixture = '''<!doctype html><html><head><style>
html,body{margin:0;width:100%;height:100%}.window{width:1000px;height:700px}.content{height:620px}.page{display:none}.page.active{display:block}
</style></head><body>
<div id="appWindow" class="window"><div class="titlebar"><span id="windowDocumentTitle">Chess-Publisher</span></div>
<div class="tabs">
<div id="tabDgt" class="tab">DGT Boards</div><div id="tabMain" class="tab">Tournament Setup</div><div id="tabRegistration" class="tab">Lists & Players</div>
<div id="tabPairings" class="tab">Pairings</div><div id="tabStandings" class="tab">Standings</div><div id="tabExport" class="tab">Other / Export</div>
<div id="tabSchedule" class="tab">Tournament Schedule</div><div id="tabChessResults" class="tab">Chess-Results</div>
</div><div class="content"><section id="main" class="page active"></section><section id="hub" class="page"></section></div></div>
<script>
let stateDirty=false;const data={preferences:{}};function saveAll(){} function saveData(){} function updateWorkflowTabs(){} function dgtOnTabLeave(){} function dgtOnTabEnter(){}
window.showTab=function(id,button){document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tabs .tab').forEach(t=>t.classList.remove('active'));document.getElementById(id)?.classList.add('active');button?.classList.add('active');};
function check(value,message){if(!value)throw new Error(message);}
window.addEventListener('load',()=>{
  try{
    const tabs=document.querySelector('#appWindow .tabs');
    const hub=document.createElement('div');hub.id='tabHub';hub.className='tab';hub.textContent='Online & Cloud (Beta)';hub.onclick=()=>showTab('hub',hub);tabs.appendChild(hub);
    const all=[...tabs.querySelectorAll('.tab')];
    check(all.length===9,'expected nine primary tabs after dynamic Hub insertion');
    const tabsRect=tabs.getBoundingClientRect();const hubRect=hub.getBoundingClientRect();const tops=all.map(x=>x.getBoundingClientRect().top);
    check(getComputedStyle(tabs).display==='grid','tab bar is not grid layout');
    check(getComputedStyle(hub).display!=='none'&&getComputedStyle(hub).visibility!=='hidden'&&Number(getComputedStyle(hub).opacity)>0,'Online & Cloud tab is hidden');
    check(Math.max(...tops)-Math.min(...tops)<2,'Online & Cloud wrapped to a hidden second row');
    check(hubRect.left>=tabsRect.left-2&&hubRect.right<=tabsRect.right+2,'Online & Cloud is outside horizontal tab viewport');
    check(hubRect.top>=tabsRect.top-2&&hubRect.bottom<=tabsRect.bottom+2,'Online & Cloud is outside vertical tab viewport');
    check(tabs.scrollHeight<=tabs.clientHeight+1,'tab bar contains a clipped second row');
    hub.click();check(document.getElementById('hub').classList.contains('active'),'Online & Cloud tab cannot activate hub page');
    document.body.setAttribute('data-hub-tab-test','PASS');
  }catch(error){document.body.setAttribute('data-hub-tab-test','FAIL: '+error.message);}
});
</script></body></html>'''
    with tempfile.TemporaryDirectory(prefix='cp-hub-tab-browser-') as raw:
        temp = Path(raw)
        html = temp / 'hub-tab.html'
        rendered = inject_window_mode(fixture.encode())
        rendered = inject_online_hub_tab_visibility(rendered)
        html.write_bytes(rendered)
        cp = _run_browser(_browser(), html.as_uri(), 1000)
        if cp.returncode != 0:
            raise RuntimeError(f'Online Hub Chromium regression failed rc={cp.returncode}: {cp.stderr[-2000:]}')
        if 'data-hub-tab-test="PASS"' not in cp.stdout:
            raise RuntimeError(f'Online Hub browser regression failed: {cp.stdout[-5000:]}\n{cp.stderr[-2000:]}')
    print('LINUX_ONLINE_HUB_TAB_BROWSER=PASS (dynamic ninth tab remains visible, single-row and clickable)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
