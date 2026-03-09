# EHR_Preprocessing_Getting_Started Subplan

## Context
The Getting Started notebook was refactored to be world-class, beginner-friendly, and fully CLAUDE.md compliant. Three refactoring passes were completed: compliance fixes, sandwich format fix, and beginner simplification.

## Final Notebook Structure (68 cells)

### Section 0: Front Matter (cells 0-4)
1. **Title** — Fixed `<h4>...</h3>` → `<h4>...</h4>`
2. **Goal, Assumptions & Data Limits** (NEW)
3. **External notebook link** (NEW, placeholder URL)
4. **Tutorial Structure & Prerequisites** — Fixed "three" → "four" parts
5. **Gaining Access to MIMIC-IV**

### Section 1: Environment Setup (cells 5-11)
6. **Setting Up Compute Environment** — Directory tree + bash script
7. **Import Libraries & Define `base_dir`** — Simplified (no heapq, no defaultdict)
8. **Unzip Data** — Uses `base_dir`, explained `!` shell escape
9. **Create Summary Directory**

### Section 2: Understanding EHR Data (cells 12-16)
10. **What Data Is Available?** — Fixed "date" → "data" typo
11. **Which Data Elements Are Relevant?**
12. **How Is Data Linked?** — With diagram attachment
13. **Domain Terms Glossary** (NEW) — ICD, HCPCS, NDC, ITEMID + `d_` prefix explained

### Section 3: Exploring Patient Demographics (cells 17-27)
14-20. Load → describe (with string output explanation) → interpret → age chart → gender chart → interpret

### Section 4: Step-by-Step Diagnoses Analysis (cells 28-47)
- **Step 1:** Load diagnoses
- **Step 2:** describe() with string column explanation
- **Step 3:** Top 5 codes using `value_counts().head(5)`
- **Step 4:** Patient counts using `groupby().nunique()`
- **Step 5:** Merge with data dictionary (with `df.shape`)
- **Step 6:** Word cloud (simple `zip` loop)
- ICD transition note

### Section 5: Building Reusable Function (cells 48-51)
- Why batch processing is needed (labs = 100M+ rows)
- `summarize_ehr_table` — 1 clear function, simple parameters

### Section 6: Apply to Remaining Data Types (cells 52-64)
- HCPCS, ICD Procedures, Prescriptions (with on-the-fly dict), Labs (15M batch size)

### Section 7: Closing (cells 65-67)
- Output files table, What We Accomplished, external link

---

## Change Checklist

### Critical Fixes (CLAUDE.md Violations)
- [x] Remove ALL absolute paths → single `base_dir`
- [x] Add Goal/Assumptions/Data Limits at top
- [x] Add external notebook links at start and end
- [x] Break oversized cells (120-line function → 1 simpler function; 20-line demographics → 5 cells)
- [x] Remove duplicate `get_basic_summary` definition
- [x] Replace `iterrows()` for-loop with simple `zip` loop
- [x] Add `df.shape` before/after merges and deduplications
- [x] Remove unused `file_line_count` function
- [x] Enforce sandwich format on all 22 code cells
- [x] Enforce one logical step per code cell

### Structural Fixes
- [x] **Teach-then-abstract flow** — Step-by-step diagnoses walkthrough, then wrap into function
- [x] Consolidated 3 functions → 1 (`summarize_ehr_table`)
- [x] Fix "three parts" → "four parts"
- [x] Single `base_dir` and `summary_dir` definitions
- [x] Domain terms glossary with `d_` prefix explanation

### Beginner Simplification (Pass 3)
- [x] Remove `defaultdict(lambda: defaultdict(int))` → use `groupby().nunique()`
- [x] Remove `heapq.nlargest` → use `value_counts().head(5)`
- [x] Remove `dict(zip(...))` → use explicit `for` loop with comments
- [x] Replace `code_cols` dict pattern → simple `code_col` + optional `code_version_col`
- [x] Remove `heapq` and `defaultdict` from imports
- [x] Add explanations: describe() on strings, `!` prefix, `d_` convention, batch rationale, double dedup

### Minor Fixes
- [x] Fix HTML `<h4>...</h3>` → `<h4>...</h4>`
- [x] Fix typos: "discrepancy", "data contained", "four parts"
- [x] Consolidate imports in single cell
- [x] Clean up gender chart color logic (`.map()`)
- [x] Create `requirements.txt`

---

## Verification
- [ ] Run all cells top-to-bottom in clean kernel
- [x] No absolute paths remain
- [x] All non-function code cells ≤ 10 lines
- [x] Sandwich format on every code cell
- [x] `df.shape` printed around merges
- [x] No for-loops on DataFrames
- [x] No advanced patterns (defaultdict, heapq, lambda, iterrows)
- [x] 10 output files produced (patient_counts + wordcloud per data type)
- [ ] User to provide GitHub repo URL for external links
