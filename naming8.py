"""naming8.py — window twelve. Fault 54: a challenge screen served with HTTP 200 is a refusal (challenge, re-runnable), never a page.
Fault 52: a name is bounded by the company \u2014 'Place Role Name' descriptors stripped, a span ending in a role noun is a description, a bare
place is not a company. Ruling (b): a rename the page states without 'formerly' \u2014 the host derived from or linked for the bound name, and a
sentence on that page naming the bound name with a rename or merger verb \u2014 proves, construction 'renamed', current name recorded."""
import re,html
import naming,naming4,naming5
CHALLENGE=re.compile(r'(?i)robot challenge|access denied|just a moment|verify you are human|attention required|are you a robot|checking your browser|security check|request blocked|pardon our interruption|cf-chl-|captcha-delivery|px-captcha')
def is_challenge(body):
    b=body or ''; t=(re.search(r'<title[^>]*>(.*?)</title>',b,re.S|re.I) or [None,''])[1]
    return bool(CHALLENGE.search(t)) or (len(re.sub(r'<[^>]+>','',b))<2500 and bool(CHALLENGE.search(b[:6000])))
PLACES=['Florida','South Florida','Central Florida','North Florida','Southwest Florida','Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala','Venice','Doral','Boca Raton','Clearwater','St. Petersburg','Nebraska','Texas','Georgia','Alabama']
ROLE=r'(?:Distributor|Distributors|Maker|Makers|Manufacturer|Manufacturers|Supplier|Suppliers|Developer|Developers|Provider|Providers|Operator|Operators|Retailer|Retailers|Builder|Builders|Contractor|Contractors|Firm|Firms)'
PL='(?:'+'|'.join(re.escape(p) for p in sorted(PLACES,key=len,reverse=True))+')'
def cleanup(co):
    """Returns (name or None, note)."""
    c=naming.clean(co)
    if re.fullmatch(PL,c): return None,'a bare place name, not a company'
    m=re.match(r'^(?:'+PL+r'\s+)?'+ROLE+r'\s+([A-Z0-9].+)$',c)
    if m: return m.group(1),f'title-case descriptor stripped from \u201c{c}\u201d'
    if re.search(r'\b'+ROLE+r'$',c): return None,'a description ending in a role noun, not a name'
    return c,None
RENAME=re.compile(r'(?i)\b(?:merg(?:e|es|ing|ed) (?:to form|into|with)|is now|are now|now known as|formerly|rebrand(?:s|ed|ing)? (?:as|to)|renamed|has become|became|joins|joined)\b')
def host_core(host): return re.sub(r'[^a-z0-9]','',re.sub(r'^www\.','',host.lower()).split('.')[0])
def prove_site8(body,company,host):
    if is_challenge(body): return 'challenge'
    if naming4.PARKED.search((body or '')[:20000]): return None
    p=naming5.prove_site5(body,company)
    if p: return p
    core=naming5.core(company).replace(' ','')
    if not core or core not in host_core(host): return None
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',body or '',flags=re.S|re.I))))
    for s in re.split(r'(?<=[.!?])\s+',t[:20000]):
        if core in re.sub(r'[^a-z0-9]','',s.lower()) and RENAME.search(s):
            cur=(re.search(r'<title[^>]*>(.*?)</title>',body or '',re.S|re.I) or [None,''])[1]; cur=naming.clean(cur.split('|')[-1]) if '|' in cur else naming.clean(cur)
            return {'where':'page sentence','span':s.strip()[:220],'construction':'renamed (the page states it; no \u201cformerly\u201d)','current_name':cur,'whole_name':naming5.core(company)}
    return None
