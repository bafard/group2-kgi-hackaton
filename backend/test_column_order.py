import pandas as pd
import sys
sys.path.append('/home/appuser/app')

from app.utils.inspection_data_mapper import get_all_inspection_data_columns

print("🧪 TESTING COLUMN ORDER FIX")
print("=" * 40)

# Get database column order
db_columns = get_all_inspection_data_columns()
print(f"Database columns ({len(db_columns)}):")

# Find Sprocket columns
sprocket_indices = []
for i, col in enumerate(db_columns):
    if 'Sprocket_PercentWorn' in col:
        sprocket_indices.append((i, col))
        print(f"  {i:3d}. {col}")

print(f"\nSprocket PercentWorn order in database list: {[col for _, col in sprocket_indices]}")

# Create test data in exact database column order
test_data = {}
for col in db_columns:
    if col == 'Inspection_ID':
        test_data[col] = [119499]
    elif col == 'Machine_Type':
        test_data[col] = ['komatsu']  
    elif col == 'SMR':
        test_data[col] = [35000]
    elif col == 'Sprocket_PercentWorn_RHS':
        test_data[col] = [68.94]
    elif col == 'Sprocket_PercentWorn_LHS':
        test_data[col] = [68.94]
    else:
        # Default values for other columns
        if 'Date' in col:
            test_data[col] = [None]
        elif 'SMR' in col or 'Hours' in col:
            test_data[col] = [0]
        elif 'PercentWorn' in col:
            test_data[col] = [0.0]
        else:
            test_data[col] = [None]

# Create DataFrame in exact database order
df_test = pd.DataFrame(test_data)
print(f"\nTest DataFrame created: {df_test.shape}")
print(f"Column order matches database: {list(df_test.columns) == db_columns}")

# Check Sprocket columns specifically
sprocket_in_df = [col for col in df_test.columns if 'Sprocket_PercentWorn' in col]
print(f"Sprocket columns in DataFrame: {sprocket_in_df}")

print("✅ Column order test completed!")