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
        cursor = None
        try:
            connection = self.get_connection()
            if not connection:
                print("Failed to establish database connection")
                return "Database connection failed"

            cursor = connection.cursor(dictionary=True)

            # Check if user exists first
            cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
            if cursor.fetchone():
                print(f"Email {email} already exists")
                return "Email already exists"

            # Insert new user
            sql = "INSERT INTO users (Name, Email, Password) VALUES (%s, %s, %s)"
            
            try:
                cursor.execute(sql, (name, email, password))
                connection.commit()
                print(f"User {email} registered successfully!")
                return "success"
            except mysql.connector.Error as insert_error:
                print(f"Insert Error Details: Errno: {insert_error.errno}, SQLState: {insert_error.sqlstate}, Msg: {insert_error}")
                connection.rollback()
                return f"Insert error: {insert_error}"

        except mysql.connector.Error as e:
            print(f"MySQL Error Details: Errno: {e.errno}, SQLState: {e.sqlstate}, Msg: {e}")
            if connection:
                connection.rollback()
            return f"Registration error: {e}"
        except Exception as e:
            print(f"Unexpected error during registration: {e}")
            if connection:
                connection.rollback()
            return f"Unexpected error: {e}"
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def login(self, email, password):
        connection = None
        cursor = None
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