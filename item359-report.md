# Item 359 — the operator view, and a guard so it stays clean

DashRite Advisory LLC · HOT Leads · 2026-11-01 · head before `c7c1e2d` · **this upload holds 34 files**, listed in `delivery-manifest.json`.

## Founders 72

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Verdict | Pass | Hold | Blind |
|---|---|---|---|
| On the brief (`c7c1e2d`) | 7 of 72 | 0 | **64 of 72** |
| On the delivery | 7 of 72 | 0 | **64 of 72** |

- **Denominator:** 72 seats and 725.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

**`gate.py` exited 4** at the open: file count 9 of 9; validator 54 of 54; stop 3 set. Fresh clone against raw: 612 of 612 files agree.

## 1–2 · What came off, and where it went

**37 elements on 27 pages** — the index, 25 expansion pages, california.html and florida-expansion.html — were relocated whole and unedited into the standard’s `history_operator_view_item359`. Each entry keeps its page, its element and what replaced it, if anything.

**2186 words** left the operator view.

**On the index:**
- **Call-ready:** “327 rows across 320 companies in 27 markets”.
- **Backlog:** “Acquisition backlog: 182 rows”.
- **Dialable:** kept, without its history.
- **Removed:** the “Measured 2026-10-31, self-overlap checked…” block; the retired totals; the 353, 203, 267 and 552 lines; the settled-contest narratives; and two market-table annotations naming Item 323.

**On the market pages:**
- 25 “The prior 50-row expansion … is retired” paragraphs;
- California’s residue addendum;
- Florida intake’s “(Item 320 Part 9)” heading.

## 3 · The rule, written into the standard

A figure on the operator view stands alone. Its derivation, its history and the figures it replaced live in the standard. One document, one reader.

## 4 · The guard, proven by a forced failure

`opview_guard.py` runs inside `gate.py`’s stop 2. It refuses `Item ###`, “at the close of”, “at head ”, “is withdrawn”, “is retired”, “re-measured”, or a bare commit hash in rendered text. It reads all of `index.html` and every console page, and everything outside the row tables on the 54 market pages.

| Step | Gate exit | Guard reading |
|---|---|---|
| **Before** | — | refused 27 of 82 pages |
| **After the relocation** | — | 82 of 82 clean |
| **Planted:** “ (at the close of Item 357)” on the call-ready line | **3** | 81 of 82 |
| **Removed** (index back to its pre-plant bytes) | **4** | 82 of 82 |

The 4 at the end is stop 3, still set on watts.com, as ruled.

**Scope, decided and reported (A8).** On market pages the guard doesn’t read inside the row tables. A row’s dated source lines name items by design: they are the evidence the validator requires. Overrule if you want them read too.

## 5 · The register entry

The removal ruled in Item 351 came back, and came back again. This time it was derivation written inside the figures. The commits that brought it in, each by the build’s own passes:
- `5f6f98e` (31 Oct): the “Measured…” block;
- `c82dd28` (31 Oct): “Item 325 added 160 rows…”;
- `a634164` (1 Nov): the backlog’s “at the close of…” history.

It was found by the Chair reading the live page, not by any instrument. The guard exists because the ruling alone did not hold.

## 6 · First screenful (Chromium, 1366×768)

| | Line under the title | First number |
|---|---|---|
| **Before** | “Call-ready: 327 rows across 320 companies (counted by company name) in 27 markets (Florida 58; Item 325 added 160 rows …” | 327, buried in narrative |
| **After** | “**Call-ready: 327 rows across 320 companies in 27 markets**” — nothing else on the line | **327** |

No script errors. Both screenshots ship with this upload.

## Close

- **Validator:** 54 of 54.
- **Call-ready:** 327, unchanged. No row changed, so the entry 15 check is clean.
- **Reads:** 0.
