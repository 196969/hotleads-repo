# Item 362 — the operational close

DashRite Advisory LLC · HOT Leads · 2026-11-01 · head before `8c92fc3`.

**Two uploads to two different repositories:**
- **hotleads-repo:** 84 files, listed in `delivery-manifest.json`.
- **DashRite-Advisory- (the website):** 48 pointer pages.

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

## Gate

**`gate.py` exited 4.** Clone against raw: 617 of 617 files agree.

## 1 · florida.html, settled with a status code — 200

`196969.github.io/DashRite-Advisory-/florida.html` → **301** → `dashriteadvisory.com/florida.html` → **200**.

- The composer block is present and **unfixed**: no `DRA_GATE`. It begins: `id="dr-email">(function(){ var slug=location.pathname.split('/').pop()…`
- **Done:** the website’s 48 market pages are replaced by one-line pointers to the hotleads-repo copy. Each carries noindex, a canonical link and an immediate redirect, and **no composer remains on the website**.
- **Proof** — opening `dashriteadvisory.com/florida.html` and landing on the fixed page — runs at the gate after you upload, because it can’t be shown before the files are live.

## 2 · The suppression control — proven by exercising (Chromium)

| Step | Result |
|---|---|
| Before loading | The instruction shows; every Email button is locked |
| Load a file with 1 record | “Suppression list loaded — 1 record(s) — file dated 2026-11-01 — loaded …”; the button stays offered |
| Add an address to the local file and **re-load it, without clearing storage** | 2 records |
| Try the newly added address | **Refused at Copy** (unsubscribe) |

On 53 market pages. `chicago.html` has no Item 314 loader, so its composer still refuses at Copy when no list is loaded.

## 3 · The operator instruction, in your words

“Every Email button stays locked until the suppression list is loaded. That is the fail-safe, not a fault. Load it before the first call of the day.”
- It is on every market page’s suppression line and on all 27 consoles.
- **Edward’s guide isn’t in this repository**, so it needs the same sentence added where the guide lives.

## 4 · The standard, amended; the fault written

The repository-level robots.txt is inert on its own; the host-root file is the one that acts, and it doesn’t exist. The register entry, in your words: *a mitigation verified at the wrong address, reported as working, caught by checking the host root. The 200 proved the file existed, not that it functioned.*

## 5 · Stop 3 — settled: watts.com fails both routes, and three tasks are struck

**Page-text test, unchanged:** fail. The page calls the company “Watts”.

**Corroboration route:**
- **SEC filing:** the 10-K filed 2026-02-23 names Watts Water Technologies and **never mentions watts.com**. The SEC submissions record’s website field is empty.
- **Structured data:** the page names “Watts” and “Watts Llc” — not the legal entity.
- **Registry entry:** not available to this reader. There is no registry seed on disk.

**The other plants:** nutrition.gov fails on the domain exclusion and accurate.com on the page test, as expected.

**Struck as unreachable by this reader:**
- Part D’s re-runs;
- the Alabama and Oklahoma census;
- the dealer-block re-reads.

The reader is not released. Four items of drift end here.

## 6 · The four contests

| Contest | Reader | Result |
|---|---|---|
| Zirkle Fruit | Firecrawl, 200 | Read; **no revenue figure on the page — held** |
| Elliott Electric Supply | Firecrawl, 200 | Read; **no revenue figure — held** |
| Christensen Arms | Firecrawl, 200 | Read; **no controlling owner named — held** |
| Rappahannock Oyster | — | **Read struck.** I re-probed `rroysters.com`, a domain I recalled rather than sourced. Own knowledge is refused, so that read proves nothing. Held, and registered as my fault. |

## Close

- **Call-ready, measured:** 327 rows across 320 companies, unchanged — no row was written.
- **Backlog, measured:** 182, unchanged.
- **Validator:** 54 of 54. **Guard:** 82 of 82.
- **Reads:** 11 in total:
  - SEC: 3 (the ticker list, the submissions record and the 10-K);
  - Firecrawl: 5 (four contest pages and watts.com);
  - plain fetch: 3 (the website check and the accurate.com plant).
