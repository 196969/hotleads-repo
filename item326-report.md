# Item 326 — the 274 integrity breaks

DashRite Advisory LLC · HOT Leads · 31 October 2026 · opened on `c82dd28` (the Item 325 commit, gated clean: 446 of 446 files, 32 of 32 at the commit-pinned address). Zero reads, 15 markets.

## The definition every row moved on

**Status answers whether the verification held. Tier answers whether the row fits the practice.**

| What the row’s own note establishes | Result |
|---|---|
| A scale or fit demotion, with the verification held | Reclassified |
| A control demotion (shared control is what was verified) | Verified |
| Public or PE control | Tier C, Downgraded |
| A Tier C row whose note names the disqualifier | Downgraded |
| Neither tier nor status | Named and left |

Downgraded means the verification failed or the row is out. No row moved to make a count balance.

## The four counts (of 274)

| Count | Rows |
|---|---|
| Moved on its own note | **102** |
| Moved to Tier C by disqualifier | **5** |
| Named and left | **167** |
| Note contradicts itself | **0** |

**The 102 moved on their own note:**
- 97 to Reclassified: dealer-block rows, professional-practice classes, real-estate classes, franchise systems, and scale.
- 4 to Verified, each a control demotion: Cooks Pest Control (Alabama parent), Winzeler Gear (family-owned acquirer), Dot Transportation (subsidiary of a large in-state family company), and Ed Napleton Honda (within a large family group).
- 1 Tier C row to Downgraded: Wintrust Financial (Chicago), whose note says “Public company”.

**The 5 moved to Tier C by disqualifier:**
- Gibson Brands (Tennessee): PE-owned.
- Columbia Sportswear (Oregon): public.
- Willamette Valley Vineyards (Oregon): Nasdaq.
- Oregon Tool (Oregon): Platinum Equity owned.
- Scheid Family Wines (California): publicly reporting, OTC-traded.

**Two rows read in full against the pattern’s first answer:**
- **Martin Resource Management (Texas):** its note names a publicly traded MLP, but the company is that MLP’s private parent. It is Reclassified (structure + scale), not Tier C.
- **Scottsdale Ferrari (Arizona):** its note records a “public-parent suspicion — confirm”. A suspicion is not a disqualifier, so the row is named and left.

**The 167 named and left, by reason** (the result, not a shortfall):

| Reason | Rows |
|---|---|
| The note leaves verification open (“Verify”, “Pending”, “not individually verified”, “ghost-row”, “See #”) | 63 |
| An owner or acquirer is named, but the note doesn’t say whether it is public or PE | 59 |
| Employee-owned or ESOP | 21 |
| Competitor | 11 |
| The note settles neither tier nor status | 10 |
| Tier A row whose note gives a scale or fit demotion | 1 |
| Tier C row whose note names no disqualifier (Sikich, Chicago) | 1 |
| A suspicion, not an established disqualifier | 1 |

What some of these mean:
- **The 59 owner-named rows** include notes like “KKR owned”, “Carlyle owned”, “EMCOR subsidiary” and “Hearst owned”. The owner is named, but the note does not state its class. Moving them on knowledge of who KKR is would be moving them on something outside the note. One ruling, “a named PE firm or public company in the note counts as stating the class”, would settle most of them.
- **The 21 employee-owned rows** sit against the standing ESOP ruling, which seats a named-decision-maker ESOP row in Tier A. This brief moves a tier only by disqualifier.
- **The 11 competitors:** the standing 19 October ruling gives them Unverified, a status this brief’s mapping does not include.
- **The Tier A row:** Reclassified means demoted, so writing it on a Tier A row would make status and tier disagree.

**The fourth count, contradictions.** A note contradicts itself if its own disposition clauses send the row to different tiers, or if it states a public or PE disqualifier and also an independent or no-sponsor finding. No row met either test.

**By market:**

| Market | Moved on own note | To Tier C | Named and left |
|---|---|---|---|
| Arizona | 34 | 0 | 9 |
| California | 10 | 1 | 2 |
| Chicago | 6 | 0 | 3 |
| Colorado | 27 | 0 | 8 |
| Georgia | 1 | 0 | 21 |
| Minnesota | 0 | 0 | 16 |
| Missouri | 0 | 0 | 12 |
| New York | 0 | 0 | 17 |
| North Carolina | 3 | 0 | 19 |
| Oregon | 0 | 3 | 13 |
| Tennessee | 0 | 1 | 0 |
| Texas | 9 | 0 | 38 |
| Utah | 0 | 0 | 2 |
| Virginia | 0 | 0 | 2 |
| Washington | 12 | 0 | 5 |

Downgraded rows outside Tier C: **274 → 167.**

## The dropdown precondition

This was checked before any write:
- The six files that gain “Reclassified” have the option added in the same pass: Arizona, California, Colorado, North Carolina, Texas and Washington.
- `chicago.html` has no status dropdown, so there was nothing to add. Under the standing rule, a control the file never had is not added.

Pre-existing mismatches, reported and not touched, because no row this pass wrote depends on them:
- Tennessee’s rows carry Downgraded, which its dropdown lacks.
- Texas’s rows carry Unverified, which its dropdown lacks.
- Eight files offer “Research pending” or “Pending by rule” with no working-file row carrying it.

## Close

- **Validator:** 54 of 54 on final bytes. No source line was written.
- **Index:**
  - Verified 3,715 / 3,632 → **3,718 / 3,635.** Georgia 112 → 113; Chicago +2, moved by the certain changes, since its published figure doesn’t reproduce by count.
  - Dialable 4,177 / 4,088 → 4,172 / 4,083.
  - Tier C rows 1,796 → 1,801.
  - The market column still sums to the headline.
- **Records:** every row, with its decision and the words of its note it moved on, is in `item326-rows.json`.
