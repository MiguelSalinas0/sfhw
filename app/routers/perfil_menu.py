from flask import render_template, request, flash
from app import bp
from app.api.api_perfil import *
from app.api.api_usuario import *
from app.decorators import login_required, permission_required


@bp.route('/nuevo_perfil/<op>')
# @permission_required('sistema')
@login_required
def nuevo_perfil(op):
    if op == '1':
        perfiles, error = get_all_perfil()
        if error == None:
            return render_template('nuevo_perfil.html', op=op, perfiles=perfiles)
    if op == '2':
        bandera = False
        usuarios, error = get_all_user()
        if error == None:
            return render_template('nuevo_perfil.html', op=op, usuarios=usuarios, bandera=bandera)
    if op == '3':
        menus, error = get_all_menu()
        perfiles, error = get_perfil_to_menu()
        perfilesNoAsignado = []
        for perfil in perfiles:
            if perfil['NOMBRE'] == None:
                perfilesNoAsignado.append(perfil)
        if error == None:
            return render_template('nuevo_perfil.html', op=op, menus=menus, perfiles=perfilesNoAsignado)


@bp.route('/nuevo_perfil/select_usr', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def select_usr():
    if request.method == "POST":
        usr = request.form['usuario']
        usuarios, error = get_all_user()
        us_per, error = get_rol(usr)
        if error == None:
            return render_template('nuevo_perfil.html', op='2', usuarios=usuarios, usr=usr, us_per=us_per)


@bp.route('/nuevo_perfil/eliminar_perfil', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def eliminar_perfil():
    if request.method == "POST":
        perfil = request.form['ide']
        error = delete_perfil(perfil)
        perfiles, error = get_all_perfil()
        if error == None:
            flash('Se eliminó el perfil', category='info')
            return render_template('nuevo_perfil.html', op='1', perfiles=perfiles)
        else:
            flash('No se pudo eliminar el perfil', category='error')
            return render_template('nuevo_perfil.html', op='1', perfiles=perfiles)


@bp.route('/nuevo_perfil/eliminar_menu', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def eliminar_menu():
    if request.method == "POST":
        menu = request.form['ide']
        error = delete_menu(menu)
        menus, error = get_all_menu()
        perfiles, error = get_perfil_to_menu()
        perfilesNoAsignado = []
        for perfil in perfiles:
            if perfil['NOMBRE'] == None:
                perfilesNoAsignado.append(perfil)
        if error == None:
            flash('Se eliminó el menú', category='info')
            return render_template('nuevo_perfil.html', op='3', menus=menus, perfiles=perfilesNoAsignado)
        else:
            flash('No se pudo eliminar el menú', category='error')
            return render_template('nuevo_perfil.html', op='3', menus=menus, perfiles=perfilesNoAsignado)


@bp.route('/nuevo_perfil/mod_perfil', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def mod_perfil():
    if request.method == "POST":
        op = request.form['option']
        usuarios, error = get_all_user()
        if op == '1':
            nombre = request.form['name'].upper()
            error = insert_perfil(nombre)
            perfiles, error = get_all_perfil()
            if error == None:
                flash('Se agregó el nuevo perfil', category='info')
                return render_template('nuevo_perfil.html', op=op, usuarios=usuarios, perfiles=perfiles)
            else:
                flash('No se pudo agregar el nuevo perfil', category='error')
                return render_template('nuevo_perfil.html', op=op, usuarios=usuarios, perfiles=perfiles)
        if op == '2':
            bandera = False
            usr = request.form['usuario']
            opc = request.form.getlist('opciones')
            us_per, error = get_rol(usr)
            rolesNoTiene = []
            rolesTiene = []
            rolesAsignar = []
            rolesQuitar = []
            for item in us_per:
                if usr != item['IDUSR']:
                    rolesNoTiene.append(item)
                else:
                    rolesTiene.append(item)
            for rol in rolesNoTiene:
                if rol['ID'] in opc:
                    rolesAsignar.append(rol)
            for rol in rolesTiene:
                if rol['ID'] not in opc:
                    rolesQuitar.append(rol)
            error = insert_usr_perfil(rolesAsignar, rolesQuitar, usr)
            if error == None:
                flash('Se modificaron los perfiles', category='info')
                return render_template('nuevo_perfil.html', op=op, usuarios=usuarios, bandera=bandera)
            else:
                flash('No se pudieron modificar los perfiles', category='error')
                return render_template('nuevo_perfil.html', op=op, usuarios=usuarios, bandera=bandera)
        if op == '3':
            menu = request.form['menu'].upper()
            perfil = request.form['perfil']
            error = insert_menu(menu, perfil)
            menus, error = get_all_menu()
            perfiles, error = get_perfil_to_menu()
            perfilesNoAsignado = []
            for perfil in perfiles:
                if perfil['NOMBRE'] == None:
                    perfilesNoAsignado.append(perfil)
            if error == None:
                flash('Se agregó el nuevo menú', category='info')
                return render_template('nuevo_perfil.html', op=op, menus=menus, perfiles=perfilesNoAsignado)
            else:
                flash('No se pudo agregar el nuevo menú', category='error')
                return render_template('nuevo_perfil.html', op=op, menus=menus, perfiles=perfilesNoAsignado)
