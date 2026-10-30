"""naming2.py — pattern set v2 (window six; fault 41 repaired). Verbs case-insensitive; a name starts with a capital and runs lazily to a
declared end; the expansion pattern is removed from naming. A matched span that is not a company (division, facility, business unit, firm,
generic phrase) is REJECTED with its span — a distinct status from unbound: the pattern worked and the span is not a company. Body binds are read
only from sentences that speak of the headline's parties. The ownership proof records its construction: direct, formerly, or d/b/a."""
import re
from naming import clean,PUB,city_from,detector,same,prove_site
NM=r"(?P<%s>[A-Z0-9][^,;:()]*?)"
END=r"(?=$|,|;|:| (?i:in|for|from|to|and|as|amid|after|with|on|at|deal)\b| -)"
I=lambda w: '(?i:'+w+')'
P2=[('{acquirer} completes/announces acquisition of {company}', NM%'acq'+' '+I('completes|announces|closes|finalizes')+' '+I('(?:the )?acquisition of')+' (?:'+I('Florida-based')+' )?'+NM%'co'+END),
    ('{acquirer} expands into ... with acquisition of {company}', NM%'acq'+' '+I('expands into')+r' [\w ]+? '+I('with(?: the)? acquisition of')+' '+NM%'co'+END),
    ('{acquirer} acquires controlling interest of {company}', NM%'acq'+' '+I('(?:acquires|buys) (?:a )?(?:controlling|majority|minority) (?:interest|stake) (?:of|in)')+' '+NM%'co'+END),
    ('{acquirer} acquires {company}', NM%'acq'+' '+I('acquires|has acquired|buys|to acquire|agrees to acquire|snaps up|purchases')+' (?:'+I('Florida-based')+' )?'+NM%'co'+END),
    ('{acquirer} agrees to $X {company} acquisition', '(?:'+I('Florida-based')+' )?'+NM%'acq'+' '+I('agrees to|to make|announces')+r' \$[\d.]+ ?[BMK]?(?i:illion)? '+NM%'co'+' '+I('acquisition|deal|purchase')),
    ('{company} acquired by {acquirer}', NM%'co'+' '+I('(?:has been |is |was )?(?:acquired by|sold to|bought by|purchased by)')+' '+r'(?P<acq>\S[^,;:()]*?)'+END),
    ('{company} names/appoints an officer', NM%'co'+' '+I('names|appoints|hires|taps|promotes')+r' [\w .\-]{2,40}? '+I('(?:as )?(?:its |new )*(?:CFO|chief financial officer|COO|chief operating officer|controller)'))]
P2=[(n,re.compile('^'+p)) for n,p in P2]
NONCO=re.compile(r"\b(?i:division|divisions|business|businesses|facility|facilities|unit|units|operations|assets|portfolio|stake|plant|firm|company|companies|branch|location|locations|segment|brand|line)\s*$|^(?i:a|an|the|local|regional)\s")
def bind2(text,where):
    t=re.sub(r'\s+-\s*$','',text).strip()
    for name,pat in P2:
        m=pat.search(t)
        if not m: continue
        co=clean(m.group('co')); acq=clean(m.groupdict().get('acq') or '') or None
        rec={'pattern':name,'span':m.group(0)[:200],'position':where}
        if NONCO.search(co): return {'rejected':True,'span_taken':co,'acquirer':acq,'name_extraction':rec,'why':'the matched span is not a company name (division, facility, business unit, firm or generic phrase)'}
        return {'company':co,'acquirer':acq,'name_extraction':rec,'acquirer_extraction':dict(rec) if acq else None}
    return None
def name2(title,body_text):
    t=PUB.sub('',re.sub(r'\s+-\s*$','',clean(title))); hb=bind2(t,'headline'); bb=None
    anchors=[w.lower() for w in re.findall(r'[A-Za-z]{3,}',' '.join(x for x in ((hb or {}).get('company') or (hb or {}).get('span_taken') or '',(hb or {}).get('acquirer') or '') if x))][:3]
    for i,s in enumerate(re.split(r'(?<=[.!?])\s+',body_text[:12000])):
        if anchors and not any(a in s.lower() for a in anchors): continue
        r=bind2(clean(s),f'body sentence {i+1}')
        if r and not r.get('rejected'): bb=r; break
    out={'headline':t,'pattern_set':'v2'}; out.update(city_from(body_text,t))
    if hb and hb.get('rejected'): out.update(state='rejected: span not a company',**hb); return out
    if hb and bb and not same(hb['company'],bb['company']): out.update(state='bind disputed',headline_bind=hb,body_bind=bb); return out
    b=hb or bb
    if b: out.update(state='bound',**b,body_bind_agrees=bool(hb and bb)); return out
    d=detector(body_text,t); out.update(state='unbound',split='headline-unmatched (a company is named; the patterns did not bind it)' if d['companies_found'] else 'no-company-named (the detector found none)',**d); return out
def prove_site2(body,company):
    base=prove_site(body,company)
    if not base: return None
    sp=base['span']; m=re.search(r'^(.*?)\s+(?:formerly|previously|f/k/a|fka)\s+',sp,re.I); d=re.search(r'(.*?)\s+(?:d/b/a|dba)\s+',sp,re.I)
    if m: base.update(construction='formerly',current_name=clean(m.group(1)))
    elif d: base.update(construction='d/b/a',current_name=clean(d.group(1)))
    else: base['construction']='direct'
    return base
