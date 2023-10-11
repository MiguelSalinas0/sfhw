from flask import jsonify, render_template, request, flash
from app import bp
from app.api.api_cliente import get_cliente
from app.api.api_excel import *
from app.decorators import login_required, permission_required

import json


@bp.route('/ejemplo_list_excel')
@permission_required('sistema')
@login_required
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


@bp.route('/procesar_exc', methods=['POST'])
@permission_required('sistema')
@login_required
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









@bp.route('/procesar_formulario', methods=['POST'])
@permission_required('sistema')
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