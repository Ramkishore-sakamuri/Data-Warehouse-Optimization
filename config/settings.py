import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'sales_warehouse.db')
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'sales_records.csv')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Ensure reports directory exists
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)
