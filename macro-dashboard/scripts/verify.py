#!/usr/bin/env python3
"""
Render the built dashboard and check it.

Usage:
    python3 scripts/verify.py macro-dashboard-2026-08-19.html

Screenshots both tabs in both themes, reports console and page errors, and
re greps the RENDERED text for hyphens (checking the source is useless, CSS and
URLs are full of them).

Needs playwright. If chromium is not found it prints the paths it tried.
"""

import glob
import json
import os
import subprocess
import sys
import tempfile

SHOT_JS = r"""
import { chromium } from 'playwright';

const file = process.argv[2];
const outDir = process.argv[3];

const candidates = [undefined, process.env.CHROME_PATH].filter((v, i) => i === 0 || v);

let browser = null, lastErr = null;
for (const executablePath of candidates) {
  try { browser = await chromium.launch(executablePath ? { executablePath } : {}); break; }
  catch (e) { lastErr = e; }
}
if (!browser) { console.log(JSON.stringify({ fatal: String(lastErr) })); process.exit(0); }

const page = await browser.newPage({ viewport: { width: 1180, height: 1400 }, deviceScaleFactor: 2 });
const errs = [];
page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
page.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });

await page.goto('file://' + file);
await page.waitForTimeout(600);

const shots = [];
const snap = async (name) => {
  const p = outDir + '/verify-' + name + '.png';
  await page.screenshot({ path: p, fullPage: true });
  shots.push(p);
};

let text = '';
await snap('verdicts-light');
text += await page.evaluate(() => document.body.innerText);
await page.click('#tab-s'); await page.waitForTimeout(350);
await snap('signals-light');
await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
await page.waitForTimeout(150);
text += '\n' + await page.evaluate(() => document.body.innerText);
await page.click('#themebtn'); await page.waitForTimeout(300);
await snap('signals-dark');
await page.click('#tab-v'); await page.waitForTimeout(300);
await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
await page.waitForTimeout(150);
await snap('verdicts-dark');
text += '\n' + await page.evaluate(() => document.body.innerText);

const hyphen = [...new Set(text.split('\n'))].filter(l => l.includes('-'));
console.log(JSON.stringify({ errs, shots, hyphen }));
await browser.close();
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    html = os.path.abspath(sys.argv[1])
    if not os.path.exists(html):
        print(f"  ERROR no such file: {html}")
        sys.exit(1)
    out_dir = os.path.dirname(html) or "."

    env = dict(os.environ)
    if "CHROME_PATH" not in env:
        found = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))
        if found:
            env["CHROME_PATH"] = found[-1]

    # node resolves packages relative to the script's own directory, so the temp
    # script has to live somewhere that can see node_modules
    probe = subprocess.run(["node", "-e", "console.log(require.resolve('playwright'))"],
                           capture_output=True, text=True, cwd=os.getcwd())
    if probe.returncode != 0:
        print("  ..    playwright not found, installing")
        subprocess.run(["npm", "i", "playwright"], capture_output=True, text=True,
                       cwd=os.getcwd())

    js = os.path.join(os.getcwd(), ".macro-verify.mjs")
    with open(js, "w", encoding="utf-8") as f:
        f.write(SHOT_JS)

    proc = subprocess.run(["node", js, html, out_dir], capture_output=True,
                          text=True, env=env, cwd=os.getcwd())
    try:
        os.unlink(js)
    except OSError:
        pass

    line = (proc.stdout or "").strip().splitlines()
    if not line:
        print("  ERROR playwright produced no output")
        print(proc.stderr[-2000:])
        sys.exit(1)
    try:
        res = json.loads(line[-1])
    except json.JSONDecodeError:
        print("  ERROR could not parse verifier output")
        print(proc.stdout[-2000:])
        print(proc.stderr[-2000:])
        sys.exit(1)

    if res.get("fatal"):
        print("  ERROR could not launch chromium")
        print("        " + res["fatal"][:400])
        print("        set CHROME_PATH, or npm i playwright")
        sys.exit(1)

    ok = True
    if res["errs"]:
        ok = False
        for e in res["errs"]:
            print(f"  ERROR {e}")
    else:
        print("  OK    no console or page errors")

    if res["hyphen"]:
        ok = False
        print("  ERROR hyphen found in rendered text:")
        for h in res["hyphen"][:20]:
            print(f"        {h}")
    else:
        print("  OK    no hyphen in rendered text")

    print("  SHOTS " + ", ".join(os.path.basename(s) for s in res["shots"]))
    print("        read these before shipping, the validator checks data not layout")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
