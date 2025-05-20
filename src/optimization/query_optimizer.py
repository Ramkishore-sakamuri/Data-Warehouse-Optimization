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
