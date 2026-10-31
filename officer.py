"""officer.py — #61 rebuilt (third instance): an officer is bound to a company only by the grammar of one clause, never by appearing in the same span.
A clause is cut at sentence ends, line and bar breaks, headline joins (a lower-case word followed by a capitalised run with no full stop), and at 40 words.
Frames that bind, and only these:
  S1  <Company> names|appoints|hires|promotes|taps|welcomes|announces <Person> (as|to) (its|new)* <Title>     \u2014 the company is the clause's subject
  S2  <Person>, <Title> of|at <Company>                                                                      \u2014 the company is the title's object
  S3  <Company>'s|<Company> <Title> <Person>                                                                 \u2014 the company possesses the title
Anything else binds nothing."""
import re
import naming10,naming5
TITLE=r'(Chief Executive Officer|Chief Financial Officer|Chief Operating Officer|CEO|CFO|COO|President|Founder|Co-Founder|Owner|Managing Director|Managing Partner|General Manager)'
PERSON=r"([A-Z][a-zA-Z'\-]+(?: [A-Z]\.)? [A-Z][a-zA-Z'\-]+)"
def clauses(text):
    t=re.sub(r'\s+',' ',text or '')
    parts=re.split(r'(?<=[.!?])\s+|\s*[|\u2022\u00b7]\s*|\s{2,}',t)
    out=[]
    for p in parts:
        # a headline run into body text: cut before a capitalised run that follows a word with no stop, when the run starts a new title-case headline
        p=re.sub(r"(\b[a-z][a-z0-9]*)\s+(?=(?:[A-Z][\w&'-]*\s){3,}[A-Z])",lambda m: m.group(1)+' \u2016 ',p)   # a body word then a new title-case run
        for q in p.split(' \u2016 '):
            w=q.split()
            for i in range(0,len(w),40): out.append(' '.join(w[i:i+40]))
    return out
def bind(text,company):
    core=naming5.core(company)
    if not core: return None
    for c in clauses(text):
        n=naming5.norm(c)
        if core not in n.replace(' ','') and core not in n: continue
        cn=re.escape(company.split()[0])
        for pat,frame in ((r"""(?P<co>[A-Z][\w&'.\-]*(?: (?:&|of|and|[A-Z][\w&'.\-]*))*)"""+r' (?i:names|appoints|hires|promotes|taps|welcomes|announces) (?:(?i:industry veteran|veteran|longtime|former) )?'+PERSON+r' (?i:as|to) (?:(?i:its|new|the) )*'+TITLE,'S1'),
                          (PERSON+r', (?:the )?'+TITLE+r' (?i:of|at) '+r"""(?P<co>[A-Z][\w&'.\-]*(?: (?:&|of|and|[A-Z][\w&'.\-]*))*)""",'S2'),
                          (r"""(?P<co>[A-Z][\w&'.\-]*(?: (?:&|of|and|[A-Z][\w&'.\-]*))*)"""+r"(?:\u2019s|'s)? "+TITLE+r' '+PERSON,'S3')):
            for m in re.finditer(pat,c):
                co=m.group('co'); g=[x for x in m.groups() if x and x!=co]
                person=next((x for x in g if naming10.is_person(x)),None); title=next((x for x in g if re.fullmatch(TITLE,x)),None)
                if person and title and naming10.names_company(co,company): return {'name':person,'title':title,'frame':frame,'clause':c[:220]}
    return None
