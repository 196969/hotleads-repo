"""Operator-view guard (Item 359, 2026-11-01). A figure on the operator view stands alone: its derivation, its history and the
figures it replaced live in the standard. Fails if the rendered text of the page chrome carries any of the patterns below.
Scope: all of index.html and console-*.html; on market pages, everything outside the row tables (a row's own dated source
lines stay — they are evidence, governed by validate.py, not operator narrative). Archive pages (*-archive.html) are excluded by
declaration: they hold screened-out Tier C rows and are neither sending nor operator surfaces (florida-standard.json, declared_exclusions)."""
import re,sys,html,glob,os
PAT=[('Item ###',re.compile(r'\bItem \d{3}')),('at the close of',re.compile(r'at the close of',re.I)),('at head ',re.compile(r'\bat head ',re.I)),
     ('is withdrawn',re.compile(r'\bis withdrawn',re.I)),('is retired',re.compile(r'\bis retired',re.I)),('re-measured',re.compile(r'\bre-measured',re.I)),
     ('bare commit hash',re.compile(r'\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b'))]
def rendered(s,market):
    s=re.sub(r'(?is)<(script|style|template)[^>]*>.*?</\1>',' ',s); s=re.sub(r'(?is)<!--.*?-->',' ',s)
    if market: s=re.sub(r'(?is)<table[^>]*>.*?</table>',' ',s)
    return html.unescape(re.sub(r'<[^>]+>',' ',s))
HDR=[('retired',re.compile(r'\bretired\b',re.I)),('restated',re.compile(r'\brestated\b',re.I)),('none reproduces',re.compile(r'none reproduces',re.I)),('earlier quoted',re.compile(r'earlier quoted',re.I))]
DATE=re.compile(r'\b(?:20\d\d-\d\d-\d\d|\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec) 20\d\d)\b')
def header_hits(s):
    """Item 364: the operator-facing header (everything before the first table) carries what the page is, current figures and one date."""
    # Item 366: the operator header is the <header> element where a page has one; otherwise its title and subtitle lines (h1, div.meta, div.sub, p.lede)
    hd=re.search(r'(?is)<header\b[^>]*>.*?</header>',s)
    if hd: h=hd.group(0)
    else:
        b=s.find('<body'); t=s.find('<table',b if b>=0 else 0); pre=s[max(b,0):t if t>0 else len(s)]
        h=' '.join(m.group(0) for m in re.finditer(r'(?is)<h1\b[^>]*>.*?</h1>|<div class="(?:meta|sub)"[^>]*>.*?</div>|<p class="lede"[^>]*>.*?</p>',pre))
    h=re.sub(r'(?is)<(script|style|template)[^>]*>.*?</\1>',' ',h)
    out=[]
    for m in re.finditer(r'(?is)<(div|p|span|h1|h2|h3|header)\b[^>]*>((?:(?!<(?:div|p|table)\b).)*?)</\1>',h):
        txt=html.unescape(re.sub(r'<[^>]+>',' ',m.group(2)))
        for lab,rx in HDR:
            if rx.search(txt): out.append((lab,txt.strip()[:120]))
        if len(set(DATE.findall(txt)))>1: out.append(('two dates in one subtitle',txt.strip()[:120]))
        for m in DATE.finditer(txt):   # Item 366: every header date is the measurement date, marked as such
            if not re.search(r'measured\s*$',txt[:m.start()],re.I): out.append(('date not marked as the measurement date',txt.strip()[:120])); break
    return out
def check(path):
    name=os.path.basename(path); market=not (name=='index.html' or name.startswith('console-'))
    t=rendered(open(path,encoding='utf-8').read(),market); hits=[]
    for lab,rx in PAT:
        for m in rx.finditer(t): hits.append((lab,t[max(0,m.start()-40):m.end()+40].replace('\n',' ')))
    return hits+header_hits(open(path,encoding='utf-8').read())
def scope(root='.'):
    M=sorted({os.path.basename(p).replace('-expansion.html','') for p in glob.glob(os.path.join(root,'*-expansion.html'))})
    return [os.path.join(root,'index.html')]+sorted(glob.glob(os.path.join(root,'console-*.html')))+[os.path.join(root,g) for m in M for g in (m+'.html',m+'-expansion.html') if os.path.exists(os.path.join(root,g))]
if __name__=='__main__':
    bad={p:check(p) for p in (sys.argv[1:] or scope())}; bad={p:h for p,h in bad.items() if h}
    for p,h in bad.items(): print('OPVIEW REFUSED',os.path.basename(p),len(h),'hit(s):',h[0][0],'|',h[0][1][:90])
    print(f'operator-view guard: {len([1 for _ in (sys.argv[1:] or scope())])-len(bad)} of {len(sys.argv[1:] or scope())} pages clean'); sys.exit(1 if bad else 0)
