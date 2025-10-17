import pandas as pd
import sys
import os
sys.path.append('/home/appuser/app')

from app.utils.inspection_data_mapper import get_mapped_columns, INSPECTION_DATA_FIELD_MAPPING
from app.utils.sql_server_connection import insert_dataframe_to_database

# Create test file with duplicate mappings
data = {
    'Inspection ID': [119499, 119500],
    'Machine Type': ['komatsu', 'hitachi'],
    'Model Code': ['PC1250-8R', 'EX1200'],
    'Serial No': [35992, 35993],
    'Inspected By': ['M RIZKY ANANDA', 'JOHN DOE'],
    'SMR': [35000, 36000],
    'Equipment Number': ['EX 1186', 'EX 1187'],
    'Machine ID': ['EX 1186', 'EX 1187'],  # This creates duplicate mapping
    'Inspection Date': ['2025-07-29', '2025-07-30'],
    'Working Hour Per Day': [15.3, 16.5]
}

df = pd.DataFrame(data)
print("Original DataFrame:")
print(f"Columns: {list(df.columns)}")
print(f"Shape: {df.shape}")

# Test the duplicate handling logic
print("\n🔍 Testing duplicate mapping handling...")

# Get mapped columns
mapped = get_mapped_columns(df.columns)
print(f"\nMapped columns ({len(mapped)}):")
for excel_col, db_col in mapped.items():
    print(f"  {excel_col} -> {db_col}")

# Rename columns
df_mapped = df.rename(columns=mapped)
print(f"\nAfter rename - Columns: {list(df_mapped.columns)}")

# Check for duplicates
duplicate_cols = df_mapped.columns[df_mapped.columns.duplicated()].tolist()
if duplicate_cols:
    print(f"⚠️  Found duplicate columns: {duplicate_cols}")
    print("Original shape:", df_mapped.shape)
    
    # Remove duplicates (keep first occurrence)
    df_mapped = df_mapped.loc[:, ~df_mapped.columns.duplicated()]
    print(f"✅ After removing duplicates - Shape: {df_mapped.shape}")
    print(f"✅ After removing duplicates - Columns: {list(df_mapped.columns)}")
else:
    print("✅ No duplicates found")

print(f"\nFinal DataFrame:")
print(df_mapped)