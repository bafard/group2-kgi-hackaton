#!/usr/bin/env python3
"""
Test full inspection data upload with actual Excel-like data
to verify the parameter binding issue is resolved.
"""

import sys
import os
sys.path.append('/home/appuser/app')

import pandas as pd
from app.utils.inspection_data_mapper import get_mapped_columns, get_all_inspection_data_columns
from app.utils.sql_server_connection import SQLServerConnection

def test_full_upload():
    """Test inspection data upload with realistic Excel data"""
    
    # Create realistic test data matching Excel format
    test_data = {
        'Inspection_ID': [119557, 119558, 119559, 119560, 119561],
        'Machine_Type': ['komatsu', 'komatsu', 'komatsu', 'komatsu', 'komatsu'],
        'Model_Code': ['PC200-8', 'PC200-8', 'PC350-8', 'PC200-8', 'PC350-8'],
        'Serial_No': ['A12345', 'A12346', 'A12347', 'A12348', 'A12349'],
        'Inspected_By': ['Inspector1', 'Inspector2', 'Inspector1', 'Inspector3', 'Inspector2'],
        'Link_Type': ['Master Pin', 'Master Pin', 'Master Pin', 'Master Pin', 'Master Pin'],
        'Link_Spec': ['Standard', 'Standard', 'Heavy Duty', 'Standard', 'Heavy Duty'],
        'Bushing_Spec': ['Standard', 'Standard', 'HD', 'Standard', 'HD'],
        'Track_Roller_Spec': ['Standard', 'Standard', 'HD', 'Standard', 'HD'],
        'Equipment_Number': ['EQ001', 'EQ002', 'EQ003', 'EQ004', 'EQ005'],
        'SMR': [35250, 35300, 35400, 35500, 35600],
        'Delivery_Date': ['2024-01-15', '2024-01-20', '2024-01-25', '2024-02-01', '2024-02-05'],
        'Inspection_Date': ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04', '2024-12-05'],
        'Branch_Name': ['Jakarta', 'Jakarta', 'Surabaya', 'Jakarta', 'Surabaya'],
        'Customer_Name': ['PT ABC', 'PT DEF', 'PT GHI', 'PT JKL', 'PT MNO'],
        'Job_Site': ['Site A', 'Site B', 'Site C', 'Site D', 'Site E'],
        'Attachments': ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf', 'file5.pdf'],
        'Comments': ['Good condition', 'Minor wear', 'Replace soon', 'Excellent', 'Check next month'],
        'WorkingHourPerDay': [8.0, 10.0, 12.0, 8.0, 10.0],
        'UnderfootConditions_Terrain': ['Rocky', 'Sandy', 'Clay', 'Rocky', 'Sandy'],
        'UnderfootConditions_Abrasive': ['High', 'Medium', 'Low', 'High', 'Medium'],
        'Sprocket_PercentWorn_RHS': [25.5, 30.0, 45.5, 15.0, 35.5],
        'Sprocket_PercentWorn_LHS': [26.0, 29.5, 46.0, 14.5, 36.0],
        'Sprocket_ReplaceDate_LHS': ['2024-06-01', '2024-07-15', '2024-03-20', '2024-08-10', '2024-05-25'],
        'Sprocket_ReplaceDate_RHS': ['2024-06-01', '2024-07-15', '2024-03-20', '2024-08-10', '2024-05-25']
    }
    
    df = pd.DataFrame(test_data)
    print(f"📊 Test DataFrame shape: {df.shape}")
    print(f"📊 Test columns: {list(df.columns)}")
    
    # Test mapping
    mapped = get_mapped_columns(df.columns.tolist())
    print(f"✅ Mapped {len(mapped)} out of {len(df.columns)} columns")
    
    # Map columns
    df_mapped = df.rename(columns=mapped)
    
    # Get database columns and filter to existing ones (exclude ID)
    all_db_columns = get_all_inspection_data_columns()
    available_columns = set(df_mapped.columns)
    final_columns = [col for col in all_db_columns if col in available_columns and col != 'ID']
    df_final = df_mapped[final_columns]
    
    print(f"📊 Final DataFrame shape: {df_final.shape}")
    print(f"📊 Final columns ({len(final_columns)}): {final_columns[:10]}...")
    
    # Convert data types
    print("🔄 Converting data types...")
    
    # Integer columns
    int_columns = ['Inspection_ID', 'SMR']
    for col in int_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('Int64')
            print(f"  ✅ Converted {col} to integer")
    
    # Date columns  
    date_columns = ['Delivery_Date', 'Inspection_Date', 'Sprocket_ReplaceDate_LHS', 'Sprocket_ReplaceDate_RHS']
    for col in date_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_datetime(df_final[col], errors='coerce')
            print(f"  ✅ Converted {col} to datetime")
    
    # Decimal columns  
    decimal_columns = ['WorkingHourPerDay', 'Sprocket_PercentWorn_LHS', 'Sprocket_PercentWorn_RHS']
    for col in decimal_columns:
        if col in df_final.columns:
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
            print(f"  ✅ Converted {col} to decimal")
    
    print(f"📊 Data types after conversion:")
    for col in df_final.columns[:10]:
        print(f"  {col}: {df_final[col].dtype}")
    
    # Test database insertion
    try:
        sql_server = SQLServerConnection()
        
        print("🗑️ Truncating InspectionData table...")
        sql_server.truncate_table("InspectionData")
        
        print("💾 Inserting test data to database...")
        records_processed = sql_server.insert_dataframe_to_table(
            df_final, 
            "InspectionData", 
            if_exists='append'
        )
        
        print(f"✅ SUCCESS! Inserted {records_processed} records successfully")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_upload()
    if success:
        print("\\n🎉 Test completed successfully!")
    else:
        print("\\n💥 Test failed!")