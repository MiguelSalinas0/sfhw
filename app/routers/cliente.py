from flask import render_template, url_for, request, redirect, session, flash
from app.api.api_credito import *
from app.api.api_usuario import *
from app.api.api_cliente import *

from app import bp
from app.decorators import login_required, permission_required


@bp.route('/cliente', methods=['POST', 'GET'], defaults={"idclien": 0})
@bp.route('/cliente/<idclien>', methods=['POST', 'GET'])
@permission_required('sistema')
@login_required
def cliente(idclien):
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
        return redirect(url_for('bp.cliente'))


@bp.route('/grabarCliente', methods=["POST"])
@permission_required('sistema')
@login_required
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
            # datosCliente = json.dumps(datosCliente, indent=4)
            print('datos de cliente')
            print(datosCliente)
            print('--------------------------------')
            datosCliente, error = insert_cliente(datosCliente=datosCliente)
            if error == None:
                flash(f"Error insertando datos del cliente: {error}", "error")
            else:
                flash(f"Nuevo cliente grabado", "info")
        else:
            # datosCliente = json.dumps(datosCliente, indent=4)
            datosCliente, error = update_cliente(datosCliente=datosCliente)
            # error = None
            # print(datosCliente)
            if error == None:
                flash(f"Datos del cliente actualizados", "info")
            else:
                flash(f"Error actualizando datos del cliente: {error}", "error")
    return redirect(url_for('bp.cliente'))


@bp.route('/estado_cuenta')
@permission_required('sistema')
@login_required
def estado_cuenta():
    if session.get("cliente") != []:
        creditos_otorgados = get_historial_creditos(session['cliente']['CLIEN'])
        return render_template('estadocuenta.html', creditos_otorgados=creditos_otorgados)
    else:
        flash("Se debe seleccionar un cliente", category="error")
        return redirect(url_for('bp.cliente'))
