"""
Test comprehensive NULL value handling in upload scenario
"""
import sys, os
sys.path.append('/home/appuser/app')

import pandas as pd
import numpy as np
from app.utils.inspection_data_mapper import get_mapped_columns, get_all_inspection_data_columns
from app.utils.sql_server_connection import sql_server

def create_test_data_with_nulls():
    """Create test data with various NULL scenarios"""
    
    # Data with mixed NULL values
    data = {
        'Inspection_ID': [119557, 119558, 119559],
        'Machine_Type': ['komatsu', None, 'komatsu'],  # String NULL
        'Model_Code': ['PC200-8', 'PC200-8', None],    # String NULL
        'Serial_No': ['A12345', 'A12346', 'A12347'],
        'Inspected_By': ['User1', 'User2', 'User3'],
        'Link_Type': ['GST', None, 'GST'],             # String NULL
        'Link_Spec': ['STD', 'STD', None],             # String NULL
        'Bushing_Spec': ['STD', 'STD', 'STD'],
        'Track_Roller_Spec': ['STD', None, 'STD'],     # String NULL
        'Equipment_Number': ['EQ001', 'EQ002', 'EQ003'],
        'SMR': [35250, None, 35400],                   # Integer NULL
        'Delivery_Date': ['2019-04-07', None, '2019-04-09'],  # Date NULL
        'Inspection_Date': ['2025-08-28', '2025-08-29', None], # Date NULL
        'Branch_Name': ['SEREAK', 'BRANCH2', 'BRANCH3'],
        'Customer_Name': ['CUSTOMER1', None, 'CUSTOMER3'],     # String NULL
        'Job_Site': ['SITE1', 'SITE2', None],                 # String NULL
        'Attachments': [None, None, None],                     # All NULL
        'Comments': [None, 'Test comment', None],              # Mixed NULL
        'WorkingHourPerDay': [15.3, None, 12.5],              # Decimal NULL
        'UnderfootConditions_Terrain': ['LEVEL', None, 'SLOPE'], # String NULL
        'UnderfootConditions_Abrasive': ['High', 'Medium', None], # String NULL
        'Sprocket_PercentWorn_RHS': [76.93, None, 80.5],      # Decimal NULL
        'Sprocket_PercentWorn_LHS': [77.85, 75.2, None],      # Decimal NULL
        'Sprocket_ReplaceDate_LHS': ['2024-12-13', None, '2024-12-15'], # Date NULL
        'Sprocket_ReplaceDate_RHS': ['2024-12-10', '2024-12-11', None], # Date NULL
    }
    
    return pd.DataFrame(data)

def test_null_handling_comprehensive():
    print("🧪 Testing comprehensive NULL value handling...")
    
    # Create test data
    df = create_test_data_with_nulls()
    print(f"📊 Created test DataFrame: {df.shape}")
    print(f"📊 Columns: {list(df.columns)[:5]}... (showing first 5)")
    
    # Check initial NULL counts
    print("\n📈 Initial NULL counts:")
    for col in df.columns:
        null_count = df[col].isna().sum()
        if null_count > 0:
            print(f"  {col}: {null_count} NULLs")
    
    # Step 1: Map columns
    mapped = get_mapped_columns(df.columns.tolist())
    print(f"\n✅ Mapped {len(mapped)} out of {len(df.columns)} columns")
    
    # Step 2: Get all database columns and filter
    all_db_columns = get_all_inspection_data_columns()
    available_columns = set(df.columns)
    final_columns = [col for col in all_db_columns if col in available_columns and col != 'ID']
    df_final = df[final_columns].copy()
    
    print(f"\n📊 Final DataFrame for database: {df_final.shape}")
    print(f"📊 Columns: {list(df_final.columns)[:5]}... (showing first 5)")
    
    # Step 3: Convert data types
    print("\n🔄 Converting data types...")
    
    # Integer columns
    int_columns = ['Inspection_ID', 'SMR']
    for col in int_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('Int64')
            print(f"  ✅ Converted {col} to Int64")
    
    # Date columns
    date_columns = ['Delivery_Date', 'Inspection_Date', 'Sprocket_ReplaceDate_LHS', 'Sprocket_ReplaceDate_RHS']
    for col in date_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_datetime(df_final[col], errors='coerce')
            print(f"  ✅ Converted {col} to datetime")
    
    # Decimal columns
    decimal_columns = ['WorkingHourPerDay', 'Sprocket_PercentWorn_LHS', 'Sprocket_PercentWorn_RHS']
    for col in decimal_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
            print(f"  ✅ Converted {col} to float")
    
    # Step 4: Handle NULL values for pyodbc
    print("\n🧹 Cleaning NULL values for pyodbc compatibility...")
    
    for col in df_final.columns:
        # Handle datetime columns - replace NaT with None
        if df_final[col].dtype == 'datetime64[ns]':
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
            
        # Handle nullable integer columns - replace <NA> with None
        elif str(df_final[col].dtype).startswith('Int'):
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
            
        # Handle float columns - replace NaN with None
        elif df_final[col].dtype in ['float64', 'float32']:
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
            
        # Handle object columns - replace NaN with None
        elif df_final[col].dtype == 'object':
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
    
    # Convert numpy types to native Python types
    print("\n🔧 Converting numpy types to native Python types...")
    
    for col in df_final.columns:
        if str(df_final[col].dtype).startswith('Int'):
            df_final[col] = df_final[col].apply(lambda x: int(x) if pd.notna(x) and x is not None else None)
        elif df_final[col].dtype in ['float64', 'float32']:
            df_final[col] = df_final[col].apply(lambda x: float(x) if pd.notna(x) and x is not None else None)
    
    print("✅ NULL value handling completed")
    
    # Step 5: Check final data types and sample
    print("\n📊 Final data types and sample values:")
    for col in df_final.columns[:10]:  # Show first 10 columns
        sample_val = df_final[col].iloc[0]
        print(f"  {col}: {type(sample_val)} = {repr(sample_val)}")
    
    # Step 6: Test database insert
    print(f"\n💾 Testing database insert with {len(df_final)} rows...")
    try:
        # Test connection first
        if sql_server.test_connection():
            print("✅ Database connection successful")
            
            # Truncate test - use a safe approach
            print("🗑️ Truncating InspectionData table...")
            sql_server.truncate_table('InspectionData')
            print("✅ Table truncated")
            
            # Insert data
            records_inserted = sql_server.insert_dataframe_to_table(
                df_final, 
                'InspectionData',
                if_exists='append'
            )
            
            print(f"🎉 SUCCESS! Inserted {records_inserted} records with NULL values")
            
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        print(f"Error type: {type(e)}")
        
        # Show first row parameters for debugging
        print(f"\n🔍 First row parameters for debugging:")
        first_row = df_final.iloc[0]
        params = tuple(first_row.values)
        for i, param in enumerate(params):
            print(f"  [{i}] {type(param)} = {repr(param)}")

if __name__ == "__main__":
    test_null_handling_comprehensive()