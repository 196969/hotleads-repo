"""naming.py — Item 320 rulings 11–16: the builder names the company from the article it fetched. Every bind carries its derivation
(pattern, span, position); city and acquirer the same. Headline and body bound separately; disagreement is held as 'bind disputed', never
resolved here. An unbound candidate carries the company detector's result and the spans it examined."""
import re,html
PUB=re.compile(r'\s+[-\u2013\u2014|]\s+[^-\u2013\u2014|]{2,60}$')   # Google News headline suffix " - Publisher"
STOPEND=r'(?=$|[,;:]| (?:in|for|to|and|from|as|amid|after|with|on|at|of|deal|expanding|expands|plans|sets|adds)\b)'
P=[('ACQ: {acquirer} acquires {company}',re.compile(r'^(?P<acq>[A-Z][\w&\'’.\- ]{1,60}?) (?:acquires|has acquired|buys|completes acquisition of|agrees to acquire|to acquire|snaps up|purchases) (?P<co>[A-Z][\w&\'’.\- ]{1,60}?)'+STOPEND)),
   ('ACQ: {company} acquired by {acquirer}',re.compile(r'^(?P<co>[A-Z][\w&\'’.\- ]{1,60}?) (?:(?:has been|is|was) )?(?:acquired by|sold to|bought by|purchased by) (?P<acq>[A-Z][\w&\'’.\- ]{1,60}?)'+STOPEND)),
   ('PE: {acquirer} invests in {company}',re.compile(r'^(?P<acq>[A-Z][\w&\'’.\- ]{1,60}?) (?:invests in|backs|makes (?:an )?investment in|recapitali[sz]es|partners with) (?P<co>[A-Z][\w&\'’.\- ]{1,60}?)'+STOPEND)),
   ('FRAC: {company} names/appoints an officer',re.compile(r'^(?P<co>[A-Z][\w&\'’.\- ]{1,60}?) (?:names|appoints|hires|taps|promotes|welcomes) (?P<acq>[A-Z][\w\'’.\- ]{1,40}?) (?:as |to )?(?:its )?(?:new )?(?:CFO|chief financial officer|COO|chief operating officer|controller|president|CEO|chief executive)',re.I)),
   ('FRAC: {company} expands/opens',re.compile(r'^(?P<co>[A-Z][\w&\'’.\- ]{1,60}?) (?:to expand|expands|plans expansion|opens new|breaks ground|relocates headquarters|to open)'+r'\b'))]
GENERIC=re.compile(r'^(?:a|an|the|this|local|florida|south florida|tampa|miami|orlando|jacksonville)?\s*(?:company|firm|business|investment firm|private equity firm|group|startup|developer|investor|buyer|family)s?$',re.I)
SUFFIX=re.compile(r'\b([A-Z][\w&\'’.\-]*(?: [A-Z][\w&\'’.\-]*){0,4} (?:Inc|LLC|L\.L\.C|Corp|Corporation|Co|Company|Group|Holdings|Partners|Capital|Industries|Enterprises|Ltd))\b\.?')
FLCITY=re.compile(r'\b(Miami|Fort Lauderdale|Tampa|Orlando|Jacksonville|West Palm Beach|Sarasota|Naples|Fort Myers|Pensacola|Tallahassee|Gainesville|Lakeland|Ocala|Boca Raton|Doral|Coral Gables|Clearwater|St\. Petersburg|Hialeah|Daytona Beach|Melbourne|Jupiter|Delray Beach|Pompano Beach|Hollywood|Kissimmee|Sanford|Bradenton|Port St\. Lucie|Vero Beach|Palm Beach Gardens|Weston|Plantation|Sunrise)\b')
def clean(t): return re.sub(r'\s+',' ',html.unescape(t or '')).strip(' .,;:\'"\u201c\u201d')
def bind_text(text,where):
    for name,pat in P:
        m=pat.search(text)
        if not m: continue
        co=clean(m.group('co')); acq=clean(m.group('acq')) if 'acq' in m.groupdict() and m.group('acq') else None
        if not co or GENERIC.match(co): continue
        return {'company':co,'acquirer':acq,'name_extraction':{'pattern':name,'span':m.group(0)[:200],'position':where},'acquirer_extraction':{'pattern':name,'span':m.group(0)[:200],'position':where} if acq else None}
    return None
def same(a,b):
    na=set(w.lower() for w in re.findall(r'[A-Za-z]{3,}',a)); nb=set(w.lower() for w in re.findall(r'[A-Za-z]{3,}',b)); return bool(na and nb and (na<=nb or nb<=na or len(na&nb)>=max(1,min(len(na),len(nb))-0)))
def city_from(body_text,title):
    for where,txt in (('headline',title),('body',body_text[:6000])):
        m=FLCITY.search(txt)
        if m: return {'city':m.group(1),'city_extraction':{'pattern':'Florida city name in text','span':txt[max(0,m.start()-60):m.end()+40],'position':where}}
    return {'city':None,'city_extraction':{'pattern':'Florida city name in text','span':None,'position':'none found in headline or first 6000 characters'}}
def detector(body_text,title):
    spans=[]; found=[]
    for where,txt in (('headline',title),('body',body_text[:8000])):
        for m in SUFFIX.finditer(txt): found.append(m.group(1)); spans.append({'position':where,'span':txt[max(0,m.start()-40):m.end()+20]})
    return {'detector':'legal-form suffix (Inc, LLC, Corp, Co, Company, Group, Holdings, Partners, Capital, Industries, Enterprises, Ltd) over the headline and the first 8000 body characters','companies_found':sorted(set(found))[:10],'spans_examined':spans[:10]}
def name(title,body_text):
    """Returns the naming record: bound / bind disputed / unbound (with split and detector)."""
    t=PUB.sub('',clean(title)); hb=bind_text(t,'headline'); bb=None
    for i,s in enumerate(re.split(r'(?<=[.!?])\s+',body_text[:12000])):
        r=bind_text(clean(s),f'body sentence {i+1}')
        if r: bb=r; break
    out={'headline':t}; out.update(city_from(body_text,t))
    if hb and bb and not same(hb['company'],bb['company']):
        out.update(state='bind disputed',headline_bind=hb,body_bind=bb); return out
    b=hb or bb
    if b: out.update(state='bound',**b,body_bind_agrees=bool(hb and bb)); return out
    d=detector(body_text,t); out.update(state='unbound',split='headline-unmatched (a company is named; the patterns did not bind it)' if d['companies_found'] else 'no-company-named (the detector found none)',**d); return out

def prove_site(body,company):
    """Fault 39's class repaired in shape: a site belongs to the bound company only when its own page names it in the page title, a main
    heading, or the copyright line. Returns the proving span and where it sits, or None. Read from the same fetch test 1 reads."""
    toks=[w.lower() for w in re.findall(r'[A-Za-z]{3,}',company) if w.lower() not in ('inc','llc','corp','company','group','the','and','holdings')]
    if not toks: return None
    places=[('title',' '.join(re.findall(r'<title[^>]*>(.*?)</title>',body,re.S|re.I))),('main heading',' '.join(re.findall(r'<h1[^>]*>(.*?)</h1>',body,re.S|re.I))),('copyright line',' '.join(re.findall(r'(?:&copy;|\u00a9|Copyright)[^<]{0,120}',body,re.I))),('og:site_name',' '.join(re.findall(r'og:site_name"\s+content="([^"]+)"',body)))]
    for where,txt in places:
        t=clean(re.sub(r'<[^>]+>',' ',txt)); low=t.lower().replace('-',' ')
        if t and all(tk in low.replace(' ','') or tk in low for tk in toks[:2]): return {'where':where,'span':t[:160]}
    return None

