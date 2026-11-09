---
name: brief
description: Read before writing, balloting or building against any DashRite brief. Governing text is document 15 (Comprehensive Brief Standard) at its current revision; this file carries only the checks the Chair has ruled, by date, so a build cannot start on a brief that fails them.
---
# Brief checks (Build Stack v4 ch.41 item 1)
Document 15 governs. This list is not a restatement of it; each line is a Chair ruling with its date.
1. A brief carries a revision mark and a clock-read timestamp, or it is not ballotable (5 Nov 2026). Where a Chair order arrives without one, the build session files it as a consolidated brief at its own clock read, attributed to the order, and the ballot attaches to that revision (Item 422).
2. No amendment by reference: a brief is reissued consolidated (5 Nov 2026).
3. Every section names its mechanism and its file (document 15 Revision 3, 9 Nov 2026).
4. Every rule carries a fire case and a not-fire case, as files graded by code, written before the first edit (9 Nov 2026).
5. Every plant proves well-formedness against the store's writers before it proves firing (Item 421, 9 Nov 2026).
6. Gate first; the Founders 72 ballot on the brief second, its verdict written to the state file; the first edit third. The PreToolUse hook (hook_require_ballot.py) refuses the first edit until the verdict is there (Item 422).
7. The pre-issue checklist in document 15 §21 is read before a brief issues.
