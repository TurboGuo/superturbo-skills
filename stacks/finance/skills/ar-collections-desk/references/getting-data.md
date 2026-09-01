# Getting the ledger into the skill

Three paths. All three end with a file in `data/`, then `ar.py snapshot`.
Checked August 2026. Re check the tool names before relying on them.

---

## Path A: the QuickBooks connector, in Claude or ChatGPT

Fastest when the client already uses QuickBooks Online, and it is free on both clients.

**Claude:** sidebar to Customize to Connectors, plus button, Browse connectors, Intuit
QuickBooks, Connect. Then in a chat, plus button to Connectors to toggle it on.

**ChatGPT:** Plugins in the left sidebar, search "Intuit QuickBooks", Connect, sign in.

Ask for the open invoices, then **save the raw response** to `data/invoices.json` before doing
anything else. The script reads the nested QuickBooks shapes directly: `CustomerRef.name`,
`DocNumber`, `TxnDate`, `DueDate`, `TotalAmt`, `Balance`, `BillEmail.Address`.

Do not retype figures out of the chat into a file. Save the response.

### The no subscription half

The Intuit connector also works without a QuickBooks Online subscription: attach or paste a CSV,
PDF or image of transactions and it returns a profit and loss statement, a cash flow summary and
an industry benchmark. That path is useful for a first conversation, but it is **not** an
invoice ledger. This skill needs invoice level data with due dates and open balances, so a
client on that path uses Path B.

---

## Path B: CSV export, works everywhere

No connection, no developer account, no subscription. Works in every country, on every plan, and
for a client who will not grant an AI tool ledger access. It is also the only path that handles
several client organisations in one run.

**QuickBooks Online**
1. Reports, then **Invoice List** for invoice level detail, or **A/R Aging Detail**.
2. Set the report period wide enough to include the oldest open invoice.
3. Export, then Export to Excel or CSV.
4. For payment behaviour as well, export a paid invoice list over the last 12 months and pass
   both files after `--input`.

Columns the script reads without configuration: `Date`, `Num`, `Customer`, `Due Date`, `Amount`,
`Open Balance`, `Email`, `Status`, `Currency`, `Paid Date`. Extra columns are ignored.

**Xero**
1. Business, then Invoices, then the Awaiting Payment tab.
2. Select all, then Export. Xero writes `Invoices.csv`.
3. For payment history, repeat on the Paid tab and pass both files.
4. Or: Accounting, Reports, Aged Receivables Detail, Export.

**Any other ledger.** Anything that exports one row per invoice will work if it carries a
customer, an invoice number, a date, a due date, an amount and an open balance under any of the
common names. Run `snapshot` and read the exceptions: unmapped columns show up there.

### Dates are the thing that goes wrong

US exports are month first (`04/15/2026`), most of the rest of the world is day first
(`15/04/2026`). The script detects the order from values that can only be one way round, and
**reports the order it used** in the workings block. Check that line.

A file where every date is ambiguous, for example a short list where nothing exceeds the 12th,
cannot be detected. Pass `--date-order mdy` or `--date-order dmy` yourself. Getting this wrong
turns a 90 day debt into a 3 day debt silently.

---

## Path C: a local MCP server

For a client already running the official Intuit or Xero MCP server, or a hosted fork. Call the
invoice list tool, save the raw JSON to `data/invoices.json`, then run `snapshot` on it.

Read access is enough. This skill never writes to a ledger.

---

## What good input looks like

| Field | Needed | Why |
| --- | --- | --- |
| Customer | yes | Grouping, statements, briefs |
| Invoice number | yes | Every figure has to be traceable to a document |
| Due date | for ageing | Without it the invoice lands in the No due column |
| Open balance | yes | The amount still owed, not the invoice total |
| Invoice total | for DSO | Credit sales in the period |
| Email | for briefs | Missing emails are reported as call these instead |
| Paid date | for behaviour | Average days to pay, and who pays early |
| Currency | if not one | Never mix currencies in a total |

Include paid invoices in the export. Without them there is no payment history, and payment
history is 20 points of the priority score.
