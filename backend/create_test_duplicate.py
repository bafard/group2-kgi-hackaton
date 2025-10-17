import pandas as pd

# Create simple test data with potential duplicate columns
data = {
    'Inspection ID': [119499],
    'Machine Type': ['komatsu'],
    'Model Code': ['PC1250-8R'],
    'Serial No': [35992],
    'Inspected By': ['M RIZKY ANANDA'],
    'SMR': [35000],
    'Equipment Number': ['EX 1186'],
    'Machine ID': ['EX 1186']  # This creates duplicate mapping to Equipment_Number
}

# Create DataFrame and save as Excel
df = pd.DataFrame(data)
df.to_excel('test_duplicate_mapping.xlsx', index=False)
print(f"Created test file with columns: {list(df.columns)}")
print(f"Data preview:\n{df}")