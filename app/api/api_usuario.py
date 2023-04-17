import hashlib
from db.db import get_db


def get_usuario(usuario: str, clave: str):
    error = None
    con, cur = get_db()
    cur.execute('select * from usuario where NOMBRE_USR = ?', (usuario,))
    usuario = cur.fetchone()
    if usuario == None:
        error = {'error': 'usuario o contraseña inválida'}
        con.commit()
        return {}, error
    else:
        usuario = cur.to_dict(usuario)
        result = hashlib.sha384(bytes(clave, encoding='utf-8'))
        if result.hexdigest() == usuario.get('PASSWORD'):
            con.commit()
            return {'USUARIO': usuario.get('USUARIO'), 'NOMBRE': usuario.get('NOMBRE')}, error
        else:
            error = {'error': 'usuario o contraseña inválida'}
            con.commit()
            return {}, error


def get_user(iduser: str):
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM USUARIO WHERE USUARIO.USUARIO = ?', (iduser,))
    user = cur.fetchone()
    if user == None:
        user = {}
        error = {'error': 'usuario no encontrado'}
    else:
        user = cur.to_dict(user)
    con.commit()
    return user, error


def insert_usuario(user_info: dict):
    clave = hashlib.sha384(bytes(user_info.get('clave'), encoding='utf-8'))
    user_info['clave'] = clave.hexdigest()
    error = None
    con, cur = get_db()
    cur.execute('SELECT MAX(USUARIO) FROM USUARIO')
    max = cur.fetchone()
    max = cur.to_dict(max)
    indice = int(max.get('MAX')) + 1
    indi = f'{indice:06d}'
    try:
        cur.execute('INSERT INTO USUARIO (USUARIO, NOMBRE, SUCURSAL, CATEGORIA, TDOC, DNI, CARGO, DOMICILIO1, ' +
                    'DOMICILIO2, LOCALIDAD, CODPROV, CPOSTAL, TELEFONO, CODAREA, CODAREA1, TELEFONO1, EMAIL, OBS, "PASSWORD", INHA, N_USU_A, N_USU_M, NOMBRE_USR)' + 
                    'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (indi,
                                                                                user_info.get('nombre'),
                                                                                user_info.get('sucursal'),
                                                                                user_info.get('catego'),
                                                                                user_info.get('tipodoc'),
                                                                                user_info.get('dni'),
                                                                                user_info.get('cargo'),
                                                                                user_info.get('domicilio1'),
                                                                                user_info.get('domicilio2'),
                                                                                user_info.get('localidad'),
                                                                                user_info.get('provincia'),
                                                                                user_info.get('cpostal'),
                                                                                user_info.get('telefono'),
                                                                                user_info.get('codarea'),
                                                                                user_info.get('codarea1'),
                                                                                user_info.get('telefono1'),
                                                                                user_info.get('email'),
                                                                                user_info.get('obs'),
                                                                                user_info.get('clave'),
                                                                                0,
                                                                                0,
                                                                                0,
                                                                                user_info.get('user_name')))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error':'Error grabando usuario: ' + str(E)}
    return error


def update_user(user_info: dict, id_user):
    error = None
    con, cur = get_db()
    cur.execute('SELECT PASSWORD FROM USUARIO WHERE USUARIO = ?', (id_user,))
    clave = cur.fetchone()
    clave = cur.to_dict(clave)
    if user_info.get('clave') == '':
        user_info['clave'] = clave.get('PASSWORD')
    elif clave.get('PASSWORD') == hashlib.sha384(bytes(user_info.get('clave'), encoding='utf-8')).hexdigest():
        user_info['clave'] = clave.get('PASSWORD')
    else:
        user_info['clave'] = hashlib.sha384(bytes(user_info.get('clave'), encoding='utf-8')).hexdigest()
    try:
        cur.execute('UPDATE USUARIO SET NOMBRE = ?, SUCURSAL = ?, CATEGORIA = ?, TDOC = ?, DNI = ?, CARGO = ?, ' +
                    'DOMICILIO1 = ?, DOMICILIO2 = ?, LOCALIDAD = ?, CODPROV = ?, CPOSTAL = ?, TELEFONO = ?, CODAREA = ?, CODAREA1 = ?, TELEFONO1 = ?, EMAIL = ?, OBS = ?,' + 
                    '"PASSWORD" = ?, INHA = ?, N_USU_A = ?, N_USU_M = ?, NOMBRE_USR = ?' +
                    'WHERE USUARIO = ?',(user_info.get('nombre'),
                                        user_info.get('sucursal'),
                                        user_info.get('catego'),
                                        user_info.get('tipodoc'),
                                        user_info.get('dni'),
                                        user_info.get('cargo'),
                                        user_info.get('domicilio1'),
                                        user_info.get('domicilio2'),
                                        user_info.get('localidad'),
                                        user_info.get('provincia'),
                                        user_info.get('cpostal'),
                                        user_info.get('telefono'),
                                        user_info.get('codarea'),
                                        user_info.get('codarea1'),
                                        user_info.get('telefono1'),
                                        user_info.get('email'),
                                        user_info.get('obs'),
                                        user_info.get('clave'),
                                        0,
                                        0,
                                        0,
                                        user_info.get('user_name'),
                                        id_user))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error':'Error actualizando usuario: ' + str(E)}
    return error


def drop_user(id_user):
    error = None
    con, cur = get_db()
    try:
        cur.execute("UPDATE USUARIO SET INHA = 1 WHERE USUARIO = ?", (id_user,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error':'Error eliminando usuario: ' + str(E)}
    return error