from db.db import get_db


def get_all_perfil():
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM PERFILES ORDER BY ID')
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def insert_perfil(name: str):
    error = None
    con, cur = get_db()
    cur.execute('SELECT MAX(ID) FROM PERFILES')
    max = cur.fetchone()
    max = cur.to_dict(max)
    indice = int(max.get('MAX')) + 1
    indice = f'{indice:05d}'
    name = name.upper()
    try:
        cur.execute("INSERT INTO PERFILES (ID, PERFIL, NCAMBIO) VALUES (?,?,?)",
                    (indice, name, 0,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando perfil: ' + str(E)}
    return error


def insert_usr_perfil(rolesAsignar: list, rolesQuitar: list, usr: str):
    error = None
    con, cur = get_db()
    for rol in rolesAsignar:
        try:
            cur.execute("INSERT INTO USR_PERFIL (IDUSR, IDPERFIL, NCAMBIO, SISTEMA) VALUES (?,?,?,?)",
                        (usr, rol['ID'], 0, 1))
            con.commit()
        except Exception as E:
            con.rollback()
            print(f"Unexpected {E=}, {type(E)=}")
            error = {'error': 'Error grabando nuevo usuario_perfil: ' + str(E)}
    for rol in rolesQuitar:
        try:
            cur.execute("DELETE FROM USR_PERFIL UP WHERE UP.IDPERFIL = ? AND UP.IDUSR = ?",
                        (rol['ID'], usr))
            con.commit()
        except Exception as E:
            con.rollback()
            print(f"Unexpected {E=}, {type(E)=}")
            error = {'error': 'Error quitando el usuario_perfil: ' + str(E)}
    return error


def delete_perfil(idPerfil):
    error = None
    con, cur = get_db()
    try:
        cur.execute("DELETE FROM PERFILES P WHERE P.ID = ?", (idPerfil,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error eliminando perfil: ' + str(E)}
    return error


def get_all_menu():
    error = None
    con, cur = get_db()
    cur.execute('SELECT M.ID, M.ID_P, M.NOMBRE, P.PERFIL FROM MENU M JOIN PERFILES P ON M.ID_P = P.ID')
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def insert_menu(name_menu, perfil):
    error = None
    con, cur = get_db()
    cur.execute('SELECT MAX(ID) FROM MENU')
    max = cur.fetchone()
    max = cur.to_dict(max)
    indice = int(max.get('MAX')) + 1
    indice = f'{indice:06d}'
    try:
        cur.execute("INSERT INTO MENU (ID, ID_P, NOMBRE) VALUES (?,?,?)",
                    (indice, perfil, name_menu,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando menu: ' + str(E)}
    return error


def delete_menu(idMenu):
    error = None
    con, cur = get_db()
    try:
        cur.execute("DELETE FROM MENU M WHERE M.ID = ?", (idMenu,))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error eliminando menu: ' + str(E)}
    return error


def get_perfil_to_menu():
    error = None
    con, cur = get_db()
    cur.execute('SELECT P.ID, P.PERFIL, M.NOMBRE FROM PERFILES P LEFT OUTER JOIN MENU M ON P.ID = M.ID_P')
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error
