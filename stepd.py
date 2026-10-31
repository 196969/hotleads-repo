"""Step D \u2014 zero reads. The call-ready definition applied to the 200 rows, the completion queue measured and ranked, the dial order, and the
completion-queue page with the contact block (the two Step C enrichments the queue needs)."""
import re,html,json,collections
import naming10
DATE=r'\d{4}-\d\d-\d\d'
ROLE=re.compile(r'^(info|sales|contact|hello|office|admin|support|service|customerservice|orders|inquiries|team|hr|careers|marketing)$',re.I)
TITLEW=re.compile(r'(?i)\b(president|ceo|chief|owner|founder|principal|general manager|managing|director|cfo|coo|partner|vice president|vp)\b')
INDUSTRY=re.compile(r'(?i)manufactur|industrial|distribut|wholesale|import|food|beverage|construct|trade|transport|logistic|freight|trucking|retail|field|event|marketing|brand|sales|design|services|fraud')
def rows_of(path,which,source):
    t=open(path,encoding='utf-8').read(); tb=re.findall(r'<table[^>]*>(.*?)</table>',t,re.S)[which]
    hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]; out=[]
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)
        if not c: continue
        d={h:html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',c[i]))).strip() for i,h in enumerate(hd) if i<len(c)}
        d['_links']=re.findall(r'href="(https?://[^"]+)"',r); d['_source']=source; out.append(d)
    return out
def assess(d):
    dm=d.get('Decision maker',''); words=re.findall(r"[A-Z][a-zA-Z'\-]+",dm)
    has_person=any(naming10.is_person(' '.join(words[i:i+2])) for i in range(max(0,len(words)-1))) and bool(TITLEW.search(dm))
    phone=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',d.get('Phone',''))
    em=re.search(r'[\w.+-]+@[\w.-]+\.\w{2,}',d.get('Email','')+' '+d.get('Email or address','')+' '+d.get('Notes',''))
    dated=bool(re.search(DATE,d.get('Address source','')+' '+d.get('Notes','')+' '+d.get('Decision maker','')))
    contact=bool(phone or em) and dated
    tier=d.get('Tier',''); fit=tier in ('A','B','Unverified')   # fit = the market standard's tier test already passed; an industry word list failed 40 good rows ("mfg", "dist", "3PL")
    sig=re.search(r'(?:Acquisitions|Fractionals|Private Equity|PE) signal[^\u00b7]*\u00b7[^\u00b7]*?('+DATE+')',d.get('Notes',''))
    sig_date=sig.group(1) if sig else (re.search(DATE,d.get('Company history','')) or [None])[0] if d.get('Company history') else None
    missing=[x for x,ok in (('named decision maker with title',has_person),('published phone or email with a dated Src:',contact),('practice fit (tier and industry)',fit)) if not ok]
    role=bool(em and ROLE.match(em.group(0).split('@')[0]))
    return {'company':d.get('Company','')[:60],'tier':tier,'source':d['_source'],'call_ready':not missing,'missing':missing,'signal':sig_date or 'Blind','phone':phone.group(0) if phone else None,'email':em.group(0) if em else None,'role_inbox':role,'dm':dm[:80],'links':d['_links'][:3]}
def est(m): return 5*len(m)
