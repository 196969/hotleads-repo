#!/usr/bin/env python3
"""HOT Leads gate — the three integrity stops as code (Item 349, 2026-11-01).

Usage:  python3 gate.py check [--since <commit>]
Exit 0  all three integrity stops clear (the gate never prints a pass slogan; it prints its measurements)
Exit 2  STOP 1 — delivered-vs-committed file-count shortfall (delivery-manifest.json against the commit)
Exit 3  STOP 2 — validator below 54 of 54 market files
Exit 4  STOP 3 — a reader failed its own proof plant (reader-plants.json)
Exit 10 STOP 9 — an archive row breaks the archive invariant: every row Tier C, Status Downgraded, Pending by rule or Research pending
Exit 8  STOP 7 — an index figure disagrees with the rows, re-counted by index_measure.py, or a figure the method covers is missing
Exit 7  STOP 6 — a Google or Gmail route, font, script or search URL on a market, expansion or archive page
Exit 6  STOP 5 — a market page carries the retired Day 3/10/30 cadence (the one cadence is the six-step sequence)
Exit 5  STOP 4 — the plain suppression file is not empty (suppression.json): the hashed route is required once any entry exists
Everything else is reported and does not halt.
"""
import sys, os, json, subprocess, hashlib, glob, urllib.request, time

def sh(*a): return subprocess.check_output(a).decode()

def stop1(since):
    if not os.path.exists('delivery-manifest.json'):
        print('STOP 1 · no delivery-manifest.json in the head — cannot count the delivery'); return False
    m = json.load(open('delivery-manifest.json'))
    delivered = sorted(m['files'])
    committed = sorted(sh('git', 'diff', '--name-only', since or m['base'], 'HEAD').split())
    missing = [f for f in delivered if f not in committed]
    print(f"STOP 1 · file count by name: delivered {len(delivered)} · committed {len(committed)} · missing {len(missing)} {missing}")
    return not missing

def stop2():
    markets = sorted({os.path.basename(p).replace('-expansion.html', '') for p in glob.glob('*-expansion.html')})
    files = [g for m in markets for g in (m + '.html', m + '-expansion.html') if os.path.exists(g)]
    ok = sum(subprocess.run([sys.executable, 'validate.py', f], capture_output=True).returncode == 0 for f in files)
    print(f"STOP 2 · validator {ok} of {len(files)}")
    og = subprocess.run([sys.executable, 'opview_guard.py'], capture_output=True, text=True)   # Item 359: the operator view stays clean
    print('STOP 2 · ' + (og.stdout.strip().splitlines() or ['operator-view guard: no output'])[-1])
    return ok == len(files) == 54 and og.returncode == 0

def stop3():
    if not os.path.exists('reader-plants.json'):
        print('STOP 3 · no reader-plants.json — no reader has proved itself; nothing may be read'); return False
    P = json.load(open('reader-plants.json'))
    bad = [p['plant'] for p in P['plants'] if p['result'] != p['expected']]
    print(f"STOP 3 · reader plants {len(P['plants']) - len(bad)} of {len(P['plants'])} as expected · failed {bad}")
    return not bad

def stop4():
    # Item 381-G (2026-11-04): under the ruled route the plain published list may only ever be empty.
    # A non-empty plain file is a refusal, not a warning; the message names the route, not only the fault.
    ROUTE = 'plain suppression file carries a readable address; the hashed route is required once any entry exists'
    if not os.path.exists('suppression.json'):
        print('STOP 4 · suppression.json not present · nothing published, nothing exposed'); return True
    try:
        S = json.load(open('suppression.json', encoding='utf-8'))
    except Exception as e:
        print(f'STOP 4 · suppression.json does not parse ({e}) · it cannot be shown to carry no address · refused'); return False
    E = S.get('entries') if isinstance(S, dict) else None
    if not isinstance(E, list):
        print('STOP 4 · suppression.json has no entries array · it cannot be shown to carry no address · refused'); return False
    clear = [i for i, e in enumerate(E) if isinstance(e, dict) and any(isinstance(e.get(k), str) and e.get(k).strip() for k in ('address', 'domain'))]
    why = ROUTE if clear else 'plain suppression file is not empty; the hashed route is required once any entry exists'
    print(f"STOP 4 · suppression.json entries {len(E)} · in the clear {len(clear)}" + ('' if not E else f' · refused: {why}'))
    return len(E) == 0

def stop5():
    # Item 413 (2026-11-06): the Day 3/10/30 Log-touch cadence arrived three times with a stale copy and was caught each time
    # only by inference from the counts. This stop names it. The one cadence is the six-step page sequence (days 0, 3, 8, 15, 25, 40).
    import glob, re
    M = sorted({os.path.basename(p)[:-len('-expansion.html')] for p in glob.glob('*-expansion.html')})
    pages = [g for m in M for g in (m + '.html', m + '-expansion.html', m + '-archive.html') if os.path.exists(g)]
    rx = re.compile(r'Day\s*3\s*/\s*10\s*/\s*30', re.I)
    hit = [p for p in pages if rx.search(open(p, encoding='utf-8', errors='replace').read())]
    print(f'STOP 5 · Day 3/10/30 cadence on {len(hit)} of {len(pages)} market pages' + (f' · refused: {hit[:5]}' if hit else ''))
    return not hit

def stop6():
    # Item 413 Ruling 10 (2026-11-06): Google and Gmail were cleaned out once; this stop holds them out. Any http(s) route to a
    # Google host (search, news, fonts, static assets, tag manager, analytics, mail) or any Gmail address fails, on every
    # market, expansion and archive page derived from the market set.
    import glob, re
    M = sorted({os.path.basename(p)[:-len('-expansion.html')] for p in glob.glob('*-expansion.html')})
    pages = [g for m in M for g in (m + '.html', m + '-expansion.html', m + '-archive.html') if os.path.exists(g)]
    rx = re.compile(r'https?://[^\s"\'<>]*\b(?:google|googleapis|gstatic|googletagmanager|google-analytics|googleusercontent|gmail)\.[a-z]|[\w.+-]+@gmail\.com|mail\.google\.com', re.I)
    hit = {}
    for p in pages:
        n = len(rx.findall(open(p, encoding='utf-8', errors='replace').read()))
        if n: hit[p] = n
    print(f'STOP 6 · Google or Gmail route on {len(hit)} of {len(pages)} market pages' + (f' · refused: {dict(list(hit.items())[:5])}' if hit else ''))
    return not hit

def stop7():
    # Item 413 (2026-11-06): every counted figure on index.html is re-counted from the market files by index_measure.py and must
    # match at zero tolerance; a figure the method does not know, or one it covers that is missing, fails. All four company rules
    # are measured on every run; the page carries the headline rule (legal form folded only inside one market) and the kept-form
    # alternative, and must not carry the struck full-fold or PA-excluded counts.
    import re, index_measure as I
    o = I.measure('.')
    s = open('index.html', encoding='utf-8').read()
    hp, hs, wrong = I.held(s, o, True)
    want = {k: o[k] for k in ('markets', 'full_treatment', 'verified_rows', 'verified_cos_within', 'verified_cos_kept', 'kept_minus_within',
                              'expansion_rows', 'expansion_verified', 'dialable_ab', 'call_ready_email', 'tier_contradictions')}
    want.update(held_pairs=hp, held_still=hs)
    for m, c in o['cards'].items():
        want['ver:' + m] = '%d · %d' % (c['ver_rows'], c['ver_cos'])
        want['all:' + m] = '%d · %d' % (c['rows'], c['cos'])
        want['exp:' + m] = c['exp_ver']
    got = {k: re.sub(r'<[^>]+>', '', v).replace(',', '').strip() for k, v in re.findall(r'data-m="([^"]+)"[^>]*>(.*?)</(?:b|td|span)>', s, re.S)}
    for k in got:
        if k.startswith('vcall:'):
            want[k] = o['cards'][k[6:]]['vcall']
    bad = [(k, str(v), got.get(k)) for k, v in want.items() if got.get(k) != str(v)]
    extra = [k for k in got if k not in want]
    cp, cf, cbad = I.count_lines('.')   # Item 416: every market page's printed count line, re-counted from its own rows
    bad += [('count line ' + f, k, str(a), str(v)) for f, k, v, a in cbad]
    want_n = len(want) + cf
    print(f'STOP 7 · index and count-line figures matching the rows: {want_n - len(bad)} of {want_n} ({len(want)} on the index, {cf} on {cp} market count lines)'
          f' · company rules measured: within-market fold {o["verified_cos_within"]}, kept {o["verified_cos_kept"]}, full fold {o["verified_cos_foldall"]}, fold without PA {o["verified_cos_fold_nopa"]}'
          + (f' · disagree: {bad}' if bad else '') + (f' · unknown: {extra[:4]}' if extra else '')
          + (f' · held-pair tiers printed wrong: {wrong[:4]}' if wrong else ''))
    return not bad and not extra and not wrong

def stop9():
    # Item 415 (2026-11-06): the archive invariant, guarded. Every row on every <market>-archive.html (derived from the market
    # set) is Tier C and reads Downgraded, Pending by rule or Research pending; none reads Verified. Status records the row's
    # standing, not whether a decision maker was found (florida-standard.json, declared_exclusions.archives.invariant).
    import glob, index_measure as I
    M = sorted({os.path.basename(p)[:-len('-expansion.html')] for p in glob.glob('*-expansion.html')})
    ok = {'Downgraded', 'Pending by rule', 'Research pending'}
    n = 0; bad = []
    for m in M:
        f = m + '-archive.html'
        if not os.path.exists(f):
            bad.append((m, 'no archive page')); continue
        hd, R = I.rows(f)
        si, ti, ci = hd.index('Status'), hd.index('Tier'), hd.index('Company')
        for k, r in enumerate(R):
            n += 1
            st, t = I.cl(r[si]), I.cl(r[ti])
            if t != 'C' or st not in ok:
                bad.append((m, 'row %d' % (k + 1), I.company(r[ci]), 'Tier ' + t, st))
    print(f'STOP 9 · archive invariant: {n - len(bad)} of {n} archive rows hold it' + (f' · refused: {bad}' if bad else ''))
    return not bad

def report_hashes():
    head = sh('git', 'rev-parse', 'HEAD').strip()
    files = sh('git', 'ls-files').split(); bad = 0
    for f in files:
        try:
            b = urllib.request.urlopen(f'https://raw.githubusercontent.com/196969/hotleads-repo/{head}/{f}', timeout=60).read()
        except Exception as e:
            print('report · raw unreadable', f, e); bad += 1; continue
        if hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest() != sh('git', 'rev-parse', 'HEAD:' + f).strip(): bad += 1
    print(f"report · head {head[:12]} · commit-pinned raw agrees on {len(files) - bad} of {len(files)} files")

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] != 'check': print(__doc__); sys.exit(1)
    since = sys.argv[sys.argv.index('--since') + 1] if '--since' in sys.argv else None
    if not stop1(since): sys.exit(2)
    if not stop2(): sys.exit(3)
    if not stop3(): sys.exit(4)
    if not stop4(): sys.exit(5)
    if not stop5(): sys.exit(6)
    if not stop6(): sys.exit(7)
    if not stop7(): sys.exit(8)
    if not stop9(): sys.exit(10)
    if '--hashes' in sys.argv: report_hashes()
    print('integrity stops clear: 8 of 8 (measurements above)')
