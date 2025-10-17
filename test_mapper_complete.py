#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')

from app.utils.inspection_data_mapper import get_all_inspection_data_columns, map_excel_to_database_columns
from app.utils.sql_server_connection import sql_server

try:
    print("=== INSPECTION DATA MAPPER VALIDATION ===")
    
    # Get columns from mapper
    mapper_cols = get_all_inspection_data_columns()
    print(f'Mapper has {len(mapper_cols)} columns')
    
    # Get columns from actual database
    col_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData'
    ORDER BY ORDINAL_POSITION
    """
    db_result = sql_server.execute_query(col_query)
    db_cols = [row[0] for row in db_result]
    print(f'Database has {len(db_cols)} columns')
    
    # Find missing columns in mapper
    missing_in_mapper = set(db_cols) - set(mapper_cols)
    print(f'\nColumns in database but missing in mapper ({len(missing_in_mapper)}):')
    for col in sorted(missing_in_mapper):
        print(f'  - {col}')
    
    # Find extra columns in mapper
    extra_in_mapper = set(mapper_cols) - set(db_cols)
    print(f'\nColumns in mapper but missing in database ({len(extra_in_mapper)}):')
    for col in sorted(extra_in_mapper):
        print(f'  - {col}')
    
    # Test sample columns that were problematic before
    test_cols = ['Idlers_Brand_LHS1', 'LinkHeight_PercentWorn_LHS', 'LinkPitch_Brand_LHS', 'Sprocket_Brand_LHS']
    print(f'\n=== TESTING SPECIFIC COLUMNS ===')
    for col in test_cols:
        in_mapper = col in mapper_cols
        in_db = col in db_cols
        status = "✅ OK" if (in_mapper and in_db) else "❌ MISSING"
        print(f'  {col}: Mapper={in_mapper}, Database={in_db} {status}')
    
    # Test mapping functionality
    print(f'\n=== TESTING MAPPING FUNCTIONALITY ===')
    sample_excel_columns = ['Machine ID', 'Inspection Date', 'Link Pitch Brand LHS', 'Idlers Brand LHS1']
    
    # Create a mock DataFrame-like dict for testing
    mock_df_columns = sample_excel_columns
    mapped_columns = map_excel_to_database_columns(type('MockDF', (), {'columns': mock_df_columns})())
    
    print(f'Sample Excel columns: {sample_excel_columns}')
    print(f'Mapped columns: {mapped_columns}')
    
    print(f'\n=== SUMMARY ===')
    mapper_coverage = (len(set(mapper_cols) & set(db_cols)) / len(db_cols)) * 100
    print(f'Mapper coverage: {mapper_coverage:.1f}% ({len(set(mapper_cols) & set(db_cols))}/{len(db_cols)} columns)')
    
    if len(missing_in_mapper) == 0 and len(extra_in_mapper) == 0:
        print('✅ PERFECT MATCH: All columns synchronized!')
    elif len(missing_in_mapper) <= 5 and len(extra_in_mapper) <= 5:
        print('⚠️  MINOR ISSUES: Small discrepancies found')
    else:
        print('❌ MAJOR ISSUES: Significant discrepancies found')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()