import mysql.connector
from mysql.connector import Error
import time

class ConnectDatabase:
    def __init__(self):
        self._host = "junction.proxy.rlwy.net"
        self._user = "root"
        self._password = "AdGzajmAwcJPccXxoWqeFGAEiQISUGeM"
        self._database = "railway"
        self._port = 22274
        
        self.con = None
        self.cursor = None

    def get_connection(self):
        """Create a new database connection"""
        try:
            connection = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database,
                port=self._port
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None

    def register(self, name, email, password):
        connection = None
        try:
            connection = self.get_connection()
            if not connection:
                return "Database connection failed"

            cursor = connection.cursor(dictionary=True)

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
            if cursor.fetchone():
                return "Email already exists"

            # Insert new user
            sql = "INSERT INTO users (Name, Email, Password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, password))
            connection.commit()
            
            print("User registered successfully!")
            return "User registered successfully"

        except Error as e:
            print(f"Registration error: {e}")
            if connection:
                connection.rollback()
            return str(e)
        finally:
            if connection:
                if cursor:
                    cursor.close()
                connection.close()

    def login(self, email, password):
        connection = None
        try:
            connection = self.get_connection()
            if not connection:
                return "Database connection failed"

            cursor = connection.cursor(dictionary=True)

            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
            user = cursor.fetchone()

            if not user:
                return "Email does not exist"

            # Verify password
            if user['Password'] == password:
                return "True details"
            else:
                return "Incorrect password"

        except Error as e:
            print(f"Login error: {e}")
            return str(e)
        finally:
            if connection:
                if cursor:
                    cursor.close()
                connection.close()