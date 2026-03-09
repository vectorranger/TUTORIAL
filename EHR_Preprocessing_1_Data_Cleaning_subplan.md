# EHR_Preprocessing_1_Data_Cleaning Subplan

## Context
The Data Cleaning notebook transforms raw MIMIC-IV data (diagnoses, procedures, medications, labs) into a standardized four-column schema (`subject_id`, `date`, `code`, `coding_system`) saved as patient-level batch CSVs. The current notebook has significant CLAUDE.md violations: hardcoded absolute paths, 6+ functions defined before the reader sees the logic, oversized cells (150+ line function block), missing sandwich format, no goal/recap, and no output validation.

## Proposed Logical Flow (~55 cells)

### Section 0: Front Matter (4 cells)
- Title + Author (fix `<h4>...</h3>` tag mismatch)
- **Goal statement**: what this notebook accomplishes and the target output schema
- **Recap**: link back to Getting Started (3 key data elements, data exploration)
- **External notebook link** (placeholder URL)

### Section 1: Setup (3 cells)
- Imports (pandas, os, tqdm only — remove logging, time, sys, clear_output)
- `base_dir` using relative path (NOT absolute)
- Create output directory

### Section 2: What Data Cleaning Involves (2 cells)
- Explain the 5 cleaning sub-steps and why each matters
- **Reference table**: the 5 datasets we'll clean, their source files, code/date columns, and coding_system labels

### Section 3: Step-by-Step Walkthrough on Diagnoses (~16 cells)
Walk through every cleaning step inline before defining any function.

**3a: Load the Data (3 cells)** — Load diagnoses + admissions, explain why merge is needed (timestamps in separate file)

**3b: Assess Missingness (3 cells)** — Check nulls in both tables, interpret results

**3c: Filter Columns and Merge (4 cells)** — Merge on subject_id + hadm_id, print df.shape before/after, check nulls post-merge, drop nulls

**3d: Standardize Schema (3 cells)** — Truncate dates to YYYY-MM-DD, rename columns to standard names, add coding_system column (ICD + version)

**3e: Remove Duplicates (3 cells)** — Print shape before/after drop_duplicates, explain why we deduplicate twice (now + after code rollup)

### Section 4: Why Batch Processing? (3 cells)
- Explain motivation BEFORE showing function (labs = 158M rows)
- Load admissions, extract unique patients, assign batch numbers 1-8 using modulo
- Display patient counts per batch

### Section 5: Building the Reusable Cleaning Function (3 cells)
- Transition: "We now wrap the walkthrough steps into a single function"
- ONE function: `clean_data_by_batch()` with named parameters (not opaque dict)
- Explain parameters and how `code_version_col` works

**Function signature:**
```python
def clean_data_by_batch(input_file_path, output_dir, patient_batches,
                        code_col, date_col, coding_system_label,
                        code_version_col=None, chunk_size=15_000_000):
```

### Section 6: Clean Diagnoses (3 cells)
- Explain diagnoses pre-merge requirement (timestamps in separate file)
- Merge diagnoses + admissions, save to temp CSV
- Call `clean_data_by_batch()` with diagnoses parameters

### Section 7: Clean Procedures (5 cells)
- Explain two sources: HCPCS (CPT billing codes) + ICD procedure codes
- Sample + clean HCPCS
- Sample + clean ICD procedures

### Section 8: Clean Medications (3 cells)
- Explain NDC codes + starttime as timestamp
- Sample + clean prescriptions

### Section 9: Clean Labs (4 cells)
- Explain this is the largest dataset (158M+ rows), will take ~30 minutes
- Sample + clean labevents
- Note on parallelization for HPC users

### Section 10: Validation and Summary (5 cells) — NEW
- Verify all expected batch files exist (8 batches x 5 data sources)
- Load one sample batch per data type, verify column schema
- Summary table of row counts per data type
- Output directory tree

### Section 11: Closing (3 cells)
- "What We Accomplished" bullet summary
- "A Note on Erroneous Data" — move commented-out date filtering here as prose (explain when it applies in real-world data, not needed for MIMIC)
- External notebook link + teaser for Code Rollup

---

## Key Technical Changes

### Functions: 7 → 1
**DELETE:** `setup_logger`, `print_and_log_cleaning`, `missing_values_summary`, `clean_data`, `clean_data_batch_supportfunc`, `file_line_count`
**REWRITE:** `clean_data_by_batch` — simplified with named params, no logging, no dict-of-dicts

### Pattern Simplifications
| Current (advanced) | Refactored (beginner-friendly) |
|---|---|
| `dict(zip(patient_ids['subject_id'], patient_ids['batch_num']))` | `chunk.merge(patient_batches, on='subject_id')` |
| `cols_of_interest = {"patient_id": "subject_id", "date": "admittime", ...}` | Named params: `code_col="icd_code", date_col="admittime"` |
| `[item for key, item in cols_of_interest.items() if item is not None and key != "coding_system"]` | Explicit list: `usecols = ["subject_id", date_col, code_col]` |
| `print_and_log_cleaning(message)` | `print(message)` |
| `clear_output(wait=True); display(...)` | `print(...)` / `display(...)` |

### Other Fixes
- Absolute path → relative `base_dir`
- Fix `<h4>...</h3>` → `<h4>...</h4>`
- Add df.shape before/after every merge and dedup
- Sandwich format on every code cell
- Max 5-10 lines per code cell
- One logical step per code cell

---

## Critical Files
- `EHR_Preprocessing_1_Data_Cleaning.ipynb` — notebook to refactor
- `EHR_Preprocessing_Getting_Started.ipynb` — pattern reference
- `EHR_Preprocessing_2_Code_Rollup.ipynb` — downstream consumer (verify output schema compatibility)
- `CLAUDE.md` — rules reference
- `UPDATE_TRACK.md` — update with schema handoff after completion

## Output Schema (must preserve for downstream)
```
subject_id (str) | date (str, YYYY-MM-DD) | code (str) | coding_system (str)
```
Saved to: `processed_data/step3_cleaned_rawdata/{DataType}/{datatype}_batch{N}_{source}.csv`

---

## Change Checklist

### Critical Fixes (CLAUDE.md Violations)
- [x] Remove absolute path → single `base_dir` with relative path
- [x] Add Goal statement at top
- [x] Add recap of previous notebook
- [x] Add external notebook links at start and end
- [x] Fix HTML `<h4>...</h3>` → `<h4>...</h4>`
- [x] Break 150+ line function cell into teach-then-abstract flow
- [x] Enforce sandwich format on all code cells
- [x] Enforce one logical step per code cell
- [x] Enforce max 5-10 lines per code cell
- [x] Add `df.shape` before/after every merge and dedup
- [x] Replace `dict(zip(...))` with merge-based batch filtering
- [x] Replace opaque `cols_of_interest` dict with named parameters
- [x] Remove logging infrastructure (setup_logger, print_and_log_cleaning)
- [x] Consolidate 7 functions → 1 (`clean_data_by_batch`)
- [x] Comment the "why" not the "what"

### Structural Fixes
- [x] Move batch processing explanation BEFORE function definition
- [x] Add transitions between sections
- [x] Add explanations for procedures/medications/labs (currently bare)
- [x] Move erroneous data discussion to closing appendix (not commented-out code)
- [x] Add validation section with output file verification

### Verification
- [ ] Run all cells top-to-bottom in clean kernel
- [ ] No absolute paths remain
- [ ] All non-function code cells <= 10 lines
- [ ] Sandwich format on every code cell
- [ ] `df.shape` printed around merges/dedups
- [ ] No for-loops on DataFrames
- [ ] No advanced patterns (dict(zip), complex comprehensions)
- [ ] Output schema matches: subject_id, date, code, coding_system
- [ ] 40 batch files produced (8 batches x 5 sources)
- [ ] UPDATE_TRACK.md updated with schema handoff
