# Item 323 follow-on — close report

DashRite Advisory LLC · HOT Leads · 31 October 2026 · opened on head `81c8e13`, under rulings 1–4 of 31 October 2026.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

**Founders 72 on this brief (head `81c8e13`):**
- 72 seats, 725.0 by weight.
- Pass 6 · Hold 0 · Blind 65 · Chair 1.
- Weight passing: 60.0 of 710.0 voting (Chair excluded).

**Founders 72 on this delivery:** the same figures. It is reported, not adopted (entry 34).

**Item 307:** Buffett, Cuban, Herjavec and Lemonis read Blind until item 307 is run as its own pass. P9’s missing `check_part9` key is a known gap against item 307.

**Roster file and council side by side:** the file reads 76 entries and 765.0; the council reads 72 seats and 725.0.

## Gate on head `81c8e13`

- Head was `81c8e13`, the commit after `c3c62dd`.
- Commit against delivery: the commit changed 30 files (17 modified, 13 added). That is exactly the 30 delivered, and all 30 match the delivered bytes by SHA-256.
- Clone against cache-busted raw: 421 of 421 files agree by length, git blob and SHA-256 (`item323-followon-gate.json`).
- The same limits carry as before: the contents API was not read, and the cache-buster is unverified, with `ls-remote` carrying the head.
- Validator on the live market files: 50 of 54 passed.
- The 4 refusals all predate this item and failed identically at `c3c62dd`, in files the upload did not touch:
  - las-vegas.html: 28 undated lines.
  - pennsylvania.html: 34 undated lines. This pass fixes it.
  - michigan.html and ohio.html: 1 undated line each.

## Pennsylvania — the 34 lines (ruling 1)

No new reads were spent. Every line comes from Item 323 Part 3’s 99 reads (ceiling 100).

**Lines (of 34):**
- Re-dated: 19.
- Re-verified to a changed fact: 3 (Gertrude Hawk, Oxford Development, Utz).
- Read but not re-established at that read: 12.

`pennsylvania.html` now holds 0 undated lines out of 73, and the validator passes.

**The 12 not re-established,** each in the form `Src: read <page> 2026-10-31 — fact not re-established at this read`:

| Row | Company | Page named on the line | Status |
|---|---|---|---|
| 74 | Tony Luke’s | tonylukes.com/find-a-location | Downgraded, kept |
| 82 | Ernest Bock & Sons | pennsylvaniadb.com company page (refused) | Unverified, kept |
| 85 | Benchmark Construction | benchmarkgc.com/team-member/robert-brandt-iii | **Verified → Unverified** |
| 111 | E.G. Stoltzfus | html.duckduckgo.com search | Unverified, kept |
| 162 | McKnight Realty Partners | loopnet.com broker profile (refused) | Downgraded, kept |
| 182 | Weaber Lumber | weaberlumber.com/contact | Downgraded, kept |
| 196 | Esbenshade Farms | cpbj.com article (refused) | Downgraded, kept |
| 6 | Weis Markets | weismarkets.com/board-directors (refused) | Downgraded, kept |
| 46 | Coosemans Philadelphia | html.duckduckgo.com search | Downgraded, kept |
| 54 | Lancaster Foods | lancasterfoods.com history page | Downgraded, kept |
| 127 | Gilbert Associates | prabook.com biography | Downgraded, kept |
| 132 | Drucker & Scaccetti | armanino.com merger page (refused) | Downgraded, kept |

**The two weakest lines.** #46 and #111 name a search, not a fact page. The reader of that run logged an empty result as a refusal, so this record cannot say whether the source refused or the fact is absent (register 14). A calibration probe today re-ran the #46 query and got 10 results. That suggests a transient failure then, but proves nothing about then, and it was not used on the row.

**Withdrawal.** My earlier description, “the search returned no result,” is withdrawn and restated as “cannot tell which.”

**The distinction recorded.** A line can be unestablished while the row’s status rests on something else entirely. The 9 Downgraded rows and 2 Unverified rows among the 12 keep their status. The line’s honesty is separate from what the row’s tier or disqualification rests on.

**Rows (of the 15 Verified rows at risk):**
- 11 stay Verified.
- 4 move to Unverified:
  - #85: its only line was not re-established.
  - #26 Marburger and #27 Brunton: decision maker unconfirmed (standing Tier A rule).
  - #200 Yoder’s: no decision maker on the row.
- Pennsylvania Verified rows: 103 → 99. Call-ready: unchanged at 3 rows by the Florida-reproducing rule.

## Routes 1 and 3 on the 24 (ruling 3)

Same sample and seed 323. Every route ran on every row with no early exit. Reader v3 was used, and it records four outcomes.

**Reads:** 69 of 100 spent (Route 1: 28 of its 40; Route 3: 41).
- **Void:** 12 of 69, recorded beside the spend.
  - 10 refused: 1 search, 3 association pages, 6 outlet pages.
  - 2 empty: 1 search on each route.
- **Calibration:** 5 reads outside any ceiling, logged separately.

| Route | Attempted | Sourced | Rate (of 24) | Reads | Reads per sourced row | Actual vs estimate per row |
|---|---|---|---|---|---|---|
| 4 · company pages (Part 1) | 24 | 7 | 29.2% | 72 | 10.3 | — |
| 1 · associations | 24 | 1 | 4.2% | 28 | 28.0 | 1.2 vs 40 (a ceiling, not an estimate) |
| 2 · chambers (Part 1) | 24 | 1 | 4.2% | 29 valid | 29.0 | 1.2 vs 2.0 |
| 3 · trade press | 24 | 0 | 0.0% | 41 | none sourced | 1.7 vs 2.0 |

- All four routes are now whole-sample on a denominator of 24, and they are compared with each other and with Item 322’s 17.5% control (10 of 57).
- **Route 1 directories:** 4 probed and 3 refused (npfda.org, members.hempbeveragealliance.org and my.afius.org). The one read was safnow.org, and it sourced a number.
- **Route 3:** a result counts as trade press only by a declared outlet rule, written in `item323-followon-routes.json`.

**Contact field, all four routes:**
- Single route: 7.
- Agreed: 0.
- Resolved by precedence: 1 (Trans-Phos).
- Disputed, unresolved: 0.

**Written:** Sunshine Bouquet (florida.html #10). The number is (732) 274-2900, from its Society of American Florists member listing (single route). It replaces the unsourced (305) 599-9600. The 732 area code is New Jersey, recorded as read.

## Close

**Florida, as rows / companies:**

| Measure | Rows / companies |
|---|---|
| All | 200 / 197 |
| Dialable | 114 / 113 |
| Call-ready | 58 / 58 |
| Verified-callable | 16 / 16 (21 withdrawn) |
| Tier C | 86 / 84 |

Short of call-ready, 56 rows:
- source the number: 40
- acquire a number: 14
- find the name and source the number: 1
- ask for the name: 1
- contact disputed, unresolved: 0

**Pennsylvania, as rows:** 208 all, 99 Verified, 3 call-ready and 61 Tier C. Companies are moved only by the four rows that left Verified.

**Regenerated:**
- `dial-pack.json`, `Florida-Dial-Pack.docx` and `Core-BD-Report-Florida.docx`.
- `index.html`: headline Verified 3,720 / 3,637; call-ready 108 / 108 (Florida 58); Pennsylvania restated and its flag replaced.
- `florida-standard.json`: the four-route table, as the figure every market opens on.

**Validator:** passed on all 3 market files delivered.

## Register

**14 (Chair’s wording).** An instrument that cannot distinguish “refused” from “found nothing.” Fixed in reader v3, which passed a known-answer test (results and empty); every row the old reader touched carries the caveat.

**15 (new, Build, own disclosure).** A rewritten dated line that closed a sentence it did not source.
- In four Pennsylvania rows (Brunton, Volpatt, Leonard S. Fiore and Weaber), the contact binder read my new ownership line as sourcing the phone.
- It did so because the line closed a preceding “Phone per <directory>” sentence. Weaber’s line also contained the words “contact page.”
- That would have made 4 rows falsely call-ready (Pennsylvania 3 → 7).
- It was caught before delivery by reading each call-ready change against the sentence that bound it.
- Each rewritten line now opens its own sentence, stating it reads ownership and decision maker only.
- **Standing rule proposed:** a rewritten source line never closes a sentence it did not read, and every call-ready movement is read against its binding sentence before it is counted.

## Carried

- `undated-exposure.json` still describes Pennsylvania as it stood before this pass. It is a prior record and was left untouched under the record-name rule.
- Las Vegas (28 lines), Michigan (1) and Ohio (1) carry undated lines outside this item.
- The Word Build Standard at the project root needs the four-route table.
