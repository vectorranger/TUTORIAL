# CLAUDE.md

This file provides strict guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an **EHR (Electronic Health Record) Preprocessing Tutorial** using MIMIC-IV 3.1 data. It consists of a series of Jupyter notebooks walking through the end-to-end process of cleaning, standardizing, and analyzing clinical data for research purposes. The author is Vidul Ayakulangara Panickan.

## Notebook Pipeline

1. **Getting_Started** - Workspace setup, MIMIC-IV data download/unzip, data exploration and summarization
2. **1_Data_Cleaning** - Assess missingness, filter columns, standardize schema , remove duplicates. Processes in patient-level batches
3. **2_Code_Rollup** - Map granular EHR codes to standardized parent codes 
4. **3_Natural_Language_Processing** - Convert clinical notes to UMLS CUI codes using dictionary-based NLP (petehr library). 
5. **4_Cohort_Creation** - Define patient cohorts, extract and aggregate data into patient-level count matrices for both codified and NLP features

## Project Role
You are generating a world-class, beginner-friendly EHR data processing and NLP tutorial. In all interactions and commits, be concise, direct, and technically precise. Maintain readable, grammatically correct prose for all plain English explanations, but avoid fluff.

## Language Refactoring Rules
* Adopt an encouraging, action-oriented tutorial tone that explains technical concepts in plain English and prioritizes the "why" behind every step.
* Lead each section with what the reader will learn or accomplish, not just what the code does.
* After every code cell output, explain what the result means and why it matters for the analysis — do not let outputs speak for themselves.
* Use phrases like "We do this because…", "Notice that…", "This tells us…" to connect code to understanding.
* Avoid jargon without definition. When a technical term first appears, define it in one sentence before using it in code.
* Write transitions between sections so the reader understands how each step builds on the last.

## Code Refactoring Rules
* **Teach then abstract:** When introducing a new operation, first walk through each step inline with a concrete example, then wrap the proven steps into a reusable function. Never show a function before the reader has seen the logic it encapsulates.
* **Avoid advanced Python patterns.** Use simple, readable alternatives:
    - Regular dicts and `if` checks instead of `defaultdict`
    - `sorted(..., reverse=True)[:N]` or `value_counts().head(N)` instead of `heapq.nlargest`
    - Explicit `for` loops with clear variable names instead of `dict(zip(...))` one-liners
    - Named parameters instead of opaque dicts (e.g., `code_col="icd_code"` not `code_cols={"code": "icd_code"}`)
* **Minimize function count.** Prefer one clear, well-commented function over multiple small abstractions. Each function should map to a concept the reader already understands from the inline walkthrough.
* **Comment the "why", not the "what."** Add inline comments only where the reason behind a line is not obvious (e.g., why we deduplicate twice, why we read in batches).

## Infrastructure & Setup Rules
* Write download scripts handling PhysioNet authentication (e.g., `wget` with credential flags or the `wfdb` package).
* Ensure a universal environment setup with an outputted `requirements.txt`.
* Provide a clear "Introductory Setup" for local Mac and Windows environments.
* Create a distinctly separate "Advanced Module" containing SLURM sbatch templates for HPC job scheduling and scaling.
* Use relative paths or a single `base_dir` variable exclusively. NEVER use absolute paths.

## Tutorial Structure Rules
* State the goal the very top of each notebook.
* Provide a one-paragraph recap of the previous notebook at the start of each new notebook, if applicable.
* Maintain a logical flow of concepts so the user does not get lost.
* Use conceptual headings (e.g., "Removing Redundant Data"), rather than raw function names.
* Define domain terms (PheCode, CUI, UMLS) in plain English before writing the associated code.
* Link to the full external executable notebook at the start and end (format: `github_repo/TUTORIAL/notebook_name`).

## Code Presentation Rules
* Write clean, organized, human-understandable code using naming conventions that are intuitive for beginners.
* Limit code blocks to a maximum of 5-10 lines. 
* Execute strictly one logical transformation or analytical step per code block.
* Use the "sandwich format" for all code cells: 1. Short plain English explanation -> 2. Hero code -> 3. Output table/shape.

## Pandas & Data Engineering Rules
* Expose logic step-by-step using vectorization. 
* Strictly use zero `for` loops for data manipulation (loops are only permitted for I/O operations or plotting).
* Treat dates as strings during initial processing to keep logic straightforward, and cast medical codes to strings to avoid merge failures.
* Print `df.shape` immediately before and after every merge or deduplication step.
* Explicitly code validation checks, create flags, filter data, and count unmapped codes.

## Downstream Analysis Rules
* Demonstrate longitudinal to cross-sectional transformations using `groupby` and `pivot_table`.
* Calculate exact, highly specific metrics (e.g., answering "how many times did each specific CUI appear for a patient in a given month?").
* Explain all chart outputs and matrix results in plain English.

## State Management & Context Handoff Rules
Because this pipeline spans multiple notebooks with evolving schemas, you MUST rely on `UPDATE_TRACK.md` for state tracking to avoid context degradation.
* **Initialization:** At the start of any prompt or session, silently read `UPDATE_TRACK.md` to understand the current progress, upstream schema dependencies, and active notebook.
* **Completion Protocol:** When you finish processing a notebook according to its `[Notebook name]_subplan.md`, you must update `UPDATE_TRACK.md` by:
    1. Adding a high-level summary of the transformations applied.
    2. Documenting the exact schema handoff (final DataFrame shapes, new column names, and data types).
    3. Marking the notebook's subplan with `[x]`.
    4. Pushing to Github
* **Context Wipe Enforcement:** After updating `UPDATE_TRACK.md`, you must STOP execution entirely and output the following exact message to the user: *"Notebook complete and tracker updated. Please run `/clear` in your terminal to wipe my context window before we begin the next notebook."*
* **Resumption:** When the user provides the next prompt after a `/clear`, you must load the newly updated schemas from `UPDATE_TRACK.md` before writing any new downstream code.

## Subplan Initiation Trigger
When the user says "create [Notebook Name] Subplan", you must:
1.  **Enter Plan Mode:** Create a temporary file called `[Notebook Name]_subplan.md`.
2.  Read the notebook, understand the content, structure of the notebook
3. **Brainstorm:** Ask me clarifying questions about the target audience, setup requirements, and any gaps in the current draft. 
4.  **Propose a logical flow:** Outline a new structure on how the content should be organized for better clarity and understand for new users
5. Ensure the refactored notebook sticks to the best practcies mentions in CLAUDE.md for this project.
5. After a plan is devised, go through the plan again and list any unresolved questions to answer
6. **Wait for Approval:** Present the plan to the user and wait for a "Go" before writing any code.
7. Make a checklist of changes, updates need to be made.
8. As updates are being made, keep track of it by adding [X] next to it
9. After each update, push to Github