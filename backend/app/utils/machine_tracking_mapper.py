"""
Mapping untuk field Machine_Tracking table
Membantu mapping kolom Excel ke field database Machine_Tracking untuk KOMTRAX system
"""

# Mapping kolom Excel yang umum ke field database Machine_Tracking
MACHINE_TRACKING_FIELD_MAPPING = {
    # Basic Information
    'model': 'Model',
    'type': 'Type',
    
    # Serial Number variations
    'serial': 'Serial',
    'serial_number': 'Serial',
    'serial number': 'Serial',
    'serialnumber': 'Serial',
    'sn': 'Serial',
    's/n': 'Serial',
    
    # Delivery Date variations
    'delivery_date_eqp_care': 'Delivery_Date_EQP_Care',
    'delivery date eqp care': 'Delivery_Date_EQP_Care',
    'delivery_date': 'Delivery_Date_EQP_Care',
    'delivery date': 'Delivery_Date_EQP_Care',
    'deliverydateeqpcare': 'Delivery_Date_EQP_Care',
    
    # Machine Location variations
    'machine_location': 'Machine_Location',
    'machine location': 'Machine_Location',
    'machinelocation': 'Machine_Location',
    'location': 'Machine_Location',
    
    # GPS coordinates variations
    'latitude': 'Latitude',
    'lat': 'Latitude',
    'longitude': 'Longitude',
    'long': 'Longitude',
    'lng': 'Longitude',
    
    # GPS Time variations
    'gps_time': 'GPS_Time',
    'gps time': 'GPS_Time',
    'gpstime': 'GPS_Time',
    'gps timestamp': 'GPS_Time',
    'gps_timestamp': 'GPS_Time',
    
    # SMR Hours variations
    'smr_hours': 'SMR_Hours',
    'smr hours': 'SMR_Hours',
    'smrhours': 'SMR_Hours',
    'smr': 'SMR_Hours',
    'hours': 'SMR_Hours',
    
    # Last Communication Date variations
    'last_communication_date': 'Last_Communication_Date',
    'last communication date': 'Last_Communication_Date',
    'lastcommunicationdate': 'Last_Communication_Date',
    'last_communication': 'Last_Communication_Date',
    'last communication': 'Last_Communication_Date',
    'communication_date': 'Last_Communication_Date',
    'communication date': 'Last_Communication_Date',
}

def get_all_machine_tracking_columns():
    """Return all actual column names from Machine_Tracking table (excluding ID as it's auto-increment)"""
    columns = [
        'Model',
        'Type',
        'Serial',
        'Delivery_Date_EQP_Care',
        'Machine_Location',
        'Latitude',
        'Longitude',
        'GPS_Time',
        'SMR_Hours',
        'Last_Communication_Date'
    ]
    return columns

def filter_excel_columns_for_machine_tracking(excel_df):
    """Filter Excel DataFrame to only include columns that exist in Machine_Tracking table"""
    db_columns = get_all_machine_tracking_columns()
    
    print(f"🔍 DEBUG: Excel columns found: {list(excel_df.columns)}")
    print(f"🔍 DEBUG: Database columns expected: {db_columns}")
    
    # Find columns that exist in both Excel and database
    matching_columns = []
    for col in excel_df.columns:
        # Clean column name for comparison
        clean_col = col.strip()
        
        # Check if column exists in database (exact match)
        if clean_col in db_columns:
            matching_columns.append(col)
            print(f"✅ Matched column: '{col}' -> '{clean_col}'")
        else:
            # Try various name variations
            variations = [
                clean_col.replace(' ', '_'),
                clean_col.replace('-', '_'),
                clean_col.replace(' ', ''),
                clean_col.replace('_', ' '),
                clean_col.title().replace(' ', '_'),
                clean_col.upper(),
                clean_col.lower()
            ]
            
            found_match = False
            for variant in variations:
                if variant in db_columns:
                    matching_columns.append(col)
                    print(f"✅ Matched column (variant): '{col}' -> '{variant}'")
                    found_match = True
                    break
            
            if not found_match:
                print(f"❌ No match for column: '{col}'")
    
    print(f"Found {len(matching_columns)} matching columns out of {len(excel_df.columns)} Excel columns for Machine_Tracking")
    print(f"Matching columns: {matching_columns}")
    
    # Return DataFrame with only matching columns
    return excel_df[matching_columns]

def map_excel_to_machine_tracking_columns(excel_df):
    """Map Excel DataFrame columns to Machine_Tracking database column names"""
    mapped_columns = {}
    db_columns = get_all_machine_tracking_columns()
    
    # Convert Excel column names to match database fields
    for col in excel_df.columns:
        # Clean column name (remove spaces, convert to proper case, etc.)
        clean_col = col.strip()
        
        # Direct mapping if exists
        if clean_col.lower() in MACHINE_TRACKING_FIELD_MAPPING:
            mapped_columns[col] = MACHINE_TRACKING_FIELD_MAPPING[clean_col.lower()]
            print(f"🔗 Mapped via dictionary: '{col}' -> '{MACHINE_TRACKING_FIELD_MAPPING[clean_col.lower()]}'")
        else:
            # Try exact match first
            if clean_col in db_columns:
                mapped_columns[col] = clean_col
                print(f"🔗 Exact match: '{col}' -> '{clean_col}'")
            else:
                # Try various name variations
                variations = [
                    clean_col.replace(' ', '_'),
                    clean_col.replace('-', '_'),
                    clean_col.replace(' ', ''),
                    clean_col.replace('_', ' '),
                    clean_col.title().replace(' ', '_'),
                    clean_col.upper(),
                    clean_col.lower()
                ]
                
                found_match = False
                for variant in variations:
                    if variant in db_columns:
                        mapped_columns[col] = variant
                        print(f"🔗 Variant match: '{col}' -> '{variant}'")
                        found_match = True
                        break
                
                if not found_match:
                    # Try fuzzy matching based on common patterns
                    col_lower = clean_col.lower().replace(' ', '').replace('_', '').replace('-', '')
                    for db_field in db_columns:
                        db_lower = db_field.lower().replace(' ', '').replace('_', '').replace('-', '')
                        if col_lower == db_lower:
                            mapped_columns[col] = db_field
                            print(f"🔗 Fuzzy match: '{col}' -> '{db_field}'")
                            found_match = True
                            break
                
                if not found_match:
                    print(f"❌ Skipping column '{col}' - not found in Machine_Tracking table")
    
    return mapped_columns