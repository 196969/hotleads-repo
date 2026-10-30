"""naming6.py — window ten: one definition of a company, shared by the precondition and the detector (fault 49 closed). A company-shaped token is
a legal-form suffix, a capitalised multi-word name, or a single capitalised word, adjacent to a signal verb \u2014 naming5.TOK/VERB, imported, not
re-implemented. The detector reports every such token in the headline and the article's own text, with its span."""
import re
import naming3,naming5
def detector_unified(text,title,field):
    found=[]; spans=[]
    pat=re.compile('('+naming5.TOK+r')\s+'+naming5.VERB+'|'+naming5.VERB+r'\s+(?:[\w\-]+\s){0,2}('+naming5.TOK+')')
    for where,txt in (('headline',title),('article text',(text or '')[:8000])):
        for m in pat.finditer(txt or ''):
            tok=(m.group(1) or m.group(2) or '').strip()
            if tok and tok not in found: found.append(tok); spans.append({'position':where,'span':txt[max(0,m.start()-30):m.end()+30]})
    return {'detector':'the precondition\u2019s company-shaped token (legal suffix, capitalised multi-word name or single capitalised word) adjacent to a signal verb, over the headline and the article\u2019s own text ('+field+')','companies_found':found[:10],'spans_examined':spans[:10]}
naming3.detector3=detector_unified
