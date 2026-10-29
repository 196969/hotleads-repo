"""retire.py — Item 317 (2026-10-29). Applies retirements recorded by the console.
For each row in <market>-outreach.json carrying retired with moved false, moves that row, by key, from <market>.html
into <market>-archive.html: the archive row carries data-retired (reason, date, user, moved_to) and the reason in front
of its note; the working row is removed, never deleted from the record. Refuses a retirement with no reason or a reason
off the closed list. Run by the build, never by a page:  python3 retire.py florida"""
import json,re,sys,html
REASONS=('no longer trading','acquired','out of market','out of band')
def ok(reason): return reason in REASONS or re.fullmatch(r'duplicate of #\d+',reason or '') is not None
def main(m):
    O=json.load(open(m+'-outreach.json',encoding='utf-8')); t=open(m+'.html',encoding='utf-8').read(); a=open(m+'-archive.html',encoding='utf-8').read(); moved=[]; refused=[]
    for k,v in sorted(O.get('rows',{}).items(),key=lambda x:x[0]):
        R=v.get('retired')
        if not R or R.get('moved'): continue
        if not ok(R.get('reason')): refused.append((k,R.get('reason'))); continue
        tb=re.search(r'<tbody id="tb">(.*?)</tbody>',t,re.S); rows=[x for x in re.findall(r'<tr[^>]*>.*?</tr>',tb.group(1),re.S) if re.search(r'<td[^>]*>\s*'+re.escape(k)+r'\s*</td>',x)]
        if len(rows)!=1: refused.append((k,'row not found exactly once in '+m+'.html')); continue
        tr=rows[0]; cells=list(re.finditer(r'(<td[^>]*>)(.*?)(</td>)',tr,re.S)); last=cells[-1]
        note=f'Retired from {m}.html {R["date"]} ({R["reason"]}). '
        rec=json.dumps({k2:R[k2] for k2 in ('reason','date','user','moved_to')},ensure_ascii=False).replace('"','&quot;')
        new=re.sub(r'^<tr', '<tr data-retired="'+rec+'"', tr[:last.start(2)]+note+last.group(2)+tr[last.end(2):],count=1)
        t=t.replace(tr,'',1); ab=re.search(r'(<tbody[^>]*>)(.*?)(</tbody>)',a,re.S); a=a[:ab.end(2)]+new+a[ab.end(2):]
        R['moved']=True; v['updated']=__import__('datetime').datetime.utcnow().isoformat()+'Z'; moved.append(k)
    open(m+'.html','w',encoding='utf-8').write(t); open(m+'-archive.html','w',encoding='utf-8').write(a); json.dump(O,open(m+'-outreach.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
    print('moved:',moved,'| refused:',refused)
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else 'florida')
