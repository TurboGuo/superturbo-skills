---
name: format-master
description: Formats, converts and audits citations and manuscripts in APA 7, ASA, APSA, Chicago, MLA 9, Harvard, AMA, IEEE and GB/T 7714-2015. Fixes a reference list in place, converts a whole manuscript between styles, checks that every in-text citation has a reference and every reference is cited, and applies journal-specific and 学位论文 overrides. Use when a reference list is inconsistent, when switching target journals, or before submission. Also triggers on Chinese: 参考文献格式, 改成 APA 格式, 国标格式, GB/T 7714, 引用格式不对, 参考文献怎么写, 文献格式转换, 学位论文格式, 著录格式. 用中文提问时用中文回答.
argument-hint: "format | convert <from> <to> | audit | manuscript | journal <name> [<file>]"
---

# Format Master

> Citation store and citekey convention: [../academic-master/references/workspace.md](../academic-master/references/workspace.md).


## 语言 / Language

**用户用中文提问，就全程用中文回答**，包括追问、表格标题、图表标注和写进文件的正文。
用中文学术语体直接写，不要先用英文构思再翻译。术语对照表和因果表述的中文阶梯见
[LANGUAGE.md](../../LANGUAGE.md)。这条规则优先于本文件里的其他格式约定。

Reply in the language the user wrote in. Full policy and the EN/中文 terminology
table: [LANGUAGE.md](../../LANGUAGE.md).

Formatting is mechanical, which is exactly why it should never be done by hand and never be done by memory. Work from structured data — a `.bib` or a CSL-JSON record — and generate the string. **Never retype a reference from a PDF's first page**, because that is how a wrong year enters a manuscript and survives to print.

## Modes

| Mode | Use it when |
|---|---|
| `format` | Turn library records into a formatted reference list |
| `convert` | Move a whole manuscript from one style to another |
| `audit` | Find mismatches, missing entries, orphans and malformed records |
| `manuscript` | Fix an existing document in place, in-text and list together |
| `journal` | Apply one journal's house overrides on top of a base style |

---

## The order of operations, and it matters

1. **Get the metadata right first.** A perfectly formatted wrong citation is still wrong. Resolve every DOI; the metadata that comes back from Crossref beats the metadata on the PDF.
2. **Then apply the style.** Style is a rendering of correct data, never a substitute for it.
3. **Then audit.** In-text and list must agree, both directions.

---

## Mode: format

Read from `.research/library/references.json` (CSL-JSON) or `.bib`. Render with the rules in [references/styles.md](references/styles.md) and the per-type patterns in [references/source-types.md](references/source-types.md).

**Prefer a real CSL processor when one is available** — `pandoc --citeproc` with a CSL file from the Zotero Style Repository handles 10,000+ styles correctly and handles the edge cases you will otherwise get wrong. Generate by hand only when no processor is reachable, and then check the output against the patterns file rather than against memory.

```bash
pandoc draft.md --citeproc --bibliography=references.bib \
       --csl=apa.csl -o draft.docx
```

Order the list correctly, because each style differs:

| Style | List order | Multiple works, same author |
|---|---|---|
| APA 7, ASA, Chicago author-date, GB/T author-year | Alphabetical by first author surname | Chronological, earliest first; `2019a`, `2019b` for same-year |
| IEEE, AMA, GB/T 顺序编码制 | Order of first citation | n/a, numbered |
| MLA 9 | Alphabetical | Alphabetical by title, with a 3-em dash for the repeated author |

---

## Mode: convert

Style conversion is not find-and-replace. Each style has its own rules for author count, capitalization, punctuation and what gets included at all. See the conversion trap table in [references/styles.md](references/styles.md).

Convert both halves together — the in-text citations and the reference list — or the manuscript ends up half-converted, which is worse than either style alone. The traps that catch people:

- **Numeric to author-date.** IEEE `[7]` gives you no author or year in the text; you must resolve every number to its reference and rebuild the sentence, sometimes rewording it because `[7] showed that` becomes `<Author> (<year>) showed that`.
- **Sentence case to title case.** APA and GB/T use sentence case for article titles; ASA, Chicago, MLA use headline case. Converting means recasing every title, and proper nouns must survive — "the Chinese state" recases differently from "the chinese state".
- **Author-count cut-offs differ.** APA 7 lists up to 20 and elides at 21+; ASA lists all; Chicago elides after 10 in the list; GB/T lists three then `等` or `et al.`
- **`&` versus `and`.** APA uses `&` inside parentheses and `and` in narrative text. ASA and Chicago use `and` in both.
- **Access dates.** MLA and Chicago sometimes want them; APA 7 wants them only for content likely to change.

---

## Mode: audit

Report every one of these; the first two are the ones that get caught in review:

| Check | Why it matters |
|---|---|
| In-text citation with no reference entry | The most common submission-desk rejection |
| Reference entry never cited | Padding, and reviewers notice |
| Year mismatch between in-text and list | Usually a preprint-to-published slip |
| Author name spelled differently across entries | Breaks alphabetical order and looks careless |
| Missing DOI where one exists | Resolve it; most styles now require it |
| DOI formatted as `doi:10.xxxx` | APA 7 requires `https://doi.org/10.xxxx` |
| `et al.` used in the reference list where the style forbids it | Style-specific, check the table |
| Same-year works by one author without `a`/`b` suffixes | Ambiguous in-text |
| Retracted source cited without a retraction note | Serious. Check Retraction Watch or Crossref's retraction flag |
| Preprint cited when a published version exists | Cite the published version and say so |
| Page numbers missing on a direct quotation | Required in every style, and reviewers check quotations |
| A reference that cannot be resolved at all | Flag as `[UNVERIFIED]`, never quietly keep it |

Report as a table with the location, the problem and the fix. Then offer to apply the fixes.

---

## Mode: manuscript

Fix a real document in place. Read it, list what will change **before** changing anything, and change nothing else — no rewording, no restructuring, no "improvements" to prose the user did not ask about.

For `.docx`, work on a copy and keep the original untouched. For LaTeX, prefer fixing the `.bib` and the `\bibliographystyle` over editing `.tex`. For Markdown, prefer pandoc with a CSL file.

---

## Mode: journal

Base style plus house overrides. Always ask for the journal's current author guidelines URL and read it — house rules change and a two-year-old memory of them is a liability. Common overrides in [references/journal-overrides.md](references/journal-overrides.md).

---

## Chinese: GB/T 7714-2015

Two systems, and they are not interchangeable. Ask which the target uses:

**顺序编码制** (numeric, the default for most Chinese journals):
```
[1] 作者甲, 作者乙, 作者丙. ［期刊论文篇名］[J]. ［刊名］, 2019, 35(4): 112-125.
[2] BURT R S. Structural holes: the social structure of competition[M]. Cambridge, MA: Harvard University Press, 1992.
```
（条目 1 为占位符；条目 2 是真实文献，用来演示外文著者姓全大写、名用不加点的缩写。）
In-text: `……已有研究表明[1,3-5]。`

**著者-出版年制** (author-year, used by some journals and many 学位论文):
```
作者甲, 作者乙, 作者丙. 2019. ［期刊论文篇名］[J]. ［刊名］, 35(4): 112-125.
```
In-text: `(作者甲 等, 2019)`

The document-type markers are mandatory and are the thing most often missing: `[M]` 专著, `[J]` 期刊, `[C]` 论文集, `[D]` 学位论文, `[R]` 报告, `[S]` 标准, `[P]` 专利, `[N]` 报纸, `[EB/OL]` 电子公告, `[DB/OL]` 数据库, `[J/OL]` 网络期刊. Full rules and the ordering of 中文 and 英文 entries in [references/gbt7714.md](references/gbt7714.md).

**For a 学位论文, the university template outranks GB/T.** Ask for the template first; most Chinese universities publish a 学位论文格式规范 that specifies margins, 字体, 行距 and reference format, and the 答辩 committee checks against that document, not against the national standard.

---

## Citation store integration

| Store | Read | Write |
|---|---|---|
| Local (default) | Parse `references.bib` and `references.json` | Append, deduplicate on DOI first |
| Zotero | Read the library through a Zotero MCP server | Write new items; keep Better BibTeX keys as citekeys |
| EndNote | User exports RIS; convert RIS to BibTeX | Emit RIS for the user to import back |

RIS to BibTeX and back is a lossy round trip. Warn the user which fields do not survive (typically `notes`, `tags`, and custom fields) rather than letting them find out after reimporting.

## Hard rules

1. **用中文提问就用中文回答**，全程，包括表格和图注。术语见 [LANGUAGE.md](../../LANGUAGE.md)。Reply in the language the user wrote in.
2. **Never invent metadata.** If a field is missing, resolve it or mark it missing. A guessed page range is a fabrication.
3. **Resolve the DOI before formatting.** Crossref beats the PDF's cover page.
4. **Use a CSL processor when one is available.** Hand-generation is the fallback, not the default.
5. **Convert in-text and list together, never one alone.**
6. **Say what you will change before changing a manuscript**, and change nothing else.
7. **The journal's own guidelines outrank every rule here.** So does a university 学位论文 template.
