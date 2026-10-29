"""Phase 0 audit — the HOT Leads per-field correctness audit, staleness read, five-class classification and file comparison.
Mechanical rules only; every rule is printed with its result so the audit can be re-run on any market the same way."""
import re,sys,json,datetime,collections
import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.abspath(__file__))); import validate
TODAY=datetime.date(2026,10,29); WINDOW_DAYS=365
cell=lambda c: re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',c)).strip()
MONTHS={m:i+1 for i,m in enumerate(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])}
def dates(text):
    out=[]
    for y,m,d in re.findall(r'\b(20[0-9]{2})-(\d{2})-(\d{2})\b',text): out.append(datetime.date(int(y),int(m),int(d)))
    for m,d,y in re.findall(r'\b(\d{1,2})/(\d{1,2})/(20[0-9]{2})\b',text):
        if 1<=int(m)<=12: out.append(datetime.date(int(y),int(m),min(int(d),28)))
    for m,y in re.findall(r'\b(\d{1,2})/(20[0-9]{2})\b',text):
        if 1<=int(m)<=12: out.append(datetime.date(int(y),int(m),1))
    for mon,y in re.findall(r'\b([A-Z][a-z]{2})[a-z]*\.? (20[0-9]{2})\b',text):
        if mon.lower() in MONTHS: out.append(datetime.date(int(y),MONTHS[mon.lower()],1))
    for y in re.findall(r'\b(?:FY|in |since |as of |, )?(20[0-9]{2})\b',text): out.append(datetime.date(int(y),1,1))
    return out
ROLE=re.compile(r'\b(family|owners?|principal|management|team|office|leadership|founders?|estate|group)\b',re.I)
def person(name):
    w=[x for x in re.split(r'\s+',name.strip()) if x]
    if len(w)<2: return False
    if ROLE.search(name) and not re.search(r'\b(Jr|Sr|II|III)\b',name): return False
    return bool(re.match(r"^[A-Z][\w'’.\-]*$",w[0])) and bool(re.match(r"^[A-Z]",w[-1]))
def audit(path):
    t=open(path,encoding='utf-8').read(); tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S).group(1)
    hd=[cell(x) for x in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]; ix={h:i for i,h in enumerate(hd)}
    rows=[]
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',r,re.S)
        if len(c)<len(hd): continue
        C=lambda h: c[ix[h]] if h in ix else ''
        comp_raw=C('Company'); m=re.search(r'<strong>(.*?)</strong>',comp_raw,re.S); company=cell(m.group(1)) if m else cell(comp_raw).split(' ')[0]
        ground=cell(re.sub(r'<strong>.*?</strong>','',comp_raw,flags=re.S))
        note=cell(C('Notes')); dm_raw=C('Decision maker'); m2=re.search(r'<strong>(.*?)</strong>',dm_raw,re.S); dm=cell(m2.group(1)) if m2 else cell(dm_raw)
        title=cell(re.sub(r'<strong>.*?</strong>','',dm_raw,flags=re.S)) if m2 else ''
        if not m2 and ',' in dm: dm,title=[x.strip() for x in dm.split(',',1)]
        if re.search(r'not published|^—$|^-$',dm,re.I) and not re.search(r'\(',dm): dm=''
        phone=cell(C('Phone')); email=cell(C('Email')) if 'Email' in ix else None
        links=C('Links'); site=re.search(r'href="(https?://[^"]+)"',links); site=site.group(1) if site else None
        site=None if site and re.search(r'google\.|linkedin\.',site) else site
        src=[s.strip() for s in re.split(r'Src:',note)[1:]]+re.findall(r'\[Live-checked [^\]]+\][^|]*',note); D=dates(note); dated=bool(D)
        R={'file':path,'company':company,'ground':ground,'tier':cell(C('Tier')),'status':cell(C('Status')),'dm':dm,'title':title,'phone':phone,'email':email,'site':site,'note':note,'src':src,'dates':[str(d) for d in D]}
        # Item 313 (2026-10-29): a source is sourced only if the date is on the Src: line itself; a date elsewhere in the note dates something else
        # One rule, one definition (29 Oct 2026): a Src: line and its date are read by validate.py, the gate's validator; the audit imports it and never reimplements it.
        own=[l[4:] for l in validate.lines(note)]+re.findall(r'\[Live-checked [^\]]+\]',note)
        R['src_lines']=own; R['src_dated']=[validate.has_date(x) for x in own]
        R['undated_src']=[x.strip()[:120] for x,d in zip(own,R['src_dated']) if not d]
        R['f_company']='Absent' if not company else ('Sourced' if any(R['src_dated']) else 'Named-unsourced')
        # Classifier pass (2026-10-29): a trading check counts only if its date sits on the check line itself; a line ends at a full stop followed by a space, a semicolon or a bar, so a URL's dots do not end it
        # Item 320 Part 1.5: one definition of where a line ends (validate.line_end)
        _tl=[note[m.start():m.end()+validate.line_end(note[m.end():])] for m in re.finditer(r"\b(verified|checked|confirmed|active|sunbiz|registry)\b",note,re.I)]
        R['trading_lines']=[x[:140] for x in _tl if dates(x)]
        R['f_trading']='Checked' if R['trading_lines'] else 'Unchecked'
        R['f_dm']='Absent' if not dm or dm in ('—','-') else ('Role/family' if not person(dm) else ('Sourced' if dated else 'Named-unsourced'))
        R['f_title']='Absent' if not title else ('Dated' if dated else 'Undated')
        hasphone=bool(re.search(r'\d{3}[^\d]{0,3}\d{3}[^\d]{0,3}\d{4}',phone))
        R['f_phone']='Absent' if not hasphone else ('Sourced' if re.search(r'(phone|tel|number|main line|switchboard)',note,re.I) and dated else 'Present-unsourced')
        if email is None: R['f_email']='Absent (no column)'
        elif re.search(r'[\w.+-]+@[\w.-]+\.\w+',email): R['f_email']='Address'
        elif re.search(r'not published|n/?a|none',email,re.I): R['f_email']='State'
        elif re.search(r'\d{3}[^\d]{0,3}\d{3}[^\d]{0,3}\d{4}',email): R['f_email']='Malformed'
        else: R['f_email']='Absent'
        asrc=cell(C('Address source')) if 'Address source' in ix else None
        R['addrsrc']=asrc
        R['f_addrsrc']='Absent (no field)' if asrc is None else ('Sourced' if re.search(r'read 20\d\d-\d\d-\d\d',asrc) else 'Empty')
        toks=[w for w in re.findall(r'[a-z0-9]+',company.lower()) if len(w)>=4 and w not in ('company','group','international','industries','corporation','holdings','services','products','distributors','distribution','enterprises','brands','foods','america','florida','south','north','global')]
        if not site: R['f_site']='Absent'
        else:
            host=re.sub(r'^www\.','',re.match(r'https?://([^/]+)',site).group(1)).lower(); sld=re.sub(r'[^a-z0-9]','',host.split('.')[-2] if '.' in host else host)
            calnum=re.sub(r'[^a-z0-9]','',company.lower()); ctoks=[w for w in re.findall(r'[a-z0-9]+',company.lower()) if len(w)>=3]
            initials=''.join(w[0] for w in re.findall(r'[a-z0-9]+',company.lower()))
            resid=sld
            for tk in sorted(ctoks,key=len,reverse=True): resid=resid.replace(tk,'')
            ok = sld==calnum or (len(sld)>=3 and sld==initials) or len(resid)<=3 or (len(sld)>=4 and sld in calnum)
            R['f_site']='Matches' if ok else 'Mismatch'; R['site_host']=host
        tier=R['tier']; R['f_tier']='Absent' if tier not in ('A','B','C') else ('Reasoned' if re.search(r'\b(tier|fit)\b',note,re.I) else 'Asserted')
        R['f_ground']='Present' if ground else 'Absent'
        rows.append(R)
    return hd,rows
def vdates(n):
    """Item: corrected Window test (2026-10-29). Only verification dates count: a date on a Src: line, or after verified / read / checked / confirmed / live-checked. A date of an event in the company's history is not a verification date."""
    out=[]
    # Item 320 Parts 1.4-1.5: our dates only (after read, verified, checked, confirmed, Live-checked) — a publication date dates the source, not our check; the segment ends where validate.line_end says a line ends
    for seg in [n[m.start():m.end()+validate.line_end(n[m.end():])] for m in re.finditer(r'(?:\b[Vv]erified\b|\b[Rr]ead\b|\b[Cc]hecked\b|\b[Cc]onfirmed\b|Live-checked)',n)]:
        for y,m,d in re.findall(r'\b(20[0-9]{2})-(\d{2})-(\d{2})\b',seg): out.append(datetime.date(int(y),int(m),int(d)))
        for m,d,y in re.findall(r'\b(\d{1,2})/(\d{1,2})/(20[0-9]{2})\b',seg):
            if 1<=int(m)<=12: out.append(datetime.date(int(y),int(m),min(int(d),28)))
        for m,y in re.findall(r'(?<!/)\b(\d{1,2})/(20[0-9]{2})\b',seg):
            if 1<=int(m)<=12: out.append(datetime.date(int(y),int(m),1))
        for d,mon,y in re.findall(r'\b(\d{1,2}) ([A-Z][a-z]{2})[a-z]*\.? (20[0-9]{2})\b',seg):
            if mon.lower() in MONTHS: out.append(datetime.date(int(y),MONTHS[mon.lower()],min(int(d),28)))
        for mon,y in re.findall(r'(?<!\d )\b([A-Z][a-z]{2})[a-z]*\.? (20[0-9]{2})\b',seg):
            if mon.lower() in MONTHS: out.append(datetime.date(int(y),MONTHS[mon.lower()],1))
    return out
def staleness(rows):
    out=collections.Counter(); lo=TODAY-datetime.timedelta(days=365)
    for R in rows:
        D=vdates(R.get('note',''))
        if not D: R['stale']='Blind (no verification date)'; out['Blind (no verification date)']+=1
        elif all(d>=lo for d in D): R['stale']='Inside window'; out['Inside window']+=1
        else: R['stale']='Outside on a verification date'; out['Outside on a verification date']+=1
        m=re.search(r'Trading checked \((site|registry)\)',R.get('note','')); R['trading_kind']=m.group(1) if m else ('registry' if re.search(r'\b(sunbiz|registry)\b[^.]{0,40}\b20\d\d',R.get('note',''),re.I) else ('other dated check' if R.get('f_trading')=='Checked' else None))
    return out
def classify(rows):
    out=collections.Counter()
    for R in rows:
        reasons=[]
        if R['f_site']=='Mismatch': reasons.append('website names a different company')
        if R['f_dm']=='Role/family': reasons.append('role or family as decision maker')
        if R['f_email']=='Malformed': reasons.append('phone number in the Email cell')
        if R['f_title']!='Absent' and R['f_dm']=='Absent': reasons.append('title with no person')
        if not R['src'] and not R['site'] and R['f_phone']=='Absent': cls='Not real'; reasons=['no source, no website, no phone establishes the company']
        elif reasons: cls='Suspect'
        elif R['f_company']=='Sourced' and R['f_trading']=='Checked' and R['f_dm']=='Sourced' and R['stale']=='Inside window': cls='Live'
        elif R['f_company']=='Sourced' and R['stale']!='Inside window': cls='Stale'; reasons=['sourced once, outside the window' if R['stale']!='No date' else 'sourced, undated']
        elif R['f_company']=='Sourced': cls='Sourced, with gaps'; reasons=['missing '+g for g in [g for g,f in (('trading check','f_trading'),('dated decision maker','f_dm')) if R[f] not in ('Sourced','Checked')]]
        else: cls='Unsourced'; reasons=['no dated Src: line']
        R['source_state']='sourced' if R['f_company']=='Sourced' else ('blind' if re.search(r'Company source not found[^.]*refused',R.get('note',''),re.I) else 'unsourced')
        R['gaps']=[g for g,f in (('trading check','f_trading'),('dated decision maker','f_dm')) if R[f] not in ('Sourced','Checked')]
        R['class']=cls; R['why']=reasons; out[cls]+=1
    return out
if __name__=='__main__':
    files=sys.argv[1:]; ALL=[]
    for f in files:
        hd,rows=audit(f); st=staleness(rows); cl=classify(rows); ALL+=rows
        print(f'\n== {f}: {len(rows)} rows | columns {hd}')
        for fld in ['f_company','f_trading','f_dm','f_title','f_phone','f_email','f_addrsrc','f_site','f_tier','f_ground']: print(f'   {fld[2:]:10}',dict(collections.Counter(R[fld] for R in rows)))
        print('   status    ',dict(collections.Counter(R['status'] for R in rows)))
        print('   staleness ',dict(st)); print('   class     ',dict(cl))
        mis=[(R['company'],R.get('site_host')) for R in rows if R['f_site']=='Mismatch']; print(f'   website/company mismatches ({len(mis)}):',mis)
        print('   role/family decision makers:',[R['dm'] for R in rows if R['f_dm']=='Role/family'])
        print('   not real:',[R['company'] for R in rows if R['class']=='Not real'])
    json.dump(ALL,open('audit_rows.json','w'),indent=1,ensure_ascii=False)
    # file comparison
    norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
    by=collections.defaultdict(list)
    for R in ALL: by[norm(R['company'])].append(R)
    dup=[v for v in by.values() if len(v)>1]
    print(f'\n== comparison: companies appearing in more than one file: {len(dup)}')
    for v in dup:
        facts=[(R['file'],R['dm'],R['phone'],R['tier'],R['status']) for R in v]; same=len({(x[1],x[2],x[3]) for x in facts})==1
        print('   ',v[0]['company'],'|','duplicate, same facts' if same else 'CONTRADICTION','|',facts)
