#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')
import pandas as pd

from app.utils.inspection_data_mapper import get_all_inspection_data_columns
from app.utils.sql_server_connection import sql_server

try:
    print("=== TESTING REAL DATABASE INSERT ===")
    
    # Get only columns that actually exist in database
    all_db_columns = get_all_inspection_data_columns()
    print(f"Database has {len(all_db_columns)} columns")
    
    # Create DataFrame with only valid database columns
    # Use first 5 columns for testing
    test_columns = all_db_columns[:5]
    print(f"Testing with columns: {test_columns}")
    
    # Create dummy data 
    dummy_data = {}
    for col in test_columns:
        if col == 'ID':
            dummy_data[col] = [None]  # Let database auto-increment
        elif 'Date' in col:
            dummy_data[col] = ['2024-01-15']
        elif col in ['SMR', 'Equipment_Number']:
            dummy_data[col] = ['TEST001']
        else:
            dummy_data[col] = ['Test Value']
    
    df = pd.DataFrame(dummy_data)
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {list(df.columns)}")
    
    # Remove ID column for insert (auto-increment)
    if 'ID' in df.columns:
        df = df.drop('ID', axis=1)
        print("Removed ID column for insert")
    
    print(f"Final DataFrame for insert:")
    print(df.head())
    
    # Try actual insert
    print(f"\n🧪 Attempting database insert...")
    
    try:
        records_processed = sql_server.insert_dataframe_to_table(
            df, 
            'InspectionData', 
            if_exists='append'
        )
        print(f"✅ SUCCESS! Inserted {records_processed} records")
        
    except Exception as insert_error:
        print(f"❌ INSERT FAILED: {insert_error}")
        # Print more details about the error
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()