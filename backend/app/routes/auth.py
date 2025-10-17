from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import hashlib
import os
from datetime import datetime
from typing import Optional
from ..utils.sql_server_connection import sql_server

router = APIRouter()

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate user against Users table in RAGPrototipe database
    """
    try:
        conn = sql_server.get_connection()
        cursor = conn.cursor()
        
        # Query to get user by username
        query = """
        SELECT 
            ID,
            Username,
            Email,
            Password_Hash,
            Full_Name,
            Role,
            Department,
            Is_Active,
            Phone,
            Employee_ID,
            Manager_ID,
            Profile_Picture,
            Login_Count
        FROM Users 
        WHERE Username = ? AND Is_Active = 1
        """
        
        cursor.execute(query, (request.username,))
        user_row = cursor.fetchone()
        
        if not user_row:
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )
        
        # Convert row to dict
        columns = [column[0] for column in cursor.description]
        user_data = dict(zip(columns, user_row))
        
        # Verify password
        if not verify_password(request.password, user_data['Password_Hash']):
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )
        
        # Update last login and login count
        update_query = """
        UPDATE Users 
        SET 
            Last_Login = GETDATE(),
            Login_Count = ISNULL(Login_Count, 0) + 1,
            Last_Updated_At = GETDATE()
        WHERE ID = ?
        """
        cursor.execute(update_query, (user_data['ID'],))
        conn.commit()
        
        # Prepare user response (exclude sensitive data)
        user_response = {
            'id': user_data['ID'],
            'username': user_data['Username'],
            'email': user_data['Email'],
            'fullName': user_data['Full_Name'],
            'role': user_data['Role'],
            'department': user_data['Department'],
            'phone': user_data['Phone'],
            'employeeId': user_data['Employee_ID'],
            'managerId': user_data['Manager_ID'],
            'profilePicture': user_data['Profile_Picture'],
            'loginCount': user_data['Login_Count'] + 1  # Include the updated count
        }
        
        cursor.close()
        conn.close()
        
        return LoginResponse(
            success=True,
            message="Login successful",
            user=user_response
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.get("/verify-token")
async def verify_token():
    """
    Endpoint to verify if user session is still valid
    This is a placeholder - in production you'd verify JWT tokens
    """
    return {"valid": True}

@router.post("/logout")
async def logout():
    """
    Logout endpoint - in production this would invalidate tokens
    """
    return {"success": True, "message": "Logged out successfully"}

# Utility endpoint to create hashed passwords for testing
@router.post("/hash-password")
async def create_password_hash(password: str):
    """
    Utility endpoint to create password hashes for database seeding
    Remove this in production!
    """
    return {"password": password, "hash": hash_password(password)}