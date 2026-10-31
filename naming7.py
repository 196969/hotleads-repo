"""naming7.py — window eleven. Fault 51's repair as a precondition: a headline whose bound target names a property is stopped before any read.
Fault 50's repair: an article-link candidate must point off the publisher's own host."""
import re,html
import naming,naming4,naming5
PROP=re.compile(r'(?i)\b(hotel|hotels|resort|resorts|marina|marinas|apartment|apartments|park|parks|property|properties)\b')
def property_precondition(title):
    """Ruled tails (hotel, resort, marina, apartment, park, property); builder decision: matched anywhere in the bound target, not only as its last
    word, because '200-Unit Pensacola Apartment Community' carries the word before its tail. Returns (passes, reason)."""
    r=naming4.name4(html.unescape(title or ''),'')
    if r.get('state')=='bound' and PROP.search(r.get('company') or ''): return False,'the bound target names a property: '+r['company']
    return True,None
def registrable(host):
    p=host.lower().split('.'); return '.'.join(p[-2:]) if len(p)>=2 else host.lower()
def publisher_host(body,fallback):
    m=re.search(r'<link[^>]+rel="canonical"[^>]+href="https?://([^/"]+)',body or '') or re.search(r'og:url"\s+content="https?://([^/"]+)',body or '')
    return (m.group(1) if m else (re.sub(r'^https?://','',fallback or '').split('/')[0])).lower()
