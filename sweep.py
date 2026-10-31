import re,html,json,collections,os,stepd
LIVE='/home/claude/dash/i320/sweep/out/'
MK=sorted(f[:-15] for f in os.listdir(LIVE) if f.endswith('-expansion.html'))
SCREEN=re.compile(r'(?i)(out[- ]of[- ]state|publicly traded|\bpublic\b|NYSE|NASDAQ|sponsor|PE[- ]backed|private[- ]equity|portfolio (?:company|of)|acquired by|sold to|subsidiary|\bparent\b|co-?op(?:erative)?\b|out[- ]of[- ]band|BAND RISK|far exceeds|KILLED|division door|not (?:\w+[- ])?owned)')
def core(n):
    n=re.sub(r"[\u2019']",'',n.upper()); n=re.sub(r'\(.*?\)','',n); n=re.sub(r'[^A-Z0-9 &]',' ',n); n=re.sub(r'\b(INC|LLC|CORP|CORPORATION|CO|COMPANY|THE|OF|COMPANIES|LTD|GROUP|HOLDINGS)\b',' ',n); return ' '.join(n.split())
def rows(m):
    out=[]
    for f in (f'{m}.html',f'{m}-expansion.html'):
        t=open(LIVE+f,encoding='utf-8').read(); tabs=list(re.finditer(r'<table([^>]*)>(.*?)</table>',t,re.S))
        idx=[0]+([i for i,x in enumerate(tabs) if 'id="intake"' in x.group(1)] if f.endswith('expansion.html') else [])
        for i in idx:
            tb=tabs[i].group(2); hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]
            if 'Company' not in hd: continue
            for r in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
                c=re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)
                if not c or len(c)<=hd.index('Company'): continue
                d={h:html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',c[j]))).strip() for j,h in enumerate(hd) if j<len(c)}
                if 'Flags' in d and 'Notes' not in d: d['Notes']=d['Flags']
                d['_links']=[]; d['_source']=f; a=stepd.assess(d)
                nm=html.unescape(re.sub('<[^>]+>','',(re.search(r'<strong>(.*?)</strong>',c[hd.index('Company')],re.S) or [None,d['Company']])[1])).strip()
                if re.search(r'(?i)open slot|reserved',nm): continue
                notes=d.get('Notes','')
                vc=a['call_ready'] and bool(re.search(r'Trading checked',notes)) and bool(re.search(r'\d{4}-\d\d-\d\d',d.get('Address source','')))
                out.append({'file':f+(' (intake)' if i else ''),'row':re.sub('<[^>]+>','',c[0]).strip(),'name':nm,'core':core(nm),'city':d.get('City',''),'tier':a['tier'],'status':d.get('Status',''),'cr':a['call_ready'],'vc':vc,'notes':notes})
    return out
