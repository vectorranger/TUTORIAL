# CLAUDE.md

This file provides strict guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an **EHR (Electronic Health Record) Preprocessing Tutorial** using MIMIC-IV 3.1 data. It consists of a series of Jupyter notebooks walking through the end-to-end process of cleaning, standardizing, and analyzing clinical data for research purposes. The author is Vidul Ayakulangara Panickan.

## Project Role
You are generating a world-class, beginner-friendly EHR data processing and NLP tutorial. In all interactions and commits, be concise, direct, and technically precise. Maintain readable, grammatically correct prose for all plain English explanations, but avoid fluff. 

## Infrastructure & Setup Rules
* Write download scripts handling PhysioNet authentication (e.g., `wget` with credential flags or the `wfdb` package).
* Ensure a universal environment setup with an outputted `requirements.txt`.
* Provide a clear "Introductory Setup" for local Mac and Windows environments.
* Create a distinctly separate "Advanced Module" containing SLURM sbatch templates for HPC job scheduling and scaling.
* Use relative paths or a single `base_dir` variable exclusively. NEVER use absolute paths.

## Tutorial Structure Rules
* State the goal, clinical assumptions (e.g., inferred dates), and data limits at the very top of each notebook.
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