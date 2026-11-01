#!/usr/bin/env python3
"""HOT Leads gate — the three integrity stops as code (Item 349, 2026-11-01).

Usage:  python3 gate.py check [--since <commit>]
Exit 0  all three integrity stops clear (the gate never prints a pass slogan; it prints its measurements)
Exit 2  STOP 1 — delivered-vs-committed file-count shortfall (delivery-manifest.json against the commit)
Exit 3  STOP 2 — validator below 54 of 54 market files
Exit 4  STOP 3 — a reader failed its own proof plant (reader-plants.json)
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
    if '--hashes' in sys.argv: report_hashes()
    print('integrity stops clear: 3 of 3 (measurements above)')
