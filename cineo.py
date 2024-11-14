from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

cineo = Flask(__name__)
db = MySQL(cineo)
#pythonanywhere
cineo.config.from_object(config['development'])
adminSession = LoginManager(cineo)

@adminSession.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(db, user_id)

@cineo.route('/')
def home():
    return render_template('home.html')


@cineo.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0, None, request.form['correo'], request.form['clave'], None, None)
        usuarioAutenticado = ModelUser.signin(db, usuario)
        
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                session ['NombreU'] = usuarioAutenticado.nombre
                session ['PerfilU'] = usuarioAutenticado.perfil
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return redirect(url_for('sPeliculas'))
            else:
                flash('Contraseña incorrecta')
                return redirect(url_for('signin'))  
        else:
            flash('Usuario no encontrado')
            return redirect(url_for('signin'))
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
        regUsuario = db.connection.cursor()
        regUsuario.execute("INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s, %s, %s, %s)",(nombre, correo, claveCifrada, fechaReg))
        db.connection.commit()
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

@cineo.route('/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('home'))

@cineo.route('/sUsuario', methods=['GET'])
def sUsuario():
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

@cineo.route('/iUsuario', methods=['POST'])
def iUsuario():
    nombre = request.form['nombre']
    correo = request.form['correo']
    clave = request.form['clave']
    claveCifrada = generate_password_hash(clave)
    fechaReg = datetime.datetime.now()
    perfil = request.form['perfil']  

    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO usuario (nombre, correo, clave, fechareg, perfil) VALUES (%s, %s, %s, %s, %s)",(nombre, correo, claveCifrada, fechaReg, perfil))
    db.connection.commit()
    flash('Usuario agregado')
    return redirect(url_for('sUsuario'))

@cineo.route('/uUsuario/<int:id>', methods=['POST'])
def uUsuario(id):
    nombre = request.form['nombre']
    correo = request.form['correo']
    perfil = request.form['perfil']

    cursor = db.connection.cursor()
    cursor.execute("UPDATE usuario SET nombre=%s, correo=%s, perfil=%s WHERE id=%s",(nombre.upper(), correo, perfil, id))
    db.connection.commit()
    cursor.close()
    flash('Usuario actualizado')
    return redirect(url_for('sUsuario'))

@cineo.route('/dUsuario/<int:id>', methods=['POST'])
def dUsuario(id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM usuario WHERE id=%s", (id,))
    db.connection.commit()
    cursor.close()
    flash('Usuario eliminado')
    return redirect(url_for('sUsuario'))

@cineo.route('/sPeliculas', methods=['GET', 'POST'])
def sPerfiles():
    selPeliculas = db.connection.cursor()
    selPeliculas.execute("SELECT * FROM peliculas")
    pel = selPeliculas.fetchall()
    selPeliculas.close()
    if session['PerfilU'] == 'A':
        return render_template ('peliculas.html', peliculas=pel)
    return render_template('user.html', peliculas=pel)

''' if __name__ == "__main__":
    cineo.config.from_object(config['development'])
    cineo.run(port=5000) '''
