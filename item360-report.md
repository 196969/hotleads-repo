# Item 360 — the exposure mitigations

DashRite Advisory LLC · HOT Leads · 2026-11-01 · head before `90c119d` · **this upload holds 85 files**, all to the repository root, listed in `delivery-manifest.json`. **One deletion by hand:** `suppression.json`.

## Founders 72

**Boies, standing dissent (ruling 28), carried in every verdict:** DR-CSA-0002 reads “Unevidenced — no signed copy on file”; it bears on EST-1044.

| Verdict | Pass | Hold | Blind |
|---|---|---|---|
| On the brief (`90c119d`) | 7 of 72 | 0 | **64 of 72** |
| On the delivery | 7 of 72 | 0 | **64 of 72** |

- **Denominator:** 72 seats and 725.0.
- **Buffett and Cuban** read Blind: the roster labels their readings in prose (“out-prepare”) rather than by seat, so they cannot be bound (Item 307).
- **Lemonis** reads Blind by construction: no `check_part9` key, and his Part 9 ground was withdrawn on 30 October.
- **Herjavec** votes from seat `sell`, named and merged in Item 307.

## Gate

**`gate.py` exited 4:**
- file count 34 of 34;
- validator 54 of 54;
- guard 82 of 82;
- stop 3 set.

Clone against raw: 616 of 616 files agree.

## 1 · robots.txt — written, and weaker than the brief assumes

`robots.txt` at the root reads `User-agent: *` / `Disallow: /`. Its fetched status and body are reported at the gate after you commit, since a file can’t be served before it lands.

**Its honest limits:**
- **It stops compliant indexing, not access.** Anyone holding a URL still reads the file.
- **It probably won’t even be read.** Crawlers read robots.txt only at the host root, `https://196969.github.io/robots.txt`, which answered **404** today because no `196969.github.io` repository exists. A file at `/hotleads-repo/robots.txt` sits where crawlers don’t look.

**What would make it count:** a `196969.github.io` repository whose root `robots.txt` disallows `/hotleads-repo/`, or a `noindex` tag on each page. Both are written into the standard, so the mitigation isn’t described as more than it is.

## 2 · suppression.json — out of the served repository, and proven against a local copy

**Every page now reads the list from the operator’s own computer** — the 54 market pages and all 27 consoles. Nothing reads it from the public site:
- The page offers **Load the suppression list from this computer**.
- The loaded list is kept in that browser.
- With no local copy, **every address stays withheld**: fail closed.

**Proven in Chromium:**
- With no local copy, 150 of 150 Florida Email links are withheld, and the load control shows.
- With the local file loaded, the links are released.
- A suppressed domain, and separately a suppressed address, are each **refused at Copy**.
- `send.py`, reading a local `suppression.json`, refused the suppressed address (reason: do-not-contact).

**The list held 0 entries when it was removed,** so no one was ever named on the public site.

**Before Eddie emails:** keep `suppression.json` (supplied separately, not for the repository) on the machine he uses, and load it once in each browser.

## 3 · The standard entry

The standard’s `exposure_item360` sets the contradiction down in full. The Partner Pack sentence is quoted word for word: “not to be exported, shared, merged into another system or carried to another venture. Their value rests on their accuracy and on their being the firm’s alone”. Beside it, the measured fact: the lists are publicly served without sign-in.

## 4 · What is exposed, measured on 2026-11-01

| Exposed | Count |
|---|---|
| Verified decision-maker rows | **3,804** (of 6,421 rows in the 54 market files) |
| Rows carrying a published phone number | **1,291** |
| Outreach logs | **28** |
| Working-evidence files (item records, read logs, per-URL records, run reports) | **295** |

**Not done, by ruling:** the repository stays public and no market file moves. That is Item 361.

## Close

- **Validator:** 54 of 54.
- **Operator-view guard:** 82 of 82.
- **Call-ready:** unchanged at 327.
- **Reads:** 0.
