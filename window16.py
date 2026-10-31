import naming6
import asyncio,json,re,html,datetime,collections,urllib.parse,hashlib,os
import bot,discovery,practice,intake,naming,naming4,naming5,naming6,naming7,naming8,naming9
TODAY=discovery.TODAY
METROS=['Miami','Fort Lauderdale','Tampa','Orlando','Jacksonville','West Palm Beach','Sarasota','Naples','Fort Myers','Pensacola','Tallahassee','Gainesville','Lakeland','Ocala']
INDUSTRIES=['manufacturing','distribution','food and beverage','construction','transportation logistics','multi-site retail','field services','events','sales organization','marketing agency']
QP={'Acquisitions':[f'"Florida" {w}' for w in ('company acquired','acquisition','"sold to"','"CEO retiring"','succession family business')]+[f'"{m}" company acquired' for m in METROS]+[f'Florida {i} company acquired' for i in INDUSTRIES],
    'Private Equity':['"Florida" "private equity" invests','"Florida" "portfolio company"','"Florida" "private equity" acquires']+[f'"{m}" "private equity"' for m in METROS[:5]],
    'Fractionals':['"Florida" company "names" CFO','"Florida" "chief financial officer" appointed']+[f'"{m}" company names CFO' for m in METROS[:5]]}
R={'window':16,'executives':{},'roster_probe':{},'completion':{},'am':None,'checks':{},'revenue':{},'refused_queue':[],'cleanup':[],'revenue':{},'property_stopped':0,'queue_halts':[],'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'revenue':{},'memorial':None,'disc':{'articles_read':0,'florida_signal':0,'reaching_binding':0,'site_by_article_link':0,'site_by_derived_host':0,'no_site_by_any_route':0,'precondition_stopped':0},'routes':[],'per_query':{},'counts':collections.Counter(),'parked':{},'directory':{},'pe':collections.Counter(),'admitted_by_test':[],'decisions':[],'stopped':None}
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
    read0,b,p=await discovery.browser_reader()
    async def read(url):
        code,body,final=await read0(url)
        if isinstance(code,int) and code<400 and naming8.is_challenge(body): return 'challenge',body,final   # fault 54: a challenge screen is a refusal
        return code,body,final
    day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Acquisitions':50,'Private Equity':10,'Fractionals':10,'Directory probes':0,'Ownership':0,'Refused queue':0,'Revenue class':0,'Completion':0,'Executives':60,'Roster probe':12}
    for k in budget: day.spent[k]=0
    consec=collections.Counter()
    async def rd(pr,src,url,pk):
        if pk in R['parked']: return None,'parked',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,src,url); spent[pr]+=1
        if r[0] is False:
            consec[pk]+=1
            if consec[pk]>=3: R['parked'][pk]=f'parked for the window: 3 consecutive refusals (last {r[1]})'
        elif r[0]: consec[pk]=0; open(f'w16-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')
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
    CHK={}
    def CK(name,res):
        c=CHK.setdefault(name,{'calls':0,'stopped':0}); c['calls']+=1
        if not res[0]: c['stopped']+=1
        return res
    import hashlib as _h, os as _o
    def filed(url):
        for d in ('w15-bodies','w14-bodies','w13-bodies','w12-bodies','w11-bodies','w10-bodies','w9-bodies','w8-bodies','w7-bodies','w6-bodies'):
            p=f"{d}/{_h.sha1(url.encode()).hexdigest()[:12]}.html"
            if _o.path.exists(p): return open(p,errors='ignore').read()
        return None
    TITLE=r'(Chief Executive Officer|CEO|President|Founder|Co-Founder|Owner|Managing Director|Managing Partner|General Manager|Chief Financial Officer|CFO|Chief Operating Officer|COO)'
    def find_dm(text):
        m=re.search(r'\b([A-Z][a-z]+(?: [A-Z]\.)? [A-Z][a-zA-Z\'\-]+)\s*(?:,|\u2013|\u2014|-|\||\n|is|as)?\s*(?:the |our |its )?'+TITLE+r'\b',text) or re.search(TITLE+r'\s*(?:,|\u2013|\u2014|-|:)?\s*([A-Z][a-z]+(?: [A-Z]\.)? [A-Z][a-zA-Z\'\-]+)',text)
        if not m: return None
        g=m.groups(); name,title=(g[0],g[1]) if not re.match(TITLE,g[0]) else (g[1],g[0])
        if re.search(r'(?i)^(the|our|read|meet|contact|about|view|learn|click)\b',name): return None
        return {'name':name,'title':title,'span':m.group(0)[:160]}
    async def complete_one(k,e):
        rec={'company':e['company'],'site':e.get('site') or e.get('company_url')}
        sig=(e.get('signal') or {}); st=(e.get('feed_title') or '')+'. '+(sig.get('sentence') or '')
        dm=find_dm(st) if re.search(r'(?i)CFO|chief financial|COO|chief operating',st) else None
        if dm: rec['decision_maker']=dict(dm,url=sig.get('url'),read=sig.get('read'),source='the dated signal article'); return rec
        site=rec['site']
        if not site: rec['decision_maker']=None; rec['why']='no proved site to read'; return rec
        home=filed(site)
        if not home:
            r=await rd('Completion','complete:home',site,'complete:'+site)
            if not r[0]: rec['decision_maker']=None; rec['why']=f'home page refused ({r[1]}) \u2014 re-runnable'; return rec
            home=r[2]
        host=re.sub(r'^https?://(www\.)?','',site).split('/')[0]
        links=[]
        for m in re.finditer(r'<a\b[^>]*href="([^"#]+)"[^>]*>(.*?)</a>',home,re.S|re.I):
            u=m.group(1); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()
            if re.search(r'leadership|our team|management|executive|about us|^\s*about\s*$|who we are|our people|team',txt+' '+u.lower()):
                if u.startswith('/'): u='https://'+host+u
                if host in u and u not in links: links.append(u)
        dm=find_dm(T(home)); src=site
        for u in links[:2]:
            if dm: break
            r=await rd('Completion','complete:leadership',u,'complete:'+u)
            if r[0]: dm=find_dm(T(r[2])); src=u
        rec['leadership_links_tried']=links[:2]
        if dm: rec['decision_maker']=dict(dm,url=src,read=TODAY,source='the company\u2019s own page')
        else: rec['decision_maker']=None; rec['why']='no named executive with a title on the pages read'
        return rec
    def person_ok(n): return bool(re.fullmatch(r"[A-Z][a-z]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+",n or '')) and not re.match(r'(?i)(principal|owner|president|founder|manager|director|chief|our|the|meet|about|contact|read|view)\b',n)
    async def exec_discovery():
        six=['American Fasteners','Health Network One','Moneysolver','Sts Aviation Group','Marino Performance Motors','Trakamerica','FreightCenter']
        disp={'Sts Aviation Group':'STS Aviation Group','Trakamerica':'TrakAmerica'}
        state={}
        for c in six:
            k=next((k for k,e in Q.items() if e.get('company')==c and e.get('test1_pass')),None)
            if k: state[c]={'key':k,'routes':[],'dm':None}
        def site_of(c): e=Q[state[c]['key']]; return e.get('site') or e.get('company_url')
        async def r_pages(c,words):
            site=site_of(c)
            if not site: return 'no proved site'
            home=filed(site)
            if not home:
                r=await rd('Executives','exec:home',site,'exec:'+site)
                if not r[0]: return f'home page refused ({r[1]})'
                home=r[2]
            host=re.sub(r'^https?://(www\.)?','',site).split('/')[0]; links=[]
            for m in re.finditer(r'<a\b[^>]*href="([^"#]+)"[^>]*>(.*?)</a>',home,re.S|re.I):
                u=m.group(1); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()+' '+u.lower()
                if re.search(words,txt):
                    if u.startswith('/'): u='https://'+host+u
                    if host in u and u not in links: links.append(u)
            if not links: return 'the home page links no such page'
            r=await rd('Executives','exec:page',links[0],'exec:'+links[0])
            if not r[0]: return f'{links[0]} refused ({r[1]})'
            dm=find_dm(T(r[2]))
            if dm and person_ok(dm['name']): state[c]['dm']=dict(dm,url=links[0],read=TODAY,source='the company\u2019s own page'); return 'named executive found'
            return f'{links[0]} read; no named executive with a title'
        async def r_linkedin(c):
            slug=re.sub(r'[^a-z0-9]+','-',disp.get(c,c).lower()).strip('-'); u='https://www.linkedin.com/company/'+slug
            r=await rd('Executives','exec:linkedin',u,'linkedin')
            if not r[0]: return f'refused ({r[1]}) \u2014 slug built from the name, labelled a guess'
            dm=find_dm(T(r[2]))
            if dm and person_ok(dm['name']): state[c]['dm']=dict(dm,url=u,read=TODAY,source='LinkedIn public company page'); return 'named executive found'
            return 'read; no named executive with a title (slug built from the name)'
        async def r_press(c):
            n=disp.get(c,c); r=await rd('Executives','exec:press',gnews(f'"{n}" (CEO OR president OR founder OR owner)'),'gnews_rss')
            if not r[0]: return f'refused ({r[1]})'
            tok=n.split()[0].lower()
            for u in [html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',r[2])][1:3]:
                r2=await rd('Executives','exec:article',u,'gnews_rss')
                if not r2[0]: continue
                for s in re.split(r'(?<=[.!?])\s+',T(r2[2])):
                    if tok in s.lower():
                        dm=find_dm(s)
                        if dm and person_ok(dm['name']): state[c]['dm']=dict(dm,url=u,read=TODAY,source='trade press naming the officer with the company in the same sentence'); return 'named executive found'
            return 'articles read; no sentence naming an officer with the company'
        for label,fn in (('team page',lambda c: r_pages(c,r'\bteam\b|our people|who we are')),('leadership page',lambda c: r_pages(c,r'leadership|management|executive|about')),('LinkedIn public company page',r_linkedin),('trade-press article naming an officer',r_press)):
            for c in list(state):
                if state[c]['dm']: continue
                res=await fn(c); state[c]['routes'].append({'route':label,'result':res})
        for c,s in state.items():
            e=Q[s['key']]; R['executives'][c]={'routes':s['routes'],'dm':s['dm']}
            if s['dm']:
                e['decision_maker']=s['dm']
                if e.get('test5') not in (None,'no reachable channel with source and date'): e['status']='ADMITTED BY TEST (1, 2, 5; size Blind; named executive) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4'
            else: e['status']='COMPLETE, CONTACT OUTSTANDING \u2014 every test passed, size Blind, executive routes spent on the row'; e['executive_routes_spent']=s['routes']
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    async def roster_probe():
        for nm,home in (('Florida Restaurant and Lodging Association','https://www.frla.org/'),('Manufacturers Association of Florida','https://www.mafmfg.com/'),('FloridaMakes','https://www.floridamakes.com/'),('Florida Trucking Association','https://www.fltrucking.org/')):
            rec={'home':home}; r=await rd('Roster probe','roster:home',home,'roster:'+home)
            if not r[0]: rec['result']=f'home refused ({r[1]})'; R['roster_probe'][nm]=rec; continue
            host=re.sub(r'^https?://(www\.)?','',home).split('/')[0]; links=[]
            for m in re.finditer(r'<a\b[^>]*href="([^"#]+)"[^>]*>(.*?)</a>',r[2],re.S|re.I):
                u=m.group(1); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()
                if re.search(r'member directory|membership directory|find a member|member list|members directory|directory|our members|manufacturer directory|supplier directory',txt):
                    if u.startswith('/'): u='https://'+host+u
                    if u not in links: links.append(u)
            rec['directory_links']=links[:3]
            if not links: rec['result']='the home page links no member directory'; R['roster_probe'][nm]=rec; continue
            r2=await rd('Roster probe','roster:directory',links[0],'roster:'+links[0])
            if not r2[0]: rec['result']=f'directory refused ({r2[1]})'; R['roster_probe'][nm]=rec; continue
            t=T(r2[2]); fl=len(re.findall(r'\b[A-Z][a-zA-Z .]+,\s*(?:FL|Florida)\b',t)); names=len(re.findall(r'\b(?:Inc|LLC|Corp|Company|Co)\.?\b',t))
            rec.update(directory=links[0],bytes=len(r2[2]),city_state_pairs_on_page=fl,legal_suffix_names_on_page=names,login_wall=bool(re.search(r'(?i)log ?in to view|members only|sign in to|member login required',t)),result=('LOCATION ON FACE: city, FL appears on the listing page' if fl>=10 else ('listing page read; city on face too rare to read as a roster' if fl else 'listing page read; no city on its face')))
            R['roster_probe'][nm]=rec
    async def complete_rows():
        nine=['American Fasteners','Health Network One','Moneysolver','Alpha Foundations','Palm Medical Centers','Altitude Water','Sts Aviation Group','Marino Performance Motors','Trakamerica']
        # AM Distributors recovered first (#52): re-bound at zero reads, then its site by any route
        ak=next((k for k,e in Q.items() if 'AM Distributors' in (e.get('feed_title') or '')),None)
        if ak:
            e=Q[ak]; co,note=naming8.cleanup('Miami HVAC Distributor AM Distributors'); e.update(company=co,status='re-bound window fifteen (#52): '+(note or ''))
            ok2,why2=intake.test2_absent(co,None,day.idx); e['test2']=why2; rec={'company':co,'test2':why2}
            if ok2:
                art=filed(e['signal']['url']) or ''; cands=[]; tried=[]
                for m in re.finditer(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',art,re.S|re.I):
                    h=re.sub(r'^https?://(www\.)?','',m.group(1)).split('/')[0].lower()
                    if 'amdistributors' in h.replace('-',''): cands.append(('article link','https://'+h+'/')); break
                cands+= [('derived host','https://www.'+x+'/') for x in naming4.derived_hosts(co)]
                for rt,url in cands:
                    r=await rd('Completion','am:'+rt,url,'am:'+url)
                    if not r[0]: tried.append({'route':rt,'host':url,'outcome':f'refused ({r[1]})' if r[0] is False else 'not read'}); continue
                    pf=naming8.prove_site8(r[2],co,re.sub(r'^https?://','',url).split('/')[0])
                    if not isinstance(pf,dict): tried.append({'route':rt,'host':url,'outcome':'refused (challenge)' if pf=='challenge' else 'failed the proof'}); continue
                    tried.append({'route':rt,'host':url,'outcome':'proved'}); tt=T(r[2]); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':url,'read':TODAY,'address_text':addr or tt[:300]})
                    ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':url,'read':TODAY} if ph else None,'address':{'value':addr,'url':url,'read':TODAY} if addr else None})
                    e.update(site=url,site_proof=pf,site_route=rt,test1=why,test1_pass=t1,test5=ch,phone={'value':ph.group(0),'url':url,'read':TODAY} if ph else None,band={'in_band':None,'why':intake.SIZE_UNSOURCED}); break
                rec['routes']=tried; rec['test1']=e.get('test1'); rec['test5']=e.get('test5')
                if e.get('test1_pass') and e.get('test5') not in (None,'no reachable channel with source and date'): nine.append(co)
            R['am']=rec
        for c in nine:
            k=next((k for k,e in Q.items() if e.get('company')==c and e.get('test1_pass')),None)
            if not k: R['completion'][c]={'why':'row not found passing test 1'}; continue
            e=Q[k]; rec=await complete_one(k,e); e['decision_maker']=rec.get('decision_maker'); R['completion'][c]=rec
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    async def revenue_four():
        four=['Altitude Water','Sts Aviation Group','Marino Performance Motors','Trakamerica']
        disp={'Sts Aviation Group':'STS Aviation Group','Trakamerica':'TrakAmerica'}
        def routes(n): return [('Wikipedia search','https://en.wikipedia.org/w/index.php?search='+urllib.parse.quote('"'+n+'"')+'&title=Special:Search&go=Go','wikipedia'),('Florida Trend search','https://www.floridatrend.com/search?q='+urllib.parse.quote('"'+n+'"'),'floridatrend:search'),('Google News: name + revenue',gnews('"'+n+'" revenue'),'gnews_rss'),('Google News: name + "annual sales"',gnews('"'+n+'" "annual sales"'),'gnews_rss'),('Google News: name + employees',gnews('"'+n+'" employees'),'gnews_rss'),('Google News: name + growth',gnews('"'+n+'" growth'),'gnews_rss'),('Google News: name + "Inc. 5000" (press mention)',gnews('"'+n+'" "Inc. 5000"'),'gnews_rss')]
        for c in four: R['revenue'][c]={'name_read_as':disp.get(c,c),'routes':[{'route':'Inc. 5000 list','result':'parked under its code (403 \u00d73, window five) \u2014 not read; no size reading'}],'figure':None,'employees':None}
        for i in range(7):
            for c in four:
                out=R['revenue'][c]
                if out['figure']: continue
                n=disp.get(c,c); label,url,pk=routes(n)[i]; toks=[w.lower() for w in re.findall(r'[A-Za-z]{3,}',n)][:1]
                r=await rd('Revenue class','revenue:'+label[:20],url,pk)
                if r[0] is None: out['routes'].append({'route':label,'result':'not read: '+str(r[1])}); continue
                if not r[0]: out['routes'].append({'route':label,'result':f'refused ({r[1]}) \u2014 re-runnable'}); continue
                body=r[2]
                if 'wikipedia' in url:
                    hit='mw-search-results' not in body; t=T(body); m=re.search(r'Revenue\s*[^$]{0,40}(?:US)?\$\s?([\d.,]+)\s?(million|billion)',t) if hit else None
                    if m: out['figure']={'value':float(m.group(1).replace(',',''))*(1e9 if m.group(2)=='billion' else 1e6),'span':m.group(0),'url':url,'read':TODAY,'source':'Wikipedia infobox'}
                    out['routes'].append({'route':label,'result':'figure found' if m else ('no article matched \u2014 not a size reading' if not hit else 'article read; no revenue figure')}); continue
                links=[html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',body)][1:3] if 'news.google' in url else list(dict.fromkeys(re.findall(r'href="(https?://(?:www\.)?floridatrend\.com/article/\d+/[^"]*)"',body)))[:2]
                got='no item for the name \u2014 not a size reading'
                for u in links:
                    r2=await rd('Revenue class','revenue:article',u,pk)
                    if not r2[0]: continue
                    t=T(r2[2]); fig=sn=None
                    for snt in re.split(r'(?<=[.!?])\s+',t):
                        if toks and toks[0] in snt.lower() and re.search(r'(?i)\b(?:revenue|revenues|annual sales|in sales|sales of|top line|turnover)\b',snt) and not DEAL.search(snt):
                            mm=re.search(r'\$\s?([\d.,]+)\s?(million|billion|M\b|B\b|bn\b|mil\b|MM\b)',snt,re.I)
                            if mm: fig=float(mm.group(1).replace(',',''))*(1e9 if mm.group(2).lower() in ('billion','b','bn') else 1e6); sn=snt.strip()[:300]; break
                    ne,es=emp_sent(t,toks)
                    if ne and not out['employees']: out['employees']={'value':ne,'span':es,'url':u,'read':TODAY,'flag':'employee count \u2014 recorded, not a size reading'}
                    if fig: out['figure']={'value':fig,'span':sn,'url':u,'read':TODAY,'source':'trade press'}; got='figure found'; break
                    got='article(s) read; no sentence naming the company with a revenue figure (deal values excluded)'
                out['routes'].append({'route':label,'result':got})
        for c in four:
            out=R['revenue'][c]; k=next((k for k,e in Q.items() if e.get('company')==c and e.get('test1_pass')),None)
            if out['figure'] and k:
                e=Q[k]; ceil=1e8 if e['practice']=='Private Equity' else 25e6; v=out['figure']['value']; e['band']={'in_band':v<=ceil,'why':f"published revenue {v:.0f} vs {ceil:.0f} (Src: {out['figure']['url']} \u00b7 read {TODAY})",'figure':out['figure']}
                e['status']='ADMITTED BY TEST (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4' if v<=ceil else 'band-rejected at test 1: published revenue above the ceiling'
                if v<=ceil: R['admitted_by_test'].append(k)
            if out['employees'] and k: Q[k]['employees_published']=out['employees']
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    async def refused_queue():
        skip=('InterContinental Miami','Westshore Grand Hotel','200-Unit Pensacola Apartment Community','Door Maker','Fort Myers')
        for k,e in [(k,e) for k,e in Q.items() if (e.get('status') or '').startswith('refused')]:
            co=e.get('company') or ''
            if co in skip: R['refused_queue'].append({'company':co,'result':'not re-run: fails the name or asset test (faults 52, 57)'}); continue
            got=None; tried=[]
            for t in [t for t in e.get('routes_tried',[]) if t['outcome'].startswith('refused')]:
                url=t['host']; r=await rd('Refused queue','rerun:'+e['source'][:10],url,'rerun:'+url)
                if r[0] is None: tried.append({'host':url,'outcome':'not read: '+str(r[1])}); continue
                if r[0] is False: tried.append({'host':url,'outcome':('refused again (challenge)' if str(r[1])=='challenge' else f'refused again ({r[1]})')}); continue
                pf=naming8.prove_site8(r[2],co,re.sub(r'^https?://','',url).split('/')[0])
                if pf=='challenge': tried.append({'host':url,'outcome':'refused again (challenge)'}); continue
                if not pf: tried.append({'host':url,'outcome':'read; failed the proof'}); continue
                tried.append({'host':url,'outcome':'proved'}); got=(url,r[2],pf); break
            if got:
                url,page,pf=got; tt=T(page); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':url,'read':TODAY,'address_text':addr or tt[:300]})
                ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':url,'read':TODAY} if ph else None,'address':{'value':addr,'url':url,'read':TODAY} if addr else None})
                e.update(site=url,site_proof=pf,test1=why,test1_pass=t1,test5=ch,band={'in_band':None,'why':intake.SIZE_UNSOURCED}); e['status']='re-run window thirteen: site proved; '+('passes tests 1, 2 and 5; held size-unsourced' if t1 and t5 else ('test 1 failed: '+why if not t1 else 'no channel published'))
            elif all(x['outcome'].startswith('refused again') for x in tried) and tried: e['status']='refused again on every route (window thirteen) \u2014 re-runnable, not an absence'
            elif tried: e['status']='re-run window thirteen: routes read, none proved \u2014 no site found by any route'
            R['refused_queue'].append({'company':co,'tried':tried,'status':e['status']})
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    async def directory_first():
        R['directory']['AGC chapters']='parked under its code (404, window ten) \u2014 not re-probed'
    async def revenue_six():
        held=['American Fasteners','Health Network One','Moneysolver','Alpha Foundations','Palm Medical Centers','SeaWorld']
        fresh={'SeaWorld':['SeaWorld','SeaWorld Entertainment'],'Palm Medical Centers':['Palm Medical Centers']}
        for c in held: R['revenue'][c]={'routes':[],'figure':None,'employees':None}
        for c in held[:4]: R['revenue'][c]['routes'].append({'route':'every free route','result':'no unspent free route: Wikipedia, Florida Trend\u2019s own search, Google News by name with revenue, employees, annual sales, growth and Inc. 5000 press mention already read (windows five, eight, nine); Inc. 5000 list parked under its code'})
        plan=[]
        for c,nms in fresh.items():
            plan.append((c,'Wikipedia search','https://en.wikipedia.org/w/index.php?search='+urllib.parse.quote('"'+nms[-1]+'"')+'&title=Special:Search&go=Go','wikipedia'))
        for c,nms in fresh.items():
            plan.append((c,'Florida Trend search','https://www.floridatrend.com/search?q='+urllib.parse.quote('"'+nms[0]+'"'),'floridatrend:search'))
        for term in ('revenue','"annual sales"','employees'):
            for c,nms in fresh.items(): plan.append((c,'Google News: name + '+term,gnews('"'+nms[0]+'" '+term),'gnews_rss'))
        for c,label,url,pk in plan:
            out=R['revenue'][c]
            if out['figure']: continue
            r=await rd('Revenue class','revenue:'+label[:20],url,pk)
            if r[0] is None: out['routes'].append({'route':label,'result':'not read: '+str(r[1])}); continue
            if not r[0]: out['routes'].append({'route':label,'result':f'refused ({r[1]}) \u2014 re-runnable'}); continue
            body=r[2]; toks=[w.lower() for w in re.findall(r'[A-Za-z]{3,}',c)][:1]
            if 'wikipedia' in url:
                hit='mw-search-results' not in body; t=T(body); m=re.search(r'Revenue\s*[^$]{0,40}(?:US)?\$\s?([\d.,]+)\s?(million|billion)',t) if hit else None
                if m: out['figure']={'value':float(m.group(1).replace(',',''))*(1e9 if m.group(2)=='billion' else 1e6),'span':m.group(0),'url':'en.wikipedia.org search: '+fresh[c][-1],'read':TODAY,'source':'Wikipedia infobox'}
                out['routes'].append({'route':label,'result':'figure found' if m else ('no article matched \u2014 not a size reading' if not hit else 'article read; no revenue figure')}); continue
            links=[html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',body)][1:3] if 'news.google' in url else list(dict.fromkeys(re.findall(r'href="(https?://(?:www\.)?floridatrend\.com/article/\d+/[^"]*)"',body)))[:2]
            got='no item for the name \u2014 not a size reading'
            for u in links:
                r2=await rd('Revenue class','revenue:article',u,pk)
                if not r2[0]: continue
                t=T(r2[2]); fig,sn=None,None
                for snt in re.split(r'(?<=[.!?])\s+',t):
                    if toks[0] in snt.lower() and re.search(r'(?i)\b(?:revenue|revenues|annual sales|in sales|sales of)\b',snt) and not DEAL.search(snt):
                        mm=re.search(r'\$\s?([\d.,]+)\s?(million|billion|M\b|B\b|bn\b)',snt,re.I)
                        if mm: fig=float(mm.group(1).replace(',',''))*(1e9 if mm.group(2).lower() in ('billion','b','bn') else 1e6); sn=snt.strip()[:300]; break
                ne,es=emp_sent(t,toks)
                if ne and not out['employees']: out['employees']={'value':ne,'span':es,'url':u,'read':TODAY,'flag':'employee count \u2014 recorded, not a size reading'}
                if fig: out['figure']={'value':fig,'span':sn,'url':u,'read':TODAY,'source':'trade press'}; got='figure found'; break
                got='article(s) read; no sentence naming the company with a revenue figure (deal values excluded)'
            out['routes'].append({'route':label,'result':got})
        for c in held:
            out=R['revenue'][c]; k=next((k for k,e in Q.items() if e.get('company')==c and (e.get('test1_pass') or e.get('site_route'))),None)
            if out['figure'] and k:
                e=Q[k]; ceil=1e8 if e['practice']=='Private Equity' else 25e6; v=out['figure']['value']; e['band']={'in_band':v<=ceil,'why':f"published revenue {v:.0f} vs {ceil:.0f} (Src: {out['figure']['url']} \u00b7 read {TODAY})",'figure':out['figure']}
                e['status']='ADMITTED BY TEST (1, 2, 5, band) \u2014 Unverified, awaiting the Chair\u2019s tests 3 and 4' if v<=ceil else 'band-rejected at test 1: published revenue above the ceiling'
                if v<=ceil: R['admitted_by_test'].append(k)
            if out['employees'] and k: Q[k]['employees_published']=out['employees']
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    try:
        done=set(json.load(open('reports/w9-engine.json'))['per_query'])|set(json.load(open('reports/w10-engine.json'))['per_query'])|set(json.load(open('reports/w11-engine.json'))['per_query'])|set(json.load(open('reports/w12-engine.json'))['per_query'])|set(json.load(open('reports/w13-engine.json'))['per_query'])|set(e['source'] for e in [])
        for i_ in INDUSTRIES:
            for m_ in METROS[:6]: QP['Acquisitions'].append(f'"{m_}" {i_} company acquires')
        for m_ in METROS[5:]: QP['Fractionals'].append(f'"{m_}" company names CFO'); QP['Private Equity'].append(f'"{m_}" "private equity" acquires')
        for i_ in INDUSTRIES:
            for m_ in METROS[6:]: QP['Acquisitions'].append(f'"{m_}" {i_} company acquires')
            QP['Private Equity'].append(f'Florida {i_} "private equity" platform'); QP['Fractionals'].append(f'Florida {i_} company names CFO')
        # 4-5 · the precondition (proved before this pass) applied, then the queries
        seen={e.get('feed_title') for e in Q.values()}; queues={pr:[x for x in q if x not in done] for pr,q in QP.items()}
        await exec_discovery()
        await roster_probe()
        await directory_first()
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
                     seen.add(ttl); ok,span=CK('headline precondition',naming5.precondition(ttl)); naming9.is_abbrev.ctx=ttl; ok,span=(CK('property precondition (open test)',naming9.property_precondition2(ttl)) if ok else (ok,span))
                     if not ok: pq['precondition_stopped']+=1; R['disc']['precondition_stopped']+=1; continue
                     n+=1; a=await rd(pr,'gnews_rss:article',lk,'gnews_rss')
                     if not a[0]: continue
                     R['disc']['articles_read']+=1; pq['articles_read']+=1; d,f=pubdate(a[2]); t=T(a[2]); sent=next((s for s in re.split(r'(?<=[.!?])\s+',t) if re.search(practice.KW[pr],s,re.I) and re.search(r'\bFlorida\b|'+'|'.join(METROS),s)),None)
                     if not (d and sent): continue
                     R['disc']['florida_signal']+=1; R['disc']['reaching_binding']+=1; pq['florida_signal']+=1; pq['reaching_binding']+=1
                     k=f'{pr}:gnews_rss_w16:{len(Q)}'; e=Q[k]={'practice':pr,'source':'gnews_rss_w16','company':'','signal':{'sentence':sent[:400],'url':lk,'published':d,'read':TODAY},'date_field':f,'feed_title':ttl,'query':q,'precondition_span':span,'evidence_source':'signal','status':'proposed \u2014 unconfirmed'}
                     res=naming4.name4(ttl,a[2]); e['naming']=res; R['counts']['processed']+=1; st=res['state']
                     if st.startswith('rejected'): R['counts']['rejected']+=1; e['status']='rejected: span not a company \u2014 '+res.get('span_taken',''); continue
                     if st=='bind disputed': R['counts']['disputed']+=1; e['status']='bind disputed \u2014 held'; continue
                     if st=='unbound': R['counts']['unbound']+=1; R['counts']['unbound:'+res['split'][:20]]+=1; e['status']='unbound'; check(); continue
                     co,cnote=naming8.cleanup(res['company']); CK('name bounds (#52)',(co is not None,None))
                     if co and CK('abbreviation test (#56)',(not naming9.is_abbrev(co),None))[0] is False: co,cnote=None,'an abbreviation or ticker, not a name (fault 56)'
                     if co and CK('asset test (#57)',(not naming9.is_asset(co)[0],None))[0] is False: co,cnote=None,'an asset, not an entity (fault 57): '+naming9.is_asset(co)[1]
                     if not co: R['cleanup'].append({'bound':res['company'],'note':cnote}); R['counts']['rejected']+=1; e['status']='rejected: '+cnote+' \u2014 '+res['company']; continue
                     if cnote: R['cleanup'].append({'bound':res['company'],'kept':co,'note':cnote})
                     e.update(company=co,company_named='provisional until the site proves it',acquirer=res.get('acquirer'),city=res.get('city'))
                     ok2,why2=intake.test2_absent(co,None,day.idx); e['test2']=why2
                     if not ok2: e['status']='on file \u2014 a signal against the existing row'; continue
                     toks=[w.lower() for w in re.findall(r'[A-Za-z]{4,}',co) if w.lower() not in ('company','group','holdings','industries','florida','construction','services')]; cands=[]; tried=[]; pub=naming7.registrable(naming7.publisher_host(a[2],lk))
                     for m in re.finditer(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',a[2],re.S|re.I):
                         host=re.sub(r'^https?://(www\.)?','',m.group(1)).split('/')[0].lower(); txt=re.sub(r'<[^>]+>',' ',m.group(2)).lower()
                         if toks and (any(tk in host.replace('-','') for tk in toks) or toks[0] in txt) and 'news.google' not in host and naming7.registrable(host)!=pub: cands.append(('article link','https://'+host+'/')); break
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
                     if not site and any(x['outcome'].startswith('refused') for x in tried): R['disc']['refused_re_runnable']=R['disc'].get('refused_re_runnable',0)+1; e['status']='refused on a route (re-runnable) \u2014 not an absence'; continue
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
        R['directory']['AGC chapters']='parked under its code (404, window ten) \u2014 not re-probed'
        for k in [k for k,e in Q.items() if (e['source']=='suncap' and e.get('florida_on_card') and not e.get('routes_tried')) ]+[k for k,e in Q.items() if e['source']=='hig' and not e.get('entry_read') and e.get('sponsor_page')]:
            e=Q[k]; r=await rd('Private Equity','entry:'+e['source'],e['sponsor_page'],'entry:'+e['source'])
            if r[0] is None: break
            e['entry_read']=TODAY; R['pe']['entries']+=1
            if not r[0]: continue
            t=T(r[2]); m=re.search(r'(?:Headquarters|Location|HQ)\s*[:\-]?\s*([A-Z][A-Za-z .\-]+,\s*(?:FL|Florida|[A-Z]{2}|[A-Z][a-z]+))',t); lf=m.group(1) if m else None; e['location_field']=lf
            if e['source']=='hig' and not (lf and re.search(r'\bFL\b|Florida',lf)): continue
            R['pe']['florida']+=1; link=discovery.site_link(r[2],e['company']); tried=[]; site=page=pf=None
            for rt,url in ([('sponsor entry link',link)] if link else [])+[('derived host','https://www.'+h+'/') for h in naming4.derived_hosts(e['company'])]:
                s2=await rd('Private Equity','site:'+rt,url,'site:'+url)
                if s2[0] is None: tried.append({'route':rt,'host':url,'outcome':'not read'}); continue
                if s2[0] is False: tried.append({'route':rt,'host':url,'outcome':'did not resolve' if str(s2[1]) in ('net','timeout') else f'refused ({s2[1]})'}); continue
                pf=naming8.prove_site8(s2[2],e['company'],re.sub(r'^https?://','',url).split('/')[0])
                if pf=='challenge': tried.append({'route':rt,'host':url,'outcome':'refused (challenge) \u2014 re-runnable'}); continue
                if not pf: tried.append({'route':rt,'host':url,'outcome':'resolved but failed the proof'}); continue
                tried.append({'route':rt,'host':url,'outcome':'proved'}); site,page=url,s2[2]; break
            e['routes_tried']=tried
            if not site: e['status']='no site found by any route \u2014 held'; R['pe']['no_site']+=1; continue
            e['site']=site; e['site_proof']=pf; tt=T(page); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',tt)[:2]); t1,why=intake.test1_florida({'url':site,'read':TODAY,'address_text':addr or tt[:300]}); e['test1']=why; e['test1_pass']=t1
            ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',tt); t5,ch=intake.test5_channel({'phone':{'value':ph.group(0),'url':site,'read':TODAY} if ph else None,'address':{'value':addr,'url':site,'read':TODAY} if addr else None}); e['test5']=ch; e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}
            if t1: R['pe']['test1_pass']+=1; e['status']='site proved; passes tests 1, 2'+(' and 5' if t5 else '')+'; held size-unsourced'
        mk=None
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
    R['checks']={k:dict(v,reading=('never ran' if v['calls']==0 else ('stopped nothing' if v['stopped']==0 else f"stopped {v['stopped']}"))) for k,v in CHK.items()}
    for nm in ('headline precondition','property precondition (open test)','name bounds (#52)','abbreviation test (#56)','asset test (#57)'): R['checks'].setdefault(nm,{'calls':0,'stopped':0,'reading':'NEVER RAN (0 calls)'})
    R['spent']=dict(spent); R['budget']=budget; R['counts']=dict(R['counts']); R['pe']=dict(R['pe']); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/w16-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],R['counts'],dict(spent))
    await b.close(); await p.stop()
asyncio.run(go())
