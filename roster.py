"""roster.py — the roster reader (Step C): a listing-page mode that reads name, sector, location and status from the card itself, so only
cards that carry Florida on their face cost a company read. Built from Sun Capital's live card form (div.box-portfolio, strong.title,
span.sector, span.location-icon, data-strategy), not from memory."""
import re,html
def clean(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s or ''))).strip()
def suncap_cards(body):
    out=[]
    for m in re.finditer(r'<div class="box-portfolio[^"]*"([^>]*)>(.*?)</a>\s*</div>',body or '',re.S):
        attrs,inner=m.group(1),m.group(2)
        name=clean((re.search(r'<strong class="title">(.*?)</strong>',inner,re.S) or [None,''])[1])
        sector=clean((re.search(r'<span class="sector">.*?<span>(.*?)</span>',inner,re.S) or [None,''])[1])
        loc=clean((re.search(r'<span class="location-icon">(.*?)</span>',inner,re.S) or [None,''])[1])
        link=(re.search(r'href="([^"]+)"',inner) or [None,''])[1]; strat=(re.search(r'data-strategy="([^"]*)"',attrs) or [None,''])[1]
        if name: out.append({'name':name,'sector':sector,'location':loc,'status':strat,'entry':link})
    return out
