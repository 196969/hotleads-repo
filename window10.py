import naming6
import asyncio,json,re,html,datetime,collections,urllib.parse,hashlib,os
import bot,discovery,practice,intake,naming,naming4,naming5,naming6
TODAY=discovery.TODAY
METROS=['Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala']
INDUSTRIES=['manufacturing','distribution','food and beverage','construction','transportation logistics','multi-site retail','field services','events','sales organization','marketing agency']
QP={'Acquisitions':[f'"Florida" {w}' for w in ('company acquired','acquisition','"sold to"','"CEO retiring"','succession family business')]+[f'"{m}" company acquired' for m in METROS]+[f'Florida {i} company acquired' for i in INDUSTRIES],
    'Private Equity':['"Florida" "private equity" invests','"Florida" "portfolio company"','"Florida" "private equity" acquires']+[f'"{m}" "private equity"' for m in METROS[:5]],
    'Fractionals':['"Florida" company "names" CFO','"Florida" "chief financial officer" appointed']+[f'"{m}" company names CFO' for m in METROS[:5]]}
R={'window':10,'queue_halts':[],'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revenue':{},'memorial':None,'disc':{'articles_read':0,'florida_signal':0,'reaching_binding':0,'site_by_article_link':0,'site_by_derived_host':0,'no_site_by_any_route':0,'precondition_stopped':0},'routes':[],'per_query':{},'counts':collections.Counter(),'parked':{},'directory':{},'pe':collections.Counter(),'admitted_by_test':[],'decisions':[],'stopped':None}
class Stop(Exception): pass
def check():
    c=R['counts']; p=c['processed']
    if c['wrong']>3 or (p>=10 and c['wrong']/p>0.2): raise Stop(f"WRONGNESS STOP: {c['wrong']} article-linked hosts failed the proof, of {p} processed")
    if c['unbound']>3 or (p>=10 and c['unbound']/p>0.2): raise Stop(f"UNBOUND STOP: {c['unbound']} unbound of {p} processed")
def T(b): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',b or '',flags=re.S|re.I))))
def pubdate(b):
    for nm,pt in (('JSON-LD datePublished',r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)'),('article:published_time',r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)'),('time[datetime]',r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)')):
        m=re.search(pt,b or '')
        if m: return m.group(1),nm
    return None,None
DEAL=re.compile(r'(?i)acquir|\bdeal\b|transaction|valued|purchase price|funding|raised|investment of|\bloan\b|contract|grant|expansion|bond')
def rev_sent(text,toks):
    for s in re.split(r'(?<=[.!?])\s+',text):
        low=s.lower()
        if not all(t in low for t in toks): continue
        m=re.search(r'\$\s?([\d.,]+)\s?(million|billion)',s,re.I)
        if m and re.search(r'(?i)\b(?:revenue|revenues|annual sales|in sales|sales of)\b',s) and not DEAL.search(s): return float(m.group(1).replace(',',''))*(1e9 if m.group(2).lower()=='billion' else 1e6),s.strip()[:300]
    return None,None
def emp_sent(text,toks):
    for s in re.split(r'(?<=[.!?])\s+',text):
        if all(t in s.lower() for t in toks):
            m=re.search(r'\b(\d[\d,]{0,6})\+? (?:employees|workers|team members|staff)\b',s,re.I)
            if m: return m.group(1),s.strip()[:300]
    return None,None
def gnews(q): return 'https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-US&gl=US&ceid=US:en'
async def go():
    read,b,p=await discovery.browser_reader(); day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Acquisitions':55,'Private Equity':70,'Fractionals':55,'Directory probes':8,'Ownership':1}
    for k in budget: day.spent[k]=0
    consec=collections.Counter()
    async def rd(pr,src,url,pk):
        if pk in R['parked']: return None,'parked',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,src,url); spent[pr]+=1
        if r[0] is False:
            consec[pk]+=1
            if consec[pk]>=3: R['parked'][pk]=f'parked for the window: 3 consecutive refusals (last {r[1]})'
        elif r[0]: consec[pk]=0; open(f'w10-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')
        return r
    async def run_route(subj,label,url,pk,own,toks):
        out=R['revenue'][subj]
        r=await rd('Revenue class','revenue:'+label[:24],url,pk)
        if r[0] is None: out['routes'].append({'route':label,'result':'not read: '+str(r[1])}); return
        if not r[0]: out['routes'].append({'route':label,'result':f'refused ({r[1]}) \u2014 re-runnable'}); return
        body=r[2]
        if 'wikipedia' in url:
            hit='mw-search-results' not in body; m=re.search(r'Revenue\s*[^$]{0,40}(?:US)?\$\s?([\d.,]+)\s?(million|billion)',T(body)) if hit else None
            if m: out['figure']={'value':float(m.group(1).replace(',',''))*(1e9 if m.group(2)=='billion' else 1e6),'span':m.group(0),'url':'en.wikipedia.org search: '+subj,'read':TODAY,'source':'Wikipedia infobox'}
            out['routes'].append({'route':label,'result':'figure found' if m else ('no article matched \u2014 not a size reading' if not hit else 'article read; no revenue figure')}); return
        links=[html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',body)][1:3] if 'news.google' in url else list(dict.fromkeys(re.findall(r'href="(https?://(?:www\.)?floridatrend\.com/article/\d+/[^"]*)"',body)))[:2]
        got='no item for the name \u2014 not a size reading'
        for u in links:
            if own and own in u: continue
            r2=await rd('Revenue class','revenue:article',u,pk)
            if not r2[0]: continue
            t=T(r2[2]); fig,s=rev_sent(t,toks); ne,es=emp_sent(t,toks); d,f=pubdate(r2[2])
            if ne and not out['employees']: out['employees']={'value':ne,'span':es,'url':u,'read':TODAY,'flag':'employee count \u2014 recorded, not a size reading (revenue only)'}
            if fig: out['figure']={'value':fig,'span':s,'url':u,'read':TODAY,'published':d,'source':'trade press'}; got='figure found'; break
            got='article(s) read; no sentence naming the company with a revenue figure (deal values excluded)'
        out['routes'].append({'route':label,'result':got})
    try:
        done=set(json.load(open('reports/w9-engine.json'))['per_query'])
        # 4-5 · the precondition (proved before this pass) applied, then the queries
        seen={e.get('feed_title') for e in Q.values()}; queues={pr:[x for x in q if x not in done] for pr,q in QP.items()}
        try:
         while any(queues.values()) and 'gnews_rss' not in R['parked']:
             for pr in ('Acquisitions','Private Equity','Fractionals'):
                 if not queues[pr]: continue
                 q=queues[pr].pop(0); r=await rd(pr,'gnews_rss',gnews(q),'gnews_rss'); pq=R['per_query'][q]={'practice':pr,'articles_read':0,'florida_signal':0,'reaching_binding':0,'precondition_stopped':0}
                 if r[0] is None:
                     if r[1]=='budget': queues[pr]=[]
                     continue
                 if not r[0]: pq['refused']=str(r[1]); continue
                 n=0
                 for it in re.findall(r'<item>(.*?)</item>',r[2],re.S):
                     ttl=html.unescape(re.sub(r'<[^>]+>','',(re.search(r'<title>(.*?)</title>',it,re.S) or [None,''])[1])); lk=html.unescape((re.search(r'<link>(.*?)</link>',it,re.S) or [None,''])[1].strip())
                     if ttl in seen or n>=2 or not (re.search(r'\bFlorida\b|\bFL\b|'+'|'.join(METROS),ttl) and re.search(practice.KW[pr],ttl,re.I)): continue
                     seen.add(ttl); ok,span=naming5.precondition(ttl)
                     if not ok: pq['precondition_stopped']+=1; R['disc']['precondition_stopped']+=1; continue
                     n+=1; a=await rd(pr,'gnews_rss:article',lk,'gnews_rss')
                     if not a[0]: continue
                     R['disc']['articles_read']+=1; pq['articles_read']+=1; d,f=pubdate(a[2]); t=T(a[2]); sent=next((s for s in re.split(r'(?<=[.!?])\s+',t) if re.search(practice.KW[pr],s,re.I) and re.search(r'\bFlorida\b|'+'|'.join(METROS),s)),None)
                     if not (d and sent): continue
                     R['disc']['florida_signal']+=1; R['disc']['reaching_binding']+=1; pq['florida_signal']+=1; pq['reaching_binding']+=1
                     k=f'{pr}:gnews_rss_w10:{len(Q)}'; e=Q[k]={'practice':pr,'source':'gnews_rss_w10','company':'','signal':{'sentence':sent[:400],'url':lk,'published':d,'read':TODAY},'date_field':f,'feed_title':ttl,'query':q,'precondition_span':span,'evidence_source':'signal','status':'proposed \u2014 unconfirmed'}
                     res=naming4.name4(ttl,a[2]); e['naming']=res; R['counts']['processed']+=1; st=res['state']
                     if st.startswith('rejected'): R['counts']['rejected']+=1; e['status']='rejected: span not a company \u2014 '+res.get('span_taken',''); continue
                     if st=='bind disputed': R['counts']['disputed']+=1; e['status']='bind disputed \u2014 held'; continue
                     if st=='unbound': R['counts']['unbound']+=1; R['counts']['unbound:'+res['split'][:20]]+=1; e['status']='unbound'; check(); continue
                     co=res['company']; e.update(company=co,company_named='provisional until the site proves it',acquirer=res.get('acquirer'),city=res.get('city'))
                     ok2,why2=intake.test2_absent(co,None,day.idx); e['test2']=why2
                     if not ok2: e['status']='on file \u2014 a signal against the existing row'; continue
                     toks=[w.lower() for w in re.findall(r'[A-Za-z]{4,}',co) if w.lower() not in ('company','group','holdings','industries','florida','construction','services')]; cands=[]; tried=[]
                     for m in re.finditer(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',a[2],re.S|re.I):
                         host=re.sub(r'^https?://(www\.)?','',m.group(1)).split('/')[0].lower(); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()
                         if toks and (any(tk in host.replace('-','') for tk in toks) or toks[0] in txt) and 'news.google' not in host: cands.append(('article link','https://'+host+'/')); break
                     for h in naming4.derived_hosts(co): cands.append(('derived host','https://www.'+h+'/'))
                     site=page=pf=route=None
                     for rt,url in cands:
                         s2=await rd(pr,'site:'+rt,url,'site:'+url)
                         if s2[0] is None: tried.append({'route':rt,'host':url,'outcome':'not read: '+str(s2[1])}); continue
                         if s2[0] is False: tried.append({'route':rt,'host':url,'outcome':'did not resolve' if str(s2[1]) in ('net','timeout') else f'refused ({s2[1]})'}); continue
                         pf=naming5.prove_site5(s2[2],co)
                         if not pf:
                             tried.append({'route':rt,'host':url,'outcome':'resolved but failed the proof'})
                             if rt=='article link': R['counts']['wrong']+=1; check()
                             continue
                         tried.append({'route':rt,'host':url,'outcome':'proved'}); site,page,route=url,s2[2],rt; break
                     e['routes_tried']=tried; R['routes'].append({'company':co,'tried':tried})
                     if not site: R['disc']['no_site_by_any_route']+=1; e['status']='no site found by any route (routes on the row) \u2014 held; a fact about the guesses'; continue
                     R['disc']['site_by_article_link' if route=='article link' else 'site_by_derived_host']+=1; e.update(site=site,site_route=route,site_proof=pf,company_named=True)
                     if pf.get('construction') in ('formerly','d/b/a'): e['current_name']=pf['current_name']
                     tt=T(page); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
                     ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':site,'read':TODAY} if ph else None,'address':{'value':addr,'url':site,'read':TODAY} if addr else None}); e['test5']=ch
                     e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}
                     e['status']=('site proved ('+route+'); passes tests 1, 2 and 5; held size-unsourced') if (t1 and t5) else ('site proved ('+route+'); '+('test 5: no channel' if t1 else 'test 1 failed: '+why))
                 json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        except Stop as st_:
            R['queue_halts'].append({'queue':'Google News discovery','reason':str(st_),'continued_with':'the Source Directory remainder'}); json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # the Source Directory's remainder
        for nm,u in (('Florida Restaurant and Lodging Association','https://www.frla.org'),('AGC chapters','https://www.agc.org/chapters')):
            r=await rd('Directory probes','directory',u,'directory:'+nm); R['directory'][nm]=('answered \u2014 declared as a finder; no candidates' if r[0] else f'refused ({r[1]}) \u2014 parked under its code') if r[0] is not None else 'not read'
        for k in [k for k,e in Q.items() if e['source']=='hig' and not e.get('entry_read') and e.get('sponsor_page')]:
            e=Q[k]; r=await rd('Private Equity','entry:hig',e['sponsor_page'],'entry:hig')
            if r[0] is None: break
            e['entry_read']=TODAY; R['pe']['entries']+=1
            if not r[0]: continue
            t=T(r[2]); m=re.search(r'(?:Headquarters|Location|HQ)\s*[:\-]?\s*([A-Z][A-Za-z .\-]+,\s*(?:FL|Florida|[A-Z]{2}|[A-Z][a-z]+))',t); lf=m.group(1) if m else None; e['location_field']=lf
            if not (lf and re.search(r'\bFL\b|Florida',lf)): continue
            R['pe']['florida']+=1; link=discovery.site_link(r[2],e['company']); tried=[]; site=page=pf=None
            for rt,url in ([('sponsor entry link',link)] if link else [])+[('derived host','https://www.'+h+'/') for h in naming4.derived_hosts(e['company'])]:
                s2=await rd('Private Equity','site:'+rt,url,'site:'+url)
                if s2[0] is None: tried.append({'route':rt,'host':url,'outcome':'not read'}); continue
                if s2[0] is False: tried.append({'route':rt,'host':url,'outcome':'did not resolve' if str(s2[1]) in ('net','timeout') else f'refused ({s2[1]})'}); continue
                pf=naming5.prove_site5(s2[2],e['company'])
                if not pf: tried.append({'route':rt,'host':url,'outcome':'resolved but failed the proof'}); continue
                tried.append({'route':rt,'host':url,'outcome':'proved'}); site,page=url,s2[2]; break
            e['routes_tried']=tried
            if not site: e['status']='no site found by any route \u2014 held'; R['pe']['no_site']+=1; continue
            e['site']=site; e['site_proof']=pf; tt=T(page); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
            ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':site,'read':TODAY} if ph else None,'address':{'value':addr,'url':site,'read':TODAY} if addr else None}); e['test5']=ch; e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}
            if t1: R['pe']['test1_pass']+=1; e['status']='site proved; passes tests 1, 2'+(' and 5' if t5 else '')+'; held size-unsourced'
        mk=next((k for k,e in Q.items() if e.get('company')=='Memorial Healthcare System'),None)
        if mk:
            e=Q[mk]; r=await rd('Ownership','ownership:memorial','https://en.wikipedia.org/w/index.php?search='+urllib.parse.quote('"Memorial Healthcare System"')+'&title=Special:Search&go=Go','wikipedia')
            if r[0]:
                t=T(r[2]); m=re.search(r'[^.]{0,160}\b(South Broward Hospital District|special taxing district|public health system|public hospital|taxing district|independent special district)\b[^.]{0,160}',t,re.I)
                R['memorial']={'route':'Wikipedia search (third-party; the home page read in window nine states no ownership form)','read':TODAY,'finding':m.group(0).strip() if m else None,'reading':'public or district ownership stated \u2014 the Chair\u2019s conditional retirement confirmed' if m else ('no article matched \u2014 unresolved' if 'mw-search-results' in r[2] else 'article read; no ownership form stated \u2014 unresolved')}
                if m: e['status']='RETIRED (practice fit, the Chair\u2019s judgement at tests 3 and 4): public hospital district \u2014 confirmed by a third-party read \u00b7 '+TODAY; e['retired']={'reason':'practice fit: a public hospital district has no owner to sell, no equity, no fractional seat (Chair\u2019s judgement; confirmed by read)','date':TODAY,'user':'Timothy A. Edick'}
            else: R['memorial']={'reading':f'refused ({r[1]}) \u2014 unresolved'}
        R['stopped']='completed'
    except Stop as s: R['stopped']=str(s)
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    R['spent']=dict(spent); R['budget']=budget; R['counts']=dict(R['counts']); R['pe']=dict(R['pe']); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/w10-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],R['counts'],dict(spent))
    await b.close(); await p.stop()
asyncio.run(go())
