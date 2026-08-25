# 语言规则 / Language policy

**这条规则优先于每个技能里的其他所有格式约定。**
This rule outranks every other formatting convention in every skill.

## 一条规则 / The one rule

**用户用什么语言提问，就用什么语言回答。**
Reply in the language the user wrote in. Chinese in, Chinese out. English in,
English out. 中英混杂的提问，按主导语言回答，除非用户另有说明。

这适用于：对话、追问、报告、表格标题、图表标注、文件里写的正文。
This covers conversation, clarifying questions, reports, table headers, figure
labels, and the prose written into files.

**不要先用英文想好再翻译。** 直接用中文学术语体写。翻译腔是审稿人一眼就能看出来的
问题，见 `literature-review-master/references/anti-patterns.md` 第 12 条。

## 三个例外 / Three exceptions

1. **引文格式不跟着语言走，跟着期刊走。** 用户用中文提问但投稿 APA 期刊，参考文献
   就是 APA。见 [format-master](skills/format-master/SKILL.md)。
2. **代码、变量名、文件名保持英文。** Stata 和 R 的注释可以用中文。
3. **专有名词、方法名、统计量第一次出现时中英并列**，之后用中文：
   「双重差分（difference-in-differences, DiD）」，之后写「双重差分」。

## 中文提问时会触发的技能 / Chinese triggers

| 用户可能说 | 触发 |
|---|---|
| 帮我找文献、查一下相关研究、有哪些人做过 | `academic-master hunt` |
| 我有个想法、这个选题行不行、帮我想想 | `academic-master discuss` |
| 了解我的研究偏好、记住我的方向 | `academic-master calibrate` |
| 写文献综述、综述怎么写、国内外研究现状 | `literature-review-master` |
| 用什么方法、研究设计、样本量、要多少人 | `method-master` |
| 画个理论模型、概念框架、变量关系图、因果图 | `theory-graph-master` |
| 参考文献格式、改成 APA、GB/T 7714、格式不对 | `format-master` |
| 结论怎么写、讨论部分、这个结果说明什么、贡献是什么 | `insight-master` |

## 学术术语对照 / Terminology

用中文输出时使用左列，不要自己造词。
When writing in Chinese use the left column; do not coin new terms.

### 变量与设计
| 中文 | English |
|---|---|
| 自变量 / 因变量 | independent / dependent variable |
| 中介变量 | mediator |
| 调节变量 | moderator |
| 控制变量 | control variable |
| 混淆变量 / 混杂因素 | confounder |
| 对撞因子 | collider |
| 内生性 | endogeneity |
| 遗漏变量偏误 | omitted variable bias |
| 反向因果 | reverse causality |
| 选择性偏误 | selection bias |
| 分析层次 / 分析单位 | level / unit of analysis |
| 边界条件 | boundary condition |
| 作用机制 | mechanism |

### 方法
| 中文 | English |
|---|---|
| 随机对照实验 | randomized controlled trial |
| 准实验 | quasi-experiment |
| 双重差分 | difference-in-differences (DiD) |
| 断点回归 | regression discontinuity (RDD) |
| 工具变量 | instrumental variable (IV) |
| 倾向得分匹配 | propensity score matching (PSM) |
| 合成控制法 | synthetic control |
| 固定效应模型 | fixed effects model |
| 多层线性模型 / 分层线性模型 | multilevel / hierarchical linear model |
| 结构方程模型 | structural equation modeling (SEM) |
| 验证性因子分析 | confirmatory factor analysis (CFA) |
| 扎根理论 | grounded theory |
| 主题分析 | thematic analysis |
| 内容分析 | content analysis |
| 个案研究 / 案例研究 | case study |
| 民族志 | ethnography |
| 过程追踪 | process tracing |
| 混合方法 | mixed methods |
| 德尔菲法 | Delphi method |
| 定性比较分析 | qualitative comparative analysis (QCA) |
| 元分析 / 荟萃分析 | meta-analysis |
| 系统性文献综述 | systematic review |
| 理论抽样 | theoretical sampling |
| 理论饱和 | theoretical saturation |

### 测量与检验
| 中文 | English |
|---|---|
| 信度 | reliability |
| 效度 | validity |
| 内部效度 / 外部效度 | internal / external validity |
| 构念效度 | construct validity |
| 聚合效度 / 区分效度 | convergent / discriminant validity |
| 共同方法偏差 | common method variance (CMV) |
| 编码者间一致性 | inter-coder reliability |
| 稳健性检验 | robustness check |
| 安慰剂检验 | placebo test |
| 平行趋势假设 | parallel trends assumption |
| 效应量 | effect size |
| 统计功效 | statistical power |
| 置信区间 | confidence interval |
| 显著性水平 | significance level |
| 边际效应 | marginal effect |
| 中介效应 / 调节效应 | mediation / moderation effect |

### 写作
| 中文 | English |
|---|---|
| 文献综述 | literature review |
| 研究现状 | state of the research |
| 研究述评 | critical appraisal of the literature |
| 研究缺口 | research gap |
| 理论贡献 | theoretical contribution |
| 实践启示 | practical implications |
| 研究局限 | limitations |
| 未来研究方向 | future research |
| 研究设计 | research design |
| 摘要 / 关键词 | abstract / keywords |
| 学位论文 | thesis or dissertation |
| 开题报告 | research proposal |
| 参考文献 | references |

## 因果表述的中文对应 / The causal ladder in Chinese

[insight-master 的语言阶梯](skills/insight-master/references/language-ladder.md)
在中文里同样适用，而且中文更容易滑上去，因为「影响」在日常中文里比 "affect"
更弱、在学术中文里却被读作因果。

| 设计 | 可以说 | 不可以说 |
|---|---|---|
| 横截面调查 | 相关、存在关联、与……正相关、可以预测 | 影响、导致、促进、提升、造成、驱动 |
| 面板固定效应 | 在个体内部与……相关 | 导致（除非处理了时变混淆） |
| 匹配 / 加权 | 在可观测变量控制下相关 | 导致（除非做了敏感性分析） |
| 可信的 DiD / RDD / IV | 导致、使……提高、使……下降（限定于该估计量） | 把局部处理效应推广到总体 |
| 随机实验 | 导致 | 推广到研究人群和情境之外 |
| 质性研究 | 受访者描述、该案例显示、在此情境中 | 大多数、百分之多少、普遍存在 |

**「影响」是因果动词。** 中文论文里最常见的越界就是横截面数据配上「显著影响」。
如果设计支持因果，就写「导致」；不支持，就写「相关」。
