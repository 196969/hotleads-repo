import asyncio,json,re,html,datetime,collections,urllib.parse,hashlib,os
import bot,discovery,practice,intake,naming,naming2
TODAY=discovery.TODAY
METROS=['Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala']
INDUSTRIES=['manufacturing','distribution','food and beverage','construction','transportation logistics','multi-site retail','field services','events','sales organization','marketing agency']
QP={'Acquisitions':[f'"Florida" {w}' for w in ('company acquired','acquisition','"sold to"','"CEO retiring"','succession family business')]+[f'"{m}" company acquired' for m in METROS]+[f'Florida {i} company acquired' for i in INDUSTRIES],
    'Private Equity':['"Florida" "private equity" invests','"Florida" "portfolio company"','"Florida" "private equity" acquires']+[f'"{m}" "private equity"' for m in METROS[:5]],
    'Fractionals':['"Florida" company "names" CFO','"Florida" "chief financial officer" appointed']+[f'"{m}" company names CFO' for m in METROS[:5]]}
R={'window':6,'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'disc':{'articles_read':0,'florida_signal':0,'reaching_binding':0,'no_site_linked':0},'per_query':{},'thirteen':[],'counts':collections.Counter(),'parked':{},'directory':{},'pe':collections.Counter(),'admitted_by_test':[],'decisions':[],'stopped':None,'rows':{}}
class Stop(Exception): pass
def check():
    c=R['counts']; p=c['processed']
    if c['wrong']>3 or (p>=10 and c['wrong']/p>0.2): raise Stop(f"WRONGNESS STOP: {c['wrong']} binds whose found site does not name them, of {p} processed")
    if c['unbound']>3 or (p>=10 and c['unbound']/p>0.2): raise Stop(f"UNBOUND STOP: {c['unbound']} unbound of {p} processed")
def T(b): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',b or '',flags=re.S|re.I))))
def pubdate(b):
    for nm,pt in (('JSON-LD datePublished',r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)'),('article:published_time',r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)'),('time[datetime]',r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)')):
        m=re.search(pt,b or '')
        if m: return m.group(1),nm
    return None,None
def site_for_name(body,company):
    """Builder decision (window six): a site is found FOR the bound name only when the link's host carries a 4+ letter token of the name, or its anchor
    text carries the name's first token; a generic 'website' link is not taken, because on an acquisition article it is as likely the acquirer's."""
    toks=[w.lower() for w in re.findall(r'[A-Za-z]{4,}',company) if w.lower() not in ('company','group','holdings','industries','florida','construction','services')]
    deny=('linkedin','twitter','facebook','youtube','instagram','google','news','prnewswire','businesswire','globenewswire','bizjournals','wp.com','gravatar','x.com')
    for m in re.finditer(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',body,re.S|re.I):
        u=m.group(1); host=re.sub(r'^https?://(www\.)?','',u).split('/')[0].lower(); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()
        if any(d in host for d in deny): continue
        if toks and (any(t in host.replace('-','') for t in toks) or toks[0] in txt): return 'https://'+host+'/'
    return None
async def go():
    read,b,p=await discovery.browser_reader(); day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Acquisitions':64,'Private Equity':64,'Fractionals':64,'Directory probes':8}
    for k in budget: day.spent[k]=0
    consec=collections.Counter()
    async def rd(pr,src,url,pk):
        if pk in R['parked']: return None,'parked',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,src,url); spent[pr]+=1
        if r[0] is False:
            consec[pk]+=1
            if consec[pk]>=3: R['parked'][pk]=f'parked for the window: 3 consecutive refusals (last {r[1]})'
        elif r[0]: consec[pk]=0
        if r[0]: open(f'w6-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')   # read and filed before anything is deleted
        return r
    async def settle(k,e,body,pr):
        """naming v2 on the fetched article; a bind is provisional until the site proves it."""
        res=naming2.name2(e.get('feed_title') or '',T(body)); e['naming']=res; R['counts']['processed']+=1; st=res['state']
        if st.startswith('rejected'): R['counts']['rejected']+=1; e['status']='rejected: the matched span is not a company \u2014 '+res.get('span_taken',''); return
        if st=='bind disputed': R['counts']['disputed']+=1; e['status']='bind disputed \u2014 held, not resolved by the builder'; return
        if st=='unbound': R['counts']['unbound']+=1; R['counts']['unbound:'+res['split'][:20]]+=1; e['status']='unbound \u2014 detector result on the row'; check(); return
        co=res['company']; e.update(company=co,company_named='provisional until the site proves it',acquirer=res.get('acquirer'),city=res.get('city'))
        ok2,why2=intake.test2_absent(co,None,day.idx); e['test2']=why2
        if not ok2: e['status']='on file \u2014 a signal against the existing row'; return
        site=site_for_name(body,co)
        if not site: R['disc']['no_site_linked']+=1; e['status']='unprovable-by-link, held: the article links no site for the bound name'; return
        r=await rd(pr,'site:'+e['source'],site,'site')
        if r[0] is None: e['status']='site not read: '+str(r[1]); return
        if not r[0]: e['status']=f'site refused ({r[1]}) \u2014 re-runnable'; R['counts']['site_refused']+=1; return
        pf=naming2.prove_site2(r[2],co); e['site']=site; e['site_proof']=pf
        if not pf: R['counts']['wrong']+=1; e['status']='WRONG BIND: the site found for the name does not name the company'; e['company_named']=False; check(); return
        R['counts']['proved']+=1; e['company_named']=True
        if pf.get('construction') in ('formerly','d/b/a'): e['current_name']=pf['current_name']
        tt=T(r[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
        ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); em=[z for z in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',tt) if not re.search(r'\.(png|jpg|svg|webp)$',z)]
        e['phone']={'value':ph.group(0),'url':site,'read':TODAY} if ph else None; e['email']={'value':em[0],'url':site,'read':TODAY,'role_inbox':bool(re.match(r'^(info|sales|contact|hello|office|admin|support)',em[0].split('@')[0],re.I))} if em else None
        t5,ch=intake.test5_channel({'phone':e['phone'],'address':{'value':addr,'url':site,'read':TODAY} if addr else None,'form':{'value':'form','url':site,'read':TODAY} if re.search(r'<form',r[2],re.I) else None}); e['test5']=ch
        ceil=1e8 if pr=='Private Equity' else 25e6; m=re.search(r'\$\s?([\d.,]+)\s?(million|billion)\b[^.]{0,60}(?:revenue|sales)|(?:revenue|sales)[^.]{0,60}\$\s?([\d.,]+)\s?(million|billion)',tt,re.I)
        if m: v=float((m.group(1) or m.group(3)).replace(',',''))*(1e9 if (m.group(2) or m.group(4)).lower()=='billion' else 1e6); e['band']={'in_band':v<=ceil,'why':f'published revenue {v:.0f} vs {ceil:.0f} (Src: {site} \u00b7 read {TODAY})'}
        else: e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}
        if not t1: e['status']='site proved; test 1 failed: '+why
        elif t1 and t5 and e['band']['in_band']: e['status']='ADMITTED BY TEST (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'; R['admitted_by_test'].append(k)
        elif t1 and t5: e['status']='site proved; passes tests 1, 2 and 5; held size-unsourced'
        else: e['status']='site proved; passes test 1; no reachable channel published (test 5)'
    try:
        # 2 · the 13 re-bound, site proof enforced
        for k,e in [(k,e) for k,e in Q.items() if e['source']=='gnews_rss']:
            r=await rd('Acquisitions','gnews_rss:reread',e['signal']['url'],'gnews_rss')
            if r[0] is None: break
            if not r[0]: R['thirteen'].append({'key':k,'state':f'refused ({r[1]})'}); continue
            R['disc']['articles_read']+=1; R['disc']['florida_signal']+=1; R['disc']['reaching_binding']+=1
            await settle(k,e,r[2],'Acquisitions'); R['thirteen'].append({'key':k,'headline':e.get('feed_title'),'state':e['naming']['state'],'bound':e.get('company') or e['naming'].get('span_taken'),'pattern':(e['naming'].get('name_extraction') or {}).get('pattern'),'span':(e['naming'].get('name_extraction') or {}).get('span'),'status':e.get('status'),'site':e.get('site'),'proof':e.get('site_proof')})
            json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 3 · Google News on the widened queries
        seen={e.get('feed_title') for e in Q.values()}; queues={pr:list(q) for pr,q in QP.items()}
        while any(queues.values()) and 'gnews_rss' not in R['parked']:
            for pr in ('Acquisitions','Private Equity','Fractionals'):
                if not queues[pr] or 'gnews_rss' in R['parked']: continue
                q=queues[pr].pop(0); r=await rd(pr,'gnews_rss','https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-US&gl=US&ceid=US:en','gnews_rss')
                pq=R['per_query'][q]={'practice':pr,'articles_read':0,'florida_signal':0,'reaching_binding':0,'no_site_linked':0}
                if r[0] is None:
                    if r[1]=='budget': queues[pr]=[]
                    continue
                if not r[0]: pq['refused']=str(r[1]); continue
                n=0
                for it in re.findall(r'<item>(.*?)</item>',r[2],re.S):
                    ttl=html.unescape(re.sub(r'<[^>]+>','',(re.search(r'<title>(.*?)</title>',it,re.S) or [None,''])[1])); lk=html.unescape((re.search(r'<link>(.*?)</link>',it,re.S) or [None,''])[1].strip())
                    if ttl in seen or n>=2 or not (re.search(r'\bFlorida\b|\bFL\b|'+'|'.join(METROS),ttl) and re.search(practice.KW[pr],ttl,re.I)): continue
                    seen.add(ttl); n+=1; a=await rd(pr,'gnews_rss:article',lk,'gnews_rss')
                    if not a[0]: continue
                    R['disc']['articles_read']+=1; pq['articles_read']+=1; d,f=pubdate(a[2]); t=T(a[2]); sent=next((s for s in re.split(r'(?<=[.!?])\s+',t) if re.search(practice.KW[pr],s,re.I) and re.search(r'\bFlorida\b|'+'|'.join(METROS),s)),None)
                    if not (d and sent): continue
                    R['disc']['florida_signal']+=1; R['disc']['reaching_binding']+=1; pq['florida_signal']+=1; pq['reaching_binding']+=1
                    k=f'{pr}:gnews_rss_w6:{len(Q)}'; Q[k]={'practice':pr,'source':'gnews_rss_w6','company':'','signal':{'sentence':sent[:400],'url':lk,'published':d,'read':TODAY},'date_field':f,'feed_title':ttl,'query':q,'evidence_source':'signal','status':'proposed \u2014 unconfirmed'}
                    before=R['disc']['no_site_linked']; await settle(k,Q[k],a[2],pr); pq['no_site_linked']+=R['disc']['no_site_linked']-before
                json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 4 · the Source Directory's remainder
        for nm,u in (('Florida Restaurant and Lodging Association','https://www.frla.org'),('AGC chapters','https://www.agc.org/chapters')):
            r=await rd('Directory probes','directory',u,'directory:'+nm); R['directory'][nm]=('answered \u2014 declared as a finder; produces no candidates' if r[0] else f'refused ({r[1]}) \u2014 parked under its code') if r[0] is not None else 'not read'
        rel=sum(max(0,budget[x]-spent[x]) for x in ('Acquisitions','Fractionals')); budget['Private Equity']+=rel; R['decisions'].append(f'addition 5: {rel} unspent Acquisitions and Fractionals reads released to Private Equity after Google News was read or parked')
        for k in [k for k,e in Q.items() if (e['source']=='suncap' and e.get('florida_on_card') and not e.get('site_proof')) or (e['source']=='hig' and not e.get('entry_read') and e.get('sponsor_page'))]:
            e=Q[k]; r=await rd('Private Equity','entry:'+e['source'],e['sponsor_page'],'entry:'+e['source'])
            if r[0] is None: break
            e['entry_read']=TODAY; R['pe']['entries']+=1
            if not r[0]: continue
            t=T(r[2])
            if e['source']=='hig':
                m=re.search(r'(?:Headquarters|Location|HQ)\s*[:\-]?\s*([A-Z][A-Za-z .\-]+,\s*(?:FL|Florida|[A-Z]{2}|[A-Z][a-z]+))',t); lf=m.group(1) if m else None; e['location_field']=lf
                if not (lf and re.search(r'\bFL\b|Florida',lf)): continue
            R['pe']['florida']+=1; site=discovery.site_link(r[2],e['company'])
            if not site: e['status']='unprovable-by-link, held: the sponsor entry names no company site'; R['disc']['no_site_linked']+=1; continue
            r2=await rd('Private Equity','site:'+e['source'],site,'site')
            if r2[0] is None: break
            if not r2[0]: e['status']=f'site refused ({r2[1]})'; continue
            pf=naming2.prove_site2(r2[2],e['company']); e['site']=site; e['site_proof']=pf
            if not pf: e['status']='site not proved \u2014 the sponsor\u2019s link does not name the company (no Florida finding)'; R['pe']['not_proved']+=1; continue
            if pf.get('construction') in ('formerly','d/b/a'): e['current_name']=pf['current_name']
            tt=T(r2[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
            ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':site,'read':TODAY} if ph else None,'address':{'value':addr,'url':site,'read':TODAY} if addr else None}); e['test5']=ch
            e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}
            if t1: R['pe']['test1_pass']+=1; e['status']='site proved; passes tests 1, 2'+(' and 5' if t5 else '')+'; held size-unsourced'
            else: e['status']='site proved; test 1 failed: '+why
        R['stopped']='completed'
    except Stop as s: R['stopped']=str(s)
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    R['spent']=dict(spent); R['budget']=budget; R['counts']=dict(R['counts']); R['pe']=dict(R['pe']); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/w6-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],R['counts'],dict(spent))
    await b.close(); await p.stop()
asyncio.run(go())
