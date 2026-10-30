import asyncio,json,re,time,html,datetime
import bot,discovery,practice,intake
C=json.load(open("practice-classes.json")); P=C["discovery"]["practices"]["Private Equity"]["sources"]
async def go():
    read,b,p=await discovery.browser_reader()
    day=discovery.Day("florida","Timothy A. Edick",read); day.Q=json.load(open("florida-intake-queue.json")); day.spent={"Private Equity":10,"Acquisitions":22,"Fractionals":3}
    bot.RUN_START=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    tv=[s for s in P if s["id"]=="trivest"][0]; r=await day.one_read("Private Equity","trivest",tv["route"])
    if r[0]: open("scratch-trivest.html","w").write(r[2])
    for s in P:
        body=open("scratch-"+s["id"]+".html").read(); its=discovery.items(s,body); day.rep["sources_state"][s["id"]]={"state":f"parsed from the read body: {len(its)} companies, {sum(1 for x in its if x[2])} Florida cards","reads":1}
        for u,t,fl in its:
            k=day.queue_candidate("Private Equity",s,t,s["route"],f"{t} is named on {s['name']}\u2019s portfolio page{' (card mentions Florida)' if fl else ''}.",discovery.TODAY,None)
            if k not in ("filtered","on file"): day.Q[k]["sponsor"]=s["name"]; day.Q[k]["sponsor_page"]=u; day.Q[k]["florida_on_card"]=fl
    json.dump(day.Q,open("florida-intake-queue.json","w"),indent=1,ensure_ascii=False)
    try:
        for k in sorted([k for k,e in day.Q.items() if e.get("test1") is None and e["practice"]=="Private Equity"],key=lambda k:(not day.Q[k].get("florida_on_card"),k)): await day.test1(k)
        day.rep["stopped"]="completed"
    except (bot.Refused,bot.Halted) as e: day.rep["stopped"]=str(e)
    json.dump(day.Q,open("florida-intake-queue.json","w"),indent=1,ensure_ascii=False); json.dump(day.rep,open("pe-pass-report.json","w"),indent=1,ensure_ascii=False); print(json.dumps(day.rep["candidates"]),day.rep["stopped"],day.spent)
    await b.close(); await p.stop()
asyncio.run(go())
