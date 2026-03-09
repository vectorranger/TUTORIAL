# EHR_Preprocessing_Getting_Started Subplan

## Context
The Getting Started notebook is the entry point for the entire EHR preprocessing tutorial. It currently has strong content but suffers from CLAUDE.md rule violations (absolute paths, oversized code cells, duplicate function definitions, missing goal/assumptions section) and a redundant flow where diagnoses data is explored manually and then re-processed with the same functions. This refactor will make it world-class, beginner-friendly, and fully compliant.

## Proposed Notebook Structure

### Section 0: Front Matter
1. **Title** - Fix `<h4>...</h3>` tag mismatch
2. **Goal, Assumptions & Data Limits** (NEW) - Required by CLAUDE.md at top of every notebook
3. **Link to external executable notebook** (NEW) - Required at start and end
4. **Tutorial Structure & Prerequisites** - Fix "three parts" → "four parts"
5. **Gaining Access to MIMIC-IV** - Keep as-is

### Section 1: Environment Setup
6. **Setting Up Compute Environment** - Keep directory tree + bash script
7. **Import Libraries & Define `base_dir`** - Single cell, ALL imports, ONE `base_dir` definition (no absolute paths)
8. **Unzip Data** - Use `base_dir` (remove hardcoded absolute path)
9. **Create Summary Directory** - Use `base_dir`

### Section 2: Understanding EHR Data (Conceptual, No Code)
10. **What Data Is Available?** - Module list + data types table. Fix "date contained" → "data contained"
11. **Which Data Elements Are Relevant?** - Key elements table + hosp module table
12. **How Is Data Linked?** - Identifiers + diagram
13. **Domain Terms Glossary** (NEW) - Define ICD, HCPCS/CPT, NDC, ITEMID before code uses them

### Section 3: Exploring Patient Demographics
14. Section header markdown
15. **Load demographics** (sandwich, ~5 lines)
16. **Summary stats & missing values** (sandwich, ~5 lines)
17. Interpretation markdown
18. **Age distribution chart** (sandwich, ~8 lines)
19. **Gender distribution chart** (sandwich, ~8 lines)
20. Demographics interpretation markdown (364,627 patients, 52% female, age spike at 91)

### Section 4: Summarizing EHR Data Tables
21. Section header - "Summarizing the Hosp Module"
22. **Batch processing rationale** markdown
23. **Define `get_basic_summary`** (sandwich, single definition - remove duplicate)
24. **Define `generate_wordcloud`** (sandwich, replace iterrows for-loop with vectorized `dict(zip(...))`)
25. **Define `generate_complete_summary`** (sandwich, with preceding explanation)
26. **Diagnoses: ICD Codes** - ICD-9/ICD-10 explanation markdown
27. **Summarize Diagnoses** code cell
28. Diagnoses interpretation markdown
29. **HCPCS Procedures** markdown
30. **Summarize HCPCS** code cell
31. **ICD Procedures** markdown
32. **Summarize ICD Procedures** code cell
33. **Prescriptions** markdown
34. **Summarize Prescriptions** code cell
35. **Laboratory Tests** markdown
36. **Summarize Labs** code cell
37. **Output Files Summary** markdown

### Section 5: Closing
38. **What We Accomplished / Next Steps** - Preview Data Cleaning notebook
39. **Link to external notebook** (end link)

---

## Change Checklist

### Critical Fixes (CLAUDE.md Violations)
- [x] Remove ALL absolute paths (3+ instances of `/n/data1/...`). Use single `base_dir` variable
- [x] Add Goal/Assumptions/Data Limits cell at notebook top
- [x] Add external notebook links at start and end
- [x] Break 120-line function cell into 3 separate cells (get_basic_summary, generate_wordcloud, generate_complete_summary)
- [x] Break ~20-line demographics cell into separate cells (describe, age chart, gender chart)
- [x] Remove duplicate `get_basic_summary` definition (defined in 2 places)
- [x] Replace `for index, row in df.iterrows()` in wordcloud with `dict(zip(df[col], df['counts']))`
- [x] Add `df.shape` prints before/after merges (in generate_complete_summary and inline merge)
- [x] Remove unused `file_line_count` function
- [x] Enforce sandwich format on all code cells
- [x] Enforce one logical step per code cell

### Structural Fixes
- [x] **Diagnoses flow: "Teach then apply"** — keep brief manual exploration (load, describe, head) as teaching moment, then define functions and call generate_complete_summary on all 5 data types. Remove the inline wordcloud and manual merge-with-dictionary from the manual section
- [x] Define functions BEFORE applying them (move function definitions before generate_complete_summary calls)
- [x] Fix tutorial structure: "three parts" → "four parts"
- [x] Consolidate `base_directory` → `base_dir` — define once, reuse everywhere
- [x] Remove `summary_directory` redefinitions in each summary cell → single `summary_dir`
- [x] Add domain term definitions (ICD, HCPCS, NDC, ITEMID) before code

### Minor Fixes
- [x] Fix HTML: `<h4>...</h3>` → `<h4>...</h4>`
- [x] Fix typos: "descrepency" → "discrepancy", "date contained" → "data contained", etc.
- [x] Remove duplicate imports (imported in 2 cells currently)
- [x] Clean up gender chart color logic (use `.map()` instead of dict comprehension)
- [x] Create standalone `requirements.txt` in repo root (pandas, wordcloud, matplotlib, tqdm, jupyter)

---

## Verification
- [ ] Run all cells top-to-bottom in a clean kernel to confirm no errors
- [x] Confirm no absolute paths remain
- [x] Confirm all non-function code cells are ≤10 lines
- [x] Confirm sandwich format on every code cell
- [x] Confirm df.shape printed around merges
- [x] Confirm no for-loops on DataFrames
- [x] Confirm 16 summary output files are still generated (same generate_complete_summary calls)
- [ ] User to provide GitHub repo URL for external notebook links (placeholder `<GITHUB_REPO_URL>` used)
