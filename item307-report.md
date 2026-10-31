# Item 307 — the four theme seats and the P9 key

DashRite Advisory LLC · HOT Leads · 31 October 2026 · opened on `472e7d4`. Zero live reads; this item read the repository only.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `472e7d4`, roster before naming) | 6 | 0 | 65 | 60.0 |
| On this delivery (roster after naming) — reported, not adopted (entry 34) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0, Chair included, in both verdicts.
- **Roster file:** 76 entries and 765.0 before; 75 entries and 755.0 after.
- **Blind seats:** Buffett, Cuban and Lemonis read Blind; their theme seats are not established by the roster. Herjavec is named and votes.

**Against the projection on record.** The projection was Pass 7 · Hold 2 · Blind 62, weight 70.0. The measured result is Pass 7 · Hold 0 · Blind 64, weight 70.0. **They do not agree.**
- The weight passing matches only by coincidence of the arithmetic.
- The projection assumed three seats named: Buffett Hold, Cuban Hold and Herjavec Pass.
- The roster established only one of them, Herjavec. Buffett’s and Cuban’s Hold readings stay on record and do not vote.

## Gate

- Head `472e7d4`, the expected head.
- Fresh clone against cache-busted raw: 430 of 430 files agree by length, git blob and SHA-256, on the first read (`item307-gate.json`).
- Register entry 16 required no re-read: no disagreement arose, and the commit was not minutes old.

## Section 3 — the P9 decision, taken first: outcome (b)

Lemonis is recorded as Blind by construction, with the reason written on his roster entry: no Part 9 check is defined, and the seat reads Blind on Part 9 until one exists (`item307-p9-decision.json`).

**Basis, read in the roster:**
- The record of 30 October 2026 (step 9.0) withdrew Lemonis’s Part 9 ground under the second edition’s Section 2 table.
- His entry’s own note says the same.

**Why not (a):** supplying a check would reverse that recorded withdrawal. It would also need a Lemonis column in `f72seats.py`’s Part 9 map, which this item does not change. No check was written, so none needed a planted-case proof.

## Section 4 — the naming, by reading the roster

| Entry | Result | What the roster says |
|---|---|---|
| P3 Robert Herjavec | **Named: seat `sell`** (“Sell and protect”) | Its own record of 31 October (Step D) labels the Herjavec reading “sell and protect”, which is the seat’s exact name; core run three labels it “protect what is callable”. |
| B1 Warren Buffett | Not established; Blind | No record or field names the seat. |
| P2 Mark Cuban | Not established; Blind | The records label the Cuban reading “out-prepare”, which is no seat’s name. |
| P9 Marcus Lemonis | Not established; Blind | The records label his readings “process”, one word of seat `ppp` (“People, process, product”) and not its name. A partial match is not a reading, so the seat is not named. It would read Blind on Part 9 regardless, under outcome (b). |

**The P3 merge:**
- P3’s `fields_by_part` and `check_part9` merged into `sell`, dated 31 October 2026, with the basis written on the seat (`merged_from`).
- The P3 entry retired after the merge, its reading carried on `sell` (Item 323 §2.1 remedy).
- B1, P2 and P9 keep their readings on record, each with an `item307` note saying why it was not named.

## For the Chair

`ppp` is the only seat whose name contains Lemonis’s label, and `f72seats.py`’s Part 9 text describes his reading as a people, process or product test. Both point at `ppp`, but neither is the roster naming the seat. I held it as not established rather than name it from a partial match. Naming it would change no verdict, because his seat is Blind on Part 9 by construction.

Buffett and Cuban need a roster reading to name them. There is nothing in the repository today to name them from.

## Stop conditions

None fired:
- The gate agreed.
- The roster accounts under §2.2 and Amendment 3: 75 entries, 755.0; council 72 seats, 725.0.
- No seat was named by inference.
- No source line was written.
