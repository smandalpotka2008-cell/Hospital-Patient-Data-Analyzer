# Project Summary — Hospital Patient Data Analyzer (PS No. 16)

## 1. Project Overview
The **Hospital Patient Data Analyzer** solves Problem Statement 16 for the B.Tech Computer Science and Engineering Python project. Using Python 3, Object-Oriented Programming (`HospitalDataAnalyzer` class), Pandas, and Matplotlib, the program automates hospital record preprocessing and generates actionable clinical operations metrics:
- **Data Cleaning:** Automatically drops duplicate `Patient_ID` rows, handles missing or out-of-range ages using median imputation, and validates admission/discharge dates.
- **Department & Gender Analysis:** Uses `groupby()` to summarize patient distribution across hospital departments and genders.
- **Length of Stay & Age Segmentation:** Calculates exact hospital stay durations (including same-day 0-day discharges), overall mean stay, age brackets (`0-40`, `41-60`, `61+`), and plots a bar chart of average stay by department.

---

## 2. Difficulties Faced & How They Were Solved
1. **Handling Missing & Non-Numeric Age Values:**
   - *Difficulty:* Empty cells or malformed strings in the `Age` column caused type errors during age-group categorization and statistical calculations.
   - *Solution:* Converted `Age` safely using `pd.to_numeric(..., errors='coerce')`, filtered unrealistic values (`< 0` or `> 120`), computed the median of valid ages (`45`), and filled missing entries cleanly before casting back to integers.
2. **Same-Day Discharge & Date Parsing:**
   - *Difficulty:* Patients admitted and discharged on the same date (`2026-08-10` to `2026-08-10`) needed to register accurately as `0 days` without throwing division or date-subtraction errors.
   - *Solution:* Parsed `Admit_Date` and `Discharge_Date` with `pd.to_datetime()` and extracted `.dt.days` from the timedelta difference, preserving `0` day stays accurately in the mean calculation.
3. **Preserving Unobserved Age Groups in Output:**
   - *Difficulty:* When a dataset had zero patients in the `61+` bracket, `groupby()` omitted the empty category by default.
   - *Solution:* Used `pd.cut()` with defined bins (`0-40`, `41-60`, `61+`) alongside `groupby('Age_Group', observed=False)` so every age group is consistently displayed even when its count is `0`.

---

## 3. Working Test Cases & Screenshots
All four test cases specified in the problem statement were verified. Screenshot outputs are stored in the `Screenshots/` folder:

### Test Case 1: Normal Input (Menu Option 1)
- **Expected:** `Cardiology: 2 | Ortho: 1`, `Total patients: 3`
- **Screenshot:** `Screenshots/TestCase1_DepartmentCount.png`

### Test Case 2: Boundary / Minimum Input (Menu Option 2)
- **Expected:** `P4: 0 days`, `Average stay: 0.00 days`
- **Screenshot:** `Screenshots/TestCase2_BoundaryStay.png`

### Test Case 3: Invalid Input (Duplicates & Missing Age)
- **Expected:** `Duplicates removed: 1`, `Missing Age filled with median: 45`
- **Screenshot:** `Screenshots/TestCase3_DataCleaning.png`

### Test Case 4: Different Valid Scenario (Menu Option 3)
- **Expected:** `Average stay: 3.67 days`, `Age groups: 0-40: 1 | 41-60: 2 | 61+: 0`, `Bar chart displayed`
- **Screenshots:** `Screenshots/TestCase4_StayAndAgeGroups.png` and `Screenshots/TestCase4_BarChart.png`
