# Item 372-HL · The manual suppression load retired across all 27 markets
DashRite Advisory LLC · 4 November 2026 · base 4fb0e05 · 196969/hotleads-repo, main

## Founders 72 (72 seats, 725.0)
- **Brief, read on 4fb0e05:** 4 Pass · 2 Hold · 65 Blind · Chair.
  - Boies, standing dissent, carried: "standing dissent, carried: a published suppression list must expose no person; this one exposes none only because it is empty, and the day it is not, the route must change before the file does"
  - #55: "the Chair's local copy is not readable from this build; the verifying count comes from the published history (0 and 0)"
- **Delivery, read on the delivered bytes:** 6 Pass · 1 Hold · 64 Blind · Chair. Boies's standing dissent is carried, as above.

## Gate
- Before the first edit: head 4fb0e05, raw plus a fresh clone, 671 of 671 files agree on byte count, git blob and SHA-256.
- gate.py check exit 0 on live before the edit, and exit 0 on a local commit of these bytes (see the close).

## Part 1 — the count, verified
- The Chair's local copy is not reachable from this build.
- Readable copies: suppression.json at 3cfbdcd, 0 entries; at 592c7d7, 0 entries. No other suppression file exists in the repository or its history.
- Nothing readable contradicts the ruling, so Route A ships.

## What shipped
- **suppression.json** at the repository root: entries [], published 2026-11-04, note "empty — no opt-out has been recorded as of this date".
- **One reader on 54 market pages and 27 consoles.**
  - It reads the published file, fetched fresh, then this computer's copy, then merges them as a union.
  - It fails closed only when both are unreadable.
  - The same result feeds the row hold, the composer's Copy rich check and the console queue's check.
  - The status line names each source with its count, and the merge total.
- **The picker** is kept on market pages and added to all 27 consoles, writing the same key. Label: "Load an updated suppression list (optional — the published list is read automatically)".
- **The instruction**, on 54 market pages and 27 consoles: "The published suppression list is read automatically. A file loaded from this computer is optional and merges with it. Email unlocks when either reads; it locks only when both fail."

## Proof, per page (item372hl-proof-table.json; raw readings in item372hl-proof-raw.json)
Every page was rendered under six conditions:
- both sources removed (published 404, no local copy);
- the published file alone;
- the local copy alone;
- a planted suppressed address via the published file, via the local copy, and in both.

The planted address is the page's first row address where the Email column carries one, which is true on 3 pages: chicago, florida and illinois. Everywhere else it is a proof address, entered in the composer.

**81 of 81 pass every column.** Page errors: 0.

| Page | Email controls | Locked, both removed | Unlocked, published alone | Unlocked, local alone | Planted refused, every route | Planted row withheld | Published / local / merged, plant in both |
|---|---|---|---|---|---|---|---|
| arizona.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| arizona-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| california.html | 112 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| california-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| chicago.html | 238 | ✓ | ✓ | ✓ | ✓ | ✓ | 1 / 1 / 1 |
| chicago-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| colorado.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| colorado-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| florida.html | 150 | ✓ | ✓ | ✓ | ✓ | ✓ | 1 / 1 / 1 |
| florida-expansion.html | 43 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| georgia.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| georgia-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| illinois.html | 200 | ✓ | ✓ | ✓ | ✓ | ✓ | 1 / 1 / 1 |
| illinois-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| indiana.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| indiana-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| iowa.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| iowa-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| kentucky.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| kentucky-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| las-vegas.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| las-vegas-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| michigan.html | 149 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| michigan-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| minnesota.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| minnesota-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| missouri.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| missouri-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| new-jersey.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| new-jersey-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| new-york.html | 126 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| new-york-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| north-carolina.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| north-carolina-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| ohio.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| ohio-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| oregon.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| oregon-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| pennsylvania.html | 158 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| pennsylvania-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| south-carolina.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| south-carolina-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| tennessee.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| tennessee-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| texas.html | 138 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| texas-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| utah.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| utah-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| virginia.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| virginia-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| washington.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| washington-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| wisconsin.html | 200 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| wisconsin-expansion.html | 50 | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-arizona.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-california.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-chicago.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-colorado.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-florida.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-georgia.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-illinois.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-indiana.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-iowa.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-kentucky.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-las-vegas.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-michigan.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-minnesota.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-missouri.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-new-jersey.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-new-york.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-north-carolina.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-ohio.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-oregon.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-pennsylvania.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-south-carolina.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-tennessee.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-texas.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-utah.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-virginia.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-washington.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |
| console-wisconsin.html | console | ✓ | ✓ | ✓ | ✓ | — | 1 / 1 / 1 |

## Close
- Parity: zero deviations across 54 market pages and 27 consoles.
- Validator 54 of 54 · guard 82 of 82.
- End to end 32 of 32.
- Load errors 0 across 182 pages.
- Reversal: 81 of 81 changed files byte-identical. suppression.json is new.
- Google 0 · Gmail 0, including this package's own files.
