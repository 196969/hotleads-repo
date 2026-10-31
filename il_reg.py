"""Item 321: the Illinois register, parsed only as the Secretary of State's published layouts define it (proc_corp_data.pdf, proc_llc_data.pdf).
Join key: the 8-digit file number, positions 1-8 in every file. Read from the zips as handed over; nothing is fetched."""
import zipfile,glob,re
UP='/mnt/user-data/uploads/'
def lines(key):
    zf=zipfile.ZipFile(sorted(glob.glob(UP+f'*{key}.zip'))[-1])
    with zf.open(zf.infolist()[0]) as fh:
        fh.readline()
        for ln in fh:
            r=ln.decode('latin-1').rstrip('\r\n')
            if r.startswith('END OF FILE'): return
            yield r
def core(n):
    n=re.sub(r"[\u2019'`]",'',n.upper()); n=re.sub(r'\(.*?\)','',n); n=n.replace('&',' AND '); n=re.sub(r'[^A-Z0-9 ]',' ',n)
    n=re.sub(r'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|THE|LTD|LIMITED|LP|LLP|PC|PLLC)\b',' ',n); return ' '.join(n.split())
