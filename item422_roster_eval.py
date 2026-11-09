#!/usr/bin/env python3
"""Item 422 eval: "the roster file's seat count and weight total equal the app roster's."
The app roster is derived at run time from Dash's own _councilRoster() (Item 368: the app roster is the ballot), loaded headless from
a Dash index.html: --dash <path>, else DASH_INDEX, else the live raw file on 196969/dash-app-@branch. Nothing about the app roster is typed here.
  --cases   the known-answer cases: item422_fire_roster.json must PASS and ballot to the app's total;
            item422_notfire_roster.json must FAIL. Exit 0 only if both behave.
  --live    founders-roster.json in the repository root must PASS.
Grading compares seat count, weight total and the seat names one for one (a reconciliation names its items; counts only confirm)."""
import asyncio, json, os, sys, tempfile, urllib.request
ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = 'https://raw.githubusercontent.com/196969/dash-app-/branch/index.html'
FIND = """()=>{ if(window.__dash) return true; const D=window.DCLogic; for(const e of document.querySelectorAll('*')){ const k=Object.keys(e).find(k=>k.startsWith('__reactFiber$')); if(!k) continue; let f=e[k],n=0; while(f&&n<300){ const sn=f.stateNode; if(sn&&sn.logic&&(sn.logic instanceof D)){ window.__dash=sn.logic; return true; } f=f.return; n++; } } return false }"""
def dash_path(a):
    if '--dash' in a: return a[a.index('--dash') + 1], 'file given'
    if os.environ.get('DASH_INDEX'): return os.environ['DASH_INDEX'], 'DASH_INDEX'
    p = os.path.join(tempfile.gettempdir(), 'dash-index-live.html'); urllib.request.urlretrieve(RAW, p); return p, 'live raw ' + RAW
async def app_roster(path):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); c = await b.new_context(); await c.add_init_script("try{localStorage.clear();localStorage.setItem('dash.tourDone','1')}catch(e){}")
        pg = await c.new_page(); await pg.goto('file://' + os.path.abspath(path), timeout=180000); await pg.wait_for_timeout(5000)
        assert await pg.evaluate(FIND), 'Dash app not found in ' + path
        R = await pg.evaluate("()=>{const R=window.__dash._councilRoster(); return {names:[R.chair.name].concat(R.governing.map(g=>g.name), R.adv.map(a=>a.name)), weights:[R.chair.weight].concat(R.governing.map(g=>g.weight), R.adv.map(a=>a.weight)), seats:R.seats, total:R.totalW}}")
        await b.close(); return R
def grade(roster_path, A):
    F = json.load(open(roster_path))['seats']; fn = [s['name'] for s in F]; fw = {s['name']: float(s['weight']) for s in F}
    total = round(sum(fw.values()), 2); aw = dict(zip(A['names'], A['weights']))
    extra = [n for n in fn if n not in aw]; missing = [n for n in A['names'] if n not in fw]; wdiff = [n for n in fn if n in aw and fw[n] != float(aw[n])]
    ok = len(F) == A['seats'] and total == float(A['total']) and not extra and not missing and not wdiff
    return ok, {'file': os.path.relpath(roster_path, ROOT), 'file_seats': len(F), 'file_weight': total, 'app_seats': A['seats'], 'app_weight': float(A['total']), 'in_file_not_app': extra, 'in_app_not_file': missing, 'weight_disagreements': wdiff}
def main(a):
    path, src = dash_path(a); A = asyncio.run(app_roster(path)); print(f'app roster: {A["seats"]} seats, {A["total"]} (source: {src})')
    fails = 0
    if '--cases' in a:
        ok, d = grade(os.path.join(ROOT, 'item422_fire_roster.json'), A); good = ok and d['file_weight'] == float(A['total'])
        print(('FIRE OK    ' if good else 'FIRE WRONG ') + json.dumps(d)); fails += 0 if good else 1
        ok, d = grade(os.path.join(ROOT, 'item422_notfire_roster.json'), A)
        print(('NOT-FIRE OK    ' if not ok else 'NOT-FIRE WRONG ') + json.dumps(d)); fails += 0 if not ok else 1
    if '--live' in a:
        ok, d = grade(os.path.join(ROOT, 'founders-roster.json'), A); print(('LIVE PASS ' if ok else 'LIVE FAIL ') + json.dumps(d)); fails += 0 if ok else 1
    sys.exit(1 if fails else 0)
if __name__ == '__main__': main(sys.argv[1:])
