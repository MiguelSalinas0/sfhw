import json
import pytz
import requests
import re
from flask import (Flask, jsonify, render_template, url_for, request, redirect, session, flash)
from datetime import datetime, timedelta
from api.api_cliente import *
from api.api_credito import *
from api.api_usuario import *
from api.api_perfil import *
from api.api_mensajes import *
from api.api_credixsa import *
from api.api_excel import *
from db.db import get_db, init_app

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
app.secret_key = "ffgghhllmm"


@app.before_request
def before_request():
    print('antes de la petición')
    paso = request.path
    print(paso)


@app.after_request
def after_request(response):
    print('Despues de la petición')
    return response


@app.route('/')
def index():
    if "usuario" in session:
        data = {
            'titulo': 'San Francisco Hogar'
        }
        return render_template('index.html', data=data)
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.path == '/login':
            print('se encuentra en la ruta cliente')
    if request.method == 'POST':
        usuario = request.form['usuario']
        # session.permanent = True
        clave = request.form['clave']
        datosUsr, error = get_usuario(usuario = usuario, clave = clave)
        try:
            if error == None:
                if "USUARIO" in datosUsr:
                    session["usuario"] = datosUsr["USUARIO"]
                    session["nombreUsr"] = datosUsr["NOMBRE"]
                    nomUsuario = session["nombreUsr"]
                    menus, error = get_menu(session['usuario'])
                    session['menu'] = menus
                    session["items"] = []
                    session["cliente"] = []
                    session['mensajes'] = []
                    flash(f"Inicio de sesión exitosa - { nomUsuario }", "info")
                    return redirect(url_for('usuario'))
                else:
                    flash(f"Nombre de usuario y/o clave erroneos", "error")
                    return redirect(url_for("login"))
            else:
                flash(f"Nombre de usuario y/o clave erroneos", "error")
                return redirect(url_for("login"))
        except requests.exceptions.RequestException as e:
            flash(f"Error de conección con el WS:{e}", "error")
            return redirect(url_for("login"))
    else:
        if "usuario" in session:
            usuario = session['usuario']
            flash(f"La sesión ya estaba iniciada - {usuario}", "info")
            return redirect(url_for("usuario"))
        return render_template('login.html')


@app.route('/logout')
def logout():
    if "usuario" in session:
        usuario = session["usuario"]
        flash(f"Sesión terminada - {usuario}", "info")
    session.pop("usuario", None)
    session.pop("cliente", None)
    session.pop("items", None)
    session.pop("mensajes", None)
    return redirect(url_for("login"))


@app.route('/usuario')
def usuario():
    if "usuario" in session:
        usuario = session["usuario"]
        return render_template('usuario.html', usuario=usuario)
    else:
        flash('No está iniciada la sesión')
        return redirect(url_for('login'))


@app.route('/cliente', methods=['POST', 'GET'], defaults={"idclien": 0})
@app.route('/cliente/<idclien>', methods=['POST', 'GET'])
def cliente(idclien):
    if "usuario" in session:
        if eval_menu(session.get('menu'), 'sistema'):
            tipodocs, error = get_tipodoc()
            categorias, error = get_categorias()
            tipocontribs, error = get_tipocontrib()
            estadosciviles, error = get_estadocivil()
            localidades, error = get_localidades()
            viviendas, error = get_viviendas()
            actividades, error = get_actividades()
            if error == None:
                if request.method == 'POST':
                    idclien = request.form['buscar']
                    cliente, error = get_cliente(idclien)
                    if error == None:
                        session["cliente"] = cliente
                        return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, viviendas=viviendas, actividades=actividades, categorias=categorias)
                    else:
                        cliente = 0
                        session['cliente'] = []
                        session['items'] = []
                        flash(f'Error obteniendo datos del cliente: {error}', 'error')
                        return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, viviendas=viviendas, actividades=actividades, categorias=categorias)
                else:
                    cliente = 0
                    session['cliente'] = []
                    session['items'] = []
                    return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, viviendas=viviendas, actividades=actividades, categorias=categorias)
            else:
                return redirect(url_for('cliente'))
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('usuario'))
    else:
        return redirect(url_for("login"))


@app.route('/grabarCliente', methods=["POST"])
def grabarCliente():
    if request.method == "POST":
        if eval_menu(session.get('menu'), 'sistema'):
            datosCliente = {}
            datosCliente['clien'] = request.form['clien']
            datosCliente['catego'] = request.form['catego']
            datosCliente['nombre'] = request.form['nombre']
            datosCliente['apellido'] = request.form['apellido']
            datosCliente['tdoc'] = request.form['tipodoc']
            datosCliente['dni'] = request.form['documento']
            datosCliente['ctrib'] = request.form['ctrib']
            datosCliente['domicilio1'] = request.form['domicilio1']
            datosCliente['domicilio2'] = request.form['domicilio2']
            datosCliente['calle1'] = request.form['calle1']
            datosCliente['calle2'] = request.form['calle2']
            datosCliente['codloc'] = request.form['codloc']
            datosCliente['estadociv'] = request.form['estadociv']
            datosCliente['email'] = request.form['email']
            datosCliente['codarea'] = request.form['codarea']
            datosCliente['telefono'] = request.form['telefono']
            datosCliente['codarea1'] = request.form['codarea1']
            datosCliente['telefono1'] = request.form['telefono1']
            datosCliente['vivienda'] = request.form['vivienda']
            datosCliente['actividad'] = request.form['actividad']
            datosCliente['sexo'] = request.form['sexo']
            datosCliente['fnacim'] = request.form['fnacim']
            datosCliente['email'] = request.form['email']
            datosCliente['obs'] = request.form['obs']
            datosCliente['trabajo'] = request.form['trabajo']
            datosCliente['cargo'] = request.form['cargo']
            datosCliente['domtra1'] = request.form['domtra1']
            datosCliente['domtra2'] = request.form['domtra2']
            datosCliente['loctra'] = request.form['loctra']
            datosCliente['cpostra'] = request.form['cpostra']
            datosCliente['ingresos'] = float(request.form['ingresos'])
            datosCliente['ingresos_o'] = float(request.form['ingresos_o'])
            
            if ((datosCliente['clien'] == '') or (datosCliente['clien'] == None)):
                #datosCliente = json.dumps(datosCliente, indent=4)
                print('datos de cliente')
                print(datosCliente)
                print('--------------------------------')
                datosCliente, error = insert_cliente(datosCliente = datosCliente)
                if error == None:
                    flash(f"Error insertando datos del cliente: {error}", "error")
                else:
                    flash(f"Nuevo cliente grabado", "info")
            else:
                #datosCliente = json.dumps(datosCliente, indent=4)
                datosCliente, error = update_cliente(datosCliente = datosCliente)
                #error = None
                #print(datosCliente)
                if error == None:
                    flash(f"Datos del cliente actualizados", "info")
                else:
                    flash(f"Error actualizando datos del cliente: {error}", "error")
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('cliente'))
    return redirect(url_for('cliente'))


@app.route('/estado_cuenta')
def estado_cuenta():
    if session.get("cliente") != []:
        if eval_menu(session.get('menu'), 'sistema'):
            creditos_otorgados = get_historial_creditos(session['cliente']['CLIEN'])
            return render_template('estadocuenta.html', creditos_otorgados = creditos_otorgados)
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('cliente'))
    else:
        flash("Se debe seleccionar un cliente", category = "error")
        return redirect(url_for('cliente'))


@app.route('/nuevoproducto', methods=["POST", "GET"])
def nuevoproducto():
    if session.get("cliente") != []:
        if eval_menu(session.get('menu'), 'sistema'):
        #if session['cliente']['INHA'] == '0':
            if request.method == "POST":
                items = session.get("items")
                nuevoart = request.form['codart']
                artCant = int(request.form['cantidad'])
                articulo, error = get_articulo(nuevoart)
                artUnitario = float(articulo.get('PREC1'))
                if bool(articulo) and error == None:
                    newItems = {'codigo': articulo.get('CODIGO'), 'detalle': articulo.get('NOMBRE'), 'cantidad': artCant, 'unitario': artUnitario, 'total': (articulo.get('PREC1') * artCant)}
                    items.append(newItems)
                    session["items"] = items
                    return render_template('/itemcred.html', items=session.get("items"))
                else:
                    flash("No se encontró el artículo", "error")
                    return render_template('/itemcred.html', items=session.get("items"))
            else:
                return render_template('/itemcred.html', items=session.get("items"))
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('cliente'))
        #else:
        #    flash("No se puede generar un crédito a un cliente inhabilitado", category = "error")
        #    return redirect(url_for('cliente'))
    else:
        flash("Se debe seleccionar un cliente", category = "error")
        return redirect(url_for('cliente'))
    

@app.route('/nuevocred', methods=["POST", "GET"])
def nuevocred():
    if eval_menu(session.get('menu'), 'sistema'):
        sucursales, error = get_sucursales()
        if error == None:
            return render_template('/nuevocred.html', items=session.get("items"), sucursales=sucursales)
    else:
        flash('No tiene autorización', category='error')
        return redirect(url_for('nuevoproducto'))



@app.route ('/solicitudCred', methods=["POST"])
def solicitudCred():
    if request.method=="POST":
        if eval_menu(session.get('menu'), 'sistema'):
            newItems = {'idcliente': session.get("cliente")["CLIEN"], 'sucursal': request.form['sucursal'], 'idvendedor': request.form['vendedor']}
            print(session.get("items"))
            error = new_credito(cliente_cred=newItems, items_cred=session.get("items"))
            if error == None:
                flash(f"Nuevo crédito grabado", "info")
            else:    
                flash(f"Error insertando datos de la solicitud de crédito: {error.get('error')}", "error")
            session['cliente'] = []
            session['items'] = []
            return redirect(url_for('cliente'))
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('nuevoproducto'))


@app.route('/eliminar/<i>')
def eliminar(i):
    items = session.get("items")
    bandera = False
    indice = 0
    while bandera == False and indice < len(items):
        if (items[indice]["codigo"] == i):
            del items[indice]
            session['items'] = items
            bandera = True
        else:
            indice = indice + 1
    return render_template('/itemcred.html', items=session.get("items"))


@app.route('/solicitudes')
def solicitudes():
    creditos, error = get_creditos(0)
    if error == None:
        return render_template('/solicitudes.html', solicitudes=creditos)

@app.route('/pendientes')
def pendientes():
    creditos, error = get_creditos(1)
    if error == None:
        return render_template('/solicitudes.html', solicitudes=creditos)


@app.route('/datosCredito/<id>/<estado>')
def datosCredito(id: int, estado: int):
    if eval_menu(session.get('menu'), 'sistema'):
        cliente, error = get_credito_pendiente(id, estado)
        creditos_otorgados = get_creditos_otorgados(id)
        if error == None:
            items, error_items = get_itemscred(id)
            if error_items == None:
                return render_template('/datosCred.html', cliente=cliente, items = items, creditos_otorgados = creditos_otorgados)
            else:
                flash(f'Error consultado items de crédito: {error_items}', 'error')
            return redirect(url_for('solicitudes'))
        else:
            flash(f'Error consultado crédito: {error}', 'error')
            return redirect(url_for('solicitudes'))
    else:
        flash('No tiene autorización', category='error')
        return redirect(url_for('usuario'))


@app.route('/estadocuenta')
def estadoCuenta():
    return render_template('/estadocuenta.html')


@app.route('/documentacion')
def documentacion():
    if eval_menu(session.get('menu'), 'sistema'):
        return render_template('/documentacion.html')
    else:
        flash('No tiene autorización', category='error')
        return redirect(url_for('cliente'))


@app.route('/user', methods=['POST', 'GET'], defaults={"iduser": 0})
@app.route('/user/<iduser>', methods=['POST', 'GET'])
def user(iduser):
    if "usuario" in session:
        if eval_menu(session.get('menu'), 'sistema'):
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
                        return render_template('/usuario_alt_baj.html',tipodocs=tipodocs, localidades=localidades, categorias=categorias, sucursales=sucursales, provincias=provincias)
                    else:
                        flash('Usuario no encontrado', category='error')
                        return redirect(url_for('user'))
                else:
                    iduser = 0
                    session['user'] = []
                    return render_template('/usuario_alt_baj.html',tipodocs=tipodocs, localidades=localidades, categorias=categorias, sucursales=sucursales, provincias=provincias)
            else:
                return redirect(url_for('user'))
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('usuario'))
    else:
        return redirect(url_for("login"))


@app.route('/grabarUsuario', methods=["POST"])
def grabarUsuario():
    if request.method == "POST":
        if eval_menu(session.get('menu'), 'sistema'):
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
                return redirect(url_for('user'))
            else:
                error = update_user(datosUser, datosUser.get('usuario'))
                if error == None:
                    flash('Se actualizó el usuario', category='info')
                return redirect(url_for('user'))
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('user'))


@app.route('/deleteUser')
def deleteUser():
    user = dict(session.get("user"))
    uID = user.get('USUARIO')
    if uID != None:
        if eval_menu(session.get('menu'), 'sistema'):
            error = drop_user(uID)
            if error == None:
                flash('Se inhabilitó el usuario', category='info')
                return redirect(url_for('user'))
            else:
                flash('Error al inhabilitar el usuario', category='error')
                return redirect(url_for('user'))
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('user'))
    else:
        flash('Se debe seleccionar un usuario', category='error')
        return redirect(url_for('user'))


@app.route('/nuevo_perfil/<op>')
def nuevo_perfil(op):
    if "usuario" in session:
        if eval_menu(session.get('menu'), 'sistema'):
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
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('usuario'))
    else:
        return redirect(url_for("login"))


@app.route('/nuevo_perfil/select_usr', methods=["POST", "GET"])
def select_usr():
    if request.method == "POST":
        usr = request.form['usuario']
        usuarios, error = get_all_user()
        us_per, error = get_rol(usr)
        if error == None:
            return render_template('nuevo_perfil.html', op='2', usuarios=usuarios, usr=usr, us_per=us_per)


@app.route('/nuevo_perfil/eliminar_perfil', methods=["POST", "GET"])
def eliminar_perfil():
    if request.method == "POST":
        if eval_menu(session.get('menu'), 'sistema'):
            perfil = request.form['ide']
            error = delete_perfil(perfil)
            perfiles, error = get_all_perfil()
            if error == None:
                flash('Se eliminó el perfil', category='info')
                return render_template('nuevo_perfil.html', op='1', perfiles=perfiles)
            else:
                flash('No se pudo eliminar el perfil', category='error')
                return render_template('nuevo_perfil.html', op='1', perfiles=perfiles)
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('nuevo_perfil', op='1'))


@app.route('/nuevo_perfil/eliminar_menu', methods=["POST", "GET"])
def eliminar_menu():
    if request.method == "POST":
        if eval_menu(session.get('menu'), 'sistema'):
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
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('nuevo_perfil', op='3'))


@app.route('/nuevo_perfil/mod_perfil', methods=["POST", "GET"])
def mod_perfil():
    if request.method == "POST":
        op = request.form['option']
        usuarios, error = get_all_user()
        if eval_menu(session.get('menu'), 'sistema'):
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
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('nuevo_perfil', op=op))


@app.route('/dias_3', methods=["POST", "GET"])
def dias_3():
    if eval_menu(session.get('menu'), 'sistema'):
        mensaje, error = get_mensaje(3)
        fecha_futura = datetime.now() + timedelta(days=3)
        creditosAvencer, error = get_creditos_a_vencer(fecha_futura)
        for credito in creditosAvencer:
            if credito['TELEFONO_CELULAR'] != None and credito['APENOM'] != None:
                info_msj = {}
                info_msj['tipo'] = 1
                '''invento para saber si se le envia whatsapp o sms
                if credito['METHOD'] == 'wts': 
                    info_msj['tipo'] = 1
                else:
                    info_msj['tipo'] = 0
                '''
                info_msj['idvencim'] = credito['IDVENCIM']
                info_msj['fecha'] = datetime.now().strftime('%Y/%m/%d')
                info_msj['sucursal'] = '0000'
                info_msj['clien'] = credito['CLIEN']
                info_msj['tel'] =  str(credito['TELEFONO_CELULAR'])
                msj = str(mensaje['DETALLE']).replace('%apellido+nombre%', str(credito['APENOM']).strip()).replace('%vto%', str(credito['VTO'].strftime('%d/%m/%Y')))
                if re.match(expresion_regular, info_msj.get('tel')):
                    info_msj['mensaje'] = 'Aviso de vencimiento de cuota, 3 días antes del vencimiento'
                    guardar_mensaje(info_msj, msj)
                elif info_msj.get('tel') == '':
                    info_msj['mensaje'] = 'Cliente sin número de teléfono'
                    registrar_mensajes(info_msj)
                else:
                    info_msj['mensaje'] = 'Número de teléfono mal formado'
                    registrar_mensajes(info_msj)
                '''
                data, error = get_numbers(credito['CLIEN'])
                if error == None:
                    for clave, valor in data[0].items():
                        num = valor.replace(' ', '')
                        if num != '':
                            if re.match(expresion_regular, num):
                                info_msj['mensaje'] = 'Aviso de vencimiento de cuota, 3 días antes del vencimiento'
                                info_msj['tel'] = num
                                guardar_mensaje(info_msj, msj)
                '''
        if error == None:
            return render_template('aviso_3dias.html', creditosAvencer=creditosAvencer, mensaje=mensaje)
    else:
        flash('No tiene autorización', category='error')
        return redirect(url_for('usuario'))


@app.route('/select_atraso/<op>')
def select_atraso(op):
    op = int(op)
    #sucursales, error = get_sucursales()
    if op == 1:
        return render_template('aviso_atrasado.html', opv=op)
    else:
        return render_template('aviso_atrasado.html', opv=op)


@app.route('/get_atraso', methods=["POST", "GET"])
def get_atraso():
    if request.method == 'POST':
        op = request.form['infoSel']
        #sucursal = request.form['sucursal']
        opv = int(request.form['opv'])
        bandera = False
        #sucursales, error = get_sucursales()
        #evaluar_numeros_secundarios = True if 'eval' in request.form else False
        if eval_menu(session.get('menu'), 'sistema'):
            if op == '':
                return render_template('aviso_atrasado.html', opv=opv, op=op)
            else:
                fecha_pasada = datetime.now() + timedelta(days=-int(op))
                creditos_una_cta_venc, error = get_creditos_una_cta_venc(fecha_pasada)
                if error == None:
                    tot = 0.0
                    if creditos_una_cta_venc != []:
                        bandera = True
                        for cred in creditos_una_cta_venc:
                            tot += float(cred['DEUDA_VENCIDA'])
                    long = len(creditos_una_cta_venc)
                    return render_template('aviso_atrasado.html', opv=opv, op=op, creditosVencidos=creditos_una_cta_venc, bandera=bandera, long=long, tot=tot)
        else:
            flash('No tiene autorización', category='error')
            return redirect(url_for('index'))


@app.route('/enviar_msj', methods=["POST", "GET"])
def enviar_msj():
    if request.method == 'POST':
        op = request.form['op']
        opv = int(request.form['opv'])
        #evaluar_numeros_secundarios = request.form['evaluar_numeros_secundarios']
        #sucursal = request.form['sucursal']
        mensaje, error = get_mensaje(-int(op))
        fecha_pasada = datetime.now() + timedelta(days=-int(op))
        creditos_una_cta_venc, error = get_creditos_una_cta_venc(fecha_pasada)
        if error == None:
            if creditos_una_cta_venc != []:
                crear_mensajes(creditos_una_cta_venc, mensaje, int(op))
                flash('Mensajes enviados', category='success')
                return render_template('aviso_atrasado.html', opv=opv)


@app.route('/dat_credixsa')
def dat_credixsa():
    totalDeuda = 0.0
    #nombre = session.get('cliente')['APELLIDO'] + ' ' + session.get('cliente')['NOMBRE']
    #dni = session.get('cliente')['DNI']
    nombre = 'SAAD YAMIL EZEQUIEL'
    dni = '34846201'
    data = consultar(nombre, dni)
    #data = {}
    totalDeuda = float(data.get('monto_adeudado_situaciones_1_vigentes')) + float(data.get('monto_adeudado_situaciones_2_vigentes')) + float(data.get('monto_adeudado_situaciones_3_vigentes')) + \
        float(data.get('monto_adeudado_situaciones_4_vigentes')) + float(data.get('monto_adeudado_situaciones_5_vigentes')) + float(data.get('monto_adeudado_situaciones_6_vigentes'))
    return render_template('datos_cre.html', data = data, totalDeuda = totalDeuda)


@app.route('/reg_mensajes')
def reg_mensajes():
    update_mensajes()
    msj_enviados = get_mensajes_WTS('+5492645139411', 1)
    msj_recibidos = get_mensajes_WTS('+5492645139411', 2)
    return render_template('reg_mensajes.html', msj_enviados = msj_enviados, msj_recibidos = msj_recibidos)


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return 'ok'


def pagina_no_encontrada(error):
    data = {
        'titulo': 'página no encontrada'
    }
    return render_template('404.html', data=data), 404
    # return redirect(url_for('index'))












# @app.route('/webhook', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         data = request.form
#         # message_body = data.get('Body', '')
#         number_from = data.get('From', '').split(':')
#         mensajes_enviados = get_mensajes_WTS(number_from[1], 1)
#         mensajes_recibidos = get_mensajes_WTS(number_from[1], 0)
#         men = mensajes_recibidos + mensajes_enviados
#         max_datetime = datetime.max.replace(tzinfo=pytz.UTC)
#         mensss = sorted(men, key=lambda x: x['date_sent'] if x['date_sent'] is not None else max_datetime)
#         print(mensss)
#         # print(message_body)
#         # print(data)
#         cli, error = get_cli_con_num(number_from[1])
#         if error == None:
#             flash(f'nuevo mensaje',category='info')
#             return render_template('chat.html')


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # Validar la firma de la solicitud
#     validator = RequestValidator('ad1ef7bf371bbc92f7fad8ac2b9b4b96')
#     if validator.validate(request.url, request.form, request.headers.get('X-Twilio-Signature', '')):
#         # La solicitud es válida, procesar el evento
#         data = request.form
#         event_type = data.get('EventType', '')

#         # Procesar el evento según sea necesario
#         if event_type == 'onMessageAdded':
#             message_body = data.get('Body', '')
#             conversation_sid = data.get('ConversationSid', '')
#             source = data.get('Source', '')

#             # Verificar si el mensaje proviene de WhatsApp
#             if source == 'whatsapp':
#                 # Procesar el mensaje de WhatsApp
#                 print(f"Mensaje de WhatsApp recibido en la conversación {conversation_sid}: {message_body}")

#                 # Puedes realizar acciones específicas para mensajes de WhatsApp aquí

#         return redirect(url_for('index'))
#     else:
#         # La solicitud no es válida
#         return redirect(url_for('index'))







opciones = {
    'inicio': {
        'mensaje': '¡Bienvenido! ¿Qué opción te gustaría elegir?\n'
               '1. Opción 1\n'
               '2. Opción 2\n'
               '3. Salir',
        'opciones': ['opción 1', 'opción 2', 'salir'],
    },
    'opción 1': {
        'mensaje': 'Has elegido la opción 1. ¿Quieres hacer algo más?',
        'opciones': ['opción 1.1', 'opción 1.2', 'volver'],
    },
    'opción 1.1': {
        'mensaje': 'Has elegido la subopción 1.1. ¿Quieres hacer algo más?',
        'opciones': ['volver'],
    },
    'opción 1.2': {
        'mensaje': 'Has elegido la subopción 1.2. ¿Quieres hacer algo más?',
        'opciones': ['volver'],
    },
    'opción 2': {
        'mensaje': 'Has elegido la opción 2. ¿Quieres hacer algo más?',
        'opciones': ['volver'],
    },
    'salir': {
        'mensaje': 'Gracias por usar nuestro servicio. ¡Hasta luego!',
        'opciones': [],
    },
    'volver': {
        'mensaje': 'Volviendo al menú anterior. ¿Qué opción te gustaría elegir?',
        'opciones': ['opción 1', 'opción 2', 'salir'],
    }
}
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.form
        message_body = data.get('Body', '')
        number_from = data.get('From', '')
        response = MessagingResponse()
        if number_from not in session:
            session[number_from] = 'inicio'
            response.message(opciones[session[number_from]]['mensaje'])
        current_option = session[number_from]
        if message_body.lower() == 'salir':
            del session[number_from]
            response.message(opciones[message_body.lower()]['mensaje'])
        if message_body.lower() == 'volver':
            response.message(opciones[message_body.lower()]['mensaje'])
            session[number_from] = message_body.lower()
        else:
            if message_body.lower() in opciones[current_option]['opciones']:
                current_option = message_body.lower()
                session[number_from] = current_option
                if current_option == 'opción 1':
                    resultado = metodo_opcion1()
                    response.message(resultado)
                    response.message(opciones[current_option]['mensaje'])
        return str(response)



        # mensajes_enviados = get_mensajes_WTS(number_from[1], 1)
        # mensajes_recibidos = get_mensajes_WTS(number_from[1], 0)
        # men = mensajes_recibidos + mensajes_enviados
        # max_datetime = datetime.max.replace(tzinfo=pytz.UTC)
        # mensss = sorted(men, key=lambda x: x['date_sent'] if x['date_sent'] is not None else max_datetime)
        # cli, error = get_cli_con_num(number_from[1])
        # if message_body.lower() == 'salir':
        #     del session[number_from]
        # else:
        #     if message_body.lower() in opciones[current_option]['opciones']:
        #         current_option = message_body.lower()
        # response.message(opciones[current_option]['mensaje'])
        # session[number_from] = current_option
        # return str(response)






@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    dni = request.form.get('dni')
    cliente, error = get_cliente(dni)
    if error:
        resultado_html = f"<p>{error.get('error')}" + "</p>"
        return jsonify({'resultado': resultado_html})
    else:
        resultado_html = "<p>Apellido: " + cliente.get('APELLIDO') + "</p>" + "<p>Nombre: " + cliente.get('NOMBRE') + "</p>"
        return jsonify({'resultado': resultado_html})










@app.route('/ejemplo_list_excel')
def ejemplo_list_excel():
    listaD = [
        {"DNI": "12345678", "Apellido": "Gomez", "Domicilio": "Calle 123", "Telefono": "555-1234"},
        {"DNI": "87654321", "Apellido": "Perez", "Domicilio": "Avenida 456", "Telefono": "555-5678"},
        {"DNI": "87654321", "Apellido": "Ramírez", "Domicilio": "Calle 567", "Telefono": "555-8765"},
        {"DNI": "23456789", "Apellido": "González", "Domicilio": "Avenida 654", "Telefono": "555-2345"},
        {"DNI": "34567890", "Apellido": "López", "Domicilio": "Calle 456", "Telefono": "555-3456"},
        {"DNI": "54321678", "Apellido": "Rodríguez", "Domicilio": "Avenida 987", "Telefono": "555-5432"},
        {"DNI": "98765432", "Apellido": "Martínez", "Domicilio": "Calle 789", "Telefono": "555-9876"}
    ]
    return render_template('ejemplo_list_excel.html', listaD=listaD)

@app.route('/procesar_exc', methods=['POST'])
def procesar_exc():
    listaD = [json.loads(perfil) for perfil in request.form.getlist('listaD[]')]
    seleccionados = [json.loads(select) for select in request.form.getlist('seleccionados[]')]
    elementos_no_seleccionados = [elem for elem in listaD if elem not in seleccionados]

    # print(listaD)
    # print(seleccionados)
    print(elementos_no_seleccionados)
    # generar_credixsa(elementos_no_seleccionados)
    flash('Datos recibidos y procesados', category='info')
    return render_template('ejemplo_list_excel.html', listaD=listaD)



if __name__ == '__main__':
    # esto enlaza la ruta (1er parametro), con las funcion (2do parametro)
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    init_app(app)
    app.run(debug=True, port=5000)
