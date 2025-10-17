"""
Test NULL value handling in pyodbc parameter binding
"""
import sys, os
sys.path.append('/home/appuser/app')

import pandas as pd
import numpy as np
from app.utils.sql_server_connection import SQLServerConnection

def test_null_handling():
    print("🧪 Testing NULL value handling...")
    
    # Create test data with NULL values
    data = {
        'Inspection_ID': [119557],
        'Machine_Type': ['komatsu'],
        'Model_Code': ['PC200-8'],
        'Serial_No': [None],  # NULL value
        'Inspected_By': ['TEST USER'],
        'SMR': [35250],
        'Comments': [None],   # NULL value
        'WorkingHourPerDay': [None],  # NULL decimal value
        'Delivery_Date': [pd.NaT],    # NULL date value
        'Equipment_Number': ['EQ001']
    }
    
    df = pd.DataFrame(data)
    
    print("📊 Original data types:")
    for col in df.columns:
        print(f"  {col}: {df[col].dtype} = {df[col].iloc[0]}")
    
    # Convert NULL handling
    print("\n🔄 Converting NULL values for pyodbc...")
    
    # Replace pandas NaT and None with proper NULL
    for col in df.columns:
        # Replace pandas NaT (Not a Time) with None
        if df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].where(pd.notna(df[col]), None)
        
        # Replace NaN with None for numeric columns
        elif df[col].dtype in ['float64', 'Int64']:
            df[col] = df[col].where(pd.notna(df[col]), None)
        
        # Ensure string None stays as None
        elif df[col].dtype == 'object':
            df[col] = df[col].where(pd.notna(df[col]), None)
    
    print("\n📊 After NULL conversion:")
    for col in df.columns:
        val = df[col].iloc[0]
        print(f"  {col}: {type(val)} = {repr(val)}")
    
    # Test parameter creation
    print("\n🧪 Testing parameter creation...")
    row = df.iloc[0]
    params = tuple(row.values)
    
    print(f"Parameters count: {len(params)}")
    for i, param in enumerate(params):
        print(f"  [{i}] {type(param)} = {repr(param)}")
    
    # Test database connection
    print("\n💾 Testing database insert with NULL values...")
    try:
        sql_server = SQLServerConnection()
        
        # Create a simple test table query
        columns = list(df.columns)
        placeholders = ', '.join(['?' for _ in columns])
        sql = f"SELECT {placeholders}"
        
        print(f"SQL: {sql}")
        print(f"Params: {params}")
        
        # Try to execute with cursor (simpler test)
        with sql_server.engine.raw_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchone()
            print(f"✅ SQL execution successful: {result}")
            
    except Exception as e:
        print(f"❌ SQL execution failed: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_null_handling()