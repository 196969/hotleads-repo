# Item 358 — the owed items, and the operator view

DashRite Advisory LLC · HOT Leads · 2026-11-01 · head before `b635aec` · **this upload holds 9 files**, listed at the end. **One deletion by hand:** `naming_v1.py` at the repository root.

## Founders 72

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Verdict | Pass | Hold | Blind |
|---|---|---|---|
| On the brief (`b635aec`) | 7 of 72 | 0 | **64 of 72** |
| On the delivery | 7 of 72 | 0 | **64 of 72** |

- **Denominator:** 72 seats and 725.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

**`gate.py` exited 4:**
- file count 16 of 16 (Item 357);
- validator 54 of 54;
- stop 3 set.

Fresh clone against raw: 607 of 607 files agree.

## 1 · The operator view

**Before** (Chromium, 1366×768, first screenful):
- the title, then a Florida practice-count line — so the first number a reader met was **150**;
- the stats strip;
- call-ready, the backlog line, and then **19 per-item notes** (Items 326–357), filling the rest of the screen.

**The finding:** the removal did not hold. The build’s own passes introduced those notes, one per item: the first at `4cb0e27` (Item 326) and the last at `fffc5a3` (Item 357), including after the Item 351 ruling. That is written to the register.

**After:**
- All 19 notes are relocated whole and unedited into the standard, under `history_operator_view`, each keeping its class (item number) and date.
- The call-ready line now sits directly under the title.
- The injected Florida practice line follows it.
- **The first number a reader meets is 327** — call-ready.
- No script errors.

Both screenshots ship with this upload.

## 2 · Rung 6 — not run

**The Firecrawl key is not in the environment.** I didn’t retry the plain fetch that already halted. The standard records that a free-tier key is authorised, not yet created, and where it will never be stored.

## 3 · Rung 4 — the address reader stopped on its own plant

**Plant 1 failed.** `delmontefresh.com/about-us/contact-us` was read (200), but the reader found no Florida street address on it. That is the half that must find, and it didn’t.

**Plant 2 passed.** A page with no Florida address returned none.

**Per the standing condition, the reader stops and rung 4 stays owed.** I didn’t loosen the pattern to make the plant pass. Whether the page states an address in a form the pattern misses is not established. **Reads: 2.**

## 4 · Rung 5 and Part F — blocked, verified

- No Florida registry pull and no Illinois DTA file are on disk.
- The validator’s practice-flag rule is in force.

So both are blocked, not merely unstarted. Rung 5 is recorded in your words, as a pass: the validator caught a wrong write before it landed.

## 5 · The eleven naming scripts

**Measured, not read from filenames.** Importing `stepd.py` and `officer.py`, the live pipeline, loads exactly `naming`, `naming10`, `naming2`, `naming3`, `naming4` and `naming5`.

- **`naming10` is canonical**, and the other five are its dependencies.
- **`naming6` to `naming9`** are referenced by recorded runs, so they stay.
- **Only `naming_v1` is referenced by no script.** It moves to `superseded/`, with a README saying which module is canonical and how that was established.

**My first sort was wrong, and I corrected it.** Matching import lines only, it would also have moved `naming7` and `naming9`. A whole-word search found both in use.

**Caught before delivery.** Importing the old run scripts to measure them executed their code, which rewrote three committed record files. I returned them to their committed bytes, so they don’t ship. It’s registered: a measurement that runs the thing it measures is not read-only.

## Close

- **Validator:** 54 of 54.
- **Call-ready:** unchanged at 327 rows across 320 companies. No row changed, so the entry 15 check is clean.
- **Reads:** 2, both on the address plants.

## The 9 files in this upload

- delivery-manifest.json
- florida-standard.json
- index.html
- item358-address-plants.json
- item358-index-after.png
- item358-index-before.png
- item358-report.md
- superseded/README.md
- superseded/naming_v1.py
