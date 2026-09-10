#!/usr/bin/env python3
"""Real-Chromium regression for the beta.85 Tournament Setup grid alignment."""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'linux'))
from tournament_setup_layout_integration import inject_tournament_setup_layout
from chromium_runtime_smoke import _browser, _run_browser


def main() -> int:
    # Reproduce the authoritative beta.70 DOM shape: after a complete
    # Time Control/Rating Type row, one dynamically injected help DIV is added
    # directly to the four-column Tournament Setup grid before Start Date.
    fixture = '''<!doctype html><html><head><style>
html,body{margin:0}.content{padding:12px}.form-grid-4{display:grid;grid-template-columns:158px minmax(0,1fr) 158px minmax(0,1fr);column-gap:12px;row-gap:7px;align-items:center;width:1180px}.form-grid-4>label{text-align:right}.form-grid-4 input,.form-grid-4 select,.setup-rating-type-row{min-width:0;width:100%;height:30px;box-sizing:border-box}.setup-rating-type-row select{width:100%;height:30px}
</style></head><body>
<div id="appWindow"><div class="content"><div id="main" class="page active">
<div class="form-grid-4 tournament-general-grid" id="fixtureGrid">
<label for="timeControl">Time Control</label><select id="timeControl"><option>3+2</option></select>
<label for="tournamentRatingType">Rating Type</label><div class="setup-rating-type-row"><select id="tournamentRatingType"><option>Blitz</option></select></div>
<div id="cpBeta70LongEventBox" class="help" style="margin:8px 0;padding:9px;border:1px solid #d9d9d9;border-radius:8px"><label style="display:flex;gap:8px;align-items:center"><input type="checkbox"> Tournament lasts more than 30 days / multiple ratings may apply</label><div>Duration: 0 day(s).</div></div>
<label id="startDateLabel" for="startDate">Start Date &amp; Time</label><input id="startDate">
<label id="endDateLabel" for="endDate">End Date &amp; Time</label><input id="endDate">
<label id="tournamentFormatLabel" for="tournamentFormat">Tournament Format</label><select id="tournamentFormat"><option>Individual Swiss</option></select>
<label id="pairingSystemLabel" for="pairingSystem">Pairing System</label><select id="pairingSystem"><option>FIDE Dutch System</option></select>
</div></div></div></div>
<script>
function check(value,message){if(!value)throw new Error(message);}
function centerY(r){return r.top+r.height/2;}
window.addEventListener('load',()=>{
  try{
    const grid=document.getElementById('fixtureGrid');
    const panel=document.getElementById('cpBeta70LongEventBox');
    const rect=id=>document.getElementById(id).getBoundingClientRect();
    const g=grid.getBoundingClientRect(),p=panel.getBoundingClientRect();
    const css=getComputedStyle(panel);
    check(css.gridColumnStart==='1','long-event panel does not start at grid column 1');
    check(css.gridColumnEnd==='-1','long-event panel does not end at the final grid line');
    check(Math.abs(p.left-g.left)<2&&Math.abs(p.right-g.right)<2,'long-event panel does not occupy a full grid row');
    const dateRects=[rect('startDateLabel'),rect('startDate'),rect('endDateLabel'),rect('endDate')];
    const dateCenters=dateRects.map(centerY);
    check(Math.max(...dateCenters)-Math.min(...dateCenters)<2,'Start/End Date label-control pairs are shifted');
    check(Math.min(...dateRects.map(x=>x.top))>p.bottom,'Start/End Date row overlaps or precedes long-event panel');
    const formatRects=[rect('tournamentFormatLabel'),rect('tournamentFormat'),rect('pairingSystemLabel'),rect('pairingSystem')];
    const formatCenters=formatRects.map(centerY);
    check(Math.max(...formatCenters)-Math.min(...formatCenters)<2,'Format/Pairing System label-control pairs are shifted');
    check(Math.min(...formatCenters)>Math.max(...dateCenters)+5,'Format/Pairing System is not on the next row');
    document.body.setAttribute('data-tournament-setup-layout-test','PASS');
  }catch(error){document.body.setAttribute('data-tournament-setup-layout-test','FAIL: '+error.message);}
});
</script></body></html>'''
    with tempfile.TemporaryDirectory(prefix='cp-tournament-setup-layout-') as raw:
        temp = Path(raw)
        html = temp / 'tournament-setup-layout.html'
        html.write_bytes(inject_tournament_setup_layout(fixture.encode()))
        cp = _run_browser(_browser(), html.as_uri(), 1000)
        if cp.returncode != 0:
            raise RuntimeError(f'Tournament Setup Chromium regression failed rc={cp.returncode}: {cp.stderr[-2000:]}')
        if 'data-tournament-setup-layout-test="PASS"' not in cp.stdout:
            raise RuntimeError(f'Tournament Setup layout regression failed: {cp.stdout[-5000:]}\n{cp.stderr[-2000:]}')
    print('BETA85_TOURNAMENT_SETUP_LAYOUT_BROWSER=PASS (long-event panel owns full row; following fields remain aligned)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
