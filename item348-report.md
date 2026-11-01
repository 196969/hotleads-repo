# Item 348 — the 41 A3 rows

DashRite Advisory LLC · HOT Leads · read 2026-11-01 · opened on `86cc43b`, the Item 347 commit.

**This upload holds 23 files**: 18 repository files and 5 records. The gate’s first check is this count.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `86cc43b`) | 7 | 0 | 64 | 70.0 |
| On this delivery (final bytes) — reported, not adopted (entry 34) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Every figure here is attested, not gated

Every figure here comes from a reader whose four fixes live outside the repository: the whole-domain blocklist, the route depth, the anchored two-word name rule and the narrowed private-equity phrase list. No gate reads them and no commit proves them.

## Gate, amended — the file count first

- **File count by name: delivered 15 · committed 15 · missing 0 · extra 0.** The check passed, and `florida.html` landed this time.
- Head `86cc43b`. Every committed file matches its delivered bytes.
- Clone against cache-busted raw: 502 of 502 files agree.
- The commit was under 5 minutes old, so the 15 changed files were also read at the commit-pinned address. All 15 agree.
- Validator baseline: 54 of 54.

## Part A — the 41, by source type

**Spend:** 75 of 90 reads. Work 73; void 2 refused and 0 empty — a void rate of 2.7%. One attempt per row; no row was tried twice.

| Group (one route, one rule) | Rows | Settled | Not settled | Group stop |
|---|---|---|---|---|
| Own-site reads — about, history or leadership page | 17 | 0 | 17 | no — the first five did not all refuse |
| Control-source reads — who owns or controls it | 21 | 2 | 19 | no — the first five did not all refuse |
| Class reads — public, PE, co-op, subsidiary | 3 | 0 | 3 | no — the first five did not all refuse |
| Dated-revenue reads | 0 | — | — | empty: no A3 row is owed a revenue figure (the revenue contests are held separately) |

**Settled, 2, both on the company’s own page, both moved to Tier C on class** (a parent, under the Chair’s 1 November correction):
- **Stresscon Corporation (Colorado #112):** “Stresscon is a division of the EnCon United group of companies”. Src: read stresscon.com/about-us 2026-11-01.
- **Anchor Block Company (Minnesota #55):** “Anchor Block, a subsidiary of Oldcastle APG, a CRH Company”. Src: read anchorblock.com 2026-11-01.

**Not settled, 39.** Each carries a dated line in the unestablished form, naming the page or search read. By failure mode:
- site never reached: 20
- page silent on the fact: 16
- wrong identity withdrawn: 2
- refused: 1

**What the own pages did say, recorded and not over-read (entry 31):**
- **Bedell Cellars:** “a pioneering, family owned winery” — but no current owner is named.
- **Harris Ranch:** the Harris Farms family of companies, owned by John Harris — but which entity the row is stays open.
- **Right Away Disposal:** its own domain now resolves to `wasteconnections.com`. That is recorded as read, not as a statement of acquisition.

**An instrument fault, caught mid-pass (entry 30).** The generic-word list reduced “Nutrition Industries” and “SSA Marine” to one word each, which matched `nutrition.gov` and `ssa.gov`.
- The pass stopped, and nothing had been written from either match.
- **Corrected rule:** company identity is never accepted on a .gov, .edu or .mil domain.
- Every other match in the pass was re-checked under it. None used such a domain.
- Both rows carry dated lines saying the matched site was rejected as the wrong identity.

**One line had to be fixed by edit:** L.C. Industries’ search line broke at “L.C. I…”, because the validator ends a line at a full stop followed by a capital. It was rewritten with the search as an encoded URL, and the validator passes.

## Part B — the Tops pointer, removed

Tops Friendly Markets (new-york.html #112): “See #3.” is removed. Row #3 is DeCicco & Sons, an unrelated company. The row now says so, and carries its own owed source: an ownership source for Tops itself. Registered as a false-provenance correction.

## Part C — close

- **Rows outside the amended invariant:** 63 → **61** (all 54 files), plus 1 scale-downgraded row (Zaxby’s), which is exempt.
- **Call-ready:** 312 → 312. Gained 0, lost 0; neither settled row was call-ready, so the entry 15 check is clean.
- **Companies:** 305 by company name; 312 by cell text. A count that moves only on a method change adds no company.
- **Index:**
  - Dialable 4,141 / 4,052 → **4,139 / 4,050**.
  - Tier C rows 1,832 → **1,834**.
  - Verified unchanged at 3,804 / 3,721, and the market column sums to it.
  - Item 348 note added.
- **BD report:** the counts moved, so `HOT-Leads-BD-Report.docx` is regenerated as its **third edition**. It has a page border and page numbers and passes the docx validator; it shows 61 rows outside the rule, A3 now 39.
- **Validator:** 54 of 54 on final bytes.
- **Register** (the standard’s `register_item348`):
  - the gate amendment (yours);
  - the Tops false-provenance correction;
  - the entry 30 .gov-identity instance;
  - the group-yield finding;
  - the Right Away Disposal redirect, as observed.
- **Ceiling:** 75 of 90 spent. No run died.

## The 23 files in this upload

- HOT-Leads-BD-Report.docx
- arizona.html
- california.html
- colorado.html
- florida-expansion.html
- florida-standard.json
- florida.html
- georgia.html
- index.html
- item348-founders72-verdicts.json
- item348-gate.json
- item348-lines.json
- item348-read-log.jsonl
- item348-report.md
- michigan.html
- minnesota.html
- missouri.html
- new-york.html
- oregon.html
- pennsylvania.html
- utah.html
- virginia.html
- washington.html