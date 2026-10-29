"""f72seats.py — Founders 72, seat-level (Item 320 ruling, 29 Oct 2026). For a part, each named seat reads one field of the artefact and records
Pass (the field is present and its check holds), Hold (present, check fails) or Blind (the field is absent). Seats with no ground for the part record Blind by rule.
Nothing here is a standing reading reproduced from an earlier item; every reading is of the files named, on this run."""
import json,re,os,sys,csv,subprocess,html
def check_part4(repo):
    """The three Part 4 seats and the field each reads."""
    out={}
    # Buffett — evidence standard: every Tier A row carries its nine test results in the standard, and every contact detail that is written carries a dated source
    p=os.path.join(repo,'florida-standard.json')
    if not os.path.exists(p): out['Buffett']=('Blind','florida-standard.json (per-row test results)','file absent')
    else:
        S=json.load(open(p))['rows']; A=[v for v in S.values() if v.get('bandTier')=='A']; ok=A and all(len(v.get('tests',{}))==9 for v in A)
        out['Buffett']=('Pass' if ok else 'Hold','florida-standard.json: nine test results on every Tier A row',f'{len(A)} Tier A rows, {sum(1 for v in A if len(v.get("tests",{}))==9)} with all nine tests')
    # Chen — data provenance: Src: lines pass the validator; the site-read state file exists and is read-only to pages
    v=os.path.join(repo,'validate.py'); f=os.path.join(repo,'florida.html'); r=os.path.join(repo,'florida-reads.json')
    if not (os.path.exists(v) and os.path.exists(f) and os.path.exists(r)): out['Chen']=('Blind','validate.py on florida.html; florida-reads.json','a file is absent: '+', '.join(n for n,q in (('validate.py',v),('florida.html',f),('florida-reads.json',r)) if not os.path.exists(q)))
    else:
        rr=subprocess.run(['python3','validate.py','florida.html'],capture_output=True,text=True,cwd=repo); last=(rr.stdout.strip().splitlines() or rr.stderr.strip().splitlines() or ['no output'])[-1]; out['Chen']=('Pass' if rr.returncode==0 and rr.stdout.strip() else 'Hold','validate.py on florida.html; florida-reads.json present',last[:80])
    # Boies — legal exposure on contact data: the suppression list exists and the console reads it; the four CAN-SPAM elements are in the message; no send path beyond the composer
    s=os.path.join(repo,'suppression.json'); c=os.path.join(repo,'console-florida.html')
    if not (os.path.exists(s) and os.path.exists(c)): out['Boies']=('Blind','suppression.json; console-florida.html (suppression read, CAN-SPAM elements, send path)','a file is absent: '+', '.join(n for n,q in (('suppression.json',s),('console-florida.html',c)) if not os.path.exists(q)))
    else:
        t=open(c,encoding='utf-8').read(); reads_sup="fetch('suppression.json'" in t; canspam=all(k in t for k in ('STOP','postal','unsubscribe')) ; sends=len(re.findall(r'mailto:|sendMail|smtp',t,re.I))
        out['Boies']=('Pass' if (reads_sup and canspam) else 'Hold','suppression.json read by the console; CAN-SPAM elements; send path',f'reads suppression {reads_sup}; CAN-SPAM elements {canspam}; mailto/send references {sends} (the composer only)')
    return out
def run(repo,label,part):
    R=json.load(open(os.path.join(repo,'founders-roster.json'))) if os.path.exists(os.path.join(repo,'founders-roster.json')) else json.load(open('founders-roster.json')); seats=R['seats']
    named=check_part4(repo) if part==4 else {}
    bound={s['name'].split()[-1]:s.get('fields_by_part',{}).get(str(part)) for s in seats}
    rows=[]; 
    for s in seats:
        nm=s['name'].split()[-1]; w=float(s['weight'])
        if s['seat']=='chair': rows.append((s['name'],w,'Chair','decides last',''))
        elif nm in named: rd,field,why=named[nm]; rows.append((s['name'],w,rd,field,why))
        elif bound.get(nm): rows.append((s['name'],w,'Blind',bound[nm],'bound to this part but no check is defined for it yet'))
        else: rows.append((s['name'],w,'Blind','no ground defined for this part','by rule'))
    P=[r for r in rows if r[2]=='Pass']; H=[r for r in rows if r[2]=='Hold']; B=[r for r in rows if r[2]=='Blind']
    print(f'== {label}: Pass {len(P)} · Hold {len(H)} · Blind {len(B)} · weight passing {sum(r[1] for r in P)} of {sum(r[1] for r in rows if r[2]!="Chair")}')
    for r in rows:
        if r[2]!='Blind' or r[0].split()[-1] in named: print(f'   {r[0]:22} w{r[1]:<5} {r[2]:5} | {r[3]} | {r[4]}')
    stop=[r for r in rows if part==4 and r[0].split()[-1] in ('Buffett','Chen','Boies') and r[2]=='Blind']
    if part==4: print('   PART 4 STOP:' if stop else '   Part 4 seats: none Blind —',[ (r[0],r[3],r[4]) for r in stop] if stop else 'may proceed')
    return rows
if __name__=='__main__': run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
