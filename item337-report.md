# Items 337–338 — route depth, and the four blinded rows

DashRite Advisory LLC · HOT Leads · read 2026-11-01 UTC · opened on `d49f1f7`, the Items 332/335/336 commit.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `d49f1f7`) | 7 | 0 | 64 | 70.0 |
| On this delivery (final bytes) — reported, not adopted (entry 34) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

- Head `d49f1f7`. The commit holds all 9 of the previous pass’s delivered files, byte for byte.
- Clone against cache-busted raw: 471 of 471 files agree.
- The commit was under 5 minutes old, so the 9 changed files were also read at the commit-pinned address. All 9 agree.
- Validator baseline: 54 of 54.

**Read dates.** The reads in this pass ran after midnight UTC, so every new source line carries **2026-11-01**, the date the read was taken.

## Item 337 — route depth, then the plants

**The change.** When the owner’s landing page states no class, the route now follows up to 3 links on the same site whose path or link text names the company itself, and reads those before it returns “class unread”. In order: about, our company, history, investors, who we are, our story, corporate.

**The plants — both pass.**
- **Caterpillar → public**, through SEC’s ticker list (CAT). Caterpillar’s own site refused, so this plant did not exercise route depth.
- **Publix Super Markets → neither.** The route read `publix.com`, found no class statement, followed the link to `corporate.publix.com/about-publix`, and read “…the largest employee-owned company in the United States.”
- **What this proves, and what it doesn’t.** The private plant passes on route depth. The public plant passes on route 2. Route depth has not yet been shown to reach a public company’s own investor page. That is a limit to state, not a failure.

**Instrument status.** These changes live in the builder’s research tools, not the repository. They are **attested, not gated**, and the standard now says so.

## Item 338 — the four rows (ceiling 20; spent 19, 1 remaining)

**A second fault surfaced on the first read.** The Route 4 engine still matched a company’s name to a domain by substring (entry 27’s family):
- “Accurate Box” matched `accurate.com`, a different company, which returned (800) 784-3911.
- “Alliance Shippers” matched `alliance.com`.
Those first results are withdrawn and not written. The engine’s site match is now anchored: the domain’s leading label must start with the name’s first distinctive word and carry its second. The three contact rows were then re-read.

| Row | Result | Source |
|---|---|---|
| Accurate Box Company (new-jersey.html#88) | **written (973) 345-2000** — first read `accurate.com` withdrawn | Src: read accuratebox.com 2026-11-01 |
| Rockford Toolcraft (illinois.html#1) | **written (815) 398-5507** — first read `rockfordfosgate.com` withdrawn | Src: read rockfordtoolcraft.com 2026-11-01 |
| Alliance Shippers (chicago.html #192) | **not written.** No company site in the results on the anchored rule. The (615) 358-9758 it held came from `alliance.com`, another company’s site; the hold was right, and that number is not the company’s. | — |
| Nevada Ready Mix (las-vegas.html #43) | **not re-established.** Its own site is now visible to the search (the fix worked), but the page refused. A dated line in the unestablished form is written. | Src: read nevadareadymix.com 2026-11-01 |

**What the fix recovered:**
- Accurate Box and Rockford Toolcraft are now sourced on their own sites. The Accurate Box number is in New Jersey, 973.
- Nevada Ready Mix’s site is now reachable but refused at this read.
- Alliance Shippers’ blinding turned out to be a misidentification, not a recovery.

**Both surfaces checked (entry 25).** On Accurate Box and Rockford Toolcraft, the plain-text phone cell and the note line carry the same number.

## A wrong write found and withdrawn (entry 22)

The anchored rule raised a question about every earlier Route 4 site, so I ran a zero-read **identity screen** over all 201 sites that returned a number in Items 325, 327 and 331. 54 fail a strict whole-name rule.
- The screen only sized the problem (entry 21). Reading each failure by eye, almost all are the company’s own abbreviated domain: `dickblick.com`, `estwing.com`, `trekbikes.com`, `munsch.com` and similar.
- **One was a wrong write.** In Item 331, Chicago Tag & Label (chicago.html #206) was given (312) 744-5000, read from `chicago.gov`, the City of Chicago’s contact page.
- It is withdrawn **by edit, not restore**. The Item 331 line is replaced by a dated withdrawal, and the phone cell is returned to its earlier (847) 362-5100, matching its pre-331 form byte for byte, unsourced.
- The row is short of call-ready again.

## Close

- **Call-ready:** 312 → 313 rows. Gained: Accurate Box and Rockford Toolcraft, each by a written line (entry 15). Lost: Chicago Tag & Label, by the withdrawal.
- **Companies:** 306 by company name (unchanged), 313 by cell text.
  - Rockford Toolcraft was already call-ready on Chicago #114, so its Illinois row adds a row but no company. Accurate Box adds one company; Chicago Tag & Label removes one.
  - A count that moves only because the method changed adds no company.
- **Validator:** 54 of 54 on final bytes.
- **Index:**
  - Call-ready **313 / 306**.
  - Verified unchanged at 3,805 / 3,722; the market column still sums to it.
  - An Items 337–338 note is added.
- **Standard:**
  - the attestation line (“attested, not gated”);
  - Item 335’s three counts — 13 blinded, 2 consequentially mis-written, 11 changed nothing;
  - the identity-screen result.
- **Ceilings:**
  - Item 337: plants only, 6 reads (calibration, logged).
  - Item 338: 19 of 20 spent, 1 remaining.
  - No run died.

## For the record

- **Entry 27’s family, a fifth instance:** the Route 4 engine’s name-to-domain match was a substring match too. It mis-identified Accurate Box and Alliance Shippers, and, through a looser path, Chicago Tag & Label.
- **Next, the 15 owner-named rows.** They can now run on a reader that has passed both plants, with 53 reads left in Item 332’s ceiling.