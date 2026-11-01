# Item 349 (continued, under the Chair’s ruling) — E · G · H · I · J · K

DashRite Advisory LLC · HOT Leads · 2026-11-01 · opened on `6d4ce15` · **this upload holds 67 files**, listed by name at the end of this report and in `delivery-manifest.json`.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `6d4ce15`) | 7 | 0 | 64 | 70.0 |
| On this delivery (final bytes) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.
- Blind 64 of 72 is registered as the council reporting its own absence.

## 1 · The gate’s exit code, and what it refused

**`python3 gate.py check --since 2cc89db` on head `6d4ce15` exited 4.**
- STOP 1 · file count by name: delivered 8 · committed 8 · missing 0.
- STOP 2 · validator 54 of 54.
- **STOP 3 · reader plants 2 of 3 as expected; failed: watts.com for Watts Water Technologies.**

Clone against cache-busted raw: 515 of 515 files agree.

## 2 · The three plants rerun under ruling 1(b)

Under ruling 1(b), the full name is looked for in five places: body text, page title, copyright line, legal-entity line and footer.

| Plant | Expected | Result |
|---|---|---|
| watts.com for Watts Water Technologies | pass | **unread.** A plain fetch was refused (403). Firecrawl’s keyless free tier refused on its rate limit (“You’ve hit Firecrawl’s keyless free tier rate limit”). The widened search never had a page to search. |
| nutrition.gov for Nutrition Industries | fail on the domain exclusion | fail on the domain exclusion ✓ |
| accurate.com for Accurate Box Company | fail on the page test | fail on the page test ✓ (plain fetch 200; the full name appears in none of the five places) |

Per the ruling, watts.com’s outcome does not block the pass, and the other two plants carry the proof. **Watts was not tested, not failed:** neither fetch layer produced a page. So the shorter-anchor admission is still unproven, the gate’s stop 3 stays set, and **Parts C and D stay closed**.
I made no third framing. The fix is a keyed Firecrawl call or a browser read of watts.com, and then the three plants run again.

## 3 · Owed, with blockers named

- **Part B, the Florida registry ingest.** Port 22 to `sftp.floridados.gov` is unreachable from the build environment. It needs a machine with outbound SFTP and the brief’s credentials. Not a refusal by the State.
- **Part F, net-new Tier A BD.** No seed is on disk in either state. The Florida pull is owed, above. The Illinois DTA bulk set recorded in Item 321 did not persist as a data file (registered).

## 4 · E, G, H, I, J and K as executed

### Part E — the access map (zero reads)
- Each market’s own working page now carries its registry access class, dated 2026-11-01.
- The class is taken from the Build Stack’s registry section. That is **our own document**, so each line says it is a recorded class, not a sourced read of the state’s page, and that the state’s page is the source owed.
- **Free API, no key:** Colorado, New York, Oregon.
- **Free bulk, no API:** California (weekly), Florida (SFTP, officers included), Ohio (incremental only), Texas (Comptroller).
- **Free bulk, person-downloaded, automation prohibited:** Illinois and Chicago.
- **Individual lookup or paid contract:** the other 18, under the Build Stack’s residual class, each marked as not established for that state individually.
- **Market order, by access class (recorded in the standard):** Colorado · New York · Oregon · California · Florida · Ohio · Texas · Chicago · Illinois · then the 18.
- **Alabama and Oklahoma:** census owed. It needs the amended reader, which is closed. Max-10 not spent.
- **The correction is registered and attributed:** Illinois was not the only other Florida-class market.

### Part G — dispositions, written into the standard (`board_dispositions`), each with its reader
- **Dealer blocks (20):** manual read owed by design. The Firecrawl re-probe did not run, because Part C is closed, so the closure still stands on Item 347’s plain fetch, and the record says so.
- **Four contest rows:** owed, each with its one source.
- **A4:** unsettleable by this reader.
- **Maryland:** unopened by ruling.
- **Alabama and Oklahoma:** census owed.
- **312 call-ready:** yours; not counted as owed.

### Part H — build only
- **The skills search** (`npx skills find send`, `email`, `smtp`) returned, among others: `googleworkspace/cli@gws-gmail-send`, `resend/resend-skills@resend`, `cloudflare/skills@cloudflare-email-service` and `tiangong-ai/agent-skills@email-smtp-send`. None was adopted, because a transport binds the sending account and that choice is yours. The raw list is in `item349b-skills-find.txt`.
- **`suppression.json` already existed** (Item 314) and fails closed. It is amended with the “messaged” class. Count: 0, because no outreach log exists and the Florida outreach file records no touches.
- **`send.py`** reads `suppression.json` before every message, checks for the STOP line and signature, logs every send and refusal, and caps a pass at 10 (no warming figure is on record). It refuses outright without `approved-batch.json` carrying your word and at most ten named recipients. No transport is configured. Tested: with no approval file, it refuses and exits 2.
- **Placement measurement and the 2-in-93 comparison:** none, because nothing was sent.

### Part I — Florida and Illinois, against the dialable universe (zero reads)

| Market | Rows | Tier C | Dialable | Call-ready | Share of dialable |
|---|---|---|---|---|---|
| Florida (working file) | 200 | 88 | 112 | 57 | 50.9% |
| Illinois Downstate and Chicago | 538 | 192 | 346 | 119 | 34.4% |

**Florida does not match the brief’s benchmark (200 · 115 dialable · 93 call-ready), and I haven’t forced it to.** This census, under the Item 323 fixed contact rule, measures 112 dialable and 57 call-ready. The brief’s figures may come from a different count; that is worth reconciling before either is quoted.

**Call-ready rows missing a field, named individually in `item349b-depth.json`:**
- **Florida, 39 rows:** 33 lack a dated address source, 21 a direct line.
- **Illinois, 119 rows:** the Illinois files carry no address-source column at all, so all 119 lack it; 34 also lack a direct line and 11 a title.
- The registry join that would supply addresses is Part B, which is owed.

**Practice field:** on Florida’s 57 call-ready rows, 51 read “None” with a reason and 6 are named. On Illinois’, all 119 are blank. **The standard records no practice ceilings for Dash Acquisitions, Dash Fractionals or Dash Private Equity**, so the rows are capped, not spent, and the missing ceilings are named in the to-do.

**The console on all pages:** `console-<market>.html` now exists for all 27 markets (26 new). Each is Florida’s console with its market set, its own market file fetched, a missing per-market standard handled as empty instead of breaking, and its export file named by market.
- **Not yet tested in a browser.** Features that read per-market queue and outreach files show empty where those files don’t exist.
- The validator still reads 54 of 54.

### Part J — the BD report, rebuilt operator-first
**One correction to the brief:** the report I last delivered did not open on a changelog. It opened on a status line and a method section. The stacked Item 326–348 notes the brief describes are at the top of `index.html`. I left the index as it is; moving those notes into the standard’s history is a separate edit, if you want it.

| | Before (third edition) | After |
|---|---|---|
| Pages | 3 | 18 (the dial pack holds all 312 rows) |
| First number a reader meets on page 1 | 348 (“Item 348”) | **312** — “312 rows across 305 companies in 27 markets” |

**The order it now follows:**
1. Call-ready, alone and large, in green.
2. The share of dialable: 312 of 4,139, 7.5%.
3. The verified-callable band: 23 rows, Florida’s alone, because only Florida’s files carry an address source. They are shaded at the top of each list.
4. The dial order.
5. The dial pack by market.
6. Net-new: none, in red.
7. The acquisition backlog: 101 dialable rows with an unsourced number, by market.
8. What is owed, with blockers.
9. Definitions, last.

**Format:** Calibri 11 body with headings one size up, a thin page border, a running header and page numbers on every page. Colour is used only for green (call-ready), amber (partial) and red (owed). Figures are set apart in display lines and tables. The docx validator passes.
**Gap:** there is no monogram asset in the repository, so the final page carries none. I did not invent one.

### Part K — the to-do, cleared
The standard’s `todo_cleared` sorts every item into **done**, **owed with its blocker** or **struck**.
- **Done:** the gate as code; the send path and suppression class; consoles; access classes; dispositions.
- **Owed:** Florida ingest; net-new BD; Firecrawl re-probes; the 39 rows; the watts.com plant; practice ceilings; dealer blocks; contests; Maryland; the first send batch; the 312 calls.
- **Struck:** Soulard and Boggs.
The Word master to-do lives in the project as text, so this list is the rewrite it should take.

## 5 · The log-append fix (ruling 5)

`fc.py` now appends every Firecrawl read to `fc-log.jsonl`, shipped as `firecrawl-log.jsonl`. It never rewrites the file.

## 6 · Reads spent, with the source of each count

**This continuation: 4 reads.**
- **2 Firecrawl requests** (watts.com and accurate.com), both refused on the keyless rate limit. Per Firecrawl’s pricing page, a request that returns no result is not charged. Source: `firecrawl-log.jsonl`, which appends.
- **2 plain fetches** (watts.com 403, accurate.com 200). Source: `item349b-plain-fetch-log.json`.

**Item 349’s first run: 8 reads.** 2 plain fetches (source: that run’s log file) and 6 Firecrawl credits, attested from the transcript because the log then rewrote itself.

## Close

- **Validator:** 54 of 54.
- **Rows outside the rule:** 61, unchanged.
- **Call-ready:** 312, unchanged; companies 305 by name and 312 by cell text. No row was written, so the entry 15 check is clean.
- **Index:** Item 349 note added. The market column still sums to 3,804 / 3,721.

## The 67 files in this upload

- HOT-Leads-BD-Report.docx
- arizona.html
- california.html
- chicago.html
- colorado.html
- console-arizona.html
- console-california.html
- console-chicago.html
- console-colorado.html
- console-georgia.html
- console-illinois.html
- console-indiana.html
- console-iowa.html
- console-kentucky.html
- console-las-vegas.html
- console-michigan.html
- console-minnesota.html
- console-missouri.html
- console-new-jersey.html
- console-new-york.html
- console-north-carolina.html
- console-ohio.html
- console-oregon.html
- console-pennsylvania.html
- console-south-carolina.html
- console-tennessee.html
- console-texas.html
- console-utah.html
- console-virginia.html
- console-washington.html
- console-wisconsin.html
- delivery-manifest.json
- firecrawl-log.jsonl
- florida-standard.json
- florida.html
- georgia.html
- illinois.html
- index.html
- indiana.html
- iowa.html
- item349b-depth.json
- item349b-founders72-verdicts.json
- item349b-gate.json
- item349b-plain-fetch-log.json
- item349b-report.md
- item349b-skills-find.txt
- kentucky.html
- las-vegas.html
- michigan.html
- minnesota.html
- missouri.html
- new-jersey.html
- new-york.html
- north-carolina.html
- ohio.html
- oregon.html
- pennsylvania.html
- reader-plants.json
- send.py
- south-carolina.html
- suppression.json
- tennessee.html
- texas.html
- utah.html
- virginia.html
- washington.html
- wisconsin.html