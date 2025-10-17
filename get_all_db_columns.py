#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')

from app.utils.sql_server_connection import sql_server

try:
    # Get all columns from actual database
    col_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData'
    ORDER BY ORDINAL_POSITION
    """
    db_result = sql_server.execute_query(col_query)
    db_cols = [row[0] for row in db_result]
    
    print(f"Total database columns: {len(db_cols)}")
    print("\n# All database columns:")
    print("return [")
    for i, col in enumerate(db_cols):
        print(f"    '{col}',")
    print("]")
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()