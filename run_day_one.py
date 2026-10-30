"""run_day_one.py — launches practice_browser.py on the declared day-one coverage: the first 32 Tier A rows in ascending row order (practice-classes.json run_order.day_one). The reader itself is unchanged.
Fault filed 2026-10-30: the first launch filtered by row NUMBER <= 32 (11 rows) instead of the first 32 rows in order; corrected here, the run continued on rows 12-32 of the order under the same start date."""
import sys,asyncio,practice,practice_browser
_p=practice.pipeline; lo,hi=(int(sys.argv[1]),int(sys.argv[2])) if len(sys.argv)>2 else (1,32)
practice.pipeline=lambda m:sorted(_p(m),key=lambda r:int(r['key']))[lo-1:hi]
asyncio.run(practice_browser.main('florida','Timothy A. Edick',6.0))
