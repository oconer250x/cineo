from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

cineo = Flask(__name__)
db = MySQL(cineo)
adminSession = LoginManager(cineo)

@adminSession.user_loader
def addUser(id):
    return ModelUser.get_by_id(db,id)

@cineo.route('/')
def home():
    return render_template('home.html')

@cineo.route('/signin',methods=['GET', 'POST'])
def signin():
    if request.form == 'POST':
        usuario = User(0,None,request.form['correo'],request.form['clave'],None,None)
        usuarioAutenticado = ModelUser.signin(db,usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                if usuarioAutenticado.perfil == 'A':
                    return render_template ('admin.html')
                else:
                    return render_template ('user.html')
            else:
                return 'contraseña incorrecta'
        else:
            return 'usuario inexistente'
    else:
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
        cursor.execute("INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s, %s, %s, %s)",(nombre, correo, claveCifrada, fechaReg))
        db.connection.commit()
        cursor.close()
        
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    cineo.config.from_object(config['development'])
    cineo.run(port=5000)

