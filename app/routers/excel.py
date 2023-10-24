from flask import jsonify, render_template, request, flash
from app import bp
from app.api.api_cliente import get_categorias, get_cliente
from app.api.api_credito import get_creditos_atrasados_dias
from app.api.api_excel import *
from app.decorators import login_required, permission_required

import json


@bp.route('/ejemplo_list_excel')
# @permission_required('sistema')
@login_required
def ejemplo_list_excel():
    categorias, error = get_categorias()
    if error == None:
        return render_template('ejemplo_list_excel.html', categorias=categorias)


@bp.route('/filtrar_reg', methods=['POST'])
# @permission_required('sistema')
@login_required
def filtrar_reg():
    dias_desde = int(request.form['dias_desde'])
    dias_hasta = int(request.form['dias_hasta'])
    categorias_seleccionadas = [cat.strip() for cat in request.form.getlist('cate_checkbox')]
    registros, error = get_creditos_atrasados_dias(dias_desde, dias_hasta)
    registros_filtrados = []
    categorias, error = get_categorias()
    if error == None:
        if categorias_seleccionadas != []:
            for reg in registros:
                if reg.get('CATEGORIA').strip() in categorias_seleccionadas:
                    registros_filtrados.append(reg)
            return render_template('ejemplo_list_excel.html', listaD=registros_filtrados, categorias=categorias)
        else:
            return render_template('ejemplo_list_excel.html', listaD=registros, categorias=categorias)


@bp.route('/procesar_exc', methods=['POST'])
# @permission_required('sistema')
@login_required
def procesar_exc():
    listaD = [json.loads(perfil) for perfil in request.form.getlist('listaD[]')]
    seleccionados = [json.loads(select) for select in request.form.getlist('seleccionados[]')]
    elementos_no_seleccionados = [elem for elem in listaD if elem not in seleccionados]

    print(elementos_no_seleccionados)
    # generar_credixsa(elementos_no_seleccionados)
    flash('Datos recibidos y procesados', category='info')
    return render_template('ejemplo_list_excel.html', listaD=listaD)









@bp.route('/procesar_formulario', methods=['POST'])
# @permission_required('sistema')
@login_required
def procesar_formulario():
    dni = request.form.get('dni')
    cliente, error = get_cliente(dni)
    if error:
        resultado_html = f"<p>{error.get('error')}" + "</p>"
        return jsonify({'resultado': resultado_html})
    else:
        resultado_html = "<p>Apellido: " + cliente.get('APELLIDO') + "</p>" + "<p>Nombre: " + cliente.get('NOMBRE') + "</p>"
        return jsonify({'resultado': resultado_html})