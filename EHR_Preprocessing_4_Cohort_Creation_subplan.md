# EHR_Preprocessing_4_Cohort_Creation Subplan

## Context
The Cohort Creation notebook defines a patient cohort (asthma, PheCode 495), extracts codified and NLP features for that cohort, and aggregates them into patient-level count matrices. The current notebook has significant CLAUDE.md violations: hardcoded absolute paths, a 30-line mega cell, missing sandwich format, no goal/recap, only Diagnoses processed (Procedures/Meds/Labs left as reader exercise), no domain term definitions, no transitions, redundant dropna calls, and a CSV bug that drops subject_id.

## Proposed Logical Flow (~54 cells)

### Section 0: Front Matter (4 cells)
- Title + Author
- **Goal statement:** Define an asthma patient cohort, extract all codified and NLP features, aggregate into patient-level count matrices
- **Recap:** Brief summary of Notebooks 0-3 (cleaned data → rolled-up codes → NLP CUIs)
- External notebook link

### Section 1: Setup (3 cells)
- Imports (pandas, os)
- `base_dir` using relative path
- Define output directories (codified + nlp)

### Section 2: What Is Cohort Creation? (2 cells)
- Define "cohort" in plain English, explain why we need one
- Explain the two outputs: codified count matrix + NLP count matrix

### Section 3: Defining the Asthma Cohort (8 cells)
- **3a:** Define PheCode — what it is, why it's better than raw ICD for cohort selection (2 cells)
- **3b:** Load raw diagnoses_icd.csv, display shape (1 cell)
- **3c:** Load icd_to_phecode mapping, display (1 cell)
- **3d:** Merge diagnoses with PheCode mapping, shape before/after (1 cell)
- **3e:** Filter to PheCode 495 (asthma), explain the result (1 cell)
- **3f:** Extract unique patient IDs → `asthma_cohort`, display shape (1 cell)
- **3g:** Interpret: "We identified 20,316 patients…" (1 cell)

### Section 4: Extracting Codified Data — Diagnoses Walkthrough (~8 cells)
- **4a:** Transition — explain what "extraction" means (filter rolled-up data to cohort patients) (1 cell)
- **4b:** Load rolled-up diagnoses batches, merge with cohort, display shape (3 cells)
- **4c:** Aggregate: groupby subject_id + PheCode → counts (1 cell)
- **4d:** Pivot to patient × PheCode matrix, display (1 cell)
- **4e:** Save to CSV (with subject_id fix), verify shape (1 cell)
- **4f:** Explain the output matrix — what rows/columns mean (1 cell)

### Section 5: Extracting Codified Data — Procedures, Medications, Labs (~9 cells)
- **5a:** Build a reusable extraction function wrapping the steps from Section 4 (1 cell)
- **5b-5d:** For each of Procedures, Medications, Labs: brief explanation + call function + display shape (~8 cells)

### Section 6: NLP Data — Extracting CUIs from Clinical Notes (~16 cells)
- **6a:** Transition — explain we now extract NLP features for the same cohort (1 cell)
- **6b:** Explain MIMIC-IV Note vs Hosp version mismatch (1 cell)
- **6c:** Install + import petehr, load asthma CUI dictionary (2 cells)
- **6d:** Define CUI, UMLS, ONCE in plain English (1 cell)
- **6e:** Load discharge notes, display shape (1 cell)
- **6f:** Filter to asthma cohort patients, check coverage (73%), explain data completeness (2 cells)
- **6g:** Select columns of interest, rename charttime→date, truncate date (2 cells)
- **6h:** Run Text2Code on notes — walk through one example first, then apply to all (2 cells)
- **6i:** Explode CUI strings → one row per CUI, drop duplicates, shape before/after (2 cells)
- **6j:** Aggregate: groupby subject_id + CUI → counts, pivot to matrix, save CSV (2 cells)

### Section 7: Validation & Summary (4 cells)
- Verify both output files exist and load correctly
- Summary table: data type, matrix dimensions, file path
- "What We Accomplished" bullets
- External notebook link + resources (ONCE, KESER, NILE)

---

## Key Technical Changes

| Current | Refactored |
|---|---|
| Hardcoded absolute path | Relative `base_dir` |
| 30-line mega cell (load + merge + filter + display) | One logical step per cell, sandwich format |
| No shape checks around merges | `df.shape` before and after every merge/dedup |
| Only Diagnoses for codified data | All 4 data types (Diagnoses, Procedures, Meds, Labs) |
| `index=None` drops subject_id from CSV | Reset index before save |
| `dropna(inplace=True)` called redundantly | Single dropna with shape check |
| No domain term definitions | PheCode, CUI, UMLS defined before first use |
| `!pip install petehr` buried mid-notebook | Moved to NLP section start |
| No transitions between sections | Clear transitions explaining how each step builds |
| No closing summary | "What We Accomplished" + resources |

---

## Critical Files
- `EHR_Preprocessing_4_Cohort_Creation.ipynb` — notebook to refactor
- `EHR_Preprocessing_3_Natural_Language_Processing.ipynb` — upstream NLP notebook (recap)
- `EHR_Preprocessing_2_Code_Rollup.ipynb` — upstream rolled-up data (input source)
- `CLAUDE.md` — rules reference
- `UPDATE_TRACK.md` — update with schema handoff after completion

## Output Schema
```
Codified: patient × PheCode count matrix (subject_id as column, not index)
NLP: patient × CUI count matrix (subject_id as column, not index)
```
Saved to: `processed_data/step5_cohort_aggregateddata/codified/` and `.../nlp/`

---

## Change Checklist

### Critical Fixes (CLAUDE.md Violations)
- [x] Remove absolute path → single `base_dir` with relative path
- [x] Add Goal statement at top
- [x] Add recap of previous notebooks (0-3)
- [x] Add external notebook links at start and end
- [x] Break 30-line mega cell into one-step-per-cell sandwich format
- [x] Enforce sandwich format on all code cells
- [x] Enforce one logical step per code cell
- [x] Enforce max 5-10 lines per code cell
- [x] Add `df.shape` before/after every merge and dedup
- [x] Define domain terms (PheCode, CUI, UMLS, ONCE) before first use
- [x] Fix CSV save to include subject_id column
- [x] Comment the "why" not the "what"

### Structural Fixes
- [x] Add Section 2: "What Is Cohort Creation?" conceptual intro
- [x] Add transitions between all sections
- [x] Add explanations after every code output
- [x] Process all 4 codified data types (Diagnoses, Procedures, Medications, Labs)
- [x] Teach-then-abstract: walk through Diagnoses inline, then wrap into function for the rest
- [x] Remove redundant `dropna` calls, add shape checks
- [x] Move `!pip install petehr` to NLP section start
- [x] Add data completeness discussion (73% note coverage)
- [x] Add validation section verifying output files
- [x] Add "What We Accomplished" closing summary
- [x] Add resources section (ONCE, KESER, NILE)

### Verification
- [ ] Run all cells top-to-bottom in clean kernel
- [x] No absolute paths remain
- [x] All non-function code cells <= 10 lines
- [x] Sandwich format on every code cell
- [x] `df.shape` printed around merges/dedups
- [x] No for-loops on DataFrames (only for I/O batch loading)
- [x] Output CSVs include subject_id as a column
- [x] UPDATE_TRACK.md updated with schema handoff
