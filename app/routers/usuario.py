from flask import render_template, request, session, flash, redirect, url_for
from app import bp
from app.api.api_cliente import *
from app.api.api_usuario import *
from app.decorators import login_required, permission_required


@bp.route('/usuario')
@login_required
def usuario():
    usuario = session["usuario"]
    return render_template('usuario.html', usuario=usuario)


@bp.route('/user', methods=['POST', 'GET'], defaults={"iduser": 0})
@bp.route('/user/<iduser>', methods=['POST', 'GET'])
# @permission_required('sistema')
@login_required
def user(iduser):
    tipodocs, error = get_tipodoc()
    categorias, error = get_categorias()
    localidades, error = get_localidades()
    sucursales, error = get_sucursales()
    provincias, error = get_provincias()
    if error == None:
        if request.method == 'POST':
            iduser = request.form['buscar']
            user, error = get_user(iduser)
            if user.get('USUARIO') != None:
                session["user"] = user
                return render_template('/usuario_alt_baj.html', tipodocs=tipodocs, localidades=localidades, categorias=categorias, sucursales=sucursales, provincias=provincias)
            else:
                flash('Usuario no encontrado', category='error')
                return redirect(url_for('bp.user'))
        else:
            iduser = 0
            session['user'] = []
            return render_template('/usuario_alt_baj.html', tipodocs=tipodocs, localidades=localidades, categorias=categorias, sucursales=sucursales, provincias=provincias)
    else:
        return redirect(url_for('bp.user'))


@bp.route('/grabarUsuario', methods=["POST"])
# @permission_required('sistema')
@login_required
def grabarUsuario():
    if request.method == "POST":
        datosUser = {}
        datosUser['usuario'] = request.form['usuario']
        datosUser['tipodoc'] = request.form['tipodoc']
        datosUser['dni'] = request.form['dni']
        datosUser['nombre'] = request.form['nombre']
        datosUser['catego'] = request.form['catego']
        datosUser['cargo'] = request.form['cargo']
        datosUser['email'] = request.form['email']
        datosUser['provincia'] = request.form['provincia']
        datosUser['localidad'] = request.form['localidad']
        datosUser['sucursal'] = request.form['sucursal']
        datosUser['cpostal'] = request.form['cpostal']
        datosUser['domicilio1'] = request.form['domicilio1']
        datosUser['domicilio2'] = request.form['domicilio2']
        datosUser['codarea'] = request.form['codarea']
        datosUser['telefono'] = request.form['telefono']
        datosUser['codarea1'] = request.form['codarea1']
        datosUser['telefono1'] = request.form['telefono1']
        datosUser['obs'] = request.form['obs']
        datosUser['user_name'] = request.form['user_name']
        datosUser['clave'] = request.form['clave']
        if ((datosUser['usuario'] == '') or (datosUser['usuario'] == None)):
            error = insert_usuario(datosUser)
            if error == None:
                flash('Se agregó el usuario', category='info')
            return redirect(url_for('bp.user'))
        else:
            error = update_user(datosUser, datosUser.get('usuario'))
            if error == None:
                flash('Se actualizó el usuario', category='info')
            return redirect(url_for('bp.user'))


@bp.route('/deleteUser')
# @permission_required('sistema')
@login_required
def deleteUser():
    user = dict(session.get("user"))
    uID = user.get('USUARIO')
    if uID != None:
        error = drop_user(uID)
        if error == None:
            flash('Se inhabilitó el usuario', category='info')
            return redirect(url_for('bp.user'))
        else:
            flash('Error al inhabilitar el usuario', category='error')
            return redirect(url_for('bp.user'))
    else:
        flash('Se debe seleccionar un usuario', category='error')
        return redirect(url_for('bp.user'))
