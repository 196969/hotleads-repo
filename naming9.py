"""naming9.py — window thirteen. Fault 56: an abbreviation or ticker is not a name. Fault 57: a closed word list where an open test was needed \u2014
the property precondition re-stated as a test: a span is an asset, not an entity, when (a) it carries a measure (a number with a unit: '200-Unit',
'226,500 SF', '538,000-Square-Foot'), or (b) nothing is left of it once place names and lower-case words are removed (no proper-name core:
'Orlando industrial portfolio'), or (c) its head noun is a building or land type. (c) is still a list and is stated as such; (a) and (b) are the open tests."""
import re,html
import naming,naming4,naming8
def is_abbrev(co):
    c=(co or '').strip()
    return bool(re.fullmatch(r"(?:[A-Z]\.){1,4}[A-Z]?\.?|\([A-Z]{1,6}\)|[A-Z]\.?",c)) or (bool(re.fullmatch(r"[A-Z]{2,6}",c)) and bool(re.search(r"\("+re.escape(c)+r"\)",getattr(is_abbrev,"ctx",""))))
MEASURE=re.compile(r"\b\d[\d,.]*\s*-?\s*(?:unit|units|sf|sq\.?\s*ft|square[- ]foot|square[- ]feet|acre|acres|room|rooms|bed|beds|key|keys|story|stories)\b",re.I)
HEAD=re.compile(r"(?i)\b(?:hotel|resort|marina|apartments?|community|park|portfolio|campus|plaza|tower|building|complex|development|property|properties|site|land|parcel|warehouse|center|centre)$")
PLACEW=set(w.lower() for p in naming8.PLACES for w in p.split())
def core_left(co):
    return [w for w in re.findall(r"[A-Za-z][\w&'’.\-]*",co) if w[0].isupper() and w.lower().strip('.') not in PLACEW]
def is_asset(co,keep_center=True):
    c=naming.clean(co)
    if MEASURE.search(c): return True,'(a) carries a measure'
    if not core_left(c): return True,'(b) no proper-name core once places and lower-case words are removed'
    h=HEAD.search(c)
    if h and not (keep_center and h.group(0).lower() in ('center','centre') and re.search(r'(?i)medical|health|hospital|cancer',c)): return True,'(c) head noun is a building or land type: '+h.group(0)
    return False,None
def property_precondition2(title):
    r=naming4.name4(html.unescape(title or ''),'')
    if r.get('state')=='bound':
        a,why=is_asset(r.get('company') or '')
        if a: return False,why+' \u2014 '+r['company']
    if r.get('state','').startswith('rejected'): return False,'the headline\u2019s target is already rejected as a non-company \u2014 '+(r.get('span_taken') or '')+' (stopped before its read)'
    return True,None
