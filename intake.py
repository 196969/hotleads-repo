"""intake.py — Item 320 Part 9 intake (9.3 tests, 9.4 record, 9.6 floor, 9.2 filter). Machine-settled: test 1 (Florida operating address on the
company's own page, not a registered agent), test 2 (absent from all 81 files by name and domain), test 5 (reachable channel recorded as which),
the band floor, the non-company filter, and the sourcing of every history clause. Tests 3 and 4 are human-judged in the queue and are recorded here
only as the human's decision with a name and date. Nothing here admits a row to florida.html; admitted rows enter florida-expansion.html as Unverified."""
import json,re,html,glob
NC=json.load(open('non-companies.json'))['classes']
class FloorNotRuled(Exception): pass
def host_of(u): return re.sub(r'^https?://(www\.)?','',u or '').split('/')[0].lower()
def non_company(domain):
    d=domain.lower()
    for cls,doms in NC.items():
        if any(d==x or d.endswith('.'+x) for x in doms): return cls
    return None
def index_files(pattern='*.html',exclude=()):
    norm=lambda s: re.sub(r'[^a-z0-9]','',html.unescape(s).lower().split('(')[0]); N={}
    for f in glob.glob(pattern):
        if f in exclude: continue
        t=open(f,encoding='utf-8',errors='ignore').read()
        if '<table' not in t: continue
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S):
            m=re.search(r'<strong>(.*?)</strong>',row)
            if m: N.setdefault(norm(re.sub('<[^>]+>','',m.group(1))),set()).add(f)
            for h in re.findall(r'href="https?://(?:www\.)?([^/"]+)"',row):
                if not re.search(r'google\.|linkedin\.',h): N.setdefault('DOM:'+h.lower(),set()).add(f)
    return N,norm
def test1_florida(company_page):
    """company_page: {'url','read','address_text'} read from the company's OWN page. Passes only with a Florida operating address evidenced there; a registered-agent address is not operating."""
    if not company_page or not company_page.get('url'): return False,'no company page read'
    a=company_page.get('address_text') or ''
    if re.search(r'registered agent',a,re.I): return False,'registered agent address, not operating'
    if not re.search(r'\bFL\b|\bFlorida\b',a): return False,'no Florida address on the company\u2019s own page'
    return True,f'Florida operating address on {company_page["url"]} \u00b7 read {company_page.get("read")}'
def test2_absent(company,domain,index):
    N,norm=index; hits=set(N.get(norm(company),set()))|N.get('DOM:'+(domain or '').lower(),set())
    return (not hits),('absent from all files' if not hits else 'already on file in: '+', '.join(sorted(hits)))
def test5_channel(rec):
    for k in ('phone','address','form'):
        v=rec.get(k)
        if v and v.get('value') and v.get('url') and v.get('read'): return True,k
    return False,'no reachable channel with source and date'
def floor_check(rec,floor):
    if floor is None: raise FloorNotRuled('band floor not ruled: the practice standard carries no figure (9.0.h)')
    fig=rec.get('size_figure')
    if fig is None: return False,'no size figure on a page'
    return (fig>=floor),f'figure {fig} against floor {floor}'
def history_clauses(hist):
    """Every clause carries a URL or is blank. Returns the clauses that would be written and the ones left blank."""
    out={}; blank=[]
    for k in ('years_operating','ownership_generation','size_band','why_this_practice'):
        v=hist.get(k) if hist else None
        if v and v.get('url') and v.get('read'): out[k]=v
        else: blank.append(k)
    return out,blank
def signal_usable(sig):
    if not sig or not sig.get('company_named'): return False,'listing or announcement names no company \u2014 unusable, never guessed'
    if not (sig.get('url') and sig.get('published') and sig.get('read')): return False,'signal lacks URL, publication date or read date'
    if sig.get('source_is_company_site'): return False,'a company\u2019s own page is not a signal'
    return True,'usable'
