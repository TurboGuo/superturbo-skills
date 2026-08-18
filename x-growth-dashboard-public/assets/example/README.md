# Example inputs

Fully synthetic data for a fictional account, including the post ids. Use it to
smoke test the scripts and to see the exact shape of each input file.

```bash
cd assets/example
python3 ../../scripts/prepare.py --content content.csv --overview overview.csv \
  --followers 820 --start 2026-03-02 --end 2026-03-15 --out metrics.json
python3 ../../scripts/render.py --metrics metrics.json --analysis analysis.json \
  --suggestions suggestions.json --meta meta.json --out example-dashboard.html
```

To test folder discovery instead, point `discover.py` at this directory. It should
identify `content.csv` as the content export and `overview.csv` as the overview
export from their header rows alone:

```bash
python3 scripts/discover.py assets/example
```

`analysis.json`, `suggestions.json` and `meta.json` here are deliberately thin.
They pass validation and show the schema. They are **not** a model for the writing
quality expected of a real build. For that, read `references/writing-guide.md`.
