---
name: macro-impact
description: >
  Analyze how the current macro environment is bullish or bearish for Turbo's
  asset classes: crypto, US stocks, gold, and US cash. Produces a TEXT ONLY
  reply (never HTML, never a chart or widget): a one word verdict per asset,
  three emoji tagged factors, one sentence reasoning under each, and sources
  linked only at the end. Use whenever Turbo says "macro impact", "macro read",
  "is macro bullish or bearish", "how is macro affecting my assets", "macro on
  crypto", "macro on stocks / gold / cash", "what is macro doing to X", or names
  one or more of the four asset classes and wants the current macro verdict.
  If Turbo names one asset class, cover only that one; otherwise cover all four.
---

# Macro Impact

Give Turbo a fast, sourced read on whether the CURRENT macro environment is
bullish or bearish for each asset class he holds: crypto, US stocks, gold, US
cash. Output is plain text only.

## Scope

1. Parse which asset classes Turbo asked about.
   - Names one (e.g. "macro on gold") -> cover only that one.
   - Says "all", "my assets", "everything", or names none -> cover all four in
     this order: Crypto, US Stocks, Gold, US Cash.
2. Always read the live data fresh. Never answer from memory or a cached verdict.

## Turbo's standing preferences (must follow)

- Use Exa for every web search (mcp__exa__web_search_exa / web_fetch_exa).
- Cross check X for crypto and any product or flow sentiment.
- Prefer OFFICIAL / primary sources over third party ones. For a data point,
  reach for the issuer first: the Federal Reserve (H.15, FOMC), FRED, the US
  Treasury, the BLS (CPI), the BEA (PCE), ISM (PMI), Cboe (VIX), the World Gold
  Council for gold demand, and issuer / on chain data for flows (spot ETF issuer
  pages, Glassnode, CryptoQuant). Only fall back to a third party source when the
  official one is unavailable, lagged, or does not carry the figure, AND the
  third party is an established, reputable outlet (e.g. Bloomberg, Reuters, CNBC,
  FT, WSJ, ICE, S&P, Morningstar, YCharts, Trading Economics, FXStreet). Never
  cite a random blog, forum, or unvetted aggregator as the source of a number.
- Cite every data point. Sources go ONLY at the end as hyperlinks, never inline.
- Do NOT use the hyphen / dash character "-" anywhere in the output. Write
  "risk on", "10 year", "T bill", "late cycle", etc.
- When you calculate anything (real yields), show the subtraction steps.
- Text only. Do not build an HTML file, artifact, chart, or widget for this skill
  even if a visualization would normally be offered.

## Data to pull each run

Pull the master signals once (they drive every asset), then the per asset items.
Prefer official primary sources. Suggested Exa queries and the series to read:

Master signals (shared):
- 10 year Treasury real yield -> FRED DFII10. Query: "FRED DFII10 10 year TIPS real yield latest".
- 10 year nominal yield -> FRED DGS10 / H.15. Query: "10 year treasury yield today".
- US Dollar Index DXY -> query: "DXY dollar index level today trend".
- High yield credit spread OAS -> FRED BAMLH0A0HYM2. Query: "ICE BofA US high yield OAS latest bps".
- Fed funds target + next meeting bias -> query: "fed funds rate current FOMC next meeting hike cut odds".
- Core CPI and Core PCE -> query: "US core CPI latest year over year" and latest PCE.
- ISM Manufacturing PMI -> query: "ISM manufacturing PMI latest month reading".
- VIX -> query: "VIX index level today".

Per asset add:
- Crypto: BTC price vs 50 / 100 / 200 day moving averages, spot BTC ETF flows,
  whale / on chain (Glassnode, CryptoQuant). ALSO check X for sentiment / flows.
- US Stocks: S&P 500 level, trend vs resistance, P/E (valuation), breadth.
- Gold: spot gold price, trend vs 200 day SMA, safe haven / geopolitical drivers.
- US Cash: 3 month T bill yield (FRED DGS3MO), Fed funds level and bias.

## Framework: which factors move each asset, and the sign

Evaluate each asset against its key factors. A factor is 📈 (bullish for that
asset) or 📉 (bearish for that asset) based on its CURRENT direction and level.

Crypto (highest beta liquidity asset):
- Real yields: rising / high -> 📉 ; falling / low -> 📈
- Dollar (DXY): strong / rising -> 📉 ; weak / falling -> 📈
- Fed / liquidity: hawkish, hiking, tight -> 📉 ; easing, cutting -> 📈
- Credit spreads: widening -> 📉 ; tight / tightening -> 📈
- ETF flows + whales + on chain: inflows / accumulation -> 📈 ; outflows -> 📉
- Trend: below key EMAs -> 📉 ; above -> 📈

US Stocks (claim on earnings, discount rate sensitive):
- Growth (ISM PMI): above 50 and firm -> 📈 ; below 50 -> 📉
- Credit spreads: tight -> 📈 ; widening -> 📉
- Rates / 10 year: stable or falling -> 📈 ; rising fast -> 📉
- VIX: low / normal -> 📈 ; rising / elevated -> 📉
- Valuation (P/E, CAPE) and resistance: stretched / stalled -> 📉 cap

Gold (non yielding monetary asset):
- Real yields: rising / high -> 📉 ; falling / low -> 📈
- Dollar (DXY): strong -> 📉 ; weak -> 📈
- Inflation expectations / breakevens: rising -> 📈 ; falling -> 📉
- Safe haven / geopolitics: elevated risk -> 📈 ; calm -> 📉

US Cash (T bills, money market):
- Fed funds level + bias: high, held, hawkish -> 📈 ; cutting fast -> 📉
- Real yield on cash: positive -> 📈 ; negative -> 📉
- Risk backdrop: risk off, other assets below trend -> 📈 ; strong risk on -> 📉

## Decision rules (net to one word)

1. For the asset, score each key factor as +1 (📈) or -1 (📉) using the current
   readings.
2. Net sign of the dominant factors sets the verdict:
   - Net negative -> BEARISH
   - Net positive -> BULLISH
3. Add ONE qualifier in parentheses only when true:
   - "(capped)" if bullish but valuation / resistance / policy limits upside.
   - "(bottoming)" if bearish but flows / on chain show the downside is being absorbed.
4. Real yield calculations, always show steps:
   - Gold / crypto context: real 10 year yield = nominal 10 year minus 10 year
     breakeven (or read DFII10 directly).
   - Cash: real cash yield = 3 month T bill yield minus core CPI. Show e.g.
     "3.85 minus 2.6 = 1.25 percent".

## Output format (exact)

Start with one line: "As of <date/time context>. Regime: <two or three words>."
Then, for each asset in scope, output this block. Use real bullet points with a
blank line before each list. Choose the THREE most decisive factors: usually two
that confirm the verdict plus one offset (mark the offset "(offset)").

```
**<emoji> <Asset name> — <VERDICT>**

- 📈 or 📉 <Factor headline>
  - <one sentence reasoning with the live number in it>
- 📈 or 📉 <Factor headline>
  - <one sentence reasoning>
- 📈 or 📉 <Factor headline (offset)>
  - <one sentence reasoning>
```

Asset emojis: Crypto ₿, US Stocks 📊, Gold 🥇, US Cash 💵.
Verdict is ONE word: BULLISH or BEARISH, plus an optional "(capped)" or
"(bottoming)" qualifier.

End with a single "Sources:" line: markdown hyperlinks separated by commas, no
inline citations anywhere above. Include the primary series used (FRED DFII10,
FRED BAMLH0A0HYM2, Fed H.15, ISM PMI, BLS CPI) plus the price / flow reads.

## Worked example of the target output (crypto only)

**₿ Crypto — BEARISH (bottoming)**

- 📉 Real yields headwind
  - The 10 year real yield at 2.35% with the Fed pricing a possible hike keeps the discount rate high for a no cashflow asset, and BTC near $64k sits below its 50, 100 and 200 day EMAs.
- 📉 Strong dollar and risk off
  - DXY near 101 plus the US Iran escalation strengthened the safe haven dollar and capped crypto's upside.
- 📈 ETF and whale support (offset)
  - Spot BTC ETFs logged a second straight week of inflows and whales kept accumulating with MVRV near past cycle bottoms, cushioning the downside.

Sources: [FRED DFII10](https://fred.stlouisfed.org/series/DFII10), [FXStreet BTC](https://www.fxstreet.com/cryptocurrencies), [Glassnode](https://research.glassnode.com/).

## Notes

- If a data point cannot be fetched, say so briefly in that factor rather than
  guessing, and still give the verdict from the factors you have.
- Keep each reasoning sentence to one sentence with a concrete number.
- This is analysis for Turbo's own use, not financial advice; do not add a
  disclaimer unless asked.
