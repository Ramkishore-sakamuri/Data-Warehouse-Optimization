# Data Warehouse Optimization Simulation

This project simulates key aspects of data warehouse optimization, including:
1.  Setting up a "legacy" database schema.
2.  Measuring the performance of a query.
3.  Applying an optimization technique (creating an index).
4.  Measuring the performance of the same query on the optimized schema.
5.  Implementing and running automated data quality checks.

**Disclaimer:** This is a simplified, illustrative project using Python and SQLite. Real-world data warehouse optimization is far more complex and depends on the specific DWH platform, data volume, and business needs. The performance gains shown here are conceptual and may vary significantly with larger datasets.

## Setup

1.  **Clone the repository (or create the files as listed).**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Prepare Data:**
    Ensure `data/sales_records.csv` exists and contains sample sales data. A small example is provided. For more noticeable performance differences, increase the number of rows in this CSV file, especially varying the `CustomerSegment` field.

## How to Run

Execute the main script from the root directory of the project:

```bash
python -m src.main

Okay, I can help you by outlining a simulated and illustrative project for Data Warehouse Optimization using Python and SQLite.

It's important to understand that a real-world data warehouse optimization project is highly complex, specific to the existing architecture (e.g., Redshift, BigQuery, Snowflake, on-premise SQL Server/Oracle), data volume, and business requirements. A generic, fully-fledged "real project code" that universally applies and guarantees a 60% query reduction out-of-the-box isn't feasible to generate directly.

However, I can provide you with a functional, executable Python project structure and code that demonstrates the core concepts:

Setting up a small "legacy" SQLite database.
Running a "slow" query and measuring its time.
Applying a common optimization technique (e.g., adding an index).
Running an "optimized" query and measuring its time to show improvement.
Implementing basic automated data quality checks.
This project will be a simplified model to illustrate the principles involved. The "60% reduction" is a target often achieved in real projects through various techniques; here, we'll demonstrate a qualitative improvement.

Project: Data Warehouse Optimization Simulation
Objective: To demonstrate a conceptual approach to optimizing a data warehouse by improving query performance and implementing data quality checks.

Technology Stack (Illustrative):

Python
SQLite (as a simple, file-based database)
Pandas (for data handling)
Project Tree
data_warehouse_optimization/
├── data/
│   └── sales_records.csv
├── src/
│   ├── db/
│   │   ├── __init__.py
│   │   └── database_operations.py  # Handles DB connection, setup, data loading
│   ├── optimization/
│   │   ├── __init__.py
│   │   └── query_optimizer.py      # Applies optimizations, runs queries
│   ├── quality_checks/
│   │   ├── __init__.py
│   │   └── data_validator.py       # Implements DQ checks
│   ├── sql/
│   │   ├── create_tables.sql
│   │   ├── slow_sales_report.sql
│   │   └── optimized_sales_report.sql
│   ├── utils/
│   │   ├── __init__.py
│   │   └── timing.py               # Decorator for timing functions
│   └── main.py                     # Main script to orchestrate the process
├── reports/                        # Output reports (e.g., DQ reports, performance logs)
│   └── data_quality_report.txt
├── config/
│   └── settings.py                 # Configuration (e.g., DB path)
├── README.md
└── requirements.txt
File Contents and Code
1. requirements.txt
Plaintext

pandas
2. config/settings.py
Python

# config/settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'sales_warehouse.db')
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'sales_records.csv')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Ensure reports directory exists
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)
3. data/sales_records.csv
Create a sample CSV file. For a noticeable difference in query times (even simulated), a few thousand rows would be better, but for brevity:

Code snippet

OrderID,ProductID,CustomerSegment,SaleDate,Quantity,UnitPrice,Discount,TotalSale
1001,P001,Consumer,2023-01-15,2,50.00,0.0,100.00
1002,P002,Corporate,2023-01-16,1,200.00,0.1,180.00
1003,P003,Home Office,2023-01-17,5,15.00,0.0,75.00
1004,P001,Consumer,2023-01-18,3,50.00,0.05,142.50
1005,P004,Corporate,2023-01-19,10,5.00,0.0,50.00
1006,P002,Consumer,2023-01-20,2,200.00,0.15,340.00
1007,P005,Home Office,2023-01-21,1,500.00,0.2,400.00
1008,P001,Corporate,2023-02-01,4,50.00,0.0,200.00
1009,P006,Consumer,2023-02-02,20,2.00,0.0,40.00
1010,P003,Corporate,2023-02-03,3,15.00,0.0,45.00
# ... (Add more rows, especially with varying CustomerSegment values for better query demo)
# For this example, let's add a few more for 'Corporate' to make the query more meaningful
1011,P007,Corporate,2023-02-05,1,100.00,0.0,100.00
1012,P008,Corporate,2023-02-06,2,75.00,0.05,142.50
1013,P001,Corporate,2023-02-07,5,50.00,0.0,250.00
1014,P002,Consumer,2023-02-10,1,200.00,0.1,180.00
1015,P009,Home Office,2023-02-12,2,25.00,0.0,50.00
1016,P010,Corporate,2023-02-15,3,30.00,0.02,88.20
1017,P004,Consumer,2023-02-18,8,5.00,0.0,40.00
1018,P001,Corporate,2023-02-20,2,50.00,0.0,100.00
1019,P002,Home Office,2023-02-22,1,200.00,0.1,180.00
1020,P003,Consumer,2023-02-25,4,15.00,0.0,60.00
(To truly see performance differences, you'd ideally have 10,000s or 100,000s of rows. The provided code will work, but the time differences with so little data will be minimal, often in milliseconds and susceptible to system noise. The principle remains the same.)

4. src/sql/create_tables.sql
SQL

-- src/sql/create_tables.sql
DROP TABLE IF EXISTS Sales;

CREATE TABLE Sales (
    OrderID INTEGER PRIMARY KEY,
    ProductID TEXT NOT NULL,
    CustomerSegment TEXT,
    SaleDate TEXT, -- Using TEXT for simplicity, ideally DATE type
    Quantity INTEGER,
    UnitPrice REAL,
    Discount REAL,
    TotalSale REAL
);

-- No index on CustomerSegment initially to simulate a less optimized state
5. src/utils/timing.py
Python

# src/utils/timing.py
import time

def time_it(func):
    """Decorator to measure execution time of a function."""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000  # in milliseconds
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} ms")
        return result, elapsed_time
    return wrapper
6. src/db/database_operations.py
Python

# src/db/database_operations.py
import sqlite3
import pandas as pd
from config import settings
import os

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(settings.DATABASE_PATH)
    return conn

def execute_sql_script(conn, script_path):
    """Executes an SQL script from a file."""
    with open(script_path, 'r') as sql_file:
        sql_script = sql_file.read()
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    print(f"Executed SQL script: {script_path}")

def load_data_from_csv(conn, table_name='Sales'):
    """Loads data from CSV into the specified table."""
    try:
        df = pd.read_csv(settings.RAW_DATA_PATH)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data loaded from '{settings.RAW_DATA_PATH}' into '{table_name}' table.")
        # After replacing, we need to re-run table creation if it defines specific types or constraints
        # that to_sql might not perfectly replicate, or ensure to_sql is used on an empty, pre-defined table.
        # For this example, we'll assume to_sql is sufficient after initial create_tables.sql.
        # If Sales table was dropped by to_sql with if_exists='replace', we need to recreate.
        # A better approach for incremental loads is 'append'. For full refresh, drop/create/load is fine.

        # Let's ensure the table schema from create_tables.sql is what we have after pandas load.
        # This is a bit of a simplification. In robust systems, you'd handle schema carefully.
        # For now, we'll load data first, then run create_tables.sql which will DROP IF EXISTS.
        # This is not ideal. Correct order: Create schema, then load data.
        # Let's adjust:
    except FileNotFoundError:
        print(f"Error: Raw data file not found at {settings.RAW_DATA_PATH}")
        print("Please create 'data/sales_records.csv'")
        return
    except Exception as e:
        print(f"Error loading data: {e}")


def setup_database():
    """Sets up the database: creates tables and loads initial data."""
    # Remove existing DB file to start fresh each time for this demo
    if os.path.exists(settings.DATABASE_PATH):
        os.remove(settings.DATABASE_PATH)
        print(f"Removed existing database: {settings.DATABASE_PATH}")

    conn = get_db_connection()
    try:
        # 1. Create table structures
        create_script_path = os.path.join(settings.SQL_DIR, 'create_tables.sql')
        execute_sql_script(conn, create_script_path)
        print("Database tables created successfully.")

        # 2. Load data from CSV
        df = pd.read_csv(settings.RAW_DATA_PATH)
        df.to_sql('Sales', conn, if_exists='append', index=False) # Append to existing created table
        print(f"Data loaded from '{settings.RAW_DATA_PATH}' into 'Sales' table.")

    except FileNotFoundError:
        print(f"ERROR: Ensure '{settings.RAW_DATA_PATH}' exists and '{create_script_path}' exists.")
    except Exception as e:
        print(f"Error during database setup: {e}")
    finally:
        if conn:
            conn.close()

def fetch_query_results(conn, query_sql, params=None):
    """Executes a SELECT query and returns results as a DataFrame."""
    try:
        return pd.read_sql_query(query_sql, conn, params=params)
    except Exception as e:
        print(f"Error executing query: {e}")
        return pd.DataFrame()

7. src/sql/slow_sales_report.sql
SQL

-- src/sql/slow_sales_report.sql
-- This query calculates total sales for a specific customer segment.
-- It will be slower if there's no index on CustomerSegment.
SELECT
    CustomerSegment,
    SUM(TotalSale) as TotalSalesAmount,
    AVG(Quantity) as AverageQuantity,
    COUNT(OrderID) as NumberOfOrders
FROM
    Sales
WHERE
    CustomerSegment = ? -- Parameter for customer segment
GROUP BY
    CustomerSegment;
8. src/sql/optimized_sales_report.sql
This SQL is identical to slow_sales_report.sql. The "optimization" comes from adding an index to the CustomerSegment column in the database, not from changing the SQL query itself in this specific scenario.

SQL

-- src/sql/optimized_sales_report.sql
-- This query is the same as slow_sales_report.sql.
-- The performance improvement comes from an index on CustomerSegment.
SELECT
    CustomerSegment,
    SUM(TotalSale) as TotalSalesAmount,
    AVG(Quantity) as AverageQuantity,
    COUNT(OrderID) as NumberOfOrders
FROM
    Sales
WHERE
    CustomerSegment = ? -- Parameter for customer segment
GROUP BY
    CustomerSegment;
9. src/optimization/query_optimizer.py
Python

# src/optimization/query_optimizer.py
import sqlite3
from config import settings
from src.db.database_operations import get_db_connection, fetch_query_results
from src.utils.timing import time_it
import os
import pandas as pd

def read_sql_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

@time_it
def run_sales_report_query(conn, query_sql_path, segment='Corporate'):
    """Runs the sales report query and returns results."""
    query_sql = read_sql_file(query_sql_path)
    print(f"\nRunning query from: {os.path.basename(query_sql_path)} for segment: {segment}")
    results_df = fetch_query_results(conn, query_sql, params=(segment,))
    if not results_df.empty:
        print("Query Results:")
        print(results_df.to_string())
    else:
        print("No results returned or error in query execution.")
    return results_df

def apply_optimizations(conn):
    """Applies database optimizations, e.g., creating indexes."""
    try:
        cursor = conn.cursor()
        index_name = 'idx_customer_segment'
        table_name = 'Sales'
        column_name = 'CustomerSegment'

        # Check if index already exists
        cursor.execute(f"PRAGMA index_list('{table_name}');")
        indexes = cursor.fetchall()
        if any(index_name in idx_info for idx_info in indexes):
            print(f"Index '{index_name}' already exists on '{table_name}'.")
            return

        print(f"\nApplying optimization: Creating index '{index_name}' on {table_name}({column_name})...")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({column_name});")
        conn.commit()
        print(f"Index '{index_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error applying optimizations: {e}")

def compare_query_performance():
    """
    Demonstrates query performance before and after optimization.
    Returns the performance comparison details.
    """
    conn = get_db_connection()
    if not conn:
        return None, None, 0

    slow_query_path = os.path.join(settings.SQL_DIR, 'slow_sales_report.sql')
    optimized_query_path = os.path.join(settings.SQL_DIR, 'optimized_sales_report.sql')
    test_segment = 'Corporate' # Make sure this segment has enough data

    # Run query before optimization
    print("-" * 50)
    print("Executing query on 'legacy' (unoptimized) database structure...")
    (results_before, time_before), _ = run_sales_report_query(conn, slow_query_path, segment=test_segment)


    # Apply optimization
    apply_optimizations(conn)

    # Run query after optimization
    print("-" * 50)
    print("Executing query on 'optimized' database structure...")
    (results_after, time_after), _ = run_sales_report_query(conn, optimized_query_path, segment=test_segment)
    print("-" * 50)

    reduction_percentage = 0
    if time_before > 0 and time_after > 0: # Avoid division by zero if times are too small/zero
        improvement = time_before - time_after
        if improvement > 0:
            reduction_percentage = (improvement / time_before) * 100
            print(f"Query time reduced by: {reduction_percentage:.2f}%")
            print(f"Original time: {time_before:.4f} ms, Optimized time: {time_after:.4f} ms")
        else:
            print(f"No performance improvement observed, or optimized query was slower. Original: {time_before:.4f} ms, Optimized: {time_after:.4f} ms")
            reduction_percentage = -1 # Indicate it was slower or same
    else:
        print("Could not reliably calculate performance improvement due to very small or zero execution times.")
        print(f"Original time: {time_before:.4f} ms, Optimized time: {time_after:.4f} ms")


    conn.close()
    return time_before, time_after, reduction_percentage
10. src/quality_checks/data_validator.py
Python

# src/quality_checks/data_validator.py
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
11. src/main.py (Orchestrator)
Python

# src/main.py
from src.db import database_operations
from src.optimization import query_optimizer
from src.quality_checks import data_validator
from config import settings # To ensure directories are created
import time

def main():
    print("Starting Data Warehouse Optimization Simulation...")
    start_total_time = time.perf_counter()

    # --- 1. Database Setup ---
    print("\nPHASE 1: Database Setup")
    database_operations.setup_database()
    print("Database setup complete.")

    # --- 2. Query Performance Comparison ---
    print("\nPHASE 2: Query Performance Optimization")
    time_before, time_after, reduction_percentage = query_optimizer.compare_query_performance()
    
    if time_before is not None and time_after is not None:
        print("\nPERFORMANCE SUMMARY:")
        if reduction_percentage > 0:
            print(f"✅ Query response time reduced by approximately {reduction_percentage:.2f}%.")
            print(f"   Original Time: {time_before:.4f} ms")
            print(f"   Optimized Time: {time_after:.4f} ms")
        elif reduction_percentage == -1:
            print(f"⚠️ No significant query time improvement, or optimized query was slower.")
            print(f"   Original Time: {time_before:.4f} ms")
            print(f"   Optimized Time: {time_after:.4f} ms")
        else:
            print(f"ℹ️ Could not reliably measure performance improvement (times were likely too small).")
            print(f"   Original Time: {time_before:.4f} ms")
            print(f"   Optimized Time: {time_after:.4f} ms")
            print(f"   Consider using a larger dataset in 'data/sales_records.csv' for more pronounced differences.")

    # --- 3. Data Quality Checks ---
    print("\nPHASE 3: Automated Data Quality Checks")
    data_validator.run_all_data_quality_checks()
    print("Data quality checks complete.")

    end_total_time = time.perf_counter()
    total_elapsed_time = (end_total_time - start_total_time)
    print(f"\n🏁 Simulation finished in {total_elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    # This allows running main.py directly from the root directory
    # assuming data_warehouse_optimization is the current working directory
    # For imports to work correctly when running `python src/main.py`
    # you might need to adjust PYTHONPATH or run as `python -m src.main` from root.
    # For simplicity, assume running from the project root `python -m src.main` or an IDE configured for it.
    main()
Note on running main.py:
If you are in the data_warehouse_optimization directory, you should run it as a module to ensure Python resolves the imports correctly:
python -m src.main

12. README.md
Markdown

# Data Warehouse Optimization Simulation

This project simulates key aspects of data warehouse optimization, including:
1.  Setting up a "legacy" database schema.
2.  Measuring the performance of a query.
3.  Applying an optimization technique (creating an index).
4.  Measuring the performance of the same query on the optimized schema.
5.  Implementing and running automated data quality checks.

**Disclaimer:** This is a simplified, illustrative project using Python and SQLite. Real-world data warehouse optimization is far more complex and depends on the specific DWH platform, data volume, and business needs. The performance gains shown here are conceptual and may vary significantly with larger datasets.

## Project Structure

data_warehouse_optimization/
├── data/                     # Sample data and database file
│   └── sales_records.csv     # Raw sales data
│   └── sales_warehouse.db    # SQLite database file (will be created)
├── src/                      # Source code
│   ├── db/                   # Database operations
│   ├── optimization/         # Query optimization logic
│   ├── quality_checks/       # Data quality validation
│   ├── sql/                  # SQL scripts
│   └── utils/                # Utility functions
│   └── main.py               # Main orchestrator script
├── reports/                  # Output reports
│   └── data_quality_report.txt
├── config/                   # Configuration
│   └── settings.py
├── README.md                 # This file
└── requirements.txt          # Python dependencies


## Setup

1.  **Clone the repository (or create the files as listed).**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Prepare Data:**
    Ensure `data/sales_records.csv` exists and contains sample sales data. A small example is provided. For more noticeable performance differences, increase the number of rows in this CSV file, especially varying the `CustomerSegment` field.

## How to Run

Execute the main script from the root directory of the project:

```bash
python -m src.main

##The script will:

Initialize/reset the SQLite database (data/sales_warehouse.db).
Load data from data/sales_records.csv into the Sales table.
Run a "slow" query on the Sales table (before indexing CustomerSegment) and record its execution time.
Apply an optimization: create an index on the CustomerSegment column.
Run the same query again (now "optimized") and record its execution time.
Print a comparison of the execution times.
Perform automated data quality checks (e.g., nulls, uniqueness, value ranges) on the Sales table.
Generate a data quality report in reports/data_quality_report.txt.
