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
