"""Item 323 Part 4 wrapper around f72seats.check_part9_intake. The instrument keys seats by the last word of the seat's name, so a merged seat
(name = its theme, e.g. 'Serve the badly served, bet small') would not bind its moved check, and the instrument raises KeyError on it.
The wrapper presents each merged seat under the merged entry's name for evaluation only, then maps readings back by seat id.
Council tally: seats with votes:false are reported on record and excluded; seat count and weight are read from the roster, never typed."""
import json,os,sys,shutil,tempfile
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import f72seats
def verdict(repo_files_dir,roster_path,label):
    R=json.load(open(roster_path)); tmp=tempfile.mkdtemp()
    view=json.loads(json.dumps(R))
    for s in view['seats']:
        if 'merged_from' in s: s['name']=s['merged_from']['name']
    json.dump(view,open(os.path.join(tmp,'founders-roster.json'),'w'))
    shutil.copy(os.path.join(repo_files_dir,'florida-expansion.html'),tmp)
    named=f72seats.check_part9_intake(tmp)
    rows=[]
    for s,v in zip(R['seats'],view['seats']):
        key=v['name'].split()[-1]; w=float(s['weight']); votes=s.get('votes',True)
        if s['seat']=='chair': rd,field,why='Chair','decides last',''
        elif key in named: rd,field,why=named[key]
        else: rd,field,why='Blind','no ground defined for this part' if not s.get('fields_by_part',{}).get('9') else s['fields_by_part']['9'][:60],'by rule' if not s.get('fields_by_part',{}).get('9') else 'bound, no check'
        rows.append({'seat':s['seat'],'name':s['name'],'merged_from':s.get('merged_from',{}).get('name'),'weight':w,'votes':votes,'reading':rd,'field':field,'why':why})
    V=[r for r in rows if r['votes']]
    out={'label':label,'roster_file':{'entries':len(rows),'weight':sum(r['weight'] for r in rows)},
         'council':{'seats':len(V),'weight':sum(r['weight'] for r in V),
           'pass':sum(1 for r in V if r['reading']=='Pass'),'hold':sum(1 for r in V if r['reading']=='Hold'),'blind':sum(1 for r in V if r['reading']=='Blind'),
           'weight_passing':sum(r['weight'] for r in V if r['reading']=='Pass'),'weight_voting_excl_chair':sum(r['weight'] for r in V if r['reading']!='Chair')},
         'non_voting_on_record':[r for r in rows if not r['votes']],'named_readings':[r for r in rows if r['reading']!='Blind'],
         'part9_seats':{k:next((r['reading'] for r in rows if (r['merged_from'] or r['name']).split()[-1]==k and r['votes']),'not a voting seat (theme seat unnamed, item 307) — Blind') for k in ('Branson','Cuban','Herjavec','Jain','Bogle','Buffett','Maister','Drucker','Baker')},
         'boies_dissent':'Boies, standing dissent (ruling 28), carried in every verdict: DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.'}
    return out
if __name__=='__main__':
    print(json.dumps(verdict(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:3000])
