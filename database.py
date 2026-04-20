# ===== DATABASE CONNECTION MODULE =====
# Handles MySQL connections for the sas_db database
# Stores and retrieves user credentials

import mysql.connector
from mysql.connector import Error
import hashlib

class DatabaseConnection:
    def __init__(self, host='localhost', user='root', password='', database='sas_db'):
        """Initialize database connection"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print(f"Connected to {self.database} database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from database")
    
    def create_users_table(self):
        """Create users table if it doesn't exist"""
        try:
            cursor = self.connection.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(create_table_query)
            self.connection.commit()
            cursor.close()
            print("Users table created successfully")
            return True
        except Error as e:
            print(f"Error creating users table: {e}")
            return False
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email=None):
        """Register a new user"""
        try:
            cursor = self.connection.cursor()
            hashed_password = self.hash_password(password)
            insert_query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (username, hashed_password, email))
            self.connection.commit()
            cursor.close()
            print(f"User {username} registered successfully")
            return True
        except Error as e:
            print(f"Error registering user: {e}")
            return False
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            cursor = self.connection.cursor()
            select_query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                hashed_password = self.hash_password(password)
                if result[0] == hashed_password:
                    print(f"User {username} authenticated successfully")
                    return True
            print(f"Authentication failed for user {username}")
            return False
        except Error as e:
            print(f"Error verifying user: {e}")
            return False
    
    def user_exists(self, username):
        """Check if user already exists"""
        try:
            cursor = self.connection.cursor()
            select_query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except Error as e:
            print(f"Error checking user existence: {e}")
            return False

# Initialize database on import
def init_database():
    """Initialize database with default admin user"""
    db = DatabaseConnection()
    if db.connect():
        db.create_users_table()
        # Create default admin user if it doesn't exist
        if not db.user_exists('admin'):
            db.register_user('admin', 'password', 'admin@sas.com')
        db.disconnect()
