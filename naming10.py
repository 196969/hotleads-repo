"""naming10.py — #60 and #61, one class: a span is not the thing it resembles. A person is two or three name words none of which is a title or
role word; an officer sentence counts only when it carries the company's whole name (normalised), not its first word."""
import re,html
import naming5
ROLEW=set('executive vice president senior chief officer director manager general principal owner founder co-founder partner managing operating financial technology marketing sales operations head lead regional national assistant associate deputy interim acting board chair chairman chairwoman member team staff our the meet about contact read view'.split())
def is_person(name):
    w=(name or '').replace('.',' ').split()
    if not (2<=len(w)<=3): return False
    if any(x.lower() in ROLEW for x in w): return False
    return all(re.fullmatch(r"[A-Z][a-zA-Z'\-]*",x) for x in w)
def names_company(sentence,company):
    c=naming5.core(company)
    if not c: return False
    n=' '+naming5.norm(sentence)+' '
    return (' '+c+' ') in n or (' '+c.replace(' ','')+' ') in n
