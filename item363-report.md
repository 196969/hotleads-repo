# Item 363 — rung 4’s reader, the three contests, the last dealer row

**Target repository: 196969/hotleads-repo, main.** Head before `f3c7109`. **9 files**, listed in `delivery-manifest.json`, which names that target.

## Founders 72

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Verdict | Pass | Hold | Blind |
|---|---|---|---|
| On the brief | 7 of 72 | 0 | **64 of 72** |
| On the delivery | 7 of 72 | 0 | **64 of 72** |

- **Denominator:** 72 seats and 725.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## 1 · Gate, before any edit

**`gate.py` exited 4:** file count 84 of 84; validator 54 of 54; guard 82 of 82; stop 3 set. Clone against raw: 618 of 618 files agree.

## 2 · Rung 4 — the reader is declared unreleasable, and 37 rows are struck

**The second evidence route:** a dated SEC record whose registrant name equals the row’s full name.

| Plant | Expected | Result |
|---|---|---|
| Fresh Del Monte Produce | must find | **fail**, three times |
| A name no registrant carries | must find nothing | pass |
| Accurate Box Company | must find nothing | pass |

**Why the first plant kept failing:**
1. SEC’s ticker list omits the company.
2. EDGAR’s company page returns it under its current name, DEL MONTE CORP.
3. The former-name parse still found no whole-name match.

**I stopped adjusting at the third attempt.** Three changes, each defensible on its own, add up to a reader being bent toward its plant. The reader is not released.

**Struck as unreachable by this reader:** 37 Florida call-ready rows without a dated address source, all named in the standard’s `rung4_item363`. All 37 are privately held, so their principal addresses sit in the Florida registry, which stays owed to you. They are unreachable by this reader, not by every reader.

## 3 · The three contests — closed as Blind

Each has a dated line on both of its rows, listing every route tried.

| Contest | Read (Firecrawl, 2026-11-01) | Routes tried | Result |
|---|---|---|---|
| **Zirkle Fruit** | own home page: no revenue figure | own site (plain fetch refused, Item 343; Firecrawl, Item 362); a trade-press search (Item 346); searches in Items 340 and 343 | **Blind** |
| **Elliott Electric Supply** | own home page: no revenue figure | own site (plain fetch refused, Items 340, 347 and 358; Firecrawl, Item 362) | **Blind** |
| **Christensen Arms** | own about page: no controller named | own about page (Items 343 and 362); a third-party page (Item 346) | **Blind** |

**Rappahannock** stays struck: its read used a remembered domain.

## 4 · The last dealer row — worked once

**Sewell Automotive (texas.html #119).** Its own site answered through Firecrawl (200) and names the company, but states no ownership class. **Blind**, with a dated line on the row.

## Register

Four entries:
- the bend-to-pass near-instance;
- the contests closed Blind;
- the dealer row worked;
- the second wrong-repository upload today, caught by the validator. The manifest now names its target repository.

## Close

- **Validator:** 54 of 54.
- **Guard:** 82 of 82.
- **Call-ready:** 327 rows across 320 companies, measured and unchanged. No contact was written.
- **Backlog:** 182, unchanged.
- **Reads:** 10 SEC requests (3 plant rounds) and 1 Firecrawl read.
