"""The practice field, derived from evidence on the row, never asserted. Each placement carries the phrase that placed it and the row's latest
read date. None is written explicitly with its reason. Sponsor-backed rows carrying a band-risk or above-$25M phrase are HELD and FLAGGED."""
import re
PE=re.compile(r'(?i)(PE[- ]backed|private[- ]equity|portfolio company|sponsor|backed by [A-Z][\w&]+|acquired by [A-Z][\w&]+ (?:Capital|Partners|Equity)|recapitali[sz]|H\.I\.G|Sun Capital|Boyne)')
AQ=re.compile(r'(?i)(succession(?!\s+(?:plan\s+)?in place)|no successor|for sale|selling the (?:business|company)|divest|retir(?:ing|ement)|exit (?:plan|signal|interest)|withdrawn listing)')   # a completed acquisition is history, not an exit signal
FR=re.compile(r'(?i)(vacan(?:t|cy)|interim (?:CFO|COO|controller)|hiring (?:a )?(?:CFO|COO|controller)|CFO search|no (?:CFO|controller)|owner (?:also )?(?:runs|handles|serves as) (?:finance|operations|the books))')
BAND=re.compile(r'(?i)(BAND RISK|>\s?\$?\d{2,}M|above \$?25M|\$[1-9]\d{2,}M|\$\d+(?:\.\d+)?B|billion)')
DATE=re.compile(r'\d{4}-\d\d-\d\d')
NEG=re.compile(r'(?i)\b(?:no|not|without|never)\s+(?:a\s+)?(?:published\s+)?(?:sponsor|PE|private[- ]equity|portfolio|vacancy|vacancies)[^.;]{0,30}')
def derive(text,intake_practice=None):
    text=NEG.sub(' ',text)   # a negated mention (“no sponsor or parent in note”) is evidence against, never for
    dates=DATE.findall(text); d=max(dates) if dates else 'undated'
    out=[]
    if intake_practice in ('Acquisitions','Fractionals','Private Equity'): out.append((intake_practice,'the admitted row\u2019s dated third-party signal'))
    for name,rx in (('Private Equity',PE),('Acquisitions',AQ),('Fractionals',FR)):
        m=rx.search(text)
        if m and name not in [o[0] for o in out]:
            span=text[max(0,m.start()-40):m.end()+40].strip(); out.append((name,span))
    hold=any(o[0]=='Private Equity' for o in out) and bool(BAND.search(text))
    return out,d,hold
