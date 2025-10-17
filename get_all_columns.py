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
    
    # Get all column information
    cursor.execute("""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH, ORDINAL_POSITION
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData' 
    ORDER BY ORDINAL_POSITION
    """)
    
    columns = cursor.fetchall()
    print(f'Found {len(columns)} columns in InspectionData table:\n')
    
    # Generate Python list for inspection_data_mapper.py
    print('def get_all_inspection_data_columns():')
    print('    """Return all actual column names from InspectionData table"""')
    print('    columns = [')
    
    # Group columns by 10 for better readability
    for i in range(0, len(columns), 10):
        chunk = columns[i:i+10]
        line_items = [f"'{col[0]}'" for col in chunk]
        print(f'        {", ".join(line_items)},')
    
    print('    ]')
    print('    return columns')
    print()
    
    # Also show problematic columns that don't exist
    problem_cols = ['LinkPitch_Loose', 'LinkPitch_Welded']
    existing_cols = [col[0] for col in columns]
    
    print('Columns that do not exist in database:')
    for prob_col in problem_cols:
        if prob_col not in existing_cols:
            print(f'  ❌ {prob_col}')
    
    print()
    print('Similar columns that DO exist:')
    for col in existing_cols:
        if 'LinkPitch' in col:
            print(f'  ✅ {col}')
    
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')