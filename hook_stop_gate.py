#!/usr/bin/env python3
"""Stop hook (Build Stack v4 ch.41 item 2), at the repository root. Before a session may stop, the gate and the item's evals run on the bytes
as they stand. Any non-zero exit blocks the stop (exit 2) and names the check; every exit code is read from the program, never from a pipe."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); cfg = json.load(open(os.path.join(ROOT, 'build-config.json'))); bad = []
for cmd in [cfg['gate']] + cfg['evals']:
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ['no output'])[-1]
    print(f'{" ".join(cmd)} -> exit {r.returncode} · {tail[:160]}', file=sys.stderr)
    if r.returncode != 0: bad.append(' '.join(cmd))
if bad: print('STOP REFUSED: ' + '; '.join(bad), file=sys.stderr); sys.exit(2)
sys.exit(0)
