import mysql.connector
from mysql.connector import Error

class ConnectDatabase:
    def __init__(self):
        self._host="localhost"
        self._user="root"
        self._password="Redanganim1997"
        self._database="optivision"
        self.con=None
        self.cursor=None

    def connect_db(self):
        try:
            self.con = mysql.connector.connect(host=self._host,
                                                user=self._user,
                                                password=self._password,
                                                database=self._database)
            self.cursor=self.con.cursor(dictionary=True)
            if self.con.is_connected():
                print("Connection to MySQL database successful!")
                return True
            return False
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
        
    def register(self,name,email,password):
        self.connect_db()
        sql=f"""
        INSERT INTO optivision.users(Name,Email,Password)
        VALUES (%s,%s,%s);"""

        try:
            if(self.user_exists(email)):
                return "Email already exists"
            else:
                self.cursor.execute(sql,(name,email,password))
                self.con.commit()
                print("User registered successfully!")
        except Exception as E:
            self.con.rollback()
            print(E)
            return str(E)
        finally:
            #Close the db connection
            self.con.close()
            
    def login(self,email,password):
        self.connect_db()
        sql=f"""
        SELECT Password
        FROM optivision.users
        WHERE Email=%s;"""
        try:
            if not self.user_exists(email):
                return "Email is not exist"
            else:
                self.cursor.execute(sql,(email,))
                result=self.cursor.fetchone()
                extractedPass=result['Password']
                if password==extractedPass:
                    return "True details"
        except Exception as E:
            self.con.rollback()
            print(E)
            return str(E)
        finally:
            #Close the db connection
            self.con.close()
                
    def user_exists(self,email):
        sql=f"""
        SELECT *
        FROM users
        WHERE Email=%s;"""
        self.cursor.execute(sql,(email,))
        result=self.cursor.fetchone()
        return result is not None
    


    