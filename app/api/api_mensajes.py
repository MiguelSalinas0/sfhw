from flask import session
from db.db import get_db
from twilio.rest import Client
from datetime import datetime, timedelta


account_sid = 'AC084d9e999a6ae67e6f28471ff580f0f4'
auth_token = '9ea6a34dd7209eea0bb6e636246876c3'
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
    return data, error


def get_creditos_a_vencer(fecha_futura):
    error = None
    con, cur = get_db()
    cur.callproc('GET_CUOTA_AVENCER', [fecha_futura, fecha_futura, '0000'])
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_creditos_vencidos(fecha_pasada):
    error = None
    con, cur = get_db()
    cur.callproc('GET_CUOTA_VENCIDA', [fecha_pasada, fecha_pasada, '0000', 'N'])
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def enviarWTS(mensaje: str, number: str):
    numberCom = ('whatsapp:' + number).replace(' ', '')
    message = client.messages.create(
        body=mensaje,
        from_='whatsapp:+14155238886',
        to=numberCom
    )
    return message.sid, message.status


def enviarSMS(mensaje: str, number: str):
    numberCom = number.replace(' ', '')
    message = client.messages.create(
        from_='+16203494263',
        body=mensaje,
        to=numberCom
    )
    return message.sid, message.status


def get_mensajes_WTS(number: str, sentido: int):
    numberCom = ('whatsapp:' + number).replace(' ', '')
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
        mensajes.append(msDat)
    mensajes_ordenados = sorted(mensajes, key=lambda mensaje: mensaje['date_sent'], reverse=True)
    return mensajes_ordenados


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
                except Exception as E:
                    con.rollback()
                    print(f"Unexpected {E=}, {type(E)=}")
                    error = {'error':'Error actualizando registro de mensaje: ' + str(E)}
                bandera = True
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
            if credito['METHOD'] == 'wts': 
                info_msj['tipo'] = 1
            else:
                info_msj['tipo'] = 0
            '''
            info_msj['idvencim'] = credito['IDVENCIM']
            info_msj['mensaje'] = f'Aviso de vencimiento de cuota, {dia} días vencido'
            info_msj['fecha'] = datetime.now().strftime('%Y/%m/%d')
            info_msj['sucursal'] = '0000'
            info_msj['clien'] = credito['CLIEN']
            info_msj['tel'] =  str(credito['TELEFONO_CELULAR'])
            if dia == 11 or dia == 31 or dia == 90:
                mensaje = str(mensaje['DETALLE']).replace('%apellido+nombre%', str(credito['APENOM']).strip()).replace('%vto%', str(credito['VTO'].strftime('%d/%m/%Y')))
            else:
                nuevoVencimiento = credito['VTO'] + timedelta(days=10)
                mensaje = str(mensaje['DETALLE']).replace('%apellido+nombre%', str(credito['APENOM']).strip()).replace('%vto+10%', str(nuevoVencimiento.strftime('%d/%m/%Y')))
            guardar_mensaje(info_msj, mensaje)
            data, error = get_numbers(credito['CLIEN'])
            if error == None:
                for clave, valor in data[0].items():
                    if valor.replace(' ', '') != '':
                        info_msj['tel'] = valor
                        guardar_mensaje(info_msj, mensaje)
