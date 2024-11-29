import mysql.connector
from mysql.connector import Error

class ConnectDatabase:
    def __init__(self):
        self._host = "junction.proxy.rlwy.net"
        self._user = "root"  # Changed to root
        self._password = "AdGzajmAwcJPccXxoWqeFGAEiQISUGeM"
        self._database = "optivision"  # Use the railway database
        self._port = 22274  # Add the specific Railway port
        
        self.con = None
        self.cursor = None

    def connect_db(self):
        try:
            self.con = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database,
                port=self._port
            )
            self.cursor = self.con.cursor(dictionary=True)
            if self.con.is_connected():
                print("Connection to MySQL database successful!")
                return True
            return False
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
        
    def register(self, name, email, password):
        try:
            # Ensure connection is established
            if not self.connect_db():
                return "Database connection failed"

            # Check if user exists before inserting
            if self.user_exists(email):
                return "Email already exists"

            # SQL to insert into users table
            sql = """
            INSERT INTO users (Name, Email, Password)
            VALUES (%s, %s, %s);
            """

            self.cursor.execute(sql, (name, email, password))
            self.con.commit()
            print("User registered successfully!")
            return "User registered successfully"

        except Exception as E:
            self.con.rollback()
            print(f"Registration error: {E}")
            return str(E)
        finally:
            # Close the db connection
            if self.con and self.con.is_connected():
                self.cursor.close()
                self.con.close()
            
    def login(self, email, password):
        try:
            # Ensure connection is established
            if not self.connect_db():
                return "Database connection failed"

            # Check if user exists
            if not self.user_exists(email):
                return "Email does not exist"

            # SQL to fetch password
            sql = """
            SELECT Password
            FROM users
            WHERE Email = %s;
            """

            self.cursor.execute(sql, (email,))
            result = self.cursor.fetchone()
            
            if result:
                extractedPass = result['Password']
                if password == extractedPass:
                    return "True details"
                else:
                    return "Incorrect password"
            
            return "Login failed"

        except Exception as E:
            print(f"Login error: {E}")
            return str(E)
        finally:
            # Close the db connection
            if self.con and self.con.is_connected():
                self.cursor.close()
                self.con.close()
                
    def user_exists(self, email):
        try:
            # Ensure connection is established
            if not self.connect_db():
                return False

            sql = """
            SELECT *
            FROM users
            WHERE Email = %s;
            """

            self.cursor.execute(sql, (email,))
            result = self.cursor.fetchone()
            return result is not None

        except Exception as E:
            print(f"User exists check error: {E}")
            return False
        finally:
            # Close the db connection
            if self.con and self.con.is_connected():
                self.cursor.close()
                self.con.close()