# Item 323 — close report

DashRite Advisory LLC · HOT Leads · 31 October 2026 · live head `c3c62dd` at open and at close (`git ls-remote`).

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

**Founders 72 on this brief.** This re-runs the Founders 72 on Item 322’s delivered bytes (`c3c62dd`) with the merged roster, and it replaces the withdrawn Item 322 verdict.
- Council: 72 seats, 725.0 by weight, Chair included.
- Pass 6 · Hold 0 · Blind 65 · Chair 1.
- Weight passing: 60.0 of 710.0 voting (Chair excluded).

**Founders 72 on this delivery.** Same figures on the final bytes. Part 9 reads only the intake table of `florida-expansion.html`, which this pass did not touch. This verdict is reported, not adopted (entry 34).

**Part 9 seats:**
- Pass: Branson (merged into `branson`), Jain (merged into `jain`), Bogle, Maister, Drucker and Baker.
- Blind: Buffett, Cuban and Herjavec. Their theme seats are unnamed (item 307).
- Under the roster’s standing rule, a Blind bound seat on a delivery reading is a stop.
- This is the condition §2.1 anticipates (“runs with those four Blind and says so”). It is not a Section 9 stop. It is recorded here, not adopted.

**Duplicate entries kept on record (they do not vote):**
- B1 Buffett: Hold (Band missing on I5 and I7).
- P2 Cuban: Hold (Band missing on I1, I4 and I6).
- P3 Herjavec: Pass.
- P9 Lemonis: Blind.

**Roster file and council side by side:**
- The roster file reads 76 entries and 765.0.
- The council reads 72 seats and 725.0.

## Gate (§1)

- Head was `c3c62dd` exactly.
- Clone and cache-busted raw agree on 408 of 408 files, by length, git blob and SHA-256 (`item323-gate.json`).
- Coverage limit: the GitHub contents API refused with a rate limit. That is a coverage limit, not a failure.
- Caveat: I can’t verify that raw.githubusercontent.com honours a query-string cache-buster. `ls-remote` carries the head independently.
- §1.1 did not trigger, so 16 opened the pass.
- §1.2: no file reads `decisions.json`. Literal references only; a runtime-assembled name would not show.
- `4_held_13`: 13 of 13 entries.

## Part 1 — the 48 Florida “source the number” rows

**Sample.** 24 of 48 rows, stratified by industry label, seed 323 (`item323-seed.json`). Regal Boats and Regal Marine Industries were both drawn; they are one company with one number, in two files.

**Reads.** 197 of 200 were spent, plus 4 calibration reads outside the ceiling.
- **Instrument fault:** search reader v1, a Bing HTML scrape, returned results unrelated to the query.
- Every read that depended on it is void and counted against the ceiling:
  - Routes 1–3: 96 reads.
  - Route 4: the v1 site searches on the 10 rows with no site on file.
- Reader v2 (DuckDuckGo HTML, POST) passed a known-answer test before use.

| Route | Rows validly attempted | Sourced | Rate (denominator 24) | Reads | Reads per row: actual vs estimate |
|---|---|---|---|---|---|
| 4 · company’s own pages | 24 | 7 | 29.2% | 72 (10.3 per sourced row) | estimate ~50, measured basis |
| 2 · chambers | 24 | 1 | 4.2% | 29 valid + 24 void | 1.2 actual vs 2.0 estimated |
| 1 · associations | 0 | — | unmeasured | 24 void | — |
| 3 · trade press | 0 | — | unmeasured | 48 void | no valid reads vs 2.0 estimated |

- Routes 4 and 2 cover the whole sample, so they are comparable with each other and with Item 322’s 17.5%. The sample is n=24, so the interval is wide.
- Routes 1 and 3 are not compared.
- The remaining 24 rows were not worked.

**Contact field** (two measured routes):
- Single route: 6.
- Routes agreed: 0.
- Resolved by precedence: 1. Trans-Phos takes Route 4’s (800) 940-1575; the Lakeland Chamber’s (863) 534-1575 is carried in the note.
- Disputed, unresolved: 0.

**Written to the files:** Invicta, Quirch, Refricenter, TruckMax, Duda Farm Fresh Foods, Globe Trailers and Trans-Phos. Invicta’s company page carries (954) 921-2444, not the (305) 715-9633 that was on file.

**Refusals** (one reader kind each, none confirmed by a second): 19 Route 4 pages and 3 GrowthZone chamber pages.

## Part 2 — the 13 tier contests

39 of 39 reads were spent. 4 of 13 settled and 9 of 13 are still held.

**Settled:**
- Berlin Packaging: Tier C on both rows. Chicago #237 moves B → C.
- Zeus: Tier C on both rows. South Carolina #161 moves B → C.
- Ben E. Keith: Tier C on both rows. Texas #1 moves A → C. It is family-held and out of band on scale; the ~$7.9–8B figure is an estimate.
- Winder Farms: Tier B on both rows. utah-expansion #23 moves C → B, an upward correction.

**Still held:**
- 5 with the band unestablished, because only statistical estimates were found: Hensley, Empire Southwest, Fresh Mark, Superior Beverage and Elliott Electric.
- 4 where the reads were refused: Rosboro, Christensen Arms, Rappahannock and Zirkle.

## Part 3 — Pennsylvania (staged, not delivered)

99 of 100 reads were spent.

**Lines (of 34):**
- Re-dated: 19.
- Re-verified to a changed fact: 3.
  - Gertrude Hawk: CEO Patrik Hawk.
  - Oxford Development: President and CEO Shawn Fox.
  - Utz: agreed to be acquired by Intersnack. Tier C stands.
- Not established: 12.

**Rows (of 15 at risk):**
- 11 stay Verified.
- 4 move to Unverified:
  - Benchmark Construction (#85) has no dated source left.
  - Marburger, Brunton and Yoder’s have their ownership re-dated, but the decision maker is unconfirmed under the standing Tier A rule.

**Why Pennsylvania is held out.**
- The validator refuses the staged bytes, because 12 lines remain undated.
- Writing those 12 in either 2.6 form needs a source I don’t have.
- `pennsylvania.html` is therefore delivered unchanged at `c3c62dd`. The index does not restate Pennsylvania.
- The staged work is recorded line by line in `item323-part3-pennsylvania-staged.json`.
- This needs a Chair ruling on lines that three reads can’t re-establish.

## Part 4 — the roster

- P1 Branson merged into `branson`, and P4 Jain merged into `jain`, dated 31 October 2026. `fields_by_part` and `check_part9` moved with them (`item323-merge-record.json`).
- B1, P2, P3 and P9 are marked `votes:false`; their readings are kept on record.
- **Known gap against item 307:** P9 Lemonis has no `check_part9` key.
- **Instrument note:**
  - `f72seats.py` keys seats by the last word of the name, so it fails on a merged seat (KeyError).
  - It is not repaired in this pass.
  - The verdicts use `item323_f72.py`, which agrees with `f72seats.run` on all 78 seats of the unmerged head roster.

## Close (Restoration C)

**Florida restated, as rows / companies:**

| Measure | Rows / companies |
|---|---|
| All | 200 / 197 |
| Dialable | 114 / 113 |
| Call-ready | 57 / 57 (was 50) |
| Verified-callable | 16 / 16 |
| Tier C | 86 / 84 |

- Verified-callable: the 21 previously published is withdrawn as of 31 October 2026 (§2.4). The 7 rows newly call-ready were not tested against that definition in this pass.
- Short of call-ready, 57 rows:
  - source the number: 41
  - acquire a number: 14
  - find the name and source the number: 1
  - ask for the name: 1
  - contact disputed, unresolved: 0

**Regenerated on final bytes:** `dial-pack.json`, `Florida-Dial-Pack.docx` and `Core-BD-Report-Florida.docx`, each carrying the Item 323 lineage and the 21 → 16 withdrawal.

**Index:**
- Verified rows are re-counted from the status chips. This method reproduces 26 of 27 markets at head; Chicago read 131 published against 130 counted, unexplained, and its rows are restated by count.
- The company, dialable and Tier C totals don’t reproduce from the files by this count. They are moved only by this pass’s certain changes, and the index flags that.
- Florida, Chicago, South Carolina, Texas and Utah are restated, and the contest section is updated.

**Standard:** the route-yield table is written to `florida-standard.json` (`contact_sourcing_routes`). The Word Build Standard at the project root is outside the repo and needs the same table.

**Validator:** passed on all 10 market files delivered, on final bytes.

**Out of scope, recorded only:**
- Quirch Foods is Tier B with a note reading “PE-owned (Palladium Equity since 2018)”. Under the disposition rule that reads as Tier C.
- Pennsylvania carries B/Downgraded rows, which breaks the rule that Downgraded rows sit in Tier C.

## Register (proposed)

1. A search reader used without a known-answer test, voiding 96 or more reads.
2. Measured writes deferred to the close, which a halt strands.
3. Part 3 has no rule for a line that three reads can’t establish, while Section 9 makes a validator failure a halt.
4. An instrument that keys seats by name breaks on a merge.

## Open for the Chair

1. A ruling on the 12 Pennsylvania lines.
2. Whether reads voided by an instrument fault count against a ceiling. I counted them.
3. A budget for Routes 1 and 3.
4. Item 307: name the four theme seats.
