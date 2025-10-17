import pandas as pd
import sys
import traceback
sys.path.append('/home/appuser/app')

from app.utils.inspection_data_mapper import get_all_inspection_data_columns, get_mapped_columns

print("🔍 DEBUGGING PARAMETER MISMATCH")
print("=" * 50)

# Simulate the exact process
try:
    # Create minimal test data
    test_data = {
        'Inspection_ID': [119557],
        'Machine_Type': ['komatsu'], 
        'SMR': [35250]
    }
    
    df = pd.DataFrame(test_data)
    print(f"✅ Created test DataFrame: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Data types: {df.dtypes.to_dict()}")
    
    # Get mapping
    mapped = get_mapped_columns(df.columns)
    print(f"\n✅ Mapped columns: {mapped}")
    
    # Rename columns
    df_mapped = df.rename(columns=mapped)
    print(f"✅ After rename: {list(df_mapped.columns)}")
    
    # Get database columns
    db_cols = get_all_inspection_data_columns()
    print(f"✅ Database columns count: {len(db_cols)}")
    
    # Filter columns (exclude ID)
    available_columns = set(df_mapped.columns)
    final_columns = [col for col in db_cols if col in available_columns and col != 'ID']
    print(f"✅ Final columns: {final_columns}")
    
    # Create final DataFrame
    df_final = df_mapped[final_columns]
    print(f"✅ Final DataFrame shape: {df_final.shape}")
    print(f"   Final columns: {list(df_final.columns)}")
    print(f"   Final data types: {df_final.dtypes.to_dict()}")
    
    # Check first row values
    if len(df_final) > 0:
        first_row = df_final.iloc[0]
        print(f"\n✅ First row values:")
        for col, val in first_row.items():
            print(f"   {col}: {val} ({type(val)})")
    
    print(f"\n✅ Ready for database insert!")
    print(f"   Columns count: {len(df_final.columns)}")
    print(f"   Should be 102 or less")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(traceback.format_exc())