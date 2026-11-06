"""Item 413 Part A: the one counting method for the index (repeatable by gate.py STOP 7)."""
import re,html,glob,os
def norm(name):
    # The rule stated on the index: lower-case; "&" read as "and"; every character that is not a letter or digit dropped.
    # Legal-form words (Inc., LLC, Corp. ...) are NOT stripped: two rows differing only by "Inc." versus "LLC" count as two companies.
    return re.sub(r'[^a-z0-9]','',name.lower().replace('&','and'))
def rows(f):
    t=open(f,encoding='utf-8').read(); i=t.find('<tbody id="tb"')
    hd=[re.sub('<[^>]+>','',h).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',t[t.rfind('<table',0,i):i],re.S)]
    R=[re.findall(r'<td[^>]*>(.*?)</td>',x,re.S) for x in re.findall(r'<tr(?:\s[^>]*)?>.*?</tr>',t[i:t.find('</tbody>',i)],re.S) if 'colspan' not in x]
    return hd,R
cl=lambda x: html.unescape(re.sub('<[^>]+>','',x)).strip()
def company(cell):
    # The company is the name in the cell's <strong>; the line beneath it (sector, area) is not part of the name.
    m=re.search(r'<strong>(.*?)</strong>',cell,re.S)
    return cl(m.group(1) if m else cell)
def measure(root='.'):
    M=sorted({os.path.basename(p)[:-len('-expansion.html')] for p in glob.glob(os.path.join(root,'*-expansion.html'))})
    out={'markets':len(M),'full_treatment':sum(all(os.path.exists(os.path.join(root,m+s)) for s in ('.html','-expansion.html','-archive.html')) for m in M),'cards':{}}
    allv=set(); vr=0; exr=0; exv=0; ab=0; em=0; sens=0
    for m in M:
        V=[];A=[];ev=0
        for f,kind in ((m+'.html','w'),(m+'-expansion.html','e')):
            hd,R=rows(os.path.join(root,f)); si,ci,ti=hd.index('Status'),hd.index('Company'),hd.index('Tier'); ei=hd.index('Email') if 'Email' in hd else None
            for r in R:
                c=company(r[ci]); st=cl(r[si]); A.append(c)
                if st=='Verified':
                    V.append(c)
                    if kind=='e': ev+=1
                if kind=='e': exr+=1
                if cl(r[ti]) in ('A','B'): ab+=1
                if ei is not None and re.search(r'[\w.+-]+@[\w.-]+\.\w+',cl(r[ei])): em+=1
        out['cards'][m]={'ver_rows':len(V),'ver_cos':len(set(map(norm,V))),'rows':len(A),'cos':len(set(map(norm,A))),'exp_ver':ev}
        vr+=len(V); exv+=ev; allv|=set(map(norm,V))
    out.update(verified_rows=vr,verified_cos_estate=len(allv),expansion_rows=exr,expansion_verified=exv,dialable_ab=ab,call_ready_email=em)
    LF=r'(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|lp|llp|pllc|pa|plc)$'
    out['verified_cos_estate_folded']=len({re.sub(LF,'',n) for n in allv})
    out['merged_if_legal_forms_stripped']=len(allv)-len({re.sub(r'(inc|incorporated|llc|ltd|limited|corp|corporation|co|company|lp|llp|pllc|pa|plc)$','',n) for n in allv})
    return out
if __name__=='__main__':
    import json,sys; print(json.dumps(measure(sys.argv[1] if len(sys.argv)>1 else '.'),indent=None)[:900])
