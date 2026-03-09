# EHR Pipeline Update Tracker

## Active Status
* **Current Notebook in Progress:** `EHR_Preprocessing_Getting_Started.ipynb`

## Subplan Execution Status
- [ ] `EHR_Preprocessing_Getting_Started.ipynb`
- [ ] `EHR_Preprocessing_1_Data_Cleaning.ipynb`
- [ ] `EHR_Preprocessing_2_Code_Rollup.ipynb`
- [ ] `EHR_Preprocessing_3_Natural_Language_Processing.ipynb`
- [ ] `EHR_Preprocessing_4_Cohort_Creation.ipynb`

---

## Schema & State Handoffs
*(Claude: Populate these sections immediately after finishing a notebook and before requesting a /clear)*

### 0. Getting Started Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 1. Data Cleaning Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 2. Code Rollup Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 3. NLP Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ### 4. Cohort Creation Handoff
* **Summary:** * **Final Output Shape/Location:** * **Key Columns/Data Types:** ```

By decoupling the rules (static, in `CLAUDE.md`) from the state (dynamic, in `UPDATE_TRACK.md`), you ensure that when you move to the Cohort Creation notebook, the agent perfectly remembers exactly how the CUI strings and dates were formatted back in the Data Cleaning stage. 

Would you like me to help draft the specific `subplan.md` documents for any of these individual notebooks, such as the NLP processing or the initial data cleaning steps?
