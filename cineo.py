from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

cineo = Flask(__name__)
db = MySQL(cineo)
adminSession = LoginManager(cineo)

@adminSession.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@cineo.route('/')
def home():
    return render_template('home.html')

@cineo.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0,None,request.form['correo'],request.form['clave'],None,None)
        usuarioAutenticado = ModelUser.signin(db,usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return render_template ('user.html')
            else:
                return 'contraseña incorrecta'
        else:
            flash('Contraseña incorrecta')
            return redirect(url_for('request.url'))
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
        cursor.execute("INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s, %s, %s, %s)", (nombre, correo, claveCifrada, fechaReg))
        db.connection.commit()
    cursor.close()
    return redirect(url_for('signin'))  
    return render_template('signup.html')

@cineo.route('/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('home'))

@cineo.route('/sUsuario', methods=['GET','POST'])
def sUsuario():
    sUsuario = db.connection.cursor()
    sUsuario.execute("SELECT * FROM usuario")
    u = sUsuario.fetchall()
    sUsuario.close()
    return render_template('usuarios.html',usuarios=u)

@cineo.route('/iUsuario',methods=['GET', 'POST'])
def iUsuario():
    nombre = request.form['nombre']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechaReg = datetime.datetime.now()
    perfil = request.form
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO usuario (nombre, correo, clave, fechareg, perfil) VALUES (%s, %s, %s, %s)", (nombre, correo, claveCifrada, fechaReg, perfil))
    db.connection.commit()
    flash('usuario agregado')
    return redirect(url_for('sUsuario'))

@cineo.route('/uUsuario/<int:id>', methods=['GET', 'POST'])
def uUsuario(id):
    nombre=request.form['nombre']
    correo=request.form['correo']
    perfil=request.form['perfil']
    actUsuario = db.connection.cursor()
    actUsuario.execute("UPDATE usuario SET nombre=%s,correo=%s,perfil%s WHERE id=%s", (nombre.upper(),correo,perfil))
    db.connection.commit()
    actUsuario.close()
    flash('usuario actualizado')
    return redirect(url_for('sUsuario'))

if __name__ == "__main__":
    cineo.config.from_object(config['development'])
    cineo.run(port=5000)

