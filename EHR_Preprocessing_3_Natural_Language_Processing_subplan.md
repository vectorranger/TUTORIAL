# EHR_Preprocessing_3_Natural_Language_Processing Subplan

## Context
The NLP notebook converts clinical discharge notes into structured UMLS CUI codes using dictionary-based NLP (petehr library). It is purely **pedagogical** — Notebook 4 re-implements the same pattern for a specific cohort. The current notebook has 16 cells with 10 CLAUDE.md violations: absolute path, no goal/recap, 9-operation mega cell, front-loaded alternatives (UMLS vs ONCE), unexplained outputs, undefined tools, lambda with conditional, and missing sandwich format.

## Proposed Logical Flow (~38 cells)

### Section 0: Front Matter (4 cells)
- Title + Author
- **Goal statement**: learn to convert clinical text to UMLS CUIs using dictionary-based NLP; note this is a learning exercise (Notebook 4 applies to real cohort)
- **Recap**: Notebooks 0-2 handled structured/codified data; this notebook unlocks unstructured free-text notes
- **External notebook link**

### Section 1: Setup (2 cells)
- Imports: `os`, `pandas`, `petehr.Text2Code` (with note about `pip install petehr`)
- `base_dir` + path variables for note_dir and meta_dir (relative paths, NO absolute)

### Section 2: Key Concepts (4 cells)
Define all jargon BEFORE any code uses it:
- **What is UMLS?** — 200+ biomedical vocabularies mapped to single identifiers. Keep the diabetes example table (CUI C0011849 across WHO and SNOMEDCT_US).
- **What is a CUI?** — Concept Unique Identifier. Show clinical note → extracted CUIs example.
- **How do we get CUIs from text?** — Define petehr (educational), mention NILE/cTAKES (production).
- **Where does the dictionary come from?** — Define ONCE (web app for disease-specific dictionaries). Move UMLS-from-scratch to appendix.

### Section 3: Loading the Data (4 cells)
- Load discharge notes, display shape + head
- Interpret: 331K notes, explain key columns (text, charttime, subject_id)
- Sample 1,000 notes (with `random_state=42` for reproducibility)
- Interpret: why we sample, what random_state does

### Section 4: Loading the NLP Dictionary (3 cells)
- Load diabetes dictionary CSV, display shape + head
- Interpret: STR column (terms to match), CUI column (codes), synonym coverage
- Initialize `Text2Code(dict_file)` — explain what this prepares

### Section 5: Running the NLP Conversion (3 cells)
- **Single note demo first** (teach-then-abstract): convert one note, show input text + output CUI string
- Interpret: explain comma-separated CUIs, repeated CUIs, what they mean
- **Convert all 1,000 notes**: `.map(text2cui.convert)` (not lambda), display result

### Section 6: Cleaning and Reshaping (8 cells)
Split the current mega cell into individual steps with sandwich format:
1. Select columns of interest (subject_id, charttime, note_cui)
2. Rename `charttime` → `date` + truncate to YYYY-MM-DD
3. Drop nulls (notes where NLP found no matches) — print shape before/after
4. Split comma-separated CUI strings into lists — use `.str.split(',')` not lambda
5. Explode to one CUI per row — print shape before/after
6. Deduplicate — print shape before/after, explain why (count presence, not frequency)
7. Interpret: started with 1,000 notes → ~19,000 unique patient-date-CUI combos

### Section 7: Counting CUIs per Patient (3 cells)
- Group by subject_id + CUI, count occurrences
- Display top CUIs
- Interpret: final output schema (subject_id, cui, counts)

### Section 8: Validation (2 cells)
- Print unique patients, unique CUIs, total pairs, top 5 CUIs
- Interpret: what the numbers mean

### Section 9: Closing (3 cells)
- "What We Accomplished" — 5 bullet summary + reminder that Notebook 4 applies the pattern
- "Next" teaser for Cohort Creation notebook
- External notebook link

### Section 10: Appendix (1 cell)
- Building a UMLS dictionary from scratch (moved from current cells 9-10, trimmed)

---

## Key Technical Changes

| Current | Refactored |
|---------|------------|
| Absolute path `/n/data1/hsph/...` | Relative `base_dir` |
| 9-operation mega cell (~40 lines) | 6 separate cells, one operation each |
| `lambda x: x.split(',') if x else None` | `.str.split(',')` after `.dropna()` |
| `.map(lambda x: text2cui.convert(x))` | `.map(text2cui.convert)` |
| UMLS vs ONCE front-loaded before code | ONCE inline, UMLS in appendix |
| No `random_state` on sample | `random_state=42` for reproducibility |
| petehr undefined | Defined before first use |
| CUI output unexplained | Single-note demo + interpretation |
| No function wrapping | None needed (single data type) |

---

## Critical Files
- `EHR_Preprocessing_3_Natural_Language_Processing.ipynb` — rewrite
- `EHR_Preprocessing_4_Cohort_Creation.ipynb` — verify NLP pattern is independently implemented
- `CLAUDE.md` — rules reference
- `UPDATE_TRACK.md` — update after completion

---

## Change Checklist

### Critical Fixes (CLAUDE.md Violations)
- [ ] Remove absolute path → relative `base_dir`
- [ ] Add Goal statement at top (including pedagogical purpose callout)
- [ ] Add recap of previous notebooks
- [ ] Add external notebook links at start and end
- [ ] Split 9-operation mega cell into 6 individual cells
- [ ] Replace lambda-with-conditional with `.str.split(',')`
- [ ] Replace `.map(lambda ...)` with `.map(text2cui.convert)`
- [ ] Enforce sandwich format on all code cells
- [ ] Enforce one logical step per code cell
- [ ] Enforce max 5-10 lines per code cell
- [ ] Print df.shape before/after dropna, explode, and dedup
- [ ] Define UMLS, CUI, petehr, ONCE before first use in code
- [ ] Move UMLS-from-scratch to appendix (not front-loaded)

### Structural Fixes
- [ ] Add single-note demo before processing all notes (teach-then-abstract)
- [ ] Add output interpretations after every code cell
- [ ] Add transitions between sections
- [ ] Add `random_state=42` to sample for reproducibility
- [ ] Add validation section
- [ ] Explicitly state output is not consumed downstream

### Verification
- [ ] Run all cells top-to-bottom in clean kernel
- [ ] No absolute paths remain
- [ ] All code cells ≤ 10 lines
- [ ] Sandwich format on every code cell
- [ ] df.shape printed around dropna/explode/dedup
- [ ] No advanced patterns (lambda with conditional)
- [ ] Output schema: subject_id, cui, counts
- [ ] UPDATE_TRACK.md updated with schema handoff
