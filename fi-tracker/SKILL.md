---
name: fi-tracker
description: Render Turbo's financial independence (FI) dashboard with a fixed three part layout — a progress card, an assets over time table where each cell shows total assets plus the sustainable years that pile covers while still earning the real return, and a single asset growth line chart where color encodes return rate and line style encodes saving level (all combinations on one graph, plus a dashed FI threshold line). Use when Turbo says "fi tracker", "FI dashboard", "show my FI progress", "when can I retire", "track FI", "what's my FI number", "years to financial independence", "asset growth chart". This skill assumes the user already knows what FI means and produces the personalized projection directly. If the user's request is in Chinese, render the whole dashboard and reply in Chinese.
---

# FI Tracker

Takes a user's current cash + investments, monthly saving levels, and a target monthly burn, then renders one dashboard widget that projects assets over 35 years. This skill encodes a LOCKED layout — do not add, remove, or reorder sections. The output must match the reference layout below exactly.

## When to use

Trigger on: "fi tracker", "FI dashboard", "show my FI progress", "when can I retire", "FI tracker", "track FI", "what's my FI number", "years to financial independence", "asset growth chart".

Do NOT trigger for:
1. Generic compound interest projections (use `networth-sensitivity`)
2. Burn rate analysis (use `burn-rate-tracker`)
3. Single question FI explainers (the concept is assumed known)

## Always render the latest visualization

CRITICAL freshness rules so the user always sees the current numbers:
1. Recompute every value from the current inputs on EVERY run. Never reuse a table, chart, or progress figure from an earlier turn in the conversation.
2. Run the Math section in `bash_tool` (python3) before emitting the widget, every time, even if the inputs look unchanged. The widget values come from that fresh computation, not from memory.
3. The widget `title` slug MUST be unique per render so a stale cached widget is never shown. Use `fi_tracker_{burn_in_k}_{cash_in_k}c_{invest_in_k}i_v{N}` where `{N}` increments each time you re-render within a conversation (v1, v2, v3...). A changed slug forces a fresh render.
4. If the user edits any input mid conversation, treat it as a full new run: recompute, bump the version suffix, and emit a new widget. Do not patch the old one in place.
5. Only ONE dashboard widget per response, and it must be the most recent computation.

## Inputs

Every run elicits inputs fresh via the elicitation form. The skill does NOT read portfolio.md, finance.xlsx, or any personal file.

The form keeps the SAME FIVE separated question groups as before, in this order. Every answer is a plain text input EXCEPT question 2 (cash composition), which is a single select pill group with an Other escape hatch. Apart from that one pill group there are NO single/multi select, NO cards, NO tiles, NO sliders anywhere in the form. Each remaining question is its own `.elicit-group` with one `.elicit-textarea` (or `.elicit-textarea` styled compact). Return rate and horizon are fixed in code and never asked.

1. **Cash balance** — Question: "How much cash do you have today (checking + HYSA + money market)?" `data-name="cash"`, placeholder e.g. `10000`.
2. **Cash composition** — Question: "How is your cash split, and at what real rate?" `data-name="cash_split"`, `data-multi="false"`. Render as a single select `.elicit-pills` group (plain pills, labels are short) with these four options, plus an Other escape hatch: `All checking (0% real)` [data-value=`all checking, 0% real`], `All HYSA (1.5% real)` [data-value=`all HYSA, 1.5% real`], `Half and half (0.75% real)` [data-value=`half checking half HYSA, 0.75% real`], `Other` [data-other, paired `.elicit-other` text input keyed `data-for="cash_split"`, placeholder `e.g. mostly money market, ~1% real`]. Localize the Other label to the user's language.
3. **Investment balance** — Question: "How much in investments (equities, crypto, bonds)?" `data-name="investments"`, placeholder e.g. `10000`.
4. **Target burn rate** — Question: "What monthly burn rate should I model for retirement?" `data-name="burn"`, placeholder e.g. `2000`.
5. **Monthly saving levels** — Question: "Which monthly saving levels should I project? List up to three for the clearest chart." `data-name="savings"`, placeholder e.g. `100, 500, 1000`.

Render the form via `mcp__visualize__show_widget` using the standard `.elicit-*` classes, with the canonical File header SVG, the five `.elicit-group` blocks above, and standard `.elicit-skip` / `.elicit-submit` footer buttons. Zero onclick handlers, zero `<script>`. Title slug for the FORM widget: `fi_tracker_inputs`.

Example group for the four plain text questions (repeat the pattern, swapping question text, `data-name`, and placeholder):

```html
<div class="elicit-group">
  <label class="elicit-question">How much cash do you have today (checking + HYSA + money market)?</label>
  <textarea class="elicit-textarea" data-name="cash" placeholder="e.g. 10000"></textarea>
</div>
```

Cash composition (question 2) is the one pill group. Emit it exactly like this:

```html
<div class="elicit-group">
  <label class="elicit-question">How is your cash split, and at what real rate?</label>
  <div class="elicit-pills" data-name="cash_split" data-multi="false">
    <button type="button" class="elicit-pill" data-value="all checking, 0% real">All checking (0% real)</button>
    <button type="button" class="elicit-pill" data-value="all HYSA, 1.5% real">All HYSA (1.5% real)</button>
    <button type="button" class="elicit-pill" data-value="half checking half HYSA, 0.75% real">Half and half (0.75% real)</button>
    <button type="button" class="elicit-pill" data-value="Other" data-other>Other</button>
  </div>
  <input type="text" class="elicit-other" data-for="cash_split" placeholder="e.g. mostly money market, ~1% real" hidden>
</div>
```

If the user already provided everything in plain text (in chat, not the form), skip the form entirely and go straight to computing + rendering.

### Parsing the answers

Answers arrive on one line keyed by the humanized `data-name` labels (`Cash`, `Cash split`, `Investments`, `Burn`, `Savings`). Parse into:
- `cash` (USD number)
- cash composition → cash buckets. The pill returns one of the preset values: `all checking, 0% real` → one bucket at 0% real; `all HYSA, 1.5% real` → one bucket at 1.5% real; `half checking half HYSA, 0.75% real` → TWO buckets, half the cash at 0% and half at 1.5% (do not collapse to a single 0.75% rate, since the buckets compound separately). If the Other input was used, map its words to buckets the same way: "checking" or "0%" → 0% real; "HYSA" or "high yield" → 1.5% real; a stated blend → split into the named buckets; if unstated, default to one bucket at 0% real and say so in the chat reply.
- `investments` (USD number)
- `burn_monthly` (USD per month)
- `saving levels` (list of monthly USD amounts). Aim for exactly three. If the user names more or fewer, take the first three or pad with sensible defaults $100 / $500 / $1,000.

If a required value is genuinely missing and not inferable, ask one short plain text follow up rather than re rendering an empty form.

Fixed constants (do NOT ask the user):
- Return rates for the chart: `[3%, 5%, 7%]` real
- Projection horizon: 35 years
- Base return for the progress card, the assets table, and the drawdown math: 7% real
- Milestone years for the table: 0, 5, 10, 15, 20, 25, 30, 35
- The FI threshold line drawn on the chart sits at the 7% perpetuity FI number

## Math

```python
def balance(n, saving_monthly, r, cash_buckets, invest0):
    cash_total = sum(amt * (1 + cr) ** n for amt, cr in cash_buckets)
    pmt = saving_monthly * 12
    if r == 0:
        inv = invest0 + pmt * n
    else:
        inv = invest0 * (1 + r) ** n + pmt * ((1 + r) ** n - 1) / r
    return cash_total + inv

fi_number_perpetuity = (burn_monthly * 12) / base_return   # 7% real
fi_number_4pct = (burn_monthly * 12) * 25
progress_pct = current_net_worth / fi_number_perpetuity * 100
```

### Sustainable years (the second number in each table cell)

This is the key difference from a naive assets / burn division. The pile KEEPS EARNING the base real return (7%) while being drawn down. Each year: grow by `r`, then withdraw `burn_year`. If the return alone covers the burn, the pile lasts forever.

```python
import math
def sustainable_years(A, r, burn_year):
    if A * r >= burn_year:
        return None            # perpetual — return covers burn, principal untouched
    ratio = (burn_year / r) / (burn_year / r - A)
    return math.log(ratio) / math.log(1 + r)
```

Render `None` as the word `perpetual` in the cell. Otherwise show one decimal, e.g. `47.8 yr`. The crossover happens exactly at `A == fi_number_perpetuity` (where `A*r == burn_year`).

`cash_buckets` is a list of `(amount, real_rate)` pairs derived from the parsed cash composition. The progress bar fill = `min(progress_pct, 100)`%.

## Output layout (LOCKED — render exactly these sections in order)

ONE widget via `mcp__visualize__show_widget`. Begin with a visually hidden `<h2 class="sr-only">` one sentence summary. Wrap everything in `<div style="padding: 1rem 0;">`.

### 1. Header
- 13px secondary line: `FI tracker · projected through year 35`
- 22px/500 title surfacing the headline: if no saving level reaches FI within 35 years at base return, say so (e.g. "FI not reached within 35 years at $100 per month; reached near year 22 at $1,000 per month"); otherwise name the earliest FI year per saving level.
- 13px secondary subtitle restating inputs: net worth, cash split, saving levels modeled.

### 2. Progress card
Full width, `var(--color-background-secondary)` bg, 1.5rem padding, `border-radius-lg`. A 3 up grid of metrics: current net worth, FI number (7% perpetuity), FI number (4% rule). Below it: a label `X% of FI number · $Y to go`, then a progress bar — track is `var(--color-background-primary)` with a 0.5px border, fill is `#1D9E75`, both `border-radius: 999px`, height 14px.

### 3. Assets over time table
- Title 16px/500: `Total assets over time · 7% real return`
- 13px secondary caption: `Each cell: total assets and how many years of $Xk / mo burn it sustains while still earning 7% real. At or above $[FI]k the return covers the burn, so the pile lasts forever (perpetual).`
- Table, `table-layout: fixed`, wrapped in an `overflow-x:auto` div. Header row: `Year` then one column per saving level (`$100 / mo`, etc.). Rows = milestone years.
- Each cell shows BOTH values: assets in $K, then the sustainable years (one decimal) or the word `perpetual`. Format: `$235k · 13.8 yr` or `$617k · perpetual`.
- Light green heatmap on the cells keyed to ASSET SIZE (not the years): larger balances get deeper green. Ramp: `#FAEEDA` (small) → `#EAF3DE` → `#C0DD97` → `#97C459` → `#639922` (white text) → `#3B6D11` (white text). Text on light cells uses `#412402` or `#173404`; on the two darkest greens use `#fff`.

### 4. Asset growth line chart
- Title 16px/500: `Asset growth by saving level`
- 13px secondary caption: `Color is the return rate, line style is the saving level. All [N] lines on one chart. Dashed gray marks the $[FI]k FI line.`
- TWO custom HTML legends stacked: first maps COLOR → return rate (3% gray `#888780`, 5% blue `#185FA5`, 7% teal `#1D9E75`); second maps LINE STYLE → saving level (lowest solid, middle dashed, highest dotted), drawn with `border-top` swatches in `var(--color-text-secondary)`.
- Chart.js line chart in a `position:relative; height:320px` wrapper. One dataset per (saving × return) combination — three savings × three returns = nine lines — PLUS one extra dataset: a flat dashed gray line at `fi_number_perpetuity` labeled `FI line $[FI]k` (`borderColor:'#B4B2A9'`, `borderDash:[10,6]`, `borderWidth:1.5`, `pointRadius:0`, `tension:0`). For the nine data lines: color comes from the return rate, `borderDash` from the saving level, `borderWidth:2, pointRadius:0, pointHoverRadius:4, tension:0.2`. Disable the built in legend. Tooltip label: `$500 @ 5%: $Xk`. Y axis ticks formatted `$Xk`, x axis titled `Year`. Canvas needs `role="img"` and a descriptive `aria-label`.
- Mirror `balance()` in JS with `cash0` and `invest0` injected as constants.

### 5. Insight cards
2 col responsive grid (`minmax(240px,1fr)`), each card white bg, 0.5px border, `border-radius-lg`, 14px padding, 13px/500 title + 13px secondary body. Four cards, content varies by inputs:
- "What pulls FI forward fastest" — saving rate vs return, in concrete dollar terms from the table, framed around flipping a pile from finite to perpetual
- "Where you sit today" — % complete on the FI number, and the cash drag note (0% real cash never contributes to the return that sustains withdrawals)
- "Why some cells say perpetual" — once assets reach the FI number, the real return equals the annual burn, so only growth is spent and principal stays whole; below the line principal erodes
- "Sequence of returns warning" — constant real return is a smooth best case; a weak early stretch can drain a pile that looked perpetual on paper

Loading messages: `["Building the asset table", "Drawing the growth lines"]`.
Title slug: `fi_tracker_{burn_in_k}_{cash_in_k}c_{invest_in_k}i_v{N}` (bump `{N}` on every re render — see freshness rules).

## Reference implementation (the exact chart script structure to emit, with values substituted)

`cash0`, `invest0`, the `rates` array, the `savs` array, and the FI line value are the only things that change between runs.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const cash0 = 10000, invest0 = 10000;
const fiLine = 480000;
const years = Array.from({length:36}, (_,i)=>i);
function bal(n, savingM, r){
  const pmt = savingM*12;
  const inv = r ? invest0*Math.pow(1+r,n) + pmt*(Math.pow(1+r,n)-1)/r : invest0 + pmt*n;
  return cash0 + inv;
}
const rates = [{r:0.03, c:'#888780'},{r:0.05, c:'#185FA5'},{r:0.07, c:'#1D9E75'}];
const savs = [{s:100, dash:[]},{s:500, dash:[6,4]},{s:1000, dash:[2,3]}];
const datasets = [];
rates.forEach(rt=>{ savs.forEach(sv=>{
  datasets.push({
    label:'$'+sv.s+' @ '+Math.round(rt.r*100)+'%',
    data: years.map(n=> Math.round(bal(n, sv.s, rt.r))),
    borderColor: rt.c, backgroundColor: rt.c,
    borderDash: sv.dash, borderWidth:2, pointRadius:0, pointHoverRadius:4, tension:0.2
  });
}); });
datasets.push({
  label:'FI line $'+Math.round(fiLine/1000)+'k',
  data: years.map(()=>fiLine),
  borderColor:'#B4B2A9', backgroundColor:'#B4B2A9',
  borderDash:[10,6], borderWidth:1.5, pointRadius:0, pointHoverRadius:0, tension:0
});
new Chart(document.getElementById('growthChart'), {
  type:'line', data:{ labels:years, datasets },
  options:{ responsive:true, maintainAspectRatio:false, interaction:{mode:'nearest', intersect:false},
    plugins:{ legend:{display:false}, tooltip:{ callbacks:{ label:(c)=> c.dataset.label+': $'+Math.round(c.parsed.y/1000)+'k' } } },
    scales:{ x:{ title:{display:true, text:'Year'}, ticks:{maxTicksLimit:12} },
      y:{ title:{display:true, text:'Total assets'}, ticks:{ callback:(v)=> '$'+Math.round(v/1000)+'k' } } } }
});
</script>
```

## Output style

0. **Language**: if the user's request is in Chinese, render all widget headings, table labels, legend labels, insight cards, and the chat reply in Chinese. Otherwise English. Match the user's language.
1. Round sustainable years to one decimal in table cells; whole years for FI year headlines. Render the perpetual case as the word `perpetual`.
2. All asset values shown in $K
3. Real returns only; never silently mix nominal
4. No hyphens in prose
5. Sentence case in widget headings

## Chat reply after the widget

3 to 5 sentences: the headline FI outcome at base scenario, the most actionable lever quantified from the table, the perpetuity vs 4% rule framing, and the cash drag observation. Call out the steepness near the FI line (small balance gains flip the pile from finite to perpetual). Do NOT duplicate table numbers wholesale.

## Privacy

User supplied inputs only. Does not read any personal file.

## Edge cases

1. Return 3% real at moderate burn: FI may be unreachable within 35 years — say so in the headline rather than extrapolating
2. Cash already exceeds the FI threshold: show progress at 100%+ with a note, and the table cells read perpetual from year 0
3. Single saving level: chart shows three lines (one per return rate) plus the FI line; legends still apply
4. All cash 0% portfolio: assets grow only by contributions; sustainable years stay low and never perpetual unless investments carry it over the line — flag the cash drag
