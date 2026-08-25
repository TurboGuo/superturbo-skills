# Connectors

## The plugin runs with zero connectors

Every skill here works with no MCP server attached. Literature search falls back
to web search plus DOI resolution, the citation store falls back to local
`.bib` and CSL-JSON files, and the diagram scripts need only Python. **Nothing
in this plugin requires you to sign up for anything.**

Connectors make it better, not possible. `.mcp.json` therefore ships empty on
purpose: you add only what you want, and no third-party endpoint sees your
research question unless you put it there.

## How tool references work

Skill files use `~~category` as a placeholder for whatever you connect in that
category. `~~paper search` means OpenAlex, Semantic Scholar, PubMed or whatever
else is wired up. The skills are tool-agnostic by design.

| Category | Placeholder | What it does for you |
|---|---|---|
| Paper search | `~~paper search` | Finds and ranks literature in `academic-master hunt` |
| Citation library | `~~citation library` | Reads and writes your references |
| Full text | `~~full text` | Retrieves the PDF or HTML behind a hit |
| Citation formatting | `~~csl` | Renders any of ~10,000 CSL styles |

---

## Paper search

### Available in the Claude connector directory
Add these from your connector settings; nothing to install.

> Directory contents checked on **2026-08-25**. The directory changes without
> notice — **search it yourself before concluding a source is unavailable**.
> The verdict column below reflects the directory on the date stamped here.

| Connector | Coverage | Auth | Verdict for social science |
|---|---|---|---|
| **PubMed** | 36M+ biomedical records | none | Add it only if your work touches health, epidemiology or public health |
| **Consensus** | Curated scientific search | account | Useful for a fast evidence check, weaker for sociology and area studies |
| **alphaXiv** | arXiv full text | account | Economics preprints (econ.GN) and computational social science only |
| **bioRxiv / medRxiv** | Preprints | none | Health-adjacent only |
| **Firecrawl** | Live web plus papers | account | General-purpose fallback |

**None of these covers mainstream social science well.** The directory is
biomedical and CS heavy. For sociology, political science, education and area
studies the coverage you want is OpenAlex, Crossref and Google Scholar, and
those come from a self-hosted server.

### Self-hosted, and the one worth the effort
Install command and environment variables verified against the project's PyPI
page and repository on **2026-08-25**; re-check before pasting.

`alisoroushmd/academic-research-mcp` — MIT licensed, 25 tools across OpenAlex,
Semantic Scholar, Crossref, PubMed, arXiv, medRxiv/bioRxiv, Google Scholar,
ORCID and Unpaywall, plus a PRISMA screening-log manager. **No API keys
required**, though adding an email raises the OpenAlex rate limit tenfold.

This is the single highest-value addition for a social science researcher,
because OpenAlex plus Google Scholar plus Crossref is the coverage triangle the
directory connectors do not give you.

```json
{
  "mcpServers": {
    "academic-research": {
      "command": "uvx",
      "args": ["academic-research-mcp"],
      "env": { "OPENALEX_EMAIL": "you@example.com" }
    }
  }
}
```

Others worth knowing about: `bettyguo/paperbase-mcp` (citation graphs and
BibTeX), `MCPServings/paper-mcp` (remote HTTP, so no install), `veale/academic-mcp`
(Zotero-first with institutional Primo support).

### Chinese-language literature — the honest position
**There is no public MCP server for CNKI, 万方 or 维普.** All three are
subscription databases behind institutional authentication and none exposes an
open API. The working path:

1. Search and export from CNKI or 万方 in the browser, choosing the **RefWorks**
   or **EndNote** export format
2. Save the export file into your project
3. `format-master` converts it into `.research/library/references.bib` with
   citekeys in pinyin
4. Everything downstream then works on Chinese sources exactly as on English ones

CSSCI-indexed work is partly visible in OpenAlex and Crossref, so `hunt` will
find some of it, but treat that coverage as incomplete and supplement by hand.

---

## Citation library

### Local files — the default, no setup
`.research/library/references.bib` plus a CSL-JSON mirror. Works offline, no
account, and the files are yours. Start here.

### Zotero
Several MCP servers exist. **Which one you can use depends on where Claude is
running**, and this catches people out:

| Where you run Claude | What works |
|---|---|
| Claude Code or Claude Desktop on the same machine as Zotero | Any stdio server. Simplest: `uvx --from local-zotero-mcp zotero-mcp` (read-only, no keys, talks to the desktop app on `127.0.0.1:23119`) |
| Cowork, or claude.ai in a browser | **stdio does not reach your Mac.** The session runs in an isolated cloud VM that cannot spawn a local subprocess. You need a server that exposes HTTP with OAuth — `richardjlyon/zotero-mcp` documents exactly this setup, tunnelling the local Zotero API over an authenticated HTTPS endpoint |

Feature-complete alternative: `oscardvs/zoteus` (MIT, TypeScript, one `npx`,
CSL bibliographies in ~2,800 styles, semantic search over your own library).

When Zotero is connected, treat the Zotero library as the source of truth and
regenerate the local `.bib` from it rather than editing both.

### EndNote and Mendeley
No MCP server exists for either, and none is likely: neither exposes a local API
of the kind Zotero does. The round trip:

1. In EndNote, select the references, then `File > Export`, format **RIS**
2. Put the `.ris` file in your project
3. `format-master` converts RIS to BibTeX and CSL-JSON
4. To go back, `format-master` emits RIS for `File > Import`

The round trip is lossy — notes, custom fields and some tags do not survive.
`format-master` warns you which fields it drops rather than letting you discover
it after reimporting.

---

## Full text and access

- **Unpaywall** — legal open access PDFs, free, 100k requests a day. Bundled in
  `academic-research-mcp`.
- **Your institution's proxy** — usually the only route to JSTOR, ProQuest,
  Sage, Wiley and Taylor & Francis. No MCP server can authenticate on your
  behalf; log in through the library and download by hand.
- **Ex Libris Primo** — if your university runs it, `veale/academic-mcp` can
  query it as a search source and surface the link-resolver URL.

**Never route paywalled retrieval through a shadow library.** The plugin will
not do it and will not suggest it.

---

## Citation formatting

`pandoc --citeproc` with a CSL file from the Zotero Style Repository handles
10,000+ styles, runs locally, and needs no connector. This is what
`format-master` prefers when it is available.

```bash
pandoc draft.md --citeproc --bibliography=.research/library/references.bib \
       --csl=apa.csl -o draft.docx
```

Get `apa.csl`, `american-sociological-association.csl`, or
`china-national-standard-gb-t-7714-2015-numeric.csl` from
https://www.zotero.org/styles

---

## A note on trust

Every server listed above is third-party code. Before adding one to a project
with unpublished research in it: read what it sends over the network, check the
licence, and prefer the ones that keep your library on your own machine. A
literature search query is not sensitive; an unpublished manuscript is.
