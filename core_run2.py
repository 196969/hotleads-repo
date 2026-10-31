import asyncio,json,re,html,datetime,collections,hashlib
import bot,discovery,intake,naming4,naming8,naming10,officer
TODAY=discovery.TODAY
D=json.load(open('sources-run2.json')); R={'run':'core build run two','launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'probes':{},'warn':{},'florida_trend':{},'admitted':[],'candidates':[],'stopped':None}
def T(b): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',b or '',flags=re.S|re.I))))
TITLE=r'(Chief Executive Officer|CEO|President|Founder|Co-Founder|Owner|Managing Director|General Manager|Chief Financial Officer|CFO|Chief Operating Officer|COO)'
def own_page_dm(text):
    for m in re.finditer(r"\b([A-Z][a-zA-Z'\-]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+)\s*(?:,|\u2013|\u2014|-|\|)\s*(?:the |our )?"+TITLE+r'\b',text):
        if naming10.is_person(m.group(1)): return {'name':m.group(1),'title':m.group(2),'span':text[max(0,m.start()-40):m.end()+20]}
    return None
async def go():
    read0,b,p=await discovery.browser_reader()
    async def read(url):
        code,body,final=await read0(url)
        if isinstance(code,int) and code<400 and naming8.is_challenge(body): return 'challenge',body,final
        return code,body,final
    day=discovery.Day('florida','Timothy A. Edick',read); Q=day.Q=json.load(open('florida-intake-queue.json')); day.third=10**6
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); spent=collections.Counter(); budget={'Probes':80,'Candidates':100}
    for k in budget: day.spent[k]=0
    hostrefusals=collections.Counter(); closed=set()
    async def rd(pr,source,url):
        host=re.sub(r'^https?://(www\.)?','',url).split('/')[0]
        if host in closed: return None,'closed (three refusals on this host)',None
        if spent[pr]>=budget[pr]: return None,'budget',None
        r=await day.one_read(pr,source,url); spent[pr]+=1
        if r[0]: hostrefusals[host]=0; open(f'run2-bodies/{hashlib.sha1(url.encode()).hexdigest()[:12]}.html','w').write(r[2] or '')
        elif r[0] is False:
            hostrefusals[host]+=1
            if hostrefusals[host]>=3: closed.add(host)
        return r
    try:
        for win in ('w20','w21','w22'):
            for name,url,cls in D[win]:
                r=await rd('Probes','probe:'+name,url)
                rec={'window':win,'class':cls,'url':url,'reads':1 if r[0] is not None else 0}
                if r[0] is None: rec.update(state='unread',note=str(r[1])); R['probes'][name]=rec; continue
                if r[0] is False: rec.update(state='refused',refused={str(r[1]):1},answered=0); R['probes'][name]=rec; continue
                t=T(r[2]); fl=len(re.findall(r'\b[A-Z][a-zA-Z .]+,\s*(?:FL|Florida)\b',t)); names=len(set(re.findall(r'\b[A-Z][\w&\'.-]+(?: [A-Z][\w&\'.-]+){0,3} (?:Inc|LLC|Corp|Company|Co)\.?\b',t)))
                login=bool(re.search(r'(?i)sign in to (?:view|see)|log ?in to (?:view|continue)|members only|subscribe to (?:read|continue)',t))
                rec.update(state='answering',answered=1,bytes=len(r[2]),florida_city_pairs=fl,legal_suffix_names=names,login_wall=login,
                    reading=('ROSTER SHAPE: Florida cities on the page\u2019s face' if fl>=10 else ('answered behind a login or subscription wall' if login else ('answered; company names on the page' if names>=5 else 'answered; a publication or front page, not a roster'))))
                R['probes'][name]=rec
                if name=='Florida Trend':
                    arts=list(dict.fromkeys(re.findall(r'href="(https?://(?:www\.)?floridatrend\.com/article/\d+/[^"]*)"',r[2])))[:1]
                    for u in arts:
                        a=await rd('Probes','floridatrend:article',u)
                        if a[0]:
                            m=re.search(r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)',a[2]) or re.search(r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)',a[2]) or re.search(r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)',a[2])
                            R['florida_trend']={'article':u,'structured_date':m.group(1) if m else None,'reading':'reopened under the structured-metadata date rule' if m else 'no structured date on the article read \u2014 stays stopped'}
                if name=='FloridaCommerce WARN' and r[0]:
                    rows=re.findall(r'<tr[^>]*>(.*?)</tr>',r[2],re.S); notices=[]
                    for row in rows:
                        c=[T(x) for x in re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)]
                        if len(c)>=3 and re.search(r'\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d\d-\d\d',' '.join(c)): notices.append(c[:6])
                    R['warn']={'rows_with_a_date':len(notices),'sample':notices[:5]}
        R['stopped']='completed: every declared source in windows 20\u201322 read once on its live form'
    except (bot.Refused,bot.Halted) as x: R['stopped']='ceiling or kill switch: '+str(x)
    R['spent']=dict(spent); R['closed_hosts']=sorted(closed); R['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(R,open('reports/core-run2-engine.json','w'),indent=1,ensure_ascii=False); print('DONE',R['stopped'],dict(spent))
    await b.close(); await p.stop()
asyncio.run(go())
