"""Operator-view guard (Item 359, 2026-11-01). A figure on the operator view stands alone: its derivation, its history and the
figures it replaced live in the standard. Fails if the rendered text of the page chrome carries any of the patterns below.
Scope: all of index.html and console-*.html; on market pages, everything outside the row tables (a row's own dated source
lines stay — they are evidence, governed by validate.py, not operator narrative)."""
import re,sys,html,glob,os
PAT=[('Item ###',re.compile(r'\bItem \d{3}')),('at the close of',re.compile(r'at the close of',re.I)),('at head ',re.compile(r'\bat head ',re.I)),
     ('is withdrawn',re.compile(r'\bis withdrawn',re.I)),('is retired',re.compile(r'\bis retired',re.I)),('re-measured',re.compile(r'\bre-measured',re.I)),
     ('bare commit hash',re.compile(r'\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b'))]
def rendered(s,market):
    s=re.sub(r'(?is)<(script|style|template)[^>]*>.*?</\1>',' ',s); s=re.sub(r'(?is)<!--.*?-->',' ',s)
    if market: s=re.sub(r'(?is)<table[^>]*>.*?</table>',' ',s)
    return html.unescape(re.sub(r'<[^>]+>',' ',s))
def check(path):
    name=os.path.basename(path); market=not (name=='index.html' or name.startswith('console-'))
    t=rendered(open(path,encoding='utf-8').read(),market); hits=[]
    for lab,rx in PAT:
        for m in rx.finditer(t): hits.append((lab,t[max(0,m.start()-40):m.end()+40].replace('\n',' ')))
    return hits
def scope(root='.'):
    M=sorted({os.path.basename(p).replace('-expansion.html','') for p in glob.glob(os.path.join(root,'*-expansion.html'))})
    return [os.path.join(root,'index.html')]+sorted(glob.glob(os.path.join(root,'console-*.html')))+[os.path.join(root,g) for m in M for g in (m+'.html',m+'-expansion.html') if os.path.exists(os.path.join(root,g))]
if __name__=='__main__':
    bad={p:check(p) for p in (sys.argv[1:] or scope())}; bad={p:h for p,h in bad.items() if h}
    for p,h in bad.items(): print('OPVIEW REFUSED',os.path.basename(p),len(h),'hit(s):',h[0][0],'|',h[0][1][:90])
    print(f'operator-view guard: {len([1 for _ in (sys.argv[1:] or scope())])-len(bad)} of {len(sys.argv[1:] or scope())} pages clean'); sys.exit(1 if bad else 0)
