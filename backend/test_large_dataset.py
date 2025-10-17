"""
Test upload with large dataset similar to real scenario
"""
import sys, os
sys.path.append('/home/appuser/app')

import pandas as pd
import numpy as np
from app.utils.inspection_data_mapper import get_mapped_columns, get_all_inspection_data_columns
from app.utils.sql_server_connection import sql_server

def create_large_test_dataset():
    """Create a larger test dataset similar to real data with many NULL columns"""
    
    # Create 20 rows of test data (similar to error scenario)
    rows = 20
    
    # Base data with some values
    base_data = {
        'Inspection_ID': range(119557, 119557 + rows),
        'Machine_Type': ['komatsu'] * rows,
        'Model_Code': ['PC1250-8R'] * rows,
        'Serial_No': [f'SN{i:05d}' for i in range(rows)],
        'Inspected_By': ['M RIZKY ANANDA'] * rows,
        'Link_Type': ['GST'] * rows,
        'Link_Spec': ['STD'] * rows,
        'Bushing_Spec': ['STD'] * rows,
        'Track_Roller_Spec': ['STD'] * rows,
        'Equipment_Number': [f'EX {1186 + i}' for i in range(rows)],
        'SMR': [35250 + i * 10 for i in range(rows)],
        'Delivery_Date': ['2019-04-07'] * rows,
        'Inspection_Date': ['2025-08-28'] * rows,
        'Branch_Name': ['SEREAK'] * rows,
        'Customer_Name': ['PAMAPERSADA NUSANTARA'] * rows,
        'Job_Site': ['SEKTOR 7 PAMA - ABB'] * rows,
        'WorkingHourPerDay': [15.3] * rows,
    }
    
    # Get all database columns
    all_db_columns = get_all_inspection_data_columns()
    
    # Add columns that exist in database but not in base_data as NULL
    for col in all_db_columns:
        if col not in base_data and col != 'ID':
            # Create mostly NULL columns with some random values
            values = [None] * rows
            
            # Add some random non-NULL values for variety
            if 'Brand' in col:
                values[0] = 'KOMATSU'
            elif 'PercentWorn' in col:
                values[0] = 75.5
            elif 'History_SMR' in col:
                values[0] = 6800
            elif 'History_Date' in col or 'ReplaceDate' in col:
                values[0] = '2024-12-13'
            elif 'History_Hours' in col:
                values[0] = 3500.0
            elif col in ['UnderfootConditions_Terrain', 'UnderfootConditions_Abrasive', 'UnderfootConditions_Moisture', 'UnderfootConditions_Packing']:
                values[0] = 'High'
            elif col in ['ApplicationCode_Major', 'ApplicationCode_Minor']:
                values[0] = 'Mining'
            elif col in ['Application_Ground', 'Application_Working']:
                values[0] = 'Loading'
            elif 'Type' in col:
                values[0] = 'Standard'
            elif 'Width' in col:
                values[0] = 610.0
                
            base_data[col] = values
    
    return pd.DataFrame(base_data)

def test_large_dataset_upload():
    print("🧪 Testing large dataset upload (similar to real scenario)...")
    
    # Create test data
    df = create_large_test_dataset()
    print(f"📊 Created large test DataFrame: {df.shape}")
    
    # Check column mapping
    mapped = get_mapped_columns(df.columns.tolist())
    print(f"✅ Mapped {len(mapped)} out of {len(df.columns)} columns")
    
    # Get database columns and prepare final dataset
    all_db_columns = get_all_inspection_data_columns()
    available_columns = set(df.columns)
    final_columns = [col for col in all_db_columns if col in available_columns and col != 'ID']
    df_final = df[final_columns].copy()
    
    print(f"📊 Final DataFrame shape: {df_final.shape}")
    print(f"📊 Final columns count: {len(final_columns)}")
    
    # Data type conversion (same as in upload.py)
    print("🔄 Converting data types...")
    
    # Integer columns
    int_columns = ['Inspection_ID', 'SMR', 
                  'LinkPitch_History_SMR_LHS', 'LinkPitch_History_SMR_RHS',
                  'Bushings_History_SMR_LHS', 'Bushings_History_SMR_RHS',
                  'LinkHeight_History_SMR_LHS', 'LinkHeight_History_SMR_RHS',
                  'TrackShoe_History_SMR_LHS', 'TrackShoe_History_SMR_RHS',
                  'Idlers_History_SMR_LHS1', 'Idlers_History_SMR_RHS1',
                  'Sprocket_History_SMR_LHS', 'Sprocket_History_SMR_RHS']
    
    for col in int_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('Int64')
    
    # Date columns
    date_columns = ['Delivery_Date', 'Inspection_Date',
                   'LinkPitch_History_Date_LHS', 'LinkPitch_History_Date_RHS',
                   'LinkPitch_ReplaceDate_LHS', 'LinkPitch_ReplaceDate_RHS',
                   'Bushings_History_Date_LHS', 'Bushings_History_Date_RHS',
                   'Bushings_ReplaceDate_LHS', 'Bushings_ReplaceDate_RHS',
                   'LinkHeight_History_Date_LHS', 'LinkHeight_History_Date_RHS',
                   'LinkHeight_ReplaceDate_LHS', 'LinkHeight_ReplaceDate_RHS',
                   'TrackShoe_History_Date_LHS', 'TrackShoe_History_Date_RHS',
                   'TrackShoe_ReplaceDate_LHS', 'TrackShoe_ReplaceDate_RHS',
                   'Idlers_History_Date_LHS1', 'Idlers_History_Date_RHS1',
                   'Idlers_ReplaceDate_LHS1', 'Idlers_ReplaceDate_RHS1',
                   'Sprocket_History_Date_LHS', 'Sprocket_History_Date_RHS',
                   'Sprocket_ReplaceDate_LHS', 'Sprocket_ReplaceDate_RHS']
    
    for col in date_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_datetime(df_final[col], errors='coerce')
    
    # Decimal columns
    decimal_columns = ['WorkingHourPerDay', 'TrackShoe_Width',
                      'LinkPitch_History_Hours_LHS', 'LinkPitch_History_Hours_RHS',
                      'LinkPitch_PercentWorn_LHS', 'LinkPitch_PercentWorn_RHS',
                      'Bushings_History_Hours_LHS', 'Bushings_History_Hours_RHS', 
                      'Bushings_PercentWorn_LHS', 'Bushings_PercentWorn_RHS',
                      'LinkHeight_History_Hours_LHS', 'LinkHeight_History_Hours_RHS',
                      'LinkHeight_PercentWorn_LHS', 'LinkHeight_PercentWorn_RHS',
                      'TrackShoe_History_Hours_LHS', 'TrackShoe_History_Hours_RHS',
                      'TrackShoe_PercentWorn_LHS', 'TrackShoe_PercentWorn_RHS',
                      'Idlers_History_Hours_LHS1', 'Idlers_History_Hours_RHS1',
                      'Idlers_PercentWorn_LHS1', 'Idlers_PercentWorn_RHS1',
                      'Sprocket_History_Hours_LHS', 'Sprocket_History_Hours_RHS',
                      'Sprocket_PercentWorn_LHS', 'Sprocket_PercentWorn_RHS']
    
    for col in decimal_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
    
    print("✅ Data type conversion completed")
    
    # NULL value handling (same as in updated upload.py)
    print("🧹 Cleaning NULL values for pyodbc compatibility...")
    
    for col in df_final.columns:
        if df_final[col].dtype == 'datetime64[ns]':
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
        elif str(df_final[col].dtype).startswith('Int'):
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
        elif df_final[col].dtype in ['float64', 'float32']:
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
        elif df_final[col].dtype == 'object':
            df_final[col] = df_final[col].where(pd.notna(df_final[col]), None)
    
    # Convert numpy types to native Python types
    print("🔧 Converting numpy types to native Python types...")
    
    for col in df_final.columns:
        if str(df_final[col].dtype).startswith('Int'):
            df_final[col] = df_final[col].apply(lambda x: int(x) if pd.notna(x) and x is not None else None)
        elif df_final[col].dtype in ['float64', 'float32']:
            df_final[col] = df_final[col].apply(lambda x: float(x) if pd.notna(x) and x is not None else None)
        elif df_final[col].dtype in ['int64', 'int32']:
            df_final[col] = df_final[col].apply(lambda x: int(x) if pd.notna(x) and x is not None else None)
    
    print("✅ NULL value handling and type conversion completed")
    
    # Count NULLs in final dataset
    null_counts = {}
    for col in df_final.columns:
        null_count = sum(1 for x in df_final[col] if x is None)
        if null_count > 0:
            null_counts[col] = null_count
    
    print(f"\n📈 Final NULL counts: {len(null_counts)} columns have NULLs")
    print(f"📈 Total NULL values: {sum(null_counts.values())}")
    
    # Show sample of first row parameters
    print(f"\n🔍 Sample of first row parameters (first 10):")
    first_row = df_final.iloc[0]
    params = tuple(first_row.values)
    for i, param in enumerate(params[:10]):
        print(f"  [{i}] {type(param)} = {repr(param)}")
    
    # Test database insert
    print(f"\n💾 Testing database insert with {len(df_final)} rows and {len(df_final.columns)} columns...")
    try:
        if sql_server.test_connection():
            print("✅ Database connection successful")
            
            # Truncate table
            print("🗑️ Truncating InspectionData table...")
            sql_server.truncate_table('InspectionData')
            
            # Insert data
            records_inserted = sql_server.insert_dataframe_to_table(
                df_final, 
                'InspectionData',
                if_exists='append'
            )
            
            print(f"🎉 SUCCESS! Inserted {records_inserted} records with large dataset!")
            
        else:
            print("❌ Database connection failed")
            
    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_large_dataset_upload()