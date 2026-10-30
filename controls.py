"""controls.py — planted known-answer controls, one per declared discovery source, in that source's own link form as declared in practice-classes.json. Each probe: the source's item pattern must extract exactly the planted items from the planted page, and nothing from a page of another form. Local files only; no reads. Note (C-prep): three controls first demanded a title their declared pattern never captures — a control fault, corrected; the parsers were right."""
import json,re,html,sys
import discovery
D=json.load(open('practice-classes.json'))['discovery']
PLANT={'hig':('<a href="https://hig.com/portfolio/acme-foods/">Acme Foods</a><a href="https://hig.com/about/">About</a>',[('https://hig.com/portfolio/acme-foods/','Acme Foods')]),
 'suncap':('<a href="https://www.suncappart.com/portfolio/beta-logistics/">Beta Logistics</a>',[('https://www.suncappart.com/portfolio/beta-logistics/','Beta Logistics')]),
 'trivest':('<a href="https://www.trivest.com/portfolio/gamma-marine/">Gamma Marine</a>',[('https://www.trivest.com/portfolio/gamma-marine/','Gamma Marine')]),
 'comvest':('<a href="https://www.comvest.com/portfolio/delta-health/">Delta Health</a>',[('https://www.comvest.com/portfolio/delta-health/','Delta Health')]),
 'boyne':('<a href="https://boynecapital.com/portfolio/epsilon-spices/">Epsilon Spices</a>',[('https://boynecapital.com/portfolio/epsilon-spices/','Epsilon Spices')]),
 'florida_trend':('<a href="https://www.floridatrend.com/article/12345/zeta-acquired">Zeta</a> https://www.floridatrend.com/article/12345/&sa=U <div>https://www.floridatrend.com/article/1/</div>',[('https://www.floridatrend.com/article/12345/zeta-acquired','')]),
 'bizbuysell':('<a href="https://www.bizbuysell.com/Business-Opportunity/eta-co-inc/123/">Eta Co Inc</a>',[('https://www.bizbuysell.com/Business-Opportunity/eta-co-inc/123/','Eta Co Inc')]),
 'indeed':('<a data-jk="abcdef1234" href="/x"><span title="Controller - Theta Industries">Controller</span></a>',None),
 'ziprecruiter':('<a href="https://www.ziprecruiter.com/c/Iota-Corp/Job/CFO/-in-Tampa,FL?x=1">CFO</a>',[('https://www.ziprecruiter.com/c/Iota-Corp/Job/CFO/-in-Tampa,FL?x=1','')]),
 'glassdoor':('<a href="https://www.glassdoor.com/job-listing/cfo-kappa-llc-JV_IC1154170.htm">CFO</a>',[('https://www.glassdoor.com/job-listing/cfo-kappa-llc-JV_IC1154170.htm','')])}
def probe_all():
    out={}
    for p,v in D['practices'].items():
        for src in v['sources']:
            page,expect=PLANT[src['id']]; got=discovery.items(src,page); other=discovery.items(src,'<a href="https://example.com/x">x</a>')
            ok=(got==expect if expect is not None else len(got)>0) and other==[]
            out[src['id']]={'practice':p,'classes':['the source\u2019s own link form / a page of another form','a clean href / a malformed tail (Florida Trend)'],'planted_items':expect,'parsed':got,'other_form_parsed':other,'result':'PROBE PASSED' if ok else 'PROBE FAILED'}
    return out
if __name__=='__main__': print(json.dumps(probe_all(),indent=1,ensure_ascii=False))
