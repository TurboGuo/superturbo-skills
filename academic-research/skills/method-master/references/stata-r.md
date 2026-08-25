# Stata 与 R 操作手册 / Stata and R operations

从原始数据到论文里的那张表。每一节的结构是：**命令 → 它做什么 → 坑在哪**。
坑才是这份文件存在的理由，命令本身查帮助文档就有。

约定：Stata 代码块在前，R 在后，做的是同一件事。

**可直接运行的完整骨架**：`../scripts/analysis-template.do` 和
`../scripts/analysis-template.R`。两个文件走的是同一条流程，从读入到导出表 2，
每一步带一个 `CHECK` 注释标出必须自己看一眼的输出。

---

## 1. 读入与合并

```stata
* 读入
use "data/cfps2020.dta", clear
import delimited "data/raw.csv", clear varnames(1) encoding(UTF-8)
import excel "data/raw.xlsx", sheet("Sheet1") firstrow clear

* 合并：永远写清楚是几对几，永远 assert
merge 1:1 pid year using "data/income.dta", assert(match master) keep(match)
merge m:1 hhid     using "data/household.dta"
tab _merge          // 看清楚再 drop _merge

* 追加
append using "data/wave2.dta", gen(wave_src)
```

```r
library(haven); library(dplyr)
df  <- read_dta("data/cfps2020.dta")
raw <- readr::read_csv("data/raw.csv", locale = readr::locale(encoding = "UTF-8"))

df <- df |>
  left_join(income, by = c("pid", "year"), relationship = "one-to-one") |>
  left_join(household, by = "hhid", relationship = "many-to-one")
```

**坑：**

- **Stata 的 `merge m:m` 几乎永远是错的。** 它不做笛卡尔积，做的是按顺序配对，结果通常没有任何统计意义。看到自己在写 `m:m`，说明主键选错了。
- **不写 `assert()` 就是放弃检查。** 合并后样本量变大，说明主键不唯一；变小，说明匹配失败。两种都要在合并那一刻发现，不是在跑完回归之后。
- R 的 `relationship =` 参数（dplyr 1.1.0 起）是同样的作用，**默认不报错**，所以必须手写。
- 合并前先 `isid pid year` / `stopifnot(!anyDuplicated(df[c("pid","year")]))` 确认主键唯一。

---

## 2. 重塑与聚合

```stata
* 宽转长
reshape long income_ edu_, i(pid) j(year)
* 长转宽
reshape wide income edu, i(pid) j(year)

* 聚合到家庭层面
collapse (mean) income (max) edu (count) n=pid, by(hhid year)

* 面板声明，做面板分析之前必须先做
xtset pid year
xtdescribe        // 看面板平衡与否
```

```r
library(tidyr)
long <- pivot_longer(df, cols = starts_with("income_"),
                     names_to = "year", names_prefix = "income_",
                     values_to = "income")
wide <- pivot_wider(long, id_cols = pid, names_from = year, values_from = income)

hh <- df |> group_by(hhid, year) |>
  summarise(income = mean(income, na.rm = TRUE), edu = max(edu), n = n(),
            .groups = "drop")
```

**坑：**

- **`collapse` 会静默丢掉所有没进 `by()` 和统计量列表的变量。** 聚合之前先想清楚哪些变量要保留。
- **`reshape` 对变量命名极其挑剔**，`income2020` 能识别，`income_2020_adj` 不行。改名再 reshape 比跟它较劲快。
- **聚合改变了分析单位**，也就改变了标准误应该聚类的层次，还常常改变研究问题本身。见 `threats.md` 的层次谬误。

---

## 3. 变量构造

```stata
gen lninc = ln(income)                    // income = 0 会变成缺失
gen lninc = ln(income + 1)                // 常见做法，但见下面的坑
egen edu_std = std(edu)                   // 标准化
egen hh_mean = mean(income), by(hhid)     // 组内均值
egen occ_grp  = group(occupation)         // 字符串转数值分组
recode age (0/17=1)(18/34=2)(35/59=3)(60/max=4), gen(agegrp)
ssc install winsor2
winsor2 income, cuts(1 99) replace        // 缩尾

destring income, replace force            // force 会把非数字变缺失，先看清楚
encode province, gen(prov_id)             // 字符串转带标签的数值
label define agegrp 1 "未成年" 2 "青年" 3 "中年" 4 "老年"
label values agegrp agegrp
```

```r
df <- df |> mutate(
  lninc   = log(income),
  edu_std = as.numeric(scale(edu)),
  agegrp  = case_when(age < 18 ~ "未成年", age < 35 ~ "青年",
                      age < 60 ~ "中年", TRUE ~ "老年"),
  across(c(income, wealth), ~ DescTools::Winsorize(.x, probs = c(.01, .99),
                                                  na.rm = TRUE))
) |> group_by(hhid) |> mutate(hh_mean = mean(income, na.rm = TRUE)) |> ungroup()
```

**坑：**

- **`ln(income + 1)` 不是中性的。** 加 1 这个常数会改变估计出来的弹性，而且结果对加多少敏感。零值多的时候用 Poisson 伪极大似然（`ppmlhdfe` / `fixest::fepois`）而不是 `log(y+1)`，这在收入研究里已经是主流意见。
- **`egen ... , by()` 在有缺失时不会警告**，组内全缺失会得到缺失，容易被后面的回归静默丢样本。
- **Stata 的缺失值 `.` 大于任何数字。** `gen old = age > 60` 会把缺失的人也算成老年人。永远写 `gen old = age > 60 if !missing(age)`。
- R 里 `scale()` 返回矩阵，不套 `as.numeric()` 会在后面报奇怪的错。

---

## 4. 缺失值

```stata
* 先看清楚缺失长什么样
misstable summarize
misstable patterns

* 链式方程多重插补
mi set flong
mi register imputed income edu
mi register regular age female
mi impute chained (regress) income (ologit) edu = age female, add(20) rseed(20260825)
mi estimate, post: regress lninc edu age female
```

```r
library(mice)
md.pattern(df)
imp <- mice(df, m = 20, method = c(income = "pmm", edu = "polr"), seed = 20260825)
fit <- with(imp, lm(lninc ~ edu + age + female))
summary(pool(fit))
```

**坑：**

- **插补次数 m 的经验法则：m 至少等于缺失比例的百分数。** 缺 30% 就 m = 30，不是默认的 5。
- **因变量要不要插补是个真问题。** 主流建议是插补时把 Y 放进模型（提高插补质量），但分析时用 Y 观测到的样本（MI then delete）。不要插补 Y 然后当真实数据用。
- **插补模型必须比分析模型更宽**：分析里有交互项，插补模型也要有，否则交互效应会被系统性压平。
- **`mi estimate` 之外的命令基本都不认 mi 数据。** 想画图、做事后检验，先 `mi extract 1` 或换思路。
- **列表删除（listwise）不是中立选项**，它假设完全随机缺失。用了就要在方法部分说，并且报告删掉了多少。

---

## 5. 抽样权重与复杂抽样

CGSS、CFPS、CHIP、PSID、NLSY 全都是复杂抽样，不设计声明就直接跑回归，标准误是错的。

```stata
svyset psu [pweight=weight], strata(strata) singleunit(centered)
svy: regress lninc edu age female
svy: tab edu, col ci
estat effects        // 设计效应

* 只想要加权点估计、不想要设计校正的标准误
regress lninc edu age [pw=weight], vce(robust)
```

```r
library(survey)
des <- svydesign(ids = ~psu, strata = ~strata, weights = ~weight,
                 data = df, nest = TRUE)
svyglm(lninc ~ edu + age + female, design = des) |> summary()

# tidyverse 写法
library(srvyr)
df |> as_survey_design(ids = psu, strata = strata, weights = weight) |>
  group_by(agegrp) |> summarise(inc = survey_mean(income, vartype = "ci"))
```

**坑：**

- **`[pw=]` 和 `svy:` 不是一回事。** 前者只加权点估计，后者还校正分层和聚类带来的方差。审稿人问「有没有考虑复杂抽样设计」，问的是后者。
- **权重要不要用，取决于估计目标。** 描述总体分布要用；估计一个结构参数时，加权与否会改变估计量的含义，而且如果模型设定正确，不加权更有效率。这一点要在方法部分交代，不能默认加权就是更严谨。
- **单个 PSU 的层会让 Stata 直接报错**，`singleunit(centered)` 是常用的处理，但要在脚注说明。
- R 的 `svydesign` 忘了 `nest = TRUE` 会把不同层里同编号的 PSU 当成同一个。

---

## 6. 回归与聚类标准误

```stata
* 基础
regress lninc edu age i.female i.province, vce(cluster hhid)

* 高维固定效应
ssc install reghdfe
reghdfe lninc edu age, absorb(province year) vce(cluster province)

* 面板
xtreg lninc edu age, fe vce(cluster pid)
xtreg lninc edu age, re
hausman fe re                     // 参考，不是判决

* 非线性模型：系数不是效应，一定要 margins
logit employed edu age i.female
margins, dydx(edu)                // 平均边际效应
margins female, at(edu=(0(4)16))
marginsplot, recast(line) recastci(rarea)

* 聚类数很少（< 40）
ssc install boottest
regress y x, cluster(state)
boottest x, reps(9999)
```

```r
library(fixest); library(marginaleffects)
feols(lninc ~ edu + age + i(female) | province + year, cluster = ~province, data = df)
feglm(employed ~ edu + age + female, family = binomial, data = df) |>
  avg_slopes(variables = "edu")
plot_predictions(m, condition = c("edu", "female"))

library(fwildclusterboot)
boottest(felm_model, param = "x", clustid = "state", B = 9999)
```

**坑：**

- **聚类在处理变量被分配的层次上。** 政策在省一级实施，就聚类到省，不是到个人。聚错层次会把标准误压小一个数量级。
- **聚类数少于约 40 时，聚类稳健标准误本身是有偏的**，用野聚类自助（`boottest` / `fwildclusterboot`），不要靠增加控制变量掩盖。
- **`logit` 的系数不能横向比较，也不能跨模型比较。** 加了一个控制变量之后系数变化，可能只是尺度变了，不是效应变了。永远报边际效应或预测概率。见 KHB 分解。
- **`hausman` 不是选 FE 还是 RE 的判决书。** 它检验的是 RE 的正交假设，样本大的时候几乎必然拒绝。选择应该由研究问题决定：想要组内变异就 FE。
- **交错处理的双重差分不要用 `reghdfe` 直接跑**，见 `causal-identification.md`。

---

## 7. 诊断

```stata
regress lninc edu age female
estat hettest          // 异方差 Breusch-Pagan
estat imtest, white
estat vif              // 共线性，VIF > 10 值得看，但不是硬门槛
estat ovtest           // 遗漏变量形式（Ramsey RESET）
linktest               // 模型设定
predict r, resid
predict lev, leverage
lvr2plot               // 杠杆值对残差平方
avplot edu             // 偏回归图，看单个变量是不是被少数点带的
```

```r
library(performance)
check_model(m)                    // 一次出六张诊断图
check_collinearity(m); check_heteroscedasticity(m); check_outliers(m)
car::avPlots(m)
```

**坑：**

- **共线性不是错误。** VIF 高只说明这个系数估不准，不影响其他系数，也不影响预测。为了降 VIF 删掉一个理论上必要的变量，是拿偏误换方差，通常不划算。
- **异方差在社会科学里是常态**，直接用稳健标准误，不用先检验再决定。检验的意义只在于要不要报告。
- **诊断图看的是有没有少数几个点在带整个结果。** `avplot` 上一个孤零零的点撑起整条线，比任何检验统计量都说明问题。

---

## 8. 导出结果表

这是把分析变成论文的那一步，也是最容易手工出错的一步。**不要手抄系数。**

```stata
ssc install estout
eststo clear
eststo m1: reghdfe lninc edu,            absorb(prov year) vce(cluster prov)
eststo m2: reghdfe lninc edu age female, absorb(prov year) vce(cluster prov)
esttab m1 m2 using "output/table2.rtf", replace ///
    b(3) se(3) star(* 0.05 ** 0.01 *** 0.001) ///
    stats(N r2_a, labels("观测数" "调整 R²") fmt(0 3)) ///
    label nogaps compress ///
    title("表 2 家庭背景对个人收入的影响") ///
    addnotes("括号内为聚类到省级的稳健标准误。")

* 描述统计
estpost summarize lninc edu age female
esttab using "output/table1.rtf", cells("mean(fmt(2)) sd(fmt(2)) min max") replace

* 直接写进 Word / Excel
putdocx begin
putdocx table t1 = etable
putdocx save "output/tables.docx", replace
putexcel set "output/results.xlsx", modify
```

```r
library(modelsummary)
models <- list("模型 1" = m1, "模型 2" = m2)
modelsummary(models, output = "output/table2.docx",
             stars = c('*' = .05, '**' = .01, '***' = .001),
             gof_map = c("nobs", "adj.r.squared"),
             coef_rename = c(edu = "受教育年限", age = "年龄"),
             notes = "括号内为聚类到省级的稳健标准误。")

datasummary_skim(df, output = "output/table1.docx")     # 描述统计
```

**坑：**

- **星号规则按学科不同。** 经济学常用 `* .10  ** .05  *** .01`；心理学和社会学多用 `* .05  ** .01  *** .001`。用错会被一眼看出不是本行的人。**中文期刊多数跟经济学惯例**，投稿前翻一期近刊确认。
- **`.10` 那颗星是有争议的。** 报了就等于承认在 p = 0.09 上做文章，很多社会学期刊已经不接受。
- **`stargazer` 已经很久没有大更新**，不支持 `fixest`、`lme4` 的新对象。新项目用 `modelsummary`。
- **导出到 `.rtf` 而不是 `.tex`**，除非确定用 LaTeX。中文排版下 `.rtf` 或 `.docx` 省事得多。
- 表格里的变量名要用中文标签，`label variable edu "受教育年限"` 应该在数据准备阶段就做好，不是在导表时临时改。

---

## 9. 可复现

```stata
version 18                          // 锁定语法版本
set seed 20260825
clear all
set more off
log using "logs/analysis_20260825.log", replace text
* ... 分析 ...
log close
```

```r
set.seed(20260825)
renv::init()        # 锁定包版本
renv::snapshot()
sessionInfo()       # 写进附录
```

**坑：**

- **`set seed` 要写在 do-file 开头，不是在需要随机的那一行之前。** 前面任何一个用到随机的命令都会推进随机数状态。
- **`ssc install` 的包没有版本锁定。** Stata 这边只能在方法部分写清楚用的是哪个包、哪一年装的。R 用 `renv`。
- **不要用 `cd` 写绝对路径。** 用相对路径，或者在 do-file 顶部设一个 `global root`，换一台机器只改一行。

---

## 10. 常见错误速查

| 症状 | 多半是 |
|---|---|
| 合并后样本量变多 | 主键不唯一，`m:m` 或 join 复制了行 |
| 回归样本量比预期少很多 | 某个控制变量缺失严重，`e(sample)` 看清楚 |
| 系数大得离谱 | 单位没统一，或者忘了取对数，或者被极端值带的 |
| 加了控制变量系数翻倍 | 可能控制了对撞因子，先画 DAG（`theory-graph-master dag`） |
| 标准误小得可疑 | 聚类层次错了 |
| logit 系数在两个模型间不可比 | 尺度问题，用边际效应 |
| 交互项不显著就说没有调节 | 检验功效不足，交互项要约四倍样本，见 `power.md` |
| 结果对样本区间敏感 | 报告设定曲线（specification curve），不要挑一个报 |
