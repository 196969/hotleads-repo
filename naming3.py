"""naming3.py — pattern set v3 (window seven). Built on the older 9 headlines of the 17-headline binding corpus and proved on the newer 8 it
has not seen (split by arrival, fixed before any pattern was touched). Adds: '(takes|acquires) a (majority|minority|controlling) stake in',
plural verbs ('Acquire'), proper names ending in 'Company' kept, a descriptor-prefixed name trimmed to its trailing proper-name run, 'campus'
as a non-company tail. The detector is bounded to the article's own text."""
import re,json,html
from naming import clean,PUB,city_from,same,prove_site,SUFFIX
from naming2 import NM,END,I,prove_site2
P3=[('{acquirer} completes/announces acquisition of {company}', NM%'acq'+' '+I('completes|announces|closes|finalizes')+' '+I('(?:the )?acquisition of')+' (?:'+I('Florida-based')+' )?'+NM%'co'+END),
    ('{acquirer} expands into ... with acquisition of {company}', NM%'acq'+' '+I('expands into')+r' [\w ]+? '+I('with(?: the)? acquisition of')+' '+NM%'co'+END),
    ('{acquirer} takes/acquires a stake in {company}', NM%'acq'+' '+I('(?:takes|acquires|buys|makes) (?:a )?(?:controlling|majority|minority|significant)? ?(?:interest|stake|investment) (?:of|in)')+' '+NM%'co'+END),
    ('{acquirer} acquire(s) {company}', NM%'acq'+' '+I('acquires|acquire|has acquired|have acquired|buys|buy|to acquire|agrees to acquire|agree to acquire|snaps up|purchases|purchase')+' (?:'+I('Florida-based')+' )?'+NM%'co'+END),
    ('{acquirer} agrees to $X {company} acquisition', '(?:'+I('Florida-based')+' )?'+NM%'acq'+' '+I('agrees to|to make|announces')+r' \$[\d.]+ ?[BMK]?(?i:illion)? '+NM%'co'+' '+I('acquisition|deal|purchase')),
    ('{company} acquired by {acquirer}', NM%'co'+' '+I('(?:has been |is |was )?(?:acquired by|sold to|bought by|purchased by)')+' '+r'(?P<acq>\S[^,;:()]*?)'+END),
    ('{company} names/appoints an officer', NM%'co'+' '+I('names|appoints|hires|taps|promotes')+r' [\w .\-]{2,40}? '+I('(?:as )?(?:its |new )*(?:CFO|chief financial officer|COO|chief operating officer|controller)'))]
P3=[(n,re.compile('^'+p)) for n,p in P3]
GENERIC_TAIL=re.compile(r"\b(?i:division|divisions|business|businesses|facility|facilities|unit|units|operations|assets|portfolio|stake|plant|firm|branch|location|locations|segment|brand|line|campus)\s*$")
def noncompany(co):
    if GENERIC_TAIL.search(co): return True
    if re.match(r'^(?i:a|an|the|local|regional)\s',co): return True
    w=co.split()
    if w and w[-1].lower() in ('company','companies'):
        if w[-1][0].islower() or len(w)<2 or w[-2][0].islower(): return True   # 'Florida wealth management company' — a description; 'Percopo Coatings Company' — a name
    return False
def trim(co):
    """A descriptor-prefixed name ('Florida clinical research network CRWF') keeps its trailing proper-name run ('CRWF'); recorded as trimmed."""
    w=co.split()
    if any(x[:1].islower() for x in w):
        run=[]
        for x in reversed(w):
            if x[:1].isupper() or x[:1].isdigit() or x in ('&',): run.insert(0,x)
            else: break
        if run and len(run)<len(w): return ' '.join(run),True
    return co,False
def bind3(text,where):
    t=re.sub(r'\s+-\s*$','',text).strip()
    for name,pat in P3:
        m=pat.search(t)
        if not m: continue
        co=clean(m.group('co')); acq=clean(m.groupdict().get('acq') or '') or None
        rec={'pattern':name,'span':m.group(0)[:200],'position':where}
        if noncompany(co): return {'rejected':True,'span_taken':co,'acquirer':acq,'name_extraction':rec,'why':'the matched span is not a company name (division, facility, unit, campus, firm or generic description)'}
        co2,tr=trim(co)
        if tr: rec['trimmed_from']=co
        return {'company':co2,'acquirer':acq,'name_extraction':rec,'acquirer_extraction':dict(rec) if acq else None}
    return None
def article_text(body):
    """The detector's field: the article's own text \u2014 JSON-LD articleBody, else the <article> element, else <main>; recorded which."""
    m=re.search(r'"articleBody"\s*:\s*"((?:[^"\\]|\\.){200,})"',body or '')
    if m:
        try: return json.loads('"'+m.group(1)+'"'),'JSON-LD articleBody'
        except Exception: pass
    for tag in ('article','main'):
        m=re.search(r'<'+tag+r'\b[^>]*>(.*?)</'+tag+'>',body or '',re.S|re.I)
        if m and len(m.group(1))>400: return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>|<nav.*?</nav>|<header.*?</header>|<footer.*?</footer>','',m.group(1),flags=re.S|re.I)))),'<'+tag+'> element'
    return None,'no bounded article text found'
def detector3(text,title,field):
    found=[]; spans=[]
    for where,txt in (('headline',title),('article text',(text or '')[:8000])):
        for m in SUFFIX.finditer(txt): found.append(m.group(1)); spans.append({'position':where,'span':txt[max(0,m.start()-40):m.end()+20]})
    return {'detector':'legal-form suffix over the headline and the article\u2019s own text ('+field+')','companies_found':sorted(set(found))[:10],'spans_examined':spans[:10]}
def name3(title,body):
    text,field=article_text(body); t=PUB.sub('',re.sub(r'\s+-\s*$','',clean(title))); hb=bind3(t,'headline'); bb=None
    anchors=[w.lower() for w in re.findall(r'[A-Za-z]{3,}',' '.join(x for x in ((hb or {}).get('company') or (hb or {}).get('span_taken') or '',(hb or {}).get('acquirer') or '') if x))][:3]
    for i,s in enumerate(re.split(r'(?<=[.!?])\s+',(text or '')[:12000])):
        if anchors and not any(a in s.lower() for a in anchors): continue
        r=bind3(clean(s),f'article sentence {i+1}')
        if r and not r.get('rejected'): bb=r; break
    out={'headline':t,'pattern_set':'v3','article_text_field':field}; out.update(city_from(text or '',t))
    if hb and hb.get('rejected'): out.update(state='rejected: span not a company',**hb); return out
    if hb and bb and not same(hb['company'],bb['company']): out.update(state='bind disputed',headline_bind=hb,body_bind=bb); return out
    b=hb or bb
    if b: out.update(state='bound',**b,body_bind_agrees=bool(hb and bb)); return out
    d=detector3(text,t,field); out.update(state='unbound',split='headline-unmatched (a company is named in the article\u2019s own text; the patterns did not bind it)' if d['companies_found'] else 'no-company-named (the detector found none in the article\u2019s own text)',**d); return out
def derived_hosts(co):
    base=re.sub(r'(?i)\b(inc|llc|corp|corporation|co|company|group|holdings)\b\.?','',co); words=[re.sub(r'[^a-z0-9]','',w.lower()) for w in base.split()]; words=[w for w in words if w]
    if not words: return []
    out=[''.join(words)+'.com']
    if len(words)>1: out.append('-'.join(words)+'.com')
    return out[:2]
