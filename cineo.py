from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import datetime
from config import config

cineo = Flask(__name__)
cineo.config.from_object(config['development'])
db = MySQL(cineo)

@cineo.route('/')
def home():
    return render_template('home.html')

@cineo.route('/signin')
def signin():
    return render_template('signin.html')

@cineo.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        claveCifrada = generate_password_hash(clave)
        fechaReg = datetime.datetime.now()
        
        cursor = db.connection.cursor()
        cursor.execute("INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s, %s, %s, %s)", 
                       (nombre, correo, claveCifrada, fechaReg))
        db.connection.commit()
        cursor.close()
        
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    cineo.run(port=5000)

