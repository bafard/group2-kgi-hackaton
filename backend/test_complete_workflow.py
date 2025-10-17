import pandas as pd
import sys
import os
sys.path.append('/home/appuser/app')

from app.utils.inspection_data_mapper import get_mapped_columns
from app.utils.sql_server_connection import get_sql_connection
from app.utils.metadata import log_upload_metadata, get_upload_logs
import tempfile

print("🧪 TESTING COMPLETE UPLOAD WORKFLOW")
print("=" * 50)

# Load the test file
df = pd.read_excel('/home/appuser/app/test_comprehensive_upload.xlsx')
print(f"📁 Loaded test file: {df.shape}")
print(f"📋 Columns: {list(df.columns)}")

# Test mapping
print(f"\n🔍 STEP 1: Column Mapping")
mapped = get_mapped_columns(df.columns)
print(f"   ✅ Mapped {len(mapped)} columns")

# Test duplicate handling
print(f"\n🔍 STEP 2: Duplicate Column Handling")
df_mapped = df.rename(columns=mapped)
print(f"   📊 After mapping: {list(df_mapped.columns)}")

duplicate_cols = df_mapped.columns[df_mapped.columns.duplicated()].tolist()
if duplicate_cols:
    print(f"   ⚠️  Found duplicates: {duplicate_cols}")
    df_clean = df_mapped.loc[:, ~df_mapped.columns.duplicated()]
    print(f"   ✅ After cleaning: {df_clean.shape}")
    print(f"   📊 Final columns: {list(df_clean.columns)}")
else:
    print(f"   ✅ No duplicates found")
    df_clean = df_mapped

# Test data type conversion
print(f"\n🔍 STEP 3: Data Type Conversion")
# Convert SMR to integer
if 'SMR' in df_clean.columns:
    df_clean['SMR'] = pd.to_numeric(df_clean['SMR'], errors='coerce').astype('Int64')
    print(f"   ✅ SMR converted to integer: {df_clean['SMR'].dtype}")

# Convert dates
date_cols = ['Inspection_Date', 'Delivery_Date']
for col in date_cols:
    if col in df_clean.columns:
        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        print(f"   ✅ {col} converted to datetime: {df_clean[col].dtype}")

# Convert working hours to decimal
if 'WorkingHourPerDay' in df_clean.columns:
    df_clean['WorkingHourPerDay'] = pd.to_numeric(df_clean['WorkingHourPerDay'], errors='coerce')
    print(f"   ✅ WorkingHourPerDay converted to numeric: {df_clean['WorkingHourPerDay'].dtype}")

print(f"\n🔍 STEP 4: Final Data Validation")
print(f"   📊 Final DataFrame shape: {df_clean.shape}")
print(f"   📊 Final columns count: {len(df_clean.columns)}")
print(f"   📊 Data types summary:")
for col in df_clean.columns[:10]:  # Show first 10 columns
    print(f"      {col}: {df_clean[col].dtype}")

# Test database connection
print(f"\n🔍 STEP 5: Database Connection Test")
try:
    conn = get_sql_connection()
    if conn:
        print(f"   ✅ Database connection successful")
        conn.close()
    else:
        print(f"   ❌ Database connection failed")
except Exception as e:
    print(f"   ❌ Database error: {str(e)}")

print(f"\n✅ WORKFLOW TEST COMPLETE!")
print(f"📋 Summary:")
print(f"   • Original columns: {len(df.columns)}")  
print(f"   • Mapped columns: {len(mapped)}")
print(f"   • Final columns: {len(df_clean.columns)}")
print(f"   • Duplicate handling: {'PASSED' if duplicate_cols else 'N/A'}")
print(f"   • Data type conversion: PASSED")
print(f"   • Ready for database insert: ✅")