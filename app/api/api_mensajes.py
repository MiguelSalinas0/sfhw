from flask import session
from app.db.db import get_db
from twilio.rest import Client
from datetime import datetime, timedelta
import re

# account_sid = 'ACea0f2392a2af488348a78569e7bc1c2d'
# auth_token = '61f760057145106269f1ca378b1ae2cd'
# twilio_phone_number = '+17853902449'

account_sid = 'AC084d9e999a6ae67e6f28471ff580f0f4'
auth_token = '024c7ffb5e04fbd032d0c06bdbb112f6'
twilio_phone_number = '+14155238886'
expresion_regular = r'^\+549\d{10}$'
client = Client(account_sid, auth_token)


def get_mensaje(op: int):
    switch = {
        3: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '-3' AND P.TIPOPROCESO = '1'",
        -3: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '3' AND P.TIPOPROCESO = '1'",
        -5: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '5' AND P.TIPOPROCESO = '1'",
        -9: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '9' AND P.TIPOPROCESO = '1'",
        -11: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '11' AND P.TIPOPROCESO = '1'",
        -31: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '31' AND P.TIPOPROCESO = '1'",
        -90: "SELECT * FROM PROCESOCOBCFG P WHERE P.DIAS = '90' AND P.TIPOPROCESO = '1'"
    }
    value = switch.get(op)
    error = None
    con, cur = get_db()
    cur.execute(value)
    rows = cur.fetchone()
    data = cur.to_dict(rows)
    con.commit()
    return data, error


def enviarWTS(mensaje: str, number: str):
    numberCom = ('whatsapp:' + number)
    message = client.messages.create(
        from_='whatsapp:' + twilio_phone_number,
        body=mensaje,
        to=numberCom
    )
    return message.sid, message.status


def enviarSMS(mensaje: str, number: str):
    numberCom = number
    message = client.messages.create(
        from_=twilio_phone_number,
        body=mensaje,
        to=numberCom
    )
    return message.sid, message.status


def get_mensajes_WTS(number: str, sentido: int):
    numberCom = ('whatsapp:' + number)
    if sentido == 1:
        messages = client.messages.list(to=numberCom)
    else:
        messages = client.messages.list(from_=numberCom)
    mensajes = []
    for message in messages:
        msDat = {}
        msDat['status'] = message.status
        msDat['body'] = message.body
        msDat['date_sent'] = message.date_sent
        msDat['sid'] = message.sid
        msDat['to'] = message.to
        mensajes.append(msDat)
    return mensajes


def get_status(number: str, sentido: int, id_msj):
    mensajes = get_mensajes_WTS(number, sentido)
    bandera = False
    indice = 0
    while bandera == False and indice < len(mensajes):
        if mensajes[indice]['sid'] == id_msj:
            bandera = True
    return mensajes[indice]['status'] if bandera else None


def registrar_mensajes(info_msj: dict):
    error = None
    con, cur = get_db()
    cur.execute('SELECT MAX(ID) FROM REG_MENSAJE_DEUDA')
    max = cur.fetchone()
    max = cur.to_dict(max)
    indice = int(max.get('MAX'))
    indice += 1
    try:
        cur.execute('INSERT INTO REG_MENSAJE_DEUDA (ID, TIPO, IDVENCIM, MENSAJE, FECHA, SUCURSAL, CLIEN, NTEL, SID, STATUS) ' +
                    'VALUES (?,?,?,?,?,?,?,?,?,?)', (str(indice),
                                                     info_msj.get('tipo'),
                                                     info_msj.get('idvencim'),
                                                     info_msj.get('mensaje'),
                                                     info_msj.get('fecha'),
                                                     info_msj.get('sucursal'),
                                                     info_msj.get('clien'),
                                                     info_msj.get('tel'),
                                                     info_msj.get('sid'),
                                                     info_msj.get('status')))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando registro de mensaje: ' + str(E)}
    return error


def update_mensajes():
    error = None
    con, cur = get_db()
    fecha = (datetime.now() + timedelta(days=-1)).strftime('%Y/%m/%d')
    cur.execute('SELECT * FROM REG_MENSAJE_DEUDA R WHERE R.FECHA = ?', (fecha,))
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    for mensaje in data:
        num_tel = str(mensaje.get('NTEL'))
        sid = str(mensaje.get('SID'))
        mensajes = get_mensajes_WTS(num_tel, 1)
        bandera = False
        indice = 0
        while bandera == False and indice < len(mensajes):
            if mensajes[indice]['sid'] == sid:
                try:
                    cur.execute('UPDATE REG_MENSAJE_DEUDA SET STATUS = ? WHERE SID = ?',
                                (mensajes[indice]['status'], sid))
                    con.commit()
                    bandera = True
                except Exception as E:
                    con.rollback()
                    print(f"Unexpected {E=}, {type(E)=}")
                    error = {'error':'Error actualizando registro de mensaje: ' + str(E)}
            else:
                indice += 1
    return error


def get_numbers(clien: str):
    error = None
    con, cur = get_db()
    cur.execute('SELECT C.CODAREA1 || C.TELEFONO1 AS tel1, C.CODAREA2 || C.TELEFONO2 AS tel2, ' +
                'C.CODAREA3 || C.TELEFONO3 AS tel3, C.CODAREA4 || C.TELEFONO4 AS tel4 ' +
                'FROM CLIENTES C WHERE C.CLIEN = ?', (clien,))
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    con.commit()
    return data, error


def guardar_mensaje(info_msj: dict, msj: str):
    if info_msj.get('tipo') == 1:
        sid, status = enviarWTS(msj, info_msj.get('tel'))
    else:
        sid, status = enviarSMS(msj, info_msj.get('tel'))
    info_msj['sid'] = sid
    info_msj['status'] = status
    registrar_mensajes(info_msj)


def crear_mensajes(creditosVencidos: list, mensaje: dict, dia: int):
    for credito in creditosVencidos:
        if credito['TELEFONO_CELULAR'] != None and credito['APENOM'] != None:
            info_msj = {}
            info_msj['tipo'] = 1
            '''asigno 1 si se le tiene que enviar wts o 0 si es sms
            info_msj['tipo'] = 1 if credito['METHOD'] == 'wts' else 0
            '''
            info_msj['idvencim'] = credito['IDVENCIM']
            info_msj['fecha'] = datetime.now().strftime('%Y/%m/%d')
            info_msj['sucursal'] = '0000'
            info_msj['clien'] = credito['CLIEN']
            info_msj['tel'] =  validar_y_convertir_numero(str(credito['TELEFONO_CELULAR']))
            if dia == 11 or dia == 31 or dia == 90:
                msj = str(mensaje['DETALLE']).replace('%apellido+nombre%', str(credito['APENOM']).strip()).replace('%vto%', str(credito['VTO'].strftime('%d/%m/%Y')))
            else:
                nuevoVencimiento = credito['VTO'] + timedelta(days=10)
                msj = str(mensaje['DETALLE']).replace('%apellido+nombre%', str(credito['APENOM']).strip()).replace('%vto+10%', str(nuevoVencimiento.strftime('%d/%m/%Y')))
            if re.match(expresion_regular, info_msj.get('tel')):
                info_msj['mensaje'] = f'Aviso de vencimiento de cuota, {dia} días vencido'
                guardar_mensaje(info_msj, msj)
            elif info_msj.get('tel') == '':
                info_msj['mensaje'] = 'Cliente sin número de teléfono'
                registrar_mensajes(info_msj)
            else:
                info_msj['mensaje'] = 'Número de teléfono mal formado'
                registrar_mensajes(info_msj)
            '''
            if evaluar_numeros_secundarios:
                data, error = get_numbers(credito['CLIEN'])
                if error == None:
                    for clave, valor in data[0].items():
                        num = valor.replace(' ', '')
                        if num != '':
                                if re.match(expresion_regular, num):
                                    info_msj['mensaje'] = f'Aviso de vencimiento de cuota, {dia} días vencido'
                                    info_msj['tel'] = num
                                    guardar_mensaje(info_msj, msj)
                                else:
                                    info_msj['mensaje'] = 'Número de teléfono mal formado'
                                    info_msj['tel'] = num
                                    registrar_mensajes(info_msj)
            '''


def validar_y_convertir_numero(numero: str):
    numero = numero.replace(" ", "")
    if re.match(r'^\d{9,11}$', numero):
        # Quitar el "0" inicial si está presente
        if numero.startswith('0'):
            numero = numero[1:]
        # Añadir "+549" al principio si no está presente
        if not numero.startswith('+549'):
            numero = '+549' + numero
    return numero


def contar_mensajes(clien: str):
    con, cur = get_db()
    cur.execute('SELECT COUNT(*) AS cantidad_mensajes FROM REG_MENSAJE_DEUDA r WHERE r.CLIEN = ?', (clien,))
    row = cur.fetchone()
    cant = cur.to_dict(row)
    con.commit()
    return cant


def mensajes_status(op: int, clien = ''):
    con, cur = get_db()
    if op == 0:
        fecha = (datetime.now() + timedelta(days=-13)).strftime('%Y/%m/%d')
        cur.execute('SELECT * FROM REG_MENSAJE_DEUDA R WHERE R.FECHA = ?', (fecha,))
    else:
        cur.execute('SELECT * FROM REG_MENSAJE_DEUDA R WHERE R.CLIEN = ?', (clien,))
    rows = cur.fetchall()
    data = []
    queued = []
    failed = []
    sent = []
    delivered = []
    read = []
    for row in rows:
        data.append(cur.to_dict(row))
    for mensaje in data:
        stat = str(mensaje.get('STATUS')).lower()
        if stat == 'queued':
            queued.append(mensaje)
        if stat == 'failed':
            failed.append(mensaje)
        if stat == 'sent':
            sent.append(mensaje)
        if stat == 'delivered':
            delivered.append(mensaje)
        if stat == 'read':
            read.append(mensaje)
    status = {
        'queued': queued,
        'failed': failed,
        'sent': sent,
        'delivered': delivered,
        'read': read
    }
    return status









def reg_mensaj_chat(datos: dict):
    error = None
    con, cur = get_db()
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()
    try:
        cur.execute('INSERT INTO MENSAJES_CHAT (BODY, N_TEL, FECHA, HORA) ' +
                    'VALUES (?,?,?,?)', (datos.get('body'),
                                         datos.get('tel'),
                                         fecha_actual,
                                         hora_actual,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando registro de mensaje: ' + str(E)}
    return error


def get_mensaj_chat():
    error = None
    con, cur = get_db()
    data = []
    try:
        cur.execute('SELECT * FROM MENSAJES_CHAT ms WHERE ms.LEIDO = 0')
        rows = cur.fetchall()
        for row in rows:
            data.append(cur.to_dict(row))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando registro de mensaje: ' + str(E)}
    return data, error


def update_mensaj_chat(id: int):
    error = None
    con, cur = get_db()
    try:
        cur.execute('UPDATE MENSAJES_CHAT ms SET ms.LEIDO = 1 WHERE ms.ID = ?', (id,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando registro de mensaje: ' + str(E)}
    return error


def get_one_mensaj(id: int):
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM MENSAJES_CHAT ms WHERE ms.ID = ?', (id,))
    row = cur.fetchone()
    if row == None:
        error = {'error': f'No hay datos de mensaje para ID: {id}'}
        return {}, error
    return cur.to_dict(row), error






def metodo_opcion1():
    return 'metodo ejecutado'

