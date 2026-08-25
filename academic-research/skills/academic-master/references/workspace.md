# The research workspace

Every skill in this plugin reads and writes one directory, created in the user's
project root on first use. This is what makes the six skills act like one
research partner instead of six unrelated tools.

```
.research/
  profile.md                 the researcher preference profile (academic-master owns it)
  library/
    references.bib           BibTeX, the default citation store
    references.json          CSL-JSON mirror, used by format-master for style conversion
    notes/<citekey>.md       one reading note per source
  projects/<slug>/
    idea.md                  the idea memo
    hunt-<YYYY-MM-DD>.md     scored search results
    matrix.csv               the synthesis matrix
    screening.csv            PRISMA screening log, systematic reviews only
    design.md                the method plan
    figures/                 theory diagrams, DAGs, PRISMA flow
    draft/                   review and manuscript sections
    insights.md              findings to contribution
```

## Rules for every skill

- **No invented citations anywhere, including in examples.** Worked examples use
  bracketed placeholders (`[Source A]`, `［文献甲］`, `<Author> (<year>)`), never
  a plausible-looking surname and year. A fabricated example citation is the one
  a reader copies, and a real author attached to a finding they never made is
  harder to catch than a paper that does not exist. The only real citations that
  belong in this plugin are genuine method sources and the verified record in
  `format-master/references/styles.md`.


- **Ask before creating.** On first use, tell the user the directory is being
  created and where. Never write outside the project root.
- **Never overwrite a user's file silently.** If a target exists, diff and ask.
- **Absolute dates only.** "Updated 2026-08-25", never "updated last week".
- **Write files in the working language.** Profile field 11 sets the default, but
  a turn asked in Chinese produces Chinese prose in the file it writes. See
  [../../../LANGUAGE.md](../../../LANGUAGE.md).
- **The library is append-only in practice.** Deduplicate on DOI first, then on
  normalized title with a Jaccard similarity of 0.85 or higher, then ask.

## Citation store options

The default is local files, so the plugin runs with no external tool at all.

| Store | How it is used | Set by |
|---|---|---|
| Local (default) | `library/references.bib` plus a CSL-JSON mirror | Nothing to configure |
| Zotero | Read the library, write new items, keep Better BibTeX keys as citekeys | A Zotero MCP server, see CONNECTORS.md |
| EndNote | No live connection exists. Export RIS from EndNote, the plugin converts to BibTeX, and exports RIS back for reimport | Manual, documented in CONNECTORS.md |

When Zotero is connected, the local `.bib` becomes a **mirror, not the source of
truth** — regenerate it from Zotero rather than editing it, or the two drift.

## Citekey convention

`lastname_firstsignificantword_year`, lowercase ASCII, disambiguated with a
letter suffix: `chen_broker_2023`, `chen_broker_2023a`. For Chinese-language
sources use pinyin without tones: `zhangwei_shehui_2021`.
