"""
Mapping untuk field InspectionData table
Membantu mapping kolom Excel ke field database yang sesuai
Updated to match actual database schema (103 columns) - NO DUPLICATES
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
        'Sprocket_PercentWorn_LHS',
        'Sprocket_PercentWorn_RHS',
        'Sprocket_ReplaceDate_LHS',
        'Sprocket_ReplaceDate_RHS'
    ]

# Mapping kolom Excel ke field database InspectionData
# CLEANED: No duplicates to prevent SQL parameter issues
INSPECTION_DATA_FIELD_MAPPING = {
    # Basic identification fields  
    'ID': 'ID',
    'Inspection ID': 'Inspection_ID',
    'Machine Type': 'Machine_Type',
    'Model Code': 'Model_Code',
    'Serial No': 'Serial_No',
    'Inspected By': 'Inspected_By',
    'Link Type': 'Link_Type',
    'Link Spec': 'Link_Spec',
    'Bushing Spec': 'Bushing_Spec',
    'Track Roller Spec': 'Track_Roller_Spec',
    'Equipment Number': 'Equipment_Number',
    'SMR': 'SMR',
    'Delivery Date': 'Delivery_Date',
    'Branch Name': 'Branch_Name',
    'Job Site': 'Job_Site',
    'Working Hour Per Day': 'WorkingHourPerDay',
    
    # Additional mappings for common Excel column names
    'Machine ID': 'Equipment_Number',  # Alternative name for Equipment Number
    'Inspection Date': 'Inspection_Date',
    'Comments': 'Comments',
    'Attachments': 'Attachments',
    'Customer Name': 'Customer_Name',
    
    # Working conditions
    'Underfoot Conditions Terrain': 'UnderfootConditions_Terrain',
    'Underfoot Conditions Abrasive': 'UnderfootConditions_Abrasive',
    'Underfoot Conditions Moisture': 'UnderfootConditions_Moisture',
    'Underfoot Conditions Packing': 'UnderfootConditions_Packing',
    
    # Application codes
    'Application Code Major': 'ApplicationCode_Major',
    'Application Code Minor': 'ApplicationCode_Minor',
    'Application Ground': 'Application_Ground',
    'Application Working': 'Application_Working',
    
    # Link Pitch fields - LHS (Left Hand Side)
    'Link Pitch Brand LHS': 'LinkPitch_Brand_LHS',
    'Link Pitch History SMR LHS': 'LinkPitch_History_SMR_LHS',
    'Link Pitch History Date LHS': 'LinkPitch_History_Date_LHS',
    'Link Pitch History Hours LHS': 'LinkPitch_History_Hours_LHS',
    'Link Pitch Percent Worn LHS': 'LinkPitch_PercentWorn_LHS',
    'Link Pitch Replace Date LHS': 'LinkPitch_ReplaceDate_LHS',
    
    # Link Pitch fields - RHS (Right Hand Side)
    'Link Pitch Brand RHS': 'LinkPitch_Brand_RHS',
    'Link Pitch History SMR RHS': 'LinkPitch_History_SMR_RHS',
    'Link Pitch History Date RHS': 'LinkPitch_History_Date_RHS',
    'Link Pitch History Hours RHS': 'LinkPitch_History_Hours_RHS',
    'Link Pitch Percent Worn RHS': 'LinkPitch_PercentWorn_RHS',
    'Link Pitch Replace Date RHS': 'LinkPitch_ReplaceDate_RHS',
    
    # Bushings fields - LHS
    'Bushings Brand LHS': 'Bushings_Brand_LHS',
    'Bushings History SMR LHS': 'Bushings_History_SMR_LHS',
    'Bushings History Date LHS': 'Bushings_History_Date_LHS',
    'Bushings History Hours LHS': 'Bushings_History_Hours_LHS',
    'Bushings Percent Worn LHS': 'Bushings_PercentWorn_LHS',
    'Bushings Replace Date LHS': 'Bushings_ReplaceDate_LHS',
    
    # Bushings fields - RHS
    'Bushings Brand RHS': 'Bushings_Brand_RHS',
    'Bushings History SMR RHS': 'Bushings_History_SMR_RHS',
    'Bushings History Date RHS': 'Bushings_History_Date_RHS',
    'Bushings History Hours RHS': 'Bushings_History_Hours_RHS',
    'Bushings Percent Worn RHS': 'Bushings_PercentWorn_RHS',
    'Bushings Replace Date RHS': 'Bushings_ReplaceDate_RHS',
    
    # Link Height fields - LHS
    'Link Height Brand LHS': 'LinkHeight_Brand_LHS',
    'Link Height History SMR LHS': 'LinkHeight_History_SMR_LHS',
    'Link Height History Date LHS': 'LinkHeight_History_Date_LHS',
    'Link Height History Hours LHS': 'LinkHeight_History_Hours_LHS',
    'Link Height Percent Worn LHS': 'LinkHeight_PercentWorn_LHS',
    'Link Height Replace Date LHS': 'LinkHeight_ReplaceDate_LHS',
    
    # Link Height fields - RHS
    'Link Height Brand RHS': 'LinkHeight_Brand_RHS',
    'Link Height History SMR RHS': 'LinkHeight_History_SMR_RHS',
    'Link Height History Date RHS': 'LinkHeight_History_Date_RHS',
    'Link Height History Hours RHS': 'LinkHeight_History_Hours_RHS',
    'Link Height Percent Worn RHS': 'LinkHeight_PercentWorn_RHS',
    'Link Height Replace Date RHS': 'LinkHeight_ReplaceDate_RHS',
    
    # Track Shoe fields
    'Track Shoe Type': 'TrackShoe_Type',
    'Track Shoe Width': 'TrackShoe_Width',
    'Track Shoe Width Type': 'TrackShoe_Width_Type',
    'Track Shoe Brand LHS': 'TrackShoe_Brand_LHS',
    'Track Shoe Brand RHS': 'TrackShoe_Brand_RHS',
    'Track Shoe History SMR LHS': 'TrackShoe_History_SMR_LHS',
    'Track Shoe History SMR RHS': 'TrackShoe_History_SMR_RHS',
    'Track Shoe History Date LHS': 'TrackShoe_History_Date_LHS',
    'Track Shoe History Date RHS': 'TrackShoe_History_Date_RHS',
    'Track Shoe History Hours LHS': 'TrackShoe_History_Hours_LHS',
    'Track Shoe History Hours RHS': 'TrackShoe_History_Hours_RHS',
    'Track Shoe Percent Worn LHS': 'TrackShoe_PercentWorn_LHS',
    'Track Shoe Percent Worn RHS': 'TrackShoe_PercentWorn_RHS',
    'Track Shoe Replace Date LHS': 'TrackShoe_ReplaceDate_LHS',
    'Track Shoe Replace Date RHS': 'TrackShoe_ReplaceDate_RHS',
    
    # Idlers fields - LHS1/RHS1
    'Idlers Brand LHS1': 'Idlers_Brand_LHS1',
    'Idlers Brand RHS1': 'Idlers_Brand_RHS1',
    'Idlers History SMR LHS1': 'Idlers_History_SMR_LHS1',
    'Idlers History SMR RHS1': 'Idlers_History_SMR_RHS1',
    'Idlers History Date LHS1': 'Idlers_History_Date_LHS1',
    'Idlers History Date RHS1': 'Idlers_History_Date_RHS1',
    'Idlers History Hours LHS1': 'Idlers_History_Hours_LHS1',
    'Idlers History Hours RHS1': 'Idlers_History_Hours_RHS1',
    'Idlers Percent Worn LHS1': 'Idlers_PercentWorn_LHS1',
    'Idlers Percent Worn RHS1': 'Idlers_PercentWorn_RHS1',
    'Idlers Replace Date LHS1': 'Idlers_ReplaceDate_LHS1',
    'Idlers Replace Date RHS1': 'Idlers_ReplaceDate_RHS1',
    
    # Sprocket fields
    'Sprocket Brand LHS': 'Sprocket_Brand_LHS',
    'Sprocket Brand RHS': 'Sprocket_Brand_RHS',
    'Sprocket History SMR LHS': 'Sprocket_History_SMR_LHS',
    'Sprocket History SMR RHS': 'Sprocket_History_SMR_RHS',
    'Sprocket History Date LHS': 'Sprocket_History_Date_LHS',
    'Sprocket History Date RHS': 'Sprocket_History_Date_RHS',
    'Sprocket History Hours LHS': 'Sprocket_History_Hours_LHS',
    'Sprocket History Hours RHS': 'Sprocket_History_Hours_RHS',
    'Sprocket Percent Worn LHS': 'Sprocket_PercentWorn_LHS',
    'Sprocket Percent Worn RHS': 'Sprocket_PercentWorn_RHS',
    'Sprocket Replace Date LHS': 'Sprocket_ReplaceDate_LHS',
    'Sprocket Replace Date RHS': 'Sprocket_ReplaceDate_RHS',
}


def get_mapped_columns(excel_columns):
    """
    Maps Excel column names to database field names using INSPECTION_DATA_FIELD_MAPPING.
    Only returns columns that have a mapping.
    
    Args:
        excel_columns: List of column names from Excel file
        
    Returns:
        dict: {excel_column: database_field} for mapped columns only
    """
    mapped = {}
    for excel_col in excel_columns:
        if excel_col in INSPECTION_DATA_FIELD_MAPPING:
            db_field = INSPECTION_DATA_FIELD_MAPPING[excel_col]
            mapped[excel_col] = db_field
    return mapped


def get_missing_columns(excel_columns, required_columns=None):
    """
    Returns list of columns that are in required_columns but not in excel_columns.
    If required_columns is None, uses all database columns.
    
    Args:
        excel_columns: List of column names from Excel file
        required_columns: List of required database columns (optional)
        
    Returns:
        list: Missing column names
    """
    if required_columns is None:
        required_columns = get_all_inspection_data_columns()
    
    # Get mapped database fields from Excel columns
    mapped_db_fields = set()
    for excel_col in excel_columns:
        if excel_col in INSPECTION_DATA_FIELD_MAPPING:
            mapped_db_fields.add(INSPECTION_DATA_FIELD_MAPPING[excel_col])
    
    # Find missing required columns
    missing = []
    for req_col in required_columns:
        if req_col not in mapped_db_fields:
            missing.append(req_col)
    
    return missing


def is_inspection_data_complete(excel_columns):
    """
    Checks if Excel file has all required columns for InspectionData table.
    
    Args:
        excel_columns: List of column names from Excel file
        
    Returns:
        tuple: (is_complete: bool, missing_columns: list)
    """
    missing = get_missing_columns(excel_columns)
    return len(missing) == 0, missing


def get_column_mapping_summary(excel_columns):
    """
    Returns summary of column mapping for debugging purposes.
    
    Args:
        excel_columns: List of column names from Excel file
        
    Returns:
        dict: Summary with mapped, unmapped, and missing columns
    """
    mapped = get_mapped_columns(excel_columns)
    unmapped = [col for col in excel_columns if col not in INSPECTION_DATA_FIELD_MAPPING]
    missing = get_missing_columns(excel_columns)
    
    return {
        'total_excel_columns': len(excel_columns),
        'mapped_columns': len(mapped),
        'unmapped_columns': len(unmapped),
        'missing_db_columns': len(missing),
        'mapped_details': mapped,
        'unmapped_details': unmapped,
        'missing_details': missing
    }