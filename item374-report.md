# Item 374 · The per-row Email button and the full composer, restored
DashRite Advisory LLC · 3 November 2026 · base b0bb24b · 196969/hotleads-repo, main

## Founders 72 (Dash `_councilRoster()`: 72 seats, 725.0)
- **Brief, read on b0bb24b:** 4 Pass · 2 Hold · 65 Blind · Chair. Hold: #19 User-first platform (the control was bare text, and faded to 40% wherever no suppression list was loaded) · #55 Whether a figure is shown honestly ("suppressed" carried two causes).
- **Delivery, read on the delivered bytes:** 6 Pass · 0 Hold · 65 Blind · Chair. No dissent.

## Gate
Head b0bb24b, 636 files, raw pinned to the head plus a fresh clone: 636 of 636 agree on bytes, git blob and SHA-256 (raw-plus-clone). Recorded before the first edit.

## The complaint, measured (instrument: item374-visibility-census.json)
- **florida.html, before:** 150 of 150 rows carry the control. It is `<a class="dr-em">Email</a>`, bare text in the Links cell, red text with no border, background or padding. With no suppression list in the browser, every one reads "Email — suppressed" at 40% opacity with its pointer off.
- **All 54 pages, before:**

| State | Width | Rows | Visible | Styled as a button |
|---|---|---|---|---|
| Clean | 1440 | 6414 | 0 | 0 |
| Clean | 480 | 6414 | 0 | 0 |
| List loaded | 1440 | 6414 | 6414 | 0 |
| List loaded | 480 | 6414 | 6414 | 0 |

- **console-florida.html:** no per-row Email control. The queue's Work button opens the row panel, whose "Open the composer" opens the shared composer (Item 371 ruling: the queue shape stays).
- **Composer census:** 83a861b, the last Florida composer before Items 370 and 371, against b0bb24b. Nothing missing; the additions were ruled (register 4).

## The work
- Every Email control on the 54 market pages now renders as a styled button in the Links cell. Nothing was added to the table, and the composer it opens is unchanged.
- A held control is legible, amber at full opacity: "Email — held: suppression list not loaded". "Email — suppressed" now appears only for an address on the list.
- Escape closes the panel. Focus moves into To on open and back to the button on close. A row emailed this session says so on its own button.
- The same layer is on all 54 market pages and all 27 consoles.

## Proven on the final bytes
- **Buttons, all 54 pages:**

| State | Width | Rows | Visible | Styled as a button |
|---|---|---|---|---|
| Clean | 1440 | 6414 | 6414 | 6414 |
| Clean | 480 | 6414 | 6414 | 6414 |
| List loaded | 1440 | 6414 | 6414 | 6414 |
| List loaded | 480 | 6414 | 6414 | 6414 |

  With no list loaded, all 6414 buttons are held: visible, and refusing by design.
- **Panel opens** on Florida's Invicta Watch Group row (To sales@invictawatch.com) and Arizona's Shamrock Foods row (To empty). Focus lands in To on open.
- **Resources:** with all five ticked, each link lands exactly once. Unticking Services and Request a quote removes only those two lines. Changing tone to Follow-up keeps the other three. The body at each step is in item374-behaviour.json.
- **Copy rich (Florida):** 4 clickable anchors, with named links for Who we are, How we work in your state, and the Health Assessment. Hosted logo; bold "Edward Edick"; EEdick@dashriteadvisory.com; postal line; STOP line. The label reads "Copied ✓ paste into New mail".
- **Open in Outlook (rich):** mailto:sales%40invictawatch.com?subject=Following%20up%20%E2%80%94%20DashRite%20Advisory. With CC set to "not-an-address" it refuses: "Fix CC: not-an-address".
- **Escape** closed the panel and focus returned to the row's button, which then read "Email · emailed this session".
- **Suppression:** with sales@invictawatch.com listed as unsubscribed, the row's button reads "Email — suppressed" and is held. Its title reads "suppressed: unsubscribed (2026-11-03)".
- **Parity:** zero deviations across 54 market pages; all 27 consoles carry the shared composer.
- **Structure:** 6,414 data rows at 12 cells; 0 rows with an extra cell.
- **Load errors:** 0 across 182 pages. **End to end:** 32 of 32.
- **Google search links:** 0. **Gmail URLs and Gmail-domain addresses:** 0, including this package's own files, scanned after every record was written.
- **Reversal:** 81 changed files, each reversing to the base byte for byte.

## For the operator
On a browser that has never loaded the suppression list, every Email button is held, by Item 360's fail-closed rule, and now says so. Load suppression.json on any market page and the buttons release.
