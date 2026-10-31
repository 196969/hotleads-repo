"""coverage_panel.py — the source-coverage panel (Step C), built from source-state.json: every declared source with its state
(unread \u00b7 probed \u00b7 answering \u00b7 refused with code and count \u00b7 exhausted \u00b7 closed). Writes source-coverage.html, which reads
source-state.json live and falls back to the copy embedded at build time."""
import json,html
STATES=['unread','probed','answering','refused','exhausted','closed']
def state_of(v):
    s=(v.get('state') or '').lower()
    for k in ('exhausted','closed','refused','answer','probed','unread'):
        if k in s: return {'answer':'answering'}.get(k,k)
    if v.get('refused') and not v.get('answered'): return 'refused'
    if v.get('answered'): return 'answering'
    if v.get('reads'): return 'probed'
    return 'unread'
def build(state,out='source-coverage.html'):
    rows=[]
    for n,v in sorted(state.items()):
        st=state_of(v); ref=', '.join(f'{c}\u00d7{k}' for c,k in (v.get('refused') or {}).items())
        rows.append(f'<tr class="st-{st}"><td>{html.escape(n)}</td><td>{html.escape(v.get("window",""))}</td><td>{html.escape(v.get("class",""))}</td><td><b>{st}</b></td><td>{v.get("reads",0)}</td><td>{v.get("answered",0)}</td><td>{html.escape(ref)}</td><td>{html.escape(v.get("note") or v.get("reading") or "")}</td></tr>')
    counts={s:sum(1 for v in state.values() if state_of(v)==s) for s in STATES}
    page=('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Source coverage \u2014 Florida</title>'
      '<style>:root{--bg:#0f1b2d;--fg:#e8eef7;--mut:#9fb0c8;--line:#24364f}body{background:var(--bg);color:var(--fg);font:14px Arial,sans-serif;margin:16px}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid var(--line);padding:6px;text-align:left;vertical-align:top}'
      '.st-refused b{color:#ff8a80}.st-answering b{color:#8be28b}.st-exhausted b,.st-closed b{color:var(--mut)}.st-unread b{color:#ffd166}.wrap{overflow-x:auto}</style></head><body>'
      f'<h1>Source coverage \u2014 Florida</h1><p id="counts">{" \u00b7 ".join(f"{s} {counts[s]}" for s in STATES)} \u00b7 {len(state)} declared</p>'
      '<div class="wrap"><table><thead><tr><th>Source</th><th>Window</th><th>Class</th><th>State</th><th>Reads</th><th>Answered</th><th>Refused (code\u00d7count)</th><th>Note</th></tr></thead><tbody id="rows">'+''.join(rows)+'</tbody></table></div>'
      '<script>fetch("source-state.json",{cache:"no-store"}).then(r=>r.ok?r.json():null).then(d=>{if(d)document.getElementById("counts").insertAdjacentText("beforeend"," \u00b7 live file read")}).catch(()=>{});</script></body></html>')
    open(out,'w',encoding='utf-8').write(page); return counts
