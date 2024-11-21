from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from config import config
from models.ModelUser import ModelUser
from models.entities.User import User

cineo = Flask(__name__)

# Configuración
cineo.config.from_object(config['development'])
cineo.config.from_object(config['mail'])

# Inicialización de extensiones
db = MySQL(cineo)
mail = Mail(cineo)
adminSession = LoginManager(cineo)
adminSession.login_view = 'signin'
adminSession.login_message = "Por favor, inicia sesión para acceder a esta página."

@adminSession.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(db, user_id)

# Rutas
@cineo.route('/')
def home():
    return render_template('home.html')

@cineo.route('/admin')
def admin():
    if 'PerfilU' in session and session['PerfilU'] == 'A':
        return render_template('admin.html')
    flash('Acceso no autorizado')
    return redirect(url_for('signin'))

@cineo.route('/user')
def user():
    return redirect(url_for('sPeliculas'))

@cineo.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        usuario = User(0,None,request.form['correo'],request.form['clave'],None,None)
        usuarioAutenticado = ModelUser.signin(db,usuario)
        if usuarioAutenticado is not None:
            if usuarioAutenticado.clave:
                login_user(usuarioAutenticado)
                session['NombreU'] = usuarioAutenticado.nombre
                session['PerfilU'] = usuarioAutenticado.perfil
                if usuarioAutenticado.perfil == 'A':
                    return render_template('admin.html')
                else:
                    return redirect(url_for('ssResenas'))
            else:
                flash('Contraseña incorrecta')
            return redirect(request.url)
        else:
            flash('Usuario inexistente')
            return redirect(request.url)
    else:
        return render_template('signin.html')


@cineo.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        clave = request.form.get('clave')

        if not nombre or not correo or not clave:
            flash('Todos los campos son obligatorios.')
            return redirect(request.url)

        try:
            claveCifrada = generate_password_hash(clave)
            fechaReg = datetime.datetime.now()
            cursor = db.connection.cursor()
            cursor.execute(
                "INSERT INTO usuario (nombre, correo, clave, fechareg) VALUES (%s, %s, %s, %s)",
                (nombre, correo, claveCifrada, fechaReg)
            )
            db.connection.commit()
            cursor.close()

            mensaje = Message(subject='Bienvenido XD', recipients=[correo])
            mensaje.html = render_template('mail.html', nombre=nombre)
            mail.send(mensaje)

            flash('Usuario registrado exitosamente.')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error al registrar el usuario: {e}')
            return redirect(request.url)
    return render_template('signup.html')

@cineo.route('/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    session.clear()
    flash('Has cerrado sesión correctamente.')
    return redirect(url_for('home'))

@cineo.route('/sUsuario', methods=['GET'])
def sUsuario():
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        cursor.close()
        return render_template('usuarios.html', usuarios=usuarios)
    except Exception as e:
        flash(f'Error al cargar usuarios: {e}')
        return redirect(url_for('home'))

@cineo.route('/iUsuario', methods=['POST'])
def iUsuario():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    clave = request.form.get('clave')
    perfil = request.form.get('perfil')

    if not nombre or not correo or not clave or not perfil:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('sUsuario'))

    try:
        claveCifrada = generate_password_hash(clave)
        fechaReg = datetime.datetime.now()

        cursor = db.connection.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombre, correo, clave, fechareg, perfil) VALUES (%s, %s, %s, %s, %s)",
            (nombre, correo, claveCifrada, fechaReg, perfil)
        )
        db.connection.commit()
        cursor.close()

        flash('Usuario agregado correctamente.')
    except Exception as e:
        flash(f'Error al agregar usuario: {e}')
    return redirect(url_for('sUsuario'))

@cineo.route('/uUsuario/<int:id>', methods=['POST'])
def uUsuario(id):
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    perfil = request.form.get('perfil')

    if not nombre or not correo or not perfil:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('sUsuario'))

    try:
        cursor = db.connection.cursor()
        cursor.execute(
            "UPDATE usuario SET nombre=%s, correo=%s, perfil=%s WHERE id=%s",
            (nombre.upper(), correo, perfil, id)
        )
        db.connection.commit()
        cursor.close()

        flash('Usuario actualizado correctamente.')
    except Exception as e:
        flash(f'Error al actualizar usuario: {e}')
    return redirect(url_for('sUsuario'))

@cineo.route('/dUsuario/<int:id>', methods=['POST'])
def dUsuario(id):
    try:
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM usuario WHERE id=%s", (id,))
        db.connection.commit()
        cursor.close()

        flash('Usuario eliminado correctamente.')
    except Exception as e:
        flash(f'Error al eliminar usuario: {e}')
    return redirect(url_for('sUsuario'))

@cineo.route('/sPeliculas', methods=['GET', 'POST'])
def sPeliculas():
    try:
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM pelicula")
        peliculas = cursor.fetchall()
        cursor.close()

        if 'PerfilU' in session and session['PerfilU'] == 'A':
            return render_template('peliculas.html', peliculas=peliculas)
        return render_template('user.html', peliculas=peliculas)
    except Exception as e:
        flash(f'Error al cargar películas: {e}')
        return redirect(url_for('home'))

if __name__ == "__main__":
    cineo.run(port=3300, debug=True)
