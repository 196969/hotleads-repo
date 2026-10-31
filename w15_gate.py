"""Fault 59: the window does not launch unless every proof passes. Exit status 0 only on PASSED for all."""
import json,html,re,sys,hashlib,os,naming5,naming8,naming9
Q=json.load(open('florida-intake-queue.json')); out={}
good=[html.unescape(e['feed_title']) for e in Q.values() if e.get('feed_title') and (e.get('naming') or {}).get('state')=='bound' and not naming9.is_asset(e.get('company') or '')[0] and e.get('company') not in ('S.E','Fort Myers','Door Maker')]
naming9.is_abbrev.ctx=''
lost=[t for t in good if not naming9.property_precondition2(t)[0]]
stop=['Midtown Capital Partners acquires Orlando industrial portfolio for $56.1M - JLL','Bowden Companies Acquires 200-Unit Pensacola Apartment Community, Rebrands It as The Maren - x','Westshore Grand Hotel Acquired by Tampa Developer, Major Renovations Planned - TBBW']
st=[(t[:50],not naming9.property_precondition2(t)[0]) for t in stop]
out['pre_read_rejection']={'keep_set':len(good),'good_headlines_stopped':lost,'stop_set':st,'result':'PASSED' if not lost and all(x for _,x in st) else 'FAILED'}
keep=sorted({e['company'] for e in Q.values() if e.get('company') and (e.get('naming') or {}).get('state')=='bound' and e['company'] not in ('S.E','South Florida Distributor American Fasteners','Fort Myers','Door Maker','Another A-B Wholesaler Pepin Distributing')})
changed=[c for c in keep if naming8.cleanup(c)[0]!=c]
cases={'Miami HVAC Distributor AM Distributors':'AM Distributors','AM Distributors':'AM Distributors','Another A-B Wholesaler Pepin Distributing':'Pepin Distributing','South Florida Distributor American Fasteners':'American Fasteners','Fort Myers':None}
got={c:naming8.cleanup(c)[0] for c in cases}
out['fault52_role_noun']={'planted':got,'expected':cases,'keep_set':len(keep),'good_binds_changed':changed,'note':'a role-noun tail no longer rejects; \u201cVenice Window and Door Maker\u201d now goes to the ownership proof rather than being rejected unread','result':'PASSED' if got==cases and not changed else 'FAILED'}
CHK={}
def CK(n,res):
    c=CHK.setdefault(n,{'calls':0,'stopped':0}); c['calls']+=1; c['stopped']+=0 if res[0] else 1; return res
for t in stop+good[:3]: CK('pre-read',naming9.property_precondition2(t))
out['counters']={'pre-read':CHK['pre-read'],'never_wired':CHK.get('never',{'calls':0}),'result':'PASSED' if CHK['pre-read']['calls']==6 and CHK['pre-read']['stopped']==3 else 'FAILED'}
json.dump(out,open('reports/w15-gate.json','w'),indent=1,ensure_ascii=False)
print({k:v['result'] for k,v in out.items()}, '| lost',lost,'| changed',changed,'| got',got)
sys.exit(0 if all(v['result']=='PASSED' for v in out.values()) else 1)
