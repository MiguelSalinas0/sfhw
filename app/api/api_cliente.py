from app.db.db import get_db


def get_provincias():
    error = None
    con, cur = get_db()
    cur.execute("SELECT codprov, nombre FROM PROVINCIAS")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_tipodoc():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0001'")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_tipocontrib():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0004'")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_estadocivil():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0003'")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_localidades():
    error = None
    con, cur = get_db()
    cur.execute("select codloc, nombre, cpostal from localidades where INHA = 0")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_viviendas():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0018'")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_actividades():
    error = None
    con, cur = get_db()
    cur.execute("select idtipo, nombre from tipos where TIPO = '0017'")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_categorias():
    error = None
    con, cur = get_db()
    cur.execute("select CATEGO, NOMBRE from categorias where INHA = 0")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_sucursales():
    error = None
    con, cur = get_db()
    cur.execute("select SUCURSAL, NOMBRE from sucursal where INHA = 0")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(cur.to_dict(row))
    return data, error


def get_cliente(dni: str):
    error = None
    con, cur = get_db()
    cur.execute("SELECT CLIEN, NODO, RUTA, CATEGO, Trim(NOMBRE) NOMBRE, Trim(APELLIDO) APELLIDO, CTRIB, TDOC, Trim(DNI) DNI, CUIL, " +
                "Trim(DOMICILIO1) DOMICILIO1, Trim(DOMICILIO2) DOMICILIO2, CODLOC, Trim(CALLE1) CALLE1, Trim(CALLE2) CALLE2, LATITUD, LONGITUD, CODAREA, " +
                "Trim(CODAREA) CODAREA, Trim(TELEFONO) TELEFONO, Trim(CODAREA1) CODAREA1, Trim(TELEFONO1) TELEFONO1, NTELEFONO1, CODAREA2, TELEFONO2, NTELEFONO2, " +
                "CODAREA3, TELEFONO3, NTELEFONO3, CODAREA4, TELEFONO4, NTELEFONO4, FNACIM, " +
                "SEXO, ESTADOCIV, VIVIENDA, ACTIVIDAD, REQGAR, OPCTE, DIASCTE, OPCRE, " +
                "INGRESOS, INGRESOS_O, OBSINGR, CREDITO, ADICIONAL1, ADICIONAL2, ADICIONAL3, " +
                "Trim(TRABAJO) TRABAJO, Trim(CARGO) CARGO, FINGRESO, Trim(DOMTRA1) DOMTRA1, Trim(DOMTRA2) DOMTRA2, Trim(LOCTRA) LOCTRA, Trim(CPOSTRA) CPOSTRA, CODPROVTRA, " +
                "CODAREAT1, TELTRA1, FDOCUM, ESTADOCTE, EMAIL, OBS, TLISTAPRE, LISTAPRE, " +
                "INHA, N_USU_A, F_USU_A, N_USU_M, F_USU_M, NODODAT, NUSUARIO, FUSUARIO, " +
                "NODO_ULT, ICAMBIO_ULT, ICAMBIO, NCAMBIO from clientes where DNI = ?", (dni,))
    row = cur.fetchone()
    if row == None:
        error = {'error': f'No hay datos de cliente para DNI: {dni}'}
        return {}, error
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


def insert_cliente(datosCliente):
    error = None
    return datosCliente, error


def update_cliente(datosCliente):
    error = None
    print('categoria')
    print(datosCliente['catego'])
    con, cur = get_db()
    try:
        print(datosCliente)
        cur.execute("update clientes set CATEGO=?, NOMBRE=?, APELLIDO=?, CTRIB=?, TDOC=?, DNI=?, DOMICILIO1=?, DOMICILIO2=?, " +
                    "CODLOC=?, CODAREA=?, TELEFONO=?, CODAREA1=?, TELEFONO1=?, CALLE1=?, CALLE2=?, ESTADOCIV=?, EMAIL=?, VIVIENDA=?, " +
                    "ACTIVIDAD=?, SEXO=?, FNACIM=?, OBS=?, TRABAJO=?, CARGO=?, DOMTRA1=?, DOMTRA2=?, LOCTRA=?, CPOSTRA=?, INGRESOS=?, " +
                    "INGRESOS_O=? " +
                    "where clien=?",
                    (datosCliente['catego'], datosCliente['nombre'], datosCliente['apellido'], datosCliente['ctrib'],
                     datosCliente['tdoc'], datosCliente['dni'], datosCliente['domicilio1'], datosCliente['domicilio2'], datosCliente['codloc'],
                     datosCliente['codarea'], datosCliente['telefono'], datosCliente['codarea1'], datosCliente['telefono1'], datosCliente['calle1'],
                     datosCliente['calle2'], datosCliente['estadociv'], datosCliente['email'], datosCliente['vivienda'], datosCliente['actividad'],
                     datosCliente['sexo'], datosCliente['fnacim'], datosCliente['obs'], datosCliente['trabajo'], datosCliente['cargo'], 
                     datosCliente['domtra1'], datosCliente['domtra2'], datosCliente['loctra'], datosCliente['cpostra'], datosCliente['ingresos'],
                     datosCliente['ingresos_o'], datosCliente['clien']))
        con.commit()
    except Exception as E:
        con.rollback()
        error = {'error':'Error actualizando cliente: ' + str(E)}    
    return datosCliente, error


def get_cli_con_num(numero: str):
    codigo_area = f"%{numero[4:7]}%"
    numero = numero[7:]
    error = None
    con, cur = get_db()
    cur.execute("SELECT * FROM CLIENTES c WHERE (TRIM(c.CODAREA) LIKE ? and TRIM(c.TELEFONO) = ?)", (codigo_area, numero,))
    row = cur.fetchone()
    if row == None:
        error = {'error': f'No hay datos de cliente para el número: {numero}'}
        return {}, error
    return cur.to_dict(row), error