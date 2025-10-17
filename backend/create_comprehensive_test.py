import pandas as pd

# Create comprehensive test data with potential duplicate mappings
data = {
    # Basic fields
    'Inspection ID': [119499, 119500, 119501],
    'Machine Type': ['komatsu', 'hitachi', 'caterpillar'], 
    'Model Code': ['PC1250-8R', 'EX1200', 'CAT385'],
    'Serial No': [35992, 35993, 35994],
    'Inspected By': ['M RIZKY ANANDA', 'JOHN DOE', 'JANE SMITH'],
    'SMR': [35000, 36000, 37000],
    
    # Duplicate mapping scenario
    'Equipment Number': ['EX 1186', 'EX 1187', 'EX 1188'],
    'Machine ID': ['EX 1186', 'EX 1187', 'EX 1188'],  # Both map to Equipment_Number
    
    # Additional fields
    'Inspection Date': ['2025-07-29', '2025-07-30', '2025-07-31'],
    'Delivery Date': ['2019-04-07', '2020-05-15', '2021-06-20'],
    'Customer Name': ['PAMAPERSADA NUSANTARA', 'ADARO ENERGY', 'KALTIM PRIMA COAL'],
    'Branch Name': ['SEREAK', 'SAMARINDA', 'BALIKPAPAN'],
    'Job Site': ['SEKTOR 7 PAMA - ABB', 'SITE ADARO 1', 'SITE KPC 2'],
    'Working Hour Per Day': [15.3, 16.5, 14.8],
    
    # Component data
    'Link Type': ['GST', 'STD', 'HDY'],
    'Link Spec': ['STD', 'STD', 'HVY'],
    'Bushing Spec': ['STD', 'STD', 'HVY'],
    'Track Roller Spec': ['STD', 'STD', 'HVY'],
    
    # Working conditions
    'Underfoot Conditions Terrain': ['LEVEL', 'HILLY', 'ROUGH'],
    'Underfoot Conditions Abrasive': ['High', 'Medium', 'Low'], 
    'Underfoot Conditions Moisture': ['High', 'Medium', 'Dry'],
    'Underfoot Conditions Packing': ['High', 'Medium', 'Low'],
    
    # Application
    'Application Code Major': ['Mining', 'Construction', 'Mining'],
    'Application Code Minor': ['Coal Mining', 'Road Building', 'Quarry'],
    'Application Ground': ['General Sand', 'Hard Rock', 'Coal'],
    'Application Working': ['Loading', 'Excavation', 'Loading']
}

# Create DataFrame and save as Excel
df = pd.DataFrame(data)
test_file = 'test_comprehensive_upload.xlsx'
df.to_excel(test_file, index=False)

print(f"✅ Created {test_file}")
print(f"📊 Columns: {len(df.columns)}")  
print(f"📊 Rows: {len(df)}")
print(f"📊 Columns: {list(df.columns)}")

# Show potential duplicate mapping
print(f"\n⚠️  Potential duplicate mapping:")
print(f"   'Equipment Number' and 'Machine ID' both map to 'Equipment_Number'")
print(f"   Values: {df[['Equipment Number', 'Machine ID']].to_dict('records')}")

print(f"\n💾 File saved as: {test_file}")
print(f"📂 You can now upload this file via the web interface to test the fix")