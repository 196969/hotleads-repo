import asyncio,json,re,time,html,datetime,collections,urllib.parse
import bot,discovery,practice,intake
C=json.load(open('practice-classes.json')); P={s['id']:s for s in C['discovery']['practices']['Private Equity']['sources']}; TODAY=discovery.TODAY; CEIL=C['band_by_practice']
REP={'window':3,'launch_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tier_a_reread':{},'florida_trend_metadata':{},'feeds':{},'public_record':{},'pe':{},'sunbelt':{},'reads_by_practice':{},'decisions':[]}
def pub_meta(body):
    for name,pat in (('JSON-LD datePublished',r'"datePublished"\s*:\s*"(\d{4}-\d\d-\d\d)'),('article:published_time',r'article:published_time"\s+content="(\d{4}-\d\d-\d\d)'),('time[datetime]',r'<time[^>]+datetime="(\d{4}-\d\d-\d\d)'),('meta pubdate/date',r'(?:name|property)="(?:pubdate|publish-date|date|DC\.date\.issued|parsely-pub-date)"\s+content="(\d{4}-\d\d-\d\d)')):
        m=re.search(pat,body)
        if m: return m.group(1),name
    return None,None
def dated_path(u):
    m=re.search(r'/(20\d\d)/(\d\d)/(\d\d)/',u); return (f'{m.group(1)}-{m.group(2)}-{m.group(3)}','dated URL path') if m else (None,None)
async def go():
    read,b,p=await discovery.browser_reader(); day=discovery.Day('florida','Timothy A. Edick',read); day.Q=json.load(open('florida-intake-queue.json')); Q=day.Q
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat(); day.third=10**6
    day.spent['Tier A re-read']=0; day.spent['Private Equity']=0; day.spent['Acquisitions']=0; day.spent['Fractionals']=0   # the re-read is charged off the top (ruling 9)   # thirds applied by hand below; the shared ceiling is bot.py's
    async def rd(pr,src,url):
        if bot.reads_today()>=bot.CEILING: raise bot.Refused('ceiling')
        return await day.one_read(pr,src,url)
    # ---- Ruling 9: the Tier A re-read first, off the top: every Tier A row at its own site (home page); Sunbiz refuses this reader (403, recorded as outstanding)
    S=json.load(open('florida-standard.json'))['rows']; t=open('florida.html',encoding='utf-8').read(); tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S).group(1); hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]; ix={h:i for i,h in enumerate(hd)}
    rows=[]
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if not c: continue
        k=re.sub('<[^>]+>','',c[0]).strip()
        if S.get(k,{}).get('bandTier')!='A': continue
        site=re.search(r'href="(https?://(?!www\.google|www\.linkedin)[^"]+)"',c[ix['Links']]); rows.append({'key':k,'company':html.unescape(re.search(r'<strong>(.*?)</strong>',c[1]).group(1)),'site':site.group(1) if site else None,'dm':html.unescape(re.sub('<[^>]+>',' ',c[ix['Decision maker']])).strip(),'phone':html.unescape(re.sub('<[^>]+>','',c[ix['Phone']])).strip(),'email':html.unescape(re.sub('<[^>]+>','',c[ix['Email']])).strip()})
    RR={}
    for r in rows:
        if not r['site']: RR[r['key']]={'read':'no link on the row'}; continue
        x=await rd('Tier A re-read','reread:'+r['key'],r['site']); 
        if x[0] is None: break
        ok,code,body=x
        if not ok: RR[r['key']]={'read':f'refused ({code})','link':'does not resolve to a page this reader can read'}; continue
        txt=html.unescape(re.sub(r'<[^>]+>',' ',body)); plain=re.sub(r'\s+',' ',txt)
        ph=re.findall(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',plain); em=[e for e in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',plain) if not re.search(r'\.(png|jpg|svg|js|css)$',e)]
        dmn=re.sub(r'\s{2,}.*','',r['dm']).strip(); dm_tok=[w for w in re.findall(r'[A-Z][a-z]{2,}',dmn)][:2]; dm_on=bool(dm_tok) and all(w in plain for w in dm_tok)
        phd=re.sub(r'\D','',r['phone']); ph_on=bool(phd) and phd in re.sub(r'\D','',plain); em_on=('@' in r['email']) and r['email'].lower() in plain.lower()
        RR[r['key']]={'read':'read '+TODAY,'link':'resolves','executive_named_on_site':dm_on if dm_tok else 'no named person on the row','phone_on_file_published_on_site':ph_on if phd else 'none on file','phones_published':ph[:2],'email_on_file_published_on_site':em_on if '@' in r['email'] else 'none on file','emails_published':em[:2],'florida_on_site':bool(re.search(r'\bFL\b|\bFlorida\b',plain)),'sunbiz':'refuses this reader (403) \u2014 registry half outstanding, never a pass'}
    REP['tier_a_reread']={'rows':len(rows),'read':sum(1 for v in RR.values() if v.get('read','').startswith('read')),'refused':sum(1 for v in RR.values() if v.get('read','').startswith('refused')),'no_link':sum(1 for v in RR.values() if v.get('read')=='no link on the row'),'executive_confirmed_on_site':sum(1 for v in RR.values() if v.get('executive_named_on_site') is True),'executive_not_found_on_site':sum(1 for v in RR.values() if v.get('executive_named_on_site') is False),'phone_confirmed':sum(1 for v in RR.values() if v.get('phone_on_file_published_on_site') is True),'phone_not_on_site':sum(1 for v in RR.values() if v.get('phone_on_file_published_on_site') is False),'email_confirmed':sum(1 for v in RR.values() if v.get('email_on_file_published_on_site') is True),'email_not_on_site':sum(1 for v in RR.values() if v.get('email_on_file_published_on_site') is False),'per_row':RR}
    json.dump(REP,open('reports/w3-engine.json','w'),indent=1,ensure_ascii=False)
    # ---- Ruling 6: Florida Trend re-probed on the six paid-for articles under the metadata rule
    six=[e['url'] for e in (json.loads(l) for l in open('florida-bot-log.jsonl')) if e.get('source')=='florida_trend' and e['outcome']=='read' and '/article/' in e.get('url','')][:6]; ft=[]
    for u in six:
        x=await rd('Acquisitions','florida_trend:metadata',u)
        if x[0] is None: break
        ok,code,body=x; d,f=pub_meta(body) if ok else (None,None); d2,f2=dated_path(u); ft.append({'url':u,'read':'read' if ok else f'refused ({code})','date':d or d2,'field':f or f2})
    REP['florida_trend_metadata']={'articles':ft,'dated':sum(1 for a in ft if a['date']),'result':'Florida Trend reopened under ruling 6' if any(a['date'] for a in ft) else 'stopped: none of the six carries a date in any structured form or a dated path'}
    # ---- Ruling 7: feeds, read live, undisguised; the item's pubDate is the date; linked article read for the signal clause
    FEEDS=[('Acquisitions','gnews_rss','https://news.google.com/rss/search?q=%22Florida%22+company+acquired&hl=en-US&gl=US&ceid=US:en'),('Acquisitions','prn_rss','https://www.prnewswire.com/rss/news-releases-list.rss'),('Acquisitions','gnw_rss','https://www.globenewswire.com/RssFeed/subjectcode/18-Mergers%20And%20Acquisitions/feedTitle/GlobeNewswire%20-%20Mergers%20and%20Acquisitions'),('Acquisitions','bw_rss','https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeEFpRVg=='),('Acquisitions','sfbj_rss','https://www.bizjournals.com/southflorida/news/rss'),('Acquisitions','ft_rss','https://www.floridatrend.com/rss')]
    for pr,sid,u in FEEDS:
        x=await rd(pr,sid,u)
        if x[0] is None: break
        ok,code,body=x
        if not ok: REP['feeds'][sid]=f'refused by source ({code})'; continue
        items=re.findall(r'<item>(.*?)</item>',body,re.S); got=[]
        for it in items[:40]:
            ttl=re.sub(r'<[^>]+>','',re.search(r'<title>(.*?)</title>',it,re.S).group(1) if re.search(r'<title>',it) else '').strip(); link=(re.search(r'<link>(.*?)</link>',it,re.S) or re.search(r'<guid[^>]*>(.*?)</guid>',it,re.S)); link=html.unescape(link.group(1).strip()) if link else ''; pd=re.search(r'<pubDate>(.*?)</pubDate>',it,re.S); pd=pd.group(1).strip() if pd else None
            fl=bool(re.search(r'\bFlorida\b|\bFL\b|Miami|Tampa|Orlando|Jacksonville|Fort Lauderdale|Boca Raton|West Palm',ttl,re.I)); kw=bool(re.search(practice.KW['Acquisitions'],ttl,re.I))
            got.append({'title':ttl[:120],'link':link,'pubDate':pd,'florida':fl,'signal_word':kw})
        REP['feeds'][sid]={'items':len(items),'florida_and_signal':sum(1 for g in got if g['florida'] and g['signal_word']),'sample':[g['title'] for g in got if g['florida'] and g['signal_word']][:5]}
        for g in [g for g in got if g['florida'] and g['signal_word']][:4]:
            if not g['link']: continue
            x=await rd(pr,sid+':article',g['link'])
            if x[0] is None: break
            if not x[0]: continue
            body2=x[2]; d,f=pub_meta(body2); d=d or (datetime.datetime.strptime(g['pubDate'][:25].strip(),'%a, %d %b %Y %H:%M:%S').date().isoformat() if g['pubDate'] and re.match(r'\w{3}, \d{1,2} \w{3} \d{4}',g['pubDate']) else None); f=f or ('feed pubDate' if d else None)
            txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>','',body2,flags=re.S|re.I))); txt=re.sub(r'<[^>]+>',' ',txt); sent=next((s_.strip() for s_ in re.split(r'(?<=[.!?])\s+',txt) if re.search(practice.KW['Acquisitions'],s_,re.I) and re.search(r'\bFlorida\b|\bFL\b|Miami|Tampa|Orlando|Jacksonville',s_)),None)
            if d and sent: k=day.queue_candidate(pr,{'id':sid,'name':sid},None,g['link'],sent,d,None); 
            if d and sent and k not in ('filtered','on file'): Q[k]['date_field']=f; Q[k]['feed_title']=g['title']
    # ---- Ruling 8: public record probed live: FloridaCommerce WARN (Fractionals); EDGAR full-text (PE, Acquisitions)
    for pr,sid,u in [('Fractionals','warn','https://www.floridajobs.org/office-directory/division-of-workforce-services/workforce-programs/reemployment-and-emergency-assistance-coordination-team-react/warn-notices'),('Private Equity','edgar_fts','https://efts.sec.gov/LATEST/search-index?q=%22Florida%22%20%22acquisition%22&dateRange=custom&forms=8-K&startdt=2026-07-01&enddt=2026-10-30')]:
        x=await rd(pr,sid,u)
        if x[0] is None: break
        ok,code,body=x; REP['public_record'][sid]={'read':ok,'status':str(code),'bytes':len(body) if ok else 0,'form':('JSON' if ok and body.lstrip().startswith('{') else 'HTML') if ok else None,'note':'live form read; a control is built from it before any further read' if ok else 'refused by source'}
    # ---- Ruling 10 / PE third: H.I.G. entries by the Location field; Comvest entries; Sun Capital's four unsized Florida cards; Boyne's MBP
    pe_reads=0; LIM=60
    def loc_field(body):
        t_=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',body))); m=re.search(r'(?:Headquarters|Location|HQ)\s*[:\-]?\s*([A-Z][A-Za-z .\-]+,\s*(?:FL|Florida|[A-Z]{2}|[A-Z][a-z]+))',t_); return m.group(1) if m else None
    for sid in ('hig','comvest'):
        cands=[k for k,e in Q.items() if e['source']==sid and not e.get('entry_read') and e.get('sponsor_page')]
        for k in cands:
            if pe_reads>=LIM: break
            e=Q[k]; x=await rd('Private Equity','entry:'+sid,e['sponsor_page']); pe_reads+=1
            if x[0] is None: break
            e['entry_read']=TODAY
            if not x[0]: e['entry']='refused'; continue
            lf=loc_field(x[2]); e['location_field']=lf; e['entry_location_fl']=bool(lf and re.search(r'\bFL\b|Florida',lf)); e['site_from_entry']=discovery.site_link(x[2],e['company'])
            if not e['entry_location_fl']: e['location']=f'location field: {lf}' if lf else 'no location field on the entry'; continue
            if e['site_from_entry'] and pe_reads<LIM:
                x2=await rd('Private Equity','test1:'+sid,e['site_from_entry']); pe_reads+=1
                if x2[0] is None: break
                if not x2[0]: e['test1']=f'company page refused ({x2[1]})'; continue
                txt=html.unescape(re.sub(r'<[^>]+>',' ',x2[2])); addr=' '.join(re.findall(r'[^.]{0,80}\b(?:FL|Florida)\b[^.]{0,80}',txt)[:2]); t1,why=intake.test1_florida({'url':e['site_from_entry'],'read':TODAY,'address_text':addr or txt[:300]}); e['test1']=why; e['test1_pass']=t1; e['company_url']=e['site_from_entry']
                ph=re.search(r'\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',txt); em=[z for z in re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}',txt) if not re.search(r'\.(png|jpg|svg)$',z)]
                e['phone']={'value':ph.group(0),'url':e['site_from_entry'],'read':TODAY} if ph else None; e['email']={'value':em[0],'url':e['site_from_entry'],'read':TODAY,'role_inbox':bool(re.match(r'^(info|sales|contact|hello|office|admin|support)',em[0].split('@')[0],re.I))} if em else None
                t5,ch=intake.test5_channel({'phone':e['phone'],'address':{'value':addr,'url':e['site_from_entry'],'read':TODAY} if addr else None,'form':{'value':'form','url':e['site_from_entry'],'read':TODAY} if re.search(r'<form',x2[2],re.I) else None}); e['test5']=ch
                if t1: e['status']='admitted by test (1, 2, 5) \u2014 awaiting the Chair\u2019s tests 3 and 4' if t5 else 'passes test 1; no reachable channel published (test 5)'
        json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False)
    REP['pe']={'reads':pe_reads,'hig_entries_read':sum(1 for e in Q.values() if e['source']=='hig' and e.get('entry_read')),'hig_location_fields':collections.Counter((e.get('location_field') or 'none')[-2:] for e in Q.values() if e['source']=='hig' and e.get('entry_read')).most_common(8),'florida_by_field':sum(1 for e in Q.values() if e.get('entry_location_fl')),'test1_passed':sum(1 for e in Q.values() if e.get('test1_pass')),'admitted_by_test':sum(1 for e in Q.values() if (e.get('status') or '').startswith('admitted'))}
    # ---- Sunbelt's six listings under Acquisitions
    x=await rd('Acquisitions','sunbelt','https://www.sunbeltnetwork.com/businesses-for-sale/?state=FL')
    if x[0]:
        its=list(dict.fromkeys(html.unescape(m) for m in re.findall(r'href="(https?://(?:www\.)?sunbeltnetwork\.com/business[^"]+)"',x[2])))[:6]; REP['sunbelt']={'items':len(its),'named':0,'unusable':0}
        for u in its:
            x2=await rd('Acquisitions','sunbelt:listing',u)
            if x2[0] is None: break
            if not x2[0]: continue
            txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',x2[2]))); name=re.search(r'\b([A-Z][\w&\'.-]+(?: [A-Z][\w&\'.-]+){0,4} (?:Inc|LLC|Corp|Co\.|Company|Group))\b',txt)
            if name: day.queue_candidate('Acquisitions',{'id':'sunbelt','name':'Sunbelt'},name.group(1),u,txt[:300],TODAY,None); REP['sunbelt']['named']+=1
            else: REP['sunbelt']['unusable']+=1; day.rep['unusable'].append({'url':u,'why':'listing names no company \u2014 unusable, never guessed'})
    else: REP['sunbelt']={'refused':str(x[1])}
    REP['reads_by_practice']=day.spent; REP['stopped']='completed'; json.dump(Q,open('florida-intake-queue.json','w'),indent=1,ensure_ascii=False); json.dump(REP,open('reports/w3-engine.json','w'),indent=1,ensure_ascii=False); print(json.dumps({k:REP[k] for k in ('tier_a_reread','florida_trend_metadata','feeds','public_record','pe','sunbelt','reads_by_practice')},ensure_ascii=False)[:2500])
    await b.close(); await p.stop()
asyncio.run(go())
