# EHR Preprocessing Tutorial — Comprehensive Review Report

**Date:** 2026-03-09
**Scope:** Cell-by-cell review of all 6 notebooks for code correctness, language consistency, logical flow, CLAUDE.md compliance, and improvement opportunities.

---

## Table of Contents

1. [Pipeline Overview & Structure](#1-pipeline-overview--structure)
2. [Critical Bugs (All Fixed)](#2-critical-bugs-all-fixed)
3. [Notebook-by-Notebook Findings](#3-notebook-by-notebook-findings)
4. [Cross-Notebook Consistency Issues](#4-cross-notebook-consistency-issues)
5. [CLAUDE.md Compliance Gaps](#5-claudemd-compliance-gaps)
6. [Hardcoded Statistics Inventory](#6-hardcoded-statistics-inventory)
7. [Improvement Suggestions](#7-improvement-suggestions)

---

## 1. Pipeline Overview & Structure

The tutorial consists of 6 notebooks forming a linear pipeline:

| # | Notebook | Purpose |
|---|----------|---------|
| 0 | Environment Setup | Workspace creation, Python env, MIMIC-IV download |
| 0.5 | Getting Started | Data exploration, summary statistics, word clouds |
| 1 | Data Cleaning | Missingness assessment, schema standardization, deduplication |
| 2 | Code Rollup | Map granular codes → parent codes (PheCode, CCS, RxNorm, LOINC) |
| 3 | NLP | Clinical notes → UMLS CUI codes via petehr |
| 4 | Cohort Creation | Define cohort, extract features, build patient-level count matrices |

**Overall assessment:** The pipeline is logically structured and covers the full EHR preprocessing workflow comprehensively. The progression from raw data to analysis-ready matrices is sound. The tutorial tone is generally accessible and encouraging. The issues identified below are fixable without restructuring the pipeline.

---

## 2. Critical Bugs (All Fixed)

All four bugs identified during the review have been fixed.

### BUG-1: ICD-10 Coding System Mismatch (Code Rollup + Cohort Creation) — CRITICAL — FIXED

**Impact:** Silently dropped ALL ICD-10 diagnoses from both the Code Rollup merge and Cohort Creation PheCode lookup, potentially excluding thousands of patients.

**Root cause:** Notebook 1 (Data Cleaning) produces `coding_system = "ICD" + icd_version`, yielding `"ICD9"` and `"ICD10"`. However, Notebook 2 (Code Rollup) set the PheCode mapping's coding_system to `"ICD10CM"` via `flag_to_system = {"9": "ICD9", "10": "ICD10CM"}`. Since the merge joins on `coding_system`, all ICD-10 rows failed to match. Notebook 4 (Cohort Creation) had the same mismatch when re-reading raw data.

**Fix applied:** Changed `flag_to_system` in Notebook 2 (cell-16) from `{"9": "ICD9", "10": "ICD10CM"}` to `{"9": "ICD9", "10": "ICD10"}`, making the PheCode mapping consistent with Notebook 1's output. Updated the comment to reference the correct values. Also updated the recap table in cell-2 to say `ICD10` instead of `ICD10CM`.

### BUG-2: Age Plot Lexicographic Sorting (Getting Started) — MODERATE — FIXED

**Impact:** The age distribution bar chart displayed ages in wrong order (e.g., "18", "19", "2", "20", "21"...) because `anchor_age` values are strings and `sort_index()` sorts lexicographically.

**Fix applied:** Added `.astype(int)` before `value_counts().sort_index()` in cell `9b25a2d5`:
```python
age_counts = demographics['anchor_age'].astype(int).value_counts().sort_index()
```

### BUG-3: Batch Matching with `in` Operator (Code Rollup, cell-71) — MODERATE — FIXED

**Impact:** The `rollup_data_by_batch` function used `if batch in f` to match filenames, which means `"batch1"` matches `"batch10"`, `"batch11"`, etc. This caused batch 1 to incorrectly process files from batches 10-18.

**Fix applied:** Changed to exact segment matching in cell-71:
```python
# Old: batch_files = [f for f in files if batch in f]
# New: exact match on the batch segment of the filename
batch_files = [f for f in files if f.split("_")[1] == batch]
```

### BUG-4: Latent `ICDnan` Coding System (Data Cleaning) — LOW — FIXED

**Impact:** If `code_version_col` contains null values, the string concatenation `"ICD" + str(nan)` produces `"ICDnan"`, which silently poisons downstream mappings.

**Fix applied:** Added `batch_df = batch_df.dropna(subset=[code_version_col])` before the concatenation in cell `3b09c476`, so rows with null version values are dropped before building the coding_system string.

---

## 3. Notebook-by-Notebook Findings

### 3.1 Environment Setup (`EHR_Preprocessing_Environment_Setup.ipynb`)

**Strengths:**
- Clear workspace organization with `base_dir = "EHR_TUTORIAL_WORKSPACE"`
- Good coverage of both Mac and Windows setup
- Helpful directory structure visualization

**Issues:**

| # | Cell | Type | Description |
|---|------|------|-------------|
| 1 | 13 | Sequencing | References `requirements.txt` before the git clone that creates it |
| 2 | 13 | Sandwich | Two consecutive code cells without explanatory markdown between them |
| 3 | 19 | Sandwich | Two consecutive code cells (pip install + import verification) |
| 4 | — | Missing | No definition of "EHR" or "BIDMC" when first mentioned |
| 5 | — | Missing | No external GitHub link at top and bottom of notebook |
| 6 | — | Language | Opening paragraph could better explain *why* environment setup matters |
| 7 | — | Scope | SLURM/HPC "Advanced Module" mentioned in CLAUDE.md but not present |
| 8 | — | Missing | No `df.shape` prints after data loading cells |
| 9 | — | Tone | Some cells use passive voice where active would be clearer |

### 3.2 Getting Started (`EHR_Preprocessing_Getting_Started.ipynb`)

**Strengths:**
- Excellent data exploration breadth (all major MIMIC-IV tables)
- Word cloud visualizations are engaging
- Good use of summary CSVs for reference

**Issues:**

| # | Cell | Type | Description | Status |
|---|------|------|-------------|--------|
| 1 | age plot | Bug | Lexicographic string sorting of ages (BUG-2) | **FIXED** |
| 2 | multiple | Hardcoded | 12+ hardcoded statistics that will break with different data | Open |
| 3 | — | Accuracy | `anchor_age=0` interpretation unclear (neonates? redacted?) | Open |
| 4 | — | Rendering | Embedded image via `attachment:` protocol may not render on GitHub | Open |
| 5 | — | Length | Very long notebook; could overwhelm beginners | Open |
| 6 | — | Missing | No external GitHub links | Open |
| 7 | — | Missing | No recap/transition to next notebook at the end | Open |
| 8 | — | Sandwich | Several places where output is not explained | Open |
| 9 | — | Flow | Jumps between tables without explaining the connection | Open |
| 10 | — | Tone | Some sections read as reference material rather than tutorial guidance | Open |

**Hardcoded statistics found (partial list):**
- Number of patients, admissions, diagnoses
- Specific percentages for missingness
- Date ranges
- Top-N values in various tables

### 3.3 Data Cleaning (`EHR_Preprocessing_1_Data_Cleaning.ipynb`)

**Strengths:**
- Excellent teach-then-abstract pattern for cleaning logic
- Clear schema standardization to 4-column format
- Good batch processing explanation
- Thorough deduplication with before/after shape prints

**Issues:**

| # | Cell | Type | Description | Status |
|---|------|------|-------------|--------|
| 1 | 3b09c476 | Bug | `"ICD" + str(nan)` → `"ICDnan"` (BUG-4) | **FIXED** |
| 2 | 7abc8857 + c30e9782 | Sandwich | Two consecutive code cells without markdown between them | Open |
| 3 | — | Missing | `df.shape` not printed after every merge/dedup (some are missing) | Open |
| 4 | — | Language | A few sections jump into code without the "why" | Open |
| 5 | — | Links | Recap link was placeholder | **Fixed (prior commit)** |
| 6 | — | Links | Executable notebook links were placeholders | **Fixed (prior commit)** |
| 7 | — | DS_Store | `os.listdir` calls now guarded | **Fixed (prior commit)** |
| 8 | — | Consistency | Variable naming mostly good but occasional single-letter vars | Open |
| 9 | — | Flow | Batch processing concept introduced well but batch count (8) is hardcoded | Open |
| 10 | — | Tone | Generally strong; a few cells could use warmer transitions | Open |

### 3.4 Code Rollup (`EHR_Preprocessing_2_Code_Rollup.ipynb`)

**Strengths:**
- Covers all 4 major code systems comprehensively
- Good inline walkthrough of ICD→PheCode mapping before generalization
- Clear directory structure explanation
- Validation checks at the end

**Issues:**

| # | Cell | Type | Description | Status |
|---|------|------|-------------|--------|
| 1 | cell-16 | Bug | PheCode mapping used `"ICD10CM"` vs Notebook 1's `"ICD10"` (BUG-1) | **FIXED** |
| 2 | cell-71 | Bug | `if batch in f` matches batch1→batch10 (BUG-3) | **FIXED** |
| 3 | cell-2 | Accuracy | Recap table referenced `ICD10CM` instead of `ICD10` | **FIXED** |
| 4 | cell-50 | CLAUDE.md | `roll_ndc2rxnorm` function shown before inline walkthrough (teach-then-abstract violation) | Open |
| 5 | cell-52 | Accuracy | Says "all four mapping files ready" when only 3 have been loaded at that point | Open |
| 6 | — | Import | `glob` imported but never used (dead import) | Open |
| 7 | — | Filename | `$prref 2015.csv` — suspicious filename with `$` character, may cause shell issues | Open |
| 8 | — | Filename | `CCS_Services_Procedures_v2025-1_052425.csv` — hardcoded date-stamped filename | Open |
| 9 | — | Sandwich | A few places where consecutive code cells lack explanatory markdown | Open |
| 10 | — | Flow | Medication rollup section is notably longer and more complex than others | Open |
| 11 | — | Language | Some mapping file descriptions are terse | Open |
| 12 | — | DS_Store | `os.listdir` calls now guarded | **Fixed (prior commit)** |

### 3.5 NLP (`EHR_Preprocessing_3_Natural_Language_Processing.ipynb`)

**Strengths:**
- Clear explanation of why NLP is needed for clinical data
- Good introduction to UMLS and CUI concepts
- petehr library usage is well-documented
- Discharge note selection logic is sound

**Issues:**

| # | Cell | Type | Description |
|---|------|------|-------------|
| 1 | cell-4 | Links | Placeholder GitHub link (`github_repo/TUTORIAL/...`) |
| 2 | cell-46 | Links | Placeholder GitHub link at notebook end |
| 3 | cell-6 vs cell-9 | Sequencing | `import petehr` appears before the `pip install petehr` instruction |
| 4 | cell-40 | Language | CUI interpretation section is too generic; should explain specific CUIs from the data |
| 5 | — | Missing | Version mismatch between MIMIC-IV Note v2.2 and Hosp v3.1 not explained |
| 6 | — | Missing | No progress indicator for long-running NLP processing |
| 7 | — | Lambda | `lambda` wrapper around `text2cui.convert` is unnecessary |
| 8 | — | dropna | `dropna()` without `subset` parameter is overly broad |
| 9 | — | Sandwich | Some output cells lack interpretation |
| 10 | — | Flow | Transition from note selection to NLP processing could be smoother |
| 11 | — | Tone | Generally good but some sections are dense |

**Note:** A subplan exists (`EHR_Preprocessing_3_Natural_Language_Processing_subplan.md`) for a full rewrite of this notebook.

### 3.6 Cohort Creation (`EHR_Preprocessing_4_Cohort_Creation.ipynb`)

**Strengths:**
- Clear cohort definition process (PheCode-based)
- Comprehensive feature extraction across all data types
- Good aggregation into patient-level count matrices
- Validation section at the end

**Issues:**

| # | Cell | Type | Description | Status |
|---|------|------|-------------|--------|
| 1 | cell-10 | Bug | `"ICD" + icd_version` now matches Notebook 2's corrected PheCode mapping (BUG-1 resolved upstream) | **FIXED (upstream)** |
| 2 | cell-10 | Redundancy | Re-reads raw diagnoses data instead of using rolled-up data from Notebook 2 | Open |
| 3 | — | dropna | `dropna()` without `subset` — drops rows where *any* column is null | Open |
| 4 | — | Lambda | Unnecessary lambda wrapper on `text2cui.convert` | Open |
| 5 | — | Missing | No progress indicator for NLP aggregation step | Open |
| 6 | — | Links | Opening and closing GitHub links were placeholders | **Fixed (prior commit)** |
| 7 | — | DS_Store | `os.listdir` calls now guarded | **Fixed (prior commit)** |
| 8 | — | Sandwich | Some consecutive code cells without markdown | Open |
| 9 | — | Flow | Jump from cohort definition to feature extraction could use a transition | Open |
| 10 | — | Hardcoded | Cohort size (20,316) and PheCode (495) are hardcoded in explanatory text | Open |

---

## 4. Cross-Notebook Consistency Issues

### 4.1 Link Placeholders
- **Notebooks 3 (NLP)** still has `github_repo/TUTORIAL/...` placeholder links
- Notebooks 1, 4 were fixed in prior commit
- Notebook 2 already had correct links
- Notebooks 0 and 0.5 (Env Setup, Getting Started) have no external links at all

### 4.2 `.DS_Store` Guards
- Notebooks 1, 2, 4 now have guards on `os.listdir` calls (fixed in prior commit)
- Notebook 3 should be checked during its planned rewrite

### 4.3 Variable Naming
- Generally consistent use of `base_dir`, `_dir` suffixed path variables
- Minor inconsistency: some notebooks use `folder_path` vs `input_dir` vs `data_dir` for similar concepts
- Column names are consistent across the pipeline (`subject_id`, `code`, `coding_system`, `date`)

### 4.4 Coding System Values — RESOLVED
- ~~Inconsistency between Notebook 2 and 4: Notebook 2 produced `"ICD10CM"` in the `coding_system` column; Notebook 4 expected `"ICD10"`.~~
- **Fixed:** Notebook 2's PheCode mapping now uses `"ICD10"` to match Notebook 1's output. All three notebooks (1, 2, 4) are now consistent.

### 4.5 Import Patterns
- Most notebooks import pandas, os, and numpy at the top
- Notebook 2 has a dead `glob` import
- Import ordering is not fully consistent but this is minor

### 4.6 Language & Tone
- Notebooks 1, 2, and 4 have the strongest tutorial voice ("We do this because...", "Notice that...")
- Getting Started reads more like a reference document than a guided tutorial
- Environment Setup is functional but could be warmer
- NLP notebook is mid-rewrite and has mixed tone

### 4.7 Output Directory Naming
- Consistent pattern: `step3_cleaned_rawdata`, `step4_rolledup_finaldata`, `step5_cohort_aggregateddata`
- Step numbering (3, 4, 5) vs notebook numbering (1, 2, 4) is potentially confusing for beginners but is documented

---

## 5. CLAUDE.md Compliance Gaps

| Rule | Status | Notebooks Affected |
|------|--------|--------------------|
| Sandwich format (explanation → code → output interpretation) | Partial | All notebooks have some violations |
| `df.shape` before and after every merge/dedup | Partial | Getting Started, some cells in Data Cleaning |
| Max 5-10 lines per code block | Partial | Several cells in Code Rollup and Cohort Creation exceed this |
| One logical step per code cell | Partial | A few cells combine multiple operations |
| Teach then abstract | Violated | Code Rollup cell-50 (`roll_ndc2rxnorm` shown before inline walkthrough) |
| No for-loops for data manipulation | Good | Only I/O loops detected |
| External GitHub links at top and bottom | Missing | Env Setup, Getting Started |
| Define domain terms before first use | Partial | EHR, BIDMC not defined in Env Setup |
| Recap of previous notebook at start | Partial | Some notebooks lack this |
| Zero absolute paths | Good | All paths use `base_dir` |

---

## 6. Hardcoded Statistics Inventory

Statistics that will break if the tutorial is run on a different MIMIC-IV version or subset:

### Getting Started
- Patient counts, admission counts, diagnosis counts
- Specific missingness percentages
- Date ranges for admissions
- Top-N diagnoses/procedures/medications values
- Age distribution statistics

### Data Cleaning
- Batch counts and sizes
- Before/after deduplication row counts
- Missingness percentages per column

### Code Rollup
- Mapping file row counts
- Unmapped code counts and percentages
- Before/after rollup row counts

### Cohort Creation
- Cohort size (20,316 patients)
- PheCode target (495 for asthma)
- Feature matrix dimensions
- NLP coverage percentage (73%)

**Recommendation:** Replace hardcoded statistics in markdown cells with dynamic references or add a note that "your numbers may differ" where exact values are stated in explanatory text. Code cell outputs naturally update, but the surrounding markdown does not.

---

## 7. Improvement Suggestions

### High Priority (Bugs & Correctness) — ALL RESOLVED

1. ~~**Fix BUG-1 immediately**~~ — **FIXED.** Changed `flag_to_system` in Notebook 2 from `{"9": "ICD9", "10": "ICD10CM"}` to `{"9": "ICD9", "10": "ICD10"}`. Updated recap table reference.

2. ~~**Fix BUG-2**~~ — **FIXED.** Added `.astype(int)` before `value_counts().sort_index()` in Getting Started age plot.

3. ~~**Fix BUG-3**~~ — **FIXED.** Changed `if batch in f` to `f.split("_")[1] == batch` for exact batch matching in Code Rollup.

4. ~~**Fix BUG-4**~~ — **FIXED.** Added `dropna(subset=[code_version_col])` before coding_system concatenation in Data Cleaning.

### Medium Priority (Tutorial Quality)

5. **Complete NLP notebook rewrite** — The subplan already exists. The NLP notebook has the most issues of any notebook and would benefit most from a full pass.

6. **Add external GitHub links** to Environment Setup and Getting Started notebooks (top and bottom).

7. **Fix remaining placeholder links** in NLP notebook.

8. **Fix the `pip install` sequencing** in NLP — move the install instruction before the import cell.

9. **Enforce sandwich format consistently** — Audit all consecutive code cells and add explanatory markdown between them.

10. **Replace hardcoded statistics** in markdown cells with either dynamic values or disclaimers.

### Lower Priority (Polish)

11. **Remove dead `glob` import** from Code Rollup.

12. **Fix `$prref 2015.csv` filename** — verify this is correct or rename.

13. **Add progress indicators** for long-running cells (NLP processing, batch operations).

14. **Add "what you'll learn" box** at the top of each notebook for consistency.

15. **Simplify the `dropna()` calls** — use `subset` parameter to target specific columns.

16. **Remove unnecessary lambda wrappers** around `text2cui.convert`.

17. **Standardize path variable naming** — pick one convention (`_dir` suffix) and use it everywhere.

18. **Add transition paragraphs** between major sections within each notebook.

19. **Consider splitting Getting Started** — it's the longest notebook and could be split into "Data Overview" and "Data Exploration" if it overwhelms beginners.

20. **Add a glossary notebook or appendix** — collect all domain term definitions (PheCode, CUI, UMLS, ICD, CCS, NDC, RxNorm, LOINC, CPT, HCPCS) in one place, referenced from each notebook.

### Architecture Suggestions

21. **Cohort Creation could use rolled-up data directly** instead of re-reading raw diagnoses and re-processing. This would simplify the code, reduce runtime, and avoid any future coding_system mismatches.

22. **Consider adding a "pipeline validation" notebook** (Notebook 5) that loads all final outputs and runs integrity checks — confirming row counts, checking for nulls, verifying schema consistency across all matrices.

23. **Add `UPDATE_TRACK.md` population** — the tracker file exists but most schema handoff sections are empty. Populating these as each notebook is finalized will help with maintenance.

---

## Summary

The tutorial is well-structured and covers EHR preprocessing comprehensively. All four bugs identified during the review have been fixed:

| Bug | Severity | Notebook | Fix |
|-----|----------|----------|-----|
| BUG-1: ICD-10 coding_system mismatch | Critical | Code Rollup (cell-16) | `"ICD10CM"` → `"ICD10"` in PheCode mapping |
| BUG-2: Age plot string sorting | Moderate | Getting Started (cell 9b25a2d5) | Added `.astype(int)` |
| BUG-3: Batch filename matching | Moderate | Code Rollup (cell-71) | `if batch in f` → `f.split("_")[1] == batch` |
| BUG-4: Null version → "ICDnan" | Low | Data Cleaning (cell 3b09c476) | Added `dropna(subset=[code_version_col])` |

The remaining areas for improvement are: completing the NLP notebook rewrite, enforcing CLAUDE.md formatting rules consistently, and replacing hardcoded statistics with dynamic values. The pipeline architecture is sound and does not need restructuring.

**Total issues found:** 111 across all notebooks
- Critical bugs: 1 (fixed)
- Moderate bugs: 3 (fixed)
- CLAUDE.md compliance gaps: ~30
- Language/tone improvements: ~25
- Missing links/content: ~15
- Code quality improvements: ~20
- Hardcoded statistics: ~17
