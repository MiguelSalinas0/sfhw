import requests
import json
from flask import (Flask, render_template, url_for, request, redirect, session, flash)
from datetime import timedelta
from api.api_cliente import *
from api.api_credito import new_credito, get_credito, get_itemscred
from api.api_usuario import get_usuario
from db.db import get_db, init_app


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
                    session["items"] = []
                    session["cliente"] = []
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
                if cliente != None:
                    session["cliente"] = cliente
                    return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, viviendas=viviendas, actividades=actividades, categorias=categorias)
                """
                if errorC == None:
                    session["cliente"] = cliente
                    return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, viviendas=viviendas, actividades=actividades, categorias=categorias)
                """    
            else:
                cliente = 0
                session['cliente'] = []
                session['items'] = []
                return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, viviendas=viviendas, actividades=actividades, categorias=categorias)
        else:
            return redirect(url_for('cliente'))
    else:
        return redirect(url_for("login"))


@app.route('/grabarCliente', methods=["POST"])
def grabarCliente():
    if request.method == "POST":
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
        datosCliente['codloc'] = request.form['codloc']
        datosCliente['estadociv'] = request.form['estadociv']
        datosCliente['email'] = request.form['email']
        datosCliente['codarea'] = request.form['codarea']
        datosCliente['telefono'] = request.form['telefono']
        datosCliente['codarea1'] = request.form['codarea1']
        datosCliente['telefono1'] = request.form['telefono1']
        datosCliente['sexo'] = request.form['sexo']
        datosCliente['fnacim'] = request.form['fnacim']
        datosCliente['email'] = request.form['email']
        datosCliente['obs'] = request.form['obs']
        url = session['urlWS']
        url = url + 'cliente'
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        if ((datosCliente['clien'] == '') or (datosCliente['clien'] == None)):
            datosCliente = json.dumps(datosCliente, indent=4)
            respuesta = requests.put(url, data=datosCliente, headers=newHeaders)
            if respuesta.status_code == 201:
                flash(f"Nuevo cliente grabado", "info")
            else:
                flash(f"Error insertando datos del cliente: {respuesta.status_code}", "error")
        else:
            datosCliente = json.dumps(datosCliente, indent=4)
            respuesta = requests.put(url, data=datosCliente, headers=newHeaders)
            if respuesta.status_code == 201:
                flash(f"Datos del cliente actualizados", "info")
            else:
                flash(f"Error actualizando datos del cliente: {respuesta.status_code}", "error")
    return redirect(url_for('cliente'))


@app.route('/nuevoproducto', methods=["POST", "GET"])
def nuevoproducto():
    if session.get("cliente") != []:
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
        flash("Se debe seleccionar un cliente", category = "error")
        return redirect(url_for('cliente'))
    

@app.route('/nuevocred', methods=["POST", "GET"])
def nuevocred():
    sucursales, error = get_sucursales()
    if error == None:
        return render_template('/nuevocred.html', items=session.get("items"), sucursales=sucursales)


@app.route ('/solicitudCred', methods=["POST"])
def solicitudCred():
    if request.method=="POST":
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


@app.route('/datosCredito/<id>')
def datos(id):
    cliente, error = get_credito(id)
    if error == None:
        items, error_items = get_itemscred(id)
        if error_items == None:
            return render_template('/datosCred.html', cliente=cliente, items = items)
        else:
            flash(f'Error consultado items de crédito: {error_items}', 'error')
        return redirect(url_for('solicitudes'))
    else:
        flash(f'Error consultado crédito: {error}', 'error')
        return redirect(url_for('solicitudes'))

@app.route('/estadocuenta')
def estadoCuenta():
    return render_template('/estadocuenta.html')


@app.route('/documentacion')
def documentacion():
    return render_template('/documentacion.html')


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


if __name__ == '__main__':
    # esto enlaza la ruta (1er parametro), con las funcion (2do parametro)
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    init_app(app)
    app.run(debug=True, port=5000)
