#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')
import pandas as pd

from app.utils.inspection_data_mapper import (
    get_all_inspection_data_columns, 
    filter_excel_columns_for_database,
    map_excel_to_database_columns
)
from app.utils.sql_server_connection import sql_server

try:
    print("=== TESTING UPLOAD PROCESS ===")
    
    # Create a dummy DataFrame like Excel would have
    dummy_data = {
        'Machine ID': ['M001'],
        'Inspection Date': ['2024-01-15'],
        'Customer Name': ['Test Customer'],
        'Comments': ['Test upload'],
        'LinkPitch_Brand_LHS': ['Komatsu'],
        'Idlers_Brand_LHS1': ['CAT']
    }
    
    df = pd.DataFrame(dummy_data)
    print(f"📊 Original DataFrame: {df.shape}")
    print(f"📊 Original columns: {list(df.columns)}")
    
    # Test the upload process
    df_filtered = filter_excel_columns_for_database(df)
    column_mapping = map_excel_to_database_columns(df_filtered)
    df_mapped = df_filtered.rename(columns=column_mapping)
    all_db_columns = get_all_inspection_data_columns()
    
    # Only keep columns that actually exist in the database
    final_columns = [col for col in df_mapped.columns if col in all_db_columns]
    df_final = df_mapped[final_columns]
    
    print(f"\n📊 Final DataFrame: {df_final.shape}")
    print(f"📊 Final columns: {list(df_final.columns)}")
    
    # Test inserting just one row
    print(f"\n🧪 Testing database insertion...")
    
    # Check if all final columns exist in database
    col_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData'
    """
    db_result = sql_server.execute_query(col_query)
    db_cols = set([row[0] for row in db_result])
    
    bad_cols = [col for col in df_final.columns if col not in db_cols]
    if bad_cols:
        print(f"❌ Found bad columns: {bad_cols}")
    else:
        print(f"✅ All {len(df_final.columns)} columns exist in database")
        
        # Try to insert (with dry-run first)
        print(f"\n🔍 Columns that would be inserted:")
        for i, col in enumerate(df_final.columns):
            print(f"  {i+1}. {col}")
        
        print(f"\n📝 Sample row data:")
        for col in df_final.columns:
            print(f"  {col}: {df_final[col].iloc[0]}")
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()