import asyncio,json,re,html,datetime,collections,urllib.parse,hashlib,os
import bot,discovery,practice,intake,naming,naming4,naming5
TODAY=discovery.TODAY
METROS=['Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala']
INDUSTRIES=['manufacturing','distribution','food and beverage','construction','transportation logistics','multi-site retail','field services','events','sales organization','marketing agency']
QP={'Acquisitions':[f'"Florida" {w}' for w in ('company acquired','acquisition','"sold to"','"CEO retiring"','succession family business')]+[f'"{m}" company acquired' for m in METROS]+[f'Florida {i} company acquired' for i in INDUSTRIES],
    'Private Equity':['"Florida" "private equity" invests','"Florida" "portfolio company"','"Florida" "private equity" acquires']+[f'"{m}" "private equity"' for m in METROS[:5]],
    'Fractionals':['"Florida" company "names" CFO','"Florida" "chief financial officer" appointed']+[f'"{m}" company names CFO' for m in METROS[:5]]}
R={'window':9,'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revenue':{},'memorial':None,'disc':{'articles_read':0,'florida_signal':0,'reaching_binding':0,'site_by_article_link':0,'site_by_derived_host':0,'no_site_by_any_route':0,'precondition_stopped':0},'routes':[],'per_query':{},'counts':collections.Counter(),'parked':{},'directory':{},'pe':collections.Counter(),'admitted_by_test':[],'decisions':[],'stopped':None}
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
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Revenue class':60,'Acquisitions':40,'Private Equity':50,'Fractionals':40,'Directory probes':8}
    for k in budget: day.spent[k]=0
    consec=collections.Counter()
    async def rd(pr,src,url,pk):
        if pk in R['parked']: return None,'parked',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,src,url); spent[pr]+=1
        if r[0] is False:
            consec[pk]+=1
            if consec[pk]>=3: R['parked'][pk]=f'parked for the window: 3 consecutive refusals (last {r[1]})'
        elif r[0]: consec[pk]=0; open(f'w9-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')
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
        # 1-2 · the revenue class: reserves per subject before any second read; American Fasteners' full routes first
        subj={e['company']:(k,e) for k,e in Q.items() if e.get('company') in ('Health Network One','Mainline','Moneysolver','American Fasteners','Alpha Foundations') and (e.get('test1_pass') or e.get('site_route'))}
        plans={}
        af='American Fasteners'
        plans[af]=[('Wikipedia search',f'https://en.wikipedia.org/w/index.php?search={urllib.parse.quote(chr(34)+af+chr(34))}&title=Special:Search&go=Go','wikipedia'),('Florida Trend search','https://www.floridatrend.com/search?q='+urllib.parse.quote('"'+af+'"'),'floridatrend:search'),('Google News: name + revenue',gnews(f'"{af}" revenue'),'gnews_rss'),('Google News: name + employees',gnews(f'"{af}" employees'),'gnews_rss'),('Google News: name + "annual sales"',gnews(f'"{af}" "annual sales"'),'gnews_rss'),('Google News: name + growth',gnews(f'"{af}" growth'),'gnews_rss'),('Google News: name + "Inc. 5000" (press mention)',gnews(f'"{af}" "Inc. 5000"'),'gnews_rss')]
        plans['Health Network One']=[('Google News: current name "Emboss Specialty" + revenue',gnews('"Emboss Specialty" revenue'),'gnews_rss'),('Wikipedia search: current name',f'https://en.wikipedia.org/w/index.php?search={urllib.parse.quote(chr(34)+"Emboss Specialty"+chr(34))}&title=Special:Search&go=Go','wikipedia'),('Google News: name + "Inc. 5000" (press mention)',gnews('"Health Network One" "Inc. 5000"'),'gnews_rss')]
        plans['Mainline']=[('Google News: full name "Mainline Information Systems" + revenue',gnews('"Mainline Information Systems" revenue'),'gnews_rss'),('Google News: full name + "Inc. 5000" (press mention)',gnews('"Mainline Information Systems" "Inc. 5000"'),'gnews_rss'),('Florida Trend search: full name','https://www.floridatrend.com/search?q='+urllib.parse.quote('"Mainline Information Systems"'),'floridatrend:search')]
        plans['Moneysolver']=[('Google News: name + "Inc. 5000" (press mention)',gnews('"MoneySolver" "Inc. 5000"'),'gnews_rss'),('Google News: name + "debt relief" revenue',gnews('"MoneySolver" "debt relief" revenue'),'gnews_rss')]
        plans['Alpha Foundations']=[('Google News: name + "Inc. 5000" (press mention)',gnews('"Alpha Foundations" "Inc. 5000"'),'gnews_rss'),('Google News: acquirer press (Groundworks) + revenue',gnews('Groundworks "Alpha Foundations" revenue'),'gnews_rss')]
        order=[af]+[s for s in ('Health Network One','Mainline','Moneysolver','Alpha Foundations') if s in subj]
        for s in order:
            k,e=subj[s]; R['revenue'][s]={'routes':[{'route':'Inc. 5000 list','result':'parked under its code (403 \u00d73, window five) \u2014 not read; no size reading'}] if s==af else [],'figure':None,'employees':None,'carried_routes_from_earlier_windows':'recorded in windows five and eight' if s!=af else None}
        # reserve: American Fasteners' full set, then one route per other subject, then the rest in order
        rounds=[[(af,x) for x in plans[af]]]+[[(s,plans[s][i]) for s in order[1:] if i<len(plans[s])] for i in range(3)]
        for rnd in rounds:
            for s,(label,url,pk) in rnd:
                if R['revenue'][s]['figure']: continue
                k,e=subj[s]; own=((e.get('site') or e.get('company_url') or '').split('/')+['','',''])[2]; nm=s if s!='Mainline' or 'full name' not in label else 'Mainline Information Systems'
                toks=[w.lower() for w in re.findall(r'[A-Za-z]{3,}',('Emboss Specialty' if 'Emboss' in label else nm))][:2]
                await run_route(s,label,url,pk,own,toks)
        for s in order:
            k,e=subj[s]; out=R['revenue'][s]
            if out['figure']:
                ceil=1e8 if e['practice']=='Private Equity' else 25e6; v=out['figure']['value']; e['band']={'in_band':v<=ceil,'why':f"published revenue {v:.0f} vs {ceil:.0f} (Src: {out['figure']['url']} \u00b7 read {TODAY})",'figure':out['figure']}
                if v<=ceil: e['status']='ADMITTED BY TEST (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'; R['admitted_by_test'].append(k)
                else: e['status']='band-rejected at test 1: published revenue above the ceiling'
            if out['employees']: e['employees_published']=out['employees']
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # 3 · Memorial Healthcare System: one ownership read (its own page, which states what it is)
        mk=next((k for k,e in Q.items() if e.get('company')=='Memorial Healthcare System'),None)
        if mk:
            e=Q[mk]; r=await rd('Fractionals','ownership:memorial',e.get('site') or 'https://mhs.net/','ownership')
            if r[0]:
                t=T(r[2]); m=re.search(r'[^.]{0,120}\b(South Broward Hospital District|special taxing district|public health system|public hospital|taxing district|not-for-profit|nonprofit)\b[^.]{0,120}',t,re.I)
                R['memorial']={'url':e.get('site') or 'https://mhs.net/','read':TODAY,'finding':m.group(0).strip() if m else None,'reading':('public or district ownership stated on its own page \u2014 the Chair\u2019s conditional retirement confirmed' if m and re.search(r'(?i)district|public|taxing',m.group(0)) else ('not-for-profit stated; public or district ownership not stated \u2014 the conditional retirement stays conditional' if m else 'the page states no ownership form \u2014 the conditional retirement stays conditional'))}
                if m and re.search(r'(?i)district|public|taxing',m.group(0)): e['status']='RETIRED (practice fit, Chair\u2019s judgement at tests 3 and 4): public hospital district \u2014 confirmed by its own page \u00b7 read '+TODAY; e['retired']={'reason':'practice fit: a public hospital district has no owner to sell, no equity, no fractional seat (Chair\u2019s judgement, confirmed by its own page)','date':TODAY,'user':'Timothy A. Edick'}
            else: R['memorial']={'reading':f'refused ({r[1]}) \u2014 the conditional retirement stays conditional'}
        # 4-5 · the precondition (proved before this pass) applied, then the queries
        seen={e.get('feed_title') for e in Q.values()}; queues={pr:list(q) for pr,q in QP.items()}
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
                    k=f'{pr}:gnews_rss_w9:{len(Q)}'; e=Q[k]={'practice':pr,'source':'gnews_rss_w9','company':'','signal':{'sentence':sent[:400],'url':lk,'published':d,'read':TODAY},'date_field':f,'feed_title':ttl,'query':q,'precondition_span':span,'evidence_source':'signal','status':'proposed \u2014 unconfirmed'}
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
        R['stopped']='completed'
    except Stop as s: R['stopped']=str(s)
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    R['spent']=dict(spent); R['budget']=budget; R['counts']=dict(R['counts']); R['pe']=dict(R['pe']); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/w9-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],R['counts'],dict(spent))
    await b.close(); await p.stop()
asyncio.run(go())
