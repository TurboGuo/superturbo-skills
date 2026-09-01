# NOTICE

**Built with AI assistance and may contain mistakes. Check every figure against the ledger before
sending, charging or filing.** This warning appears at the top of the HTML pack and at the foot of
every command. Do not remove it from either.

This skill is a derivative work.

## Upstream

**accounts-receivable**, from `Denymbird/accounts-receivable-skills`
https://github.com/Denymbird/accounts-receivable-skills
MIT License, Copyright (c) 2026 Paidnice.

The full upstream licence text is in `LICENSE` and **must travel with every copy of this
folder, including every client copy.** The MIT terms are satisfied by keeping `LICENSE` and
this file in place.

Everything in this skill originates there unless listed below: the snapshot model, the ageing
buckets, the DSO method, the late fee proration, the priority score, the brief format, the
tone ladder, the statement HTML, and the design rule that the script computes and the model
only narrates.

## What SuperTurbo changed, 26 Aug 2026

Verified against the upstream assertions, which all still pass, plus 33 new checks.
59 upstream plus 33 new equals 92. Only the test harness changed, to pass an explicit snapshot
path now that working state no longer defaults to the current directory.

1. **The aged table now cross foots on its own face.** Upstream excluded invoices with no due
   date from the bucket columns while still counting them in the row total, and explained the
   difference in a footnote. A controller reads that as a broken report. There is now a
   **No due** column, every row is checked against its own total, and the script prints either
   a cross foot confirmation or a CROSS FOOT FAILED block.

2. **A DSO longer than its own measurement window is refused.** Upstream printed it as fact.
   On a thin file that produces numbers like 192.8 days on a 90 day window, which does not mean
   customers take 193 days to pay, it means the balance is older than the sales history in the
   file. The script now flags it, explains why, names the window to re run with, and points at
   average days to pay instead. `dso_reliable` is in the JSON output.

3. **A customer who pays before the due date reads as early.** Upstream printed "pays -1.0 days
   late on average". Now: "pays 1.0 days early on average", and "pays on time on average"
   inside half a day either way.

4. **The date order reported is the date order used.** Upstream recomputed it for the workings
   block from dates that had already been normalised to ISO, so the detector always failed and
   the block fell back to a hardcoded `dmy`. A US QuickBooks export was parsed correctly and
   then described as day first, in the one block a client is told to trust. `normalize` now
   returns the order it used, and a multi file run that disagrees is raised as a
   `mixed_date_order` exception rather than silently picking one.

5. **Briefs and statements land beside the snapshot**, not in whatever directory the terminal
   was in. Absolute `--out` paths are honoured. Upstream scattered client files into the
   working directory.

6. **One self contained HTML collections pack, `ar.py pack`.** New, not in the upstream. Aged
   table, hand written inline SVG chart, call sheet and exceptions in a single file with no
   images, no scripts, no fonts and no external requests, readable in light and dark. `--out` is
   required so the client names the path. Upstream emitted one markdown brief plus one HTML
   statement per customer, which is a toolkit output rather than something a client opens.

7. **Month over month diff, `--compare`.** New. Each pack embeds its own figures in a
   `<script type="application/json" id="ar-state">` block, and the next run reads the previous
   pack and opens with what moved: no longer open, newly open, and moved with part payments
   named. State travels inside the deliverable, so nothing is cached on disk.

8. **Working state goes to the system temp directory**, not the current one.

Also: US and QuickBooks first defaults, a QuickBooks style US fixture
(`tests/fixtures/quickbooks_open_invoices.csv`), the Xero fixture renamed for clarity, and
`references/getting-data.md` rewritten around the QuickBooks connector path.

## Licence of the changes

The changes above are released under the same MIT terms as the upstream work, so this folder
stays single licensed and a client copy carries one `LICENSE` file. This is a deliberate
exception to SuperTurbo's default of PolyForm for its own work: a derivative of MIT code cannot
be relicensed under a non commercial licence, and splitting one script across two licences
would be worse than useless to a client.
