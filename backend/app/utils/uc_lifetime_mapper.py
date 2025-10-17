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
    'm': 'Marsh',
    
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
                clean_col.replace(' ', ''),
                clean_col.replace('_', ' '),
                clean_col.title().replace(' ', '_'),
                clean_col.upper(),
                clean_col.lower(),
                clean_col.replace('[', '').replace(']', '').lower(),  # Remove brackets
                clean_col.split('[')[-1].replace(']', '').lower() if '[' in clean_col else None  # Extract content in brackets
            ]
            
            # Remove None values
            variations = [v for v in variations if v is not None]
            
            found_match = False
            for variant in variations:
                if variant in db_columns:
                    matching_columns.append(col)
                    print(f"✅ Matched column (variant): '{col}' -> '{variant}'")
                    found_match = True
                    break
                # Check in mapping dictionary
                elif variant.lower() in UC_LIFETIME_FIELD_MAPPING:
                    matching_columns.append(col)
                    print(f"✅ Matched column (mapping): '{col}' -> '{UC_LIFETIME_FIELD_MAPPING[variant.lower()]}'")
                    found_match = True
                    break
            
            # Special handling untuk kolom header yang kompleks
            if not found_match:
                # Check if column contains key patterns
                col_lower = clean_col.lower()
                if any(pattern in col_lower for pattern in ['[s]', '[so]', '[m]', '[c]', '[hr]', '[h]', '[br]', '[ps]']):
                    # Extract the pattern and map it
                    for pattern, db_field in UC_LIFETIME_FIELD_MAPPING.items():
                        if pattern in col_lower:
                            matching_columns.append(col)
                            print(f"✅ Matched column (pattern): '{col}' -> '{db_field}' (pattern: {pattern})")
                            found_match = True
                            break
                
                if not found_match:
                    print(f"❌ No match for column: '{col}'")
    
    # Strategy 2: If we have very few matches, try positional mapping for common UC_Life_Time formats
    if len(matching_columns) <= 2 and len(excel_df.columns) >= 8:
        print("🔄 Trying positional mapping strategy for UC_Life_Time...")
        # Common pattern: Model, General_Sand, Soil, Marsh, Coal, Hard_Rock, Brittle_Rock, Pure_Sand_Middle_East, Component
        expected_order = ['Model', 'General_Sand', 'Soil', 'Marsh', 'Coal', 'Hard_Rock', 'Brittle_Rock', 'Pure_Sand_Middle_East', 'Component']
        matching_columns = []
        
        for i, col in enumerate(excel_df.columns):
            if i < len(expected_order):
                # Skip if it looks like empty or merged header
                col_str = str(col).strip()
                if not col_str.startswith('Unnamed:') or i == 0:  # Always include first column (Model)
                    matching_columns.append(col)
                    print(f"✅ Positional match: '{col}' -> '{expected_order[i]}' (position {i})")
                else:
                    # Try next few columns to find non-empty content
                    sample_data = excel_df[col].dropna().astype(str).str.strip()
                    non_empty_data = sample_data[sample_data != ''].head(3)
                    if len(non_empty_data) > 0:
                        matching_columns.append(col)
                        print(f"✅ Data-based match: '{col}' -> '{expected_order[i]}' (has data: {list(non_empty_data)})")
    
    print(f"Found {len(matching_columns)} matching columns out of {len(excel_df.columns)} Excel columns for UC_Life_Time")
    print(f"Matching columns: {matching_columns}")
    
    # Return DataFrame with only matching columns
    return excel_df[matching_columns] if matching_columns else excel_df

def map_excel_to_uc_lifetime_columns(excel_df):
    """Map Excel DataFrame columns to UC_Life_Time database column names"""
    mapped_columns = {}
    db_columns = get_all_uc_lifetime_columns()
    
    # Strategy 1: Try normal column matching
    normal_mapping_count = 0
    
    # Convert Excel column names to match database fields
    for col in excel_df.columns:
        # Clean column name (remove spaces, convert to proper case, etc.)
        clean_col = str(col).strip()
        
        # Direct mapping if exists
        if clean_col.lower() in UC_LIFETIME_FIELD_MAPPING:
            mapped_columns[col] = UC_LIFETIME_FIELD_MAPPING[clean_col.lower()]
            print(f"🔗 Mapped via dictionary: '{col}' -> '{UC_LIFETIME_FIELD_MAPPING[clean_col.lower()]}'")
            normal_mapping_count += 1
        else:
            # Try exact match first
            if clean_col in db_columns:
                mapped_columns[col] = clean_col
                print(f"🔗 Exact match: '{col}' -> '{clean_col}'")
                normal_mapping_count += 1
            else:
                # Try various name variations
                variations = [
                    clean_col.replace(' ', '_'),
                    clean_col.replace('-', '_'),
                    clean_col.replace(' ', ''),
                    clean_col.replace('_', ' '),
                    clean_col.title().replace(' ', '_'),
                    clean_col.upper(),
                    clean_col.lower(),
                    clean_col.replace('[', '').replace(']', '').lower(),  # Remove brackets
                    clean_col.split('[')[-1].replace(']', '').lower() if '[' in clean_col else None  # Extract content in brackets
                ]
                
                # Remove None values
                variations = [v for v in variations if v is not None]
                
                found_match = False
                for variant in variations:
                    if variant in db_columns:
                        mapped_columns[col] = variant
                        print(f"🔗 Variant match: '{col}' -> '{variant}'")
                        found_match = True
                        normal_mapping_count += 1
                        break
                    elif variant.lower() in UC_LIFETIME_FIELD_MAPPING:
                        mapped_columns[col] = UC_LIFETIME_FIELD_MAPPING[variant.lower()]
                        print(f"🔗 Mapping match: '{col}' -> '{UC_LIFETIME_FIELD_MAPPING[variant.lower()]}'")
                        found_match = True
                        normal_mapping_count += 1
                        break
                
                # Special pattern matching untuk header yang kompleks
                if not found_match:
                    col_lower = clean_col.lower()
                    for pattern, db_field in UC_LIFETIME_FIELD_MAPPING.items():
                        # Only match specific patterns, not single letters in middle of words
                        if pattern in col_lower and (
                            pattern.startswith('[') or  # Bracket patterns like [H], [M]
                            len(pattern) > 1 or  # Multi-character patterns
                            (len(pattern) == 1 and col_lower == pattern)  # Single letter only if exact match
                        ):
                            mapped_columns[col] = db_field
                            print(f"🔗 Pattern match: '{col}' -> '{db_field}' (pattern: {pattern})")
                            found_match = True
                            normal_mapping_count += 1
                            break
                
                if not found_match:
                    # Try fuzzy matching based on common patterns
                    col_lower = clean_col.lower().replace(' ', '').replace('_', '').replace('-', '').replace('[', '').replace(']', '')
                    for db_field in db_columns:
                        db_lower = db_field.lower().replace(' ', '').replace('_', '').replace('-', '')
                        if col_lower == db_lower:
                            mapped_columns[col] = db_field
                            print(f"🔗 Fuzzy match: '{col}' -> '{db_field}'")
                            found_match = True
                            normal_mapping_count += 1
                            break
                
                if not found_match:
                    print(f"❌ Skipping column '{col}' - not found in UC_Life_Time table")
    
    # Strategy 2: If normal mapping failed, use positional mapping
    if normal_mapping_count <= 2 and len(excel_df.columns) >= 8:
        print("🔄 Using positional mapping strategy...")
        mapped_columns = {}
        expected_order = ['Model', 'General_Sand', 'Soil', 'Marsh', 'Coal', 'Hard_Rock', 'Brittle_Rock', 'Pure_Sand_Middle_East', 'Component']
        
        for i, col in enumerate(excel_df.columns):
            if i < len(expected_order):
                mapped_columns[col] = expected_order[i]
                print(f"🔗 Positional mapping: '{col}' -> '{expected_order[i]}' (position {i})")
    
    # Check for duplicate mappings and fix them
    reverse_mapping = {}
    for col, db_field in list(mapped_columns.items()):
        if db_field in reverse_mapping:
            print(f"⚠️  Duplicate mapping detected: '{col}' and '{reverse_mapping[db_field]}' both map to '{db_field}'")
            # Remove the duplicate, keep the first one
            del mapped_columns[col]
            print(f"🗑️  Removed duplicate mapping: '{col}' -> '{db_field}'")
        else:
            reverse_mapping[db_field] = col
    
    return mapped_columns