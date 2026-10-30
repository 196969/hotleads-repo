"""naming4.py — pattern set v4 (window eight). v3 with the and-joined truncation repaired in the build half: a name does not end at ' and'
when the next word is capitalised ('Naples Senior Living and Skilled Nursing Campus'). The ownership proof refuses parked and for-sale pages
(fault 45): the route's commonest failure, planted before the route runs."""
import re
import naming3
from naming2 import NM,I
END4=r"(?=$|,|;|:| (?i:in|for|from|to|as|amid|after|with|on|at|deal)\b| and (?=[a-z])| -)"
naming3.P3=[(n,re.compile(p.pattern.replace(naming3.END if hasattr(naming3,'END') else '', ''))) for n,p in naming3.P3] if False else naming3.P3
from naming2 import END as END2
naming3.P3=[(n,re.compile(p.pattern.replace(END2,END4))) for n,p in naming3.P3]
name4=naming3.name3; derived_hosts=naming3.derived_hosts
PARKED=re.compile(r"(?i)\bis for sale\b|buy this domain|this domain (?:is|may be) for sale|domain (?:name )?for sale|premium domain|parked (?:free|domain|page)|hugedomains|sedo\.com|afternic|dan\.com|domainmarket|undeveloped\.com|godaddy\.com/domainsearch")
def prove_site4(body,company):
    import naming2
    if PARKED.search((body or '')[:20000]): return None
    return naming2.prove_site2(body,company)
