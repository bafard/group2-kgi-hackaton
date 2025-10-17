#!/usr/bin/env python3

import sys
sys.path.append('backend')

from backend.app.utils.inspection_data_mapper import get_column_mapping_summary, get_all_inspection_data_columns

def test_inspection_mapper():
    print("📊 Testing Inspection Data Mapper")
    print("=" * 50)
    
    # Test mapping summary
    summary = get_column_mapping_summary()
    print(f"Total Database Columns: {summary['total_db_columns']}")
    print(f"Available Mappings: {summary['mapping_available']}")
    
    # Test with sample Excel columns
    sample_excel_columns = [
        'Machine_Type', 'Model_Code', 'Serial_No', 'SMR', 
        'LinkPitch_Brand_LHS', 'Bushings_PercentWorn_RHS',
        'TrackShoe_Type', 'Sprocket_History_SMR_LHS',
        'Idlers_Brand_LHS1', 'LinkHeight_PercentWorn_LHS'
    ]
    
    print(f"\nSample Excel Columns: {len(sample_excel_columns)}")
    
    # Test exact matching
    db_columns = get_all_inspection_data_columns()
    matched = [col for col in sample_excel_columns if col in db_columns]
    print(f"Exact Matches: {len(matched)}/{len(sample_excel_columns)}")
    
    for col in matched:
        print(f"  ✅ {col}")
    
    if len(matched) != len(sample_excel_columns):
        not_matched = [col for col in sample_excel_columns if col not in db_columns]
        print(f"\nNot Matched: {len(not_matched)}")
        for col in not_matched:
            print(f"  ❌ {col}")
    else:
        print("\n🎉 All sample columns match database schema perfectly!")
    
    print(f"\nFirst 10 database columns:")
    for i, col in enumerate(db_columns[:10]):
        print(f"  {i+1:2d}. {col}")
    
    if len(db_columns) > 10:
        print(f"  ... and {len(db_columns) - 10} more columns")

if __name__ == "__main__":
    test_inspection_mapper()