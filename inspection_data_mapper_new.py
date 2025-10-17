"""
Mapping untuk field InspectionData table
Membantu mapping kolom Excel ke field database yang sesuai
Updated to match actual database schema (103 columns)
"""

def get_all_inspection_data_columns():
    """
    Returns list of all columns that exist in the InspectionData table.
    This matches the actual database schema exactly (103 columns).
    """
    return [
        'ID',
        'Inspection_ID',
        'Machine_Type',
        'Model_Code',
        'Serial_No',
        'Inspected_By',
        'Link_Type',
        'Link_Spec',
        'Bushing_Spec',
        'Track_Roller_Spec',
        'Equipment_Number',
        'SMR',
        'Delivery_Date',
        'Inspection_Date',
        'Branch_Name',
        'Customer_Name',
        'Job_Site',
        'Attachments',
        'Comments',
        'WorkingHourPerDay',
        'UnderfootConditions_Terrain',
        'UnderfootConditions_Abrasive',
        'UnderfootConditions_Moisture',
        'UnderfootConditions_Packing',
        'ApplicationCode_Major',
        'ApplicationCode_Minor',
        'Application_Ground',
        'Application_Working',
        'LinkPitch_Brand_LHS',
        'LinkPitch_Brand_RHS',
        'LinkPitch_History_SMR_LHS',
        'LinkPitch_History_SMR_RHS',
        'LinkPitch_History_Date_LHS',
        'LinkPitch_History_Date_RHS',
        'LinkPitch_History_Hours_LHS',
        'LinkPitch_History_Hours_RHS',
        'LinkPitch_PercentWorn_LHS',
        'LinkPitch_PercentWorn_RHS',
        'LinkPitch_ReplaceDate_LHS',
        'LinkPitch_ReplaceDate_RHS',
        'Bushings_Brand_LHS',
        'Bushings_Brand_RHS',
        'Bushings_History_SMR_LHS',
        'Bushings_History_SMR_RHS',
        'Bushings_History_Date_LHS',
        'Bushings_History_Date_RHS',
        'Bushings_History_Hours_LHS',
        'Bushings_History_Hours_RHS',
        'Bushings_PercentWorn_LHS',
        'Bushings_PercentWorn_RHS',
        'Bushings_ReplaceDate_LHS',
        'Bushings_ReplaceDate_RHS',
        'LinkHeight_Brand_LHS',
        'LinkHeight_Brand_RHS',
        'LinkHeight_History_SMR_LHS',
        'LinkHeight_History_SMR_RHS',
        'LinkHeight_History_Date_LHS',
        'LinkHeight_History_Date_RHS',
        'LinkHeight_History_Hours_LHS',
        'LinkHeight_History_Hours_RHS',
        'LinkHeight_PercentWorn_LHS',
        'LinkHeight_PercentWorn_RHS',
        'LinkHeight_ReplaceDate_LHS',
        'LinkHeight_ReplaceDate_RHS',
        'TrackShoe_Type',
        'TrackShoe_Width',
        'TrackShoe_Width_Type',
        'TrackShoe_Brand_LHS',
        'TrackShoe_Brand_RHS',
        'TrackShoe_History_SMR_LHS',
        'TrackShoe_History_SMR_RHS',
        'TrackShoe_History_Date_LHS',
        'TrackShoe_History_Date_RHS',
        'TrackShoe_History_Hours_LHS',
        'TrackShoe_History_Hours_RHS',
        'TrackShoe_PercentWorn_LHS',
        'TrackShoe_PercentWorn_RHS',
        'TrackShoe_ReplaceDate_LHS',
        'TrackShoe_ReplaceDate_RHS',
        'Idlers_Brand_LHS1',
        'Idlers_Brand_RHS1',
        'Idlers_History_SMR_LHS1',
        'Idlers_History_SMR_RHS1',
        'Idlers_History_Date_LHS1',
        'Idlers_History_Date_RHS1',
        'Idlers_History_Hours_LHS1',
        'Idlers_History_Hours_RHS1',
        'Idlers_PercentWorn_LHS1',
        'Idlers_PercentWorn_RHS1',
        'Idlers_ReplaceDate_LHS1',
        'Idlers_ReplaceDate_RHS1',
        'Sprocket_Brand_LHS',
        'Sprocket_Brand_RHS',
        'Sprocket_History_SMR_LHS',
        'Sprocket_History_SMR_RHS',
        'Sprocket_History_Date_LHS',
        'Sprocket_History_Date_RHS',
        'Sprocket_History_Hours_LHS',
        'Sprocket_History_Hours_RHS',
        'Sprocket_PercentWorn_RHS',
        'Sprocket_PercentWorn_LHS',
        'Sprocket_ReplaceDate_LHS',
        'Sprocket_ReplaceDate_RHS'
    ]

# Mapping kolom Excel ke field database InspectionData
# 1:1 mapping untuk kolom yang sama persis
INSPECTION_DATA_FIELD_MAPPING = {
    # Basic identification fields  
    'ID': 'ID',
    'Inspection ID': 'Inspection_ID',
    'Inspection_ID': 'Inspection_ID',
    'Machine Type': 'Machine_Type',
    'Machine_Type': 'Machine_Type',
    'Model Code': 'Model_Code',
    'Model_Code': 'Model_Code',
    'Serial No': 'Serial_No',
    'Serial_No': 'Serial_No',
    'Inspected By': 'Inspected_By',
    'Inspected_By': 'Inspected_By',
    'Link Type': 'Link_Type',
    'Link_Type': 'Link_Type',
    'Link Spec': 'Link_Spec',
    'Link_Spec': 'Link_Spec',
    'Bushing Spec': 'Bushing_Spec',
    'Bushing_Spec': 'Bushing_Spec',
    'Track Roller Spec': 'Track_Roller_Spec',
    'Track_Roller_Spec': 'Track_Roller_Spec',
    'Equipment Number': 'Equipment_Number',
    'Equipment_Number': 'Equipment_Number',
    'SMR': 'SMR',
    'Delivery Date': 'Delivery_Date',
    'Delivery_Date': 'Delivery_Date',
    'Branch Name': 'Branch_Name',
    'Branch_Name': 'Branch_Name',
    'Job Site': 'Job_Site',
    'Job_Site': 'Job_Site',
    'Working Hour Per Day': 'WorkingHourPerDay',
    'WorkingHourPerDay': 'WorkingHourPerDay',
    
    # Additional mappings for common Excel column names
    'Machine ID': 'Equipment_Number',  # Map Machine ID to Equipment Number
    'Inspection Date': 'Inspection_Date',
    'Inspection_Date': 'Inspection_Date',
    'Comments': 'Comments',
    'Attachments': 'Attachments',
    'Customer Name': 'Customer_Name',
    'Customer_Name': 'Customer_Name',
    
    # Working conditions
    'Underfoot Conditions Terrain': 'UnderfootConditions_Terrain',
    'UnderfootConditions_Terrain': 'UnderfootConditions_Terrain',
    'Underfoot Conditions Abrasive': 'UnderfootConditions_Abrasive',
    'UnderfootConditions_Abrasive': 'UnderfootConditions_Abrasive',
    'Underfoot Conditions Moisture': 'UnderfootConditions_Moisture',
    'UnderfootConditions_Moisture': 'UnderfootConditions_Moisture',
    'Underfoot Conditions Packing': 'UnderfootConditions_Packing',
    'UnderfootConditions_Packing': 'UnderfootConditions_Packing',
    'Application Code Major': 'ApplicationCode_Major',
    'ApplicationCode_Major': 'ApplicationCode_Major',
    'Application Code Minor': 'ApplicationCode_Minor',
    'ApplicationCode_Minor': 'ApplicationCode_Minor',
    'Application Ground': 'Application_Ground',
    'Application_Ground': 'Application_Ground',
    'Application Working': 'Application_Working',
    'Application_Working': 'Application_Working',
    'Inspection Date': 'Inspection_Date',
    'Inspection_Date': 'Inspection_Date',
    'Inspection Type': 'Inspection_Type',
    'Inspection_Type': 'Inspection_Type',
    'Inspector Name': 'Inspector_Name',
    'Inspector_Name': 'Inspector_Name',
    'Comments': 'Comments',
    'Attachments': 'Attachments',
    
    # LinkPitch fields
    'Link Pitch Brand LHS': 'LinkPitch_Brand_LHS',
    'LinkPitch_Brand_LHS': 'LinkPitch_Brand_LHS',
    'Link Pitch Brand RHS': 'LinkPitch_Brand_RHS',
    'LinkPitch_Brand_RHS': 'LinkPitch_Brand_RHS',
    'Link Pitch History SMR LHS': 'LinkPitch_History_SMR_LHS',
    'LinkPitch_History_SMR_LHS': 'LinkPitch_History_SMR_LHS',
    'Link Pitch History SMR RHS': 'LinkPitch_History_SMR_RHS',
    'LinkPitch_History_SMR_RHS': 'LinkPitch_History_SMR_RHS',
    'Link Pitch History Date LHS': 'LinkPitch_History_Date_LHS',
    'LinkPitch_History_Date_LHS': 'LinkPitch_History_Date_LHS',
    'Link Pitch History Date RHS': 'LinkPitch_History_Date_RHS',
    'LinkPitch_History_Date_RHS': 'LinkPitch_History_Date_RHS',
    'Link Pitch History Hours LHS': 'LinkPitch_History_Hours_LHS',
    'LinkPitch_History_Hours_LHS': 'LinkPitch_History_Hours_LHS',
    'Link Pitch History Hours RHS': 'LinkPitch_History_Hours_RHS',
    'LinkPitch_History_Hours_RHS': 'LinkPitch_History_Hours_RHS',
    'Link Pitch Percent Worn LHS': 'LinkPitch_PercentWorn_LHS',
    'LinkPitch_PercentWorn_LHS': 'LinkPitch_PercentWorn_LHS',
    'Link Pitch Percent Worn RHS': 'LinkPitch_PercentWorn_RHS',
    'LinkPitch_PercentWorn_RHS': 'LinkPitch_PercentWorn_RHS',
    'Link Pitch Replace Date LHS': 'LinkPitch_ReplaceDate_LHS',
    'LinkPitch_ReplaceDate_LHS': 'LinkPitch_ReplaceDate_LHS',
    'Link Pitch Replace Date RHS': 'LinkPitch_ReplaceDate_RHS',
    'LinkPitch_ReplaceDate_RHS': 'LinkPitch_ReplaceDate_RHS',
    
    # Bushings fields
    'Bushings Brand LHS': 'Bushings_Brand_LHS',
    'Bushings_Brand_LHS': 'Bushings_Brand_LHS',
    'Bushings Brand RHS': 'Bushings_Brand_RHS',
    'Bushings_Brand_RHS': 'Bushings_Brand_RHS',
    'Bushings History SMR LHS': 'Bushings_History_SMR_LHS',
    'Bushings_History_SMR_LHS': 'Bushings_History_SMR_LHS',
    'Bushings History SMR RHS': 'Bushings_History_SMR_RHS',
    'Bushings_History_SMR_RHS': 'Bushings_History_SMR_RHS',
    'Bushings History Date LHS': 'Bushings_History_Date_LHS',
    'Bushings_History_Date_LHS': 'Bushings_History_Date_LHS',
    'Bushings History Date RHS': 'Bushings_History_Date_RHS',
    'Bushings_History_Date_RHS': 'Bushings_History_Date_RHS',
    'Bushings History Hours LHS': 'Bushings_History_Hours_LHS',
    'Bushings_History_Hours_LHS': 'Bushings_History_Hours_LHS',
    'Bushings History Hours RHS': 'Bushings_History_Hours_RHS',
    'Bushings_History_Hours_RHS': 'Bushings_History_Hours_RHS',
    'Bushings Percent Worn LHS': 'Bushings_PercentWorn_LHS',
    'Bushings_PercentWorn_LHS': 'Bushings_PercentWorn_LHS',
    'Bushings Percent Worn RHS': 'Bushings_PercentWorn_RHS',
    'Bushings_PercentWorn_RHS': 'Bushings_PercentWorn_RHS',
    'Bushings Replace Date LHS': 'Bushings_ReplaceDate_LHS',
    'Bushings_ReplaceDate_LHS': 'Bushings_ReplaceDate_LHS',
    'Bushings Replace Date RHS': 'Bushings_ReplaceDate_RHS',
    'Bushings_ReplaceDate_RHS': 'Bushings_ReplaceDate_RHS',
    
    # LinkHeight fields
    'Link Height Brand LHS': 'LinkHeight_Brand_LHS',
    'LinkHeight_Brand_LHS': 'LinkHeight_Brand_LHS',
    'Link Height Brand RHS': 'LinkHeight_Brand_RHS',
    'LinkHeight_Brand_RHS': 'LinkHeight_Brand_RHS',
    'Link Height History SMR LHS': 'LinkHeight_History_SMR_LHS',
    'LinkHeight_History_SMR_LHS': 'LinkHeight_History_SMR_LHS',
    'Link Height History SMR RHS': 'LinkHeight_History_SMR_RHS',
    'LinkHeight_History_SMR_RHS': 'LinkHeight_History_SMR_RHS',
    'Link Height History Date LHS': 'LinkHeight_History_Date_LHS',
    'LinkHeight_History_Date_LHS': 'LinkHeight_History_Date_LHS',
    'Link Height History Date RHS': 'LinkHeight_History_Date_RHS',
    'LinkHeight_History_Date_RHS': 'LinkHeight_History_Date_RHS',
    'Link Height History Hours LHS': 'LinkHeight_History_Hours_LHS',
    'LinkHeight_History_Hours_LHS': 'LinkHeight_History_Hours_LHS',
    'Link Height History Hours RHS': 'LinkHeight_History_Hours_RHS',
    'LinkHeight_History_Hours_RHS': 'LinkHeight_History_Hours_RHS',
    'Link Height Percent Worn LHS': 'LinkHeight_PercentWorn_LHS',
    'LinkHeight_PercentWorn_LHS': 'LinkHeight_PercentWorn_LHS',
    'Link Height Percent Worn RHS': 'LinkHeight_PercentWorn_RHS',
    'LinkHeight_PercentWorn_RHS': 'LinkHeight_PercentWorn_RHS',
    'Link Height Replace Date LHS': 'LinkHeight_ReplaceDate_LHS',
    'LinkHeight_ReplaceDate_LHS': 'LinkHeight_ReplaceDate_LHS',
    'Link Height Replace Date RHS': 'LinkHeight_ReplaceDate_RHS',
    'LinkHeight_ReplaceDate_RHS': 'LinkHeight_ReplaceDate_RHS',
    
    # TrackShoe fields
    'Track Shoe Type': 'TrackShoe_Type',
    'TrackShoe_Type': 'TrackShoe_Type',
    'Track Shoe Width': 'TrackShoe_Width',
    'TrackShoe_Width': 'TrackShoe_Width',
    'Track Shoe Width Type': 'TrackShoe_Width_Type',
    'TrackShoe_Width_Type': 'TrackShoe_Width_Type',
    'Track Shoe Brand LHS': 'TrackShoe_Brand_LHS',
    'TrackShoe_Brand_LHS': 'TrackShoe_Brand_LHS',
    'Track Shoe Brand RHS': 'TrackShoe_Brand_RHS',
    'TrackShoe_Brand_RHS': 'TrackShoe_Brand_RHS',
    'Track Shoe History SMR LHS': 'TrackShoe_History_SMR_LHS',
    'TrackShoe_History_SMR_LHS': 'TrackShoe_History_SMR_LHS',
    'Track Shoe History SMR RHS': 'TrackShoe_History_SMR_RHS',
    'TrackShoe_History_SMR_RHS': 'TrackShoe_History_SMR_RHS',
    'Track Shoe History Date LHS': 'TrackShoe_History_Date_LHS',
    'TrackShoe_History_Date_LHS': 'TrackShoe_History_Date_LHS',
    'Track Shoe History Date RHS': 'TrackShoe_History_Date_RHS',
    'TrackShoe_History_Date_RHS': 'TrackShoe_History_Date_RHS',
    'Track Shoe History Hours LHS': 'TrackShoe_History_Hours_LHS',
    'TrackShoe_History_Hours_LHS': 'TrackShoe_History_Hours_LHS',
    'Track Shoe History Hours RHS': 'TrackShoe_History_Hours_RHS',
    'TrackShoe_History_Hours_RHS': 'TrackShoe_History_Hours_RHS',
    'Track Shoe Percent Worn LHS': 'TrackShoe_PercentWorn_LHS',
    'TrackShoe_PercentWorn_LHS': 'TrackShoe_PercentWorn_LHS',
    'Track Shoe Percent Worn RHS': 'TrackShoe_PercentWorn_RHS',
    'TrackShoe_PercentWorn_RHS': 'TrackShoe_PercentWorn_RHS',
    'Track Shoe Replace Date LHS': 'TrackShoe_ReplaceDate_LHS',
    'TrackShoe_ReplaceDate_LHS': 'TrackShoe_ReplaceDate_LHS',
    'Track Shoe Replace Date RHS': 'TrackShoe_ReplaceDate_RHS',
    'TrackShoe_ReplaceDate_RHS': 'TrackShoe_ReplaceDate_RHS',
    
    # Idlers fields
    'Idlers Brand LHS1': 'Idlers_Brand_LHS1',
    'Idlers_Brand_LHS1': 'Idlers_Brand_LHS1',
    'Idlers Brand RHS1': 'Idlers_Brand_RHS1',
    'Idlers_Brand_RHS1': 'Idlers_Brand_RHS1',
    'Idlers History SMR LHS1': 'Idlers_History_SMR_LHS1',
    'Idlers_History_SMR_LHS1': 'Idlers_History_SMR_LHS1',
    'Idlers History SMR RHS1': 'Idlers_History_SMR_RHS1',
    'Idlers_History_SMR_RHS1': 'Idlers_History_SMR_RHS1',
    'Idlers History Date LHS1': 'Idlers_History_Date_LHS1',
    'Idlers_History_Date_LHS1': 'Idlers_History_Date_LHS1',
    'Idlers History Date RHS1': 'Idlers_History_Date_RHS1',
    'Idlers_History_Date_RHS1': 'Idlers_History_Date_RHS1',
    'Idlers History Hours LHS1': 'Idlers_History_Hours_LHS1',
    'Idlers_History_Hours_LHS1': 'Idlers_History_Hours_LHS1',
    'Idlers History Hours RHS1': 'Idlers_History_Hours_RHS1',
    'Idlers_History_Hours_RHS1': 'Idlers_History_Hours_RHS1',
    'Idlers Percent Worn LHS1': 'Idlers_PercentWorn_LHS1',
    'Idlers_PercentWorn_LHS1': 'Idlers_PercentWorn_LHS1',
    'Idlers Percent Worn RHS1': 'Idlers_PercentWorn_RHS1',
    'Idlers_PercentWorn_RHS1': 'Idlers_PercentWorn_RHS1',
    'Idlers Replace Date LHS1': 'Idlers_ReplaceDate_LHS1',
    'Idlers_ReplaceDate_LHS1': 'Idlers_ReplaceDate_LHS1',
    'Idlers Replace Date RHS1': 'Idlers_ReplaceDate_RHS1',
    'Idlers_ReplaceDate_RHS1': 'Idlers_ReplaceDate_RHS1',
    'Idlers Measurement LHS1': 'Idlers_Measurement_LHS1',
    'Idlers_Measurement_LHS1': 'Idlers_Measurement_LHS1',
    'Idlers Measurement RHS1': 'Idlers_Measurement_RHS1',
    'Idlers_Measurement_RHS1': 'Idlers_Measurement_RHS1',
    'Idlers Potential Hours LHS1': 'Idlers_PotentialHours_LHS1',
    'Idlers_PotentialHours_LHS1': 'Idlers_PotentialHours_LHS1',
    'Idlers Potential Hours RHS1': 'Idlers_PotentialHours_RHS1',
    'Idlers_PotentialHours_RHS1': 'Idlers_PotentialHours_RHS1',
    
    # Sprocket fields
    'Sprocket Brand LHS': 'Sprocket_Brand_LHS',
    'Sprocket_Brand_LHS': 'Sprocket_Brand_LHS',
    'Sprocket Brand RHS': 'Sprocket_Brand_RHS',
    'Sprocket_Brand_RHS': 'Sprocket_Brand_RHS',
    'Sprocket History SMR LHS': 'Sprocket_History_SMR_LHS',
    'Sprocket_History_SMR_LHS': 'Sprocket_History_SMR_LHS',
    'Sprocket History SMR RHS': 'Sprocket_History_SMR_RHS',
    'Sprocket_History_SMR_RHS': 'Sprocket_History_SMR_RHS',
    'Sprocket History Date LHS': 'Sprocket_History_Date_LHS',
    'Sprocket_History_Date_LHS': 'Sprocket_History_Date_LHS',
    'Sprocket History Date RHS': 'Sprocket_History_Date_RHS',
    'Sprocket_History_Date_RHS': 'Sprocket_History_Date_RHS',
    'Sprocket History Hours LHS': 'Sprocket_History_Hours_LHS',
    'Sprocket_History_Hours_LHS': 'Sprocket_History_Hours_LHS',
    'Sprocket History Hours RHS': 'Sprocket_History_Hours_RHS',
    'Sprocket_History_Hours_RHS': 'Sprocket_History_Hours_RHS',
    'Sprocket Percent Worn LHS': 'Sprocket_PercentWorn_LHS',
    'Sprocket_PercentWorn_LHS': 'Sprocket_PercentWorn_LHS',
    'Sprocket Percent Worn RHS': 'Sprocket_PercentWorn_RHS',
    'Sprocket_PercentWorn_RHS': 'Sprocket_PercentWorn_RHS',
    'Sprocket Replace Date LHS': 'Sprocket_ReplaceDate_LHS',
    'Sprocket_ReplaceDate_LHS': 'Sprocket_ReplaceDate_LHS',
    'Sprocket Replace Date RHS': 'Sprocket_ReplaceDate_RHS',
    'Sprocket_ReplaceDate_RHS': 'Sprocket_ReplaceDate_RHS',
    'Sprocket Measurement LHS': 'Sprocket_Measurement_LHS',
    'Sprocket_Measurement_LHS': 'Sprocket_Measurement_LHS',
    'Sprocket Measurement RHS': 'Sprocket_Measurement_RHS',
    'Sprocket_Measurement_RHS': 'Sprocket_Measurement_RHS',
    'Sprocket Potential Hours LHS': 'Sprocket_PotentialHours_LHS',
    'Sprocket_PotentialHours_LHS': 'Sprocket_PotentialHours_LHS',
    'Sprocket Potential Hours RHS': 'Sprocket_PotentialHours_RHS',
    'Sprocket_PotentialHours_RHS': 'Sprocket_PotentialHours_RHS',
    
    # Machine specifications
    'Machine Hours': 'Machine_Hours',
    'Machine_Hours': 'Machine_Hours',
    'Machine SMR': 'Machine_SMR',
    'Machine_SMR': 'Machine_SMR',
    'Machine Model': 'Machine_Model',
    'Machine_Model': 'Machine_Model',
    'Machine Serial': 'Machine_Serial',
    'Machine_Serial': 'Machine_Serial',
    'Machine Application': 'Machine_Application',
    'Machine_Application': 'Machine_Application',
    'Machine Location': 'Machine_Location',
    'Machine_Location': 'Machine_Location',
    'Notes to Customer': 'Notes_to_Customer',
    'Notes_to_Customer': 'Notes_to_Customer',
    'Recommendations': 'Recommendations',
    
    # Customer information
    'Customer Name': 'Customer_Name',
    'Customer_Name': 'Customer_Name',
    'Company Name': 'Company_Name',
    'Company_Name': 'Company_Name'
}


def filter_excel_columns_for_database(df):
    """
    Filter dataframe to only include columns that can be mapped to database.
    Returns a new dataframe with only mappable columns.
    """
    mappable_columns = [col for col in df.columns if col in INSPECTION_DATA_FIELD_MAPPING.keys()]
    
    if not mappable_columns:
        print("❌ No mappable columns found in Excel file")
        return df
    
    print(f"📋 Found {len(mappable_columns)} mappable columns out of {len(df.columns)} total columns")
    for col in mappable_columns:
        print(f"  ✅ {col} -> {INSPECTION_DATA_FIELD_MAPPING[col]}")
    
    skipped_columns = [col for col in df.columns if col not in INSPECTION_DATA_FIELD_MAPPING.keys()]
    if skipped_columns:
        print(f"⚠️  Skipping {len(skipped_columns)} non-mappable columns:")
        for col in skipped_columns[:10]:  # Show first 10
            print(f"  ❌ {col}")
        if len(skipped_columns) > 10:
            print(f"  ... and {len(skipped_columns) - 10} more")
    
    return df[mappable_columns]


def map_excel_to_database_columns(df):
    """
    Map Excel column names to database field names using INSPECTION_DATA_FIELD_MAPPING.
    Returns dictionary mapping for pandas rename() function.
    """
    column_mapping = {}
    
    for excel_col in df.columns:
        if excel_col in INSPECTION_DATA_FIELD_MAPPING:
            db_col = INSPECTION_DATA_FIELD_MAPPING[excel_col]
            column_mapping[excel_col] = db_col
            print(f"✅ Mapping: '{excel_col}' -> '{db_col}'")
        else:
            print(f"⚠️  Skipping column '{excel_col}' - not found in database")
    
    print(f"\n📊 Total mapped columns: {len(column_mapping)}")
    return column_mapping


def validate_mapped_columns(mapped_df):
    """
    Validate that mapped DataFrame columns exist in database schema.
    """
    all_db_columns = get_all_inspection_data_columns()
    valid_columns = []
    invalid_columns = []
    
    for col in mapped_df.columns:
        if col in all_db_columns:
            valid_columns.append(col)
        else:
            invalid_columns.append(col)
    
    print(f"📋 Validation Results:")
    print(f"  ✅ Valid columns: {len(valid_columns)}")
    print(f"  ❌ Invalid columns: {len(invalid_columns)}")
    
    if invalid_columns:
        print("Invalid columns found:")
        for col in invalid_columns:
            print(f"  - {col}")
    
    return len(invalid_columns) == 0


# Test function untuk memverifikasi mapping
def test_mapping():
    """Test mapping functionality"""
    print("=== TESTING INSPECTION DATA MAPPER ===")
    
    all_columns = get_all_inspection_data_columns()
    print(f"Total database columns: {len(all_columns)}")
    
    # Test sample mappings
    test_columns = [
        'Machine ID', 'Inspection Date', 'Idlers Brand LHS1', 
        'LinkHeight_PercentWorn_LHS', 'Sprocket Brand LHS'
    ]
    
    print(f"\nTesting {len(test_columns)} sample columns:")
    for col in test_columns:
        if col in INSPECTION_DATA_FIELD_MAPPING:
            mapped = INSPECTION_DATA_FIELD_MAPPING[col]
            exists_in_db = mapped in all_columns
            status = "✅" if exists_in_db else "❌"
            print(f"  {status} '{col}' -> '{mapped}' (in DB: {exists_in_db})")
        else:
            print(f"  ❌ '{col}' - no mapping found")


if __name__ == "__main__":
    test_mapping()