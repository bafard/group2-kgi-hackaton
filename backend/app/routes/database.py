"""
Database query routes for ManageSource functionality
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
from ..utils.sql_server_connection import sql_server

logger = logging.getLogger(__name__)

router = APIRouter()

class DatabaseQueryRequest(BaseModel):
    query: str
    system_type: str = "UMS"
    params: Optional[List] = None

class DatabaseQueryResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    total_records: int
    message: str

@router.post("/query", response_model=DatabaseQueryResponse)
async def execute_database_query(request: DatabaseQueryRequest):
    """
    Execute a database query and return results.
    Supports SELECT queries for data retrieval.
    
    Args:
        request: DatabaseQueryRequest with query, system_type, and optional params
    
    Returns:
        DatabaseQueryResponse with query results
    """
    try:
        # Validate query type - only allow SELECT queries for security
        query_upper = request.query.strip().upper()
        if not query_upper.startswith('SELECT'):
            raise HTTPException(
                status_code=400, 
                detail="Only SELECT queries are allowed for security reasons"
            )
        
        # Check for potentially dangerous SQL keywords
        dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'TRUNCATE', 'CREATE']
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Query contains potentially dangerous keyword: {keyword}"
                )
        
        # Execute query
        print(f"🔍 Executing query: {request.query}")
        
        if sql_server.test_connection():
            with sql_server.get_connection() as conn:
                cursor = conn.cursor()
                
                # Reset ROWCOUNT to ensure no limit is applied
                cursor.execute("SET ROWCOUNT 0")
                
                if request.params:
                    cursor.execute(request.query, request.params)
                else:
                    cursor.execute(request.query)
                
                # Get column names
                columns = [column[0] for column in cursor.description] if cursor.description else []
                
                # Fetch all results
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                data = []
                for row in rows:
                    row_dict = {}
                    for i, value in enumerate(row):
                        column_name = columns[i] if i < len(columns) else f"column_{i}"
                        # Handle datetime objects
                        if hasattr(value, 'isoformat'):
                            row_dict[column_name] = value.isoformat()
                        else:
                            row_dict[column_name] = value
                    data.append(row_dict)
                
                print(f"✅ Query executed successfully. Returned {len(data)} records")
                
                return DatabaseQueryResponse(
                    success=True,
                    data=data,
                    total_records=len(data),
                    message=f"Query executed successfully. Retrieved {len(data)} records."
                )
        else:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )
            
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Database query failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Database query execution failed: {str(e)}"
        )

@router.get("/tables")
async def list_available_tables():
    """
    List all available tables in the database.
    
    Returns:
        List of table names
    """
    try:
        if sql_server.test_connection():
            query = """
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
            """
            
            with sql_server.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                
                tables = [row[0] for row in rows]
                
                return {
                    "success": True,
                    "tables": tables,
                    "message": f"Found {len(tables)} tables"
                }
        else:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )
            
    except Exception as e:
        logger.error(f"Failed to list tables: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve table list: {str(e)}"
        )

@router.get("/table/{table_name}/schema")
async def get_table_schema(table_name: str):
    """
    Get schema information for a specific table.
    
    Args:
        table_name: Name of the table to describe
    
    Returns:
        Table schema information
    """
    try:
        if sql_server.test_connection():
            query = """
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                CHARACTER_MAXIMUM_LENGTH,
                NUMERIC_PRECISION,
                NUMERIC_SCALE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """
            
            with sql_server.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, [table_name])
                rows = cursor.fetchall()
                
                if not rows:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Table '{table_name}' not found"
                    )
                
                schema = []
                for row in rows:
                    schema.append({
                        "column_name": row[0],
                        "data_type": row[1],
                        "is_nullable": row[2] == 'YES',
                        "max_length": row[3],
                        "numeric_precision": row[4],
                        "numeric_scale": row[5]
                    })
                
                return {
                    "success": True,
                    "table_name": table_name,
                    "schema": schema,
                    "column_count": len(schema),
                    "message": f"Retrieved schema for table '{table_name}'"
                }
        else:
            raise HTTPException(
                status_code=500,
                detail="Database connection failed"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get table schema: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve table schema: {str(e)}"
        )