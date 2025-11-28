import pandas as pd
import os
import logging
from datetime import datetime

# Setup logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File paths
INPUT_FILE = 'input/data_raw.csv'
OUTPUT_FILE = 'output/data_final.csv'

# What columns we expect in the input file
REQUIRED_COLUMNS = ['ID', 'Project_Name', 'Budget_USD', 'Start_Date', 'Status']


def check_columns(df):
    """Check if DataFrame has all required columns."""
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        logger.error(f"Missing columns: {missing}")
        return False
    return True


def clean_and_transform(df, reference_date=None):
    """
    Clean and transform the data.
    
    Steps:
    1. Standardize column names
    2. Clean budget values
    3. Clean status values
    4. Calculate project age
    5. Remove bad rows
    """
    
    # Handle empty data
    if df.empty:
        logger.warning("No data to process")
        return df
    
    start_rows = len(df)
    logger.info(f"Starting with {start_rows} rows")
    
    # Step 1: Make column names lowercase and clean
    df.columns = df.columns.str.lower().str.replace('[^a-z0-9_]', '', regex=True)
    
    # Step 2: Clean budget column
    # Convert to numbers, replace missing with 0
    df['budget_usd'] = pd.to_numeric(df['budget_usd'], errors='coerce')
    missing_budgets = df['budget_usd'].isna().sum()
    df['budget_usd'] = df['budget_usd'].fillna(0.0)
    logger.info(f"Fixed {missing_budgets} missing budgets")
    
    # Step 3: Clean status column
    # Replace missing with 'UNKNOWN', make uppercase
    missing_status = df['status'].isna().sum()
    df['status'] = df['status'].fillna('UNKNOWN').str.upper()
    logger.info(f"Fixed {missing_status} missing statuses")
    
    # Step 4: Calculate project age in days
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    
    # Use default reference date if not provided
    if reference_date is None:
        reference_date = datetime(2025, 1, 1)
    
    df['project_age_days'] = (reference_date - df['start_date']).dt.days
    
    # Step 5: Remove rows with bad dates
    df = df.dropna(subset=['start_date'])
    df = df.reset_index(drop=True)
    
    end_rows = len(df)
    removed = start_rows - end_rows
    logger.info(f"Removed {removed} rows with bad dates")
    logger.info(f"Final result: {end_rows} rows")
    
    return df


def read_data(file_path):
    """Read CSV file and validate it."""
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find file: {file_path}")
    
    logger.info(f"Reading {file_path}")
    df = pd.read_csv(file_path)
    
    # Check if file is empty
    if df.empty:
        raise ValueError("File is empty")
    
    # Check if columns are correct
    if not check_columns(df):
        raise ValueError("File has wrong columns")
    
    logger.info(f"Read {len(df)} rows successfully")
    return df


def write_data(df, file_path):
    """Write DataFrame to CSV file."""
    
    # Create output folder if it doesn't exist
    output_folder = os.path.dirname(file_path)
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
    
    # Write to file
    df.to_csv(file_path, index=False)
    logger.info(f"Saved {len(df)} rows to {file_path}")


# Main program
if __name__ == "__main__":
    logger.info("=== Starting Pipeline ===")
    
    try:
        # Step 1: Read the data
        raw_data = read_data(INPUT_FILE)
        
        # Step 2: Clean and transform
        clean_data = clean_and_transform(raw_data)
        
        # Step 3: Save the result
        write_data(clean_data, OUTPUT_FILE)
        
        logger.info("=== Pipeline Complete ===")
        
    except FileNotFoundError as e:
        logger.error(f"File problem: {e}")
    except ValueError as e:
        logger.error(f"Data problem: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
