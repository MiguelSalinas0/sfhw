from datetime import timedelta
from flask import redirect, render_template, request, flash, url_for
from app import bp
from app.api.api_cliente import get_categorias
from app.api.api_credito import obtener_clientes_a_informar
from app.api.api_excel import *
from app.decorators import login_required, permission_required

import json


@bp.route('/list_excel')
# @permission_required('sistema')
@login_required
def list_excel():
    categorias, error = get_categorias()
    if error == None:
        return render_template('list_excel.html', categorias=categorias, bandera=False)


@bp.route('/filtrar_reg', methods=['POST'])
# @permission_required('sistema')
@login_required
def filtrar_reg():
    categorias, error = get_categorias()
    fecha_actual = datetime.datetime.now()
    ultimo_pago = fecha_actual - timedelta(days=90)
    date_desde = request.form['date_desde']
    date_hasta = datetime.datetime.strptime(request.form['date_hasta'], '%Y-%m-%d')
    if date_desde == '':
        date_desde = fecha_actual - timedelta(days=4 * 365)
    else:
        date_desde = datetime.datetime.strptime(date_desde, '%Y-%m-%d')
    categorias_seleccionadas = [cat.strip() for cat in request.form.getlist('cate_checkbox')]
    registros, error = obtener_clientes_a_informar(ultimo_pago, date_desde, date_hasta, categorias_seleccionadas)
    bandera = True if len(registros) > 0 else False
    if error == None:
        return render_template('list_excel.html', listaD=registros, categorias=categorias, bander = bandera)
    else:
        flash(f'Ocurrio algún error {error}', category='error')
        return redirect(url_for('bp.list_excel'))


@bp.route('/procesar_exc', methods=['POST'])
# @permission_required('sistema')
@login_required
def procesar_exc():
    if request.method == 'POST':
        categorias, error = get_categorias()
        listaD = [json.loads(perfil) for perfil in request.form.getlist('listaD[]')]
        if request.form['submitButton'] == 'Generar Informe Credixsa':
            generar_credixsa(listaD)
        if request.form['submitButton'] == 'Generar Informe Veraz':
            generar_veraz(listaD)
        if request.form['submitButton'] == 'Generar Informe Codesa':
            generar_codesa(listaD)
        flash('Datos recibidos y procesados', category='info')
    return render_template('list_excel.html', listaD=listaD, categorias=categorias)


# @bp.route('/procesar_formulario', methods=['POST'])
# # @permission_required('sistema')
# @login_required
# def procesar_formulario():
#     dni = request.form.get('dni')
#     cliente, error = get_cliente(dni)
#     if error:
#         resultado_html = f"<p>{error.get('error')}" + "</p>"
#         return jsonify({'resultado': resultado_html})
#     else:
#         resultado_html = "<p>Apellido: " + cliente.get('APELLIDO') + "</p>" + "<p>Nombre: " + cliente.get('NOMBRE') + "</p>"
#         return jsonify({'resultado': resultado_html})