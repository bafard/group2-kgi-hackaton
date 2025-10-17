import pandas as pd
import requests
import os

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
test_file = 'test_duplicate_fix.xlsx'
df.to_excel(test_file, index=False)

print(f"Created test file: {test_file}")
print(f"Columns: {list(df.columns)}")
print(f"Rows: {len(df)}")

# Test upload via API
try:
    files = {'file': open(test_file, 'rb')}
    response = requests.post(
        'http://localhost:8001/api/upload-knowledge',
        files=files
    )
    
    print(f"\n📤 Upload response status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Upload successful!")
        print(response.json())
    else:
        print(f"❌ Upload failed: {response.text}")
        
except Exception as e:
    print(f"❌ Upload error: {str(e)}")
finally:
    if os.path.exists(test_file):
        os.remove(test_file)