import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class SQLServerConnection:
    def __init__(self):
        self.server = os.getenv('SQL_SERVER_HOST', 'localhost')
        self.port = os.getenv('SQL_SERVER_PORT', '1433')
        self.database = os.getenv('SQL_SERVER_DATABASE', 'RAGPrototipe')
        self.username = os.getenv('SQL_SERVER_USERNAME', 'sa')
        self.password = os.getenv('SQL_SERVER_PASSWORD', '')
        self.driver = os.getenv('SQL_SERVER_DRIVER', 'ODBC Driver 17 for SQL Server')
        
        # Connection string for pyodbc
        self.connection_string = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server},{self.port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            f"TrustServerCertificate=yes;"
        )
        
        # Connection string for SQLAlchemy
        self.sqlalchemy_url = (
            f"mssql+pyodbc://{self.username}:{self.password}@"
            f"{self.server}:{self.port}/{self.database}?"
            f"driver={self.driver.replace(' ', '+')}&TrustServerCertificate=yes"
        )
    
    def get_connection(self):
        """Get pyodbc connection"""
        try:
            conn = pyodbc.connect(self.connection_string)
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to SQL Server: {str(e)}")
            raise
    
    def get_engine(self):
        """Get SQLAlchemy engine"""
        try:
            engine = create_engine(self.sqlalchemy_url)
            return engine
        except Exception as e:
            logger.error(f"Failed to create SQLAlchemy engine: {str(e)}")
            raise
    
    def test_connection(self):
        """Test database connection"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def execute_query(self, query: str, params: List = None):
        """Execute a query and return results"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def truncate_table(self, table_name: str):
        """Truncate (clear all data) from specified table"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Execute TRUNCATE TABLE command
            truncate_query = f"TRUNCATE TABLE [{table_name}]"
            print(f"🗑️  Truncating table: {table_name}")
            cursor.execute(truncate_query)
            conn.commit()
            
            cursor.close()
            conn.close()
            
            print(f"✅ Table {table_name} truncated successfully")
            
        except Exception as e:
            logger.error(f"Table truncation failed for {table_name}: {str(e)}")
            raise

    def insert_dataframe_to_table(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append', batch_size: int = 50):
        """Insert pandas DataFrame to SQL Server table using batch processing"""
        try:
            if len(df) == 0:
                return 0
            
            engine = self.get_engine()
            total_rows = len(df)
            
            # If DataFrame is small enough, insert directly
            if total_rows <= batch_size:
                df.to_sql(table_name, engine, if_exists=if_exists, index=False, method='multi')
                print(f"✅ Inserted {total_rows} rows to {table_name}")
                return total_rows
            
            # Process in batches for large DataFrames
            total_inserted = 0
            batch_num = 1
            
            for start_idx in range(0, total_rows, batch_size):
                end_idx = min(start_idx + batch_size, total_rows)
                batch_df = df.iloc[start_idx:end_idx].copy()
                
                print(f"📦 Processing batch {batch_num}: rows {start_idx+1}-{end_idx} ({len(batch_df)} rows)")
                
                # For first batch, use the specified if_exists behavior
                # For subsequent batches, always append
                batch_if_exists = if_exists if start_idx == 0 else 'append'
                
                batch_df.to_sql(table_name, engine, if_exists=batch_if_exists, index=False, method='multi')
                total_inserted += len(batch_df)
                batch_num += 1
                
                print(f"✅ Batch {batch_num-1} inserted successfully ({len(batch_df)} rows)")
            
            print(f"🎉 Total inserted: {total_inserted}/{total_rows} rows to {table_name}")
            return total_inserted
            
        except Exception as e:
            logger.error(f"DataFrame insertion failed: {str(e)}")
            raise

# Global instance
sql_server = SQLServerConnection()