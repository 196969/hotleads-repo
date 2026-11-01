# superseded/ — naming modules no script references (Item 358, 2026-11-01)

**Canonical:** `naming10.py` is the entry point of the live pipeline.

**How that was established:** by measurement, not by filename. Importing `stepd.py` (the census and call-ready instrument) and `officer.py` loads exactly six modules: `naming`, `naming10`, `naming2`, `naming3`, `naming4` and `naming5`. All six stay at the root.

**Also at the root, though the live pipeline doesn’t load them:** `naming6.py`, `naming7.py`, `naming8.py` and `naming9.py`. Recorded runs reference them by name — the `window10`–`window16` discovery scripts, `core_run1`–`3`, `chi_run1`, `i322` and `w15_gate` — so moving them would break those runs’ reproducibility.

**Moved here:** `naming_v1.py` alone. It is referenced by no `.py` file. Its only mentions are the hash lists inside earlier gate records.

**A correction to this item’s first reading:** I first sorted these modules by matching `import namingN` lines. That matching missed the other forms the scripts use, so it marked `naming7` and `naming9` unreferenced. A whole-word search of every script found them in use, and they were put back. That is the same family as the runner reading the wrong cell: an instrument measuring a narrower property than it reports.
