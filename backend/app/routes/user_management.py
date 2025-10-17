from fastapi import APIRouter, HTTPException, Depends, Form, File, UploadFile
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
import hashlib
import os
import re
from pathlib import Path

# Try to import SQL Server functionality
try:
    import pandas as pd
    from ..utils.sql_server_connection import sql_server
    SQL_SERVER_AVAILABLE = True
except ImportError:
    SQL_SERVER_AVAILABLE = False

router = APIRouter()

# Pydantic models for User
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str
    department: Optional[str] = None
    phone: Optional[str] = None
    employee_id: Optional[str] = None
    manager_id: Optional[int] = None
    
    @validator('email')
    def validate_email(cls, v):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    phone: Optional[str] = None
    employee_id: Optional[str] = None
    manager_id: Optional[int] = None
    is_active: Optional[bool] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v is not None:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Invalid email format')
        return v

class UserResponse(BaseModel):
    ID: int
    Username: str
    Email: str
    Full_Name: str
    Role: str
    Department: Optional[str]
    Is_Active: bool
    Created_At: datetime
    Created_By: Optional[str]
    Last_Updated_At: Optional[datetime]
    Last_Updated_By: Optional[str]
    Last_Login: Optional[datetime]
    Login_Count: int
    Phone: Optional[str]
    Employee_ID: Optional[str]
    Manager_ID: Optional[int]
    Profile_Picture: Optional[str]

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_sql_server_available():
    """Check if SQL Server is available and raise error if not"""
    if not SQL_SERVER_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="SQL Server functionality not available. Required dependencies missing."
        )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users():
    """Get all users from database"""
    check_sql_server_available()
    
    try:
        query = """
        SELECT ID, Username, Email, Full_Name, Role, Department, Is_Active,
               Created_At, Created_By, Last_Updated_At, Last_Updated_By,
               Last_Login, Login_Count, Phone, Employee_ID, Manager_ID, Profile_Picture
        FROM Users
        ORDER BY Created_At DESC
        """
        
        result = sql_server.execute_query(query)
        
        users = []
        for row in result:
            user = UserResponse(
                ID=row[0],
                Username=row[1],
                Email=row[2],
                Full_Name=row[3],
                Role=row[4],
                Department=row[5],
                Is_Active=bool(row[6]),
                Created_At=row[7],
                Created_By=row[8],
                Last_Updated_At=row[9],
                Last_Updated_By=row[10],
                Last_Login=row[11],
                Login_Count=row[12] or 0,
                Phone=row[13],
                Employee_ID=row[14],
                Manager_ID=row[15],
                Profile_Picture=row[16]
            )
            users.append(user)
        
        return users
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int):
    """Get user by ID"""
    check_sql_server_available()
    
    try:
        query = """
        SELECT ID, Username, Email, Full_Name, Role, Department, Is_Active,
               Created_At, Created_By, Last_Updated_At, Last_Updated_By,
               Last_Login, Login_Count, Phone, Employee_ID, Manager_ID, Profile_Picture
        FROM Users
        WHERE ID = ?
        """
        
        result = sql_server.execute_query(query, [user_id])
        
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        
        row = result[0]
        user = UserResponse(
            ID=row[0],
            Username=row[1],
            Email=row[2],
            Full_Name=row[3],
            Role=row[4],
            Department=row[5],
            Is_Active=bool(row[6]),
            Created_At=row[7],
            Created_By=row[8],
            Last_Updated_At=row[9],
            Last_Updated_By=row[10],
            Last_Login=row[11],
            Login_Count=row[12] or 0,
            Phone=row[13],
            Employee_ID=row[14],
            Manager_ID=row[15],
            Profile_Picture=row[16]
        )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create new user"""
    check_sql_server_available()
    
    try:
        # Check if username or email already exists
        check_query = "SELECT COUNT(*) FROM Users WHERE Username = ? OR Email = ?"
        existing = sql_server.execute_query(check_query, [user.username, user.email])
        
        if existing[0][0] > 0:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        # Hash password
        password_hash = hash_password(user.password)
        
        # Insert new user
        insert_query = """
        INSERT INTO Users (Username, Email, Password_Hash, Full_Name, Role, Department, 
                          Is_Active, Created_At, Created_By, Phone, Employee_ID, Manager_ID, Login_Count)
        VALUES (?, ?, ?, ?, ?, ?, 1, GETDATE(), 'System', ?, ?, ?, 0)
        """
        
        sql_server.execute_query(insert_query, [
            user.username, user.email, password_hash, user.full_name, user.role,
            user.department, user.phone, user.employee_id, user.manager_id
        ])
        
        # Get the created user
        get_query = "SELECT TOP 1 ID FROM Users WHERE Username = ? ORDER BY Created_At DESC"
        result = sql_server.execute_query(get_query, [user.username])
        user_id = result[0][0]
        
        return await get_user_by_id(user_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    """Update existing user"""
    check_sql_server_available()
    
    try:
        # Check if user exists
        existing = await get_user_by_id(user_id)
        
        # Build dynamic update query
        update_fields = []
        params = []
        
        if user.username is not None:
            update_fields.append("Username = ?")
            params.append(user.username)
        
        if user.email is not None:
            update_fields.append("Email = ?")
            params.append(user.email)
            
        if user.full_name is not None:
            update_fields.append("Full_Name = ?")
            params.append(user.full_name)
            
        if user.role is not None:
            update_fields.append("Role = ?")
            params.append(user.role)
            
        if user.department is not None:
            update_fields.append("Department = ?")
            params.append(user.department)
            
        if user.phone is not None:
            update_fields.append("Phone = ?")
            params.append(user.phone)
            
        if user.employee_id is not None:
            update_fields.append("Employee_ID = ?")
            params.append(user.employee_id)
            
        if user.manager_id is not None:
            update_fields.append("Manager_ID = ?")
            params.append(user.manager_id)
            
        if user.is_active is not None:
            update_fields.append("Is_Active = ?")
            params.append(user.is_active)
        
        if update_fields:
            update_fields.append("Last_Updated_At = GETDATE()")
            update_fields.append("Last_Updated_By = ?")
            params.append("System")
            
            update_query = f"UPDATE Users SET {', '.join(update_fields)} WHERE ID = ?"
            params.append(user_id)
            
            sql_server.execute_query(update_query, params)
        
        return await get_user_by_id(user_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete user (soft delete by setting Is_Active = False)"""
    check_sql_server_available()
    
    try:
        # Check if user exists
        await get_user_by_id(user_id)
        
        # Soft delete - set Is_Active to False
        update_query = """
        UPDATE Users 
        SET Is_Active = 0, Last_Updated_At = GETDATE(), Last_Updated_By = 'System'
        WHERE ID = ?
        """
        
        sql_server.execute_query(update_query, [user_id])
        
        return {"message": "User deactivated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/users/{user_id}/activate")
async def activate_user(user_id: int):
    """Activate user (set Is_Active = True)"""
    check_sql_server_available()
    
    try:
        # Check if user exists
        await get_user_by_id(user_id)
        
        # Activate user
        update_query = """
        UPDATE Users 
        SET Is_Active = 1, Last_Updated_At = GETDATE(), Last_Updated_By = 'System'
        WHERE ID = ?
        """
        
        sql_server.execute_query(update_query, [user_id])
        
        return {"message": "User activated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/users/search/{search_term}")
async def search_users(search_term: str):
    """Search users by username, email, or full name"""
    check_sql_server_available()
    
    try:
        query = """
        SELECT ID, Username, Email, Full_Name, Role, Department, Is_Active,
               Created_At, Created_By, Last_Updated_At, Last_Updated_By,
               Last_Login, Login_Count, Phone, Employee_ID, Manager_ID, Profile_Picture
        FROM Users
        WHERE Username LIKE ? OR Email LIKE ? OR Full_Name LIKE ?
        ORDER BY Created_At DESC
        """
        
        search_pattern = f"%{search_term}%"
        result = sql_server.execute_query(query, [search_pattern, search_pattern, search_pattern])
        
        users = []
        for row in result:
            user = UserResponse(
                ID=row[0],
                Username=row[1],
                Email=row[2],
                Full_Name=row[3],
                Role=row[4],
                Department=row[5],
                Is_Active=bool(row[6]),
                Created_At=row[7],
                Created_By=row[8],
                Last_Updated_At=row[9],
                Last_Updated_By=row[10],
                Last_Login=row[11],
                Login_Count=row[12] or 0,
                Phone=row[13],
                Employee_ID=row[14],
                Manager_ID=row[15],
                Profile_Picture=row[16]
            )
            users.append(user)
        
        return users
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/departments")
async def get_departments():
    """Get all unique departments"""
    check_sql_server_available()
    
    try:
        query = "SELECT DISTINCT Department FROM Users WHERE Department IS NOT NULL ORDER BY Department"
        result = sql_server.execute_query(query)
        
        departments = [row[0] for row in result]
        return {"departments": departments}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/roles")
async def get_roles():
    """Get all unique roles"""
    check_sql_server_available()
    
    try:
        query = "SELECT DISTINCT Role FROM Users WHERE Role IS NOT NULL ORDER BY Role"
        result = sql_server.execute_query(query)
        
        roles = [row[0] for row in result]
        return {"roles": roles}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")