#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')
import pandas as pd

from app.utils.inspection_data_mapper import (
    filter_excel_columns_for_database,
    map_excel_to_database_columns,
    get_all_inspection_data_columns
)
from app.utils.sql_server_connection import sql_server

try:
    print("=== TESTING DATA TYPE CONVERSION ===")
    
    # Create dummy data with proper data types
    dummy_data = {
        'Machine ID': ['M001'],  # Maps to Equipment_Number (string) 
        'Inspection Date': ['2024-01-15'],  # Maps to Inspection_Date (date)
        'Customer Name': ['Test Customer'],  # Maps to Customer_Name (string)
        'Comments': ['Test upload with data types'],  # Maps to Comments (string)
        'SMR': ['12345'],  # Integer field
        'LinkPitch_PercentWorn_LHS': ['85.5'],  # Decimal field
        'LinkPitch_History_Date_LHS': ['2023-12-01'],  # Date field
    }
    
    df = pd.DataFrame(dummy_data)
    print(f"📊 Original DataFrame: {df.shape}")
    print(f"📊 Original columns: {list(df.columns)}")
    
    # Apply the same process as in upload.py
    df_filtered = filter_excel_columns_for_database(df)
    column_mapping = map_excel_to_database_columns(df_filtered)
    df_mapped = df_filtered.rename(columns=column_mapping)
    all_db_columns = get_all_inspection_data_columns()
    
    # Only keep columns that actually exist in the database
    final_columns = [col for col in df_mapped.columns if col in all_db_columns]
    df_final = df_mapped[final_columns]
    
    print(f"\n📊 Before type conversion:")
    print(df_final.dtypes)
    
    # Apply data type conversions (same as in upload.py)
    print("\n🔄 Converting data types...")
    
    # Integer columns
    int_columns = ['SMR']
    for col in int_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('Int64')
            print(f"  ✅ Converted {col} to integer")
    
    # Date columns  
    date_columns = ['Inspection_Date', 'LinkPitch_History_Date_LHS']
    for col in date_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_datetime(df_final[col], errors='coerce')
            print(f"  ✅ Converted {col} to datetime")
    
    # Decimal columns
    decimal_columns = ['LinkPitch_PercentWorn_LHS']
    for col in decimal_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
            print(f"  ✅ Converted {col} to decimal")
    
    print(f"\n📊 After type conversion:")
    print(df_final.dtypes)
    print(f"\n📊 Sample data:")
    print(df_final.head())
    
    # Test database insertion
    print(f"\n🧪 Testing database insertion...")
    try:
        records_processed = sql_server.insert_dataframe_to_table(
            df_final, 
            'InspectionData', 
            if_exists='append'
        )
        print(f"✅ SUCCESS! Inserted {records_processed} records")
        
    except Exception as insert_error:
        print(f"❌ INSERT FAILED: {insert_error}")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()