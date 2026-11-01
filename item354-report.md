# Item 354 — rungs 3 to 6 · halted at rung 3 on the Chair’s quarter-no-contact stop

DashRite Advisory LLC · HOT Leads · 2026-11-01 · head before `71fad92` · **this upload holds 9 files**, listed at the end.

## Verdicts

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `71fad92`) | 7 | 0 | **64** | 70.0 |
| On this delivery (final bytes) | 7 | 0 | **64** | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

**`gate.py` exited 4.**
- Item 353 file count: 88 of 88 committed, byte for byte.
- The commit was under 5 minutes old, so the 88 were also read at the commit-pinned address. All 88 agree.
- Full repository: 583 of 583 files agree.
- Validator: 54 of 54.
- Stop 3 set on watts.com.

## The backlog, re-defined (written first, in one pass, as ruled)

**The predicate is written in the standard, in `acquisition_backlog_predicate`.**
- **Universe:** every row with a Tier cell in the 54 market files.
- **Clause 1, old-rule call-ready:** a named person with a title word; a phone matching `\(?\b\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b` or an email, plus any ISO date in the address-source, notes or decision-maker cells; and Tier A, B or Unverified. The code is `stepd.assess` at commit `e986c45`.
- **Clause 2, no source line naming the contact:** `stepd.contact_source_bound` at the head being counted returns False. It names the three tests: the last seven digits of the phone, the email, or a listed contact word in the sentence a dated Src: line closes.
- **Measured: 197.** Florida 39 · Texas 36 · Chicago 32 · Pennsylvania 19 · Georgia 12 · North Carolina 9 · Las Vegas 9, and the rest 1–7 each.

**The 203 is withdrawn.** It was published at `5d44b36`. Re-measured at that commit under its stated sentence, it reads 267, and the commit records no definition that yields 203.
**The 552 is kept separate:** dialable rows with an unsourced number. That is prospecting, not backlog.
**The 101 fault is filed as mine.** One phone format gave 101; the instrument’s own pattern, on the same rows on the same day, gives 552.

**Florida 13 → 39, explained:**
- At the 203’s commit, the same predicate counts **58** Florida rows.
- Since then, 18 of those gained a sourced contact (Items 323 onward), 1 moved to Tier C, and none entered. That makes **39**.
- The published 13 is reproduced by no count, and goes with the 203.

## Rung 3 — halted after 8 rows

The first-reached set is 73 rows: Florida 39, Chicago 32 and Illinois 2, worked Florida first.
- **Budget:** 219 reads, a cap of 5 per row, and the quarter-no-contact halt. I judged it after a minimum sample of 8 rows, so that one early miss could not stop the run.
- **Halted at 8 rows:** 7 of 8 produced no sourced contact.
- **Spent: 12 of 219 reads.** Remaining: 207.
- No row passed 5 reads.

| Row | Result |
|---|---|
| florida.html#8 PJ Distributors General import/dis | — · search unclassified · 1 reads |
| florida.html#11 Turbana Corp Produce import · Sout | — · search unclassified · 1 reads |
| florida.html#12 Fresh Del Monte Produce Produce im | — · search unclassified · 1 reads |
| florida.html#15 Southern Glazer's Wine & Spirits | (866) 375-9555 · company page · 3 reads |
| florida.html#16 National Beverage (LaCroix) | — · no number on the company pages read · 3 reads |
| florida.html#18 Watsco HVAC distribution · Southea | — · search unclassified · 1 reads |
| florida.html#22 Presidente Supermarkets Grocery +  | — · search unclassified · 1 reads |
| florida.html#25 Perry Ellis International Apparel  | — · search empty · 1 reads |

**What the halt reads, and what it can’t separate:**
1. **The search reader refused.** Five of the 8 searches came back unclassified, meaning a consent or block page, not results.
2. **The runner asked badly — my fault, filed under entry 30.** It took names from the census’s Company cell, which joins the name to its sub-label. Queries went out as “PJ Distributors General impo…” and “Fresh Del Monte Produce Prod…”.

**Eight rows can’t say how much each cause contributed.** Nothing was written from a malformed identity. The one write, Southern Glazer’s, was re-checked under its proper name: the site match (`southernglazers.com`) is unchanged.

**One contact sourced:** Southern Glazer’s Wine & Spirits (florida.html #15) is written as (866) 375-9555, read from `southernglazers.com/contact-us` on 2026-11-01.
- It replaces an unsourced (954) number.
- **Judgement flagged for you:** the sourced line is a national toll-free number. The local one it replaces was unsourced, so the rule wrote the toll-free. If a Florida office line matters more for Eddie, that needs a source naming it.

## Not reached, because of the halt

Under the brief’s stopping rule, nothing below rung 3 ran:
- the rest of rung 3;
- rung 4, Florida’s 39 missing fields;
- rung 5, the practice field;
- rung 6;
- Dash CRM builds A and B.

**Two things would let rung 3 restart honestly:**
1. Fix the runner to read the company name from the row’s own bold name cell, not the joined Company cell. This is mine to do, at zero reads.
2. Re-plant the search reader: two known rows, one expected to return a number. A refusing search engine shows up there before any budget is spent.

## Close

- **Call-ready, measured:** 312 → **313** (+1, Southern Glazer’s). By company name, 306. The entry 15 check is clean: one gained, matching one written line.
- **Validator:** 54 of 54.
- **Index:** the backlog line is restated with the predicate, the withdrawal and the 552 kept separate. The call-ready line now reads 313 / 306, and an Item 354 note is added.
- **Reads:** 12 of 219, counted from `item354-read-log.jsonl`.

## The 9 files in this upload

- delivery-manifest.json
- florida-standard.json
- florida.html
- index.html
- item354-backlog-recount.json
- item354-founders72-verdicts.json
- item354-read-log.jsonl
- item354-report.md
- item354-rung3-reads.json