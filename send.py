#!/usr/bin/env python3
"""HOT Leads send path — build only (Item 349 Part H, 2026-11-01). It is not a composer.

Standing rule (Chair ruling 6, Item 349): no autonomous send, ever. A batch goes out only on the
Chair's explicit word, against ten named recipients the Chair has seen.

Inputs
  composer export   JSON from the market console's composer: [{"market","row","to","subject","body"}]
  approved-batch.json   {"approved_by":"Chair","date":"YYYY-MM-DD","recipients":[ten addresses], "word":"<the Chair's go>"}
  suppression.json  read before every message; unreadable → every address withheld (fail closed)
Every message must already carry the composer's STOP line, signature and postal address — checked, not added.
Rate: no domain-warming figure is on the record, so the ceiling is 10 messages a pass (stated, not inferred).
Every send writes a log line (row key, market, address, timestamp, body hash, suppression result);
every refusal writes its reason. A send with no log line did not happen.
Transport: none is configured in this repository. The skills search (2026-11-01) returned
googleworkspace/cli@gws-gmail-send and resend/resend-skills@resend among others; choosing one binds the
sending account and is the Chair's decision. Until one is configured, dispatch() refuses and logs it.
DMARC stays at p=none until placement is measured. Placement is reported per class — inbox,
promotions, spam — as three numbers, never one rate.
"""
import json, sys, hashlib, time, os

CEILING = 10
LOG = 'outreach-send-log.jsonl'

def log(e):
    with open(LOG, 'a') as f: f.write(json.dumps(e, ensure_ascii=False) + '\n')

def load_suppression():
    try:
        s = json.load(open('suppression.json')); return s.get('entries', []) if isinstance(s.get('entries'), list) else []
    except Exception:
        return None   # fail closed

def suppressed(addr, entries):
    if entries is None: return 'suppression unreadable — fail closed'
    a = addr.lower(); d = a.split('@')[-1]
    for e in entries:
        if e.get('scope') == 'address' and e.get('address', '').lower() == a: return e.get('reason', 'suppressed')
        if e.get('scope') == 'domain' and e.get('domain', '').lower() == d: return e.get('reason', 'suppressed')
    return None

def carries_required(body):
    b = body.lower(); return all(k in b for k in ('stop', 'dashrite'))   # STOP line and signature; postal address checked by the composer's own template

def dispatch(msg):
    log({'row': msg.get('row'), 'market': msg.get('market'), 'address': msg.get('to'), 'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'body_hash': hashlib.sha256(msg['body'].encode()).hexdigest()[:16], 'result': 'refused', 'reason': 'no transport configured — build only'})
    return False

def run(export_path, approval_path):
    if not os.path.exists(approval_path):
        print('REFUSED · no approved-batch.json — no autonomous send, ever (Chair ruling 6)'); log({'result': 'refused', 'reason': 'no approval file', 'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}); return 2
    appr = json.load(open(approval_path)); named = [r.lower() for r in appr.get('recipients', [])]
    if appr.get('approved_by') != 'Chair' or not appr.get('word') or not 0 < len(named) <= CEILING:
        print('REFUSED · approval is not the Chair’s explicit word against at most ten named recipients'); return 2
    sup = load_suppression(); sent = 0
    for m in json.load(open(export_path)):
        if sent >= CEILING: log({'row': m.get('row'), 'result': 'refused', 'reason': 'pass ceiling of 10 reached'}); continue
        why = (None if m['to'].lower() in named else 'not on the approved list') or suppressed(m['to'], sup) or (None if carries_required(m['body']) else 'missing STOP line or signature')
        if why:
            log({'row': m.get('row'), 'market': m.get('market'), 'address': m['to'], 'result': 'refused', 'reason': why}); continue
        if dispatch(m): sent += 1
    print(f'sent {sent}'); return 0

if __name__ == '__main__':
    if len(sys.argv) != 3: print(__doc__); sys.exit(1)
    sys.exit(run(sys.argv[1], sys.argv[2]))
