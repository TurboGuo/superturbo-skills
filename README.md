# 🚀 superturbo-skills

Turbo's personal skill library for Claude. 🧩 Each skill lives in its own folder at the root of this repo, right alongside this README — **there is no wrapper `skills/` folder**. To install a skill, just point Claude at its folder (each contains a `SKILL.md` plus any templates or assets it needs). ✨

## 📚 Skills

### 💰 fi-tracker
Renders Turbo's financial independence (FI) dashboard: a progress card, an assets-over-time table where each cell shows total assets plus how many years that pile sustains, and a single asset-growth line chart where color encodes return rate and line style encodes saving level.
- 🗣️ **Triggers:** "fi tracker", "FI dashboard", "when can I retire", "years to financial independence"
- 🌏 Replies in Chinese when the request is in Chinese.

### 🏦 fomc-short-analysis-plain
Plain-text-only variant of Turbo's short FOMC note — no visualization or rendered widgets, so it works inside Claude and on general gateways like Telegram and Slack. Leads with a **📈 POTENTIAL HIKE** or **📉 POTENTIAL CUT** verdict, two one-sentence reasons backed by official Fed sources, and exactly three institutions each tagged with their tendency and cited to the bank's own research site.
- 🗣️ **Triggers:** "fomc plain", "fomc analysis", "analyze the last fomc", "fomc preview", or a named meeting date

### 🌐 macro-dashboard
The visual counterpart to `macro-impact`: builds a self-contained two-tab HTML dashboard answering whether the **current** macro environment is bullish or bearish for US stocks, US cash, gold, and crypto. Pulls live data fresh from official sources, scores every asset against a fixed factor matrix, computes net scores at render time so the verdict can never disagree with the matrix, and publishes a dated artifact each run.
- 🗣️ **Triggers:** "macro dashboard", "宏观仪表盘", "宏观影响看板", "给我宏观分析", "宏观怎么看"
- 🌏 A Chinese request renders the **entire page** in Chinese — copy, labels, tooltips, charts, and disclaimer — not just the analysis.
- 🧪 `scripts/build.py` validates before writing (matrix width, cell values, source pairs, verdict/score agreement, the no-hyphen rule) and `scripts/verify.py` screenshots both tabs in both themes.
- 🔎 Uses Exa for search and cross-checks X for crypto flows and sentiment.

### 📊 macro-impact
Text-only read on whether the current macro environment is bullish or bearish for Turbo's four asset classes — crypto, US stocks, gold, and US cash. Ask about all four or just one. For each asset it returns a one-word verdict, three 📈/📉-tagged factors with a one-sentence reasoning each, and sources linked only at the end. Pulls live data fresh, prefers official/primary sources (Fed, FRED, Treasury, BLS, BEA, ISM, Cboe), and shows the real-yield math.
- 🗣️ **Triggers:** "macro impact", "macro read", "is macro bullish or bearish", "how is macro affecting my assets", "macro on crypto / stocks / gold / cash"
- 🔎 Uses Exa for search and cross-checks X for crypto sentiment and flows.

### 📰 news-and-knowledge-base-assistant
Builds a curated daily news brief across your chosen topics, renders an inline reading widget with text highlighting and comment notes, and files highlighted items into atomic topic notes in your knowledge base.
- 🗣️ **Triggers:** "daily news", "today's news", "morning brief", "news brief", or a fresh morning chat with no specific task
- 📦 Ships with a reader template and configurable source list.

### 🎓 academic-research
A social-science research partner shipped as a **plugin bundle of six skills** sharing one `.research/` workspace: `academic-master` (learns your research profile, then hunts literature scored against it), `literature-review-master`, `method-master` (design choice, power arithmetic, Stata/R operations manual), `theory-graph-master` (frameworks, causal DAGs, SEM paths, PRISMA), `format-master` (APA 7 / ASA / Chicago / MLA 9 / Harvard / AMA / IEEE / GB-T 7714-2015), and `insight-master` (result → finding → contribution, with a causal-language ladder that blocks overclaiming).
- 🗣️ **Triggers:** "帮我找一下关于……的文献", "写文献综述", "该用什么研究方法", "画个理论模型图", "参考文献格式", "literature review", "which method should I use", "format my references"
- 📦 Unlike the other entries this folder is a **plugin**, so it keeps its own `.claude-plugin/plugin.json` and internal `skills/` layout — install with `claude plugins add academic-research` or drop it into `.claude/plugins/`.
- 🌏 Fully bilingual: Chinese questions trigger Chinese phrasing and answer in 学术语体, covering 述+评 review conventions, GB/T 7714-2015, and 学位论文 template rules.
- ⚖️ PolyForm Noncommercial 1.0.0 — free for your own theses, papers, teaching and any university or public research body; see `academic-research/COMMERCIAL.md`.

### 🧭 ai-tool-guideline
Builds a beginner pitfall manual for one named AI tool, delivered as a markdown file the client can keep. Asks which tool, which operating system, how far they want to get and where they are stuck, then researches the official site and docs plus the official community and public experience posts, and writes the traps nobody warns a first-time user about — as a staged journey with a concrete pass check before each next step. Every trap carries a source, an evidence level, the version it applies to and the date collected, so the manual can be re-dated instead of quietly going stale. Also appends a new trap to a manual the client already has.
- 🗣️ **Triggers:** "help me get started with X", "what should I watch out for with X", "I keep getting stuck installing X", "写一份 X 的避坑手册", "X 有哪些坑", "小白怎么用 X"
- 🌏 Writes the manual in whichever language the client asked in, while always researching Chinese *and* English sources.
- 🚫 Not for choosing *which* tool to use (that's `ai-tool-search`) or vetting a third-party skill or connector before install (that's `install-safety-check`).
- ⚖️ PolyForm Noncommercial 1.0.0 — free for personal and non-commercial use; see `ai-tool-guideline/COMMERCIAL.md`.

### ✍️ turbo-x-writer
Turns raw material (insights, transcripts, research findings, on-chain data, AI workflow notes) into a ready-to-post X package: one final post, the matching image-generation prompt in Turbo's editorial vintage style, a reply, and a pre-flight QC checklist against the algorithm landmines. Built on Turbo's locked 90-day beat of AI-enhanced crypto research and agent deployment.
- 🗣️ **Triggers:** "write me an X post", "draft a tweet", "turn this into a thread", "Data Drop", "Crypto AI Stack"

### 🐦 x-writer
Analyzes any user's X/Twitter writing style and generates draft posts that sound like them. Shareable and generic (not tied to Turbo's voice).
- 🗣️ **Triggers:** "draft tweets for me", "write posts in my style", "ghostwrite", "tweet ideas", "x writer"
- 🔑 Requires a Bearer Token and X handle set in the skill config before use.

### 📈 x-growth-dashboard-public
Turns any X (Twitter) account's own analytics exports into a single-file HTML diagnostic board: three externally benchmarked scores out of 100, a follower curve with follows-per-post, 3–5 overall suggestions, and a post-by-post explanation from two angles — what the published ranking algorithm did, and what a professional would change. Runs fully offline on Python 3; the rendered HTML makes no network calls.
- 🗣️ **Triggers:** "why is my X account not growing", "X growth audit", "X analytics report", "post by post review", or uploading `account_analytics_content` / `account_overview_analytics` CSVs
- 📥 Needs the two CSV exports from [analytics.x.com](https://analytics.x.com) plus your current follower count. A connected X API tool is optional enrichment, never a substitute.
- 🧪 Ships synthetic example data in `assets/example/` for a smoke test before you feed it real numbers.

### 📕 xiaohongshu-growth-dashboard-public
The Xiaohongshu (小红书) counterpart: turns the creator-backend「笔记列表明细表」export into a single-file Chinese HTML 涨粉诊断看板 — three 100-point scores, a follower curve, per-note diagnosis from both the recommendation algorithm's angle and a working creator's, and 3–5 executable next actions. Covers and profile screenshots are optional inputs that unlock cover/conversion analysis.
- 🗣️ **Triggers:** 「小红书涨粉分析」「笔记复盘」「为什么不涨粉」「小红书数据诊断」「账号数据看板」, or uploading a 笔记列表明细表 export
- 🌏 Chinese-first output. No account authorization, API key, or connector required.
- 🔎 `scripts/discover.py` finds exports in a folder by header row, so renamed or duplicated files still resolve.

### 🍗 crazy-thursday-joke
Searches and sends a currently-trending "疯狂星期四" (KFC Crazy Thursday / V我50) joke to remind Turbo it's Thursday and time to grab KFC. Also fires when Turbo asks what day it is — if today happens to be Thursday, it answers with a joke instead of a plain date.
- 🗣️ **Triggers:** "疯四段子", "疯狂星期四", "来个疯四", "crazy thursday", "今天星期几"
- 🌏 Chinese-first; uses WebSearch to pull a fresh joke each time and always cites the source.

---

🛠️ Built by Turbo.
