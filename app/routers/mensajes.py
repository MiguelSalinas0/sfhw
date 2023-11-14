from flask import jsonify, redirect, render_template, request, flash, url_for
import pytz
from app import bp
from app.api.api_cliente import *
from app.api.api_credito import *
from app.api.api_mensajes import *

from twilio.twiml.messaging_response import MessagingResponse

from app.decorators import login_required, permission_required

from PyQt6.QtWidgets import QApplication


@bp.route('/dias_3', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def dias_3():
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
            info_msj['tel'] = str(credito['TELEFONO_CELULAR'])
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


@bp.route('/select_atraso/<op>')
# @permission_required('sistema')
@login_required
def select_atraso(op):
    op = int(op)
    # sucursales, error = get_sucursales()
    return render_template('aviso_atrasado.html', opv=op)


@bp.route('/get_atraso', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def get_atraso():
    if request.method == 'POST':
        op = request.form['infoSel']
        # sucursal = request.form['sucursal']
        opv = int(request.form['opv'])
        bandera = False
        # sucursales, error = get_sucursales()
        # evaluar_numeros_secundarios = True if 'eval' in request.form else False
        if op == '':
            return render_template('aviso_atrasado.html', opv=opv, op=op)
        else:
            fecha_pasada = datetime.now() + timedelta(days=-int(op))
            creditos_una_cta_venc, error = get_creditos_una_cta_venc(
                fecha_pasada)
            if error == None:
                tot = 0.0
                if creditos_una_cta_venc != []:
                    bandera = True
                    for cred in creditos_una_cta_venc:
                        tot += float(cred['DEUDA_VENCIDA'])
                long = len(creditos_una_cta_venc)
                return render_template('aviso_atrasado.html', opv=opv, op=op, creditosVencidos=creditos_una_cta_venc, bandera=bandera, long=long, tot=tot)


@bp.route('/enviar_msj', methods=["POST", "GET"])
# @permission_required('sistema')
@login_required
def enviar_msj():
    if request.method == 'POST':
        op = request.form['op']
        opv = int(request.form['opv'])
        # evaluar_numeros_secundarios = request.form['evaluar_numeros_secundarios']
        # sucursal = request.form['sucursal']
        mensaje, error = get_mensaje(-int(op))
        fecha_pasada = datetime.now() + timedelta(days=-int(op))
        creditos_una_cta_venc, error = get_creditos_una_cta_venc(fecha_pasada)
        if error == None:
            if creditos_una_cta_venc != []:
                crear_mensajes(creditos_una_cta_venc, mensaje, int(op))
                flash('Mensajes enviados', category='success')
                return render_template('aviso_atrasado.html', opv=opv)


@bp.route('/reg_mensajes')
# @permission_required('sistema')
@login_required
def reg_mensajes():
    msj_enviados = get_mensajes_WTS('+5492645139411', 1)
    msj_recibidos = get_mensajes_WTS('+5492645139411', 2)
    return render_template('reg_mensajes.html', msj_enviados=msj_enviados, msj_recibidos=msj_recibidos)







@bp.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.form
        message_body = data.get('Body', '')
        number_from = data.get('From', '').split(':')
        # mensajes_enviados = get_mensajes_WTS(number_from[1], 1)
        # mensajes_recibidos = get_mensajes_WTS(number_from[1], 0)
        # men = mensajes_recibidos + mensajes_enviados
        # max_datetime = datetime.max.replace(tzinfo=pytz.UTC)
        # mensss = sorted(men, key=lambda x: x['date_sent'] if x['date_sent'] is not None else max_datetime)
        # cli, error = get_cli_con_num(number_from[1])
        dat = {}
        dat['body'] = message_body
        dat['tel'] = number_from[1]
        reg_mensaj_chat(dat)
        # if error == None:
        #     dat = {}
        #     dat['body'] = message_body
        #     dat['tel'] = number_from[1]
        #     reg_mensaj_chat(dat)
        #     # mostrar_dialog(number_from[1], message_body)
        return redirect(url_for('bp.usuario'))





















@bp.route('/open_chat', methods=['POST'])
def open_chat():
    return render_template('chat.html')


@bp.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    mensajes, error = get_mensaj_chat()
    if error is None:
        for mensaje in mensajes:
            cliente, errorC = get_cli_con_num(mensaje.get('N_TEL'))
            if errorC is None:
                mensaje['AYN'] = cliente.get('APELLIDO') + ', ' + cliente.get('NOMBRE')
            else:
                mensaje['AYN'] = ''
            mensaje['FECHA'] = mensaje['FECHA'].isoformat()
            mensaje['HORA'] = mensaje['HORA'].isoformat()
        return jsonify(mensajes)


@bp.route('/marcar_leido', methods=['POST'])
def marcar_leido():
    if request.method == 'POST':
        id_ms = request.form.get('id_ms')
        error = update_mensaj_chat(int(id_ms))
        if error == None:
            return jsonify(True)


@bp.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    if request.method == 'POST':
        respuesta = request.form.get('respuesta')
        n_telefono = request.form.get('n_telefono')
        id_ms = request.form.get('id_ms')
    idm, status = enviarWTS(respuesta, n_telefono)
    response = {
        'respuesta': respuesta,
        'n_telefono': n_telefono,
        "id_ms": id_ms
    }
    print(response)



# @app.route('/webhook', methods=['POST'])
# @login_required
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















# opciones = {
#     'inicio': {
#         'mensaje': '¡Bienvenido! ¿Qué opción te gustaría elegir?\n'
#                '1. Opción 1\n'
#                '2. Opción 2\n'
#                '3. Salir',
#         'opciones': {
#             1: 'opción 1',
#             2: 'opción 2',
#             3: 'salir'
#         }
#     },
#     'opción 1': {
#         'mensaje': 'Has elegido la opción 1. ¿Quieres hacer algo más?',
#         'opciones': ['opción 1.1', 'opción 1.2', 'volver'],
#     },
#     'opción 1.1': {
#         'mensaje': 'Has elegido la subopción 1.1. ¿Quieres hacer algo más?',
#         'opciones': ['volver'],
#     },
#     'opción 1.2': {
#         'mensaje': 'Has elegido la subopción 1.2. ¿Quieres hacer algo más?',
#         'opciones': ['volver'],
#     },
#     'opción 2': {
#         'mensaje': 'Has elegido la opción 2. ¿Quieres hacer algo más?',
#         'opciones': ['volver'],
#     },
#     'salir': {
#         'mensaje': 'Gracias por usar nuestro servicio. ¡Hasta luego!',
#         'opciones': [],
#     },
#     'volver': {
#         'mensaje': 'Volviendo al menú anterior. ¿Qué opción te gustaría elegir?',
#         'opciones': ['opción 1', 'opción 2', 'salir'],
#     }
# }
# @bp.route('/webhook', methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         data = request.form
#         message_body = data.get('Body', '')
#         number_from = data.get('From', '')
#         response = MessagingResponse()
#         if number_from not in session:
#             session[number_from] = 'inicio'
#             response.message(opciones[session[number_from]]['mensaje'])
#         current_option = session[number_from]
#         if message_body.lower() == 'salir':
#             del session[number_from]
#             response.message('Gracias por usar nuestro servicio. ¡Hasta luego!')
#         if message_body.lower() == 'volver':
#             response.message(opciones[current_option]['mensaje'])
#             session[number_from] = 'inicio'
#         else:
#             if message_body.isdigit():
#                 if int(message_body) in opciones[current_option]['opciones']:
#                     current_option = opciones[current_option]['opciones'][int(message_body)]
#                     print(current_option)
#                     session[number_from] = current_option
#                     response.message(opciones[current_option]['mensaje'])
#                 else:
#                     response.message('Opción no válida. Por favor, elige una opción válida.')
#         return str(response)
