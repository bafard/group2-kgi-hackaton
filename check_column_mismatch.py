#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')

from app.utils.sql_server_connection import sql_server

try:
    # Get actual database columns
    col_query = """
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = 'InspectionData'
    ORDER BY ORDINAL_POSITION
    """
    db_result = sql_server.execute_query(col_query)
    db_cols = set([row[0] for row in db_result])

    # Error columns from the SQL query in the error message
    error_cols = [
        'Inspection_ID', 'Distributor_Code', 'Machine_Type', 'Model_Code', 'Serial_No', 
        'Inspected_By', 'Link_Type', 'Link_Spec', 'Bushing_Spec', 'Track_Roller_Spec', 
        'Carrier_Roller_Spec', 'Idler_Spec', 'Sprocket_Spec', 'Shoe_Spec', 'Impact', 
        'Shoe_Type', 'Criteria_Origin', 'Equipment_Number', 'SMR', 'Delivery_Date', 
        'Inspection_Date', 'User_ID', 'User_Name', 'Branch_Name', 'Customer_Name', 
        'Customer_Address', 'Job_Site', 'Attachments', 'Comments', 'Active_Inspection', 
        'Inspection_Origin', 'Create_ID', 'Created_Date', 'Last_Update_ID', 'Last_Updated_Date', 
        'Manufacturer', 'LinkPitchConstant', 'WorkingHourPerDay', 'Picture_Count',
        'UnderfootConditions_Terrain', 'UnderfootConditions_Abrasive', 'UnderfootConditions_Moisture', 
        'UnderfootConditions_Packing', 'ApplicationCode_Major', 'ApplicationCode_Minor', 
        'Application_Ground', 'Application_Working', 'HotPin_Diagnosis_LHS', 'HotPin_Diagnosis_RHS', 
        'HotPin_Comments_LHS', 'HotPin_Comments_RHS', 'LinkPitch_Loose', 'LinkPitch_Welded', 
        'LinkPitch_Brand_LHS', 'LinkPitch_Brand_RHS', 'LinkPitch_History_LHS', 'LinkPitch_History_RHS', 
        'LinkPitch_History_SMR_LHS', 'LinkPitch_History_SMR_RHS', 'LinkPitch_Measurement_LHS', 
        'LinkPitch_Measurement_RHS', 'LinkPitch_PercentWorn_LHS', 'LinkPitch_PercentWorn_RHS', 
        'LinkPitch_PotentialHours_LHS', 'LinkPitch_PotentialHours_RHS', 'LinkPitch_PotentialDays_LHS', 
        'LinkPitch_PotentialDays_RHS', 'LinkPitch_ReplaceDate_LHS', 'LinkPitch_ReplaceDate_RHS', 
        'LinkPitch_100Life_LHS', 'LinkPitch_100Life_RHS'
    ]

    print('=== COLUMN MISMATCH ANALYSIS ===')
    print(f'Error SQL has {len(error_cols)} columns')
    print(f'Database has {len(db_cols)} columns')
    
    missing_cols = []
    print('\nColumns in error SQL but NOT in actual database:')
    for col in error_cols:
        if col not in db_cols:
            missing_cols.append(col)
            print(f'  ❌ {col}')
    
    print(f'\nTotal missing columns: {len(missing_cols)}')
    
    if len(missing_cols) > 0:
        print('\nThis is why the SQL INSERT fails!')
        print('The application is trying to insert into columns that dont exist.')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()