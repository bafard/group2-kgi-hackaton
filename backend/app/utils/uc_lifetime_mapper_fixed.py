"""
Mapping untuk field UC_Life_Time table
Membantu mapping kolom Excel ke field database UC_Life_Time untuk Expected Lifetime system
"""

# Mapping kolom Excel yang umum ke field database UC_Life_Time
UC_LIFETIME_FIELD_MAPPING = {
    # Basic Information
    'model': 'Model',
    'model code': 'Model',
    'modelcode': 'Model',

    # Lifetime conditions variations - dengan berbagai format yang mungkin
    'general_sand': 'General_Sand',
    'general sand': 'General_Sand',
    'generalsand': 'General_Sand',
    '[s]': 'General_Sand',  # Untuk format [S] di Excel
    's': 'General_Sand',

    'soil': 'Soil',
    '[so]': 'Soil',  # Format [SO]
    'so': 'Soil',

    'marsh': 'Marsh',
    '[m]': 'Marsh',  # Format [M]

    'coal': 'Coal',
    '[c]': 'Coal',  # Format [C]
    'c': 'Coal',

    'hard_rock': 'Hard_Rock',
    'hard rock': 'Hard_Rock',
    'hardrock': 'Hard_Rock',
    'hard_rock_conditions': 'Hard_Rock',
    '[hr]': 'Hard_Rock',  # Format [HR]
    'hr': 'Hard_Rock',
    '[h]': 'Hard_Rock',  # Format [H]
    'h': 'Hard_Rock',

    'brittle_rock': 'Brittle_Rock',
    'brittle rock': 'Brittle_Rock',
    'brittlerock': 'Brittle_Rock',
    'brittle_rock_conditions': 'Brittle_Rock',
    '[br]': 'Brittle_Rock',  # Format [BR]
    'br': 'Brittle_Rock',

    'pure_sand_middle_east': 'Pure_Sand_Middle_East',
    'pure sand middle east': 'Pure_Sand_Middle_East',
    'puresandmiddleeast': 'Pure_Sand_Middle_East',
    'pure_sand': 'Pure_Sand_Middle_East',
    'pure sand': 'Pure_Sand_Middle_East',
    'middle_east_sand': 'Pure_Sand_Middle_East',
    'middle east sand': 'Pure_Sand_Middle_East',
    '[ps]': 'Pure_Sand_Middle_East',  # Format [PS]
    'ps': 'Pure_Sand_Middle_East',

    'component': 'Component',
    'components': 'Component',
    'comp': 'Component',
}

def get_all_uc_lifetime_columns():
    """Return all actual column names from UC_Life_Time table (excluding ID as it's auto-increment)"""
    columns = [
        'Model',
        'General_Sand',
        'Soil',
        'Marsh',
        'Coal',
        'Hard_Rock',
        'Brittle_Rock',
        'Pure_Sand_Middle_East',
        'Component'
    ]
    return columns

def filter_excel_columns_for_uc_lifetime(excel_df):
    """Filter Excel DataFrame to only include columns that exist in UC_Life_Time table"""
    db_columns = get_all_uc_lifetime_columns()

    print(f"🔍 DEBUG: Excel columns found: {list(excel_df.columns)}")
    print(f"🔍 DEBUG: Database columns expected: {db_columns}")
    
    # Check if we need to find the real header row
    if any("Unnamed:" in str(col) for col in excel_df.columns):
        print("⚠️ Detected 'Unnamed' columns - looking for real header row...")
        # Try to find the row with the actual headers
        for i in range(min(5, len(excel_df))):  # Check first 5 rows
            row_data = excel_df.iloc[i].astype(str).str.lower()
            # Count how many expected headers we find in this row
            header_matches = sum(1 for val in row_data if any(header.lower() in str(val).lower() for header in ['model', 'general_sand', 'soil', 'marsh', 'coal', 'hard_rock', 'brittle_rock', 'pure_sand', 'component']))
            
            if header_matches >= 5:  # If we find at least 5 matching headers
                print(f"✅ Found real headers at row {i}: {list(row_data)}")
                # Use this row as headers and skip previous rows
                new_excel_df = excel_df.iloc[i+1:].copy()
                new_excel_df.columns = excel_df.iloc[i].values
                excel_df = new_excel_df
                print(f"🔄 Updated Excel columns: {list(excel_df.columns)}")
                break

    # Strategy 1: Try normal column matching
    matching_columns = []

    for i, col in enumerate(excel_df.columns):
        # Clean column name for comparison
        clean_col = str(col).strip()

        # Check if column exists in database (exact match)
        if clean_col in db_columns:
            matching_columns.append(col)
            print(f"✅ Matched column: '{col}' -> '{clean_col}'")
        else:
            # Try various name variations
            variations = [
                clean_col.replace(' ', '_'),
                clean_col.replace('-', '_'),
                clean_col.lower().replace(' ', '_'),
                clean_col.title().replace(' ', '_')
            ]

            matched = False
            for var in variations:
                if var in db_columns:
                    matching_columns.append(col)
                    print(f"✅ Matched column (variant): '{col}' -> '{var}'")
                    matched = True
                    break
            
            if not matched:
                # Check for mapping patterns
                if clean_col.lower() in UC_LIFETIME_FIELD_MAPPING:
                    mapped_to = UC_LIFETIME_FIELD_MAPPING[clean_col.lower()]
                    if mapped_to in db_columns:
                        matching_columns.append(col)
                        print(f"✅ Matched column (mapping): '{col}' -> '{mapped_to}'")
                        matched = True

            if not matched:
                print(f"❌ No match for column: '{col}'")

    print(f"Found {len(matching_columns)} matching columns out of {len(excel_df.columns)} Excel columns for UC_Life_Time")
    print(f"Matching columns: {matching_columns}")

    # If we don't have enough matches, try positional mapping strategy
    if len(matching_columns) < len(db_columns):
        print(f"🔄 Trying positional mapping strategy for UC_Life_Time...")
        return try_positional_mapping_uc_lifetime(excel_df)

    # Return filtered dataframe with matching columns only
    filtered_df = excel_df[matching_columns]
    return filtered_df

def try_positional_mapping_uc_lifetime(excel_df):
    """Try to map Excel columns to UC_Life_Time based on position and data content"""
    db_columns = get_all_uc_lifetime_columns()
    excel_columns = list(excel_df.columns)
    
    # Get sample data to help with mapping
    sample_data = excel_df.head(3).fillna('').astype(str)
    
    position_mapping = {}
    matched_columns = []
    
    # First pass: try exact matches and mappings
    for i, col in enumerate(excel_columns):
        clean_col = str(col).strip()
        
        # Check direct mapping first
        if clean_col.lower() in UC_LIFETIME_FIELD_MAPPING:
            target_field = UC_LIFETIME_FIELD_MAPPING[clean_col.lower()]
            if target_field in db_columns and target_field not in position_mapping.values():
                position_mapping[col] = target_field
                matched_columns.append(col)
                print(f"✅ Positional match: '{col}' -> '{target_field}' (position {i})")
                continue
        
        # Try positional mapping if within range
        if i < len(db_columns):
            target_field = db_columns[i]
            if target_field not in position_mapping.values():
                position_mapping[col] = target_field
                matched_columns.append(col)
                print(f"✅ Positional match: '{col}' -> '{target_field}' (position {i})")
            continue
    
    # Second pass: try data-based matching for remaining columns
    for col in excel_columns:
        if col in matched_columns:
            continue
            
        # Check data content for clues
        col_data = sample_data[col].tolist()
        col_data_str = ' '.join(col_data).lower()
        
        # Look for keyword hints in the data
        for target_field in db_columns:
            if target_field not in position_mapping.values():
                target_lower = target_field.lower()
                
                # Check if field name appears in data
                if target_lower in col_data_str or target_field.replace('_', ' ').lower() in col_data_str:
                    position_mapping[col] = target_field
                    matched_columns.append(col)
                    print(f"✅ Data-based match: '{col}' -> '{target_field}' (has data: {col_data})")
                    break
    
    print(f"Positional mapping result: {len(matched_columns)} columns mapped")
    
    if matched_columns:
        return excel_df[matched_columns]
    else:
        return excel_df

def map_excel_to_uc_lifetime_columns(excel_df):
    """Map Excel DataFrame columns to UC_Life_Time database column names with duplicate prevention"""
    mapped_columns = {}
    db_columns = get_all_uc_lifetime_columns()
    used_targets = set()  # Track already used target columns

    # Strategy 1: Try dictionary mapping first
    normal_mapping_count = 0

    # Convert Excel column names to match database fields
    for col in excel_df.columns:
        # Clean column name (remove spaces, convert to proper case, etc.)
        clean_col = str(col).strip()

        # Direct mapping if exists
        if clean_col.lower() in UC_LIFETIME_FIELD_MAPPING:
            target_field = UC_LIFETIME_FIELD_MAPPING[clean_col.lower()]
            if target_field not in used_targets:  # Prevent duplicates
                mapped_columns[col] = target_field
                used_targets.add(target_field)
                print(f"🔗 Mapped via dictionary: '{col}' -> '{target_field}'")
                normal_mapping_count += 1
            else:
                print(f"⚠️ Skipping duplicate mapping: '{col}' -> '{target_field}' (already mapped)")
        else:
            # Try exact match first
            if clean_col in db_columns and clean_col not in used_targets:
                mapped_columns[col] = clean_col
                used_targets.add(clean_col)
                print(f"🔗 Exact match: '{col}' -> '{clean_col}'")
                normal_mapping_count += 1
            else:
                # Try to find a pattern match but be very specific
                matched = False
                
                # Check if it's a known header pattern with very specific matching
                if "[H]" in clean_col or "Hard Rock" in clean_col:
                    if "Hard_Rock" not in used_targets:
                        mapped_columns[col] = "Hard_Rock"
                        used_targets.add("Hard_Rock")
                        print(f"🔗 Mapping match: '{col}' -> 'Hard_Rock'")
                        normal_mapping_count += 1
                        matched = True
                
                if not matched:
                    print(f"❌ No mapping found for: '{col}'")

    print(f"Found {normal_mapping_count} mapped columns via dictionary/exact match")

    # If we don't have enough mappings, don't try pattern matching - it's too risky
    # Instead, return what we have
    return mapped_columns