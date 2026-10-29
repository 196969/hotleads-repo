"""bot.py — the Research Bot's containment (Item 320 Part 6, D0). It reads, logs and proposes; it never writes a field a human has not confirmed,
and it never sends. Everything it produces lands in <market>-bot-queue.json for a human to confirm one entry at a time (Part 7.5).
Containment, all read from bot-config.json: a kill switch (file), a daily read ceiling enforced in code, an append-only audit log, a write fence."""
import json,os,time,datetime,sys
CFG=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'bot-config.json')))
LOG=CFG['audit_log']; KILL=CFG['kill_switch']; FENCE=set(CFG['write_fence']); CEILING=int(CFG['daily_read_ceiling'])
class Halted(Exception): pass
class Refused(Exception): pass
class FenceError(Exception): pass
def log(entry):
    entry['ts']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with open(LOG,'a',encoding='utf-8') as f: f.write(json.dumps(entry,ensure_ascii=False)+'\n')      # append only: this is the only way the log is ever opened
RUN_START=None   # the run's UTC start date, set at launch; a "day" for the ceiling is this date (Item 320 Part 11 ruling, 29 Oct 2026)
def reads_today():
    """Reads counted against the ceiling: every read stamped on or after the run's UTC start date, across midnight. Before a run starts, the current UTC date."""
    start=RUN_START or datetime.datetime.now(datetime.timezone.utc).date().isoformat(); n=0
    if os.path.exists(LOG):
        for line in open(LOG,encoding='utf-8'):
            try: e=json.loads(line)
            except Exception: continue
            if e.get('kind')=='read' and e.get('ts','')[:10]>=start: n+=1
    return n
def killed(): return os.path.exists(KILL)
def write(queue,key,field,value):
    """The write fence. The bot may write addr_found, bot_note and bot_status on a queue entry, and nothing else, anywhere."""
    if field not in FENCE:
        log({'kind':'fence','row':key,'field':field,'outcome':'refused'}); raise FenceError(f'write to {field!r} refused: the bot writes only {sorted(FENCE)}')
    queue.setdefault(key,{})[field]=value; log({'kind':'write','row':key,'field':field,'outcome':'written'})
def run(market,rows,reader):
    """rows: [(key, url)]; reader(url) -> (outcome, found). One timed read per row, under the kill switch and the ceiling. Returns the queue."""
    qp=market+'-bot-queue.json'; queue=json.load(open(qp)) if os.path.exists(qp) else {}
    global RUN_START
    if RUN_START is None: RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    log({'kind':'run','market':market,'rows':len(rows),'ceiling':CEILING,'ceiling_is_assumed':CFG['ceiling_is_assumed'],'outcome':'start','run_start_utc':RUN_START})
    done=0
    for key,url in rows:
        if killed(): log({'kind':'halt','row':key,'reason':'kill switch present','reads_done_this_run':done}); raise Halted('kill switch present — halted before row '+str(key))
        if reads_today()>=CEILING: log({'kind':'ceiling','row':key,'reads_today':reads_today(),'ceiling':CEILING,'outcome':'refused'}); raise Refused(f'read refused: {reads_today()} reads today, ceiling {CEILING} (assumed)')
        t0=time.time(); outcome,found=reader(url); el=round(time.time()-t0,2)
        log({'kind':'read','row':key,'url':url,'outcome':outcome,'elapsed':el}); done+=1
        if found: write(queue,key,'addr_found',found); write(queue,key,'bot_note','read '+url); write(queue,key,'bot_status','proposed — unconfirmed')
    json.dump(queue,open(qp,'w'),indent=1,ensure_ascii=False); log({'kind':'run','market':market,'outcome':'complete','reads':done}); return queue
