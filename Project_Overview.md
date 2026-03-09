# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an EHR (Electronic Health Record) preprocessing tutorial built as a series of Jupyter notebooks. It demonstrates a complete pipeline for processing MIMIC-IV clinical data, from raw EHR records to analysis-ready patient-level feature matrices.

## Notebook Pipeline

The notebooks must be run in order, as each produces outputs consumed by the next:

1. **Getting_Started** - Workspace setup, MIMIC-IV data download/unzip, data exploration and summarization
2. **1_Data_Cleaning** - Assess missingness, filter columns, standardize schema (`subject_id`, `date`, `code`, `coding_system`), remove duplicates. Processes in patient-level batches (8 batches by default)
3. **2_Code_Rollup** - Map granular EHR codes to standardized parent codes (ICD→PheCode for diagnoses, NDC→RxNorm ingredient for meds, CPT/HCPCS/ICD-PCS→CCS for procedures, ITEMID→LOINC component for labs). Uses mapping files from `Rollup_Mappings/` directory
4. **3_Natural_Language_Processing** - Convert clinical notes to UMLS CUI codes using dictionary-based NLP (petehr library). Uses term-CUI dictionaries from ONCE app stored in `meta_files/`
5. **4_Cohort_Creation** - Define patient cohorts (e.g., asthma via PheCode 495), extract and aggregate data into patient-level count matrices for both codified and NLP features

## Key Data Conventions

- All data is loaded with `dtype=str` to prevent type coercion issues (especially with medical codes like ICD that have leading zeros)
- Cleaned data follows a standard schema: `subject_id`, `date`, `code`, `coding_system`
- Timestamps are truncated to date-only (`str[:10]`) unless working with time-series data
- MIMIC-IV identifiers: `subject_id` (patient), `hadm_id` (hospital admission), `stay_id` (ICU stay)
- ICD-9 and ICD-10 codes coexist in the data (transition date: Oct 1, 2015); both must be included for studies spanning this period

## Workspace Structure

The notebooks expect a workspace at a configurable `base_directory` (set via `LOCATION` variable) with this layout:

```
EHR_TUTORIAL_WORKSPACE/
├── raw_data/structured_data/physionet.org/files/mimiciv/3.1/hosp/   # MIMIC-IV hosp CSVs
├── raw_data/note_data/physionet.org/files/mimic-iv-note/2.2/note/  # Clinical notes
├── processed_data/
│   ├── Summary/                    # Generated summaries and wordclouds
│   ├── step3_cleaned_rawdata/      # Cleaned batched CSVs (Diagnoses/, Labs/, Medication/, Procedures/)
│   ├── step4_rolledup_finaldata/   # Code-rolled-up batched CSVs
│   └── step5_cohort_aggregateddata/  # Final patient-level matrices (codified/ and nlp/)
└── scripts/EHR-Processing-Tutorial-main/
    ├── meta_files/                 # NLP dictionaries (ONCE exports)
    └── Rollup_Mappings/            # Code rollup mapping files (icd_to_phecode.csv, etc.)
```

## Environment

- **Conda env**: `ehr_tutorial`
- **Key libraries**: pandas, wordcloud, matplotlib, tqdm, petehr (NLP toolkit)
- **External dependencies**: MIMIC-IV 3.1 access (PhysioNet credentialed), UMLS account for NLP dictionaries

## Processing Patterns

- Large datasets (e.g., labevents with 158M+ rows) are processed in chunked batches using `pd.read_csv(chunksize=...)` and patient-level batching
- The `clean_data_by_batch()` function handles the full cleaning pipeline per batch: filter columns, drop nulls, truncate dates, rename to standard schema, deduplicate, assign coding system
- The `generate_complete_summary()` function provides data profiling: basic stats, top-frequency items, patient-code pair counts, and wordclouds
- Code rollup uses UMLS crosswalks; unmapped codes are retained and flagged for manual review
