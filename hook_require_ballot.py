#!/usr/bin/env python3
"""PreToolUse hook (Build Stack v4 ch.41 item 3), at the repository root. Refuses any Edit, Write or MultiEdit on a path outside the
exempt patterns in build-config.json until the Founders 72 ballot verdict on the item's brief is written to the state file.
Claude Code passes the tool call as JSON on stdin; exit 2 blocks the call and its stderr is shown to the model; exit 0 permits it.
Wired by claude-settings.json, which the build session copies to its own .claude/settings.json."""
import fnmatch, json, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__)); cfg = json.load(open(os.path.join(ROOT, 'build-config.json')))
ev = json.load(sys.stdin)
if ev.get('tool_name') not in ('Edit', 'Write', 'MultiEdit', 'NotebookEdit'): sys.exit(0)
path = os.path.relpath(os.path.abspath(os.path.join(ROOT, (ev.get('tool_input') or {}).get('file_path', ''))), ROOT).replace(os.sep, '/')
if any(fnmatch.fnmatch(path, p) for p in cfg['exempt_patterns']): sys.exit(0)
sp = os.path.normpath(os.path.join(ROOT, cfg['state_file']))
def refuse(why): print(f'REFUSED by hook_require_ballot (Item {cfg["item"]}): {why}. First edit target: {path}', file=sys.stderr); sys.exit(2)
if not os.path.exists(sp): refuse(f'no state file at {cfg["state_file"]}')
try: st = json.load(open(sp))
except Exception as e: refuse(f'state file does not parse ({e})')
b = (st.get('ballots') or {}).get('brief') or {}
if not (b.get('revision') and b.get('clock') and isinstance(b.get('seats'), list) and b.get('seat_count') == 72 and len(b['seats']) >= 1):
    refuse('the Founders 72 verdict on the brief is not in the state file (needs revision, clock, seat_count 72 and the seat readings)')
sys.exit(0)
