import pandas as pd
from app.utils.inspection_data_mapper import get_mapped_columns, INSPECTION_DATA_FIELD_MAPPING

# Load test file
df = pd.read_excel('test_duplicate_mapping.xlsx')
print("Original columns:", list(df.columns))

# Get mapped columns
mapped = get_mapped_columns(df.columns)
print(f"\nMapped columns ({len(mapped)}):")
for excel_col, db_col in mapped.items():
    print(f"  {excel_col} -> {db_col}")

# Rename columns according to mapping
df_renamed = df.rename(columns=mapped)
print(f"\nRenamed DataFrame columns: {list(df_renamed.columns)}")

# Check for duplicate columns after renaming
duplicate_cols = df_renamed.columns[df_renamed.columns.duplicated()].tolist()
if duplicate_cols:
    print(f"❌ DUPLICATE COLUMNS FOUND: {duplicate_cols}")
    print("This will cause SQL parameter duplication!")
else:
    print("✅ No duplicate columns after mapping")

print(f"\nDataFrame shape: {df_renamed.shape}")
print(f"DataFrame preview:\n{df_renamed}")