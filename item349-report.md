# Item 349 — HOT Leads: the final run · HALTED at integrity stop 3

DashRite Advisory LLC · HOT Leads · 2026-11-01 · opened on `2cc89db`, the Item 348 commit.

**First line of the record — the gate is converted.** `gate.py` is now in the repository. It runs the three integrity stops as code and exits non-zero on each:
- **exit 2:** a delivered-vs-committed file-count shortfall, checked against `delivery-manifest.json`;
- **exit 3:** the validator below 54 of 54;
- **exit 4:** a reader that failed its own proof plant, checked against `reader-plants.json`.

Everything else, it reports. **Run on this delivery, it will exit 4**, because the reader’s proof failed (Part A below). That is the hook working.

**This upload holds 8 files**, listed by name at the end of this report and in `delivery-manifest.json`.

## Verdicts (head of report)

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Founders 72 · Part 9 | Pass | Hold | Blind | Weight passing (of 710.0) |
|---|---|---|---|---|
| On this brief (head `2cc89db`) | 7 | 0 | 64 | 70.0 |
| On this delivery (no market file changed) | 7 | 0 | 64 | 70.0 |

- **Denominator:** 72 seats and 725.0. **Roster file:** 75 entries and 755.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

Section 13’s point stands as a recorded defect: **Blind 64 of 72 is the instrument reporting its own absence.**

## Every figure here is attested, not gated

The amended reader, its Firecrawl fetch layer and its plant results live in the builder’s tools. `reader-plants.json` records them, so that `gate.py` can read them.

## Gate

- **File count by name: delivered 23 · committed 23 · missing 0 · extra 0.**
- Head `2cc89db`.
- Clone against cache-busted raw: 507 of 507 files agree.
- Validator baseline: 54 of 54.

## Part A — the reader amendment, and why the pass stops here

**The amendment.** A candidate domain may match on a shorter anchor: its leading label starts with the name’s first distinctive word. Nothing is accepted unless the page’s own text names the company in full. .gov, .edu and .mil domains are always excluded.

**The plants, on two fetch layers:**

| Plant | Expected | Plain fetch | Firecrawl (keyless) |
|---|---|---|---|
| watts.com for Watts Water Technologies | pass | **refused (403)** | **fail.** The landing page (200) and the depth page `/our-story/history` (200) both read, and neither contains “Watts Water Technologies”. The site calls the company “Watts”. |
| nutrition.gov for Nutrition Industries | fail on the domain exclusion | fail on the domain exclusion ✓ | fail on the domain exclusion ✓ |
| accurate.com for Accurate Box Company | fail on the page test | fail on the page test ✓ (200; the page names a different company) | fail on the page test ✓ |

**Integrity stop 3 fired on both fetch layers.** Under Section 2, Part A stops and works nothing. And because the stop is an integrity stop, **the pass halts.** Parts D, E (census reads) and F (qualification reads) all depend on this reader, and no read was spent on them.

**What the failure shows, stated for a ruling rather than fixed mid-pass.** The plant and the rule disagree.
- Watts’ own pages name the company “Watts”, never “Watts Water Technologies”. So a full-name page test refuses the very case the amendment exists to admit.
- I have not loosened the rule to make the plant pass. A reader that has its rule bent until its own proof passes has proved nothing.
- **Options for the Chair:**
  1. The page test accepts the name minus generic words (“Watts” plus “water technologies” as generic).
  2. The page test accepts the name on the page title or copyright line.
  3. A different first plant.

  Each needs the same three plants run again before use.

## Part B — the Florida registry ingest: not run, blocked by the environment

- **What happened:** `sftp.floridados.gov` resolves, but port 22 does not connect from this sandbox: no connection in 25 seconds, two attempts, and an HTTPS probe returns 403.
- **What that means:** the build environment allows web traffic only. It is not a refusal by the State.
- **What it needs:** a machine with outbound SFTP — Claude Code or your own PC — using the credentials in the brief.
- **What it blocks:** F.1’s Florida seed. The Illinois DTA bulk set from Item 321 is not in the repository as a data file; only the market pages are.

## Firecrawl — verified at source before anything depends on it

- **Keyless works:** a POST to `api.firecrawl.dev/v2/scrape` with no key returned HTTP 200, with the page’s own status code in its metadata.
- **The limits, read at firecrawl.dev/pricing on 2026-11-01:** Free plan 1,000 credits a month; 10 scrapes a minute; a page that answers 403 or 404 still costs 1 credit.
- **What it showed:** `watts.com` refuses a plain fetch (403) but answers Firecrawl (200). That is evidence for Section 0’s rule that a plain-fetch refusal is a finding about our reader, not about the door.

## Reads spent

**8 in total:** 2 plain-fetch plant reads (watts.com 403, accurate.com 200) and 6 Firecrawl credits (the pricing page, three watts.com landing reads, watts.com history, accurate.com).

**One gap in the log, reported as a gap:** the Firecrawl log file kept only its last run’s two entries, because each run rewrote it. The 6 credits are counted from the runs’ printed output, not from the file.

## Not run — every part after Part A, by the halt

Each part opens on the next run once the reader is re-proved, or now if you rule that a part doesn’t depend on the reader:
- **C:** Firecrawl re-probes.
- **D:** the 39 A3 rows.
- **E:** the access map. Its published-class rows are zero-read and don’t depend on the reader; only the Alabama and Oklahoma census does.
- **F:** net-new BD.
- **G:** dispositions.
- **H:** suppression and the send bot.
- **I:** Florida and Illinois to depth, and the console on all 54 pages.
- **J:** the BD report rebuild.
- **K:** the to-do.

**One standing caution for Part H.** I will build the send path and `suppression.json`, but I will not dispatch real emails from an autonomous pass. The first batch goes out only on your explicit go, against a named list of ten recipients you have seen. A sent email can’t be recalled.

## Close

- **Validator:** 54 of 54. No market file changed.
- **Call-ready:** unchanged at 312 rows (305 companies by name, 312 by cell text). No row was written, so the entry 15 check is clean.
- **Rows outside the rule:** unchanged at 61.

## The 8 files in this upload

- delivery-manifest.json
- gate.py
- item349-founders72-verdicts.json
- item349-gate.json
- item349-plain-fetch-log.json
- item349-firecrawl-log.json
- item349-report.md
- reader-plants.json
