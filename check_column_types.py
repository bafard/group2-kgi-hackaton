#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')

from app.utils.sql_server_connection import sql_server

try:
    print("=== CHECKING DATABASE COLUMN TYPES ===")
    
    # Get column information including data types
    col_query = """
    SELECT 
        COLUMN_NAME, 
        DATA_TYPE, 
        IS_NULLABLE,
        COLUMN_DEFAULT,
        CHARACTER_MAXIMUM_LENGTH
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData'
    ORDER BY ORDINAL_POSITION
    """
    
    db_result = sql_server.execute_query(col_query)
    
    print(f"Found {len(db_result)} columns:")
    print(f"{'Column Name':<30} {'Type':<15} {'Nullable':<8} {'Default':<10} {'Max Len':<8}")
    print("-" * 80)
    
    int_columns = []
    datetime_columns = []
    required_columns = []
    
    for row in db_result:
        col_name = row[0]
        data_type = row[1]
        is_nullable = row[2]
        default_val = row[3] if row[3] else ''
        max_length = row[4] if row[4] else ''
        
        print(f"{col_name:<30} {data_type:<15} {is_nullable:<8} {str(default_val):<10} {str(max_length):<8}")
        
        # Categorize columns by type
        if data_type in ['int', 'bigint', 'smallint', 'tinyint']:
            int_columns.append(col_name)
        elif data_type in ['datetime', 'datetime2', 'date', 'time']:
            datetime_columns.append(col_name)
        if is_nullable == 'NO':
            required_columns.append(col_name)
    
    print(f"\n=== COLUMN ANALYSIS ===")
    print(f"Integer columns ({len(int_columns)}):")
    for col in int_columns:
        print(f"  {col}")
    
    print(f"\nDateTime columns ({len(datetime_columns)}):")
    for col in datetime_columns:
        print(f"  {col}")
    
    print(f"\nRequired (NOT NULL) columns ({len(required_columns)}):")
    for col in required_columns:
        print(f"  {col}")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()