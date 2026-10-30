"""day_one.py — Chunk C as one pass (second edition, Section 14). Order: gate · known-answer read (a failure stops Florida Trend only) · six re-reads · every declared source probed with its control · round-robin discovery under the thirds split to the ceiling or exhaustion · candidates to the Intake queue · Part 10 re-measure · one report. Attended only. Run: python3 day_one.py --attended "Timothy A. Edick" [--dry]"""
import json,re,sys,os,time,datetime,asyncio,html,subprocess
import bot,practice,discovery,controls,remeasure
def gate_report():
    r=subprocess.run(['git','log','-1','--format=%h'],capture_output=True,text=True); return {'head':r.stdout.strip() or 'n/a','note':'full three-way file agreement is checked by the build before launch; this records the head the run saw'}
async def main(attended,dry=False,read_fn=None):
    rep={'chunk':'C \u2014 discovery day one','step_executed':'Section 14 Chunk C, one pass','attended_by':attended,'dry_run':dry,'gate':gate_report(),'order':[],'known_answer':None,'re_reads':None,'probes':None,'discovery':None,'part_10':None,'sitting':None}
    # probes (no reads)
    P=controls.probe_all(); rep['probes']={k:v['result'] for k,v in P.items()}; failed=[k for k,v in P.items() if v['result']!='PROBE PASSED']
    D=json.load(open('practice-classes.json'))['discovery']
    day=discovery.Day('florida',attended,read_fn); 
    for k in failed: day.rep['sources_state'][k]={'state':'probe failed','reads':0}
    # known-answer read: one Florida Trend article already read on 30 Oct with a visible date; failure stops Florida Trend only
    L=[json.loads(l) for l in open(bot.LOG)] if os.path.exists(bot.LOG) else []; six=[e['url'] for e in L if e.get('source')=='florida_trend' and e['outcome']=='read' and '/article/' in e.get('url','') and e['ts'][:10]=='2026-10-30']
    ka={'article':six[0] if six else None,'result':None}
    if ka['article'] and 'florida_trend' not in failed:
        r=await day.one_read('Acquisitions','florida_trend',ka['article'])
        if r[0]: d=practice.pub_date(r[2]); ka['date_extracted']=d
        if r[0] and ka.get('date_extracted'): ka['result']='PASSED'
        elif r[0]:
            # fix-and-prove on a miss: look for the page's visible date form and add it to the extractor, proved on a planted page of that form
            m=re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b|\b(\d{4})-(\d\d)-(\d\d)\b|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? (\d{1,2}), (\d{4})',re.sub('<[^>]+>',' ',r[2]))
            ka['visible_date_form']=m.group(0) if m else None; ka['result']='FAILED \u2014 Florida Trend stopped (no visible date form found to fix against)' if not m else 'FIXED-AND-PROVED pending: visible date form found; extractor patched for this form'
            if m:
                old=practice.pub_date; 
                def patched(body,_old=old):
                    d=_old(body)
                    if d: return d
                    mm=re.search(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',re.sub('<[^>]+>',' ',body[:30000]))
                    if mm: return f'{mm.group(3)}-{int(mm.group(1)):02d}-{int(mm.group(2)):02d}'
                    mm=re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? (\d{1,2}), (\d{4})',re.sub('<[^>]+>',' ',body[:30000]))
                    if mm: return datetime.datetime.strptime(f'{mm.group(1)[:3]} {mm.group(2)} {mm.group(3)}','%b %d %Y').date().isoformat()
                    return None
                practice.pub_date=patched; proved=patched('<html><body><p>Posted 10/02/2026 by staff</p></body></html>')=='2026-10-02'; ka['result']='FIXED-AND-PROVED' if (proved and patched(r[2])) else 'FAILED \u2014 Florida Trend stopped'
        else: ka['result']=f'FAILED \u2014 refused ({r[1]}); Florida Trend stopped'
        if ka['result'].startswith('FAILED'): day.rep['sources_state']['florida_trend']={'state':'stopped: known-answer read failed','reads':1}
    else: ka['result']='not run: no logged article to use' if not ka['article'] else 'not run: probe failed'
    rep['known_answer']=ka
    # six re-reads with the proved extractor (paid for on 30 Oct; not counted twice)
    rr=[]
    if ka['result'] in ('PASSED','FIXED-AND-PROVED'):
        for u in six[:6]:
            r=await day.one_read('Acquisitions','florida_trend',u)
            if r[0] is None: break
            ok,code,body=r; d=practice.pub_date(body) if ok else None; rr.append({'url':u,'outcome':'read' if ok else f'refused ({code})','published':d})
    rep['re_reads']=rr
    rep['discovery']=await day.run()
    json.dump(day.Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    rep['part_10']=remeasure.measure()
    rep['sitting']={'note':'the Chair judges tests 3 and 4 in one sitting at the end, by name, in the console\u2019s Intake tab; start and end clock times stated in one line; apply_queue.py carries the confirmed'}
    json.dump(rep,open('report-day-one.json','w'),indent=1,ensure_ascii=False); return rep
if __name__=='__main__':
    a=sys.argv; name=a[a.index('--attended')+1] if '--attended' in a else None
    if not name: print('refused: attended only'); sys.exit(2)
    if bot.reads_today()>=bot.CEILING: print(f'refused before read 1: {bot.reads_today()} reads on the start date'); sys.exit(3)
    async def go():
        read,b,p=await discovery.browser_reader()
        try: await main(name,False,read)
        finally: await b.close(); await p.stop()
    asyncio.run(go())
