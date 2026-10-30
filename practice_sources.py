"""practice_sources.py — Item 320 Part 12: each source's own site search, no provider in the middle. One reader per source, declared in
practice-classes.json under sources.trade_press.readers. Attended browser, the declared user agent, the kill switch before and after every read,
the shared ceiling honoured (one number per day, the run's UTC start date), every read logged with its reader and source. A refusal by a source is
logged as refused by source; the run moves on. Candidates (sentence, URL, publication date, source) enter the Practice queue unconfirmed."""
import json,re,sys,os,time,datetime,asyncio,html,urllib.parse
import bot,practice
C=json.load(open('practice-classes.json')); SRC=C['sources']['trade_press']; TODAY=datetime.date.today().isoformat()
UA='DashRite-Advisory-attended-reader/1.0 (research; contact TEdick@dashriteadvisory.com)'
def parse_results(src,body): return list(dict.fromkeys(html.unescape(m) for m in re.findall(SRC['readers'][src]['result_link'],body)))[:2]
async def main(market,attended,cadence,lo=1,hi=32):
    from playwright.async_api import async_playwright
    rows=sorted(practice.pipeline(market),key=lambda r:int(r['key']))[lo-1:hi]; qp=market+'-practice-queue.json'; Q=json.load(open(qp)) if os.path.exists(qp) else {}; rp=market+'-practice-reads.json'; RR=json.load(open(rp)) if os.path.exists(rp) else {}
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    rep={'market':market,'reader':'browser (attended by '+attended+')','run_start_utc':bot.RUN_START,'sources':SRC['order'],'rows_declared':[r['key'] for r in rows],'rows_reached':0,'reads_this_run':0,'reads_today_before_run':bot.reads_today(),'reads_by_source':{},'candidates':{},'refusals_by_source':{},'stopped':None,'stopped_at':None}
    bot.log({'kind':'run','market':market,'reader':'browser','attended_by':attended,'outcome':'start','run_start_utc':bot.RUN_START,'part':12})
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--no-sandbox','--disable-gpu']); ctx=await b.new_context(user_agent=UA)
        async def read(url):
            pg=await ctx.new_page()
            try: r=await pg.goto(url,timeout=25000,wait_until='domcontentloaded'); await pg.wait_for_timeout(1500); code=r.status if r else 'net'; body=await pg.content()
            except Exception as e: code,body='timeout' if 'Timeout' in type(e).__name__ else 'net',''
            await pg.close(); return code,body
        def logread(key,url,code,src,t0):
            ok=isinstance(code,int) and code<400; bot.log({'kind':'read','row':key,'url':url,'outcome':'read' if ok else 'refused','kind_detail':None if ok else str(code),'elapsed':round(time.time()-t0,2),'reader':'browser','source':src}); rep['reads_this_run']+=1; rep['reads_by_source'][src]=rep['reads_by_source'].get(src,0)+1; return ok
        def guard(key,src):
            if bot.killed(): raise bot.Halted(f'kill switch present — halted at row {key}, source {src}')
            if bot.reads_today()>=bot.CEILING: raise bot.Refused(f'ceiling {bot.CEILING} reached at row {key}, source {src}')
        try:
            for r in rows:
                RR.setdefault(r['key'],{'classes_read':{},'refusals':[],'sources_read':{}}); RR[r['key']].setdefault('sources_read',{}); RR[r['key']].setdefault('refusals',[]); rep['rows_reached']+=1
                for src in SRC['order']:
                    S=SRC['readers'][src]; q=S['search'].format(q=urllib.parse.quote(r['company']))
                    guard(r['key'],src); t0=time.time(); code,body=await read(q); ok=logread(r['key'],q,code,src,t0); guard(r['key'],src)
                    if not ok: RR[r['key']]['sources_read'][src]=f'search refused ({code}) {TODAY}'; rep['refusals_by_source'][src]=rep['refusals_by_source'].get(src,0)+1; await asyncio.sleep(cadence); continue
                    hits=parse_results(src,body); RR[r['key']]['sources_read'][src]=f'read {TODAY}: {len(hits)} result(s) parsed'
                    for h in hits:
                        await asyncio.sleep(cadence); guard(r['key'],src); t0=time.time(); code,body=await read(h); ok=logread(r['key'],h,code,src,t0); guard(r['key'],src)
                        if not ok: RR[r['key']]['refusals'].append({'url':h,'why':f'page refused ({code}) — {src}'}); rep['refusals_by_source'][src]=rep['refusals_by_source'].get(src,0)+1; continue
                        for crit in ('Acquisitions','Fractionals','Private Equity'):
                            cand,why=practice.candidate(r,crit,'trade_press',h,body)
                            if cand: cand.update(source=src,reader='browser'); Q[f'{r["key"]}:{crit}:{len([k for k in Q if k.startswith(r["key"]+":"+crit)])}']=cand; rep['candidates'][crit+'/'+src]=rep['candidates'].get(crit+'/'+src,0)+1
                            else: RR[r['key']]['refusals'].append({'url':h,'criterion':crit,'why':why})
                    json.dump(Q,open(qp,'w'),indent=1,ensure_ascii=False); json.dump(RR,open(rp,'w'),indent=1,ensure_ascii=False); await asyncio.sleep(cadence)
            rep['stopped']='completed'
        except bot.Refused as e: rep['stopped']='ceiling'; rep['stopped_at']=str(e)
        except bot.Halted as e: rep['stopped']='kill switch'; rep['stopped_at']=str(e)
        await b.close()
    json.dump(Q,open(qp,'w'),indent=1,ensure_ascii=False); json.dump(RR,open(rp,'w'),indent=1,ensure_ascii=False)
    rep['run_end_utc']=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); rep['straddled_midnight_utc']=rep['run_end_utc']!=rep['run_start_utc']; rep['reads_today_after_run']=bot.reads_today()
    bot.log({'kind':'run','market':market,'reader':'browser','outcome':rep['stopped'],'stopped_at':rep['stopped_at'],'reads':rep['reads_this_run']}); json.dump(rep,open('bot-report-part12-run.json','w'),indent=1); print(json.dumps(rep))
if __name__=='__main__':
    a=sys.argv; name=a[a.index('--attended')+1] if '--attended' in a else None
    if not name: print('refused: attended only — pass --attended NAME'); sys.exit(2)
    asyncio.run(main('florida',name,float(a[a.index('--cadence')+1]) if '--cadence' in a else 6.0))
