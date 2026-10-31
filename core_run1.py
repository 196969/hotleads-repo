import asyncio,json,re,html,datetime,collections,urllib.parse,hashlib,os
import bot,discovery,intake,naming4,naming8,naming9,naming10,roster
TODAY=discovery.TODAY; NOW=datetime.date.today()
R={'run':'core build run one','launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stepA':{'contact':{},'refused':{}},'w18':{},'w19':{},'sources':{},'admitted':[],'decisions':[],'stopped':None}
def T(b): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',b or '',flags=re.S|re.I))))
TITLE=r'(Chief Executive Officer|CEO|President|Founder|Co-Founder|Owner|Managing Director|Managing Partner|General Manager|Chief Financial Officer|CFO|Chief Operating Officer|COO)'
def find_dm(text,company=None):
    for s in re.split(r'(?<=[.!?])\s+',text):
        if company and not naming10.names_company(s,company): continue
        for m in re.finditer(r"\b([A-Z][a-zA-Z'\-]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+)\s*(?:,|\u2013|\u2014|-|\||as|is)?\s*(?:the |our |its |new )?"+TITLE+r'\b',s):
            if naming10.is_person(m.group(1)): return {'name':m.group(1),'title':m.group(2),'span':s.strip()[:200]}
        for m in re.finditer(TITLE+r"\s*(?:,|\u2013|\u2014|-|:)?\s*([A-Z][a-zA-Z'\-]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+)",s):
            if naming10.is_person(m.group(2)): return {'name':m.group(2),'title':m.group(1),'span':s.strip()[:200]}
    return None
def src(name): R['sources'].setdefault(name,{'reads':0,'answered':0,'refused':collections.Counter(),'yield':0})
async def go():
    read0,b,p=await discovery.browser_reader()
    async def read(url):
        code,body,final=await read0(url)
        if isinstance(code,int) and code<400 and naming8.is_challenge(body): return 'challenge',body,final
        return code,body,final
    day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter()
    budget={'Step A':55,'Private Equity':85,'Acquisitions':55}
    for k in budget: day.spent[k]=0
    consec=collections.Counter(); closed={}
    async def rd(pr,source,url):
        src(source)
        if source in closed: return None,'closed',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,source,url); spent[pr]+=1; R['sources'][source]['reads']+=1
        if r[0]: R['sources'][source]['answered']+=1; consec[source]=0; open(f'w18-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')
        elif r[0] is False:
            R['sources'][source]['refused'][str(r[1])]+=1; consec[source]+=1
            if consec[source]>=3: closed[source]=f'three refusals (last {r[1]})'
        return r
    async def prove_and_test(co,cands,pr,source):
        tried=[]
        for rt,url in cands:
            if not url: continue
            r=await rd(pr,source+':site',url)
            if r[0] is None: tried.append({'route':rt,'host':url,'outcome':'not read: '+str(r[1])}); continue
            if r[0] is False: tried.append({'route':rt,'host':url,'outcome':('refused (challenge)' if str(r[1])=='challenge' else f'refused ({r[1]})')+' \u2014 re-runnable'}); continue
            pf=naming8.prove_site8(r[2],co,re.sub(r'^https?://','',url).split('/')[0])
            if not isinstance(pf,dict): tried.append({'route':rt,'host':url,'outcome':'refused (challenge)' if pf=='challenge' else 'resolved but failed the proof'}); continue
            tried.append({'route':rt,'host':url,'outcome':'proved'}); tt=T(r[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2])
            t1,why=intake.test1_florida({'url':url,'read':TODAY,'address_text':addr or tt[:300]}); ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt)
            em=[z for z in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',tt) if not re.search(r'\.(png|jpg|svg|webp)$',z)]
            t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':url,'read':TODAY} if ph else None,'address':{'value':addr,'url':url,'read':TODAY} if addr else None})
            return {'site':url,'page':r[2],'proof':pf,'test1':(t1,why),'test5':ch if t5 else None,'phone':ph.group(0) if ph else None,'email':em[0] if em else None,'address':addr or None,'tried':tried}
        return {'tried':tried}
    async def leadership(co,site,page,pr,source):
        dm=find_dm(T(page))
        if dm: return dict(dm,url=site,read=TODAY,source='the company\u2019s own page')
        host=re.sub(r'^https?://(www\.)?','',site).split('/')[0]; links=[]
        for m in re.finditer(r'<a\b[^>]*href="([^"#]+)"[^>]*>(.*?)</a>',page or '',re.S|re.I):
            u=m.group(1); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()+' '+u.lower()
            if re.search(r'leadership|our team|\bteam\b|management|executive|about',txt):
                if u.startswith('/'): u='https://'+host+u
                if host in u and u not in links: links.append(u)
        for u in links[:2]:
            r=await rd(pr,source+':leadership',u)
            if r[0]:
                dm=find_dm(T(r[2]))
                if dm: return dict(dm,url=u,read=TODAY,source='the company\u2019s own page')
        return None
    def admit(k,e,dm,tier,reason):
        e.update(decision_maker=dm,tier=tier,tier_reason=reason,status=f'ADMITTED BY TEST (1, 2, 5; size Blind; named executive) \u2014 Tier {tier} \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'); R['admitted'].append({'key':k,'company':e['company'],'practice':e['practice'],'tier':tier,'reason':reason,'dm':dm['name']+', '+dm['title']})
    def gnews(q): return 'https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=en-US&gl=US&ceid=US:en'
    try:
        # ---- Step A, reading half: the three contact-outstanding on every named route
        disp={'Moneysolver':'MoneySolver','Trakamerica':'TrakAmerica','Marino Performance Motors':'Marino Performance Motors'}
        for c,n in disp.items():
            k=next(k for k,e in Q.items() if e.get('company')==c and e.get('test1_pass')); e=Q[k]; slug=re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-'); dom=re.sub(r'^https?://(www\.)?','',e.get('site') or e.get('company_url') or '').split('/')[0]
            routes=[('The Ladders','theladders',f'https://www.theladders.com/company/{slug}-jobs'),('RocketReach','rocketreach',f'https://rocketreach.co/{slug}-management_b5c'),('Hunter','hunter',f'https://hunter.io/companies/{dom}'),('trade press','gnews_rss',gnews(f'"{n}" (president OR CEO OR owner OR founder)'))]
            rec=[]; dm=None
            for label,source,url in routes:
                if dm: break
                r=await rd('Step A',source,url)
                if r[0] is None: rec.append({'route':label,'result':'not read: '+str(r[1])}); continue
                if not r[0]: rec.append({'route':label,'result':f'refused ({r[1]})'+(' \u2014 the URL path is built from the name, a labelled guess' if source!='gnews_rss' else '')}); continue
                if source=='gnews_rss':
                    for u in [html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',r[2])][1:3]:
                        r2=await rd('Step A','gnews_rss:article',u)
                        if r2[0]:
                            d=find_dm(T(r2[2]),n)
                            if d: dm=dict(d,url=u,read=TODAY,source='trade press, whole company name in the sentence'); break
                    rec.append({'route':label,'result':'named executive found' if dm else 'articles read; no sentence naming an officer with the whole company name'})
                else:
                    d=find_dm(T(r[2]),n); rec.append({'route':label,'result':'named executive found' if d else 'read; no named officer with the whole company name (behind an account wall or absent)'})
                    if d: dm=dict(d,url=url,read=TODAY,source=label)
            R['stepA']['contact'][c]={'routes':rec,'dm':dm}
            if dm: admit(k,e,dm,'A' if e['source']!='hig' else 'B','sponsor portfolio membership: an ownership-form signal' if e['source']=='hig' else 'dated third-party signal within 18 months')
            else: e['status']='COMPLETE, CONTACT OUTSTANDING \u2014 measured shut on The Ladders, RocketReach, Hunter and the trade press this run (routes on the row)'; e['contact_routes_run1']=rec
        # ---- Step A: the 24 refused-re-runnable, re-run in full (candidates failing the name or asset test are recorded, not re-read)
        for k,e in [(k,e) for k,e in Q.items() if (e.get('status') or '').startswith('refused')]:
            co=e.get('company') or ''
            if naming8.cleanup(co)[0] is None or naming9.is_asset(co)[0] or co in ('California AI Company',):
                R['stepA']['refused'][co]={'result':'not re-read: the candidate fails the name or asset test, so no read can admit it (O\u2019Leary: a read must earn its return)'}; continue
            hosts=[t['host'] for t in e.get('routes_tried',[]) if t['outcome'].startswith('refused')]
            res=await prove_and_test(co,[('re-run',h) for h in hosts],'Step A','refused-queue')
            if not res.get('site'):
                e['status']='refused again on every route (core run one) \u2014 re-runnable, measured shut this run' if all('refused' in t['outcome'] for t in res['tried']) else 'routes re-read; none proved \u2014 no site found by any route'
                R['stepA']['refused'][co]={'result':e['status'],'tried':res['tried']}; continue
            e.update(site=res['site'],site_proof=res['proof'],test1=res['test1'][1],test1_pass=res['test1'][0],test5=res['test5'],phone={'value':res['phone'],'url':res['site'],'read':TODAY} if res['phone'] else None)
            if not res['test1'][0]: e['status']='site proved; test 1 failed: '+res['test1'][1]; R['stepA']['refused'][co]={'result':e['status']}; continue
            dm=await leadership(co,res['site'],res['page'],'Step A','refused-queue')
            sig=(e.get('signal') or {}).get('published') or ''
            old=bool(sig) and (NOW-datetime.date.fromisoformat(sig[:10])).days>548
            if dm and res['test5']: admit(k,e,dm,'B' if old else 'A','dated third-party signal older than 18 months' if old else 'dated third-party signal within 18 months'); R['stepA']['refused'][co]={'result':'recovered and admitted'}
            else: e['status']='COMPLETE, CONTACT OUTSTANDING \u2014 recovered site, tests passed; no named executive on the pages read' if res['test5'] else 'site proved; no published channel (test 5)'; R['stepA']['refused'][co]={'result':e['status']}
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        # ---- Window 18: sponsor portfolios
        cards=roster.suncap_cards(open('scratch-suncap.html',errors='ignore').read()); fl=[c for c in cards if c['location'].lower()=='florida']
        R['w18']['sun_capital']={'cards_on_the_roster':len(cards),'florida_on_face':len(fl),'unread_entries_not_florida':len(cards)-len(fl),'decision':'the roster reader reads location from the card; the non-Florida entries are not read (a read that cannot place a company in Florida earns nothing)','companies':[]}
        for c in fl:
            co=c['name']; k=next((k for k,e in Q.items() if e['source']=='suncap' and e.get('florida_on_card') and naming10.names_company(e.get('company',''),co)),None) or f'Private Equity:suncap:card:{co}'
            e=Q.setdefault(k,{'practice':'Private Equity','source':'suncap','company':co,'sponsor':'Sun Capital Partners','sponsor_page':c['entry'],'evidence_source':'sponsor portfolio card'})
            e.update(company=co,card={'sector':c['sector'],'location':c['location'],'status':c['status']},sponsor_page=c['entry'])
            r=await rd('Private Equity','suncap:entry',c['entry'])
            link=discovery.site_link(r[2],co) if r[0] else None; idate=None
            if r[0]:
                m=re.search(r'(?:Investment Date|Date of Investment|Acquired|Invested)[:\s]*([A-Z][a-z]+ \d{4}|\d{4})',T(r[2])); idate=m.group(1) if m else None
            res=await prove_and_test(co,[('sponsor entry link',link)]+[('derived host','https://www.'+h+'/') for h in naming4.derived_hosts(co)],'Private Equity','suncap')
            rec={'company':co,'sector':c['sector'],'status':c['status'],'investment_date_on_entry':idate,'routes':res['tried']}
            if res.get('site') and res['test1'][0]:
                e.update(site=res['site'],site_proof=res['proof'],test1=res['test1'][1],test1_pass=True,test5=res['test5'],phone={'value':res['phone'],'url':res['site'],'read':TODAY} if res['phone'] else None,signal={'sentence':f"Sun Capital Partners portfolio: {co} ({c['sector'] or 'sector not shown'}, Florida, {c['status'] or 'status not shown'})",'url':c['entry'],'published':idate,'read':TODAY})
                dm=await leadership(co,res['site'],res['page'],'Private Equity','suncap')
                if dm and res['test5']:
                    recent=False
                    if idate and re.search(r'\d{4}',idate): recent=int(re.search(r'\d{4}',idate).group(0))>=NOW.year-1
                    admit(k,e,dm,'A' if (recent and c['status']=='active') else 'B','sponsor holding, investment within 18 months' if (recent and c['status']=='active') else ('sponsor holding realized (prior), an ownership-form signal' if c['status']!='active' else 'sponsor portfolio membership with no dated investment on the entry: an ownership-form signal'))
                    rec['result']='admitted'
                else: e['status']='COMPLETE, CONTACT OUTSTANDING \u2014 no named executive on the pages read' if res['test5'] else 'site proved; no published channel (test 5)'; rec['result']=e['status']
            else: e['status']=('test 1 failed: '+res['test1'][1]) if res.get('site') else 'no site found by any route \u2014 held (routes on the row)'; rec['result']=e['status']
            R['w18']['sun_capital']['companies'].append(rec)
        R['w18']['boyne']={'entries':0,'florida':0,'companies':[]}
        for k,e in [(k,e) for k,e in Q.items() if e['source']=='boyne' and not e.get('entry_read')]:
            r=await rd('Private Equity','boyne:entry',e['sponsor_page']); e['entry_read']=TODAY; R['w18']['boyne']['entries']+=1
            if not r[0]: continue
            t=T(r[2]); fl_=re.search(r'[^.]{0,60}\b(?:[A-Z][a-z]+(?: [A-Z][a-z]+)?,\s*(?:FL|Florida))\b[^.]{0,40}',t)
            if not fl_: e['status']='location not on the entry \u2014 held, location unread'; continue
            R['w18']['boyne']['florida']+=1; co=e['company']; link=discovery.site_link(r[2],co)
            res=await prove_and_test(co,[('sponsor entry link',link)]+[('derived host','https://www.'+h+'/') for h in naming4.derived_hosts(co)],'Private Equity','boyne')
            rec={'company':co,'florida_span':fl_.group(0)[:120],'routes':res['tried']}
            if res.get('site') and res['test1'][0]:
                e.update(site=res['site'],site_proof=res['proof'],test1=res['test1'][1],test1_pass=True,test5=res['test5'],phone={'value':res['phone'],'url':res['site'],'read':TODAY} if res['phone'] else None,signal={'sentence':f'Boyne Capital portfolio: {co}','url':e['sponsor_page'],'published':None,'read':TODAY})
                dm=await leadership(co,res['site'],res['page'],'Private Equity','boyne')
                if dm and res['test5']: admit(k,e,dm,'B','sponsor portfolio membership with no dated investment on the entry: an ownership-form signal'); rec['result']='admitted'
                else: e['status']='COMPLETE, CONTACT OUTSTANDING \u2014 no named executive on the pages read' if res['test5'] else 'site proved; no published channel'; rec['result']=e['status']
            else: e['status']=('test 1 failed') if res.get('site') else 'no site found by any route \u2014 held'; rec['result']=e['status']
            R['w18']['boyne']['companies'].append(rec)
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
        probes18=[('Trivest','https://www.trivest.com/portfolio/'),('ACG','https://www.acg.org'),('ACG chapters','https://www.acg.org/chapters'),('SBIA','https://www.sbia.org'),('PE Hub','https://www.pehub.com'),('SEC EDGAR search','https://www.sec.gov/edgar/search/'),('SEC EDGAR full-text','https://efts.sec.gov/LATEST/search-index?q=%22Florida%22%20%22acquisition%22&forms=8-K'),('Crunchbase','https://www.crunchbase.com')]
        probes19=[('BizBuySell Florida','https://www.bizbuysell.com/florida-businesses-for-sale/'),('BizBuySell','https://www.bizbuysell.com'),('BizQuest','https://www.bizquest.com/florida-businesses-for-sale/'),('DealStream','https://dealstream.com/florida-businesses-for-sale'),('BusinessBroker.net','https://www.businessbroker.net/state/florida-businesses-for-sale.aspx'),('LoopNet','https://www.loopnet.com/biz/florida-businesses-for-sale/'),('IBBA','https://www.ibba.org'),('M&A Source','https://www.masource.org'),('Sunbelt','https://www.sunbeltnetwork.com/businesses-for-sale/?state=FL'),('Transworld','https://www.tworld.com'),('Murphy Business','https://www.murphybusiness.com')]
        for win,lst,pr in (('w18',probes18,'Private Equity'),('w19',probes19,'Acquisitions')):
            R[win].setdefault('probes',{})
            for nm,u in lst:
                r=await rd(pr,'probe:'+nm,u)
                if r[0] is None: R[win]['probes'][nm]={'state':'not read: '+str(r[1])}; continue
                if not r[0]: R[win]['probes'][nm]={'state':f'refused ({r[1]})'}; continue
                t=T(r[2]); fl_n=len(re.findall(r'\b[A-Z][a-zA-Z .]+,\s*(?:FL|Florida)\b',t)); named=len(set(re.findall(r'\b[A-Z][\w&\'.-]+(?: [A-Z][\w&\'.-]+){0,3} (?:Inc|LLC|Corp|Company|Co)\.?\b',t)))
                listings=len(re.findall(r'(?i)asking price|cash flow|for sale',t))
                R[win]['probes'][nm]={'state':'answered','bytes':len(r[2]),'florida_city_pairs':fl_n,'legal_suffix_names':named,'listing_markers':listings,'reading':('listing page: listings carry location but name no company' if listings and not named else ('answered; company names present' if named else 'answered; no listing or company names on the page read'))}
        R['stopped']='completed'
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    for v in R['sources'].values(): v['refused']=dict(v['refused'])
    R['spent']=dict(spent); R['closed']=closed; R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/core-run1-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],dict(spent),'admitted',len(R['admitted']))
    await b.close(); await p.stop()
asyncio.run(go())
