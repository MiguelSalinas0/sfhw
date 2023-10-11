from flask import render_template, url_for, request, redirect, session, flash
from app.api.api_cliente import *
from app.api.api_credito import *
from app.api.api_usuario import *

from app import bp
from app.decorators import login_required, permission_required


@bp.route('/nuevoproducto', methods=["POST", "GET"])
@permission_required('sistema')
@login_required
def nuevoproducto():
    if session.get("cliente") != []:
        # if session['cliente']['INHA'] == '0':
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
        # else:
        #    flash("No se puede generar un crédito a un cliente inhabilitado", category = "error")
        #    return redirect(url_for('bp.cliente'))
    else:
        flash("Se debe seleccionar un cliente", category="error")
        return redirect(url_for('bp.cliente'))


@bp.route('/nuevocred', methods=["POST", "GET"])
@permission_required('sistema')
@login_required
def nuevocred():
    sucursales, error = get_sucursales()
    if error == None:
        return render_template('/nuevocred.html', items=session.get("items"), sucursales=sucursales)


@bp.route('/solicitudCred', methods=["POST"])
@permission_required('sistema')
@login_required
def solicitudCred():
    if request.method == "POST":
        newItems = {'idcliente': session.get("cliente")["CLIEN"], 'sucursal': request.form['sucursal'], 'idvendedor': request.form['vendedor']}
        print(session.get("items"))
        error = new_credito(cliente_cred=newItems, items_cred=session.get("items"))
        if error == None:
            flash(f"Nuevo crédito grabado", "info")
        else:
            flash(f"Error insertando datos de la solicitud de crédito: {error.get('error')}", "error")
        session['cliente'] = []
        session['items'] = []
        return redirect(url_for('bp.cliente'))


@bp.route('/eliminar/<i>')
@permission_required('sistema')
@login_required
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


@bp.route('/solicitudes')
@permission_required('sistema')
@login_required
def solicitudes():
    creditos, error = get_creditos(0)
    if error == None:
        return render_template('/solicitudes.html', solicitudes=creditos)


@bp.route('/pendientes')
@permission_required('sistema')
@login_required
def pendientes():
    creditos, error = get_creditos(1)
    if error == None:
        return render_template('/solicitudes.html', solicitudes=creditos)


@bp.route('/datosCredito/<id>/<estado>')
@permission_required('sistema')
@login_required
def datosCredito(id: int, estado: int):
    cliente, error = get_credito_pendiente(id, estado)
    creditos_otorgados = get_creditos_otorgados(id)
    if error == None:
        items, error_items = get_itemscred(id)
        if error_items == None:
            return render_template('/datosCred.html', cliente=cliente, items=items, creditos_otorgados=creditos_otorgados)
        else:
            flash(f'Error consultado items de crédito: {error_items}', 'error')
        return redirect(url_for('bp.solicitudes'))
    else:
        flash(f'Error consultado crédito: {error}', 'error')
        return redirect(url_for('bp.solicitudes'))
