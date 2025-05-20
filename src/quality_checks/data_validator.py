import pandas as pd
from src.db.database_operations import get_db_connection
from config import settings
import os

class DataQualityChecker:
    def __init__(self, connection):
        self.conn = connection
        self.results = []

    def check_nulls(self, table_name, column_name, threshold_percent=0):
        """Checks for NULL values in a specified column."""
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL;"
        total_query = f"SELECT COUNT(*) FROM {table_name};"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        null_count = cursor.fetchone()[0]
        cursor.execute(total_query)
        total_count = cursor.fetchone()[0]

        if total_count == 0:
            status = "PASS"
            message = f"DQ Check: NULLs in '{column_name}'. Table '{table_name}' is empty. Check skipped."
            self.results.append({"check": f"NULLs in {table_name}.{column_name}", "status": status, "message": message})
            return status == "PASS"

        null_percentage = (null_count / total_count) * 100
        
        if null_percentage > threshold_percent:
            status = "FAIL"
            message = f"DQ Check: NULLs in '{column_name}'. Found {null_count} ({null_percentage:.2f}%) NULLs, exceeds threshold of {threshold_percent}%."
        else:
            status = "PASS"
            message = f"DQ Check: NULLs in '{column_name}'. Found {null_count} ({null_percentage:.2f}%) NULLs. Within threshold."
        
        self.results.append({"check": f"NULLs in {table_name}.{column_name}", "status": status, "message": message})
        print(message)
        return status == "PASS"

    def check_uniqueness(self, table_name, column_name):
        """Checks for duplicate values in a specified column (intended for PKs)."""
        query = f"SELECT {column_name}, COUNT(*) FROM {table_name} GROUP BY {column_name} HAVING COUNT(*) > 1;"
        duplicates_df = pd.read_sql_query(query, self.conn)
        
        if duplicates_df.empty:
            status = "PASS"
            message = f"DQ Check: Uniqueness of '{column_name}' in '{table_name}'. All values are unique."
        else:
            status = "FAIL"
            message = f"DQ Check: Uniqueness of '{column_name}' in '{table_name}'. Found {len(duplicates_df)} duplicate value(s). Examples: {duplicates_df[column_name].head().tolist()}"
            
        self.results.append({"check": f"Uniqueness in {table_name}.{column_name}", "status": status, "message": message})
        print(message)
        return status == "PASS"

    def check_value_range(self, table_name, column_name, min_val=None, max_val=None):
        """Checks if values in a column are within the specified range."""
        conditions = []
        if min_val is not None:
            conditions.append(f"{column_name} < {min_val}")
        if max_val is not None:
            conditions.append(f"{column_name} > {max_val}")
        
        if not conditions:
            message = f"DQ Check: Value range for '{column_name}' in '{table_name}'. No min/max specified. Check skipped."
            self.results.append({"check": f"Value range in {table_name}.{column_name}", "status": "SKIPPED", "message": message})
            print(message)
            return True

        condition_str = " OR ".join(conditions)
        query = f"SELECT COUNT(*) FROM {table_name} WHERE {condition_str};"
        
        cursor = self.conn.cursor()
        cursor.execute(query)
        out_of_range_count = cursor.fetchone()[0]

        if out_of_range_count == 0:
            status = "PASS"
            message = f"DQ Check: Value range for '{column_name}' in '{table_name}'. All values within specified range (min: {min_val}, max: {max_val})."
        else:
            status = "FAIL"
            message = f"DQ Check: Value range for '{column_name}' in '{table_name}'. Found {out_of_range_count} values out of range (min: {min_val}, max: {max_val})."

        self.results.append({"check": f"Value range in {table_name}.{column_name}", "status": status, "message": message})
        print(message)
        return status == "PASS"

    def generate_report(self):
        report_path = os.path.join(settings.REPORTS_DIR, 'data_quality_report.txt')
        num_checks = len(self.results)
        num_passed = sum(1 for r in self.results if r['status'] == "PASS")
        num_failed = sum(1 for r in self.results if r['status'] == "FAIL")
        num_skipped = sum(1 for r in self.results if r['status'] == "SKIPPED")

        with open(report_path, 'w') as f:
            f.write("Data Quality Check Report\n")
            f.write("=" * 30 + "\n")
            for res in self.results:
                f.write(f"Check: {res['check']}\n")
                f.write(f"Status: {res['status']}\n")
                f.write(f"Message: {res['message']}\n")
                f.write("-" * 20 + "\n")
            
            f.write("\nSummary:\n")
            f.write(f"Total Checks: {num_checks}\n")
            f.write(f"Passed: {num_passed}\n")
            f.write(f"Failed: {num_failed}\n")
            f.write(f"Skipped: {num_skipped}\n")
        
        print(f"\nData quality report generated at: {report_path}")
        if num_failed > 0:
            print("WARNING: Some data quality checks failed!")
        else:
            print("All data quality checks passed or were skipped.")

def run_all_data_quality_checks():
    """Runs a predefined set of data quality checks."""
    conn = get_db_connection()
    if not conn:
        print("Could not connect to database. Skipping data quality checks.")
        return

    print("\n" + "=" * 50)
    print("RUNNING DATA QUALITY CHECKS")
    print("=" * 50)
    
    checker = DataQualityChecker(conn)

    # Define checks
    checker.check_nulls(table_name='Sales', column_name='OrderID', threshold_percent=0)
    checker.check_nulls(table_name='Sales', column_name='ProductID', threshold_percent=0)
    checker.check_nulls(table_name='Sales', column_name='CustomerSegment', threshold_percent=5) # Allow some nulls

    checker.check_uniqueness(table_name='Sales', column_name='OrderID')
    
    checker.check_value_range(table_name='Sales', column_name='Quantity', min_val=1)
    checker.check_value_range(table_name='Sales', column_name='Discount', min_val=0.0, max_val=1.0)
    checker.check_value_range(table_name='Sales', column_name='TotalSale', min_val=0.0)

    checker.generate_report()
    conn.close()
