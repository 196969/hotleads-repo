"""Window sixteen's gate (fault 59): exit 0 only if every proof passes."""
import subprocess,shutil,re,json,sys
out={}
r=subprocess.run(['python3','validate.py','florida-expansion.html'],capture_output=True,text=True).stdout
m=re.search(r'(\d+) in the intake table',r); out['validator_on_live']={'output':r.strip()[-220:],'intake_src_read':int(m.group(1)) if m else 0,'result':'PASSED' if m and int(m.group(1))>0 and 'VALIDATOR PASSED' in r else 'FAILED'}
shutil.copy('florida-expansion.html','/tmp/planted.html'); t=open('/tmp/planted.html',encoding='utf-8').read()
t2=t.replace('Size: Blind (ruled, window fifteen).','Size: Blind (ruled, window fifteen). Src: planted page with no date.',1); open('/tmp/planted.html','w',encoding='utf-8').write(t2)
p=subprocess.run(['python3','validate.py','/tmp/planted.html'],capture_output=True,text=True)
out['validator_on_planted_undated_intake_line']={'refused':p.returncode!=0,'output':p.stdout.strip()[-200:],'result':'PASSED' if p.returncode!=0 and t2!=t else 'FAILED'}
json.dump(out,open('reports/w16-gate.json','w'),indent=1); print({k:v['result'] for k,v in out.items()},out['validator_on_live']['intake_src_read'])
sys.exit(0 if all(v['result']=='PASSED' for v in out.values()) else 1)
