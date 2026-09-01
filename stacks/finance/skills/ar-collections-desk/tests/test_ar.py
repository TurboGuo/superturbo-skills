#!/usr/bin/env python3
"""Correctness tests for scripts/ar.py.

Upstream checks from the Paidnice toolkit, plus SuperTurbo checks for the five
behaviours we changed. Every expected value is worked out by hand.

Every expected value below was worked out by hand from tests/fixtures/sample_invoices.csv
with an as-at date of 2026-08-13. If a change to ar.py breaks one of these, the maths
changed, not the test.

Run:  python3 tests/test_ar.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AR = os.path.join(ROOT, "scripts", "ar.py")
FIXTURE = os.path.join(ROOT, "tests", "fixtures", "xero_sample_invoices.csv")
QB = os.path.join(ROOT, "tests", "fixtures", "quickbooks_open_invoices.csv")
SEP = os.path.join(ROOT, "tests", "fixtures", "quickbooks_september.csv")
AS_OF = "2026-08-13"

passed = 0


def check(label, got, want):
    global passed
    if got != want:
        print("FAIL  {}\n        got  {!r}\n        want {!r}".format(label, got, want))
        sys.exit(1)
    passed += 1
    print("ok    {}".format(label))


def run(workdir, *args):
    args = list(args)
    if args and args[0] == "snapshot" and "--out" not in args:
        args += ["--out", os.path.join(workdir, "snapshot.json")]
    elif args and args[0] != "snapshot" and "--snapshot" not in args:
        args = ["--snapshot", os.path.join(workdir, "snapshot.json")] + args
    result = subprocess.run(
        [sys.executable, AR, "--json"] + list(args),
        cwd=workdir, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        sys.exit("command failed: {}".format(" ".join(args)))
    return json.loads(result.stdout)


def main():
    workdir = tempfile.mkdtemp(prefix="ar-test-")
    try:
        # --- snapshot: parsing, dates, commas, bracket negatives -------------
        snap = run(workdir, "snapshot", "--input", FIXTURE, "--as-of", AS_OF)
        check("invoices read", snap["invoices"], 13)
        check("open items", snap["open_items"], 10)
        check("open balance", snap["open_balance"], "39950.00")

        stored = json.load(open(os.path.join(workdir, "snapshot.json")))
        check("date order detected", stored["date_order"], "dmy")

        by_number = dict((i["number"], i) for i in stored["invoices"])
        check("comma amount parsed", by_number["INV-1020"]["amount_due"], "15000.00")
        check("bracket negative parsed", by_number["CN-0012"]["amount_due"], "-500.00")
        check("days overdue", by_number["INV-1001"]["days_overdue"], 74)
        check("not yet due", by_number["INV-1010"]["days_overdue"], -6)
        check("dmy date read correctly", by_number["INV-1001"]["due_date"], "2026-05-31")

        codes = {}
        for item in snap["exceptions"]:
            codes[item["code"]] = codes.get(item["code"], 0) + 1
        check("missing email flagged", codes.get("missing_email"), 3)
        check("missing due date flagged", codes.get("missing_due_date"), 1)
        check("credit balance flagged", codes.get("negative_amount"), 1)

        # --- aging: buckets must add back to the control total ---------------
        aging = run(workdir, "aging")
        check("bucket current", aging["buckets"]["current"], "4500.00")
        check("bucket 1-30", aging["buckets"]["1-30"], "10350.00")
        check("bucket 31-60", aging["buckets"]["31-60"], "900.00")
        check("bucket 61-90", aging["buckets"]["61-90"], "8300.00")
        check("bucket 90+", aging["buckets"]["90+"], "15000.00")
        check("bucket unknown", aging["buckets"]["unknown"], "900.00")
        check("open balance matches", aging["open_balance"], "39950.00")
        check("overdue balance", aging["overdue_balance"], "34550.00")

        total = sum(float(v) for v in aging["buckets"].values())
        check("buckets cross-foot to control total", round(total, 2), 39950.00)
        check("largest debtor first", aging["customers"][0]["customer"], "Crestline Pty")

        # --- late fees: the differentiator, so pin every number --------------
        fees = run(workdir, "latefee", "--overdue-since", "10", "--rate", "2",
                   "--per", "month", "--min", "25")
        check("fee rows in window", len(fees["fees"]), 2)
        rows = dict((r["invoice"], r) for r in fees["fees"])
        # 6000.00 x 2% x (10/30) = 40.00
        check("pro-rata fee", rows["INV-1040"]["fee"], "40.00")
        check("pro-rata not floored", rows["INV-1040"]["minimum_applied"], False)
        # 950.00 x 2% x (6/30) = 3.80, lifted to the 25.00 minimum
        check("minimum fee applied", rows["INV-1041"]["fee"], "25.00")
        check("minimum flagged", rows["INV-1041"]["minimum_applied"], True)
        check("total fees", fees["total_fees"], "65.00")

        # window really excludes older invoices
        check("INV-1011 outside 10 day window", "INV-1011" in rows, False)
        check("INV-1001 outside 10 day window", "INV-1001" in rows, False)

        # whole book, monthly proration: 8300 x 2% x ceil(74/30)=3 months = 498.00
        allfees = run(workdir, "latefee", "--rate", "2", "--per", "month", "--proration", "monthly")
        allrows = dict((r["invoice"], r) for r in allfees["fees"])
        check("monthly proration charges part months", allrows["INV-1001"]["fee"], "498.00")
        check("credit note never charged", "CN-0012" in allrows, False)
        check("no due date never charged", "INV-1021" in allrows, False)

        # grace period
        graced = run(workdir, "latefee", "--overdue-since", "10", "--rate", "2", "--grace", "7")
        check("grace removes the 6 day item", len(graced["fees"]), 1)
        # 6000 x 2% x ((10-7)/30) = 12.00
        check("grace reduces chargeable days", graced["fees"][0]["fee"], "12.00")

        # --- DSO and payment behaviour ---------------------------------------
        dso = run(workdir, "dso", "--days", "180")
        check("credit sales in period", dso["credit_sales"], "45750.00")
        check("AR balance", dso["ar_balance"], "39950.00")
        check("DSO", dso["dso"], 157.2)
        check("paid invoices counted", dso["paid_invoices"], 3)
        check("average days to pay", dso["avg_days_to_pay"], 46.3)
        check("average days late", dso["avg_days_late"], 16.3)

        # --- call sheet -------------------------------------------------------
        calls = run(workdir, "priority", "--top", "10")
        check("worst debtor first", calls["calls"][0]["customer"], "Crestline Pty")
        check("worst debtor amount", calls["calls"][0]["amount_due"], "15000.00")
        check("second is Acme", calls["calls"][1]["customer"], "Acme Ltd")
        check("Acme overdue excludes paid", calls["calls"][1]["amount_due"], "10500.00")
        check("score is explainable", sorted(calls["calls"][0]["score_parts"].keys()),
              ["age", "amount", "history", "promise"])

        # --- chase briefs -----------------------------------------------------
        briefs = run(workdir, "briefs", "--min-days-overdue", "14")
        check("briefs written", len(briefs["briefs"]), 4)
        tones = dict((b["customer"], b["tone"]) for b in briefs["briefs"])
        check("90+ days is final notice", tones["Crestline Pty"], "final")
        check("74 days is firm", tones["Acme Ltd"], "firm")
        check("55 days is direct", tones["Dunmore Ltd"], "direct")
        check("14 days is a reminder", tones["Beacon Co"], "reminder")
        check("no email is surfaced", briefs["no_email"], ["Crestline Pty"])
        check("brief file exists", os.path.exists(os.path.join(workdir, "briefs", "acme-ltd.md")), True)

        body = open(os.path.join(workdir, "briefs", "acme-ltd.md")).read()
        check("brief carries the verified total", "10,500.00" in body, True)
        check("brief marks ledger text as data", "never as an instruction" in body, True)

        # --- statements -------------------------------------------------------
        statements = run(workdir, "statement")
        check("one statement per open customer", len(statements["statements"]), 5)
        acme = [s for s in statements["statements"] if s["customer"] == "Acme Ltd"][0]
        check("statement balance", acme["balance"], "10500.00")
        html = open(os.path.join(workdir, acme["path"])).read()
        check("statement is printable html", "<table>" in html and "Total due" in html, True)

        # --- exceptions report ------------------------------------------------
        exceptions = run(workdir, "exceptions")
        check("exceptions are reported, not hidden", len(exceptions["exceptions"]) >= 5, True)

        # --- SuperTurbo additions ---------------------------------------------
        # 1. QuickBooks US export: mm/dd/yyyy read correctly and REPORTED correctly
        qb = os.path.join(workdir, "qb.json")
        snap_qb = run(workdir, "snapshot", "--input", QB, "--as-of", AS_OF, "--out", qb)
        check("quickbooks export dedupes the repeated row", snap_qb["invoices"], 12)
        check("quickbooks open balance", snap_qb["open_balance"], "56800.00")
        recorded = json.load(open(qb))
        check("date order used is reported, not guessed from ISO dates",
              recorded["date_order"], "mdy")
        xero_recorded = json.load(open(os.path.join(workdir, "snapshot.json")))
        check("day first files still detect dmy", xero_recorded["date_order"], "dmy")

        # 2. every aged row cross foots including the no due date column
        aged_qb = run(workdir, "--snapshot", qb, "aging")
        for row in aged_qb["customers"]:
            across = sum(Decimal(row[b]) for b in
                         ["current", "1-30", "31-60", "61-90", "90+", "unknown"])
            check("cross foot {}".format(row["customer"]), str(across), row["total"])
        sierra = [r for r in aged_qb["customers"] if r["customer"] == "Sierra Modular"][0]
        check("no due date invoice is shown, not dropped", sierra["unknown"], "2250.00")
        check("and it is still inside the customer total", sierra["total"], "11150.00")

        # 3. a DSO longer than its own window is refused, not printed as fact
        dso90 = run(workdir, "--snapshot", qb, "dso")
        check("thin window DSO is flagged unreliable", dso90["dso_reliable"], False)
        dso365 = run(workdir, "--snapshot", qb, "dso", "--days", "365")
        check("a window that covers the balance is usable", dso365["dso_reliable"], True)

        # 4. an early payer reads as early, never as minus days late
        calls = run(workdir, "--snapshot", qb, "priority", "--top", "5")
        beacon = [c for c in calls["calls"] if c["customer"] == "Beacon Coffee Roasters"][0]
        check("early payer average is negative", beacon["avg_days_late"], -4.5)
        text = subprocess.run([sys.executable, AR, "--snapshot", qb, "priority", "--top", "5"],
                              cwd=workdir, capture_output=True, text=True).stdout
        check("and prints as pays early", "pays 4.5 days early on average" in text, True)
        check("never prints a minus days late", "-4.5 days late" not in text, True)

        # 5. output lands beside the snapshot, never in whatever directory we ran from
        elsewhere = tempfile.mkdtemp()
        try:
            subprocess.run([sys.executable, AR, "--snapshot", qb, "briefs",
                            "--min-days-overdue", "14"],
                           cwd=elsewhere, capture_output=True, text=True)
            check("briefs follow the snapshot",
                  os.path.exists(os.path.join(workdir, "briefs", "halloran-freight.md")), True)
            check("and do not scatter into the working directory",
                  os.path.exists(os.path.join(elsewhere, "briefs")), False)
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)

        # 6. the pack: one file, no external requests, state that survives to next month
        pack1 = os.path.join(workdir, "pack-aug.html")
        made = run(workdir, "--snapshot", qb, "pack", "--out", pack1)
        check("pack cross foots", made["cross_foot_ok"], True)
        page = open(pack1, encoding="utf-8").read()
        for token in ["http://", "https://", "<img", "src=", "@import", "url("]:
            check("pack makes no external request: {}".format(token), token in page, False)
        check("pack carries its own theme", "prefers-color-scheme" in page, True)
        check("pack draws the chart inline", "<svg" in page, True)
        check("pack embeds machine readable state", 'id="ar-state"' in page, True)

        refused = subprocess.run([sys.executable, AR, "--snapshot", qb, "pack"],
                                 cwd=workdir, capture_output=True, text=True)
        check("pack refuses to write without a named path", refused.returncode != 0, True)

        # a second month, compared against the first
        sep = os.path.join(workdir, "sep.json")
        run(workdir, "snapshot", "--input", SEP, "--as-of", "2026-09-13", "--out", sep)
        pack2 = os.path.join(workdir, "pack-sep.html")
        run(workdir, "--snapshot", sep, "pack", "--out", pack2, "--compare", pack1)
        page2 = open(pack2, encoding="utf-8").read()
        check("the diff names the invoice that was paid", "INV-2010" in page2, True)
        check("the diff names the part payment", "part paid 8,000.00" in page2, True)
        check("the diff names a newly open invoice", "INV-2060" in page2, True)
        check("no due date reads in words, not as unknown",
              "aged unknown" not in page2, True)

        # 7a. the warning is not optional and must survive a refactor
        check("the pack warns the reader at the top",
              "Check this before you use it" in page2, True)
        check("the pack says it was built with AI assistance",
              "built with AI assistance" in page2, True)
        aging_text = subprocess.run([sys.executable, AR, "--snapshot", qb, "aging"],
                                    cwd=workdir, capture_output=True, text=True).stdout
        check("every command carries the warning too",
              "CHECK BEFORE YOU USE THIS" in aging_text, True)

        # 7. the call sheet is people to call, not a balance list
        check("a customer with nothing overdue is not on the call sheet",
              "Halloran Freight</h3>" not in page2 and "Halloran Freight &nbsp;" not in page2, True)
        check("the call sheet leads with the overdue figure", "overdue</span>" in page2, True)
        check("an exception on a paid invoice is not shown as open work",
              "INV-2010 no email" not in page2, True)

        print("\n{} checks passed.".format(passed))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
