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
