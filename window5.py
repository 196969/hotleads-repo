import asyncio,json,re,html,datetime,collections,urllib.parse
import bot,discovery,practice,intake,naming
C=json.load(open('practice-classes.json')); TODAY=discovery.TODAY
exec(open('window4.py').read().split("THIRD=64")[0].split("C=json.load")[1].join(['C=json.load','']) if False else '')
METROS=['Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala']
INDUSTRIES=['manufacturing','distribution','food and beverage','construction','transportation logistics','multi-site retail','field services','events','sales organization','marketing agency']
QP={'Acquisitions':[f'"Florida" {w}' for w in ('company acquired','acquisition','"sold to"','"CEO retiring"','succession family business')]+[f'"{m}" company acquired' for m in METROS]+[f'Florida {i} company acquired' for i in INDUSTRIES],
    'Private Equity':['"Florida" "private equity" invests','"Florida" "portfolio company"','"Florida" "private equity" acquires']+[f'"{m}" "private equity"' for m in METROS[:5]],
    'Fractionals':['"Florida" company "names" CFO','"Florida" "chief financial officer" appointed','"Florida" company expansion headquarters']+[f'"{m}" company names CFO' for m in METROS[:5]]+[f'"{m}" company expansion jobs' for m in METROS[:5]]}
R={'window':5,'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revenue':{},'revenue_sources':{},'thirteen':[],'feed_quality':{},'naming':{'processed':0,'bound':0,'disputed':0,'unbound':0,'split':collections.Counter()},'parked':{},'directory':{},'pe':collections.Counter(),'test1':collections.Counter(),'admitted_by_test':[],'decisions':[],'stopped':None,'proof':collections.Counter()}
class Stop(Exception): pass
def check():
    n=R['naming']; p=n['processed']
    if n['disputed']>3 or (p>=10 and n['disputed']/p>0.2): raise Stop(f"disputed-bind stop: {n['disputed']} of {p}")
    if n['unbound']>3 or (p>=10 and n['unbound']/p>0.2): raise Stop(f"unbound stop: {n['unbound']} of {p}, split {dict(n['split'])}")
def T(body): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',body or '',flags=re.S|re.I))))
def pubdate(body):
    for nm,pt in (('JSON-LD datePublished',r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)'),('article:published_time',r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)'),('time[datetime]',r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)')):
        m=re.search(pt,body or '')
        if m: return m.group(1),nm
    return None,None
FIG=re.compile(r'\$\s?([\d.,]+)\s?(million|billion|M\b|B\b)',re.I)
def revenue_sentence(text,company):
    toks=[w for w in re.findall(r'[A-Za-z]{3,}',company)][:2]
    for s in re.split(r'(?<=[.!?])\s+',text):
        if re.search(r'revenue|sales',s,re.I) and all(t.lower() in s.lower() for t in toks):
            m=FIG.search(s)
            if m: return float(m.group(1).replace(',',''))*(1e9 if m.group(2).lower().startswith('b') else 1e6),s.strip()[:300]
    return None,None
async def go():
    read,b,p=await discovery.browser_reader(); day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Revenue class':24,'Acquisitions':56,'Private Equity':56,'Fractionals':56,'Directory probes':8}
    for k in budget: day.spent[k]=0
    consec=collections.Counter()
    async def rd(pr,src,url,park_key=None):
        pk=park_key or src
        if pk in R['parked']: return None,'parked',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,src,url); spent[pr]+=1
        if r[0] is False:
            consec[pk]+=1
            if consec[pk]>=3: R['parked'][pk]=f'parked for the window: 3 consecutive refusals (last {r[1]})'
        elif r[0]: consec[pk]=0
        return r
    try:
        # 1 · third-party revenue class, spent on the four held first
        four=[(k,e) for k,e in Q.items() if e.get('test1_pass') and e['source']=='hig']
        for k,e in four:
            co=re.sub(r'\bSpl\b','SPL',e['company']); out={'company':co,'tried':[],'figure':None}
            # Wikipedia's own search (reference class, builder decision: a cited infobox figure is a third-party publication)
            r=await rd('Revenue class','wikipedia','https://en.wikipedia.org/w/index.php?search='+urllib.parse.quote(f'"{co}"')+'&title=Special:Search&go=Go','wikipedia')
            if r[0]:
                t=T(r[2]); isart='mw-search-results' not in r[2]
                m=re.search(r'Revenue\s*[^$]{0,40}(US)?\$\s?([\d.,]+)\s?(million|billion)',t) if isart and co.split()[0].lower() in t[:400].lower() else None
                out['tried'].append({'source':'Wikipedia search','url':r[2] and 'en.wikipedia.org search','result':('infobox revenue '+m.group(0)) if m else ('article without a revenue figure' if isart else 'no article matched \u2014 not a size reading')})
                if m: out['figure']={'value':float(m.group(2).replace(',',''))*(1e9 if m.group(3).lower()=='billion' else 1e6),'span':m.group(0),'source':'Wikipedia (infobox)','url':'en.wikipedia.org/w/index.php?search='+co,'read':TODAY}
            elif r[0] is False: out['tried'].append({'source':'Wikipedia search','result':f'refused ({r[1]})'})
            # Florida Trend's own search (a different route from its parked news route)
            if not out['figure']:
                r=await rd('Revenue class','floridatrend:search','https://www.floridatrend.com/search?q='+urllib.parse.quote(f'"{co}"'),'floridatrend:search')
                if r[0]:
                    links=list(dict.fromkeys(re.findall(r'href="(https?://(?:www\.)?floridatrend\.com/article/\d+/[^"]*)"',r[2])))[:2]; got='no article link for the name \u2014 not a size reading'
                    for u in links:
                        r2=await rd('Revenue class','floridatrend:article',u,'floridatrend:search')
                        if r2[0]:
                            fig,s=revenue_sentence(T(r2[2]),co); d,f=pubdate(r2[2])
                            if fig: out['figure']={'value':fig,'span':s,'source':'Florida Trend','url':u,'read':TODAY,'published':d}; got='figure found'; break
                            got='articles read; no sentence naming the company with a revenue figure'
                    out['tried'].append({'source':'Florida Trend search','result':got})
                elif r[0] is False: out['tried'].append({'source':'Florida Trend search','result':f'refused ({r[1]})'})
            # Google News RSS, the company's name with "revenue"
            if not out['figure']:
                r=await rd('Revenue class','gnews_rss:revenue','https://news.google.com/rss/search?q='+urllib.parse.quote(f'"{co}" revenue')+'&hl=en-US&gl=US&ceid=US:en','gnews_rss')
                if r[0]:
                    links=[html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',r[2])][1:3]; got=f'{len(links)} items; none with a sentence naming the company and a revenue figure'
                    for u in links:
                        r2=await rd('Revenue class','gnews_rss:article',u,'gnews_rss')
                        if r2[0]:
                            fig,s=revenue_sentence(T(r2[2]),co); d,f=pubdate(r2[2])
                            if fig: out['figure']={'value':fig,'span':s,'source':'news article via Google News RSS','url':u,'read':TODAY,'published':d}; got='figure found'; break
                    out['tried'].append({'source':'Google News RSS','result':got})
                elif r[0] is False: out['tried'].append({'source':'Google News RSS','result':f'refused ({r[1]})'})
            # Inc. 5000 own search: absence is never a size reading
            if not out['figure']:
                r=await rd('Revenue class','inc5000:search','https://www.inc.com/inc5000/search?query='+urllib.parse.quote(co),'inc5000')
                if r[0]:
                    m=re.search(re.escape(co.split()[0])+r'[^$]{0,200}\$\s?([\d.,]+)\s?(million|billion|M|B)\b',T(r[2]),re.I)
                    if m: out['figure']={'value':float(m.group(1).replace(',',''))*(1e9 if m.group(2).lower().startswith('b') else 1e6),'span':m.group(0)[:200],'source':'Inc. 5000','url':'inc.com/inc5000/search?query='+co,'read':TODAY}
                    out['tried'].append({'source':'Inc. 5000 search','result':'figure found' if m else 'not listed; Inc. 5000 is growth-filtered and absence is not a size reading'})
                elif r[0] is False: out['tried'].append({'source':'Inc. 5000 search','result':f'refused ({r[1]})'})
            if out['figure']:
                ceil=1e8; fig=out['figure']['value']; e['band']={'in_band':fig<=ceil,'why':f"published revenue {fig:.0f} vs {ceil:.0f} (Src: {out['figure']['url']} \u00b7 read {TODAY}; {out['figure']['source']})",'figure':out['figure']}
                e['status']=('in band \u2014 tests 1, 2 and 5 passed; site proof pending' if fig<=ceil else 'band-rejected at test 1: published revenue above the Private Equity ceiling')
            else: e['status']='held size-unsourced: no third-party revenue figure found this window on the routes tried'
            R['revenue'][e['company']]=out
            # the site-ownership proof on the four (their test-1 passes predate the rule): same fetch, the home page
            r=await rd('Private Equity','proof:hig',e['company_url'])
            if r[0]:
                pr_=naming.prove_site(r[2],co); e['site_proof']=pr_ or 'site not proved'; R['proof']['proved' if pr_ else 'not proved']+=1
                if not pr_: e['status']='site not proved \u2014 its earlier test-1 pass is withdrawn until a proved page carries it'; e['test1_pass']=False
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 2 · Google News, the window's first discovery read: the 13 (paid-for, re-runnable), then the widened queries
        for k,e in [(k,e) for k,e in Q.items() if e['source']=='gnews_rss' and not e.get('naming')]:
            r=await rd('Acquisitions','gnews_rss:reread',e['signal']['url'],'gnews_rss')
            if r[0] is None: break
            if not r[0]: R['thirteen'].append({'key':k,'state':f'refused ({r[1]})'}); continue
            res=naming.name(e.get('feed_title') or '',T(r[2])); e['naming']=res; R['naming']['processed']+=1
            if res['state']=='bind disputed': R['naming']['disputed']+=1
            elif res['state']=='unbound': R['naming']['unbound']+=1; R['naming']['split'][res['split'][:20]]+=1
            else: R['naming']['bound']+=1; e['company']=res['company']; e['company_named']=True; e['city']=res['city']
            R['thirteen'].append({'key':k,'state':res['state'],'company':res.get('company'),'derivation':res.get('name_extraction'),'split':res.get('split')}); check()
        queues={pr:list(qs) for pr,qs in QP.items()}
        while any(queues.values()) and 'gnews_rss' not in R['parked']:
            for pr in ('Acquisitions','Private Equity','Fractionals'):
                if not queues[pr]: continue
                q=queues[pr].pop(0); r=await rd(pr,'gnews_rss','https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-US&gl=US&ceid=US:en','gnews_rss')
                fq=R['feed_quality'][q]={'practice':pr,'articles_read':0,'florida_signal':0,'reached_binding':0}
                if r[0] is None: queues={x:[] for x in queues}; break
                if not r[0]: fq['refused']=str(r[1]); continue
                for it in re.findall(r'<item>(.*?)</item>',r[2],re.S):
                    ttl=html.unescape(re.sub(r'<[^>]+>','',(re.search(r'<title>(.*?)</title>',it,re.S) or [None,''])[1])); lk=html.unescape((re.search(r'<link>(.*?)</link>',it,re.S) or [None,''])[1].strip())
                    if not (re.search(r'\bFlorida\b|\bFL\b|'+'|'.join(METROS),ttl) and re.search(practice.KW[pr],ttl,re.I)) or fq['articles_read']>=2: continue
                    a=await rd(pr,'gnews_rss:article',lk,'gnews_rss')
                    if not a[0]: continue
                    fq['articles_read']+=1; d,f=pubdate(a[2]); t=T(a[2]); sent=next((s for s in re.split(r'(?<=[.!?])\s+',t) if re.search(practice.KW[pr],s,re.I) and re.search(r'\bFlorida\b|'+'|'.join(METROS),s)),None)
                    if not (d and sent): continue
                    fq['florida_signal']+=1; fq['reached_binding']+=1; res=naming.name(ttl,t); R['naming']['processed']+=1
                    k=f'{pr}:gnews_rss_w5:{fq["reached_binding"]}:{len(Q)}'; Q[k]={'practice':pr,'source':'gnews_rss_w5','company':'','signal':{'sentence':sent[:400],'url':lk,'published':d,'read':TODAY},'date_field':f,'feed_title':ttl,'query':q,'naming':res,'evidence_source':'signal','status':'proposed \u2014 unconfirmed'}
                    if res['state']=='bind disputed': R['naming']['disputed']+=1; Q[k]['status']='bind disputed \u2014 held'; check(); continue
                    if res['state']=='unbound': R['naming']['unbound']+=1; R['naming']['split'][res['split'][:20]]+=1; Q[k]['status']='unbound'; check(); continue
                    R['naming']['bound']+=1; Q[k].update(company=res['company'],company_named=True,city=res['city']); check()
                    ok2,why2=intake.test2_absent(res['company'],None,day.idx); Q[k]['test2']=why2
                    site=discovery.site_link(a[2],res['company'])
                    if not ok2 or not site: Q[k]['test1']='on file' if not ok2 else 'the article links no site for the bound name \u2014 test 1 not settled'; continue
                    s2=await rd(pr,'test1:gnews',site,'test1')
                    if not s2[0]: Q[k]['test1']=f'company page refused ({s2[1]})'; continue
                    pf=naming.prove_site(s2[2],res['company']); Q[k]['site_proof']=pf or 'site not proved'
                    if not pf: Q[k]['test1']='site not proved'; R['proof']['not proved']+=1; continue
                    R['proof']['proved']+=1; tt=T(s2[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); Q[k]['test1']=why; Q[k]['test1_pass']=t1; R['test1']['pass' if t1 else 'fail']+=1
                json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 3 · the Source Directory's remainder: FRLA and AGC chapters probed as finders; H.I.G.'s unread entries and Sun Capital's six Florida cards under the PE third, with the site proof
        for nm,u in (('Florida Restaurant and Lodging Association','https://www.frla.org'),('AGC chapters','https://www.agc.org/chapters')):
            r=await rd('Directory probes','directory:'+nm[:20],u); R['directory'][nm]=('answered \u2014 declared as a finder, no candidates' if r[0] else f'refused ({r[1]}) \u2014 parked under its code') if r[0] is not None else 'not read'
        budget['Private Equity']+=max(0,budget['Acquisitions']-spent['Acquisitions'])+max(0,budget['Fractionals']-spent['Fractionals']); R['decisions'].append('addition 5: unspent Acquisitions and Fractionals reads released to Private Equity after Google News was read or parked')
        sun=[k for k,e in Q.items() if e['source']=='suncap' and e.get('florida_on_card') and not e.get('site_proof')]
        hig=[k for k,e in Q.items() if e['source']=='hig' and not e.get('entry_read') and e.get('sponsor_page')]
        for k in sun+hig:
            e=Q[k]; src='entry:'+e['source']; r=await rd('Private Equity',src,e['sponsor_page'],src)
            if r[0] is None: break
            e['entry_read']=TODAY; R['pe']['entries']+=1
            if not r[0]: continue
            t=T(r[2]); m=re.search(r'(?:Headquarters|Location|HQ)\s*[:\-]?\s*([A-Z][A-Za-z .\-]+,\s*(?:FL|Florida|[A-Z]{2}|[A-Z][a-z]+))',t)
            if e['source']=='hig':
                lf=m.group(1) if m else None; e['location_field']=lf
                if not (lf and re.search(r'\bFL\b|Florida',lf)): continue
            R['pe']['florida']+=1; site=discovery.site_link(r[2],e['company'])
            if not site: e['test1']='entry names no company site'; continue
            r2=await rd('Private Equity','test1:'+e['source'],site,'test1')
            if r2[0] is None: break
            if not r2[0]: e['test1']=f'company page refused ({r2[1]})'; continue
            pf=naming.prove_site(r2[2],e['company']); e['site_proof']=pf or 'site not proved'
            if not pf: e['test1']='site not proved'; R['proof']['not proved']+=1; continue
            R['proof']['proved']+=1; e['company_url']=site; tt=T(r2[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
            ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':site,'read':TODAY} if ph else None,'address':{'value':addr,'url':site,'read':TODAY} if addr else None}); e['test5']=ch
            fig,s=revenue_sentence(tt,e['company']); e['band']={'in_band':fig<=1e8,'why':f'published revenue {fig:.0f} ({site} \u00b7 read {TODAY}): {s}'} if fig else {'in_band':None,'why':intake.SIZE_UNSOURCED}
            if t1: R['pe']['test1_pass']+=1
            if t1 and t5 and e['band']['in_band']: e['status']='admitted by test (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'; R['admitted_by_test'].append(k)
            elif t1 and t5: e['status']='passes tests 1, 2 and 5; site proved; held size-unsourced'
        R['stopped']='completed'
    except Stop as s: R['stopped']='NAMING STOP FIRED: '+str(s)
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    R['spent']=dict(spent); R['budget']=budget; R['naming']['split']=dict(R['naming']['split']); R['pe']=dict(R['pe']); R['test1']=dict(R['test1']); R['proof']=dict(R['proof']); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/w5-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],dict(spent))
    await b.close(); await p.stop()
asyncio.run(go())
