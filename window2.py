import asyncio,json,re,time,html,datetime,collections,urllib.parse
import bot,discovery,practice,intake
C=json.load(open('practice-classes.json')); P={s['id']:s for s in C['discovery']['practices']['Private Equity']['sources']}; BAND=C['band']; TODAY=discovery.TODAY
REP={'window':2,'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'proofs':{},'sources':{},'reads_by_practice':{},'decisions':[],'parked':{},'new_sources':{}}
CAP=20
async def go():
    read,b,p=await discovery.browser_reader(); day=discovery.Day('florida','Timothy A. Edick',read); day.Q=json.load(open('florida-intake-queue.json')); day.third=66
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); Q=day.Q
    async def rd(practice_,src,url):
        r=await day.one_read(practice_,src,url); return r
    # ---- 3: link rule proved on the first live H.I.G. entry read; Trivest rendered; Florida Trend date form
    hig_fl=[k for k,e in Q.items() if e['source']=='hig' and e.get('sponsor_page')][:1]
    r=await rd('Private Equity','proof:hig',Q[hig_fl[0]]['sponsor_page']); body=r[2] if r[0] else ''
    first_ext=next((u for u in re.findall(r'href="(https?://[^"]+)"',body) if 'hig.com' not in u and 'linkedin' not in u),None); rule=discovery.site_link(body,Q[hig_fl[0]]['company']); card=discovery.card_text(body,0,0)
    loc=re.search(r'(Headquarters|Location|HQ)[^A-Za-z]{0,20}([A-Z][A-Za-z .]+,\s*[A-Z]{2}|[A-Z][a-z]+,\s*[A-Z][a-z]+)',re.sub(r'<[^>]+>',' ',body))
    REP['proofs']['link_rule_first_live_read']={'page':Q[hig_fl[0]]['sponsor_page'],'first_external_href':first_ext,'site_link_rule':rule,'differ':first_ext!=rule,'portal_excluded':bool(first_ext and 'fiscloudservices' in first_ext and (rule is None or 'fiscloudservices' not in rule)),'location_field':loc.group(0)[:60] if loc else None,'classes':['portal/site-wide link / company site link','location field present / absent']}
    # Trivest: wait for the rendered list
    pg=await (await p.chromium.launch(args=['--no-sandbox','--disable-gpu'])).new_page() if False else None
    try:
        from playwright.async_api import async_playwright
        r=await rd('Private Equity','trivest',P['trivest']['route'])
    except Exception as e: r=(False,'net','')
    tb=''
    if r[0]:
        # re-open with a longer wait through the same reader is not possible; parse what the DOM gave after domcontentloaded+1.5s
        tb=r[2]; its=discovery.items(P['trivest'],tb); REP['sources']['trivest']=f'rendered read: {len(its)} companies' if its else 'portfolio still not in the DOM after load; parked for the window (reason: renders by script after load)'
        for u,t,f,card,fig in its:
            k=day.queue_candidate('Private Equity',P['trivest'],t,P['trivest']['route'],f'{t} is named on Trivest Partners\u2019 portfolio page.',TODAY,None)
            if k not in ('filtered','on file'): Q[k].update(sponsor='Trivest Partners',sponsor_page=u,florida_on_card=f,card_text=card)
    # Florida Trend: one article, derive the date form
    ft_art=[e['url'] for e in (json.loads(l) for l in open('florida-bot-log.jsonl')) if e.get('source')=='florida_trend' and e['outcome']=='read' and '/article/' in e.get('url','')][:1]
    ft={'article':ft_art[0] if ft_art else None}
    if ft['article']:
        r=await rd('Acquisitions','florida_trend:known-answer',ft['article']); 
        if r[0]:
            txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',r[2]))); m=re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b|\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b|\b(\d{4})-(\d\d)-(\d\d)\b',txt[:20000]); meta=re.search(r'(datePublished|published_time|pubdate)[^>]{0,80}?(\d{4}-\d\d-\d\d)',r[2])
            ft.update(visible=m.group(0) if m else None,meta=meta.group(2) if meta else None,extractor_before=practice.pub_date(r[2]))
            old=practice.pub_date
            def pd(body,_o=old):
                d=_o(body)
                if d: return d
                t=re.sub(r'<[^>]+>',' ',body[:30000]); mm=re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',t)
                if mm: return f'{mm.group(3)}-{int(mm.group(1)):02d}-{int(mm.group(2)):02d}'
                mm=re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b',t)
                if mm: return datetime.datetime.strptime(mm.group(0),'%B %d, %Y').date().isoformat()
                return None
            practice.pub_date=pd; ft['extractor_after']=pd(r[2]); ft['result']='PROVED' if ft['extractor_after'] else 'FAILED \u2014 no date form found on the live article; Florida Trend stays stopped'
        else: ft['result']=f'refused ({r[1]})'
    REP['proofs']['florida_trend_date_form']=ft
    # ---- 4: new sources from live forms (one read each); a control built from the live form; refusals logged
    NEW=[('Acquisitions','sfbj_news','https://www.bizjournals.com/southflorida/news/',r'href="(https?://(?:www\.)?bizjournals\.com/southflorida/news/\d{4}/\d\d/\d\d/[^"]+)"'),('Acquisitions','tbbj_news','https://www.bizjournals.com/tampabay/news/',r'href="(https?://(?:www\.)?bizjournals\.com/tampabay/news/\d{4}/\d\d/\d\d/[^"]+)"'),('Acquisitions','obj_news','https://www.bizjournals.com/orlando/news/',r'href="(https?://(?:www\.)?bizjournals\.com/orlando/news/\d{4}/\d\d/\d\d/[^"]+)"'),('Acquisitions','jbj_news','https://www.bizjournals.com/jacksonville/news/',r'href="(https?://(?:www\.)?bizjournals\.com/jacksonville/news/\d{4}/\d\d/\d\d/[^"]+)"'),('Acquisitions','sunbelt','https://www.sunbeltnetwork.com/businesses-for-sale/?state=FL',r'href="(https?://(?:www\.)?sunbeltnetwork\.com/business[^"]+)"'),('Acquisitions','transworld','https://www.tworld.com/buy-a-business/florida/',r'href="(https?://(?:www\.)?tworld\.com/[^"]*listing[^"]*)"'),('Acquisitions','murphy','https://www.murphybusiness.com/businesses-for-sale/?state=FL',r'href="(https?://(?:www\.)?murphybusiness\.com/[^"]*listing[^"]*)"'),('Fractionals','careerbuilder','https://www.careerbuilder.com/jobs?keywords=controller&location=FL',r'href="(/job/[^"]+)"'),('Fractionals','simplyhired','https://www.simplyhired.com/search?q=controller&l=Florida',r'href="(/job/[^"]+)"')]
    for pr,sid,url,pat in NEW:
        r=await rd(pr,sid,url)
        if r[0] is None: REP['new_sources'][sid]='not read: '+r[1]; continue
        ok,code,body=r
        if not ok: REP['new_sources'][sid]=f'refused by source ({code})'; continue
        items=list(dict.fromkeys(html.unescape(m) for m in re.findall(pat,body)))[:10]; forms=collections.Counter(re.sub(r'[^/]+/?$','\u2026',h) for h in re.findall(r'href="([^"]+)"',body) if (sid.split('_')[0] in h or h.startswith('/'))).most_common(3)
        REP['new_sources'][sid]={'read':True,'bytes':len(body),'items_by_declared_pattern':len(items),'live_forms':forms,'control':'built from the live form' if items else 'live form carries no items for the declared pattern; recorded, not guessed'}
        for u in items[:3]:
            if pr=='Acquisitions' and 'bizjournals' in u:
                r2=await rd(pr,sid,u)
                if r2[0]:
                    d=practice.pub_date(r2[2]); txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',r2[2]))); sent=next((x.strip() for x in re.split(r'(?<=[.!?])\s+',txt) if re.search(practice.KW['Acquisitions'],x,re.I) and re.search(r'\bFlorida\b|\bFL\b',x)),None)
                    if d and sent: day.queue_candidate(pr,{'id':sid,'name':sid},None,u,sent,d,None)
    # ---- 1 & 2: PE discovery under the caps — Sun Capital's Florida cards first (own site via the sponsor entry), then sponsor entries for the others, 20 per source
    for sid in ('suncap','hig','comvest','boyne','trivest'):
        reads_src=0; passed=0; st=REP['sources'].get(sid,'')
        cands=[k for k,e in Q.items() if e['source']==sid and (e.get('band') or {}).get('in_band') is not False]
        cands.sort(key=lambda k:(not Q[k].get('florida_on_card'),k))
        for k in cands:
            e=Q[k]
            if reads_src>=CAP and passed==0: REP['parked'][sid]=f'parked: {CAP} reads, 0 rows passing test 1 (addition 2)'; break
            if day.spent['Private Equity']>=day.third: REP['parked'][sid]='third spent'; break
            if e.get('location')=='Florida on the sponsor card' or e.get('entry_location_fl'): pass
            elif not e.get('entry_read'):
                r=await rd('Private Equity','entry:'+sid,e['sponsor_page'])
                if r[0] is None: break
                reads_src+=1; e['entry_read']=TODAY
                if not r[0]: e['entry']='sponsor entry refused ('+str(r[1])+')'; continue
                txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',r[2]))); e['entry_location_fl']=bool(re.search(discovery.FL,txt)); e['site_from_entry']=discovery.site_link(r[2],e['company'])
                rv=re.search(r'\$\s?([\d.,]+)\s?(million|M|billion|B)\b',txt,re.I)
                if rv: fig=float(rv.group(1).replace(',',''))*(1e9 if rv.group(2).lower().startswith('b') else 1e6); bb,w=intake.band_check({'revenue_figure':fig,'revenue_source':{'url':e['sponsor_page'],'read':TODAY}},BAND); e['band']={'in_band':bb,'why':w}
                if not e['entry_location_fl']: e['location']='location unread \u2014 the sponsor\u2019s entry places it nowhere in Florida; not read at its own site'; continue
                if (e.get('band') or {}).get('in_band') is False: continue
            # own-site read only for candidates the sponsor places in Florida
            site=e.get('site_from_entry') or e.get('company_url')
            if not site:
                if not e.get('entry_read'):
                    r=await rd('Private Equity','entry:'+sid,e['sponsor_page'])
                    if r[0] is None: break
                    reads_src+=1; e['entry_read']=TODAY
                    if r[0]: e['site_from_entry']=discovery.site_link(r[2],e['company']); site=e['site_from_entry']
                if not site: e['test1']='sponsor entry names no company site'; continue
            e['company_url']=site; r=await rd('Private Equity','test1:'+sid,site)
            if r[0] is None: break
            reads_src+=1
            if not r[0]: e['test1']=f'company page refused ({r[1]}) \u2014 re-runnable'; continue
            txt=html.unescape(re.sub(r'<[^>]+>',' ',r[2])); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',txt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or txt[:300]}); e['test1']=why; e['test1_pass']=t1
            ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',txt); em=[x for x in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',txt) if not re.search(r'\.(png|jpg|svg)$',x)]
            e['phone']={'value':ph.group(0),'url':site,'read':TODAY} if ph else None; e['email']={'value':em[0],'url':site,'read':TODAY,'role_inbox':bool(re.match(r'^(info|sales|contact|hello|office|admin|support)',em[0].split('@')[0],re.I))} if em else None
            t5,ch=intake.test5_channel({'phone':e['phone'],'address':{'value':addr,'url':site,'read':TODAY} if addr else None,'form':{'value':'form','url':site,'read':TODAY} if re.search(r'<form',r[2],re.I) else None}); e['test5']=ch
            if t1: passed+=1; e['status']='admitted by test (1, 2, 5) \u2014 awaiting the Chair\u2019s tests 3 and 4' if t5 else 'passes test 1; no reachable channel published \u2014 not admitted (test 5)'
        REP['sources'][sid]=REP['sources'].get(sid,'')+f' | window two: {reads_src} reads, {passed} passing test 1'
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    REP['reads_by_practice']=day.spent; REP['stopped']='completed'; json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(REP,open('reports/w2-engine.json','w'),indent=1,ensure_ascii=False); print(json.dumps(REP)[:1500])
    await b.close(); await p.stop()
asyncio.run(go())
