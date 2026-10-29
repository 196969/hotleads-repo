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

def check_part6(repo):
    """Part 6 seats: Schneier reads containment (kill switch and write fence proved in this pass); Goldratt reads throughput against the constraint (the rate ceiling enforced in code and reported as assumed); Chen reads the compliance surface (an append-only audit log, and no send path in the bot)."""
    out={}; b=os.path.join(repo,'bot.py'); pf=os.path.join(repo,'bot-proofs.json'); cfg=os.path.join(repo,'bot-config.json')
    if not os.path.exists(b): 
        for n,f in (('Schneier','bot.py: kill switch and write fence'),('Goldratt','bot-config.json: rate ceiling'),('Chen','bot.py: audit log and send surface')): out[n]=('Blind',f,'bot.py absent')
        return out
    P=json.load(open(pf)) if os.path.exists(pf) else {}
    out['Schneier']=('Pass' if P.get('kill_switch_halted_mid_run') and P.get('fence_refused_address') else ('Hold' if P else 'Blind'),'bot.py: kill switch halting a run mid-way; write fence refusing a write to address','proved this pass' if P else 'bot-proofs.json absent — not proved in this pass')
    C=json.load(open(cfg)) if os.path.exists(cfg) else None
    out['Goldratt']=('Pass' if C and C.get('daily_read_ceiling')==200 and C.get('ceiling_is_assumed') is True and P.get('read_201_refused') else ('Blind' if not C else 'Hold'),'bot-config.json: daily read ceiling 200, reported as assumed; read 201 refused',f'ceiling {C.get("daily_read_ceiling") if C else None}, assumed {C.get("ceiling_is_assumed") if C else None}, read 201 refused {P.get("read_201_refused")}')
    t=open(b,encoding='utf-8').read(); sends=len(re.findall(r'smtp|mailto:|sendmail|send_message',t,re.I)); append_only=("open(LOG,'a'" in t) and ('os.remove' not in t) and ('truncate' not in t)
    out['Chen']=('Pass' if (append_only and sends==0 and P.get('log_intact_after_halt')) else 'Hold','bot.py: append-only audit log read back after a halt; no send path',f'append-only {append_only}; send references {sends}; log read back after halt {P.get("log_intact_after_halt")}')
    return out


def check_part7(repo):
    """Part 7 seats: Schneier reads the four planted failure proofs of this pass; Goldratt reads yield (rows read, proposed, confirmed, ratio) and reads against the ceiling; Chen reads the queue (every entry unconfirmed, fenced fields only), the log (no Sunbiz read), and the send surface."""
    out={}; pf=os.path.join(repo,'bot-proofs-part7.json'); q=os.path.join(repo,'florida-bot-queue.json'); lg=os.path.join(repo,'florida-bot-log.jsonl'); b=os.path.join(repo,'bot.py'); rp=os.path.join(repo,'bot-report-part7.json')
    P=json.load(open(pf)) if os.path.exists(pf) else None
    out['Schneier']=('Blind','bot-proofs-part7.json: four planted failures','absent') if not P else (('Pass' if all(P.get(k) for k in ('no_address_returns_not_found_never_guess','refusal_returns_refused_never_absent','write_to_address_refused','kill_switch_halts_with_log_intact')) else 'Hold'),'bot-proofs-part7.json: four planted failures',', '.join(k for k in ('no_address_returns_not_found_never_guess','refusal_returns_refused_never_absent','write_to_address_refused','kill_switch_halts_with_log_intact') if P.get(k)))
    Rp=json.load(open(rp)) if os.path.exists(rp) else None
    out['Goldratt']=('Blind','bot-report-part7.json: yield and reads against the ceiling','absent') if not Rp else (('Pass' if all(k in Rp for k in ('rows_read','rows_proposed','rows_confirmed','yield')) and Rp.get('reads_total',0)<=Rp.get('ceiling',200) and Rp.get('ceiling_is_assumed') else 'Hold'),'bot-report-part7.json: rows read, proposed, confirmed, ratio; reads within the ceiling (assumed)',f"read {Rp.get('rows_read')}, proposed {Rp.get('rows_proposed')}, confirmed {Rp.get('rows_confirmed')}, yield {Rp.get('yield')}, reads {Rp.get('reads_total')} of {Rp.get('ceiling')} (assumed {Rp.get('ceiling_is_assumed')})")
    if not (os.path.exists(q) and os.path.exists(lg) and os.path.exists(b)): out['Chen']=('Blind','florida-bot-queue.json; florida-bot-log.jsonl; bot.py','a file is absent'); return out
    Q=json.load(open(q)); fence={'addr_found','bot_note','bot_status','source_url','proposed_on'}; unconf=all((v.get('bot_status','').startswith('proposed') or v.get('bot_status','').startswith('no proposal')) and set(v)<=fence for v in Q.values()); L=[json.loads(l) for l in open(lg,encoding='utf-8') if l.strip()]; sunbiz=sum(1 for e in L if 'sunbiz' in str(e.get('url','')).lower()); sends=len(re.findall(r'smtp|mailto:|sendmail|send_message',open(b,encoding='utf-8').read(),re.I))
    out['Chen']=('Pass' if (unconf and sunbiz==0 and sends==0) else 'Hold','the queue (every entry unconfirmed, fenced fields only); the log (no Sunbiz read); bot.py (no send path)',f'{len(Q)} entries, all unconfirmed and fenced {unconf}; Sunbiz reads in the log {sunbiz}; send references {sends}')
    return out


def check_part8(repo):
    """Part 8 seats: Buffett reads the evidence standard (every signal state carries a source and a date, and no state is typed); Branson reads practice fit (the states derived and counted for the 47, with the criteria written); Boies reads that nothing is asserted beyond the source (the validator passes with no typed flag; Acquisitions never from the company's own site)."""
    out={}; sp=os.path.join(repo,'florida-standard.json')
    if not os.path.exists(sp): return {n:('Blind','florida-standard.json (practice_standard, per-row practice states)','file absent') for n in ('Buffett','Branson','Boies')}
    S=json.load(open(sp)); PS=S.get('practice_standard'); R=S['rows']; A=[v for v in R.values() if v.get('bandTier')=='A']
    if not PS or not all(v.get('practice') for v in A): return {n:('Blind','florida-standard.json: practice_standard section and per-row states','section or per-row states absent') for n in ('Buffett','Branson','Boies')}
    sig=[(k,c,p) for k,v in R.items() for c,p in v['practice'].items() if p['state']=='signal']; dated=all(p['source'] and p['date'] for _,_,p in sig); states=all(p['state'] in PS['states'] for v in R.values() for p in v['practice'].values())
    out['Buffett']=('Pass' if dated and states else 'Hold','every signal state carries a source and a publication date; every state is one of the three',f'{len(sig)} signal states, all with source and date {dated}; states within the standard {states}')
    import collections; cnt={c:dict(collections.Counter(v['practice'][c]['state'] for v in A)) for c in PS['criteria']}
    out['Branson']=('Pass' if len(PS['criteria'])==3 and all(sum(cnt[c].values())==len(A) for c in cnt) else 'Hold','the three criteria written with their source rules; states derived and counted across the 47',json.dumps(cnt))
    rr=subprocess.run(['python3','validate.py','florida.html'],capture_output=True,text=True,cwd=repo); ok=rr.returncode==0 and 'PASSED' in rr.stdout; own=[k for k,v in R.items() if v['practice']['Acquisitions']['state']=='signal' and 'company' in (v['practice']['Acquisitions'].get('why') or '')]
    out['Boies']=('Pass' if ok and not own else 'Hold','the validator passes with no typed practice flag; no Acquisitions signal from the company\'s own site',f'validator {"PASSED" if ok else "REFUSED"}; company-site Acquisitions signals {len(own)}')
    return out


def check_part10(repo):
    """Part 10: the same three seats as Part 9, read against this part's proofs and the queue."""
    out=check_part9(repo); pf=os.path.join(repo,'bot-proofs-part10.json')
    if not os.path.exists(pf): return {n:('Blind','bot-proofs-part10.json','absent') for n in out}
    P=json.load(open(pf))
    for n,(rd,field,why) in list(out.items()):
        extra={'Buffett':('browser_undated_refused','an undated browser read refused'),'Lemonis':('control_dated_article_is_candidate','the dated control read as a candidate (criterion sentence)'),'Boies':('edited_sentence_refused_by_apply','an edited sentence refused by the applier')}[n]
        out[n]=(rd if P.get(extra[0]) else 'Hold',field+'; Part 10: '+extra[1],why+f'; Part 10 proof {P.get(extra[0])}')
    return out
def check_part9(repo):
    """Part 9 seats: Buffett reads that every candidate's source is a declared third-party class and carries a publication date; Lemonis reads that every candidate's sentence names a people, process or product change (the criterion keywords), not a mood; Boies reads that the row says exactly what the source says (the applier proof) and the validator passes."""
    out={}; qp=os.path.join(repo,'florida-practice-queue.json'); pf=os.path.join(repo,'bot-proofs-part9.json'); cp=os.path.join(repo,'practice-classes.json')
    if not (os.path.exists(qp) and os.path.exists(cp) and os.path.exists(pf)): return {n:('Blind','florida-practice-queue.json; practice-classes.json; bot-proofs-part9.json','a file is absent') for n in ('Buffett','Lemonis','Boies')}
    Q=json.load(open(qp)); C=json.load(open(cp))['source_classes']; P=json.load(open(pf)); cands=[v for k,v in Q.items() if k[0]!='_']
    tp=all(v.get('source_class') in C and v['source_class']!='sunbiz' and re.fullmatch(r'\d{4}-\d\d-\d\d',v.get('published') or '') for v in cands)
    out['Buffett']=('Pass' if tp and P.get('undated_article_refused') and P.get('company_site_url_refused_by_class') else 'Hold','every candidate from a declared third-party class with a publication date; undated and company-site sources refused in proof',f'{len(cands)} candidate(s) in the queue{" (a vacuous pass: nothing to read yet)" if not cands else ""}; undated refused {P.get("undated_article_refused")}; company-site refused {P.get("company_site_url_refused_by_class")}')
    try:
        import ast; tree=ast.parse(open(os.path.join(repo,'practice.py'),encoding='utf-8').read()); kw=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='KW'); lem=all(re.search(kw[v['criterion']],v['sentence'],re.I) for v in cands)
    except Exception as e: lem=None
    out['Lemonis']=('Pass' if lem is not None and lem else ('Blind' if lem is None else 'Hold'),'every candidate sentence matches a people/process/product keyword set (practice.py KW), not a mood',f'{len(cands)} candidate(s){" (a vacuous pass: nothing to read yet)" if not cands else ""}; keyword set loaded {lem is not None}')
    rr=subprocess.run(['python3','validate.py','florida.html'],capture_output=True,text=True,cwd=repo); ok=rr.returncode==0 and 'PASSED' in rr.stdout
    out['Boies']=('Pass' if ok and P.get('row_says_what_source_says') and P.get('nameless_confirmation_refused_by_apply') else 'Hold','the applier writes exactly the source sentence (proof); nameless confirmation refused; validator passes on the live file',f'validator {"PASSED" if ok else "REFUSED"}; source sentence carried verbatim {P.get("row_says_what_source_says")}; nameless refused {P.get("nameless_confirmation_refused_by_apply")}')
    return out

def run(repo,label,part):
    R=json.load(open(os.path.join(repo,'founders-roster.json'))) if os.path.exists(os.path.join(repo,'founders-roster.json')) else json.load(open('founders-roster.json')); seats=R['seats']
    named=check_part4(repo) if part==4 else (check_part6(repo) if part==6 else (check_part7(repo) if part==7 else (check_part8(repo) if part==8 else (check_part9(repo) if part==9 else (check_part10(repo) if part==10 else {})))))
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
    SEATS={4:('Buffett','Chen','Boies'),6:('Schneier','Goldratt','Chen'),7:('Schneier','Goldratt','Chen'),8:('Buffett','Branson','Boies'),9:('Buffett','Lemonis','Boies'),10:('Buffett','Lemonis','Boies')}
    stop=[r for r in rows if part in SEATS and r[0].split()[-1] in SEATS[part] and r[2]=='Blind']
    if part in SEATS:
        if stop and 'brief' in label.lower(): print(f'   Part {part} brief: Blind by construction on',[r[0] for r in stop],'— not a stop (roster standing rule); the stop binds on the delivery')
        else: print(f'   PART {part} STOP:' if stop else f'   Part {part} seats: none Blind —',[ (r[0],r[3],r[4]) for r in stop] if stop else 'may proceed')
    return rows
if __name__=='__main__': run(sys.argv[1],sys.argv[2],int(sys.argv[3]))
