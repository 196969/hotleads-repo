# Item 408 · The 6 November regression restored
DashRite Advisory LLC · 6 November 2026 · base c6a6644 · 196969/hotleads-repo, main

## Founders 72 (72 seats, 725.0)
- **Brief:** 2 Pass · 3 Hold · 66 Blind · Chair. Boies's standing dissent is carried.
- **Delivery:** 4 Pass · 1 Hold · 66 Blind · Chair. Boies, #55, upheld and routed to Item 412: "The index carries figures the rows do not all support."

## What was restored, from 26a7ad6 (the last clean state)
- **52 market pages:** every market page except florida.html and florida-expansion.html, which 0d2e650 did not regress.
- **27 archive pages:** their Item 382 headers are back.
- **index.html:** Ruling 1's protection of 2f27f73 is lifted for this file only.
- **Untouched:** every other file from the ten 6 November commits, including suppression.json.

## Measured
**suppression.json:** 0 entries at 4e5d5bc, 26a7ad6, 0d2e650 and head. 0d2e650 was the only commit to touch it, and changed the wording only.

**gate.py check** on a local commit of exactly these files on c6a6644: **exit 0.**
- STOP 1: 81 delivered, 81 committed, 0 missing.
- STOP 2: validator 54 of 54, guard 82 of 82.
- STOP 3: plants 5 of 5.
- STOP 4: suppression.json entries 0, in the clear 0.

| Measure | Before (live c6a6644) | After |
|---|---|---|
| Validator | 50 of 54 | 54 of 54 |
| Operator-view guard | 29 of 82 | 82 of 82 |
| Pages carrying the Day 3/10/30 cadence | 52 | 0 |
| Archive headers with "Figures measured" | 0 of 27 | 27 of 27 |

**Reversal:** 80 of 80 changed files reverse to the live bytes, byte for byte.

## Item 412 · the restored index's figures against the rows (measured; nothing edited)

| Index says | Rows measure today |
|---|---|
| 3,804 Verified rows | 3,804 rows with Status "Verified" (3,805 with the one "Verified w/ caveat") |
| 3,721 Verified companies | 3,798 distinct companies per market. My name normalisation may differ from the index's, and its method is not on file. |
| 902 / 902 expansion rows / companies | 1,343 rows, 1,343 companies |
| Call-ready 327 rows / 320 companies; Dialable 4,139 / 4,050; Acquisition backlog 182 | Not derivable here: the definitions are not on file in this repo. |

The delta is reported, not corrected. A restoration that also edits figures stops being a restoration.
