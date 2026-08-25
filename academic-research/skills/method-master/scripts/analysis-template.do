*==============================================================================
* 项目：<项目名>
* 作者：<姓名>            创建：2026-08-25            最后修改：
* 说明：从原始数据到表 2 的完整流程。每个 CHECK 处停下来看一眼输出。
* 依赖：reghdfe estout winsor2 boottest   (ssc install <name>)
*==============================================================================
version 18
clear all
set more off
set seed 20260825

* 只改这一行就能换机器
global root "."
global raw  "$root/data/raw"
global work "$root/data/work"
global out  "$root/output"
cap mkdir "$work"
cap mkdir "$out"

log using "$root/logs/analysis_`c(current_date)'.log", replace text

*------------------------------------------------------------------------------
* 1  读入与合并
*------------------------------------------------------------------------------
use "$raw/individual.dta", clear
isid pid year                                   // CHECK 主键唯一，不唯一直接报错

count
local n_start = r(N)

merge m:1 hhid year using "$raw/household.dta", ///
      assert(match master) keep(match master) gen(_m_hh)
tab _m_hh                                       // CHECK 匹配情况
drop _m_hh

count
di "合并前 `n_start' 行，合并后 " r(N) " 行"     // CHECK 两个数应该一致

*------------------------------------------------------------------------------
* 2  变量构造
*------------------------------------------------------------------------------
* 注意 Stata 的缺失值大于任何数字，所有比较都要排除缺失
gen byte female = (gender == 2) if !missing(gender)
gen byte urban  = (hukou  == 1) if !missing(hukou)

* 收入：零值多的时候用 ppmlhdfe，不要 log(y+1)。见 references/stata-r.md 第 3 节
gen lninc = ln(income) if income > 0

egen edu_std   = std(eduyear)
egen fa_edu_hh = max(father_edu), by(hhid)

winsor2 income, cuts(1 99) suffix(_w)

label variable lninc      "收入对数"
label variable edu_std    "受教育年限（标准化）"
label variable female     "女性"
label variable fa_edu_hh  "父亲受教育年限"

*------------------------------------------------------------------------------
* 3  缺失值
*------------------------------------------------------------------------------
misstable summarize lninc edu_std female fa_edu_hh   // CHECK 缺失比例
* m 至少等于缺失百分数。缺 20% 就 add(20)，不是默认的 5
* mi set flong
* mi register imputed fa_edu_hh
* mi register regular female age
* mi impute chained (regress) fa_edu_hh = female age, add(20) rseed(20260825)

*------------------------------------------------------------------------------
* 4  抽样权重（复杂抽样数据必做）
*------------------------------------------------------------------------------
* svyset psu [pweight=weight], strata(strata) singleunit(centered)
* svy: regress lninc edu_std female

*------------------------------------------------------------------------------
* 5  描述统计（表 1）
*------------------------------------------------------------------------------
eststo clear
estpost summarize lninc edu_std female fa_edu_hh, detail
esttab using "$out/table1.rtf", replace ///
    cells("mean(fmt(2)) sd(fmt(2)) min(fmt(2)) max(fmt(2)) count(fmt(0))") ///
    label nomtitle nonumber title("表 1 变量描述统计")

*------------------------------------------------------------------------------
* 6  主回归（表 2）
*------------------------------------------------------------------------------
* 聚类在处理被分配的层次上。这里假设是省
eststo clear
eststo m1: reghdfe lninc fa_edu_hh,                       absorb(prov year) vce(cluster prov)
eststo m2: reghdfe lninc fa_edu_hh female age,            absorb(prov year) vce(cluster prov)
eststo m3: reghdfe lninc fa_edu_hh female age urban,      absorb(prov year) vce(cluster prov)

* CHECK 实际回归样本，和数据行数通常不一样，差额要能解释
di e(N)
count if e(sample)

* 聚类数少于 40 就用野聚类自助
qui tab prov
if r(r) < 40 {
    di "聚类数 = " r(r) "，小于 40，改用野聚类自助"
    * boottest fa_edu_hh, reps(9999)
}

esttab m1 m2 m3 using "$out/table2.rtf", replace ///
    b(3) se(3) star(* 0.05 ** 0.01 *** 0.001) ///
    stats(N r2_a, labels("观测数" "调整 R²") fmt(0 3)) ///
    label nogaps compress ///
    title("表 2 父亲受教育年限对个人收入的影响") ///
    addnotes("括号内为聚类到省级的稳健标准误。省份和年份固定效应已控制。")

*------------------------------------------------------------------------------
* 7  诊断
*------------------------------------------------------------------------------
qui regress lninc fa_edu_hh female age urban i.prov i.year
estat hettest
estat vif
avplot fa_edu_hh, name(av_faedu, replace)      // CHECK 是不是少数点带的
graph export "$out/diag_avplot.pdf", replace

*------------------------------------------------------------------------------
* 8  稳健性
*------------------------------------------------------------------------------
* 换缩尾后的因变量
* 换聚类层次
* 分样本
* 每一个都要说明是事前设定的还是探索性的

log close
