"""Item 413 (Parts A and B): the one counting method for every figure on index.html. gate.py STOP 7 re-runs it."""
import re,html,glob,os
LF=r'(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|lp|llp|pllc|pa|plc)$'
LF_NOPA=r'(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|lp|llp|pllc|plc)$'
def norm(name):
    # lower-case; "&" read as "and"; every character that is not a letter or a digit dropped
    return re.sub(r'[^a-z0-9]','',name.lower().replace('&','and'))
def fold(n,rx=LF): return re.sub(rx,'',n)
cl=lambda x: html.unescape(re.sub('<[^>]+>','',x)).strip()
def company(cell):
    # the company is the bold name in the cell; the sector line beneath it is not part of the name
    m=re.search(r'<strong>(.*?)</strong>',cell,re.S); return cl(m.group(1) if m else cell)
def rows(f):
    t=open(f,encoding='utf-8').read(); i=t.find('<tbody id="tb"')
    hd=[re.sub('<[^>]+>','',h).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',t[t.rfind('<table',0,i):i],re.S)]
    R=[re.findall(r'<td[^>]*>(.*?)</td>',x,re.S) for x in re.findall(r'<tr(?:\s[^>]*)?>.*?</tr>',t[i:t.find('</tbody>',i)],re.S) if 'colspan' not in x]
    return hd,R
def within(names):
    # the headline rule: a trailing legal form is folded only where the name occurs both with and without it inside one market
    c={}
    for n in names: c.setdefault(fold(n),set()).add(n)
    return {n:(min(g) if len(g)>1 else n) for g in c.values() for n in g}
EMAIL=re.compile(r'[\w.+-]+@[\w.-]+\.\w+')
def measure(root='.'):
    P=lambda f:os.path.join(root,f)
    M=sorted({os.path.basename(p)[:-len('-expansion.html')] for p in glob.glob(P('*-expansion.html'))})
    out={'markets':len(M),'full_treatment':sum(all(os.path.exists(P(m+s)) for s in ('.html','-expansion.html','-archive.html')) for m in M),'cards':{},'tab':{}}
    estate_kept=set(); estate_within=set(); estate_fold=set(); estate_nopa=set(); vr=exr=exv=ab=em=0; contra=0
    for m in M:
        V=[];A=[];ev=0;vcall=0;tabs={}
        for f,kind in ((m+'.html','w'),(m+'-expansion.html','e')):
            hd,R=rows(P(f)); si,ci,ti=hd.index('Status'),hd.index('Company'),hd.index('Tier'); ei=hd.index('Email') if 'Email' in hd else None
            tabs[f]=[]
            for r in R:
                c=norm(company(r[ci])); st=cl(r[si]); t=cl(r[ti]); has=bool(ei is not None and EMAIL.search(cl(r[ei])))
                A.append(c); tabs[f].append((company(r[ci]),t))
                if kind=='e': exr+=1
                if t in ('A','B'): ab+=1
                if has: em+=1
                if st=='Verified':
                    V.append(c); vcall+=has
                    if kind=='e': ev+=1
        wm=within(set(A))
        out['cards'][m]={'ver_rows':len(V),'ver_cos':len({wm[x] for x in V}),'rows':len(A),'cos':len({wm[x] for x in A}),'exp_ver':ev,'vcall':vcall}
        out['tab'][m]=tabs
        W={};E={}
        for c,t in tabs[m+'.html']: W.setdefault(wm[norm(c)],set()).add(t)
        for c,t in tabs[m+'-expansion.html']: E.setdefault(wm[norm(c)],set()).add(t)
        contra+=sum(1 for k in set(W)&set(E) if W[k]!=E[k])
        vr+=len(V); exv+=ev
        estate_kept|=set(V); estate_within|={wm[x] for x in V}; estate_fold|={fold(x) for x in V}; estate_nopa|={fold(x,LF_NOPA) for x in V}
    out.update(verified_rows=vr,verified_cos_within=len(estate_within),verified_cos_kept=len(estate_kept),verified_cos_foldall=len(estate_fold),
               verified_cos_fold_nopa=len(estate_nopa),kept_minus_within=len(estate_kept)-len(estate_within),expansion_rows=exr,expansion_verified=exv,
               dialable_ab=ab,call_ready_email=em,tier_contradictions=contra)
    return out
def held(index_html,o,detail=False):
    """The held tier-contradiction pairs listed on the index: how many, how many still differ in tier in the rows, and any
    printed tier that no longer matches its row."""
    s=index_html; i=s.find('<section class="held-pairs"'); t=s[i:s.find('</section>',i)]
    items=re.findall(r'<li>(.*?)</li>',t,re.S); still=0; wrong=[]
    for li in items:
        x=cl(li); m=re.search(r'(\S+)\.html row (\d+) Tier (\w).*?(\S+)\.html row (\d+) Tier (\w)',x)
        f1,r1,t1,f2,r2,t2=m.groups(); mk=f1.replace('-expansion','')
        a=o['tab'][mk][f1+'.html'][int(r1)-1]; b=o['tab'][mk][f2+'.html'][int(r2)-1]
        still+=a[1]!=b[1]
        if t1!=a[1]: wrong.append((f1,int(r1),t1,a[1]))
        if t2!=b[1]: wrong.append((f2,int(r2),t2,b[1]))
    return (len(items),still,wrong) if detail else (len(items),still)
def count_lines(root='.'):
    """Item 416: each market and expansion page prints a count line (N rows · Status N · Tier N) above its table; every printed
    count is re-counted from that page's own rows. Returns (pages with a count line, figures checked, disagreements)."""
    import collections
    P=lambda f:os.path.join(root,f)
    M=sorted({os.path.basename(p)[:-len('-expansion.html')] for p in glob.glob(P('*-expansion.html'))})
    keys=r'(Verified|Downgraded|Reclassified|Unverified|Pending by rule|Research pending|Tier A|A|B|C)'
    pages=0; figs=0; bad=[]
    for m in M:
        for f in (m+'.html',m+'-expansion.html'):
            s=open(P(f),encoding='utf-8',errors='replace').read(); b=s.find('<body'); t=s.find('<table',b)
            txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',s[b:t]))))
            mm=re.search(r'· ([\d,]+) rows((?: · %s [\d,]+)+)'%keys,txt)
            if not mm: continue
            hd,R=rows(P(f)); st=collections.Counter(cl(r[hd.index('Status')]) for r in R); ti=collections.Counter(cl(r[hd.index('Tier')]) for r in R)
            pages+=1; figs+=1
            if int(mm.group(1).replace(',',''))!=len(R): bad.append((f,'rows',mm.group(1),len(R)))
            for k,v in re.findall(r'· %s ([\d,]+)'%keys,mm.group(2)):
                figs+=1; a=ti.get('A',0) if k=='Tier A' else ti.get(k,0) if k in('A','B','C') else st.get(k,0)
                if a!=int(v.replace(',','')): bad.append((f,k,v,a))
    return pages,figs,bad
