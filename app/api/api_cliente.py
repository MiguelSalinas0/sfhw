import requests
from flask import session
from db.db import get_db

def get_provincias():
    error = None
    con, cur = get_db()
    cur.execute("SELECT codprov, nombre FROM PROVINCIAS")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error
    

def get_tipodoc():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0001'")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error

def get_tipocontrib():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0004'")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error

def get_estadocivil():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0003'")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    
    return data, error

def get_localidades():
    error = None
    con, cur = get_db()
    cur.execute("select codloc, nombre, cpostal from localidades where INHA = 0")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    
    return data, error

def get_viviendas():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0018'")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    
    return data, error

def get_actividades():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0017'")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    
    return data, error

def get_categorias():
    error = None
    con, cur = get_db()
    cur.execute("select CATEGO, NOMBRE from categorias where INHA = 0")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    
    return data, error

def get_sucursales():
    error = None
    con, cur = get_db()
    cur.execute("select SUCURSAL, NOMBRE from sucursal where INHA = 0")
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    
    return data, error

def get_cliente(dni: str):
    error = None
    con, cur = get_db()
    cur.execute("SELECT CLIEN, NODO, RUTA, CATEGO, NOMBRE, APELLIDO, CTRIB, TDOC, DNI, CUIL, " +
                "DOMICILIO1, DOMICILIO2, CODLOC, CALLE1, CALLE2, LATITUD, LONGITUD, CODAREA, " +
                "TELEFONO, CODAREA1, TELEFONO1, NTELEFONO1, CODAREA2, TELEFONO2, NTELEFONO2, " +
                "CODAREA3, TELEFONO3, NTELEFONO3, CODAREA4, TELEFONO4, NTELEFONO4, FNACIM, " +
                "SEXO, ESTADOCIV, VIVIENDA, ACTIVIDAD, REQGAR, OPCTE, DIASCTE, OPCRE, " +
                "INGRESOS, INGRESOS_O, OBSINGR, CREDITO, ADICIONAL1, ADICIONAL2, ADICIONAL3, " +
                "TRABAJO, CARGO, FINGRESO, DOMTRA1, DOMTRA2, LOCTRA, CPOSTRA, CODPROVTRA, " +
                "CODAREAT1, TELTRA1, FDOCUM, ESTADOCTE, EMAIL, OBS, TLISTAPRE, LISTAPRE, " +
                "INHA, N_USU_A, F_USU_A, N_USU_M, F_USU_M, NODODAT, NUSUARIO, FUSUARIO, " +
                "NODO_ULT, ICAMBIO_ULT, ICAMBIO, NCAMBIO from clientes where DNI = ?", (dni,))
    row = cur.fetchone()
    return cur.to_dict(row), error


def get_articulo(idArt: str = "0"):
    error = None
    idArt = idArt.zfill(8)
    con, cur = get_db()
    cur.execute("select A.CODIGO, A.NOMBRE, P.PLISTA, P.PREC1, P.PREC2, P.PREC3 " +
                "from articulos A " +
                "left join precios P on P.CODIGO = A.CODIGO and P.IDPRECIO = 0 " +
                "where " + 
                "A.CODIGO = ?", (idArt,))
    row = cur.fetchone()
    if row == None:
        error = '{"error":"No existe el artículo"}'
        return {}, error
    return cur.to_dict(row), error

def get_creditos(estado: int = 0):
    error = None
    con, cur = get_db()
    cur.execute("select C.ID, C.IDCLIENTE, (TRIM(CL.NOMBRE) || ''', ''' || TRIM(CL.APELLIDO)) NOMCLI, C.FECHA, C.IDSUCURSAL, S.NOMBRE as SUCURSAL, C.IDVENDEDOR, C.TOTAL " +
                "from creditos C " +
                "join clientes CL " +
                "  on CL.CLIEN = C.IDCLIENTE " +
                "left join sucursal S on S.SUCURSAL = C.IDSUCURSAL " +
                "where ESTADO = ?", (estado,))
    rows =cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error