# Item 356 — rung 3 resumed · halted on the refusal stop

DashRite Advisory LLC · HOT Leads · 2026-11-01 · head before `a634164` · **this upload holds 8 files**, listed at the end.

## Verdicts

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `a634164`) | 7 of 72 | 0 | **64 of 72** | 70.0 |
| On this delivery (final bytes) | 7 of 72 | 0 | **64 of 72** | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate at the open

`gate.py` exited 4, as expected: file count 12 of 12, validator 54 of 54, stop 3 set. The full repository agrees, 596 of 596 files.

## The stop I chose, stated so you can overrule it

You said “begin” without picking between the two thresholds. Under A8, I chose to **count refusals only** toward the quarter stop, because that matches its stated purpose: a refusing route, not poor rows. The minimum sample is 8 rows, as before.

## Rung 3, rows 9 onward — halted after 14 rows

| Row | Result | Reads |
|---|---|---|
| florida.html#26 JM Family Enterprises | — · no company site in the search results | 1 |
| florida.html#27 World Kinect | — · no number on the company pages read | 2 |
| florida.html#28 HEICO | — · site heico.com refused | 2 |
| florida.html#33 Eco Window Systems | — · no number on the company pages read | 2 |
| florida.html#40 Florida Crystals | — · no company site in the search results | 1 |
| florida.html#41 Vigo Importing | — · no company site in the search results | 1 |
| florida.html#43 Great Bay Distributors | — · site greatbaybud.com refused | 2 |
| florida.html#48 Rooms To Go | (888) 709-5380 · company page | 2 |
| florida.html#51 Helios Technologies (Sun Hydraulics) | — · no company site in the search results | 1 |
| florida.html#54 Bealls Inc. | (800) 683-8039 · company page | 3 |
| florida.html#55 Tervis | — · no number on the company pages read | 3 |
| florida.html#63 Regal Boats | — · site regalboats.com refused | 2 |
| florida.html#73 Beaver Street Fisheries | — · no company site in the search results | 1 |
| florida.html#80 Boston Whaler | — · site bostonwhaler.com refused | 2 |

**The halt:** 4 of 14 rows were refused (heico.com, greatbaybud.com, regalboats.com, bostonwhaler.com), which is more than a quarter.

**The other misses:**
- 5 rows had no company site that passed the whole-name rule.
- 3 sites were read and showed no number within the 3-read path.

**All four refusals were plain fetches.** Firecrawl answered two plain-fetch refusals earlier today, so these four are evidence about our reader until they are re-probed. The keyless tier can’t carry that many requests; **a free Firecrawl API key would.**

## Counts (Section 3.5), each reproducible from the delivered files

| Count | Value |
|---|---|
| Rows worked this item | 14 (rows 9–22 of the 73) |
| Rows sourced | 2: Rooms To Go, **(888) 709-5380** from roomstogo.com; Bealls Inc., **(800) 683-8039** from beallsinc.com/beallsinc/contact |
| Unresolved at cost | 0 — no row reached 5 reads |
| Reads | 25 of 188 this item · **44 of 207** across Items 355–356 |
| Backlog | 195 → **193** |
| Call-ready | 314 → **316** · gained: florida #48 and #54 · lost: none · entry 15 clean (2 gained, 2 lines written) |

**Both new numbers are toll-free.** Each replaced an unsourced local number (Tampa 813 and Bradenton 941). The rule writes the sourced one. If Eddie needs the local lines, they need sources naming them.

## Close

- **Validator:** 54 of 54.
- **Index:** call-ready 316 / 309 (companies by name); backlog 193; Item 356 note added.
- **Register:** three entries, each with its evidence.

## To continue rung 3

51 of the 73 rows are left, and 163 reads. Either of these would let it proceed honestly:
1. **A free Firecrawl API key.** The four refused sites are re-probed once, and the run continues with Firecrawl behind the plain fetch.
2. **Your ruling** to continue under the refusal stop as it stands. It would likely fire again on the next refused site.

## The 8 files in this upload

- delivery-manifest.json
- florida-standard.json
- florida.html
- index.html
- item356-founders72-verdicts.json
- item356-read-log.jsonl
- item356-report.md
- item356-rows.json