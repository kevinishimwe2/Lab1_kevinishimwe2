# Lab 1: Grade Evaluator & Archiver

**Course:** Introduction to Python Programming and Databases  
**Institution:** African Leadership University — BSE Year 1, Trimester 2

---

## Project Structure

```
lab1_<github_username>/
├── grade-evaluator.py   # Python grade processing application
├── organizer.sh         # Bash archival script
├── grades.csv           # Your input CSV file (create before running)
├── archive/             # Auto-created by organizer.sh
├── organizer.log        # Auto-created by organizer.sh
└── README.md            # This file
```

---

## 1. grades.csv Format

Before running the Python script, create a `grades.csv` file in the same directory.  
The file **must** use this exact header row and column structure:

```
assignment,group,score,weight
Quiz 1,Formative,72,10
Quiz 2,Formative,45,10
Lab Report 1,Formative,80,15
Lab Report 2,Formative,40,15
Participation,Formative,65,10
Midterm Exam,Summative,55,20
Final Exam,Summative,48,20
```

**Rules your CSV must satisfy:**
| Rule | Requirement |
|---|---|
| `score` | Between 0 and 100 (inclusive) for every row |
| Total `weight` | Must sum to exactly **100** |
| Summative `weight` total | Must equal exactly **40** |
| Formative `weight` total | Must equal exactly **60** |

---

## 2. Running the Python Application (`grade-evaluator.py`)

### Prerequisites
- Python 3.6 or higher
- No external packages required (uses only `csv`, `sys`, `os` from the standard library)

### Steps

```bash
# Navigate to the project directory
cd lab1_<github_username>

# Run the script
python3 grade-evaluator.py
```

When prompted, enter the name of your CSV file:

```
Enter the name of the CSV file to process (e.g., grades.csv): grades.csv
```

### What the Script Does

| Step | Feature | Description |
|---|---|---|
| a | Grade Validation | Ensures every score is between 0 and 100 |
| b | Weight Validation | Verifies weights sum to 100 (Summative=40, Formative=60) |
| c | GPA Calculation | Computes weighted final grade; GPA = (grade / 100) × 5.0 |
| d | Pass / Fail | Student passes only if **both** Summative ≥ 50% and Formative ≥ 50% |
| e | Resubmission Logic | Identifies failed formative assignments (score < 50%) with the highest weight |
| f | Final Output | Prints PASSED / FAILED verdict and resubmission recommendation |

### Sample Output

```
--- Processing Grades ---
✔ All scores are valid (0-100).
✔ Weight validation passed (Total=100, Summative=40, Formative=60).

--- Grade Summary ---
  Summative Score : 20.60 / 40  (51.50%)
  Formative Score : 36.20 / 60  (60.33%)
  Final Grade     : 56.80%
  GPA             : 2.84 / 5.0

--- Final Decision ---
  Status: PASSED ✔

--- Resubmission Recommendation ---
  The following failed formative assignment(s) carry the highest weight
  and are eligible for resubmission:
    • Lab Report 2  (Score: 40.0%,  Weight: 15.0%)
```

### Error Handling

| Scenario | Behaviour |
|---|---|
| File not found | Prints a clear error message and exits |
| Empty CSV file | Prints a clear error message and exits |
| Score out of 0–100 | Lists offending assignments and exits |
| Weights don't add up | Reports each weight violation and exits |

---

## 3. Running the Shell Script (`organizer.sh`)

### Prerequisites
- A Unix/Linux/macOS terminal **or** Git Bash on Windows
- A `grades.csv` file must exist in the current directory before running

### Steps

```bash
# Make the script executable (only needed once)
chmod +x organizer.sh

# Run the script
./organizer.sh
```

### What the Script Does

1. **Checks** that `grades.csv` exists — exits with an error if it doesn't
2. **Creates** an `archive/` directory if one doesn't already exist
3. **Generates** a timestamp in `YYYYMMDD-HHMMSS` format
4. **Renames and moves** `grades.csv` → `archive/grades_YYYYMMDD-HHMMSS.csv`
5. **Creates** a fresh empty `grades.csv` in the current directory
6. **Appends** a log entry to `organizer.log` in the format:
   ```
   [20251105-170000] | original: grades.csv | archived: archive/grades_20251105-170000.csv
   ```

### Sample Output

```
Created archive directory: archive/
Archived: 'grades.csv' → 'archive/grades_20251105-170000.csv'
Reset: New empty 'grades.csv' created in current directory.
Logged: Entry written to 'organizer.log'.

✔ Archival complete.
  Timestamp : 20251105-170000
  Archived  : archive/grades_20251105-170000.csv
  Log file  : organizer.log
```

### organizer.log Example (after multiple runs)

```
[20251105-170000] | original: grades.csv | archived: archive/grades_20251105-170000.csv
[20251105-180532] | original: grades.csv | archived: archive/grades_20251105-180532.csv
[20251106-090015] | original: grades.csv | archived: archive/grades_20251106-090015.csv
```

---

## 4. Typical Workflow

```bash
# Step 1 — Fill in grades.csv with student data
nano grades.csv

# Step 2 — Run the grade evaluator to get results
python3 grade-evaluator.py

# Step 3 — Archive the processed grades and reset the workspace
./organizer.sh

# Step 4 — grades.csv is now empty and ready for the next student's data
```

---

## 5. Learning Objectives Covered

1. File handling — reading, parsing, and processing structured CSV data
2. Conditional logic — data validation, pass/fail determination, resubmission selection
3. Shell scripting — automating file organisation and generating persistent logs