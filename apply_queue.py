"""apply_queue.py — Item 320 Part 7.5. Carries CONFIRMED queue entries to the row. Run by the build after the Chair commits <market>-bot-queue.json
exported from the console. An entry is applied only if bot_status is 'confirmed' and confirmed_by and confirmed_on are present (C8: record only).
It writes the address into Email, the source into Address source as '<page> · read <date>', and 'Src: <page> · read <date>' in front of the note.
Unconfirmed, rejected or already-applied entries are never touched. Usage: python3 apply_queue.py florida"""
import json,re,sys,html
def main(m):
    Q=json.load(open(m+'-bot-queue.json',encoding='utf-8')); t=open(m+'.html',encoding='utf-8').read(); tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S)
    hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb.group(1),re.S)]; ix={h:i for i,h in enumerate(hd)}; applied=[]; refused=[]
    for k,e in Q.items():
        if e.get('bot_status')!='confirmed': continue
        if not (e.get('confirmed_by') and e.get('confirmed_on') and e.get('addr_found')): refused.append((k,'confirmed without confirmed_by, confirmed_on or an address')); continue
        note=json.loads(e.get('bot_note','{}')); src=note.get('source_url'); d=e['confirmed_on']
        if not src: refused.append((k,'no source_url')); continue
        tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S); rows=[x for x in re.findall(r'<tr[^>]*>.*?</tr>',tb.group(1),re.S) if re.search(r'<td[^>]*>\s*'+re.escape(k)+r'\s*</td>',x)]
        if len(rows)!=1: refused.append((k,'row not found exactly once')); continue
        row=rows[0]; c=list(re.finditer(r'(<td[^>]*>)(.*?)(</td>)',row,re.S)); parts=[]; last=0; page=re.sub(r'^https?://(www\.)?','',src).rstrip('/')
        for i,cell in enumerate(c):
            b=cell.group(2); h=hd[i]
            if h=='Email': b=html.escape(e['addr_found'])
            elif h=='Address source': b=f'{page} \u00b7 read {d}'
            elif h=='Notes': b=f'Src: {page} \u00b7 read {d} (address {e["addr_found"]} published on the company\u2019s own page; bot-proposed, confirmed by {html.escape(e["confirmed_by"])} on {d}). '+b
            parts.append(row[last:cell.start(2)]+b); last=cell.end(2)
        t=t.replace(row,''.join(parts)+row[last:],1); e['bot_status']='applied'; e['applied_on']=d; applied.append(k)
    open(m+'.html','w',encoding='utf-8').write(t); json.dump(Q,open(m+'-bot-queue.json','w',encoding='utf-8'),indent=1,ensure_ascii=False); print('applied:',applied,'| refused:',refused)
if __name__=='__main__': main(sys.argv[1] if len(sys.argv)>1 else 'florida')
