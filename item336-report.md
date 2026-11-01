# Items 336 · 332 · 335 — consolidated pass

DashRite Advisory LLC · HOT Leads · 31 October 2026 · opened on `a12c92a`, the Items 333–334 commit.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `a12c92a`) | 7 | 0 | 64 | 70.0 |
| On this delivery (final bytes) — reported, not adopted (entry 34) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

- Head `a12c92a`. The commit holds all 15 of Items 333–334’s delivered files, byte for byte.
- Clone against cache-busted raw: 466 of 466 files agree.
- The commit was under 5 minutes old, so the 15 changed files were also read at the commit-pinned address. All 15 agree.
- Validator baseline: 54 of 54.

## Part A — Item 336 · Grubb and Gay (zero reads)

**Grubb Properties** (north-carolina.html #92)
- **Struck:** “Family-owned since 1963. Third generation.”
- **Governing text:** “DOWNGRADED to B on 26 Aug 2026 — the sixth pre-check caught this one. The file tagged Grubb Properties family-owned; it is NOT. Clay Grubb states repeatedly and in his own words that he "successfully transformed Grubb Properties from a family-owned business to an employee- and board-owned company." The company’s own site: "In bu…”
- **Outcome: Verified.** the governing text: “Grubb Properties today is 100% employee- and board-owned”, quoted from the company’s own site — employee ownership is what was verified.
- **Strike:** over-strike: the span also took in “Third generation”, a fact about Clay Grubb that the governing text restates (“third generation”); nothing lost.

**Gay Construction** (georgia.html #81)
- **Struck:** “Family-owned since 1972.”
- **Governing text:** “Downgraded to B 2026-08-26 (ESOP class): 75+ yrs in continuous operation serving healthcare/university/private clients, but no single-family decision-maker door.…”
- **Outcome: named and left.** the governing text names the “ESOP class” but no clause establishes employee ownership, and it names no single decision maker — named and left.
- **Strike:** exact: the strike covers only “Family-owned since 1972.”.

Downgraded rows outside Tier C: **95 → 94.**

## Part B — Item 332 · the reader fix and the 15

### B1 · The blocklist, every pattern checked

**The fix.** All 52 patterns were substring matches on the domain. The list is now a set of **whole registrable domains** (`x.com`, `twitter.com`, `linkedin.com` and so on), matched on the domain’s registrable part.
- A known-answer test of the matcher passes:
  - `publix.com`, `accuratebox.com`, `rockfordtoolcraft.com`, `careers.davidweekleyhomes.com`, `plumbing.com` and `aboutamazon.com` pass through.
  - `x.com`, `mobile.twitter.com`, `www.linkedin.com`, `en.wikipedia.org` and `craft.co` are blocked.
- The company-site check in the class reader now anchors the owner’s name to the start of a domain label, not to any substring of the domain.

**Every pattern could match a substring of a legitimate domain** — that is what a substring pattern is. Six of them already had, in the logs (zero reads):

| Pattern | Meant to block | Already over-matched in the logs |
|---|---|---|
| `x\.com` | x.com | accuratebox.com, elementix.com, truckmax.com, publix.com, menupix.com, capdex.com, weeklyad.publix.com, corporate.publix.com |
| `yellowpages` | yellowpages.com | yellowpages.net |
| `amazon` | amazon.com | aboutamazon.com, s3.amazonaws.com |
| `google` | google.com | search.google |
| `craft\.co` | craft.co | rockfordtoolcraft.com |
| `careers` | (no domain — a word) | careersclaxtonpoultry.com, careers.davidweekleyhomes.com, bairdcareers.com |

**Two consequential over-matches besides `x.com`:**
- **`craft.co` inside `rockfordtoolcraft.com`** hid Rockford Toolcraft’s own site, in Illinois.
- **`careers`** blocked company pages, including `careers.davidweekleyhomes.com`. It named no domain at all, and is removed.

**Shapes no log has shown yet, which the fix closes:**
- `bing.com` inside “plumbing.com”;
- `owler` inside fowler… and bowler…;
- `manta`, `apollo`, `ebay`, `indeed`, `salary` and `amazon` inside longer names;
- `dnb.com` inside any name ending in “dnb.com”.

### B2 · Both plants — the precondition failed. Part B stops here.

- **Caterpillar → public.** Pass. Read through SEC’s ticker list (CAT).
- **Publix Super Markets → class unread, where it had to return neither.** Fail.

**What changed and what didn’t:**
- The fix worked as a fix: the reader now reaches and reads `publix.com`. Before entry 27’s fix it never did.
- But route 1 reads only the landing page it is handed, and Publix’s storefront home page carries no ownership statement. The press route returned the same page.
- So the fault behind the private plant has moved: from the blocklist, which kept the owner’s site out of view, to the route’s depth, which reads the front page and never the about page. That is a second build, not this one.

**Recorded:** the 15 owner-named rows stay unread, with the reader named as unable to produce “neither”. B3, the three blinded rows, was not run, because it comes after the plants. No read was spent on them. The 44 rows naming no outside owner stay named and left.

**About “Alliance Cut”.** No row carries that name. The discarded domain `alliancecutx.com` came up in Item 331’s search for **Chicago #192, Alliance Shippers**. It is not Alliance Shippers’ site: the token “alliance” matched the start of a different company’s domain. So that discard changed nothing for the row. Alliance Shippers stays held (area code 615), and needs its own read.

**Ceiling:** 60. Spent 7, all on the plants. Remaining 53. No run died.

## Every Route 4 rate from Items 323 to 331 is qualified

In `florida-standard.json`, each section of route rates now carries a dated line: “Measured before entry 27’s fix (2026-10-31). The reader could not reach domains ending in “x.com”. The rate is a floor, not a ceiling.” The sections are:
- `contact_sourcing_routes` (Florida);
- `item325_market_route_yields`;
- `item327_market_route_yields`;
- `item331_carried_remainders`.
The rates are qualified, not withdrawn. The `craft.co` and `careers` over-matches widen the same caveat.

## Part C — Item 335 · the log sweep (zero reads)

Every logged search result from Items 324, 325 and 327 was checked for a domain that the `x.com` pattern discarded.

| Item | Row | Market | Discarded domain | Was it the company’s own site? | The row’s line now |
|---|---|---|---|---|---|
| 324 | Ellis Island Casino | las-vegas | markertrax.com | directory, listing or community page | re-dated |
| 324 | Wells Cargo | las-vegas | elementix.com | directory, listing or community page | written “not re-established at this read” |
| 324 | Nevada Ready Mix | las-vegas | nevadareadymix.com | **own site** | written “not re-established at this read” |
| 324 | South Point Hotel Casino | las-vegas | lifeoutofthebox.com | directory, listing or community page | re-dated |
| 325 | Callie's Charleston Biscuits | south-carolina | menupix.com | directory, listing or community page | no line written by this route (no number found) |
| 325 | Seefried Industrial Properties | georgia | capdex.com | directory, listing or community page | written (404) 233-0204 |
| 325 | Seefried Industrial Properties | georgia | elementix.com | directory, listing or community page | written (404) 233-0204 |
| 325 | Cavender’s Boot City | texas | visitmesquitetx.com | directory, listing or community page | no line written by this route (no number found) |
| 325 | David Weekley Homes | texas | goodlandtx.com | directory, listing or community page | written (844) 777-3717 |
| 325 | David Weekley Homes | texas | mayfairtx.com | directory, listing or community page | written (844) 777-3717 |
| 325 | Underbrink's Bakery | illinois | menupix.com | directory, listing or community page | no line written by this route (no number found) |
| 325 | Stampin' Up! | utah | news4jax.com | news | no line written by this route (no number found) |
| 325 | Accurate Box Company | new-jersey | accuratebox.com | **own site** | held (518) 366-9017 |
| 327 | Marquette Companies | chicago | elementix.com | directory, listing or community page | written (630) 420-4730 |
| 327 | Inland Real Estate Group | chicago | elementix.com | directory, listing or community page | no line written by this route (no number found) |

**The three counts:**
- **Rows blinded:** 13 rows, across 15 discarded results.
- **Rows blinded and consequentially mis-written:** 2.
  - **Nevada Ready Mix** (Las Vegas #43): its own `nevadareadymix.com` was discarded, and its line reads “not re-established at this read”.
  - **Accurate Box Company** (New Jersey #88): its own `accuratebox.com` was discarded, and it holds an out-of-state number taken from a trade-press page.
- **Rows where the discard changed nothing:** 11. Every discarded domain on those rows was a directory, listing, community or news page, not the company’s site.

**Corrections available.** Nevada Ready Mix and Accurate Box can be corrected once their own sites are read. They are not written here: each correction needs the read the row never got, which is its own item with its own ceiling.
**Outside the brief’s three items:** Rockford Toolcraft (Illinois, hidden by `craft.co`) and the Alliance Shippers read (Item 331) belong in the same follow-up.

## Close

- **Call-ready:** 312 → 312. No contact line was written in this pass; status changes do not move call-ready. Entry 15 is clean.
- **Companies, two methods:** 306 by company name; 312 by cell text. Cell text includes the sub-label, so it counts every row as a company. A count that moves only on a method change adds no company.
- **Validator:** 54 of 54 on final bytes.
- **Index:** Verified 3,804 / 3,721 → **3,805 / 3,722** (Grubb, North Carolina 114 → 115). The market column sums to the headline.
- **Standard:**
  - the entry 27 qualifiers;
  - the minority-stake rule, as a dated amendment;
  - the 93 named-and-left rows from Items 333–334, by reason group. These groups are a sizing screen, entry 21, not a classification.
  - No mean.
- **Ceilings:** Part B 60 (7 spent, 53 remaining). Parts A and C read nothing. No run died, so there is no gap between log and ceiling.