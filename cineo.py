from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
from datetime import datetime


cineo = Flask(__name__)
db    = MySQL(cineo)

@cineo.route('/')
def home():
    return render_template('home.html')

@cineo.route('/signin')
def signin():
    return render_template('signin.html')

@cineo.route('/signup')
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contraseña = request.form['password']
        claveCifrada = generate_password_hash(contraseña)
        fechaReg = datetime.now() 

    return render_template('signup.html')

if __name__ == "__main__":
    cineo.run(debug=True,port=3300)
