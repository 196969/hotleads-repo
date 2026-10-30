"""naming5.py — window nine. (1) The ownership proof requires the WHOLE bound name, normalised, contiguous in the proving field (title, main
heading, copyright line, site name); parked and for-sale pages refused; construction recorded. (2) The headline precondition: a company-shaped
token (a legal-form suffix, a capitalised multi-word name, or a single capitalised word) adjacent to a signal verb, or the article is not read."""
import re,html
import naming,naming4
LEGAL=r'(?:inc|llc|l\.l\.c|corp|corporation|co|company|ltd|plc|lp|llp)'
def norm(s): return ' '.join(re.sub(r"[\u2019'’]s\b",'',re.sub(r'[^a-z0-9 ]',' ',re.sub(r"[\u2019'’]",'',html.unescape(s or '').lower()))).split())
def core(name):
    w=norm(name).split()
    while w and re.fullmatch(LEGAL,w[-1]): w=w[:-1]
    return ' '.join(w)
def prove_site5(body,company):
    if naming4.PARKED.search((body or '')[:20000]): return None
    c=core(company)
    if not c: return None
    places=[('title',' '.join(re.findall(r'<title[^>]*>(.*?)</title>',body or '',re.S|re.I))),('main heading',' '.join(re.findall(r'<h1[^>]*>(.*?)</h1>',body or '',re.S|re.I))),('copyright line',' '.join(re.findall(r'(?:&copy;|\u00a9|Copyright)[^<]{0,120}',body or '',re.I))),('og:site_name',' '.join(re.findall(r'og:site_name"\s+content="([^"]+)"',body or '')))]
    for where,txt in places:
        t=naming.clean(re.sub(r'<[^>]+>',' ',txt)); n=' '+norm(t)+' '
        if ' '+c+' ' in n or ' '+c.replace(' ','')+' ' in n:
            out={'where':where,'span':t[:160],'whole_name':c}
            m=re.search(r'^(.*?)\s+(?:formerly|previously|f/k/a|fka)\s+',t,re.I); d=re.search(r'(.*?)\s+(?:d/b/a|dba)\s+',t,re.I)
            if m: out.update(construction='formerly',current_name=naming.clean(m.group(1)))
            elif d: out.update(construction='d/b/a',current_name=naming.clean(d.group(1)))
            else: out['construction']='direct'
            return out
    return None
VERB=r'(?i:acquires?|acquired|acquisition|buys|sold|names|appoints|takes|invests|expands|completes|announces|agrees|merges?|purchases?)'
SUF=r"(?:Inc|LLC|Corp|Co|Company|Group|Holdings|Partners|Capital|Industries)\.?"
TOK=r"(?:[A-Z0-9][\w&'’.\-]*(?: (?:&|[A-Z0-9][\w&'’.\-]*))*)"
def precondition(title):
    t=naming.PUB.sub('',naming.clean(html.unescape(title or '')))
    m=re.search(TOK+r'\s+'+VERB,t) or re.search(VERB+r'\s+(?:[\w\-]+\s){0,2}'+TOK,t)
    return bool(m),(m.group(0) if m else None)
