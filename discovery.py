"""discovery.py — Item 320 second edition, Chunk C: discovery day one as one pass. Reads only the sources declared in practice-classes.json
['discovery'], through the attended browser (undisguised), under bot.py's containment (shared ceiling by the run's UTC start date, kill switch
before and after every read, append-only log). Thirds split per practice; round-robin one source per practice per round; a source that refuses,
whose probe fails or whose reader crashes stops that source only. Every candidate lands in florida-intake-queue.json unconfirmed. Nothing here
admits a row, writes a working file, or sends."""
import json,re,sys,os,time,datetime,asyncio,html,urllib.parse
import bot,practice,intake
C=json.load(open('practice-classes.json')); D=C['discovery']; BAND=C['band']; TODAY=datetime.date.today().isoformat()
UA='DashRite-Advisory-attended-reader/1.0 (research; contact TEdick@dashriteadvisory.com)'
PRACTICES=['Private Equity','Acquisitions','Fractionals']
def card_text(body,a,b):
    """The text of the smallest element enclosing the anchor (li, article, div or tr), bounded by its own tags; never the neighbours."""
    for tag in ('li','article','tr','div'):
        o=body.rfind('<'+tag,0,a); c=body.find('</'+tag+'>',b)
        if o!=-1 and c!=-1 and c-o<4000 and body.count('<'+tag,o+1,a)==body.count('</'+tag+'>',o+1,a): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',body[o:c])))
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',body[a:b])))
def site_link(body,company):
    """The company's own site from a sponsor's company page: an anchor whose text says website/visit/www, or whose host matches the company's slug tokens; site-wide and portal links excluded. None if none qualifies (never the first external href)."""
    toks=[w.lower() for w in re.findall(r'[A-Za-z]{4,}',company)][:2]; deny=('fiscloudservices','linkedin','twitter','facebook','youtube','instagram','google','wp.com','gravatar','wordpress','x.com','vimeo','apple.com','mailto','hig.com','suncappart','trivest','comvest','boynecapital')
    best=None
    for m in re.finditer(r'<a\b[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>',body,re.S|re.I):
        u=m.group(1); t=re.sub(r'<[^>]+>',' ',m.group(2)).strip().lower()
        if any(x in u.lower() for x in deny) or re.search(r'\.(png|jpg|svg|css|js|pdf)(\?|$)',u): continue
        host=re.sub(r'^https?://(www\.)?','',u).split('/')[0].lower()
        if re.search(r'website|visit|www\.',t) or t==host: return u
        if toks and any(tk in host.replace('-','') for tk in toks): best=best or u
    return best
FL=r'\bFL\b|\bFlorida\b|Miami|Tampa|Orlando|Jacksonville|Fort Lauderdale|Boca Raton|West Palm|Naples|Sarasota|Doral|Coral Gables|St\. Petersburg|Clearwater|Pompano|Hialeah|Tallahassee|Gainesville|Pensacola|Lakeland|Daytona|Melbourne|Ocala|Fort Myers|Hollywood, FL|Deerfield|Jupiter|Stuart|Vero Beach'
def items(src,body):
    """Items on a source page: anchors whose href matches the source's declared pattern (derived from the live form); the name is the anchor's text with tags stripped, else the href's slug in words. Nothing is guessed: the name comes from the page's own link."""
    pat=src['item_pattern']; out=[]; seen=set()
    for m in re.finditer(r'<a\b[^>]*href="('+pat+r')"[^>]*>(.*?)</a>',body,re.S|re.I):
        u=html.unescape(m.group(1)); 
        if re.search(r'[<>\s]|&sa=|&ved=|/feed/?$|oembed',u) or u in seen: continue
        seen.add(u); t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',m.group(2)))).strip()
        if not t or len(t)>90 or re.fullmatch(r'(active|exited|realized|current|former|view|read more|learn more|visit|website)',t,re.I): t=re.sub(r'[-_]+',' ',u.rstrip('/').split('/')[-1].replace('portfolio-','')).strip().title()
        card=card_text(body,m.start(),m.end())
        rev=re.search(r'\$\s?([\d.,]+)\s?(million|M|billion|B)\b',card,re.I); fig=float(rev.group(1).replace(',',''))*(1e9 if rev.group(2).lower().startswith('b') else 1e6) if rev else None
        out.append((u,t,bool(re.search(FL,card)),card[:300],fig))
    return out
class Day:
    def __init__(s,market,attended,read_fn,log_fn=None):
        s.market=market; s.attended=attended; s.read=read_fn; s.q=market+'-intake-queue.json'; s.Q=json.load(open(s.q)) if os.path.exists(s.q) else {}
        s.idx=intake.index_files('*.html'); s.spent={p:0 for p in PRACTICES}; s.third=D['thirds']['per_practice']
        s.rep={'date_utc':TODAY,'run_start_utc':None,'run_end_utc':None,'straddled_midnight_utc':False,'reads_total':0,'reads_by_practice':{},'reads_by_source':{},'refusals_by_source':{},'probes':{},'sources_state':{},'candidates':{'examined':0,'queued':0,'by_practice':{},'by_source':{}},'filtered_non_companies':[],'band_rejected':[],'size_unsourced':0,'unusable':[],'on_file_signals':[],'stopped':None,'stopped_at':None}
    async def one_read(s,practice_,src_id,url):
        if bot.killed(): raise bot.Halted(f'kill switch present \u2014 before a read ({practice_}/{src_id})')
        if bot.reads_today()>=bot.CEILING: raise bot.Refused(f'ceiling {bot.CEILING} reached before {practice_}/{src_id}')
        if s.spent[practice_]>=s.third: return None,'third spent',None
        await asyncio.sleep(2.0)
        t0=time.time(); code,body,final=await s.read(url); ok=isinstance(code,int) and code<400
        bot.log({'kind':'read','practice':practice_,'source':src_id,'url':url,'outcome':'read' if ok else 'refused','kind_detail':None if ok else str(code),'elapsed':round(time.time()-t0,2),'reader':'browser'})
        s.spent[practice_]+=1; s.rep['reads_total']+=1; s.rep['reads_by_practice'][practice_]=s.rep['reads_by_practice'].get(practice_,0)+1; s.rep['reads_by_source'][src_id]=s.rep['reads_by_source'].get(src_id,0)+1
        if not ok: s.rep['refusals_by_source'][src_id]=s.rep['refusals_by_source'].get(src_id,{}); s.rep['refusals_by_source'][src_id][str(code)]=s.rep['refusals_by_source'][src_id].get(str(code),0)+1
        if bot.killed(): raise bot.Halted(f'kill switch present \u2014 after a read ({practice_}/{src_id})')
        return ok,code,body
    def queue_candidate(s,practice_,src,name,signal_url,sentence,published,company_url=None):
        s.rep['candidates']['examined']+=1
        dom=intake.host_of(company_url) if company_url else None
        nc=intake.non_company(dom) if dom else None
        if nc: s.rep['filtered_non_companies'].append({'name':name,'domain':dom,'class':nc}); return 'filtered'
        ok2,why2=intake.test2_absent(name,dom,s.idx) if name else (True,'no name to check')
        if not ok2: s.rep['on_file_signals'].append({'name':name,'practice':practice_,'source':src['id'],'signal_url':signal_url,'why':why2}); return 'on file'
        key=f'{practice_}:{src["id"]}:{len([k for k in s.Q if k.startswith(practice_+":"+src["id"])])}'
        s.Q[key]={'practice':practice_,'source':src['id'],'company':name or '','company_named':bool(name),'signal':{'sentence':sentence[:400],'url':signal_url,'published':published,'read':TODAY},'evidence_source':'signal','company_url':company_url,'test1':None,'test2':why2,'band':None,'status':'proposed \u2014 unconfirmed','tests_3_4':None}
        s.rep['candidates']['queued']+=1; s.rep['candidates']['by_practice'][practice_]=s.rep['candidates']['by_practice'].get(practice_,0)+1; s.rep['candidates']['by_source'][src['id']]=s.rep['candidates']['by_source'].get(src['id'],0)+1
        return key
    async def test1(s,key):
        e=s.Q[key]
        if not e.get('company_url') and e.get('sponsor_page'): e['company_url']=e['sponsor_page']
        if not e.get('company_url'): e['test1']='no company page known \u2014 read on a later day once named'; return
        sponsor_hosts=('hig.com','suncappart.com','trivest.com','comvest.com','boynecapital.com')
        if any(h in e['company_url'] for h in sponsor_hosts):
            r=await s.one_read(e['practice'],'test1:'+e['source'],e['company_url'])
            if r[0] is None: e['test1']='not read: '+r[1]; return
            ok,code,body=r
            if not ok: e['test1']=f'sponsor company page refused ({code}) \u2014 re-runnable'; return
            ext=[u for u in re.findall(r'href="(https?://[^"]+)"',body) if not any(h in u for h in sponsor_hosts+('linkedin.com','twitter.com','facebook.com','youtube.com','instagram.com','google.com','wp.com','gravatar','wordpress','x.com')) and not re.search(r'\.(png|jpg|svg|css|js|pdf)(\?|$)',u)]
            txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',body))); e['sponsor_page_text_fl']=bool(re.search(r'\bFL\b|\bFlorida\b',txt))
            if not ext: e['test1']='sponsor page names no company site; Florida on the sponsor page: '+str(e['sponsor_page_text_fl'])+' (not the company\u2019s own page \u2014 test 1 not settled)'; return
            e['company_url']=ext[0]
        r=await s.one_read(e['practice'],'test1:'+e['source'],e['company_url'])
        if r[0] is None: e['test1']='not read: '+r[1]; return
        ok,code,body=r
        if not ok: e['test1']=f'company page refused ({code}) \u2014 re-runnable'; return
        txt=html.unescape(re.sub(r'<[^>]+>',' ',body)); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',txt)[:2])
        t1,why=intake.test1_florida({'url':e['company_url'],'read':TODAY,'address_text':addr or txt[:300]}); e['test1']=why; e['test1_pass']=t1
        m=re.search(r'\$\s?([\d.,]+)\s?(million|M|billion|B)\b',txt,re.I)
        if m:
            fig=float(m.group(1).replace(',',''))*(1e9 if m.group(2).lower().startswith('b') else 1e6); b,w=intake.band_check({'revenue_figure':fig,'revenue_source':{'url':e['company_url'],'read':TODAY}},BAND); e['band']={'in_band':b,'why':w}
            if b is False: s.rep['band_rejected'].append({'key':key,'why':w})
        else: e['band']={'in_band':None,'why':intake.SIZE_UNSOURCED}; s.rep['size_unsourced']+=1
    async def run_source(s,practice_,src,round_no):
        st=s.rep['sources_state'].setdefault(src['id'],{'state':'not yet read','reads':0}); 
        if st['state'].startswith('refused') or st['state']=='exhausted' or st['state']=='probe failed': return
        if src['kind']=='portfolio page':
            if st['reads']: st['state']='exhausted'; return
            r=await s.one_read(practice_,src['id'],src['route']); st['reads']+=1
            if r[0] is None: st['state']='third spent'; return
            ok,code,body=r
            if not ok: st['state']=f'refused by source ({code})'; return
            its=items(src,body); st['state']=f'read: {len(its)} portfolio companies named, {sum(1 for x in its if x[2])} with a Florida mention on the card'
            for u,t,fl in its:
                k=s.queue_candidate(practice_,src,t,src['route'],f'{t} is named on {src["name"]}\u2019s portfolio page{" (card mentions Florida)" if fl else ""}.',TODAY,None)
                if k not in ('filtered','on file'): s.Q[k]['sponsor']=src['name']; s.Q[k]['sponsor_page']=u; s.Q[k]['florida_on_card']=fl
        elif src['kind'] in ('site search','job board search'):
            qs=src.get('queries',[]); i=st['reads']
            if i>=len(qs): st['state']='exhausted'; return
            q=qs[i]; url=src['route'].format(q=urllib.parse.quote(q),n=8+len(q)); r=await s.one_read(practice_,src['id'],url); st['reads']+=1
            if r[0] is None: st['state']='third spent'; return
            ok,code,body=r
            if not ok: st['state']=f'refused by source ({code})'; return
            its=items(src,body); st['state']=f'read {i+1} of {len(qs)} queries; last gave {len(its)} items'
            for u,t in its[:3]:
                if src['kind']=='site search':
                    r2=await s.one_read(practice_,src['id'],u)
                    if r2[0] is None: break
                    ok2,code2,body2=r2
                    if not ok2: continue
                    d=practice.pub_date(body2); txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',body2)))
                    sent=next((x.strip() for x in re.split(r'(?<=[.!?])\s+',txt) if re.search(practice.KW['Acquisitions'],x,re.I) and re.search(r'\bFlorida\b|\bFL\b',x)),None)
                    if d and sent: s.queue_candidate(practice_,src,None,u,sent,d,None)
                    elif not d: s.rep['unusable'].append({'url':u,'why':'no publication date'})
                else: s.queue_candidate(practice_,src,t or None,u,f'{t} \u2014 {q} posting in Florida on {src["name"]}.',TODAY,None)
        elif src['kind']=='listing index':
            if st['reads']: st['state']='exhausted'; return
            r=await s.one_read(practice_,src['id'],src['route']); st['reads']+=1
            if r[0] is None: st['state']='third spent'; return
            ok,code,body=r
            if not ok: st['state']=f'refused by source ({code})'; return
            its=items(src,body); st['state']=f'read: {len(its)} listings'
            for u,t in its:
                if not re.search(r'\b(Inc|LLC|Corp|Co\.|Company|Group)\b',t): s.rep['unusable'].append({'url':u,'why':'listing names no company \u2014 unusable, never guessed'})
                else: s.queue_candidate(practice_,src,t,u,f'{t} is listed for sale in Florida on BizBuySell.',TODAY,None)
        json.dump(s.Q,open(s.q,'w'),indent=1,ensure_ascii=False)
    async def run(s):
        bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); s.rep['run_start_utc']=bot.RUN_START
        bot.log({'kind':'run','market':s.market,'reader':'browser','attended_by':s.attended,'outcome':'start','run_start_utc':bot.RUN_START,'chunk':'C'})
        try:
            for rnd in range(1,60):
                live=False
                for p in PRACTICES:
                    for src in D['practices'][p]['sources']:
                        st=s.rep['sources_state'].get(src['id'],{}).get('state','not yet read')
                        if st.startswith(('refused','stopped','parked')) or st in ('exhausted','probe failed','third spent'): continue
                        await s.run_source(p,src,rnd); live=True; break
                if not live: break
            for k in sorted([k for k,e in s.Q.items() if e.get('test1') is None],key=lambda k:(not s.Q[k].get('florida_on_card'),k)): await s.test1(k)
            s.rep['stopped']='completed: every source read, refused or exhausted'
        except bot.Refused as e: s.rep['stopped']='ceiling'; s.rep['stopped_at']=str(e)
        except bot.Halted as e: s.rep['stopped']='kill switch'; s.rep['stopped_at']=str(e)
        json.dump(s.Q,open(s.q,'w'),indent=1,ensure_ascii=False); s.rep['run_end_utc']=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); s.rep['straddled_midnight_utc']=s.rep['run_end_utc']!=s.rep['run_start_utc']; s.rep['thirds_spent']=s.spent
        bot.log({'kind':'run','market':s.market,'reader':'browser','outcome':s.rep['stopped'],'stopped_at':s.rep['stopped_at'],'reads':s.rep['reads_total']}); return s.rep
async def browser_reader():
    from playwright.async_api import async_playwright
    p=await async_playwright().start(); b=await p.chromium.launch(args=['--no-sandbox','--disable-gpu']); ctx=await b.new_context(user_agent=UA)
    async def read(url):
        pg=await ctx.new_page()
        try: r=await pg.goto(url,timeout=25000,wait_until='domcontentloaded'); await pg.wait_for_timeout(1500); code=r.status if r else 'net'; body=await pg.content(); final=pg.url
        except Exception as e: code,body,final=('timeout' if 'Timeout' in type(e).__name__ else 'net'),'',url
        await pg.close(); return code,body,final
    return read,b,p
