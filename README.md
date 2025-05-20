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


##The script will:

Initialize/reset the SQLite database (data/sales_warehouse.db).
Load data from data/sales_records.csv into the Sales table.
Run a "slow" query on the Sales table (before indexing CustomerSegment) and record its execution time.
Apply an optimization: create an index on the CustomerSegment column.
Run the same query again (now "optimized") and record its execution time.
Print a comparison of the execution times.
Perform automated data quality checks (e.g., nulls, uniqueness, value ranges) on the Sales table.
Generate a data quality report in reports/data_quality_report.txt.
