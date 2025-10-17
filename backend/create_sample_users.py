import hashlib
from datetime import datetime
from app.utils.sql_server_connection import sql_server

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_sample_users():
    """Create sample users in the database"""
    try:
        conn = sql_server.get_connection()
        cursor = conn.cursor()
        
        # Sample users data
        users = [
            {
                'username': 'admin',
                'email': 'admin@komatsu.com',
                'password': 'admin123',
                'full_name': 'System Administrator',
                'role': 'admin',
                'department': 'IT',
                'phone': '+62-21-1234567',
                'employee_id': 'EMP001',
                'manager_id': None
            },
            {
                'username': 'analyst',
                'email': 'analyst@komatsu.com',
                'password': 'analyst123',
                'full_name': 'Data Analyst',
                'role': 'analyst',
                'department': 'Analytics',
                'phone': '+62-21-1234568',
                'employee_id': 'EMP002',
                'manager_id': None
            },
            {
                'username': 'operator',
                'email': 'operator@komatsu.com',
                'password': 'operator123',
                'full_name': 'System Operator',
                'role': 'operator',
                'department': 'Operations',
                'phone': '+62-21-1234569',
                'employee_id': 'EMP003',
                'manager_id': None
            },
            {
                'username': 'viewer',
                'email': 'viewer@komatsu.com',
                'password': 'viewer123',
                'full_name': 'System Viewer',
                'role': 'viewer',
                'department': 'General',
                'phone': '+62-21-1234570',
                'employee_id': 'EMP004',
                'manager_id': None
            },
            {
                'username': 'user',
                'email': 'user@komatsu.com',
                'password': 'user123',
                'full_name': 'Regular User',
                'role': 'user',
                'department': 'General',
                'phone': '+62-21-1234571',
                'employee_id': 'EMP005',
                'manager_id': None
            }
        ]
        
        # Check if users table exists and has the correct structure
        check_table_query = """
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'Users' AND TABLE_SCHEMA = 'dbo'
        ORDER BY ORDINAL_POSITION
        """
        
        cursor.execute(check_table_query)
        columns = cursor.fetchall()
        
        if not columns:
            print("Users table not found. Please create it first.")
            return
        
        print("Users table structure:")
        for col in columns:
            print(f"  {col[0]} ({col[1]})")
        
        # Insert or update users
        for user in users:
            # Check if user already exists
            check_query = "SELECT ID FROM Users WHERE Username = ?"
            cursor.execute(check_query, (user['username'],))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Update existing user
                update_query = """
                UPDATE Users SET 
                    Email = ?,
                    Password_Hash = ?,
                    Full_Name = ?,
                    Role = ?,
                    Department = ?,
                    Phone = ?,
                    Employee_ID = ?,
                    Manager_ID = ?,
                    Is_Active = 1,
                    Last_Updated_At = GETDATE(),
                    Last_Updated_By = 'System'
                WHERE Username = ?
                """
                cursor.execute(update_query, (
                    user['email'],
                    hash_password(user['password']),
                    user['full_name'],
                    user['role'],
                    user['department'],
                    user['phone'],
                    user['employee_id'],
                    user['manager_id'],
                    user['username']
                ))
                print(f"Updated user: {user['username']}")
            else:
                # Insert new user
                insert_query = """
                INSERT INTO Users (
                    Username, Email, Password_Hash, Full_Name, Role, Department,
                    Is_Active, Created_At, Created_By, Last_Updated_At, Last_Updated_By,
                    Phone, Employee_ID, Manager_ID, Login_Count
                ) VALUES (?, ?, ?, ?, ?, ?, 1, GETDATE(), 'System', GETDATE(), 'System', ?, ?, ?, 0)
                """
                cursor.execute(insert_query, (
                    user['username'],
                    user['email'],
                    hash_password(user['password']),
                    user['full_name'],
                    user['role'],
                    user['department'],
                    user['phone'],
                    user['employee_id'],
                    user['manager_id']
                ))
                print(f"Created user: {user['username']}")
        
        conn.commit()
        print("\nSample users created/updated successfully!")
        
        # Display created users
        cursor.execute("SELECT Username, Email, Full_Name, Role, Department FROM Users WHERE Is_Active = 1")
        users_list = cursor.fetchall()
        
        print("\nActive users in database:")
        for user in users_list:
            print(f"  {user[0]} - {user[2]} ({user[3]}) - {user[1]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    create_sample_users()