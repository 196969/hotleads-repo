# Item 327 — consolidated pass (Parts A–D)

DashRite Advisory LLC · HOT Leads · 31 October 2026 · opened on `4cb0e27`, the Item 326 commit.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `4cb0e27`) | 7 | 0 | 64 | 70.0 |
| On this delivery (final bytes) — reported, not adopted (entry 34) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

- Head `4cb0e27`. The commit holds all 14 of Item 326’s delivered files, byte for byte.
- Clone against cache-busted raw: 449 of 449 files agree.
- The commit was under 5 minutes old at the first read, so the 14 changed files were also read at the commit-pinned address. All 14 agree (`item327-gate.json`).
- Validator baseline: 54 of 54.

## Part A — Item 327a · the 32 rows (zero reads)

- **A1, employee-owned (21):** 19 moved Downgraded → Verified; 2 named and left. Tier is unchanged.
- **A2, competitors (11):** all 11 moved Downgraded → Unverified.
- The four-outcome status mapping is recorded in `florida-standard.json` as a dated amendment, with its reason.

| Market | Row | Result | The clause it moved on |
|---|---|---|---|
| texas | Gulf Coast Machine & Supply (#28) | named and left | read in full: the note says “privately held, no co-op or ESOP indicators” — it negates employee ownership; Ite |
| texas | Austin Industries (#32) | Verified | Employee-owned (ESOP). |
| texas | SpawGlass (#34) | Verified | Employee-owned (ESOP) since 1953. |
| texas | Bartlett Cocke General Contractors (#36) | Verified | Employee-owned. |
| texas | Chamberlin Roofing & Waterproofing (#44) | Verified | Employee-owned. |
| texas | TDIndustries (#47) | Verified | Employee-owned (ESOP) since 1952. |
| texas | Improving (#77) | Verified | Employee-owned technology consultancy. |
| texas | Sammons Enterprises (#93) | Verified | Employee-owned holding company. |
| texas | Higginbotham Insurance (#94) | Verified | Employee-owned insurance brokerage. |
| georgia | Choate Construction (#76) | Verified | Employee-owned since 1989. |
| georgia | Gay Construction (#81) | named and left | the note asserts the ESOP class without a clause establishing employee ownership |
| georgia | McCarthy GA (#93) | Verified | Employee-owned. |
| georgia | Tindall Corporation GA (#119) | Verified | Employee-owned. |
| north-carolina | National Spinning (#60) | Verified | OWNERSHIP: EMPLOYEE-OWNED since the 1990s, not family — the fourth NC family-to-employee-ownership case in thi |
| north-carolina | LandDesign (#100) | Verified | Employee-owned. |
| north-carolina | McAdams Company (#139) | Verified | Employee-owned. |
| north-carolina | Stewart Inc. (#141) | Verified | Employee-owned. |
| north-carolina | Little Diversified Architectural (#144) | Verified | Employee-owned. |
| missouri | QuikTrip MO (#17) | Verified | Oklahoma employee-owned parent. |
| missouri | UHY MO (#144) | Unverified | National firm — competitor. |
| minnesota | Baker Tilly MN (#168) | Unverified | Competitor. |
| minnesota | Wipfli MN (#169) | Unverified | Competitor. |
| new-york | Stewart’s Shops (#11) | Verified | Family and employee-owned. |
| california | Stater Bros. Markets (#70) | Verified | Family and employee-owned since 1936. |
| washington | Clark Nuber (#101) | Unverified | Accounting firm — competitor. |
| washington | Moss Adams (#102) | Unverified | Large accounting/advisory — competitor. |
| colorado | ACM LLP (#165) | Unverified | Accounting firm — competitor. |
| colorado | Richey May (#166) | Unverified | Accounting/advisory — competitor. |
| colorado | Causey Demgen & Moore (#167) | Unverified | Accounting firm — competitor. |
| colorado | Stockman Kast Ryan (#168) | Unverified | Accounting firm — competitor. |
| colorado | Dalby Wendland (#169) | Unverified | Accounting firm — competitor. |
| arizona | Henry+Horne (#52) | Unverified | Accounting firm — competitor. |

**Named and left:**
- **Gulf Coast Machine & Supply:** the note says “no co-op or ESOP indicators”. It negates employee ownership; Item 326 filed it under employee-owned on a keyword match, in error.
- **Gay Construction:** the note names the “ESOP class” without a clause that establishes employee ownership.

**A3, the 167 restated.** In Item 326’s 15 markets, measured on final bytes after Parts A and C: **167 → 131.**
- The brief projected 136. The measured figure is 131: 36 rows moved (30 in Part A, 6 in Part C), and one Part A row had to be re-applied (see the faults below).

**Item 326’s “owner named” group (59) was largely a keyword misfile.** 44 of the 59 notes say only “Family-owned” or “Partner-owned” — they describe the row’s own ownership, not a third-party owner. Those 44, and Ater Wynne (“Merged”, with no owner named), are named and left with zero reads, because the note settles neither tier nor status. Part C read only the 14 rows that name a third-party owner.

## Part B — Item 329 · the dropdown sweep (zero reads, all 54 files)

- **Static markup:** 18 of 54 files list fewer statuses in their filter markup than their rows hold. Tennessee and Texas are among them, as Item 326 reported.
- **What the reader actually sees:** 53 of 54 files rebuild the status filter at page load from the statuses the rows carry (Item 312’s script). Their static options are discarded before a reader sees them.
- **Result: 0 files hold a status the reader cannot reach.** `chicago.html` has no status filter at all, and stays as it is.

**So no file is written in Part B.** The fault Item 326 reported was an instrument fault, my own: a static-markup check that never ran the page. Adding options the page deletes at load would change nothing a reader sees. Item 326’s six static option additions were likewise inert, and are recorded as such. The full sweep is in `item329-sweep.json`.

## Part C — Item 328 · the owner-named rows (reads)

**Spend:** 55 of 120 reads.
- Work reads that returned something: 20.
- Void: 34 refused and 1 empty — a void rate of **63.6%**, measured on this part alone. Most were search refusals from the search provider.
- Reads per row settled: 9.2.
- Calibration reads (known-answer tests and diagnosis) are logged separately, outside the ceiling.

**Known-answer test: 1 of 2.**
- The planted public company (Caterpillar) was established as public, through SEC’s list of exchange-traded registrants (`sec.gov/files/company_tickers.json`).
- The planted privately held owner (Hearst) returned “class unread”. That is a failure to classify, not a wrong class.
- So every “class unread” line in this part may hide an owner whose class a better reader could establish. That caveat stands beside every Part C figure.
- The first planted case, Blackstone, was a poor choice and was replaced: it is both a PE firm and a listed issuer.

**The four counts, on the 14 rows with a named third-party owner:**
- **Moved to Tier C by established class: 6.** Each owner is a listed issuer on SEC’s ticker list, read on 31 October 2026:
  - Mills Fleet Farm (KKR)
  - Howard S. Wright (Balfour Beatty, ADR)
  - Vigor Industrial (Carlyle)
  - Forest Electric (EMCOR)
  - Five Star Electric (Tutor Perini)
  - Bergmann Associates (Colliers)
- **Moved with class established as neither: 0.**
- **Named and left: 8.**
  - 7 with the class unread, not unknown: Armanino, Hearst, Taft, Lathrop, Emart, China Construction America and Zonin. Their owner sites and searches were refused, empty or silent, and the SEC ticker list carries no issuer of those names.
  - 1, Mayer Hoffman McCann: CBIZ is a listed issuer, but the note says “affiliated”, not owned.
- **Owner’s source contradicts the note: 0.**

**One misread, caught before any write:** for Armanino, the classifier matched “privately-held” in a sentence describing Armanino’s clients. The row was held as class unread, not written as “neither”.

## Part D — Item 327 · the five unreached markets (reads; per-market 150, total 750)

| Market | Rows in scope | Route 4 | vs Florida 29.2% | R1 (given) | R2 (given) | R3 (given) | Rows written | Held | Reads | Void refused | Void empty | Void rate | Reads per row written | Rows unreached |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chicago | 108 | 33/83 (39.8%) | at or above | 0/0 | 0/0 | 0/0 | 32 | 1 | 150 | 37 | 0 | 24.7% | 4.5 | 25 |
| california | 1 | 1/1 (100.0%) | at or above | 0/0 | 0/0 | 0/0 | 1 | 0 | 3 | 0 | 0 | 0.0% | 3.0 | 0 |
| washington | 1 | 0/1 (0.0%) | below | 0/1 | 0/1 | 0/1 | 0 | 0 | 4 | 2 | 0 | 50.0% | — | 0 |
| colorado | 2 | 0/2 (0.0%) | below | 0/2 | 0/2 | 0/2 | 0 | 0 | 8 | 2 | 1 | 37.5% | — | 0 |
| arizona | 1 | 0/1 (0.0%) | below | 0/1 | 0/1 | 0/1 | 0 | 0 | 4 | 1 | 0 | 25.0% | — | 0 |

- **Chicago’s 150 bound** with 25 of its 108 rows unreached and no confirmation route given. Those 25 are named in `item327-routes.json`.
- California, Washington, Colorado and Arizona each had 1 or 2 rows in scope. Most of their short rows lack a named decision maker, which is outside this route’s scope.
- **Total spend:** 169 of 750. No run died; every read is in the log.
- **Held:** Angelo Caputo’s Fresh Market. The site shopcaputos.com does not carry the name’s first word, so identity is not established.
- **Stray cells:** three Chicago rows (Pepper Construction, Power Construction, Bulley & Andrews) carry a stray twelfth cell holding a phone number, after Flags. This is pre-existing, and was written around, not repaired.
- Chicago’s two C/Verified rows from Item 326 were not re-opened.

**Entry 15, per market:**
- chicago: call-ready 23 → 55. Gained 32, all by a written line; 0 unexplained, 0 lost.
- california: call-ready 0 → 1. Gained 1, all by a written line; 0 unexplained, 0 lost.
- washington: call-ready 0 → 0. Gained 0, all by a written line; 0 unexplained, 0 lost.
- colorado: call-ready 0 → 0. Gained 0, all by a written line; 0 unexplained, 0 lost.
- arizona: call-ready 0 → 0. Gained 0, all by a written line; 0 unexplained, 0 lost.

**§5.4 integrity, in the five markets:**
- chicago: 3 rows outside Downgraded ⇔ Tier C, all left from Item 326’s named-and-left set.
- california: 2 rows outside Downgraded ⇔ Tier C, all left from Item 326’s named-and-left set.
- washington: 3 rows outside Downgraded ⇔ Tier C, all left from Item 326’s named-and-left set.
- colorado: 3 rows outside Downgraded ⇔ Tier C, all left from Item 326’s named-and-left set.
- arizona: 8 rows outside Downgraded ⇔ Tier C, all left from Item 326’s named-and-left set.

## Across all 27 markets

- **Call-ready: 268 → 301 rows.** Gained 33; every gained row traces to a line this pass wrote (entry 15). 0 unexplained, 0 lost.
- **Dialable:** 4172 → 4166 rows. **Tier C:** 2249 → 2255 rows, on this pass’s census universe.
- **Companies are now counted by company name.** The index’s earlier 267 counted rows by cell text. By name, 6 companies hold two call-ready rows each: Martin Engineering, Forest City Gear, Palmer Candy, Vonachen Group, The Libman Company and Blick Art Materials. Call-ready reads **301 rows across 295 companies.**
- **A finding the brief did not ask for.** The integrity sweep over all 27 markets finds 124 Downgraded rows outside Tier C in five closed markets that Item 326 never checked: Florida 25, Michigan 23, Ohio 35, Las Vegas 10 and Pennsylvania 31. They are reported, not repaired. They need their own item.

## Ceilings

| Part | Ceiling | Spent | Remaining |
|---|---|---|---|
| Part C | 120 | 55 | 65 |
| Part D | 750 | 169 | 581 |

No run died, so the log and the ceilings agree.

## Faults found in this pass, my own

1. **Item 326’s dropdown check read static markup the page discards at load** (Part B above).
2. **Item 326’s “owner named” keyword caught “Family-owned” and “Partner-owned”**, misfiling 44 rows (Part A above).
3. **A restore wiped an earlier part’s write.** To undo a Part D write carrying the wrong item label, I restored `california.html` from git, which also removed Part A’s Stater Bros. edit. The loss was caught by reconciling the 36 moves against the integrity breaks, row by row, and the write was re-applied before the close.
   - **Proposed rule:** a file is never restored from git mid-pass; a wrong write is corrected by an edit.

## Close

- **Validator:** 54 of 54 on final bytes.
- **Index:**
  - Headline Verified 3,718 / 3,635 → **3,737 / 3,654**, from Part A’s 19 rows. The market column sums to the headline.
  - Call-ready 268 / 267 → **301 / 295.**
  - Dialable 4,172 / 4,083 → 4,166 / 4,077.
  - Tier C rows 1,801 → 1,807.
  - Item 327 note added.
- **Standard:** Part D’s measured yields and void rates, by market, and Part C’s owner-class spend are written to `florida-standard.json`, with no programme mean.