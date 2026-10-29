"""reads.py — Item 320 Part 2 (C6, 29 Oct 2026). Site-read state per row, in <market>-reads.json at the repository root.
Two states the file can tell apart:
  refused   — the reader was turned away (kind: 403, 503, 522, challenge, timeout, net). Re-runnable. Recorded only when two readers of
              different kinds (script and browser) have both been refused; one reader's refusal is 'unconfirmed' and is not a fact about the site.
  not_found — a reader got in (HTTP < 400, no challenge page, a real body) and the thing looked for is not published. Not re-read.
Also: read (got in and found it), and closed (ruled closed to automated reading — phone only). A refusal is never counted in an absence total.
Usage: python3 reads.py florida record <key> <reader:script|browser> <outcome> [--kind K] [--found]   ·   python3 reads.py florida counts
"""
import json,re,sys,os,datetime
TODAY=datetime.date.today().isoformat()
REFUSAL_KINDS=('403','503','522','challenge','timeout','net')
def classify(status,title='',body='',looked_for_found=None):
    """Classify one read attempt. status: int HTTP code, or 'timeout'/'net'. Returns (outcome, kind)."""
    if status in ('timeout','net'): return 'refused',status
    if re.search(r'just a moment|verify you are human|access denied|attention required',(title or '')+' '+(body or '')[:600],re.I): return 'refused','challenge'
    if isinstance(status,int) and status>=400: return 'refused',str(status)
    return ('read' if looked_for_found else 'not_found'),None
def load(m):
    p=m+'-reads.json'; return json.load(open(p,encoding='utf-8')) if os.path.exists(p) else {'_doc':__doc__.split('\n')[0],'rows':{}}
def save(m,R): json.dump(R,open(m+'-reads.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
def record(m,key,reader,outcome,kind=None,date=None,note=''):
    """Record one attempt and derive the row's state. Returns the row's state after the record."""
    assert reader in ('script','browser'),'reader must be script or browser'; assert outcome in ('read','not_found','refused','closed')
    R=load(m); row=R['rows'].setdefault(str(key),{'state':None,'attempts':[]}); date=date or TODAY
    row['attempts'].append({'date':date,'reader':reader,'outcome':outcome,'kind':kind,'note':note})
    if outcome=='closed': row['state']='closed'; row['rerun']=False; row['reason']=note or 'ruled closed to automated reading — phone only'
    elif outcome in ('read','not_found'): row['state']=outcome; row['rerun']=False; row['kind']=None   # a successful read settles the row; nothing is re-read
    else:
        kinds={a['reader'] for a in row['attempts'] if a['outcome']=='refused'}
        if row['state'] in ('read','not_found','closed'): pass          # a later refusal does not undo a successful read
        elif len(kinds)>=2: row['state']='refused'; row['rerun']=True; row['kind']=kind
        else: row['state']='refused (unconfirmed — one reader)'; row['rerun']=True; row['kind']=kind
    row['last']=date; save(m,R); return row['state']
def counts(m):
    R=load(m); rows=R['rows'].values()
    return {'refused (re-runnable)':sum(1 for r in rows if r['state']=='refused'),'refused, unconfirmed (one reader)':sum(1 for r in rows if r['state'] and r['state'].startswith('refused (unconfirmed')),'not_found (absent, not re-read)':sum(1 for r in rows if r['state']=='not_found'),'read':sum(1 for r in rows if r['state']=='read'),'closed (phone only)':sum(1 for r in rows if r['state']=='closed'),'absence total (not_found only — refusals never counted)':sum(1 for r in rows if r['state']=='not_found'),'re-run list':sorted(k for k,r in R['rows'].items() if r.get('rerun'))}
if __name__=='__main__':
    m=sys.argv[1]; cmd=sys.argv[2]
    if cmd=='counts': print(json.dumps(counts(m),indent=1))
    elif cmd=='record':
        key,reader,outcome=sys.argv[3:6]; kind=sys.argv[sys.argv.index('--kind')+1] if '--kind' in sys.argv else None; print(record(m,key,reader,outcome,kind))
