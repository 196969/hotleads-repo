"""practice_browser.py — the attended browser reader (Item 320 Part 10). Same pipeline as practice.py, read through a real browser at a human
cadence, under bot.py's containment (one shared daily ceiling, kill switch, append-only log) and Part 8's standard. Each read is logged with its
reader. It is attended: it runs only while a named person is present (--attended NAME), pauses between reads, and identifies itself in its user
agent. A 403 is honoured as a refusal. Order comes from practice-classes.json run_order; it is never typed here."""
import json,re,sys,os,time,datetime,asyncio,html
import bot,practice
C=json.load(open('practice-classes.json')); ORDER=C['run_order']['class_order']; TODAY=datetime.date.today().isoformat()
SEARCH='https://html.duckduckgo.com/html/?q='
UA='DashRite-Advisory-attended-reader/1.0 (research; contact TEdick@dashriteadvisory.com)'
async def main(market,attended,cadence):
    from playwright.async_api import async_playwright
    rows=sorted(practice.pipeline(market),key=lambda r:int(r['key'])); qp=market+'-practice-queue.json'; Q=json.load(open(qp)) if os.path.exists(qp) else {}; rp=market+'-practice-reads.json'; RR=json.load(open(rp)) if os.path.exists(rp) else {}
    rep={'market':market,'date':TODAY,'reader':'browser (attended by '+attended+')','class_order':ORDER,'rows_in_pipeline':len(rows),'rows_reached':0,'reads_this_run':0,'reads_today_before_run':bot.reads_today(),'candidates':{},'classes_read':{},'refusals':{},'stopped':None}
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat()   # the ceiling's day is this run's UTC start date, across midnight (Part 11 ruling)
    rep['run_start_utc']=bot.RUN_START
    bot.log({'kind':'run','market':market,'reader':'browser','attended_by':attended,'outcome':'start','reads_today_before':bot.reads_today(),'run_start_utc':bot.RUN_START})
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--no-sandbox','--disable-gpu']); ctx=await b.new_context(user_agent=UA); st={}
        async def read(url):
            pg=await ctx.new_page()
            try: r=await pg.goto(url,timeout=25000,wait_until='domcontentloaded'); await pg.wait_for_timeout(1500); code=r.status if r else 'net'; body=await pg.content()
            except Exception as e: code,body='timeout' if 'Timeout' in type(e).__name__ else 'net',''
            await pg.close(); return code,body,(pg.url if False else url)
        try:
            for r in rows:
                RR.setdefault(r['key'],{'classes_read':{},'refusals':[]}); rep['rows_reached']+=1
                for cls in ORDER:
                    cl=C['source_classes'][cls]
                    if cl.get('reads_permitted')==0: RR[r['key']]['classes_read'][cls]='not read (0 reads permitted)'; continue
                    q=SEARCH+__import__('urllib.parse').parse.quote(f'{r["company"]} Florida '+('acquisition OR succession OR sold' if cls=='broker' else 'CFO OR controller OR "director of operations"' if cls=='job_board' else 'portfolio' if cls=='sponsor' else 'acquired OR acquisition OR CFO OR "private equity"'))
                    # one logged read per URL: the search, then up to two class-domain pages
                    if bot.killed(): raise bot.Halted('kill switch present — halted before a read')
                    code,body,f=await read(q); bot.log({'kind':'read','row':r['key'],'url':q,'outcome':'read' if isinstance(code,int) and code<400 else 'refused','kind_detail':None if isinstance(code,int) and code<400 else str(code),'elapsed':None,'reader':'browser'}); rep['reads_this_run']+=1
                    if bot.reads_today()>=bot.CEILING: raise bot.Refused(f'ceiling: {bot.reads_today()} reads today')
                    if bot.killed(): raise bot.Halted('kill switch present')
                    if not (isinstance(code,int) and code<400) or 'uddg=' not in body: RR[r['key']]['classes_read'][cls]='search refused'; rep['refusals']['search refused']=rep['refusals'].get('search refused',0)+1; await asyncio.sleep(cadence); continue
                    hits=[html.unescape(__import__('urllib.parse').parse.unquote(m)) for m in re.findall(r'uddg=([^&"]+)',body)]; hits=[h for h in hits if practice.class_of(h)==cls][:2]
                    RR[r['key']]['classes_read'][cls]=f'read {TODAY} (browser): {len(hits)} class hit(s)'
                    for h in hits:
                        await asyncio.sleep(cadence)
                        if bot.killed(): raise bot.Halted('kill switch present — halted before a read')
                        t0=time.time(); code,body,f=await read(h); ok=isinstance(code,int) and code<400
                        bot.log({'kind':'read','row':r['key'],'url':h,'outcome':'read' if ok else 'refused','kind_detail':None if ok else str(code),'elapsed':round(time.time()-t0,2),'reader':'browser'}); rep['reads_this_run']+=1
                        if bot.reads_today()>=bot.CEILING: raise bot.Refused(f'ceiling: {bot.reads_today()} reads today')
                        if bot.killed(): raise bot.Halted('kill switch present')
                        if not ok: RR[r['key']]['refusals'].append({'url':h,'why':f'page refused ({code}) — browser'}); rep['refusals'][f'page refused ({code})']=rep['refusals'].get(f'page refused ({code})',0)+1; continue
                        for crit in cl['criteria']:
                            cand,why=practice.candidate(r,crit,cls,h,body)
                            if cand: cand['reader']='browser'; Q[f'{r["key"]}:{crit}:{len([k for k in Q if k.startswith(r["key"]+":"+crit)])}']=cand; rep['candidates'][crit+'/'+cls]=rep['candidates'].get(crit+'/'+cls,0)+1
                            else: RR[r['key']]['refusals'].append({'url':h,'criterion':crit,'why':why}); rep['refusals'][why.split(':')[0]]=rep['refusals'].get(why.split(':')[0],0)+1
                    json.dump(Q,open(qp,'w'),indent=1,ensure_ascii=False); json.dump(RR,open(rp,'w'),indent=1,ensure_ascii=False); await asyncio.sleep(cadence)
                # not read -> no signal found only when all four permitted classes returned a read for the row
                cr=RR[r['key']]['classes_read']; permitted=[c for c in ORDER if C['source_classes'][c].get('reads_permitted')!=0]
                if all(str(cr.get(c,'')).startswith('read') for c in permitted) and not any(k.startswith(r['key']+':') for k in Q): RR[r['key']]['derivable']='no signal found (all four classes read, nothing returned)'; rep['classes_read'][r['key']]=cr
            rep['stopped']='completed'
        except bot.Refused as e: rep['stopped']='ceiling: '+str(e)
        except bot.Halted as e: rep['stopped']='kill switch: '+str(e)
        await b.close()
    rep['run_end_utc']=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); rep['straddled_midnight_utc']=rep['run_end_utc']!=rep['run_start_utc']
    rep['reads_today_after_run']=bot.reads_today(); bot.log({'kind':'run','market':market,'reader':'browser','outcome':rep['stopped'],'reads':rep['reads_this_run']})
    json.dump(rep,open('bot-report-part10.json','w'),indent=1); print(json.dumps(rep))
if __name__=='__main__':
    a=sys.argv; name=a[a.index('--attended')+1] if '--attended' in a else None
    if not name: print('refused: the browser reader runs attended only — pass --attended NAME'); sys.exit(2)
    if bot.reads_today()>=bot.CEILING: print(f'refused before read 1: {bot.reads_today()} reads already in today\u2019s shared log (ceiling {bot.CEILING}); run on a clean day'); sys.exit(3)
    asyncio.run(main(a[1] if len(a)>1 and not a[1].startswith('--') else 'florida',name,float(a[a.index('--cadence')+1]) if '--cadence' in a else 6.0))
