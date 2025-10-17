#!/usr/bin/env python3
import sys
sys.path.append('/home/appuser/app')

from app.utils.sql_server_connection import sql_server

try:
    # Test connection
    connected = sql_server.test_connection()
    print(f'SQL Server connection: {connected}')
    
    if connected:
        # Check if InspectionData table exists
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'InspectionData'
        """
        result = sql_server.execute_query(query)
        print(f'InspectionData table exists: {len(result) > 0}')
        
        if len(result) > 0:
            # Get column names
            col_query = """
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'InspectionData'
            ORDER BY ORDINAL_POSITION
            """
            columns_result = sql_server.execute_query(col_query)
            columns = [row[0] for row in columns_result]
            print(f'Total columns in InspectionData: {len(columns)}')
            
            # Check for Brand columns
            brand_cols = [col for col in columns if 'Brand' in col]
            print(f'\nBrand columns in database ({len(brand_cols)}):')
            for col in brand_cols:
                print(f'  {col}')
                
            # Check for LinkHeight columns
            link_cols = [col for col in columns if 'LinkHeight' in col]
            print(f'\nLinkHeight columns in database ({len(link_cols)}):')
            for col in link_cols:
                print(f'  {col}')
                
            # Check for Idlers_Brand columns
            idlers_brand_cols = [col for col in columns if 'Idlers_Brand' in col]
            print(f'\nIdlers_Brand columns in database ({len(idlers_brand_cols)}):')
            for col in idlers_brand_cols:
                print(f'  {col}')
                
        else:
            print('InspectionData table does not exist - need to create it first')
            
    else:
        print('Cannot connect to SQL Server')
        
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()