# Item 325 — all remaining markets, on the measured route table

DashRite Advisory LLC · HOT Leads · 31 October 2026 · opened on `9375ea9`, the Item 324 commit.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `9375ea9`) | 7 | 0 | 64 | 70.0 |
| On this delivery (final bytes) — reported, not adopted (entry 34) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0, Chair included.
- **Roster file:** 75 entries and 755.0.
- **Seat by seat:**
  - Buffett and Cuban read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
  - Lemonis reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
  - Herjavec votes from seat `sell`, named and merged in Item 307.
- The roster is unchanged by this pass, so the two readings agree.

## Gate and opening findings

- Head `9375ea9`. Clone against cache-busted raw: 439 of 439 files agree by length, git blob and SHA-256 (`item325-gate.json`).
- Validator baseline (§2.2): 54 of 54 market files.

**Item 324’s `index.html` did not land.** The Item 324 commit took 7 of the 8 delivered files, and the live index still read Las Vegas at 22 Verified rows against 18 in the file. The gate itself agreed, so this was not a halt. This pass’s index restatement counts from the files, so it carries Item 324’s Las Vegas restatement, and says so on the page.

**Census instrument (`item325-census.json`, zero reads).** At head it reproduces the index’s 108 call-ready rows and 4,178 dialable rows, so the opening figures are measured, not typed. It does not reproduce the index’s “all rows” or Tier C totals, which use a different universe; those are restated only by this pass’s certain changes.

**Instrument faults found during the pass:**
- **Killed runs.** The sandbox kills a background process, and stops any command at 300 seconds. Two runs died before writing their logs: 21 reads were lost in Texas, and up to 24 in Georgia (counted at the upper bound). Both count against those markets’ 150 under ruling 2. The engine was rebuilt to save after every row and to stop itself before the limit.
- **Engine known-answer test, 2 of 3.** With a number on file, it reproduced Badia Spices’ (305) 629-8000 and Quirch’s (800) 458-5252. With no number on file, Refricenter returned a published branch number, not the HQ. Wherever a company’s pages publish several numbers, the written line therefore says so and leaves it to the dialler to confirm.

**Proposed register entry 17.** A run killed by its host before its log is written loses reads that still count. The engine must persist after every read or row, and stop itself inside the host’s limit.

## §6.1 · Undated source lines

There were none. All 54 market files passed the validator at the gate, so no market in scope carried an undated line.

## §6.2 · Contact sourcing — per market, against its own 150

**Scope:** rows with a named decision maker that are short of call-ready only for want of a sourced contact.

**Order:** Route 4 ran on every row in scope. Routes 1, 2 and 3 ran only on rows Route 4 failed, each counted against the rows it was given.

**Before any write, every number passed these screens:**
- A 555 placeholder is rejected.
- A Route 4 site must carry the first word of the company’s name.
- A non-toll-free area code outside the market’s state is held as unattributed.

**Void rate:** refused and empty reads, as a share of logged reads. Lost reads are excluded.

| Market | Rows in scope | Route 4 | vs Florida 29.2% | R1 (given) | R2 (given) | R3 (given) | Rows written | Disputed | Held | Reads (of 150) | Lost | Void refused | Void empty | Void rate | Reads per row written | Rows unreached |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| texas | 61 | 26/61 (42.6%) | at or above | 1/3 | 0/0 | 0/0 | 23 | 0 | 4 | 150 | 21 | 15 | 2 | 13.2% | 5.6 | 0 |
| georgia | 83 | 24/58 (41.4%) | at or above | 0/0 | 0/0 | 0/0 | 23 | 0 | 1 | 150 | 24 | 12 | 4 | 12.7% | 6.2 | 25 |
| north-carolina | 13 | 3/13 (23.1%) | **below** | 0/10 | 0/10 | 0/10 | 3 | 0 | 0 | 61 | 0 | 9 | 11 | 32.8% | 20.3 | 0 |
| south-carolina | 17 | 6/17 (35.3%) | at or above | 0/11 | 1/11 | 2/11 | 8 | 0 | 0 | 68 | 0 | 8 | 1 | 12.7% | 9.7 | 0 |
| tennessee | 19 | 4/19 (21.1%) | **below** | 0/15 | 3/15 | 1/15 | 5 | 1 | 1 | 85 | 0 | 13 | 14 | 31.8% | 14.2 | 0 |
| virginia | 7 | 4/7 (57.1%) | at or above | 1/3 | 0/3 | 1/3 | 3 | 1 | 1 | 28 | 0 | 3 | 0 | 10.7% | 7.0 | 0 |
| wisconsin | 53 | 26/53 (49.1%) | at or above | 2/27 | 0/3 | 0/0 | 27 | 0 | 1 | 150 | 0 | 20 | 15 | 23.3% | 5.4 | 0 |
| iowa | 19 | 7/19 (36.8%) | at or above | 1/12 | 1/12 | 2/12 | 11 | 0 | 0 | 86 | 0 | 12 | 7 | 22.1% | 7.8 | 0 |
| illinois | 84 | 37/70 (52.9%) | at or above | 0/0 | 0/0 | 0/0 | 37 | 0 | 0 | 150 | 0 | 15 | 2 | 11.3% | 4.1 | 14 |
| new-jersey | 14 | 6/14 (42.9%) | at or above | 0/8 | 0/8 | 2/8 | 7 | 0 | 1 | 55 | 0 | 11 | 7 | 32.7% | 6.9 | 0 |
| indiana | 17 | 5/17 (29.4%) | at or above | 0/12 | 0/12 | 1/12 | 6 | 0 | 0 | 79 | 0 | 18 | 6 | 30.4% | 13.2 | 0 |
| kentucky | 3 | 0/3 (0.0%) | **below** | 0/3 | 0/3 | 0/3 | 0 | 0 | 0 | 19 | 0 | 4 | 2 | 31.6% | — | 0 |
| utah | 13 | 3/13 (23.1%) | **below** | 0/10 | 0/10 | 1/10 | 4 | 0 | 0 | 67 | 0 | 14 | 2 | 23.9% | 16.8 | 0 |
| missouri | 1 | 0/1 (0.0%) | **below** | 0/1 | 0/1 | 0/1 | 0 | 0 | 0 | 4 | 0 | 1 | 3 | 100.0% | — | 0 |
| minnesota | 2 | 1/2 (50.0%) | at or above | 0/1 | 0/1 | 0/1 | 1 | 0 | 0 | 6 | 0 | 2 | 2 | 66.7% | 6.0 | 0 |
| oregon | 0 | 0/0 | — | 0/0 | 0/0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | None% | — | 0 |
| new-york | 6 | 2/6 (33.3%) | at or above | 0/4 | 0/4 | 0/2 | 2 | 0 | 0 | 25 | 0 | 2 | 4 | 24.0% | 12.5 | 0 |
| chicago | — | not reached: the 1,200 total bound | | | | | | | | 0 | | | | | | all |
| california | — | not reached: the 1,200 total bound | | | | | | | | 0 | | | | | | all |
| washington | — | not reached: the 1,200 total bound | | | | | | | | 0 | | | | | | all |
| colorado | — | not reached: the 1,200 total bound | | | | | | | | 0 | | | | | | all |
| arizona | — | not reached: the 1,200 total bound | | | | | | | | 0 | | | | | | all |

**What the table shows:**
- **Route 4 below Florida’s 29.2%** in North Carolina (23.1%), Tennessee (21.1%), Utah (23.1%), Kentucky (0 of 3) and Missouri (0 of 1). Indiana matches it (29.4%).
- **Void rates** run from 10.7% (Virginia) to 32.8% (North Carolina) across markets with more than 10 reads. Each market’s own figure is its basis; none is averaged (entry 18).
- **The ceiling bound** in Texas, Georgia, Wisconsin and Illinois. Georgia left 25 rows and Illinois 14 rows with no Route 4 read; both are named in `item325-routes.json`. Texas spent its last reads on confirmations, so only 3 of its 35 Route 4 failures were given a confirmation route.
- **Oregon** had no row in scope, because no row with a named decision maker lacked only a contact.

**Held rows** (number read, not written):
- wisconsin · Baker Cheese: (202) 737-4332 — area code 202 is outside Wisconsin, and the page’s identity with this row is not established by location — read, held, not written
- new-jersey · Accurate Box Company: (518) 366-9017 — area code 518 is outside New Jersey, and the page’s identity with this row is not established by location — read, held, not written
- texas · Elliott Electric Supply: (417) 862-1313 — area code 417 is outside Texas, and the page’s identity with this row is not established by location — read, held, not written
- texas · Texas Restaurant Supply: (972) 579-4612 — site texrestaurantsupply.com does not carry the name’s first word “texas” — identity not established
- texas · Kent Companies: (616) 534-4909 — area code 616 is outside Texas, and the page’s identity with this row is not established by location — read, held, not written
- texas · James Avery Artisan Jewelry: (808) 924-7460 — site jewelrystoredirectory.com does not carry the name’s first word “james” — identity not established
- georgia · Mingledorff’s: (555) 555-5555 — placeholder number (555 exchange) — not a number
- tennessee · Cumberland International Trucks: (904) 783-9822 — area code 904 is outside Tennessee, and the page’s identity with this row is not established by location — read, held, not written
- virginia · Michael Shaps Wineworks: (434) 296-3438 — site virginiawineworks.com does not carry the name’s first word “michael” — identity not established

**Disputed rows** (“contact disputed, unresolved”, no number written):
- tennessee · Bandit Lites: candidates [[3, '(615) 641-9000'], [2, '(865) 971-3071']]
- virginia · Blanchard's Coffee Roasting: candidates [[1, '(804) 687-9443'], [3, '(804) 355-0111']]

**The total binding.** After 1,183 engine reads and 17 tier-contest reads, the 1,200 bound before Chicago, California, Washington, Colorado and Arizona.

## §3.3 · Entry 15, per market

Every call-ready row gained in every market traces to a line this pass wrote. There are 160 gained rows against 160 written lines; none is unexplained and none was lost.

| Market | Call-ready before | After | Gained by a written line | Unexplained | Lost |
|---|---|---|---|---|---|
| texas | 0 | 23 | 23 | 0 | 0 |
| georgia | 0 | 23 | 23 | 0 | 0 |
| north-carolina | 0 | 3 | 3 | 0 | 0 |
| south-carolina | 0 | 8 | 8 | 0 | 0 |
| tennessee | 0 | 5 | 5 | 0 | 0 |
| virginia | 0 | 3 | 3 | 0 | 0 |
| wisconsin | 0 | 27 | 27 | 0 | 0 |
| iowa | 0 | 11 | 11 | 0 | 0 |
| illinois | 20 | 57 | 37 | 0 | 0 |
| new-jersey | 0 | 7 | 7 | 0 | 0 |
| indiana | 0 | 6 | 6 | 0 | 0 |
| kentucky | 0 | 0 | 0 | 0 | 0 |
| utah | 0 | 4 | 4 | 0 | 0 |
| missouri | 0 | 0 | 0 | 0 | 0 |
| minnesota | 0 | 1 | 1 | 0 | 0 |
| oregon | 0 | 0 | 0 | 0 | 0 |
| new-york | 0 | 2 | 2 | 0 | 0 |
| chicago | 23 | 23 | 0 | 0 | 0 |
| california | 0 | 0 | 0 | 0 | 0 |
| washington | 0 | 0 | 0 | 0 | 0 |
| colorado | 0 | 0 | 0 | 0 | 0 |
| arizona | 0 | 0 | 0 | 0 | 0 |

## §6.3 · Tier contests in scope (3 reads each, counted against the 1,200)

- **Rosboro (Oregon): settled, Tier C on both rows.** oregon.html #70 moves B → C / Downgraded. Wynnchurch Capital partnered with management to acquire Rosboro in December 2016 (`Src: read wynnchurch.com/portfolio/rosboro-holdings 2026-10-31`). Current control was not re-read.
- **Still held:**
  - Rappahannock (Virginia): both pages refused.
  - Christensen Arms (Utah): both pages refused.
  - Zirkle (Washington): the page read did not carry the fact, and zirklefruit.com refused.
  - Hensley (Arizona): band unestablished; only a statistical “over $500 million” estimate was read.
  - Empire Southwest (Arizona): both searches refused.
  - Elliott Electric (Texas): not read; Texas’s 150 was spent.

## §6.4 · Integrity, Downgraded ⇔ Tier C, on final bytes

This pass created none of these breaks and cleared none.
- Rows breaking the rule: 274 across 15 markets. Every one is present at head.
- Mostly B/Downgraded, plus A/Downgraded in 5 markets and 2 C/Verified rows in Chicago.
- Repairing them needs a judgement not ruled here: which way each row moves, and whether a scale demotion to B carries “Downgraded”. So under §8 each market is named here at the integrity step and nothing is repaired. This pass’s writes in those markets came before the check, so they stand.

| Market | Breaks | Types |
|---|---|---|
| texas | 47 | {'B/Downgraded': 46, 'A/Downgraded': 1} |
| georgia | 22 | {'B/Downgraded': 22} |
| north-carolina | 22 | {'B/Downgraded': 22} |
| tennessee | 1 | {'B/Downgraded': 1} |
| virginia | 2 | {'B/Downgraded': 1, 'A/Downgraded': 1} |
| utah | 2 | {'B/Downgraded': 2} |
| missouri | 12 | {'B/Downgraded': 9, 'A/Downgraded': 3} |
| minnesota | 16 | {'A/Downgraded': 8, 'B/Downgraded': 8} |
| oregon | 16 | {'B/Downgraded': 15, 'A/Downgraded': 1} |
| new-york | 17 | {'B/Downgraded': 17} |
| chicago | 9 | {'C/Verified': 2, 'B/Downgraded': 7} |
| california | 13 | {'B/Downgraded': 13} |
| washington | 17 | {'B/Downgraded': 17} |
| colorado | 35 | {'B/Downgraded': 35} |
| arizona | 43 | {'B/Downgraded': 43} |

## Opening and closing census, every market

All figures are rows. Companies are restated in the index headline only.

| Market | Rows | Call-ready open → close | Short of call-ready open → close | Tier C open → close |
|---|---|---|---|---|
| texas | 188 | 0 → 23 | 119 → 96 | 69 → 69 |
| georgia | 250 | 0 → 23 | 134 → 111 | 116 → 116 |
| north-carolina | 250 | 0 → 3 | 128 → 125 | 122 → 122 |
| south-carolina | 250 | 0 → 8 | 180 → 172 | 70 → 70 |
| tennessee | 250 | 0 → 5 | 178 → 173 | 72 → 72 |
| virginia | 250 | 0 → 3 | 187 → 184 | 63 → 63 |
| wisconsin | 250 | 0 → 27 | 214 → 187 | 36 → 36 |
| iowa | 250 | 0 → 11 | 202 → 191 | 48 → 48 |
| illinois | 250 | 20 → 57 | 170 → 133 | 60 → 60 |
| new-jersey | 250 | 0 → 7 | 188 → 181 | 62 → 62 |
| indiana | 250 | 0 → 6 | 170 → 164 | 80 → 80 |
| kentucky | 250 | 0 → 0 | 166 → 166 | 84 → 84 |
| utah | 250 | 0 → 4 | 171 → 167 | 79 → 79 |
| missouri | 250 | 0 → 0 | 177 → 177 | 73 → 73 |
| minnesota | 250 | 0 → 1 | 180 → 179 | 70 → 70 |
| oregon | 250 | 0 → 0 | 165 → 164 | 85 → 86 |
| new-york | 176 | 0 → 2 | 141 → 139 | 35 → 35 |
| chicago | 288 | 23 → 23 | 132 → 132 | 133 → 133 |
| california | 162 | 0 → 0 | 122 → 122 | 40 → 40 |
| washington | 250 | 0 → 0 | 115 → 115 | 135 → 135 |
| colorado | 250 | 0 → 0 | 114 → 114 | 136 → 136 |
| arizona | 250 | 0 → 0 | 110 → 110 | 140 → 140 |

## Close

**Dial packs and Core BD Reports.** None exists in the repository for any market in scope; only Florida has them. None was created, because that would be a new build, not the regeneration §9 names.

**Index:**
- Headline Verified 3,720 / 3,637 → **3,715 / 3,632**. That includes Item 324’s Las Vegas −4, which had not landed, and Oregon −1 (Rosboro). The market column sums to the headline.
- Call-ready 108 → **268 rows / 267 companies.** Palmer Candy holds two call-ready rows in Iowa.
- Dialable 4,178 / 4,089 → 4,177 / 4,088.
- Tier C rows 1,795 → 1,796.

**Standard:** every worked market’s measured yields, void rates and reads per row are written to `florida-standard.json` (`item325_market_route_yields`), labelled by market, with no programme mean.

**Validator:** 54 of 54 on final bytes, equal to the §2.2 baseline.

## Remainder, for its own item

- Chicago, California, Washington, Colorado and Arizona: not reached.
- The Georgia and Illinois rows left unreached when their markets’ 150 bound.
- The confirmation routes not given to Texas’s Route 4 failures.
- Six tier contests still held.
- The 274 integrity breaks, which need a ruling before any repair.