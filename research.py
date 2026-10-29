"""research.py — the Research Bot's one pass (Item 320 Part 7). Reads, under bot.py's containment; proposes into <market>-bot-queue.json; admits nothing.
Per row: resolves the research link (the first read), reads the company's own home, contact and about pages for a published contact address and a
named person's address, gathers the sentences that bear on the three practice criteria (text only, never judged here), and checks the name and
domain against every other table file. It does not guess an address, infer a decision maker, read Sunbiz, or treat a refusal as an absence."""
import json,re,html,glob,sys,os,urllib.request,ssl,time,datetime
import bot,reads
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
BELOW_FLOOR=re.compile(r'^(careers?|jobs?|hr|recruit\w*|talent|employment|resumes?|hiring|apply|internships?)\d*$',re.I)   # 7.2 ruling (29 Oct 2026): a careers or jobs inbox is below the floor — never proposed
PRECEDENCE=['contact','contactus','info','sales','office','hello','inquiries','enquiries','general']   # 7.2 ruling: the selection rule, declared; "first address on the page" is struck
def choose(emails):
    """The bot's selection among role inboxes published on the page: by declared precedence, then any other role inbox not below the floor; a named person's address is never selected (human only)."""
    cands=[e for e in emails if not BELOW_FLOOR.match(e.split('@')[0]) and ROLE.match(e.split('@')[0])]
    for p in PRECEDENCE:
        for e in cands:
            if re.sub(r'\d+$','',e.split('@')[0]).lower()==p: return e
    return cands[0] if cands else None
EM=re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
ROLE=re.compile(r'^(info|sales|contact|contactus|hello|office|admin|support|customerservice|customercare|service|services|orders?|marketing|hr|careers?|jobs|media|press|pr|ir|investors?|webmaster|accounting|billing|inquiries|enquiries|general|team|help|reception|quotes?|purchasing|parts|privacy|legal|noreply|no-reply|feedback|recruiting|talent|employment|safety|export|import|wholesale|retail|shop|store|cs|mail|email|newsletter)\d*$',re.I)
SIG=re.compile(r'[^.]{0,100}\b(generation|family[- ]owned|succession|retir\w*|acquir\w*|acquisition|merger|for sale|exploring|CFO|chief financial|COO|chief operating|controller|vacan\w*|hiring|now hiring|expan\w*|new facility|growing|private equity|sponsor|portfolio company|backed by)\b[^.]{0,100}',re.I)
def fetch(u):
    try: r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=12,context=ctx); b=r.read(500000).decode('utf-8','ignore'); return r.status,'',b
    except urllib.error.HTTPError as e: return e.code,'',''
    except Exception as e: return ('timeout' if 'timed out' in str(e).lower() else 'net'),'',''
def index_others(market):
    norm=lambda s: re.sub(r'[^a-z0-9]','',html.unescape(s).lower().split('(')[0]); N={}
    for f in glob.glob('*.html'):
        if f in (market+'.html',) or not f.endswith('.html'): continue
        t=open(f,encoding='utf-8',errors='ignore').read()
        if '<table' not in t: continue
        for row in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S):
            m=re.search(r'<strong>(.*?)</strong>',row)
            if m: N.setdefault(norm(re.sub('<[^>]+>','',m.group(1))),set()).add(f)
            for h in re.findall(r'href="https?://(?:www\.)?([^/"]+)"',row):
                if not re.search(r'google\.|linkedin\.',h): N.setdefault('DOM:'+h.lower(),set()).add(f)
    return N,norm
def pipeline(market):
    S=json.load(open(market+'-standard.json'))['rows']; t=open(market+'.html',encoding='utf-8').read(); tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S).group(1)
    hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]; ix={h:i for i,h in enumerate(hd)}; rows=[]
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if not c: continue
        k=re.sub('<[^>]+>','',c[0]).strip()
        if S.get(k,{}).get('bandTier')!='A': continue
        comp=html.unescape(re.search(r'<strong>(.*?)</strong>',c[1]).group(1)); site=re.search(r'href="(https?://[^"]+)"[^>]*>Website',row) or next((m for m in re.finditer(r'href="(https?://(?!www\.google|www\.linkedin)[^"]+)"',c[ix['Links']])),None)
        asrc=html.unescape(re.sub('<[^>]+>','',c[ix['Address source']])).strip() if 'Address source' in ix else ''
        rows.append({'key':k,'company':comp,'site':site.group(1) if site else None,'email_on_file':html.unescape(re.sub('<[^>]+>','',c[ix['Email']])).strip() if 'Email' in ix else '','address_sourced':bool(re.search(r'\b20\d\d-\d\d-\d\d\b',asrc))})
    return rows
def make_reader(state):
    def reader(url):
        status,title,body=fetch(url); outcome,kind=reads.classify(status,title,body,looked_for_found=None)
        if outcome=='refused': state['last']={'outcome':'refused','kind':kind,'url':url}; return 'refused',None
        txt=html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S|re.I)); plain=re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',txt))
        host=re.sub(r'^https?://(www\.)?','',url).split('/')[0].lower(); base=host.split('.')[-2] if host.count('.')>=1 else host
        emails=sorted({e.lower().strip('.') for e in EM.findall(txt) if base in e.lower().split('@')[1] and not re.search(r'\.(png|jpe?g|gif|svg|webp)$',e.lower())})
        state['last']={'outcome':'read','url':url,'emails':emails,'named':[e for e in emails if not ROLE.match(e.split('@')[0]) and re.fullmatch(r'[a-z]+([._-][a-z]+)?',e.split('@')[0])],'signals':[m.group(0).strip()[:220] for m in SIG.finditer(plain)][:6],'names_company':None}
        pick=choose(emails); state['last']['below_floor']=[e for e in emails if BELOW_FLOOR.match(e.split('@')[0])]; state['last']['outcome']='read' if pick else 'not_found'
        return ('read' if pick else 'not_found'),pick
    return reader
def main(market):
    rows=pipeline(market); N,norm=index_others(market); state={}; reader=make_reader(state); qp=market+'-bot-queue.json'; queue=json.load(open(qp)) if os.path.exists(qp) else {}
    report={'market':market,'date':datetime.date.today().isoformat(),'rows_in_pipeline':len(rows),'rows_read':0,'rows_refused':0,'rows_not_found':0,'rows_proposed':0,'rows_confirmed':0,'reads_total':0,'ceiling':bot.CEILING,'ceiling_is_assumed':bot.CFG['ceiling_is_assumed'],'skipped_no_link':[]}
    for r in rows:
        if not r['site']: report['skipped_no_link'].append(r['key']); continue
        host=re.sub(r'^https?://(www\.)?','',r['site']).split('/')[0]; urls=['https://'+host,'https://'+host+'/contact','https://'+host+'/about']
        found=None; notes=[]; link=None; sig=[]; named=[]; below=[]
        if r['address_sourced']: urls=urls   # the pages are still read for link, practice signals and duplicates; no address is proposed (7.2: nothing over a sourced address)
        for u in urls:
            try: bot.run(market,[(r['key'],u)],reader)   # one read per URL, each under the kill switch and the ceiling, each logged
            except bot.Halted: raise
            except bot.Refused: raise
            report['reads_total']+=1; L=state.get('last',{})
            if link is None: link='refused ('+str(L.get('kind'))+')' if L.get('outcome')=='refused' else 'resolves'
            if L.get('outcome')=='read': sig+=L.get('signals',[]); named+=L.get('named',[])
            below+=L.get('below_floor',[])
            if L.get('outcome')=='read' and L.get('emails') and not found and not r['address_sourced']:
                pick=choose(L['emails'])
                if pick: found=(pick,u,L.get('named'))
        dup=sorted(set(N.get(norm(r['company']),set()))|N.get('DOM:'+host.lower(),set()))
        e=queue.setdefault(r['key'],{})
        if link.startswith('refused'): report['rows_refused']+=1
        elif found: report['rows_read']+=1
        else: report['rows_not_found']+=1
        if found:
            addr,src,nm=found; person=[x for x in (nm or []) if x!=addr]
            if r['email_on_file'] and '@' in r['email_on_file'] and r['email_on_file'].lower()==addr: pass
            bot.write(queue,r['key'],'addr_found',addr); bot.write(queue,r['key'],'bot_note',json.dumps({'source_url':src,'read':report['date'],'link':link,'named_person_addresses':person[:3],'practice_signals':sig[:4],'duplicates_in_other_files':dup},ensure_ascii=False)); bot.write(queue,r['key'],'bot_status','proposed — unconfirmed'); report['rows_proposed']+=1
        else:
            why='refused — re-runnable' if link.startswith('refused') else ('row already holds a sourced address — nothing proposed over it (7.2)' if r['address_sourced'] else ('only careers/jobs inboxes published on the pages read ('+', '.join(sorted(set(below)))+') — below the floor, nothing proposed (7.2)' if below else 'not found — no address published on the pages read; nothing guessed'))
            bot.write(queue,r['key'],'bot_note',json.dumps({'link':link,'read':report['date'],'result':why,'practice_signals':sig[:4],'duplicates_in_other_files':dup},ensure_ascii=False)); bot.write(queue,r['key'],'bot_status','no proposal — '+('refused' if link.startswith('refused') else ('sourced address on file' if r['address_sourced'] else ('below floor' if below else 'not found'))))
        json.dump(queue,open(qp,'w'),indent=1,ensure_ascii=False)
        print(f"#{r['key']:>3} {r['company'][:26]:26} link {link[:18]:18} {'proposed '+found[0] if found else ('no address on pages read' if not link.startswith('refused') else 'refused')}",flush=True)
    report['yield']=round(report['rows_proposed']/report['rows_in_pipeline'],3) if rows else None; report['yield_note']='proposed over pipeline rows; confirmed is 0 until a named human confirms each entry in the console (Part 7.5)'
    json.dump(report,open('bot-report-part7.json','w'),indent=1); print(json.dumps(report))
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else 'florida')
