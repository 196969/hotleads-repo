import json,sys,coverage_panel,os
out={'officer_rebuild':json.load(open('reports/run2-officer-proof.json'))['result']}
planted={'a':{'reads':0},'b':{'reads':1,'answered':0,'refused':{}},'c':{'reads':2,'answered':2},'d':{'reads':3,'answered':0,'refused':{'403':3}},'e':{'state':'exhausted'},'f':{'state':'closed'}}
c=coverage_panel.build(planted,'/tmp/panel-planted.html'); page=open('/tmp/panel-planted.html').read()
ok=c=={'unread':1,'probed':1,'answering':1,'refused':1,'exhausted':1,'closed':1} and '403\u00d73' in page
out['coverage_panel']='PASSED' if ok else 'FAILED'
json.dump({'officer_rebuild':out['officer_rebuild'],'coverage_panel':{'planted_counts':c,'result':out['coverage_panel'],'classes':['unread / probed / answering / refused with code and count / exhausted / closed']}},open('reports/run2-gate.json','w'),indent=1,ensure_ascii=False)
print(out); sys.exit(0 if all(v=='PASSED' for v in out.values()) else 1)
