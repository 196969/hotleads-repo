"""remeasure.py — Part 10 harness (second edition): counts on the working standard and the intake table, three sources of movement stated separately against the baseline, the bot's yield beside the band movement. No reads."""
import json,re,html,collections,sys,os
BASE={'rows':150,'strict':21,'address_eligible':29,'bands':{'1':14,'2':4,'3':13,'4':119},'workable':32,'band_1':12,'callable':21}
def measure(market='florida',queue=None,prev=None):
    S=json.load(open(market+'-standard.json'))['rows']; B=dict(sorted(collections.Counter(str(v['band']) for v in S.values()).items()))
    t=open(market+'-expansion.html',encoding='utf-8').read(); m=re.search(r'<table id="intake">(.*?)</table>',t,re.S); rows=re.findall(r'<tr[^>]*>(.*?)</tr>',m.group(1),re.S) if m else []
    intake=[]
    for r in rows:
        c=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)]
        if c: intake.append({'key':c[0],'company':c[1],'practice':c[8].split(' \u2014 ')[0],'tier':c[11],'band':c[10]})
    qp=queue or market+'-intake-queue.json'; Q=json.load(open(qp)) if (queue is not False and os.path.exists(qp)) else {}
    now={'rows':len(S),'bands':B,'workable':sum(v['workable'] for v in S.values()),'band_1':B.get('1',0),'tier_A':sum(1 for v in S.values() if v['bandTier']=='A'),'intake_rows':len(intake),'intake_by_practice':dict(collections.Counter(x['practice'] for x in intake)),'intake_tier':dict(collections.Counter(x['tier'] for x in intake)),'intake_band_typed':sum(1 for x in intake if x['band'] not in ('derived','','\u2014'))}
    yld={'candidates_queued':sum(1 for v in Q.values() if isinstance(v,dict)),'confirmed':sum(1 for v in Q.values() if isinstance(v,dict) and v.get('status') in ('confirmed','applied')),'rejected':sum(1 for v in Q.values() if isinstance(v,dict) and v.get('status')=='rejected')}
    yld['yield']=round(yld['confirmed']/yld['candidates_queued'],3) if yld['candidates_queued'] else None
    return {'baseline':BASE,'now':now,'movement':{'net_new':{'intake_rows_unverified':len(intake),'promoted_to_working':0,'note':'net-new enters the intake table as Unverified only; nothing is promoted until a recorded act (9.5)'},'data_repairs':'none this day unless the report names them','instrument_corrections':'none this day unless the report names them'},'bot_yield':yld}
if __name__=='__main__': print(json.dumps(measure(),indent=1))
