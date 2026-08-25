# =============================================================================
# 项目：<项目名>
# 作者：<姓名>            创建：2026-08-25            最后修改：
# 说明：从原始数据到表 2 的完整流程。每个 CHECK 处停下来看一眼输出。
# 依赖：haven dplyr tidyr fixest modelsummary marginaleffects performance mice
#       survey srvyr DescTools fwildclusterboot
# =============================================================================
set.seed(20260825)

library(haven); library(dplyr); library(tidyr)
library(fixest); library(modelsummary); library(marginaleffects)

root <- "."
raw  <- file.path(root, "data/raw")
out  <- file.path(root, "output")
dir.create(out, showWarnings = FALSE, recursive = TRUE)

# -----------------------------------------------------------------------------
# 1  读入与合并
# -----------------------------------------------------------------------------
ind <- read_dta(file.path(raw, "individual.dta"))
hh  <- read_dta(file.path(raw, "household.dta"))

stopifnot(!anyDuplicated(ind[c("pid", "year")]))      # CHECK 主键唯一
n_start <- nrow(ind)

df <- ind |>
  left_join(hh, by = c("hhid", "year"), relationship = "many-to-one")

cat("合并前", n_start, "行，合并后", nrow(df), "行\n")   # CHECK 两个数应一致

# -----------------------------------------------------------------------------
# 2  变量构造
# -----------------------------------------------------------------------------
df <- df |> mutate(
  female  = as.integer(gender == 2),
  urban   = as.integer(hukou  == 1),
  # 零值多的时候用 fepois，不要 log(y+1)。见 references/stata-r.md 第 3 节
  lninc   = ifelse(income > 0, log(income), NA_real_),
  edu_std = as.numeric(scale(eduyear)),
  income_w = DescTools::Winsorize(income, probs = c(.01, .99), na.rm = TRUE)
) |>
  group_by(hhid) |>
  mutate(fa_edu_hh = max(father_edu, na.rm = TRUE)) |>
  ungroup() |>
  mutate(fa_edu_hh = ifelse(is.infinite(fa_edu_hh), NA_real_, fa_edu_hh))
  # ^ 组内全缺失时 max(na.rm=TRUE) 返回 -Inf，必须显式转回 NA

# -----------------------------------------------------------------------------
# 3  缺失值
# -----------------------------------------------------------------------------
vars <- c("lninc", "edu_std", "female", "fa_edu_hh")
colMeans(is.na(df[vars]))                              # CHECK 缺失比例
# m 至少等于缺失百分数
# imp <- mice::mice(df[vars], m = 20, seed = 20260825)
# fit <- with(imp, lm(lninc ~ fa_edu_hh + female)); summary(mice::pool(fit))

# -----------------------------------------------------------------------------
# 4  抽样权重（复杂抽样数据必做）
# -----------------------------------------------------------------------------
# des <- survey::svydesign(ids = ~psu, strata = ~strata, weights = ~weight,
#                          data = df, nest = TRUE)
# summary(survey::svyglm(lninc ~ fa_edu_hh + female, design = des))

# -----------------------------------------------------------------------------
# 5  描述统计（表 1）
# -----------------------------------------------------------------------------
datasummary_skim(df[vars], output = file.path(out, "table1.docx"))

# -----------------------------------------------------------------------------
# 6  主回归（表 2）
# -----------------------------------------------------------------------------
# 聚类在处理被分配的层次上
m1 <- feols(lninc ~ fa_edu_hh                        | prov + year, cluster = ~prov, data = df)
m2 <- feols(lninc ~ fa_edu_hh + female + age         | prov + year, cluster = ~prov, data = df)
m3 <- feols(lninc ~ fa_edu_hh + female + age + urban | prov + year, cluster = ~prov, data = df)

cat("实际回归样本：", nobs(m3), " / 数据行数：", nrow(df), "\n")  # CHECK 差额要能解释

n_clust <- dplyr::n_distinct(df$prov)
if (n_clust < 40) cat("聚类数 =", n_clust, "，小于 40，改用野聚类自助 fwildclusterboot\n")

modelsummary(
  list("模型 1" = m1, "模型 2" = m2, "模型 3" = m3),
  output = file.path(out, "table2.docx"),
  stars  = c('*' = .05, '**' = .01, '***' = .001),
  gof_map = c("nobs", "adj.r.squared"),
  coef_rename = c(fa_edu_hh = "父亲受教育年限", female = "女性",
                  age = "年龄", urban = "城镇户口"),
  title = "表 2 父亲受教育年限对个人收入的影响",
  notes = "括号内为聚类到省级的稳健标准误。省份和年份固定效应已控制。"
)

# -----------------------------------------------------------------------------
# 7  诊断
# -----------------------------------------------------------------------------
m_lm <- lm(lninc ~ fa_edu_hh + female + age + urban + factor(prov) + factor(year), data = df)
performance::check_collinearity(m_lm)
performance::check_heteroscedasticity(m_lm)
car::avPlots(m_lm, terms = ~ fa_edu_hh)                # CHECK 是不是少数点带的

# -----------------------------------------------------------------------------
# 8  稳健性
# -----------------------------------------------------------------------------
# 换缩尾后的因变量、换聚类层次、分样本
# 每一个都要说明是事前设定的还是探索性的

sessionInfo()   # 写进附录
