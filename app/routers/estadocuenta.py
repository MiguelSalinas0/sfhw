from flask import render_template
from app.api.api_usuario import *
from app.api.api_credixsa import *

from app import bp
from app.decorators import login_required, permission_required


@bp.route('/estadocuenta')
# @permission_required('sistema')
@login_required
def estadoCuenta():
    return render_template('/estadocuenta.html')


@bp.route('/documentacion')
# @permission_required('sistema')
@login_required
def documentacion():
    return render_template('/documentacion.html')


@bp.route('/dat_credixsa')
# @permission_required('sistema')
@login_required
def dat_credixsa():
    totalDeuda = 0.0
    # nombre = session.get('cliente')['APELLIDO'] + ' ' + session.get('cliente')['NOMBRE']
    # dni = session.get('cliente')['DNI']
    nombre = 'SAAD YAMIL EZEQUIEL'
    dni = '34846201'
    data = consultar(nombre, dni)
    # data = {}
    totalDeuda = float(data.get('monto_adeudado_situaciones_1_vigentes')) + float(data.get('monto_adeudado_situaciones_2_vigentes')) + float(data.get('monto_adeudado_situaciones_3_vigentes')) + \
        float(data.get('monto_adeudado_situaciones_4_vigentes')) + float(data.get(
            'monto_adeudado_situaciones_5_vigentes')) + float(data.get('monto_adeudado_situaciones_6_vigentes'))
    return render_template('datos_cre.html', data=data, totalDeuda=totalDeuda)
