import asyncio,json,re,html,datetime,collections,urllib.parse,time
import bot,discovery,practice,intake,naming
C=json.load(open('practice-classes.json')); BANDS=C['band_by_practice']; TODAY=discovery.TODAY
METROS=['Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala']
INDUSTRIES=['manufacturing','distribution','food and beverage','construction','transportation logistics','multi-site retail','field services','events','sales organization','marketing agency']
QP={'Acquisitions':[f'"Florida" {w}' for w in ('company acquired','acquisition','"sold to"','"CEO retiring"','succession family business')]+[f'"{m}" company acquired' for m in METROS]+[f'Florida {i} company acquired' for i in INDUSTRIES],
    'Private Equity':['"Florida" "private equity" invests','"Florida" "portfolio company"','"Florida" "private equity" acquires']+[f'"{m}" "private equity"' for m in METROS[:5]],
    'Fractionals':['"Florida" company "names" CFO','"Florida" "chief financial officer" appointed','"Florida" company expansion headquarters']+[f'"{m}" company names CFO' for m in METROS[:5]]+[f'"{m}" company expansion jobs' for m in METROS[:5]]}
THIRD=64; PROBES=8
DIRECTORY=[('ACG chapters','https://www.acg.org/chapters'),('Florida DBPR','https://www.myfloridalicense.com'),('Florida Chamber','https://www.flchamber.com'),('SelectFlorida','https://www.selectflorida.org'),('Manufacturers Association of Florida','https://www.mafmfg.com'),('FloridaMakes','https://www.floridamakes.com'),('Florida Trucking Association','https://www.fltrucking.org'),('LinkedIn Jobs (Florida controller / ops director)','https://www.linkedin.com/jobs/search/?keywords=controller%20OR%20%22director%20of%20operations%22&location=Florida')]
PARKED={'Sunbiz':'0 reads permitted','BizBuySell Florida':'403 (window one)','FloridaCommerce WARN':'403 (window three)','South Florida / Tampa Bay / Orlando / Jacksonville Business Journals':'403 news sections and feed','Florida Trend':'stopped: no date in any form (window three)','Indeed':'403','ZipRecruiter':'403','Glassdoor':'403','Trivest':'renders after load','Transworld':'404','Murphy Business':'404','CareerBuilder':'403','SimplyHired':'403','EDGAR full-text':'403','GlobeNewswire feed':'403','Sunbelt':'broker listing, unnamed (Chair ruling)','Comvest entries':'no location field in 20 entries read \u2014 not repeated','Boyne entries':'one Florida placement settled (MBP, no Florida address)'}
class Stop(Exception): pass
R={'window':4,'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'naming':{'processed':0,'bound':0,'disputed':0,'unbound':0,'split':collections.Counter()},'feed_quality':{},'thirteen':[],'directory':{},'pe':{},'decisions':[],'stopped':None,'admitted_by_test':[],'test1':collections.Counter(),'budget':{}}
def check_stops():
    n=R['naming']; p=n['processed']
    if n['disputed']>3 or (p>=10 and n['disputed']/p>0.2): raise Stop(f"disputed-bind stop: {n['disputed']} disputed of {p} processed")
    if n['unbound']>3 or (p>=10 and n['unbound']/p>0.2): raise Stop(f"unbound stop: {n['unbound']} unbound of {p} processed (split {dict(n['split'])})")
async def go():
    read,b,p=await discovery.browser_reader(); day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Acquisitions':THIRD,'Private Equity':THIRD,'Fractionals':THIRD,'Directory probes':PROBES}; R['budget']=budget
    for k in ('Acquisitions','Private Equity','Fractionals','Directory probes'): day.spent[k]=0
    async def rd(pr,src,url):
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,src,url); spent[pr]+=1; return r
    def text_of(body): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S|re.I))))
    async def name_and_test(k,e,body,pr):
        txt=text_of(body); r=naming.name(e.get('feed_title') or e['signal']['sentence'],txt); e['naming']=r; R['naming']['processed']+=1
        if r['state']=='bind disputed': R['naming']['disputed']+=1; e['status']='bind disputed \u2014 held, not resolved by the builder'; check_stops(); return
        if r['state']=='unbound': R['naming']['unbound']+=1; R['naming']['split'][r['split'][:20]]+=1; e['status']='unbound \u2014 filtered with the detector\u2019s result'; check_stops(); return
        R['naming']['bound']+=1; e['company']=r['company']; e['company_named']=True; e['city']=r['city']; e['acquirer']=r.get('acquirer'); check_stops()
        ok2,why2=intake.test2_absent(e['company'],None,day.idx); e['test2']=why2
        if not ok2: e['status']='on file \u2014 a signal against the existing row'; return
        site=discovery.site_link(body,e['company']); e['company_url']=site
        if not site: e['test1']='the article links no site matching the bound name \u2014 test 1 not settled (no provider is read)'; R['test1']['no site linked']+=1; return
        x=await rd(pr,'test1:'+e['source'],site)
        if x[0] is None: e['test1']='not read: '+str(x[1]); R['test1']['not read']+=1; return
        if not x[0]: e['test1']=f'company page refused ({x[1]})'; R['test1']['refused']+=1; return
        t=text_of(x[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',t)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or t[:300]}); e['test1']=why; e['test1_pass']=t1; R['test1']['pass' if t1 else 'fail']+=1
        ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',t); em=[z for z in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',t) if not re.search(r'\.(png|jpg|svg|webp)$',z)]
        e['phone']={'value':ph.group(0),'url':site,'read':TODAY} if ph else None; e['email']={'value':em[0],'url':site,'read':TODAY,'role_inbox':bool(re.match(r'^(info|sales|contact|hello|office|admin|support|customerservice)',em[0].split('@')[0],re.I))} if em else None
        t5,ch=intake.test5_channel({'phone':e['phone'],'address':{'value':addr,'url':site,'read':TODAY} if addr else None,'form':{'value':'form','url':site,'read':TODAY} if re.search(r'<form',x[2],re.I) else None}); e['test5']=ch
        rv=re.search(r'\$\s?([\d.,]+)\s?(million|M|billion|B)\b(?=[^.]{0,40}(?:revenue|sales))',t,re.I); ceil=BANDS.get(pr,{'ceiling':25000000})['ceiling']
        if rv: fig=float(rv.group(1).replace(',',''))*(1e9 if rv.group(2).lower().startswith('b') else 1e6); e['band']={'in_band':fig<=ceil,'why':f'published revenue {fig:.0f} vs {ceil} ({site} \u00b7 read {TODAY})'}
        else: e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}
        if t1 and t5 and e['band']['in_band']: e['status']='admitted by test (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'; R['admitted_by_test'].append(k)
        elif t1 and t5: e['status']='passes tests 1, 2 and 5; published revenue not found \u2014 held size-unsourced, not admitted'
    try:
        # 1 · the 13, off the top, body re-reads charged to Acquisitions
        for k,e in [(k,e) for k,e in Q.items() if e['source']=='gnews_rss']:
            x=await rd('Acquisitions','gnews_rss:reread',e['signal']['url'])
            if x[0] is None: break
            if not x[0]: e['status']=f'article refused ({x[1]}) on re-read'; R['thirteen'].append({'key':k,'state':'refused'}); continue
            await name_and_test(k,e,x[2],'Acquisitions'); R['thirteen'].append({'key':k,'state':e['naming']['state'],'company':e.get('company'),'derivation':e['naming'].get('name_extraction'),'split':e['naming'].get('split')})
            json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 2 · Google News RSS widened, separate counted queries, round-robin by practice under the thirds
        seen={e.get('feed_title') for e in Q.values()}|{e['signal']['url'] for e in Q.values() if e.get('signal')}
        queues={pr:list(qs) for pr,qs in QP.items()}
        while any(queues.values()):
            for pr in ('Acquisitions','Private Equity','Fractionals'):
                if not queues[pr] or spent[pr]>=budget[pr]: queues[pr]=[] if spent[pr]>=budget[pr] else queues[pr]; continue
                q=queues[pr].pop(0); u='https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-US&gl=US&ceid=US:en'
                x=await rd(pr,'gnews_rss',u); fq={'practice':pr,'articles_read':0,'florida_signal':0,'reached_binding':0,'items':0,'refused':None}
                R['feed_quality'][q]=fq
                if x[0] is None: break
                if not x[0]: fq['refused']=str(x[1]); continue
                items=re.findall(r'<item>(.*?)</item>',x[2],re.S); fq['items']=len(items); kw=practice.KW[pr]; cand=[]
                for it in items:
                    ttl=html.unescape(re.sub(r'<[^>]+>','',(re.search(r'<title>(.*?)</title>',it,re.S) or [None,''])[1])).strip(); lk=re.search(r'<link>(.*?)</link>',it,re.S); lk=html.unescape(lk.group(1).strip()) if lk else ''; pd=(re.search(r'<pubDate>(.*?)</pubDate>',it,re.S) or [None,None])[1]
                    if ttl in seen or lk in seen: continue
                    if re.search(r'\bFlorida\b|\bFL\b|'+'|'.join(METROS),ttl) and re.search(kw,ttl,re.I): cand.append((ttl,lk,pd)); seen.add(ttl)
                for ttl,lk,pd in cand[:3]:
                    a=await rd(pr,'gnews_rss:article',lk)
                    if a[0] is None: break
                    if not a[0]: continue
                    fq['articles_read']+=1; body=a[2]; d,f=None,None
                    for nm,pt in (('JSON-LD datePublished',r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)'),('article:published_time',r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)'),('time[datetime]',r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)')):
                        mm=re.search(pt,body)
                        if mm: d,f=mm.group(1),nm; break
                    if not d and pd and re.match(r'\w{3}, \d{1,2} \w{3} \d{4}',pd.strip()): d=datetime.datetime.strptime(pd.strip()[:25],'%a, %d %b %Y %H:%M:%S').date().isoformat(); f='feed pubDate'
                    t=text_of(body); sent=next((s.strip() for s in re.split(r'(?<=[.!?])\s+',t) if re.search(kw,s,re.I) and re.search(r'\bFlorida\b|\bFL\b|'+'|'.join(METROS),s)),None)
                    if not (d and sent): continue
                    fq['florida_signal']+=1; fq['reached_binding']+=1
                    k=f'{pr}:gnews_rss_w4:{len([z for z in Q if z.startswith(pr+":gnews_rss_w4")])}'
                    Q[k]={'practice':pr,'source':'gnews_rss_w4','company':'','company_named':False,'signal':{'sentence':sent[:400],'url':lk,'published':d,'read':TODAY},'date_field':f,'feed_title':ttl,'query':q,'evidence_source':'signal','status':'proposed \u2014 unconfirmed','test1':None}
                    await name_and_test(k,Q[k],body,pr)
                json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 3 · the Source Directory's Florida section: answering sources probed once each (off the top); parked stay parked
        for nm,u in DIRECTORY:
            x=await rd('Directory probes','directory:'+nm[:20],u)
            if x[0] is None: R['directory'][nm]='not read: probe budget spent'; continue
            if not x[0]: R['directory'][nm]=f'refused ({x[1]}) \u2014 parked under its code'; continue
            t=text_of(x[2]); R['directory'][nm]={'answered':True,'bytes':len(x[2]),'named_companies_by_suffix':len(set(naming.SUFFIX.findall(t[:20000]))),'decision':'declared as a finder (not a practice signal); company sites and member listings are never signals'}
        R['directory_parked']=PARKED
        # PE third's remainder: H.I.G. entries by the Location field, Florida ones to their own site
        hig=[k for k,e in Q.items() if e['source']=='hig' and not e.get('entry_read') and e.get('sponsor_page')]; pe=collections.Counter()
        for k in hig:
            if spent['Private Equity']>=budget['Private Equity']: break
            e=Q[k]; x=await rd('Private Equity','entry:hig',e['sponsor_page'])
            if x[0] is None: break
            e['entry_read']=TODAY; pe['entries']+=1
            if not x[0]: continue
            t=text_of(x[2]); m=re.search(r'(?:Headquarters|Location|HQ)\s*[:\-]?\s*([A-Z][A-Za-z .\-]+,\s*(?:FL|Florida|[A-Z]{2}|[A-Z][a-z]+))',t); lf=m.group(1) if m else None; e['location_field']=lf
            if not (lf and re.search(r'\bFL\b|Florida',lf)): continue
            pe['florida']+=1; e['entry_location_fl']=True; site=discovery.site_link(x[2],e['company'])
            if not site: e['test1']='entry names no company site'; continue
            x2=await rd('Private Equity','test1:hig',site)
            if x2[0] is None: break
            if not x2[0]: e['test1']=f'company page refused ({x2[1]})'; continue
            e['company_url']=site; tt=text_of(x2[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
            ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':site,'read':TODAY} if ph else None,'address':{'value':addr,'url':site,'read':TODAY} if addr else None}); e['test5']=ch
            rv=re.search(r'\$\s?([\d.,]+)\s?(million|M|billion|B)\b(?=[^.]{0,40}(?:revenue|sales))',tt,re.I)
            e['band']={'in_band':(float(rv.group(1).replace(',',''))*(1e9 if rv.group(2).lower().startswith('b') else 1e6))<=1e8,'why':'published revenue on own site'} if rv else {'in_band':None,'why':intake.SIZE_UNSOURCED}
            if t1: pe['test1_pass']+=1
            if t1 and t5 and e['band']['in_band']: e['status']='admitted by test (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'; R['admitted_by_test'].append(k)
            elif t1 and t5: e['status']='passes tests 1, 2 and 5; published revenue not found \u2014 held size-unsourced, not admitted'
        R['pe']=dict(pe); R['stopped']='completed: the order ran to its end within the ceiling'
    except Stop as s: R['stopped']='NAMING STOP FIRED: '+str(s)
    except (bot.Refused,bot.Halted) as e: R['stopped']='ceiling or kill switch: '+str(e)
    R['spent']=dict(spent); R['naming']['split']=dict(R['naming']['split']); R['test1']=dict(R['test1']); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/w4-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',json.dumps({k:R[k] for k in ('stopped','naming','spent','admitted_by_test')}))
    await b.close(); await p.stop()
asyncio.run(go())
