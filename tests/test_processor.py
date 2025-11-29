import unittest
import pandas as pd
from datetime import datetime
from src.data_processor import clean_and_transform, check_columns


class TestDataProcessor(unittest.TestCase):
    """Tests for the data processor."""
    
    def setUp(self):
        """Create sample data for testing."""
        self.sample_data = pd.DataFrame({
            'ID': [1, 2, 3, 4],
            'Project_Name': ['project_A', 'PROJECT-B', 'project c', 'Invalid_Project'],
            'Budget_USD': [10000.0, '25000', None, 5000.0],
            'Start_Date': ['2024-01-01', '2024-02-15', 'N/A', 'Invalid_Date'],
            'Status': ['COMPLETE', 'in progress', 'pending', None]
        })
    
    def test_basic_cleaning(self):
        """Test that cleaning works correctly."""
        result = clean_and_transform(self.sample_data.copy())
        
        # Should have 2 rows (2 bad dates removed)
        self.assertEqual(len(result), 2)
        
        # Budget should be numbers
        self.assertTrue(pd.api.types.is_float_dtype(result['budget_usd']))
        
        # Status should be uppercase
        self.assertEqual(result.loc[1, 'status'], 'IN PROGRESS')
        
        # Should calculate project age
        self.assertEqual(result.loc[0, 'project_age_days'], 366)
        
        # Column names should be lowercase
        self.assertIn('project_name', result.columns)
    
    def test_empty_data(self):
        """Test handling empty data."""
        empty = pd.DataFrame()
        result = clean_and_transform(empty)
        self.assertTrue(result.empty)
    
    def test_all_null_budgets(self):
        """Test when all budgets are missing."""
        data = pd.DataFrame({
            'ID': [1, 2],
            'Project_Name': ['A', 'B'],
            'Budget_USD': [None, None],
            'Start_Date': ['2024-01-01', '2024-02-01'],
            'Status': ['COMPLETE', 'PENDING']
        })
        result = clean_and_transform(data)
        
        # All budgets should be 0.0
        self.assertTrue((result['budget_usd'] == 0.0).all())
    
    def test_all_bad_dates(self):
        """Test when all dates are invalid."""
        data = pd.DataFrame({
            'ID': [1, 2],
            'Project_Name': ['A', 'B'],
            'Budget_USD': [1000, 2000],
            'Start_Date': ['invalid', 'bad_date'],
            'Status': ['COMPLETE', 'PENDING']
        })
        result = clean_and_transform(data)
        
        # Should have no rows left
        self.assertEqual(len(result), 0)
    
    def test_custom_date(self):
        """Test using a custom reference date."""
        data = pd.DataFrame({
            'ID': [1],
            'Project_Name': ['A'],
            'Budget_USD': [1000],
            'Start_Date': ['2024-01-01'],
            'Status': ['COMPLETE']
        })
        
        # Use Dec 31, 2024 as reference
        custom_date = datetime(2024, 12, 31)
        result = clean_and_transform(data, reference_date=custom_date)
        
        # Should be 365 days
        self.assertEqual(result.loc[0, 'project_age_days'], 365)
    
    def test_column_check_pass(self):
        """Test column validation with correct columns."""
        self.assertTrue(check_columns(self.sample_data))
    
    def test_column_check_fail(self):
        """Test column validation with wrong columns."""
        bad_data = pd.DataFrame({'ID': [1], 'Name': ['Test']})
        self.assertFalse(check_columns(bad_data))

    def test_no_rows_after_cleaning(self):
        """Test case where all rows are removed after cleaning."""
        data = pd.DataFrame({
            'ID': [1, 2],
            'Project_Name': ['A', 'B'],
            'Budget_USD': [None, None],
            'Start_Date': ['invalid_date1', 'invalid_date2'],
            'Status': [None, None]
        })
        result = clean_and_transform(data)
        
        # All rows should be removed
        self.assertEqual(len(result), 0)

    def test_valid_data(self):
        """Test case where all rows are remained after cleaning."""
        data = pd.DataFrame({
            'ID': [1, 2],
            'Project_Name': ['A', 'B'],
            'Budget_USD': [1000, 2000],
            'Start_Date': ['2024-01-01', '2024-01-02'],
            'Status': ['COMPLETE', 'PENDING']
        })
        result = clean_and_transform(data)

        # All rows should be removed
        self.assertEqual(len(result), 2)
        self.assertEqual(result.loc[0, 'id'], 1)
        self.assertEqual(result.loc[1, 'id'], 2)
        self.assertEqual(result.loc[0, 'project_name'], 'A')
        self.assertEqual(result.loc[1, 'project_name'], 'B')
        self.assertEqual(result.loc[:, "budget_usd"].tolist(), [1000.0, 2000.0])
        self.assertEqual(result.loc[:, "status"].tolist(), ['COMPLETE', 'PENDING'])
        self.assertEqual(result.loc[:, "start_date"].tolist(), [
            pd.to_datetime('2024-01-01'),
            pd.to_datetime('2024-01-02')
        ])
        self.assertEqual(result.loc[:, "project_age_days"].tolist(), [366, 365])


if __name__ == '__main__':
    unittest.main()
