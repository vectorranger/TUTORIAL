# EHR Preprocessing Tutorial — Updated Comprehensive Review Report (v2)

**Date:** 2026-03-09
**Scope:** Deep-dive cell-by-cell review of all notebooks, cross-referenced against the original `final_report.md` and CLAUDE.md compliance rules.

---

## Changes from Report v1

This report confirms all findings from v1 and adds **23 new issues** not previously identified. Key new findings include:
- A **semantic mismatch** in NLP vs codified count matrices (Cohort Creation)
- Multiple **for-loop violations** in Getting Started and Code Rollup
- Missing **post-output explanations** in Getting Started
- Combined-operation cells in NLP notebook
- Missing **df.shape** prints in NLP and Cohort Creation

---

## Table of Contents

1. [Pipeline Overview](#1-pipeline-overview)
2. [Critical Bugs (All Fixed — from v1)](#2-critical-bugs-all-fixed)
3. [NEW Issues Found in v2](#3-new-issues-found-in-v2)
4. [Notebook-by-Notebook Findings](#4-notebook-by-notebook-findings)
5. [Cross-Notebook Consistency Issues](#5-cross-notebook-consistency-issues)
6. [CLAUDE.md Compliance Gaps](#6-claudemd-compliance-gaps)
7. [Actionable Fix List](#7-actionable-fix-list)

---

## 1. Pipeline Overview

| # | Notebook | Purpose |
|---|----------|---------|
| 0 | Environment Setup | Workspace creation, Python env, MIMIC-IV download |
| 0.5 | Getting Started | Data exploration, summary statistics, word clouds |
| 1 | Data Cleaning | Missingness assessment, schema standardization, deduplication |
| 2 | Code Rollup | Map granular codes → parent codes (PheCode, CCS, RxNorm, LOINC) |
| 3 | NLP | Clinical notes → UMLS CUI codes via petehr |
| 4 | Cohort Creation | Define cohort, extract features, build patient-level count matrices |

**Overall assessment:** The pipeline is well-structured and logically sound. All 4 critical/moderate bugs from v1 are confirmed fixed. The remaining work is primarily CLAUDE.md compliance, language polish, and a few code quality issues.

---

## 2. Critical Bugs (All Fixed — from v1)

All four bugs identified in v1 remain fixed. No new bugs found.

| Bug | Severity | Notebook | Fix Applied |
|-----|----------|----------|-------------|
| BUG-1: ICD-10 coding_system mismatch | Critical | Code Rollup | `"ICD10CM"` → `"ICD10"` |
| BUG-2: Age plot lexicographic sorting | Moderate | Getting Started | Added `.astype(int)` |
| BUG-3: Batch filename matching | Moderate | Code Rollup | `if batch in f` → `f.split("_")[1] == batch` |
| BUG-4: Latent `ICDnan` coding system | Low | Data Cleaning | Added `dropna(subset=[code_version_col])` |

---

## 3. NEW Issues Found in v2

These issues were **not identified** in the original `final_report.md`:

### 3.1 Semantic Mismatch: NLP vs Codified Counts (Cohort Creation) — HIGH

**Location:** Cohort Creation, cells 37-40
**Issue:** The codified matrices count total occurrences (a PheCode appearing 3 times in different records = count of 3). The NLP matrix deduplicates on `(subject_id, date, cui)` before counting, so it counts unique *dates* a CUI appeared, not total mentions. This changes the semantics of the count matrices without explanation.
**Impact:** Downstream analysis comparing codified and NLP feature counts would be comparing apples to oranges.
**Fix:** Add an explicit markdown cell explaining this design decision and its implications for downstream analysis.

### 3.2 For-Loop Violations — Getting Started — MEDIUM

**Location:** Getting Started, cell `e5b6f992` and inside `summarize_ehr_table` (cell `979e463a`)
**Issue:** Uses `for name, count in zip(...): word_freq[name] = count` for building word frequency dicts. This is a for-loop for data manipulation, violating CLAUDE.md.
**Fix:** Replace with `.set_index(desc_col)['patient_count'].to_dict()` or `dict(zip(...))`.

### 3.3 For-Loop Violations — Code Rollup — MEDIUM

**Location:** Code Rollup, cells 15, 38, 40
**Issue:** Uses `for col in columns: df[col] = df[col].str.strip()` for data cleaning. This is a for-loop for data manipulation.
**Fix:** Replace with explicit per-column calls or `df[cols] = df[cols].apply(lambda c: c.str.strip())`.

### 3.4 Missing Post-Output Explanations — Getting Started — MEDIUM

**Location:** Getting Started, after cells `effa7f8c`, `e2cb0453`, `f669c1de`, `caea2803`
**Issue:** The four `summarize_ehr_table` calls produce word clouds and top-10 tables, but none have post-output interpretation cells. CLAUDE.md: "do not let outputs speak for themselves."
**Fix:** Add brief markdown cells after each call interpreting what the top codes/conditions reveal.

### 3.5 Combined Operations in Single Cells — NLP — MEDIUM

**Location:** NLP notebook
- Cell `q2k9f5pb5y`: Combines `drop_duplicates()` AND `rename()` in one cell
- Cell `6fmt483ekju`: Combines `to_csv()` AND `Text2Code()` initialization in one cell
**Fix:** Split each into two separate cells with explanatory markdown between them.

### 3.6 Missing df.shape After Aggregations — NLP — MEDIUM

**Location:** NLP notebook, cells `e2ed689e` and `dvpzf2dxzn`
**Issue:** Groupby aggregations create new DataFrames but do not print `.shape`.
**Fix:** Add `print(f"Shape: {df.shape}")` after each aggregation.

### 3.7 No Validation for Unmapped NLP Results — Cohort Creation — MEDIUM

**Location:** Cohort Creation, cell 37
**Issue:** After NLP conversion, there is no check for how many notes produced zero CUIs or how many CUIs were unmatched. CLAUDE.md requires "explicitly code validation checks" and "count unmapped codes."
**Fix:** Add a validation cell counting notes with empty/null CUI results.

### 3.8 Potential None Propagation — Cohort Creation — MEDIUM

**Location:** Cohort Creation, cells 36-38
**Issue:** If `text2cui.convert()` returns empty string, `lambda x: x.split(',') if x else None` returns `None`, which is not dropped before `explode()`. This could propagate null values into the final matrix.
**Fix:** Add `dropna()` between the split and explode steps.

### 3.9 `dropna()` Without Subset — NLP & Cohort Creation — LOW

**Location:** NLP cell `kmcac6j0yng`, Cohort Creation cell 35
**Issue:** `dropna()` called without `subset` parameter, which drops rows where *any* column is null, not just the target column.
**Fix:** Add `subset=['text']` or the appropriate target column.

### 3.10 Missing Goal Expansion — Getting Started — LOW

**Location:** Getting Started, cell `8c2f18b0`
**Issue:** Goal statement is too terse ("Explore MIMIC-IV 3.1 EHR data and generate summary statistics"). Should tell readers what they will *learn or accomplish*.
**Fix:** Expand to mention understanding EHR data structure, patient demographics, and building a reusable summarization pipeline.

### 3.11 Missing Recap — Getting Started — LOW

**Location:** Getting Started, top of notebook
**Issue:** No recap of the Environment Setup notebook. CLAUDE.md requires a recap of the previous notebook.
**Fix:** Add a one-paragraph recap of what was set up in the Environment Setup notebook.

### 3.12 Overwhelming Reference Material — Getting Started — LOW

**Location:** Getting Started, cell `96b8fddc`
**Issue:** A 10-row MIMIC table reference is presented before any code. CLAUDE.md: "Front-load only the information needed for the next step."
**Fix:** Trim to only the tables used in this notebook, or move to an appendix.

### 3.13 patient_count Type Issue — Getting Started — LOW

**Location:** Getting Started, cell `e5b6f992` and inside `summarize_ehr_table`
**Issue:** `patient_count` is a string (all data read as `dtype=str`) but passed to `WordCloud.generate_from_frequencies()` which expects numeric values.
**Fix:** Cast to `int` before passing: `word_freq[name] = int(count)`.

### 3.14 Variable Shadowing — Code Rollup — LOW

**Location:** Code Rollup, cells 28 and 30
**Issue:** `cpt2ccs` is first a list (cell 28), then overwritten as a DataFrame (cell 30). Same variable name for two different types is confusing.
**Fix:** Rename the list to `cpt2ccs_rows` or similar.

### 3.15 Missing 4-Pipeline Overview Table — Code Rollup — LOW

**Location:** Code Rollup, cell 7
**Issue:** The subplan specified a reference table showing all 4 data types, their raw codes, parent codes, and mapping sources. This was planned but not implemented.
**Fix:** Add the overview table to the "What is Code Rollup?" section.

### 3.16 NDC Teach-Then-Abstract Violation — Code Rollup — LOW

**Location:** Code Rollup, cell 50
**Issue:** `roll_ndc2rxnorm` function is presented as a 30+ line block without an inline walkthrough first. Other mappings follow teach-then-abstract, but NDC does not.
**Fix:** Add a brief inline walkthrough before the function, or add extensive comments within.

### 3.17 Missing .endswith('.csv') Filter — Code Rollup — LOW

**Location:** Code Rollup, cell 58
**Issue:** `os.listdir` filters hidden files but not non-CSV files. If unexpected files exist, they would be included.
**Fix:** Add `.endswith('.csv')` to the filter.

### 3.18 SettingWithCopyWarning Risk — Code Rollup — LOW

**Location:** Code Rollup, cell 66
**Issue:** Filtered DataFrame slice may trigger `SettingWithCopyWarning`. Adding `.copy()` would prevent this.
**Fix:** Add `.copy()` to the filtered assignment.

### 3.19 Unnecessary Lambda — NLP & Cohort Creation — LOW

**Location:** NLP and Cohort Creation notebooks
**Issue:** `lambda x: text2cui.convert(x)` is equivalent to `.map(text2cui.convert)`.
**Fix:** Remove the lambda wrapper.

### 3.20 Missing External GitHub Links — Getting Started — LOW

**Location:** Getting Started, top and bottom
**Issue:** No external GitHub notebook links as required by CLAUDE.md.
**Fix:** Add links in the format `github_repo/TUTORIAL/notebook_name`.

### 3.21 i2b2/VINCI Tangent — Getting Started — LOW

**Location:** Getting Started, cell `41586bea`
**Issue:** Mentions i2b2 and VINCI frameworks which are never used in the tutorial. Could overwhelm beginners.
**Fix:** Remove or shorten to a single sentence with a link for interested readers.

### 3.22 Imprecise Age Explanation — Getting Started — LOW

**Location:** Getting Started, cell `ec4eff96`
**Issue:** States "ages over 89 are depicted as 90+" — the actual MIMIC-IV behavior is that ages are capped at 91. Also, the explanation of `anchor_age=0` for pediatric patients is imprecise.
**Fix:** Correct to reflect MIMIC-IV's actual anonymization approach.

### 3.23 NDC Deduplication Silent Drop — Getting Started — LOW

**Location:** Getting Started, cell `d1e0742b`
**Issue:** `drop_duplicates(subset=['ndc'], keep='first')` silently drops alternative drug names for the same NDC (generic vs brand). No note to the reader.
**Fix:** Add a brief comment explaining this choice.

---

## 4. Notebook-by-Notebook Findings

### 4.1 Getting Started

| Priority | Issue | Type | Status |
|----------|-------|------|--------|
| HIGH | Post-output explanations missing after 4 summarize_ehr_table calls | CLAUDE.md | NEW |
| HIGH | For-loop for word frequency dict building | CLAUDE.md | NEW |
| MEDIUM | Missing external GitHub links at top/bottom | CLAUDE.md | NEW |
| MEDIUM | Missing recap of Environment Setup | CLAUDE.md | NEW |
| LOW | Goal statement too terse | Language | NEW |
| LOW | patient_count needs int cast for WordCloud | Code | NEW |
| LOW | Overwhelming reference table before code | Flow | NEW |
| LOW | i2b2/VINCI tangent | Flow | NEW |
| LOW | Imprecise age explanations | Accuracy | NEW |
| LOW | NDC dedup silent drop | Accuracy | NEW |
| LOW | 12+ hardcoded statistics | Hardcoded | v1 |
| LOW | Embedded image via attachment: may not render on GitHub | Rendering | v1 |

### 4.2 Data Cleaning

| Priority | Issue | Type | Status |
|----------|-------|------|--------|
| MEDIUM | Function cell ~50 lines (violates 5-10 line rule) | CLAUDE.md | v1 |
| LOW | admissions.csv read 3 times without explanation | Redundancy | v1 |
| LOW | ICD not formally defined on first use | Language | NEW |
| LOW | SLURM mentioned but not defined | Language | NEW |
| LOW | .startswith('.') filter lacks explanatory comment | Code | NEW |
| LOW | 158M rows claim should be verified | Accuracy | v1 |

### 4.3 Code Rollup

| Priority | Issue | Type | Status |
|----------|-------|------|--------|
| MEDIUM | For-loops for column stripping (cells 15, 38, 40) | CLAUDE.md | NEW |
| MEDIUM | NDC function shown before inline walkthrough | CLAUDE.md | v1 |
| LOW | Variable shadowing of cpt2ccs | Code | NEW |
| LOW | Missing 4-pipeline overview table | Flow | NEW |
| LOW | Missing .endswith('.csv') filter | Code | NEW |
| LOW | SettingWithCopyWarning risk in cell 66 | Code | NEW |
| LOW | Dead glob import | Code | v1 |
| LOW | $prref 2015.csv suspicious filename | Code | v1 |

### 4.4 NLP

| Priority | Issue | Type | Status |
|----------|-------|------|--------|
| HIGH | Placeholder GitHub links (cells ef7cc2ae, u1hsdj82k6j) | Links | v1 |
| MEDIUM | Two operations combined in cell q2k9f5pb5y (dedup+rename) | CLAUDE.md | NEW |
| MEDIUM | Two operations combined in cell 6fmt483ekju (save+init) | CLAUDE.md | NEW |
| MEDIUM | Missing df.shape after groupby aggregations | CLAUDE.md | NEW |
| MEDIUM | import petehr before pip install instruction | Sequencing | v1 |
| LOW | dropna() without subset parameter | Code | NEW |
| LOW | Unnecessary lambda wrapper | Code | v1 |
| LOW | Hardcoded approximate counts in markdown | Hardcoded | NEW |
| LOW | MIMIC-IV Note version mismatch not flagged | Accuracy | v1 |

### 4.5 Cohort Creation

| Priority | Issue | Type | Status |
|----------|-------|------|--------|
| HIGH | NLP vs codified count semantics mismatch | Accuracy | **NEW** |
| MEDIUM | No validation for unmapped NLP results | CLAUDE.md | NEW |
| MEDIUM | Potential None propagation after NLP conversion | Code | NEW |
| MEDIUM | dropna() without subset parameter | Code | v1 |
| LOW | Function cell 22 exceeds 10 lines | CLAUDE.md | v1 |
| LOW | Missing df.shape in batch-level merges | CLAUDE.md | v1 |
| LOW | Unnecessary lambda wrapper | Code | v1 |
| LOW | Hardcoded cohort sizes in markdown | Hardcoded | v1 |

---

## 5. Cross-Notebook Consistency Issues

| Issue | Notebooks Affected | Status |
|-------|--------------------|--------|
| Placeholder GitHub links | NLP | Open (v1) |
| Missing GitHub links entirely | Getting Started, Env Setup | Open (v1 + NEW) |
| Variable naming inconsistency (folder_path vs input_dir vs data_dir) | Multiple | Open (v1) |
| Tone inconsistency (reference vs tutorial voice) | Getting Started, Env Setup | Open (v1) |
| Dead imports (glob in Code Rollup) | Code Rollup | Open (v1) |
| .DS_Store guards | Notebooks 1, 2, 4 fixed; NLP pending | Partial (v1) |
| Hardcoded statistics in markdown | All notebooks | Open (v1) |
| dropna() without subset | NLP, Cohort Creation | Open (NEW) |
| Unnecessary lambda wrappers | NLP, Cohort Creation | Open (v1) |

---

## 6. CLAUDE.md Compliance Gaps

| Rule | Status | Details |
|------|--------|---------|
| Sandwich format | **Partial** | Getting Started missing post-output explanations for 4 cells |
| df.shape before/after merges | **Partial** | Missing in NLP aggregations, Cohort Creation batch merges |
| Max 5-10 lines per code block | **Partial** | Data Cleaning (~50 line function), Code Rollup (30+ and 25+ line functions), Cohort Creation (27 line function) |
| One logical step per cell | **Partial** | NLP has 2 cells combining operations |
| Teach then abstract | **Violated** | Code Rollup NDC section shows function before walkthrough |
| No for-loops for data manipulation | **Violated** | Getting Started (word freq), Code Rollup (column stripping) |
| External GitHub links at top/bottom | **Missing** | Getting Started, Env Setup have none; NLP has placeholders |
| Define domain terms before first use | **Partial** | EHR/BIDMC not defined in Env Setup; ICD not formally defined in Data Cleaning |
| Recap of previous notebook | **Partial** | Getting Started missing recap of Env Setup |
| Relative paths / base_dir | **Pass** | All notebooks compliant |
| Dates as strings | **Pass** | All notebooks compliant |
| Medical codes as strings | **Pass** | All notebooks compliant |
| Conceptual headings | **Pass** | All notebooks compliant |
| Validation checks | **Partial** | Missing unmapped CUI validation in Cohort Creation |

---

## 7. Actionable Fix List

### HIGH PRIORITY (6 fixes)

| # | Notebook | Fix | Type |
|---|----------|-----|------|
| H1 | Cohort Creation | Add markdown explaining NLP vs codified count semantics difference | Accuracy |
| H2 | Getting Started | Add post-output explanation cells after 4 summarize_ehr_table calls | CLAUDE.md |
| H3 | Getting Started | Replace for-loops with vectorized dict creation in word freq code | CLAUDE.md |
| H4 | NLP | Replace placeholder GitHub links with actual URLs | Links |
| H5 | Cohort Creation | Add validation cell counting notes with empty/null CUI results | CLAUDE.md |
| H6 | Cohort Creation | Add dropna() between NLP split and explode to prevent None propagation | Code |

### MEDIUM PRIORITY (10 fixes)

| # | Notebook | Fix | Type |
|---|----------|-----|------|
| M1 | Code Rollup | Replace for-loops in cells 15, 38, 40 with explicit per-column calls | CLAUDE.md |
| M2 | NLP | Split cell q2k9f5pb5y into separate dedup and rename cells | CLAUDE.md |
| M3 | NLP | Split cell 6fmt483ekju into separate save and init cells | CLAUDE.md |
| M4 | NLP | Add df.shape after groupby aggregations | CLAUDE.md |
| M5 | Getting Started | Add external GitHub links at top and bottom | CLAUDE.md |
| M6 | Getting Started | Add recap of Environment Setup at top | CLAUDE.md |
| M7 | NLP | Fix import/install sequencing (pip install before import) | Sequencing |
| M8 | NLP/Cohort Creation | Fix dropna() to use subset parameter | Code |
| M9 | Cohort Creation | Fix dropna(subset=['text']) instead of bare dropna() | Code |
| M10 | Getting Started | Cast patient_count to int before WordCloud | Code |

### LOW PRIORITY (13 fixes)

| # | Notebook | Fix | Type |
|---|----------|-----|------|
| L1 | Getting Started | Expand goal statement | Language |
| L2 | Getting Started | Trim or move MIMIC table reference to appendix | Flow |
| L3 | Getting Started | Remove/shorten i2b2/VINCI tangent | Flow |
| L4 | Getting Started | Fix imprecise age explanations | Accuracy |
| L5 | Getting Started | Note NDC dedup silently drops alternatives | Accuracy |
| L6 | Code Rollup | Rename cpt2ccs list to avoid variable shadowing | Code |
| L7 | Code Rollup | Add 4-pipeline overview table | Flow |
| L8 | Code Rollup | Add .endswith('.csv') to file filters | Code |
| L9 | Code Rollup | Add .copy() in cell 66 to prevent SettingWithCopyWarning | Code |
| L10 | Code Rollup | Remove dead glob import | Code |
| L11 | NLP/Cohort Creation | Remove unnecessary lambda wrappers | Code |
| L12 | Data Cleaning | Define ICD on first use | Language |
| L13 | All notebooks | Add "your numbers may differ" disclaimer for hardcoded stats | Hardcoded |

---

## Summary

**Total issues tracked:** 134 (111 from v1 + 23 new in v2)

| Category | Count | High | Medium | Low |
|----------|-------|------|--------|-----|
| Bugs (all fixed) | 4 | 1 | 2 | 1 |
| CLAUDE.md compliance | ~35 | 3 | 5 | ~27 |
| Language/tone | ~25 | 0 | 1 | ~24 |
| Code quality | ~25 | 1 | 4 | ~20 |
| Missing links/content | ~15 | 1 | 2 | ~12 |
| Accuracy | ~13 | 1 | 1 | ~11 |
| Hardcoded statistics | ~17 | 0 | 0 | ~17 |

The pipeline architecture is sound. No structural changes needed. The highest-impact fix is **H1** (documenting the NLP vs codified count semantics mismatch in Cohort Creation), as it affects the interpretation of all downstream analysis.
