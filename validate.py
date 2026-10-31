"""validate.py — 6.1 (2026-10-29). The source validator, run in the gate before any market file is delivered, and before any hand edit is committed.
A Src: line is valid only if its own date sits on the line itself. A line runs from "Src:" to the first full stop followed by a space (or a semicolon-free end of note);
a URL's dots never end it. A date anywhere else in the note dates something else. Exit status 1 if any line fails, listing each by file, row and text.
Usage: python3 validate.py florida.html [more market files ...]"""
import re,sys,html,datetime
MONTHS={m:i+1 for i,m in enumerate(['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'])}
COLMAP={'chicago.html':{'Notes':'Flags'}}
def has_date(s):
    return bool(re.search(r'\b20\d\d-\d\d-\d\d\b|\b\d{1,2}/\d{1,2}/20\d\d\b|\b\d{1,2}/20\d\d\b|\b\d{1,2} [A-Z][a-z]{2}[a-z]*\.? 20\d\d\b|\b[A-Z][a-z]{2}[a-z]*\.? 20\d\d\b',s))
ABBR={'incl','approx','est','inc','co','corp','ltd','st','ave','jr','sr','no','vs','etc','e.g','i.e','dept','mr','mrs','ms','dr','u.s','fl'}
def line_end(rest):
    """A line ends at a full stop closing a sentence: the word before it is more than one letter and not an abbreviation,
    and the next character is a capital, an opening quote or bracket, or the end of the note. A URL's dots never end it."""
    for m in re.finditer(r'\.(?=\s|$)',rest):
        before=rest[:m.start()]; prev=before[-1:] 
        nxt=rest[m.end():].lstrip()[:1]
        # Item 320 Part 1.1 (Chair's ruling): a digit or a bracket before the full stop ends the sentence; only a single letter or a listed abbreviation continues it
        if not (prev.isdigit() or prev in ')]'):
            w=re.search(r'([A-Za-z.]+)$',before); word=(w.group(1) if w else '').lower().strip('.')
            if (len(word)==1 and word.isalpha()) or word in ABBR: continue
        if nxt=='' or nxt.isupper() or nxt in '\u201c"(\u2018': return m.start()
    return len(rest)
def lines(note):
    for m in re.finditer(r'Src:',note):
        rest=note[m.end():]; yield 'Src:'+rest[:line_end(rest)]
PRACTICE_FLAG=re.compile(r'data-practice="(Acquisitions|Fractionals|Private Equity)"')
SIGNAL_LINE=re.compile(r'(Acquisitions|Fractionals|Private Equity|PE) signal: [^\u00b7]+? \u00b7 published \d{4}-\d\d-\d\d \u00b7 read \d{4}-\d\d-\d\d \u2014 ')
def practice_flags(rows):
    """Item 320 Part 8: a practice flag on a row is valid only if the row's note carries a dated signal line for that criterion. A flag with no such line was typed, and is refused."""
    bad=[]
    for key,cells in rows:
        for m in PRACTICE_FLAG.finditer(cells):
            crit=m.group(1); lines=[x for x in SIGNAL_LINE.finditer(html.unescape(cells)) if x.group(1).replace('PE','Private Equity')==crit]
            if not lines: bad.append((key,crit))
    return bad

INTAKE_TIER='Unverified'
INTAKE_SRC=[0]   # Src: lines read in the intake table — reported, so a check that saw nothing reads as such
def intake_table(t):
    """Item 320 9.0.f: rows of the intake table (id="intake") must carry Tier 'Unverified' and an empty or 'derived' Band cell. A typed band or any other tier is refused."""
    m=re.search(r'<table id="intake">(.*?)</table>',t,re.S)
    if not m: return []
    hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',m.group(1),re.S)]; ix={h:i for i,h in enumerate(hd)}; bad=[]
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>',m.group(1),re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if not c: continue
        key=re.sub('<[^>]+>','',c[0]).strip(); band=re.sub('<[^>]+>','',c[ix['Band']]).strip(); tier=re.sub('<[^>]+>','',c[ix['Tier']]).strip()
        if band and band.lower() not in ('derived','\u2014','-'): bad.append((key,f'typed band in the intake table: {band!r}'))
        if tier!=INTAKE_TIER: bad.append((key,f'intake tier must be {INTAKE_TIER!r}, found {tier!r}'))
        for cell in c:
            for l in lines(html.unescape(re.sub(r'<[^>]+>',' ',cell))):
                INTAKE_SRC[0]+=1
                if not has_date(l): bad.append((key,'intake: '+l.strip()[:120]))
    return bad

def check(path):
    t=open(path,encoding='utf-8').read(); tb=re.search(r'<table[^>]*>(.*?)</table>',t,re.S).group(1)
    hd=[re.sub(r'\s+',' ',re.sub('<[^>]+>','',h)).strip() for h in re.findall(r'<th[^>]*>(.*?)</th>',tb,re.S)]; ix={h:i for i,h in enumerate(hd)}
    for std,hdr in COLMAP.get(path.split('/')[-1],{}).items():
        if hdr in ix and std not in ix: ix[std]=ix[hdr]
    bad=[]; n=0; flagrows=[]
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>',tb,re.S):
        c=re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)
        if not c or 'Notes' not in ix or ix['Notes']>=len(c): continue
        note=html.unescape(re.sub(r'<[^>]+>',' ',c[ix['Notes']])); key=re.sub('<[^>]+>','',c[0]).strip(); flagrows.append((key,row))
        for l in lines(note):
            n+=1
            if not has_date(l): bad.append((key,l.strip()[:120]))
    for key,crit in practice_flags(flagrows): bad.append((key,f'typed practice flag: {crit} with no dated signal line'))
    bad+=intake_table(t)
    return n,bad
if __name__=='__main__':
    fails=0
    for f in sys.argv[1:]:
        n,bad=check(f); fails+=len(bad)
        print(f'{f}: {n} Src: lines read in the main table, {INTAKE_SRC[0]} in the intake table, {len(bad)} without a date on the line itself'); INTAKE_SRC[0]=0
        for k,l in bad: print(f'   row #{k}: {l}')
    print('VALIDATOR PASSED' if not fails else f'VALIDATOR REFUSED — {fails} undated Src: line(s); the date must sit on the line itself'); sys.exit(1 if fails else 0)
