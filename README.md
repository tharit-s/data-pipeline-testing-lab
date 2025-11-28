# data-pipeline-testing-lab

**Testable data cleaning pipeline project. Practice for DE assessments.**

## Project Overview

This repository demonstrates a complete, test-driven approach to data cleaning and transformation using Python and Pandas. 

The project structure separates source code (`src`), unit tests (`tests`), and data files (`input`/`output`) for maintainability and follows industry best practices.

## Features

- ✅ **Unit-tested data transformation functions** - 7 comprehensive tests covering normal and edge cases
- ✅ **Schema validation** - Validates required columns before processing
- ✅ **Logging for observability** - Tracks data quality metrics at each step
- ✅ **Error handling** - Graceful handling of missing files, empty data, and invalid formats
- ✅ **Edge case handling** - Handles empty data, null values, and invalid dates
- ✅ **Configurable transformations** - Flexible reference dates for calculations
- ✅ **Data quality metrics** - Logs row counts, null fills, and retention percentages

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tharit-s/data-pipeline-testing-lab.git
    cd data-pipeline-testing-lab
    ```

2.  **Set up virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Unit Tests (Recommended First):**
    ```bash
    python -m unittest tests.test_processor
    ```
    
    For verbose output:
    ```bash
    python -m unittest tests.test_processor -v
    ```

5.  **Run the Full Pipeline (End-to-End):**
    ```bash
    python src/data_processor.py
    ```
    This will create `output/data_final.csv` with cleaned data.

6.  **Deactivate virtual environment when done:**
    ```bash
    deactivate
    ```

## Project Structure

```
data-pipeline-testing-lab/
├── input/
│   └── data_raw.csv         # Sample messy data
├── output/
│   └── .gitkeep             # Output directory placeholder
├── src/
│   ├── __init__.py          # Package marker
│   └── data_processor.py    # Core ETL logic
├── tests/
│   ├── __init__.py          # Package marker
│   └── test_processor.py    # Unit tests
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## What the Pipeline Does

### Input Data (Messy)
```csv
ID,Project_Name,Budget_USD,Start_Date,Status
101,Aurora_Migration,45000,2024-03-01,COMPLETE
102,etl_refactor,22000,2024-05-15,IN PROGRESS
103,Data_Lake_Setup,,2024-06-01,
104,API Integration,60000,2024-07-20,complete
105,Reporting_Dash,18000,Not Available,IN PROGRESS
106,warehouse upgrade,NaN,2024-09-01,complete
107,ML_Pipeline,35000,,IN PROGRESS
```

### Transformations Applied

1. **Column Standardization** - Converts to lowercase snake_case
2. **Budget Cleaning** - Converts to numeric, fills missing with 0.0
3. **Status Standardization** - Fills missing with 'UNKNOWN', converts to uppercase
4. **Feature Engineering** - Calculates project age in days
5. **Data Quality** - Removes rows with invalid dates

### Output Data (Clean)
```csv
id,project_name,budget_usd,start_date,status,project_age_days
101,Aurora_Migration,45000.0,2024-03-01,COMPLETE,306.0
102,etl_refactor,22000.0,2024-05-15,IN PROGRESS,231.0
103,Data_Lake_Setup,0.0,2024-06-01,UNKNOWN,214.0
104,API Integration,60000.0,2024-07-20,COMPLETE,165.0
106,warehouse upgrade,0.0,2024-09-01,COMPLETE,122.0
```

## Test Coverage

All 7 tests validate:

- ✅ **Basic cleaning** - Column names, budget conversion, status standardization, project age
- ✅ **Empty data** - Handles empty DataFrames gracefully
- ✅ **All null budgets** - Fills all missing budgets with 0.0
- ✅ **All invalid dates** - Removes all rows when dates can't be parsed
- ✅ **Custom reference date** - Calculates age from configurable date
- ✅ **Schema validation (pass)** - Accepts correct column structure
- ✅ **Schema validation (fail)** - Rejects incorrect column structure

## Key Functions

### `clean_and_transform(df, reference_date=None)`
Core transformation function that:
- Standardizes column names
- Cleans budget and status columns
- Calculates project age
- Removes invalid rows

### `read_data(file_path)`
Reads CSV with validation:
- Checks file exists
- Validates schema
- Handles empty files

### `write_data(df, file_path)`
Writes cleaned data to CSV with logging

### `check_columns(df)`
Validates DataFrame has required columns

## Sample Log Output

```
2025-11-28 16:16:55 - INFO - === Starting Pipeline ===
2025-11-28 16:16:55 - INFO - Reading input/data_raw.csv
2025-11-28 16:16:55 - INFO - Read 7 rows successfully
2025-11-28 16:16:55 - INFO - Starting with 7 rows
2025-11-28 16:16:55 - INFO - Fixed 2 missing budgets
2025-11-28 16:16:55 - INFO - Fixed 1 missing statuses
2025-11-28 16:16:55 - INFO - Removed 2 rows with bad dates
2025-11-28 16:16:55 - INFO - Final result: 5 rows
2025-11-28 16:16:55 - INFO - Saved 5 rows to output/data_final.csv
2025-11-28 16:16:55 - INFO - === Pipeline Complete ===
```

## What This Demonstrates

This project showcases data engineering best practices:

- **Testing** - Unit tests with edge cases and mock data
- **Code Quality** - Clean, readable code with comments
- **Data Quality** - Schema validation, null handling, data profiling
- **Production Thinking** - Logging, error handling, configurability
- **Documentation** - Clear README and inline comments
- **Version Control** - Proper .gitignore and project structure
- **Reproducibility** - requirements.txt and virtual environment

## Technologies Used

- **Python 3.13+**
- **Pandas** - Data manipulation and transformation
- **unittest** - Testing framework
- **logging** - Observability and debugging

## Future Enhancements

Potential improvements for production use:

- Add CI/CD pipeline (GitHub Actions)
- Add pre-commit hooks (black, flake8, mypy)
- Add configuration file (YAML/JSON)
- Add Docker support
- Add data profiling reports
- Add performance benchmarks
- Add more data quality checks

## License

This is a learning project for data engineering practice.

## Author

Created as a portfolio project to demonstrate data engineering skills for technical assessments.
