from PyQt5 import QtWidgets
from GUI.Login import Ui_Login  
from GUI.Register import Ui_Register
from DB_connection import ConnectDatabase


class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.RegisterButton.clicked.connect(self.open_register_page)
        self.db=ConnectDatabase()
        self.email=self.ui.EmailEditBox
        self.password=self.ui.PasswordEditBox
        self.errorMessage=self.ui.ErrorMessage_label
        self.ui.LogInButton.clicked.connect(self.login)
        
    def login(self):
        try:
            email=self.email.text().strip()
            password=self.password.text().strip()
            if  not (password and email):
                self.errorMessage.setText("All fields are required!")
            else:
                result=self.db.login(email,password)
                if result=="Email is not exist":
                    self.errorMessage.setText("Email is not exist!")
                elif result=="True details":
                    self.errorMessage.setStyleSheet("color: rgb(0, 128, 0);")
                    self.errorMessage.setText("True Details!")
                else:
                    self.errorMessage.setText("Incorrect password!")
        except Exception as e:
            print(f"Error in login method: {str(e)}")
    def open_register_page(self):
        self.register_page = RegisterPage()
        self.register_page.show()
        self.close()  # Close the login page
        
class RegisterPage(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegisterPage, self).__init__()
        self.ui = Ui_Register()
        self.ui.setupUi(self)
        #go back to the login page
        self.ui.backButton.clicked.connect(self.open_login_page)
        #database connection object
        self.db=ConnectDatabase()
        
        self.name=self.ui.NameEditBox
        self.email=self.ui.EmailEditBox
        self.password=self.ui.Password1EditBox
        self.confirmPassword=self.ui.Password2EditBox
        self.registerButton=self.ui.RegisterButton
        self.ErrorMessage=self.ui.ErrorMessage_label

        self.registerButton.clicked.connect(self.register)
    def register(self):
        try:       
            # Get the values
            name = self.name.text().strip()
            email = self.email.text().strip()
            password = self.password.text().strip()
            confirmPassword= self.confirmPassword.text().strip()

            if password!=confirmPassword:
                self.ErrorMessage.setText("Passwords do not match!")
            elif  not (name and email and password and confirmPassword):
                self.ErrorMessage.setText("All fields are required!")
            else:
                result = self.db.register(name, email, password)
                if result is None:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Confirm")
                    msg.setText("Successfully Registered!")
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    self.open_login_page()
                elif result=="Email already exists":
                    self.ErrorMessage.setText("Email already exists!")
                else:
                    print("Error in registeration")

        except Exception as e:
            print(f"Error in register method: {str(e)}")
    

    def open_login_page(self):
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()  # Close the register page

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = LoginPage()
    main_window.show()
    sys.exit(app.exec_())


