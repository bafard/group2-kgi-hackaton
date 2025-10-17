import pyodbc
import os

# Database connection
host = "10.146.89.65"
port = "1433"
database = "RAGPrototipe"
username = "KUIICT"
password = "Komatsu12345678"
driver = "FreeTDS"

connection_string = f'DRIVER={{{driver}}};SERVER={host};PORT={port};DATABASE={database};UID={username};PWD={password};'

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Get column information
    cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData' 
    ORDER BY ORDINAL_POSITION
    """)
    
    columns = cursor.fetchall()
    print(f'Found {len(columns)} columns in InspectionData table:')
    print()
    
    # Look for LinkPitch related columns
    linkpitch_cols = [col for col in columns if 'LinkPitch' in col[0] or 'linkpitch' in col[0].lower()]
    print('LinkPitch related columns:')
    for col in linkpitch_cols:
        print(f'  - {col[0]} ({col[1]})')
    print()
        
    # Look for columns that might be similar to LinkPitch_Loose
    loose_cols = [col for col in columns if 'loose' in col[0].lower()]
    print('Columns containing "loose":')
    for col in loose_cols:
        print(f'  - {col[0]} ({col[1]})')
    print()
    
    # Show all column names for reference
    print('All columns (first 50):')
    for i, col in enumerate(columns[:50]):
        print(f'  {i+1:3d}. {col[0]}')
    
    if len(columns) > 50:
        print(f'  ... and {len(columns) - 50} more columns')
    
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')