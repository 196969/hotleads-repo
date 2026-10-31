"""Gate (#59): the inherited instruments re-proved on planted cases before first use in Chicago and Illinois."""
import json,sys,officer,roster,coverage_panel,naming10
o={}
cases=[('TrakAmerica','Collections firms TrakAmerica and peers grow Millennium Capital & Recovery Corporation Appoints Industry Veteran Jason Collins as President',None),('STS Aviation Group','King will report to Mark Smith, President of STS Aviation Group.','Mark Smith'),('Health Network One','Personnel note: Health Network One appoints Heyward Donigan as CEO','Heyward Donigan'),('Alpha Foundations','Alpha Foundations General Manager Nick Blasco said the deal closes Friday.','Nick Blasco')]
o['officer extractor (#61)']=all((officer.bind(t,c) or {}).get('name')==x for c,t,x in cases)
cards=roster.suncap_cards(open('scratch-suncap.html',errors='ignore').read()); o['roster reader']=len([c for c in cards if c['location']=='Florida'])==6
c=coverage_panel.build({'a':{'reads':0},'b':{'reads':1,'answered':0,'refused':{}},'c':{'reads':2,'answered':2},'d':{'reads':3,'answered':0,'refused':{'403':3}},'e':{'state':'exhausted'},'f':{'state':'closed'}},'/tmp/p.html'); o['source-coverage panel']=all(v==1 for v in c.values())
o['person test (#60)']=naming10.is_person('Mark Smith') and not naming10.is_person('Executive Vice') and not naming10.is_person('Principal Greg')
r={k:('PASSED' if v else 'FAILED') for k,v in o.items()}; json.dump(r,open('chi-gate.json','w'),indent=1); print(r); sys.exit(0 if all(v=='PASSED' for v in r.values()) else 1)
