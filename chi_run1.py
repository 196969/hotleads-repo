import asyncio,json,re,html,datetime,collections,hashlib
import bot,discovery,naming4,naming8,naming10,officer
TODAY=discovery.TODAY; W=json.load(open('chi-work.json')); R={'run':'Chicago and Illinois, Step Two window one','launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':[],'stopped':None}
def T(b): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',b or '',flags=re.S|re.I))))
TITLE=r'(Chief Executive Officer|CEO|President|Founder|Co-Founder|Owner|Managing Director|General Manager|Chief Financial Officer|CFO|Chief Operating Officer|COO|Principal|Managing Partner)'
ROLE=re.compile(r'^(info|sales|contact|hello|office|admin|support|service|customerservice|orders|inquiries|team|hr|careers|marketing)$',re.I)
def own_dm(t):
    for m in re.finditer(r"\b([A-Z][a-zA-Z'\-]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+)\s*(?:,|\u2013|\u2014|-|\||\s)\s*(?:the |our )?"+TITLE+r'\b',t):
        if naming10.is_person(m.group(1)): return {'name':m.group(1),'title':m.group(2),'span':t[max(0,m.start()-30):m.end()+20]}
    for m in re.finditer(TITLE+r"\s*(?:,|\u2013|\u2014|-|:)?\s*([A-Z][a-zA-Z'\-]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+)",t):
        if naming10.is_person(m.group(2)): return {'name':m.group(2),'title':m.group(1),'span':t[max(0,m.start()-30):m.end()+20]}
    return None
def contact(t,host):
    ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',t)
    ems=[z for z in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',t) if not re.search(r'\.(png|jpg|svg|webp|gif)$',z) and 'sentry' not in z and 'example' not in z]
    em=next((z for z in ems if host.split('.')[-2] in z.split('@')[1]),ems[0] if ems else None)
    return (ph.group(0) if ph else None),em
async def go():
    read0,b,p=await discovery.browser_reader()
    async def read(url):
        code,body,final=await read0(url)
        if isinstance(code,int) and code<400 and naming8.is_challenge(body): return 'challenge',body,final
        return code,body,final
    day=discovery.Day('florida','Timothy A. Edick',read); day.Q={}; day.third=10**6; bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    day.spent['Completion']=0; spent=[0]; refusals=collections.Counter(); closed=set()
    async def rd(url,source):
        host=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
        if host in closed: return None,'host closed (three refusals on this host)',None
        if spent[0]>=196: return None,'budget',None
        r=await day.one_read('Completion',source,url); spent[0]+=1
        if r[0]: refusals[host]=0; open(f'run3-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')
        elif r[0] is False:
            refusals[host]+=1
            if refusals[host]>=3: closed.add(host)
        return r
    try:
        for w in W:
            co=w['name']; rec={'company':co,'source':w['source'],'key':w['key'],'missing':w['missing'],'routes':[],'found':{}}
            site=w['site']; page=None
            cands=([('row site link',site)] if site else [])+[('derived host','https://www.'+h+'/') for h in naming4.derived_hosts(re.sub(r'\(.*?\)','',co))]
            for rt,u in cands:
                r=await rd(u,'run3:site')
                if r[0] is None: rec['routes'].append({'route':rt,'host':u,'outcome':'not read: '+str(r[1])}); continue
                if not r[0]: rec['routes'].append({'route':rt,'host':u,'outcome':f'refused ({r[1]})'}); continue
                pf=naming8.prove_site8(r[2],re.sub(r'\(.*?\)','',co).strip(),re.sub(r'^https?://','',u).split('/')[0])
                if not isinstance(pf,dict) and rt!='row site link': rec['routes'].append({'route':rt,'host':u,'outcome':'resolved but failed the proof'}); continue
                rec['routes'].append({'route':rt,'host':u,'outcome':'read'+(' (proved)' if isinstance(pf,dict) else ' (the row\u2019s own site link)')}); site,page=u,r[2]; break
            if page:
                host=re.sub(r'^https?://(www\.)?','',site).split('/')[0]; t=T(page)
                links=[]
                for m in re.finditer(r'<a\b[^>]*href="([^"#]+)"[^>]*>(.*?)</a>',page,re.S|re.I):
                    u=m.group(1); tx=re.sub(r'<[^>]+>',' ',m.group(2)).lower()+' '+u.lower()
                    if u.startswith('/'): u='https://'+host+u
                    if host in u: links.append((tx,u))
                if 'published phone or email with a dated Src:' in w['missing']:
                    ph,em=contact(t,host); src=site
                    if not (ph or em):
                        cu=next((u for tx,u in links if re.search(r'contact|locations|find us',tx)),None)
                        if cu:
                            r=await rd(cu,'run3:contact'); rec['routes'].append({'route':'contact page','host':cu,'outcome':'read' if r[0] else (f'refused ({r[1]})' if r[0] is False else 'not read: '+str(r[1]))})
                            if r[0]: ph,em=contact(T(r[2]),host); src=cu
                    if ph or em: rec['found']['contact']={'phone':ph,'email':em,'role_inbox':bool(em and ROLE.match(em.split('@')[0])),'src':src,'read':TODAY}
                if 'named decision maker with title' in w['missing']:
                    dm=own_dm(t); src=site
                    if not dm:
                        for lu in [u for tx,u in links if re.search(r'leadership|our team|\bteam\b|management|executive|about|who we are|history',tx)][:2]:
                            r=await rd(lu,'run3:leadership'); rec['routes'].append({'route':'leadership/about page','host':lu,'outcome':'read' if r[0] else (f'refused ({r[1]})' if r[0] is False else 'not read: '+str(r[1]))})
                            if r[0]:
                                dm=own_dm(T(r[2])); src=lu
                                if dm: break
                    if dm: rec['found']['dm']=dict(dm,src=src,read=TODAY,source='the company\u2019s own page')
            if 'named decision maker with title' in w['missing'] and 'dm' not in rec['found']:
                n=re.sub(r'\(.*?\)','',co).strip(); r=await rd('https://news.google.com/rss/search?q='+re.sub(' ','%20','"'+n+'" (president OR CEO OR owner OR founder)')+'&hl=en-US&gl=US&ceid=US:en','run3:press')
                rec['routes'].append({'route':'trade press (officer.py)','host':'news.google.com','outcome':'read' if r[0] else (f'refused ({r[1]})' if r[0] is False else 'not read: '+str(r[1]))})
                if r[0]:
                    for u in [html.unescape(x) for x in re.findall(r'<link>(.*?)</link>',r[2])][1:3]:
                        r2=await rd(u,'run3:press-article')
                        if r2[0]:
                            d=officer.bind(T(r2[2]),n)
                            if d: rec['found']['dm']=dict(d,src=u,read=TODAY,source='trade press, bound by one clause\u2019s grammar'); break
            need=set(w['missing']); got={'published phone or email with a dated Src:' if 'contact' in rec['found'] else None,'named decision maker with title' if 'dm' in rec['found'] else None}
            if need<=got: rec['state']='completed'
            elif rec['routes'] and all(x['outcome'].startswith('refused') or 'closed' in x['outcome'] for x in rec['routes']): rec['state']='measured shut'
            else: rec['state']='partial'; rec['remaining_routes']=['Sunbiz officer list (refuses this reader, 403)','LinkedIn company page (refuses this reader, 999)']
            rec['reads']=len([x for x in rec['routes'] if not x['outcome'].startswith('not read')]); R['rows'].append(rec)
            json.dump(R,open('reports/chi-run1-engine.json','w'),indent=1,ensure_ascii=False)
        R['stopped']='completed: the whole queue worked'
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    R['spent']=spent[0]; R['closed_hosts']=sorted(closed); json.dump(R,open('reports/chi-run1-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],spent[0],collections.Counter(r['state'] for r in R['rows']))
    await b.close(); await p.stop()
asyncio.run(go())
