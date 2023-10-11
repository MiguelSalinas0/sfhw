from flask import render_template, url_for, request, redirect, session, flash

from app.api.api_usuario import *

from app import bp

def mostrar_mensaje_flash(tipo, mensaje):
    flash(mensaje, tipo)

def mostrar_error_conexion():
    mostrar_mensaje_flash("error", "Error de conexión con el servicio web")


@bp.route('/')
def index():
    if "usuario" in session:
        data = {
            'titulo': 'San Francisco Hogar'
        }
        return render_template('index.html', data=data)
    else:
        return redirect(url_for("bp.login"))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        datosUsr, error = get_usuario(usuario=usuario, clave=clave)
        print(datosUsr)
        if error:
            mostrar_mensaje_flash("error", "Nombre de usuario y/o clave incorrectos")
        elif "USUARIO" in datosUsr:
            session["usuario"] = datosUsr["USUARIO"]
            session["nombreUsr"] = datosUsr["NOMBRE"]
            nomUsuario = session["nombreUsr"]
            menus, error = get_menu(session['usuario'])
            if error:
                mostrar_error_conexion()
            else:
                session['menu'] = menus
                session["items"] = []
                session["cliente"] = []
                session['mensajes'] = []
                mostrar_mensaje_flash("info", f"Inicio de sesión exitosa - {nomUsuario}")
                return redirect(url_for('bp.usuario'))
        else:
            mostrar_mensaje_flash("error", "Nombre de usuario y/o clave incorrectos")
    elif "usuario" in session:
        usuario = session['usuario']
        mostrar_mensaje_flash("info", f"La sesión ya estaba iniciada - {usuario}")
        return redirect(url_for("bp.usuario"))
    return render_template('login.html')


@bp.route('/logout')
def logout():
    if "usuario" in session:
        usuario = session.pop("usuario")
        session.pop("cliente", None)
        session.pop("items", None)
        session.pop("mensajes", None)
        mostrar_mensaje_flash("info", f"Sesión terminada - {usuario}")
    return redirect(url_for("bp.login"))
