"""practice.py — the practice pipeline's reader (Item 320 Part 9). Under bot.py's containment and Part 8's standard. Reads third-party sources only,
by the classes declared in practice-classes.json; never the company's own site; Sunbiz at its declared 0. Each read is one logged, ceiling-counted
read. Output per row per criterion: a candidate signal (sentence, URL, publication date, source class) into <market>-practice-queue.json as
unconfirmed. Refusals are logged with their reason: undated page, jurisdiction, class. It derives nothing; the standard does."""
import json,re,html,sys,os,urllib.request,urllib.parse,ssl,datetime,time
import bot
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
C=json.load(open('practice-classes.json')); CLASSES=C['source_classes']; TODAY=datetime.date.today().isoformat()
KW={'Acquisitions':r'\b(acquir\w*|acquisition|merger|merge[sd]?|sold to|sale of|for sale|succession|successor|retir\w*|ownership transition|transition of ownership|buyout|ESOP|next generation|third[- ]generation|changes? hands)\b',
    'Fractionals':r'\b(CFO|chief financial officer|controller|VP of finance|vice president of finance|finance director|director of finance|COO|chief operating officer|VP of operations|director of operations|interim (CFO|COO|CEO|controller)|fractional)\b',
    'Private Equity':r'\b(portfolio compan\w*|platform (investment|company|acquisition)|add-on|bolt-on|private equity|sponsor|recapitali[sz]\w*|growth equity|majority (stake|investment)|invest\w* in)\b'}
def host_of(u): return re.sub(r'^https?://(www\.)?','',u).split('/')[0].lower()
def class_of(u):
    h=host_of(u)
    for k,v in CLASSES.items():
        if any(h==d or h.endswith('.'+d) for d in v['domains']): return k
    return None
def pub_date(body):
    for pat in (r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)',r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)',r'content="(\d{4}-\d\d-\d\d)[^"]*"\s+(?:property|name)="(?:article:published_time|pubdate|publish-date|date)"',r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)',r'"dateCreated"\s*:\s*"(\d{4}-\d\d-\d\d)',r'"uploadDate"\s*:\s*"(\d{4}-\d\d-\d\d)'):
        m=re.search(pat,body)
        if m: return m.group(1)
    m=re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d{1,2}), (\d{4})\b',re.sub('<[^>]+>',' ',body[:20000]))
    if m:
        try: return datetime.datetime.strptime(m.group(0),'%B %d, %Y').date().isoformat()
        except Exception: return None
    return None
def fetch(u):
    try: r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=12,context=ctx); return r.status,r.read(600000).decode('utf-8','ignore'),r.geturl()
    except urllib.error.HTTPError as e: return e.code,'',u
    except Exception as e: return ('timeout' if 'timed out' in str(e).lower() else 'net'),'',u
def pipeline(market):
    S=json.load(open(market+'-standard.json'))['rows']; t=open(market+'.html',encoding='utf-8').read(); tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S).group(1)
    hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]; ix={h:i for i,h in enumerate(hd)}; rows=[]
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if not c: continue
        k=re.sub('<[^>]+>','',c[0]).strip()
        if S.get(k,{}).get('bandTier')!='A': continue
        comp=html.unescape(re.search(r'<strong>(.*?)</strong>',c[1]).group(1)); city=html.unescape(re.sub('<[^>]+>','',c[ix['City']])).strip()
        site=re.search(r'href="(https?://(?!www\.google|www\.linkedin)[^"]+)"',c[ix['Links']]); rows.append({'key':k,'company':comp,'city':city,'host':host_of(site.group(1)) if site else None})
    return rows
def candidate(row,crit,cls,url,body):
    """Returns (candidate or None, refusal reason or None). A candidate needs: a third-party class, a publication date, the company named, a criterion sentence, and Florida jurisdiction."""
    if cls is None or (row['host'] and (host_of(url)==row['host'] or host_of(url).endswith('.'+row['host']))): return None,'refused by class: the company\u2019s own site is not a source' if row['host'] and row['host'] in host_of(url) else 'refused by class: not a declared source class'
    if crit not in CLASSES[cls]['criteria']: return None,f'refused by class: {cls} is not declared for {crit}'
    d=pub_date(body)
    if not d: return None,'refused: no publication date on the page'
    plain=re.sub(r'\s+',' ',html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S|re.I))); text=re.sub('<[^>]+>',' ',plain)
    tok=[w for w in re.findall(r'[A-Za-z]{4,}',row['company']) if w.lower() not in ('company','group','corp','inc','llc','international','holdings','enterprises','distributors','distributing','services','systems')][:1]
    if not tok or tok[0].lower() not in text.lower(): return None,'refused: the page does not name the company'
    if not re.search(r'\bFlorida\b|\bFL\b|'+re.escape(row['city'] or 'Florida'),text): return None,'refused on jurisdiction: the page names neither Florida nor the row\u2019s city (a same-name company elsewhere)'
    sents=[s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if tok[0].lower() in s.lower() and re.search(KW[crit],s,re.I)]
    if not sents: return None,f'no {crit} sentence naming the company on the page'
    return {'criterion':crit,'sentence':sents[0][:400],'sentence_as_read':sents[0][:400],'url':url,'published':d,'source_class':cls,'read':TODAY,'status':'proposed \u2014 unconfirmed'},None
def search(q,domains,state):
    u='https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)
    def reader(url):
        s,b,f=fetch(url); state['body']=b; return ('read' if s=='ok' or (isinstance(s,int) and s<400) else 'refused'),None
    return u,reader
def main(market,classes_this_run):
    rows=pipeline(market); qp=market+'-practice-queue.json'; Q=json.load(open(qp)) if os.path.exists(qp) else {}; rp=market+'-practice-reads.json'; RR=json.load(open(rp)) if os.path.exists(rp) else {}
    rep={'market':market,'date':TODAY,'rows':len(rows),'classes_this_run':classes_this_run,'reads_total':0,'candidates':0,'refusals':{},'reads_per_row_per_class':None,'ceiling':bot.CEILING,'ceiling_is_assumed':bot.CFG['ceiling_is_assumed']}
    st={}
    for r in rows:
        RR.setdefault(r['key'],{'classes_read':{},'refusals':[]})
        for cls in classes_this_run:
            if CLASSES[cls].get('reads_permitted')==0: RR[r['key']]['classes_read'][cls]='not read (0 reads permitted)'; continue
            crits=CLASSES[cls]['criteria']; q=f'"{r["company"]}" Florida '+(' OR '.join('site:'+d for d in CLASSES[cls]['domains'][:4]) if False else ' '.join(CLASSES[cls]['domains'][:3]).replace('.com','')) 
            u,reader=search(f'{r["company"]} Florida {CLASSES[cls]["what"].split(" ")[0]} '+('acquisition OR succession OR sold' if cls=='broker' else 'CFO OR controller OR "director of operations"' if cls=='job_board' else 'portfolio' if cls=='sponsor' else 'acquired OR acquisition OR CFO OR "private equity"'),CLASSES[cls]['domains'],st)
            try: bot.run(market,[(r['key'],u)],reader)
            except (bot.Halted,bot.Refused): raise
            rep['reads_total']+=1; body=st.get('body','')
            if 'uddg=' not in body: RR[r['key']]['classes_read'][cls]='search refused'; rep['refusals']['search refused']=rep['refusals'].get('search refused',0)+1; continue
            hits=[html.unescape(urllib.parse.unquote(m)) for m in re.findall(r'uddg=([^&"]+)',body)]; hits=[h for h in hits if class_of(h)==cls][:2]
            RR[r['key']]['classes_read'][cls]=f'read {TODAY}: {len(hits)} class hit(s)'
            for h in hits:
                def rd(url): s,b,f=fetch(url); st['page']=(s,b,f); return ('read' if isinstance(s,int) and s<400 else 'refused'),None
                try: bot.run(market,[(r['key'],h)],rd)
                except (bot.Halted,bot.Refused): raise
                rep['reads_total']+=1; s,b,f=st.get('page',(0,'',h))
                if not (isinstance(s,int) and s<400): RR[r['key']]['refusals'].append({'url':h,'why':f'page refused ({s})'}); continue
                for crit in crits:
                    cand,why=candidate(r,crit,cls,f,b)
                    if cand: Q[f'{r["key"]}:{crit}:{len([k for k in Q if k.startswith(r["key"]+":"+crit)])}']=cand; rep['candidates']+=1; bot.write({}, r['key'],'bot_note',json.dumps({'practice_candidate':cand},ensure_ascii=False))
                    else: RR[r['key']]['refusals'].append({'url':f,'criterion':crit,'why':why}); rep['refusals'][why.split(':')[0]]=rep['refusals'].get(why.split(':')[0],0)+1
            json.dump(Q,open(qp,'w'),indent=1,ensure_ascii=False); json.dump(RR,open(rp,'w'),indent=1,ensure_ascii=False)
        print(f"#{r['key']:>3} {r['company'][:24]:24} reads so far {rep['reads_total']:3} | candidates {rep['candidates']}",flush=True)
        time.sleep(1.5)
    rep['reads_per_row_per_class']=round(rep['reads_total']/(len(rows)*len([c for c in classes_this_run if CLASSES[c].get('reads_permitted')!=0])),2); json.dump(rep,open('bot-report-part9.json','w'),indent=1); print(json.dumps(rep))
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else 'florida',sys.argv[2].split(',') if len(sys.argv)>2 else ['trade_press','job_board'])
