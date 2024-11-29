from flask import Flask, render_template, request, redirect, url_for, flash
from DB_connection import ConnectDatabase

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Important for flash messages

db = ConnectDatabase()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_process():
    email = request.form['email']
    password = request.form['password']
    
    result = db.login(email, password)
    
    if result == "True details":
        # Successful login logic
        return redirect(url_for('dashboard'))
    elif result == "Email is not exist":
        flash('Email does not exist', 'error')
    else:
        flash('Incorrect password', 'error')
    
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_process():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('register'))
    
    result = db.register(name, email, password)
    
    if result == "success":
        flash('Successfully Registered!', 'success')
        return redirect(url_for('login'))
    elif result == "Email already exists":
        flash('Email already exists', 'error')
    else:
        flash(f'Registration failed: {result}', 'error')
    
    return redirect(url_for('register'))

@app.route('/dashboard')
def dashboard():
    return "Welcome!"

if __name__ == '__main__':
    app.run(debug=True)