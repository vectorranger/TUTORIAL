# EHR Pipeline Update Tracker

## Active Status
* **Current Notebook in Progress:** `EHR_Preprocessing_4_Cohort_Creation.ipynb` (refactoring complete, pending kernel run)

## Subplan Execution Status
- [ ] `EHR_Preprocessing_Getting_Started.ipynb`
- [ ] `EHR_Preprocessing_1_Data_Cleaning.ipynb`
- [ ] `EHR_Preprocessing_2_Code_Rollup.ipynb`
- [ ] `EHR_Preprocessing_3_Natural_Language_Processing.ipynb`
- [x] `EHR_Preprocessing_4_Cohort_Creation.ipynb`

---

## Schema & State Handoffs
*(Claude: Populate these sections immediately after finishing a notebook and before requesting a /clear)*

### 0. Getting Started Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 1. Data Cleaning Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 2. Code Rollup Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 3. NLP Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 4. Cohort Creation Handoff
* **Summary:** Defined an asthma cohort (PheCode 495, 20,316 patients), extracted all codified features (Diagnoses/PheCodes, Procedures/CCS, Medications/RxNorm, Labs/LoincComponents) and NLP features (CUIs from discharge notes via petehr), aggregated into patient-level count matrices.
* **Final Output Shape/Location:**
  - `processed_data/step5_cohort_aggregateddata/codified/Diagnoses.csv` — 20,316 patients × 1,725 PheCodes
  - `processed_data/step5_cohort_aggregateddata/codified/Procedures.csv` — 20,316 patients × N CCS codes
  - `processed_data/step5_cohort_aggregateddata/codified/Medication.csv` — 20,316 patients × N RxNorm codes
  - `processed_data/step5_cohort_aggregateddata/codified/Labs.csv` — 20,316 patients × N LoincComponents
  - `processed_data/step5_cohort_aggregateddata/nlp/CUI_counts.csv` — ~14,958 patients × ~229 CUIs
* **Key Columns/Data Types:** All matrices have `subject_id` (str) as first column, remaining columns are code identifiers (str headers) with integer count values. NLP matrix has fewer patients (73% note coverage) due to MIMIC-IV Note v2.2 vs Hosp v3.1 version mismatch.

By decoupling the rules (static, in `CLAUDE.md`) from the state (dynamic, in `UPDATE_TRACK.md`), you ensure that when you move to the Cohort Creation notebook, the agent perfectly remembers exactly how the CUI strings and dates were formatted back in the Data Cleaning stage. 

Would you like me to help draft the specific `subplan.md` documents for any of these individual notebooks, such as the NLP processing or the initial data cleaning steps?
