import requests
import json
from flask import (Flask, render_template, url_for, request, redirect, session, flash)
from datetime import timedelta
from api.api_cliente import *

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
            'titulo': 'el título'
        }
        return render_template('index.html', data=data)
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.path == '/login':
            print('se envuentra en la ruta cliente')
    if request.method == 'POST':
        usuario = request.form['usuario']
        # session.permanent = True
        clave = request.form['clave']
        session["urlWS"] = 'http://localhost:8080/datasnap/rest/TSFHWebSvr/'
        url = session['urlWS'] + 'usuario' + '/' + usuario + '/' + clave
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datosUsr = respuesta.json()
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


@app.route('/logout.html')
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
        tipocontribs, error = get_tipocontribuciones()
        estadosciviles, error = get_estadocivil()
        localidades, error = get_localidades()
        if error == None:
            if request.method == 'POST':
                print('1')
                idclien = request.form['buscar']
                cliente, errorC = get_cliente(idclien)
                if errorC == None:
                    session["cliente"] = cliente
                    return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, categorias=categorias)
            else:
                print('2')
                cliente = 0
                session['cliente'] = []
                session['items'] = []
                return render_template('cliente.html', tipodocs=tipodocs, tipocontribs=tipocontribs, estadosciviles=estadosciviles, localidades=localidades, categorias=categorias)
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
            respuesta = requests.post(url, json=datosCliente, headers=newHeaders)
            if respuesta.status_code == 201:
                flash(f"Nuevo cliente grabado", "info")
            else:
                flash(f"Error insertando datos del cliente: {respuesta.status_code}", "error")
        else:
            datosCliente = json.dumps(datosCliente, indent=4)
            respuesta = requests.put(url, json=datosCliente, headers=newHeaders)
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
            if bool(articulo) and error == None:
                newItems = {'codigo': articulo.get('codigo'), 'detalle': articulo.get('nombre'), 'cantidad': artCant, 'unitario': articulo.get('prec1'), 'total': (articulo.get('prec1') * artCant)}
                items.append(newItems)
                session["items"] = items
                return render_template('/itemcred.html', items=session.get("items"))
            else:
                flash("No se encontró el artículo")
                return render_template('/itemcred.html', items=session.get("items"))
        else:
            return render_template('/itemcred.html', items=session.get("items"))
    else:
        flash("Se debe seleccionar un cliente", category = "error")
        return redirect(url_for('cliente'))
    

@app.route('/nuevocred', methods=["POST", "GET"])
def nuevocred():
    print('nuevo credito')
    sucursales, error = get_sucursales()
    if error == None:
        return render_template('/nuevocred.html', items=session.get("items"), sucursales=sucursales)


@app.route ('/solicitudCred', methods=["POST"])
def solicitudCred():
    if request.method=="POST":
        cred = {}
        Dcliente = []
        newItems = {'idcliente': session.get("cliente")["CLIEN"], 'sucursal': request.form['sucursal']}
        Dcliente.append(newItems)
        cred["cliente"] = Dcliente
        cred["items_cred"] = session.get("items")
        cred = json.dumps(cred, indent=4)
        print(cred)
        url = session['urlWS'] + 'solcred'
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        respuesta = requests.put(url, json=cred, headers=newHeaders)
        if respuesta.status_code == 201:
            flash(f"Nuevo crédito grabado", "info")
        else:    
            flash(f"Error insertando datos de la solicitud de crédito: {respuesta.status_code}", "error")
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


@app.route('/estadocuenta')
def estadoCuenta():
    return render_template('/estadocuenta.html')


@app.route('/documentacion')
def documentacion():
    return render_template('/documentacion.html')


@app.route('/estsolicitud')
def estSolicitud():
    return render_template('/estsolicitud.html')


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
    app.run(debug=True, port=5000)
