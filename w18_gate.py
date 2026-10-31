import json,sys,roster,naming10
cards=roster.suncap_cards(open('scratch-suncap.html',errors='ignore').read())
fl=[c for c in cards if c['location'].lower()=='florida']
names=sorted(c['name'] for c in fl)
out={'roster_reader':{'cards':len(cards),'florida_on_face':len(fl),'florida_names':names,'expected_florida':6,'classes':['a card carrying Florida on its face / another state','a clean card title / card text run into the name (window two\u2019s failure: \u201cLoan Logics Business Services Florida Actively seeking add-on acquisitions\u201d)'],
  'result':'PASSED' if len(fl)==6 and not any(('Florida' in n or 'Actively' in n) for n in names) and len(cards)>=100 else 'FAILED'},
 'person_and_whole_name':{'result':'PASSED' if naming10.is_person('Mark Smith') and not naming10.is_person('Executive Vice') and naming10.names_company('King will report to Mark Smith, President of STS Aviation Group.','Sts Aviation Group') else 'FAILED'}}
json.dump(out,open('reports/w18-gate.json','w'),indent=1,ensure_ascii=False); print({k:v['result'] for k,v in out.items()},names)
sys.exit(0 if all(v['result']=='PASSED' for v in out.values()) else 1)
