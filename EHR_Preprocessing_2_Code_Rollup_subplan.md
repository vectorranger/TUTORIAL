# EHR_Preprocessing_2_Code_Rollup Subplan

## Context
The Code Rollup notebook maps granular EHR codes (ICD, CPT, NDC, ITEMID) to standardized parent codes (PheCode, CCS, RxNorm, LOINC Component). It takes the cleaned four-column data from Notebook 1 and produces rolled-up batch files with a three-column schema (`subject_id`, `date`, `parent_code`). The current notebook has significant CLAUDE.md violations and structural problems that make it hard for beginners to follow.

## Current Problems

### CLAUDE.md Violations
- **Hardcoded absolute paths** throughout (6+ occurrences of `/n/data1/hsph/...`)
- **Functions before logic** — 4 mapping-generation functions (`roll_icd2phe`, `roll_cpt2ccs`, `roll_icd_procedures_to_ccs`, `roll_ndc2rxnorm`) are shown before the reader understands what they do
- **No Goal statement** at the top
- **No recap** of previous notebook
- **No sandwich format** — code cells lack pre-explanation and post-interpretation
- **Oversized code cells** — Cell 28 is 90+ lines containing 4 functions
- **Advanced Python patterns**: `dict(zip(...))` in NDC mapping, `lambda` expressions, `itertuples` loop
- **Duplicate imports** — `import os` appears in cells 2, 4, 10, 14, 28
- **`clear_output(wait=True)`** hides intermediate progress from the reader
- **No transitions** between sections — jumps from mapping creation to rollup execution without explanation
- **No validation/verification** section at the end
- **Unused imports**: `sys`, `time`, `logging` carried over from Data Cleaning

### Structural Problems
- The notebook does TWO distinct things (create mapping files + perform rollup) but doesn't clearly separate or motivate them
- Diagnoses rollup is done TWICE — once inline as a walkthrough (cells 17-26), then again via the function (cells 30-31). The teach-then-abstract pattern is good in principle but the current execution is confusing
- The "Defining Functions" section (cell 27-28) appears abruptly mid-notebook with no transition
- Cell 28 defines `rollup`, `summarize_unmapped`, `filter_rolledup_data`, and `rollup_data_by_batch` all at once — 4 functions in a single cell
- Procedure rollup requires 3 mapping files (CPT→CCS, ICD-10-PCS→CCS, ICD-9-CM→CCS) merged into one — this complexity is not explained to the reader
- NDC→RxNorm mapping requires downloading RXNSAT.RRF from UMLS — prerequisite not clearly stated

## Proposed Logical Flow (~60 cells)

### Section 0: Front Matter (4 cells)
- Title + Author
- **Goal**: Map granular EHR codes to clinically meaningful parent codes for downstream analysis
- **Recap**: Link back to Data Cleaning — we cleaned 5 data sources into a standard schema (`subject_id`, `date`, `code`, `coding_system`), saved as 8 patient-level batches
- External notebook link

### Section 1: Setup (3 cells)
- Imports: `pandas`, `os`, `tqdm`, `glob`, `zipfile`, `urllib.request` only
- `base_dir` using relative path
- Create output directories (`step4_rolledup_intermediatedata`, `step4_rolledup_finaldata`)

### Section 2: What is Code Rollup? (3 cells)
- Explain WHY we roll up: granular codes → sparse data, hard to compare across institutions
- Two-step process: (1) normalize to standard vocabulary, (2) aggregate to parent codes
- **Reference table** showing the 4 rollup pipelines:

| Data Type | Raw Code System | Standard Code | Parent Code | Mapping Source |
|-----------|----------------|---------------|-------------|----------------|
| Diagnoses | ICD-9/ICD-10 | (already standard) | PheCode | PheWAS Catalog |
| Procedures | CPT, ICD-9-CM, ICD-10-PCS | (already standard) | CCS | HCUP |
| Medications | NDC | RxNorm | RxNorm Ingredient | UMLS/RxNorm |
| Labs | ITEMID (local) | LOINC | LOINC Component | MIMIC-provided + LOINC hierarchy |

- Note about codebooks (keep existing note about master mapping files)

### Section 3: Part 1 — Creating Rollup Mapping Files (heading cell)
- Brief explanation: before we can roll up, we need mapping tables that translate each raw code to its parent code

### Section 3a: Diagnoses Mapping — ICD to PheCode (~5 cells)
- Explain ICD and PheCode in plain English (keep existing good definitions)
- Download the PheWAS Catalog mapping file
- **Inline walkthrough**: load the CSV, show what it looks like, filter for ICD-9/ICD-10, normalize codes (remove dots), rename columns
- Wrap into `roll_icd2phe()` function — but SIMPLER than current (no chained `.loc` operations)
- Show sample output (first 10 rows)

### Section 3b: Procedures Mapping — CPT/ICD to CCS (~7 cells)
- Explain CPT codes and CCS in plain English (keep existing definitions)
- **CPT → CCS**: download HCUP file, show the range-expansion logic inline first, then function
- **ICD Procedures → CCS**: download ICD-10-PCS and ICD-9-CM files, explain two procedure code systems, create mapping
- **Merge** CPT and ICD procedure mappings into a single `HCPCS_ICDPROC_to_CCS.csv`
- Show combined output

### Section 3c: Medications Mapping — NDC to RxNorm (~5 cells)
- Explain NDC and RxNorm in plain English
- **PREREQUISITE callout**: downloading RXNSAT.RRF from UMLS requires a UMLS account — explain how to get it
- Walk through the mapping logic: filter RXNSAT for NDC rows → map to ingredient level
- Show sample output
- Simplify: replace `dict(zip(...))` with merge, remove lambda

### Section 3d: Labs Mapping — ITEMID to LOINC Component (~4 cells)
- Explain ITEMID (MIMIC-local) vs LOINC (standard) vs LOINC Component (parent)
- Load MIMIC-provided `lab_itemid_to_loinc.csv` + `LOINC_Hierarchy` file
- Merge to create ITEMID → LOINC Component mapping
- Show sample output + note about low LOINC coverage in MIMIC

### Section 4: Part 2 — Performing the Rollup (heading cell)
- Transition: "Now that we have mapping files for all four data types, we can apply them to our cleaned data from Notebook 1."

### Section 4a: Step-by-Step Walkthrough — Diagnoses Rollup (~8 cells)
- Load one sample batch of cleaned diagnoses data
- Load the ICD→PheCode mapping
- **Inline walkthrough**:
  1. Left-merge cleaned data with mapping on `code` + `coding_system`, print shape before/after
  2. Add `Rollup_Status` flag, show output
  3. Inspect unmapped codes — explain what they are and why they exist
  4. Filter to only rolled-up rows, keep `subject_id`, `date`, `PheCode`
  5. Deduplicate, print shape before/after
- Explain what each step accomplished

### Section 4b: Building the Reusable Rollup Function (~3 cells)
- Transition: "We'll now wrap these steps into reusable functions for the remaining data types"
- **ONE function**: `rollup_data_by_batch()` — simplified with named parameters
  - Remove `clear_output(wait=True)` — use `tqdm` progress bar instead
  - Remove nested `base_directory` hardcoding inside function
  - Use named parameters instead of config dict: `rollup_data_by_batch(input_dir, output_dir, rollup_mapping, parent_col, child_col, ...)`
- **ACTUALLY**: keep the config dict approach since it's already in use and makes calling cleaner, BUT use named keys that match column purposes

### Section 4c: Roll Up All Diagnoses (2 cells)
- Apply function to all 8 batches
- Show final output shape

### Section 4d: Roll Up Procedures (3 cells)
- Explain two sources merged into one mapping
- Apply function, show output

### Section 4e: Roll Up Medications (3 cells)
- Apply function, show output

### Section 4f: Roll Up Labs (3 cells)
- Note about low LOINC coverage
- Apply function, show output

### Section 5: Validation and Summary (~5 cells)
- Verify all expected output files exist (8 batches × 4 data types = 32 files in `step4_rolledup_finaldata`)
- Load one sample file per data type, verify schema
- Summary table of row counts per data type (before vs after rollup)
- Output directory tree

### Section 6: Closing (3 cells)
- "What We Accomplished" bullet summary
- Output schema handoff for Notebook 3
- Next Step link → NLP notebook

---

## Key Technical Changes

### Functions: 8 → 4 (max)
**Mapping generation (keep but simplify):**
- `roll_icd2phe` — simplify chained operations
- `roll_cpt2ccs` — keep (the range-expansion logic is inherently procedural)
- `roll_icd_procedures_to_ccs` — simplify, remove `_normalize_cols` inner function
- `roll_ndc2rxnorm` — replace `dict(zip(...))` with merge, remove lambda

**Rollup execution (consolidate):**
- Current: `rollup`, `summarize_unmapped`, `filter_rolledup_data`, `rollup_data_by_batch` (4 functions)
- Refactored: `rollup_data_by_batch` (1 function that does everything inline)

### Pattern Simplifications
| Current (advanced) | Refactored (beginner-friendly) |
|---|---|
| `dict(zip(ing['base'], ing['ingredient']))` + `lambda x: base2ing.get(x, x)` | `pd.merge(table, ing, left_on='RXCUI', right_on='base', how='left')` |
| `df.apply(lambda s: s.str.strip())` | `df[col] = df[col].str.strip()` per column |
| `itertuples` loop in CPT range expansion | Keep (unavoidable for range expansion) but add clear comments |
| `clear_output(wait=True); display(...)` | `tqdm` progress bar |
| Config dict with opaque keys | Config dict with clearly named keys + comments |
| 4 separate helper functions for rollup | 1 function with inline logic |

### Other Fixes
- 6+ absolute paths → single relative `base_dir`
- Remove duplicate imports (5 import blocks → 1)
- Remove unused imports (`sys`, `time`, `logging`)
- Add `df.shape` before/after every merge and dedup
- Sandwich format on every code cell
- Max 5-10 lines per code cell
- One logical step per code cell
- Add transitions between all sections

---

## Resolved Questions

1. **UMLS/RxNorm**: Provide a pre-built NDC_to_RxNorm.csv in the repo as the default path. Show UMLS download as an optional/advanced step for users who want to build their own mapping.
2. **Intermediate data**: Keep both output tiers (intermediate with rollup status + final filtered).
3. **LOINC coverage**: Note the limitation in plain English but don't show a workaround — just move on.
4. **Teach pattern**: Keep the walk-through + redo approach — teach inline on diagnoses, define function, re-run diagnoses via function to prove it works, then apply to other 3 data types.

---

## Critical Files
- `EHR_Preprocessing_2_Code_Rollup.ipynb` — notebook to refactor
- `EHR_Preprocessing_1_Data_Cleaning.ipynb` — upstream producer (verify input schema)
- `EHR_Preprocessing_3_Natural_Language_Processing.ipynb` — downstream consumer
- `CLAUDE.md` — rules reference
- `UPDATE_TRACK.md` — update with schema handoff after completion

## Input Schema (from Notebook 1)
```
subject_id (str) | date (str, YYYY-MM-DD) | code (str) | coding_system (str)
```
Location: `processed_data/step3_cleaned_rawdata/{DataType}/{datatype}_batch{N}_{source}.csv`

## Output Schema
```
subject_id (str) | date (str, YYYY-MM-DD) | {ParentCode} (str)
```
Where `{ParentCode}` is `PheCode`, `CCS`, `RxNorm`, or `LoincComponent` depending on data type.

Location: `processed_data/step4_rolledup_finaldata/{DataType}/rolledup_batch{N}.csv`

---

## Change Checklist

### Critical Fixes (CLAUDE.md Violations)
- [x] Remove all absolute paths → single `base_dir` with relative path
- [x] Add Goal statement at top
- [x] Add recap of previous notebook
- [x] Add external notebook links at start and end
- [x] Break 90+ line function cell (cell 28) into teach-then-abstract flow
- [x] Enforce sandwich format on all code cells
- [x] Enforce one logical step per code cell
- [x] Enforce max 5-10 lines per code cell
- [x] Add `df.shape` before/after every merge and dedup
- [x] Replace `dict(zip(...))` with merge in NDC mapping
- [x] Replace `lambda` with explicit operations
- [x] Remove `clear_output(wait=True)` — use `tqdm` instead
- [x] Remove unused imports (`sys`, `time`, `logging`)
- [x] Consolidate duplicate import blocks → single block
- [x] Consolidate 4 rollup helper functions → 1 (`rollup_data_by_batch`) + 1 small helper (`save_unmapped_summary`)
- [x] Comment the "why" not the "what"

### Structural Fixes
- [x] Add "What is Code Rollup?" conceptual section before any code
- [x] Add reference table of 4 rollup pipelines
- [x] Clearly separate Part 1 (creating mappings) from Part 2 (performing rollup)
- [x] Add transitions between all sections
- [x] Add plain-English definitions for all domain terms (PheCode, CCS, RxNorm, LOINC, NDC, CPT)
- [x] Add UMLS prerequisite callout for NDC→RxNorm
- [x] Add validation section with output file verification
- [x] Add closing summary with output schema handoff

### Verification
- [ ] Run all cells top-to-bottom in clean kernel
- [ ] No absolute paths remain
- [ ] All non-function code cells ≤ 10 lines
- [ ] Sandwich format on every code cell
- [ ] `df.shape` printed around merges/dedups
- [ ] No advanced patterns (dict(zip), complex lambda, comprehensions)
- [ ] Output schema matches: subject_id, date, {ParentCode}
- [ ] 32 batch files produced (8 batches × 4 data types in `step4_rolledup_finaldata`)
- [ ] UPDATE_TRACK.md updated with schema handoff
