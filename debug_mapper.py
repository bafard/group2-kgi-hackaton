#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')

from app.utils.inspection_data_mapper import (
    get_all_inspection_data_columns, 
    INSPECTION_DATA_FIELD_MAPPING
)
from app.utils.sql_server_connection import sql_server

try:
    print("=== INSPECTION DATA MAPPER DEBUG ===")
    
    # Get actual database columns
    col_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData'
    ORDER BY ORDINAL_POSITION
    """
    db_result = sql_server.execute_query(col_query)
    db_cols = set([row[0] for row in db_result])
    
    # Get mapper columns
    mapper_cols = set(get_all_inspection_data_columns())
    
    print(f"Database has: {len(db_cols)} columns")
    print(f"Mapper has: {len(mapper_cols)} columns")
    
    # Check mapping targets
    mapping_targets = set(INSPECTION_DATA_FIELD_MAPPING.values())
    print(f"Mapping targets: {len(mapping_targets)} unique columns")
    
    # Find problematic mappings
    bad_mappings = mapping_targets - db_cols
    if bad_mappings:
        print(f"\n❌ BAD MAPPINGS (target columns not in database):")
        for col in sorted(bad_mappings):
            print(f"  {col}")
            # Find which Excel columns map to this bad target
            for excel_col, target_col in INSPECTION_DATA_FIELD_MAPPING.items():
                if target_col == col:
                    print(f"    ← '{excel_col}'")
    else:
        print("\n✅ All mapping targets exist in database")
    
    # Check if mapper columns match database
    missing_from_mapper = db_cols - mapper_cols
    extra_in_mapper = mapper_cols - db_cols
    
    if missing_from_mapper:
        print(f"\n⚠️  Columns in DB but missing from mapper ({len(missing_from_mapper)}):")
        for col in sorted(missing_from_mapper):
            print(f"  {col}")
    
    if extra_in_mapper:
        print(f"\n⚠️  Columns in mapper but not in DB ({len(extra_in_mapper)}):")
        for col in sorted(extra_in_mapper):
            print(f"  {col}")
    
    if not missing_from_mapper and not extra_in_mapper and not bad_mappings:
        print("\n🎉 EVERYTHING LOOKS GOOD!")
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()