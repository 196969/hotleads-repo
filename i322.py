"""Item 322: for each in-scope row, up to 3 reads of the company site the row already names (home, /contact, /contact-us). Records, per read,
whether the page shows the row's number and whether the page itself displays a full date (a year alone is not a date). Nothing else is read."""
import asyncio,json,re,datetime,discovery,naming8
W=json.load(open('scope71.json')); MON='(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\\.?'
DATE=re.compile(r'\b(?:'+MON+r' \d{1,2},? \d{4}|\d{1,2} '+MON+r' \d{4}|\d{4}-\d\d-\d\d|\d{1,2}/\d{1,2}/\d{4})\b')
log=open('florida-item322-log.jsonl','a'); out=[]; spent=0
def T(b): return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'(?is)<script.*?</script>|<style.*?</style>','',b or '')))
async def go():
    global spent
    read,b,p=await discovery.browser_reader()
    for w in W:
        rec={'key':w['key'],'source':w['source'],'company':w['company'],'phone':w['phone'],'site':w['site'],'routes':[],'result':None}
        if not w['site']: rec['result']='not sourced \u2014 no company site on the row; finding one is discovery, out of scope'; out.append(rec); continue
        digits=re.sub(r'\D','',w['phone'])[-10:]
        for path in ('','/contact','/contact-us'):
            if spent>=171: break
            url=f"https://{w['site']}{path}"
            try: code,body,final=await read(url)
            except Exception as ex: code,body,final='error:'+type(ex).__name__,'',url
            spent+=1; txt=T(body); ok=isinstance(code,int) and code<400 and not naming8.is_challenge(body or '')
            has_num=ok and digits in re.sub(r'\D','',txt); dates=DATE.findall(txt) if ok else []
            r={'url':url,'code':str(code),'number_on_page':has_num,'page_dates':dates[:3]}
            rec['routes'].append(r); log.write(json.dumps({'kind':'read','url':url,'outcome':'read' if ok else 'refused','kind_detail':str(code),'reader':'browser','ts':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n'); log.flush()
            if has_num and dates: rec['result']='sourced'; break
        if not rec['result']:
            rec['result']=('not sourced \u2014 the number is on the company\u2019s pages, but no page that shows it displays a date' if any(x['number_on_page'] for x in rec['routes']) else 'not sourced \u2014 every route refused or did not show the number')
        out.append(rec); json.dump({'spent':spent,'rows':out},open('i322-engine.json','w'),indent=1,ensure_ascii=False)
    await b.close(); await p.stop(); print('DONE spent',spent)
asyncio.run(go())
